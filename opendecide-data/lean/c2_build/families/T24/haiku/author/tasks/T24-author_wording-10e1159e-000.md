# T24 authoring task T24-author_wording-10e1159e-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T24/haiku/author/answers/T24-author_wording-10e1159e-000.json

Task kind: author_wording; items: 6; outputs expected: 48.

You are writing short pieces of text for a synthetic training dataset about everyday customer-service
policies (returns, repairs, bookings, deposits, fees and the like). Everything you write is either a reusable template
(a program later fills each {SLOT} placeholder with a value) or a set of invented values. Write natural, varied
English. Invent everything: never copy text from real companies, products, people, laws, websites or published
datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write QUESTION WORDINGS. A program shows two versions of one invented customer-service policy (an original
version and a revised version), the record of one case and the rules for applying a version to a case: each version,
applied on its own, gives the case one outcome. Then it asks one question in your wording. Each item states exactly
what the question must mean; write the number of distinct wordings it asks for, all with that meaning.

Hard rules (a wording that breaks one is thrown away):
1. One question, 8-30 words, ending with "?". No placeholders, no names, no digits or numbers, no dates, no time
   words (today, now, currently, already, yet, soon, later), no hedges (maybe, probably, seems, likely, think).
2. Keep the meaning exactly as the item states it: do not widen, narrow or soften it. The question is about the
   OUTCOME FOR THIS CASE, never about the wording of the policy: use the word "outcome", and "this case" or "the case".
3. Refer to the versions only as "the original version", "the revised version", "both versions", "the two versions"
   or "the revision". Never "new policy", "old policy", "update", "draft" or the like.
4. Never name an outcome and never list answer choices.
5. Negation exactly as the item says. Negation words and cues: not, n't, no, none, nobody, nothing, nowhere, never,
   neither, nor, and also without, fail to, lack, unless, except, false, cannot, hardly. Never start a question with
   "Isn't", "Doesn't", "Don't", "Aren't" or "Wasn't": such leading questions read two ways.
6. Capital letter only on the first word. Vary the structure across your wordings (the case as the subject, the
   revised version as the subject, "Under ...", "Comparing ...", short and long forms).

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "wordings": ["<question 1>", "<question 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qd91158b9bb",
  "brief": {
   "meaning": "yes/no, the negated form of asking whether the revision alters this case's outcome: yes exactly when the outcome stays as it was. Put exactly one 'not' or 'n't' on the verb of altering (change, alter, give another outcome), inside the question (e.g. 'Is it true that ... does not ...?' or 'Does ... not ...?'); no other negation word or cue",
   "style": "phrased as a check made by an auditor who reads both documents side by side; plain words; wordings unlike common phrasings",
   "how_many": 8
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "no placeholders"
  ]
 },
 {
  "qid": "q77eb6d4fe1",
  "brief": {
   "meaning": "yes/no with a double negation whose meaning is positive: it asks whether it is untrue that the revision leaves this case's outcome as it was, so yes exactly when the two outcomes differ. Use exactly two negation words from: not, n't, no, never, nothing (e.g. 'Is it not true that ... makes no difference to the outcome ...?' or 'Is it not the case that ... leaves the outcome with no change ...?'), both in the one sentence, and no other negation cue (no fail to, without, false, unless)",
   "style": "phrased as a check made by an auditor who reads both documents side by side; plain words; wordings unlike common phrasings",
   "how_many": 8
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "no placeholders"
  ]
 },
 {
  "qid": "q0a5f58f298",
  "brief": {
   "meaning": "yes/no: does this case get one and the same outcome under both versions? Yes exactly when the two outcomes are equal. Use a positive word for equality (same, identical, unchanged, alike, equal); no negation word or cue at all",
   "style": "phrased as a check made by an auditor who reads both documents side by side; plain words; wordings unlike common phrasings",
   "how_many": 8
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "no placeholders"
  ]
 },
 {
  "qid": "qeabcef238e",
  "brief": {
   "meaning": "asks which outcome this case gets under the revised version. The reader picks the outcome from a list shown after the question, so the question names no outcome. No negation word or cue at all",
   "style": "phrased as a check made by an auditor who reads both documents side by side; plain words; wordings unlike common phrasings",
   "how_many": 8
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "no placeholders"
  ]
 },
 {
  "qid": "q38ca707608",
  "brief": {
   "meaning": "yes/no: asks whether the revision fails to alter this case's outcome: yes exactly when the outcome stays as it was. Use 'fail to', 'fails to' or 'failed to' exactly once with a verb of altering (change, alter, shift); no other negation word or cue at all (no not, n't, no, never, nothing, without)",
   "style": "phrased as a check made by an auditor who reads both documents side by side; plain words; wordings unlike common phrasings",
   "how_many": 8
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "no placeholders"
  ]
 },
 {
  "qid": "qfd6ab3a306",
  "brief": {
   "meaning": "yes/no: does this case get a different outcome under the revised version than under the original version? Yes exactly when the two outcomes differ. No negation word or cue at all",
   "style": "phrased as a check made by an auditor who reads both documents side by side; plain words; wordings unlike common phrasings",
   "how_many": 8
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "no placeholders"
  ]
 }
]
