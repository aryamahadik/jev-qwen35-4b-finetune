# G3-H extraction T26-extract_g3h-70f7fd01-000 (family T26)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T26/pilot_i1/g3h/answers/T26-extract_g3h-70f7fd01-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "change": <value or null>, "counterparty": <value or null>, "req_id": <value or null>, "requester": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q6ead29e655",
  "text": "Voicemail transcript: Yeah, hi, it's Rosa Quintero from Forge Hollow Tools, and this is urgent, so I'm going to ramble a bit, sorry. Our COO is waiting, the deadline is very tight, and the director keeps chasing us. What I'm asking is to pay the invoice that came with the request, and the reference is INV-21676. It's a bit of a mess on our end and I'm pushing hard, so the cut-off is close. Thanks, and sorry for the mess. Bye.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qa16b14c929",
  "text": "Summary: Forwarded request, plain and routine\nRequested by: Ada Ekwueme, Forge Hollow Tools\nReference: INV-21776\nCover line: Forwarding the text below exactly as it was written.\nForwarded text:\nPlease release payment on the invoice sent with the request.\nThank you for your help with this.\nKind regards,\nAda Ekwueme\nDetails: Calm, routine, and courteous throughout, with the reference kept exactly as shown above.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q6e1dc9a0fc",
  "text": "Summary: Urgent request to send the refund the customer asked for\nRequested by: Theo Vance, Marrowline Media\nReference: RF-42937\nPriority: High, with a hard cut-off\nDetails: Background is that our VP is waiting on this and the cut-off is tight. People who depend on this are waiting too, so the request is being pushed quickly from our side. Thank you, truly.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q7370aed775",
  "text": "Summary: Follow-up on INV-90515\nRequested by: Ines Calloway, Forge Hollow Tools\nQuoted ask: please pay the invoice that came with the request, reference INV-90515.\nDetails: picking up from the thread above, the wording stays exactly the same. Sorry for the repeated messages, the thread has grown a bit. Our office is in a bit of a squeeze, so the timing is loose. Thanks for your patience with this, it is appreciated.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qd120254615",
  "text": "Viktor Sandor from Ondrell Seed Co. Hi, sorry, going round in circles here.\nThe story is our marketing folks asked for the thing a while back, and it sort of got stuck in the middle, long story.\nRight, so please add admin rights on the billing system, reference IT-23409. Sorry, rambling. Thanks for bearing with the wandering, it is a bit of a jumble.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q1b23539bd9",
  "text": "Subject: URGENT request SH-70357\n\nHi finance team,\n\nThis message comes from the assistant to Kenji Morita, who is asking for the matter to be moved quickly.\n\nPlease send the pending shipment to a new address.\n\nThe CFO is waiting, the deadline is close, and priority is high. The reference is SH-70357, so thank you for moving fast on it.\n\nThanks,\nAssistant to Kenji Morita, Saltmere Boat Components",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qcc685327b2",
  "text": "Memo\nFrom: Ravi Anand, Rindle Linen Hire\nRe: urgent request LG-91123\n\nOriginal message: This is urgent, and the CFO is waiting. Ravi Anand wants this matter moved fast, and the VP is watching the deadline. Please issue a new login security key for the account.\n\nNudge: Following up ahead of the cut-off, because priority is high. Thank you for moving quickly, and thanks again.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q01ca88bcf2",
  "text": "Summary: Forwarded request, plain and routine\nRequested by: Ada Ekwueme, Forge Hollow Tools\nReference: INV-21776\nCover line: Forwarding the text below exactly as it was written.\nForwarded text:\nPlease release payment on the invoice sent with the request.\nThank you for your help with this.\nKind regards,\nAda Ekwueme\nDetails: Calm, routine, and courteous throughout, with the reference kept exactly as shown above.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q61b9fa9d57",
  "text": "Subject: Urgent request, reference BK-61326\n\nHi finance team,\n\nForwarding this from my colleague below, it is urgent and our CEO is waiting on it.\n\nForwarded message:\nPlease switch the payout bank account on file. The reference is BK-61326. The cut-off is fast approaching, and this is a priority for our leadership.\n\nThanks,\nInes Calloway\nCaldora Metrics Software",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q34a90ae402",
  "text": "Aiko Brandt from Jorvik Electrical Wholesale, urgent: please swap in the new tax form for the vendor, and do it fast, because the VP is waiting.\nRef TX-79461, and the CFO is watching the cut-off, so priority is high and speed is key.\nThanks for moving fast, and thank you for your help with this, as it matters to the team at Jorvik Electrical Wholesale.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q59a1be1331",
  "text": "Viktor Sandor from Ondrell Seed Co. Hi, sorry, going round in circles here.\nThe story is our marketing folks asked for the thing a while back, and it sort of got stuck in the middle, long story.\nRight, so please add admin rights on the billing system, reference IT-23409. Sorry, rambling. Thanks for bearing with the wandering, it is a bit of a jumble.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q15e4e8c624",
  "text": "Subject: Routine request, reference VO-94005\n\nHi finance team,\n\nAda Ekwueme here from Oberlane Freight Lines, with a calm, routine request. Please onboard the vendor as a supplier. The reference is VO-94005, and the pace is easy from our side.\n\nFollowing up on my previous message, just a gentle nudge to see whether it is in your queue. Hope the rest of your session goes smoothly.\n\nThanks,\nAda Ekwueme\nOberlane Freight Lines",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q4866297daf",
  "text": "Memo\nFrom: the assistant to Omar Farouk, Jorvik Electrical Wholesale\nRe: request TX-23819\n\nReplying in this thread, quoting the original ask: Please swap in the new tax form for the vendor.\n\nThe matter is calm and routine, and it sits well within normal planning. Omar Farouk is grateful for your patience with this, and thank you for keeping it in the usual flow.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qace38541ea",
  "text": "Subject: URGENT request DX-25171\n\nHi finance team,\n\nThis message comes from the assistant to Aiko Brandt, who is asking for the matter to be moved quickly.\n\nPlease send the customer list export to the requester.\n\nThe CFO is waiting, the deadline is close, and priority is high. The reference is DX-25171, so thank you for moving fast on it.\n\nThanks,\nAssistant to Aiko Brandt, Halvorn Fitness Gear",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q23fefebe17",
  "text": "Subject: Re: urgent request, VO-31406\n\nHi finance team,\n\nThank you for your fast attention. Quoting my previous note here: 'Please add the vendor to the supplier list.'\n\nThis is urgent, and our CFO is waiting. The deadline is tight and the cut-off is fast approaching, so the matter is a priority for our leadership. The request comes from Lucia Ferrante at Icemere Cold Store, and our reference is VO-31406.\n\nThanks,\nLucia Ferrante\nIcemere Cold Store",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q26ad65f04b",
  "text": "Dear finance team,\n\nThis is an urgent request from Velcora Energy Services, and our CFO is waiting for a reply. Background: our auditors spotted a mismatch in the details on our side, and the cut-off for our report is fast approaching.\n\nReference: RA-75437\nRequested by: Mira Castell\n\nPlease update the address payments are sent to. That update is the piece we are waiting on, and the mismatch goes away after it. This is a priority for our leadership, so please move it to the top of your queue.\n\nThank you,\nMira Castell\nVelcora Energy Services",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q45d6512b93",
  "text": "Summary: Follow-up on VO-58045\nRequested by: Kofi Mensah, Icemere Cold Store\nQuoted ask: please add the vendor to the supplier list, reference VO-58045.\nDetails: picking up from the thread above, the wording stays exactly the same. Sorry for the repeated messages, the thread has grown a bit. Our office is in a bit of a squeeze, so the timing is loose. Thanks for your patience with this, it is appreciated.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q9d914af923",
  "text": "Requested by: Mira Castell, Lexwell Translations\nReference: INV-58506\nDetails: so, um, the team has been running around in circles, long story, sort of messy. Right, so please release payment on the invoice sent with the request, reference INV-58506. Sorry, it's a bit rambly, thanks for bearing with it, it is appreciated.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q0ad5f33b21",
  "text": "Memo\nFrom: the assistant to Arjun Mehta, Icemere Cold Store\nRe: request VO-12268\n\nReplying in this thread, quoting the original ask: Please onboard the vendor as a supplier.\n\nThe matter is calm and routine, and it sits well within normal planning. Arjun Mehta is grateful for your patience with this, and thank you for keeping it in the usual flow.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q9dc4549a74",
  "text": "Subject: Urgent request, reference PY-91193\n\nHi finance team,\n\nForwarding this from my colleague below, it is urgent and our CEO is waiting on it.\n\nForwarded message:\nPlease redirect the employee's salary deposits. The reference is PY-91193. The cut-off is fast approaching, and this is a priority for our leadership.\n\nThanks,\nClara Jun\nOravelle Potters Guild",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q405f89c50d",
  "text": "Subject: Urgent, reference CT-33131\n\nHi finance team,\n\nSo, this is a bit of a long story, sorry in advance. Our CFO is waiting on it, and the deadline is tight. We have been going back and forth internally for a while, and the cut-off is fast approaching, so this is a priority for us.\n\nPlease switch the contract to the new payment terms. The reason is that the update happened upstream, and the old figures keep showing up in the system, which is a big headache for the team. Anyway, the reference is CT-33131, and this comes from Yara Haddad at Brassett Laboratory Glass.\n\nThanks, sorry again for the wall of text,\nYara Haddad\nBrassett Laboratory Glass",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q2ae418e845",
  "text": "Memo\nFrom: Malik Oduya, Dunmere Pipe Works\nRe: urgent request CL-74482\n\nOriginal message: This is urgent, and the CFO is waiting. Malik Oduya wants this matter moved fast, and the VP is watching the deadline. Please raise the customer's credit limit.\n\nNudge: Following up ahead of the cut-off, because priority is high. Thank you for moving quickly, and thanks again.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q513a924976",
  "text": "Subject: URGENT request HR-37225\n\nHi team,\n\nMira Castell at Cassillo Risk Brokers here, forwarding my message below with a short cover line: this is urgent and the deadline is close.\n\nForwarded text:\nPlease edit the salary band in the employee record. The reference is HR-37225. The VP is waiting, so priority is high and the cut-off is near. Thank you for moving fast.\n\nRegards,\nMira Castell",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q88d940c3a2",
  "text": "Internal memo\nFrom: Ravi Anand, Oravelle Potters Guild\nRe: PY-35024, flagged as urgent\n\nOur VP is waiting on this, and the deadline is tight.\n\nWe are asking to redirect the employee's salary deposits, and I'm marking it as a priority from our side. Thanks for the quick attention, and sorry for the rush.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qc1332d12ef",
  "text": "Memo\nFrom: the assistant to Clara Jun, Carnmoor Kitchen Fitters\nRe: request PL-21429\n\nThis memo is written by the assistant on behalf of Clara Jun, who is away from the office. The matter is calm and routine, and it is a straightforward tidy-up.\n\nPlease load the new unit prices onto open orders.\n\nThank you for your help with this, and warm wishes.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q6a23d90690",
  "text": "Summary: Forwarded request, plain and routine\nRequested by: Tomas Ferreira, Marlhorn Trail Gear\nReference: DX-96423\nCover line: Forwarding the text below exactly as it was written.\nForwarded text:\nPlease export the customer contact list to the requester.\nThank you for your help with this.\nKind regards,\nTomas Ferreira\nDetails: Calm, routine, and courteous throughout, with the reference kept exactly as shown above.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q3329e0bfe5",
  "text": "Memo\nFrom: Yara Haddad, Tarnwell Metals\nTo: finance team\nRe: Urgent, reference CT-73974\n\nSo, here is the situation in bits.\n\nOpening bit: our auditors caught a mismatch on our side.\n\nMiddle bit: the fix is to switch the contract to the new payment terms.\n\nClosing bit: our CFO is waiting, the deadline is tight, and this is a priority for our leadership. Reference: CT-73974. Sorry for the rush.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q383600f0ac",
  "text": "Subject: Ref PL-23776, in pieces\n\nHello team,\n\nSending this in pieces, as the bits came in. Our crew at Sallow Tongue School has been stuck in a tangle with the shared workspace, and it has been slow going since.\n\nAlso, the old setup has stopped fitting how we work, so the team wants a fresh start.\n\nSo please update open orders to the new price list, reference PL-23776. Appreciate your time on this.\n\nBest,\nTheo Vance",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qced28ba95b",
  "text": "Memo\nFrom: the assistant to Ines Calloway, Forge Hollow Tools\nRe: request INV-63816\n\nThis memo is written by the assistant on behalf of Ines Calloway, who is away from the office. The matter is calm and routine, and it is a straightforward tidy-up.\n\nPlease release payment on the invoice sent with the request.\n\nThank you for your help with this, and warm wishes.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q17b7838223",
  "text": "Dear finance team members,\n\nOur director is waiting on this, and the deadline is tight, so I am being direct. I am writing to load the new unit prices onto open orders, reference PL-27481, and I'm marking it as a priority.\n\nFollowing up on my note above, and the cut-off is getting tighter. I'm nudging this again because the deadline is pressing.\n\nKind regards,\nElias Brook\nCarnmoor Kitchen Fitters",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q34a617b1b8",
  "text": "Memo\nFrom: Clara Jun, Ondrell Seed Co\nRe: Urgent request IT-48993\n\nThis is urgent, and our CFO has been asking about it.\n\nOur ask is to grant administrator access to the billing system, and the reference is IT-48993.\n\nThe deadline is tight and the cut-off is close, so I'm marking this as a priority from our side.\n\nSorry for the rush, and thank you for reading this through.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qb8c97112d0",
  "text": "Subject: URGENT PY-72340\n\nHi team,\n\nSo sorry for the long message, but let me explain properly. Bea Holm from Velmara Gatherings here, and the thing is the director keeps bringing this up, and the CFO has been asking about it too, so it has become a talking point in meetings. Anyway, please redirect the employee's salary deposits, and do it fast, because the cut-off is close and the VP is waiting. The reference is PY-72340, which is what people keep quoting back at the office.\n\nThanks, and sorry again for the wandering.\nBea Holm",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q3044699d20",
  "text": "Summary: Follow-up on IT-38162\nRequested by: Noor Siddiqui, Fernbrook Dental Supply\nQuoted ask: please grant administrator access to the billing system, reference IT-38162.\nDetails: picking up from the thread above, the wording stays exactly the same. Sorry for the repeated messages, the thread has grown a bit. Our office is in a bit of a squeeze, so the timing is loose. Thanks for your patience with this, it is appreciated.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qc634f56292",
  "text": "Ticket: RA-13176\nOpened by: Jonah Pell, Velcora Energy Services\nSubject: Rush to update the address payments are sent to\nNotes: Our director has asked for this, and the cut-off is tight. We have been holding off on it, which is why it has become urgent. The rest of the team is waiting on this, so it is being raised quickly.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q85a7108cc0",
  "text": "Memo\nFrom: Malik Oduya, Dunmere Pipe Works\nRe: urgent request CL-74482\n\nOriginal message: This is urgent, and the CFO is waiting. Malik Oduya wants this matter moved fast, and the VP is watching the deadline. Please raise the customer's credit limit.\n\nNudge: Following up ahead of the cut-off, because priority is high. Thank you for moving quickly, and thanks again.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qdbe1cf412c",
  "text": "Summary: Follow-up on IT-38162\nRequested by: Noor Siddiqui, Fernbrook Dental Supply\nQuoted ask: please grant administrator access to the billing system, reference IT-38162.\nDetails: picking up from the thread above, the wording stays exactly the same. Sorry for the repeated messages, the thread has grown a bit. Our office is in a bit of a squeeze, so the timing is loose. Thanks for your patience with this, it is appreciated.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qc2ea94b51a",
  "text": "Subject: URGENT HR-23510\n\nHi team,\n\nSo sorry for the long message, but let me explain properly. Kenji Morita from Sudsway Laundry here, and the thing is the director keeps bringing this up, and the CFO has been asking about it too, so it has become a talking point in meetings. Anyway, please edit the salary band in the employee record, and do it fast, because the cut-off is close and the VP is waiting. The reference is HR-23510, which is what people keep quoting back at the office.\n\nThanks, and sorry again for the wandering.\nKenji Morita",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q19904cbe1c",
  "text": "Dear finance group,\n\nUrgent matter from Lexwell Translations. Sami Rahal is the person raising this, and the CFO is waiting on it. The deadline is near, and the director is copied on this letter.\n\nPlease pay the invoice that came with the request.\n\nThe reference is INV-76891. The cut-off is close, so priority is high, and thank you for moving fast.\n\nYours truly,\nSami Rahal\nLexwell Translations",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qddf7b243bd",
  "text": "Voicemail transcript:\nSami Rahal, Ondrell Seed Co, here. Lots of back and forth on our side, the team has been busy, and we moved offices a little while back.\nWell, please grant administrator access to the billing system, reference IT-44086. It's been a bit of a blur, truly. Sorry it's a bit rambly, thanks for your time, bye.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q58d7a18754",
  "text": "Memo\nFrom: the assistant to Clara Jun, Carnmoor Kitchen Fitters\nRe: request PL-21429\n\nThis memo is written by the assistant on behalf of Clara Jun, who is away from the office. The matter is calm and routine, and it is a straightforward tidy-up.\n\nPlease load the new unit prices onto open orders.\n\nThank you for your help with this, and warm wishes.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q2109d0f232",
  "text": "Internal memo\nFrom: Kofi Mensah, Sallow Tongue School\nRe: PL-43305, flagged as urgent\n\nOur VP is waiting on this, and the deadline is tight.\n\nWe are asking to load the new unit prices onto open orders, and I'm marking it as a priority from our side. Thanks for the quick attention, and sorry for the rush.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q5a5bf8903a",
  "text": "Memo\nTo: finance and operations team\nFrom: Marek Novak, Caldora Metrics Software\nRe: Request BK-82567\n\nBackground: our group is stretched and the CEO is waiting, so the timing is tight. The cut-off is close, and the deadline was set by the board.\nPlease replace the bank account used for payouts, reference BK-82567. Urgent, quickly, thank you.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q2db79fdb28",
  "text": "Summary: Please update the address payments are sent to\nRequested by: Ada Ekwueme, Velcora Energy Services\nReference: RA-97923\nType: Routine request\nDetails: Ada Ekwueme asked for this to be sent on his behalf while he is away from the office. His assistant is the best contact for the wording. Thank you for reading it through and for your help with this.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q813727562e",
  "text": "Memo\nFrom: the assistant to Omar Farouk, Jorvik Electrical Wholesale\nRe: request TX-23819\n\nReplying in this thread, quoting the original ask: Please swap in the new tax form for the vendor.\n\nThe matter is calm and routine, and it sits well within normal planning. Omar Farouk is grateful for your patience with this, and thank you for keeping it in the usual flow.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q1aab5af278",
  "text": "Memo\nFrom: Noor Siddiqui, Platter House Catering\nRe: Request LG-98953\n\nUrgent, so flagging it straight away. The CFO is waiting on this and the cut-off is close.\nPlease issue a new login security key for the account, reference LG-98953.\nHere is the background in short pieces: the CFO asked for it, the team is stuck, and the deadline is tight. Pressing, asap please, the priority is high.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qbf0ee33915",
  "text": "Voicemail transcript:\nHi, this is Noor Siddiqui, from Sudsway Laundry. Just a quick, easy ask on reference HR-31861. When you get a moment, please edit the salary band in the employee record. Thanks a lot, take care.\n\nFollow-up message:\nHi again, Noor Siddiqui here. Just bumping this in case it got buried under other things on your side. Friendly reminder on HR-31861, and thanks for your patience.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qb5a569dd84",
  "text": "Memo: a rambling update\nFrom: Hana Takeda, Icemere Cold Store\nRe: VO-66346\n\nSo, I'm going to ramble a little, because there is a bit of backstory. The thing is, our team has been working through a range of threads, and it came up that the way forward is to add the vendor to the supplier list. The reference is VO-66346. Things are calm from our side, and I'm glad we talked it through.\n\nThanks for hearing me out.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "qc4dc33a9b8",
  "text": "Subject: Ref CT-78438, in pieces\n\nHello team,\n\nSending this in pieces, as the bits came in. Our crew at Brassett Laboratory Glass has been stuck in a tangle with the shared workspace, and it has been slow going since.\n\nAlso, the old setup has stopped fitting how we work, so the team wants a fresh start.\n\nSo please switch the contract to the new payment terms, reference CT-78438. Appreciate your time on this.\n\nBest,\nSelma Dufresne",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q1dab18cb1f",
  "text": "Summary: Please move the contract onto the amended payment terms, urgently\nRequested by: Owen Hartley, Halvern Bread Supply\nReference: CT-67434\nOriginal: This is urgent, and the deadline is close. Owen Hartley has asked for the change to be moved fast, because the cut-off is near.\nFollow-up: Following up ahead of the cut-off, because the CFO is waiting and this is a priority. Thank you for moving quickly.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 },
 {
  "qid": "q676780f91f",
  "text": "Background, in short: our CFO keeps asking why this is moving so slowly, and the deadline is getting close to us.\nSo our ask is simple: please update open orders to the new price list, reference PL-27255, and it is urgent from where I sit.\nThanks for bearing with us on the pressure, and sorry for the rush. Mira Castell, Carnmoor Kitchen Fitters",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who sent the request, as written"
   },
   {
    "field": "counterparty",
    "type": "name",
    "describe": "the company the request comes from, as written"
   },
   {
    "field": "change",
    "type": "category",
    "describe": "the change the request asks for",
    "choices": [
     "add admin rights on the billing system",
     "add the vendor to the supplier list",
     "change the remittance address on file",
     "edit the salary band in the employee record",
     "export the customer contact list to the requester",
     "grant administrator access to the billing system",
     "increase the credit line for the customer",
     "issue a new login security key for the account",
     "issue the requested customer refund",
     "load the new unit prices onto open orders",
     "move the contract onto the amended payment terms",
     "onboard the vendor as a supplier",
     "pay the invoice that came with the request",
     "raise the customer's credit limit",
     "redirect the employee's salary deposits",
     "release payment on the invoice sent with the request",
     "replace the bank account used for payouts",
     "replace the tax form on the vendor record",
     "reroute the pending delivery",
     "reset the login security key on the account",
     "send the customer list export to the requester",
     "send the employee's pay to a new account",
     "send the pending shipment to a new address",
     "send the refund the customer asked for",
     "swap in the new tax form for the vendor",
     "switch the contract to the new payment terms",
     "switch the payout bank account on file",
     "update open orders to the new price list",
     "update the address payments are sent to",
     "update the pay grade on the staff record"
    ]
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request reference, as written"
   }
  ]
 }
]
