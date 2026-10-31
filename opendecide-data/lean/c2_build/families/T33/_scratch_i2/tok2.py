import sys
sys.path.insert(0,'.')
from c2_kit import cards
mx,tok=cards._tokenizer()
c=lambda s: len(tok.encode(s,add_special_tokens=False).ids)
G={
"done":"A step is done if a try got 200, 201 or 204, a retry with the same idempotency key got 409, or a try got 202 and the job's last poll says succeeded.",
"other":"Any other try status does nothing. A poll's status 200 means nothing; its state counts.",
"res":"Result: amount_cents on the try that got 200 or 201, else on the job's last poll.",
"claim":"Claim rules: a claim is about the step whose target it names.\n- No step in the log has that target: not shown in the log.\n- That step is not done, or the claim's amount differs from its result: contradicted.\n- Otherwise: supported.",
"closed":"The log is complete and the only evidence: no other call, retry or poll took place.",
"tclm":"If several claims are contradicted or not shown, answer the one first in the message; if none, answer None.",
"tchk":"If several checks fail, answer the lowest-numbered one; if none fails, answer None.",
"crit":"Success criterion for step 3: every check must hold; a check on a value the log does not show fails; polls are not tries.",
}
C={
"done":["Done if a try got 200, 201 or 204, a retry with the same key got 409, or a try got 202 and its job's last poll says succeeded.",
"Done if try 200, 201 or 204, retry with the same key 409, or try 202 and its job's last poll says succeeded.",
"A step is done if a try got 200, 201 or 204, a retry with the same key got 409, or a 202 try's job last poll says succeeded.",
"Done if a try got 200, 201 or 204; a retry with the same key got 409; or a try got 202 and the job's last poll says succeeded.",
"Done if: try 200, 201 or 204; retry with the same key 409; try 202 with the job's last poll succeeded."],
"other":["Any other try status does nothing. A poll's status 200 means nothing; its state counts.",
"Any other try status: nothing. A poll's status 200: nothing; its state counts.",
"Any other try status counts for nothing; a poll's status 200 too, only its state.",
"Any other try status does nothing; a poll's 200 means nothing, its state counts."],
"res":["Result: amount_cents from the 200 or 201 try, else the job's last poll.","Result: amount_cents on the 200 or 201 try, else the job's last poll.","Result: amount_cents on the 200 or 201 try, else on the last poll."],
"claim":["Claim rules: a claim is about the step whose target it names. No step has that target: not shown in the log. That step is not done, or its amount differs from the result: contradicted. Otherwise: supported.",
"A claim is about the step whose target it names. No step has that target: not shown in the log. That step is not done, or its amount differs from the result: contradicted. Otherwise: supported.",
"Claim rules: a claim is about the step with its target. No such step: not shown in the log. That step is not done, or its amount differs from the result: contradicted. Otherwise: supported.",
"Claims: a claim is about the step whose target it names. No step with that target: not shown. Step not done, or its amount differs from the result: contradicted. Otherwise: supported."],
"closed":["The log is complete and the only evidence: no other call, retry or poll took place.","The log is complete and the only evidence: no other call, retry or poll happened.","The log is complete and the only evidence; no other call, retry or poll took place.","Complete log, the only evidence: no other call, retry or poll took place."],
"tclm":["Answer the first claim in the message that is contradicted or not shown; if none, answer None.","If several claims are contradicted or not shown, answer the first in the message; if none, None."],
"tchk":["Answer the lowest-numbered failing check; if none fails, answer None.","If several checks fail, answer the lowest-numbered; if none, None."],
"crit":["Success criterion for step 3: every check must hold; a check on a value not in the log fails; polls are not tries.","Step 3 criterion: every check must hold; a check on a value not in the log fails; polls are not tries."],
}
for k,g in G.items():
    print(k,c(g))
    for a in C[k]:
        print('   ',c(a),cards.variant_problems(g,a),a[:60])
