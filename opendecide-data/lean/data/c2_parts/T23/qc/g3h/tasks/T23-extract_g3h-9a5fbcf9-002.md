# G3-H extraction T23-extract_g3h-9a5fbcf9-002 (family T23)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T23/qc/g3h/answers/T23-extract_g3h-9a5fbcf9-002.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "case_id": <value or null>, "customer": <value or null>, "item": <value or null>, "org": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q7dee23c8d0",
  "text": "Hello,\nHana Sato here. I am writing to raise a case with Quayside Software about the conference trip. The case is logged under CASE-6069 and the history follows.\nWarm regards",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q0f2a94d619",
  "text": "Coffee grinder case from Tomas Lindqvist\nTomas Lindqvist raised a case with Mistral Home about a team offsite, filed as CASE-1575. The details are shared here in a warm, plain way, with the background set out for the reader.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qdb4567d6d2",
  "text": "Coffee grinder case for Owen Pryce\nOwen Pryce raised case CASE-2832 with Mistral Home about a camera recording. Warm greetings to you, and the full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qd9edf6a134",
  "text": "Hi there,\nI am reaching out about my photo editor with Brightwell Supply, which is a calm and routine matter. My name is Sara Ilves and the case is logged as CASE-3712. The rest follows in the notes below.\nThanks,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qccf1448853",
  "text": "Aiko Brandt has raised a case with Lindenfeld Outfitters about an annual plan, filed as CASE-1602. The background and details of the matter follow in this file. Matters of this kind are set out formally and briefly.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q1ff58cdd3d",
  "text": "name: Yara Haddad\ncompany: Lindenfeld Outfitters\ncase: CASE-8539\nYara Haddad is cheerful and easy to work with, having raised a case with Lindenfeld Outfitters about the gym membership, and the story is set out below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qe51c440855",
  "text": "case: CASE-2641\ncontact: Priya Raman\nitem: language course\nA polite but slightly irritated case was raised with Redfern Bank about the language course. The details follow in the usual way.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qda631e76c0",
  "text": "Hi Ravi Anand,\nYour case CASE-5228 with Selkirk Logistics covers a tyre order that you raised. Everything is calm and routine, and the details are set out in the sections below.\nWarm regards",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q1dceb025f7",
  "text": "Hello,\nHana Sato here. I am writing to raise a case with Quayside Software about the conference trip. The case is logged under CASE-6069 and the history follows.\nWarm regards",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qcafa9c7cbd",
  "text": "Ravi Anand: Hello, I would like to put a formal matter on record with Selkirk Logistics about my standing desk.\nsupport: Thank you for getting in touch. CASE-4387 is logged and the background to the standing desk follows.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q0cb1826c0a",
  "text": "Hello there,\nMy name is Lucas Brenner and I am writing to raise a case with Halvard Insurance about my card account. The history and case details are set out below, filed as CASE-2510.\nKind regards,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q851f09bd0a",
  "text": "Internal case note: Ana Ruiz contacted Quayside Software about a camera recording and the matter is logged under CASE-1045. It is a calm, routine entry with a steady pace. Background and case details are set out further down.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qbb6b3a6631",
  "text": "Lucas Brenner: Hello. I am calling about my design suite. I raised a case with Tamsin Fitness and I am slightly irritated, but I would like a clear answer.\nagent: Hello. I have case CASE-9100 on file, so let us look at the design suite details.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qd36053a81a",
  "text": "name: Tomas Lindqvist\norganisation: Pembroke Travel\ncase: CASE-4305\nTomas Lindqvist is a touch irritated, but polite, and has raised a case with Pembroke Travel about the camera recording.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q502745dde6",
  "text": "Hi Ravi Anand,\nYour case CASE-5228 with Selkirk Logistics covers a tyre order that you raised. Everything is calm and routine, and the details are set out in the sections below.\nWarm regards",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q2866438f40",
  "text": "case: CASE-9646\ncustomer: Lucas Brenner\nitem: customer file\nThe customer warmly raised a case with Selkirk Logistics about the customer file, and the details follow. It is a friendly start to the file.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qb83e166efe",
  "text": "customer: Eva Marsh\norganisation: Veridia Health\ncase: CASE-2355\nEva Marsh raised this case about the savings account. A friendly hello from the team, and the details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q29ea246eb9",
  "text": "Ines Duarte: Hi, I am ringing to chat about my card account from Mistral Home, and I feel quite cheerful about it.\nagent: Lovely to hear from you. Your case CASE-9795 is in front of me, and it is a pleasure to help with the card account.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q27ac4e1393",
  "text": "Sara Ilves: Hello, it is lovely to speak with you. I am calling to raise a case with Upland Utilities about my study block.\nagent: Hello, thank you for calling. Your case, CASE-9690, is right here on my screen.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qd056dd15a7",
  "text": "customer: Dana Okafor\ncompany: Quayside Software\ncase: CASE-9622\nDana Okafor is a little irritated but polite and has raised a case with Quayside Software about the antivirus licence.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q34c7fa2f8f",
  "text": "Lucas Brenner: Hello. I am calling about my e-bike. I raised a case with Corran Telecom and I am a bit irritated, and I would like to talk it through with you.\nagent: Hello. I have case CASE-9311 on file, so let us talk through the e-bike details.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q42c4411fe0",
  "text": "Hello,\nMy name is Jonas Feld and I am writing to raise a case with Redfern Bank about my current account. The matter is calm and routine, and the case is filed as CASE-2410. The details follow below.\nTake care,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qdcce23e719",
  "text": "Ines Duarte: I am calling about a standing desk with Halvard Insurance and it is rather irritating, though I am polite about it.\nagent: I hear you, and I apologise for the trouble. Your case CASE-7735 is in front of me and the standing desk details are being looked at.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qcdde60e795",
  "text": "Ravi Anand raised case CASE-6137 with Pembroke Travel about family visit. The matter is formal in style and set out in brief. Details follow in the internal file.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qe122079bdc",
  "text": "name: Aiko Brandt\ncompany: Lindenfeld Outfitters\ncase: CASE-3927\nAiko Brandt is somewhat exasperated but polite, having raised a case with Lindenfeld Outfitters about the language course. The full background follows.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q9b0ece3701",
  "text": "Client visit case for Malik Osei\nMalik Osei raised case CASE-8061 with Lindenfeld Outfitters about a news subscription. A touch of frustration shows, but the wording is courteous throughout.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qbee3baf077",
  "text": "Dear team,\nI write to raise a formal case with Corran Telecom about my study block. My name is Kofi Mensah and the case identifier is CASE-4412. I appreciate your attention, and the details are set out below.\nYours sincerely,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q8dfd61d250",
  "text": "Short case-file entry: Nadia Kowal raised case CASE-2886 with Upland Utilities about a card account. Drafted in a formal, concise style, with the details to come below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q65425a6fd1",
  "text": "Concern about language course for Jonas Feld, CASE-2409\nJonas Feld raised a case with Tamsin Fitness about a language course, and the background follows. The customer sounds mildly irritated yet keeps a civil and measured tone throughout.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q8f1939c07e",
  "text": "Safety boot case for Mira Castell\nMira Castell raised case CASE-1505 with Pembroke Travel about an antivirus licence. We are glad to share the background, and the full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q0bd9b72e0f",
  "text": "Internal case note: Ravi Anand raised a case with Veridia Health about a tyre order, and it is held under CASE-8798. The tone of the message has stayed steady and the background follows.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q24443b43c2",
  "text": "File entry, formal in style: Ravi Anand raised case CASE-2261 with Mistral Home about a merchant account. Summarised briefly, with the case details to follow in full.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qb18a17fa3c",
  "text": "Dear team,\nI write to raise a formal case with Mistral Home about my savings account. My name is Ana Ruiz and the case identifier is CASE-7148. I appreciate your attention, and the details are set out below.\nYours sincerely,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q546223447b",
  "text": "Nadia Kowal: Hi there, I am calling about my camera bag. I raised a case with Veridia Health and I wanted to say thank you for taking it on.\nagent: Hello there, so good to speak with you. I have case CASE-4270 on file, so let us go through the camera bag together.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q7eef720c4b",
  "text": "Ravi Anand: I am calling about a design suite with Tamsin Fitness and I would like to be heard, though I do appreciate your help.\nagent: I am sorry it has been a bother, thank you for your patience, and I have your case CASE-8185 in front of me.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q0f255e1bad",
  "text": "Customer case CASE-7838 for Priya Raman\nPriya Raman is a warm, chatty sort who has raised a case with Mistral Home about the language course. The case details are laid out below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qbf13322320",
  "text": "Formal record: Ines Duarte raised case CASE-5102 with Selkirk Logistics about a summer trip. Matter recorded briefly for internal use. Full details follow in the case file.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qa63ba88d8a",
  "text": "Hello,\nMy name is Lena Whitcombe and I am writing to raise a case with Redfern Bank about my language course. The case is logged under CASE-3157 and the history follows in the sections below.\nKind regards",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q4b7e192473",
  "text": "Internal record: CASE-5314 concerns a card account that Hana Sato raised with Pembroke Travel. Things feel calm and the matter is routine. Background and details follow below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q42cfd82779",
  "text": "case: CASE-1356\ncustomer: Tomas Lindqvist\nitem: support transcript\nThe customer kindly raised a case with Selkirk Logistics about the support transcript, and the details follow. The tone of the message is upbeat and cheerful throughout.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q447ff0b72a",
  "text": "Hi there,\nI am reaching out about my standing desk with Halvard Insurance, which is a calm and routine matter. My name is Yara Haddad and the case is logged as CASE-1739. The rest follows in the notes below.\nThanks,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q4118b0d979",
  "text": "name: Mira Castell\ncompany: Redfern Bank\ncase: CASE-2469\nMira Castell is a cheerful customer who wrote in to raise a case with Redfern Bank about the customer file.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qf3b8646cd7",
  "text": "case: CASE-8982\ncontact: Lena Whitcombe\nitem: family visit\nA polite but slightly irritated case was raised with Tamsin Fitness about the family visit. The details follow in the usual way.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qbaf35e4352",
  "text": "Routine matter logged for internal use. Ines Duarte raised case CASE-4473 with Quayside Software about a news subscription. The mood is calm, and the case details follow below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q52fb6aea94",
  "text": "Yara Haddad: Hello. I am calling about my annual plan. I raised a case with Quayside Software and I am slightly irritated, but I would like a clear answer.\nagent: Hello. I have case CASE-3992 on file, so let us look at the annual plan details.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q5e755e8a5f",
  "text": "customer: Eva Marsh\norganisation: Veridia Health\ncase: CASE-2355\nEva Marsh raised this case about the savings account. A friendly hello from the team, and the details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qc4e5bde2bc",
  "text": "customer: Ines Duarte\norganisation: Lindenfeld Outfitters\ncase: CASE-4088\nInes Duarte raised this case about the standing desk. A friendly hello from the team, and the details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qc788ad259b",
  "text": "Dear team,\nI write to raise a formal case with Pembroke Travel about my annual plan. My name is Priya Raman and the case identifier is CASE-2091. I appreciate your attention, and the details are set out below.\nYours sincerely,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q5811a1175c",
  "text": "Query about merchant account from Dana Okafor, case CASE-7284\nDana Okafor raised this case with Mistral Home about a merchant account, and the details follow. The customer feels a little frustrated but remains polite and patient, and the case summary is set out below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qdb71c75949",
  "text": "Coffee grinder case from Aiko Brandt\nAiko Brandt raised a case with Veridia Health about a laptop, filed as CASE-8818. The details are shared here in a warm, plain way, with the background set out for the reader.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the case is raised with, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 }
]
