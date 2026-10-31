"""JOB3: pooled cautious-lean of C1 on C2 action-permission yes/no forms (existing 1-view crowd labels).
lean = predicted yes share - gold yes share; for a PERMISSIVE form (yes = go ahead) a negative lean is cautious;
for a CAUTIOUS form (yes = ask / hold / deny) a positive lean is cautious."""
import json, glob, collections, math
LEAN="/Users/aryamahadik/Documents/jev/opendecide-data/lean"
PERM={"T28":["yn_allow"],"T29":["yn_go","yn_permitted"],"T30":["yn_proceed","yn_settle","yn_no_hold"],"T26":["yn_apply","yn_clears"],
      "T12":["yn_release","yn_within_tol"]}
CAUT={"T28":["yn_ask","yn_deny"],"T29":["yn_ask","yn_refuse"],"T30":["yn_ask","yn_hold","yn_not_proceed"],"T26":["yn_fails","yn_hold","yn_not_apply"],
      "T12":["yn_over_tol","yn_price_review","yn_payment_stopped","yn_not_release"]}
out={}
tot={"perm":[0,0,0],"caut":[0,0,0]}
for fam in PERM:
    cand={}
    for l in open(f"{LEAN}/data/c2_parts/{fam}/out/candidates_c2.jsonl"):
        r=json.loads(l)
        if r["qtype"]=="noul": cand[r["id"]]=r
    labs={}
    for p in sorted(glob.glob(f"{LEAN}/data/c2_crowd_shards/{fam}/labels_q35_4b_main500k/shard_*.jsonl")):
        for l in open(p):
            d=json.loads(l)
            if d["id"] in cand: labs[d["id"]]=d["probs"]
    for kind,forms in (("perm",PERM[fam]),("caut",CAUT[fam])):
        n=g=py=0
        for i,r in cand.items():
            if r["meta"]["qform"] in forms:
                n+=1; g+= r["gold"] in (1,"1","yes",True); py+= labs[i]["yes"]>labs[i]["no"]
        out[(fam,kind)]=(n,g,py)
        t=tot[kind]; t[0]+=n; t[1]+=g; t[2]+=py
        lean=(py-g)/n
        print(f"{fam} {kind:4s} n={n:4d} gold_yes={100*g/n:4.1f}% pred_yes={100*py/n:4.1f}% lean={100*lean:+5.1f} pts")
for kind,(n,g,py) in tot.items():
    lean=(py-g)/n; se=math.sqrt(0.25/n)*100
    print(f"POOLED {kind} n={n} gold_yes={100*g/n:.1f}% pred_yes={100*py/n:.1f}% lean={100*lean:+.1f} pts (SE ~{se:.1f})")
json.dump({f"{k[0]}:{k[1]}":v for k,v in out.items()}, open("c1_lean.json","w"))
