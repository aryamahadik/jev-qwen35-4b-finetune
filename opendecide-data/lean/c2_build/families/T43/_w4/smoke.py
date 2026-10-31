import sys, time, collections
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
import pilot
from families.T43 import plugin as P
plugin, ctx = P.make_plugin()
n = int(sys.argv[1]); sm = sys.argv[2]
t0 = time.time(); cnt = collections.Counter(); fails = 0
for k in range(n):
    seed = pilot.SEED_BASE + 777_000 + k
    try:
        spec = plugin.sample(seed, sm)
        rr = plugin.render(spec, ctx)
    except Exception as e:
        fails += 1; print('FAIL', seed, type(e).__name__, str(e)[:150]); continue
    st = spec.structure
    cnt[(st['template'] if st['kind']=='line' else st['template'], rr.row['gold'][:6])] += 1
print(sm, n, 'fails', fails, 'sec', round(time.time()-t0,1), dict(P.DIAG))
print(rr.row['state'][-420:] if len(sys.argv)>3 else '')
