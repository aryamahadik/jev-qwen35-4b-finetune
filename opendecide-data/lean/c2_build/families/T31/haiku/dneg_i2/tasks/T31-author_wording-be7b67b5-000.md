# T31 double-negation authoring task T31-author_wording-be7b67b5-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/dneg_i2/answers/T31-author_wording-be7b67b5-000.json

Task kind: author_wording; items: 16; answers expected: 16 (one per item, each with its qid).

This task file is the only file you may open. Do not open, list or search any other file or folder.

You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given moment: sign-off requests in companies, and software agents (AI assistants working through chains of sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write QUESTION WORDINGS about whether a software agent may use a permission scope at the time of a request. A program shows a rule card and a block of records, then asks one
question in your wording. Each item states exactly what the question must mean; write one wording per item, and make
the wordings in this task clearly different from each other.

Placeholders (plain, exactly as written; no grammar helpers inside questions):
  {CANDIDATE}  a person's full name        {REQ_AGENT}  an agent id such as ledger-bot
  {REQ_SCOPE}  a scope id such as invoices.send   {REQ_ID}  the request's reference code
Use each placeholder the item requires exactly once; use {REQ_ID} only where the item allows it (at most once);
use no other placeholder.

Hard rules (a wording that breaks one is thrown away):
1. One question, 6-30 words, ending with "?".
2. Keep the meaning exactly as the item states it: same person, agent or scope, the time of the request, no
   widening, narrowing or softening.
3. Sign-off questions call the role "the accountable (A) role", "the A role" or "the accountable approver"; never
   "responsible", "owner", "manager" or "in charge" (those name other things).
4. Agent questions are about permission at the time of the request (whether the agent may use the scope then),
   never about whether the agent's grant lists the scope.
5. Time: "at the time of the request", "when the request was made", "at that moment", or no time phrase. Never now,
   currently, today, still, already, yet, at present.
6. Negation exactly as the item asks (two cancelling 'not' words with the explicit outer frame the item names). No other negation word anywhere: none of n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, fail to, refuse to, decline to, hardly, barely, scarcely, few, except, unless, false, other than, free of, no longer, rule out, prevent ... from; no contracted negatives.
7. No digits, number words, dates, names or capital letters (except the first word and the placeholders); no hedges
   (maybe, probably, seems, likely). Never list answer choices; never mention any other person, agent or scope.

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "text": "<your
question>"}. Nothing else in the file.

EXACT ANSWER CONTRACT (a checking program drops an entry that breaks it; the entry is lost):
- The answer file holds ONE JSON array of exactly 16 objects, one per item, each exactly {"qid": "<the item's qid>", "text": "<the question>"} with no other key.
- text: one line, 6-30 words, one question ending with exactly one '?', and it starts with the outer frame named in the item's rules (the frame, then the embedded statement).
- text holds the placeholders {REQ_AGENT}, {REQ_SCOPE} each exactly once, written plain with braces; {REQ_ID} at most once, and only when the item allows it. No other placeholder, no grammar helper.
- Exactly two 'not' words in the whole question (the frame's and the one named in the item's rules). No other negation word, no contraction ending in n't, no word that means block, bar, deny, lack, forbid or prevent.
- Valid JSON only: no text before or after the array; write a double quote inside a string as \".
- The 16 questions of this file must differ from one another (no two the same).

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qf279191b68",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: passive voice where natural.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not correct that'",
   "put the second 'not' on 'entitled' ('... is not entitled to use ...')"
  ]
 },
 {
  "qid": "qd1123cda9e",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not correct that'",
   "put the second 'not' on 'permitted' ('... is not permitted to use ...')"
  ]
 },
 {
  "qid": "q10eb6c2518",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: conversational, as a colleague would ask.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not correct that'",
   "put the second 'not' on 'allowed' ('... is not allowed to use ...')"
  ]
 },
 {
  "qid": "q39e0c70d1b",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: precise and slightly technical.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not true that'",
   "put the second 'not' on 'authorised' ('... is not authorised to use ...')"
  ]
 },
 {
  "qid": "q81e87d54d1",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: passive voice where natural.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not true that'",
   "put the second 'not' on 'allowed' ('... is not allowed to use ...')"
  ]
 },
 {
  "qid": "qb4cf376ec3",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: formal, as in an audit checklist.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not true that'",
   "put the second 'not' on 'allowed' ('... is not allowed to use ...')"
  ]
 },
 {
  "qid": "q34b2bc9aa9",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: short (under 14 words).",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not correct that'",
   "put the second 'not' on 'authorised' ('... is not authorised to use ...')"
  ]
 },
 {
  "qid": "q6625ce2f21",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: direct and plain.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not true that'",
   "put the second 'not' on 'permitted' ('... is not permitted to use ...')"
  ]
 },
 {
  "qid": "q8b407b44d4",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: formal, as in an audit checklist.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not correct that'",
   "put the second 'not' on 'entitled' ('... is not entitled to use ...')"
  ]
 },
 {
  "qid": "q5d53f9bdbb",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: direct and plain.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not the case that'",
   "put the second 'not' on 'authorised' ('... is not authorised to use ...')"
  ]
 },
 {
  "qid": "qf47d8ded59",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not true that'",
   "put the second 'not' on 'entitled' ('... is not entitled to use ...')"
  ]
 },
 {
  "qid": "qb3267d9789",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: direct and plain.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not true that'",
   "put the second 'not' on 'permitted' ('... is not permitted to use ...')"
  ]
 },
 {
  "qid": "qa97bc5229f",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: short (under 14 words).",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not true that'",
   "put the second 'not' on 'entitled' ('... is not entitled to use ...')"
  ]
 },
 {
  "qid": "q61bc41df32",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not the case that'",
   "put the second 'not' on 'allowed' ('... is not allowed to use ...')"
  ]
 },
 {
  "qid": "q6f8ab6ea09",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: formal, as in an audit checklist.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not true that'",
   "put the second 'not' on 'allowed' ('... is not allowed to use ...')"
  ]
 },
 {
  "qid": "qea98cb30a0",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope. Style: conversational, as a colleague would ask.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
   "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
   "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)",
   "open with exactly 'Is it not the case that'",
   "put the second 'not' on 'authorised' ('... is not authorised to use ...')"
  ]
 }
]

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/dneg_i2/answers/T31-author_wording-be7b67b5-000.json and nothing else.
