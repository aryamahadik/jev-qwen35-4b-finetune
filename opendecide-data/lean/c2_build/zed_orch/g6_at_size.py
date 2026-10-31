"""G6 at the spec 6.3 sample size (>= 5,000 QC rows): an in-memory build of a family's current generator at the pilot
seed base, G15 off, then pilot.g6 / g7 / g10 unchanged (same bar: chance + 2 pp, every view and model). Writes
<family>/<dir>/G6_AT_<n>.json. Families whose runner changes the build (T21 schedule) must use their own runner.
  ../../.venv/bin/python -B zed_orch/g6_at_size.py T28 [--n 6000] [--dir pilot_i1]   (from c2_build)"""
import argparse, json, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))
import pilot, pilot_loaders as PL  # noqa: E402
ap = argparse.ArgumentParser()
ap.add_argument("family")
ap.add_argument("--n", type=int, default=6000)
ap.add_argument("--dir", default="pilot_i1")
a = ap.parse_args()
t0 = time.time()
with PL.open_family(a.family) as kit:
    b = pilot.build_pilot(kit, a.n, run_g15=False)
    g6 = pilot.g6(b.infos)
    g7 = pilot.g7(b.infos)
    g10 = pilot.g10(b.infos, b.units, kit.plugin)
cells = {}
for part in ("yes_no", "choice"):
    p = g6.get(part) or {}
    if p.get("n"):
        cells[part] = {"n": p["n"], "chance": p["chance"],
                       "max": max((p[v][m], v, m) for v in p if isinstance(p[v], dict) and "lr" in p[v] for m in ("lr", "gbt"))}
out = {"family": a.family, "n_rows": len(b.infos), "seconds": round(time.time() - t0), "seed_base": pilot.SEED_BASE,
       "G6_verdict": g6["verdict"], "G6_fails": g6["fails"], "G6_cells_max": cells,
       "G7_verdict": g7.get("verdict"), "G10_verdict": g10.get("verdict"),
       "G10_fails": {k: v for k, v in (g10.get("checks") or {}).items() if v.get("verdict") == "fail"}}
Path(PL.family_dir(a.family), a.dir, f"G6_AT_{a.n}.json").write_text(json.dumps(out, indent=1, default=str))
print(json.dumps({k: out[k] for k in ("family", "n_rows", "G6_verdict", "G7_verdict", "G10_verdict", "seconds")}))
