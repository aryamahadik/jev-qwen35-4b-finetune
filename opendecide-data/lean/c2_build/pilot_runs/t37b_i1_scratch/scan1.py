import sys, json, random
from collections import defaultdict
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
import pilot_t37b as P
from t37b import select as SEL, builder as BL, sources as SRC
pool = P.load_pool(); inp = P.load_inputs(lambda *_: None)
bases, rep = SEL.eligible(inp["rows"], inp["rels"], old_ids=inp["old_ids"], old_groups=inp["old_groups"], old_states=inp["old_states"], status=P.status_fn(inp["deny"]))
plan, r = SEL.plan_block(bases, n_complement=1400, n_equiv=600, seed="t37b-pilot-1", equiv_pool=pool.choices())
cands = BL.build_candidates(plan, records=pool.records)
print(len(plan), sum(c.ok for c in cands))
by = defaultdict(list)
for c in cands:
    by[(c.item.base.entry.key, c.item.kind)].append(c)
random.seed(3)
for (e,k), cs in sorted(by.items()):
    if k=='equiv': 
        for c in random.sample(cs, min(2,len(cs))): print(f"[{e} {k}] {c.item.base.row['instructions'][:110]}  ==>  {c.question[:130]}")
        continue
    for c in random.sample(cs, min(2,len(cs))):
        print(f"[{e} {k}] {c.item.base.row['instructions'][:110]}  ==>  {c.question[:150]}")
