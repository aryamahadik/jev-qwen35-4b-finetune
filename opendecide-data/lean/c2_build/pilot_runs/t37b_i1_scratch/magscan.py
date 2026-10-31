import sys, json, math
from collections import defaultdict
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
import pilot as PI, pilot_t37b as P
rows=[json.loads(l) for l in open('/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i1/rows.jsonl')]
infos=[P._info(r) for r in rows]
feats=[]
for i in infos:
    cat,num=PI.meta_features(i)
    feats.append((i.row['meta']['t37b']['entry'], i.row['meta']['t37b']['kind'], i.row['gold'], num))
# overall AUC-like: mann-whitney for each numeric feature
def auc(xs,ys):
    pos=[x for x,y in zip(xs,ys) if y==1]; neg=[x for x,y in zip(xs,ys) if y==0]
    s=0
    for p in pos:
        for n in neg: s+= (p>n)+0.5*(p==n)
    return s/(len(pos)*len(neg))
ys=[f[2] for f in feats]
for k in ('len_state','n_numbers','mag_max','mag_mean','len_q','len_card','n_lines'):
    print('ALL',k, round(auc([f[3][k] for f in feats], ys),3))
by=defaultdict(list)
for f in feats: by[f[0]].append(f)
for e,fs in sorted(by.items()):
    if len(fs)<20: continue
    ys_=[f[2] for f in fs]
    print(e, len(fs), {k: round(auc([f[3][k] for f in fs], ys_),2) for k in ('len_state','n_numbers','mag_mean','mag_max')})
