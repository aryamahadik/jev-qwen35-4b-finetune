"""T33 fix round 2: after pull_stage.sh. Rewrites the VM prefix to the Mac staging prefix in every .md / .json / .txt of the
staged gen_root (so G5-H task files carry Mac paths), recomputes each manifest task_sha256, checks that no VM path is left, and
(when the three A50 builds 11M / 12M / 13M are in out/) writes the A50 aggregate into the STAGED qc (gen_root/T33/qc/G6_A50.json,
GEN_REPORT.json, QC_REPORT.json). install.py later re-points the staging prefix to data/c2_parts/T33 and repeats the aggregate there.
Idempotent. Never writes under data/c2_parts."""
import hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
STAGE = C2 / "zed_orch" / "T33_fix_r2"
SRC = STAGE / "gen_root" / "T33"
VMPFX = "/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/T33_fix_r2/gen_root/T33"
n = 0
for p in sorted(SRC.rglob("*")):
    if p.is_file() and p.suffix in (".md", ".json", ".txt"):
        s = p.read_text(encoding="utf-8")
        if VMPFX in s:
            p.write_text(s.replace(VMPFX, str(SRC)), encoding="utf-8")
            n += 1
print("files rewritten to Mac staging paths:", n)
for gate in ("g5h", "g3h"):
    mp = SRC / "qc" / gate / "manifest.json"
    if mp.exists():
        m = json.loads(mp.read_text())
        for t in m.get("tasks", []):
            tf = Path(t["task_file"])
            assert tf.is_file() and str(tf).startswith(str(SRC)), tf
            t["task_sha256"] = hashlib.sha256(tf.read_text(encoding="utf-8").encode()).hexdigest()
        mp.write_text(json.dumps(m, indent=1))
        print(gate, "manifest rehashed:", len(m.get("tasks", [])), "tasks")
bad = [str(p) for p in SRC.rglob("*") if p.is_file() and p.suffix in (".md", ".json", ".txt") and b"/home/aryamahadik" in p.read_bytes()]
print("files still holding /home/aryamahadik:", len(bad), bad[:3])
have = [sb for sb in (11_000_000, 12_000_000, 13_000_000) if (STAGE / "out" / f"T33_b{sb}.json").is_file()]
print("A50 builds present:", have)
if len(have) == 3 and (SRC / "qc" / "GEN_REPORT.json").is_file():
    import zed_orch.g6_a50_full as A
    A.OUTDIR = STAGE / "out"
    r = A.aggregate("T33", root=STAGE / "gen_root")
    print(json.dumps({"verdict": r["verdict"], "worst": r["worst_cell"], "failing": r["failing_cells"], "bases": r["seed_bases"],
                      "single": r["single_build_max_excess_pp"], "program_pass_a50": r.get("program_pass_a50"),
                      "program_failing_a50": r.get("program_failing_a50")}, indent=1))
