"""W9 T32: install the VM generation (zed_orch/w9_t32/gen_root/T32) into data/c2_parts/T32, re-point the G5-H / G3-H task paths
from the VM tree to this Mac, recompute the manifest task hashes, then aggregate the A50 G6 (B0 = the new QC build + the three
fresh 6,000-row builds in zed_orch/w9_t32/out2). Old qc task folders and reports are already in qc/_superseded_w9."""
import hashlib, json, shutil, sys
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
LEAN = C2.parent
SRC = C2 / "zed_orch" / "w9_t32" / "gen_root10" / "T32"
DST = LEAN / "data" / "c2_parts" / "T32"
VMPFX = "/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root10/T32"
assert (DST / "qc" / "_superseded_w9" / "g5h").exists(), "old task folders not superseded yet"
for old in ("g5h", "g3h"):
    if (DST / "qc" / old).exists():
        shutil.rmtree(DST / "qc" / old)
for f in ("G6_A50.json",):
    if (DST / "qc" / f).exists():
        (DST / "qc" / f).unlink()
for sub in ("out", "qc"):
    for p in sorted((SRC / sub).rglob("*")):
        if p.is_file():
            t = DST / sub / p.relative_to(SRC / sub)
            t.parent.mkdir(parents=True, exist_ok=True)
            if "_superseded" in t.parts or "_backup" in t.parts:
                continue
            if t.exists():
                t.chmod(0o644); t.unlink()
            shutil.copy2(p, t)
n = 0
for p in sorted(DST.rglob("*")):
    if p.is_file() and "_superseded_w9" not in p.parts and "_backup_w8" not in p.parts and p.suffix in (".md", ".json", ".txt"):
        s = p.read_text(encoding="utf-8")
        if VMPFX in s:
            p.write_text(s.replace(VMPFX, str(DST)), encoding="utf-8"); n += 1
for gate in ("g5h", "g3h"):
    mp = DST / "qc" / gate / "manifest.json"
    if mp.exists():
        m = json.loads(mp.read_text())
        for t in m.get("tasks", []):
            tf = Path(t["task_file"])
            t["task_sha256"] = hashlib.sha256(tf.read_text(encoding="utf-8").encode()).hexdigest()
        mp.write_text(json.dumps(m, indent=1))
print("rewritten", n)
import zed_orch.g6_a50_full as A
A.OUTDIR = C2 / "zed_orch" / "w9_t32" / "out8"
r = A.aggregate("T32")
print(json.dumps({"verdict": r["verdict"], "worst": r["worst_cell"], "failing": r["failing_cells"], "bases": r["seed_bases"],
                  "single": r["single_build_max_excess_pp"]}, indent=1))
