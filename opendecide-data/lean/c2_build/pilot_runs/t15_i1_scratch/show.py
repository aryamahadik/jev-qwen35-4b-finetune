import sys, json
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode = True
import pilot_loaders as PL
from c2_kit import pipeline
want = sys.argv[1:]
with PL.open_family('T15') as kit:
    plugin, ctx = kit.plugin, kit.ctx
    shown = set()
    for seed in range(0, 400):
        spec = plugin.sample(seed, 'S4' if seed % 2 else 'S1')
        key = (spec.qform, spec.sampler)
        if spec.qform not in want or key in shown: continue
        shown.add(key)
        rr = plugin.render(spec, ctx)
        r = rr.row
        print('=====', spec.qform, spec.sampler, r['meta']['defs_style'], 'gold', r['gold'])
        print('--state--'); print(r['state']); print('--card--'); print(r['card']); print('--instructions--'); print(r['instructions']); print('--options--', r['options'])
