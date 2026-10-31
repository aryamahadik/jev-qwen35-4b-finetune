"""Spec-level simulation of the emitted rows (base + complement + twin + equiv + inv), no rendering: used to tune the
twin keep rates, P_TWIN and the question shares. Usage: emit.py N_SEEDS [out.json]"""
import sys, collections, json, time
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode=True
import pilot_loaders as PL
from families.T33 import plugin as T

def cls(q, a):
    if q in ('ch_bad_claim',): return 'none' if a=='none' else 'item'
    return a

def run(plugin, N, seed0=900000):
    rows=[]   # (qform, role, gold_class, k, sampler, sub, checks tuple)
    t0=time.time()
    for seed in range(seed0, seed0+N):
        for smp in ('S1','S2','S3','S4'):
            spec=plugin.sample(seed, smp)
            st=spec.structure
            g=plugin.solve_a(spec)
            def row(q, role, gold, sp):
                k=None; checks=None
                if q=='ch_failed_check':
                    checks=tuple(sp.structure['checks']); k=len(checks)+1
                elif q=='ch_bad_claim': k=len(sp.structure['claims'])+1
                elif q=='ch_claim_verdict': k=3
                rows.append((q, role, cls(q,gold), k, smp, st['sub'], checks))
            row(spec.qform,'base',g,spec)
            for p in plugin.relations(spec):
                if p.kind=='complement':
                    row(p.qform,'complement', plugin.solve_a(spec.replace(qform=p.qform)), spec)
                elif p.kind=='twin':
                    row(spec.qform,'twin', plugin.solve_a(plugin.derive(p.spec)), p.spec)
                elif p.kind=='equiv':
                    row(spec.qform,'equiv', g, spec)
                elif p.kind=='inv':
                    row(spec.qform,'attack', g, spec)
    return rows, time.time()-t0

def report(rows, plugin):
    n=len(rows)
    out={'rows':n}
    roles=collections.Counter(r[1] for r in rows)
    out['roles']={k:round(v/n,4) for k,v in roles.items()}
    yn=[r for r in rows if plugin.QFORMS[r[0]].qtype=='noul']
    out['yn_share']=round(len(yn)/n,4)
    out['yes_rate']=round(sum(r[2] for r in yn)/len(yn),4)
    # per-form yes rate and twin yes rate
    pf={}
    for q in plugin.QFORMS:
        s=[r for r in yn if r[0]==q]
        if s:
            tw=[r for r in s if r[1]=='twin']
            pf[q]={'n':len(s),'yes':round(sum(r[2] for r in s)/len(s),3),'twin_n':len(tw),'twin_yes':round(sum(r[2] for r in tw)/max(1,len(tw)),3)}
    out['per_form']=pf
    # yes is bad
    yb=[r for r in yn if plugin.QFORMS[r[0]].yes_is_bad]
    out['yes_is_bad_share']=round(len(yb)/len(yn),4)
    # verdict
    v=[r for r in rows if r[0]=='ch_claim_verdict']
    c=collections.Counter(r[2] for r in v); out['verdict']={k:round(x/len(v),3) for k,x in c.items()}
    vt=[r for r in v if r[1]=='twin']; c=collections.Counter(r[2] for r in vt); out['verdict_twin']={k:round(x/len(vt),3) for k,x in c.items()}
    # abstain by k
    for q in ('ch_bad_claim','ch_failed_check'):
        sub=[r for r in rows if r[0]==q]
        d=collections.defaultdict(lambda:[0,0])
        for r in sub:
            d[r[3]][0]+=1; d[r[3]][1]+= (r[2]=='none')
        out['abstain_'+q]={k:[v[0], round(v[1]/v[0],3), round(1/k,3)] for k,v in sorted(d.items())}
    # fcc gold by check type vs expected
    fcc=[r for r in rows if r[0]=='ch_failed_check']
    shown=collections.Counter(); gold=collections.Counter(); exp=collections.Counter()
    for r in fcc:
        opts=list(r[6])+['none']
        for o in opts:
            exp[o]+=1/len(opts)
            shown[o]+=1
        gold[r[2]]+=1
    out['fcc']={o:[shown[o], gold[o], round(exp[o],1), round(gold[o]-exp[o],1), round((gold[o]-exp[o])/shown[o],3)] for o in shown}
    out['sub_a_share']=round(sum(1 for r in rows if r[5]=='a')/n,4)
    return out

if __name__=='__main__':
    N=int(sys.argv[1])
    with PL.open_family('T33') as kit:
        rows, dt = run(kit.plugin, N)
        rep=report(rows, kit.plugin); rep['seconds']=round(dt)
        print(json.dumps(rep, indent=1))
