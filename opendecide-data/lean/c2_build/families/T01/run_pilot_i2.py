"""families/T01/run_pilot_i2.py: the T01 pilot of fix iteration 2 (C2_DATA_SPEC 6.4 steps 5-6; ROUND2_BRIEF), written to pilot_i2/.

A copy of run_pilot_i1.py with output folder pilot_i2/ (pilot/ and pilot_i1/ stay untouched) and two additions:
  - the pool loader also reads the frozen double-negation supplement pools_v2/dneg_i2_supplement.json when it exists
    (dneg_i2.make_ctx_i2 replaces freeze_v2.make_ctx for the run; pilot_loaders.py is not edited, and the supplement's
    freeze record sha-checks the frozen pool files). Without the supplement the run is the frozen pools, as in iteration 1.
  - `g6`: the A43 run at a larger size (default 6,000 rows, G15 off) with pilot.g6 / g7 / g10 unchanged, written to
    pilot_i2/G6_AT_<n>.json (zed_orch/g6_at_size.py builds from the unpatched loader, so it cannot see the supplement).
The same code as pilot.run_family otherwise: the program gates G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G6, G7, G10,
overlay, spec 3.0, and the G5-H / G3-H task files (written, never answered here). No Haiku, no model, no network.

  ../../.venv/bin/python -B families/T01/run_pilot_i2.py run              (from lean/c2_build) write pilot_i2/
  ../../.venv/bin/python -B families/T01/run_pilot_i2.py dry              in memory; prints rows / relations sha256
  ../../.venv/bin/python -B families/T01/run_pilot_i2.py determinism      dry under PYTHONHASHSEED 1 and 4242, compare
  ../../.venv/bin/python -B families/T01/run_pilot_i2.py g6 [--n 6000]    G6 / G7 / G10 at size -> pilot_i2/G6_AT_6000.json
"""
from __future__ import annotations

import contextlib
import dataclasses
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

from families.T01 import dneg_i2 as D  # noqa: E402  (captures freeze_v2.make_ctx before the patch below)
from families.T01 import freeze_v2 as FV  # noqa: E402

OUT = "pilot_i2"


class _RedirectDir(type(Path())):
    """kit.dir whose `/ "pilot"` (pilot.run_family's output folder) is `/ pilot_i2` instead."""

    def __truediv__(self, key):
        if key == "pilot":
            return Path(str(self)) / OUT
        return super().__truediv__(key)


@contextlib.contextmanager
def _patched():
    import pilot_loaders as PL
    real_open, real_ctx = PL.open_family, FV.make_ctx

    @contextlib.contextmanager
    def patched(fid):
        with real_open(fid) as kit:
            yield dataclasses.replace(kit, dir=_RedirectDir(kit.dir))
    PL.open_family, FV.make_ctx = patched, D.make_ctx_i2
    try:
        yield PL
    finally:
        PL.open_family, FV.make_ctx = real_open, real_ctx


def run(write: bool, n: int | None = None) -> dict:
    import pilot
    with _patched():
        return pilot.run_family("T01", n or pilot.N_ROWS, write=write, run_g15=True,
                                log=lambda m: print(m, file=sys.stderr, flush=True))


def g6_at(n: int) -> dict:
    import pilot
    t0 = time.time()
    with _patched() as PL:
        with PL.open_family("T01") as kit:
            b = pilot.build_pilot(kit, n, run_g15=False)
            g6, g7 = pilot.g6(b.infos), pilot.g7(b.infos)
            g10 = pilot.g10(b.infos, b.units, kit.plugin)
            out_dir = Path(PL.family_dir("T01"), OUT)
    cells = {}
    for part in ("yes_no", "choice"):
        p = g6.get(part) or {}
        if p.get("n"):
            cells[part] = {"n": p["n"], "chance": p["chance"],
                           "max": max((p[v][m], v, m) for v in p if isinstance(p[v], dict) and "lr" in p[v]
                                      for m in ("lr", "gbt"))}
    out = {"family": "T01", "n_rows": len(b.infos), "seconds": round(time.time() - t0), "seed_base": pilot.SEED_BASE,
           "G6_verdict": g6["verdict"], "G6_fails": g6["fails"], "G6_cells_max": cells,
           "G7_verdict": g7.get("verdict"), "G10_verdict": g10.get("verdict"),
           "G10_fails": {k: v for k, v in (g10.get("checks") or {}).items() if v.get("verdict") == "fail"},
           "G10_double_negation_share": (g10.get("checks") or {}).get("double_negation_share"),
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
                          "n_rows": f["n_rows"], "n_relations": f["n_relations"]}))
        return 0
    print(json.dumps({"summary": rep["summary"], "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
