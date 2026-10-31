# G3-H extraction T21-extract_g3h-8b690ff4-005 (family T21)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T21/pilot/g3h/answers/T21-extract_g3h-8b690ff4-005.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 9. Answers expected: 9 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "agreement": <value or null>, "claimant": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q847c58f1b0",
  "text": "counsel: Mabrey Gardens Network has raised a claim under the Sorrowmere deposit agreement\ncolleague: understood, the wording is in the usual folder\ncounsel: thanks, that is the main point",
  "schema": [
   {
    "field": "claimant",
    "type": "name",
    "describe": "the party bringing the claim, as written"
   },
   {
    "field": "agreement",
    "type": "name",
    "describe": "the agreement under discussion, as written"
   }
  ]
 },
 {
  "qid": "qb045f80c84",
  "text": "Dear colleague,\nPellinder Community Trust has raised a claim under the Quorrin tree planting agreement.\nThis is a routine matter and the background is straightforward.\nRegards,",
  "schema": [
   {
    "field": "claimant",
    "type": "name",
    "describe": "the party bringing the claim, as written"
   },
   {
    "field": "agreement",
    "type": "name",
    "describe": "the agreement under discussion, as written"
   }
  ]
 },
 {
  "qid": "q31eae3aa4d",
  "text": "Claimant: Tarnweld Materials Hub\nAgreement: Hespery collection agreement\nMatter: routine claim raised, logged for reference.",
  "schema": [
   {
    "field": "claimant",
    "type": "name",
    "describe": "the party bringing the claim, as written"
   },
   {
    "field": "agreement",
    "type": "name",
    "describe": "the agreement under discussion, as written"
   }
  ]
 },
 {
  "qid": "qd3cb2348b2",
  "text": "Where do I begin with a claim under the Quarrymere licence agreement?\nCorvell Telecom has raised a claim under the Quarrymere licence agreement, and the wording that follows is set out in plain language. The rest of this page keeps things friendly and clear.",
  "schema": [
   {
    "field": "claimant",
    "type": "name",
    "describe": "the party bringing the claim, as written"
   },
   {
    "field": "agreement",
    "type": "name",
    "describe": "the agreement under discussion, as written"
   }
  ]
 },
 {
  "qid": "qc0d7f43fe3",
  "text": "Teswick Hospitality Group has raised a claim under the Vantrey catering agreement. The board has the summary in front of it. The matter is routine for the group.",
  "schema": [
   {
    "field": "claimant",
    "type": "name",
    "describe": "the party bringing the claim, as written"
   },
   {
    "field": "agreement",
    "type": "name",
    "describe": "the agreement under discussion, as written"
   }
  ]
 },
 {
  "qid": "qe4c7992b9b",
  "text": "Dear colleague,\nPellham Linen Works has raised a claim under the Quillmoor franchise agreement, and this is a routine part of our desk work.\nKind regards, Contracts desk",
  "schema": [
   {
    "field": "claimant",
    "type": "name",
    "describe": "the party bringing the claim, as written"
   },
   {
    "field": "agreement",
    "type": "name",
    "describe": "the agreement under discussion, as written"
   }
  ]
 },
 {
  "qid": "q2c9e1fc0af",
  "text": "Huddle record:\n- Opaline Facilities Trust has raised a claim under the Vellarin booking agreement, and the room is busy.\n- Calls run down the list.",
  "schema": [
   {
    "field": "claimant",
    "type": "name",
    "describe": "the party bringing the claim, as written"
   },
   {
    "field": "agreement",
    "type": "name",
    "describe": "the agreement under discussion, as written"
   }
  ]
 },
 {
  "qid": "q806c2da582",
  "text": "Ferrinex Council has raised a claim under the Sabrine compost offtake agreement. This memo is written in a formal and careful manner for the legal group. The dispute is described only in general terms.",
  "schema": [
   {
    "field": "claimant",
    "type": "name",
    "describe": "the party bringing the claim, as written"
   },
   {
    "field": "agreement",
    "type": "name",
    "describe": "the agreement under discussion, as written"
   }
  ]
 },
 {
  "qid": "qe02d454f14",
  "text": "Session on the Tolgarth sponsorship agreement:\n- Oxlade Estates has raised a claim under the Tolgarth sponsorship agreement.\n- The matter is set out in general terms for the group to review.",
  "schema": [
   {
    "field": "claimant",
    "type": "name",
    "describe": "the party bringing the claim, as written"
   },
   {
    "field": "agreement",
    "type": "name",
    "describe": "the agreement under discussion, as written"
   }
  ]
 }
]
