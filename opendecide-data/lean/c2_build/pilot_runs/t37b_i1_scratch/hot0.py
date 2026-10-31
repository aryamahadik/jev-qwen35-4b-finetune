import sys, json, re, random
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from c2_kit import paths
from t37b import polarity as PA, polarity_b as PB, sources as SRC
E = SRC.ENTRY_BY_KEY["gd_hotpotqa_yesno/q"]
qs=[]
with open('/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts/golden_train.jsonl') as f:
    for line in f:
        if '"source": "gd_hotpotqa_yesno"' not in line: continue
        r=json.loads(line)
        if r.get('qtype')!='noul' or r.get('role')!='aff': continue
        qs.append(r['instructions'])
print(len(qs))
acc=[]; a_only=0; b_only=0
for q in qs:
    a=PA.base_feasible_a('syntactic',q,E); b=PB.base_feasible_b('syntactic',q,E)
    if a and b: acc.append(q)
    elif a: a_only+=1
    elif b: b_only+=1
print('both accept',len(acc),'a only',a_only,'b only',b_only)
random.seed(1)
bad=0
for q in random.sample(acc,40):
    t=sorted(PA.syntactic_targets(q,E,"Is it true that"))
    rel=[PA.classify_a(q,x,'syntactic',E)[0]+'/'+PB.classify_b(q,x,'syntactic',E,SRC.FRAMES_TRAIN)[0] for x in t]
    print(q,'=>',t[0],rel)
# every accepted: check all targets read opposite by both
n=0
for q in acc:
    for fr in SRC.FRAMES_TRAIN:
        for x in PA.syntactic_targets(q,E,fr):
            ra=PA.classify_a(q,x,'syntactic',E,SRC.FRAMES_TRAIN)[0]; rb=PB.classify_b(q,x,'syntactic',E,SRC.FRAMES_TRAIN)[0]
            if not (ra==rb=='opposite'): n+=1
print('targets not read opposite by both:',n)
# shape stats of refused
refused=[q for q in qs if q not in set(acc)]
random.seed(2)
for q in random.sample(refused,15): print('REFUSED',q)
