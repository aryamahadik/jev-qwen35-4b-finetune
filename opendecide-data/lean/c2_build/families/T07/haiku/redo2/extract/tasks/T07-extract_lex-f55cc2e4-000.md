# T07 redo2 extraction task T07-extract_lex-f55cc2e4-000 (kind extract_lex; read redo2-r2)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/redo2/extract/answers/T07-extract_lex-f55cc2e4-000.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 50 objects: one per item below, each item answered once.
- Each object has exactly two keys: "qid" and "meaning". No other keys.
- "qid": copy the item's qid exactly. The qids of this task: q40fa5bc872, q2236cc6dae, q9bf3f58480, qd39e476e37, q6935de9824, qd7ab2c0118, q5601b36ef2, qe8bccb5370, q6d8ed1c817, q6955e156c2, qc6a8123633, q668beab3e1, qbbfa5ef99a, q51d7c739fa, qbde2a7d7f1, q6ba98c4164, q4db0bac05d, qfa859b8c1c, qcf105c1517, q6a819a2625, qddb96cd1fb, qfaba0da05b, q0a903d0b1d, qe11a7e6a7e, q7d0d36b69d, q711fb41973, q6a4bce5b7f, qf5bf9ee67f, qd99434f6e6, q52388733bd, q014dbeccaf, qa653e96abf, qc27accea64, qc714a97b73, q1d51ca8fe3, q740bd76b72, q5c9fa0620c, q6e619f2f29, q0a8e28306b, q84c6586e52, qc6de9fbf9f, q93e6af1415, q56ba448658, qb2f4beb946, qa06396a5ae, qa4486de2be, q87ef83056f, q6b2b1b8196, qa8cd4fa307, q75bc63c8ae.
- "meaning": one of the item's "choices", copied character for character.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments.
Literal shape: [{"qid": "q40fa5bc872", "meaning": "<one choice, copied exactly>"}, ...]

Task kind: extract_lex; read redo2-r2; items: 50; outputs expected: 50.

## Instructions

TASK: NAME THE MEANING OF EACH SHORT TEXT.

Each item has a "text" (one short sentence or one question, with a sample value already filled in) and a list of
"choices" (meanings). For each item, read the text on its own and pick the single choice whose meaning the text
expresses.

Rules:
- Copy the chosen choice exactly, character for character, as the "meaning" value. Do not change, shorten, translate
  or combine choices, and do not write a new meaning.
- If two choices seem close, pick the closer one. Always pick exactly one choice.
- Judge each item on its own. Do not compare it with other items, and do not use any other file or source.
- The text is the only evidence.

Output: one JSON array with exactly one object per item, keyed by the item's "qid":
[{"qid": "...", "meaning": "..."}]
No other keys, no comments, no text outside the JSON.
Write the whole answer with the Write tool to the ANSWER FILE named in your task file, and nowhere else.

## Items (50; answer every item, keyed by its qid)

```json
[
 {
  "qid": "q40fa5bc872",
  "text": "Which headline offers does order ORD-792364 from Kofi Asante truly get, by the terms set out in what the advertisement says?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q2236cc6dae",
  "text": "Under the promotion's terms, will order ORD-896637 from Lena Whitcombe lose out on double reward points, as the footnotes state?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q9bf3f58480",
  "text": "Items with open box status fall outside this benefit.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "qd39e476e37",
  "text": "Excludes all items with clearance status.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q6935de9824",
  "text": "Items that hold the clearance status are excluded from the main benefit.",
  "choices": [
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qd7ab2c0118",
  "text": "Do the promotion's footnotes show that order ORD-987814 placed by Hugo Lindqvist forfeits free returns?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q5601b36ef2",
  "text": "Every item priced as refurbished is excluded from this offer.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qe8bccb5370",
  "text": "Under the advertisement's conditions, taken in general, does order ORD-608568 from Selin Yilmaz lose out on double reward points?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q6d8ed1c817",
  "text": "Which headline offers from the advertisement and its fine print actually reach customer Nadia Haddad on order ORD-535522?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q6955e156c2",
  "text": "Does order ORD-183992 from Priya Raman lose out on free installation according to the advertisement and its fine print?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qc6a8123633",
  "text": "Which of the headline offers that what the advertisement says lists does order ORD-836141 from Ravi Anand truly get?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q668beab3e1",
  "text": "Items whose status is clearance are excluded.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "qbbfa5ef99a",
  "text": "Does order ORD-343206 from Clara Voss forfeit free gift wrapping under the advertisement and its fine print?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q51d7c739fa",
  "text": "Taking the promotion's terms and footnotes into account, has order ORD-304960 from Jonah Pryce lost out on free gift wrapping?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "qbde2a7d7f1",
  "text": "Which of the headline offers does order ORD-627243 from Jonah Pryce truly get under the advertisement and its fine print?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q6ba98c4164",
  "text": "For members at Plus or lower.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount"
  ]
 },
 {
  "qid": "q4db0bac05d",
  "text": "Do the advertisement's conditions, in general, mean that order ORD-215851 from Ines Duarte forfeits free gift wrapping?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "qfa859b8c1c",
  "text": "For membership levels up to Premier and below.",
  "choices": [
   "the order subtotal must be at least the named amount",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "qcf105c1517",
  "text": "Looking at the advertisement and its fine print, which condition attached to free assembly does customer Hugo Lindqvist, on order ORD-994434, miss, if any?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q6a819a2625",
  "text": "Under the promo's footnotes, does order ORD-907817 from Felix Moreau forfeit free gift wrapping?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "qddb96cd1fb",
  "text": "Judging by what the advertisement says, will order ORD-470155 from Clara Voss forfeit the price match?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qfaba0da05b",
  "text": "According to the promotion's footnotes, does order ORD-925392 placed by Kofi Asante lose out on free assembly?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q0a903d0b1d",
  "text": "Under the advertisement's conditions in general, does order ORD-257680 placed by Selin Yilmaz lose out on free shipping?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qe11a7e6a7e",
  "text": "Reading closely what the advertisement says, has the order ORD-883392 from Dana Okafor lost out on the price match?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q7d0d36b69d",
  "text": "Given the advertisement and its fine print, will order ORD-327322 from Felix Moreau lose out on free gift wrapping?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q711fb41973",
  "text": "Restricted to members at Green and below.",
  "choices": [
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "q6a4bce5b7f",
  "text": "Restricted to members at the Blue level and lower.",
  "choices": [
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "qf5bf9ee67f",
  "text": "Checking the advertisement and its fine print, which of its headline offers does customer Ines Duarte truly receive on order ORD-506295?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "qd99434f6e6",
  "text": "Which condition attached to free assembly in the advertisement and its fine print does order ORD-583138 from Nadia Haddad miss, if any?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q52388733bd",
  "text": "Reserved for members at Plus or below.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "q014dbeccaf",
  "text": "Given the advertisement's conditions in general, does order ORD-211233 from Nadia Haddad forfeit the lifetime warranty?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qa653e96abf",
  "text": "Taking the advertisement and its fine print into account, has order ORD-733909 from Dana Okafor lost out on free returns?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qc27accea64",
  "text": "According to what the advertisement says, which condition attached to free gift wrapping does order ORD-161167 from Kofi Asante miss, if any?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "qc714a97b73",
  "text": "Only items with refurbished status are excluded from the main benefit.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q1d51ca8fe3",
  "text": "Given the advertisement and its fine print, which of its headline offers does order ORD-928142, placed by Jonah Pryce, really get?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q740bd76b72",
  "text": "Looking at the advertisement and its fine print, does order ORD-387736, placed by Felix Moreau, forfeit the price match?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q5c9fa0620c",
  "text": "Taking into account what the advertisement says, which condition attached to free returns does customer Nadia Haddad on order ORD-527752 miss, if any?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q6e619f2f29",
  "text": "Items marked with the open box status fall outside the benefit set out here.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q0a8e28306b",
  "text": "Does what the advertisement says mean that order ORD-438790 from Priya Raman forfeits free gift wrapping?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q84c6586e52",
  "text": "Excludes items with clearance status.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qc6de9fbf9f",
  "text": "Limited to membership at the Plus level or below.",
  "choices": [
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "q93e6af1415",
  "text": "Items priced as final sale are excluded.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "only items in the named product category get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q56ba448658",
  "text": "Measured against the promo's footnotes, does order ORD-601282 from Owen Mensah lose out on free installation?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "qb2f4beb946",
  "text": "Applies to members of the Basic level or lower.",
  "choices": [
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "qa06396a5ae",
  "text": "Which condition, if any, tied to the lifetime warranty in what the advertisement says does order ORD-954087 from Ravi Anand miss?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "qa4486de2be",
  "text": "Measured against the advertisement and its fine print, does order ORD-676900 from Clara Voss lose out on the lifetime warranty?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q87ef83056f",
  "text": "Limited to members at the Gold level or lower.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be at least the named amount",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "q6b2b1b8196",
  "text": "Reserved for the Green level and lower.",
  "choices": [
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "qa8cd4fa307",
  "text": "According to what the advertisement says, which of its headline offers does order ORD-605719 from Owen Mensah actually get?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q75bc63c8ae",
  "text": "Under the promotion's terms and footnotes, does order ORD-940836 placed by Clara Voss forfeit the price match?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 }
]
```
