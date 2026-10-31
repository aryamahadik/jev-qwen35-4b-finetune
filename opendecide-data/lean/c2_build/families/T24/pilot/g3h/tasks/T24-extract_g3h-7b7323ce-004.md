# G3-H extraction T24-extract_g3h-7b7323ce-004 (family T24)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T24/pilot/g3h/answers/T24-extract_g3h-7b7323ce-004.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 3. Answers expected: 3 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "customer": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q3829b4aaea",
  "text": "A courteous opening message came in from Hugo Laine about the case. The entry records a calm tone and a clear description of the request. Please route it to the team that reviews these cases.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who raised the case, as written"
   }
  ]
 },
 {
  "qid": "qb0e89e8f5d",
  "text": "Tomas Ferreira wrote about the case. Short and clear message, and the file is ready for the team to review. Please look at the request when you have a chance.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who raised the case, as written"
   }
  ]
 },
 {
  "qid": "q495b84467a",
  "text": "Grace Mensah opened the thread with a kind and courteous message. The message asked that the request be reviewed by someone with patience. Please answer the contact in a warm and respectful tone.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who raised the case, as written"
   }
  ]
 }
]
