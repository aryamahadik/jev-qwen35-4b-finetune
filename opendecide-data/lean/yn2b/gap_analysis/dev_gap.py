import json,collections,ast,sys
from pathlib import Path
L=Path('/Users/aryamahadik/Documents/jev/opendecide-data/lean')
M4,M2='q35_4b_pxE','q35_2b_armI_1600'
sets=sys.argv[1].split(',')
allrec=[]
for s in sets:
    rows={}
    for l in open(L/f'data/{s}.jsonl'):
        r=json.loads(l); rows[r['id']]=r
    P={}
    for m in (M4,M2):
        P[m]={}
        for l in open(L/f'preds_{s}/{m}.jsonl'):
            x=json.loads(l); P[m][x['id']]=x['probs']
    by=collections.defaultdict(lambda: collections.defaultdict(list))
    for i,r in rows.items():
        if i not in P[M4] or i not in P[M2]: continue
        q=r['qtype']
        opts=r['options']
        if isinstance(opts,str):
            try: opts=ast.literal_eval(opts)
            except Exception: opts=None
        if q=='noul':
            g=r['gold']; g= 1 if g in (1,'1','yes',True) else 0
        for m in (M4,M2):
            pr=P[m][i]
            if q=='noul':
                y=float(pr.get('yes',0)); n=float(pr.get('no',0)); p=y/(y+n) if y+n else .5
                c=(p>0.5)==(g==1); d='fY' if (p>0.5 and g==0) else ('fN' if (p<=0.5 and g==1) else '')
                ab=0.2<p<0.8
            else:
                keys=opts if opts else [k for k in pr if not k.startswith('_')]
                best=max(keys,key=lambda k: float(pr.get(k,0)))
                c=best==r['gold']; d=''; ab=False
            meta=r.get('meta')
            if isinstance(meta,str):
                try: meta=ast.literal_eval(meta)
                except Exception: meta={}
            fam=(meta or {}).get('family') or (meta or {}).get('task') or ''
            by[(s,r['source'],q,r.get('role'))][m].append((c,d,ab))
    for k,v in by.items():
        n=len(v[M4])
        a4=sum(c for c,_,_ in v[M4]); a2=sum(c for c,_,_ in v[M2])
        fy2=sum(d=='fY' for _,d,_ in v[M2]); fn2=sum(d=='fN' for _,d,_ in v[M2])
        fy4=sum(d=='fY' for _,d,_ in v[M4]); fn4=sum(d=='fN' for _,d,_ in v[M4])
        ab2=sum(a for *_,a in v[M2]); ab4=sum(a for *_,a in v[M4])
        allrec.append(dict(set=k[0],source=k[1],qtype=k[2],role=k[3],n=n,a4=a4,a2=a2,fy4=fy4,fn4=fn4,fy2=fy2,fn2=fn2,ab4=ab4,ab2=ab2))
json.dump(allrec,open('/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/73bb87c6-8519-454d-98bb-7961fcde73b9/scratchpad/gap/dev_gap.json','w'))
# summary per set x qtype
agg=collections.defaultdict(lambda:[0,0,0,0,0])
for r in allrec:
    k=(r['set'],r['qtype']); a=agg[k]; a[0]+=r['n']; a[1]+=r['a4']; a[2]+=r['a2']; a[3]+=r['ab4']; a[4]+=r['ab2']
for k,a in sorted(agg.items()): print('%-16s %-7s n=%5d 4B %.3f 2B %.3f gap %+.3f | abst4 %.2f abst2 %.2f'%(k[0],k[1],a[0],a[1]/a[0],a[2]/a[0],(a[1]-a[2])/a[0],a[3]/a[0],a[4]/a[0]))
