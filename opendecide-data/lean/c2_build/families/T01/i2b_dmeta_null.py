"""Diagnostic: (1) permutation null of the choice d_meta LR (gold position re-drawn uniformly within each row, same
folds) to size the CV noise of this cell; (2) cluster-aware (deduped by card + option set) k-stratified association of
the row-level features with the gold position.   ../../.venv/bin/python -B families/T01/i2b_dmeta_null.py [file.json]"""
import json
import random
import sys
from collections import Counter

_src = open(__file__.replace("i2b_dmeta_null.py", "i2b_dmeta_ablate.py")).read().split('res = {"chance"')[0]
exec(compile(_src, "ablate_head", "exec"))   # defines rows, cv(), strat_chi(), CATS ... (no analysis run)

out = {"full": cv()}
orig = [r["gold"] for r in rows]
nulls = []
for s in range(6):
    rng = random.Random(s)
    for r, g in zip(rows, orig):
        r["gold"] = rng.randrange(r["k"])
    nulls.append(cv())
for r, g in zip(rows, orig):
    r["gold"] = g
out["null_acc"] = nulls
out["null_mean"] = round(sum(nulls) / len(nulls), 4)
out["null_sd"] = round((sum((x - out["null_mean"]) ** 2 for x in nulls) / (len(nulls) - 1)) ** 0.5, 4)
# dedupe: one row per (card, option tuple, gold position)
seen, ded = set(), []
for r in rows:
    key = (r["card"], tuple(r["opts"]), r["gold"])
    if key not in seen:
        seen.add(key)
        ded.append(r)
out["n_rows"], out["n_distinct_card_options_gold"] = len(rows), len(ded)
out["rows_per_card"] = round(len(rows) / len({r["card"] for r in rows}), 2)
full_rows = rows
rows[:] = ded
st = []
for c in CATS:
    x, dof = strat_chi(lambda r, c=c: r["cat"][c])
    st.append({"feature": c, "chi2": round(x, 1), "dof": dof, "chi2_per_dof": round(x / dof, 2) if dof else None})
out["dedup_k_strat_pos_assoc"] = sorted(st, key=lambda d: -(d["chi2_per_dof"] or 0))
rows[:] = full_rows
(OUT / "DMETA_NULL.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
