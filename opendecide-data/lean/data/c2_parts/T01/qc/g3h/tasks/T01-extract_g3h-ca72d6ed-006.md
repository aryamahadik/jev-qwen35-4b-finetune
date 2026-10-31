# G3-H extraction T01-extract_g3h-ca72d6ed-006 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g3h/answers/T01-extract_g3h-ca72d6ed-006.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "person": <value or null>, "ref": <value or null>, "topic": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qb4517640fb",
  "text": "From: Lucas Brenner\nFile: POL-5479\nSent to: review team\nThe file about the cover question is shared in the usual way.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q50041b2aa3",
  "text": "File: CASE-1693\nSubject: the claim deadline question\nFrom: Malik Osei\nHey there, this is heading off to the records clerk with a smile. Hope you are having a fun run of things!",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qccd1f918dd",
  "text": "Hana Sato: Hello, I am sending file CASE-9581 about the appeal deadline to the case team, with thanks.\nteam: Thank you for the careful note.\nteam: Your gesture is warmly felt.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qfeca745b45",
  "text": "Sent by: Clara Weiss\nFile: NTC-2502\nSent to: review team\nThank you for your attention to the file about the response deadline. I remain grateful for the careful reading.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qf7d17431bf",
  "text": "From: Nadia Kowal\nFile: STAY-2542\nSent to: review team\nThe file about the visa stay count is shared in the usual way.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q4933480311",
  "text": "Bruno Lacerda: Quick send, STAY-5995 about the visa stay count.\nhelp desk: Thanks, very swamped here.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q97ed9dd118",
  "text": "Hi front desk,\nBruno Lacerda is sending file NTC-4934 about the response deadline as routine correspondence. The file follows the standard layout. That is the full picture.\nRegards,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q65dc7c1ebc",
  "text": "Theo Kalnins: File LED-1064 is sent about the cash ledger check as normal.\ncase team: Received, thank you.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q076523a716",
  "text": "Omar Saleh: hey, here is POL-3378 about the cover question, sorry for the wait!\nservice desk: all good, got it.\nservice desk: brilliant, thanks a lot.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q9ef2c7d296",
  "text": "Dear front desk,\nMalik Osei is writing to share file POL-2484 about the loss claim with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qb05f95160d",
  "text": "Dear duty clerk,\nOwen Pryce is sending file NTC-9710 about the notice response. The file is attached for your desk. Thanks in advance for your help.\nBest,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qb9740701e3",
  "text": "File: CASE-4152\nSubject: the claim deadline question\nSent by: Iris Vance\nHey there, this goes over to the records clerk. Hope everything is going nicely for you!",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q6e8f318669",
  "text": "Owen Pryce: Quick word, here is file POL-9568 about the insurance claim, I am swamped.\nservice: Thanks, I see it.\ndesk: Great, shared with the team.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q509ac5f47e",
  "text": "Hi admin team, Omar Saleh here with file CASE-2975 about the complaint filing. Thanks so much for helping keep everything tidy. It is a pleasure to share it with you all.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q1db12e5e58",
  "text": "Hi duty clerk,\nOmar Saleh is sending file NTC-8178 about the reply timing question. Writing fast, I am swamped. Attached is the file.\nThanks,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qda6eaeb05e",
  "text": "Iris Vance sends file POL-9862 about the cover question to the desk. This is the regular version, laid out in the standard format. The desk has the full set on hand. Passing it along as usual.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q4c43b8d2ce",
  "text": "Lena Whitcombe: Quick send of LED-1954 about the teller ledger review.\nservice desk: Thanks, that is in.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qb416a98f33",
  "text": "Bruno Lacerda: sending file STAY-8529 about the visa stay count, with thanks.\nintake team: thank you, this is received.\nintake team: appreciated.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q71bab76383",
  "text": "Hi front desk,\nBruno Lacerda is sending file NTC-4934 about the response deadline as routine correspondence. The file follows the standard layout. That is the full picture.\nRegards,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qd176aa278d",
  "text": "Hi duty clerk,\nAiko Brandt here with file POL-7590 about the insurance claim, and I am so glad it all came together. Hope it makes your work a little easier.\nCheers,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q7d87a9640f",
  "text": "Jonas Feld: file NTC-3877 about the response deadline is here.\nintake team: received, thanks.\nintake team: that is everything for this file.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qe3d7943624",
  "text": "Dear duty clerk,\nOwen Pryce is sending file NTC-9710 about the notice response. The file is attached for your desk. Thanks in advance for your help.\nBest,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q87d5fae90b",
  "text": "Ana Ruiz: Hello, I am sending file STAY-2797 about the visa stay count. My thanks in advance.\nintake team: Thank you, this has been received with care.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q7b75394e34",
  "text": "Sent by: Ines Duarte\nFile: CASE-9017\nSent to: records clerk\nShort note, my queue is packed. The file is about the appeal deadline and is attached.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q6e9a19fbf6",
  "text": "Dear front desk,\nBruno Lacerda is sending file LED-2566 about the teller ledger review. This is a routine send and the file is full. The matter is in good shape as usual.\nRegards",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q82f80207de",
  "text": "Nadia Kowal has passed on file STAY-9135 about the visa stay count to the desk. This memo goes with the file so it is on hand in the usual way. Thank you for your help.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q2197264dde",
  "text": "Sent by: Lena Whitcombe\nFile: LED-1907\nSent to: records clerk\nHappy to share the file about the teller ledger review, it was fun to put together. Hope it helps with the sorting.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q455a1942d9",
  "text": "File: CASE-6413\nSubject: the complaint filing\nSent by: Clara Weiss\nHey there, this goes over to the records clerk. Hope everything is going nicely for you!",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qbe693240b1",
  "text": "Sent by: Owen Pryce\nFile: NTC-6448\nSent to: review team\nThank you for your attention to the file about the response deadline. I remain grateful for the careful reading.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qb326c1c315",
  "text": "Felix Ortega: Dear team, I am forwarding file STAY-6316 about the visa stay count to the intake team.\nintake: Thank you for passing it along.\nteam: With thanks for your courtesy.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qf56ade3b1b",
  "text": "Iris Vance is sending file CASE-5131 about the claim deadline question to the admin team. It goes out in a hurry, with the attached pages in place. Thanks in advance.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q65f301ca5d",
  "text": "Hi duty clerk,\nYara Haddad here with file NTC-6951 about the notice response, and I am so glad it all came together. Hope it makes your work a little easier.\nCheers,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q956b1b6da5",
  "text": "Hi front desk,\nFelix Ortega is sending file PO-3615 about the purchase request as routine correspondence. The file follows the standard layout. That is the full picture.\nRegards,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q12a6b0beff",
  "text": "Internal memo for the desk.\n\nTomas Lindqvist sends file POL-5718 about the insurance claim to the desk, with the review team copied in. Thank you for your careful work on this matter. I appreciate the effort put into it.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q26b3a245b7",
  "text": "Freya Holm sends file STAY-1696 about the visa stay count to the desk. This is the regular version, laid out in the standard format. The desk has the full set on hand. Passing it along as usual.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q9a33989bd0",
  "text": "File: POL-4121\nSubject: the insurance claim\nSent by: Kofi Mensah\nHey there, this goes over to the records clerk. Hope everything is going nicely for you!",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q8f48f23deb",
  "text": "From: Paolo Greco\nFile: LED-6126\nSent to: records clerk\nThis file about the teller ledger review is sent over in a hurry. Thanks.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q484354526e",
  "text": "Priya Raman: sending POL-2735 about the cover question, in a rush.\nservice desk: got it, thanks.\ndesk: that is the full file.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qcfddfce009",
  "text": "From: Kofi Mensah\nFile: NTC-7479\nSent to: review team\nThe file about the response deadline is shared in the usual way.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q235624005a",
  "text": "Mira Castell: Sending CASE-4754 about the complaint filing, a routine send.\nintake team: Received, thanks.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q7597c4d954",
  "text": "Dear front desk,\nMira Castell is writing to share file STAY-4433 about the residence day count with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qe5527d6ff3",
  "text": "Ines Duarte: Busy, but here is PO-5018 about the purchase request.\nhelp desk: Received, thanks.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q27ad922d88",
  "text": "Hi admin team, this is Sara Ilves sharing file CASE-5005 about the complaint filing. It was a pleasure to pull it together. Thanks for keeping an eye on it.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q189cf69217",
  "text": "Maya Lindgren: Hey, sending case file NTC-4476 about the response deadline, hope it brightens the room.\ndesk: That is a lovely note, thanks!\ndesk: Good fun, I enjoyed reading it.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q3aabc2ff91",
  "text": "Yara Haddad has shared file STAY-2655 about the residence day count with the desk. The file goes in the usual way. This memo is for the file set.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q650c5cd149",
  "text": "Dear front desk,\nI am writing to share file CASE-3608 about the claim deadline question, sent by Hana Sato. Thank you for reading this message. The file is in full and in good shape. With respect and thanks.\nYours faithfully",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q651bb3dc2e",
  "text": "Lena Whitcombe sent file STAY-3640 about the visa stay count to the desk. The file is shared as part of the usual exchange. This is routine and straightforward.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qbb60d5e661",
  "text": "Dear duty clerk,\nDana Okafor is sending file POL-8252 about the insurance claim. It is attached here. Hope your work goes well.\nCheers,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "q11faa00715",
  "text": "Maya Lindgren sends file POL-8818 about the cover question to the desk. With thanks for your attention, the material is laid out with care. Respectfully yours.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 },
 {
  "qid": "qef49ea4c53",
  "text": "Tomas Lindqvist: Quick word, here is file POL-2024 about the insurance claim, I am swamped.\nservice: Thanks, I see it.\ndesk: Great, shared with the team.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
   },
   {
    "field": "ref",
    "type": "id",
    "describe": "the file, case or notice reference, as written"
   },
   {
    "field": "topic",
    "type": "str",
    "describe": "what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes \"about the ...\"; the topic does not include that \"the\")"
   }
  ]
 }
]
