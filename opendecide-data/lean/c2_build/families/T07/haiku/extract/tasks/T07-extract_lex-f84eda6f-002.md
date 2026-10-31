# T07 extraction task T07-extract_lex-f84eda6f-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/extract/answers/T07-extract_lex-f84eda6f-002.json

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
  "qid": "q6df821addb",
  "text": "Stock flagged as production sits outside this offer.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "qeea9409a24",
  "text": "The order subtotal must be at least $0.00 for this offer to apply.",
  "choices": [
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "q2812094b0b",
  "text": "Applies to orders placed ahead of 28 February 2026.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed on the named date or earlier",
   "the order must be placed strictly before the named date"
  ]
 },
 {
  "qid": "qc30c66247e",
  "text": "Offer by offer, which headline offers from the advertisement and its fine print does Dana Okafor actually get on order INV-20419?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q97dd872ccb",
  "text": "Membership tier production or lower applies.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "qe5aa46b489",
  "text": "Members whose level sits at production or lower may take part.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "qf4d22a4572",
  "text": "Under the advertised terms, does order INV-20419 from Dana Okafor go short of production according to the advertisement and its fine print?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "qcf8a8f3e1e",
  "text": "The order date needs to be on or before 28 February 2026.",
  "choices": [
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier",
   "the order must be placed on the named date or later"
  ]
 },
 {
  "qid": "q154d42910d",
  "text": "Products assigned to the production category are excluded.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "qb5a97db94b",
  "text": "Items drawn from the production category miss the headline benefit.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "qbaba8a2ff2",
  "text": "Taking order INV-20419 from Dana Okafor against the advertised terms, which condition in the small print attached to production does it miss, if any?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q9906986f75",
  "text": "Orders placed on 28 February 2026 itself are excluded.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed on the named date or earlier",
   "the order must be placed strictly before the named date"
  ]
 },
 {
  "qid": "qa18c629fe9",
  "text": "Going by the ad and its small print, does order INV-20419 from Dana Okafor fail to get production under the advertised terms?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q533a05c5bf",
  "text": "Which condition, if any, of the ad and its small print attached to production does order INV-20419 from Dana Okafor miss?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qa7ec5a29c7",
  "text": "Going by the ad and its small print, does order INV-20419 from Dana Okafor lose out on production under the advertised terms?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "qac235aa83d",
  "text": "Which of the advertised terms does order INV-20419 from Dana Okafor actually get with the small print applied offer by offer?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q2db96c28bd",
  "text": "Is it not true that Dana Okafor on order INV-20419 doesn't get production under the promotion?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "qe28a00431c",
  "text": "Is it true that Dana Okafor's order INV-20419 does not get production under the advertised terms?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q3eba48b0a2",
  "text": "Only orders placed before 28 February 2026 count toward this offer.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier"
  ]
 },
 {
  "qid": "qf7c626d0c8",
  "text": "Going by the advertised terms, which condition attached to production does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q46c7e74791",
  "text": "For order INV-20419 from Dana Okafor, which condition in the small print attached to production does it miss, if any, as the advertisement says?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "qe72e6d5e47",
  "text": "Which headline offers from the promo does Dana Okafor on order INV-20419 actually receive, footnotes considered?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q74a5f8c800",
  "text": "Judged by the advertised terms, does order INV-20419 from Dana Okafor end up shut out of production?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q38c2dac580",
  "text": "Does order INV-20419 from Dana Okafor forfeit production under the advertised terms, as set out by the advertisement and its fine print?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q0ce6c3d773",
  "text": "Anything filed under the production category sits outside this offer.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "qb12ceb25cc",
  "text": "Does the order INV-20419 placed by Dana Okafor go short of production under the advertised terms?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qebe23cf54e",
  "text": "Delivery to production is the sole route to the headline benefit.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qf07ea8d04e",
  "text": "Is it true that Dana Okafor, placing order INV-20419, does not get production under the promotion?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q38cba6aac3",
  "text": "Reading the advertisement alongside its fine print, does Dana Okafor receive production on order INV-20419?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q561c2a43d9",
  "text": "Orders headed for delivery in production are kept out of this offer.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "qaefcc68fad",
  "text": "Any product that belongs to the production category is excluded from the offer.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qb40c80a72f",
  "text": "Going by what the advertisement says, does order INV-20419 from Dana Okafor get production under its headline and that headline's small print?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q752d19896c",
  "text": "Valid only for items in the production category.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "q077f84ff8b",
  "text": "production items are excluded from this offer.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q6d746f9819",
  "text": "Valid for orders placed before 28 February 2026.",
  "choices": [
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier",
   "the order must be placed on the named date or later"
  ]
 },
 {
  "qid": "q82e7050ad7",
  "text": "Taking the small print into account offer by offer, what are the advertised terms that Dana Okafor actually gets on order INV-20419?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qdc18b6d1e9",
  "text": "Going by the promotion's headline and its footnotes, does Dana Okafor on order INV-20419 fail to earn production?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qf043f30ed0",
  "text": "Going by what the advertisement says, which condition in the small print attached to production does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "qadf57ecc37",
  "text": "The subtotal of the order needs to be $0.00 or higher.",
  "choices": [
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "qfad1bc1f43",
  "text": "Judging by the promo's footnotes, does order INV-20419 from Dana Okafor fail to get production?",
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
  "qid": "qeccd67a98f",
  "text": "Which condition from the small print attached to production in the advertisement and its fine print does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qa7094d2286",
  "text": "For the order INV-20419 placed by Dana Okafor, which of the advertised terms does it actually get when the small print is checked offer by offer?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qb50ae868f0",
  "text": "Is it true that, under the advertised terms, the order INV-20419 from Dana Okafor doesn't get production?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q41ccd40028",
  "text": "Qualifying orders are placed before 28 February 2026, excluding that date.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed on the named date or earlier",
   "the order must be placed strictly before the named date"
  ]
 },
 {
  "qid": "q9a9703dab8",
  "text": "Based on what the advertisement says, does order INV-20419 from Dana Okafor fail to get production under the advertised terms?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q78df35864a",
  "text": "Reading what the advertisement says alongside the advertised terms, does order INV-20419 from Dana Okafor fail to secure production?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q192326d5da",
  "text": "Looking at Dana Okafor's order INV-20419 and what the advertisement says, which condition in the small print attached to production does it miss, if any?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qe67dd60e64",
  "text": "Placed before 28 February 2026 counts; that very day is excluded.",
  "choices": [
   "the order must be placed on the named date or earlier",
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or later"
  ]
 },
 {
  "qid": "q7b927ba5d0",
  "text": "For production members and above.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "qc60960e1fa",
  "text": "Does the ad and its small print say that order INV-20419 from Dana Okafor gets production?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 }
]
