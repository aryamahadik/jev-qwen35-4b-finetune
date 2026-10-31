import sys, random, collections
sys.dont_write_bytecode = True
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from families.T06 import fixtures as FX, plugin as T
ctx = FX.ctx(); pl = T.T06Plugin(lexicon=ctx.lexicon)
rng = random.Random('dbg')
cnt = collections.Counter(); sets = collections.Counter()
for i in range(2000):
    sc = pl._scenario(rng)
    base = pl._draw_base(rng, sc, 'act', 'X', 'S', rng.choice(T.N_REJ), rng.choice(T.N_WD))
    sh = T._shown_keys(base)
    sets[sh]+=1
    cnt[sum(k != 'none' for k in sh)] += 1
print(cnt)
for k,v in sets.most_common(12): print(v, k)
