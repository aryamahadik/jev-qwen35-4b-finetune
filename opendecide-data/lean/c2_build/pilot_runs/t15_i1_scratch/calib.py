"""Calibration of the ch_claimant plan (G0 v1.3): tally cells over many seeds (NOT the pilot's 900000 block)."""
import sys, collections, json, time
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode = True
from concurrent.futures import ProcessPoolExecutor

def work(args):
    lo, hi = args
    import pilot_loaders as PL
    from c2_kit import pipeline
    from families.T15 import plugin as T
    out = collections.Counter(); drops = collections.Counter()
    with PL.open_family('T15') as kit:
        plugin, ctx = kit.plugin, kit.ctx
        for seed in range(lo, hi):
            for smp in ('S1', 'S2', 'S3', 'S4'):
                card = seed % 10
                if card < 6: continue
                if T._share(T.QFORM_SHARES['claimants'], T._weyl(seed, smp, 1)) != 'ch_claimant': continue
                try:
                    spec = plugin.sample(seed, smp)
                except Exception as e:
                    drops['sample'] += 1; continue
                res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
                if not res.ok:
                    drops['unit'] += 1; continue
                for rr in res.rendered:
                    os_ = rr.option_set
                    k = len(os_.options); shown = os_.abstain_shown; gn = bool(os_.meta.get('gold_is_abstain'))
                    out[(rr.row['role'], k, shown, gn)] += 1
    return dict((("|".join(map(str, k))), v) for k, v in out.items()), dict(drops)

if __name__ == '__main__':
    lo, hi, nproc = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    step = (hi - lo) // (nproc * 4) or 1
    chunks = [(a, min(a + step, hi)) for a in range(lo, hi, step)]
    tot = collections.Counter(); dr = collections.Counter(); t0 = time.time()
    with ProcessPoolExecutor(nproc) as ex:
        for o, d in ex.map(work, chunks):
            for k, v in o.items(): tot[k] += v
            for k, v in d.items(): dr[k] += v
    print('drops', dict(dr), 'seconds', round(time.time() - t0))
    cells = collections.defaultdict(lambda: [0, 0]); roles = collections.defaultdict(lambda: [0, 0])
    for key, v in sorted(tot.items()):
        role, k, shown, gn = key.split('|'); k = int(k)
        c = cells[(k, shown)]; c[0] += v; c[1] += v if gn == 'True' else 0
        r = roles[role]; r[0] += v; r[1] += v if gn == 'True' else 0
    for (k, shown), (n, g) in sorted(cells.items()):
        print(f'k={k} shown={shown}: rows {n} gold_nobody {g} share {g / n:.3f}')
    for role, (n, g) in sorted(roles.items()):
        print(f'role {role}: rows {n} nobody {g}')
    allr = sum(v for v in tot.values()); print('total rows', allr)
    json.dump(tot, open('/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/pilot_runs/t15_i1_scratch/calib_last.json', 'w'))
