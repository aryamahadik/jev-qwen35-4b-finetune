"""families/T06/run_pilot.py: the T06 pilot driver (C2_DATA_SPEC 6.4 steps 5-6), with T06's own pool loader.

T06 had no pilot loader in pilot_loaders.py, and other family leads edit that shared file in parallel, so the loader
lives here and is registered into `pilot_loaders.LOADERS` in this process only (no shared file is edited). It follows
the loader order that freeze_v2.py documents:

    pools = freeze_v2.load_pools_v2()     MANIFEST.json verified (every file's sha256 and size); refuses a SHORT freeze
    ctx = freeze_v2.kit_ctx(pools)        Mode T skins, admitted Mode F documents (thinned to <= 25%), attack lines, one
                                          wording skin per admitted form, G-LEX registry rebuilt from lexicon.json
    with freeze_v2.wired_plugin(pools):   swaps plugin.STORES / CUSTOMERS / ITEMS / JURIS / JURIS_HELD for the pack data
        T06Plugin(lexicon=ctx.lexicon)

pilot.py writes a family's pilot to <family dir>/pilot/. `--out pilot` (the default) is iteration 0, `--out pilot_i1`
is fix iteration 1 (the same `pilot.run_family`: the same build, gates, G5-H / G3-H task files and report, only the
output folder redirected). Program gates only: G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G6, G7, G10,
overlay, spec 3.0. G3-H and G5-H stay pending: the task files are written, never answered here.

  ../../.venv/bin/python -B families/T06/run_pilot.py --out pilot       (from lean/c2_build; iteration 0)
  ../../.venv/bin/python -B families/T06/run_pilot.py --out pilot_i1    (fix iteration 1)
  add --dry-run to run in memory (nothing written); run under two PYTHONHASHSEEDs and compare the sha256s.
"""
from __future__ import annotations

import argparse
import contextlib
import dataclasses
import importlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402


@contextlib.contextmanager
def _t06():
    P = importlib.import_module("families.T06.plugin")
    FV = importlib.import_module("families.T06.freeze_v2")
    pools = FV.load_pools_v2()                                    # sha-checked; refuses a SHORT freeze
    ctx = FV.kit_ctx(pools)
    with FV.wired_plugin(pools):
        yield PL.FamilyKit("T06", PL.family_dir("T06"), P.T06Plugin(lexicon=ctx.lexicon), ctx,
                           "freeze_v2.load_pools_v2() (sha-checked) / kit_ctx(); with wired_plugin(pools): "
                           "T06Plugin(lexicon=ctx.lexicon)", "pools_v2/",
                           ["plugin.STORES / CUSTOMERS / ITEMS / JURIS / JURIS_HELD are swapped for the pack data "
                            "while the pilot runs and restored on exit"])


def _redirect(out_name: str):
    class _RedirectDir(type(Path())):
        """kit.dir whose `/ "pilot"` (pilot.run_family's output folder) is `/ <out_name>` instead."""

        def __truediv__(self, key):
            if key == "pilot":
                return Path(str(self)) / out_name
            return super().__truediv__(key)

    @contextlib.contextmanager
    def open_family(fid, _orig=_t06):
        with _orig() as kit:
            yield dataclasses.replace(kit, dir=_RedirectDir(kit.dir))
    return open_family


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=pilot.N_ROWS)
    ap.add_argument("--out", default="pilot", help="output folder under families/T06 (pilot or pilot_i1)")
    ap.add_argument("--dry-run", action="store_true", help="in memory: write nothing")
    ap.add_argument("--no-g15", action="store_true", help="skip G15 (speed; never for the real pilot)")
    a = ap.parse_args(argv)
    PL.LOADERS["T06"] = _t06
    PL.open_family = _redirect(a.out)                             # pilot.PL is this module object
    rep = pilot.run_family("T06", a.n, write=not a.dry_run, run_g15=not a.no_g15,
                           log=lambda m: print(m, file=sys.stderr, flush=True))
    print(json.dumps({"family": rep["family"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"], "n_rows": rep["files"]["n_rows"],
                      "summary": rep["summary"], "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
