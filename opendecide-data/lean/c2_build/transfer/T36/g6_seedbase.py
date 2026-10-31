"""transfer/T36/g6_seedbase.py: zed_orch/g6_at_size.py with a seed base argument (the shared script has none).
In-memory build of the current generator at --seed-base (G15 off), then pilot.g6 / g7 / g10 unchanged. Writes
<out> (JSON). From lean/c2_build:  ../../.venv/bin/python -B transfer/T36/g6_seedbase.py --seed-base 900000 --n 6000 --out F"""
import argparse, json, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import pilot, pilot_loaders as PL  # noqa: E402
ap = argparse.ArgumentParser()
ap.add_argument("--seed-base", type=int, required=True)
ap.add_argument("--n", type=int, default=6000)
ap.add_argument("--out", required=True)
a = ap.parse_args()
t0 = time.time()
with PL.open_family("T36") as kit:
    b = pilot.build_pilot(kit, a.n, seed_base=a.seed_base, run_g15=False)
    g6 = pilot.g6(b.infos)
    g7 = pilot.g7(b.infos)
    g10 = pilot.g10(b.infos, b.units, kit.plugin)
cells = {}
for part in ("yes_no", "choice"):
    p = g6.get(part) or {}
    if p.get("n"):
        cells[part] = {"n": p["n"], "chance": p["chance"],
                       "bar": round(p["chance"] + 0.02, 4),
                       "all": {f"{v}/{m}": p[v][m] for v in p if isinstance(p[v], dict) and "lr" in p[v] for m in ("lr", "gbt")}}
out = {"seed_base": a.seed_base, "n_rows": len(b.infos), "seconds": round(time.time() - t0),
       "G6_verdict": g6["verdict"], "G6_fails": g6["fails"], "G6_cells": cells,
       "G7_verdict": g7.get("verdict"), "G7_fails": g7.get("fails") or g7.get("failures"),
       "G10_verdict": g10.get("verdict"),
       "G10_fails": {k: v for k, v in (g10.get("checks") or {}).items() if v.get("verdict") == "fail"}}
Path(a.out).write_text(json.dumps(out, indent=1, default=str))
print(json.dumps({k: out[k] for k in ("seed_base", "n_rows", "G6_verdict", "G7_verdict", "G10_verdict", "seconds")}))
print(json.dumps({p: {k: v for k, v in c["all"].items() if v > c["bar"] - 0.02} for p, c in cells.items()}))
