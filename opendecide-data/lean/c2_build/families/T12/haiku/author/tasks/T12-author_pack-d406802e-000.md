# T12 authoring task T12-author_pack-d406802e-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/author/answers/T12-author_pack-d406802e-000.json

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
  "qid": "q578d548ada",
  "brief": "Write one pack. The buyer is a florist chain; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "qfedb98aaac",
  "brief": "Write one pack. The buyer is a car repair shop; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q197f0b1d53",
  "brief": "Write one pack. The buyer is a garden centre; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q7ceb9b7f0f",
  "brief": "Write one pack. The buyer is a laundry service; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "qafbd5dce79",
  "brief": "Write one pack. The buyer is a food manufacturer; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "qa42443a75e",
  "brief": "Write one pack. The buyer is a city library; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q53c3055732",
  "brief": "Write one pack. The buyer is a natural history museum; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q4fb1e12741",
  "brief": "Write one pack. The buyer is a bakery chain; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q20af2c175b",
  "brief": "Write one pack. The buyer is a catering company; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q87089b797a",
  "brief": "Write one pack. The buyer is a bicycle maker; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q52392f8a43",
  "brief": "Write one pack. The buyer is a theatre company; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "qcf1b92cf10",
  "brief": "Write one pack. The buyer is a community clinic; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q3d7326e0e1",
  "brief": "Write one pack. The buyer is a school district office; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q65ba7d513c",
  "brief": "Write one pack. The buyer is an IT services firm; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q7dfaacc7db",
  "brief": "Write one pack. The buyer is an office cleaning company; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q00f9102b55",
  "brief": "Write one pack. The buyer is a furniture workshop; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q2939a7c11b",
  "brief": "Write one pack. The buyer is a craft brewery; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "qed2adfe309",
  "brief": "Write one pack. The buyer is a boutique hotel; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q3c6ccb573d",
  "brief": "Write one pack. The buyer is a veterinary clinic; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q511a42e27c",
  "brief": "Write one pack. The buyer is a research laboratory; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "qe9744faa81",
  "brief": "Write one pack. The buyer is a print works; its currency is USD. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "qffbdacd01d",
  "brief": "Write one pack. The buyer is a dental practice; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q30e1d349f2",
  "brief": "Write one pack. The buyer is a facilities management group; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "q9305303d26",
  "brief": "Write one pack. The buyer is a building contractor; its currency is EUR. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 },
 {
  "qid": "qccdd97ea66",
  "brief": "Write one pack. The buyer is a field services contractor; its currency is GBP. Answer field: \"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this task must differ from each other."
 }
]
