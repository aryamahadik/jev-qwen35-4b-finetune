"""Calibrate OUTCOME_ELIGIBLE / OUTCOME_W so every ch_outcome option is gold on 1/k of the ROWS (twins and copies included)."""
import sys, collections, json, time
import numpy as np
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode = True
from concurrent.futures import ProcessPoolExecutor
EPS = 0.13

def work(args):
    lo, hi, elig, w = args
    import pilot_loaders as PL
    from families.T15 import plugin as T
    T.OUTCOME_ELIGIBLE = {int(k): v for k, v in elig.items()}
    T.OUTCOME_W = {int(k): tuple(v) for k, v in w.items()}
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

def measure(lo, hi, nproc, elig, w):
    step = max(1, (hi - lo) // (nproc * 3))
    chunks = [(a, min(a + step, hi), elig, w) for a in range(lo, hi, step)]
    cnt = collections.Counter()
    with ProcessPoolExecutor(nproc) as ex:
        for o in ex.map(work, chunks):
            for k, v in o.items():
                kg, b, tw = json.loads(k); cnt[(kg, b, tw)] += v
    return cnt

def analyse(cnt, kg):
    classes = ['eligible'] + [f'fail_{"ABCD"[i]}' for i in range(kg)]
    n = len(classes)
    base = np.array([sum(v for (g, b, t), v in cnt.items() if g == kg and b == c) for c in classes], float)
    r = base / base.sum()
    tau = np.zeros(n); T = np.zeros((n, n))
    for i, c in enumerate(classes):
        ex = {t: sum(v for (g, b, t2), v in cnt.items() if g == kg and b == c and t2 == t) for t in classes}
        tot_ex = sum(ex.values()); tau[i] = tot_ex / base[i]
        for j, t in enumerate(classes): T[i, j] = ex[t] / tot_ex if tot_ex else 0
    def mix(q):
        row = q * (1 + EPS) + (q * tau) @ T
        return row / row.sum()
    q = np.ones(n) / n
    for _ in range(1000):
        m = mix(q); q = q * (1 / n) / m; q /= q.sum()
    return classes, r, mix(r), q, int(base.sum())

if __name__ == '__main__':
    lo, hi, nproc, iters = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    from families.T15 import plugin as T0
    elig = dict(T0.OUTCOME_ELIGIBLE); w = {k: list(v) for k, v in T0.OUTCOME_W.items()}
    for it in range(iters):
        t0 = time.time()
        a = lo + it * (hi - lo)
        cnt = measure(a, a + (hi - lo), nproc, elig, w)
        print(f'--- iteration {it} seeds {a}-{a + hi - lo} ({round(time.time() - t0)} s)')
        newe, neww = {}, {}
        for kg in (2, 3, 4):
            classes, r, m, q, n = analyse(cnt, kg)
            print(f' gates {kg} specs {n}: realised base {dict(zip(classes, np.round(r, 3)))}')
            print(f'    mixture {dict(zip(classes, np.round(m, 3)))}  want {round(1 / len(classes), 3)}')
            print(f'    solved q {dict(zip(classes, np.round(q, 3)))}')
            newe[kg] = float(q[0])
            ww = np.array(w[kg], float) * (q[1:] / np.maximum(r[1:], 1e-6)) ** 0.9
            neww[kg] = list(ww / ww.sum())
            # keep the relative scale of W (only ratios matter among avail)
        elig, w = newe, neww
        print(' params', json.dumps({'elig': {k: round(v, 3) for k, v in elig.items()}, 'w': {k: [round(x, 3) for x in v] for k, v in w.items()}}))
