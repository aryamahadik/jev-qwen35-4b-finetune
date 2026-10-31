"""Run the id-only sealed checker (lean/sealed_nd/qc/sealed_check.py, as a program; its exports are never read) on
every F5 output and list the blocking hits (ids and hit kinds only).

  python -m gen.run_sealed candidates_r1 qc_sample mixdev_S5 cue_bank
"""
from __future__ import annotations

import json
import subprocess
import sys

from .common import LEAN, OUT, TMP

CHECKER = LEAN / "sealed_nd" / "qc" / "sealed_check.py"
PY = "/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python"


def views(name):
    """cue_bank (JSON) is checked through a one-object-per-line view in tmp/."""
    if name == "cue_bank":
        d = json.load(open(OUT / "cue_bank.json"))
        p = TMP / "sealed_view_cue_bank.jsonl"
        with open(p, "w") as f:
            for t in d["templates"]:
                f.write(json.dumps({"id": t["key"], "example": t["example"]}) + "\n")
        return p, None
    return OUT / f"{name}.jsonl", "state,card,instructions"


def run(name):
    src, structure = views(name)
    out = TMP / f"{name}.sealedqc.jsonl"
    summ = TMP / f"{name}.sealedqc.summary.json"
    cmd = [PY, str(CHECKER), str(src), "--id-field", "id", "--out", str(out), "--summary", str(summ), "--workers", "4"]
    if structure:
        cmd += ["--structure-fields", structure]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode not in (0, 1, 2, 3):
        raise SystemExit(f"sealed_check failed on {name}: {p.stderr[-400:]}")
    s = json.load(open(summ))
    hits = []
    with open(out) as f:
        for line in f:
            r = json.loads(line)
            if r.get("hit"):
                hits.append({"id": r["id"], "kinds": r.get("hit_kinds")})
    return {"file": str(src.name), "rows": s.get("rows"), "rows_hit": s.get("rows_hit"),
            "rows_report_only": s.get("rows_report_only"), "parse_errors": s.get("parse_errors"),
            "checker_sha256": s.get("checker_sha256"), "suite_sha256": s.get("suite_sha256"),
            "blocking_hits": hits}


def main(argv=None):
    names = (argv or sys.argv[1:]) or ["candidates_r1", "qc_sample", "mixdev_S5", "cue_bank"]
    res = {n: run(n) for n in names}
    q = OUT / "sealed_check_summary.json"
    if q.exists():      # merge: re-running one set keeps the other sets' results
        res = {**json.load(open(q)), **res}
    json.dump(res, open(OUT / "sealed_check_summary.json", "w"), indent=1)
    print(json.dumps({n: {k: v for k, v in r.items() if k != "blocking_hits"} | {"n_blocking": len(r["blocking_hits"])}
                      for n, r in res.items()}, indent=1))


if __name__ == "__main__":
    main()
