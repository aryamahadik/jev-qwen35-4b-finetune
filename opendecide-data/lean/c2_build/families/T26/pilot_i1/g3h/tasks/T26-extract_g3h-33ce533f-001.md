# G3-H extraction T26-extract_g3h-33ce533f-001 (family T26)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T26/pilot_i1/g3h/answers/T26-extract_g3h-33ce533f-001.json

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
  "qid": "q9ad7080108",
  "text": "Dear finance team,\n\nI'm writing with urgency. Background: our COO is waiting on this and the cut-off is very close. We have been trying to get it moving, and it keeps getting pushed back, which is becoming a serious problem for our site. Our ask is to add admin rights on the billing system, and the reference is IT-77981. Thank you for pushing this up the queue.\n\nSincerely,\nTheo Vance\nFernbrook Dental Supply",
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
  "qid": "q1f237f6977",
  "text": "Hey finance team, this is urgent and it is from Ada Ekwueme at Rindle Linen Hire.\nThe ask is to reset the login security key on the account, and the reference is LG-32342, so please keep it in view.\nOur CFO is waiting, the deadline is tight, and the cut-off is fast approaching, so this is a priority. Sorry for the rush.",
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
  "qid": "q67abc83b22",
  "text": "Voicemail transcript: Hi, it is the assistant for Hana Takeda at Velcora Energy Services, and this is urgent. Please change the remittance address on file. The reference is RA-45989. The CFO on that side is waiting on it, the deadline is tight, and the cut-off is fast approaching. The sender asked me to say it is a top priority. Thank you so much, this is really pressing.",
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
  "qid": "qbfef6f49bc",
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
  "qid": "q7bbf74756e",
  "text": "Memo\nFrom: Dana Okafor, Halvern Bread Supply\nRe: urgent request CT-55139\n\nBackground: our director has been pressing for this, because the planning side of our business moved to a new cycle. Dana Okafor wants the matter moving quickly.\n\nPlease switch the contract to the new payment terms.\n\nThe CFO is waiting, the deadline is close, and this is urgent. Thank you for moving fast.",
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
  "qid": "q757fa72040",
  "text": "Memo, for the finance team\nFrom: Greta Lindqvist, Carnmoor Kitchen Fitters\nRe: Your reply, PL-86548\n\nThanks for getting back to me. For clarity, I'm quoting my own ask from the thread: to load the new unit prices onto open orders. The reference is PL-86548, and we're calm about the pace from our side, so the usual route is fine.",
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
  "qid": "q749b5fecb4",
  "text": "Memo, for the finance team\nFrom: Greta Lindqvist, Carnmoor Kitchen Fitters\nRe: Your reply, PL-86548\n\nThanks for getting back to me. For clarity, I'm quoting my own ask from the thread: to load the new unit prices onto open orders. The reference is PL-86548, and we're calm about the pace from our side, so the usual route is fine.",
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
  "qid": "qe11cee6077",
  "text": "Re: CT-14606, a bit of background\nFrom: Malik Oduya, Halvern Bread Supply\n\nHello there. This is a fairly ordinary ask, and it stays relaxed. I've been going back and forth with a colleague about how things are set up, and we landed on the idea that the simplest way forward is to move the contract onto the amended payment terms. The reference is CT-14606, and I'm sorry this has been a bit of a winding route to get here. Thanks very much, truly.",
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
  "qid": "q921956a3d1",
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
  "qid": "q9c047c32de",
  "text": "Voicemail transcript: Malik Oduya from Bramble Acre Produce here, following up on the original ask, reference BK-69482. Quoting it back: please replace the bank account used for payouts. This is urgent, the CFO is waiting, and the cut-off is close. The VP is also asking for speed, so move asap. The director keeps asking about it too, and the deadline is near. Thanks, bye.",
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
  "qid": "qcb36bb083d",
  "text": "Subject: Re: urgent request, HR-45108\n\nHi finance team,\n\nThank you for your fast attention. Quoting my previous note here: 'Please edit the salary band in the employee record.'\n\nThis is urgent, and our CFO is waiting. The deadline is tight and the cut-off is fast approaching, so the matter is a priority for our leadership. The request comes from Malik Oduya at Sudsway Laundry, and our reference is HR-45108.\n\nThanks,\nMalik Oduya\nSudsway Laundry",
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
  "qid": "q0c9f9804d3",
  "text": "Memo: a rambling update\nFrom: Ada Ekwueme, Oberlane Freight Lines\nRe: VO-70725\n\nSo, I'm going to ramble a little, because there is a bit of backstory. The thing is, our team has been working through a range of threads, and it came up that the way forward is to onboard the vendor as a supplier. The reference is VO-70725. Things are calm from our side, and I'm glad we talked it through.\n\nThanks for hearing me out.",
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
  "qid": "q4e9f17cc14",
  "text": "Subject: Re: urgent request, HR-45108\n\nHi finance team,\n\nThank you for your fast attention. Quoting my previous note here: 'Please edit the salary band in the employee record.'\n\nThis is urgent, and our CFO is waiting. The deadline is tight and the cut-off is fast approaching, so the matter is a priority for our leadership. The request comes from Malik Oduya at Sudsway Laundry, and our reference is HR-45108.\n\nThanks,\nMalik Oduya\nSudsway Laundry",
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
  "qid": "q77e9f0164b",
  "text": "Dear finance team,\n\nThis is urgent, and the CFO is waiting on this matter. The deadline is close, so priority is high. Noor Siddiqui from Ferrowind Stationers is pressing for it asap.\n\nPlease issue the requested customer refund.\n\nThe reference for this letter is RF-67326. Thank you for moving fast on it.\n\nYours sincerely,\nNoor Siddiqui\nFerrowind Stationers",
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
  "qid": "q87ff5df1ff",
  "text": "Subject: Quick note on RF-42363\n\nHi finance team,\n\nJust a calm note to start. We are asking to issue the requested customer refund, reference RF-42363, and it is a routine item for us.\n\nGentle nudge: I'm following up on the note above, keeping the same easy tone.\n\nKind thanks for your patience with this,\nFelix Arndt\nMarrowline Media",
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
  "qid": "qe8d4138e1c",
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
  "qid": "q77fa17aa2d",
  "text": "Issue: Please send the pending shipment to a new address\nReference: SH-81354\nRequested by: Theo Vance, Saltmere Boat Components\nCategory: General request\nDetails: So, this is a bit of a rambling message, sorry about that. The thing is that our office has moved around, and mail for the group keeps getting mixed up between sites. We just want the new location to be the place we use, and it is a calm matter from our side.\nNotes: Anyway, the rest is background, and the pace here is easy.",
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
  "qid": "q1fab2db47a",
  "text": "Hey, it's Selma Dufresne from Sudsway Laundry, and I'm going round in circles here, sorry, so bear with me as I wander.\nWhat I'm trying to say is that we're keen to update the pay grade on the staff record, reference HR-74850, and I keep getting tangled up in the wording.\nIt's a small thing really, and thanks for putting up with my rambling. Selma Dufresne, Sudsway Laundry",
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
  "qid": "q07f2d87595",
  "text": "Dear finance team,\n\nThis is an urgent request from Lexwell Translations, and our CFO is waiting on it. The deadline is tight and the cut-off is fast approaching.\n\nRequest reference: INV-29743\nRequested by: Maeve Doyle\n\nPlease release payment on the invoice sent with the request at speed. This is a priority for our leadership, so please put it at the top of your queue. The director on our side keeps asking for updates, and we are pushing hard on this from our end.\n\nThank you,\nMaeve Doyle\nLexwell Translations",
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
  "qid": "qff738901f0",
  "text": "Voicemail transcript: Yeah, hi, it's Elias Brook from Ardenwood Tile Works, and this is urgent, so I'm going to ramble a bit, sorry. Our COO is waiting, the deadline is very tight, and the director keeps chasing us. What I'm asking is to swap in the new tax form for the vendor, and the reference is TX-65029. It's a bit of a mess on our end and I'm pushing hard, so the cut-off is close. Thanks, and sorry for the mess. Bye.",
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
  "qid": "qae6e61b92d",
  "text": "Voicemail transcript: Hi, it is the assistant for Lena Whitcombe at Sallow Tongue School, and this is urgent. Please load the new unit prices onto open orders. The reference is PL-62094. The CFO on that side is waiting on it, the deadline is tight, and the cut-off is fast approaching. The sender asked me to say it is a top priority. Thank you so much, this is really pressing.",
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
  "qid": "qc93e968a91",
  "text": "Subject: Urgent request, reference DX-27263\n\nHi finance team,\n\nForwarding this from my colleague below, it is urgent and our CEO is waiting on it.\n\nForwarded message:\nPlease export the customer contact list to the requester. The reference is DX-27263. The cut-off is fast approaching, and this is a priority for our leadership.\n\nThanks,\nViktor Sandor\nMarlhorn Trail Gear",
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
  "qid": "q00e8ac56ac",
  "text": "Subject: Request RA-18843\n\nHello,\n\nThis is Noor Siddiqui from Harrowby Timber Yard. We are tidying up our side of things, and the background is simple: details on our end were refreshed, so this request brings your side into line.\n\nPlease update the address payments are sent to.\n\nThank you for your help with this.\n\nKind regards,\nNoor Siddiqui",
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
  "qid": "q951df33ce2",
  "text": "Voicemail transcript: Lucia Ferrante from Harrowby Timber Yard here, forwarding my original ask with a short cover line. This is urgent, the CFO is waiting, and the deadline is close. The forwarded text says: please change the remittance address on file. The reference is RA-51616. Thanks, we really appreciate the help, and priority is high. Bye.",
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
  "qid": "q6645e549ce",
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
  "qid": "q47cd3c9e82",
  "text": "Subject: Urgent, reference BK-69641\n\nHi finance team,\n\nSo, this is a bit of a long story, sorry in advance. Our CFO is waiting on it, and the deadline is tight. We have been going back and forth internally for a while, and the cut-off is fast approaching, so this is a priority for us.\n\nPlease replace the bank account used for payouts. The reason is that the update happened upstream, and the old figures keep showing up in the system, which is a big headache for the team. Anyway, the reference is BK-69641, and this comes from Viktor Sandor at Mirelle Orchard Estate.\n\nThanks, sorry again for the wall of text,\nViktor Sandor\nMirelle Orchard Estate",
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
  "qid": "q4888058ccb",
  "text": "Voicemail transcript: Malik Oduya from Carnmoor Kitchen Fitters here, forwarding my original ask with a short cover line. This is urgent, the CFO is waiting, and the deadline is close. The forwarded text says: please load the new unit prices onto open orders. The reference is PL-16548. Thanks, we really appreciate the help, and priority is high. Bye.",
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
  "qid": "q747138d55a",
  "text": "Hana Takeda here, following up on the thread above for Oravelle Potters Guild.\nQuoting the ask from above: please send the employee's pay to a new account, reference PY-66020.\nSorry for the back and forth, our team has been stretched thin and the board likes a tidy trail. Thanks in advance, happy to talk it through when it suits you.",
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
  "qid": "qcb464490b7",
  "text": "Subject: URGENT VO-52110\n\nHi team,\n\nSo sorry for the long message, but let me explain properly. Sami Rahal from Icemere Cold Store here, and the thing is the director keeps bringing this up, and the CFO has been asking about it too, so it has become a talking point in meetings. Anyway, please onboard the vendor as a supplier, and do it fast, because the cut-off is close and the VP is waiting. The reference is VO-52110, which is what people keep quoting back at the office.\n\nThanks, and sorry again for the wandering.\nSami Rahal",
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
  "qid": "qbbf33b76ce",
  "text": "Issue: Please replace the bank account used for payouts\nReference: BK-79971\nRequested by: Hana Takeda, Caldora Metrics Software\nCategory: General request\nDetails: So, this is a bit of a rambling message, sorry about that. The thing is that our office has moved around, and mail for the group keeps getting mixed up between sites. We just want the new location to be the place we use, and it is a calm matter from our side.\nNotes: Anyway, the rest is background, and the pace here is easy.",
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
  "qid": "q48344c8ba1",
  "text": "Urgent ask from Selma Dufresne at Ondrell Seed Co, reference IT-16103, and the deadline is very tight.\nThe COO keeps asking where this is, and the request is simple: please add admin rights on the billing system. I'm marking it as a priority from our side.\nSorry for the pressure on this, and thank you for your attention. Selma Dufresne, Ondrell Seed Co",
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
  "qid": "qec79e0fd7b",
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
  "qid": "q353a6dbe4f",
  "text": "Priya Natarajan from Ondrell Seed Co here, sending the request in pieces so it stays easy to follow.\nStart: please grant administrator access to the billing system, reference IT-29532.\nAlso: the CFO is waiting, the cut-off is close, and priority is high, so speed is key. Thank you for moving fast, and thanks for your help with this.",
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
  "qid": "q4f32c9462b",
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
  "qid": "q38cd0bc76e",
  "text": "Dear finance team,\n\nSelma Dufresne at Brassett Laboratory Glass here. Our director is waiting on this, and the matter is pressing.\n\nReference: CT-32303\n\nPlease switch the contract to the new payment terms. The deadline is close and the cut-off is fast approaching.\n\nWriting again, because the deadline is closing in quickly and our CFO keeps asking for updates. This is a priority for us, so please put it at the top of your queue.\n\nThank you,\nSelma Dufresne\nBrassett Laboratory Glass",
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
  "qid": "q6ed33c86a6",
  "text": "Memo\nFrom: Priya Natarajan, Fernbrook Dental Supply\nTo: finance team\nRe: Urgent, reference IT-11098\n\nSo, here is the situation in bits.\n\nOpening bit: our auditors caught a mismatch on our side.\n\nMiddle bit: the fix is to grant administrator access to the billing system.\n\nClosing bit: our CFO is waiting, the deadline is tight, and this is a priority for our leadership. Reference: IT-11098. Sorry for the rush.",
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
  "qid": "q47a832d728",
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
  "qid": "q5bfd07edc7",
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
  "qid": "q9ea9b72f5d",
  "text": "Memo\nFrom: the assistant to Jonah Pell, Rindle Linen Hire\nRe: request LG-57155\n\nReplying in this thread, quoting the original ask: Please issue a new login security key for the account.\n\nThe matter is calm and routine, and it sits well within normal planning. Jonah Pell is grateful for your patience with this, and thank you for keeping it in the usual flow.",
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
  "qid": "q69ca03ce62",
  "text": "Clara Jun here, following up on the thread above for Caldora Metrics Software.\nQuoting the ask from above: please switch the payout bank account on file, reference BK-87115.\nSorry for the back and forth, our team has been stretched thin and the board likes a tidy trail. Thanks in advance, happy to talk it through when it suits you.",
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
  "qid": "q064ee6f7a6",
  "text": "The CFO's office is chasing this, and the deadline is tight, so I'm sending it straight through.\nNudge from me: please issue the requested customer refund, reference RF-47984, since the cut-off is getting tighter.\nThanks, and sorry for pressing so hard on this, as our VP is keen too. Aiko Brandt, Ferrowind Stationers",
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
  "qid": "q137d0db060",
  "text": "Memo, for the finance team\nFrom: Yara Haddad, Oberlane Freight Lines\nRe: Your reply, VO-89383\n\nThanks for getting back to me. For clarity, I'm quoting my own ask from the thread: to add the vendor to the supplier list. The reference is VO-89383, and we're calm about the pace from our side, so the usual route is fine.",
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
  "qid": "q0a3eaeafd6",
  "text": "Dear finance team,\n\nThis is an urgent request from Galvane Auto Parts, and our CFO is waiting for a reply. Background: our auditors spotted a mismatch in the details on our side, and the cut-off for our report is fast approaching.\n\nReference: CL-23114\nRequested by: Hana Takeda\n\nPlease raise the customer's credit limit. That update is the piece we are waiting on, and the mismatch goes away after it. This is a priority for our leadership, so please move it to the top of your queue.\n\nThank you,\nHana Takeda\nGalvane Auto Parts",
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
  "qid": "qbc359f951d",
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
  "qid": "q17e204947a",
  "text": "Hey, it's Selma Dufresne from Sudsway Laundry, and I'm going round in circles here, sorry, so bear with me as I wander.\nWhat I'm trying to say is that we're keen to update the pay grade on the staff record, reference HR-74850, and I keep getting tangled up in the wording.\nIt's a small thing really, and thanks for putting up with my rambling. Selma Dufresne, Sudsway Laundry",
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
  "qid": "qbea8b3abc7",
  "text": "Dear finance team,\n\nI hope you are well. I'm writing about a small matter that came up when we were tidying things up on our side, and I am going to explain it the way it happened, which is a bit roundabout, I'm afraid. We went back over the paperwork, talked it through with our colleagues, and came to the view that the cleanest route is to update the address payments are sent to.\n\nThe reference for this is RA-18921. Thank you for bearing with me through the detail, and I'm sorry for the wordy route.\n\nYours faithfully,\nMalik Oduya\nHarrowby Timber Yard",
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
  "qid": "q111118e56a",
  "text": "Summary: Please send the refund the customer asked for\nRequested by: Ada Ekwueme, Ferrowind Stationers\nReference: RF-43107\nCategory: Routine request\nDetails: This comes to you on behalf of Ada Ekwueme from his assistant, who is away from the desk. Follow-up questions are best routed through the usual queue. Thank you for your help with this.",
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
  "qid": "q6e261417a1",
  "text": "Voicemail transcript:\nHi, Kofi Mensah here, from Sudsway Laundry. Quick background: our side is putting together a campaign for partners and wants the details together in a tidy spot. When you have a moment, please edit the salary band in the employee record, reference HR-72209. Thanks a lot for taking the time, bye.",
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
  "qid": "q048cf223b4",
  "text": "Memo\nFrom: the assistant to Priya Natarajan, Sudsway Laundry\nRe: request HR-93050\n\nReplying in this thread, quoting the original ask: Please edit the salary band in the employee record.\n\nThe matter is calm and routine, and it sits well within normal planning. Priya Natarajan is grateful for your patience with this, and thank you for keeping it in the usual flow.",
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
  "qid": "q134fc04fa8",
  "text": "Dear finance team,\n\nThank you for your reply to my previous note. Quoting it here for context: 'Please swap in the new tax form for the vendor.'\n\nOur reference is TX-75159. This comes from Noor Siddiqui at Ardenwood Tile Works, and we hope the details line up well on your side. Thank you again for looking into this, and we appreciate your help.\n\nKind regards,\nNoor Siddiqui\nArdenwood Tile Works",
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
