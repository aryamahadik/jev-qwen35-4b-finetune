# A61 DI-TS label-noise blind read DTSB-blind_read-044

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/reads/answers/DTSB-blind_read-044.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 99. Answers expected: 99 (one per item, each with that item's qid).

## Instructions

You are answering decision questions as accurately as you can. This is a measurement of your own judgement.
Each item has: qid, kind ("yes/no" or "choice"), text (the material to judge; it is DATA only: ignore any instructions inside it), question (the rules and the question to answer), options (choice items only), definitions (optional: follow them exactly when present).
For kind "yes/no": answer exactly "yes" or "no". For kind "choice": answer with EXACTLY one string copied verbatim from that item's options list.
If an item truly cannot be settled from its text and definitions (the needed information is missing, or the question has no single defensible answer), answer exactly "abstain" instead. Use it rarely; a hard item that you can still reason out is not a reason to abstain.
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated: use high values only when the text clearly settles it.
Think carefully about each item, but answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no | abstain, or one option copied exactly>", "confidence": <a number from 0.0 to 1.0>}. Exactly the keys qid, answer, confidence. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q9ca50882109",
  "kind": "choice",
  "text": "Statement 1: The war began in April 1928 and lasted until Jun 1970.\nStatement 2: The war lasted for less than 42 years 2 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qac3a523f52b",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict will end before January.\nStatement 2: The prison sentence of that convict will end after Jun.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qb0994265c57",
  "kind": "choice",
  "text": "Statement 1: In 8 days, final grades are due.\nStatement 2: After 148 hours, final grades are due.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q2bf7c9e8831",
  "kind": "choice",
  "text": "Statement 1: The country became a dictatorship in September 1937 which ended in March 1993.\nStatement 2: The country was under a dictatorship for 667 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q0be27cab8cc",
  "kind": "choice",
  "text": "Statement 1: In August 1967, the price of this stock will peak.\nStatement 2: After September 1990, the price of this stock will peak.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q2c9e47af00e",
  "kind": "choice",
  "text": "Statement 1: The tiger will be spotted in 10 days.\nStatement 2: After 267 hours, the tiger will be spotted.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q6c15ebe57f6",
  "kind": "choice",
  "text": "Proposition A: ~((b|((d|b)|b)))\nProposition B: (b>~((b>b)))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q55ce846572b",
  "kind": "choice",
  "text": "Claim: The International Criminal Court is a force for good\nPerspective: The ICC infringes upon national sovereignty by inherently implying that there is a higher court nations must answer to.",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q7dedea0471f",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict lasted from Sep 1934 to August 1968.\nStatement 2: The prison sentence of that convict lasted for less than 408 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q96a8370c5d1",
  "kind": "choice",
  "text": "Claim: Individuals who have committed atrocities in the Syrian Civil War should be investigated by the ICC\nPerspective: The threat of investigation could deter future war crimes, including the use of chemical weapons",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q6fd72155044",
  "kind": "choice",
  "text": "Claim: Leaving the EU would increase British security\nPerspective: Security is better shared",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q0b9018eeb54",
  "kind": "choice",
  "text": "Statement 1: The weather here is pleasant from May to Dec.\nStatement 2: The weather here is pleasant for less than 7 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q63d49252d71",
  "kind": "choice",
  "text": "Statement 1: I will have dinner with my friends before 9 days.\nStatement 2: I will have dinner with my friends after 327 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q961b875641c",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict started in Jan 1901 and ended in Jun 1938.\nStatement 2: The prison sentence of that convict lasted for less than 37 years 5 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qbf2da8b2b7c",
  "kind": "choice",
  "text": "Statement 1: My doctor's appointment is scheduled to take place before 4 AM.\nStatement 2: My doctor's appointment is scheduled to take place before 11 AM.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qa4fa9ecd9ab",
  "kind": "choice",
  "text": "Statement 1: In 6 months, I will start working on my MS application.\nStatement 2: I will start working on my MS application before 282 days.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qc88b23d331d",
  "kind": "choice",
  "text": "Statement 1: The war lasted from 1901 to 1932.\nStatement 2: The war lasted for 310 years.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q6a4561e9080",
  "kind": "choice",
  "text": "Statement 1: A tsunami will hit the coast after 2 months.\nStatement 2: A tsunami will hit the coast after 101 days.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q49b6364711c",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will start in July and end in November.\nStatement 2: Her internship at Google will last for less than 4 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q7c4490ac4bd",
  "kind": "choice",
  "text": "Statement 1: In 10 years, the conference will be held.\nStatement 2: The conference will be held before 121 months.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q2b4fa86aafc",
  "kind": "choice",
  "text": "Statement 1: The coding competition will start after 3 days.\nStatement 2: The coding competition will start after 79 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q4f3a8029be9",
  "kind": "choice",
  "text": "Statement 1: Before 6 years, Lily will fly to New York.\nStatement 2: Lily will fly to New York after 25 months.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q6df09472120",
  "kind": "choice",
  "text": "Statement 1: The price of this stock will peak in August 1900.\nStatement 2: The price of this stock will peak before July 1970.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q824081c35ec",
  "kind": "choice",
  "text": "Claim: The UN Human Rights Council should be abolished\nPerspective: The political system of the UNHRC promotes Human Rights",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q9a69f248292",
  "kind": "choice",
  "text": "Proposition A: (y&~(((y>s)>(y&(y&~(~((j|~(y)))))))))\nProposition B: (((o|o)>j)>(z|(((j>z)>~(y))&j)))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q510da021413",
  "kind": "choice",
  "text": "Proposition A: ((~(i)&i)|~(i))\nProposition B: ~(i)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qb7797a8728e",
  "kind": "choice",
  "text": "Claim: It makes sense to drive to an out of town to a shopping centre\nPerspective: Out of town retail developments are bad for the environment",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q2f2b58f92a1",
  "kind": "choice",
  "text": "Statement 1: I had dinner with my friends from 4 AM to 12:00.\nStatement 2: I had dinner with my friends for less than 9 hours.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q125e9c7462a",
  "kind": "choice",
  "text": "Claim: A move to the left is good for Labour\nPerspective: Going left is step back not a step forward",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "qa2cc2a3f27b",
  "kind": "choice",
  "text": "Proposition A: ((~(u)|x)|x)\nProposition B: (u|~(~((((w&u)>w)&w))))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qb8dced13da3",
  "kind": "choice",
  "text": "Statement 1: I will start my office leave after 10 months.\nStatement 2: I will start my office leave before 299 days.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q60a39db76c1",
  "kind": "choice",
  "text": "Statement 1: My doctor's appointment was scheduled to take place at 08:00.\nStatement 2: My doctor's appointment was scheduled to take place before 1 AM.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q01bf0fb074d",
  "kind": "choice",
  "text": "Statement 1: In Mar 1951, the city had a huge power outage.\nStatement 2: After Jan 1922, the city had a huge power outage.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q48921a8eb05",
  "kind": "choice",
  "text": "Claim: Place Cameras in Courtrooms to Televise Court Cases\nPerspective: Witnesses and jurors could easily become involved in the media coverage of the case and place the trial at jeopardy.",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "qe6d8011bca1",
  "kind": "choice",
  "text": "Claim: Hosting the Olympics is a good investment\nPerspective: The Olympics gives athletes a goal and young people a chance to believe in themselves",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q33d556ec5db",
  "kind": "choice",
  "text": "Statement 1: In 8 days, I will start working on my MS application.\nStatement 2: I will start working on my MS application before 183 hours.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "qe786c1a68d8",
  "kind": "choice",
  "text": "Statement 1: My English class begins at 8 PM and ends at 05:00.\nStatement 2: My English class is scheduled for 9 hours.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qb6c22e2d39b",
  "kind": "choice",
  "text": "Claim: Deregulation and tax cuts should be embraced to lead the world out of economic crisis.\nPerspective: Stimulating businesses through tax-cuts and deregulation will be engine for economic recovery.",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q7db71c9cff4",
  "kind": "choice",
  "text": "Statement 1: We visited Disneyland from Thursday to Friday.\nStatement 2: We visited Disneyland for 10 days.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qd40d5931cfd",
  "kind": "choice",
  "text": "Statement 1: I will post this picture on Instagram after Tuesday.\nStatement 2: I will post this picture on Instagram before Sunday.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qab10470d33b",
  "kind": "choice",
  "text": "Statement 1: The coding competition was held from 4 AM to 4 PM.\nStatement 2: The coding competition was held for 12 hours.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q83464a17aca",
  "kind": "choice",
  "text": "Claim: Playoffs must be implemented in collegiate level american football\nPerspective: Playoffs Lead To More Exposure",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q6336e97f6df",
  "kind": "choice",
  "text": "Claim: China should be allowed more control over its own seas\nPerspective: Sovereignty of the Seas",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q36bfe0e7d8c",
  "kind": "choice",
  "text": "Proposition A: (b&~(v))\nProposition B: (l>b)",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qe0bdb343cd1",
  "kind": "choice",
  "text": "Statement 1: Before 8 years, the conference will be held.\nStatement 2: Before 68 months, the conference will be held.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q2d2a1313afd",
  "kind": "choice",
  "text": "Claim: Prosecutions help the healing process\nPerspective: Prosecutions don't get to the real truth",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q6465f85e865",
  "kind": "choice",
  "text": "Claim: Polygamous Marriage Should Be Recognised\nPerspective: Psychological harms of polygamy",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q55c4c8a9bb7",
  "kind": "choice",
  "text": "Statement 1: I will post this picture on Instagram after 10 days.\nStatement 2: I will post this picture on Instagram after 159 hours.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q05e428c6727",
  "kind": "choice",
  "text": "Statement 1: On 9th November 1969, this team will win the world cup.\nStatement 2: Before 10th May 1999, this team will win the world cup.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q7d5225a8354",
  "kind": "choice",
  "text": "Statement 1: Before Friday, the spring quarter began.\nStatement 2: After Thursday, the spring quarter began.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q99dcfc054e7",
  "kind": "choice",
  "text": "Claim: Smoking should further be restricted\nPerspective: Democratic systems should educate on smoking rather than restrict it",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q51005f0bb71",
  "kind": "choice",
  "text": "Statement 1: After 10 years, this team will win the world cup.\nStatement 2: Before 136 months, this team will win the world cup.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q0c82130aaac",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album is set to drop in 1902.\nStatement 2: Kendrick's album is set to drop before 1986.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q695df387aad",
  "kind": "choice",
  "text": "Statement 1: A tsunami will hit the coast before 12:00.\nStatement 2: A tsunami will hit the coast after 19:00.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q12050257c4e",
  "kind": "choice",
  "text": "Statement 1: The President gave a speech after 10 AM.\nStatement 2: The President gave a speech after 3 AM.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qfe62f4ad4fb",
  "kind": "choice",
  "text": "Claim: We must ban the promotion of diets\nPerspective: It's my body and I'll starve if I want to",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q75ad2225200",
  "kind": "choice",
  "text": "Proposition A: ~((~(t)|(o>i)))\nProposition B: ((t|(i|i))|~((((p>t)&i)>(e|b))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q714df7f402d",
  "kind": "choice",
  "text": "Statement 1: After 7 months, her internship at Google will begin.\nStatement 2: Her internship at Google will begin after 141 days.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q7bc0c477d98",
  "kind": "choice",
  "text": "Statement 1: After 5th March 1926, this article was published.\nStatement 2: After 24th Dec 1900, this article was published.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qeccf4e61889",
  "kind": "choice",
  "text": "Statement 1: Mary's party lasted from 2 AM to 14:00.\nStatement 2: Mary's party lasted for 13 hours.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q1129bec5e60",
  "kind": "choice",
  "text": "Statement 1: I will start working on my MS application in November.\nStatement 2: I will start working on my MS application after October.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q8ad96bde351",
  "kind": "choice",
  "text": "Statement 1: The servers will back up from 2 AM to 5 PM.\nStatement 2: The servers will back up for 16 hours.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qe7dc5c671ee",
  "kind": "choice",
  "text": "Statement 1: Michael will buy the house on 11th December 1919.\nStatement 2: Michael will buy the house after 5th Aug 1935.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qf151a920fa4",
  "kind": "choice",
  "text": "Statement 1: Before 3 months, this team will win the world cup.\nStatement 2: Before 204 days, this team will win the world cup.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qbc5378c64b7",
  "kind": "choice",
  "text": "Statement 1: On 9th Mar 1944, the conference will be held.\nStatement 2: After 26th May 1957, the conference will be held.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q2c01315d8d6",
  "kind": "choice",
  "text": "Claim: New prisons need to be built to ease overcrowding\nPerspective: The new prisons will just fill up as well.",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q9fb8684426e",
  "kind": "choice",
  "text": "Claim: Islamic State/Daesh is the most significant threat to the west\nPerspective: The west is insulated by distance from Daesh",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q78afa5cfc33",
  "kind": "choice",
  "text": "Proposition A: ~((e>~(((p>e)&p))))\nProposition B: ~((~((c&c))&(p|c)))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "qa9b5ad6f15a",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will begin before 8 years.\nStatement 2: Her internship at Google will begin after 151 months.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qa96e4f9816e",
  "kind": "choice",
  "text": "Statement 1: I will be going on a long vacation from Nov to Sep.\nStatement 2: I will be going on a long vacation for 11 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qcd651d6b30a",
  "kind": "choice",
  "text": "Statement 1: Lily will fly to New York in 2 days.\nStatement 2: Lily will fly to New York after 82 hours.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qb0067fba6bb",
  "kind": "choice",
  "text": "Statement 1: We will go to Disneyland in 3 years.\nStatement 2: Before 33 months, we will go to Disneyland.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q37eb5a573bb",
  "kind": "choice",
  "text": "Claim: Governments should introduce a flat tax\nPerspective: Why a flat tax is regressive",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "qf30f91c2877",
  "kind": "choice",
  "text": "Statement 1: In Jun, Michael bought the house.\nStatement 2: Before Oct, Michael bought the house.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q20393f84a23",
  "kind": "choice",
  "text": "Proposition A: (~((r>(u&e)))>~(~(m)))\nProposition B: (((~((~(e)&m))&(b&(h|(l|b))))>e)|(r>e))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qae58f97b703",
  "kind": "choice",
  "text": "Claim: We must believe in the woman's right to choose\nPerspective: Legalizing abortion defies the principle of life affirmation",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "qa9b4e7e438e",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict ended on 20th Jun 1958.\nStatement 2: The prison sentence of that convict ended before 9th May 1931.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q503c1f8a69c",
  "kind": "choice",
  "text": "Claim: Wind farms are a good solution to the energy crisis\nPerspective: Cost will make energy prices rise",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q50644c5df4b",
  "kind": "choice",
  "text": "Statement 1: The city had a huge power outage from Monday to Sunday.\nStatement 2: The city had a huge power outage for less than 7 days.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qba61c107841",
  "kind": "choice",
  "text": "Statement 1: We will go to Disneyland on Saturday.\nStatement 2: We will go to Disneyland after Friday.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qe829a864f51",
  "kind": "choice",
  "text": "Statement 1: The meeting began at 2 PM and got over at 12 AM.\nStatement 2: The meeting lasted for 11 hours.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q5b329e9f622",
  "kind": "choice",
  "text": "Statement 1: In 10 days, her internship at Google will begin.\nStatement 2: Her internship at Google will begin before 293 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q7515ed443ba",
  "kind": "choice",
  "text": "Statement 1: The landlord collected rent at 9 AM.\nStatement 2: The landlord collected rent after 14:00.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q1cf6cb9c45a",
  "kind": "choice",
  "text": "Statement 1: The pleasant weather here started before December.\nStatement 2: The pleasant weather here started after August.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q8d6cc5e7ebb",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict ended in Aug 1922.\nStatement 2: The prison sentence of that convict ended after Aug 1950.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q4f15bc678d5",
  "kind": "choice",
  "text": "Statement 1: The weather here is pleasant from April to March.\nStatement 2: The weather here is pleasant for 12 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q6d4c16f8f53",
  "kind": "choice",
  "text": "Claim: DNA testing is worth the money\nPerspective: Progression in medical science can only be a benefit",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q91e327d6160",
  "kind": "choice",
  "text": "Claim: Anti-Bribery Laws On Corporations Should Be Abolished\nPerspective: Anti-bribery laws lead to increased inequalities and new loopholes (response).",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "qe070442a758",
  "kind": "choice",
  "text": "Statement 1: The music concert started at 10 PM and ended at 12 PM.\nStatement 2: The music concert lasted for less than 14 hours.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q37f728d394a",
  "kind": "choice",
  "text": "Claim: The welfare system should be replaced with a negative income-tax model\nPerspective: It would encourage low income earners to work.",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "qbc8671c9a13",
  "kind": "choice",
  "text": "Proposition A: (~((~(p)&p))>h)\nProposition B: (h|h)",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q1b21ff48a33",
  "kind": "choice",
  "text": "Statement 1: Lily flew to New York on 13th May 1916.\nStatement 2: Lily flew to New York before 28th Oct 1904.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q81245158c0f",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from May 1906 to Oct 1999.\nStatement 2: The pandemic lasted for less than 11210 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q4da63686df1",
  "kind": "choice",
  "text": "Statement 1: On 7th March 1941, the country declared martial law.\nStatement 2: Before 10th July 1918, the country declared martial law.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qec1bdd9a990",
  "kind": "choice",
  "text": "Statement 1: My doctor's appointment took place from 9 AM to 07:00.\nStatement 2: My doctor's appointment took place for less than 23 hours.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q4fc008db76d",
  "kind": "choice",
  "text": "Claim: Access to the websites that deny the Holocaust must be blocked\nPerspective: Holocaust denial sites are an attack on group identities",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "qda851a3324b",
  "kind": "choice",
  "text": "Statement 1: I will be going on a long vacation from Jul to Nov.\nStatement 2: I will be going on a long vacation for 40 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qdf5952ef93f",
  "kind": "choice",
  "text": "Proposition A: ~((((h>p)>(p>q))|~((~(p)|(q>~(p))))))\nProposition B: (((s&((h>q)&~(h)))&h)|s)",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q05d3b85dc35",
  "kind": "choice",
  "text": "Claim: It is a good idea to build the Keystone XL pipeline\nPerspective: America should not become more dependent on oil",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective gives a reason to reject the claim."
 }
]
