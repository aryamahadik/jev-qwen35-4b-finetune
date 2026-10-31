# A61 DI-TS label-noise blind read DTSB-blind_read-023

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/reads/answers/DTSB-blind_read-023.json

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
  "qid": "q02adb0cdc5d",
  "kind": "choice",
  "text": "Statement 1: After 1 day, the prison sentence of that convict will end.\nStatement 2: Before 14 hours, the prison sentence of that convict will end.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qa19bc9172ba",
  "kind": "choice",
  "text": "Claim: Allow voting at 16 in European Parliament elections\nPerspective: A slippery slope to forcing all countries to allow the vote at sixteen for all votes",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "q8c478590f23",
  "kind": "choice",
  "text": "Statement 1: The failing company will issue major layoffs after 10 days.\nStatement 2: After 252 hours, the failing company will issue major layoffs.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q17c07fc49e1",
  "kind": "choice",
  "text": "Statement 1: The music concert will start in in 9 months.\nStatement 2: The music concert will start in before 319 days.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qe4b987f8c8c",
  "kind": "choice",
  "text": "Claim: Abortion should be legal\nPerspective: Modern abortion procedures are safe and do not cause lasting health issues such as cancer and infertility.",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q0847f739ed8",
  "kind": "choice",
  "text": "Claim: European Parliament elections should involve only one voting district: all of Europe and not separate country seats\nPerspective: Big countries will dominate",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q5f333d25500",
  "kind": "choice",
  "text": "Claim: Legalize sex work in order to make controls more feasible and effective to combat HIV/AIDS\nPerspective: Legalising ensures health care and safe sex.",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q232c5d5b4e1",
  "kind": "choice",
  "text": "Proposition A: ~(((n>t)|(a|(~(f)|t))))\nProposition B: ~((f>(((n>a)>n)>(a&~(a)))))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q6d3463aea6e",
  "kind": "choice",
  "text": "Statement 1: On 27th, Michael will reach my house.\nStatement 2: Before 28th, Michael will reach my house.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qa9b4cefaedc",
  "kind": "choice",
  "text": "Statement 1: We attended outdoor concerts from May 1931 to Aug 1959.\nStatement 2: We attended outdoor concerts for less than 28 years 3 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q36261ad20b6",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from Feb 1947 to Jan 1961.\nStatement 2: The pandemic lasted for 139 years 2 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q65dae0d9684",
  "kind": "choice",
  "text": "Statement 1: Lily will fly to New York before 2 years.\nStatement 2: Lily will fly to New York before 27 months.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q1cc93debc60",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict started in Jul 1908 and ended in Jun 1928.\nStatement 2: The prison sentence of that convict lasted for 239 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q92e1f7e272c",
  "kind": "choice",
  "text": "Proposition A: ((f&f)&(f>r))\nProposition B: ~(~((~(~(((r>r)>g)))|((g>f)>f))))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qb4f2fbf173e",
  "kind": "choice",
  "text": "Statement 1: In 5 hours, our favorite breakfast restaurant will open.\nStatement 2: After 1 minutes, our favorite breakfast restaurant will open.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qf65b7258933",
  "kind": "choice",
  "text": "Statement 1: I will be on my office leave from 16th to 21st.\nStatement 2: I will be on my office leave for 6 days.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qca5d8f9377f",
  "kind": "choice",
  "text": "Statement 1: In 7 years, the government budget will come out.\nStatement 2: Before 117 months, the government budget will come out.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qca84352d611",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album is set to drop before 5 years.\nStatement 2: Before 105 months, Kendrick's album is set to drop.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q4f6a6abbc7f",
  "kind": "choice",
  "text": "Claim: The Western intervention in Libya has been a success\nPerspective: US intervention is not consistent with other aspects of US law",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "qadedf53db46",
  "kind": "choice",
  "text": "Statement 1: The Presidential election took place on 5th July 1996.\nStatement 2: The Presidential election took place before 11th December 1998.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qc9874535cbf",
  "kind": "choice",
  "text": "Statement 1: The conference will be held in 7 months.\nStatement 2: The conference will be held before 328 days.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qc8e76fd6bda",
  "kind": "choice",
  "text": "Claim: Government should be required to obtain warrants to access data that can be used to track an individual\nPerspective: Reducing trust in the state",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "qd2a418eca5a",
  "kind": "choice",
  "text": "Statement 1: Michael will buy the house after 7 years.\nStatement 2: After 34 months, Michael will buy the house.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qe4dfe94fa01",
  "kind": "choice",
  "text": "Statement 1: On 24th June 1905, we will go to Disneyland.\nStatement 2: Before 15th June 1997, we will go to Disneyland.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q9c2ebe4d044",
  "kind": "choice",
  "text": "Statement 1: Lily departed for New York at 11 AM and arrived at 8 AM.\nStatement 2: Lily flew to New York for less than 21 hours.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qfbfc3b1feed",
  "kind": "choice",
  "text": "Statement 1: I posted this picture on Instagram after Jul 1951.\nStatement 2: I posted this picture on Instagram after March 1948.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qf1ecee1359e",
  "kind": "choice",
  "text": "Proposition A: (e|(m&(e&o)))\nProposition B: (((~((m&m))>(b&a))&~(e))>v)",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "qd2e3503dd85",
  "kind": "choice",
  "text": "Statement 1: Michael bought the house in 1961.\nStatement 2: Michael bought the house before 1909.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q8aafd9a2885",
  "kind": "choice",
  "text": "Statement 1: Before 19th August 1973, the tiger was last spotted.\nStatement 2: After 18th August 1940, the tiger was last spotted.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "qce9eee689d2",
  "kind": "choice",
  "text": "Claim: Capital punishment should be abolished in Africa\nPerspective: Capital punishment is a comparatively small issue",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q2abc3b0739a",
  "kind": "choice",
  "text": "Proposition A: (~((q|s))&~((d>((r>g)&~(d)))))\nProposition B: (((s>q)>s)|(r>q))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "qed7ff6fd4b0",
  "kind": "choice",
  "text": "Statement 1: Lily will fly to New York after 8 days.\nStatement 2: After 310 hours, Lily will fly to New York.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qe16d87195a4",
  "kind": "choice",
  "text": "Statement 1: The President will give a speech before 1 day.\nStatement 2: Before 21 hours, the President will give a speech.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qaaf6e3795d5",
  "kind": "choice",
  "text": "Statement 1: The government budget came out in June.\nStatement 2: The government budget came out before Mar.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q62bcf7657be",
  "kind": "choice",
  "text": "Statement 1: Before July 1948, we started attending outdoor concerts.\nStatement 2: Before Dec 1904, we started attending outdoor concerts.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q42b83b183b9",
  "kind": "choice",
  "text": "Claim: Human Cloning has to be banned\nPerspective: Cloning should be allowed for those who can’t otherwise have a child",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q434d3af7386",
  "kind": "choice",
  "text": "Statement 1: The conference will be held in 9 years.\nStatement 2: Before 164 months, the conference will be held.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qb60f3b9e27d",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out after 14th.\nStatement 2: The government budget will come out before 27th.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q43e45231027",
  "kind": "choice",
  "text": "Proposition A: ((t&(h&((h&h)>f)))&((f>t)|(~(~(h))|f)))\nProposition B: ((f>l)&(h>((l|((t>(h|t))&(t&t)))|(f>l))))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q26d19dc281f",
  "kind": "choice",
  "text": "Statement 1: Before 9 days, I will have dinner with my friends.\nStatement 2: I will have dinner with my friends before 330 hours.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qa04da66ee28",
  "kind": "choice",
  "text": "Statement 1: After 6 months, Kendrick's album is set to drop.\nStatement 2: After 63 days, Kendrick's album is set to drop.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q8a507056749",
  "kind": "choice",
  "text": "Statement 1: The war lasted from Oct 1931 to Nov 1997.\nStatement 2: The war lasted for 793 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q9c49130460d",
  "kind": "choice",
  "text": "Statement 1: Before 1 day, the park will open.\nStatement 2: The park will open after 35 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q339ab4387dd",
  "kind": "choice",
  "text": "Claim: Same-Sex Marriage Should Be Legal\nPerspective: Expanding the Right to Marry Serves the State",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "q1e17604732a",
  "kind": "choice",
  "text": "Statement 1: We attended outdoor concerts from Jan 1959 to Feb 1971.\nStatement 2: We attended outdoor concerts for less than 145 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q04fdec13f1b",
  "kind": "choice",
  "text": "Statement 1: The park is open from 16th to 22nd.\nStatement 2: The park is open for 60 days.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q9058aac921e",
  "kind": "choice",
  "text": "Statement 1: Before Nov 1901, Kendrick's album is set to drop.\nStatement 2: After Dec 1961, Kendrick's album is set to drop.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q7db9b1f829d",
  "kind": "choice",
  "text": "Statement 1: On 19th May 1984, they will get married.\nStatement 2: Before 11th Jul 1917, they will get married.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qf2565a1fd37",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out before Apr 1935.\nStatement 2: The government budget will come out before Feb 1913.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "qca4fbdd9953",
  "kind": "choice",
  "text": "Statement 1: The Presidential election is set to take place in 10 years.\nStatement 2: After 77 months, the Presidential election is set to take place.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q4cfbfd8b8a2",
  "kind": "choice",
  "text": "Statement 1: The war lasted from November 1925 to November 1989.\nStatement 2: The war lasted for 64 years.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q90936ddbdad",
  "kind": "choice",
  "text": "Proposition A: (l&((r|w)|~(~(((l&(e&e))&~((w>w)))))))\nProposition B: (((~(r)>c)|((l&c)&((w&l)>c)))|w)",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q0529536130e",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album dropped after Jan 1956.\nStatement 2: Kendrick's album dropped after November 1931.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "qa38d820151b",
  "kind": "choice",
  "text": "Proposition A: ((e|y)&y)\nProposition B: (((r&y)|~(r))&(y|((r|e)>(y>e))))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q0817afc8c7e",
  "kind": "choice",
  "text": "Claim: Violent video games cause violent crime\nPerspective: Violent video games desensitise users",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q9562ef415e8",
  "kind": "choice",
  "text": "Claim: People should become vegetarian\nPerspective: Vegetarianism is healthier ",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "qf80ecf9508d",
  "kind": "choice",
  "text": "Statement 1: After 6 years, the government budget will come out.\nStatement 2: After 24 months, the government budget will come out.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "qcca98081ab7",
  "kind": "choice",
  "text": "Statement 1: In 3 years, Michael will buy the house.\nStatement 2: After 6 months, Michael will buy the house.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q9515190762f",
  "kind": "choice",
  "text": "Statement 1: Before 9 days, this article will be published.\nStatement 2: This article will be published before 302 hours.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qd8e66d1d6c1",
  "kind": "choice",
  "text": "Statement 1: In October, the park was open.\nStatement 2: Before Jun, the park was open.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q47f32ead424",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out after 17th July 1950.\nStatement 2: The government budget will come out before 11th May 1953.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q5a5aa07ee98",
  "kind": "choice",
  "text": "Statement 1: Before December, I started my office leave.\nStatement 2: After July, I started my office leave.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qa949cff20da",
  "kind": "choice",
  "text": "Statement 1: Before 2 months, the price of this stock will peak.\nStatement 2: Before 125 days, the price of this stock will peak.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "q07a6ef2260a",
  "kind": "choice",
  "text": "Statement 1: The country was under a dictatorship from November 1908 to November 1917.\nStatement 2: The country was under a dictatorship for less than 1080 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q84facb2ac94",
  "kind": "choice",
  "text": "Proposition A: (~(((h|f)>((f>r)|i)))&h)\nProposition B: ~(((~((i|i))&r)|((h>f)&r)))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qae7141ff120",
  "kind": "choice",
  "text": "Statement 1: The war began in July.\nStatement 2: The war began after March.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q2bfa8a4b203",
  "kind": "choice",
  "text": "Proposition A: (((~((k|k))|k)&(~(o)|~(~(h))))&m)\nProposition B: (m|k)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q93156faf08c",
  "kind": "choice",
  "text": "Statement 1: After 1 month, this team will win the world cup.\nStatement 2: This team will win the world cup after 87 days.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q6363b5f6fc6",
  "kind": "choice",
  "text": "Statement 1: The coding competition was held from 6th to 8th.\nStatement 2: The coding competition was held for less than 20 days.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q5d2d7c1e461",
  "kind": "choice",
  "text": "Statement 1: After 1 day, final grades are due.\nStatement 2: After 29 hours, final grades are due.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qa7e2614e7a9",
  "kind": "choice",
  "text": "Proposition A: (i&b)\nProposition B: (b|~(((n&~(i))&((~(l)>~(n))&t))))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q460b85d3ec3",
  "kind": "choice",
  "text": "Statement 1: We will go to Disneyland on 26th Oct 1948.\nStatement 2: We will go to Disneyland before 13th Mar 1962.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q5e2274b2db3",
  "kind": "choice",
  "text": "Proposition A: ~((r>u))\nProposition B: (r&((r&(((u&f)>(f&f))>(~(u)|(r>f))))|r))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q80df736d80c",
  "kind": "choice",
  "text": "Statement 1: We rode our bikes from 00:00 to 14:00.\nStatement 2: We rode our bikes for less than 14 hours.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q4f262868bc5",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album is set to drop in 8 years.\nStatement 2: Kendrick's album is set to drop after 149 months.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qb1be8833aeb",
  "kind": "choice",
  "text": "Claim: Parents have to be allowed to monitor their children's online and mobile communications\nPerspective: Monitoring decreases children’s involvement with pornography. ",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qe70c788f2d3",
  "kind": "choice",
  "text": "Statement 1: The coding competition was held from 12 PM to 7 AM.\nStatement 2: The coding competition was held for less than 190 hours.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qf7261aefb29",
  "kind": "choice",
  "text": "Statement 1: A tsunami will hit the coast before 9 days.\nStatement 2: A tsunami will hit the coast after 303 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q6e729261817",
  "kind": "choice",
  "text": "Statement 1: After Jul, the conference was held.\nStatement 2: After December, the conference was held.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qa8ae4349665",
  "kind": "choice",
  "text": "Statement 1: The spring quarter begins in December and ends in March.\nStatement 2: The spring quarter lasts for 30 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qaa311315976",
  "kind": "choice",
  "text": "Statement 1: In February, the prison sentence of that convict will end.\nStatement 2: After February, the prison sentence of that convict will end.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q240626606cb",
  "kind": "choice",
  "text": "Statement 1: We started attending outdoor concerts in Jan 1936 and stopped in Jul 1984.\nStatement 2: We attended outdoor concerts for 5820 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qfc687221c58",
  "kind": "choice",
  "text": "Claim: Recognise Kosovo as an independent state\nPerspective: Self-determination is a human right",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q77b133d2ec6",
  "kind": "choice",
  "text": "Statement 1: Apple will release the new iPhone before 1 month.\nStatement 2: After 57 days, Apple will release the new iPhone.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q4329b0ff53d",
  "kind": "choice",
  "text": "Proposition A: (~(~((~(m)&g)))|~((v>b)))\nProposition B: (m>(((b&v)&v)>g))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qa6a7844dd58",
  "kind": "choice",
  "text": "Statement 1: After 8 years, the price of this stock will peak.\nStatement 2: The price of this stock will peak before 105 months.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q501230037bd",
  "kind": "choice",
  "text": "Statement 1: My grandfather was born on 15th January 1937.\nStatement 2: My grandfather was born before 24th February 1980.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q7d603b498dd",
  "kind": "choice",
  "text": "Statement 1: The city had a huge power outage from 13:00 to 20:00.\nStatement 2: The city had a huge power outage for 70 hours.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q4713b766edf",
  "kind": "choice",
  "text": "Claim: War criminals should be prosecuted\nPerspective: Problems with symbolic justice",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q6e62c3e6b74",
  "kind": "choice",
  "text": "Statement 1: The conference was held on 12th Jan 1941.\nStatement 2: The conference was held before 14th Jun 1934.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qd9f6d5464a7",
  "kind": "choice",
  "text": "Claim: Britain should become a republic\nPerspective: The Monarchy is backward and prejudiced",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q3d31977affc",
  "kind": "choice",
  "text": "Claim: The US and Israel should join the International Criminal Court\nPerspective: ICC trials violate the due process guarantees of the US constitution",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q5561883ce64",
  "kind": "choice",
  "text": "Proposition A: (~((g|(g|(v&v))))&(~(m)|~(~(e))))\nProposition B: ~(((v&e)&~(t)))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q5c765c3f0c6",
  "kind": "choice",
  "text": "Statement 1: After 10th, Michael will buy the house.\nStatement 2: After 18th, Michael will buy the house.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qed0fd6312dd",
  "kind": "choice",
  "text": "Statement 1: After 1965, we went to Disneyland.\nStatement 2: After 1950, we went to Disneyland.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q739f3b279e4",
  "kind": "choice",
  "text": "Statement 1: The coding competition started at 1 PM and ended at 3 AM.\nStatement 2: The coding competition was held for 14 hours.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q5e098a0fc73",
  "kind": "choice",
  "text": "Statement 1: The Presidential election took place in October.\nStatement 2: The Presidential election took place before September.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q480b1aa6801",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from December 1907 to April 1977.\nStatement 2: The pandemic lasted for less than 69 years 4 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qf4fc360cd42",
  "kind": "choice",
  "text": "Statement 1: The war began in Feb 1955 and lasted until Sep 1956.\nStatement 2: The war lasted for 15 years 10 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 }
]
