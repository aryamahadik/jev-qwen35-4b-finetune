import sys, collections, json
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode=True
import pilot_loaders as PL
from families.T33 import plugin as T
N=int(sys.argv[1]) if len(sys.argv)>1 else 3000
with PL.open_family('T33') as kit:
    plugin=kit.plugin
    avail=collections.Counter(); base=collections.Counter(); n_sp=collections.Counter()
    for seed in range(900000, 900000+N):
        for smp in ('S1','S2','S3','S4'):
            spec=plugin.sample(seed, smp)
            n_sp[spec.qform]+=1
            norm=lambda x: x if (isinstance(x,int) or x in ('none','supported','contradicted','not_shown') or str(x).startswith('crit.')) else 'item'
            a=norm(plugin.solve_a(spec))
            base[(spec.qform, a)]+=1
            t=plugin._twin(spec)
            if t is not None:
                avail[(spec.qform, norm(t.expect), a)]+=1
    out={}
    for q in sorted(n_sp):
        av=collections.Counter()
        for k,v in avail.items():
            if k[0]==q: av[str(k[1])]+=v
        out[q]={'n':n_sp[q], 'avail_by_twin_gold':dict(av), 'base_gold':{str(k[1]):v for k,v in base.items() if k[0]==q},
                'avail_by_base_gold':{str(g):sum(v for k,v in avail.items() if k[0]==q and k[2]==g) for g in {k[1] for k in base if k[0]==q}}}
    print(json.dumps(out, indent=1))
