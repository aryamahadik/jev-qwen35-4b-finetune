import json,sys,random,hashlib
from collections import Counter,defaultdict
sys.path.insert(0,'.')
import pilot as PI, pilot_t37b as PT
dirs=['pilot_i3b_full']+[f'pilot_i3b_qc{i}' for i in range(2,7)]
rows=[]
for d in dirs:
    for l in open(f't37b/{d}/rows.jsonl'):
        r=json.loads(l); r['id']=d+'|'+r['id']; rows.append(r)
def key(r,lvl):
    t=r['meta']['t37b']; return t['entry'] if lvl=='entry' else t['base_source']
def bal(rows,lvl,minfrac=0.0):
    g=defaultdict(lambda:defaultdict(list))
    for r in rows:
        t=r['meta']['t37b']; k=(key(r,lvl),t['base_gold']); g[k][t['kind']=='equiv'].append(r)
    out=[]
    for k,d in g.items():
        n=min(len(d[True]),len(d[False]))
        for side in (True,False):
            l=sorted(d[side],key=lambda r:hashlib.md5(r['id'].encode()).hexdigest())
            out+=l[:n]
    return out
for lvl in ('entry','source'):
    sub=bal(rows,lvl)
    c=Counter(r['meta']['t37b']['base_source'] for r in sub)
    infos=[PT._info(r) for r in sub]
    g6=PI.g6(infos); y=g6['yes_no']
    print(lvl,len(sub),{k:y[k] for k in('a_question','c_card_without_question','d_meta')},dict(c))
