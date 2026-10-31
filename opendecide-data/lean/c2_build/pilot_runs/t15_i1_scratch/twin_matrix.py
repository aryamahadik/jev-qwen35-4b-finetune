"""ch_outcome: base class distribution and base -> twin transitions (construction only, no rendering)."""
import sys, collections, json, time
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode = True
from concurrent.futures import ProcessPoolExecutor

def work(args):
    lo, hi = args
    import pilot_loaders as PL
    from families.T15 import plugin as T
    out = collections.Counter()
    with PL.open_family('T15') as kit:
        plugin = kit.plugin
        for seed in range(lo, hi):
            for smp in ('S1', 'S2', 'S3', 'S4'):
                if seed % 10 >= 6: continue
                if T._share(T.QFORM_SHARES['gates'], T._weyl(seed, smp, 1)) != 'ch_outcome': continue
                spec = plugin.sample(seed, smp)
                k = len(spec.structure['gates']); b = plugin.solve_a(spec)
                tw = None
                if T.uhash(T.FAMILY, 'twin', spec.sampler, spec.seed) < T.TWIN_RATE:
                    p = plugin._twin(spec)
                    tw = None if p is None else p.expect
                out[(k, b, tw)] += 1
    return {json.dumps(k): v for k, v in out.items()}

if __name__ == '__main__':
    lo, hi, nproc = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    step = max(1, (hi - lo) // (nproc * 3))
    chunks = [(a, min(a + step, hi)) for a in range(lo, hi, step)]
    tot = collections.Counter(); t0 = time.time()
    with ProcessPoolExecutor(nproc) as ex:
        for o in ex.map(work, chunks):
            for k, v in o.items(): tot[k] += v
    json.dump(tot, open(sys.argv[4], 'w'))
    print('specs', sum(tot.values()), round(time.time() - t0))
