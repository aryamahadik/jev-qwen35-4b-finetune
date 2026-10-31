import json,collections,sys,math
from pathlib import Path
L=Path('/Users/aryamahadik/Documents/jev/opendecide-data/lean')
def load(split):
    rows={}
    for l in open(L/f'data/{split}.jsonl'):
        r=json.loads(l); rows[r['id']]=r
    return rows
def preds(split,m):
    p=L/f'preds_{split}/{m}.jsonl'
    if not p.exists(): return None
    return {json.loads(l)['id']:json.loads(l)['probs'] for l in open(p)}
def pyes(pr):
    if pr is None: return None
    y=float(pr.get('yes',0)); n=float(pr.get('no',0))
    return y/(y+n) if y+n>0 else 0.5
def run(split,models,roles=('aff',)):
    rows=load(split)
    P={m:preds(split,m) for m in models}
    P={m:v for m,v in P.items() if v}
    ids=[i for i,r in rows.items() if r['qtype']=='noul' and r['role'] in roles]
    by=collections.defaultdict(list)
    for i in ids: by[rows[i]['source']].append(i)
    out=[]
    tot={m:[0,0,0.0] for m in P}
    for s,ii in sorted(by.items()):
        rec={'source':s,'n':len(ii),'yes_share':sum(rows[i]['gold']==1 for i in ii)/len(ii)}
        for m,pp in P.items():
            c=0;fy=0;fn=0;br=0;miss=0
            for i in ii:
                p=pyes(pp.get(i))
                g=rows[i]['gold']
                if p is None: miss+=1; p=0.5
                pred=1 if p>0.5 else 0
                if p==0.5: pred=-1
                c+= pred==g
                if pred==1 and g==0: fy+=1
                if pred!=1 and g==1: fn+=1
                br+=(p-g)**2
            rec[m]=(c/len(ii), fy, fn, br/len(ii))
            tot[m][0]+=c; tot[m][1]+=len(ii); tot[m][2]+=br
        out.append(rec)
    return out,tot,P,rows,by
if __name__=='__main__':
    split=sys.argv[1]; models=sys.argv[2].split(','); roles=tuple(sys.argv[3].split(',')) if len(sys.argv)>3 else ('aff',)
    out,tot,P,rows,by=run(split,models,roles)
    ours=[m for m in P if not m.startswith('jev')]
    for m in P: print(m,'overall acc %.3f brier %.3f n=%d'%(tot[m][0]/tot[m][1],tot[m][2]/tot[m][1],tot[m][1]))
    ranked=[]
    for rec in out:
        j=rec['jev_guard'][0]
        line='%-26s n=%3d y%%=%.2f '%(rec['source'],rec['n'],rec['yes_share'])
        for m in P:
            a,fy,fn,b=rec[m]; line+=' | %s %.3f fY%d fN%d B%.3f'%(m.replace('q35_4b_','').replace('jev_',''),a,fy,fn,b)
        print(line)
    print('ranked by (jev - ours)*n:')
    for m in ours:
        r=sorted(out,key=lambda rec:-(rec['jev_guard'][0]-rec[m][0])*rec['n'])
        print(' ',m,[(rec['source'],round((rec['jev_guard'][0]-rec[m][0])*rec['n'],1)) for rec in r[:8]])
