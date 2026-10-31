import sys, json, time, math
from collections import Counter, defaultdict
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
import pilot_t37b as P
from t37b import select as SEL, sources as SRC
pool = P.load_pool()
inp = P.load_inputs()
bases, rep = SEL.eligible(inp["rows"], inp["rels"], old_ids=inp["old_ids"], old_groups=inp["old_groups"], old_states=inp["old_states"], status=P.status_fn(inp["deny"]))
print('eligible', len(bases))
for tgt,(nc,ne) in (("pilot",(700,300)),("full",(1400,600))):
  for bal in (True, False):
    t=time.time()
    plan, r = SEL.plan_block(bases, n_complement=nc, n_equiv=ne, seed="t37b-pilot-1", equiv_pool=pool.choices(), balance=bal)
    yr = r.get("partner_yes_rate")
    print(tgt, 'balance',bal, 'rows',len(plan), 'kinds',r['kinds'], 'basis',r['basis'],'passes',r['passes'], 'yes',round(yr,4), 'imp',round(r['implicit_share'],3),'nonsyn',round(r['non_syntactic_share'],3),'pass',r['pass'], round(time.time()-t,1),'s')
    if bal:
        # per (entry,kind) and wording cells
        cell=defaultdict(lambda:[0,0]); wc=defaultdict(lambda:[0,0])
        for i in plan:
            sd=SEL._side(i.base,i.kind)
            cell[(i.base.entry.key,i.kind)][sd]+=1
            wc[SEL._wording_cell(i.base,i.kind,i.frame,i.cue,i.variant,i.meta)][sd]+=1
        print(' cells max |diff|', max(abs(a-b) for a,b in cell.values()), 'wording cells max |diff|', max(abs(a-b) for a,b in wc.values()), 'n wording cells', len(wc))
        print(' src', dict(Counter(i.base.row['source'] for i in plan).most_common(5)))
        print(' by kind yes-rate', {k: round(sum(SEL._side(i.base,i.kind) for i in plan if i.kind==k)/max(1,sum(1 for i in plan if i.kind==k)),3) for k in SRC.KINDS})
