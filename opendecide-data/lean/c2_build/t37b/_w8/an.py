import pickle,sys,collections as C
ch=pickle.load(open(sys.argv[1],'rb'))
print(len(ch)); r0=ch[0][0]; print(list(r0.keys())); print(r0['options'],r0['gold'],r0['meta'])
pos=C.defaultdict(C.Counter); kd=C.defaultdict(C.Counter); n=C.Counter()
for r,k in ch:
    kk=len(r['options']); g=r['options'].index(r['gold']); n[kk]+=1
    pos[kk][g]+=1
    for key in k[g]: kd[kk][key]+=1
    kd[kk]['all']+=1
print(n,{k:dict(v) for k,v in pos.items()})
for kk in kd: print(kk,{a:round(b/kd[kk]['all'],3) for a,b in kd[kk].items()})
# per-option base rate of kinds
base=C.defaultdict(C.Counter)
for r,k in ch:
    kk=len(r['options'])
    for s in k:
        for key in s: base[kk][key]+=1
    base[kk]['all']+=len(k)
for kk in base: print('opt',kk,{a:round(b/base[kk]['all'],3) for a,b in base[kk].items()})
