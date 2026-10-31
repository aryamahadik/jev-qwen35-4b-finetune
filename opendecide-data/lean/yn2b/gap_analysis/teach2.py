import json,glob,collections,re
D='/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_label_shards/acct_arya-mahadik-ai/labels_q35_4b_pxE/'
lab={}
for f in glob.glob(D+'shard_*.jsonl'):
    for l in open(f):
        x=json.loads(l)
        if 'yes' in x['probs']: lab[x['id']]=float(x['probs']['yes'])
F='/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts/golden_train.jsonl'
grp=lambda s: ('gen_procedural' if s.startswith('gd_gen') or s.startswith('pg_') or s.startswith('proc') else
  'tables_numeric' if any(k in s for k in ('tab','wtq','finqa','totto','feverous','infotabs','tathqa','tatqa','boardgame','uscg')) else
  'moral_social' if any(k in s for k in ('sc101','mfrc','msn','comve','ethics','social')) else
  'safety_hate' if any(k in s for k in ('hate','slur','sexism','prejudice','toxic','offens','aegis')) else 'other')
c=collections.defaultdict(collections.Counter)
for l in open(F):
    i=l[8:l.index('"',8)]
    if i not in lab: continue
    r=json.loads(l)
    if r['qtype']!='noul': continue
    m=r.get('meta') or ''
    if "'teacher'" in str(m): 
        c['ALL']['human_teacher_kept']+=1
        continue
    p=lab[i]; g=1 if r['gold'] in (1,'1') else 0
    eps=0.05
    y=0.5*(g*(1-2*eps)+eps)+0.5*p
    for k in ('ALL',grp(r['source'])):
        c[k]['n']+=1; c[k]['mid']+=0.2<y<0.8; c[k]['wrongside']+=(y>=0.5)!=(g==1); c[k]['t_wrong']+=(p>=0.5)!=(g==1)
for k,v in c.items(): 
    n=v['n'] or 1
    print('%-16s n=%6d  KD target y in (0.2,0.8): %.3f | target on wrong side: %.3f | teacher wrong: %.3f | human-teacher rows kept: %d'%(k,v['n'],v['mid']/n,v['wrongside']/n,v['t_wrong']/n,v['human_teacher_kept']))
