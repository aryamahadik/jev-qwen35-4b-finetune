# G3-H extraction T01-extract_g3h-ca72d6ed-007 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g3h/answers/T01-extract_g3h-ca72d6ed-007.json

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
  "qid": "qdeebfb0ea5",
  "text": "Omar Saleh: Quick send, PO-8406 about the supplier order.\nhelp desk: Got it.",
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
  "qid": "q01b5f8fc25",
  "text": "Hey there, quick heads up that Yara Haddad has sent file STAY-8536 about the residence day count to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.",
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
  "qid": "qf4dfe77c5e",
  "text": "Tomas Lindqvist: Routine send, NTC-3682 about the reply timing question.\nintake team: Received, thank you.",
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
  "qid": "q9c337492db",
  "text": "Maya Lindgren: Quick send of CASE-9517 about the claim deadline question.\nservice desk: Thanks, that is in.",
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
  "qid": "qb33a3089f2",
  "text": "Theo Kalnins: Hello, I am sending file POL-2302 about the cover question to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.",
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
  "qid": "qc0cad6bb30",
  "text": "From: Paolo Greco\nFile: POL-7349\nSent to: records clerk\nHi there, here is the file about the insurance claim. Hope all is well with you!",
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
  "qid": "qed680e47cd",
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
  "qid": "qaaa01dc16e",
  "text": "Felix Ortega: Sending LED-1414 about the cash ledger check, a routine send.\nintake team: Received, thanks.",
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
  "qid": "q829aacc24c",
  "text": "Hi admin team, Paolo Greco here with file PO-5680 about the purchase request. Thanks so much for helping keep everything tidy. It is a pleasure to share it with you all.",
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
  "qid": "qcdf03984cc",
  "text": "Sent by: Ravi Anand\nFile: LED-3596\nSent to: review team\nThis is a standard note about the cash ledger check. The file is laid out as usual.",
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
  "qid": "q8d02e9c692",
  "text": "Ana Ruiz sends file CASE-7003 about the complaint filing to the admin team. Quick note, I am snowed under. The attachment carries the main points near the top. Off I go.",
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
  "qid": "q274060fb47",
  "text": "Felix Ortega: file POL-9693 about the insurance claim is here.\nintake team: received, thanks.\nintake team: that is everything for this file.",
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
  "qid": "q7de7fa650b",
  "text": "Tomas Lindqvist: Dear team, I am forwarding file POL-5670 about the insurance claim to the intake team.\nintake: Thank you for passing it along.\nteam: With thanks for your courtesy.",
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
  "qid": "q66ce12ec9d",
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
  "qid": "qcf874db62c",
  "text": "Omar Saleh has sent file CASE-4574 about the complaint filing to the admin team. It is a friendly little bundle for the admin desks. Thanks for the lovely teamwork.",
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
  "qid": "q5d059b482a",
  "text": "Felix Ortega sends file STAY-9383 about the border stay check to the desk. The file keeps to the standard format. A full copy sits with the desk too.",
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
  "qid": "qc2b2dfe5b0",
  "text": "Dear front desk team,\n\nMy name is Ines Duarte, and I am writing to send file CASE-6095 about the claim deadline question.\n\nThe file is attached below. Thank you for your help with this matter.\n\nKind regards,",
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
  "qid": "qe0e9680dc1",
  "text": "Felix Ortega: Sending POL-4673 about the cover question, short and sharp.\nservice desk: Received.",
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
  "qid": "q87a53d70e8",
  "text": "File: POL-1256\nSubject: the insurance claim\nSent by: Jonas Feld\nHey there, this goes over to the records clerk. Hope everything is going nicely for you!",
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
  "qid": "q8bfd3ec88d",
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
  "qid": "q3e9f1b70bd",
  "text": "Kofi Mensah: sending NTC-6620 about the response deadline, here it is.\nhelp desk: got it, thanks.\nhelp desk: that is the whole pack.",
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
  "qid": "q7111b20724",
  "text": "Lena Whitcombe: Sending POL-9829 about the loss claim, a routine send.\nintake team: Received, thanks.",
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
  "qid": "qb5357f8eb0",
  "text": "Dear duty clerk,\nQuick send from Omar Saleh: file LED-1068 about the cash ledger check is in. Sending it over fast as I am on the move. The attachment is full and whole. Thanks a bunch.\nKind regards",
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
  "qid": "q6783724eac",
  "text": "Internal memo for the desk.\n\nClara Weiss sends file POL-9260 about the insurance claim to the desk, with the review team copied in. Thank you for your careful work on this matter. I appreciate the effort put into it.",
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
  "qid": "qd1d253e871",
  "text": "File: STAY-9185\nSubject: the residence day count\nFrom: Malik Osei\nSending this straight across to the records clerk. The desk is very busy and stretched.",
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
  "qid": "q4e6e64fb36",
  "text": "Jonas Feld sends file STAY-1899 about the residence day count to the admin team. Writing fast because I am swamped. The file is attached and the main points sit at the top. Off to other work.",
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
  "qid": "q3093faf5df",
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
  "qid": "qdece5b10ce",
  "text": "Dear front desk,\nThis is Aiko Brandt writing to share file CASE-9370 about the complaint filing. The file is attached here. I hope this finds you well.\nKind regards,",
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
  "qid": "q3438977d4d",
  "text": "Lucas Brenner: Quick send, POL-3620 about the loss claim.\nhelp desk: Thanks, very swamped here.",
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
  "qid": "q44c0a18a9e",
  "text": "Omar Saleh sends file CASE-7142 about the appeal deadline to the desk. The file is set out in full with the usual headings. Thank you for your attention to this matter.",
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
  "qid": "q0f2fabd5d5",
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
  "qid": "qa20a491a7b",
  "text": "Hana Sato: Hiya! Sending CASE-6275 about the claim deadline question, all good here.\nservice desk: Lovely, thanks for the heads up!",
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
  "qid": "q4c031103e4",
  "text": "Ravi Anand: sending STAY-1179 about the residence day count, in a rush.\nservice desk: got it, thanks.\ndesk: that is the full file.",
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
  "qid": "qfce6b4abce",
  "text": "Dear front desk,\nThis is Paolo Greco writing to share file STAY-7819 about the visa stay count. The file is attached here. I hope this finds you well.\nKind regards,",
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
  "qid": "qcc38a606a8",
  "text": "Dear duty clerk,\nLena Whitcombe is sending file POL-9412 about the loss claim. It is attached here. Hope your work goes well.\nCheers,",
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
  "qid": "qdd9824989f",
  "text": "Kofi Mensah: sending NTC-6620 about the response deadline, here it is.\nhelp desk: got it, thanks.\nhelp desk: that is the whole pack.",
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
  "qid": "q6a0748b3e0",
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
  "qid": "qc821c22c1e",
  "text": "Aiko Brandt sends file CASE-8002 about the appeal deadline to the desk. With thanks for your attention, the material is laid out with care. Respectfully yours.",
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
  "qid": "qd56b120786",
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
  "qid": "q6c264175b6",
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
  "qid": "q75ccefb4d9",
  "text": "Hi front desk,\nInes Duarte sends file CASE-9404 about the claim deadline question in the usual form. The file sits in the standard layout alongside the other sheets.\nRegards,",
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
  "qid": "q07866c335f",
  "text": "Felix Ortega: Sending POL-9635 about the loss claim, a routine send.\nintake team: Received, thanks.",
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
  "qid": "qf416fa703b",
  "text": "Priya Raman has sent file CASE-4654 about the claim deadline question to the desk. This is a routine item and the file is attached in full. The desk is copied for completeness. This memo concerns only the sending of the file.",
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
  "qid": "qd78aa0ce1b",
  "text": "Hi duty clerk,\nBruno Lacerda is sending file POL-3957 about the cover question, with the main points at the top. Quick note, I am buried under other work.\nBest,",
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
  "qid": "q25ae57a08d",
  "text": "Sent by: Ana Ruiz\nFile: CASE-7528\nSent to: review team\nThe file is a routine copy about the claim deadline question. It follows the standard layout used by the team.",
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
  "qid": "q5aae455002",
  "text": "From: Freya Holm\nFile: STAY-5275\nSent to: review team\nI am passing on this file about the visa stay count. Thank you for your help.",
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
  "qid": "qb727cbd61b",
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
  "qid": "q344859ba95",
  "text": "Dear duty clerk,\nFelix Ortega here, sending file LED-5112 about the branch cash review. Very busy stretch on this end. The file is full and sent over fast. Thanks, speedy as ever.\nBest",
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
  "qid": "qf342784584",
  "text": "Dear front desk team,\n\nMy name is Mira Castell, and I am writing to send file POL-4150 about the loss claim.\n\nThe file is attached below. Thank you for your help with this matter.\n\nKind regards,",
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
  "qid": "q9a46848cf4",
  "text": "File: STAY-9185\nSubject: the residence day count\nFrom: Malik Osei\nSending this straight across to the records clerk. The desk is very busy and stretched.",
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
