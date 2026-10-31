import sys
sys.path.insert(0,'.')
from c2_kit import cards
mx,tok=cards._tokenizer()
c=lambda s: len(tok.encode(s,add_special_tokens=False).ids)
full="""Log rules (lines in time order):
- A step is done if a try got 200, 201 or 204, a retry with the same idempotency key got 409, or a try got 202 and the job's last poll says succeeded.
- Any other try status does nothing. A poll's status 200 means nothing; its state counts.
- Result: amount_cents on the try that got 200 or 201, else on the job's last poll.
- amount_cents is cents (100 = $1).
Claim rules: a claim is about the step whose target it names.
- No step in the log has that target: not shown in the log.
- That step is not done, or the claim's amount differs from its result: contradicted.
- Otherwise: supported.
The log is complete and the only evidence: no other call, retry or poll took place."""
comp_b="""Log rules (lines in time order):
- Done if try 200, 201 or 204, retry with the same key 409, or try 202 and its job's last poll says succeeded.
- Any other try status does nothing; a poll's 200 means nothing, its state counts.
- Result: amount_cents on the 200 or 201 try, else the job's last poll.
- amount_cents: cents (100 = $1).
Claim rules: a claim is about the step whose target it names. No step has that target: not shown in the log. That step is not done, or its amount differs from the result: contradicted. Otherwise: supported.
The log is complete and the only evidence: no other call, retry or poll took place."""
comp_p=comp_b.replace("\n- "," ").replace("\nClaim"," Claim").replace("\nThe log"," The log")
print(c(full),c(comp_b),c(comp_p))
print(comp_p)
for s in ("\n- ","\n","- "," ","; ","Done: "): print(repr(s),c("a"+s+"b")-2)
