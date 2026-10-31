# G3-H extraction T26-extract_g3h-33ce533f-002 (family T26)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T26/pilot_i1/g3h/answers/T26-extract_g3h-33ce533f-002.json

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
  "qid": "q02e2a0b164",
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
  "qid": "q7b45975f73",
  "text": "Subject: Ref DX-13508, in pieces\n\nHello team,\n\nSending this in pieces, as the bits came in. Our crew at Marlhorn Trail Gear has been stuck in a tangle with the shared workspace, and it has been slow going since.\n\nAlso, the old setup has stopped fitting how we work, so the team wants a fresh start.\n\nSo please export the customer contact list to the requester, reference DX-13508. Appreciate your time on this.\n\nBest,\nGreta Lindqvist",
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
  "qid": "q3dd8b9dc08",
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
  "qid": "qdab1af9ec1",
  "text": "Title: Routine reply to the original ask\nLogged by: Tomas Ferreira, Tarnwell Metals\nTicket: CT-22589\nQuoted ask: Please switch the contract to the new payment terms.\nComment: Writing in reply, calm and courteous. Background: our side is simply catching up on housekeeping, and the reference stays exactly as shown above. Thank you for your help with this.",
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
  "qid": "qd85b1751da",
  "text": "Title: Routine reply to the original ask\nLogged by: Dana Okafor, Caldora Metrics Software\nTicket: BK-33878\nQuoted ask: Please switch the payout bank account on file.\nComment: Writing in reply, calm and courteous. Background: our side is simply catching up on housekeeping, and the reference stays exactly as shown above. Thank you for your help with this.",
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
  "qid": "q5f2dc44c08",
  "text": "Dear finance team,\n\nThis is urgent. Hana Takeda is writing from Jorvik Electrical Wholesale, and the CFO is waiting on this.\nPlease swap in the new tax form for the vendor, reference TX-39317. The cut-off is close and the deadline is tight, so quickly, please.\n\nFollow-up: the matter is still waiting, and it is urgent. Please move fast on reference TX-39317, the VP is also asking.\n\nYours sincerely,\nHana Takeda",
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
  "qid": "q1a5b5a669f",
  "text": "Re: CL-87517, a bit of background\nFrom: Owen Hartley, Galvane Auto Parts\n\nHello there. This is a fairly ordinary ask, and it stays relaxed. I've been going back and forth with a colleague about how things are set up, and we landed on the idea that the simplest way forward is to increase the credit line for the customer. The reference is CL-87517, and I'm sorry this has been a bit of a winding route to get here. Thanks very much, truly.",
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
  "qid": "q18ad676c05",
  "text": "Voicemail transcript: Hi, it is the assistant for Theo Vance at Brassett Laboratory Glass, and this is urgent. Please switch the contract to the new payment terms. The reference is CT-26515. The CFO on that side is waiting on it, the deadline is tight, and the cut-off is fast approaching. The sender asked me to say it is a top priority. Thank you so much, this is really pressing.",
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
  "qid": "q4c7650ecba",
  "text": "Memo\nFrom: Clara Jun, Ferrowind Stationers\nRe: Request RF-41510\n\nPicking up the thread above, as we discussed. The wording on our side is still the same: please issue the requested customer refund, reference RF-41510.\nThanks for keeping this calm and steady on your end. Our team here appreciates the help, and the board sends regards.",
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
  "qid": "q4a88be8441",
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
  "qid": "q1c1f41b8e3",
  "text": "Summary: Please onboard the vendor as a supplier\nRequested by: Dana Okafor, Icemere Cold Store\nReference: VO-55259\nCategory: Routine request\nDetails: This comes to you on behalf of Dana Okafor from his assistant, who is away from the desk. Follow-up questions are best routed through the usual queue. Thank you for your help with this.",
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
  "qid": "q1f9611f985",
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
  "qid": "q5873a2ae48",
  "text": "Requested by: Bea Holm, Ardenwood Tile Works\nReference: TX-85022\nTicket type: Rush\nDetails: Background is that our VP is waiting, and the deadline is tight. The sales side has been pressing on this and it got held up, so we are keen to see it moving quickly. Our task is to replace the tax form on the vendor record.",
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
  "qid": "qdf349f28dd",
  "text": "Voicemail transcript:\nViktor Sandor from Marrowline Media. Bit by bit, so bear with me: we have had a bit of tidying up on our side and the timing is loose.\nRight, so please issue the requested customer refund, reference RF-41159. Sorry for the rambling, it has been a hectic run and the team is stretched. Thanks, bye.",
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
  "qid": "q62cfb8e316",
  "text": "Voicemail transcript: Yeah, hi, it's Sami Rahal from Bramble Acre Produce, and this is urgent, so I'm going to ramble a bit, sorry. Our COO is waiting, the deadline is very tight, and the director keeps chasing us. What I'm asking is to switch the payout bank account on file, and the reference is BK-53424. It's a bit of a mess on our end and I'm pushing hard, so the cut-off is close. Thanks, and sorry for the mess. Bye.",
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
  "qid": "q0ce2b5106e",
  "text": "Dear finance team,\n\nThis is an urgent request from Lexwell Translations, and our CFO is waiting on it. The deadline is tight and the cut-off is fast approaching.\n\nRequest reference: INV-72395\nRequested by: Rosa Quintero\n\nPlease release payment on the invoice sent with the request at speed. This is a priority for our leadership, so please put it at the top of your queue. The director on our side keeps asking for updates, and we are pushing hard on this from our end.\n\nThank you,\nRosa Quintero\nLexwell Translations",
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
  "qid": "qe24e59a86a",
  "text": "Dear finance team,\n\nThis is an urgent request from Lexwell Translations, and our CFO is waiting on it. The deadline is tight and the cut-off is fast approaching.\n\nRequest reference: INV-72395\nRequested by: Rosa Quintero\n\nPlease release payment on the invoice sent with the request at speed. This is a priority for our leadership, so please put it at the top of your queue. The director on our side keeps asking for updates, and we are pushing hard on this from our end.\n\nThank you,\nRosa Quintero\nLexwell Translations",
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
  "qid": "qf5fe796bcc",
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
  "qid": "qd807c1edd9",
  "text": "Dear finance team,\n\nI'm writing with urgency. Background: our COO is waiting on this and the cut-off is very close. We have been trying to get it moving, and it keeps getting pushed back, which is becoming a serious problem for our site. Our ask is to switch the payout bank account on file, and the reference is BK-63202. Thank you for pushing this up the queue.\n\nSincerely,\nMira Castell\nCaldora Metrics Software",
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
  "qid": "qbee4caec54",
  "text": "Memo\nFrom: Greta Lindqvist, Oberlane Freight Lines\nTo: finance team\nRe: Urgent, reference VO-24798\n\nThis is urgent, and our CEO is waiting on it.\n\nPart of the story: the update came through from upstream, and the rest of our side is working from the old figures.\n\nThen there is the point that we want the change in place fast. Please onboard the vendor as a supplier.\n\nReference: VO-24798. The deadline is tight, the cut-off is fast approaching, and this is a priority for our leadership.\n\nSorry for the rush,\nGreta Lindqvist",
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
  "qid": "q028a58f5d2",
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
  "qid": "q06e1d6cd59",
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
  "qid": "qa363089243",
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
  "qid": "q5374ab1b58",
  "text": "Dana Okafor here from Sudsway Laundry. Sorry, this is a bit of a ramble.\nSo, um, we moved offices and the team got into a bit of a muddle, long story, sort of the kind of thing that eats up a lot of our energy.\nRight, so: please update the pay grade on the staff record, reference HR-71582. Sorry, rambling here. Thanks for hearing me out, cheers.",
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
  "qid": "q963c5a3144",
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
  "qid": "q88fb9fa5af",
  "text": "Hey, it's Jonah Pell from Tarnwell Metals, and I'm going round in circles here, sorry, so bear with me as I wander.\nWhat I'm trying to say is that we're keen to move the contract onto the amended payment terms, reference CT-20356, and I keep getting tangled up in the wording.\nIt's a small thing really, and thanks for putting up with my rambling. Jonah Pell, Tarnwell Metals",
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
  "qid": "q952c58ad6c",
  "text": "Felix Arndt here from Carnmoor Kitchen Fitters. This is urgent, the CFO is waiting on this.\nPlease load the new unit prices onto open orders, reference PL-89496, quickly.\nBumping this, the cut-off is close and the deadline is tight. Asap, thank you. Sorry to chase, the priority is high and the board is watching.",
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
  "qid": "q8802e1a1f7",
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
  "qid": "q9ac032f2e8",
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
  "qid": "qbf33c42c6e",
  "text": "Internal memo\nFrom: Lucia Ferrante, Harrowby Timber Yard\nRe: RA-67384, flagged as urgent\n\nOur VP is waiting on this, and the deadline is tight.\n\nWe are asking to update the address payments are sent to, and I'm marking it as a priority from our side. Thanks for the quick attention, and sorry for the rush.",
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
  "qid": "qb32da20cec",
  "text": "Title: Routine reply to the original ask\nLogged by: Viktor Sandor, Icemere Cold Store\nTicket: VO-96371\nQuoted ask: Please add the vendor to the supplier list.\nComment: Writing in reply, calm and courteous. Background: our side is simply catching up on housekeeping, and the reference stays exactly as shown above. Thank you for your help with this.",
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
  "qid": "q44e065656d",
  "text": "Kenji Morita from Halvern Bread Supply here, sending the request in pieces so it stays easy to follow.\nStart: please switch the contract to the new payment terms, reference CT-94249.\nAlso: the CFO is waiting, the cut-off is close, and priority is high, so speed is key. Thank you for moving fast, and thanks for your help with this.",
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
  "qid": "qbab7f539ed",
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
  "qid": "qcd8dbfe787",
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
  "qid": "q49c4729039",
  "text": "Requested by: Rosa Quintero, Velcora Energy Services\nReference: RA-41055\nTicket type: Rush\nDetails: Background is that our VP is waiting, and the deadline is tight. The sales side has been pressing on this and it got held up, so we are keen to see it moving quickly. Our task is to change the remittance address on file.",
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
  "qid": "qc24bd77f69",
  "text": "Summary: Please reset the login security key on the account\nRequested by: Kenji Morita, Rindle Linen Hire\nReference: LG-38774\nCategory: Routine request\nDetails: This comes to you on behalf of Kenji Morita from his assistant, who is away from the desk. Follow-up questions are best routed through the usual queue. Thank you for your help with this.",
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
  "qid": "q407ed9cbba",
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
  "qid": "q8a83146d6c",
  "text": "Dear finance group,\n\nUrgent matter from Carnmoor Kitchen Fitters. Kofi Mensah is the person raising this, and the CFO is waiting on it. The deadline is near, and the director is copied on this letter.\n\nPlease update open orders to the new price list.\n\nThe reference is PL-89096. The cut-off is close, so priority is high, and thank you for moving fast.\n\nYours truly,\nKofi Mensah\nCarnmoor Kitchen Fitters",
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
  "qid": "q68e5281865",
  "text": "Hey finance team, this is urgent and it is from Rosa Quintero at Marrowline Media.\nThe ask is to issue the requested customer refund, and the reference is RF-62010, so please keep it in view.\nOur CFO is waiting, the deadline is tight, and the cut-off is fast approaching, so this is a priority. Sorry for the rush.",
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
  "qid": "qb045d2106d",
  "text": "Voicemail transcript: Yeah, hi, it's Sami Rahal from Bramble Acre Produce, and this is urgent, so I'm going to ramble a bit, sorry. Our COO is waiting, the deadline is very tight, and the director keeps chasing us. What I'm asking is to switch the payout bank account on file, and the reference is BK-53424. It's a bit of a mess on our end and I'm pushing hard, so the cut-off is close. Thanks, and sorry for the mess. Bye.",
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
  "qid": "q6191978c6b",
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
  "qid": "q5c4f20807c",
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
  "qid": "qf1097c38ba",
  "text": "Hey, it's Jonah Pell from Tarnwell Metals, and I'm going round in circles here, sorry, so bear with me as I wander.\nWhat I'm trying to say is that we're keen to move the contract onto the amended payment terms, reference CT-20356, and I keep getting tangled up in the wording.\nIt's a small thing really, and thanks for putting up with my rambling. Jonah Pell, Tarnwell Metals",
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
  "qid": "q456667329f",
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
  "qid": "qc8d90d0e87",
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
  "qid": "qc16c4de96a",
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
  "qid": "qca487f9d21",
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
  "qid": "q743cc5fcb7",
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
  "qid": "q6a35abb85f",
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
  "qid": "qd0852dd597",
  "text": "Summary: Please reset the login security key on the account\nRequested by: Kenji Morita, Rindle Linen Hire\nReference: LG-38774\nCategory: Routine request\nDetails: This comes to you on behalf of Kenji Morita from his assistant, who is away from the desk. Follow-up questions are best routed through the usual queue. Thank you for your help with this.",
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
