import json,glob,collections,ast
D='/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_label_shards/acct_arya-mahadik-ai/labels_q35_4b_pxE/'
lab={}
for f in glob.glob(D+'shard_*.jsonl'):
    for l in open(f):
        x=json.loads(l); lab[x['id']]=x['probs']
F='/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts/golden_train.jsonl'
acc=collections.defaultdict(collections.Counter)
for l in open(F):
    # fast prefilter on id
    i=l[8:l.index('"',8)]
    if i not in lab: continue
    r=json.loads(l); p=lab[i]; q=r['qtype']; s=r['source']
    a=acc[(s,q)]; a['n']+=1
    if q=='noul':
        g=1 if r['gold'] in (1,'1') else 0
        py=float(p['yes']); ok=(py>=0.5)==(g==1)
        a['ok']+=ok; a['fY']+=(py>=0.5 and g==0); a['fN']+=(py<0.5 and g==1)
        a['soft']+=(0.2<py<0.8); a['bs']+=0  
        a['brier_x1e4']+=int(1e4*(py-g)**2)
    else:
        opts=r['options']
        if isinstance(opts,str): opts=ast.literal_eval(opts)
        best=max(opts,key=lambda o: float(p.get(o,0)))
        a['ok']+=best==r['gold']
json.dump({'|'.join(k):dict(v) for k,v in acc.items()},open('/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/73bb87c6-8519-454d-98bb-7961fcde73b9/scratchpad/gap/teach.json','w'))
print('done',len(lab),sum(v['n'] for v in acc.values()))
