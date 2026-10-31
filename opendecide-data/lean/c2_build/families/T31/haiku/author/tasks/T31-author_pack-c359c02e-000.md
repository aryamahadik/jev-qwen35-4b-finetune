# T31 authoring task T31-author_pack-c359c02e-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_pack-c359c02e-000.json

Task kind: author_pack; items: 36; answers expected: 36 (one per item, each with its qid).

You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given moment: sign-off requests in companies, and software agents (AI assistants working through chains of sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write AGENT PERMISSION PACKS. Each item gives an invented setting where software agents work;
write one pack for it as a JSON object {"scopes": [...], "tasks": [...], "agents": [...]}:
  scopes   10-12 distinct permission scope ids of the form resource.action, lowercase letters only around one dot
           (for example "rooms.book", "invoices.send"); resources and actions vary;
  tasks    exactly 4 distinct lowercase singular noun phrases (1-4 words) naming tasks an agent does in that setting
           (for example "invoice run"); no task contains another;
  agents   exactly 6 distinct agent ids: lowercase words joined by hyphens, 2-3 parts (for example "stock-checker").

Hard rules: invented and generic (no real company, product, brand, person or place names); no digits or number words;
no word in any value may be a negation (not, no, none, never, nor, deny, lack, without ...); every pack in this task
clearly different from the others.

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "pack": {...}}.
Nothing else in the file.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q27bac6f4bf",
  "brief": "Setting: a software team's release process."
 },
 {
  "qid": "q25f12ef426",
  "brief": "Setting: a co-op grocery."
 },
 {
  "qid": "qedad86d5c6",
  "brief": "Setting: a museum shop."
 },
 {
  "qid": "q7d3e1088c0",
  "brief": "Setting: a university admissions office."
 },
 {
  "qid": "qf6117933ef",
  "brief": "Setting: an insurance broker's claims desk."
 },
 {
  "qid": "qb90f5d82af",
  "brief": "Setting: a marketing agency."
 },
 {
  "qid": "q2271375bc3",
  "brief": "Setting: a design studio's client work."
 },
 {
  "qid": "q03f6d05169",
  "brief": "Setting: a utility's field service."
 },
 {
  "qid": "q58303ede64",
  "brief": "Setting: a photography studio."
 },
 {
  "qid": "qd0e05a200f",
  "brief": "Setting: a farm shop's deliveries."
 },
 {
  "qid": "qa6644bce4a",
  "brief": "Setting: a clinic's appointment desk."
 },
 {
  "qid": "q39a94db922",
  "brief": "Setting: a gym's member desk."
 },
 {
  "qid": "qfcaffb7ee9",
  "brief": "Setting: an IT helpdesk."
 },
 {
  "qid": "q63fa0f27f7",
  "brief": "Setting: a freight forwarder."
 },
 {
  "qid": "q5cadc1afd3",
  "brief": "Setting: a city council's permits office."
 },
 {
  "qid": "q1b7925a67f",
  "brief": "Setting: a restaurant group's purchasing."
 },
 {
  "qid": "q90b0f2ae77",
  "brief": "Setting: a pharmacy's stock control."
 },
 {
  "qid": "qfd2c03dee8",
  "brief": "Setting: a translation agency."
 },
 {
  "qid": "qf05e99316a",
  "brief": "Setting: a hotel's front office."
 },
 {
  "qid": "qef8ddc1216",
  "brief": "Setting: an event venue's bookings."
 },
 {
  "qid": "q54421a9492",
  "brief": "Setting: an e-commerce returns desk."
 },
 {
  "qid": "q91bfdd5543",
  "brief": "Setting: a podcast network."
 },
 {
  "qid": "q6b98d76a9f",
  "brief": "Setting: an HR team's onboarding work."
 },
 {
  "qid": "qd50d3cb64c",
  "brief": "Setting: a home-care provider."
 },
 {
  "qid": "qcf40350525",
  "brief": "Setting: a language school."
 },
 {
  "qid": "q2dc6ad668c",
  "brief": "Setting: a bike repair shop."
 },
 {
  "qid": "q38dd85db00",
  "brief": "Setting: a travel agency."
 },
 {
  "qid": "q3ddf0de8f5",
  "brief": "Setting: an online bookshop's operations."
 },
 {
  "qid": "qfa57b53aa7",
  "brief": "Setting: a newsroom's publishing desk."
 },
 {
  "qid": "qc13cd3a498",
  "brief": "Setting: a nonprofit's donor relations."
 },
 {
  "qid": "qbb1ac3386a",
  "brief": "Setting: a recruitment firm."
 },
 {
  "qid": "qe81ddd7ed2",
  "brief": "Setting: a school's timetabling office."
 },
 {
  "qid": "q9011fc80ab",
  "brief": "Setting: a law office's filing."
 },
 {
  "qid": "qe3fb3d2494",
  "brief": "Setting: a research group's data pipeline."
 },
 {
  "qid": "qfad7c229e0",
  "brief": "Setting: a small accounting practice."
 },
 {
  "qid": "qdb1d8f69a9",
  "brief": "Setting: a property management office."
 }
]

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_pack-c359c02e-000.json and nothing else.
