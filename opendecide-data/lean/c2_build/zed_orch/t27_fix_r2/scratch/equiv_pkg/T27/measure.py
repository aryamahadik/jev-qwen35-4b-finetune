"""families/T27/measure.py: in-memory balance and length measurement for the T27 fixes (writes nothing).

Builds relation units through pipeline.build_unit (G15 off for speed; the pilot runs it) over the training samplers and
prints, for the rows that passed: the choice-row gold counts by row role, the gold position and gold-is-longest
share (the G10 checks), the card styles, the control share, the yes/no share, and the real-tokenizer length report
(c2_kit.cards.token_report). Used to tune the sampler before a pilot; the pilot gates (pilot.py) are the record.

  ../../.venv/bin/python -B families/T27/measure.py [--rows 1200] [--seed-base 900000] > out.txt   (from lean/c2_build)
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
for p in (C2_BUILD, C2_BUILD / "families" / "T27"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import run_pilot as RP  # noqa: E402
from c2_kit import cards as CD  # noqa: E402
from c2_kit import pipeline  # noqa: E402
from c2_kit.choiceplan import chi2_uniform_p  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=1200)
    ap.add_argument("--seed-base", type=int, default=900000)
    ap.add_argument("--no-tokens", action="store_true")
    ap.add_argument("--choice-only", action="store_true", help="build only ch_next units (faster cue analysis)")
    ap.add_argument("--dump", default="", help="write the built rows to this jsonl (analysis only)")
    a = ap.parse_args(argv)
    rows, tags = [], Counter()
    with RP._t27() as kit:
        plugin, ctx = kit.plugin, kit.ctx
        train = [s for s in plugin.SAMPLERS if s not in plugin.HELD_OUT_SAMPLERS]
        k = 0
        while len(rows) < a.rows:
            smp, seed = train[k % len(train)], a.seed_base + k // len(train)
            k += 1
            spec = plugin.sample(seed, smp)
            if a.choice_only and spec.qform != "ch_next":
                continue
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            if not res.ok:
                tags["dropped:" + ",".join(sorted({g for g, _ in res.problems}))] += 1
                continue
            rows += res.rows
    if a.dump:
        Path(a.dump).write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    ch = [r for r in rows if r["qtype"] == "choice"]
    yn = [r for r in rows if r["qtype"] == "noul"]
    from families.T27.plugin import OPTION_TEXT
    key = {v: k_ for k_, v in OPTION_TEXT.items()}
    out = {"rows": len(rows), "units_dropped": dict(tags), "yes_no_share": round(len(yn) / len(rows), 4),
           "yes_rate": round(sum(r["gold"] for r in yn) / max(1, len(yn)), 4)}
    out["choice_gold"] = dict(Counter(key[r["gold"]] for r in ch))
    out["choice_gold_share"] = {k_: round(v / len(ch), 4) for k_, v in out["choice_gold"].items()}
    out["by_twin_kind"] = {t: dict(Counter(key[r["gold"]] for r in ch if str(r["meta"]["twin_kind"]) == t))
                           for t in sorted({str(r["meta"]["twin_kind"]) for r in ch})}
    pos = Counter(r["options"].index(r["gold"]) for r in ch)
    out["gold_position"] = dict(sorted(pos.items()))
    out["gold_position_chi2_p"] = chi2_uniform_p([pos[i] for i in range(3)])
    longest = sum(1 for r in ch if len(r["gold"]) == max(len(o) for o in r["options"]))
    out["gold_is_longest_pp"] = round(100 * (longest / len(ch) - 1 / 3), 2)
    out["defs_styles"] = dict(Counter(r["meta"]["defs_style"] for r in rows))
    out["twin_kinds"] = dict(Counter(r["meta"]["twin_kind"] for r in rows))
    if not a.no_tokens:
        rep = CD.token_report(rows)
        out["tokens"] = {k_: rep[k_] for k_ in ("counted_by", "mean", "max", "after_placement", "rules_ratio_needed",
                                                "rules_mean", "pass")}
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
