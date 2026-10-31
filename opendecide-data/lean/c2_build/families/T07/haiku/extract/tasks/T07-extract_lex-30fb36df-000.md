# T07 extraction task T07-extract_lex-30fb36df-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/extract/answers/T07-extract_lex-30fb36df-000.json

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
  "qid": "q6cee559640",
  "text": "Which condition in the footnotes attached to production does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q8ab23f637d",
  "text": "Do the advertisement and its fine print together let order INV-20419 from Dana Okafor get production?",
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
  "qid": "q17d1bebcad",
  "text": "Orders submitted on or before 28 February 2026 are accepted.",
  "choices": [
   "the order must be placed on the named date or later",
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier"
  ]
 },
 {
  "qid": "qfb8959537f",
  "text": "For production, which footnote condition does order INV-20419 from Dana Okafor miss, if any?",
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
  "qid": "q04f95b0678",
  "text": "Under the advertised terms, does the order INV-20419 placed by Dana Okafor fail to earn production, based on the ad and its small print?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q6c0f4da89a",
  "text": "Taking order INV-20419 from Dana Okafor and reading the ad and its small print, which condition attached to production does it miss, if any?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q3f57c90cae",
  "text": "Under the promo's terms, does Dana Okafor fail to receive production on order INV-20419?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q3b8d46133f",
  "text": "Is it true that order INV-20419 from Dana Okafor does not get production under the advertised terms, per the ad and its small print?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qfedff61488",
  "text": "Based on what the advertisement says, is it true that order INV-20419 from Dana Okafor does not get production under the advertised terms?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q569937109e",
  "text": "Checking the small print offer by offer, which of the advertised terms does Dana Okafor actually get on order INV-20419?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "qfd09abe89e",
  "text": "Is it true that Dana Okafor's order INV-20419 does not get production under the advertised terms?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "qe926e96df6",
  "text": "The advertisement and its fine print attach conditions to production; which, if any, does order INV-20419 from Dana Okafor miss?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q48913e400b",
  "text": "Items sold as production are excluded.",
  "choices": [
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit"
  ]
 },
 {
  "qid": "q871cb4d20f",
  "text": "Which of the advertised terms does order INV-20419 from Dana Okafor actually get with the small print applied offer by offer?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q70a428727b",
  "text": "Offer by offer, which headline offers from the advertisement and its fine print does Dana Okafor actually get on order INV-20419?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q525889e9b5",
  "text": "Under the advertised terms, does order INV-20419 from Dana Okafor go short of production, according to the ad and its small print?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "qde573dee5d",
  "text": "Reading the ad and its small print offer by offer, which headline offers does order INV-20419 from Dana Okafor actually get?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "qc1880fe3b7",
  "text": "Anything filed under the production category sits outside this offer.",
  "choices": [
   "items in the named product category are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q56078fc0ea",
  "text": "Orders placed by 28 February 2026 are valid, and the stated day is included.",
  "choices": [
   "the order must be placed on the named date or earlier",
   "the order must be placed on the named date or later",
   "the order must be placed strictly before the named date"
  ]
 },
 {
  "qid": "qdf0e525cf8",
  "text": "Does order INV-20419 from Dana Okafor lose out on production under the advertised terms, as the advertisement and its fine print describe?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q1752c84bf0",
  "text": "Excludes delivery to production.",
  "choices": [
   "items with the named price status are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "q4e2bcab80f",
  "text": "Reading the ad and its small print alongside the advertised terms, does order INV-20419 from Dana Okafor lose out on production?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q5df0ae36c1",
  "text": "For production members and above.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "q32af2c0371",
  "text": "Valid for orders placed from 28 February 2026 onward.",
  "choices": [
   "the order must be placed on the named date or earlier",
   "the order must be placed on the named date or later",
   "the order must be placed strictly before the named date"
  ]
 },
 {
  "qid": "q420f8c9517",
  "text": "Headline benefit applies to orders with delivery in production only.",
  "choices": [
   "orders delivered to the named region are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit"
  ]
 },
 {
  "qid": "q11279eff64",
  "text": "Valid for orders placed before 28 February 2026.",
  "choices": [
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or later",
   "the order must be placed on the named date or earlier"
  ]
 },
 {
  "qid": "q2536af9c1c",
  "text": "Members ranked production and above are the only ones covered.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a lower one"
  ]
 },
 {
  "qid": "q6e407f3b71",
  "text": "Under what the advertisement says, headline and small print included, does Dana Okafor get production on order INV-20419?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q0e042be367",
  "text": "Does order INV-20419 from Dana Okafor fail to receive production under the advertised terms?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q8592f0fbd1",
  "text": "Is it not the case that order INV-20419 from Dana Okafor does not get production under the advertised terms?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q163fab0a05",
  "text": "When its fine print is included, does the advertisement say that order INV-20419 from Dana Okafor receives production?",
  "choices": [
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any"
  ]
 },
 {
  "qid": "q0916768c3c",
  "text": "Only the production category earns the headline benefit.",
  "choices": [
   "orders delivered to the named region are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "only items in the named product category get the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "qcc3df35990",
  "text": "The order subtotal must be above $0.00.",
  "choices": [
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount"
  ]
 },
 {
  "qid": "qf5c8b3515c",
  "text": "Does order INV-20419 from Dana Okafor fail to get production under the advertised terms, as the advertisement and its fine print spell out?",
  "choices": [
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)"
  ]
 },
 {
  "qid": "q3be0e4d2b9",
  "text": "Under the promo's terms, does Dana Okafor forfeit production on order INV-20419?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q1555294117",
  "text": "Membership tier production or lower applies.",
  "choices": [
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "q87ece4f855",
  "text": "Between the advertisement and its fine print, does order INV-20419 from Dana Okafor get production?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q935760e0a3",
  "text": "Valid for orders placed on or before 28 February 2026.",
  "choices": [
   "the order must be placed on the named date or earlier",
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or later"
  ]
 },
 {
  "qid": "q62eab41a5e",
  "text": "Requires membership at production or higher.",
  "choices": [
   "the order subtotal must be at least the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one",
   "the order subtotal must be strictly greater than the named amount"
  ]
 },
 {
  "qid": "q8044ee88d4",
  "text": "The headline benefit is set aside for anything in the production category.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "items with the named price status are excluded from the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q2c48bcac3b",
  "text": "Which ad condition attached to production does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit"
  ]
 },
 {
  "qid": "q9912c0790f",
  "text": "Do the advertised terms, taking in the headline and small print, let Dana Okafor get production on order INV-20419?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "q0f1f1b87ad",
  "text": "Under the advertised terms, is it true that order INV-20419 from Dana Okafor does not get production, as the ad and its small print states?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q79f04ce2bc",
  "text": "The subtotal of the order needs to be $0.00 or higher.",
  "choices": [
   "the order subtotal must be at least the named amount",
   "the order subtotal must be strictly greater than the named amount",
   "the customer's membership level must be the named level or a lower one",
   "the customer's membership level must be the named level or a higher one"
  ]
 },
 {
  "qid": "q7a5415d77a",
  "text": "Going by what the advertisement says, does order INV-20419 from Dana Okafor get production under its headline and that headline's small print?",
  "choices": [
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets"
  ]
 },
 {
  "qid": "q1ef54ca943",
  "text": "Does Dana Okafor's order INV-20419 miss which ad condition attached to production, if any?",
  "choices": [
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit"
  ]
 },
 {
  "qid": "q76b423c746",
  "text": "Eligibility for the benefit is restricted to the production product category.",
  "choices": [
   "only items in the named product category get the headline benefit",
   "only orders delivered to the named region get the headline benefit",
   "items in the named product category are excluded from the headline benefit",
   "orders delivered to the named region are excluded from the headline benefit",
   "items with the named price status are excluded from the headline benefit"
  ]
 },
 {
  "qid": "q43104e1231",
  "text": "Which condition in the ad and its small print attached to production does order INV-20419 from Dana Okafor miss, if any?",
  "choices": [
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')",
   "asks whether the customer's order gets the named headline benefit"
  ]
 },
 {
  "qid": "qeb468aeb39",
  "text": "Reading what the advertisement says alongside the advertised terms, does order INV-20419 from Dana Okafor fail to secure production?",
  "choices": [
   "asks which fine-print condition of the named headline the order misses, if any",
   "asks whether the customer's order fails to get the named headline benefit",
   "asks which of the advertised headline offers the order gets",
   "asks whether the customer's order gets the named headline benefit",
   "asks whether it is not the case that the customer's order does not get the named headline benefit",
   "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
   "asks whether the customer's order does not get the named headline benefit (one 'not')"
  ]
 },
 {
  "qid": "q16ca4c6da0",
  "text": "Orders placed on the date 28 February 2026 count, and so do all later orders.",
  "choices": [
   "the order must be placed strictly before the named date",
   "the order must be placed on the named date or earlier",
   "the order must be placed on the named date or later"
  ]
 }
]
