import sys, json
from collections import Counter
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from c2_kit import polarity as KP
NEG = ("wrong", "contradict\\w*", "refut\\w*", "go(?:es)? against", "unacceptable", "bad", "hateful", "unreliable")
rows=[json.loads(l) for l in open('t37b/pilot_i1/rows.jsonl')]
c=Counter(); ex={}
for r in rows:
    t=r['meta']['t37b']
    if t['kind']!='syntactic': continue
    rd=KP.read(r['instructions'], negatives=NEG)
    if rd.mixed:
        c[t['entry']]+=1; ex.setdefault(t['entry'], r['instructions'])
print(sum(c.values()), 'of', sum(1 for r in rows if r['meta']['t37b']['kind']=='syntactic'), 'syntactic partners are mixed (S>=1 and a negative predicate)')
for k,v in c.items(): print(k, v, '|', ex[k][:120])
