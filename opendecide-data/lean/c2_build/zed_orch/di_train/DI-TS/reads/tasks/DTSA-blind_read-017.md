# A61 DI-TS label-noise blind read DTSA-blind_read-017

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/reads/answers/DTSA-blind_read-017.json

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
  "qid": "qbfb0f74896a",
  "kind": "choice",
  "text": "Statement 1: In 7 years, they will get married.\nStatement 2: They will get married after 55 months.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qb3047a274ac",
  "kind": "choice",
  "text": "Statement 1: Before 19th August 1973, the tiger was last spotted.\nStatement 2: After 18th August 1940, the tiger was last spotted.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "q4563fbd3ed1",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from October 1961 to February 2000.\nStatement 2: The pandemic lasted for 38 years 5 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qeb879540c11",
  "kind": "choice",
  "text": "Statement 1: My English class is scheduled from 8 PM to 13:00.\nStatement 2: My English class is scheduled for 18 hours.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q7d1c7d95f9e",
  "kind": "choice",
  "text": "Proposition A: ((t>~(~(k)))&(k&k))\nProposition B: (~(((k>~(k))>(k&c)))>~((k>k)))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q6041799e20a",
  "kind": "choice",
  "text": "Statement 1: The park is open from May to Oct.\nStatement 2: The park is open for less than 5 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q36b1154c0f7",
  "kind": "choice",
  "text": "Claim: Aid Should Be Tied To Human Rights\nPerspective: Government and citizens are often not the same entity.",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q97a2b14ae3b",
  "kind": "choice",
  "text": "Statement 1: We visited Disneyland from Saturday to Monday.\nStatement 2: We visited Disneyland for 3 days.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q5943ce15086",
  "kind": "choice",
  "text": "Statement 1: Before 5 months, basketball season will end.\nStatement 2: Basketball season will end before 31 days.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q6c968d99e28",
  "kind": "choice",
  "text": "Proposition A: (((x|a)&k)|(a&(k|k)))\nProposition B: (k|~((~(~((x>x)))|(~((k|~(k)))>k))))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qfd80c90ed11",
  "kind": "choice",
  "text": "Proposition A: ~(((~(n)|((n&h)>(n>h)))&((n|(n|n))|s)))\nProposition B: (((h>n)>n)&(n>((s>h)&n)))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qff3ee80cbba",
  "kind": "choice",
  "text": "Statement 1: The conference lasted from Thursday to Monday.\nStatement 2: The conference lasted for 5 days.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q0862eb455c1",
  "kind": "choice",
  "text": "Proposition A: ~((c>t))\nProposition B: ((((c>r)|h)>c)>i)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q71bc89b4931",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict started in March 1969 and ended in Apr 1973.\nStatement 2: The prison sentence of that convict lasted for 490 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q79968df9438",
  "kind": "choice",
  "text": "Statement 1: In Nov 1937, the government budget will come out.\nStatement 2: Before Jul 1999, the government budget will come out.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q01c57f143a3",
  "kind": "choice",
  "text": "Statement 1: Before Dec, I will start my office leave.\nStatement 2: Before Jul, I will start my office leave.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q2e66f04366f",
  "kind": "choice",
  "text": "Proposition A: ~(((j|s)|g))\nProposition B: (~((v>s))|((x|j)>~(s)))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q630b4eecd2d",
  "kind": "choice",
  "text": "Statement 1: On 28th July 1943, the conference will be held.\nStatement 2: After 19th November 1988, the conference will be held.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q70bf1433df1",
  "kind": "choice",
  "text": "Statement 1: We started attending outdoor concerts in Jan and stopped in Apr.\nStatement 2: We attended outdoor concerts for less than 3 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q44291b5809e",
  "kind": "choice",
  "text": "Claim: Public Transport Should Be Free\nPerspective: Will encourage people not to drive",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "qe0e20a9a9f4",
  "kind": "choice",
  "text": "Statement 1: They will get married after 3 months.\nStatement 2: They will get married after 83 days.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q3ef716badaa",
  "kind": "choice",
  "text": "Statement 1: I started working on my MS application in June.\nStatement 2: I started working on my MS application before March.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "q0db0f1b3ac7",
  "kind": "choice",
  "text": "Statement 1: The conference will be held in 9 years.\nStatement 2: Before 164 months, the conference will be held.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q3a50d60a992",
  "kind": "choice",
  "text": "Statement 1: Before 4 years, Lily will fly to New York.\nStatement 2: Lily will fly to New York before 80 months.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q86172820d5c",
  "kind": "choice",
  "text": "Claim: Remotely Controlled Weapons Systems Should Not Be Used In Combat\nPerspective: We put in danger less people in the combat",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q665f3588402",
  "kind": "choice",
  "text": "Statement 1: In 4 years, Michael will buy the house.\nStatement 2: After 102 months, Michael will buy the house.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qa1f9586fe5d",
  "kind": "choice",
  "text": "Statement 1: We visited Disneyland from 15:00 to 6 PM.\nStatement 2: We visited Disneyland for less than 3 hours.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q77a6bb07fbc",
  "kind": "choice",
  "text": "Proposition A: ~((~(((p>(l>s))&s))|c))\nProposition B: (c>~(~((l&(~((l>d))>(~(l)|s))))))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qfd267cfee8d",
  "kind": "choice",
  "text": "Statement 1: Michael will buy the house in December 1927.\nStatement 2: Michael will buy the house after Aug 1910.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qf36667a8bc0",
  "kind": "choice",
  "text": "Claim: Forced evictions are necessary for African cities to become global players.\nPerspective: Forced evictions are a natural path of development.",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "qb7d51bff89f",
  "kind": "choice",
  "text": "Statement 1: After 2 years, the government budget will come out.\nStatement 2: The government budget will come out before 77 months.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qabaf37c9e12",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict lasted from September 1974 to Jan 1982.\nStatement 2: The prison sentence of that convict lasted for 880 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qa80ac17c939",
  "kind": "choice",
  "text": "Proposition A: (((e&(k|l))&((e&u)>(m|b)))&(f&(e>h)))\nProposition B: ((f&l)|m)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q550078c6d4e",
  "kind": "choice",
  "text": "Claim: We should allow death penalty for the worst of the worst criminals\nPerspective: Execution helps alleviate the overcrowding of prisons.",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q03f5a9f5417",
  "kind": "choice",
  "text": "Statement 1: Before Sep 1985, the tiger was last spotted.\nStatement 2: Before Aug 1989, the tiger was last spotted.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qc99320c7ac1",
  "kind": "choice",
  "text": "Claim: Women should be allowed on the front line\nPerspective: Creating a level playing field for all applicants to college is the best way to create diversity.",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q9119580b120",
  "kind": "choice",
  "text": "Proposition A: (((((b&c)|~((l&l)))>b)|(y>y))>c)\nProposition B: (~(l)|(c&l))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qd4218682c1e",
  "kind": "choice",
  "text": "Statement 1: The coding competition started at 16:00.\nStatement 2: The coding competition started before 16:00.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qcff93f78e33",
  "kind": "choice",
  "text": "Statement 1: Basketball season starts in September and ends in Nov.\nStatement 2: Basketball season lasts for 2 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qfcaa3164338",
  "kind": "choice",
  "text": "Statement 1: The pandemic began in Sep 1947 and lasted until January 1952.\nStatement 2: The pandemic lasted for less than 520 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q3ad10f4f506",
  "kind": "choice",
  "text": "Claim: We can trust Republicans with the economy\nPerspective: Deregulation contributed to the banking crises and, therefore the 2009 economic crash ",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q34a3a617930",
  "kind": "choice",
  "text": "Proposition A: (q&i)\nProposition B: (s>~(i))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qcdcb3a4015f",
  "kind": "choice",
  "text": "Statement 1: He will leave his job after 2 days.\nStatement 2: After 145 hours, he will leave his job.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q328645f9ab8",
  "kind": "choice",
  "text": "Statement 1: At 11 AM, the landlord collected rent.\nStatement 2: After 2 PM, the landlord collected rent.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q04dcbc58346",
  "kind": "choice",
  "text": "Proposition A: (((((e&o)|k)&p)|((b|~(e))>(b|e)))&(b&b))\nProposition B: ((p&e)|(o|(o|p)))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q52551d8d6c5",
  "kind": "choice",
  "text": "Statement 1: The failing company issued major layoffs from 25th to 26th.\nStatement 2: The failing company issued major layoffs for 1 day.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q509f2fe3ede",
  "kind": "choice",
  "text": "Proposition A: ~((f>(k|k)))\nProposition B: (a>(n>m))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q3335d84c293",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will begin after 10 months.\nStatement 2: Before 335 days, her internship at Google will begin.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q7a37bb5eb00",
  "kind": "choice",
  "text": "Statement 1: After 10 months, the failing company will issue major layoffs.\nStatement 2: After 398 days, the failing company will issue major layoffs.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qa09da66f632",
  "kind": "choice",
  "text": "Statement 1: Jake is planning to move after 14th.\nStatement 2: Jake is planning to move before 8th.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qfe877700f79",
  "kind": "choice",
  "text": "Statement 1: This article will be published in 10 days.\nStatement 2: After 267 hours, this article will be published.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q743a3667584",
  "kind": "choice",
  "text": "Statement 1: He will leave his job before 2 months.\nStatement 2: He will leave his job before 75 days.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q2726bf1641b",
  "kind": "choice",
  "text": "Claim: It is important to use foreign aid funds to research and distribute software that allows bloggers and journalists in non-democratic countries to evade censorship and conceal their online activities.\nPerspective: This will needlessly antagonise non-democratic countries",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q240a32835db",
  "kind": "choice",
  "text": "Proposition A: (q&~(e))\nProposition B: (((v|t)&e)>~((~(v)|t)))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q63669420d2b",
  "kind": "choice",
  "text": "Proposition A: ~((((q|q)>~(~(((o|d)>~(i)))))|(q>d)))\nProposition B: (~(~(q))&(d>(k|h)))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q15b445d6258",
  "kind": "choice",
  "text": "Statement 1: After 6 months, the park will open.\nStatement 2: The park will open before 58 days.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qbe6b2d6cea2",
  "kind": "choice",
  "text": "Statement 1: The price of this stock will peak in 5 days.\nStatement 2: After 206 hours, the price of this stock will peak.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q681d839de29",
  "kind": "choice",
  "text": "Statement 1: In 1 month, the prison sentence of that convict will end.\nStatement 2: The prison sentence of that convict will end after 6 days.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q78ea1d92838",
  "kind": "choice",
  "text": "Statement 1: Before 9 months, the Presidential election is set to take place.\nStatement 2: The Presidential election is set to take place before 356 days.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q6889b5a1b05",
  "kind": "choice",
  "text": "Statement 1: The servers will back up before 1 day.\nStatement 2: The servers will back up before 23 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q04d94a2af8c",
  "kind": "choice",
  "text": "Statement 1: The park is open from 19:00 to 6 AM.\nStatement 2: The park is open for less than 12 hours.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q63bae4282c0",
  "kind": "choice",
  "text": "Statement 1: The pleasant weather here starts in May and ends in July.\nStatement 2: The weather here is pleasant for less than 2 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qe08ff60f311",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will last from 24th to 26th.\nStatement 2: Her internship at Google will last for less than 20 days.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q7824ba8ec9b",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict started in May 1961 and ended in March 1983.\nStatement 2: The prison sentence of that convict lasted for 263 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qbc15390c359",
  "kind": "choice",
  "text": "Proposition A: (((e&d)&(n|(d>v)))&d)\nProposition B: (((v&(n>m))>(d>i))|e)",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q703c8a60bd8",
  "kind": "choice",
  "text": "Proposition A: ((k|w)&(b|(w&k)))\nProposition B: ((w|((k|w)&(b|k)))|k)",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qc22da69f1aa",
  "kind": "choice",
  "text": "Proposition A: ~((((y|q)&~((l&(l>l))))|q))\nProposition B: ((l|q)>(y|l))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "qa6932e7d404",
  "kind": "choice",
  "text": "Statement 1: The music concert started in June.\nStatement 2: The music concert started before Jul.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q05bdc166439",
  "kind": "choice",
  "text": "Statement 1: In Dec, the pleasant weather here will start.\nStatement 2: Before Aug, the pleasant weather here will start.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q1d6a8664e5a",
  "kind": "choice",
  "text": "Statement 1: Lily will fly to New York after 8 days.\nStatement 2: After 310 hours, Lily will fly to New York.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qcc7ca80a95d",
  "kind": "choice",
  "text": "Statement 1: Apple will release the new iPhone before 8 months.\nStatement 2: Before 189 days, Apple will release the new iPhone.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q851e13ee3ef",
  "kind": "choice",
  "text": "Proposition A: ~(((u&g)>(s|~((o&((r>d)&g))))))\nProposition B: ((y>~(d))>(~((u&o))|(s>r)))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q26c58fec15f",
  "kind": "choice",
  "text": "Statement 1: We will go to Disneyland in 1 year.\nStatement 2: We will go to Disneyland before 7 months.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q1721b28965e",
  "kind": "choice",
  "text": "Claim: Corporal Punishment Should Be Reintroduced\nPerspective: It brings fear in the person ",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "q7e21e954864",
  "kind": "choice",
  "text": "Claim: Remove Bush tax cuts for the wealthy\nPerspective: Expiring Tax Cuts Would Cause a Double Dip Recession",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qae664adc51f",
  "kind": "choice",
  "text": "Statement 1: My doctor's appointment started at at 17:00 and went until 8 AM.\nStatement 2: My doctor's appointment took place for less than 16 hours.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qa0b335ee276",
  "kind": "choice",
  "text": "Statement 1: After 7 PM, Luke ate dinner.\nStatement 2: After 11 AM, Luke ate dinner.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q79d7aed3238",
  "kind": "choice",
  "text": "Proposition A: ((c|(x>f))&d)\nProposition B: (~(~((c&(c|c))))|~((d>y)))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q083b06c0791",
  "kind": "choice",
  "text": "Claim: Joe Calzaghe deserves to be recognized as one of the greatest boxers of all time\nPerspective: of course not he had 5 good fights and four of them were past there best.",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q10b15dea9c7",
  "kind": "choice",
  "text": "Proposition A: ~(((j&i)>~(~(c))))\nProposition B: ((~(c)|(j&c))|(y&p))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q85a32376984",
  "kind": "choice",
  "text": "Claim: Terrorism should not be allowed publicity\nPerspective: Publicity creates a public forum for terrorist organizations. ",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "qffe7f5fdbcd",
  "kind": "choice",
  "text": "Statement 1: The Presidential election is set to take place after 8 years.\nStatement 2: The Presidential election is set to take place before 85 months.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q10db5219648",
  "kind": "choice",
  "text": "Statement 1: The football game will begin at 07:00.\nStatement 2: The football game will begin after 01:00.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qf0dd9bc7a26",
  "kind": "choice",
  "text": "Statement 1: Before Nov 1962, Michael bought the house.\nStatement 2: After Mar 1950, Michael bought the house.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q3e02fe82396",
  "kind": "choice",
  "text": "Proposition A: (((h&h)&n)&(((n>i)>p)&~(c)))\nProposition B: (((h|~(p))>((x|((c|d)|i))|(n>i)))|x)",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q8cc806e8e79",
  "kind": "choice",
  "text": "Statement 1: In 1 day, my English class will begin.\nStatement 2: My English class will begin before 1 hour.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "qb326a3306b2",
  "kind": "choice",
  "text": "Claim: Put taxes/revenue from oil into a trust fund independent of politicians influence\nPerspective: An independent trust fund discourages investment.",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q760a7592a39",
  "kind": "choice",
  "text": "Statement 1: Before 2 years, the price of this stock will peak.\nStatement 2: The price of this stock will peak after 10 months.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q1e88b4012b8",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict lasted from January 1905 to July 1907.\nStatement 2: The prison sentence of that convict lasted for less than 31 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q6e0213ee4ab",
  "kind": "choice",
  "text": "Claim: The health benefits of genetically modified foods outweigh their risks\nPerspective: We don’t need to eat GM food to be healthy ",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q8a233d915dd",
  "kind": "choice",
  "text": "Claim: Abolish the monarchy.\nPerspective: Most other countries in Europe have abandoned the monarch",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "q694544dec31",
  "kind": "choice",
  "text": "Claim: Act to regulate the activities of Sovereign Wealth Funds\nPerspective: SWFs should be welcomed for the benefits they bring rather than ostracized for doing what others do. ",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "qf47a1e9e044",
  "kind": "choice",
  "text": "Statement 1: The conference lasted from Monday to Saturday.\nStatement 2: The conference lasted for less than 5 days.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qfede377b187",
  "kind": "choice",
  "text": "Proposition A: ((r>~(v))&d)\nProposition B: ~(((k&k)&f))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qf22733344d9",
  "kind": "choice",
  "text": "Proposition A: (~((w>(u>b)))&~(h))\nProposition B: ~((~((((x>(h&t))&x)|(u&(t>p))))&b))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q107442aef14",
  "kind": "choice",
  "text": "Claim: India’s Ban on the Satanic Verses is justified\nPerspective: Protection of Minors",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q1b22032dea1",
  "kind": "choice",
  "text": "Claim: (as a Christian Church) allow the ordination of gay and lesbian priests\nPerspective: Homosexuality is a sin in the Bible",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q1efe9c665da",
  "kind": "choice",
  "text": "Proposition A: (m&((n>(n|a))>~(a)))\nProposition B: (a>m)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "qb4a22d85056",
  "kind": "choice",
  "text": "Claim: A permanent UNSC seat with veto power must be reserved to an African country\nPerspective: More vetoes mean less action",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective gives a reason to reject the claim."
 }
]
