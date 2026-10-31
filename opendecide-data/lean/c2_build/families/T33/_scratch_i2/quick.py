import sys, json, collections, statistics
sys.path.insert(0,'.')
from families.T33 import plugin as T, fixtures as FX
from c2_kit import cards
ctx=FX.ctx(); pl=T.T33Plugin(lexicon=ctx.lexicon)
rows=[]
for seed in range(1000,1250):
    for smp in ("S1","S2","S3","S4"):
        sp=pl.sample(seed,smp); rows.append(pl.render(sp,ctx).row)
def rules(r):
    return cards.split_rules(r)[0]
mx,tok=cards._tokenizer()
c=lambda s: len(tok.encode(s or '',add_special_tokens=False).ids)
rep=cards.token_report(rows, rules_of=rules)
print(json.dumps(rep))
by=collections.defaultdict(list)
for r in rows: by[(r['qtype'],r['meta']['defs_style'][-5:])].append(c(rules(r)))
print({k:(len(v),round(statistics.mean(v))) for k,v in by.items()})
by=collections.defaultdict(list)
for r in rows: by[r['meta']['wording_id'][:0]+r['qtype']].append(c(r['state']))
print({k:round(statistics.mean(v)) for k,v in by.items()})
