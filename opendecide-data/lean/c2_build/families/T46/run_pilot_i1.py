"""families/T46/run_pilot_i1.py: the T46 pilot / loader driver (C2_DATA_SPEC 6.4 steps 5-6), same pattern as T28 / T45.

pilot.py writes a family's pilot to <family dir>/pilot/; this driver runs the same `pilot.run_family` with the output
folder redirected to pilot_i1/ and registers the T46 loader at RUNTIME (pilot_loaders.LOADERS["T46"]; pilot_loaders.py
is not edited). gen_full_c2.py imports this module for its loader patch (RUNNER["T46"] = ("run_pilot_i1", 1)): the
import registers the loader, so the full generation opens T46 over the frozen pools.

The loader reads the FROZEN pools (families/T46/pools/, written by haiku_author.freeze) and refuses to run without them.
The in-memory stand-ins of fixtures.py are for tests and dry runs only (--standin, or T46_STANDIN=1 for gen_full_c2).

  ../../.venv/bin/python -B families/T46/run_pilot_i1.py --dry-run --n 300 --standin   (from lean/c2_build)
Determinism: run it under two PYTHONHASHSEEDs and compare rows_sha256.
"""
from __future__ import annotations

import argparse
import contextlib
import dataclasses
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402

OUT_NAME = "pilot_i1"
STANDIN = os.environ.get("T46_STANDIN") == "1"


class _RedirectDir(type(Path())):
    def __truediv__(self, key):
        if key == "pilot":
            return Path(str(self)) / OUT_NAME
        return super().__truediv__(key)


@contextlib.contextmanager
def _t46():
    from families.T46 import haiku_author as HA
    from families.T46 import plugin as P
    if STANDIN:
        plugin, ctx = P.make_plugin()
        pools = "in code (fixtures.py stand-ins; tests and dry runs only)"
        notes = ["stand-in pools admitted by 'program:stand-in-N' extractions; NOT the frozen Haiku pools"]
    else:
        if not HA.frozen_pools_exist():
            raise RuntimeError("T46: no frozen Haiku pools in families/T46/pools/ (run haiku_author admit); "
                               "T46_STANDIN=1 / --standin is for tests and dry runs only")
        plugin, ctx = HA.load_plugin()
        pools = "families/T46/pools/ (frozen Haiku pools, admitted 2/2)"
        notes = [f"pool manifest sha256 {HA.pools_manifest_sha()[:16]}"]
    yield PL.FamilyKit("T46", PL.family_dir("T46"), plugin, ctx, "families/T46/plugin.make_plugin() / haiku_author.load_plugin()",
                       pools, notes)


PL.LOADERS["T46"] = _t46


@contextlib.contextmanager
def _open_family_i1(fid):
    with PL.LOADERS[fid]() as kit:
        yield dataclasses.replace(kit, dir=_RedirectDir(kit.dir))


def main(argv=None) -> int:
    global STANDIN
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=pilot.N_ROWS)
    ap.add_argument("--dry-run", action="store_true", help="in memory: write nothing")
    ap.add_argument("--no-g15", action="store_true", help="skip G15 (speed; never for the real pilot)")
    ap.add_argument("--standin", action="store_true", help="use the fixtures.py stand-in pools (tests only)")
    a = ap.parse_args(argv)
    STANDIN = a.standin or STANDIN
    PL.open_family = _open_family_i1
    rep = pilot.run_family("T46", a.n, write=not a.dry_run, run_g15=not a.no_g15,
                           log=lambda m: print(m, file=sys.stderr, flush=True))
    print(json.dumps({"family": rep["family"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"], "n_rows": rep["files"]["n_rows"],
                      "summary": rep["summary"], "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
