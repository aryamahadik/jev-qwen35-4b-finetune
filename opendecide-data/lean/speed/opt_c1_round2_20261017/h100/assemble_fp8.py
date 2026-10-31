#!/usr/bin/env python3
"""assemble_fp8.py: parts -> the two shards (sha256 checked against the shas recorded on od-cpu1/od-l4b), then fp8_manifest.json
(every file's bytes + sha256) for the in-container verification. Run after dl_parts finished."""
import hashlib, json, sys
from pathlib import Path
H = Path(__file__).resolve().parent
parts, dst = H / "stage" / "parts", H / "stage" / "c1_fp8_block"
sys.path.insert(0, str(H))
from oc1 import r2 as R2
want = R2.FP8_SHARD_SHA256
psha = {l.split()[1]: l.split()[0] for l in (parts / "parts.sha256").read_text().splitlines() if l.strip()}
for shard, sha in want.items():
    names = sorted(n for n in psha if n.startswith(shard + ".part."))
    out = dst / shard
    h = hashlib.sha256()
    with open(out, "wb") as f:
        for n in names:
            b = (parts / n).read_bytes()
            if hashlib.sha256(b).hexdigest() != psha[n]:
                raise SystemExit(f"part {n} sha mismatch")
            f.write(b)
            h.update(b)
    print(shard, len(names), "parts", out.stat().st_size, "bytes", h.hexdigest()[:16], "OK" if h.hexdigest() == sha else "MISMATCH")
    if h.hexdigest() != sha:
        raise SystemExit("shard sha mismatch")
files = {}
for p in sorted(dst.rglob("*")):
    if p.is_file() and not p.name.startswith(".") and p.name != "fp8_manifest.json":
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        files[str(p.relative_to(dst))] = {"bytes": p.stat().st_size, "sha256": h.hexdigest()}
(dst / "fp8_manifest.json").write_text(json.dumps({"built": "od-cpu1/od-l4b 17 Oct 2026 (build_fp8_block.py); config.json modules_to_not_convert extended with "
                                                   "model.visual.blocks.N.attn.qkv_proj (SGLang's fused vision qkv name); shards untouched",
                                                   "config_json_orig_sha256": (H / "stage" / "config.json.orig.sha256").read_text().split()[0],
                                                   "files": files}, indent=1))
print(len(files), "files in the manifest")
