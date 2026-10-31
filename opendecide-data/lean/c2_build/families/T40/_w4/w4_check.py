"""T40 A45 (d) pre-freeze check, IN MEMORY (no row is written): build N rows, G6 pooled + per head, G7, G10, probes, reseed audit.
  ../../../../.venv/bin/python -B families/T40/_prefreeze/prefreeze_check.py --n 7000 --out families/T40/_prefreeze/result.json  (from lean/c2_build)
Only aggregate numbers are written."""
from __future__ import annotations
import argparse, json, sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(C2)); sys.path.insert(0, str(C2 / "families" / "T40"))
import pilot, pilot_loaders as PL
from families.T40 import loader, plugin as TP
from families.T40 import test_t40 as TT
from c2_kit import rows as R
from families.T40 import edit as E
import numpy as np

def maj(ys):
    c = collections.Counter(ys); return max(c.values()) / len(ys)

def head(i): return i.spec.structure["head"]

def probe_fmt(infos, feats, ys):
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.model_selection import GroupKFold
    X = np.array([feats(i) for i in infos], float); y = np.array(ys)
    g = np.array([i.row["meta"]["card_id"] for i in infos]); pred = np.zeros(len(y), dtype=y.dtype)
    for tr, te in GroupKFold(n_splits=5).split(X, y, g):
        pred[te] = HistGradientBoostingClassifier(max_iter=100, random_state=0).fit(X[tr], y[tr]).predict(X[te])
    return round(float((pred == y).mean()), 4)

def fmt(i):
    r = i.row; s = r["state"]
    return [len(s), s.count("\n"), s.count("["), s.count("("), s.count("*"), s.count('"'), len(r["instructions"]),
            len(r["card"] or ""), len(r["meta"]["c2"]["register"]), len(r["question"]) if "question" in r else len(i.question)]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=7000); ap.add_argument("--out"); a = ap.parse_args()
    loader.register(); out = {}
    with PL.open_family("T40") as kit:
        b = pilot.build_pilot(kit, a.n, run_g15=False, log=lambda m: print(m, file=sys.stderr, flush=True))
        infos = b.infos
        out["rows"] = len(infos); out["by_head"] = dict(collections.Counter(head(i) for i in infos))
        out["by_head_qtype"] = {f"{h}/{q}": c for (h, q), c in collections.Counter((head(i), i.row["qtype"]) for i in infos).items()}
        out["build_drops"] = b.stats["drops_by_gate"]
        gates = pilot.program_gates(b)
        out["program_gates"] = {k: g["verdict"] for k, g in gates.items() if k in pilot.PROGRAM_GATES}
        def g6s(sub):
            r = pilot.g6(sub)
            return {"verdict": r["verdict"], "fails": r["fails"], "yes_no": r["yes_no"], "choice": r["choice"]}
        out["g6_pooled"] = g6s(infos)
        out["g6_head"] = {h: g6s([i for i in infos if head(i) == h]) for h in "ABC"}
        def prefix(k):
            tot, sub = 0, []
            for i in infos:
                if tot >= k: break
                sub.append(i); tot += 1
            return sub
        for k in (6000, 1333):                      # W4: the same seeds at smaller sizes (a fixed leak must not grow with data)
            sub = prefix(k)
            out[f"prefix_{k}"] = {"rows": len(sub), "by_head_qtype": {f"{h}/{q}": c for (h, q), c in collections.Counter((head(i), i.row["qtype"]) for i in sub).items()},
                                  "max_rows_per_card": max(collections.Counter(i.row["meta"]["card_id"] for i in sub).values())}
            if k >= 5000:
                out[f"prefix_{k}"]["g6_head"] = {h: g6s([i for i in sub if head(i) == h]) for h in "ABC"}
                out[f"prefix_{k}"]["g6_pooled"] = g6s(sub)
        out["g7"] = {"verdict": (g7 := pilot.g7(infos))["verdict"]}
        g10 = pilot.g10(infos, b.units, kit.plugin); out["g10"] = {"verdict": g10["verdict"], "failing": g10.get("failing")}
        # probes
        pr = {}
        for h in ["ALL", "A", "B", "C"]:
            sub = [i for i in infos if h == "ALL" or head(i) == h]
            yn = [i for i in sub if i.row["qtype"] == "noul"]; ch = [i for i in sub if i.row["qtype"] == "choice"]
            e = {}
            if len(yn) >= 100:
                ys = [int(i.row["gold"]) for i in yn]; e["fmt_yn"] = {"acc": probe_fmt(yn, fmt, ys), "chance": round(maj(ys), 4), "n": len(yn)}
            if len(ch) >= 100:
                ys = [str(i.row["gold"]) for i in ch]
                lab = [kit.plugin.label(i.spec) for i in ch]
                e["fmt_choice_label"] = {"acc": probe_fmt(ch, fmt, lab), "chance": round(maj(lab), 4), "n": len(ch)}
            if h == "C" and len(ch) >= 100:
                def dsz(i):
                    st, env = i.spec.structure, i.spec.env()
                    o = E.render_tokens(st["old"], "O", env); n = E.render_tokens(st["new"], "N", env)
                    return [len(o), len(n), len(n) - len(o), o.count("\n"), n.count("\n"), sum(c.isdigit() for c in n) - sum(c.isdigit() for c in o)]
                lab = [kit.plugin.label(i.spec) for i in ch]
                e["diff_choice_label"] = {"acc": probe_fmt(ch, dsz, lab), "chance": round(maj(lab), 4), "n": len(ch)}
            pr[h] = e
        out["probes"] = pr
        # reseed audit
        plug = TP.T40Plugin(lexicon=kit.ctx.lexicon); plug.RNG_SALT = "|audit"
        specs = [i.spec for i in infos if i.row["role"] == "base"]
        pick = specs[:: max(1, int(len(specs) / (0.03 * len(infos))))]; flips = 0
        for sp in pick:
            c = TP.design(sp.seed, sp.sampler); sp2 = plug.sample(sp.seed, sp.sampler)
            flips += plug.label(sp2) != c["label"] or sp2.qform != sp.qform
            rr = plug.render(sp2, kit.ctx); view = plug.parse(rr.row, kit.ctx)
            flips += plug.solve_b(view) != plug.solve_a(sp2)
        out["reseed"] = {"audited": len(pick), "flips": int(flips)}
        toks = [R.approx_tokens(i.row) for i in infos]
        out["tokens"] = {"mean": round(sum(toks) / len(toks), 1), "max": max(toks)}
        cards = collections.Counter(i.row["meta"]["card_id"] for i in infos); out["max_rows_per_card"] = max(cards.values())
    s = json.dumps(out, indent=1, default=str)
    if a.out: Path(a.out).write_text(s)
    print(s[:6000])
main()
