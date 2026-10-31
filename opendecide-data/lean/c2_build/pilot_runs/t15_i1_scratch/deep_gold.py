import sys, collections
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode = True
import pilot_loaders as PL
from families.T15 import plugin as T
with PL.open_family('T15') as kit:
    plugin = kit.plugin
    c = collections.Counter()
    for seed in range(300000, 304000):
        for smp in ('S1', 'S2', 'S3', 'S4'):
            spec = plugin.sample(seed, smp)
            if spec.qform not in T.TRACK_OF or plugin.QFORMS[spec.qform].qtype != 'noul': continue
            g = plugin.solve_a(spec)
            c[(spec.structure['track'], bool(spec.deep), spec.qform in ('yn_eligible','yn_dneg_eligible','yn_may_claim','yn_dneg_claim'), g)] += 1
    for track in ('gates', 'claimants'):
        for deep in (False, True):
            for pos in (True, False):
                y = c[(track, deep, pos, 1)]; n = y + c[(track, deep, pos, 0)]
                print(track, 'deep', deep, 'positive-form' if pos else 'complement', 'n', n, 'gold yes', round(y / max(1, n), 3))
