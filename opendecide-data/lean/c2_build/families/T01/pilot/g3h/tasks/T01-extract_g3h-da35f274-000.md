# G3-H extraction T01-extract_g3h-da35f274-000 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T01/pilot/g3h/answers/T01-extract_g3h-da35f274-000.json

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
  "qid": "q16d694bdf5",
  "text": "Dear front desk,\nFelix Ortega respectfully sends file STAY-3414 about the visa stay count. My thanks go to you for looking at this. The file is in full and in good shape.\nYours sincerely",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qbfbdc5136b",
  "text": "Ines Duarte: Hello, I am sending file POL-8458 about the cover question. My thanks in advance.\nintake team: Thank you, this has been received with care.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q932b722fa0",
  "text": "Bruno Lacerda: file CASE-2677 about the complaint filing is attached here.\ncase team: thank you, that is received.\ncase team: kind regards.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q5215c2483e",
  "text": "Lena Whitcombe: Hey hey, here is PO-1742 about the buying request, all looking lovely.\nservice desk: Thanks a bunch, lovely to see it!",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q41db1ac638",
  "text": "Hi front desk,\nEva Marsh sends file STAY-8365 about the border stay check as a routine copy. The file follows the standard layout and sits with the desk.\nRegards,",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qfeeaf0eba7",
  "text": "Hey there, quick heads up that Freya Holm has sent file NTC-3766 about the notice response to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q58891f4a5e",
  "text": "Omar Saleh: File NTC-6791 is sent about the notice response as normal.\ncase team: Received, thank you.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qd7d457fdc1",
  "text": "Ines Duarte: sending NTC-4132 about the notice response, here it is.\nhelp desk: got it, thanks.\nhelp desk: that is the whole pack.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q08d83061ea",
  "text": "Owen Pryce: File STAY-1065 is sent about the visa stay count as normal.\ncase team: Received, thank you.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q449416b480",
  "text": "Sent by: Clara Weiss\nFile: STAY-4973\nSent to: records clerk\nFast message from me, the inbox is overflowing. The file is about the border stay check and is attached.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q39dc472b43",
  "text": "Hi front desk,\nOwen Pryce sends file NTC-2550 about the response deadline as a standard copy. The file keeps to the usual format.\nRegards,",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q1a7a585a50",
  "text": "Sent by: Jonas Feld\nFile: POL-1842\nSent to: review team\nThank you for your attention to the file about the cover question. I remain grateful for the careful reading.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q2db14ed241",
  "text": "Sara Ilves: sending NTC-3654 about the notice response, fast and short.\nhelp desk: okay, got it.\nhelp desk: thanks, that is the whole thing.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q21131796a9",
  "text": "File: CASE-9406\nSubject: the claim deadline question\nFrom: Nadia Kowal\nHi there, sending this small file over to the records clerk. Lovely to share it with you all!",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qe9d9f2f3e1",
  "text": "Felix Ortega: Quick send of POL-6563 about the insurance claim.\nservice desk: Thanks, that is in.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q39099b7f94",
  "text": "Dear duty clerk,\nFreya Holm here, sending file STAY-7952 about the visa stay count. Very busy stretch on this end. The file is full and sent over fast. Thanks, speedy as ever.\nBest",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q5111bbce69",
  "text": "Priya Raman: sending file POL-8032 about the loss claim, with thanks.\nintake team: received, thank you.\nintake team: best wishes.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q24654d9ce1",
  "text": "Sent by: Bruno Lacerda\nFile: NTC-2156\nSent to: records clerk\nHappy to share the file about the notice response, it was fun to put together. Hope it helps with the sorting.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q35f403f6e4",
  "text": "Hi duty clerk,\nFreya Holm here with file NTC-4249 about the response deadline, and I am so glad it all came together. Hope it makes your work a little easier.\nCheers,",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q7db22b0061",
  "text": "Hi front desk,\nOmar Saleh sends file POL-9350 about the cover question as a regular copy. The file follows the standard format. That covers the routine points.\nRegards,",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q7aedf71027",
  "text": "Sent by: Clara Weiss\nFile: STAY-4973\nSent to: records clerk\nFast message from me, the inbox is overflowing. The file is about the border stay check and is attached.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qfe85e21952",
  "text": "Kofi Mensah: File POL-7800 is sent about the cover question as normal.\ncase team: Received, thank you.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qa83275a9fc",
  "text": "Felix Ortega: file POL-5421 about the cover question is here.\nintake team: received, thanks.\nintake team: that is everything for this file.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qd9cc6e8e5e",
  "text": "Iris Vance sends file CASE-9666 about the claim deadline question to the admin team. Hope you all are doing well with the busy stretch, this is a fun read. Thanks for keeping the wheels turning.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q80beef68c6",
  "text": "Yara Haddad: Respectfully, I am passing file POL-7148 about the insurance claim to the case team.\nteam: Thank you for the note.\nteam: The care shown is much appreciated.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q8307351fd1",
  "text": "Sara Ilves: sending NTC-3654 about the notice response, fast and short.\nhelp desk: okay, got it.\nhelp desk: thanks, that is the whole thing.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q99c8e9e04a",
  "text": "Owen Pryce: File STAY-1065 is sent about the visa stay count as normal.\ncase team: Received, thank you.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qb70503ae46",
  "text": "Bruno Lacerda: Greetings, I am sending file CASE-2663 about the claim deadline question for your kind attention.\ncase team: Thank you very much, it has been received.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q87556b7037",
  "text": "Jonas Feld: I am sending file PO-8814 about the purchase request, with thanks.\nintake team: thank you, received.\nintake team: kind regards.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q5627389e6e",
  "text": "Nadia Kowal: file LED-5281 about the branch cash review is attached.\ncase team: received, thanks.\ncase team: that is the whole file.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q9ab19d4cff",
  "text": "Nadia Kowal: file LED-5281 about the branch cash review is attached.\ncase team: received, thanks.\ncase team: that is the whole file.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q6e722443f5",
  "text": "Dana Okafor: file NTC-9442 about the response deadline is attached here.\ncase team: thank you, that is received.\ncase team: kind regards.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q00de64ff84",
  "text": "Aiko Brandt: sending file NTC-1485 about the reply deadline, with thanks.\nintake team: received, thank you.\nintake team: best wishes.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q4c2db9b2da",
  "text": "Hi front desk,\nOwen Pryce sends file STAY-7995 about the residence day count as a routine copy. The file follows the standard layout and sits with the desk.\nRegards,",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q94132631e7",
  "text": "Ines Duarte: Sending STAY-8054 about the visa stay count as usual.\ncase team: Received.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q7a2185188e",
  "text": "Felix Ortega: Hey, sending case file NTC-4364 about the notice response, hope it brightens the room.\ndesk: That is a lovely note, thanks!\ndesk: Good fun, I enjoyed reading it.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q2466305407",
  "text": "Priya Raman: sending STAY-1585 about the visa stay count, here it is.\nhelp desk: got it, thanks.\nhelp desk: that is the whole pack.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qad6ffffac8",
  "text": "Theo Kalnins: Greetings, I am sending file STAY-2529 about the border stay check for your kind attention.\ncase team: Thank you very much, it has been received.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q714c025178",
  "text": "Hi admin team, Nadia Kowal here with file NTC-9168 about the response deadline. Thanks so much for helping keep everything tidy. It is a pleasure to share it with you all.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qa79e8dee3f",
  "text": "File: STAY-9860\nSubject: the residence day count\nFrom: Tomas Lindqvist\nThis file is respectfully passed to the review team. With warm thanks for your attention.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q92bcf229fe",
  "text": "Sara Ilves: Hey hey, here is CASE-7039 about the complaint filing, all looking lovely.\nservice desk: Thanks a bunch, lovely to see it!",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qc7394d0a70",
  "text": "Hi admin team, Nadia Kowal here with file NTC-9168 about the response deadline. Thanks so much for helping keep everything tidy. It is a pleasure to share it with you all.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qf8c13f4cd9",
  "text": "Felix Ortega sends file STAY-2825 about the visa stay count to the desk. The file is set out in full with the usual headings. Thank you for your attention to this matter.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "q5a5bd92323",
  "text": "Lucas Brenner: sending PO-8328 about the purchase request, in a rush.\nservice desk: got it, thanks.\ndesk: that is the full file.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qb9a1756386",
  "text": "Dana Okafor has sent file NTC-3766 about the response deadline to the desk. This memo goes with the file so the desk has it on hand. Thank you for your help with it.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qb1560e3317",
  "text": "Kofi Mensah: sending NTC-1041 about the response deadline, here it is.\nhelp desk: got it, thanks.\nhelp desk: that is the whole pack.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qe17813f249",
  "text": "Tomas Lindqvist: Busy, but here is POL-9622 about the cover question.\nhelp desk: Received, thanks.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qef89517ae0",
  "text": "Ines Duarte: I am sending file PO-3317 about the purchase request, with thanks.\nintake team: thank you, received.\nintake team: kind regards.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qa86e5cb537",
  "text": "Yara Haddad: Sending file STAY-7506 about the residence day count, the regular copy.\nteam: Thanks, the copy is in the standard format.\nteam: All of it follows the usual layout.",
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
    "describe": "what the message is about, as written"
   }
  ]
 },
 {
  "qid": "qaf7a1360e9",
  "text": "Felix Ortega: file NTC-4757 about the response deadline is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.",
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
    "describe": "what the message is about, as written"
   }
  ]
 }
]
