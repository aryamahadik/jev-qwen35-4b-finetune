# G3-H extraction T23-extract_g3h-25f8f43c-001 (family T23)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T23/pilot/g3h/answers/T23-extract_g3h-25f8f43c-001.json

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
  "qid": "q487c590749",
  "text": "Dear support team,\nI am writing to raise a case with Corran Telecom about my family visit. My name is Mira Castell and the case is filed under CASE-4479. I appreciate your careful attention and the details follow.\nKind regards,",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q62516788f7",
  "text": "Lena Whitcombe: Hello, I am writing to raise a case with Corran Telecom about my cable reel.\nsupport: Hello. The case sits under CASE-7885 with the routine notes beside it.\nLena Whitcombe: Thanks, that covers it.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q222a3aacfa",
  "text": "name: Hana Sato\ncompany: Pembroke Travel\ncase: CASE-4368\nHana Sato is cheerful and easy to work with, having raised a case with Pembroke Travel about the house move, and the story is set out below.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q4c3deaccd6",
  "text": "Jonas Feld: Hello, I am writing to raise a case with Redfern Bank about my savings account.\nsupport: Hello, thank you for writing. This is routine, and your case is logged under CASE-1410.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q24ab410f90",
  "text": "Kofi Mensah: Hello, I am writing to raise a matter about my language course with Brightwell Supply.\nsupport: Thank you for your message. Your case CASE-7851 is open and the language course details follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qb20f1cd603",
  "text": "Dear support team,\nI am writing to raise a case with Pembroke Travel about my camera bag. My name is Lucas Brenner and the case is filed under CASE-6835. I appreciate your careful attention and the details follow.\nKind regards,",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qb68939947d",
  "text": "File entry, formal in style: Priya Raman raised case CASE-9077 with Selkirk Logistics about a current account. Summarised briefly, with the case details to follow in full.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q669d3cf409",
  "text": "Customer case CASE-9820 for Lena Whitcombe\nLena Whitcombe is a warm, chatty sort who has raised a case with Halvard Insurance about the e-bike. The case details are laid out below.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q812a2d72c2",
  "text": "Theo Kalnins raised a case with Lindenfeld Outfitters about the grocery order. The matter is recorded under CASE-2041. The case is routine and the history follows in order.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q82007f14ac",
  "text": "Hi team,\nMy name is Nadia Kowal and I am writing to raise a case with Selkirk Logistics about my notes app. The background and details follow, filed under CASE-6224.\nRegards,",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qc6ca799a7a",
  "text": "Eva Marsh: Hi there, I am calling about my photo editor. I raised a case with Tamsin Fitness and I wanted to say thank you for taking it on.\nagent: Hello there, so good to speak with you. I have case CASE-9012 on file, so let us go through the photo editor together.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q83c045bb16",
  "text": "Help with streaming plan for Tomas Lindqvist, case CASE-5781\nTomas Lindqvist raised a friendly case with Brightwell Supply about the streaming plan, and the details follow. The team is pleased to take a look and the conversation is off to a warm start.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qed961fac92",
  "text": "Jonas Feld: Hello. I am writing about my family visit. I raised a case with Corran Telecom and I would like to talk the details over.\nsupport: Hello. I have case CASE-2040 on file and the family visit details follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q6312dd9593",
  "text": "Priya Raman: Hello. I am writing about my coffee grinder. I raised a case with Upland Utilities about it.\nsupport: Hello. I have case CASE-8220 on file, and the coffee grinder details follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qe1fb3b0afc",
  "text": "case: CASE-4589\ncustomer: Nadia Kowal\nitem: laptop\nI raised this case with Upland Utilities about the laptop, and the history follows below. I would appreciate a clear reply.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q86563704df",
  "text": "Eva Marsh: Hello, I am writing to raise a case with Halvard Insurance about savings account.\nsupport: Hello. Your matter is recorded as CASE-2543 and the full details are set out in order.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q2f56d728fe",
  "text": "Lena Whitcombe: Hello. I raised a case with Halvard Insurance about my merchant account and I am writing to set out the matter.\nsupport: Hello. I have case CASE-3952 on file and the merchant account details follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q75a19e04fe",
  "text": "customer: Owen Pryce\ncompany: Mistral Home\ncase: CASE-7021\nOwen Pryce is a little irritated but polite and has raised a case with Mistral Home about the camera bag.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qfbef38c0d9",
  "text": "case: CASE-8248\ncustomer: Ravi Anand\nitem: support transcript\nThe customer politely raised a case with Selkirk Logistics about the support transcript, though mildly irritated. The details of the matter follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q967250ab61",
  "text": "case: CASE-6137\ncustomer: Yara Haddad\nitem: client visit\nThe customer warmly raised a case with Lindenfeld Outfitters about the client visit, and the details follow. It is a friendly start to the file.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q2f83896fb4",
  "text": "Hello team,\nI am writing to raise a case with Tamsin Fitness about my coffee grinder. My name is Priya Raman and the case identifier is CASE-4678. I trust the matter is in careful hands and the details follow.\nRegards,",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qf2e96f8d28",
  "text": "Customer case CASE-2538 for Jonas Feld\nJonas Feld is a delight to deal with and has raised a case with Pembroke Travel about the washing machine. The case is logged under CASE-2538 and the details are set out below.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q5d4ae24775",
  "text": "Dear Mira Castell,\nYour case CASE-6547 concerning an card account was raised with Selkirk Logistics. The matter is summarised here briefly and the details follow.\nYours faithfully",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q6cfe1e4af8",
  "text": "Jonas Feld: Hello, I am ringing about my coffee grinder with Corran Telecom, and I would love a friendly chat.\nagent: Hello and lovely to hear from you. I have your case CASE-8708 in front of me and I am glad to help with the coffee grinder.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qd46d412990",
  "text": "Streaming plan concern from Lucas Brenner\nLucas Brenner raised case CASE-2375 with Redfern Bank about a design suite. The mood is mildly frustrated but polite, and the details follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q38dcdef20d",
  "text": "Sara Ilves: Hello, I am calling to raise a case with Selkirk Logistics about my washing machine, and I am a little irritated but polite about it.\nagent: Thank you for calling. Your case is logged under CASE-3688 and the background is set out in full.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q32ca645157",
  "text": "Theo Kalnins: Hello, I am calling about my coffee grinder. I raised a case with Lindenfeld Outfitters and I would like to go over the details.\nagent: Thanks for calling. I have case CASE-7106 on file, so let us go through what happened.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q835700a8a4",
  "text": "customer: Nadia Kowal\norganisation: Mistral Home\ncase: CASE-7303\nNadia Kowal raised a ticket with Mistral Home about the standing desk, and the details are set out below.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qae8bb106d0",
  "text": "Dear support team,\nI am writing to raise a case with Corran Telecom about my family visit. My name is Mira Castell and the case is filed under CASE-4479. I appreciate your careful attention and the details follow.\nKind regards,",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q84e4180b54",
  "text": "Jonas Feld: Hello, I am writing to raise a case with Redfern Bank about my savings account.\nsupport: Hello, thank you for writing. This is routine, and your case is logged under CASE-1410.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qeefc1ddd50",
  "text": "Owen Pryce: Hello. I raised a case with Upland Utilities about my e-bike, and I would like the matter looked into.\nsupport: Hello. I have case CASE-4411 on file and the e-bike details follow in full.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qb83409d224",
  "text": "Mira Castell: Hello, I am writing to raise a case with Brightwell Supply about my conference trip.\nsupport: Hello. The case sits under CASE-7173 with the routine notes beside it.\nMira Castell: Thanks, that covers it.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q7b1b29699a",
  "text": "Ana Ruiz: Hello, I am calling about my antivirus licence. I raised a case with Brightwell Supply and I would like to go over the details.\nagent: Thanks for calling. I have case CASE-4051 on file, so let us go through what happened.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q481db5fe7f",
  "text": "customer: Lena Whitcombe\ncompany: Upland Utilities\ncase: CASE-4304\nLena Whitcombe is a little irritated but polite and has raised a case with Upland Utilities about the safety boot.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q9f5cfdac6c",
  "text": "Ravi Anand: Hello. I am writing about my family visit. I raised a case with Tamsin Fitness about it.\nsupport: Hello. I have case CASE-8910 on file, and the family visit details follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q52034f1a15",
  "text": "Eva Marsh: Hello there, I am getting in touch about a team offsite from Veridia Health. It is a routine matter and I am calm about it.\nsupport: Hello, thank you for reaching out. Your case CASE-5511 is logged and the team offsite details follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qbdb396a80c",
  "text": "Ravi Anand: Hello, I wish to make a formal note about my e-bike from Corran Telecom.\nsupport: Hello. The case CASE-6452 has been filed and the e-bike background is being gathered.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qf8904584d3",
  "text": "Jonas Feld: I am calling about a camera bag with Selkirk Logistics and I would like to be heard, though I do appreciate your help.\nagent: I am sorry it has been a bother, thank you for your patience, and I have your case CASE-4085 in front of me.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qbfe20625d3",
  "text": "File entry, formal in style: Eva Marsh raised case CASE-8899 with Halvard Insurance about a language course. Summarised briefly, with the case details to follow in full.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q6638b9aac8",
  "text": "Priya Raman: Hello there, I am getting in touch about a customer file from Tamsin Fitness. It is a routine matter and I am calm about it.\nsupport: Hello, thank you for reaching out. Your case CASE-2128 is logged and the customer file details follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q75562accca",
  "text": "Card account concern from Ravi Anand\nRavi Anand raised case CASE-4711 with Mistral Home about a language course. A little cross, though civil, and the details follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q5cdaa392ce",
  "text": "Malik Osei: Hello there, I am getting in touch about a streaming plan from Tamsin Fitness. It is a routine matter and I am calm about it.\nsupport: Hello, thank you for reaching out. Your case CASE-7306 is logged and the streaming plan details follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qc9a4306b16",
  "text": "customer: Kofi Mensah\norganisation: Halvard Insurance\ncase: CASE-5106\nKofi Mensah raised this case about the printer order. A friendly hello from the team, and the details follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qeaf64e1809",
  "text": "Dear team,\nI write to raise a formal case with Pembroke Travel about my current account. My name is Owen Pryce and the case identifier is CASE-5422. I appreciate your attention, and the details are set out below.\nYours sincerely,",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qba5cc6f723",
  "text": "Owen Pryce: Hello, I am writing to raise a case with Veridia Health about my standing desk.\nsupport: Hello. This matter sits under CASE-8545 alongside the routine notes.\nOwen Pryce: Lovely, thank you.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q19cc32f37d",
  "text": "Customer case CASE-7868 for Hana Sato\nHana Sato has very kindly raised a case with Veridia Health about the current account. Everything relevant is set out below, with the story told in order.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qe568629051",
  "text": "customer: Theo Kalnins\norganisation: Upland Utilities\ncase: CASE-8361\nTheo Kalnins raised this case about a payroll record. There is mild annoyance here, though the customer remains polite, and the details follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q67b20d35c9",
  "text": "name: Ines Duarte\ncompany: Mistral Home\ncase: CASE-5945\nInes Duarte is glad to have raised a case with Mistral Home about the office chair, and the background is set out below.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "qa424fa9c29",
  "text": "customer: Nadia Kowal\norganisation: Mistral Home\ncase: CASE-7303\nNadia Kowal raised a ticket with Mistral Home about the standing desk, and the details are set out below.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 },
 {
  "qid": "q883bf347f5",
  "text": "Lucas Brenner: Hello, I am calling about case CASE-5860 with Mistral Home. I am a little frustrated about the notes app, though I am happy to explain.\nagent: Thank you for calling, Lucas Brenner. I appreciate your patience, and the full details follow.",
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
    "describe": "what the case is about, as written"
   },
   {
    "field": "case_id",
    "type": "id",
    "describe": "the case reference, as written"
   }
  ]
 }
]
