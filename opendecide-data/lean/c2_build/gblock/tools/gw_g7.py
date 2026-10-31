"""G7-style shortcut screen for GW (A40 quality note): a one-sided binomial per unigram / bigram / metadata feature, per wave-2
type, alpha 0.01 Bonferroni over the features tested (n >= 20). It reuses pilot.ngrams and pilot._pb_test (the program-family G7's
own helpers); the family G7 itself (pilot.g7) needs pilot RowInfo objects, so this is its wave-2 form. Report only: it writes
data/c2_parts/GW/qc/G7_GW.json; no row is dropped or relabelled here.

    python -B gblock/tools/gw_g7.py            (from c2_build)
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

CB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CB))
import pilot as P  # noqa: E402
from scipy.stats import binom  # noqa: E402

GW = CB.parent / "data" / "c2_parts" / "GW"


def meta_feats(r: dict) -> set:
    w = r["meta"]["wave2"]
    f = {f"meta:wording={w.get('wording_id')}", f"meta:task={w.get('haiku_task_id') or r['meta'].get('card_id')}"}
    # model-visible properties only: the construction labels (slot, kind, variant, pii_type, position) are the gold's own
    # definition and never appear in the prompt, so they are not features
    for k, edges in (("state", (100, 200, 400, 700, 1000, 1500, 2500)), ("instr", (150, 300, 500, 800))):
        n = len(r["state"] if k == "state" else r["instructions"])
        f.add(f"num:len_{k}~{next((i for i, e in enumerate(edges) if n <= e), len(edges))}")
    return f


def screen(rows: list) -> dict:
    yn = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    feats = defaultdict(list)
    for n, r in enumerate(yn):
        for f in P.ngrams(r["instructions"] + "\n" + r["state"]) | meta_feats(r):
            feats[f].append(n)
    y = [int(r["gold"]) for r in yn]
    yres = []
    for f, ix in feats.items():
        if len(ix) < P.N_MIN or len(ix) > len(yn) - P.N_MIN:
            continue
        k = sum(y[j] for j in ix)
        x = max(k, len(ix) - k)
        yres.append({"feature": f, "n": len(ix), "yes": k, "p": float(min(1.0, binom.sf(x - 1, len(ix), 0.5)))})
    units = defaultdict(lambda: defaultdict(list))
    for ri, r in enumerate(ch):
        kinds = sorted(meta_feats(r))
        for j, o in enumerate(r["options"]):
            g = int(o == r["gold"])
            for f in {"opt:" + t for t in P.ngrams(o)} | {"optpos=%d" % j}:
                units[f][ri].append(g)
                for m in kinds:
                    if m.startswith(("meta:wording", "meta:task")):
                        units[f + "&" + m][ri].append(g)
    cres = []
    for f, per in units.items():
        ps, x = [], 0
        for ri, gs in per.items():
            k = len(ch[ri]["options"])
            if len(gs) == k:
                continue
            ps.append(len(gs) / k)
            x += sum(gs)
        if len(ps) < P.N_MIN:
            continue
        p, mu = P._pb_test(ps, x)
        cres.append({"feature": f, "n_rows": len(ps), "gold_hits": x, "expected": round(mu, 2), "p": p})
    n_tests = len(yres) + len(cres)
    thr = P.ALPHA / max(1, n_tests)
    fy = sorted((o for o in yres if o["p"] < thr), key=lambda o: o["p"])
    fc = sorted((o for o in cres if o["p"] < thr), key=lambda o: o["p"])
    return {"rows": len(rows), "yes_no_rows": len(yn), "choice_rows": len(ch), "n_tests": n_tests, "bonferroni_p": thr,
            "yes_no_fails": len(fy), "choice_fails": len(fc), "yes_no_fail_top": fy[:12], "choice_fail_top": fc[:12],
            "verdict": "pass" if not (fy or fc) else "fail"}


def main() -> None:
    rows = [json.loads(l) for l in (GW / "out" / "candidates_c2.jsonl").open(encoding="utf-8")]
    by = defaultdict(list)
    for r in rows:
        by[r["meta"]["wave2"]["type"]].append(r)
    res = {t: screen(v) for t, v in sorted(by.items())}
    out = {"gate": "G7-style (A40 quality note), per type", "alpha": P.ALPHA, "n_min": P.N_MIN,
           "constructed_types_binding": ["W1", "W3", "W4", "W5", "W7", "W8"], "report_only_types": ["W2", "W6"], "by_type": res,
           "verdicts": {t: v["verdict"] for t, v in res.items()}}
    (GW / "qc" / "G7_GW.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out["verdicts"]), {t: (v["yes_no_fails"], v["choice_fails"], v["n_tests"]) for t, v in res.items()})


if __name__ == "__main__":
    main()
