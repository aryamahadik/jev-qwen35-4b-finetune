# G3-H extraction T01-extract_g3h-ca72d6ed-002 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g3h/answers/T01-extract_g3h-ca72d6ed-002.json

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
  "qid": "qe123c3bac6",
  "text": "Sent by: Lena Whitcombe\nFile: PO-2444\nSent to: records clerk\nShort note, my queue is packed. The file is about the purchase request and is attached.",
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
  "qid": "qb7334c3beb",
  "text": "Hey there, quick heads up that Kofi Mensah has sent file NTC-2210 about the response deadline to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.",
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
  "qid": "q0a50c3322c",
  "text": "Priya Raman: Hi, here is file NTC-5750 about the response deadline, with plenty of cheer.\ndesk: Lovely, thanks so much!\ndesk: That is fun to read.",
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
  "qid": "q402a9f9882",
  "text": "Dana Okafor: sending STAY-2549 about the residence day count, in a rush.\nservice desk: got it, thanks.\nservice desk: good work, cheers.",
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
  "qid": "qea9a7193e7",
  "text": "Mira Castell: Sending STAY-3307 about the residence day count as usual.\ncase team: Received.",
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
  "qid": "q8d5f6727f7",
  "text": "Maya Lindgren has shared file LED-9060 about the branch cash review with the desk. The file goes in the usual way. This memo is for the file set.",
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
  "qid": "q71374a52e6",
  "text": "Dear front desk,\nRavi Anand is writing to share file CASE-2441 about the claim deadline question with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,",
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
  "qid": "qee42d671c3",
  "text": "Dear duty clerk,\nTheo Kalnins is sending file NTC-7846 about the reply deadline. The file is attached for your desk. Thanks in advance for your help.\nBest,",
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
  "qid": "q759e2152da",
  "text": "Yara Haddad: file CASE-4276 about the claim deadline question is here.\nintake team: received, thanks.\nintake team: that is everything for this file.",
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
  "qid": "q5fbceedb7f",
  "text": "Hi duty clerk,\nHana Sato is sending file PO-8837 about the purchase request. Writing fast, I am swamped. Attached is the file.\nThanks,",
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
  "qid": "qf01e96c289",
  "text": "Dear duty clerk,\nTheo Kalnins is sending file POL-4943 about the loss claim. The file is attached for your desk. Thanks in advance for your help.\nBest,",
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
  "qid": "q7c4595557f",
  "text": "Bruno Lacerda: Busy desk, sending STAY-9105 about the residence day count, straight over.\nhelp desk: In hand.",
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
  "qid": "qad67acb5e2",
  "text": "Sent by: Clara Weiss\nFile: STAY-1237\nSent to: review team\nThe file is a routine copy about the residence day count. It follows the standard layout used by the team.",
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
  "qid": "q6a67d0a531",
  "text": "Sent by: Bruno Lacerda\nFile code: NTC-9540\nFor: review team\nThe file about the response deadline is passed along as usual.",
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
  "qid": "qe94fd4270a",
  "text": "Iris Vance: I am sending file POL-9430 about the loss claim, with thanks.\nintake team: thank you, received.\nintake team: kind regards.",
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
  "qid": "qd2db4a795e",
  "text": "Eva Marsh: Hey there! Sending file STAY-1249 about the border stay check your way, hope it helps lol.\nservice: Thanks so much, that is great.\ndesk: Awesome, we have it on screen.",
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
  "qid": "qaaf788f2d9",
  "text": "Lucas Brenner: Hello, I am sending file NTC-6208 about the response deadline to the case team, with thanks.\nteam: Thank you for the careful note.\nteam: Your gesture is warmly felt.",
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
  "qid": "q3f5061cf54",
  "text": "Hi duty clerk,\nHana Sato is sending file NTC-2583 about the notice response, with the main points at the top. Quick note, I am buried under other work.\nBest,",
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
  "qid": "q2b026329fd",
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
  "qid": "q64488ec780",
  "text": "Felix Ortega: hi! Here is CASE-8280 about the appeal deadline.\nhelp desk: lovely, received.\nhelp desk: great, enjoy your work.",
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
  "qid": "q5f0e0e2567",
  "text": "Hey there, quick heads up that Bruno Lacerda has sent file NTC-4881 about the notice response to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.",
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
  "qid": "q11743c524c",
  "text": "Clara Weiss: Hey, sending CASE-9311 about the claim deadline question, hope all is well!\nhelp desk: Lovely, thanks for sending it across.",
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
  "qid": "q48dd3dbffe",
  "text": "Maya Lindgren has shared file LED-9060 about the branch cash review with the desk. The file goes in the usual way. This memo is for the file set.",
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
  "qid": "q259391e3ba",
  "text": "Dear front desk,\nPaolo Greco is sending file PO-3559 about the purchase request. The file is attached here for your records. I appreciate the help with it.\nKind regards,",
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
  "qid": "q11911c36d0",
  "text": "Internal memo for the desk.\n\nLena Whitcombe sends file POL-4658 about the insurance claim to the desk, with the review team copied in. Thank you for your careful work on this matter. I appreciate the effort put into it.",
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
  "qid": "qc8d727a713",
  "text": "Dana Okafor sends file POL-7909 about the insurance claim to the desk. The file keeps to the standard format. A full copy sits with the desk too.",
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
  "qid": "q2328a26a61",
  "text": "Ana Ruiz: passing along CASE-4468 about the claim deadline question.\nintake team: thanks, that is clear.\nintake team: great, thanks again.",
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
  "qid": "qaa56afd4e7",
  "text": "Freya Holm: file PO-2372 about the purchase request is attached here.\ncase team: thank you, that is received.\ncase team: kind regards.",
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
  "qid": "qd06da931e5",
  "text": "Clara Weiss: Sending STAY-3547 about the border stay check, routine as usual.\nintake team: Thanks, received.",
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
  "qid": "qf953ffe56c",
  "text": "Theo Kalnins: sending file PO-5502 about the purchase request, with thanks.\nintake team: thank you, this is received.\nintake team: appreciated.",
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
  "qid": "q4e3e7f5d49",
  "text": "Yara Haddad: Sending LED-9332 about the teller ledger review, a routine send.\nintake team: Received, thanks.",
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
  "qid": "q83bfe416e4",
  "text": "File: LED-9163\nSubject: the branch cash review\nFrom: Priya Raman\nSending this straight across to the records clerk. The desk is very busy and stretched.",
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
  "qid": "q64275e60d6",
  "text": "Lena Whitcombe: hey, here is POL-4449 about the insurance claim, sorry for the wait!\nservice desk: all good, got it.\nservice desk: brilliant, thanks a lot.",
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
  "qid": "q688bc58284",
  "text": "Hana Sato: passing along CASE-5247 about the claim deadline question.\nintake team: thanks, that is clear.\nintake team: great, thanks again.",
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
  "qid": "q15ea993cfe",
  "text": "Hi admin team, Aiko Brandt here with file LED-1198 about the cash ledger check. Thanks so much for helping keep everything tidy. It is a pleasure to share it with you all.",
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
  "qid": "qff3e8bca48",
  "text": "Eva Marsh: Hello, I am sending file LED-8525 about the cash ledger check to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.",
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
  "qid": "qc61caa2869",
  "text": "Dear duty clerk,\nMaya Lindgren is sending file STAY-7013 about the border stay check. It is attached here. Hope your work goes well.\nCheers,",
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
  "qid": "q86644eb670",
  "text": "Theo Kalnins: file POL-5186 about the insurance claim is attached here.\ncase team: thank you, that is received.\ncase team: kind regards.",
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
  "qid": "q6d652e7e74",
  "text": "Dear front desk,\nI am writing to share file PO-6112 about the purchase request, sent by Hana Sato. Thank you for reading this message. The file is in full and in good shape. With respect and thanks.\nYours faithfully",
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
  "qid": "q603fc2f222",
  "text": "Hey there, quick heads up that Kofi Mensah has sent file NTC-2210 about the response deadline to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.",
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
  "qid": "q323609e91c",
  "text": "Maya Lindgren sends file STAY-7224 about the visa stay count to the admin team. Sending this across quickly because I am tied up with other work. The full file is attached for the team. Thanks for taking it.",
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
  "qid": "q36ec498df7",
  "text": "Aiko Brandt: Hiya! Sending POL-8694 about the insurance claim, all good here.\nservice desk: Lovely, thanks for the heads up!",
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
  "qid": "qfedb385e5f",
  "text": "Eva Marsh: Hello, I am sending file CASE-7220 about the claim deadline question to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.",
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
  "qid": "qe665d22935",
  "text": "Nadia Kowal: file PO-9303 about the supplier order is attached here.\ncase team: thank you, that is received.\ncase team: that is all for this file.",
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
  "qid": "q31218f53be",
  "text": "Ana Ruiz has sent file STAY-7389 about the border stay check to the desk. This is a routine item and the file is attached in full. The desk is copied for completeness. This memo concerns only the sending of the file.",
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
  "qid": "q407a4ca1ed",
  "text": "From: Paolo Greco\nFile: CASE-8402\nSent to: review team\nThis file about the appeal deadline is passed along with thanks for your help.",
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
  "qid": "qa9b992306d",
  "text": "From: Omar Saleh\nFile: PO-8414\nSent to: records clerk\nThis file about the supplier order is sent over in a hurry. Thanks.",
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
  "qid": "q2ddc6526d4",
  "text": "Dear front desk,\nInes Duarte is sending file CASE-7437 about the appeal deadline. This is a routine send and the file is full. The matter is in good shape as usual.\nRegards",
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
  "qid": "q4c7061325c",
  "text": "Paolo Greco: File CASE-6871 is sent about the claim deadline question as normal.\ncase team: Received, thank you.",
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
  "qid": "q1be5d07086",
  "text": "Omar Saleh: Sending CASE-1227 about the complaint filing, a routine send.\nintake team: Received, thanks.",
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
