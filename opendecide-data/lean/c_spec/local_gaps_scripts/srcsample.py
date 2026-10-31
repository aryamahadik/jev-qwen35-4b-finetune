import json, sys, ast
from multiprocessing import Pool
SRC="/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts/golden_train.jsonl"
import os
def work(a):
    k,s,e=a; out={}
    with open(SRC,'rb') as fh:
        if s: fh.seek(s-1); fh.readline()
        while fh.tell()<=e:
            l=fh.readline()
            if not l: break
            r=json.loads(l); src=r['source']; d=out.setdefault(src,{'ins':[], 'opt':None,'state':None,'card':None})
            if len(d['ins'])<3 and r['instructions'] not in d['ins'] and (r['role'] in ('aff','choice') or len(d['ins'])<1): d['ins'].append(r['instructions'][:220])
            if d['opt'] is None and r['qtype']=='choice': d['opt']=str(r['options'])[:220]
            if d['state'] is None: d['state']=r['state'][:160]
            if d['card'] is None and r.get('card'): d['card']=r['card'][:200]
    return out
if __name__=='__main__':
  size=os.path.getsize(SRC); n=9; cuts=[size*i//n for i in range(n+1)]
  with Pool(n) as p: parts=p.map(work,[(i,cuts[i],cuts[i+1]-1 if i<n-1 else size) for i in range(n)])
  m={}
  for part in parts:
      for k,v in part.items():
          if k not in m: m[k]=v
          else:
              for x in v['ins']:
                  if len(m[k]['ins'])<3 and x not in m[k]['ins']: m[k]['ins'].append(x)
              for f in ('opt','state','card'):
                  if m[k][f] is None: m[k][f]=v[f]
  json.dump(m,open('src_samples.json','w'))
  print(len(m))
