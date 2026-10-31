# T12 extraction task T12-extract_lex-d7b27e55-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/extract/answers/T12-extract_lex-d7b27e55-003.json

Task kind: extract_lex; items: 50; answer fields: meaning.

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

You read one short phrase or sentence about an accounts-payable (AP) policy card and say which meaning it expresses. Each item has a "text" (the phrase or sentence, with an example value filled in) and a "choices" list of meanings. For each item, pick the one choice that the text says most plainly, and copy that choice exactly, character for character, into the "meaning" field. Judge the words of the text only: do not guess from what would be sensible for an AP policy, and do not reason about any other item. Answer every item once; no item may be skipped or repeated.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array in the answer format below, one entry per item. No other file, no other text.

Answer format: [{"qid": "<qid>", "meaning": "<one choice, copied exactly>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "q1d147d3672",
  "text": "Is it true, as a new clerk, that invoice INV-20419 fails the price check taken by itself?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q06f8c351d4",
  "text": "Is it true that invoice INV-20419 is not released for payment under the AP policy?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "qb39ac1b2d9",
  "text": "Would you say invoice INV-20419 fails the price check, looking only at that check?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q05379e845d",
  "text": "Is it not true for invoice INV-20419 that it is not released for payment under the policy?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "q0d6e52ba8a",
  "text": "With reference to the card, what action is set out for invoice INV-20419?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "qb2c8ccd1c1",
  "text": "Does the policy decide that invoice INV-20419 ends in a hold, a review, a rejection, or a routing to a senior approver?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q1f7447f156",
  "text": "Under the policy, is it not the case that invoice INV-20419 is not released for payment?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "q5bbf6e0e24",
  "text": "Is a hold, a review, a rejection, or a routing to a senior approver what happens to invoice INV-20419 under the policy?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q2e8ec1571b",
  "text": "Judged on its own, does the price check show that bill INV-20419 fails?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q243b2b4c23",
  "text": "Would you agree that it is not the case that bill INV-20419 is not released for payment under the AP policy?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q582ebfb622",
  "text": "Under the AP policy, does invoice INV-20419 end up released for payment?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "qa3e35b48f5",
  "text": "Does the card clear invoice INV-20419 for payment?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "qc4a770d81a",
  "text": "What's the move for invoice INV-20419 according to the rules?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "qe5e6737521",
  "text": "Does the card's verdict on invoice INV-20419 come out as not released for payment?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q1c609cde81",
  "text": "Does bill INV-20419 pass the price check when it is taken on its own?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q77677848f4",
  "text": "Looking at the outcome for invoice INV-20419 as this policy sets it, which line, if any, fails the price check?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q3bf72cd314",
  "text": "Put simply, is it not true that invoice INV-20419 is not released for payment under the card?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "q56e4246405",
  "text": "Having weighed invoice INV-20419 under the policy, which action has it decided on?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q1cff39137b",
  "text": "Taken on its own, does bill INV-20419 pass the price check?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q769d9448c5",
  "text": "Taken on its own, does bill INV-20419 fail the price check?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "qf51b985d98",
  "text": "Under the AP policy, what action is assigned to bill INV-20419?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "qa63cf15a36",
  "text": "Seen by a new clerk, does the AP policy block payment of invoice INV-20419?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q7ee7f1b384",
  "text": "As a check of the AP policy, does invoice INV-20419 pass the price check when that check is judged on its own?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "qe2c9424b16",
  "text": "Isn't it accurate that bill INV-20419 is not released for payment, according to the card?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q603b7d7bfb",
  "text": "Just the price check on its own, then: does invoice INV-20419 fail it?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "qf1e060d860",
  "text": "Trainee, would bill INV-20419 fail the price check by itself?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q0cc95c58a3",
  "text": "Checking how the policy treats invoice INV-20419: does it pass the price check taken on its own?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "qed952a9735",
  "text": "Would this policy let invoice INV-20419 be paid?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q576625d3bb",
  "text": "Would the policy's treatment of invoice INV-20419 amount to price-variance review as its only action?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q2859e1fbc5",
  "text": "Under this policy, what becomes of invoice INV-20419 as an action?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q81d5346a34",
  "text": "Does the card let invoice INV-20419 through to payment?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q4f9875c71c",
  "text": "Under this policy, does invoice INV-20419 wind up not released for payment?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "qbda922bd53",
  "text": "So what does the policy actually tell us to do with invoice INV-20419?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q4c78e8b6e6",
  "text": "Is invoice INV-20419 released to be paid under the card?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q9252a26fa0",
  "text": "Does price-variance review account for everything the card gives bill INV-20419?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q748afd427e",
  "text": "Would a new AP clerk find invoice INV-20419 released for payment by the policy?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q1c0882e657",
  "text": "Is it not right to say that invoice INV-20419 is not released for payment under the policy?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "qcdb63cf4bc",
  "text": "Under the card, is invoice INV-20419 just not released for payment?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q30ae78f0ae",
  "text": "In the policy's check of invoice INV-20419, which line, if any, fails the price check?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q7eff369bcf",
  "text": "On bill INV-20419, which line, if any, is failing the price check?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "q9d26b31d01",
  "text": "Under the AP policy, which line of invoice INV-20419, if any, fails the price check and drives the end result?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q90e7300b13",
  "text": "Under the policy, does invoice INV-20419 go to price-variance review as its only action?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q78f9005f5e",
  "text": "Is it not the case that the AP policy's checks on invoice INV-20419 leave the invoice not released for payment?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "qdd58949ea6",
  "text": "Looking only at the price check, does bill INV-20419 pass?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "qc2fa8d02da",
  "text": "Looking at the card, which action would bill INV-20419 end up with?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "qa757299f85",
  "text": "Stuck on the rules, which action fits invoice INV-20419?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "q37468510e3",
  "text": "Which action does the policy tell us to take for invoice INV-20419?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q6428b66886",
  "text": "Looking at all of it, what should we do with invoice INV-20419?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q745ac70cf6",
  "text": "Does the card say that bill INV-20419 is not released for payment?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "qde593bf856",
  "text": "Put simply, if you are looking only at the price check, does invoice INV-20419 fail it?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice"
  ]
 }
]
