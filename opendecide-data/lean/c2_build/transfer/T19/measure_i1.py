"""transfer/T19/measure_i1.py: in-memory balance and length measurement for the T19 fix iteration 1 (writes nothing).

Builds relation units through pilot.build_pilot (the pilot's own seeds, G15 off for speed; the pilot runs it) over the
training samplers and prints, for the rows that passed: the row shares the fixes aim at (yes/no, twins, equiv, abstain gold,
verdict golds by row role), the card styles, the spec 3.0 length report (c2_kit.cards.token_report, the pinned tokenizer) and the
pilot's own G10 / overlay / spec_3_0 checks. --g6 / --g7 add the partial-input and feature gates (slow; at the pilot's seeds and
at larger n they show which features are real). Used to tune the sampler before a pilot; the pilot gates (pilot.py) are the record.

  cd lean/c2_build
  ../../.venv/bin/python -B transfer/T19/measure_i1.py [--rows 2000] [--seed-base 900000] [--g6] [--g7]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from c2_kit import cards as CD  # noqa: E402
from c2_kit.choiceplan import plan_report  # noqa: E402


def measure(n_rows: int = 2000, seed_base: int = PI.SEED_BASE, *, g6: bool = False, g7: bool = False) -> dict:
    with PL.open_family("T19") as kit:
        b = PI.build_pilot(kit, n_rows, seed_base=seed_base, run_g15=False, log=lambda *_: None)
        plugin = kit.plugin
        infos = b.infos
        rows = [i.row for i in infos]
        n = len(rows)
        role = Counter(r["role"] for r in rows)
        yn = [r for r in rows if r["qtype"] == "noul"]
        ch = [r for r in rows if r["qtype"] == "choice"]
        vd = [r for r in ch if r["meta"]["qform"] == "ch_verdict"]
        out = {"rows": n, "units": b.stats["units_written"], "yes_no_share": round(len(yn) / n, 4),
               "roles": dict(role), "twin_share": round(role["twin"] / n, 4),
               "equiv_share": round(role["equiv"] / n, 4), "qform": dict(Counter(r["meta"]["qform"] for r in rows)),
               "twin_by_qform": dict(Counter(r["meta"]["qform"] for r in rows if r["role"] == "twin"))}
        # ch_verdict golds over all rows and over bases alone
        gold = Counter(r["gold"] for r in vd)
        gold_b = Counter(r["gold"] for r in vd if r["role"] == "base")
        out["ch_verdict"] = {"rows": len(vd), "gold": dict(gold),
                             "gold_share": {k: round(v / len(vd), 4) for k, v in sorted(gold.items())},
                             "base_gold_share": {k: round(v / max(1, sum(gold_b.values())), 4)
                                                 for k, v in sorted(gold_b.items())}}
        sets = [i.rr.option_set for i in infos if i.rr is not None and i.rr.option_set is not None]
        out["plan_report"] = plan_report(sets)
        out["card_styles"] = CD.style_report(rows)
        out["tokens"] = CD.token_report(rows)
        out["G10"] = PI.g10(infos, b.units, plugin)["checks"]
        out["overlay"] = {k: v["value"] for k, v in PI.overlay(b.units, plugin)["checks"].items()}
        out["spec_3_0"] = {k: v["value"] for k, v in PI.spec30(infos, plugin)["checks"].items()
                           if k in ("max_tokens", "mean_tokens", "mode_f_share", "deep_share")}
        if g6:
            out["G6"] = PI.g6(infos)
        if g7:
            out["G7"] = PI.g7(infos)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=2000)
    ap.add_argument("--seed-base", type=int, default=PI.SEED_BASE)
    ap.add_argument("--g6", action="store_true")
    ap.add_argument("--g7", action="store_true")
    a = ap.parse_args(argv)
    print(json.dumps(measure(a.rows, a.seed_base, g6=a.g6, g7=a.g7), indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
