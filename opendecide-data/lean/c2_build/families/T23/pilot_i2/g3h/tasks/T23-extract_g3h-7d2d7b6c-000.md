# G3-H extraction T23-extract_g3h-7d2d7b6c-000 (family T23)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T23/pilot_i2/g3h/answers/T23-extract_g3h-7d2d7b6c-000.json

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
  "qid": "q699238e520",
  "text": "Annual plan case, Mira Castell\nMira Castell raised case CASE-7497 with Halvard Insurance about a camera bag. Some mild grumbling is there, but the manner is civil and the details follow.",
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
  "qid": "q7f80750db2",
  "text": "Internal summary for the file. Kofi Mensah raised case CASE-5454 with Redfern Bank about a current account. It is a brief, formal matter and details follow.",
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
  "qid": "q8102c9930b",
  "text": "Brief entry for the file: Lena Whitcombe raised case CASE-1728 with Selkirk Logistics about a printer toner. The register is formal, and the case details follow in full. Kept on file.",
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
  "qid": "qcd7caedf45",
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
  "qid": "q3e7708b6c6",
  "text": "Hana Sato has raised a case with Halvard Insurance about the camera bag. The matter appears as CASE-4396. The routine history and the case details follow below.",
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
  "qid": "q338d169e22",
  "text": "Lena Whitcombe raised a case with Upland Utilities about the streaming plan. The matter is recorded under CASE-4366. The case is routine and the history follows in order.",
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
  "qid": "qd3488fa455",
  "text": "Routine matter logged for internal use. Lena Whitcombe raised case CASE-4304 with Upland Utilities about a safety boot. The mood is calm, and the case details follow below.",
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
  "qid": "qf690e12044",
  "text": "Sara Ilves raised a case with Halvard Insurance about a laptop. The case is filed as CASE-5608. The history of the case and its details follow in full.",
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
  "qid": "q11776b9add",
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
  "qid": "q4265cbb9f8",
  "text": "case: CASE-6190\ncontact: Lucas Brenner\nitem: study block\nThe customer is slightly put out but remains courteous, and wrote to Halvard Insurance about the study block. Background and the case details follow.",
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
  "qid": "q06ce885b66",
  "text": "customer: Yara Haddad\ncase: CASE-5302\nitem: washing machine\nYara Haddad raised this case with Selkirk Logistics about the washing machine. Hope you are well, and the full details follow.",
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
  "qid": "q8cb87e6491",
  "text": "case: CASE-1266\ncontact: Lena Whitcombe\nitem: printer toner\nA polite but slightly irritated case was raised with Corran Telecom about the printer toner. The details follow in the usual way.",
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
  "qid": "q6a3f19f8d3",
  "text": "Lena Whitcombe has raised a case with Lindenfeld Outfitters about a tyre order, filed as CASE-4387. The background and details follow below. This is kept brief and formal for the file.",
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
  "qid": "q3e48175ac7",
  "text": "Mira Castell raised a case with Mistral Home about a grocery order. The case is filed as CASE-8692. The history of the case and its details follow in full.",
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
  "qid": "q83e9b7c062",
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
  "qid": "q418e10de18",
  "text": "Client visit case for Jonas Feld\nJonas Feld raised case CASE-8177 with Veridia Health about a printer order. A touch of frustration shows, but the wording is courteous throughout.",
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
  "qid": "qea16689172",
  "text": "Hello,\nMy name is Eva Marsh and I am writing to raise a case with Halvard Insurance about my laptop. The matter is routine and the history follows below under CASE-3014.\nBest regards,",
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
  "qid": "q7a6cb5b206",
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
  "qid": "q60efad3192",
  "text": "customer: Aiko Brandt\norganisation: Corran Telecom\ncase: CASE-4616\nAiko Brandt raised this case about a summer trip. The customer sounds a bit put out but polite, and the full details follow.",
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
  "qid": "q0bbfd76494",
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
  "qid": "qdd0dd3ddbf",
  "text": "Customer case CASE-3204 for Eva Marsh\nEva Marsh is a warm, chatty sort who has raised a case with Mistral Home about the support transcript. The case details are laid out below.",
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
  "qid": "qb80b1adf36",
  "text": "Tomas Lindqvist: Hello, I am calling about my payroll record. I raised a case with Mistral Home and I am feeling a little irritated and would value a clear explanation.\nagent: Hello. I have case CASE-2342 on file, so let us go through the payroll record background.",
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
  "qid": "qf7183b4095",
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
  "qid": "qb738190535",
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
  "qid": "q17e92df62a",
  "text": "Help with language course for Tomas Lindqvist, case CASE-6523\nTomas Lindqvist raised a friendly case with Veridia Health about the language course, and the details follow. The team is pleased to take a look and the conversation is off to a warm start.",
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
  "qid": "qa4c2582d44",
  "text": "Hello,\nMy name is Lucas Brenner and I am writing to raise a case with Brightwell Supply about my family visit. The case is logged under CASE-3537 and the history follows in the sections below.\nKind regards",
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
  "qid": "q7a25bdf9be",
  "text": "Lucas Brenner: Hello. I am writing about my cable reel and I raised a case with Redfern Bank about it.\nsupport: Hello. I have case CASE-8723 on file, and the cable reel details are set out below.",
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
  "qid": "q1dc15bc10e",
  "text": "Friendly query on office chair for Eva Marsh, CASE-5955\nEva Marsh reached out to Pembroke Travel about an office chair in a warm and friendly way, and the background follows. The conversation is pleasant and the case details are set out below.",
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
  "qid": "qbd63e6336f",
  "text": "Hana Sato has raised a case with Halvard Insurance about the camera bag. The matter appears as CASE-4396. The routine history and the case details follow below.",
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
  "qid": "q80379cf8b4",
  "text": "Safety boot matter for Priya Raman\nPriya Raman raised case CASE-6425 with Quayside Software about a printer toner. Hope you are well, and the full details follow.",
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
  "qid": "q60cad7c0ae",
  "text": "Nadia Kowal: Hello, I am writing to raise a case with Brightwell Supply about e-bike.\nsupport: Hello. Your matter is recorded as CASE-4120 and the full details are set out in order.",
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
  "qid": "qdfc674e5e7",
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
  "qid": "q3243a2ece4",
  "text": "case: CASE-6349\ncustomer: Lucas Brenner\nitem: standing desk\nThe customer politely raised a case with Selkirk Logistics about the standing desk, though mildly irritated. The details of the matter follow.",
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
  "qid": "q0f41717fac",
  "text": "Sara Ilves has raised a case with Pembroke Travel about the notes app. The case appears as CASE-1010. This is a routine note and the case history follows below.",
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
  "qid": "q4f3da0d902",
  "text": "Hello,\nMy name is Lucas Brenner and I am writing to raise a case with Quayside Software about my standing desk. The matter is calm and routine, and the case is filed as CASE-9787. The details follow below.\nTake care,",
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
  "qid": "q5c26b56319",
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
  "qid": "qa2016c4e40",
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
  "qid": "qc21903c21b",
  "text": "customer: Tomas Lindqvist\norganisation: Lindenfeld Outfitters\ncase: CASE-2676\nTomas Lindqvist raised this case about a sofa order. There is mild annoyance here, though the customer remains polite, and the details follow.",
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
  "qid": "qdeeff8d732",
  "text": "Formal record: Ines Duarte raised case CASE-3432 with Selkirk Logistics about a washing machine. Matter recorded briefly for internal use. Full details follow in the case file.",
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
  "qid": "q0b8f651ef8",
  "text": "Theo Kalnins: Hello. I am calling about my language course. I raised a case with Halvard Insurance and I would like to talk the matter over.\nagent: Hello. I have case CASE-7467 on file, and the language course details are in front of me.",
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
  "qid": "qa835f8627e",
  "text": "case: CASE-1266\ncontact: Lena Whitcombe\nitem: printer toner\nA polite but slightly irritated case was raised with Corran Telecom about the printer toner. The details follow in the usual way.",
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
  "qid": "q363ba62d86",
  "text": "Lucas Brenner has raised a case with Selkirk Logistics about a card account, filed as CASE-5280. The background and details of the matter follow in this file. Matters of this kind are set out formally and briefly.",
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
  "qid": "qa5001df0bf",
  "text": "Dana Okafor: Hello there, I am getting in touch about a client visit from Tamsin Fitness. It is a routine matter and I am calm about it.\nsupport: Hello, thank you for reaching out. Your case CASE-1708 is logged and the client visit details follow.",
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
  "qid": "q28babf7a2d",
  "text": "Lucas Brenner has raised a case with Selkirk Logistics about a card account, filed as CASE-5280. The background and details of the matter follow in this file. Matters of this kind are set out formally and briefly.",
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
