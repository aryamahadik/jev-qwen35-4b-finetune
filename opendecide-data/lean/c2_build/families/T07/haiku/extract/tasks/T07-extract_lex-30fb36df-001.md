# T07 extraction task T07-extract_lex-30fb36df-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/extract/answers/T07-extract_lex-30fb36df-001.json

Task kind: extract_lex; read r1; items: 50; outputs expected: 50.

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
  "qid": "q7396087ec3",
  "text": "Going by the ad and its small print, is it true that order INV-20419 from Dana Okafor doesn't get production under the advertised terms?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qe80c689288",
  "text": "Does what the advertisement says, with that headline's small print counted, mean that order INV-20419 from Dana Okafor earns production?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q3c229024cd",
  "text": "Of the promo's headline offers, which does order INV-20419 from Dana Okafor truly get, with footnotes applied?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q93945f4873",
  "text": "Taking the headline and its small print together, does order INV-20419 from Dana Okafor earn production under what the advertisement says?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q8833b4f3ab",
  "text": "Orders dated on or before 28 February 2026 count.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier"
  ]
 },
 {
  "qid": "q018be7c3cc",
  "text": "Applies to order subtotals of $0.00 or more.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "q0c84cb3273",
  "text": "Eligibility is limited to the production category.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "qeac19f4548",
  "text": "Any delivery to production is excluded from this offer.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q64fef471d4",
  "text": "Would it be fair to say it is not the case that Dana Okafor does not get production on order INV-20419 under the advertised terms?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q59e3912767",
  "text": "production items are excluded from this offer.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "q0c3e9039f8",
  "text": "Measured against the advertised terms in full, does order INV-20419 from Dana Okafor lose out on production?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q3981231fd8",
  "text": "Valid for orders placed on or after 28 February 2026.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier"
  ]
 },
 {
  "qid": "qfe856ae580",
  "text": "Offer by offer, which headline offers does what the advertisement says, small print included, actually give Dana Okafor on order INV-20419?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "qefde08219a",
  "text": "Going by the advertisement and its fine print, which condition attached to production does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q7c32640b8b",
  "text": "Does order INV-20419 from Dana Okafor forfeit production under the advertised terms, as set out by the advertisement and its fine print?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q3c0f204b59",
  "text": "Does order INV-20419 from Dana Okafor come with production under what the advertisement says, headline and small print included?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q506079d004",
  "text": "For order INV-20419 placed by Dana Okafor, which headline offers does the advertisement and its fine print actually allow, offer by offer?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "qa39720fd8e",
  "text": "Covers the production product category only.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q9d82e9a97c",
  "text": "Any item priced as production sits outside the headline benefit.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "qb2316d6c90",
  "text": "Which headline offers from the promo does Dana Okafor on order INV-20419 actually receive, footnotes considered?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q2b00cdf424",
  "text": "Is it not accurate to say that Dana Okafor does not get production with order INV-20419 under the advertised terms?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q1fdd2895b7",
  "text": "Taking order INV-20419 from Dana Okafor and reading what the advertisement says, which condition in the small print attached to production does it miss, if any?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qdac6b9245c",
  "text": "Judging by the promo's footnotes, does order INV-20419 from Dana Okafor fail to get production?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "qc046bdf517",
  "text": "Does the ad, with its small print taken into account, mean that Dana Okafor earns production on order INV-20419?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "qedee3dec9d",
  "text": "Under the advertised terms, does order INV-20419 from Dana Okafor go short of production according to the advertisement and its fine print?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qee45d2433e",
  "text": "Valid on orders over $0.00.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "qc217f45bd6",
  "text": "According to the promo's footnotes, does Dana Okafor go short of production with order INV-20419?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qa5f9a85805",
  "text": "The order subtotal must be at least $0.00 for this offer to apply.",
  "choices": [
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "q31dd1d7040",
  "text": "Reading the advertisement and its fine print, is it true that the order INV-20419 from Dana Okafor doesn't get production under the advertised terms?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qaf18a12c56",
  "text": "Is it true that order INV-20419 from Dana Okafor doesn't get production under the promo's footnotes?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "qf630eb9f9b",
  "text": "Goods filed under a different category from production fall outside the benefit.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qa726f5ce6d",
  "text": "For order INV-20419 from Dana Okafor, which headline offers hold up under the ad and its small print, offer by offer?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q48ed5b4b34",
  "text": "Orders must be placed earlier than 28 February 2026.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier"
  ]
 },
 {
  "qid": "qd49a2b3df2",
  "text": "For order INV-20419 from Dana Okafor, which condition in the small print attached to production does it miss, if any, as the advertisement says?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q39b7f7cba8",
  "text": "Applies to orders placed ahead of 28 February 2026.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed on the named date or earlier",
   "the order must be placed strictly before the named date"
  ]
 },
 {
  "qid": "qd4d9ad52b2",
  "text": "Placed before 28 February 2026 counts; that very day is excluded.",
  "choices": [
   "the order must be placed on the named date or earlier",
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or later"
  ]
 },
 {
  "qid": "qadc3d9c844",
  "text": "Measured against the advertised terms in full, does order INV-20419 from Dana Okafor fail to secure production?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q38fd25c6c2",
  "text": "Under the advertised terms, which condition in the small print attached to production does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q4fa76e7cbb",
  "text": "Isn't it true that order INV-20419 from Dana Okafor doesn't get production under the promo's footnotes?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q7f12e8eb64",
  "text": "Reserved for members ranked production or higher.",
  "choices": [
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "qdcb481c574",
  "text": "The headline benefit stops short of delivery to production.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "qd7958a6a74",
  "text": "Based on what the advertisement says, does order INV-20419 from Dana Okafor fail to get production under the advertised terms?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q3b613aadd5",
  "text": "For order INV-20419 from Dana Okafor, which headline offers does what the advertisement says actually grant, checked offer by offer against small print?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "qf102fdf310",
  "text": "Qualifying orders: subtotal $0.00 or more.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount"
  ]
 },
 {
  "qid": "qfeec34c87d",
  "text": "Under the promotion's footnotes, does order INV-20419 from Dana Okafor fail to secure production?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "qaca125bf71",
  "text": "Products assigned to the production category are excluded.",
  "choices": [
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q5f20a1d175",
  "text": "Does order INV-20419 from Dana Okafor come with production under the ad and its small print?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "qed7eddfe9b",
  "text": "Does order INV-20419 from Dana Okafor forfeit production under the advertised terms, as those terms are written?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q8b5e1da82f",
  "text": "Does Dana Okafor get production on order INV-20419 when the advertised terms, with the headline and its small print, are applied?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "qebdd6879b5",
  "text": "Under the advertised terms, and going by what the advertisement says, is it true that order INV-20419 from Dana Okafor doesn't get production?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 }
]
