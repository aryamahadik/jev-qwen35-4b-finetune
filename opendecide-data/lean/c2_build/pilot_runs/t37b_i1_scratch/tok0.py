import sys, json
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
import pilot as P
rows=[json.loads(l) for l in open('/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot/rows.jsonl')]
bases=[json.loads(l) for l in open('/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot/bases.jsonl')]
t,how=P.real_tokens(rows)
print(how, len(t), sum(t)/len(t), max(t), sorted(t)[:5], sorted(t)[-8:])
from collections import defaultdict
by=defaultdict(list)
for r,x in zip(rows,t): by[r['meta']['t37b']['entry']].append(x)
for k,v in sorted(by.items()): print(k, len(v), round(sum(v)/len(v)))
