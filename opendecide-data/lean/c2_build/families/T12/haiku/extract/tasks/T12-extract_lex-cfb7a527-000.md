# T12 extraction task T12-extract_lex-cfb7a527-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/extract/answers/T12-extract_lex-cfb7a527-000.json

Task kind: extract_lex; items: 50; answer fields: meaning.

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

You read one short phrase or sentence about an accounts-payable (AP) policy card and say which meaning it expresses. Each item has a "text" (the phrase or sentence, with an example value filled in) and a "choices" list of meanings. For each item, pick the one choice that the text says most plainly, and copy that choice exactly, character for character, into the "meaning" field. Judge the words of the text only: do not guess from what would be sensible for an AP policy, and do not reason about any other item. Answer every item once; no item may be skipped or repeated.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array in the answer format below, one entry per item. No other file, no other text.

Answer format: [{"qid": "<qid>", "meaning": "<one choice, copied exactly>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "q17e72cf623",
  "text": "Under this policy, what becomes of invoice INV-20419 as an action?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "qbc24ffbcd4",
  "text": "Does the policy block payment of invoice INV-20419?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q16023c8dca",
  "text": "Which action does the policy give bill INV-20419?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "q799f5c3eca",
  "text": "Does the policy stop or block payment of invoice INV-20419 for any reason?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q39550fd23e",
  "text": "Taken on its own, does bill INV-20419 pass the price check?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q4c735873a9",
  "text": "Can you check how the policy treats invoice INV-20419 and say which action it gets?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "qfa554375e6",
  "text": "Judged by the price check on its own, would invoice INV-20419 pass that check?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q45b32a00f6",
  "text": "Is it true that invoice INV-20419 gets sent to price-variance review, and that is all?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "qb906f3174e",
  "text": "Setting aside every other check, does invoice INV-20419 pass the price check looked at on its own?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q041143e78b",
  "text": "Given the outcome this policy gives invoice INV-20419, which line, if any, fails the price check?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "qb811861bfb",
  "text": "Is the claim that invoice INV-20419 is not released for payment, under the AP policy, not true?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q03849d597a",
  "text": "If this policy is applied to invoice INV-20419, is price-variance review its sole action?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q4e42ea25c3",
  "text": "Please verify the policy's reading of invoice INV-20419: which action does it apply?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "q30fa9fe553",
  "text": "Does bill INV-20419 fail the price check when it is taken on its own?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "qeb95357968",
  "text": "Does the policy release bill INV-20419 for payment?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "q94782f181c",
  "text": "Does the policy decide that invoice INV-20419 is released for payment?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "qf9fc21105e",
  "text": "Quick question: what action does the card give invoice INV-20419?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "q61e2c1e041",
  "text": "Under the AP policy, which line of invoice INV-20419, if any, fails the price check and drives the end result?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "qadb9fa5298",
  "text": "Is a price-variance review all the policy assigns to bill INV-20419?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review"
  ]
 },
 {
  "qid": "q46e99cb0a1",
  "text": "Is bill INV-20419 released for payment under the policy?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment"
  ]
 },
 {
  "qid": "qd55744cc81",
  "text": "Is price-variance review the only action that this policy assigns to invoice INV-20419?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q51d955e0d9",
  "text": "Is any line of invoice INV-20419 failing the price check, and which line, if any, is it?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q4241666c43",
  "text": "Is invoice INV-20419 not released for payment once the AP policy has been applied to it?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "qa980dc341d",
  "text": "Being new to AP, does the card say invoice INV-20419 is released for payment?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "qbef4f03844",
  "text": "Does what the policy decides for invoice INV-20419 mean it fails the price check taken on its own?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q5fefdc2b1e",
  "text": "On bill INV-20419, which line, if any, is failing the price check?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "qfc31c3751e",
  "text": "Starting out in AP, what is the action that the card sets for invoice INV-20419?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q1d5902ab78",
  "text": "Is it not so that invoice INV-20419 is not released for payment under the AP policy?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q1824e9a5c3",
  "text": "Walk me through it: having read the card, what action sits on invoice INV-20419?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "qce63adf38c",
  "text": "Is it true, as a new clerk, that invoice INV-20419 fails the price check taken by itself?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "qcea113f3af",
  "text": "Is payment of bill INV-20419 stopped under the policy?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice"
  ]
 },
 {
  "qid": "q053b51ff53",
  "text": "Checking how this policy treats invoice INV-20419, which line, if any, fails the price check?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q7f0286a9f3",
  "text": "Trainee, is it not accurate to say that bill INV-20419 is not released for payment under this policy?",
  "choices": [
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "qf7c83773ac",
  "text": "Is it right to say that, under this policy, invoice INV-20419 passes the price check taken on its own?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "qff492cb302",
  "text": "Does the card let invoice INV-20419 through to payment?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment"
  ]
 },
 {
  "qid": "q08944f8bbf",
  "text": "Looking at all of it, what should we do with invoice INV-20419?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q563986c1d4",
  "text": "Having weighed invoice INV-20419 under the policy, which action has it decided on?",
  "choices": [
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "q93eeb1fc25",
  "text": "What treatment does the AP policy give invoice INV-20419, expressed as an action?",
  "choices": [
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q83389c6fde",
  "text": "Does the policy send bill INV-20419 into a hold, a review, a rejection, or a routing to a senior approver?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "qdd91fc83ac",
  "text": "Put plainly, will invoice INV-20419 end up not released for payment?",
  "choices": [
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the policy stops payment of the invoice",
   "asks which action the policy gives the invoice",
   "asks which invoice line fails the price check, if any"
  ]
 },
 {
  "qid": "q9262a5488e",
  "text": "Does the policy stop invoice INV-20419 with a hold, a review, a rejection, or a routing to a senior approver?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q992730244e",
  "text": "Trainee, would a price-variance review be the sole action that bill INV-20419 gets under the policy?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own"
  ]
 },
 {
  "qid": "q429651221a",
  "text": "Going by the way the AP policy treats invoice INV-20419, what line, if any, fails the price check?",
  "choices": [
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice ends in one of the failure actions"
  ]
 },
 {
  "qid": "q760dcd4557",
  "text": "According to this policy, which action applies to bill INV-20419?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "qf5e5ad0048",
  "text": "Looking only at the price check, does bill INV-20419 pass?",
  "choices": [
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice is not released for payment",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "q74c860fdf8",
  "text": "Put simply, if you are looking only at the price check, does invoice INV-20419 fail it?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the policy stops payment of the invoice"
  ]
 },
 {
  "qid": "qff5b775340",
  "text": "So, taken on its own, does invoice INV-20419 pass the price check?",
  "choices": [
   "asks whether the invoice is not released for payment",
   "asks which invoice line fails the price check, if any",
   "asks which action the policy gives the invoice",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q0b336f23fd",
  "text": "What is the resulting action the policy sets for invoice INV-20419?",
  "choices": [
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice ends in one of the failure actions",
   "asks which action the policy gives the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is released for payment",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice fails the price check, taken on its own"
  ]
 },
 {
  "qid": "q07c155f023",
  "text": "Is it the policy's decision to release bill INV-20419 for payment?",
  "choices": [
   "asks whether the invoice ends in one of the failure actions",
   "asks whether the invoice is released for payment",
   "asks which action the policy gives the invoice",
   "asks whether the invoice passes the price check, taken on its own",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks whether the policy stops payment of the invoice",
   "asks whether the policy sends the invoice to price-variance review",
   "asks which invoice line fails the price check, if any",
   "asks whether it is not true that the invoice is not released for payment"
  ]
 },
 {
  "qid": "q3962f15c00",
  "text": "Tell me, in plain words, which action the card gives invoice INV-20419?",
  "choices": [
   "asks whether the policy stops payment of the invoice",
   "asks whether the invoice is released for payment",
   "asks whether it is not true that the invoice is not released for payment",
   "asks whether the policy sends the invoice to price-variance review",
   "asks whether the invoice is not released for payment",
   "asks whether the invoice fails the price check, taken on its own",
   "asks which invoice line fails the price check, if any",
   "asks whether the invoice passes the price check, taken on its own",
   "asks which action the policy gives the invoice",
   "asks whether the invoice ends in one of the failure actions"
  ]
 }
]
