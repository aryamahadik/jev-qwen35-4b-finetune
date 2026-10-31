"""Score the G5 blind read: tmp/chk/g5_answers.jsonl ({"k", "ans": displayed letter, "flag"?, "note"?}) against gold,
mapping the displayed letter back through the row's permutation. Prints counts and the k of disagreements only."""
import json, sys
F7 = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F7"
P = {json.loads(l)["k"]: json.loads(l) for l in open(F7 + "/tmp/chk/g5_prompts.jsonl")}
rows = {}
for l in open(F7 + "/out/candidates_r1.jsonl"):
    r = json.loads(l); rows[r["id"]] = r
A = {}
for l in open(F7 + "/tmp/chk/g5_answers.jsonl"):
    a = json.loads(l); A[a["k"]] = a
dis = []
for k, a in sorted(A.items()):
    p = P[k]; r = rows[p["id"]]; perm = p["perm"]
    j = "ABCDEFGHIJ".index(a["ans"]); mine = r["options"][perm[j]]
    if mine != r["gold"]:
        dis.append(k)
print(json.dumps({"read": len(A), "agree": len(A) - len(dis), "disagree_k": dis}))
