"""Run the id-only sealed checker (lean/sealed_nd/qc/sealed_check.py, as a program; its exports are never opened) on
every COMMIT output; write tmp/sealed/hits.json (ids and hit kinds only) and, for blocking hits, add the rows' commit
record ids to gen/data/sealed_exclude.json so the next build replaces them. Prints counts only."""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "gen"))
import common as C  # noqa: E402

CHECKER = C.LEAN / "sealed_nd" / "qc" / "sealed_check.py"
PY = "/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python"
FILES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}


def run(tag: str) -> dict:
    sd = C.TMP / "sealed"
    sd.mkdir(parents=True, exist_ok=True)
    path = C.OUT / f"{FILES[tag]}.jsonl"
    out, summ = sd / f"{tag}.sealedqc.jsonl", sd / f"{tag}.summary.json"
    cmd = [PY, str(CHECKER), str(path), "--id-field", "id", "--out", str(out), "--summary", str(summ),
           "--structure-fields", "state,card,instructions,options", "--workers", "2",
           "--skip-fields", "meta.git_sha,meta.structure_hash,meta.seed"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode not in (0, 3):
        raise SystemExit(f"checker failed on {tag}: rc {p.returncode} {p.stderr[-300:]}")
    s = json.load(open(summ))
    hits, kinds, blocking = [], Counter(), []
    for line in open(out):
        r = json.loads(line)
        if r.get("hit"):
            ks = r.get("hit_kinds") or r.get("kinds") or r.get("kind") or []
            if isinstance(ks, (str, dict)):
                ks = [ks]
            kk = [k.get("kind") if isinstance(k, dict) else k for k in ks]
            hits.append(r.get("id"))
            kinds.update(kk)
            if not r.get("report_only"):
                blocking.append(r.get("id"))
    return {"rows": sum(1 for _ in open(path)), "hits": len(hits), "blocking_rows": len(blocking),
            "blocking_ids": blocking, "kinds": dict(kinds), "summary_blocking": s.get("blocking_hits"),
            "summary_report_only": s.get("report_only_rows"), "suite_sha256": s.get("suite_sha256")}


if __name__ == "__main__":
    res = {}
    excl_p = C.DATA / "sealed_exclude.json"
    excl = set(json.load(open(excl_p))) if excl_p.exists() else set()
    n0 = len(excl)
    for tag in sys.argv[1:] or list(FILES):
        res[tag] = run(tag)
        ids = set(res[tag]["blocking_ids"])
        if ids:
            for line in open(C.OUT / f"{FILES[tag]}.jsonl"):
                r = json.loads(line)
                if r["id"] in ids:
                    excl.add(r["meta"]["text_source"]["record_id"])
            for line in open(C.OUT / f"{FILES[tag]}.sidecar.jsonl"):
                sd = json.loads(line)
                if sd["id"] in ids:
                    excl.update(e["record_id"] for e in sd.get("extra_records") or [])
        print(tag, {k: v for k, v in res[tag].items() if k != "blocking_ids"}, flush=True)
    with open(C.TMP / "sealed" / "hits.json", "w") as f:
        json.dump(res, f, indent=1)
    if len(excl) > n0:
        json.dump(sorted(excl), open(excl_p, "w"))
    print("SEALED_DONE new_excluded", len(excl) - n0, flush=True)
