# G3-H extraction T23-extract_g3h-9a5fbcf9-004 (family T23)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T23/qc/g3h/answers/T23-extract_g3h-9a5fbcf9-004.json

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
  "qid": "qef0093c6ae",
  "text": "Ines Duarte: Hello, I am writing to raise a case with Upland Utilities about conference trip.\nsupport: Hello. Your matter is recorded as CASE-7123 and the full details are set out in order.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qc499c0f59d",
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
  "qid": "qfb901fc3eb",
  "text": "Client visit case for Theo Kalnins\nTheo Kalnins raised case CASE-9672 with Selkirk Logistics about a team offsite. A touch of frustration shows, but the wording is courteous throughout.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q4e7f0668ab",
  "text": "Summer trip case from Dana Okafor\nDana Okafor raised a case with Redfern Bank about the camera bag, filed as CASE-9009. Everything about the matter is set out below in a warm and friendly way.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qd6ede3d698",
  "text": "Dear Ravi Anand,\nYour case CASE-1151 concerning a card account was raised with Lindenfeld Outfitters. The matter is summarised here briefly and the details follow.\nYours faithfully",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qf40b3314b6",
  "text": "Dana Okafor: Hello, I am writing to raise a case with Veridia Health about my notes app.\nsupport: Hello. This matter sits under CASE-6013 alongside the routine notes.\nDana Okafor: Lovely, thank you.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qceb13b9a96",
  "text": "customer: Nadia Kowal\norganisation: Lindenfeld Outfitters\ncase: CASE-3948\nNadia Kowal raised this case about a language course. The customer sounds a bit put out but polite, and the full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q1084cbfc23",
  "text": "case: CASE-1440\ncustomer: Tomas Lindqvist\nitem: safety boot\nTomas Lindqvist raised a case with Redfern Bank about a safety boot. Thanks so much for reading the history and details below, and it is lovely to be in touch.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q6e76c06a1b",
  "text": "Formal record: Tomas Lindqvist raised case CASE-9141 with Veridia Health about a client visit. Matter recorded briefly for internal use. Full details follow in the case file.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qaa94af0ebf",
  "text": "Nadia Kowal: Hello. I raised a case with Selkirk Logistics about my conference trip, and I would like it looked into.\nsupport: Hello. I have case CASE-4162 on file and the conference trip details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qdaa4e03e9f",
  "text": "Safety boot matter for Tomas Lindqvist\nTomas Lindqvist raised case CASE-5222 with Pembroke Travel about a printer order. Hope you are well, and the full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q5e62ed6907",
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
  "qid": "qc6958da182",
  "text": "Safety boot case for Malik Osei\nMalik Osei raised case CASE-3376 with Tamsin Fitness about a savings account. We are glad to share the background, and the full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q073386929b",
  "text": "Internal case note: Ana Ruiz raised a formal case with Corran Telecom about a laptop. The case is recorded under CASE-6641. Background details follow in brief, set out in a concise and orderly format.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q400f88cfcb",
  "text": "Hello there,\nMy name is Mira Castell and I am writing about a conference trip from Selkirk Logistics. It is a routine matter and I am keen to keep things calm. The case is logged as CASE-5644 and the background follows.\nBest wishes,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q99d22b27f9",
  "text": "Customer case CASE-6934 for Jonas Feld\nJonas Feld is a warm, chatty sort who has raised a case with Veridia Health about the support transcript. The case details are laid out below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q7c2cd34231",
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
  "qid": "q0a4655e01a",
  "text": "Malik Osei: Hello, I wish to make a formal note about my antivirus licence from Tamsin Fitness.\nsupport: Hello. The case CASE-4071 has been filed and the antivirus licence background is being gathered.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q35809f2a15",
  "text": "Ravi Anand: Hey, I am ringing about my conference trip. I raised case CASE-8223 with Selkirk Logistics, and I would love a friendly chat.\nagent: Hello Ravi Anand, so nice to hear from you. The full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qd1fda358e5",
  "text": "Lena Whitcombe: Hello. I raised a case with Mistral Home about my office chair, and I would like the matter looked into.\nsupport: Hello. I have case CASE-9820 on file and the office chair details follow in full.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q46081ea2ac",
  "text": "Aiko Brandt: Hi, I am calling about my grocery order. I raised a case with Tamsin Fitness and I am a little frustrated, though I would like a clear explanation.\nagent: Thanks for getting in touch. I have case CASE-3842 on file, so tell me more about the grocery order.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qb3a2b22578",
  "text": "Card account concern from Malik Osei\nMalik Osei raised case CASE-5706 with Selkirk Logistics about a language course. A little cross, though civil, and the details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q66aac03339",
  "text": "Customer case CASE-7621 for Jonas Feld\nJonas Feld is a little put out, but polite, having raised a case with Tamsin Fitness about the office chair. The full history of the matter sits below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q3678d32f21",
  "text": "Mild frustration over language course for Nadia Kowal, CASE-3128\nNadia Kowal raised a polite case with Selkirk Logistics about a language course, and the details follow. The customer is a little annoyed but remains courteous while the matter is discussed.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q9cee9ab5c3",
  "text": "Hello team,\nMy name is Hana Sato and I have raised a case with Quayside Software about my meal kit plan. The background and case details are set out below under CASE-3106. It is a fairly ordinary matter.\nKind regards,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q465d2734c8",
  "text": "Gym membership case for Yara Haddad\nYara Haddad raised case CASE-6891 with Veridia Health about a design suite. The customer is a little frustrated but polite, and the details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q2dc37f0b14",
  "text": "Sara Ilves: Hello. I raised a case with Tamsin Fitness about my house move, and I would like it looked into.\nsupport: Hello. I have case CASE-1777 on file and the house move details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qdade53c8e7",
  "text": "name: Sara Ilves\ncompany: Veridia Health\ncase: CASE-7647\nSara Ilves is cheerful and easy to work with, having raised a case with Veridia Health about the grocery order, and the story is set out below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qeb8fe68ae0",
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
  "qid": "q4f3e7c6c82",
  "text": "Internal case note: Ana Ruiz formally raised a case with Brightwell Supply about a current account. The record sits under CASE-6482, and the summary is kept brief and to the point. Background follows in a concise form.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q39e52b0d8f",
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
  "qid": "qcf062a4262",
  "text": "Nadia Kowal: Hello, I am writing to raise a case with Veridia Health about my camera bag.\nsupport: Hello. The case sits under CASE-8497 with the routine notes beside it.\nNadia Kowal: Thanks, that covers it.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q0be85e56b9",
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
  "qid": "q3114d1e672",
  "text": "Dana Okafor has raised a case with Lindenfeld Outfitters about a camera recording, filed as CASE-4670. The background and details of the matter follow in this file. Matters of this kind are set out formally and briefly.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qd0ac5ae3a5",
  "text": "customer: Theo Kalnins\ncase: CASE-2934\nitem: grocery order\nTheo Kalnins raised this case with Selkirk Logistics about the grocery order. Hope you are well, and the full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q701ffb8e32",
  "text": "Internal case note: Ana Ruiz raised a formal case with Corran Telecom about a laptop. The case is recorded under CASE-6641. Background details follow in brief, set out in a concise and orderly format.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q9e07c20748",
  "text": "Dear team,\nI write to raise a formal case with Corran Telecom about my annual plan. My name is Malik Osei and the case identifier is CASE-3492. I appreciate your attention, and the details are set out below.\nYours sincerely,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q9920f802e7",
  "text": "Owen Pryce: Hello, I am calling about case CASE-3600 with Lindenfeld Outfitters. I am a bit irritated about my language course, though I am staying calm.\nagent: Hello Owen Pryce, thank you for calling. I hear the concern, and the full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qe13cd10dd5",
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
  "qid": "qfc6bf45c63",
  "text": "Hello,\nMy name is Ana Ruiz and I am writing to raise a case with Upland Utilities about my design suite. The matter is routine and the history follows below under CASE-5446.\nBest regards,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q32752f199b",
  "text": "Ines Duarte: Hello, I am writing to raise a case with Upland Utilities about conference trip.\nsupport: Hello. Your matter is recorded as CASE-7123 and the full details are set out in order.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q6b2c26a872",
  "text": "Lena Whitcombe raised a case with Pembroke Travel about the e-bike. The matter is recorded under CASE-1365. The case is routine and the history follows in order.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qe71fc469fb",
  "text": "Aiko Brandt: Hi there, thanks for picking up. I am calling about my office chair and I raised a case with Corran Telecom, which I am happy to talk through.\nagent: Hello there, lovely to hear from you. I have case CASE-8308 on file, so let us go through the office chair together.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qb44c29f166",
  "text": "case: CASE-2652\ncontact: Ines Duarte\nitem: tyre order\nA polite but slightly irritated case was raised with Selkirk Logistics about the tyre order. The details follow in the usual way.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qfe38457949",
  "text": "Hello Lena Whitcombe,\nThank you for raising case CASE-7886 with Lindenfeld Outfitters about your language course. The style is formal and brief, and the case details appear below.\nWith best regards",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qb6b815044c",
  "text": "Customer case CASE-8049 for Mira Castell\nMira Castell is a little put out, but polite, having raised a case with Pembroke Travel about the merchant account. The full history of the matter sits below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qd822c65dc8",
  "text": "Nadia Kowal: Hi there, I raised case CASE-6864 with Tamsin Fitness about my tyre order.\nsupport: Hello Nadia Kowal, thanks for getting in touch. This is a routine matter and the full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q3b38cabc92",
  "text": "name: Tomas Lindqvist\ncompany: Veridia Health\ncase: CASE-3439\nTomas Lindqvist is somewhat exasperated but polite, having raised a case with Veridia Health about the current account. The full background follows.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qf6d01df479",
  "text": "Customer case CASE-6934 for Jonas Feld\nJonas Feld is a warm, chatty sort who has raised a case with Veridia Health about the support transcript. The case details are laid out below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q2ea13e36fd",
  "text": "Lucas Brenner raised a case with Tamsin Fitness about a grocery order. The case is filed as CASE-8856. The history of the case and its details follow in full.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
