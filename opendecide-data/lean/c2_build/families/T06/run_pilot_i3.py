"""families/T06/run_pilot_i3.py: the T06 pilot of fix iteration 3 (A44 a), written to pilot_i3/.

A copy of run_pilot_i2.py with the output folder pilot_i3 and one loader change: the wordings of the T06 forms listed in
zed_orch/a43f_quarantine.json (A43 f: double negation under a negated frame) are excluded from the kit context, so the
pilot equals what full generation produces. pilot_loaders.py is not edited.

  ../../.venv/bin/python -B families/T06/run_pilot_i3.py                      (from lean/c2_build)
  ../../.venv/bin/python -B families/T06/run_pilot_i3.py --dry-run            (in memory, prints the sha256s)
  ../../.venv/bin/python -B families/T06/run_pilot_i3.py --dry-run --n 6000 --no-g15 --g6-json <file>

Determinism: run it under two PYTHONHASHSEEDs and compare the printed rows_sha256 / relations_sha256.
"""
from __future__ import annotations

import argparse
import contextlib
import dataclasses
import importlib.util
import json
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402

OUT_NAME = "pilot_i3"
QUARANTINE = frozenset(json.loads((C2_BUILD / "zed_orch" / "a43f_quarantine.json").read_text())["T06"])


def _load_run_pilot():
    spec = importlib.util.spec_from_file_location("t06_run_pilot", Path(__file__).with_name("run_pilot.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _drop_quarantined(ctx):
    """The kit context without the wording skins of a quarantined form (by skin id or by any of its lexicon form ids)."""
    skins = {k: s for k, s in ctx.skins.items()
             if not (s.kind == "wording" and (k in QUARANTINE or QUARANTINE.intersection(s.lexicon_ids or ())))}
    return dataclasses.replace(ctx, skins=skins)


def _write_g6_at(rep: dict, path: str, seconds: int) -> None:
    """The fields zed_orch/g6_at_size.py writes, from the in-memory run's own G6 / G7 / G10 (same functions, same bars)."""
    g = rep["gates"]
    g6, g7, g10 = g["G6"], g["G7"], g["G10"]
    cells = {}
    for part in ("yes_no", "choice"):
        p = g6.get(part) or {}
        if p.get("n"):
            cells[part] = {"n": p["n"], "chance": p["chance"],
                           "max": max((p[v][m], v, m) for v in p
                                      if isinstance(p[v], dict) and "lr" in p[v] for m in ("lr", "gbt"))}
    out = {"family": "T06", "n_rows": rep["files"]["n_rows"], "seconds": seconds, "seed_base": pilot.SEED_BASE,
           "G6_verdict": g6["verdict"], "G6_fails": g6["fails"], "G6_cells_max": cells,
           "G7_verdict": g7.get("verdict"), "G10_verdict": g10.get("verdict"),
           "G10_fails": {k: v for k, v in (g10.get("checks") or {}).items() if v.get("verdict") == "fail"}}
    Path(path).write_text(json.dumps(out, indent=1, default=str))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=pilot.N_ROWS)
    ap.add_argument("--dry-run", action="store_true", help="in memory: write nothing")
    ap.add_argument("--no-g15", action="store_true", help="skip G15 (speed; never for the real pilot)")
    ap.add_argument("--g6-json", default=None,
                    help="dry-run only: write the G6/G7/G10 result (g6_at_size.py fields) to this file")
    a = ap.parse_args(argv)
    RP = _load_run_pilot()
    orig = RP._t06

    @contextlib.contextmanager
    def _t06_i3():
        with orig() as kit:
            yield dataclasses.replace(kit, ctx=_drop_quarantined(kit.ctx))

    RP._t06 = _t06_i3                                             # RP._redirect binds it as its default loader
    PL.LOADERS["T06"] = _t06_i3
    PL.open_family = RP._redirect(OUT_NAME)                       # pilot.PL is this module object
    t0 = time.time()
    rep = pilot.run_family("T06", a.n, write=not a.dry_run, run_g15=not a.no_g15,
                           log=lambda m: print(m, file=sys.stderr, flush=True))
    if a.g6_json:
        _write_g6_at(rep, a.g6_json, round(time.time() - t0))
    print(json.dumps({"family": rep["family"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"], "n_rows": rep["files"]["n_rows"],
                      "summary": rep["summary"], "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
