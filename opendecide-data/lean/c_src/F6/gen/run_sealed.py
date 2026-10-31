"""Run the id-only sealed checker (lean/sealed_nd/qc/sealed_check.py, as a program; its exports are never read) on an
F6 output file and record ids and hit kinds only.

  python -m gen.run_sealed <set> [path]
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter

from .common import LEAN, OUT, TMP, PY, SEALED_SUITE_SHA256, progress, sha256_file

CHECKER = LEAN / "sealed_nd" / "qc" / "sealed_check.py"
NAMES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}


def check(path, tag: str) -> dict:
    sd = TMP / "sealed"
    sd.mkdir(parents=True, exist_ok=True)
    out = sd / f"{tag}.sealedqc.jsonl"
    summ = sd / f"{tag}.summary.json"
    cmd = [PY, str(CHECKER), str(path), "--id-field", "id", "--out", str(out), "--summary", str(summ),
           "--structure-fields", "state,card,instructions,options",
           "--skip-fields", "meta.structure_hash,meta.seed,meta.git_sha,group_id,call_id,meta.card_id,meta.domain_pack,"
                            "meta.format_style,meta.wording_id,meta.spec_id,meta.gen_version,meta.licence",
           "--workers", "2"]   # v3d: local runs use <= 2 workers
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode not in (0, 3):
        raise SystemExit(f"sealed checker failed: rc {p.returncode}")
    s = json.load(open(summ))
    if s.get("suite_sha256") != SEALED_SUITE_SHA256:
        raise SystemExit("sealed checker suite sha mismatch")
    hits, kinds, rep = [], Counter(), Counter()
    n = 0
    with open(out) as f:
        for line in f:
            r = json.loads(line)
            n += 1
            kn = lambda k: k.get("kind") if isinstance(k, dict) else k  # noqa: E731
            if r.get("hit"):
                hk = [kn(k) for k in r.get("hit_kinds") or []]
                hits.append({"id": r["id"], "kinds": hk})
                kinds.update(hk)
            for k in r.get("report_kinds") or []:
                rep[kn(k)] += 1
    res = {"rows": n, "hits": len(hits), "hit_ids": hits, "hit_kinds": dict(kinds), "report_kinds": dict(rep),
           "checker_sha256": s.get("checker_sha256"), "input_sha256": sha256_file(path)}
    return res


def main():
    tag = sys.argv[1]
    path = sys.argv[2] if len(sys.argv) > 2 else OUT / f"{NAMES[tag]}.jsonl"
    res = check(path, tag)
    json.dump(res, open(TMP / f"sealed_{tag}.json", "w"), indent=1)
    progress(f"sealed_check {tag}: rows {res['rows']}, hits {res['hits']} {res['hit_kinds']}, "
             f"report-only {dict(res['report_kinds'])}")
    print(json.dumps({k: v for k, v in res.items() if k != "hit_ids"}, indent=1))


if __name__ == "__main__":
    main()
