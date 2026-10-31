import json,sys,hashlib
from collections import Counter,defaultdict
sys.path.insert(0,'.')
import pilot as PI, pilot_t37b as PT
dirs=['pilot_i3b_full']+[f'pilot_i3b_qc{i}' for i in range(2,7)]
rows=[]
for d in dirs:
    for l in open(f't37b/{d}/rows.jsonl'):
        r=json.loads(l); r['id']=d+'|'+r['id']; rows.append(r)
H=lambda r:hashlib.md5(r['id'].encode()).hexdigest()
import os
KEY=(lambda t:t['entry']) if os.environ.get('LVL')=='entry' else (lambda t:t['base_source'])
ONE={'gd_usb_factuality','gd_hotpotqa_yesno','gd_answer_equiv'}
def bal(rows,ratio=2.0,one_keep=0):
    g=defaultdict(lambda:defaultdict(list)); out=[]; one=defaultdict(list)
    for r in rows:
        t=r['meta']['t37b']; s=t['base_source']
        if s in ONE or s=='gd_hatemoji_build_v14': one[s].append(r); continue
        g[(KEY(t),t['base_gold'])][t['kind']=='equiv'].append(r)
    for k,d in g.items():
        m=min(len(d[True]),len(d[False])); lim=int(m*ratio)
        for side in (True,False):
            out+=sorted(d[side],key=H)[:min(len(d[side]),lim)] if m>0 else []
    for s,l in one.items(): out+=sorted(l,key=H)[:one_keep]
    return out
for ratio,ok in ((2.0,0),):
    sub=bal(rows,ratio,ok)
    infos=[PT._info(r) for r in sub]
    g6=PI.g6(infos)['yes_no']; g7=PI.g7(infos)
    print(ratio,ok,len(sub),g6['c_card_without_question'],g6['d_meta'],g7.get('verdict'),[(f['feature'],f['n'],f['yes_rate']) for f in (g7.get('yes_no_card_adjusted_fails') or [])][:8],flush=True)
