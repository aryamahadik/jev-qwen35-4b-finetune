# A61 DI-TS label-noise blind read DTSB-blind_read-024

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/reads/answers/DTSB-blind_read-024.json

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
  "qid": "q6f2a50aa5d6",
  "kind": "choice",
  "text": "Statement 1: The country became a dictatorship in Nov 1920 which ended in Nov 1937.\nStatement 2: The country was under a dictatorship for 17 years 1 month.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qa92d35417de",
  "kind": "choice",
  "text": "Statement 1: The landlord will collect rent in 8 days.\nStatement 2: After 291 hours, the landlord will collect rent.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qbd244eeb5d6",
  "kind": "choice",
  "text": "Statement 1: In November, I will start my office leave.\nStatement 2: Before October, I will start my office leave.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qa1b411e7cf1",
  "kind": "choice",
  "text": "Statement 1: After 1 AM, Luke ate dinner.\nStatement 2: Before 13:00, Luke ate dinner.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q36772a79b87",
  "kind": "choice",
  "text": "Claim: punishment should fit the criminal\nPerspective: The onus should not be on punishing the criminal.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "qcc2bd36b27a",
  "kind": "choice",
  "text": "Claim: Any job is better than no job\nPerspective: Some jobs genuinely need higher qualifications.",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q32e07303398",
  "kind": "choice",
  "text": "Claim: Liberal democracies are better at providing people’s needs than non-democracies.\nPerspective: Democracies are more likely to be economically successful",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "qbdb0f8ddd76",
  "kind": "choice",
  "text": "Statement 1: The Presidential election is set to take place after 6 months.\nStatement 2: After 185 days, the Presidential election is set to take place.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qd28f777f523",
  "kind": "choice",
  "text": "Statement 1: A huge power outage in the city started on Tuesday and ended on Thursday.\nStatement 2: The city had a huge power outage for 3 days.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q0d168b50c52",
  "kind": "choice",
  "text": "Statement 1: Before Dec 1943, this team will win the world cup.\nStatement 2: After Oct 1978, this team will win the world cup.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q0630d6966c8",
  "kind": "choice",
  "text": "Statement 1: After 7 PM, Luke ate dinner.\nStatement 2: After 11 AM, Luke ate dinner.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q7b9883835c9",
  "kind": "choice",
  "text": "Statement 1: We started attending outdoor concerts in July 1929 and stopped in November 1966.\nStatement 2: We attended outdoor concerts for 449 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q01f388da33c",
  "kind": "choice",
  "text": "Claim: There must be a ban the sale of 3D printers to households\nPerspective: Household 3D printing can, in the short term, destroy developing economies",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q92f0b32ba8c",
  "kind": "choice",
  "text": "Statement 1: On 18th Dec 1947, my grandfather was born.\nStatement 2: After 11th February 1943, my grandfather was born.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qdae9f0e798d",
  "kind": "choice",
  "text": "Statement 1: My English class is scheduled from 12 PM to 7 PM.\nStatement 2: My English class is scheduled for 8 hours.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q801f3a33a66",
  "kind": "choice",
  "text": "Proposition A: ((y&v)&(v|(((y&((a&a)>d))>a)>y)))\nProposition B: ~(~((((~(d)&~(((c>v)&a)))>r)|(y|j))))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q1068d0b8de4",
  "kind": "choice",
  "text": "Statement 1: Before 2 years, the government budget will come out.\nStatement 2: Before 82 months, the government budget will come out.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q8498638c588",
  "kind": "choice",
  "text": "Proposition A: ((((p>g)|g)|(g|(~(g)|(n>(x&b)))))>(l&y))\nProposition B: ~((~((~(l)|(g|x)))&y))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q084ebd238a3",
  "kind": "choice",
  "text": "Statement 1: A tsunami will hit the coast after 9 days.\nStatement 2: A tsunami will hit the coast before 202 hours.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qada65ebc1e1",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict started in Mar 1901 and ended in June 1902.\nStatement 2: The prison sentence of that convict lasted for less than 15 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qce5a8875bd0",
  "kind": "choice",
  "text": "Proposition A: ((h>g)&g)\nProposition B: ~(((n&f)&k))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qe82798d6f2c",
  "kind": "choice",
  "text": "Statement 1: Before 1 year, Lily will fly to New York.\nStatement 2: Lily will fly to New York after 11 months.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qc85f507514e",
  "kind": "choice",
  "text": "Statement 1: The country was under a dictatorship from 1934 to 1956.\nStatement 2: The country was under a dictatorship for 22 years.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q09917bb48bc",
  "kind": "choice",
  "text": "Statement 1: The spring quarter will begin in 5 months.\nStatement 2: The spring quarter will begin after 202 days.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "qc73b0472f6f",
  "kind": "choice",
  "text": "Proposition A: ((s>s)>((o|(o>~(z)))>o))\nProposition B: (((r|z)|r)|(s&s))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "qfc125c3d51c",
  "kind": "choice",
  "text": "Statement 1: Before 10 days, he will leave his job.\nStatement 2: Before 324 hours, he will leave his job.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qc8742235fd0",
  "kind": "choice",
  "text": "Statement 1: I will start working on my MS application in 6 days.\nStatement 2: After 229 hours, I will start working on my MS application.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q7c17bb927e3",
  "kind": "choice",
  "text": "Statement 1: The servers backed up before 11 PM.\nStatement 2: The servers backed up after 18:00.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qa048368d44d",
  "kind": "choice",
  "text": "Statement 1: I will start working on my MS application after Oct.\nStatement 2: I will start working on my MS application before Nov.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qcbdd3be9888",
  "kind": "choice",
  "text": "Proposition A: (r&(r&((u>a)|l)))\nProposition B: ((a&(a|r))>r)",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q13eb3be54b3",
  "kind": "choice",
  "text": "Statement 1: On 19th Jul 1913, the tiger was last spotted.\nStatement 2: Before 22nd Mar 1979, the tiger was last spotted.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "qcc46ca0ef56",
  "kind": "choice",
  "text": "Statement 1: The war began in Oct 1927 and lasted until Jul 1942.\nStatement 2: The war lasted for less than 147 years 6 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q72a6fe5d776",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will last from May to Oct.\nStatement 2: Her internship at Google will last for less than 6 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q518813cde7a",
  "kind": "choice",
  "text": "Statement 1: Our favorite breakfast restaurant opened before August 1945.\nStatement 2: Our favorite breakfast restaurant opened after June 1979.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q7499f279f8c",
  "kind": "choice",
  "text": "Statement 1: The President's speech started at 6 AM and ended at 7 AM.\nStatement 2: The President gave a speech for 1 hour.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qbbb827f7213",
  "kind": "choice",
  "text": "Statement 1: Michael reached my house at 8 PM and left at 4 PM.\nStatement 2: Michael visited my house for 20 hours.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qb44433d0ac8",
  "kind": "choice",
  "text": "Proposition A: ~(((n>d)|~((d|n))))\nProposition B: (((d&(d&(n|~((d|d)))))|(o&o))>o)",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q2baedccf1b8",
  "kind": "choice",
  "text": "Claim: Bottled water should be banned\nPerspective: Bottled water costs up to 1,000 times the price of tap water",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q06b6e4930b8",
  "kind": "choice",
  "text": "Proposition A: ~((~((v|~((k&k))))|k))\nProposition B: ~((~(v)&~(k)))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "qe1d6aa40372",
  "kind": "choice",
  "text": "Statement 1: My grandfather was born in April 1908 and died in Oct 1969.\nStatement 2: My grandfather lived for less than 7380 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q723d4681556",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out before 2 years.\nStatement 2: The government budget will come out after 6 months.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q4e475a065e9",
  "kind": "choice",
  "text": "Claim: The Church of England should be separated from the British state.\nPerspective: Separating Church and State in England would be harmful to national identity. ",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q239fb91e8fd",
  "kind": "choice",
  "text": "Statement 1: My grandfather was born in 1941 and died in 1970.\nStatement 2: My grandfather lived for 30 years.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qca705096f59",
  "kind": "choice",
  "text": "Proposition A: ~(~((g>((~((i>(i&i)))&o)&(g|o)))))\nProposition B: ((o>~((((g|i)>o)&o)))>(i&i))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "qd7815335d2d",
  "kind": "choice",
  "text": "Claim: The Spread of Nuclear Weapons: More may be better\nPerspective: No country has an inherent right to invade or use aggression against another.",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qa79048e0268",
  "kind": "choice",
  "text": "Statement 1: After 8 months, the country will declare martial law.\nStatement 2: After 230 days, the country will declare martial law.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q03831f4417e",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict will end before 10 months.\nStatement 2: The prison sentence of that convict will end before 229 days.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q0dac63d7836",
  "kind": "choice",
  "text": "Statement 1: The park opens in May and closes in Feb.\nStatement 2: The park is open for 9 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q27b55197a1e",
  "kind": "choice",
  "text": "Statement 1: Before 20th May 1909, he left his job.\nStatement 2: Before 9th November 1931, he left his job.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q5e72e51b70b",
  "kind": "choice",
  "text": "Proposition A: ~(((k&(d>g))|((d&g)>q)))\nProposition B: ((o|q)|(~((q|q))&~((~(t)&w))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q8e84803295f",
  "kind": "choice",
  "text": "Proposition A: ~((~((e&((p|d)|~(m))))|(d|(l&t))))\nProposition B: ((n>t)|(f>(m>~(l))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q20eb75a6552",
  "kind": "choice",
  "text": "Statement 1: They will get married before 8 years.\nStatement 2: After 112 months, they will get married.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q2526ab7e4c7",
  "kind": "choice",
  "text": "Statement 1: The price of this stock will peak before 12 PM.\nStatement 2: The price of this stock will peak before 2 AM.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qff495b77ec2",
  "kind": "choice",
  "text": "Statement 1: My grandfather lived from October 1989 to April 2000.\nStatement 2: My grandfather lived for less than 10 years 7 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qe31ed58a430",
  "kind": "choice",
  "text": "Statement 1: Before 9 days, the servers will back up.\nStatement 2: The servers will back up before 215 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "qb8e4e78cd25",
  "kind": "choice",
  "text": "Claim: African governments must implement tougher protections for animals\nPerspective: Heavy handed approaches do not solve the motivations for poaching",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q44643ec658f",
  "kind": "choice",
  "text": "Claim: Increased taxes are good for America\nPerspective: 2.  No - it discourages incentive, increases dependence upon the government, and, if carried too far, impoverishes and oppresses people. ",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q37d396e721b",
  "kind": "choice",
  "text": "Statement 1: The failing company started issuing major layoffs on 23rd which ended on 28th.\nStatement 2: The failing company issued major layoffs for less than 6 days.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qbc796ddcca7",
  "kind": "choice",
  "text": "Proposition A: (~(((w|(e|e))|~(c)))&(e>w))\nProposition B: ~(e)",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q0e8798f5c02",
  "kind": "choice",
  "text": "Proposition A: ~(((q&(d>v))>(v|(((q>(p&v))>p)>(x&w)))))\nProposition B: ((~(v)&~(((v|x)|v)))>(q&(d&(w|p))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q6ec11e0e5d8",
  "kind": "choice",
  "text": "Statement 1: They will get married before 2 years.\nStatement 2: After 9 months, they will get married.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q39310d87f48",
  "kind": "choice",
  "text": "Statement 1: At 1 PM, we rode our bikes.\nStatement 2: After 15:00, we rode our bikes.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qe86ccbd12cd",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out after 9 months.\nStatement 2: The government budget will come out after 387 days.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q2218957e1cf",
  "kind": "choice",
  "text": "Claim: Countries with very harsh training methods from participating in international competitions should be banned.\nPerspective: Harsh training methods aren’t necessarily abusive.",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qfa7f1cb610d",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album is set to drop before 6 months.\nStatement 2: Before 77 days, Kendrick's album is set to drop.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qa887355214b",
  "kind": "choice",
  "text": "Statement 1: In 1949, Lily flew to New York.\nStatement 2: After 1955, Lily flew to New York.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qa8d74b7d0d7",
  "kind": "choice",
  "text": "Statement 1: We will go to Disneyland after April.\nStatement 2: We will go to Disneyland after August.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qd90832d1734",
  "kind": "choice",
  "text": "Statement 1: On 25th, the servers will back up.\nStatement 2: After 11th, the servers will back up.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q65cf5ef2531",
  "kind": "choice",
  "text": "Statement 1: Before 10 months, basketball season will end.\nStatement 2: Basketball season will end before 423 days.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q57dc5d4cfa3",
  "kind": "choice",
  "text": "Claim: Speed limits should be reduced\nPerspective: Negative impact on the environment ",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q7281fbbf333",
  "kind": "choice",
  "text": "Statement 1: After January 1940, Kendrick's album is set to drop.\nStatement 2: Before Dec 1906, Kendrick's album is set to drop.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q1da1e0d2178",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from Nov 1913 to November 1977.\nStatement 2: The pandemic lasted for 769 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q411a6f67dd1",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will last from Feb to Jun.\nStatement 2: Her internship at Google will last for 5 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q865d927c5ab",
  "kind": "choice",
  "text": "Statement 1: Basketball season lasts from Feb to Jun.\nStatement 2: Basketball season lasts for less than 5 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q8e928ddedb4",
  "kind": "choice",
  "text": "Statement 1: Before 2 AM, a tsunami will hit the coast.\nStatement 2: Before 11 AM, a tsunami will hit the coast.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qbf3746f55d7",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album is set to drop after 10 months.\nStatement 2: After 365 days, Kendrick's album is set to drop.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qd33bfefb85a",
  "kind": "choice",
  "text": "Statement 1: The war began in April 1958 and lasted until November 1990.\nStatement 2: The war lasted for less than 3910 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q931e79a895f",
  "kind": "choice",
  "text": "Statement 1: In June, Apple will release the new iPhone.\nStatement 2: After December, Apple will release the new iPhone.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qcbee03387fd",
  "kind": "choice",
  "text": "Claim: The voting age should be lowered to 16\nPerspective: YES, give them the rights they deserve!",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "q6026deb9b82",
  "kind": "choice",
  "text": "Statement 1: The coding competition started at 17:00 and ended at 1 PM.\nStatement 2: The coding competition was held for 21 hours.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q8a6dbbf95d1",
  "kind": "choice",
  "text": "Proposition A: ~(((n>a)|((~((y&(o&s)))&s)|~(q))))\nProposition B: ((d|~(~(j)))>s)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q304db934a13",
  "kind": "choice",
  "text": "Statement 1: The city will have a huge power outage before 8 days.\nStatement 2: The city will have a huge power outage after 89 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q893ff095905",
  "kind": "choice",
  "text": "Statement 1: Lily flew to New York from 10 PM to 12 PM.\nStatement 2: Lily flew to New York for less than 140 hours.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q56d4def94e6",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album dropped before 1941.\nStatement 2: Kendrick's album dropped before 1912.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q507d2f30c3b",
  "kind": "choice",
  "text": "Proposition A: ((r>~(v))&d)\nProposition B: ~(((k&k)&f))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qa7fae5111c1",
  "kind": "choice",
  "text": "Statement 1: The football game will begin at 6 AM and last until 3 AM.\nStatement 2: The football game will be telecasted for 22 hours.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qa9018218994",
  "kind": "choice",
  "text": "Claim: Police Service Should Be Armed (UK)\nPerspective: An armed police force will deter criminal behaviour",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qa8f4e519865",
  "kind": "choice",
  "text": "Statement 1: At 3 PM, the meeting will begin.\nStatement 2: Before 2 PM, the meeting will begin.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qcf2488cb007",
  "kind": "choice",
  "text": "Claim: Individuals should be able to legally bypass copyright protection technologies for fair use reasons.\nPerspective: Fair use can be misused",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "qe8bdce3e734",
  "kind": "choice",
  "text": "Statement 1: Before Aug, Michael bought the house.\nStatement 2: Before Mar, Michael bought the house.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q7ab23d9251e",
  "kind": "choice",
  "text": "Claim: We should believe in corporal punishment for adult offenders\nPerspective: Flogging will be over-utilised, rehabilitation will be under-utilised ",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q24e80fd8607",
  "kind": "choice",
  "text": "Statement 1: We will go to Disneyland after 8 years.\nStatement 2: Before 78 months, we will go to Disneyland.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q02632a13a05",
  "kind": "choice",
  "text": "Proposition A: (j&d)\nProposition B: ((c|(i&i))|((w|c)&j))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q89107fbf0e9",
  "kind": "choice",
  "text": "Proposition A: (((r|u)&h)&((r>g)&~((h&l))))\nProposition B: ((u|((p>p)&((l&e)&(p&u))))|e)",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q16efcc74b49",
  "kind": "choice",
  "text": "Statement 1: The music concert will start in in 6 days.\nStatement 2: Before 193 hours, the music concert will start in.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qdd436e5617e",
  "kind": "choice",
  "text": "Statement 1: I will start working on my MS application after 3 days.\nStatement 2: Before 8 hours, I will start working on my MS application.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q0a3d9036ee5",
  "kind": "choice",
  "text": "Statement 1: I will be leaving on a long vacation in January and be back in April.\nStatement 2: I will be going on a long vacation for 30 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qf8059c2f0c1",
  "kind": "choice",
  "text": "Statement 1: Lily will fly to New York before 3 years.\nStatement 2: After 1 month, Lily will fly to New York.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qa80047670dd",
  "kind": "choice",
  "text": "Proposition A: ~(((~(n)|((n&h)>(n>h)))&((n|(n|n))|s)))\nProposition B: (((h>n)>n)&(n>((s>h)&n)))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 }
]
