# G3-H extraction T23-extract_g3h-7d2d7b6c-002 (family T23)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T23/pilot_i2/g3h/answers/T23-extract_g3h-7d2d7b6c-002.json

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
  "qid": "qd395de5b15",
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
  "qid": "qf21d1c8efe",
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
  "qid": "qef4204e213",
  "text": "Sara Ilves raised case CASE-3538 with Halvard Insurance about camera bag. The matter is formal in style and set out in brief. Details follow in the internal file.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q701a116391",
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
  "qid": "qaae1145a65",
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
  "qid": "qac5ffe7532",
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
  "qid": "q98f6f07986",
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
  "qid": "qbf0a13dd64",
  "text": "Theo Kalnins: Hello, I would like to put a formal matter on record with Pembroke Travel about my customer file.\nsupport: Thank you for getting in touch. CASE-4428 is logged and the background to the customer file follows.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q8b56de214c",
  "text": "Lucas Brenner: Hello. I am calling about my washing machine. I raised a case with Veridia Health and I am a bit irritated, and I would like to talk it through with you.\nagent: Hello. I have case CASE-2718 on file, so let us talk through the washing machine details.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qe5841c82f7",
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
  "qid": "q783822477e",
  "text": "Customer case CASE-7621 for Malik Osei\nMalik Osei is a delight to deal with and has raised a case with Upland Utilities about the savings account. The case is logged under CASE-7621 and the details are set out below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q2b9f7efff5",
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
  "qid": "qaded0a0bba",
  "text": "Ravi Anand raised a case with Mistral Home about a streaming plan, filed as CASE-1987. The background and details of the matter follow below. This is a routine matter for the team to read through.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qb93abdd014",
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
  "qid": "qe61457ba0a",
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
  "qid": "q638096b830",
  "text": "case: CASE-5880\ncustomer: Lucas Brenner\nitem: coffee grinder\nLucas Brenner raised a case with Mistral Home about a coffee grinder. Thanks so much for reading the history and details below, and it is lovely to be in touch.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q06968df466",
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
  "qid": "qb1e415bd57",
  "text": "Dear support team,\nI am writing to raise a case with Quayside Software about my study block. My name is Nadia Kowal and the case is filed under CASE-7162. I appreciate your careful attention and the details follow.\nKind regards,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qaec0ff31af",
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
  "qid": "q23ccddc315",
  "text": "Dana Okafor: Hi there, I am calling about my laptop. I raised case CASE-2802 with Redfern Bank, and it is nice to be in touch.\nagent: Hi Dana Okafor, so good to speak with you. The full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qc6bc6a00e3",
  "text": "Dana Okafor: Hi there, I am calling about my laptop. I raised case CASE-2802 with Redfern Bank, and it is nice to be in touch.\nagent: Hi Dana Okafor, so good to speak with you. The full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q5b8831e045",
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
  "qid": "q285d5b305c",
  "text": "Sara Ilves: Hello, I wish to make a formal note about my laptop from Tamsin Fitness.\nsupport: Hello. The case CASE-9071 has been filed and the laptop background is being gathered.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qd11a7a8096",
  "text": "Hello,\nJonas Feld here. I am writing to raise a case with Tamsin Fitness about the safety boot. The case is logged under CASE-6980 and the history follows.\nWarm regards",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q3fc980cf52",
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
  "qid": "q41a503b6c7",
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
  "qid": "q97b450f9a7",
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
  "qid": "qe663f49b3a",
  "text": "name: Lucas Brenner\ncompany: Pembroke Travel\ncase: CASE-2286\nLucas Brenner is a bit peeved but courteous. He has raised a case with Pembroke Travel about the payroll record, and the details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qb32f1e9cfd",
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
  "qid": "q423dacebd2",
  "text": "Coffee grinder case for Owen Pryce\nOwen Pryce raised case CASE-5993 with Upland Utilities about a payroll record. Warm greetings to you, and the full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q22056d6f5f",
  "text": "Lena Whitcombe: Hello. I am calling about my design suite. I raised a case with Tamsin Fitness and I am a bit irritated, and I would like to talk it through with you.\nagent: Hello. I have case CASE-6776 on file, so let us talk through the design suite details.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qaef120cc8f",
  "text": "Lena Whitcombe: Hello. I am calling about my design suite. I raised a case with Tamsin Fitness and I am a bit irritated, and I would like to talk it through with you.\nagent: Hello. I have case CASE-6776 on file, so let us talk through the design suite details.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qe48a0e9cfd",
  "text": "Lena Whitcombe raised a case with Redfern Bank about the camera bag. The matter is recorded under CASE-2198. The case is routine and the history follows in order.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q415e8e343f",
  "text": "Kofi Mensah: Hi there, thanks for picking up. I am calling about my savings account and I raised a case with Pembroke Travel, which I am happy to talk through.\nagent: Hello there, lovely to hear from you. I have case CASE-3723 on file, so let us go through the savings account together.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q0949f46561",
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
  "qid": "q9f20294cb4",
  "text": "Owen Pryce has raised a case with Upland Utilities about a payroll record. The case carries the label CASE-5993. Everything about the matter is routine, and the history follows in full.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qa5993adb60",
  "text": "Dana Okafor: Hello. I am calling about my standing desk. I raised a case with Upland Utilities and I am a bit irritated, though I would appreciate a clear reply.\nagent: Hello. I have case CASE-5366 on file, and the standing desk details are right here.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qcbac1b49c4",
  "text": "Dana Okafor: Hello. I am calling about my standing desk. I raised a case with Upland Utilities and I am a bit irritated, though I would appreciate a clear reply.\nagent: Hello. I have case CASE-5366 on file, and the standing desk details are right here.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q0e606e2b42",
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
  "qid": "qebf3443ca7",
  "text": "Aiko Brandt has raised a case with Quayside Software about the customer file. The case appears as CASE-7021. This is a routine note and the case history follows below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q59962da793",
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
  "qid": "q7a886572c8",
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
  "qid": "qfa1b30f965",
  "text": "Mild frustration over standing desk for Ana Ruiz, CASE-7588\nAna Ruiz raised a polite case with Corran Telecom about a standing desk, and the details follow. The customer is a little annoyed but remains courteous while the matter is discussed.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qaa99fbe2a4",
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
  "qid": "qa74008d2c9",
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
  "qid": "q26999097d0",
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
  "qid": "qf52506b539",
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
  "qid": "q3416a13bab",
  "text": "Nadia Kowal: Hello, I am writing to raise a case with Pembroke Travel about my current account.\nsupport: Thank you for writing. The case sits under CASE-9063 with its full details.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
