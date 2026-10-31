import sys
sys.dont_write_bytecode=True
sys.path.insert(0,'/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from c2_kit import pipeline
from families.T06 import fixtures as FX, plugin as T
ctx=FX.ctx(); pl=T.T06Plugin(lexicon=ctx.lexicon)
bad=0; tot=0
for seed in range(300):
    for smp in pl.SAMPLERS:
        spec=pl.sample(seed,smp)
        if spec.qform not in T.END_FORMS: continue
        tot+=1
        res=pipeline.build_unit(pl, spec, ctx, run_g15=False)
        if not res.ok:
            bad+=1
            if bad<=3:
                print(seed,smp,spec.qform,res.problems[:2])
                for rp in pl.relations(spec):
                    print('  ', rp.kind, getattr(rp,'note',None))
print('ch_end specs',tot,'bad',bad)
print('----')
for seed, smp in ((29,'S4'),(91,'S2')):
    spec=pl.sample(seed,smp)
    print(seed, smp, spec.qform, T.facts(spec).delivered, T.facts(spec).possession, T.facts(spec).requested, T.facts(spec).n_rej, T.facts(spec).n_wd)
    print('  base opts', pl._end_options(spec) is not None)
    for rp in pl.relations(spec):
        if rp.kind=='metamorphic':
            sp=rp.spec
            o=pl._end_options(pl.derive(sp)) if sp is not None else 'nospec'
            print('  ', rp.note, 'ok' if o not in (None,) else 'NONE', sp.seed if sp is not None else None, T.facts(sp).delivered if sp is not None else None)
print('====')
from c2_kit.distractors import build_options
spec=pl.sample(29,'S4')
key=pl.row_key(spec)
for sp in (spec, [rp for rp in pl.relations(spec) if rp.kind=='metamorphic' and 'shift' in rp.note][0].spec):
    sp=pl.derive(sp)
    ans=pl.solve_a(sp); f=T.facts(sp)
    print(f.possession, ans)
    for m in pl.error_models(): 
        try:
            r=m.fn(sp) if hasattr(m,'fn') else None
        except Exception as e: r=repr(e)
        print('   ', getattr(m,'name',m), r)
    print(' plan', pl.end_plan(key))
    os_=build_options(sp, ans, pl.error_models(), row_key=key, render_key=lambda x:x, order_key=str, plan=pl.end_plan(key), strict_plan=False)
    print(' ', None if os_ is None else [(o.key,o.err) for o in os_.options])
