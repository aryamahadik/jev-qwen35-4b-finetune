# G3-H extraction T01-extract_g3h-ca72d6ed-000 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g3h/answers/T01-extract_g3h-ca72d6ed-000.json

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
  "qid": "qf9f0b7640c",
  "text": "Aiko Brandt: Hello, I am sending file NTC-4941 about the notice response to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.",
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
  "qid": "q93d7f9295a",
  "text": "Aiko Brandt: sending file NTC-3386 about the response deadline, with thanks.\nintake team: thank you, this is received.\nintake team: appreciated.",
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
  "qid": "q9f7f6eddb1",
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
 },
 {
  "qid": "q7a0dd36139",
  "text": "Sent by: Hana Sato\nFile: POL-9833\nSent to: records clerk\nFast message from me, the inbox is overflowing. The file is about the insurance claim and is attached.",
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
  "qid": "qbe92cedd58",
  "text": "Sent by: Dana Okafor\nFile: CASE-4236\nSent to: records clerk\nShort note, my queue is packed. The file is about the appeal deadline and is attached.",
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
  "qid": "q80f2c74be4",
  "text": "File: LED-1066\nSubject: the cash ledger check\nFrom: Owen Pryce\nRespectfully passing this file on to the review team. Thank you kindly for your attention.",
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
  "qid": "q70f9df2420",
  "text": "Omar Saleh: file POL-5318 about the insurance claim is here.\nintake team: received, thanks.\nintake team: that is everything for this file.",
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
  "qid": "q58944e564a",
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
  "qid": "q986b060d2a",
  "text": "File: CASE-2566\nSubject: the claim deadline question\nFrom: Lucas Brenner\nQuick send to the records clerk. The desk is swamped, sorry for the speed.",
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
  "qid": "q69176b55c8",
  "text": "Dana Okafor: Hey there! Sending file CASE-2544 about the appeal deadline your way, hope it helps lol.\nservice: Thanks so much, that is great.\ndesk: Awesome, we have it on screen.",
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
  "qid": "q377110046a",
  "text": "Ana Ruiz: sending LED-4027 about the cash ledger check, here it is.\nhelp desk: got it, thanks.\nhelp desk: that is the whole pack.",
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
  "qid": "q31ea9fcf5a",
  "text": "Sent by: Mira Castell\nFile: CASE-7642\nSent to: records clerk\nHappy to share the file about the appeal deadline, it was fun to put together. Hope it helps with the sorting.",
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
  "qid": "qf7379a8a0a",
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
  "qid": "q8c0dba3bc9",
  "text": "Hi front desk,\nJonas Feld sends file STAY-5212 about the visa stay count as a standard copy. The file keeps to the usual format.\nRegards,",
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
  "qid": "qd79a09a96e",
  "text": "Hi duty clerk,\nYara Haddad here, sending file STAY-3484 about the visa stay count and hoping it brightens your desk. Big thanks to the team on this.\nCheers,",
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
  "qid": "q9a248693cc",
  "text": "Bruno Lacerda: file LED-6523 about the cash ledger check is attached.\ncase team: received, thanks.\ncase team: that is the whole file.",
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
  "qid": "q75536ef13c",
  "text": "Ana Ruiz: Hello, I am sending file NTC-8765 about the notice response to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.",
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
  "qid": "q233bb679aa",
  "text": "Sent by: Kofi Mensah\nFile: POL-5497\nSent to: records clerk\nHappy to share the file about the cover question, it was fun to put together. Hope it helps with the sorting.",
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
  "qid": "qfbd889edef",
  "text": "Aiko Brandt: Quick send, NTC-3938 about the reply timing question.\nhelp desk: Got it.",
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
  "qid": "qae23401c42",
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
  "qid": "qffe6fc206d",
  "text": "Freya Holm: Dear team, I am forwarding file STAY-4107 about the border stay check to the intake team.\nintake: Thank you for passing it along.\nteam: With thanks for your courtesy.",
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
  "qid": "q6937664ff7",
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
  "qid": "q72c1114b62",
  "text": "Kofi Mensah: Greetings, I am sending file CASE-1226 about the complaint filing for your kind attention.\ncase team: Thank you very much, it has been received.",
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
  "qid": "q0d76cbab18",
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
  "qid": "q6f3e592b80",
  "text": "Felix Ortega: Hey there! Sending file NTC-2874 about the notice response your way, hope it helps lol.\nservice: Thanks so much, that is great.\ndesk: Awesome, we have it on screen.",
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
  "qid": "q8fb1090994",
  "text": "Hi duty clerk,\nLucas Brenner here, just sending file POL-6760 about the loss claim. It is all in there with some friendly notes on the side, hope they make it fun.\nCheers,",
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
  "qid": "qf95689edcf",
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
  "qid": "qfe4fc82151",
  "text": "Lena Whitcombe: Hey hey, here is NTC-9046 about the response deadline, all looking lovely.\nservice desk: Thanks a bunch, lovely to see it!",
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
  "qid": "qd635519391",
  "text": "Malik Osei sent file STAY-3945 about the visa stay count to the desk. The file is shared as part of the usual exchange. This is routine and straightforward.",
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
  "qid": "q3637490ad1",
  "text": "Sender: Dana Okafor\nFile: CASE-1900\nTo: records clerk\nThe file about the appeal deadline is attached. Sending it on in a hurry.",
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
  "qid": "q87b35b2838",
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
  "qid": "q7699e9d5c5",
  "text": "Freya Holm: Hello. I am forwarding file POL-9351 about the cover question. My thanks for your help.\ncase team: Thank you, the file has been received.",
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
  "qid": "q72e0e3e91b",
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
  "qid": "qcbccc5a368",
  "text": "Hana Sato: Sending STAY-6864 about the visa stay count, short and sharp.\nservice desk: Received.",
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
  "qid": "q2b83c5e37b",
  "text": "Clara Weiss: Dear team, I am forwarding file LED-8656 about the cash ledger check to the intake team.\nintake: Thank you for passing it along.\nteam: With thanks for your courtesy.",
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
  "qid": "qbad1571b0a",
  "text": "Theo Kalnins: Sending CASE-9038 about the appeal deadline as usual.\ncase team: Received.",
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
  "qid": "q12fc047651",
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
  "qid": "qbbeb6baa26",
  "text": "Theo Kalnins: Routine send, NTC-9062 about the response deadline.\nintake team: Received, thank you.",
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
  "qid": "q7fddc75cb7",
  "text": "Sent by: Paolo Greco\nFile: STAY-6488\nSent to: review team\nThank you for your attention to the file about the residence day count. I remain grateful for the careful reading.",
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
  "qid": "q763ae87fac",
  "text": "Eva Marsh: Hiya! Sending PO-4668 about the purchase request, all good here.\nservice desk: Lovely, thanks for the heads up!",
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
  "qid": "q00d21cb98a",
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
  "qid": "q09f47ef695",
  "text": "Yara Haddad: Hello. I am forwarding file STAY-2376 about the residence day count. My thanks for your help.\ncase team: Thank you, the file has been received.",
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
  "qid": "qf24010c252",
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
  "qid": "q2db22ae8f8",
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
  "qid": "qeaba44d84c",
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
  "qid": "qfdd741e726",
  "text": "Jonas Feld has sent file LED-1504 about the teller ledger review to the admin team. It is a friendly little bundle for the admin desks. Thanks for the lovely teamwork.",
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
  "qid": "q1ecbc5ecd0",
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
  "qid": "q8bf6bde9cc",
  "text": "Dear front desk,\nDana Okafor is sending file STAY-6924 about the residence day count. The file is attached here for your records. I appreciate the help with it.\nKind regards,",
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
  "qid": "qcbf8f1c8b2",
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
  "qid": "q76a938e50b",
  "text": "Lucas Brenner sends file PO-4523 about the supplier order to the desk. With thanks for your attention, the material is laid out with care. Respectfully yours.",
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
