# G3-H extraction T25-extract_g3h-7ad5ec37-002 (family T25)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/data/c2_parts/T25/qc/g3h/answers/T25-extract_g3h-7ad5ec37-002.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 5. Answers expected: 5 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "asker": <value or null>, "attr": <value or null>, "org": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q679ccb0c71",
  "text": "This internal memo records that Ximena Ferreira, a support agent, is handling a request about the entry price at Thimble Lane Evening Classes. The extract supplied for that request has been pasted in for reference. The matter is being dealt with in a formal and orderly manner. Please keep this with the usual support papers.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "q8d48cbc8a4",
  "text": "This write-up explains how Fionnuala Doyle looked into the custom cake deposit at Pellham Coding Academy. I am getting settled in the role, so I worked through the extract I pasted in as quickly as I could. Writing this down helps me keep track of the steps for whoever starts after me.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "qaf20a6cce3",
  "text": "Dear colleague,\nMy name is Fionnuala Doyle and I am writing to look into the padlock price at Starling Cinema. I have pasted what was found below for your reference. Thank you for your help on this matter.\nKind regards,",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "q400d0d009b",
  "text": "Yaw Ofori: I need to get a reply out on the late return fee at Quayside Lettings Office and I am a bit rushed.\ncolleague: Pass me the extract and I will help you draft it.\ncolleague: Keep going, we are nearly through it.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "q2b8b9103ae",
  "text": "Arjun Sethi: Need to check the damage deposit at Corrie Hall Institute, I am juggling a busy list at the moment.\ncolleague: Send the extract over and I will look at it with you.\ncolleague: Happy to help you work through it.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 }
]
