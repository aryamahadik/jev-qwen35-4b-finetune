# T07 extraction task T07-extract_lex-f84eda6f-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/extract/answers/T07-extract_lex-f84eda6f-003.json

Task kind: extract_lex; read r2; items: 50; outputs expected: 50.

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

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qfda3ed1926",
  "text": "Reading the ad and its small print offer by offer, which headline offers does order INV-20419 from Dana Okafor actually get?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q4456e1fd61",
  "text": "Which ad condition attached to production does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q155b73abfe",
  "text": "Reading what the advertisement says, small print included, offer by offer, which headline offers does order INV-20419 from Dana Okafor actually get?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q01fa986046",
  "text": "Does what the advertisement says, with that headline's small print counted, mean that order INV-20419 from Dana Okafor earns production?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "qe041a8553c",
  "text": "Products sitting in any category besides production fall outside this offer.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items in the named product category are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q2b746f50a1",
  "text": "Is it not true that the order INV-20419 from Dana Okafor does not get production, judging by the advertisement and its fine print?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qc6863b70ea",
  "text": "Which headline offers does order INV-20419 from Dana Okafor actually get when the advertisement and its fine print are applied offer by offer?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q895cbeb38a",
  "text": "Orders delivered to production are excluded.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q8636822b06",
  "text": "Members ranked production and above are the only ones covered.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be at least the named amount",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "qd5b34a3653",
  "text": "Applies to order subtotals of $0.00 or more.",
  "choices": [
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "q21f8a79155",
  "text": "Eligibility is limited to members at production level or lower.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be at least the named amount",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "q9b8fc1a030",
  "text": "Does order INV-20419 from Dana Okafor end up shut out of production under the advertised terms, per the ad and its small print?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q870f5dcc00",
  "text": "Orders submitted on or before 28 February 2026 are accepted.",
  "choices": [
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or later",
   "the order must be placed on the named date or earlier"
  ]
 },
 {
  "qid": "qb9d7e0fd81",
  "text": "Orders must be placed on or after 28 February 2026.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier"
  ]
 },
 {
  "qid": "q21fbb2d651",
  "text": "Delivery to production only.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "qb63d04074d",
  "text": "Could you say which of the advertised terms Dana Okafor actually gets on order INV-20419 while the small print is checked offer by offer?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q099f4b5d26",
  "text": "Qualifying orders: subtotal $0.00 or more.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "q14d06b58fe",
  "text": "Orders must be placed earlier than 28 February 2026.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier"
  ]
 },
 {
  "qid": "q4da0fc1c12",
  "text": "Items listed at production pricing are excluded from the benefit.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "q775f74c2b2",
  "text": "The benefit is withheld from anything with production pricing.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q9febf3b0fd",
  "text": "Excludes the production category.",
  "choices": [
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "q95c642a309",
  "text": "Which headline offers from the ad and its small print does order INV-20419 placed by Dana Okafor actually get, offer by offer?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q73ebd368e9",
  "text": "According to the promo's footnotes, does Dana Okafor go short of production with order INV-20419?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q43d2e9025c",
  "text": "Headline benefit applies to orders with delivery in production only.",
  "choices": [
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "q6bf87fffde",
  "text": "Under the advertised terms, is it true that order INV-20419 from Dana Okafor does not get production?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q9a5b7fa27f",
  "text": "An order qualifies with a subtotal of $0.00 or more.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount"
  ]
 },
 {
  "qid": "q643a855f29",
  "text": "Any order placed on 28 February 2026 and beyond is accepted.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier"
  ]
 },
 {
  "qid": "qd9d673a44c",
  "text": "For order INV-20419 from Dana Okafor, which headline offers does what the advertisement says actually grant, checked offer by offer against small print?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "qc0d62699bf",
  "text": "Earlier orders are accepted, and so is the date 28 February 2026 itself.",
  "choices": [
   "the order must be placed on the named date or earlier",
   "the order must be placed on the named date or later",
   "the order must be placed strictly before the named date"
  ]
 },
 {
  "qid": "qf074eb1ae9",
  "text": "Valid: any order taken on or before 28 February 2026.",
  "choices": [
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or later",
   "the order must be placed on the named date or earlier"
  ]
 },
 {
  "qid": "qea51435e9c",
  "text": "Does order INV-20419 from Dana Okafor go short of production under the advertised terms, judging by what the advertisement says?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qd1352ac228",
  "text": "Does Dana Okafor's order INV-20419 miss which ad condition attached to production, if any?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q28928d7342",
  "text": "Any delivery to production is excluded from this offer.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q09cfcd6f5a",
  "text": "Placed on or after 28 February 2026, the order qualifies.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed on the named date or earlier",
   "the order must be placed strictly before the named date"
  ]
 },
 {
  "qid": "qb185387bf1",
  "text": "Which promo headline offers does order INV-20419 from Dana Okafor actually get, footnotes applied?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q87c2a572fc",
  "text": "Is it the case that order INV-20419 from Dana Okafor fails to earn production under the promotion?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q1d718d69a4",
  "text": "Which condition in the ad's small print attached to production does Dana Okafor's order INV-20419 miss, if any?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q4f0a185bfd",
  "text": "Taking the headline and its small print together, does order INV-20419 from Dana Okafor earn production under what the advertisement says?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q1651fe8cbd",
  "text": "Reading what the advertisement says, with its headline and small print together, does order INV-20419 from Dana Okafor receive production?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q8c3c696bd4",
  "text": "Would you say it is not the case that Dana Okafor does not get production on order INV-20419 when the advertisement and its fine print are read?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q2044aab325",
  "text": "Delivery to production sits outside the headline benefit.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items in the named product category are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qe75aff3359",
  "text": "For order INV-20419 from Dana Okafor, does it fail to receive production under the advertised terms, as the ad and its small print describe?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q338de0595e",
  "text": "Order subtotal strictly more than $0.00.",
  "choices": [
   "the order subtotal must be at least the named amount",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "q410e3fb4bd",
  "text": "Items sold as production are excluded.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "q55db47bf37",
  "text": "Qualifying subtotal: strictly above $0.00.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "q5dbe59b981",
  "text": "Going by the advertisement and its fine print, does order INV-20419 from Dana Okafor end up shut out of production under the advertised terms?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q942216410a",
  "text": "Valid on orders over $0.00.",
  "choices": [
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "qb5debda225",
  "text": "Is it the case that order INV-20419 from Dana Okafor earns production under the advertised terms, headline and small print included?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q41022e6320",
  "text": "Valid only for orders delivered to production.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q07ad15ab76",
  "text": "Reading the ad and its small print together, does order INV-20419 from Dana Okafor fail to secure production under the advertised terms?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 }
]
