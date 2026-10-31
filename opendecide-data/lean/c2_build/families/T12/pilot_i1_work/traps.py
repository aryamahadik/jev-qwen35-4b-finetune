"""scratch: trap / balance shares over sampled training specs under overridden constants."""
import sys, json, collections
sys.path.insert(0, '.')
sys.dont_write_bytecode = True
from families.T12 import plugin as P, fixtures as FX
ov = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
N = int(sys.argv[2]) if len(sys.argv) > 2 else 600
for k, v in ov.items():
    if k in ('LINES_W', 'QFORM_SHARES'): v = tuple(tuple(x) for x in v)
    setattr(P, k, v)
ctx = FX.ctx(); pl = P.T12Plugin(lexicon=ctx.lexicon)
specs = [pl.sample(sd, smp) for sd in range(N) for smp in ('S1', 'S2', 'S3', 'S4')]
tags = collections.Counter(t for s in specs for t in s.tags)
n = len(specs)
print({k: round(v / n, 3) for k, v in sorted(tags.items())})
print('lines', {k: round(v / n, 3) for k, v in sorted(collections.Counter(s.structure['n'] for s in specs).items())})
print('checks', {k: round(v / n, 3) for k, v in sorted(collections.Counter(len(s.structure['checks']) for s in specs).items())})
yn = [s for s in specs if s.qform.startswith('yn_')]
print('yn base', round(len(yn) / n, 3), 'yes', round(sum(pl.solve_a(s) for s in yn) / len(yn), 3))
