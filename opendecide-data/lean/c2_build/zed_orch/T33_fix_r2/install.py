"""T33 fix round 2 (A52 d): install the staged generation (zed_orch/T33_fix_r2/gen_root/T33) into data/c2_parts/T33.

NOT run by the agent that staged it: the orchestrator runs it AFTER the G13 run (it replaces candidates_c2.jsonl,
candidates_c2.relations.jsonl, mixdev_S5.jsonl and MANIFEST.json of T33, so the G13 logs of T33 become stale: re-run G13 for T33).

  ../.venv/bin/python -B zed_orch/T33_fix_r2/install.py            (from lean/c2_build; installs into data/c2_parts/T33)
  ../.venv/bin/python -B zed_orch/T33_fix_r2/install.py --check    (no writes: preconditions + what it would do)

What it does (modelled on zed_orch/w9_t32/install.py):
  1. refuses when a G13 run is alive, when the staged tree is missing a file, or when the staged out/ is not the A52 d generation
     (GEN_REPORT seeds must be the T33_fix_r2 bases);
  2. old state -> data/c2_parts/T33/qc/_superseded_r2/: the old qc task folders (g5h, g3h), GEN_REPORT.json, QC_REPORT.json,
     G6_A50.json, _generated/, and a copy of the old out/ files (chmod u+w on out/ first: the batch4 protection is undone);
  3. copies the staged out/ and qc/ (without _superseded*/_backup*) into data/c2_parts/T33/;
  4. rewrites the VM prefix and the staging prefix to data/c2_parts/T33 in every .md / .json / .txt (task files, manifests,
     reports), recomputes each manifest task_sha256;
  5. writes the A50 aggregate (zed_orch/g6_a50_full.aggregate: B0 = the new QC build, 11M / 12M / 13M builds from
     zed_orch/T33_fix_r2/out/) into data/c2_parts/T33/qc/G6_A50.json and records it in GEN_REPORT.json / QC_REPORT.json;
  6. checks: no "/home/aryamahadik" left, out/ files equal MANIFEST sha256, _generated equals out/.
Task files are self-contained (answer path inside); key.json files are orchestrator only."""
import argparse, hashlib, json, shutil, subprocess, sys, os, stat
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
LEAN = C2.parent
STAGE = C2 / "zed_orch" / "T33_fix_r2"
SRC = STAGE / "gen_root" / "T33"
VMPFX = "/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/T33_fix_r2/gen_root/T33"
STAGE_BASES = (300_000_000, 301_000_000, 302_000_000)
OUT_FILES = ("MANIFEST.json", "candidates_c2.jsonl", "candidates_c2.relations.jsonl", "mixdev_S5.jsonl")
SKIP = ("_superseded", "_backup")

ap = argparse.ArgumentParser()
ap.add_argument("--check", action="store_true", help="preconditions only, no writes")
ap.add_argument("--dst", default=None, help="test only: install into this T33 folder instead of data/c2_parts/T33 "
                "(must lie under lean/; its parent is used as the aggregate root)")
a = ap.parse_args()
DST = Path(a.dst).resolve() if a.dst else LEAN / "data" / "c2_parts" / "T33"
ROOT = DST.parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def fail(msg):
    raise SystemExit("install.py: " + msg)


# ---- 1. preconditions
if not a.dst:
    ps = subprocess.run(["pgrep", "-f", "g13_c2|decontam_g13"], capture_output=True, text=True).stdout.split()
    ps = [x for x in ps if x != str(os.getpid())]
    if ps:
        fail(f"a G13 run is alive (pids {' '.join(ps)}), not installing; re-run when it has ended")
for f in OUT_FILES:
    if not (SRC / "out" / f).is_file():
        fail(f"staged out/{f} missing")
for f in ("GEN_REPORT.json", "QC_REPORT.json", "G6_A50.json"):
    if not (SRC / "qc" / f).is_file():
        fail(f"staged qc/{f} missing (run the staged A50 aggregate first)")
gen = json.loads((SRC / "qc" / "GEN_REPORT.json").read_text())
seeds = gen["seeds"]
if (seeds["candidates"], seeds["qc"], seeds["mixdev"]) != STAGE_BASES:
    fail(f"staged GEN_REPORT seeds {seeds} are not the T33_fix_r2 bases {STAGE_BASES}")
for sb in (11_000_000, 12_000_000, 13_000_000):
    if not (STAGE / "out" / f"T33_b{sb}.json").is_file():
        fail(f"staged A50 build out/T33_b{sb}.json missing")
man = json.loads((SRC / "out" / "MANIFEST.json").read_text())
for f, m in man["files"].items():
    if sha(SRC / "out" / f) != m["sha256"]:
        fail(f"staged out/{f} does not match its MANIFEST sha256")
left = [str(p) for p in SRC.rglob("*") if p.is_file() and p.suffix in (".md", ".json", ".txt")
        and VMPFX.encode() in p.read_bytes()]
print("staged files still holding the VM prefix (rewritten below):", len(left))
if a.check:
    print("check ok: staged T33 generation", seeds, "rows", man["files"]["candidates_c2.jsonl"]["rows"],
          "-> would install into", DST)
    sys.exit(0)
if not DST.exists():
    fail(f"{DST} missing")

# ---- 2. old state -> qc/_superseded_r2
sup = DST / "qc" / "_superseded_r2"
if sup.exists():
    fail(f"{sup} already exists: install.py was run before (A52 d: one round)")
sup.mkdir(parents=True)
(DST / "out").chmod(0o755)
for p in (DST / "out").iterdir():
    p.chmod(0o644)
(sup / "out").mkdir()
for p in sorted((DST / "out").iterdir()):
    shutil.copy2(p, sup / "out" / p.name)
for name in ("g5h", "g3h", "GEN_REPORT.json", "QC_REPORT.json", "G6_A50.json", "_generated"):
    if (DST / "qc" / name).exists():
        shutil.move(str(DST / "qc" / name), str(sup / name))

# ---- 3. copy the staged out/ and qc/
for sub in ("out", "qc"):
    for p in sorted((SRC / sub).rglob("*")):
        if p.is_file() and not any(s in x for x in p.relative_to(SRC / sub).parts for s in SKIP):
            t = DST / sub / p.relative_to(SRC / sub)
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, t)
            t.chmod(0o644)

# ---- 4. paths -> this Mac (VM prefix and staging prefix), manifest hashes
n = 0
for p in sorted(DST.rglob("*")):
    if p.is_file() and p.suffix in (".md", ".json", ".txt") and not any(s in x for x in p.relative_to(DST).parts for s in SKIP):
        s = p.read_text(encoding="utf-8")
        t = s.replace(VMPFX, str(DST)).replace(str(SRC), str(DST))
        if t != s:
            p.write_text(t, encoding="utf-8")
            n += 1
print("files with rewritten paths:", n)
for gate in ("g5h", "g3h"):
    mp = DST / "qc" / gate / "manifest.json"
    if mp.exists():
        m = json.loads(mp.read_text())
        for t in m.get("tasks", []):
            tf = Path(t["task_file"])
            assert str(tf).startswith(str(DST)), tf
            t["task_sha256"] = hashlib.sha256(tf.read_text(encoding="utf-8").encode()).hexdigest()
        mp.write_text(json.dumps(m, indent=1))
        print(gate, "manifest rehashed:", len(m.get("tasks", [])), "tasks")

# ---- 5. the A50 aggregate (B0 = the new QC build; 11M / 12M / 13M from the staged out/)
import zed_orch.g6_a50_full as A
A.OUTDIR = STAGE / "out"
r = A.aggregate("T33", root=ROOT)
print(json.dumps({"verdict": r["verdict"], "worst": r["worst_cell"], "failing": r["failing_cells"], "bases": r["seed_bases"],
                  "single": r["single_build_max_excess_pp"], "program_pass_a50": r.get("program_pass_a50"),
                  "program_failing_a50": r.get("program_failing_a50")}, indent=1))

# ---- 6. checks
bad = [str(p) for p in DST.rglob("*") if p.is_file() and p.suffix in (".md", ".json", ".txt") and not any(
    s in x for x in p.relative_to(DST).parts for s in SKIP) and b"/home/aryamahadik" in p.read_bytes()]
assert not bad, bad
man = json.loads((DST / "out" / "MANIFEST.json").read_text())
for f, m in man["files"].items():
    assert sha(DST / "out" / f) == m["sha256"], f
for f in ("candidates_c2.jsonl", "candidates_c2.relations.jsonl", "mixdev_S5.jsonl"):
    assert sha(DST / "qc" / "_generated" / f) == sha(DST / "out" / f), f
print("install ok:", DST, "| candidates", man["files"]["candidates_c2.jsonl"]["rows"],
      "| NEXT: re-run G13 for T33 (candidates and mixdev changed), then the G5-H reads (qc/g5h/tasks)")
