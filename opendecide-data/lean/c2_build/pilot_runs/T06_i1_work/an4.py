import json, collections, statistics as st
R=[r for r in json.load(open('feats6000b.json')) if r['qtype']=='noul']
for r in R: r['m']=r['num']['mag_mean']
ms=sorted(r['m'] for r in R)
qs=[ms[int(len(ms)*q/10)] for q in range(10)]+[ms[-1]]
print([round(x,2) for x in qs])
b=collections.defaultdict(list)
for r in R:
    j=sum(r['m']>=q for q in qs[1:-1]); b[j].append(r['refund'])
print({k:(len(v),round(sum(v)/len(v),3)) for k,v in sorted(b.items())})
print('mean m refund vs not', st.mean(r['m'] for r in R if r['refund']), st.mean(r['m'] for r in R if not r['refund']))
for c in (True,False):
    S=[r for r in R if r['counts']==c]
    print('counts',c,len(S), st.mean(r['m'] for r in S if r['refund']) if any(r['refund'] for r in S) else None, st.mean(r['m'] for r in S if not r['refund']))
# by format (date form) via cat format_style? record container only
b=collections.defaultdict(list)
for r in R: b[(r['cat']['format_style'].split('/')[1], r['counts'])].append(r['m'])
print({k:(len(v),round(st.mean(v),3)) for k,v in b.items()})
