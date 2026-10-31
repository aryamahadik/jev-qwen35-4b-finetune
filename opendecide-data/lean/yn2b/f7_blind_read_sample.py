"""Blind-read sampler for F7 (checklist section 4, item 11): 10 rows per MUST item (picked by the sidecar 'phen' field
only), 100 random train rows, 20 probe rows and every devx row. Writes the blinded batches (card, state, question,
options; no gold, role or meta) and, separately, the hidden gold file. Use a NEW --seed and a NEW --out folder for a
fresh read (the first read used seed 20261002 in the scratchpad folder 'blind').

  python yn2b/f7_blind_read_sample.py [--seed 20261002] [--out <scratchpad>/blind]
"""
import argparse
import json
import os
import random

SCRATCH = '/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/73bb87c6-8519-454d-98bb-7961fcde73b9/scratchpad'
D = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts'
MUST = [1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 16, 21, 22, 24, 27, 36]
ap = argparse.ArgumentParser()
ap.add_argument('--seed', type=int, default=20261002)
ap.add_argument('--out', default=f'{SCRATCH}/blind')
a = ap.parse_args()
B = a.out
os.makedirs(B, exist_ok=True)
rng = random.Random(a.seed)
train = [json.loads(l) for l in open(f'{D}/f7_train.jsonl')]
tmeta = [json.loads(l) for l in open(f'{D}/f7_meta.jsonl')]
assert all(x['id'] == y['id'] for x, y in zip(train, tmeta))
probe = [json.loads(l) for l in open(f'{D}/f7_probe.jsonl')]
devx = [json.loads(l) for l in open(f'{D}/f7_devx.jsonl')]
chosen = []
used = set()
for item in MUST:
    idx = [i for i, m in enumerate(tmeta) if item in m['phen'] and i not in used]
    pick = rng.sample(idx, 10)
    for i in pick:
        used.add(i)
        chosen.append(('must%d' % item, 'train', train[i]))
rest = [i for i in range(len(train)) if i not in used]
for i in rng.sample(rest, 100):
    used.add(i)
    chosen.append(('random', 'train', train[i]))
for r in rng.sample(probe, 20):
    chosen.append(('probe', 'probe', r))
for r in devx:
    chosen.append(('devx', 'devx', r))
# blinded view: no gold, role, meta
gold = {}
blind = []
for tag, split, r in chosen:
    gold[r['id']] = {'gold': r['gold'], 'tag': tag, 'split': split}
    blind.append({'tag': tag, 'id': r['id'], 'qtype': r['qtype'], 'card': r['card'], 'state': r['state'],
                  'instructions': r['instructions'], 'options': r['options']})
json.dump(gold, open(f'{B}/HIDDEN_gold.json', 'w'))
json.dump([b['id'] for b in blind], open(f'{B}/order.json', 'w'))
os.makedirs(f'{B}/batches', exist_ok=True)
for k in range(0, len(blind), 20):
    with open(f'{B}/batches/b%03d.txt' % (k // 20), 'w') as f:
        for b in blind[k:k + 20]:
            f.write('=' * 30 + '\n')
            f.write(f"ID {b['id']}  [{b['tag']}] qtype={b['qtype']}\n")
            f.write('--CARD--\n' + (b['card'] or '(none)') + '\n')
            f.write('--STATE--\n' + b['state'] + '\n')
            f.write('--Q--\n' + b['instructions'] + '\n')
            if b['options']:
                f.write('--OPTIONS--\n')
                for j, o in enumerate(b['options']):
                    f.write(f'  [{j}] {o}\n')
print(len(blind), len(os.listdir(f'{B}/batches')), B)
