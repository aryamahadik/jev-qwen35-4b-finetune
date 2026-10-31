from an6 import *
print('base', accs([mk(r) for r in R]))
print('question view', accs([mk(r) for r in R], 'a_question'))
import collections
print(collections.Counter(r['gold_key'] for r in R))
def nn(r): return {'reject': r['n_rej'], 'withdraw': r['n_wd'], 'store': r['p']}
c=collections.Counter()
for r in R:
    n=nn(r)
    if r['gold_key']=='none': continue
    mx=max(n[k] for k in r['display'] if n[k] is not None)
    c['gold_is_maxN' if n[r['gold_key']]==mx else 'not']+=1
print(c)
