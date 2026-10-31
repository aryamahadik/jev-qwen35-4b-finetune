"""Block-phase dry run of mix_c2 (W6 task B): admission, provisional per-block selection, the plan, apply_targets and the A49 (c)
assertions on the rows the block phase holds. Stops before the replay draw (its inputs do not exist yet). Reads only; writes
zed_orch/block_phase_dry.json. Token counts are rows.approx_tokens (chars/3, conservative), not the tokenizer.

    python -B zed_orch/block_phase_dry.py      (from c2_build)
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import mix_c2 as m  # noqa: E402
from c2_kit import rows as R  # noqa: E402

ilog = m.MixInputLog(m.load_never_train(None, None))
rep, probs = {}, []
entered = m.admit_blocks(ilog, [], rep)
HYP = "--all-on-disk" in sys.argv        # what-if: every non-carry block with candidates on disk, QC pass ignored (provisional selection)
if HYP:
    entered = [b for b in m.TARGETS if b not in m.CARRY and m.c2io.fam_files(b)["cand"].exists()]
    rep["entry"]["left_out"] = {b: ["no candidates on disk"] for b in m.TARGETS if b not in entered}
blocks, parts = {}, {}
for b in entered:
    try:
        br, brel, par, bpool, bparts = m.load_block(ilog, b, False, rep, probs)
    except SystemExit as e:
        rep["entry"]["left_out"][b] = [f"{b}: {e}"]
        continue
    blocks[b], parts[b] = (br, brel), bparts
plan = m.plan_shares({b: len(v[0]) for b, v in blocks.items()}) if blocks else {}
rows = [r for v in blocks.values() for r in v[0]]
rels = [x for v in blocks.values() for x in v[1]]
if blocks:
    rows, rels, cap = m.apply_targets(rows, rels, plan["targets"], parts)
    ntok = {r["id"]: R.approx_tokens(r) for r in rows}
    a49, ap = m.a49c_assert(rows, rels, ntok)
    capr, cp = m.cap_checks(rows, ntok, False)
else:
    a49, ap, capr, cp = {}, [], {}, []
left = rep["entry"]["left_out"]
out = {"hypothetical_all_on_disk": HYP, "admitted": sorted(blocks), "left_out": {b: v[:3] for b, v in left.items()}, "plan": plan.get("targets"),
       "rows_after_apply_targets": dict(Counter(r["_block"] for r in rows)),
       "a49c_binding_problems": ap, "a49c_by_block": {b: {"binding": v["binding"], "failing": v["failing"]} for b, v in a49.items()},
       "cap_problems": cp, "load_problems": probs}
Path(HERE / "zed_orch" / ("block_phase_dry_hyp.json" if HYP else "block_phase_dry.json")).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
print(json.dumps({k: out[k] for k in ("admitted", "rows_after_apply_targets")}))
print("A49c binding problems:", len(ap)); [print("  ", x[:230]) for x in ap[:40]]
print("cap problems:", len(cp)); [print("  ", x[:200]) for x in cp[:15]]
print("left out (sample):", {b: v[0][:90] for b, v in list(left.items())[:40]})
