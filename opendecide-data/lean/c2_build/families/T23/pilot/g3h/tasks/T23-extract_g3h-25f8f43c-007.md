# G3-H extraction T23-extract_g3h-25f8f43c-007 (family T23)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T23/pilot/g3h/answers/T23-extract_g3h-25f8f43c-007.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 22. Answers expected: 22 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "case_id": <value or null>, "customer": <value or null>, "item": <value or null>, "org": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q105776c7db",
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
  "qid": "q859ae2ce31",
  "text": "Dear support team,\nMy name is Hana Sato and I am writing to raise a case with Lindenfeld Outfitters about my family visit. The background and details follow below, filed as CASE-6936. I look forward to your reply.\nKind regards,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q5feb6718ca",
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
  "qid": "q70c708071b",
  "text": "Short case-file entry: Sara Ilves raised case CASE-2541 with Brightwell Supply about a payroll record. Drafted in a formal, concise style, with the details to come below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q8d54ca54d8",
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
  "qid": "q8784a451f8",
  "text": "Dear colleagues,\nI am writing to raise a matter with Redfern Bank about my payroll record. My name is Dana Okafor and the case is logged as CASE-6950. I appreciate your attention to the details that follow.\nYours faithfully,",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qe919209205",
  "text": "Owen Pryce: Hello, I am ringing about my notes app with Quayside Software, and I would love a friendly chat.\nagent: Hello and lovely to hear from you. I have your case CASE-4782 in front of me and I am glad to help with the notes app.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qd384d5f431",
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
  "qid": "q56270e6ca8",
  "text": "Card account concern from Eva Marsh\nEva Marsh raised case CASE-1131 with Veridia Health about a photo editor. A little cross, though civil, and the details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q0d4a4588b5",
  "text": "Hana Sato: Hello, it is so nice to speak with you. I am calling about my camera bag from Brightwell Supply, and it is a pleasant matter.\nagent: Hello, how nice to hear from you. I have your case CASE-3350 in front of me and I am glad you rang.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qa813d8b797",
  "text": "Gym membership case for Dana Okafor\nDana Okafor raised case CASE-3645 with Pembroke Travel about a current account. The customer is a little frustrated but polite, and the details follow.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q911307a6fb",
  "text": "Query about support transcript from Ines Duarte, case CASE-1499\nInes Duarte raised this case with Upland Utilities about a support transcript, and the details follow. The customer feels a little frustrated but remains polite and patient, and the case summary is set out below.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qd4530847ce",
  "text": "Hello,\nNadia Kowal here. I am writing to raise a case with Veridia Health about my language course. The case is filed under CASE-8099 and the history follows.\nSincerely",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q29dcf50440",
  "text": "Owen Pryce: I am ringing about my coffee grinder from Corran Telecom, and I am a little cross, though I do appreciate your help.\nagent: I understand the frustration and thank you for bearing with me, and your case CASE-7282 is in front of me.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qb8cc0bb67d",
  "text": "Owen Pryce: I am ringing about my coffee grinder from Corran Telecom, and I am a little cross, though I do appreciate your help.\nagent: I understand the frustration and thank you for bearing with me, and your case CASE-7282 is in front of me.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qbb0cc82216",
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
  "qid": "q122fbca22f",
  "text": "Summer trip case from Hana Sato\nHana Sato raised a case with Quayside Software about the photo editor, filed as CASE-3507. Everything about the matter is set out below in a warm and friendly way.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q33e68a1f5f",
  "text": "Hana Sato: Hello. I am calling about my payroll record. I raised a case with Brightwell Supply and I would like a straightforward explanation.\nagent: Hello. I have case CASE-2948 on file, so let us go through the payroll record together.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "q4289261e0c",
  "text": "Dana Okafor has raised a case with Tamsin Fitness about a cable reel, filed as CASE-9774. The background and details follow below. This is kept brief and formal for the file.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qecbb920ae2",
  "text": "Customer file case raised by Mira Castell\nMira Castell raised a case with Brightwell Supply about the site audit, filed as CASE-3758. The matter is a little frustrating, and the background is set out below for the team.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qa9c8986716",
  "text": "Client visit case for Nadia Kowal\nNadia Kowal raised case CASE-7162 with Quayside Software about a study block. A touch of frustration shows, but the wording is courteous throughout.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
  "qid": "qb816e4a254",
  "text": "Priya Raman raised a case with Tamsin Fitness about a photo editor, filed as CASE-7347. The background and details of the matter follow below. This is a routine matter for the team to read through.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the customer who raised the case, as written"
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
