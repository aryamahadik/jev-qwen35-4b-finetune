import sys, collections
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode = True
import pilot_loaders as PL
from families.T15 import plugin as T
from c2_kit.distractors import build_closed
N = int(sys.argv[1])
with PL.open_family('T15') as kit:
    plugin = kit.plugin
    tot = collections.defaultdict(lambda: [0.0, 0.0, 0]); byfield = collections.defaultdict(lambda: [0, 0.0]); bypos = collections.defaultdict(lambda: [0, 0.0])
    elig = collections.defaultdict(lambda: [0, 0]); n = 0
    for seed in range(200000, 200000 + N):
        for smp in ('S1', 'S2', 'S3', 'S4'):
            if seed % 10 >= 6: continue
            if T._share(T.QFORM_SHARES['gates'], T._weyl(seed, smp, 1)) != 'ch_outcome': continue
            spec = plugin.sample(seed, smp)
            gates = tuple(spec.structure['gates'])
            ans = plugin.solve_a(spec)
            keys = [T.ELIGIBLE] + [f"fail_{T.LETTERS[i]}" for i in range(len(gates))]
            os_ = build_closed(spec, ans, keys, plugin.error_models(), row_key='x', render_key=lambda k: T.outcome_text(k, gates))
            texts = [o.text for o in os_.options]; lens = [len(t) for t in texts]
            top = [j for j, x in enumerate(lens) if x == max(lens)]
            gi = os_.gold_index
            a = tot[len(gates)]; a[0] += (1 / len(top)) if gi in top else 0; a[1] += 1 / len(texts); a[2] += 1
            elig[len(gates)][0] += ans == 'eligible'; elig[len(gates)][1] += 1
            # which option is the longest and was it gold, by field label
            f_long = [T.FIELDS[gates[T.LETTERS.index(os_.options[j].key[-1])]].fid for j in top if os_.options[j].key != 'eligible']
            for j, o in enumerate(os_.options):
                if o.key == 'eligible': continue
                fid = gates[T.LETTERS.index(o.key[-1])]
                byfield[fid][0] += 1; byfield[fid][1] += 1 / len(texts) * 0 + (j == gi)
            n += 1
    print('specs', n)
    for k, a in sorted(tot.items()): print('gates', k, 'rows', a[2], 'longest pp', round(100 * (a[0] - a[1]) / a[2], 2), 'eligible share', round(elig[k][0] / elig[k][1], 3), 'want', round(1 / (k + 1), 3))
    allp = sum(a[0] - a[1] for a in tot.values()) / sum(a[2] for a in tot.values()); print('overall longest pp', round(100 * allp, 2))
    for fid, (c, g) in sorted(byfield.items()): print(fid, 'options', c, 'gold rate', round(g / c, 3))
