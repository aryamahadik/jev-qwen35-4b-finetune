# G3-H extraction T23-extract_g3h-7d2d7b6c-001 (family T23)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T23/pilot_i1/g3h/answers/T23-extract_g3h-7d2d7b6c-001.json

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
  "qid": "qa245be42cc",
  "text": "Formal record: Ines Duarte raised case CASE-3432 with Selkirk Logistics about an washing machine. Matter recorded briefly for internal use. Full details follow in the case file.",
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
  "qid": "qe100ed57d0",
  "text": "Mild frustration over conference trip for Ana Ruiz, CASE-7806\nAna Ruiz raised a polite case with Lindenfeld Outfitters about a conference trip, and the details follow. The customer is a little annoyed but remains courteous while the matter is discussed.",
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
  "qid": "q71384d1c22",
  "text": "Hello team,\nI am writing to raise a case with Mistral Home about my office chair. My name is Ines Duarte and the case identifier is CASE-5945. I trust the matter is in careful hands and the details follow.\nRegards,",
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
  "qid": "q9f5150a081",
  "text": "Customer case CASE-4385 for Owen Pryce\nOwen Pryce is a little put out, but polite, having raised a case with Upland Utilities about the photo editor. The full history of the matter sits below.",
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
  "qid": "qa368d032ed",
  "text": "Internal summary for the file. Ines Duarte raised case CASE-4636 with Halvard Insurance about a house move. It is a brief, formal matter and details follow.",
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
  "qid": "q24ea7dd0c5",
  "text": "Client visit case for Owen Pryce\nOwen Pryce raised case CASE-4485 with Tamsin Fitness about a e-bike. A touch of frustration shows, but the wording is courteous throughout.",
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
  "qid": "q0c205ed72e",
  "text": "Aiko Brandt: Hello, I am writing to raise a case with Upland Utilities about my savings account.\nsupport: Hello. The case sits under CASE-9676 with the routine notes beside it.\nAiko Brandt: Thanks, that covers it.",
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
  "qid": "qd24d80f20b",
  "text": "Hello team,\nI am writing to raise a case with Mistral Home about my office chair. My name is Ines Duarte and the case identifier is CASE-5945. I trust the matter is in careful hands and the details follow.\nRegards,",
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
  "qid": "q77b3679e7b",
  "text": "Customer file case raised by Lena Whitcombe\nLena Whitcombe raised a case with Quayside Software about the coffee grinder, filed as CASE-3402. The matter is a little frustrating, and the background is set out below for the team.",
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
  "qid": "q6123d14fbb",
  "text": "case: CASE-9307\ncustomer: Ines Duarte\nitem: washing machine\nI raised this case with Lindenfeld Outfitters about the washing machine, and the history follows below. I would appreciate a clear reply.",
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
  "qid": "q33dca604f5",
  "text": "Customer file case raised by Mira Castell\nMira Castell raised a case with Upland Utilities about the design suite, filed as CASE-1447. The matter is a little frustrating, and the background is set out below for the team.",
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
  "qid": "qaa4ecf1839",
  "text": "case: CASE-6825\ncontact: Tomas Lindqvist\nitem: conference trip\nThe customer has reached out to Corran Telecom about the conference trip, and the details follow. The tone is friendly and the conversation feels pleasant.",
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
  "qid": "q870c5c5721",
  "text": "Hello,\nAna Ruiz here. I am writing to raise a case with Brightwell Supply about my language course. The case is filed under CASE-4558 and the history follows.\nSincerely",
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
  "qid": "q1655152856",
  "text": "Internal summary for the file. Ines Duarte raised case CASE-4636 with Halvard Insurance about a house move. It is a brief, formal matter and details follow.",
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
  "qid": "q44187967d1",
  "text": "Hello Kofi Mensah,\nYour case CASE-4159 with Quayside Software concerns a standing desk that you raised. This is a calm, routine matter and the full details follow.\nBest wishes",
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
  "qid": "q1d3e6504ca",
  "text": "Nadia Kowal: Hi there, I raised case CASE-8424 with Quayside Software about my client visit.\nsupport: Hello Nadia Kowal, thanks for getting in touch. This is a routine matter and the full details follow.",
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
  "qid": "qf4d0eaef17",
  "text": "Client visit case for Owen Pryce\nOwen Pryce raised case CASE-4485 with Tamsin Fitness about a e-bike. A touch of frustration shows, but the wording is courteous throughout.",
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
  "qid": "qad4531cced",
  "text": "Mild frustration over conference trip for Ana Ruiz, CASE-7806\nAna Ruiz raised a polite case with Lindenfeld Outfitters about a conference trip, and the details follow. The customer is a little annoyed but remains courteous while the matter is discussed.",
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
  "qid": "q91fdf8ef4f",
  "text": "Friendly query on office chair for Eva Marsh, CASE-5955\nEva Marsh reached out to Pembroke Travel about a office chair in a warm and friendly way, and the background follows. The conversation is pleasant and the case details are set out below.",
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
  "qid": "q55d3272c95",
  "text": "Routine matter logged for internal use. Eva Marsh raised case CASE-5511 with Veridia Health about a team offsite. The mood is calm, and the case details follow below.",
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
  "qid": "q1aeb80a204",
  "text": "Routine matter logged for internal use. Eva Marsh raised case CASE-5511 with Veridia Health about a team offsite. The mood is calm, and the case details follow below.",
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
  "qid": "q6f3daabcb7",
  "text": "Mira Castell has raised a case with Upland Utilities about a safety boot. The case carries the label CASE-3146. Everything about the matter is routine, and the history follows in full.",
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
  "qid": "q577309e737",
  "text": "Customer case CASE-8234 for Ravi Anand\nRavi Anand has very kindly raised a case with Mistral Home about the grocery order. Everything relevant is set out below, with the story told in order.",
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
  "qid": "qd18207688c",
  "text": "Dear sir or madam,\nI am Dana Okafor and I am writing to raise a case with Lindenfeld Outfitters about my client visit. The background and details follow below, filed as CASE-8628.\nWith thanks,",
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
  "qid": "q5b69803df3",
  "text": "Aiko Brandt: Hello, I wish to make a formal note about my site audit from Upland Utilities.\nsupport: Hello. The case CASE-4212 has been filed and the site audit background is being gathered.",
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
  "qid": "qa01cbe4f9e",
  "text": "Mira Castell raised a case with Mistral Home about an grocery order. The case is filed as CASE-8692. The history of the case and its details follow in full.",
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
  "qid": "q3c288c4bb6",
  "text": "Friendly query on standing desk for Ravi Anand, CASE-6928\nRavi Anand reached out to Tamsin Fitness about a standing desk in a warm and friendly way, and the background follows. The conversation is pleasant and the case details are set out below.",
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
  "qid": "q4616ac543b",
  "text": "customer: Sara Ilves\norganisation: Tamsin Fitness\ncase: CASE-6846\nSara Ilves raised a ticket with Tamsin Fitness about the customer file, and the details are set out below.",
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
  "qid": "q80175ae6a5",
  "text": "Hello,\nTheo Kalnins here. I am writing to raise a case with Lindenfeld Outfitters about my summer trip, which is logged under CASE-3674. The history and case details follow.\nYours sincerely",
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
  "qid": "q5e2f803b3d",
  "text": "Customer case CASE-1837 for Ines Duarte\nInes Duarte is a delight to deal with and has raised a case with Redfern Bank about the language course. The case is logged under CASE-1837 and the details are set out below.",
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
  "qid": "q43a9d63198",
  "text": "Ana Ruiz: Hello. I am writing about my news subscription and I raised a case with Corran Telecom about it.\nsupport: Hello. I have case CASE-5708 on file, and the news subscription details are set out below.",
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
  "qid": "qcb75fd52bc",
  "text": "customer: Ines Duarte\ncompany: Pembroke Travel\ncase: CASE-8043\nInes Duarte is a little irritated but polite and has raised a case with Pembroke Travel about the printer order.",
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
  "qid": "qd9b1e8da9e",
  "text": "Theo Kalnins: Hello, I am writing to raise a case with Brightwell Supply about my e-bike.\nsupport: Hello, thank you for writing. This is routine, and your case is logged under CASE-5261.",
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
  "qid": "q14d6d00425",
  "text": "Jonas Feld: Hello, I am writing to raise a matter about my design suite with Lindenfeld Outfitters.\nsupport: Thank you for your message. Your case CASE-5838 is open and the design suite details follow.",
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
  "qid": "q01f935ed13",
  "text": "Internal case note: Yara Haddad raised a calm and routine case with Halvard Insurance about a photo editor, and the case is logged under CASE-2857. The entry is standard and the tone is steady throughout. The background and the case details follow in the usual format.",
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
  "qid": "q47d72cdd5d",
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
  "qid": "q9748de78dd",
  "text": "case: CASE-8464\ncontact: Lucas Brenner\nitem: printer toner\nThe customer is slightly put out but remains courteous, and wrote to Lindenfeld Outfitters about the printer toner. Background and the case details follow.",
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
  "qid": "q1c7a9d548c",
  "text": "Aiko Brandt: Hello, I hope things are well. I am calling about my site audit with Tamsin Fitness and I would love a warm and friendly chat.\nagent: Hello, it is so good to speak with you. Your case CASE-6278 is open and I would be delighted to help with the site audit.",
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
  "qid": "qcdaef08e7b",
  "text": "Aiko Brandt has raised a case with Upland Utilities about a laptop, filed as CASE-8033. The background and details follow below. This is kept brief and formal for the file.",
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
  "qid": "q79ae5cc978",
  "text": "Sara Ilves: Hello. I am writing about my safety boot and I raised a case with Quayside Software about it.\nsupport: Hello. I have case CASE-5263 on file, and the safety boot details are set out below.",
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
  "qid": "q2e85f21895",
  "text": "Malik Osei: Hello, it is lovely to speak with you. I am calling to raise a case with Corran Telecom about my standing desk.\nagent: Hello, thank you for calling. Your case, CASE-6312, is right here on my screen.",
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
  "qid": "q668f59de3e",
  "text": "Hana Sato: Hello, I hope you are all doing well! I am calling about my antivirus licence from Quayside Software and I am feeling upbeat.\nagent: Lovely to hear from you! I have your case CASE-3825 up and I am happy to look into the antivirus licence with you.",
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
  "qid": "q18ef8f53ee",
  "text": "case: CASE-7992\ncustomer: Yara Haddad\nitem: e-bike\nThe customer wrote to Mistral Home about the e-bike in a bright and upbeat way. All involved are pleased to take the matter forward.",
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
  "qid": "q1c7c70b36c",
  "text": "Coffee grinder case from Dana Okafor\nDana Okafor raised a case with Mistral Home about a payroll record, filed as CASE-5022. The details are shared here in a warm, plain way, with the background set out for the reader.",
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
