"""Run the sealed-suite checker (lean/sealed_nd/qc/sealed_check.py, run as a black-box program; its folder is never
opened) on an F3 output file and list the row ids with a blocking hit. Counts only; never prints text.

  python sealed.py <rows.jsonl>  ->  <rows>.sealedqc.jsonl, <rows>.sealedqc.summary.json, prints hit ids count
"""
from __future__ import annotations

import json
import subprocess
import sys

from f3common import LEAN

CHECKER = LEAN / "sealed_nd" / "qc" / "sealed_check.py"
PY = LEAN.parent / ".venv" / "bin" / "python"


def run(path, workers=6):
    out = str(path)[:-6] + ".sealedqc.jsonl"
    summ = str(path)[:-6] + ".sealedqc.summary.json"
    cmd = [str(PY), str(CHECKER), str(path), "--out", out, "--summary", summ, "--workers", str(workers)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode not in (0, 1):
        raise RuntimeError(f"sealed_check exit {p.returncode}")
    hits = []
    with open(out) as f:
        for line in f:
            o = json.loads(line)
            if o.get("hit"):
                hits.append(o.get("id"))
    summary = json.load(open(summ))
    return hits, summary


if __name__ == "__main__":
    hits, summary = run(sys.argv[1])
    print(json.dumps({"rows_with_blocking_hit": len(hits), "summary_keys": sorted(summary)[:20]}))
