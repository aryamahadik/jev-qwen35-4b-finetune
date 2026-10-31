# G3-H extraction T23-extract_g3h-9a5fbcf9-000 (family T23)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T23/qc/g3h/answers/T23-extract_g3h-9a5fbcf9-000.json

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
  "qid": "qb81c5acdbc",
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
  "qid": "q0669e433c5",
  "text": "Yara Haddad has raised a case with Tamsin Fitness about the e-bike. The matter appears as CASE-9830. The routine history and the case details follow below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q778d978fe4",
  "text": "Safety boot matter for Dana Okafor\nDana Okafor raised case CASE-4325 with Pembroke Travel about a coffee grinder. Hope you are well, and the full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qb1e7557b0b",
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
  "qid": "q03bb8dc4f8",
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
  "qid": "q109da0f9f2",
  "text": "Eva Marsh: Hello, I am writing to raise a case with Quayside Software about my e-bike.\nsupport: Thank you for writing. The case sits under CASE-1514 with its full details.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q826a7d0c6d",
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
  "qid": "q9fee8ccb47",
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
  "qid": "q447592b10b",
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
  "qid": "q7972e816d6",
  "text": "Tomas Lindqvist: Hi there, I am calling about my printer toner. I raised case CASE-6093 with Brightwell Supply, and it is nice to be in touch.\nagent: Hi Tomas Lindqvist, so good to speak with you. The full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q8ea5885616",
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
  "qid": "qc331b0d6a4",
  "text": "Hi Theo Kalnins,\nYour case CASE-2426 with Upland Utilities covers a photo editor that you raised. Everything is calm and routine, and the details are set out in the sections below.\nWarm regards",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qe627058276",
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
  "qid": "q1e0c73c0b0",
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
  "qid": "qeaf08e904a",
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
  "qid": "q41a096a934",
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
  "qid": "q7d6837a7a3",
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
  "qid": "qee66c13a6c",
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
  "qid": "qa1943ebe97",
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
  "qid": "qce863810f9",
  "text": "Dear colleagues,\nI am writing to raise a matter with Pembroke Travel about my current account. My name is Priya Raman and the case is logged as CASE-2838. I appreciate your attention to the details that follow.\nYours faithfully,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qeb8029c0c4",
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
  "qid": "q99a1b82d07",
  "text": "Kofi Mensah and the tyre order\nKofi Mensah raised case CASE-2488 with Upland Utilities about a tyre order. Mild impatience comes through, but the customer stays civil and the details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q4bfc810546",
  "text": "Brief entry for the file: Sara Ilves raised case CASE-1758 with Redfern Bank about a camera recording. The register is formal, and the case details follow in full. Kept on file.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qaa90da7bb4",
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
  "qid": "qe6f05032ee",
  "text": "Internal case note: Dana Okafor formally raised a case with Halvard Insurance about an e-bike. The record sits under CASE-6361, and the summary is kept brief and to the point. Background follows in a concise form.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qe5904934a3",
  "text": "Lucas Brenner: Hello there, I would like to talk about my tyre order, case CASE-8312 with Upland Utilities.\nagent: Hi Lucas Brenner, lovely to speak with you. Hope you are well, and the full details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q69bc7f16f7",
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
  "qid": "q843a704816",
  "text": "Card account concern from Nadia Kowal\nNadia Kowal raised case CASE-8444 with Veridia Health about a printer toner. A little cross, though civil, and the details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q3669cc1367",
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
  "qid": "q7ebd6f04e9",
  "text": "Yara Haddad has raised a case with Tamsin Fitness about the e-bike. The matter appears as CASE-9830. The routine history and the case details follow below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q348f5690a9",
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
  "qid": "qddb5ffe10c",
  "text": "Dear Hana Sato,\nThank you for raising case CASE-2513 with Mistral Home about your client visit. This is a routine matter, and the full details follow below.\nKind regards",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q0b3a8e67a9",
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
  "qid": "q91aff2a813",
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
  "qid": "qcaa7288a33",
  "text": "Formal record: Jonas Feld raised case CASE-3447 with Quayside Software about a payroll record. Matter recorded briefly for internal use. Full details follow in the case file.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q6753b9059c",
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
  "qid": "q1bfd5e49dc",
  "text": "Ana Ruiz: Hello. I am calling about my notes app. I raised a case with Veridia Health and I would like a straightforward explanation.\nagent: Hello. I have case CASE-9063 on file, so let us go through the notes app together.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q3c1be452a2",
  "text": "Lucas Brenner: Hi, I am writing to raise a case with Pembroke Travel about the client visit.\nsupport: Hello. The case is logged under CASE-6105 and the usual details follow.\nLucas Brenner: Thanks, that is everything for this call.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q6100306124",
  "text": "Internal case note: Lucas Brenner formally raised a case with Veridia Health about a washing machine. The record sits under CASE-8273, and the summary is kept brief and to the point. Background follows in a concise form.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qbeebe8f10a",
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
  "qid": "q7bb5692358",
  "text": "Routine matter logged for internal use. Mira Castell raised case CASE-7594 with Tamsin Fitness about a streaming plan. The mood is calm, and the case details follow below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qb0260ee99f",
  "text": "Internal record: CASE-5769 concerns a card account that Ana Ruiz raised with Redfern Bank. Things feel calm and the matter is routine. Background and details follow below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qde64f3073b",
  "text": "Priya Raman: Hello. I raised a case with Veridia Health about my annual plan and I would like the matter reviewed.\nsupport: Hello. I have case CASE-8514 on file and the annual plan details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qe8978a1dd2",
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
  "qid": "qa7b8c9d86c",
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
  "qid": "q1c0c4bd80f",
  "text": "Hello team,\nMy name is Theo Kalnins and I have raised a case with Halvard Insurance about my client visit. The background and case details are set out below under CASE-8620. It is a fairly ordinary matter.\nKind regards,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qad629df2f7",
  "text": "Sara Ilves and the meal kit plan\nSara Ilves raised case CASE-3046 with Redfern Bank about a meal kit plan. Mild impatience comes through, but the customer stays civil and the details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q1f1ab925f0",
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
  "qid": "q8716b2e867",
  "text": "case: CASE-5488\ncustomer: Theo Kalnins\nitem: study block\nThe customer kindly raised a case with Lindenfeld Outfitters about the study block, and the details follow. The tone of the message is upbeat and cheerful throughout.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qd48a3e68ff",
  "text": "Yara Haddad raised case CASE-3797 with Selkirk Logistics about a grocery order. The case is calm and routine. Background is filed below, along with the rest of the details.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
