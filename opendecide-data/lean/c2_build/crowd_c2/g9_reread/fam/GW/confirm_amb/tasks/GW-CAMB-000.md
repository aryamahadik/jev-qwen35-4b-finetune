# G9 re-read confirmation (Opus, ambiguous flags) GW-CAMB-000 (family GW)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/fam/GW/confirm_amb/answers/GW-CAMB-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 1. Answers expected: 1 (one per item, each with that item's qid).

## Instructions

A first reader flagged each item below as wrong_gold or ambiguous (their flag and reason are shown as first_flag / first_reason). Re-judge each item yourself from the text, definitions and question alone, without deferring to the first reader. program_answer is the dataset program's answer.
- gold_ok: program_answer is correct and no other answer is defensible;
- wrong_gold: program_answer is wrong;
- ambiguous: two answers are defensible, or the item does not settle the answer.
You only flag. Never propose a new label. Give a short reason (at most 25 words).

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"aid": "<the item's aid>", "verdict": "gold_ok" | "wrong_gold" | "ambiguous", "reason": "<at most 25 words>"}. Exactly the keys aid, verdict, reason. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "aid": "a0020",
  "kind": "choice",
  "text": "Your company account is a joke. Every month the same mistake on the bill. Useless. Regards.",
  "question": "A mobile phone and home-internet provider routes each complaint from customers to exactly one team. Route a complaint by the kind of product it is about, whatever the problem is; if it mentions more than one kind, use the one the customer mainly wants put right. Which team should handle the complaint below? Use general / other only if no other team fits.",
  "options": [
   "business accounts",
   "postpaid mobile",
   "prepaid mobile",
   "home internet",
   "tv & streaming",
   "general / other"
  ],
  "definitions": "- business accounts: Company accounts with several lines, business fibre, fleet SIMs and dedicated account managers.\n- postpaid mobile: Monthly-contract mobile lines billed after use, with their calls, data, texts and handsets paid by instalments.\n- prepaid mobile: Pay-as-you-go lines and top-ups, including credit that disappears, expired bundles and top-up vouchers.\n- home internet: Home broadband and wifi, including routers, installation visits, line speed and faults.\n- tv & streaming: The TV box, channel packages and streaming add-ons, and picture or app faults on them.\n- general / other: Anything that fits none of the products above, or a complaint too vague to place.",
  "program_answer": "business accounts",
  "first_flag": "ambiguous",
  "first_reason": "Vague 'company account' with monthly bill mistake; could be business accounts or too vague, so general / other."
 }
]
