# T07 extraction task T07-extract_lex-30fb36df-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/extract/answers/T07-extract_lex-30fb36df-002.json

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
  "qid": "q4a4e01001f",
  "text": "Under the advertisement and its fine print, does Dana Okafor earn production with order INV-20419?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q1613d2156b",
  "text": "Orders must be placed on or after 28 February 2026.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed on the named date or earlier",
   "the order must be placed strictly before the named date"
  ]
 },
 {
  "qid": "q887c3e41f1",
  "text": "Minimum order subtotal: $0.00.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "q023caf151d",
  "text": "Anything with delivery in production is excluded from the headline benefit.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q9bf69e2949",
  "text": "Placed on or after 28 February 2026, the order qualifies.",
  "choices": [
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier",
   "the order must be placed on the named date or later"
  ]
 },
 {
  "qid": "q67f39958cb",
  "text": "Orders count only with a subtotal beyond $0.00.",
  "choices": [
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be at least the named amount"
  ]
 },
 {
  "qid": "q873a426421",
  "text": "Based on what the advertisement says, does order INV-20419 from Dana Okafor lose out on production under the advertised terms?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "qc896fb8653",
  "text": "Which condition, drawn from the ad and its small print attached to production, does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q8ebabb52d9",
  "text": "The order date needs to be on or before 28 February 2026.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed on the named date or earlier",
   "the order must be placed strictly before the named date"
  ]
 },
 {
  "qid": "q1021730ac5",
  "text": "Members at the production level or higher only.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "qdc6e8aea5b",
  "text": "Going by the promotion's headline and its footnotes, does Dana Okafor on order INV-20419 fail to earn production?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "qc3881dab67",
  "text": "Orders delivered to production are excluded.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "q4cb18ec648",
  "text": "Looking at the promotion and its footnotes, which headline offers does Dana Okafor on order INV-20419 actually obtain?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q7ee2486642",
  "text": "Going by what the advertisement says, small print included, offer by offer, which headline offers does Dana Okafor actually get on order INV-20419?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q6a162c70ba",
  "text": "Looking at Dana Okafor's order INV-20419 and what the advertisement says, which condition in the small print attached to production does it miss, if any?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q7e59149242",
  "text": "Delivery to production only.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qa45d72f4b8",
  "text": "Delivery to production sits outside the headline benefit.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q05f47efacc",
  "text": "Reading the advertisement and its fine print, which condition in the small print attached to production does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q1124f68836",
  "text": "Is it the case that order INV-20419 from Dana Okafor fails to earn production under the promotion?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qa03ea94bca",
  "text": "In the ad, which condition attached to production does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q8c99ba5a3d",
  "text": "Any item whose status is production falls outside this offer.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "q2cf475e55f",
  "text": "Checking Dana Okafor's order INV-20419 against the ad and its small print, which condition attached to production does it miss, if any?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q8f3d17f5d0",
  "text": "Excludes production items.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "only items in the named product category get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qe9a1134425",
  "text": "Which headline offers from the ad and its small print does order INV-20419 placed by Dana Okafor actually get, offer by offer?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q35dca8f5ad",
  "text": "Reading the ad and its small print together, does order INV-20419 from Dana Okafor fail to secure production under the advertised terms?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qcf995c619f",
  "text": "Does order INV-20419 from Dana Okafor end up shut out of production under the advertised terms, per the ad and its small print?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qfd70a2799b",
  "text": "Is production something that order INV-20419 from Dana Okafor receives under the promotion's footnotes?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "qcd7a9deedb",
  "text": "Reading the advertisement and its fine print together, does order INV-20419 from Dana Okafor lose out on production under the advertised terms?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q81bd815138",
  "text": "Is it true that, under the advertised terms, the order INV-20419 from Dana Okafor doesn't get production?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q20d99b346f",
  "text": "Where the advertisement attaches small print to production, which condition, if any, does order INV-20419 from Dana Okafor miss?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "qa48ac4da21",
  "text": "Items must belong to the production product category to earn the benefit.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qc1359631f4",
  "text": "Reading the advertisement alongside its fine print, does Dana Okafor receive production on order INV-20419?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qaf7eb82b0e",
  "text": "Which headline offers does order INV-20419 from Dana Okafor actually get when the advertisement and its fine print are applied offer by offer?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q4b5c2e7cb7",
  "text": "Which condition in the small print attached to production among the advertised terms does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "qfffbf929c0",
  "text": "The benefit is reserved for delivery bound for production.",
  "choices": [
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "qadddb63660",
  "text": "Isn't it the case that order INV-20419 from Dana Okafor doesn't get production under the advertised terms?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q558dd0f8f7",
  "text": "Going by the ad and its small print, does order INV-20419 from Dana Okafor lose out on production under the advertised terms?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qf84f6f1dea",
  "text": "Could you tell me which headline offers in the ad and its small print order INV-20419 from Dana Okafor actually gets when applied offer by offer?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q0addac25e7",
  "text": "Shoppers get the headline benefit solely for delivery in production.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "only items in the named product category get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q7cee2a5d1c",
  "text": "Reading what the advertisement says, with its headline and small print together, does order INV-20419 from Dana Okafor receive production?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qc0fd7cea67",
  "text": "Eligibility is limited to members at production level or lower.",
  "choices": [
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount"
  ]
 },
 {
  "qid": "qc42600e543",
  "text": "For the offer, the order subtotal must be higher than $0.00.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "q94e5258dd5",
  "text": "Items under the production category are carved out of this offer.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q40de566b84",
  "text": "Does Dana Okafor's order INV-20419 end up shut out of production under the advertised terms, given what the advertisement says?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q40e282d647",
  "text": "The subtotal on the order has to be more than $0.00 to count.",
  "choices": [
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "qb6a94b2dca",
  "text": "Checking the ad, which small-print condition attached to production does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q10cb3d6ad2",
  "text": "Does the promotion, read with its footnotes, leave order INV-20419 from Dana Okafor forfeiting production?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q9b025cd461",
  "text": "When the headline and its small print are read against the advertised terms, does order INV-20419 from Dana Okafor receive production?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q15ddbb47d5",
  "text": "Going by the advertised terms, which condition attached to production does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q7f746612d9",
  "text": "Going by the ad and its small print, does order INV-20419 from Dana Okafor fail to get production under the advertised terms?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 }
]
