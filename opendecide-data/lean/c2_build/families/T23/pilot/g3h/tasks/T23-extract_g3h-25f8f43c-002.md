# G3-H extraction T23-extract_g3h-25f8f43c-002 (family T23)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T23/pilot/g3h/answers/T23-extract_g3h-25f8f43c-002.json

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
  "qid": "q10a7411b70",
  "text": "Hello,\nMy name is Theo Kalnins and I am writing to raise a case with Corran Telecom about my standing desk. The history and case details follow below, filed as CASE-8426.\nThanks,",
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
  "qid": "q33e9f3621f",
  "text": "Ana Ruiz: Hello, I am calling about case CASE-1152 with Pembroke Travel. It concerns my photo editor.\nagent: Hello Ana Ruiz, thank you for calling. Lovely to hear from you, and the full details follow.",
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
  "qid": "q9eb7ed79fd",
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
  "qid": "q9555b254f9",
  "text": "Short case-file entry: Nadia Kowal raised case CASE-9397 with Mistral Home about a meal kit plan. Drafted in a formal, concise style, with the details to come below.",
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
  "qid": "qc75feeca25",
  "text": "Dana Okafor: Hi, I am writing to raise a case with Upland Utilities about the language course.\nsupport: Hello. The case is logged under CASE-9857 and the usual details follow.\nDana Okafor: Thanks, that is everything for this call.",
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
  "qid": "q8be060437a",
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
  "qid": "q68992afe6a",
  "text": "Ines Duarte raised case CASE-9043 with Pembroke Travel about a printer toner. The case is calm and routine. Background is filed below, along with the rest of the details.",
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
  "qid": "q1877e51da0",
  "text": "Internal case note: Jonas Feld lodged a formal case with Pembroke Travel about a customer file. The matter is recorded under CASE-9566 and set out briefly. Background information is laid out below in a tidy and compact form.",
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
  "qid": "q91e89cbf02",
  "text": "Annual plan case, Mira Castell\nMira Castell raised case CASE-7699 with Halvard Insurance about an printer toner. Some mild grumbling is there, but the manner is civil and the details follow.",
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
  "qid": "qeb0a9c7f58",
  "text": "Theo Kalnins: Hello, I am calling about case CASE-6381 with Quayside Software. I am a bit irritated about my notes app, though I am staying calm.\nagent: Hello Theo Kalnins, thank you for calling. I hear the concern, and the full details follow.",
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
  "qid": "qf5d6ce1bc5",
  "text": "name: Nadia Kowal\ncompany: Brightwell Supply\ncase: CASE-1177\nNadia Kowal is a bit peeved but courteous. He has raised a case with Brightwell Supply about the conference trip, and the details follow.",
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
  "qid": "q3986521ba1",
  "text": "Priya Raman: Hello, I am calling about my merchant account. I raised a case with Selkirk Logistics and I would like to go over the details.\nagent: Thanks for calling. I have case CASE-8859 on file, so let us go through what happened.",
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
  "qid": "q928cc04e65",
  "text": "Lucas Brenner: Hello, I am writing to raise a case with Brightwell Supply about the standing desk.\nsupport: Hello. Your case is logged under CASE-1422 and the details follow.\nLucas Brenner: Thank you.",
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
  "qid": "q4727dd0b00",
  "text": "Aiko Brandt: Hello. I am calling about my summer trip. I raised a case with Corran Telecom and I am slightly irritated, but I would like a clear answer.\nagent: Hello. I have case CASE-4616 on file, so let us look at the summer trip details.",
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
  "qid": "q6e37674518",
  "text": "Theo Kalnins: I am calling about a support transcript with Quayside Software and it is rather irritating, though I am polite about it.\nagent: I hear you, and I apologise for the trouble. Your case CASE-3936 is in front of me and the support transcript details are being looked at.",
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
  "qid": "q2cc26df0fa",
  "text": "Owen Pryce: Hello. I am calling about my merchant account. I raised a case with Upland Utilities and I am slightly irritated, but I would like a clear answer.\nagent: Hello. I have case CASE-5798 on file, so let us look at the merchant account details.",
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
  "qid": "q4b6345aa82",
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
  "qid": "q487c50e779",
  "text": "Owen Pryce: Hello, I am phoning to raise a case with Upland Utilities about a customer file. I am so pleased to be talking with you.\nagent: Hello, thank you for phoning. Your case is logged under CASE-1441 and the full picture follows.",
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
  "qid": "q789291bce1",
  "text": "Lucas Brenner: Hello, I am writing to raise a case with Lindenfeld Outfitters about my safety boot.\nsupport: Thank you for writing. The case sits under CASE-9576 with its full details.",
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
  "qid": "q6877597b87",
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
  "qid": "q73dfbbcce1",
  "text": "Internal record: CASE-5648 concerns a streaming plan that Priya Raman raised with Upland Utilities. Things feel calm and the matter is routine. Background and details follow below.",
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
  "qid": "qdf528e1c09",
  "text": "Internal case note: Lena Whitcombe formally raised a case with Mistral Home about an printer toner. The record sits under CASE-6511, and the summary is kept brief and to the point. Background follows in a concise form.",
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
  "qid": "q51b5db4ca1",
  "text": "Ines Duarte: Hello, I am writing to raise a case with Veridia Health about current account.\nsupport: Hello. Your matter is recorded as CASE-8507 and the full details are set out in order.",
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
  "qid": "q12958dd330",
  "text": "Lena Whitcombe: Hello, I am writing about my house move. I raised a case with Halvard Insurance and I would like to walk through it.\nsupport: Hello. Case CASE-7606 is on file, and the house move details follow.",
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
  "qid": "q486d49bb68",
  "text": "Ravi Anand: Hello there, I am calling to raise a case about my language course with Mistral Home.\nagent: Hello, glad you called. I have your case in front of me under CASE-4711.\nRavi Anand: Thank you for taking the call.",
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
  "qid": "q6828c24ab5",
  "text": "Sara Ilves: Hello, it is lovely to speak with you. I am calling to raise a case with Redfern Bank about my notes app.\nagent: Hello, thank you for calling. Your case, CASE-4087, is right here on my screen.",
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
  "qid": "q9271cb78a2",
  "text": "Hello,\nKofi Mensah here. I am writing to raise a case with Halvard Insurance about my team offsite, which is logged under CASE-5661. The history and case details follow.\nYours sincerely",
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
  "qid": "q42df4d2baf",
  "text": "Mira Castell has raised a case with Veridia Health about a cable reel, filed as CASE-9551. The background and details of the matter follow in this file. Matters of this kind are set out formally and briefly.",
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
  "qid": "q12076059fd",
  "text": "Hana Sato: Hello, I am writing to raise a case with Selkirk Logistics about my savings account.\nsupport: Hello and thank you. The case sits under CASE-7455 and the full record follows.",
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
  "qid": "q8a828cb536",
  "text": "Hello,\nThis is Theo Kalnins. I am writing to raise a case with Selkirk Logistics about the family visit. The case is logged under CASE-6600 and the history follows below.\nYours faithfully",
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
  "qid": "qc2377104e2",
  "text": "Hello,\nNadia Kowal here. I am writing to raise a case with Tamsin Fitness about my grocery order. The case is filed under CASE-2849 and the history follows.\nSincerely",
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
  "qid": "q64c066532a",
  "text": "Internal case note: Ravi Anand raised a calm and routine case with Redfern Bank about a merchant account, and the case is logged under CASE-4702. The entry is standard and the tone is steady throughout. The background and the case details follow in the usual format.",
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
  "qid": "qc0f0b22424",
  "text": "Mira Castell: Hi there, thanks for picking up. I am calling about my tyre order and I raised a case with Halvard Insurance, which I am happy to talk through.\nagent: Hello there, lovely to hear from you. I have case CASE-1981 on file, so let us go through the tyre order together.",
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
  "qid": "qc07e24415e",
  "text": "Hi there,\nI am reaching out about my conference trip with Halvard Insurance, which is a calm and routine matter. My name is Ravi Anand and the case is logged as CASE-2406. The rest follows in the notes below.\nThanks,",
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
  "qid": "q1d9574b210",
  "text": "Yara Haddad: Hello, I am writing about my gym membership. I raised a case with Redfern Bank and I would like to walk through it.\nsupport: Hello. Case CASE-9894 is on file, and the gym membership details follow.",
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
  "qid": "q9c5b4d6c29",
  "text": "Nadia Kowal: Hello, I wish to make a formal note about my antivirus licence from Lindenfeld Outfitters.\nsupport: Hello. The case CASE-8329 has been filed and the antivirus licence background is being gathered.",
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
  "qid": "qe427333a23",
  "text": "Hello,\nMy name is Lucas Brenner and I am writing to raise a case with Quayside Software about my laptop. The matter is calm and routine, and the case is filed as CASE-4150. The details follow below.\nTake care,",
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
  "qid": "qabbd457243",
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
  "qid": "q6fd627dde6",
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
  "qid": "qb33151465e",
  "text": "Nadia Kowal: Hello, I would like to put a formal matter on record with Selkirk Logistics about my notes app.\nsupport: Thank you for getting in touch. CASE-9236 is logged and the background to the notes app follows.",
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
  "qid": "q123df1254c",
  "text": "Lucas Brenner: Hello, I am writing to raise a case with Lindenfeld Outfitters about my safety boot.\nsupport: Thank you for writing. The case sits under CASE-9576 with its full details.",
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
  "qid": "q3aca2b0f8c",
  "text": "Nadia Kowal: I am ringing about my payroll record from Upland Utilities, and I am a little cross, though I do appreciate your help.\nagent: I understand the frustration and thank you for bearing with me, and your case CASE-4273 is in front of me.",
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
  "qid": "qf0f79046a8",
  "text": "Mira Castell: Hello, I am calling about case CASE-4048 with Corran Telecom. I have a concern about my gym membership, but I want to stay polite.\nagent: Hello Mira Castell, thank you for calling. I hear your concern, and the full details follow.",
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
  "qid": "q24bbe319a6",
  "text": "Sara Ilves: Hello, it is lovely to speak with you. I am calling to raise a case with Redfern Bank about my notes app.\nagent: Hello, thank you for calling. Your case, CASE-4087, is right here on my screen.",
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
  "qid": "q2a69414228",
  "text": "Aiko Brandt: Hello, I am writing to raise a matter about my e-bike with Veridia Health.\nsupport: Thank you for your message. Your case CASE-3548 is open and the e-bike details follow.",
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
  "qid": "qb05b095526",
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
  "qid": "q09b78878c0",
  "text": "Internal case note: Priya Raman raised a calm and routine case with Selkirk Logistics about a current account, and the case is logged under CASE-9077. The entry is standard and the tone is steady throughout. The background and the case details follow in the usual format.",
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
  "qid": "qee041e7957",
  "text": "Internal case note: Tomas Lindqvist raised a calm and routine case with Veridia Health about a camera recording, and the case is logged under CASE-5451. The entry is standard and the tone is steady throughout. The background and the case details follow in the usual format.",
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
  "qid": "qeb60a5600a",
  "text": "Dear team,\nMy name is Tomas Lindqvist and I am writing to raise a case with Corran Telecom about my conference trip. The background and details follow below, filed as CASE-6825. Thank you for reading.\nYours faithfully,",
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
  "qid": "q1812a1e41c",
  "text": "Kofi Mensah: Hello, I am writing to raise a case with Redfern Bank about the design suite.\nsupport: Hello. Your case is logged under CASE-9134 and the details follow.\nKofi Mensah: Thank you.",
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
