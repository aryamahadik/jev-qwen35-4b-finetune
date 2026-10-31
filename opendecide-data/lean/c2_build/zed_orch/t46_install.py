"""T46 install (A59): vm_out/<ROOTNAME>/T46 (od-cpu1 full generation) -> data/c2_parts/T46, paths rewritten to this Mac, manifests
rehashed, A50 (a) G6 aggregate (B0 = the QC build in GEN_REPORT; builds 11M/12M/13M from zed_orch/a50_vm_t46/). Fresh install only.
  ../.venv/bin/python -B zed_orch/t46_install.py ROOTNAME [--check]      (from lean/c2_build)"""
import argparse, hashlib, json, shutil, subprocess, sys, os
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))
LEAN = C2.parent
ap = argparse.ArgumentParser()
ap.add_argument("rootname")
ap.add_argument("--check", action="store_true")
a = ap.parse_args()
SRC = C2 / "vm_out" / a.rootname / "T46"
VMPFX = f"/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/{a.rootname}/T46"
DST = LEAN / "data" / "c2_parts" / "T46"
OUT_FILES = ("MANIFEST.json", "candidates_c2.jsonl", "candidates_c2.relations.jsonl", "mixdev_S5.jsonl")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fail(m): raise SystemExit("t46_install: " + m)
ps = [x for x in subprocess.run(["pgrep", "-f", "g13_c2|decontam_g13"], capture_output=True, text=True).stdout.split() if x != str(os.getpid())]
if ps: fail(f"a G13 run is alive {ps}")
for f in OUT_FILES:
    if not (SRC / "out" / f).is_file(): fail(f"out/{f} missing")
for sb in (11_000_000, 12_000_000, 13_000_000):
    if not (C2 / "zed_orch" / "a50_vm_t46" / f"T46_b{sb}.json").is_file(): fail(f"A50 build {sb} missing")
man = json.loads((SRC / "out" / "MANIFEST.json").read_text())
for f, m in man["files"].items():
    if sha(SRC / "out" / f) != m["sha256"]: fail(f"{f} sha mismatch")
if DST.exists(): fail(f"{DST} exists")
if a.check:
    print("check ok", man["files"]["candidates_c2.jsonl"]["rows"], "->", DST); sys.exit(0)
for sub in ("out", "qc"):
    for p in sorted((SRC / sub).rglob("*")):
        if p.is_file():
            t = DST / sub / p.relative_to(SRC / sub); t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, t); t.chmod(0o644)
n = 0
for p in sorted(DST.rglob("*")):
    if p.is_file() and p.suffix in (".md", ".json", ".txt"):
        s = p.read_text(encoding="utf-8"); t = s.replace(VMPFX, str(DST))
        if t != s: p.write_text(t, encoding="utf-8"); n += 1
print("files with rewritten paths:", n)
for gate in ("g5h", "g3h"):
    mp = DST / "qc" / gate / "manifest.json"
    if mp.exists():
        m = json.loads(mp.read_text())
        for t in m.get("tasks", []):
            tf = Path(t["task_file"]); assert str(tf).startswith(str(DST)), tf
            t["task_sha256"] = hashlib.sha256(tf.read_text(encoding="utf-8").encode()).hexdigest()
        mp.write_text(json.dumps(m, indent=1)); print(gate, "rehashed", len(m.get("tasks", [])))
import zed_orch.g6_a50_full as A
A.OUTDIR = C2 / "zed_orch" / "a50_vm_t46"
r = A.aggregate("T46", root=DST.parent)
print(json.dumps({"verdict": r["verdict"], "worst": r["worst_cell"], "failing": r["failing_cells"], "bases": r["seed_bases"],
                  "single": r["single_build_max_excess_pp"], "program_pass_a50": r.get("program_pass_a50"),
                  "program_failing_a50": r.get("program_failing_a50")}, indent=1))
bad = [str(p) for p in DST.rglob("*") if p.is_file() and p.suffix in (".md", ".json", ".txt") and b"/home/aryamahadik" in p.read_bytes()]
assert not bad, bad
man = json.loads((DST / "out" / "MANIFEST.json").read_text())
for f, m in man["files"].items(): assert sha(DST / "out" / f) == m["sha256"], f
for f in ("candidates_c2.jsonl", "candidates_c2.relations.jsonl", "mixdev_S5.jsonl"):
    assert sha(DST / "qc" / "_generated" / f) == sha(DST / "out" / f), f
print("install ok", DST, man["files"]["candidates_c2.jsonl"]["rows"])
