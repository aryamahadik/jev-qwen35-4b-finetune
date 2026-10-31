"""zed_orch/t27_fix_r2/overlay.py: run the T27 generator with the G11 fix round 2 WITHOUT editing families/T27 (a G13 run guards
families/T27/plugin.py and pools_v2/ until it ends; install_code.py makes the same two changes on disk afterwards).

  with overlay.patched():            # before gen_full_c2.run / g6_a50_full.build / pilot code opens the family
      ...
does two things, each switched by a flag:
  balance   wording_balance.apply(T27Plugin) once the family kit is open: ctx_for / _pick_wording become the least-loaded
            pick (wording_balance.py). Held-out (S5) picks are unchanged.
  wordings  pools_v2.read_pools is wrapped so the frozen pools also hold the new ch_next and yn_beyond training wordings and
            their lexicon forms (admitted_wordings.json, written by redo5.py glex-check --record after the 2/2 G-LEX reads). This is the
            same chain run_pilot_i2._install_supplement and gen_full_c2._install_t27_g13_filter use, so the G13-seed filter
            and the A43 f / G5-H exclusions still apply to the merged pools. No file is written; none is edited.
Nothing else changes: the G13-seed exclusions, the quarantines and every gate are the ones gen_full_c2 applies.
"""
from __future__ import annotations

import contextlib
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
sys.dont_write_bytecode = True

import pilot_loaders as PL  # noqa: E402
import wording_balance as WB  # noqa: E402

ADMITTED = HERE / "admitted_wordings.json"


def admitted() -> dict | None:
    return json.loads(ADMITTED.read_text(encoding="utf-8")) if ADMITTED.is_file() else None


def _wrap_read_pools(extra: dict) -> None:
    PV = importlib.import_module("families.T27.pools_v2")
    if getattr(PV, "_r2_wrapped", False):
        PV._r2_extra = extra
        return
    orig = PV.read_pools
    PV._r2_extra = extra

    def read_pools(*a, **k):
        pools = orig(*a, **k)
        ex = getattr(PV, "_r2_extra", None)
        if ex and ex.get("wordings"):
            have = {r["piece_id"] for r in pools["wordings"]}
            have_f = {f["form_id"] for f in pools["lexicon"]["forms"]}
            if have & {r["piece_id"] for r in ex["wordings"]} or have_f & {f["form_id"] for f in ex["forms"]}:
                raise SystemExit("overlay: the pools already hold a redo5 wording (merged on disk?): drop the overlay")
            pools = dict(pools)
            pools["wordings"] = list(pools["wordings"]) + list(ex["wordings"])
            pools["lexicon"] = {**pools["lexicon"], "forms": list(pools["lexicon"]["forms"]) + list(ex["forms"])}
        return pools
    PV.read_pools = read_pools
    PV._r2_wrapped = True


@contextlib.contextmanager
def patched(balance: bool = True, wordings: bool = True, extra: dict | None = None):
    """extra: the admitted_wordings payload (default: admitted_wordings.json if it exists, else no new wordings)."""
    extra = extra if extra is not None else (admitted() if wordings else None)
    if extra:
        _wrap_read_pools(extra)
    orig = PL.open_family
    notes = []

    @contextlib.contextmanager
    def opened(fid):
        with orig(fid) as kit:
            if fid == "T27":
                if balance:
                    P = importlib.import_module("families.T27.plugin")
                    WB.apply(P.T27Plugin)
                    notes.append("G11 fix r2: least-loaded wording pick (wording_balance.py)")
                if extra and extra.get("wordings"):
                    by_q = sorted({r["qform"] for r in extra["wordings"]})
                    notes.append(f"G11 fix r2: {len(extra['wordings'])} new training wordings (" + ", ".join(
                        f"{q} {sum(1 for r in extra['wordings'] if r['qform'] == q)}" for q in by_q) + ") (redo5)")
                kit.notes = list(kit.notes) + notes
            yield kit

    PL.open_family = opened
    try:
        yield
    finally:
        PL.open_family = orig
        PV = sys.modules.get("families.T27.pools_v2")
        if PV is not None:
            PV._r2_extra = None
