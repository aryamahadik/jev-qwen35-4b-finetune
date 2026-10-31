# T12 extraction task T12-extract_lex-4d2f91a1-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/extract/answers/T12-extract_lex-4d2f91a1-000.json

Task kind: extract_lex; items: 30; answer fields: meaning.

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

You read one short phrase or sentence about an accounts-payable (AP) policy card and say which meaning it expresses. Each item has a "text" (the phrase or sentence, with an example value filled in) and a "choices" list of meanings. For each item, pick the one choice that the text says most plainly, and copy that choice exactly, character for character, into the "meaning" field. Judge the words of the text only: do not guess from what would be sensible for an AP policy, and do not reason about any other item. Answer every item once; no item may be skipped or repeated.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array in the answer format below, one entry per item. No other file, no other text.

Answer format: [{"qid": "<qid>", "meaning": "<one choice, copied exactly>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "q1570e22718",
  "text": "Find the first failing check in the check order and let it set the action for the whole card.",
  "choices": [
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the last check in the stated check order that fails decides the action",
   "the first check in the stated check order that fails decides the action",
   "the most severe failing check decides the action"
  ]
 },
 {
  "qid": "qbd172b9d85",
  "text": "Follow the check order and halt at the first check that fails, because later checks do not change the action.",
  "choices": [
   "the most severe failing check decides the action",
   "the last check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the first check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "qf829778ae9",
  "text": "When a check fails in the check order, the first such failure decides the action.",
  "choices": [
   "the first check in the stated check order that fails decides the action",
   "the last check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the most severe failing check decides the action"
  ]
 },
 {
  "qid": "qba4d8a8d4f",
  "text": "Keep to the check order, halt at the first failing check, and set the action from that check alone.",
  "choices": [
   "the most severe failing check decides the action",
   "the last check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the first check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "qaa5246dafe",
  "text": "Take the checks in the check order and let the first one that fails set the action.",
  "choices": [
   "the first check in the stated check order that fails decides the action",
   "the most severe failing check decides the action",
   "the last check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order"
  ]
 },
 {
  "qid": "q2f177114b1",
  "text": "The action stands once it is set, because checks that come later in the check order do not change it.",
  "choices": [
   "the first check in the stated check order that fails decides the action",
   "the most severe failing check decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the last check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "qcffe692db3",
  "text": "The check order sets the sequence, and the first failing check in that sequence determines the action.",
  "choices": [
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the most severe failing check decides the action",
   "the last check in the stated check order that fails decides the action",
   "the first check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "q7a650052d8",
  "text": "The first check in the check order that fails decides the action.",
  "choices": [
   "the last check in the stated check order that fails decides the action",
   "the first check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the most severe failing check decides the action"
  ]
 },
 {
  "qid": "q8ed002129e",
  "text": "Whatever the later checks in the check order show, they do not change the action.",
  "choices": [
   "the first check in the stated check order that fails decides the action",
   "the most severe failing check decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the last check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "q5afeaa5069",
  "text": "The earliest failing check in the check order settles the action for the whole card.",
  "choices": [
   "the most severe failing check decides the action",
   "the last check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the first check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "q84dbaee1df",
  "text": "The action is fixed by the first failing check in the check order, and a later check does not change it.",
  "choices": [
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the most severe failing check decides the action",
   "the first check in the stated check order that fails decides the action",
   "the last check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "q91e2d6be76",
  "text": "The action is set by the first failing check in the check order.",
  "choices": [
   "the most severe failing check decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the first check in the stated check order that fails decides the action",
   "the last check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "qef0a544e9d",
  "text": "Whichever failing check comes first in the check order decides the action, and later checks do not change it.",
  "choices": [
   "the most severe failing check decides the action",
   "the first check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the last check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "qf6d3a634c5",
  "text": "Read the check order from its start and apply the first failing check you reach to the action.",
  "choices": [
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the first check in the stated check order that fails decides the action",
   "the most severe failing check decides the action",
   "the last check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "q671dc94379",
  "text": "Work through the check order, and when you find the first failing check, use it to set the action.",
  "choices": [
   "the first check in the stated check order that fails decides the action",
   "the last check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the most severe failing check decides the action"
  ]
 },
 {
  "qid": "q7cfc31f270",
  "text": "A later check in the check order does not change an action that is already decided.",
  "choices": [
   "the most severe failing check decides the action",
   "the last check in the stated check order that fails decides the action",
   "the first check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order"
  ]
 },
 {
  "qid": "qfb5deff324",
  "text": "Walk through the check order in turn, and let the first failure you meet set the action; later checks do not change it.",
  "choices": [
   "the last check in the stated check order that fails decides the action",
   "the first check in the stated check order that fails decides the action",
   "the most severe failing check decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order"
  ]
 },
 {
  "qid": "qa6fe088f13",
  "text": "Every check that comes after the failing one in the check order does not change the action.",
  "choices": [
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the first check in the stated check order that fails decides the action",
   "the last check in the stated check order that fails decides the action",
   "the most severe failing check decides the action"
  ]
 },
 {
  "qid": "qd906d7c5bc",
  "text": "Once the checks are taken in the check order, the first one that fails settles the action.",
  "choices": [
   "the first check in the stated check order that fails decides the action",
   "the most severe failing check decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the last check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "q43fc558392",
  "text": "Later checks in the check order do not change the action that the first failing check set.",
  "choices": [
   "the first check in the stated check order that fails decides the action",
   "the last check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the most severe failing check decides the action"
  ]
 },
 {
  "qid": "q1e3a1ab0e4",
  "text": "Go through the check order one check at a time, and let the first failing check set the action.",
  "choices": [
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the last check in the stated check order that fails decides the action",
   "the most severe failing check decides the action",
   "the first check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "qcd7a99f4d3",
  "text": "Once the first failing check in the check order has set the action, later checks do not change it.",
  "choices": [
   "the most severe failing check decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the last check in the stated check order that fails decides the action",
   "the first check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "q640dc24cc6",
  "text": "Run the checks in the check order, and once one fails, let that result decide the action.",
  "choices": [
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the last check in the stated check order that fails decides the action",
   "the first check in the stated check order that fails decides the action",
   "the most severe failing check decides the action"
  ]
 },
 {
  "qid": "qf26a89f316",
  "text": "Apply the check order in sequence, and let the first check that fails determine the action.",
  "choices": [
   "the first check in the stated check order that fails decides the action",
   "the last check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the most severe failing check decides the action"
  ]
 },
 {
  "qid": "q57e21b3c1b",
  "text": "Once a check fails in the check order, later checks do not change the action.",
  "choices": [
   "the most severe failing check decides the action",
   "the last check in the stated check order that fails decides the action",
   "the first check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order"
  ]
 },
 {
  "qid": "qd7e84a70fb",
  "text": "Each check runs in the check order, and the first one that fails sets the action.",
  "choices": [
   "the most severe failing check decides the action",
   "the last check in the stated check order that fails decides the action",
   "the first check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order"
  ]
 },
 {
  "qid": "qbcb0f2f345",
  "text": "The outcome stays where the first failure put it, because later checks in the check order do not change the action.",
  "choices": [
   "the first check in the stated check order that fails decides the action",
   "the most severe failing check decides the action",
   "the last check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order"
  ]
 },
 {
  "qid": "q832eab951a",
  "text": "The check order decides which failure counts, because the first failure met in that order decides the action.",
  "choices": [
   "the last check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the first check in the stated check order that fails decides the action",
   "the most severe failing check decides the action"
  ]
 },
 {
  "qid": "q8b03641bb0",
  "text": "The action follows from the first check that fails when the checks are taken in the check order.",
  "choices": [
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the most severe failing check decides the action",
   "the first check in the stated check order that fails decides the action",
   "the last check in the stated check order that fails decides the action"
  ]
 },
 {
  "qid": "q1a5c0a0764",
  "text": "Reading the check order ends at the first failure, so later checks do not change the action.",
  "choices": [
   "the first check in the stated check order that fails decides the action",
   "the last check in the stated check order that fails decides the action",
   "the failing check printed highest in the list of checks decides the action, whatever the stated check order",
   "the most severe failing check decides the action"
  ]
 }
]
