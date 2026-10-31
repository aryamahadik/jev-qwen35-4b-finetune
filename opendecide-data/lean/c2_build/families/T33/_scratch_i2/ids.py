import sys
sys.path.insert(0,'.')
from c2_kit import cards
mx,tok=cards._tokenizer()
c=lambda s: len(tok.encode(s,add_special_tokens=False).ids)
for s in ["ik-16d7","ik-e696","ik-eac5","ik-16d","ik-16","k16d7","job-240a","job-27b0","job-3be5","j240a","job-24","ORD-20911","acct-7611","111126","7700","135090","239050",
 '{"step":1,"try":1,"tool":"shop.issue_refund","args":{"target":"ORD-20911","idempotency_key":"ik-16d7","amount_cents":111126},"status":202,"result":{"job":"job-240a"}}',
 '{"step":1,"poll":"job-240a","status":200,"result":{"state":"succeeded","amount_cents":111126,"duration_ms":135090}}',
 "step,line,tool,target,idempotency_key,field,requested,status,job,state,result,duration_ms",
 "1,poll,,,,rows,,200,job-766b,succeeded,29340,",
 "| step | line | tool | target | idempotency_key | field | requested | status | job | state | result | duration_ms |\n|---|---|---|---|---|---|---|---|---|---|---|---|",
 "Tool log:\n","Definitions:\n"]:
    print(c(s),s[:70])
