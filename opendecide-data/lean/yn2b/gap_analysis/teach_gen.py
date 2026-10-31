"""4B-E teacher quality on generator sources (read-only; 30 Sep 2026, exam-gap design).
For every labelled generator row without a human/exact teacher: is the 4B-E read on the gold side, how often does the
2B's kd 0.5 target 0.5*(0.95/0.05 gold) + 0.5*teacher fall in JevBench's abstain zone (0.2, 0.8), and does it ever land
on the wrong side of 0.5 (it never does for yes/no). Choice: 4B-E argmax wrong rate and mean p(gold).
Labels: one account's shards only (data/v14_label_shards/acct_arya-mahadik-ai/labels_q35_4b_pxE)."""
import collections, glob, json
L = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/'
lab = {}
for f in glob.glob(L + 'data/v14_label_shards/acct_arya-mahadik-ai/labels_q35_4b_pxE/shard_*.jsonl'):
    for l in open(f):
        x = json.loads(l); lab[x['id']] = x['probs']
c = collections.defaultdict(collections.Counter)
for l in open(L + 'data/v14_parts/golden_train.jsonl'):
    r = json.loads(l); s = r['source']
    if not s.startswith('gd_gen') or r['id'] not in lab:
        continue
    m = r.get('meta') or {}
    if isinstance(m.get('teacher'), dict) and m.get('teacher_src') != 'blend50':
        continue
    p = lab[r['id']]
    if r['qtype'] == 'noul':
        g = int(r['gold']); py = float(p['yes']); y = 0.5 * (g * 0.9 + 0.05) + 0.5 * py
        for k in (s, 'TOTAL'):
            c[k]['yn'] += 1; c[k]['tw'] += (py >= .5) != (g == 1); c[k]['mid'] += .2 < y < .8; c[k]['ws'] += (y >= .5) != (g == 1)
    else:
        top = max(p, key=p.get)
        for k in (s, 'TOTAL'):
            c[k]['ch'] += 1; c[k]['cw'] += top != r['gold']
print('%-26s %6s %8s %8s %8s | %6s %8s' % ('source', 'yn', 'T_wrong', 'mid', 'wrongside', 'ch', 'T_wrong'))
for k, v in sorted(c.items()):
    yn, ch = v['yn'] or 1, v['ch'] or 1
    print('%-26s %6d %8.3f %8.3f %8.3f | %6d %8.3f' % (k, v['yn'], v['tw'] / yn, v['mid'] / yn, v['ws'] / yn, v['ch'], v['cw'] / ch))
