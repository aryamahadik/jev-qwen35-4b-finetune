"""Read-only: build committed / band-edge variants of stored JevBench v1.5.4 public runs into this scratch folder.
commit: noul P(yes) -> 1/0 by argmax (ties -> 'no', the harness argmax rule).
band edge: only 0.2 < P(yes) < 0.8 moved to 0.8 (if argmax yes) or 0.2 (else); other answers untouched."""
import json, sys, shutil
from pathlib import Path
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/bench/v154')
import v154lib as L
RUNS = Path('/Users/aryamahadik/Documents/jev/bench/runs')
OUT = Path(__file__).resolve().parent / 'v154_variants'
items = L.load_public(Path('/Users/aryamahadik/Documents/jev/bench/jevbench_v154'))
types = {}
for it in (items.values() if isinstance(items, dict) else items):
    types[it['task_id'] if 'task_id' in it else it['id']] = it['question']['type']
for run in ['jev_p1', 'jev_p2', 'v154_q35_4b_pxE', 'v154_q35_2b_armI_1600']:
    for mode in ['commit', 'band']:
        d = OUT / f'{run}_{mode}'; d.mkdir(parents=True, exist_ok=True)
        shutil.copy(RUNS / run / 'manifest.json', d / 'manifest.json')
        n = 0
        with open(d / 'results.jsonl', 'w') as f:
            for line in open(RUNS / run / 'results.jsonl'):
                if not line.strip(): continue
                r = json.loads(line)
                if types.get(r['task_id']) == 'noul' and r.get('probs') and 'yes' in r['probs']:
                    p = r['probs']['yes']; yes = L.argmax_label(r['probs']) == 'yes'
                    if mode == 'commit':
                        r['probs'] = {'yes': 1.0 if yes else 0.0, 'no': 0.0 if yes else 1.0}; n += 1
                    elif 0.2 < p < 0.8:
                        r['probs'] = {'yes': 0.8 if yes else 0.2, 'no': 0.2 if yes else 0.8}; n += 1
                f.write(json.dumps(r) + '\n')
        print(run, mode, 'changed', n)
