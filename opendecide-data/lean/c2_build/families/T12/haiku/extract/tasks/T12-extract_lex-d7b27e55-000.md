# T12 extraction task T12-extract_lex-d7b27e55-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/extract/answers/T12-extract_lex-d7b27e55-000.json

Task kind: extract_lex; items: 50; answer fields: meaning.

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

You read one short phrase or sentence about an accounts-payable (AP) policy card and say which meaning it expresses. Each item has a "text" (the phrase or sentence, with an example value filled in) and a "choices" list of meanings. For each item, pick the one choice that the text says most plainly, and copy that choice exactly, character for character, into the "meaning" field. Judge the words of the text only: do not guess from what would be sensible for an AP policy, and do not reason about any other item. Answer every item once; no item may be skipped or repeated.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array in the answer format below, one entry per item. No other file, no other text.

Answer format: [{"qid": "<qid>", "meaning": "<one choice, copied exactly>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "qc2f6ccbe3a",
  "text": "Does invoice INV-20419 end in a hold, a review, a rejection, or a routing to a senior approver?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q9e7b69bd26",
  "text": "Put plainly, will invoice INV-20419 end up not released for payment?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q492a6e22d4",
  "text": "Does the AP policy agree that it is not true that invoice INV-20419 is not released for payment?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q514f0ece86",
  "text": "After the policy decides on invoice INV-20419, does that decision leave it not released for payment?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "qf460ba6862",
  "text": "Does the policy block payment of invoice INV-20419?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "qdf70010e9e",
  "text": "Is it right that the policy releases invoice INV-20419 for payment?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q54fa7daff9",
  "text": "Under the policy, is it not accurate that invoice INV-20419 is not released for payment?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q688d51b829",
  "text": "Double-checking the card, which action does it assign to invoice INV-20419?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q190b4d832a",
  "text": "Could you tell a new clerk what action the card gives invoice INV-20419?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q0755d4bb1c",
  "text": "Forget everything else for a moment: does invoice INV-20419 pass the price check on its own?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q5d47d0661e",
  "text": "Could a colleague trace how the AP policy handles invoice INV-20419, and which action follows?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q044a383fd1",
  "text": "Judged by the price check on its own, would invoice INV-20419 pass that check?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q65c3b3591c",
  "text": "Trainee, under this policy, is it not the case that bill INV-20419 is not released for payment?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "qf4e398be99",
  "text": "Is it not true that bill INV-20419 is not released for payment under the policy?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "qe894096b06",
  "text": "Judged on its own, does the price check show that bill INV-20419 passes?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "q2ec5897b63",
  "text": "As a new clerk on the AP team, which action does the policy give invoice INV-20419?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "q8aaf5bf635",
  "text": "With the card applied, what comes of invoice INV-20419?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "qb69bd3ea68",
  "text": "Looking at the unit prices on invoice INV-20419, which line, if any, fails the price check?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q0499e9757c",
  "text": "Is bill INV-20419 not released for payment under the policy?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "qab6b797302",
  "text": "What line on bill INV-20419 is the price check failing, if any?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q6a775c21c0",
  "text": "What is it that the policy decides for invoice INV-20419, in terms of action?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q42e84d3fd6",
  "text": "Just the price check here, by itself: does invoice INV-20419 pass?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q9cd6ccbb30",
  "text": "Isn't the policy saying that bill INV-20419 is not released for payment?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q0d6fcdd1eb",
  "text": "Starting out in AP, what is the action that the card sets for invoice INV-20419?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q2d07e342db",
  "text": "Is the outcome of the price check for invoice INV-20419, taken on its own, a pass under this policy?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "qb0f8f96cbe",
  "text": "Just starting out in AP, would invoice INV-20419 fail the price check when that check is judged on its own?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q60ccdd776d",
  "text": "Which action does the policy reach for invoice INV-20419?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q075defc6b7",
  "text": "Is payment of invoice INV-20419 stopped under the AP policy?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "qebf72a9e61",
  "text": "Does the policy decide that invoice INV-20419 is released for payment?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "qcbd91a1a1b",
  "text": "Please verify the policy's reading of invoice INV-20419: which action does it apply?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q2eaaee309a",
  "text": "Would this policy have invoice INV-20419 blocked from payment for some reason?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "qf1b066ddc4",
  "text": "Where the policy is applied to invoice INV-20419, what action does it call for?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "qeb8dcd4ee1",
  "text": "Does the policy's treatment of invoice INV-20419 point to any line that fails the price check, and which line, if any?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "q63ad0ea20e",
  "text": "Looking only at the price check, does invoice INV-20419 pass it under the card?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "qbb01ba16e8",
  "text": "Is the result for invoice INV-20419 a hold, a review, a rejection, or a routing to a senior approver?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q7dc0c81e7b",
  "text": "Under the terms of this policy, which action applies to invoice INV-20419?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "qed436def6e",
  "text": "Taking the steps in order, what does the AP policy decide for invoice INV-20419?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "qea82c2d70c",
  "text": "Is it not so that invoice INV-20419 is not released for payment under the AP policy?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "qcb794b19e6",
  "text": "Being new to AP, does the card say payment of invoice INV-20419 is stopped?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "qaacca6c542",
  "text": "Which line on invoice INV-20419, if any, fails the price check and so shapes the result this policy reaches?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q954606a3cc",
  "text": "Going by the way the AP policy treats invoice INV-20419, what line, if any, fails the price check?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q2816acfb03",
  "text": "Checking how this policy treats invoice INV-20419, which line, if any, fails the price check?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q4266bec0fa",
  "text": "Is a price-variance review all the policy assigns to bill INV-20419?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q35e06b95a2",
  "text": "Is there a block on payment of invoice INV-20419 under the policy?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q4c6f9c93ae",
  "text": "Trainee, is it not accurate to say that bill INV-20419 is not released for payment under this policy?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q8ad16d0386",
  "text": "Is it the case that bill INV-20419 isn't released for payment under the policy?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q92f0e1a9ca",
  "text": "Would you say it is not true that invoice INV-20419 is not released for payment under the policy?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "qb1e0e06f75",
  "text": "Is invoice INV-20419 released for payment?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q10763e4bee",
  "text": "Does invoice INV-20419 get stuck as not released for payment under the policy?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "qa893397562",
  "text": "Is it the policy's decision to release bill INV-20419 for payment?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 }
]
