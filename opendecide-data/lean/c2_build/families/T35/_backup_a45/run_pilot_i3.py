"""families/T35/run_pilot_i3.py: the T35 pilot of fix iteration 3 (A44 a, d), written to pilot_i3/.

A copy of run_pilot_i1.py (same pilot.run_family code, seeds, gates and bars; nothing is loosened) with the output folder
renamed to pilot_i3/ and two additions:
  - the loader drops every form id listed for T35 in zed_orch/a43f_quarantine.json (the 20 yn_double_neg wordings) from the
    lexicon registry and their wording skins from the pool, in memory (A44 a: the pilot equals what full generation produces;
    no frozen pool file is edited). The plugin's double_neg_ok is recomputed, so the form falls back to yn_fetch (0% double
    negation, waived by A44 b).
  - --g6: the A43 run at a larger size (default 6,000 rows, G15 off) with pilot.g6 / g7 / g10 unchanged, written to
    pilot_i3/G6_AT_<n>.json.
It writes the program-gate PILOT_REPORT.json, rows, relations and the G5-H / G3-H task files; it answers none of them.

  cd lean/c2_build
  ../../.venv/bin/python -B families/T35/run_pilot_i3.py                       # the pilot, written to families/T35/pilot_i3/
  PYTHONHASHSEED=7 ../../.venv/bin/python -B families/T35/run_pilot_i3.py --dry-run   # in memory; prints the rows sha256
  ../../.venv/bin/python -B families/T35/run_pilot_i3.py --g6 --n 6000         # A43 G6 -> pilot_i3/G6_AT_6000.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from c2_kit import paths  # noqa: E402

FID = "T35"
OUT = "pilot_i3"
QUARANTINE = C2_BUILD / "zed_orch" / "a43f_quarantine.json"


def quarantined_forms() -> set:
    return set(json.loads(QUARANTINE.read_text(encoding="utf-8")).get(FID, []))


class _Redirect:
    """kit.dir stand-in: `kit.dir / "pilot"` (the only use in run_family) resolves to <family dir>/pilot_i3."""

    def __init__(self, real: Path):
        self.real = real

    def __truediv__(self, name):
        return self.real / (OUT if name == "pilot" else name)

    def __fspath__(self):
        return str(self.real)


def apply_quarantine(kit) -> list:
    """Remove the quarantined forms (and the wording skins that use them) from the loaded kit, in memory."""
    q = quarantined_forms()
    reg = kit.plugin.lexicon
    gone = sorted(f for f in q if f in reg.forms)
    for f in gone:
        del reg.forms[f]
    skins = kit.ctx.skins
    drop = [sid for sid, sk in skins.items() if set(getattr(sk, "lexicon_ids", ()) or ()) & q]
    for sid in drop:
        del skins[sid]
    kit.plugin.double_neg_ok = kit.plugin._clean_forms("yn_double_neg")
    kit.plugin._screened.clear()
    kit.notes.append(f"A44 a: {len(gone)} quarantined form(s) and {len(drop)} wording skin(s) removed in memory")
    return gone


def install_loader() -> None:
    orig = PL.LOADERS[FID]

    def loader():
        cm = orig()

        class _Cm:
            def __enter__(self):
                kit = cm.__enter__() if hasattr(cm, "__enter__") else next(cm)
                kit.dir = _Redirect(kit.dir)
                apply_quarantine(kit)
                return kit

            def __exit__(self, *e):
                return cm.__exit__(*e)
        return _Cm()

    PL.LOADERS[FID] = loader


def g6_at_size(n: int = 6000, out: Path = None, log=print) -> dict:
    """A43 G6 at >= 5,000 rows: the same build, pilot.g6 / g7 / g10, as zed_orch/g6_at_size.py, with this loader."""
    t0 = time.time()
    with PL.open_family(FID) as kit:
        b = PI.build_pilot(kit, n, run_g15=False)
        g6, g7, g10 = PI.g6(b.infos), PI.g7(b.infos), PI.g10(b.infos, b.units, kit.plugin)
        out = Path(out) if out else Path(str(kit.dir.real)) / OUT
    cells = {}
    for part in ("yes_no", "choice"):
        p = g6.get(part) or {}
        if p.get("n"):
            cells[part] = {"n": p["n"], "chance": p["chance"],
                           "max": max((p[v][m], v, m) for v in p if isinstance(p[v], dict) and "lr" in p[v]
                                      for m in ("lr", "gbt"))}
    res = {"family": FID, "n_rows": len(b.infos), "seconds": round(time.time() - t0), "seed_base": PI.SEED_BASE,
           "G6_verdict": g6["verdict"], "G6_fails": g6["fails"], "G6_cells_max": cells,
           "G6_all_views": {part: {v: g6[part][v] for v in g6[part] if isinstance(g6[part][v], dict)}
                            for part in ("yes_no", "choice") if g6.get(part, {}).get("n")},
           "G7_verdict": g7.get("verdict"), "G10_verdict": g10.get("verdict"),
           "G10_fails": {k: v for k, v in (g10.get("checks") or {}).items() if v.get("verdict") == "fail"}}
    paths.write_json(out / f"G6_AT_{n}.json", res)
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true", help="in memory only: write nothing")
    ap.add_argument("--no-g15", action="store_true")
    ap.add_argument("--g6", action="store_true", help="A43 G6 at --n rows (default 6000) -> pilot_i3/G6_AT_<n>.json")
    a = ap.parse_args(argv)
    log = lambda m: print(m, file=sys.stderr, flush=True)  # noqa: E731
    install_loader()
    if a.g6:
        res = g6_at_size(a.n or 6000, log=log)
        print(json.dumps({k: res[k] for k in ("family", "n_rows", "G6_verdict", "G6_cells_max", "G7_verdict",
                                              "G10_verdict", "seconds")}))
        return 0 if res["G6_verdict"] == "pass" else 3
    rep = PI.run_family(FID, a.n or PI.N_ROWS, write=not a.dry_run, run_g15=not a.no_g15, log=log)
    print(json.dumps({"summary": rep["summary"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"], "n_rows": rep["files"]["n_rows"],
                      "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
