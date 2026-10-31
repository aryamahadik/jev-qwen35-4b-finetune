"""Yes/no accuracy, abstain-zone share (0.2<P<0.8), false-Yes/false-No per frame (dev_negwords, dev_claims) and per source
(pg_dev, hard_dev) for 4B-E, the 2B pilot and the 2B REF v11r (full-trained 2B). Read-only; dev splits only."""
import collections, json, os
L = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/'
M = ['q35_4b_pxE', 'q35_2b_armI_1600', 'q35_2b_v11r']
load = lambda p: {json.loads(l)['id']: json.loads(l)['probs'] for l in open(p)} if os.path.exists(p) else {}
for split in ['dev_negwords', 'dev_claims', 'pg_dev', 'hard_dev']:
    P = {m: load(f'{L}preds_{split}/{m}.jsonl') for m in M}
    acc = collections.defaultdict(collections.Counter)
    for l in open(f'{L}data/{split}.jsonl'):
        r = json.loads(l)
        if r['qtype'] != 'noul':
            continue
        w = r['instructions'].split()
        fr = r['source'] if split in ('pg_dev', 'hard_dev') else ('Jo: ...' if w[0].startswith('Jo') else ' '.join(w[:3]))
        for k in (fr, 'ALL'):
            for m in M:
                p = P[m].get(r['id'])
                if p is None:
                    continue
                py, g = p['yes'], int(r['gold'])
                acc[k][m + 'n'] += 1; acc[k][m] += (py > .5) == (g == 1); acc[k][m + 'mid'] += .2 < py < .8
                acc[k][m + 'fy'] += py > .5 and g == 0; acc[k][m + 'fn'] += py <= .5 and g == 1
    print('==', split)
    for k, c in sorted(acc.items()):
        print('%-24s' % k[:24], ' | '.join('%s %.3f mid%.2f fY%d fN%d' % (m[4:], c[m] / max(1, c[m + 'n']), c[m + 'mid'] / max(1, c[m + 'n']), c[m + 'fy'], c[m + 'fn']) for m in M), 'n=', c[M[0] + 'n'])
