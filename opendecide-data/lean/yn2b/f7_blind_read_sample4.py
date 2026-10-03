"""Fourth (fresh) blind-read sampler for F7 (checklist section 4, item 11), on the F7 part EXACTLY as the 4B top-up
fix2 uses it AFTER the source-label audit (data/v14_parts/f7fix2_train.jsonl + f7fix2_meta.jsonl, written by
extra/build_fix2.py from F7 v2 r5: golden_src/gen3/f7_repair_r5.py replaced every pair built from a flagged source
row, yn2b/f7_source_label_audit.json, yn2b/f7_fix2_drops.json).

THE READER MUST BE A NEW AGENT. The agent that assembled fix2 read blind read 3's gold and audited the source labels,
so it cannot be the blind reader. The reader must not open the generator (golden_src/gen3/), decide2, the drop list,
the audit file or any gold before its answers are frozen.

Differences from f7_blind_read_sample3.py:
  - new seed (default 20261042); --out is required (the reader's own scratch folder);
  - rows whose id OR ladder (call_id) was in read 1, 2 or 3 are excluded (yn2b/f7_blind_read_answers.tsv,
    f7_blind_read_2_answers.tsv, f7_blind_read_3_answers.tsv), and so is ladder pair f7v2-tr-00001;
  - the train file's sha256 is printed so the report can name the exact file read.
Sample = 10 rows per MUST item (sidecar 'phen' only) + 100 random train rows + 20 probe rows. The 20 probe rows are
drawn only from probe ladders the probe source-label audit did NOT flag (yn2b/f7_fix2_drops.json probe_report_only =
the rows step P leaves out of its accuracy bars, A8-prime F.P); a probe row read 4 marks wrong / ambiguous is handled
as A8-prime D says (source-label cause: report-only for 11.1, the row joins the exclusion list and step 0a is re-frozen
before step 0b; a negation-program cause fails 11.1). Writes blinded batches
(card, state, question, options only; no gold, role or meta) and a separate hidden gold file. Compare afterwards with
  python yn2b/f7_blind_read_compare.py --dir <out>

  python yn2b/f7_blind_read_sample4.py --out <reader scratch>/blind4 [--seed 20261042]
"""
import argparse
import hashlib
import json
import os
import random

LEAN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # the checkout's lean/, never a fixed path
D = os.path.join(LEAN_DIR, 'data/v14_parts')
Y = os.path.join(LEAN_DIR, 'yn2b')
MUST = [1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 16, 21, 22, 24, 27, 36]
SEEN_LADDERS = {'f7v2-tr-00001a', 'f7v2-tr-00001b'}
ap = argparse.ArgumentParser()
ap.add_argument('--seed', type=int, default=20261042)
ap.add_argument('--out', required=True)
a = ap.parse_args()
B = a.out
os.makedirs(B, exist_ok=True)
rng = random.Random(a.seed)
train = [json.loads(l) for l in open(f'{D}/f7fix2_train.jsonl')]
tmeta = [json.loads(l) for l in open(f'{D}/f7fix2_meta.jsonl')]
assert all(x['id'] == y['id'] for x, y in zip(train, tmeta))
probe = [json.loads(l) for l in open(f'{D}/f7_probe.jsonl')]
prev_ids = set()
for f in ('f7_blind_read_answers.tsv', 'f7_blind_read_2_answers.tsv', 'f7_blind_read_3_answers.tsv'):
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
flagged = set((json.load(open(f'{Y}/f7_fix2_drops.json')).get('probe_report_only') or {}))
pfresh = [r for r in probe if fresh(r) and r['meta'].get('latent_id') not in flagged]
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
print('train file sha256', hashlib.sha256(open(f'{D}/f7fix2_train.jsonl', 'rb').read()).hexdigest())
print('rows', len(blind), 'ladders', len({r["call_id"] for _, _, r in chosen}), 'batches',
      len(os.listdir(f'{B}/batches')), 'prev_ids', len(prev_ids), 'prev_calls', len(prev_calls), B)
