"""Run the id-only sealed checker (lean/sealed_nd/qc/sealed_check.py, as a program; its exports are never opened) on
every F8 output and write tmp/sealed/hits.json (ids and hit kinds only). Prints counts only."""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter

import common as CM

CHECKER = CM.LEAN / "sealed_nd" / "qc" / "sealed_check.py"
PY = "/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python"
SUITE = "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"


def run(path, tag: str) -> dict:
    sd = CM.TMP / "sealed"
    sd.mkdir(parents=True, exist_ok=True)
    out = sd / f"{tag}.sealedqc.jsonl"
    summ = sd / f"{tag}.summary.json"
    cmd = [PY, str(CHECKER), str(path), "--id-field", "id", "--out", str(out), "--summary", str(summ),
           "--structure-fields", "state,card,instructions,options", "--workers", "2",
           "--skip-fields", "meta.git_sha,meta.structure_hash,meta.seed"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode not in (0, 3):
        raise SystemExit(f"checker failed on {tag}: rc {p.returncode}")
    s = json.load(open(summ))
    if s.get("suite_sha256") != SUITE:
        raise SystemExit(f"suite sha mismatch on {tag}")
    hits, kinds, n = [], Counter(), 0
    with open(out) as f:
        for line in f:
            r = json.loads(line)
            n += 1
            if r.get("hit"):
                ks = r.get("kinds") or r.get("kind") or []
                if isinstance(ks, (str, dict)):
                    ks = [ks]
                kk = [k.get("kind") if isinstance(k, dict) else k for k in ks]
                hits.append({"id": r.get("id"), "kinds": kk})
                kinds.update(kk)
    return {"rows": n, "hits": len(hits), "hit_ids": [h["id"] for h in hits], "kinds": dict(kinds),
            "blocking": s.get("blocking_hits", s.get("hits_blocking")), "summary_keys": sorted(s)[:30]}


if __name__ == "__main__":
    hp = CM.TMP / "sealed" / "hits.json"
    res = json.load(open(hp)) if hp.exists() else {}      # repair r2: update per file, keep the other files' results
    for spec in sys.argv[1:]:
        tag, path = spec.split("=")
        res[tag] = run(path, tag)
        print(tag, {k: v for k, v in res[tag].items() if k != "hit_ids"}, flush=True)
    with open(CM.TMP / "sealed" / "hits.json", "w") as f:
        json.dump(res, f, indent=1)
