"""Compare blind-read answers (answers.tsv: id, answer, flag, reason) with the hidden gold of a sample folder.

  python yn2b/f7_blind_read_compare.py [--dir <scratchpad>/blind]
"""
import argparse
import json
import os
from collections import Counter

SCRATCH = '/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/73bb87c6-8519-454d-98bb-7961fcde73b9/scratchpad'
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data/v14_parts')  # checkout-relative
ap = argparse.ArgumentParser()
ap.add_argument('--dir', default=f'{SCRATCH}/blind')
B = ap.parse_args().dir
gold = json.load(open(f'{B}/HIDDEN_gold.json'))
rows = {}
for f in ['f7_train.jsonl', 'f7_probe.jsonl', 'f7_devx.jsonl']:
    for line in open(f'{D}/{f}'):
        r = json.loads(line)
        if r['id'] in gold:
            rows[r['id']] = r
ans = {}
for line in open(f'{B}/answers.tsv'):
    p = line.rstrip('\n').split('\t')
    while len(p) < 4:
        p.append('')
    ans[p[0]] = p
assert set(ans) == set(gold), (len(set(gold) - set(ans)), list(set(gold) - set(ans))[:5], list(set(ans) - set(gold))[:5])
dis = []
c = Counter()
for rid, g in gold.items():
    r = rows[rid]
    a = ans[rid]
    if r['qtype'] == 'choice':
        ok = r['options'][int(a[1])] == r['gold']
    else:
        ok = int(a[1]) == r['gold']
    c[(g['tag'] if g['tag'] in ('random', 'probe', 'devx') else 'must', ok)] += 1
    if not ok:
        dis.append((rid, g['tag'], a[1], r['gold'], a[2], a[3]))
print(c)
for d in dis:
    print(d)
