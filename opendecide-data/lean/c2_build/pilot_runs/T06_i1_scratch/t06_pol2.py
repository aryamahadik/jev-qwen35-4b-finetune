import sys, collections
sys.dont_write_bytecode = True
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from families.T06 import freeze_v2 as FV, plugin as P
from c2_kit import polarity as PO
pools = FV.load_pools_v2()
ctx = FV.kit_ctx(pools)
NEG = (r"refus\w*", r"declin\w*", r"turn(?:s|ed|ing)? down", r"den(?:y|ies|ied|ying)", r"reject\w*", r"ineligible", r"unentitled")
for strict in (False, True):
    for negs in ((), NEG):
        n = 0; bad = []
        for sk in ctx.skins.values():
            if sk.kind != 'wording' or not sk.qform or not sk.qform.startswith('yn'): continue
            q = P.T06Plugin.QFORMS[sk.qform]
            pr = PO.problems(sk.text, q.polarity, base=0, negatives=negs, strict_frames=strict)
            n += 1
            if pr: bad.append((sk.qform, sk.text, pr))
        print('strict', strict, 'negs', bool(negs), 'n', n, 'flagged', len(bad))
        if (not strict) or negs:
            for b in bad: print('   ', b)
