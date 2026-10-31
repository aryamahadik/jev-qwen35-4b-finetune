"""c2_build/families/T29/balance_sim.py: the pilot's row mix WITHOUT rendering (T29 fix iteration 1; nothing is written).

pilot.build_pilot draws specs round robin over the training samplers (seed SEED_BASE + k // 4) and builds one relation
unit per spec. Every unit passed in the Stage B pilot (0 drops), so the row mix is a function of plugin.sample() and
plugin.relations() alone: this module replays exactly that, reading each row's question form, gold, verdict, depth and
display facts from the specs (no skin, wording or option text). It is how the balance constants of plugin.py
(QFORM_SHARES, TWIN_KEEP, DEEP_KEEP, COMPLEMENT_W, CANNOT_SHOWN, PREMISE_RATE) are measured and re-checked, in
seconds instead of the pilot's two minutes. It never opens a path outside the family folder and the pinned pools.

  ../.venv/bin/python -B -m families.T29.balance_sim [--rows 1000] [--bases 900000,1900000] [--table twin]
(from lean/c2_build). Library use: simulate(plugin, n_rows, seed_base) -> list of row dicts; summary(rows).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

TRAIN = ("S1", "S2", "S3", "S4")
SEED_BASE = 900_000


def _row(plugin, spec, role, unit, base_answer=None, shown=None):
    ans = plugin.solve_a(spec)
    rt, conf = plugin._rule_truths(spec), plugin._confirmed_c(spec)
    verdict = plugin._verdict_c(rt, conf)
    q = spec.qform
    if shown is None:
        shown = q == "ch_verdict" and bool(spec.structure["show_abstain"])
    if q == "ch_verdict" and ans == "cannot":
        shown = True
    return {"unit": unit, "role": role, "qform": q, "qtype": plugin.QFORMS[q].qtype, "answer": ans,
            "verdict": verdict, "depth": spec.depth, "deep": bool(spec.deep), "sampler": spec.sampler,
            "card": spec.card_id, "shown": shown, "n_rules": len(spec.structure["rules"]), "tags": tuple(spec.tags)}


def simulate(plugin, n_rows: int = 1000, seed_base: int = SEED_BASE, samplers=TRAIN) -> list:
    out, k, unit = [], 0, 0
    while len(out) < n_rows:
        smp = samplers[k % len(samplers)]
        seed = seed_base + k // len(samplers)
        k += 1
        spec = plugin.sample(seed, smp)
        base = _row(plugin, spec, "base", unit)
        out.append(base)
        for prop in plugin.relations(spec):
            if prop.kind == "complement":
                s2 = spec.replace(qform=prop.qform)
                out.append({**_row(plugin, s2, "complement", unit), "base_answer": base["answer"]})
            elif prop.kind in ("twin", "premise_removal"):
                s2 = plugin.derive(prop.spec)
                r = _row(plugin, s2, "twin" if prop.kind == "twin" else "premise_removal", unit)
                r["base_answer"] = base["answer"]
                r["base_verdict"] = base["verdict"]
                out.append(r)
            elif prop.kind in ("equiv", "inv"):
                out.append({**base, "role": "equiv" if prop.kind == "equiv" else "attack"})
        unit += 1
    return out


def _share(n, d):
    return round(n / d, 4) if d else None


def summary(rows: list, plugin) -> dict:
    n = len(rows)
    yn = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    qf = plugin.QFORMS
    out = {"rows": n, "yes_no": len(yn), "yes_no_share": _share(len(yn), n),
           "yes_rate": _share(sum(r["answer"] for r in yn), len(yn))}
    out["yes_rate_by_role"] = {ro: _share(sum(r["answer"] for r in yn if r["role"] == ro),
                                          sum(1 for r in yn if r["role"] == ro)) for ro in
                               ("base", "complement", "twin", "equiv", "attack")}
    out["yes_rate_by_qform"] = {q: [_share(sum(r["answer"] for r in yn if r["qform"] == q),
                                           sum(1 for r in yn if r["qform"] == q)), sum(1 for r in yn if r["qform"] == q)]
                                for q in sorted({r["qform"] for r in yn})}
    syn = sum(1 for r in yn if qf[r["qform"]].complement_kind == "syntactic")
    out["syntactic_complement_share_of_yes_no"] = _share(syn, len(yn))
    dneg = getattr(plugin, "DNEG_FORMS", ())
    out["double_negation_share_of_yes_no"] = _share(sum(1 for r in yn if r["qform"] in dneg), len(yn))
    comp = [r for r in yn if r["role"] == "complement"]
    out["complement_share_of_yes_no"] = _share(len(comp), len(yn))
    out["non_syntactic_share_of_pairs"] = _share(sum(1 for r in comp if qf[r["qform"]].complement_kind != "syntactic"),
                                                 len(comp))
    out["yes_is_bad_share"] = _share(sum(1 for r in yn if qf[r["qform"]].yes_is_bad), len(yn))
    out["roles"] = dict(Counter(r["role"] for r in rows))
    out["twin_share"] = _share(out["roles"].get("twin", 0), n)
    out["equiv_share"] = _share(out["roles"].get("equiv", 0), n)
    out["premise_share"] = _share(out["roles"].get("premise_removal", 0), n)
    out["attack_share"] = _share(out["roles"].get("attack", 0), n)
    cv = [r for r in ch if r["qform"] == "ch_verdict"]
    shown = [r for r in cv if r["shown"]]
    out["ch_verdict"] = {"rows": len(cv), "shown": len(shown), "shown_share": _share(len(shown), len(cv)),
                         "cannot_gold": sum(r["answer"] == "cannot" for r in cv),
                         "cannot_gold_share_of_shown": _share(sum(r["answer"] == "cannot" for r in shown), len(shown)),
                         "cannot_gold_share_of_all": _share(sum(r["answer"] == "cannot" for r in cv), len(cv)),
                         "verdict_mix": dict(Counter(r["answer"] for r in cv))}
    ru = [r for r in ch if r["qform"] == "ch_rule"]
    out["ch_rule"] = {"rows": len(ru), "none_gold_share": _share(sum(r["answer"] == "none" for r in ru), len(ru))}
    by = defaultdict(Counter)
    for r in rows:
        by[r["verdict"]][min(r["depth"], 3)] += 1
    out["depth_by_verdict"] = {v: {d: round(c / sum(cn.values()), 3) for d, c in sorted(cn.items())}
                               for v, cn in sorted(by.items()) for cn in [by[v]]}
    out["deep_share"] = _share(sum(r["deep"] for r in rows), n)
    out["samplers"] = dict(Counter(r["sampler"] for r in rows))
    out["cards"] = len({r["card"] for r in rows})
    return out


def leak(rows: list, feature=lambda r: min(r["depth"], 3), shuffles: int = 20) -> dict:
    """Held-out gain (percentage points) of the best constant answer per feature value over the best constant answer, per
    group (yes/no per question form; ch_verdict rows that show / hide CANNOT DECIDE), 2-fold by unit parity. `null_pp`
    is the same number with the answers shuffled inside the group (the gain a no-signal feature shows by chance: it is
    positive because the best constant per value is picked on the training fold). Rows of one unit share their card, so
    the shuffle null understates the scatter: judge a feature over several seed bases (a real leak is the same sign
    every time; depth was +8 to +23 pp on the Stage B rows and is 0 +- 2 pp on card depth)."""
    import random
    rng = random.Random(7)
    groups = defaultdict(list)
    for r in rows:
        if r["qtype"] == "noul":
            groups[("yn", r["qform"])].append(r)
        elif r["qform"] == "ch_verdict":
            groups[("ch_shown" if r["shown"] else "ch_hidden",)].append(r)

    def gain_of(rs, answers):
        gain = 0.0
        for fold in (0, 1):
            tr = [i for i, r in enumerate(rs) if r["unit"] % 2 != fold]
            te = [i for i, r in enumerate(rs) if r["unit"] % 2 == fold]
            base = Counter(answers[i] for i in tr).most_common(1)[0][0]
            by = defaultdict(Counter)
            for i in tr:
                by[feature(rs[i])][answers[i]] += 1
            for i in te:
                f = feature(rs[i])
                pred = by[f].most_common(1)[0][0] if by.get(f) else base
                gain += ((pred == answers[i]) - (base == answers[i])) / len(rs)
        return 100 * gain

    out = {}
    for g, rs in groups.items():
        if len(rs) < 200:
            continue
        ans = [r["answer"] for r in rs]
        nulls = []
        for _ in range(shuffles):
            sh = ans[:]
            rng.shuffle(sh)
            nulls.append(gain_of(rs, sh))
        out["|".join(g)] = {"n": len(rs), "gain_pp": round(gain_of(rs, ans), 2),
                            "null_pp": round(sum(nulls) / len(nulls), 2)}
    return out


def twin_table(plugin, n_rows: int = 30000, seed_base: int = 31_000_000) -> dict:
    """TWIN_KEEP: per yes/no question form, the keep probability of a minimal-edit twin by its expected answer that makes
    twin-yes and twin-no equally frequent (the larger side is thinned to the smaller). Measured with TWIN_KEEP switched
    off, on `n_rows` rows of the pilot's row mix."""
    from families.T29 import plugin as P
    saved, P.TWIN_KEEP = P.TWIN_KEEP, {}
    try:
        rows = simulate(plugin, n_rows, seed_base)
    finally:
        P.TWIN_KEEP = saved
    cnt = defaultdict(Counter)
    for r in rows:
        if r["role"] == "twin" and r["qtype"] == "noul":
            cnt[r["qform"]][r["answer"]] += 1
    keep, info = {}, {}
    for q, c in cnt.items():
        lo = min(c[0], c[1])
        keep[q] = {a: round(lo / c[a], 3) if c[a] else 1.0 for a in (0, 1)}
        info[q] = {"twin_no": c[0], "twin_yes": c[1]}
    keep["yn_go_dneg"] = keep.get("yn_go", {})
    return {"keep": keep, "info": info}


def open_plugin():
    import pilot_loaders as PL
    return PL.open_family("T29")


def brief(r: dict) -> str:
    """A few lines of the numbers the pilot gates look at."""
    chv = r["ch_verdict"]
    return "\n".join([
        f"rows {r['rows']} yn_share {r['yes_no_share']} yes {r['yes_rate']} by role {r['yes_rate_by_role']}",
        f"  syn {r['syntactic_complement_share_of_yes_no']} dneg {r['double_negation_share_of_yes_no']} comp "
        f"{r['complement_share_of_yes_no']} nonsyn {r['non_syntactic_share_of_pairs']} yes_is_bad {r['yes_is_bad_share']}",
        f"  twin {r['twin_share']} equiv {r['equiv_share']} premise {r['premise_share']} attack {r['attack_share']}",
        f"  ch_verdict rows {chv['rows']} shown {chv['shown_share']} cannot|shown {chv['cannot_gold_share_of_shown']} "
        f"cannot|all {chv['cannot_gold_share_of_all']} mix {chv['verdict_mix']}",
        f"  ch_rule {r['ch_rule']} deep {r['deep_share']}",
        f"  yes by qform {r['yes_rate_by_qform']}",
        f"  depth by verdict {r['depth_by_verdict']}",
        f"  depth leak {r.get('leak_depth')}"])


def main(argv=None):
    import ast
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=1000)
    ap.add_argument("--bases", default=str(SEED_BASE))
    ap.add_argument("--set", nargs="*", default=[], help="NAME=VALUE overrides of families.T29.plugin constants")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--table", choices=("twin",), default=None)
    ap.add_argument("--n", type=int, default=30000, help="rows for --table")
    a = ap.parse_args(argv)
    from families.T29 import plugin as P
    for kv in a.set:
        k, v = kv.split("=", 1)
        setattr(P, k, ast.literal_eval(v))
    if a.table == "twin":
        with open_plugin() as kit:
            t = twin_table(kit.plugin, a.n)
        print(json.dumps(t["info"], indent=1))
        print("TWIN_KEEP = " + json.dumps({q: {int(k): v for k, v in d.items()} for q, d in t["keep"].items()}))
        return
    with open_plugin() as kit:
        res = {}
        for b in (int(x) for x in a.bases.split(",")):
            rows = simulate(kit.plugin, a.rows, b)
            res[b] = summary(rows, kit.plugin)
            res[b]["leak_depth"] = leak(rows)
        if a.json:
            print(json.dumps(res, indent=1, default=str))
        else:
            for b, r in res.items():
                print(f"--- base {b}\n" + brief(r))


if __name__ == "__main__":
    main()
