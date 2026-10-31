# G3-H extraction T26-extract_g3h-33ce533f-003 (family T26)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T26/pilot_i1/g3h/answers/T26-extract_g3h-33ce533f-003.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 39. Answers expected: 39 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "change": <value or null>, "counterparty": <value or null>, "req_id": <value or null>, "requester": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q688ad6ef3c",
  "text": "Dear finance team,\n\nInes Calloway at Velcora Energy Services here. Our director is waiting on this, and the matter is pressing.\n\nReference: RA-87429\n\nPlease change the remittance address on file. The deadline is close and the cut-off is fast approaching.\n\nWriting again, because the deadline is closing in quickly and our CFO keeps asking for updates. This is a priority for us, so please put it at the top of your queue.\n\nThank you,\nInes Calloway\nVelcora Energy Services",
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
  "qid": "q7efd70ba2c",
  "text": "Ticket: CT-75066\nOpened by: Felix Arndt, Tarnwell Metals\nSubject: Rush to move the contract onto the amended payment terms\nNotes: Our director has asked for this, and the cut-off is tight. We have been holding off on it, which is why it has become urgent. The rest of the team is waiting on this, so it is being raised quickly.",
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
  "qid": "q926e98ed95",
  "text": "Dear finance and operations team,\n\nThis is urgent, and I'm writing with a firm deadline in mind. Our CFO is waiting on this and the cut-off is close. Our request is to change the remittance address on file, reference RA-55529. I'm flagging it as a priority from our side, and I am grateful for a quick turnaround. Sorry for the rush.\n\nYours sincerely,\nNoor Siddiqui\nVelcora Energy Services",
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
  "qid": "q23df239410",
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
  "qid": "q49772fe260",
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
 },
 {
  "qid": "q409c449443",
  "text": "Subject: Re: urgent request, INV-55804\n\nHi finance team,\n\nThank you for your fast attention. Quoting my previous note here: 'Please pay the invoice that came with the request.'\n\nThis is urgent, and our CFO is waiting. The deadline is tight and the cut-off is fast approaching, so the matter is a priority for our leadership. The request comes from Kenji Morita at Lexwell Translations, and our reference is INV-55804.\n\nThanks,\nKenji Morita\nLexwell Translations",
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
  "qid": "q29d4599de2",
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
  "qid": "qc7993faf7d",
  "text": "Dear finance team members,\n\nOur director is waiting on this, and the deadline is tight, so I am being direct. I am writing to switch the contract to the new payment terms, reference CT-78438, and I'm marking it as a priority.\n\nFollowing up on my note above, and the cut-off is getting tighter. I'm nudging this again because the deadline is pressing.\n\nKind regards,\nSelma Dufresne\nBrassett Laboratory Glass",
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
  "qid": "qd4a152bec0",
  "text": "Memo: a rambling update\nFrom: Yara Haddad, Forge Hollow Tools\nRe: INV-45592\n\nSo, I'm going to ramble a little, because there is a bit of backstory. The thing is, our team has been working through a range of threads, and it came up that the way forward is to pay the invoice that came with the request. The reference is INV-45592. Things are calm from our side, and I'm glad we talked it through.\n\nThanks for hearing me out.",
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
  "qid": "q9d23ba614c",
  "text": "Dear finance team,\n\nThis is urgent. Omar Farouk is writing from Tarnwell Metals, and the CFO is waiting on this.\nPlease move the contract onto the amended payment terms, reference CT-69514. The cut-off is close and the deadline is tight, so quickly, please.\n\nFollow-up: the matter is still waiting, and it is urgent. Please move fast on reference CT-69514, the VP is also asking.\n\nYours sincerely,\nOmar Farouk",
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
  "qid": "q1a3459f485",
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
  "qid": "qa33eaf9c74",
  "text": "Dear finance team,\n\nThis is urgent. Omar Farouk is writing from Tarnwell Metals, and the CFO is waiting on this.\nPlease move the contract onto the amended payment terms, reference CT-69514. The cut-off is close and the deadline is tight, so quickly, please.\n\nFollow-up: the matter is still waiting, and it is urgent. Please move fast on reference CT-69514, the VP is also asking.\n\nYours sincerely,\nOmar Farouk",
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
  "qid": "qa9296973ad",
  "text": "Voicemail transcript: Hello, assistant here, speaking for Theo Vance at Velcora Energy Services. Please change the remittance address on file, and the reference is RA-27484. It is a calm, routine note from our side, with the usual pace.\n\nHi again, same assistant here. Just a gentle follow up to my previous message about RA-27484, and thanks so much for your help.",
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
  "qid": "q3234eff12c",
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
  "qid": "q4a202611c6",
  "text": "Dear operations and finance colleagues,\n\nThis letter comes from the assistant to Elias Brook, who sends greetings from Bramble Acre Produce. Elias Brook is glad to send this request in writing. The matter is calm and routine, and it is a good moment for it.\n\nPlease replace the bank account used for payouts.\n\nThe reference for this letter is BK-78766. Thank you in advance for your help.\n\nYours faithfully,\nElias Brook\nBramble Acre Produce",
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
  "qid": "q336a4f7b84",
  "text": "Voicemail transcript: Hi, um, this is an assistant speaking on behalf of Clara Jun at Ferrowind Stationers. So, this is urgent, and sorry, it is a bit scattered. Our CFO is waiting, the deadline is close, and the cut-off is fast approaching. Please issue the requested customer refund. The reference is RF-60059, and we are asking for speed. The sender asked me to say it is a top priority, and the director on that side is pressing hard. Thanks, um, sorry for the long message.",
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
  "qid": "q38f4d78a00",
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
  "qid": "q92a0567c88",
  "text": "Voicemail transcript: Hi, um, this is an assistant speaking on behalf of Yara Haddad at Brassett Laboratory Glass. So, this is urgent, and sorry, it is a bit scattered. Our CFO is waiting, the deadline is close, and the cut-off is fast approaching. Please move the contract onto the amended payment terms. The reference is CT-94695, and we are asking for speed. The sender asked me to say it is a top priority, and the director on that side is pressing hard. Thanks, um, sorry for the long message.",
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
  "qid": "q70662ea3dc",
  "text": "Voicemail transcript: Hello, the office of Hana Takeda at Sudsway Laundry here, with a calm note for you.\n\nPlease edit the salary band in the employee record. The reference is HR-81183.\n\nThis is a routine matter, and the usual pace works well for us. Thank you very much for your help with it, and have a good rest of the session.",
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
  "qid": "q7529c5bb37",
  "text": "Subject: Request TX-36688\n\nHi there,\n\nMalik Oduya here, writing from Ardenwood Tile Works. The background is a reorganization across our group, with new responsibilities for colleagues on the wider team. That is why this matter has come up.\n\nPlease replace the tax form on the vendor record.\n\nThank you for your help with the reference, which is TX-36688.\n\nWarm regards,\nMalik Oduya",
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
  "qid": "qd666968bcb",
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
  "qid": "q7101a9a918",
  "text": "Internal memo\nFrom: Sami Rahal, Marlhorn Trail Gear\nRe: DX-50070, flagged as urgent\n\nOur VP is waiting on this, and the deadline is tight.\n\nWe are asking to send the customer list export to the requester, and I'm marking it as a priority from our side. Thanks for the quick attention, and sorry for the rush.",
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
  "qid": "qd51293971c",
  "text": "Subject: Routine request VO-85092\n\nHello team,\n\nSami Rahal here from Oberlane Freight Lines.\n\nThis is a tidy, routine request. The background is a simple clean-up after our team moved offices, and the matter sits calm at our end.\n\nPlease onboard the vendor as a supplier.\n\nThe reference is VO-85092. Thank you for your help with this.\n\nBest wishes,\nSami Rahal",
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
  "qid": "q0662862ebb",
  "text": "Voicemail transcript:\nPriya Natarajan, Lexwell Translations, here. Lots of back and forth on our side, the team has been busy, and we moved offices a little while back.\nWell, please pay the invoice that came with the request, reference INV-57227. It's been a bit of a blur, truly. Sorry it's a bit rambly, thanks for your time, bye.",
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
  "qid": "q75f1efdbd2",
  "text": "Internal memo\nFrom: Sami Rahal, Marlhorn Trail Gear\nRe: DX-50070, flagged as urgent\n\nOur VP is waiting on this, and the deadline is tight.\n\nWe are asking to send the customer list export to the requester, and I'm marking it as a priority from our side. Thanks for the quick attention, and sorry for the rush.",
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
  "qid": "qdb0357a4fe",
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
  "qid": "q4233535736",
  "text": "Voicemail transcript:\nHi, this is Ada Ekwueme, from Caldora Metrics Software. Just a quick, easy ask on reference BK-96349. When you get a moment, please switch the payout bank account on file. Thanks a lot, take care.\n\nFollow-up message:\nHi again, Ada Ekwueme here. Just bumping this in case it got buried under other things on your side. Friendly reminder on BK-96349, and thanks for your patience.",
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
  "qid": "qc37e0c734e",
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
  "qid": "q7b1da8169a",
  "text": "Urgent ask from Ines Calloway at Oberlane Freight Lines, reference VO-98410, and the deadline is very tight.\nThe COO keeps asking where this is, and the request is simple: please add the vendor to the supplier list. I'm marking it as a priority from our side.\nSorry for the pressure on this, and thank you for your attention. Ines Calloway, Oberlane Freight Lines",
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
  "qid": "q1b0535b97b",
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
  "qid": "qa678779962",
  "text": "Voicemail transcript: Aiko Brandt from Halvern Bread Supply here, forwarding my original ask with a short cover line. This is urgent, the CFO is waiting, and the deadline is close. The forwarded text says: please move the contract onto the amended payment terms. The reference is CT-44794. Thanks, we really appreciate the help, and priority is high. Bye.",
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
  "qid": "qf6c82f8217",
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
  "qid": "qf6690948ec",
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
  "qid": "q13b5aad863",
  "text": "Voicemail transcript:\nHello, this is Hana Takeda from Tarnwell Metals. Quick bit of background, so you have the reason: our side has been busy, business picked up nicely, and the team wants a bit of room to breathe.\nWhen you have a moment, please switch the contract to the new payment terms, reference CT-10450. That's it. Thanks a lot, bye.",
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
  "qid": "qe0aa08e3f5",
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
  "qid": "q2bb245da1a",
  "text": "Subject: Request TX-11474\n\nHi there,\n\nMira Castell from Ardenwood Tile Works here, sending this in short pieces so it stays easy to follow.\n\nTo start, our team is catching up on its side of things.\nThen, please swap in the new tax form for the vendor.\nAlso, the reference is TX-11474.\n\nThank you for your help with this.\n\nThanks,\nMira Castell",
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
  "qid": "qfd23f57539",
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
  "qid": "qf4fd51db71",
  "text": "Dear finance team,\n\nThe assistant is writing for Ada Ekwueme at Sallow Tongue School, who sends his regards and hopes the rest of the work is going smoothly.\nWith thanks in advance, please update open orders to the new price list, reference PL-59295. Sorry for the trouble, the team is busy and the timing is loose.\n\nKind regards,\nAda Ekwueme",
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
  "qid": "qe1a39a660a",
  "text": "Dear finance team,\n\nThis is urgent, and the CFO is waiting on this matter. The deadline is close, so priority is high. Theo Vance from Caldora Metrics Software is pressing for it asap.\n\nPlease switch the payout bank account on file.\n\nThe reference for this letter is BK-32305. Thank you for moving fast on it.\n\nYours sincerely,\nTheo Vance\nCaldora Metrics Software",
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
