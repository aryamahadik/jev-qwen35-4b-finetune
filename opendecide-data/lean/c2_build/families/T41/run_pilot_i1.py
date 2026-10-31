"""families/T41/run_pilot_i1.py: the T41 pilot (C2_DATA_SPEC 6.4 steps 5-6), the same pattern as T28's run_pilot_i1.py.

T41 is a new family, so this runner registers its loader at RUNTIME (`pilot_loaders.LOADERS["T41"]`; pilot_loaders.py
is not edited) and adds T41 to the kit's family registry in memory (`c2_kit.plugin.FAMILIES["T41"] = "agent"`; kit
candidate, see BUILD_NOTES). The pilot then runs the same `pilot.run_family`, with the output folder redirected to
pilot_i1/. Program gates only: G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G6, G7, G10, overlay, spec 3.0.
G3-H and G5-H stay pending: Haiku task files are written, never answered here.

  ../../.venv/bin/python -B families/T41/run_pilot_i1.py --dry-run --n 1000      (from lean/c2_build; in memory)
  ../../.venv/bin/python -B families/T41/run_pilot_i1.py --dry-run --n 300 --no-g15
  ../../.venv/bin/python -B families/T41/run_pilot_i1.py                          (after A38: writes pilot_i1/)

Determinism: run it under two PYTHONHASHSEEDs and compare the printed rows_sha256 / relations_sha256.
"""
from __future__ import annotations

import argparse
import contextlib
import dataclasses
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402

OUT_NAME = "pilot_i1"


class _RedirectDir(type(Path())):
    """kit.dir whose `/ "pilot"` (pilot.run_family's output folder) is `/ pilot_i1` instead."""

    def __truediv__(self, key):
        if key == "pilot":
            return Path(str(self)) / OUT_NAME
        return super().__truediv__(key)


@contextlib.contextmanager
def open_t41():
    """The T41 loader: the plugin and KitCtx over the in-memory fixtures (Claude-written stand-ins; the Haiku pools replace
    them after A38, see haiku/)."""
    from families.T41 import fixtures as FX
    KP.FAMILIES.setdefault("T41", "agent")
    plugin, ctx = FX.make_plugin()
    yield PL.FamilyKit("T41", PL.family_dir("T41"), plugin, ctx, "families/T41/fixtures.py make_plugin() (in memory)",
                       "in-memory fixtures (no pool on disk)", ["fixture lexicon: 'fixture:*' extractors stand in for G-LEX"])


def register() -> None:
    PL.LOADERS["T41"] = open_t41


@contextlib.contextmanager
def _open_family_i1(fid, _orig=None):
    orig = _orig or _ORIG
    with orig(fid) as kit:
        yield dataclasses.replace(kit, dir=_RedirectDir(kit.dir))


_ORIG = PL.open_family


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=pilot.N_ROWS)
    ap.add_argument("--dry-run", action="store_true", help="in memory: write nothing")
    ap.add_argument("--no-g15", action="store_true", help="skip G15 (speed; never for the real pilot)")
    a = ap.parse_args(argv)
    register()
    PL.open_family = _open_family_i1                     # pilot.PL is this module object
    rep = pilot.run_family("T41", a.n, write=not a.dry_run, run_g15=not a.no_g15,
                           log=lambda m: print(m, file=sys.stderr, flush=True))
    print(json.dumps({"family": rep["family"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"], "n_rows": rep["files"]["n_rows"],
                      "summary": rep["summary"], "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
