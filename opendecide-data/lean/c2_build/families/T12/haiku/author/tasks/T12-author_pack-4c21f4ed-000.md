# T12 authoring task T12-author_pack-4c21f4ed-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/author/answers/T12-author_pack-4c21f4ed-000.json

Task kind: author_pack; items: 25; outputs expected: 25 (1 per item, answer field "pack").

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

You write vocabulary packs for a synthetic training dataset. Setting: in an accounts-payable (AP) team, a clerk matches a supplier's invoice against the purchase order (PO) and the goods receipt under a written company policy. A program builds every example: it prints the documents, the policy and the question, and it fills every value. Everything you write must be invented: never copy text from real companies, products, people, laws, websites or published datasets. A pack describes one invented buyer organisation and what it buys. In this task you are asked to invent names of organisations, suppliers, products and people: that is allowed here, and a program checks every field and drops a pack that breaks a rule. Each item asks for one pack in the answer field "pack".

PACK SHAPE:
R1. "pack" is one JSON object with exactly these keys: org, currency, prefixes, vendors, items, clerks, approvers.
R2. org: the buyer's name, 2-4 words, every word capitalised, ASCII letters and single spaces only.
R3. currency: copy the code the item gives (USD, EUR or GBP).
R4. prefixes: {"po": ..., "gr": ..., "inv": ...}: three different codes of 2-4 capital ASCII letters that are printed before this buyer's purchase-order numbers, goods-receipt numbers and supplier-invoice numbers (styles like PUR, GRN, SI); never NO, NOT, NOR or NON.
R5. vendors: 3 invented supplier company names that sell these items, 2-4 words each, every word capitalised, ASCII letters and single spaces only, different from each other and from org.
R6. items: 6 different things the buyer orders from these suppliers, each a list [name, unit, lo, hi]. name: 1-3 lower-case words (ASCII letters, single spaces or hyphens; no digits), a plain product name in the plural or as a mass noun (style: "paper towels", "floor wax"). unit: exactly one of bag, bottle, box, carton, case, crate, drum, kit, pack, pallet, ream, roll, set, spool, tube, unit (the unit it is ordered in; it must make sense for the product). lo, hi: integers, the usual price of ONE unit in cents (hundredths of the currency): 200 <= lo < hi, hi <= 4 x lo and hi <= 100000.
R7. clerks: 3 full names of AP clerks; approvers: 2 full names of managers who sign large invoices. A full name is a given name and a family name, each capitalised, ASCII letters only, varied origins, all 5 different; never a famous person and never a word of time, quantity, status or order as a name part (Hope, May, Will, Grace, Best, Young, Early).
R8. Product names are ordinary products: no word about paying, checking, signing or refusing anything, no negation word, and none of the 6 is the start of another.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item, in item order: {"qid": "<the item's qid>", "<answer field>": ...}. Copy each qid exactly; give exactly the number of outputs each item asks for. Valid JSON only (escape an inner double quote as \" and a line break inside a text as \n); no comments, no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "pack": {...}}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "q1fb8ab36b4",
  "brief": "Write one pack. The buyer is an ice cream maker; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q498993923b",
  "brief": "Write one pack. The buyer is a cosmetics maker; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q59ba592a26",
  "brief": "Write one pack. The buyer is a recycling centre; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q3ab30643b7",
  "brief": "Write one pack. The buyer is a coffee roaster; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q293b3d1206",
  "brief": "Write one pack. The buyer is a pet food maker; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "qa57905191b",
  "brief": "Write one pack. The buyer is a ski resort; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q425735563c",
  "brief": "Write one pack. The buyer is an optician chain; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q0064cfa107",
  "brief": "Write one pack. The buyer is a toy maker; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q1dd54a2acf",
  "brief": "Write one pack. The buyer is an architecture studio; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q0627f19eba",
  "brief": "Write one pack. The buyer is an amateur sports club; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q7dc6cbe75a",
  "brief": "Write one pack. The buyer is a film studio; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q06619961d3",
  "brief": "Write one pack. The buyer is a music school; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q37384cd885",
  "brief": "Write one pack. The buyer is a farm cooperative; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q6db9418b18",
  "brief": "Write one pack. The buyer is a gym chain; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q162fdba2c9",
  "brief": "Write one pack. The buyer is a boat yard; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "qaaf1c7528d",
  "brief": "Write one pack. The buyer is a public radio station; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "qdc8dee4bd2",
  "brief": "Write one pack. The buyer is a water utility; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q0b50cfa410",
  "brief": "Write one pack. The buyer is a textile mill; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "qcdb3cefe9c",
  "brief": "Write one pack. The buyer is a winery; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q78f28c9f32",
  "brief": "Write one pack. The buyer is a greenhouse grower; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q3059d14dd6",
  "brief": "Write one pack. The buyer is a university canteen; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "qc9750391ff",
  "brief": "Write one pack. The buyer is a packaging plant; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q4684efb198",
  "brief": "Write one pack. The buyer is a marine supply store; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q26ba68929a",
  "brief": "Write one pack. The buyer is a pottery studio; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q58d966b8be",
  "brief": "Write one pack. The buyer is a pharmacy chain; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 }
]
