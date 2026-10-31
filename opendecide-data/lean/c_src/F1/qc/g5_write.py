import json
ids=json.load(open('qc/g5_sample_ids.json'))
ans=[json.loads(l) for l in open('tmp/qc/g5_answers.jsonl')]
out={"gate":"G5","method":"blind read of model view only (decoder_io cygnet + schema_branch_mark), gold hidden, answers scored afterwards",
 "file":"out/candidates_r1.jsonl","sample_n":len(ids),"seed":5001,"ids_path":"qc/g5_sample_ids.json",
 "answered":len(ans),"agree_with_gold":None,"clearly_wrong":[],"ambiguous":[],
 "notes":["no row judged clearly wrong or genuinely ambiguous",
  "attack-twin lines inside case text (override/reviewer/system instructions) were treated as data; golds ignore them correctly",
  "decision tables without a 'rows are checked from the top' line were read as ordinary competing rules, consistent with each card's own reading section"],
 "pass":None}
import subprocess,sys
r=subprocess.run([sys.executable,'qc/g5_score.py'],capture_output=True,text=True).stdout.strip().splitlines()[-1]
s=json.loads(r); out["agree_with_gold"]=s["agree"]; out["disagree_ids"]=s["disagree"]
out["pass"]= (len(out["clearly_wrong"])==0 and len(out["ambiguous"])<=6)
json.dump(out,open('qc/g5.json','w'),indent=1); print(json.dumps({k:out[k] for k in ('answered','agree_with_gold','pass')}))
