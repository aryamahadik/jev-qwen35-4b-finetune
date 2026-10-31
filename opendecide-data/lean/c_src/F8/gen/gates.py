"""Run every F8 gate on the written outputs and write tmp/gates.json (counts only).

G3 / G15 / G18 / lints / length / units come from checks.check_file (re-parsed from the rows). G4 comes from the
metamorphic relations run inside the QC-sample build (mr.py, >= 1,000 rows), aggregated per relation and form.
negcount quotas use k_syn from c_src/common/negcount.py (sidecar).
"""
from __future__ import annotations

import collections
import json

import checks
import common as CM

FILES = [("candidates_r1", "train"), ("qc_sample", "train"), ("mixdev_S5", "dev")]


def g4_summary() -> dict:
    st = json.load(open(CM.TMP / "buildstats_qc_sample.json"))
    per = collections.Counter()
    forms = collections.defaultdict(set)
    rows_with_mr = 0
    exc = {}
    for k, v in st["mr"].items():
        key = json.loads(k)
        if isinstance(key, str):
            exc[key] = v
            continue
        rel, form, ok = key
        per[(rel, ok)] += v
        forms[rel].add(form)
    out = {}
    for rel in sorted({r for r, _ in per}):
        p, f = per[(rel, True)], per[(rel, False)]
        out[rel] = {"pass": p, "fail": f, "rate": round(100 * p / (p + f), 3) if p + f else None,
                    "forms": sorted(forms[rel])}
    return {"relations": out, "exceptions": exc}


def main():
    import build
    tools = build.Tools()
    res = {}
    for name, kind in FILES:
        p = CM.OUT / f"{name}.jsonl"
        res[name] = checks.check_file(p, CM.OUT / f"f8_controls_{name}.jsonl", CM.OUT / f"relations_{name}.jsonl",
                                      tools, training=(kind == "train"), s5=(kind == "dev"))
        CM.progress(f"gates {name}: rows {res[name].get('rows')}, G3 agree {res[name].get('G3_solverB_agree')}, "
                    f"render hash {res[name].get('G3_render_hash_match')}, G15 loader {res[name].get('G15_loader_ok')},"
                    f" max tokens {res[name].get('max_tokens')}, fails "
                    f"{sum(v for k, v in res[name].items() if k.startswith('fail'))}")
    res["G4"] = g4_summary()
    with open(CM.TMP / "gates.json", "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "tok_hist"} for k, v in res.items()
                      if k != "G4"})[:4000])
    print(json.dumps(res["G4"])[:3000])


if __name__ == "__main__":
    main()
