"""Exposure scan (no builds): for each full-generation family, what does gen_full_c2's exclusion step do to the kit?
Opens the family exactly as run() does (loader_patch + PL.open_family + quarantine_sources + apply_exclusions), then
reports skins removed, dead question forms, wording counts per live qform, whether the Redraw path would be on, and
how the plugin sets its choice display (plan_choice / build_options). CPU only.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HERE))

import gen_full_c2 as GF  # noqa: E402
import pilot_loaders as PL  # noqa: E402

FAMS = sys.argv[1:] or ["T01", "T28", "T33", "T24", "T31", "T26", "T06", "T15", "T23", "T12", "T07", "T32", "T25", "T27", "T30"]
out = {}
for fam in FAMS:
    try:
        src = GF.quarantine_sources(fam)
        banned = set().union(*map(set, src.values()))
        with GF.loader_patch(fam):
            with PL.open_family(fam) as kit0:
                kit, x = GF.apply_exclusions(kit0, banned)
                wq = Counter(s.qform for s in kit.ctx.skins.values() if s.kind == "wording" and not s.held_out and s.qform)
                wq0 = Counter(s.qform for s in kit0.ctx.skins.values() if s.kind == "wording" and not s.held_out and s.qform)
                plugin_src = (HERE / "families" / fam / "plugin.py").read_text()
                qf = getattr(kit.plugin, "QFORMS", {})
                out[fam] = {
                    "sources": {k: len(v) for k, v in src.items()}, "skins_removed": x["skins_removed"],
                    "removed_by_kind": x["removed_by_kind"], "dead_qforms": x["dead_qforms"],
                    "redraw_on": bool(x["dead_qforms"]) and fam not in GF.FALLBACK_FAMILIES,
                    "wordings_before": x["wordings_before"], "wordings_after": x["wordings_after"],
                    "wording_loss_by_qform": {q: [wq0[q], wq.get(q, 0)] for q in wq0 if wq.get(q, 0) != wq0[q]},
                    "min_wordings_live_qform": min(wq.values()) if wq else None,
                    "uses_plan_choice": "plan_choice" in plugin_src,
                    "uses_build_options": bool(re.search(r"build_options|build_closed", plugin_src)),
                    "choice_qforms": sorted(q for q, f in qf.items() if getattr(f, "qtype", None) == "choice"),
                    "n_qforms": len(qf)}
    except Exception as e:  # noqa: BLE001
        out[fam] = {"error": f"{type(e).__name__}: {e}"[:300]}
    print(fam, json.dumps({k: out[fam].get(k) for k in ("skins_removed", "dead_qforms", "redraw_on", "wording_loss_by_qform",
          "uses_plan_choice", "error")}, default=str)[:600], file=sys.stderr, flush=True)
(Path(__file__).parent / "exposure.json").write_text(json.dumps(out, indent=1, default=str))
