# T29 authoring task T29-author_pack-1f1a2d6e-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/author/answers/T29-author_pack-1f1a2d6e-000.json

Task kind: author_pack; items: 14; outputs expected: 140.

You are writing short pieces of text for a synthetic training dataset about software agents that follow
written company policies. Everything you write is either a reusable template (a program later fills each {SLOT}
placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy
text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: invent ACTION NAMES for an agent's tool catalog. Each item gives one effect class and one tone; write the
number of names it asks for.

Rules for every name:
- snake_case: 2-4 lowercase English words joined by underscores, letters only (e.g. "clear_old_notifications").
- The name describes a single tool action whose real effect is the item's effect class (a name for the class
  "deletes data" removes something; "pays money out" sends money; "changes access rights" changes who can use what).
- Tone "routine" = the name sounds everyday and harmless. Tone "drastic" = the name sounds sweeping, risky or severe.
- Never name an environment (production, staging, test, sandbox), a team or department, a kind of data class
  (personal, public, internal), a quantity or amount, a person, a time, a place, or a company.
- No negation word or prefix (not, no, never, un-, non-, dis-), no digits, no brand names.
- All names in your whole answer are distinct.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "names": ["<name 1>", "<name 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qcef4778cb4",
  "brief": {
   "effect_class": "changes data",
   "tone": "routine",
   "how_many": 10
  }
 },
 {
  "qid": "qb009fab6d2",
  "brief": {
   "effect_class": "exports data",
   "tone": "drastic",
   "how_many": 10
  }
 },
 {
  "qid": "q9f16bef779",
  "brief": {
   "effect_class": "deletes data",
   "tone": "drastic",
   "how_many": 10
  }
 },
 {
  "qid": "q292de585cd",
  "brief": {
   "effect_class": "sends messages",
   "tone": "routine",
   "how_many": 10
  }
 },
 {
  "qid": "qc3ddad6c27",
  "brief": {
   "effect_class": "changes access rights",
   "tone": "drastic",
   "how_many": 10
  }
 },
 {
  "qid": "q70802cb526",
  "brief": {
   "effect_class": "changes access rights",
   "tone": "routine",
   "how_many": 10
  }
 },
 {
  "qid": "qb46d64cc36",
  "brief": {
   "effect_class": "sends messages",
   "tone": "drastic",
   "how_many": 10
  }
 },
 {
  "qid": "qd862aa8eda",
  "brief": {
   "effect_class": "pays money out",
   "tone": "drastic",
   "how_many": 10
  }
 },
 {
  "qid": "qf7f623a78b",
  "brief": {
   "effect_class": "creates data",
   "tone": "drastic",
   "how_many": 10
  }
 },
 {
  "qid": "q700f040e06",
  "brief": {
   "effect_class": "pays money out",
   "tone": "routine",
   "how_many": 10
  }
 },
 {
  "qid": "qc0a3e60f29",
  "brief": {
   "effect_class": "changes data",
   "tone": "drastic",
   "how_many": 10
  }
 },
 {
  "qid": "qff729d84ad",
  "brief": {
   "effect_class": "creates data",
   "tone": "routine",
   "how_many": 10
  }
 },
 {
  "qid": "qd08a61d8dd",
  "brief": {
   "effect_class": "exports data",
   "tone": "routine",
   "how_many": 10
  }
 },
 {
  "qid": "qc52c8e1fc8",
  "brief": {
   "effect_class": "deletes data",
   "tone": "routine",
   "how_many": 10
  }
 }
]
