"""t37b/run_pilot_i3.py: T37b rebuilt on A46-screened bases (A45 b, A46; orchestrator ruling 15 Oct): block into pilot_i3_full/.

Base eligibility: a base is eligible only if it is in replay_screen/reads/SCORE.json "agreed" (two blind Haiku reads equal the human
gold) and not in REPLAY_DENY_A46.json / REPLAY_UNSCREENED_A46.json; the pilot sample's bad bases (A45 b) stay denied;
the None-blind-base drop (builder.decide) and the blocked templates stay. No source is dropped whole (A46). --plan-seed
re-draws the plan (QC pooling for G6 at >= 5,000 rows, A43 a). Below is the i2 docstring.

(i2:) T37b final iteration (PREREG Ruling A45 b).

  cd lean/c2_build && nice -n 10 ../../.venv/bin/python -B -m t37b.run_pilot_i2   (never `python t37b/run_pilot_i2.py`: t37b/select.py would shadow the stdlib) [--screen noise_screen/replay_noise_scores.json]
                                                                              [--out pilot_i2_full] [--dry]

What changes against pilot_i1_full (drop only, never relabel, no bar loosened):
  1. builder.decide(): a base with no blind answer is dropped (the Claude review branch can no longer keep it).
  2. Templates above the 3% disagreement bar (the 9 of pilot_i1_full's G5-H quarantine plus the S13 base-read evidence,
     noise.screen_from_pilot) are blocked in select.plan_block; sources above 3% are dropped in select.eligible.
     The sample's own units that read badly (G5-H or the S13 base read) lose their bases (deny_ids). The pilot sample
     (1-13 units per source) cannot support a per-source drop (it would collapse the plan to 9 rows), so sources drop only
     from the replay noise screen: with --screen (noise_screen/score_reads.py) the screen's per-source rates decide
     (--source-stat not_clean | drop) and only bases whose two blind reads both equal the human gold may be bases
     (allow_ids), so a base with no blind answer cannot enter; its deny_ids are dropped as well.
  3. A44 (c): the budget is the realised block (the plan's own size); pilot_size is judged against the plan.
  4. The program gates (G2, G-TW, G15, S14, G6 on the full block, G7, G10) and the Haiku task files (G5-H: 100 rows x 2
     blind reads; S13 for the same 100 units) come from pilot_t37b.run unchanged.
Without --screen the block is PROVISIONAL: the replay noise screen has not been read yet, so no base has a blind
answer. Re-run with --screen after the Haiku reads are scored; its G5-H tasks replace the provisional ones.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                    # t37b/
C2 = HERE.parent
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))

import pilot as PI  # noqa: E402
import pilot_t37b as PT  # noqa: E402
from c2_kit import paths  # noqa: E402
from t37b import noise as NZ  # noqa: E402
from t37b import select as SEL  # noqa: E402

BASE_PILOT = HERE / "pilot_i1_full"


RS = C2 / "replay_screen"


def a46_sets():
    sc = json.loads((RS / "reads" / "SCORE.json").read_text(encoding="utf-8"))
    deny = set(json.loads((RS / "REPLAY_DENY_A46.json").read_text(encoding="utf-8"))["drop_ids"])
    uns = set(json.loads((RS / "REPLAY_UNSCREENED_A46.json").read_text(encoding="utf-8"))["drop_ids"])
    agreed = set(sc["agreed"])
    return agreed - deny - uns, deny | uns, {"n_agreed": len(agreed), "n_deny": len(deny), "n_unscreened": len(uns),
                                            "agreed_in_deny_or_unscreened": len(agreed & (deny | uns))}


def main(argv=None) -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="pilot_i3_full")
    ap.add_argument("--screen", default="", help="noise_screen/replay_noise_scores.json (score_reads.py output)")
    ap.add_argument("--dry", action="store_true", help="in memory, writes nothing")
    ap.add_argument("--source-stat", default="not_clean", choices=["not_clean", "drop"],
                    help="noise.sources_over_bar: not_clean (any read off the gold, abstentions included) or drop")
    ap.add_argument("--plan-seed", default="", help="override pilot_t37b.PLAN_SEED (QC pooling draws only)")
    ap.add_argument("--twin-balance", action="store_true",
                    help="W8 experiment (select.TWIN_BALANCE): entry-level equiv:complement ratio <= 2 per base gold; with the S14 10% source cap it leaves 10 viable sources and the plan collapses (t37b/_w8/W8_RESULT.json)")
    ap.add_argument("--n", type=int, default=2000, help="target (spec 5: 2,000); the realised block is smaller")
    a = ap.parse_args(argv)
    pilot_screen = NZ.screen_from_pilot(BASE_PILOT)
    screen = None
    a46_allow, a46_deny, a46_info = a46_sets()
    blocked = pilot_screen["blocked_templates"]
    dropped_src = []                                    # A46: no source is dropped whole
    allow = a46_allow
    deny = set(pilot_screen["bad_base_ids"]) | a46_deny
    applied = {"mode": "A46 agreed-only bases", "a46": a46_info, "plan_seed": a.plan_seed,
               "bar": NZ.BAR, "blocked_templates": blocked, "dropped_sources": dropped_src,
               "source_stat": a.source_stat, "pilot_sample_sources_over_bar": pilot_screen["sample_sources_over_bar"],
               "n_pilot_bad_bases_denied": len(pilot_screen["bad_base_ids"]), "n_deny_ids": len(deny), "n_allow_ids": None if allow is None else len(allow),
               "pilot_sample_sources": {s: d for s, d in pilot_screen["sources"].items()},
               "screen_file": "replay_screen/reads/SCORE.json + REPLAY_DENY_A46.json + REPLAY_UNSCREENED_A46.json"}
    orig_el, orig_pb = SEL.eligible, SEL.plan_block

    def el(*args, **kw):
        kw.update(deny_sources=dropped_src, deny_ids=deny, allow_ids=allow)
        return orig_el(*args, **kw)

    def pb(*args, **kw):
        kw["blocked_templates"] = blocked
        return orig_pb(*args, **kw)
    SEL.eligible, SEL.plan_block = el, pb
    SEL.TWIN_BALANCE = bool(a.twin_balance)              # W8 (off by default: infeasible under the S14 caps)
    if a.plan_seed:
        PT.PLAN_SEED = a.plan_seed
    try:
        rep = PT.run(a.n, write=not a.dry, run_g15=True, out_name=a.out)
    finally:
        SEL.eligible, SEL.plan_block = orig_el, orig_pb
        SEL.TWIN_BALANCE = False
    gates = rep["gates"]
    n_rows = rep["files"]["n_rows"]
    plan_n = gates["pilot_size"]["units_attempted"]
    ps = gates["pilot_size"]
    ps.update({"bar": "A44 (c) / A45 (b): the budget is the realised block (every planned unit that passes the program "
                      "gates is written; spec 5.3: shortfalls lower the total, never refilled)",
               "verdict": "pass" if n_rows == plan_n and n_rows > 0 else "fail",
               "realised_block": n_rows, "planned_units": plan_n, "spec_target": a.n,
               "note": "the 2,000 of spec 5 is not reachable (implicit-wording capacity, A44 c); a smaller plan only "
                       "follows from the A45 (b) drops"})
    rep["a46_screen"] = applied
    rep["summary"] = PI.summarize(gates)
    rep["gate_lines"] = PI.gate_lines(gates).split("\n")
    if not a.dry:
        out = HERE / a.out
        paths.write_json(out / "PILOT_REPORT.json", rep)
        paths.write_json(out / "A45_SCREEN_APPLIED.json", applied)
    print(json.dumps({"rows": n_rows, "planned": plan_n, "applied": {k: applied[k] for k in
                      ("mode", "blocked_templates", "dropped_sources", "n_deny_ids", "n_allow_ids")},
                      "gate_lines": rep["gate_lines"]}, indent=1)[:6000])
    return rep


if __name__ == "__main__":
    main()
