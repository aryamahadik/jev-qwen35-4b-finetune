import pickle, collections, random, re
rows=pickle.load(open('rows10k_b.pkl','rb'))
ll=[(r,st) for r,st in rows if st["head"]=="ll"]
def feats(r,st):
    s=r["state"]
    run=s.split("<run>")[-1] if "<run>" in s else s[-200:]
    ins=r["instructions"]
    return {"tpl":(st["template"],st["style"]),"len":len(s),"run":len(run),"nt":len(st["tests"]),
            "maxl":max(map(len,s.split("\n"))),"q":len(ins),"nopt":len(r["options"]),
            "nfail":sum(1 for x in st["report"] if x!="p")}
F=[feats(r,st) for r,st in ll]
random.seed(1); idx=list(range(len(ll))); random.shuffle(idx); cut=len(idx)*4//5
def run(keyf,name):
    tab=collections.defaultdict(collections.Counter)
    for i in idx[:cut]: tab[keyf(F[i])][ll[i][0]["gold"]]+=1
    ok=sum((tab[keyf(F[i])].most_common(1)[0][0] if keyf(F[i]) in tab else None)==ll[i][0]["gold"] for i in idx[cut:])
    print(name, round(ok/(len(idx)-cut),4), len(tab))
run(lambda f:f["tpl"],"tpl")
run(lambda f:(f["tpl"],f["len"]),"tpl,len")
run(lambda f:(f["tpl"],f["run"]),"tpl,runlen")
run(lambda f:(f["tpl"],f["nfail"]),"tpl,nfail")
run(lambda f:(f["tpl"],f["nt"],f["nfail"]),"tpl,nt,nfail")
run(lambda f:(f["tpl"],f["nopt"]),"tpl,nopt")
run(lambda f:(f["len"],),"len")
c=collections.Counter(r["gold"] for r,_ in ll); print(c.most_common(1))
