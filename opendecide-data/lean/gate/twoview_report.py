"""REPORT ONLY (never decisive, no look): the exact 2-view readout of the new 4Bs on the 9 gate splits, from gate job 3's
identity + exact-reversal reads. It closes prep89/READOUT_DEV.md's caveat that the main run's 2-view numbers were a
proxy (identity + one seeded random view, "2v_perm"): here the 2-view read is od_gcp predict --tta (choice rows:
given order + exact reversal; yes/no rows: given letters + swapped letters; averaged in probability space, as
decoder_io.predict does), and a second, independent 2-view read (--perm-seed 1 --tta: the seeded view + ITS reversal)
measures the 2-view drift, which READOUT_DEV could not measure for the main run (it needs two independent 2-views).

  python gate/twoview_report.py --model LABEL:STD:TTA:PERM:PERM_TTA [--model ...] [--json OUT]
     e.g. C1R:q35_4b_main500k_r3:q35_4b_main500k_r3_tta:q35_4b_main500k_r3_perm:q35_4b_main500k_r3_perm_tta
          C4:q35_4b_main500k_fix2:q35_4b_main500k_fix2_tta:q35_4b_main500k_fix2_perm:q35_4b_main500k_fix2_perm_tta

Per model (rows of the 9 splits; gate_dev.score: ties count as wrong):
  accuracy   1-view, 2-view exact, and the A5 (a) served readout (choice rows 2-view, yes/no rows 1-view), each with
             the paired bootstrap of its difference to the 1-view (group_id units, 10,000 resamples, seed 0)
  drift      choice rows: 1-view flips (identity vs the seeded view) and 2-view flips (identity+reversal vs seeded+its
             reversal), all rows and rows with >= 10 options
  (e)        equivalence flips on the 722 pairs and on the 662 non-hate pairs under 1-view, 2-view and A5 (a)
  Brier      yes/no Brier (uncalibrated) 1-view vs 2-view
Every read must be complete; the TTA flags of each read's meta are checked (tta reads: tta on; others: off).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

LEAN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEAN))
import gate_dev as gd  # noqa: E402

SPLITS9 = gd.SPLITS.split(",")
HATE = {"hate"}


def stop(msg):
    sys.exit(f"twoview_report: {msg}")


def read_jsonl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def load_read(name, want_tta):
    out = {}
    for sp in SPLITS9:
        P = gd.load(sp, name)
        if P is None:
            stop(f"preds_{sp}/{name}.jsonl missing")
        m = gd.read_meta(f"preds_{sp}", name) or {}
        tta = bool(m.get("tta") or m.get("tta_choice") or m.get("tta_noul"))
        if tta != want_tta:
            stop(f"preds_{sp}/{name}: TTA {'off' if want_tta else 'on'} in its meta, expected {'on' if want_tta else 'off'}")
        out[sp] = P
    return out


def avg_view(p1, p2):
    return {k: 0.5 * (float(p1.get(k, 0.0)) + float(p2.get(k, 0.0))) for k in set(p1) | set(p2)}


def boot(units, xs, ys, seed=gd.SEED, boots=gd.BOOTS):
    by = defaultdict(lambda: [0.0, 0.0, 0])
    for u, x, y in zip(units, xs, ys):
        g = by[u]
        g[0] += x
        g[1] += y
        g[2] += 1
    G = np.array(list(by.values()))
    rng = np.random.default_rng(seed)
    bs = np.empty(boots)
    for k in range(boots):
        s = G[rng.integers(0, len(G), len(G))]
        bs[k] = (s[:, 0].sum() - s[:, 1].sum()) / s[:, 2].sum() * 100
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return round(float(lo), 2), round(float(hi), 2)


def model_report(label, std, tta, perm, ptta):
    S, T, Q, QT = load_read(std, False), load_read(tta, True), load_read(perm, False), load_read(ptta, True)
    rows, ok1, ok2, oka, units = [], [], [], [], []
    br1, br2 = [], []
    d1 = {"all": [0, 0], "ge10": [0, 0]}
    d2 = {"all": [0, 0], "ge10": [0, 0]}
    view = {}
    for sp in SPLITS9:
        for r in read_jsonl(gd.ROOT / f"data/{sp}.jsonl"):
            ps, pt = S[sp].get(r["id"]), T[sp].get(r["id"])
            pq, pqt = Q[sp].get(r["id"]), QT[sp].get(r["id"])
            if None in (ps, pt, pq, pqt):
                stop(f"{label}: a read lacks {sp}/{r['id']}")
            pa = pt if r["qtype"] == "choice" else ps
            view[(sp, r["id"])] = {"1v": ps, "2v": pt, "a5": pa}
            rows.append(r)
            units.append(f"{sp}|{r.get('group_id') or r['id']}")
            ok1.append(gd.score(r, ps)[0])
            ok2.append(gd.score(r, pt)[0])
            oka.append(gd.score(r, pa)[0])
            if r["qtype"] == "noul":
                br1.append(gd.score(r, ps)[1])
                br2.append(gd.score(r, pt)[1])
            else:
                for key in ("all",) + (("ge10",) if len(r["options"]) >= 10 else ()):
                    d1[key][0] += gd.argmax_label(r, ps) != gd.argmax_label(r, pq)
                    d1[key][1] += 1
                    d2[key][0] += gd.argmax_label(r, pt) != gd.argmax_label(r, pqt)
                    d2[key][1] += 1
    n = len(rows)
    acc = lambda xs: round(100 * sum(xs) / n, 2)  # noqa: E731
    ch = [i for i, r in enumerate(rows) if r["qtype"] == "choice"]
    yn = [i for i, r in enumerate(rows) if r["qtype"] == "noul"]
    sub = lambda xs, ix: round(100 * sum(xs[i] for i in ix) / max(1, len(ix)), 2)  # noqa: E731
    eq = {}
    for vname in ("1v", "2v", "a5"):
        k_all = k_nh = n_all = n_nh = 0
        for sp in SPLITS9:
            p = gd.ROOT / f"data/{sp}_relations.jsonl"
            if not p.exists():
                continue
            rr = {r["id"]: r for r in read_jsonl(gd.ROOT / f"data/{sp}.jsonl")}
            for rel in read_jsonl(p):
                x, y = rr.get(rel["a"]), rr.get(rel["b"])
                if rel["type"] != "equiv" or x is None or y is None or x["qtype"] != y["qtype"]:
                    continue
                f = gd.argmax_label(x, view[(sp, x["id"])][vname]) != gd.argmax_label(y, view[(sp, y["id"])][vname])
                n_all += 1
                k_all += f
                if not ({x["source"], y["source"]} & HATE):
                    n_nh += 1
                    k_nh += f
        eq[vname] = {"all": f"{k_all}/{n_all} = {100 * k_all / max(1, n_all):.2f}%",
                     "non_hate": f"{k_nh}/{n_nh} = {100 * k_nh / max(1, n_nh):.2f}%"}
    rate = lambda d: {k: f"{v[0]}/{v[1]} = {100 * v[0] / max(1, v[1]):.2f}%" for k, v in d.items()}  # noqa: E731
    return {"label": label, "reads": {"1v": std, "2v": tta, "perm1": perm, "perm1_2v": ptta}, "rows": n,
            "accuracy": {"1v": acc(ok1), "2v_exact": acc(ok2), "a5_served": acc(oka),
                         "2v_minus_1v": [round(acc(ok2) - acc(ok1), 2), boot(units, ok2, ok1)],
                         "a5_minus_1v": [round(acc(oka) - acc(ok1), 2), boot(units, oka, ok1)],
                         "choice": {"1v": sub(ok1, ch), "2v": sub(ok2, ch), "n": len(ch)},
                         "yes_no": {"1v": sub(ok1, yn), "2v": sub(ok2, yn), "n": len(yn)}},
            "choice_drift": {"1v_identity_vs_seeded": rate(d1), "2v_vs_independent_2v": rate(d2)},
            "equiv_flips": eq,
            "yes_no_brier": {"1v": round(float(np.mean(br1)), 4), "2v": round(float(np.mean(br2)), 4)}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", action="append", required=True, help="LABEL:STD:TTA:PERM:PERM_TTA")
    ap.add_argument("--json", default=None)
    ap.add_argument("--root", default=None, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    if a.root:
        gd.ROOT = Path(a.root).resolve()
    out = {"report_only": True, "never_decisive": "no look, no rule; A8-prime section E (report reads)", "models": []}
    for spec in a.model:
        parts = spec.split(":")
        if len(parts) != 5:
            stop(f"--model {spec!r}: need LABEL:STD:TTA:PERM:PERM_TTA")
        r = model_report(*parts)
        out["models"].append(r)
        print(f"== {r['label']} ({r['rows']} rows): accuracy 1v {r['accuracy']['1v']}, 2v exact {r['accuracy']['2v_exact']} "
              f"({r['accuracy']['2v_minus_1v'][0]:+.2f} {r['accuracy']['2v_minus_1v'][1]}), A5 (a) "
              f"{r['accuracy']['a5_served']} ({r['accuracy']['a5_minus_1v'][0]:+.2f} {r['accuracy']['a5_minus_1v'][1]})")
        print(f"   choice drift: 1v {r['choice_drift']['1v_identity_vs_seeded']}; 2v {r['choice_drift']['2v_vs_independent_2v']}")
        print(f"   (e) flips: {r['equiv_flips']}; yes/no Brier {r['yes_no_brier']}")
    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    main()
