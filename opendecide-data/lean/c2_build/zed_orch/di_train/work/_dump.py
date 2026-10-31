import json,sys
D=sys.argv[1];R=f"{D}/DI-TS/reads"
key=json.load(open(f"{R}/keys/key.json"));rows={}
for f in ("candidates_stage.jsonl","mixdev_S5_stage.jsonl"):
    for l in open(f"{D}/DI-TS/stage/{f}"): x=json.loads(l);rows[x["id"]]=x
inv={}
for k,v in key.items(): inv.setdefault(v,{})[k[0]]=k.split(":")[1]
T=json.load(open(f"{R}/TASKS.json"));ans={}
for t in T.values():
    for o in json.load(open(t["answer_file"])): ans[(t["reader"],o["qid"])]=(o["answer"],o["confidence"])
S=json.load(open(f"{R}/SCORE.json"))["flagged"]
for i,r in enumerate(S):
    x=rows[r];m=x["meta"]
    print(f"### {i} {r} {x['meta']['card_id'].split(':')[1]}\nSTATE: {x['state'][:700]}\nGOLD: {x['gold']} | A={ans.get(('A',inv[r]['A']))} B={ans.get(('B',inv[r]['B']))}")
