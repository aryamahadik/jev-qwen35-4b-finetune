# T12 extraction task T12-extract_lex-d7b27e55-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/extract/answers/T12-extract_lex-d7b27e55-002.json

Task kind: extract_lex; items: 50; answer fields: meaning.

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

You read one short phrase or sentence about an accounts-payable (AP) policy card and say which meaning it expresses. Each item has a "text" (the phrase or sentence, with an example value filled in) and a "choices" list of meanings. For each item, pick the one choice that the text says most plainly, and copy that choice exactly, character for character, into the "meaning" field. Judge the words of the text only: do not guess from what would be sensible for an AP policy, and do not reason about any other item. Answer every item once; no item may be skipped or repeated.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array in the answer format below, one entry per item. No other file, no other text.

Answer format: [{"qid": "<qid>", "meaning": "<one choice, copied exactly>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "qaeb3af7f54",
  "text": "Which action does the AP policy assign to invoice INV-20419 under its stated sequence of steps?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q844fae9c0d",
  "text": "Is any line of invoice INV-20419 failing the price check, and which line, if any, is it?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q5525b6c445",
  "text": "Does the AP policy send invoice INV-20419 to price-variance review, with that being the sole action the invoice gets?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "qc624e4f714",
  "text": "If you strip away the other checks, is invoice INV-20419 a pass on the price check judged by itself?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q579e9fd325",
  "text": "Is it not true that the policy's outcome for invoice INV-20419 is that it is not released for payment?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q4402f92dd8",
  "text": "Here's the deal: which action is the policy putting on invoice INV-20419?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q6d8138c389",
  "text": "Tell me, in plain words, which action the card gives invoice INV-20419?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q2c4df17aa9",
  "text": "Does the policy stop invoice INV-20419 with a hold, a review, a rejection, or a routing to a senior approver?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q921c856e7b",
  "text": "Is the outcome for invoice INV-20419 under this policy driven by any line that fails the price check, and which line, if any?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q2967df00ec",
  "text": "Is it not correct that bill INV-20419 is not released for payment under the policy?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q91cc061e07",
  "text": "Under the AP policy, which action fits invoice INV-20419?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "qaca5301d95",
  "text": "Is it not true that invoice INV-20419 is not released for payment under the policy?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q29e6bae0bf",
  "text": "Trainee, would the policy let bill INV-20419 go ahead for payment?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q9a468b2f4b",
  "text": "Is bill INV-20419 released for payment under the policy?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q163a27f211",
  "text": "What does the policy say to do with invoice INV-20419?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "qb9209b7201",
  "text": "When the policy handles invoice INV-20419, is it not accurate that the invoice is not released for payment?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q0b42bcc2e1",
  "text": "Judged only as this policy sees it, does invoice INV-20419 fail the price check taken by itself?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q52f2243998",
  "text": "Does the policy release bill INV-20419 for payment?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q0ca9d53bd5",
  "text": "Can you tell me which line of invoice INV-20419, if any, fails the price check?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "qb2905c5b2d",
  "text": "For invoice INV-20419, when only the price check is judged on its own, does the invoice fail that check under the card?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q5f8f9a3af0",
  "text": "Trainee, would a price-variance review be the sole action that bill INV-20419 gets under the policy?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "q8bba238e98",
  "text": "According to this policy, which action applies to bill INV-20419?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q6eaeb39e3b",
  "text": "In the policy's eyes, which action does invoice INV-20419 land on?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "qd16e8f7fcc",
  "text": "Is invoice INV-20419 caught by a hold, a review, a rejection, or a routing to a senior approver?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q799e597320",
  "text": "Which action does this policy give invoice INV-20419?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "qf301f01e4d",
  "text": "Does the policy send bill INV-20419 to price-variance review as its only action?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q964492c1ed",
  "text": "Does the policy send bill INV-20419 into a hold, a review, a rejection, or a routing to a senior approver?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q035610ab9f",
  "text": "Under the AP policy, is it not true that invoice INV-20419 is not released for payment?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q54f362b38e",
  "text": "Would price-variance review be the only step the card takes on invoice INV-20419?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q97ba8367a8",
  "text": "Under this policy, is it not correct that invoice INV-20419 is not released for payment?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "qa608e9124b",
  "text": "For invoice INV-20419, what decision does the card make about its action?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "qa4fbcc0bd2",
  "text": "Trainee, would bill INV-20419 pass the price check by itself?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q6d267da941",
  "text": "Quick question: what action does the card give invoice INV-20419?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "qab84d4113d",
  "text": "Is payment of bill INV-20419 stopped under the policy?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q4c495cec0f",
  "text": "Is it right to say that, under this policy, invoice INV-20419 passes the price check taken on its own?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q337b534040",
  "text": "Can you check how the policy treats invoice INV-20419 and say which action it gets?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "qe7f9027e01",
  "text": "When the AP policy is run on invoice INV-20419, does the result mark it as not released for payment?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "qb9fecfdea6",
  "text": "From where a new clerk stands, does the price check taken on its own make invoice INV-20419 fail?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q149300e86e",
  "text": "Does the policy stop or block payment of invoice INV-20419 for any reason?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q6657a01c10",
  "text": "Under this policy, does invoice INV-20419 end at a hold, a review, a rejection, or a routing to a senior approver?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "qd547dce371",
  "text": "Does the card's check on invoice INV-20419 leave that invoice not released for payment?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "qfde6b161b6",
  "text": "Setting aside every other check, does invoice INV-20419 pass the price check looked at on its own?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q0c47f6a823",
  "text": "Which action does the policy give bill INV-20419?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q5fa47d054b",
  "text": "Which line on invoice INV-20419 fails the price check, if any?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q3c078cac54",
  "text": "Does bill INV-20419 fail the price check when it is taken on its own?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "qf8e06f289e",
  "text": "So is invoice INV-20419 not released for payment under the policy?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q58c5d01010",
  "text": "Is it not correct under the AP policy that invoice INV-20419 is not released for payment?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q3031fcf35d",
  "text": "Toward what action does the AP policy lead invoice INV-20419?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q561b230b86",
  "text": "Under the policy, does the treatment of invoice INV-20419 leave it not released for payment?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "qb703f33ed0",
  "text": "Okay, with the card in hand, what's the action for invoice INV-20419?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment"
  ]
 }
]
