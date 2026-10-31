"""transfer/T21/run_pilot_i1.py: the T21 pilot after fix iteration 1 (PILOT_VERDICT FIX-1 to FIX-8), written to pilot_i1/.

c2_build/pilot.py always writes to <family dir>/pilot/ (the first pilot, kept as evidence) and draws the training
samplers round robin. This wrapper runs the very same code (pilot.run_family: same seed base, loader, gates and bars;
nothing is loosened) with two changes that need no edit of pilot.py:
  - the output folder is renamed to pilot_i1/, so the first pilot's files stay untouched;
  - FIX-5: the draw order follows plugin.SAMPLER_SEED_WEIGHTS (S4 takes 0.85 of the seeds of each of S1-S3; plugin
    .sampler_schedule), and each sampler's seeds stay consecutive from SEED_BASE (the label-first seed blocks stay whole).
    build_pilot reads plugin.SAMPLERS for its round robin, so the schedule is put on the plugin INSTANCE for the run
    (the class tuple, which pack_for reads, is unchanged) and removed afterwards.
It writes the program-gate PILOT_REPORT.json, rows, relations and the G5-H / G3-H task files; it answers none of them
(Haiku answers come later; A37 b).

  cd lean/c2_build
  ../../.venv/bin/python -B transfer/T21/run_pilot_i1.py                      # the pilot, written to transfer/T21/pilot_i1/
  PYTHONHASHSEED=7 ../../.venv/bin/python -B transfer/T21/run_pilot_i1.py --dry-run   # in memory; prints the rows sha256
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from transfer.T21 import plugin as P  # noqa: E402

OUT = "pilot_i1"
_ORIG_BUILD = PI.build_pilot


class _Redirect:
    """kit.dir stand-in: `kit.dir / "pilot"` (the only use in run_family) resolves to <family dir>/pilot_i1."""

    def __init__(self, real: Path):
        self.real = real

    def __truediv__(self, name):
        return self.real / (OUT if name == "pilot" else name)

    def __fspath__(self):
        return str(self.real)


def build_weighted(kit, n_rows: int = PI.N_ROWS, *, seed_base: int = PI.SEED_BASE, run_g15: bool = True,
                   max_attempts: int | None = None, log=None):
    """pilot.build_pilot with the draw order of plugin.sampler_schedule(plugin.SAMPLER_SEED_WEIGHTS)."""
    plugin = kit.plugin
    train = [s for s in type(plugin).SAMPLERS if s not in plugin.HELD_OUT_SAMPLERS]
    sched = P.sampler_schedule(plugin.SAMPLER_SEED_WEIGHTS, samplers=tuple(train))
    counters = collections.Counter()
    real_sample = plugin.sample

    def sample(_seed, sampler):                       # the draw's place in the schedule is not its seed: per sampler
        n = counters[sampler]
        counters[sampler] += 1
        return real_sample(seed_base + n, sampler)

    plugin.SAMPLERS = tuple(sched) + tuple(s for s in type(plugin).SAMPLERS if s in plugin.HELD_OUT_SAMPLERS)
    plugin.sample = sample
    try:
        b = _ORIG_BUILD(kit, n_rows, seed_base=seed_base, run_g15=run_g15, max_attempts=max_attempts, log=log)
    finally:
        plugin.__dict__.pop("sample", None)
        plugin.__dict__.pop("SAMPLERS", None)
    b.stats["training_samplers"] = train
    b.stats["seeds_per_sampler"] = dict(sorted(counters.items()))
    b.stats["sampler_seed_weights"] = dict(plugin.SAMPLER_SEED_WEIGHTS)
    b.stats["sampler_schedule_cycle"] = "".join(s[-1] for s in sched)
    return b


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=PI.N_ROWS)
    ap.add_argument("--dry-run", action="store_true", help="in memory only: write nothing")
    ap.add_argument("--no-g15", action="store_true")
    a = ap.parse_args(argv)
    orig = PL.open_family

    def open_family(fid):
        cm = orig(fid)

        class _Cm:
            def __enter__(self):
                kit = cm.__enter__()
                kit.dir = _Redirect(kit.dir)
                return kit

            def __exit__(self, *e):
                return cm.__exit__(*e)
        return _Cm()

    PL.open_family = open_family
    PI.build_pilot = build_weighted
    rep = PI.run_family("T21", a.n, write=not a.dry_run, run_g15=not a.no_g15,
                        log=lambda m: print(m, file=sys.stderr, flush=True))
    print(json.dumps({"summary": rep["summary"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"], "n_rows": rep["files"]["n_rows"],
                      "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
