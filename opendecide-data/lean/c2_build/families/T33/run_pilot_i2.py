"""families/T33/run_pilot_i2.py: the T33 pilot of fix iteration 2 (C2_DATA_SPEC 6.4 step 6 -> step 5; ROUND2_BRIEF).

A copy of run_pilot_i1.py with output folder pilot_i2/ (pilot/ and pilot_i1/ stay untouched) and two additions:
  - the pool loader also reads the frozen double-negation supplement pools/dneg_i2_supplement.json when it exists
    (dneg_i2.load_ctx_i2 replaces haiku_author.load_ctx for the run; pilot_loaders.py is not edited and still
    sha-checks the frozen pool files). Without the supplement the run is the frozen pools, as in iteration 1.
  - `g6`: the A43 run at a larger size (default 6,000 rows, G15 off) with pilot.g6 / g7 / g10 unchanged, written to
    pilot_i2/G6_AT_<n>.json (zed_orch/g6_at_size.py builds from the unpatched loader, so it cannot see the supplement).
The same code as `pilot.py run T33` otherwise: build_pilot over the pools, the program gates G2, G3, G4, G-SL, G-LEX,
G-TW, G15 and the row schema, G6, G7, G10, the overlay report, spec 3.0, and the G5-H / G3-H task files (not answered).
No Haiku, no model, no network.

  ../../.venv/bin/python -B families/T33/run_pilot_i2.py run              (from lean/c2_build) write pilot_i2/
  ../../.venv/bin/python -B families/T33/run_pilot_i2.py dry              in memory; prints rows / relations sha256
  ../../.venv/bin/python -B families/T33/run_pilot_i2.py determinism      dry under PYTHONHASHSEED 1 and 4242, compare
  ../../.venv/bin/python -B families/T33/run_pilot_i2.py g6 [--n 6000]    G6 / G7 / G10 at size -> pilot_i2/G6_AT_6000.json
"""
from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from families.T33 import dneg_i2 as D  # noqa: E402  (captures the frozen-pools loader before the patch below)
from families.T33 import haiku_author as HA  # noqa: E402

OUT = "pilot_i2"


def _redirect(dir_path: Path):
    class _Dir(type(Path())):
        def __truediv__(self, key):
            return Path(self) / (OUT if key == "pilot" else key)
    return _Dir(dir_path)


@contextlib.contextmanager
def _patched():
    import pilot_loaders as PL
    real_open, real_load = PL.open_family, HA.load_ctx

    @contextlib.contextmanager
    def patched(fid):
        with real_open(fid) as kit:
            kit.dir = _redirect(kit.dir)
            yield kit
    PL.open_family, HA.load_ctx = patched, D.load_ctx_i2
    try:
        yield PL
    finally:
        PL.open_family, HA.load_ctx = real_open, real_load


def run(write: bool) -> dict:
    import pilot
    with _patched():
        return pilot.run_family("T33", pilot.N_ROWS, write=write, run_g15=True,
                                log=lambda m: print(m, file=sys.stderr, flush=True))


def g6_at(n: int) -> dict:
    import pilot
    t0 = time.time()
    with _patched() as PL:
        with PL.open_family("T33") as kit:
            b = pilot.build_pilot(kit, n, run_g15=False)
            g6, g7 = pilot.g6(b.infos), pilot.g7(b.infos)
            g10 = pilot.g10(b.infos, b.units, kit.plugin)
            out_dir = Path(PL.family_dir("T33"), OUT)
    cells = {}
    for part in ("yes_no", "choice"):
        p = g6.get(part) or {}
        if p.get("n"):
            cells[part] = {"n": p["n"], "chance": p["chance"],
                           "max": max((p[v][m], v, m) for v in p if isinstance(p[v], dict) and "lr" in p[v]
                                      for m in ("lr", "gbt"))}
    out = {"family": "T33", "n_rows": len(b.infos), "seconds": round(time.time() - t0), "seed_base": pilot.SEED_BASE,
           "G6_verdict": g6["verdict"], "G6_fails": g6["fails"], "G6_cells_max": cells,
           "G7_verdict": g7.get("verdict"), "G10_verdict": g10.get("verdict"),
           "G10_fails": {k: v for k, v in (g10.get("checks") or {}).items() if v.get("verdict") == "fail"},
           "dneg_supplement": D.read_supplement() is not None}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"G6_AT_{n}.json").write_text(json.dumps(out, indent=1, default=str))
    return out


def main(argv=None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:]) or ["run"]
    cmd = argv[0]
    if cmd == "determinism":
        procs = [subprocess.Popen([sys.executable, "-B", __file__, "dry"], stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True, env={**os.environ, "PYTHONHASHSEED": hs})
                 for hs in ("1", "4242")]
        outs = [json.loads(p.communicate()[0]) for p in procs]
        same = outs[0] == outs[1]
        print(json.dumps({"identical": same, "runs": outs}, indent=1))
        return 0 if same else 1
    if cmd == "g6":
        n = int(argv[argv.index("--n") + 1]) if "--n" in argv else 6000
        out = g6_at(n)
        print(json.dumps({k: out[k] for k in ("n_rows", "G6_verdict", "G7_verdict", "G10_verdict", "seconds")}))
        return 0
    rep = run(write=(cmd == "run"))
    if cmd == "dry":
        f = rep["files"]
        print(json.dumps({"rows_sha256": f["rows_sha256"], "relations_sha256": f["relations_sha256"],
                          "n_rows": f["n_rows"], "n_relations": f["n_relations"],
                          "mean_tokens": next((g for g in rep["gate_lines"] if g.startswith("spec_3_0")), "")[:90]}))
        return 0
    print(json.dumps({"summary": rep["summary"], "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
