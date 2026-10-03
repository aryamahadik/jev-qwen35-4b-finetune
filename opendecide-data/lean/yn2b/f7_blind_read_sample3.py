"""Third (fresh) blind-read sampler for F7 (checklist section 4, item 11), on the F7 part EXACTLY as the 4B top-up
fix2 uses it (data/v14_parts/f7fix2_train.jsonl + f7fix2_meta.jsonl, written by extra/build_fix2.py: blind read 2's
wrong-source-label pairs and the probe-overlap pairs dropped).

Differences from f7_blind_read_sample2.py:
  - new seed (default 20261022); train rows come from f7fix2_train.jsonl;
  - rows whose id OR ladder (call_id) was in read 1 or read 2 (yn2b/f7_blind_read_answers.tsv,
    yn2b/f7_blind_read_2_answers.tsv) are excluded, and so is ladder pair f7v2-tr-00001 (two of its rows were seen,
    with gold, by the fix2 assembler before this read);
  - sample = 10 rows per MUST item (sidecar 'phen' only) + 100 random train rows + 20 probe rows (devx: all 220 were
    read in read 1 and the file is unchanged).
Writes blinded batches (card, state, question, options only; no gold, role or meta) and a separate hidden gold file.

  python yn2b/f7_blind_read_sample3.py [--seed 20261022] [--out <scratchpad>/blind3]
"""
import argparse
import json
import os
import random

SCRATCH = '/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/73bb87c6-8519-454d-98bb-7961fcde73b9/scratchpad'
D = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts'
Y = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/yn2b'
MUST = [1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 16, 21, 22, 24, 27, 36]
SEEN_LADDERS = {'f7v2-tr-00001a', 'f7v2-tr-00001b'}
ap = argparse.ArgumentParser()
ap.add_argument('--seed', type=int, default=20261022)
ap.add_argument('--out', default=f'{SCRATCH}/blind3')
a = ap.parse_args()
B = a.out
os.makedirs(B, exist_ok=True)
rng = random.Random(a.seed)
train = [json.loads(l) for l in open(f'{D}/f7fix2_train.jsonl')]
tmeta = [json.loads(l) for l in open(f'{D}/f7fix2_meta.jsonl')]
assert all(x['id'] == y['id'] for x, y in zip(train, tmeta))
probe = [json.loads(l) for l in open(f'{D}/f7_probe.jsonl')]
prev_ids = set()
for f in ('f7_blind_read_answers.tsv', 'f7_blind_read_2_answers.tsv'):
    prev_ids |= set(l.split('\t')[0] for l in open(f'{Y}/{f}') if l.strip())
prev_calls = set()
for r in train + probe:
    if r['id'] in prev_ids or r['meta'].get('latent_id') in SEEN_LADDERS:
        prev_calls.add(r['call_id'])


def fresh(r):
    return r['id'] not in prev_ids and r['call_id'] not in prev_calls


chosen, used = [], set()
for item in MUST:
    idx = [i for i, m in enumerate(tmeta) if item in m['phen'] and i not in used and fresh(train[i])]
    for i in rng.sample(idx, 10):
        used.add(i)
        chosen.append(('must%d' % item, 'train', train[i]))
rest = [i for i in range(len(train)) if i not in used and fresh(train[i])]
for i in rng.sample(rest, 100):
    used.add(i)
    chosen.append(('random', 'train', train[i]))
pfresh = [r for r in probe if fresh(r)]
for r in rng.sample(pfresh, 20):
    chosen.append(('probe', 'probe', r))
gold, blind = {}, []
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
print('rows', len(blind), 'ladders', len({r["call_id"] for _, _, r in chosen}), 'batches',
      len(os.listdir(f'{B}/batches')), 'prev_ids', len(prev_ids), 'prev_calls', len(prev_calls), B)
