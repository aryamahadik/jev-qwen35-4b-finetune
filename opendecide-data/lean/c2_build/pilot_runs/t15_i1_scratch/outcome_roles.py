"""ch_outcome gold shares by role (base / twin / equiv / attack), by option, over many seeds (not the pilot block)."""
import sys, collections, json, time
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode = True
from concurrent.futures import ProcessPoolExecutor

def work(args):
    lo, hi = args
    import pilot_loaders as PL
    from c2_kit import pipeline
    from families.T15 import plugin as T
    out = []
    with PL.open_family('T15') as kit:
        plugin, ctx = kit.plugin, kit.ctx
        for seed in range(lo, hi):
            for smp in ('S1', 'S2', 'S3', 'S4'):
                if seed % 10 >= 6: continue
                if T._share(T.QFORM_SHARES['gates'], T._weyl(seed, smp, 1)) != 'ch_outcome': continue
                spec = plugin.sample(seed, smp)
                res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
                if not res.ok: continue
                for r in res.rows:
                    gold_key = 'eligible' if r['gold'] == 'Eligible' else 'fail_' + r['gold'].split('Gate ')[1][0]
                    out.append((r['role'], len(r['options']), gold_key, r['meta']['twin_kind']))
    return out

if __name__ == '__main__':
    lo, hi, nproc = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    step = (hi - lo) // (nproc * 3) or 1
    chunks = [(a, min(a + step, hi)) for a in range(lo, hi, step)]
    rows = []; t0 = time.time()
    with ProcessPoolExecutor(nproc) as ex:
        for o in ex.map(work, chunks): rows += o
    print('rows', len(rows), round(time.time() - t0))
    by = collections.defaultdict(lambda: collections.Counter())
    for role, k, g, _ in rows: by[role][(k, g == 'eligible')] += 1
    for role, c in sorted(by.items()):
        n = sum(c.values()); e = sum(v for (k, ge), v in c.items() if ge)
        print(role, 'rows', n, 'eligible share', round(e / n, 3), 'mean 1/k', round(sum(v / k for (k, ge), v in c.items()) / n, 3))
    n = len(rows); e = sum(g == 'eligible' for _, _, g, _ in rows); m = sum(1 / k for _, k, _, _ in rows) / n
    print('ALL eligible share', round(e / n, 3), 'mean 1/k', round(m, 3))
    for k in (3, 4, 5):
        ss = [(r, g) for r, kk, g, _ in rows if kk == k]
        print('k', k, 'rows', len(ss), 'eligible', round(sum(g == 'eligible' for _, g in ss) / len(ss), 3), 'want', round(1 / k, 3),
              {g: round(sum(1 for _, x in ss if x == g) / len(ss), 3) for g in ('eligible', 'fail_A', 'fail_B', 'fail_C', 'fail_D')})
