import json, re, collections
P="/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts/golden_train.jsonl"
rx=re.compile(r"(what should (happen|the (agent|assistant|team|analyst|clerk|system|operator|handler|reviewer))|which action|what action|next step|how should .{0,40}(handle|treat|process|route|respond)|what is the (right|correct|appropriate) (action|disposition|outcome|response|handling)|should (the )?(invoice|claim|request|ticket|incident|order|refund|application) be)", re.I)
c=collections.Counter(); tot=collections.Counter()
for line in open(P):
    r=json.loads(line)
    if r['qtype']!='choice': continue
    tot[r['source']]+=1
    if rx.search(r['instructions']): c[r['source']]+=1
print(sum(c.values()), len(c))
for s,n in c.most_common(25): print(f"{s:34s} {n:6d} / {tot[s]}")
