# T12 extraction task T12-extract_lex-d7b27e55-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/extract/answers/T12-extract_lex-d7b27e55-001.json

Task kind: extract_lex; items: 50; answer fields: meaning.

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

You read one short phrase or sentence about an accounts-payable (AP) policy card and say which meaning it expresses. Each item has a "text" (the phrase or sentence, with an example value filled in) and a "choices" list of meanings. For each item, pick the one choice that the text says most plainly, and copy that choice exactly, character for character, into the "meaning" field. Judge the words of the text only: do not guess from what would be sensible for an AP policy, and do not reason about any other item. Answer every item once; no item may be skipped or repeated.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array in the answer format below, one entry per item. No other file, no other text.

Answer format: [{"qid": "<qid>", "meaning": "<one choice, copied exactly>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "qa9047c219f",
  "text": "Is the way this policy handles invoice INV-20419 a case where price-variance review is the sole action?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "q3219f56c9e",
  "text": "As a new clerk in AP, is invoice INV-20419 allowed through to payment under the policy?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "qdbe0058bb1",
  "text": "Is invoice INV-20419 sent to a hold, a review, a rejection, or a routing to a senior approver?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q714414befa",
  "text": "Under this policy, is bill INV-20419 cleared to be paid?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "qd6511ee831",
  "text": "Is it right that the policy stops or blocks payment of invoice INV-20419?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q5baf983466",
  "text": "The card sets an action for invoice INV-20419, but which?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q7df90c9688",
  "text": "Would the AP policy simply send invoice INV-20419 to price-variance review and leave it there?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "q71c6785a72",
  "text": "Is the outcome for invoice INV-20419 under the AP policy a hold, a review, a rejection, or a routing to a senior approver?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "qa4e7f17197",
  "text": "Forget the other checks for a sec: would invoice INV-20419 fail the price check by itself?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q4307fe5b3d",
  "text": "When the policy decides on invoice INV-20419, does that invoice fail the price check taken on its own?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q594d12c476",
  "text": "Under the AP policy, is payment of invoice INV-20419 blocked?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "qa08990e1ea",
  "text": "Is it not the case, under this policy, that invoice INV-20419 is not released for payment?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q097409f5ad",
  "text": "Trainee, does bill INV-20419 end in a hold, a review, a rejection, or a routing to a senior approver?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "qc52224697b",
  "text": "Is bill INV-20419 headed for a hold, a review, a rejection or a routing to a senior approver under the AP policy?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "qbf0493bb98",
  "text": "Does the card send invoice INV-20419 to price-variance review as its only step?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "qe17d16feae",
  "text": "Isn't it true, under the policy, that bill INV-20419 is not released for payment?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "qd00e706578",
  "text": "Is price-variance review the only action that this policy assigns to invoice INV-20419?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q66a60d3fc4",
  "text": "Under the AP policy, would bill INV-20419 count as not released for payment?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "qb594f27fa6",
  "text": "Under the policy, is it not true that the treatment of invoice INV-20419 leaves it not released for payment?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q1b05480ebc",
  "text": "Does invoice INV-20419 just go to price-variance review, and is that the only thing that happens to it?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "q685c22b31e",
  "text": "Is it true that invoice INV-20419 gets sent to price-variance review, and that is all?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "qbf8a6f0d7c",
  "text": "Is the action for invoice INV-20419 set out in the policy, and what is it?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "qd966e45a05",
  "text": "If this policy is applied to invoice INV-20419, is price-variance review its sole action?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "qe83cb0f6b6",
  "text": "Quick question for you, trainee, which line of bill INV-20419 gets flagged by the price check, if any?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q1e31d4ecce",
  "text": "Pursuant to the AP policy, which action is prescribed for invoice INV-20419?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q3e457df4d5",
  "text": "Would bill INV-20419 land in a hold, a review, a rejection, or a routing to a senior approver under the policy?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q6701eb42b2",
  "text": "Trainee, which line of bill INV-20419, if any, fails the price check?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q70f0b886a7",
  "text": "Would this policy count invoice INV-20419 as a pass on the price check looked at by itself?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q11468bbcc9",
  "text": "Trainee, what action should bill INV-20419 receive under the policy?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "qb64e314e2d",
  "text": "Taking only the price check on its own, does this policy have invoice INV-20419 fail that check?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "qbabb1ca6a4",
  "text": "Would the AP policy's sole action for invoice INV-20419 be a referral to price-variance review?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q3cfaa2aae7",
  "text": "So, taken on its own, does invoice INV-20419 pass the price check?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "q61a8431d67",
  "text": "Does the policy stop or block payment of bill INV-20419?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "qb92850a1b6",
  "text": "Does this policy's outcome for invoice INV-20419 amount to it being not released for payment?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q3040848951",
  "text": "As a new clerk in AP, is payment of invoice INV-20419 blocked under the policy?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "qa8b47eb399",
  "text": "Will the card send invoice INV-20419 to a hold, a review, a rejection, or a routing to a senior approver?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q196ec311a7",
  "text": "As a new clerk on the AP team, does invoice INV-20419 fail the price check taken on its own?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "qfb4f4883c0",
  "text": "Checking how the policy treats invoice INV-20419, is price-variance review its only action?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q966d8085f5",
  "text": "Does the policy release invoice INV-20419 for payment?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q3bc1d7ed41",
  "text": "Under the AP policy, does invoice INV-20419 pass the price check taken on its own?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q54dc993930",
  "text": "Isn't it the case that bill INV-20419 is not released for payment under the AP policy?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q6f16fd71ee",
  "text": "So does invoice INV-20419 fail the price check when you look at that check on its own?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q5717bca430",
  "text": "Would you say invoice INV-20419 passes the price check when that check is looked at on its own?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q9abd652abb",
  "text": "Seen by a new clerk, does the AP policy release invoice INV-20419 for payment?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q3fd60491b2",
  "text": "Under this policy, is the outcome for invoice INV-20419 that it is not released for payment?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "qee5702fe78",
  "text": "Looking only at the price check, does bill INV-20419 fail?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q9f519e1d3a",
  "text": "Walk me through it: having read the card, what action sits on invoice INV-20419?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q444f85400c",
  "text": "Does the policy's handling of invoice INV-20419 come down to price-variance review as the sole action?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "qa1b99154c3",
  "text": "Is it not so that the card says bill INV-20419 is not released for payment?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q6db23699eb",
  "text": "Is the claim that invoice INV-20419 is not released for payment, under the AP policy, not true?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any"
  ]
 }
]
