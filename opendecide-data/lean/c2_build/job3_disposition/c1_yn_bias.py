import json, glob, collections
LEAN="/Users/aryamahadik/Documents/jev/opendecide-data/lean"
for fam in ["T28","T29","T30","T26","T12"]:
    cand={}
    for l in open(f"{LEAN}/data/c2_parts/{fam}/out/candidates_c2.jsonl"):
        r=json.loads(l)
        if r["qtype"]=="noul": cand[r["id"]]=r
    labs={}
    for p in sorted(glob.glob(f"{LEAN}/data/c2_crowd_shards/{fam}/labels_q35_4b_main500k/shard_*.jsonl")):
        for l in open(p):
            d=json.loads(l)
            if d["id"] in cand: labs[d["id"]]=d["probs"]
    by=collections.defaultdict(lambda:[0,0,0,0])
    for i,r in cand.items():
        g=1 if r["gold"] in (1,"1","yes",True) else 0
        py=1 if labs[i]["yes"]>labs[i]["no"] else 0
        q=r["meta"]["qform"]
        b=by[q]; b[0]+=1; b[1]+=g; b[2]+=py; b[3]+=(g==py)
    print("==",fam)
    for q,(n,g,py,ok) in sorted(by.items(), key=lambda kv:-kv[1][0])[:8]:
        print(f"   {q:18s} n={n:4d} gold_yes={100*g/n:3.0f}% pred_yes={100*py/n:3.0f}% acc={100*ok/n:3.0f}%")
