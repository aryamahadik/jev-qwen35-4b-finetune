# T07 redo2 extraction task T07-extract_lex-f2fb351a-000 (kind extract_lex; read redo2-r1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/redo2/extract/answers/T07-extract_lex-f2fb351a-000.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 50 objects: one per item below, each item answered once.
- Each object has exactly two keys: "qid" and "meaning". No other keys.
- "qid": copy the item's qid exactly. The qids of this task: qa1cd5c3609, q88accfaf2d, q78dd48b66c, q4c16630c71, qe63e126b1d, q8a72dba914, q2a320c3ce2, q1fecd26c6a, qd1e5a705a6, q3453e7ec4e, q150eeeb83f, q70e2203c6c, q01821dabbe, qbe2eb8a240, q721dd7736c, q71a713283a, q573528d980, qc9f9988c86, q2c1c5c7c81, qa3d05f9d3c, qdca5afd87e, q79f227b987, q4ad046719e, qc4de39f68a, q9c84b883d9, q78315da6e9, q951f81849d, q0fc203b46e, q0c0a0bf673, q4c4b2ed682, qb66a88be27, qe2a5a59f24, q144d55595c, q2f426a0669, q61b77dda0c, q33487d4067, qb2fbb992ad, qa4c98b2f6b, qa55b3b4a8f, q4b1c7f82d7, q8ecd96d40c, q3795b4c9ae, qe45f7cba43, q4842fd25d8, q7d9993e306, qeef7da4ef2, q159d64bce3, q2130fa857e, q0f845738df, qaa9098eac4.
- "meaning": one of the item's "choices", copied character for character.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments.
Literal shape: [{"qid": "qa1cd5c3609", "meaning": "<one choice, copied exactly>"}, ...]

Task kind: extract_lex; read redo2-r1; items: 50; outputs expected: 50.

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
  "qid": "qa1cd5c3609",
  "text": "Excludes items with clearance status.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q88accfaf2d",
  "text": "Checking the advertisement and its fine print, which of its headline offers does customer Ines Duarte truly receive on order ORD-506295?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q78dd48b66c",
  "text": "Measured against the promo's footnotes, does order ORD-601282 from Owen Mensah lose out on free installation?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q4c16630c71",
  "text": "Each item bearing the refurbished status is withheld from the main benefit.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "qe63e126b1d",
  "text": "Applies to membership at Premier or lower.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "q8a72dba914",
  "text": "Measured against the advertisement and its fine print, does order ORD-676900 from Clara Voss lose out on the lifetime warranty?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q2a320c3ce2",
  "text": "According to the promotion's footnotes, does order ORD-925392 placed by Kofi Asante lose out on free assembly?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q1fecd26c6a",
  "text": "Which headline offers does customer Aiko Brandt on order ORD-743546 truly receive, given what the advertisement says?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "qd1e5a705a6",
  "text": "Given the advertisement's conditions in general, does order ORD-211233 from Nadia Haddad forfeit the lifetime warranty?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q3453e7ec4e",
  "text": "Items with open box status fall outside this benefit.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q150eeeb83f",
  "text": "Under the promotion's terms, will order ORD-896637 from Lena Whitcombe lose out on double reward points, as the footnotes state?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q70e2203c6c",
  "text": "Looking at the advertisement and its fine print, does order ORD-387736, placed by Felix Moreau, forfeit the price match?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q01821dabbe",
  "text": "Items at the final sale pricing status sit outside this promotion.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "qbe2eb8a240",
  "text": "Taking the advertisement and its fine print into account, has order ORD-733909 from Dana Okafor lost out on free returns?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q721dd7736c",
  "text": "Items marked with the open box status fall outside the benefit set out here.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "q71a713283a",
  "text": "Which headline offers does order ORD-792364 from Kofi Asante truly get, by the terms set out in what the advertisement says?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q573528d980",
  "text": "Does order ORD-183992 from Priya Raman lose out on free installation according to the advertisement and its fine print?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "qc9f9988c86",
  "text": "Limited to members at the Gold level or lower.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount"
  ]
 },
 {
  "qid": "q2c1c5c7c81",
  "text": "Taking the promotion's terms and footnotes into account, has order ORD-304960 from Jonah Pryce lost out on free gift wrapping?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qa3d05f9d3c",
  "text": "Which condition, if any, tied to the lifetime warranty in what the advertisement says does order ORD-954087 from Ravi Anand miss?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qdca5afd87e",
  "text": "Reading closely what the advertisement says, has the order ORD-883392 from Dana Okafor lost out on the price match?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q79f227b987",
  "text": "Every item priced as refurbished is excluded from this offer.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "q4ad046719e",
  "text": "Items priced as final sale are excluded.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qc4de39f68a",
  "text": "Items that hold the clearance status are excluded from the main benefit.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q9c84b883d9",
  "text": "Reserved for the Green level and lower.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be at least the named amount",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "q78315da6e9",
  "text": "According to what the advertisement says, which of its headline offers does order ORD-605719 from Owen Mensah actually get?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q951f81849d",
  "text": "Which condition attached to the price match does the order ORD-856502 placed by Felix Moreau miss, if any, under what the advertisement says?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q0fc203b46e",
  "text": "Which condition attached to free assembly in the advertisement and its fine print does order ORD-583138 from Nadia Haddad miss, if any?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q0c0a0bf673",
  "text": "Under the advertisement and its fine print, which condition attached to free returns does order ORD-850453 from Felix Moreau miss, if any?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q4c4b2ed682",
  "text": "Restricted to members at the Blue level and lower.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "qb66a88be27",
  "text": "Under the promotion's terms and footnotes, does order ORD-940836 placed by Clara Voss forfeit the price match?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "qe2a5a59f24",
  "text": "For members at Plus or lower.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "q144d55595c",
  "text": "Taking into account what the advertisement says, which condition attached to free returns does customer Nadia Haddad on order ORD-527752 miss, if any?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q2f426a0669",
  "text": "Judging by what the advertisement says, will order ORD-470155 from Clara Voss forfeit the price match?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q61b77dda0c",
  "text": "Only items with refurbished status are excluded from the main benefit.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "q33487d4067",
  "text": "Items at pre-order pricing are withheld from this benefit.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qb2fbb992ad",
  "text": "According to what the advertisement says, which condition attached to free gift wrapping does order ORD-161167 from Kofi Asante miss, if any?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "qa4c98b2f6b",
  "text": "Does what the advertisement says mean that order ORD-438790 from Priya Raman forfeits free gift wrapping?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "qa55b3b4a8f",
  "text": "Under the advertisement's conditions in general, does order ORD-257680 placed by Selin Yilmaz lose out on free shipping?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q4b1c7f82d7",
  "text": "If any, which condition in the advertisement and its fine print attached to the lifetime warranty does order ORD-707886 from Clara Voss miss?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q8ecd96d40c",
  "text": "Reserved for members at Plus or below.",
  "choices": [
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "q3795b4c9ae",
  "text": "For membership levels up to Premier and below.",
  "choices": [
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "qe45f7cba43",
  "text": "Given the advertisement and its fine print, which of its headline offers does order ORD-928142, placed by Jonah Pryce, really get?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q4842fd25d8",
  "text": "Given the advertisement and its fine print, will order ORD-327322 from Felix Moreau lose out on free gift wrapping?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q7d9993e306",
  "text": "Applies to members up to Silver or lower.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount"
  ]
 },
 {
  "qid": "qeef7da4ef2",
  "text": "Items whose status is clearance are excluded.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "q159d64bce3",
  "text": "Under the advertisement and its fine print, does order ORD-436666 from Mira Castell lose out on the price match?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q2130fa857e",
  "text": "Items whose status is final sale sit outside this offer.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q0f845738df",
  "text": "Limited to membership at the Plus level or below.",
  "choices": [
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount"
  ]
 },
 {
  "qid": "qaa9098eac4",
  "text": "Looking at the advertisement and its fine print, which condition attached to free assembly does customer Hugo Lindqvist, on order ORD-994434, miss, if any?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit"
  ]
 }
]
```
