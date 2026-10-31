# G3-H extraction T23-extract_g3h-25f8f43c-005 (family T23)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T23/pilot/g3h/answers/T23-extract_g3h-25f8f43c-005.json

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
  "qid": "q0ff6d44d9a",
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
  "qid": "q848e7752d5",
  "text": "Dear Lucas Brenner,\nYour case CASE-5404 concerning an client visit was raised with Mistral Home. The matter is summarised here briefly and the details follow.\nYours faithfully",
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
  "qid": "qb021b6a575",
  "text": "case: CASE-5296\ncustomer: Aiko Brandt\nitem: notes app\nI raised this case with Selkirk Logistics about the notes app, and the history follows below. I would appreciate a clear reply.",
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
  "qid": "q0d080f291e",
  "text": "Sara Ilves: Hello, I am calling about case CASE-8728 with Mistral Home. I am a bit irritated about my house move, though I am staying calm.\nagent: Hello Sara Ilves, thank you for calling. I hear the concern, and the full details follow.",
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
  "qid": "q27692905be",
  "text": "Theo Kalnins: Hello. I am writing about my washing machine. I raised a case with Veridia Health and I would like to talk the details over.\nsupport: Hello. I have case CASE-6535 on file and the washing machine details follow.",
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
  "qid": "q0ac8ae5ee8",
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
  "qid": "qb2ba24fd5d",
  "text": "case: CASE-2881\ncustomer: Dana Okafor\nitem: camera recording\nI raised this case with Quayside Software about the camera recording, and the history follows below. I would appreciate a clear reply.",
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
  "qid": "qe7e88fa45e",
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
  "qid": "q40e7e25afa",
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
  "qid": "q1d08561fcd",
  "text": "Dear colleagues,\nI am writing to raise a matter with Upland Utilities about my camera recording. My name is Malik Osei and the case is logged as CASE-5911. I appreciate your attention to the details that follow.\nYours faithfully,",
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
  "qid": "q8c835c729c",
  "text": "Ana Ruiz: Hello there, I am getting in touch about a study block from Selkirk Logistics. It is a routine matter and I am calm about it.\nsupport: Hello, thank you for reaching out. Your case CASE-7042 is logged and the study block details follow.",
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
  "qid": "q85124f5aa1",
  "text": "Mira Castell: Hello, I am phoning to raise a case with Upland Utilities about a camera recording. I am so pleased to be talking with you.\nagent: Hello, thank you for phoning. Your case is logged under CASE-7896 and the full picture follows.",
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
  "qid": "q793828623b",
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
  "qid": "q1ba564f0c3",
  "text": "Aiko Brandt: Hi there, thanks for picking up. I am calling about my customer file and I raised a case with Quayside Software, which I am happy to talk through.\nagent: Hello there, lovely to hear from you. I have case CASE-7021 on file, so let us go through the customer file together.",
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
  "qid": "qf9668e3ec5",
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
  "qid": "q31c4e52435",
  "text": "Lena Whitcombe: Hello. I am writing about my standing desk. I raised a case with Quayside Software and I would like to talk the details over.\nsupport: Hello. I have case CASE-3296 on file and the standing desk details follow.",
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
  "qid": "q13a3286dfb",
  "text": "Gym membership case for Theo Kalnins\nTheo Kalnins raised case CASE-7727 with Tamsin Fitness about a savings account. The customer is a little frustrated but polite, and the details follow.",
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
  "qid": "qab7d48df63",
  "text": "Customer case CASE-7055 for Nadia Kowal\nNadia Kowal is a little put out, but polite, having raised a case with Upland Utilities about the support transcript. The full history of the matter sits below.",
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
  "qid": "q62669e287f",
  "text": "customer: Ravi Anand\norganisation: Mistral Home\ncase: CASE-8234\nRavi Anand raised this case about a grocery order. The customer is mildly irritated but courteous, and the full details follow.",
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
  "qid": "qd69b183ca4",
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
  "qid": "q569046f2d1",
  "text": "Lena Whitcombe: Hello, I am writing to raise a case with Upland Utilities about my camera bag.\nsupport: Hello. The case is logged under CASE-7063.\nLena Whitcombe: Thank you, that is clear.",
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
  "qid": "q9008102b28",
  "text": "Routine matter logged for internal use. Ravi Anand raised case CASE-2753 with Lindenfeld Outfitters about a news subscription. The mood is calm, and the case details follow below.",
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
  "qid": "q36d3a7a6b8",
  "text": "name: Ravi Anand\ncompany: Veridia Health\ncase: CASE-4688\nRavi Anand is mildly vexed but civil, and has raised a case with Veridia Health about the grocery order.",
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
  "qid": "q21447a6ba1",
  "text": "Dear Lena Whitcombe,\nYour case CASE-8312 concerning an customer file was raised with Mistral Home. The matter is summarised here briefly and the details follow.\nYours faithfully",
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
  "qid": "qb3394bee13",
  "text": "Dear colleagues,\nI am writing to raise a matter with Tamsin Fitness about my site audit. My name is Ravi Anand and the case is logged as CASE-6777. I appreciate your attention to the details that follow.\nYours faithfully,",
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
  "qid": "qb848f351ab",
  "text": "Jonas Feld: Hello. I am calling about my merchant account. I raised a case with Corran Telecom and I would like to talk the matter over.\nagent: Hello. I have case CASE-6938 on file, and the merchant account details are in front of me.",
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
  "qid": "q372dd032fe",
  "text": "Ana Ruiz: Hello. I raised a case with Redfern Bank about my site audit, and I would like it looked into.\nsupport: Hello. I have case CASE-6488 on file and the site audit details follow.",
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
  "qid": "q033f7cfbd8",
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
  "qid": "qc1dd80950d",
  "text": "case: CASE-5727\ncustomer: Aiko Brandt\nitem: house move\nAiko Brandt raised a case with Pembroke Travel about an house move, and the history and details follow. Thanks for reading it through.",
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
  "qid": "qee240276de",
  "text": "Ravi Anand: Hello. I am calling about my e-bike. I raised a case with Mistral Home and I would like to talk the matter over.\nagent: Hello. I have case CASE-2298 on file, and the e-bike details are in front of me.",
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
  "qid": "qdc484e0ead",
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
  "qid": "q99cd6cfe4f",
  "text": "Ana Ruiz: Hello. I raised a case with Redfern Bank about my site audit, and I would like it looked into.\nsupport: Hello. I have case CASE-6488 on file and the site audit details follow.",
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
  "qid": "qd7c0eadcd8",
  "text": "Customer case CASE-6643 for Nadia Kowal\nNadia Kowal has very kindly raised a case with Lindenfeld Outfitters about the tyre order. Everything relevant is set out below, with the story told in order.",
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
  "qid": "q49eaaccd24",
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
  "qid": "q2b1cf80899",
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
  "qid": "qef3c96073e",
  "text": "Hello Eva Marsh,\nYour case CASE-7928 with Pembroke Travel concerns a safety boot that you raised. This is a calm, routine matter and the full details follow.\nBest wishes",
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
  "qid": "q87b657049e",
  "text": "Hello there,\nMy name is Kofi Mensah and I am writing about a language course from Veridia Health. It is a routine matter and I am keen to keep things calm. The case is logged as CASE-5115 and the background follows.\nBest wishes,",
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
  "qid": "qfcdb551bfe",
  "text": "Malik Osei: Hello, it is lovely to speak with you. I am calling to raise a case with Redfern Bank about my sofa order.\nagent: Hello, thank you for calling. Your case, CASE-4944, is right here on my screen.",
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
  "qid": "q4b88f58fb1",
  "text": "Owen Pryce: Hello, I hope you are all doing well! I am calling about my camera bag from Quayside Software and I am feeling upbeat.\nagent: Lovely to hear from you! I have your case CASE-2531 up and I am happy to look into the camera bag with you.",
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
  "qid": "q56ef400f64",
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
  "qid": "qd67b3adde9",
  "text": "Hello Eva Marsh,\nYour case CASE-7928 with Pembroke Travel concerns a safety boot that you raised. This is a calm, routine matter and the full details follow.\nBest wishes",
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
  "qid": "q8533963f54",
  "text": "Ravi Anand: Hello, I hope you are all doing well! I am calling about my summer trip from Mistral Home and I am feeling upbeat.\nagent: Lovely to hear from you! I have your case CASE-2218 up and I am happy to look into the summer trip with you.",
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
  "qid": "q9f757c300e",
  "text": "Dear support team,\nMy name is Theo Kalnins and I am writing to raise a case with Tamsin Fitness about my merchant account. The background and details follow below, filed as CASE-2404. I look forward to your reply.\nKind regards,",
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
  "qid": "q9931cabe18",
  "text": "Hello,\nJonas Feld here. I am writing to raise a case with Pembroke Travel about my notes app. The case is filed under CASE-5476 and the history follows.\nSincerely",
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
  "qid": "qa3add78543",
  "text": "Lena Whitcombe: Hello, I am writing about my support transcript. I raised a case with Lindenfeld Outfitters and I would like to walk through it.\nsupport: Hello. Case CASE-4106 is on file, and the support transcript details follow.",
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
  "qid": "q88b3c6c926",
  "text": "Hello,\nJonas Feld here. I am writing to raise a case with Pembroke Travel about my notes app. The case is filed under CASE-5476 and the history follows.\nSincerely",
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
  "qid": "q50d8f516d2",
  "text": "Hi team,\nMy name is Dana Okafor and I am writing to raise a case with Halvard Insurance about my language course. The background and details follow, filed under CASE-2670.\nRegards,",
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
  "qid": "q8e48f35388",
  "text": "Nadia Kowal: Hello, I am writing to raise a case with Tamsin Fitness about my grocery order.\nsupport: Hello, thank you for writing. This is routine, and your case is logged under CASE-4743.",
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
  "qid": "q90b4e3c4c9",
  "text": "Ravi Anand: Hello, I hope you are all doing well! I am calling about my summer trip from Mistral Home and I am feeling upbeat.\nagent: Lovely to hear from you! I have your case CASE-2218 up and I am happy to look into the summer trip with you.",
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
  "qid": "qee5e608e70",
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
 }
]
