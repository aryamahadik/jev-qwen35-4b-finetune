# T07 extraction task T07-extract_lex-f84eda6f-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/extract/answers/T07-extract_lex-f84eda6f-000.json

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
  "qid": "q704e83f071",
  "text": "Does order INV-20419 from Dana Okafor lose out on production under the advertised terms, as the advertisement and its fine print describe?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qec491f2972",
  "text": "Under the advertised terms, does order INV-20419 from Dana Okafor fail to get production?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "qb2a40a5474",
  "text": "Is it not accurate to say that Dana Okafor does not get production with order INV-20419 under the advertised terms?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q385e66e00f",
  "text": "Eligibility is limited to the production category.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qb9b05d27d4",
  "text": "Qualifying orders include the date 28 February 2026 and every later day.",
  "choices": [
   "the order must be placed on the named date or earlier",
   "the order must be placed on the named date or later",
   "the order must be placed strictly before the named date"
  ]
 },
 {
  "qid": "q87b2723f65",
  "text": "Valid for orders placed on or after 28 February 2026.",
  "choices": [
   "the order must be placed on the named date or earlier",
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or later"
  ]
 },
 {
  "qid": "qb464848433",
  "text": "Measured against the advertised terms in full, does order INV-20419 from Dana Okafor lose out on production?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q96bd5bc073",
  "text": "Orders dated on or before 28 February 2026 count.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed on the named date or earlier",
   "the order must be placed strictly before the named date"
  ]
 },
 {
  "qid": "qe4020e9418",
  "text": "Order subtotal must go beyond $0.00.",
  "choices": [
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "q387fcb230e",
  "text": "Is order INV-20419 from Dana Okafor going to go short of production when the promotion's footnotes are applied?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qeb42c87254",
  "text": "Shoppers get the headline benefit solely for delivery in production.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "q1d99e6a41e",
  "text": "Valid for orders whose subtotal is $0.00 or more.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be at least the named amount",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "q098097b76a",
  "text": "Goods in the production category fall outside the headline benefit.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "q5d91209747",
  "text": "Does order INV-20419 from Dana Okafor come with production under what the advertisement says, headline and small print included?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q82211e65bc",
  "text": "Reading the advertisement and its fine print, which condition in the small print attached to production does order INV-20419 from Dana Okafor miss, if any?",
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
  "qid": "q0f93c08487",
  "text": "Does order INV-20419 placed by Dana Okafor come with production under the promotion's terms?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q12a507367f",
  "text": "Looking at the promotion and its footnotes, which headline offers does Dana Okafor on order INV-20419 actually obtain?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q8d93b36f29",
  "text": "Under the advertised terms, with headline and small print read together, does order INV-20419 from Dana Okafor get production?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q028790624a",
  "text": "Every order placed on or after 28 February 2026 is covered by the offer.",
  "choices": [
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier",
   "the order must be placed on the named date or later"
  ]
 },
 {
  "qid": "q5e6c629b77",
  "text": "Is it not so that Dana Okafor does not get production on order INV-20419, per the advertisement and its fine print?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q67bf848e14",
  "text": "Does the order INV-20419 placed by Dana Okafor forfeit production under the advertised terms, as the ad and its small print describe?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q721efba4cd",
  "text": "Reserved for members ranked production or higher.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount"
  ]
 },
 {
  "qid": "q56575482af",
  "text": "Is it true that, under the advertised terms, Dana Okafor's order INV-20419 does not get production, according to what the advertisement says?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q69e2f47c64",
  "text": "Going by the promo's footnotes, isn't it so that order INV-20419 from Dana Okafor does not get production?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q484fa76122",
  "text": "Only a delivery to production qualifies for this offer.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q49829cbe8c",
  "text": "Per what the advertisement says, which condition in the small print attached to production does Dana Okafor's order INV-20419 miss, if any?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q7174aa52a9",
  "text": "Does order INV-20419 from Dana Okafor come with production under the ad and its small print?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "qa265c89998",
  "text": "Which condition, drawn from the ad and its small print attached to production, does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q87f90c711d",
  "text": "Every item in the production category falls outside the offer.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qcca6ca6c23",
  "text": "Only members at the production level or higher may take part.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount"
  ]
 },
 {
  "qid": "qdc9a0c4b21",
  "text": "Under the promo, is it true that Dana Okafor on order INV-20419 does not get production?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q6f9c523639",
  "text": "Does the promotion, read with its footnotes, leave order INV-20419 from Dana Okafor forfeiting production?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q1d52970248",
  "text": "Going through the advertised terms offer by offer, which of them does Dana Okafor actually get on order INV-20419?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q79c7dec5c1",
  "text": "Going by the advertised terms and what the advertisement says, does order INV-20419 from Dana Okafor lose out on production?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q76a7c21f19",
  "text": "The advertised terms attach conditions to production; which, if any, does order INV-20419 from Dana Okafor miss?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q46d02d2a4b",
  "text": "The headline benefit is withheld on delivery to production.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "q76d8fd6f5c",
  "text": "Isn't it right to say that Dana Okafor doesn't get production on order INV-20419 under the advertised terms?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q47e9032bb2",
  "text": "Items must belong to the production product category to earn the benefit.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "only items in the named product category get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qe935890daa",
  "text": "Measured against the advertised terms, which condition in the small print attached to production does Dana Okafor's order INV-20419 miss, if any?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q4d82f5ed68",
  "text": "The headline benefit is set aside for anything in the production category.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qda31a306af",
  "text": "Reading the advertisement and its fine print together, does order INV-20419 from Dana Okafor lose out on production under the advertised terms?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q68b628bd40",
  "text": "Measured against the advertised terms in full, does order INV-20419 from Dana Okafor fail to secure production?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "qc8c8227009",
  "text": "Orders must be placed before 28 February 2026, and the day itself is excluded.",
  "choices": [
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier",
   "the order must be placed on the named date or later"
  ]
 },
 {
  "qid": "qee8d363d3f",
  "text": "Each order needs delivery to production to earn the benefit.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "qcc73a5c41b",
  "text": "The order subtotal must be strictly greater than $0.00.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "q79342c3065",
  "text": "Under the advertised terms, does order INV-20419 from Dana Okafor lose out on production?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q8585d88efc",
  "text": "Under the advertisement and its fine print, does Dana Okafor earn production with order INV-20419?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qa2d08ba2d1",
  "text": "Going by the ad and its small print, is it true that order INV-20419 from Dana Okafor doesn't get production under the advertised terms?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q9e8d87160f",
  "text": "For production, which footnote condition does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q8bed8c09db",
  "text": "Does order INV-20419 from Dana Okafor forfeit production under the advertised terms, as those terms are written?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 }
]
