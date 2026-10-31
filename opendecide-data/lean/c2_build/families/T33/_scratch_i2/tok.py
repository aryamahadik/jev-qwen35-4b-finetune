import sys
sys.path.insert(0,'.')
from c2_kit import cards
mx,tok=cards._tokenizer()
c=lambda s: len(tok.encode(s,add_special_tokens=False).ids)
P=[
("done",
 "- A step is done if a try got 200, 201 or 204, a retry with the same idempotency key got 409, or a try got 202 and the job's last poll says succeeded.",
 "- A step is done if a try got 200, 201 or 204, a retry with the same key got 409, or a try got 202 and its job's last poll says succeeded.",
 "- Done if a try got 200, 201 or 204, a retry with the same key got 409, or a try got 202 and its job's last poll says succeeded."),
("other",
 "- Any other try status does nothing. A poll's status 200 means nothing; its state counts.",
 "- Any other try status does nothing; a poll's status 200 means nothing, its state counts.",
 "- Any other try status: nothing. Poll status 200: nothing, its state counts."),
("res",
 "- Result: amount_cents on the try that got 200 or 201, else on the job's last poll.",
 "- Result: amount_cents on the 200 or 201 try, else on the job's last poll.",
 "- Result: amount_cents from the 200 or 201 try, else the job's last poll."),
("unit",
 "- amount_cents is cents (100 = $1).",
 "- amount_cents: cents (100 = $1).",
 "- amount_cents: cents (100 = $1)."),
("claim",
 "Claim rules: a claim is about the step whose target it names.\n- No step in the log has that target: not shown in the log.\n- That step is not done, or the claim's amount differs from its result: contradicted.\n- Otherwise: supported.",
 "Claim rules: a claim is about the step whose target it names. No step in the log has that target: not shown in the log. That step is not done, or its amount differs from the result: contradicted. Otherwise: supported.",
 "Claims name a step by its target. No step has that target: not shown. That step is not done, or its amount differs from the result: contradicted. Otherwise: supported."),
("crit",
 "Success criterion for step 3: every check must hold; a check on a value the log does not show fails; polls are not tries.",
 "Success criterion for step 3: every check must hold; a check on a value not in the log fails; polls are not tries.",
 "Success criterion for step 3: every check must hold; a check on a value not in the log fails; polls are not tries."),
("tchk",
 "If several checks fail, answer the lowest-numbered one; if none fails, answer None.",
 "Answer the lowest-numbered failing check; if none fails, answer None.",
 "Answer the lowest-numbered failing check, else None."),
("tclm",
 "If several claims are contradicted or not shown, answer the one first in the message; if none, answer None.",
 "Answer the first claim in the message that is contradicted or not shown; if none, answer None.",
 "Answer the first claim in the message that is contradicted or not shown, else None."),
("closed",
 "The log is complete and the only evidence: no other call, retry or poll took place.",
 "The log is complete and the only evidence: no other call, retry or poll took place.",
 "The log is complete and the only evidence: no other call, retry or poll took place."),
("head","Log rules (lines in time order):","Log rules (lines in time order):","Log rules (lines in time order):"),
]
for n,f,a,b in P:
    print(n,c(f),c(a),c(b), cards.variant_problems(f.lstrip('- '),a.lstrip('- ')), cards.variant_problems(f.lstrip('- '),b.lstrip('- ')))
