# G3-H extraction T01-extract_g3h-da35f274-001 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T01/pilot/g3h/answers/T01-extract_g3h-da35f274-001.json

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
  "qid": "qb4cb393718",
  "text": "Priya Raman has sent file LED-9600 about the branch cash review to the admin team. It is a friendly little bundle for the admin desks. Thanks for the lovely teamwork.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q3bec061736",
  "text": "Felix Ortega: file LED-3639 about the cash ledger check is attached here.\ncase team: thank you, that is received.\ncase team: kind regards.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q3ee9191697",
  "text": "Maya Lindgren: Busy send, NTC-5356 about the response deadline.\nservice desk: Received, thanks.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qd0c30e328b",
  "text": "Freya Holm: Sending STAY-6848 about the visa stay count, routine as usual.\nintake team: Thanks, received.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q3f5bedfb97",
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
  "qid": "q2c8d640a11",
  "text": "File: PO-3317\nSubject: the purchase request\nFrom: Ines Duarte\nSending this straight across to the records clerk. The desk is very busy and stretched.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qc88d1f6c3f",
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
  "qid": "q06a0bab6c4",
  "text": "Theo Kalnins has shared file CASE-7734 about the complaint filing with the desk. The file goes in the usual way. This memo is for the file set.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q475d5270ea",
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
  "qid": "q095054f646",
  "text": "Clara Weiss: Hey there! Sending file POL-6360 about the loss claim your way, hope it helps lol.\nservice: Thanks so much, that is great.\ndesk: Awesome, we have it on screen.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q1784cd7697",
  "text": "Hi admin team, Sara Ilves here with file POL-5434 about the cover question. Thanks so much for helping keep everything tidy. It is a pleasure to share it with you all.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q4c15906826",
  "text": "Theo Kalnins: Hey there! Sending file CASE-5795 about the appeal deadline your way, hope it helps lol.\nservice: Thanks so much, that is great.\ndesk: Awesome, we have it on screen.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q6c3af40524",
  "text": "Paolo Greco is passing along file NTC-9326 about the response deadline to the admin team. The file is short and goes straight to the pile. It is a quick, friendly handover.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q8079753906",
  "text": "Dana Okafor: Hello, I am sending file STAY-1281 about the border stay check to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q81bd6fcfb1",
  "text": "Ines Duarte: sending STAY-7129 about the border stay check, fast and short.\nhelp desk: okay, got it.\nhelp desk: thanks, that is the whole thing.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q713877870d",
  "text": "Owen Pryce: sending POL-9265 about the cover question, in a rush.\nservice desk: got it, thanks.\ndesk: that is the full file.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q6bb9a5d5b6",
  "text": "Dana Okafor: Hello, I am sending file STAY-1281 about the border stay check to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q2c69cce4cb",
  "text": "From: Theo Kalnins\nFile: STAY-2756\nSent to: review team\nI am passing on this file about the border stay check. Thank you for your help.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qbeffab9061",
  "text": "Clara Weiss: Hello, I am sending file NTC-1153 about the notice response. My thanks in advance.\nintake team: Thank you, this has been received with care.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qbb4e1d224a",
  "text": "Mira Castell: Quick send of POL-8800 about the insurance claim.\nservice desk: Thanks, that is in.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q5d72865d72",
  "text": "Priya Raman sends file POL-2070 about the loss claim to the desk. With thanks for your attention, the material is laid out with care. Respectfully yours.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qdd33a61fb8",
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
  "qid": "q17aaa67d82",
  "text": "From: Kofi Mensah\nFile: LED-4924\nSent to: review team\nThe file about the branch cash review is shared as usual.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q9d72a74146",
  "text": "Sent by: Bruno Lacerda\nFile: LED-8100\nSent to: records clerk\nLovely to send this over, it is about the branch cash review. The notes are all tidy and sit nicely for the records team.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q4ae35cce6b",
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
  "qid": "q22ddd62e84",
  "text": "Aiko Brandt: Hello, I am sending file NTC-4522 about the reply timing question. My thanks in advance.\nintake team: Thank you, this has been received with care.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q470f1bedbb",
  "text": "Owen Pryce: sending POL-9265 about the cover question, in a rush.\nservice desk: got it, thanks.\ndesk: that is the full file.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qb525e11ffc",
  "text": "File: POL-5153\nSubject: the loss claim\nFrom: Dana Okafor\nRespectfully passing this file on to the review team. Thank you kindly for your attention.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qa694abea13",
  "text": "Maya Lindgren: Busy send, NTC-5356 about the response deadline.\nservice desk: Received, thanks.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qb329367289",
  "text": "Iris Vance: hi! Passing along CASE-3167 about the appeal deadline.\nservice desk: lovely, thanks a lot.\nservice desk: happy to help, cheers.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q37885953d9",
  "text": "Nadia Kowal: File STAY-7523 is sent about the border stay check as normal.\ncase team: Received, thank you.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qd82d953f2d",
  "text": "Dear duty clerk,\nOwen Pryce is sending file NTC-4887 about the reply timing question. It is attached here. Hope your work goes well.\nCheers,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q258b068158",
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
  "qid": "qa8fa60f308",
  "text": "File: PO-5825\nSubject: the purchase request\nSent by: Iris Vance\nHey there, this goes over to the records clerk. Hope everything is going nicely for you!",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qfa8e4ce841",
  "text": "Mira Castell: Quick send of POL-8800 about the insurance claim.\nservice desk: Thanks, that is in.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qb9d15a246d",
  "text": "File: POL-8135\nSubject: the loss claim\nFrom: Eva Marsh\nHey there, this is heading off to the records clerk with a smile. Hope you are having a fun run of things!",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q418a9a5269",
  "text": "Iris Vance: file NTC-3047 about the notice response is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qf410bb97a0",
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
  "qid": "qa926a14abb",
  "text": "Freya Holm: Sending STAY-6848 about the visa stay count, routine as usual.\nintake team: Thanks, received.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q6cb1627f1b",
  "text": "Omar Saleh: sending NTC-3935 about the notice response, in a rush.\nservice desk: got it, thanks.\nservice desk: good work, cheers.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q7c9c02a1be",
  "text": "Hi admin team, this is Clara Weiss sharing file CASE-5793 about the appeal deadline. It was a pleasure to pull it together. Thanks for keeping an eye on it.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qe2bc336621",
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
  "qid": "qd65f65d883",
  "text": "Yara Haddad: Hello, I am sending file CASE-5768 about the appeal deadline. My thanks in advance.\nintake team: Thank you, this has been received with care.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q9f4ce8341d",
  "text": "Hi duty clerk,\nFreya Holm is sending file LED-8984 about the branch cash review, with the main points at the top. Quick note, I am buried under other work.\nBest,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q325c4ed170",
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
  "qid": "q5f870879a1",
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
  "qid": "qa3fa925a50",
  "text": "Clara Weiss: Hey there! Sending file POL-6360 about the loss claim your way, hope it helps lol.\nservice: Thanks so much, that is great.\ndesk: Awesome, we have it on screen.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q155e907c9e",
  "text": "Hana Sato: Hello. I am forwarding file POL-1289 about the loss claim. My thanks for your help.\ncase team: Thank you, the file has been received.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "qd253728dd7",
  "text": "Tomas Lindqvist: Sending NTC-5017 about the response deadline as usual.\ncase team: Received.",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
  "qid": "q3d12f67882",
  "text": "Hi duty clerk,\nIris Vance is sending file POL-5329 about the cover question, with the main points at the top. Quick note, I am buried under other work.\nBest,",
  "schema": [
   {
    "field": "person",
    "type": "name",
    "describe": "the person who wrote or is named as the sender, as written"
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
