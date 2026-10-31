import json, collections
R=json.load(open('ch6000.json'))
print(len(R), collections.Counter(r['gold_key'] for r in R))
def nn(r):
    return {'reject': r['n_rej'], 'withdraw': r['n_wd'], 'store': r['p']}
# is gold the rule with the largest N among displayed?
c=collections.Counter()
for r in R:
    n=nn(r); disp=[k for k in r['display']]
    if r['gold_key']=='none': c['none']+=1; continue
    mx=max(n[k] for k in disp if n[k] is not None)
    c['gold_is_maxN' if n[r['gold_key']]==mx else 'gold_not_maxN']+=1
print(c)
# gold key by value of its own N and others
for k in ('reject','withdraw','store'):
    d=collections.defaultdict(lambda:[0,0])
    for r in R:
        if k in r['display'] and nn(r)[k] is not None:
            d[nn(r)[k]][0]+= r['gold_key']==k; d[nn(r)[k]][1]+=1
    print(k, {a:(b[1], round(b[0]/b[1],2)) for a,b in sorted(d.items())})
# 'none' gold by d vs max end
import statistics as st
dn=[r['d'] for r in R if r['gold_key']=='none']; dg=[r['d'] for r in R if r['gold_key']!='none']
print('d none', st.mean(dn), 'd other', st.mean(dg))
# by (display, gold)
d=collections.defaultdict(collections.Counter)
for r in R: d[tuple(r['display'])][r['gold_key']]+=1
for k,v in d.items(): print(k, dict(v))
# by policy
d=collections.defaultdict(collections.Counter)
for r in R: d[(r['policy'])][r['gold_key']]+=1
for k,v in sorted(d.items()): print(k, dict(v))
d=collections.defaultdict(collections.Counter)
for r in R: d[(r['reason'],r['goods'],r['seal'])][r['gold_key']]+=1
for k,v in sorted(d.items(), key=str): print(k, dict(v))
