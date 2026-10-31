import pickle, collections, random, sys
rows=pickle.load(open('rows6k.pkl','rb'))
ll=[(r,st) for r,st in rows if st["head"]=="ll"]
def key(r,st,mode):
    d=len(st["code"])-len(st["orig"])
    if mode=="tpl_delta": return (st["template"],st["style"],d)
    if mode=="tpl": return (st["template"],st["style"])
    if mode=="tpl_len": return (st["template"],st["style"],len(st["code"]))
    if mode=="len": return (len(st["code"]),)
    if mode=="delta": return (d,)
random.seed(1); idx=list(range(len(ll))); random.shuffle(idx); cut=len(idx)*4//5
for mode in ("tpl","tpl_delta","tpl_len","len","delta"):
    tab=collections.defaultdict(collections.Counter)
    for i in idx[:cut]: tab[key(*ll[i],mode)][ll[i][0]["gold"]]+=1
    ok=0
    for i in idx[cut:]:
        c=tab.get(key(*ll[i],mode))
        pred=c.most_common(1)[0][0] if c else None
        ok+= pred==ll[i][0]["gold"]
    print(mode, round(ok/(len(idx)-cut),4), "n_keys",len(tab))
dd=collections.defaultdict(collections.Counter)
for r,st in ll: dd[r["gold"]][len(st["code"])-len(st["orig"])]+=1
for k in sorted(dd): print(k, dict(sorted(dd[k].items())))
print("gold dist", collections.Counter(r["gold"] for r,_ in ll))
