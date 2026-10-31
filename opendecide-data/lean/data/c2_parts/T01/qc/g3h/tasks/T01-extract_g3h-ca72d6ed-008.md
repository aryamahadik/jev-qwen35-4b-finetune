# G3-H extraction T01-extract_g3h-ca72d6ed-008 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g3h/answers/T01-extract_g3h-ca72d6ed-008.json

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
  "qid": "qcc559835dc",
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
  "qid": "q4a21b507e7",
  "text": "Hana Sato is passing along file LED-2187 about the branch cash review to the admin team. The file is short and goes straight to the pile. It is a quick, friendly handover.",
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
  "qid": "qc7d270d5ce",
  "text": "Eva Marsh sends file PO-3616 about the purchase request to the desk. The file is set out in full with the usual headings. Thank you for your attention to this matter.",
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
  "qid": "q8e3a946115",
  "text": "Freya Holm: Hiya! Sending POL-1588 about the cover question, all good here.\nservice desk: Lovely, thanks for the heads up!",
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
  "qid": "q7a6a437b55",
  "text": "From: Nadia Kowal\nFile: POL-8668\nSent to: review team\nThe file about the insurance claim is shared in the usual way.",
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
  "qid": "qe9ab682b6d",
  "text": "Aiko Brandt: I am sending file NTC-9805 about the response deadline, with thanks.\nintake team: thank you, received.\nintake team: kind regards.",
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
  "qid": "q5030995578",
  "text": "Aiko Brandt: Hey, sending case file STAY-1506 about the visa stay count, hope it brightens the room.\ndesk: That is a lovely note, thanks!\ndesk: Good fun, I enjoyed reading it.",
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
  "qid": "q384dd951b5",
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
  "qid": "q665ba41f41",
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
  "qid": "q53616643e5",
  "text": "Dear front desk,\nDana Okafor is writing to share file NTC-2057 about the reply deadline with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,",
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
  "qid": "qa8aa987443",
  "text": "Priya Raman: sending CASE-9814 about the complaint filing, in a rush.\nservice desk: got it, thanks.\nservice desk: good work, cheers.",
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
  "qid": "qac3cb83c77",
  "text": "Jonas Feld sent file STAY-2500 about the visa stay count to the desk. The file is shared as part of the usual exchange. This is routine and straightforward.",
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
  "qid": "q6a238e06b4",
  "text": "Hi duty clerk,\nDana Okafor is sending file STAY-2382 about the visa stay count, with the main points at the top. Quick note, I am buried under other work.\nBest,",
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
  "qid": "q1723ae49e7",
  "text": "Lucas Brenner: Sending POL-4543 about the loss claim.\ncase team: Received, thank you.",
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
  "qid": "q6f785ccbcf",
  "text": "Dear front desk,\nTomas Lindqvist is writing to share file NTC-3368 about the notice response with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,",
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
  "qid": "q1a77fc56f0",
  "text": "Internal memo for the desk.\n\nHana Sato sends file PO-2033 about the purchase request to the desk, with the review team copied in. Thank you for your careful work on this matter. I appreciate the effort put into it.",
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
  "qid": "q4d05f8441f",
  "text": "Hi duty clerk,\nHope you are doing great! Felix Ortega has sent file NTC-4741 about the response deadline, all lovely and tidy. Just wanted to pop it in your inbox. Catch you round.\nCheers",
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
  "qid": "q73277ca191",
  "text": "Ines Duarte: Hello. I am forwarding file CASE-9844 about the appeal deadline. My thanks for your help.\ncase team: Thank you, the file has been received.",
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
  "qid": "q43f0a12a47",
  "text": "Ana Ruiz: file CASE-6831 about the complaint filing is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.",
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
  "qid": "qe7c524ee61",
  "text": "Hi duty clerk,\nHope you are doing great! Hana Sato has sent file POL-1205 about the loss claim, all lovely and tidy. Just wanted to pop it in your inbox. Catch you round.\nCheers",
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
  "qid": "qd97f98199c",
  "text": "Ana Ruiz: file CASE-6831 about the complaint filing is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.",
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
  "qid": "q94938c2eb0",
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
  "qid": "qd266ace84e",
  "text": "From: Omar Saleh\nFile: LED-9942\nSent to: review team\nThis file about the branch cash review is passed along with thanks for your help.",
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
  "qid": "qaf29b5537f",
  "text": "Theo Kalnins: Hi, here is file CASE-4542 about the claim deadline question, with plenty of cheer.\ndesk: Lovely, thanks so much!\ndesk: That is fun to read.",
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
  "qid": "q2d18501565",
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
  "qid": "q489c0992f3",
  "text": "Hi duty clerk,\nTomas Lindqvist sends file PO-2289 about the supplier order with a cheerful hello. The file is in the usual layout and is fun to read.\nCheers,",
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
  "qid": "qbad4846adb",
  "text": "Dear duty clerk,\nQuick send from Lucas Brenner: file CASE-9203 about the complaint filing is in. Sending it over fast as I am on the move. The attachment is full and whole. Thanks a bunch.\nKind regards",
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
  "qid": "q53599f1407",
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
  "qid": "qa46b77951d",
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
  "qid": "q64bd5d0868",
  "text": "Hana Sato sends file NTC-4740 about the response deadline to the desk. The file is set out in full with the usual headings. Thank you for your attention to this matter.",
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
  "qid": "qe088a47269",
  "text": "Sara Ilves: Dear team, I am forwarding file POL-8967 about the cover question to the intake team.\nintake: Thank you for passing it along.\nteam: With thanks for your courtesy.",
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
  "qid": "qd6f91d3112",
  "text": "Theo Kalnins: sending NTC-3466 about the response deadline, here it is.\nhelp desk: got it, thanks.\nhelp desk: that is the whole pack.",
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
  "qid": "q3b378e9e6f",
  "text": "Hi front desk,\nHana Sato sends file POL-2227 about the cover question as a regular copy. The file follows the standard format. That covers the routine points.\nRegards,",
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
  "qid": "qedd73bf923",
  "text": "Theo Kalnins: file POL-9777 about the loss claim is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.",
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
  "qid": "q863b7f39f2",
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
  "qid": "qa15cd12104",
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
  "qid": "qcd4221d3a7",
  "text": "Dear front desk,\nDana Okafor is writing to share file NTC-2057 about the reply deadline with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,",
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
  "qid": "q123a5bb3e5",
  "text": "Hana Sato has shared file STAY-9464 about the visa stay count with the desk. The file goes in the usual way. This memo is for the file set.",
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
  "qid": "q9189ef3abd",
  "text": "Omar Saleh sends file POL-1108 about the cover question to the admin team. Sending this across quickly because I am tied up with other work. The full file is attached for the team. Thanks for taking it.",
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
  "qid": "q1fbd55b416",
  "text": "Yara Haddad: hey, here is CASE-1732 about the appeal deadline, sorry for the wait!\nservice desk: all good, got it.\nservice desk: brilliant, thanks a lot.",
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
  "qid": "qa0edf3b0b2",
  "text": "Dear front desk,\nTomas Lindqvist is writing to share file NTC-3368 about the notice response with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,",
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
  "qid": "q328f708be4",
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
  "qid": "q2886fc5d88",
  "text": "Iris Vance: Sending POL-8085 about the cover question, routine as usual.\nintake team: Thanks, received.",
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
  "qid": "q77b85f4c01",
  "text": "Hiya admin team, Ines Duarte has sent file STAY-6225 about the border stay check. Hope you are all well and enjoying the work. This is just a simple pass along with every bit in place. Thanks a bunch for taking it in, lovely to share this with you.",
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
  "qid": "q2ad701c999",
  "text": "Nadia Kowal: hi there, here is LED-1667 about the teller ledger review.\nhelp desk: thanks a bunch, got it.\nhelp desk: take care.",
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
  "qid": "q017d78a190",
  "text": "Bruno Lacerda has passed on file POL-5945 about the cover question to the desk. This memo goes with the file so it is on hand in the usual way. Thank you for your help.",
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
  "qid": "qee1e7be3b6",
  "text": "Dear front desk,\nTomas Lindqvist is writing to share file NTC-3368 about the notice response with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,",
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
  "qid": "q342979425d",
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
  "qid": "q2b1cad2580",
  "text": "Ravi Anand: Hey, sending POL-3026 about the loss claim, hope all is well!\nhelp desk: Lovely, thanks for sending it across.",
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
  "qid": "q7a7a0d69cf",
  "text": "Hi duty clerk,\nPriya Raman is sending file POL-2847 about the loss claim. Writing fast, I am swamped. Attached is the file.\nThanks,",
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
