# A61 DI-TS label-noise blind read DTSA-blind_read-026

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/reads/answers/DTSA-blind_read-026.json

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
  "qid": "q4581cbc8a95",
  "kind": "choice",
  "text": "Statement 1: This team will win the world cup before 8 years.\nStatement 2: Before 36 months, this team will win the world cup.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q81b32f7f68e",
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
  "qid": "qc394064981a",
  "kind": "choice",
  "text": "Proposition A: ((x&(z>(h>h)))>~(w))\nProposition B: ~(((x>(l|((g>w)>z)))&((~(w)|x)&(x&w))))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q08430f6de99",
  "kind": "choice",
  "text": "Statement 1: The park will open before 10 days.\nStatement 2: The park will open before 307 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q244e7d64743",
  "kind": "choice",
  "text": "Statement 1: We started attending outdoor concerts in July 1908 and stopped in Jan 1947.\nStatement 2: We attended outdoor concerts for 462 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q24869c71cfe",
  "kind": "choice",
  "text": "Statement 1: In 7 months, the country will declare martial law.\nStatement 2: The country will declare martial law before 204 days.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qaa1d8b7ecca",
  "kind": "choice",
  "text": "Claim: Allow celebrities to switch off the limelight\nPerspective: It simply won’t work in an internet age",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qddd0b500ecc",
  "kind": "choice",
  "text": "Statement 1: Before February 1972, the prison sentence of that convict ended.\nStatement 2: After December 1940, the prison sentence of that convict ended.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qfcf63eeaff6",
  "kind": "choice",
  "text": "Claim: The ICC is biased against Africa\nPerspective: Africa has a strong voice in the ICC ",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "qbe6f5f07cf0",
  "kind": "choice",
  "text": "Statement 1: The city had a huge power outage from 15th to 16th.\nStatement 2: The city had a huge power outage for 2 days.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q621ab0ed142",
  "kind": "choice",
  "text": "Statement 1: Before Nov, our favorite breakfast restaurant opened.\nStatement 2: After August, our favorite breakfast restaurant opened.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qcc9a2ba83e1",
  "kind": "choice",
  "text": "Statement 1: Lily departed for New York at 11 AM and arrived at 8 AM.\nStatement 2: Lily flew to New York for less than 21 hours.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qd164bc6ee61",
  "kind": "choice",
  "text": "Statement 1: Lily will fly to New York in 10 years.\nStatement 2: After 141 months, Lily will fly to New York.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qaaad05e58aa",
  "kind": "choice",
  "text": "Proposition A: ((j&(~(o)>c))&(j|c))\nProposition B: (~(o)>(c&c))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q323fc9b27b8",
  "kind": "choice",
  "text": "Claim: People should lose their jobs for saying the wrong thing\nPerspective: Yes, it is against the law.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qfc89b892b94",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict lasted from October to January.\nStatement 2: The prison sentence of that convict lasted for 3 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qd8569cb1e08",
  "kind": "choice",
  "text": "Proposition A: ~(((l>d)>(~((a&(~(z)>t)))>~((l|d)))))\nProposition B: ((~(a)>~((f|i)))>(~(d)>(((f&i)|s)|d)))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qc765069e145",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out before 2 years.\nStatement 2: The government budget will come out after 6 months.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q27265901049",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album is set to drop before 10 years.\nStatement 2: Before 119 months, Kendrick's album is set to drop.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q4cc9b50f3c3",
  "kind": "choice",
  "text": "Proposition A: (~((b|((f&f)&b)))&f)\nProposition B: ((~(f)|(b&f))>((v&(b|k))&(b&(b>(v>b)))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q961e81c42d3",
  "kind": "choice",
  "text": "Claim: Allow donations of vital organs even at the expense of the donor's life\nPerspective: This would encourage coercion for some to die to save others",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q022a6b065c6",
  "kind": "choice",
  "text": "Statement 1: Michael bought the house after October 1955.\nStatement 2: Michael bought the house before Mar 1929.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "q6eeba4dfddb",
  "kind": "choice",
  "text": "Claim: Hosting the Olympic Games is beneficial\nPerspective: The Olympics increase valuable tourism, which can boost local economies",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "qc644a640fc7",
  "kind": "choice",
  "text": "Statement 1: We rode our bikes from 20:00 to 5 AM.\nStatement 2: We rode our bikes for 90 hours.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qd83c852f8d2",
  "kind": "choice",
  "text": "Statement 1: I will be leaving on a long vacation in October and be back in Nov.\nStatement 2: I will be going on a long vacation for 2 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q6b57ad746e7",
  "kind": "choice",
  "text": "Statement 1: Before 5 months, a tsunami will hit the coast.\nStatement 2: After 276 days, a tsunami will hit the coast.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q43cc69e23e9",
  "kind": "choice",
  "text": "Statement 1: The war will begin on Friday.\nStatement 2: The war will begin after Friday.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q738c1f2769d",
  "kind": "choice",
  "text": "Statement 1: After 7 AM, I had dinner with my friends.\nStatement 2: Before 5 PM, I had dinner with my friends.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q2df91840c6e",
  "kind": "choice",
  "text": "Statement 1: After 7 days, the country will declare martial law.\nStatement 2: The country will declare martial law after 72 hours.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q720fefa02e9",
  "kind": "choice",
  "text": "Statement 1: Basketball season starts in Dec and ends in Jan.\nStatement 2: Basketball season lasts for 1 month.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q4e04c55ba58",
  "kind": "choice",
  "text": "Statement 1: Michael bought the house before 18th Jul 1974.\nStatement 2: Michael bought the house before 17th October 1966.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qe790997d498",
  "kind": "choice",
  "text": "Proposition A: ~((((k&(k&k))>((y|y)&((y|k)>(k|a))))|a))\nProposition B: ((a>~((k&a)))|~(y))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q9cf95d7aa4b",
  "kind": "choice",
  "text": "Statement 1: After 6 days, her internship at Google will begin.\nStatement 2: Her internship at Google will begin after 203 hours.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q1bb0bc73742",
  "kind": "choice",
  "text": "Claim: Capitalism is better than socialism\nPerspective: Socialism was a twentieth century ideology which ran its course and ran out of steam when it became clear that Capitalism worked better",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "qa0cf5de3a32",
  "kind": "choice",
  "text": "Statement 1: The conference will be held in 3 years.\nStatement 2: The conference will be held before 83 months.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q6c70fbb7408",
  "kind": "choice",
  "text": "Statement 1: Before 5 days, I will have dinner with my friends.\nStatement 2: After 219 hours, I will have dinner with my friends.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q8ee56bfaa4a",
  "kind": "choice",
  "text": "Claim: Home Schooling Should Be Banned\nPerspective: Homeschooling Is Economically Beneficial",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q7d691f188bd",
  "kind": "choice",
  "text": "Statement 1: Before 5 months, my English class will begin.\nStatement 2: After 79 days, my English class will begin.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qcb45371f0bb",
  "kind": "choice",
  "text": "Statement 1: At 1 AM, the conference was held.\nStatement 2: Before 3 AM, the conference was held.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q523e7c438d2",
  "kind": "choice",
  "text": "Proposition A: ~((v>b))\nProposition B: ((w>((w|m)|(p>a)))&(((m>c)>w)>w))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qea53d94ff73",
  "kind": "choice",
  "text": "Claim: The UN should recognize a Palestinian state\nPerspective: An attempt to build up international support reinforces Israeli fears of a Palestinian state being used as a platform for attacks against them",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q0343dc436f8",
  "kind": "choice",
  "text": "Statement 1: Before 1 month, her internship at Google will begin.\nStatement 2: Her internship at Google will begin after 11 days.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qa85f8c0a3de",
  "kind": "choice",
  "text": "Proposition A: (~(v)|~((v>((t|t)>t))))\nProposition B: (o&(o|(j>g)))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q222b07af6c3",
  "kind": "choice",
  "text": "Statement 1: Michael visited my house from 8 AM to 7 PM.\nStatement 2: Michael visited my house for 12 hours.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q1719c75ee3d",
  "kind": "choice",
  "text": "Statement 1: Basketball season starts in August and ends in January.\nStatement 2: Basketball season lasts for less than 6 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qd140f268f44",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict lasted from Dec 1973 to Apr 1993.\nStatement 2: The prison sentence of that convict lasted for less than 233 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q66b50b80f32",
  "kind": "choice",
  "text": "Statement 1: After 1 year, they will get married.\nStatement 2: They will get married before 7 months.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qd3e41ff44e8",
  "kind": "choice",
  "text": "Proposition A: ~((((n|y)&(z&n))|(((y>n)&n)>s)))\nProposition B: (s|(y|n))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q49611db1350",
  "kind": "choice",
  "text": "Statement 1: Lily flew to New York from 05:00 to 07:00.\nStatement 2: Lily flew to New York for 20 hours.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q8221a64c0e5",
  "kind": "choice",
  "text": "Claim: Public Transport Should Be Free\nPerspective: We need to improve the transport system, this costs",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "qdaf02d64cc8",
  "kind": "choice",
  "text": "Proposition A: ~(~((c&y)))\nProposition B: (~(((e|s)&c))|x)",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "qadd7e04d077",
  "kind": "choice",
  "text": "Claim: Historical Artefacts Should Be Repatriated to Their Country of Origin\nPerspective: Artefacts should be accessible to the largest amount of visitors possible ",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q5729f736dee",
  "kind": "choice",
  "text": "Statement 1: Lily will fly to New York after 3 days.\nStatement 2: Before 30 hours, Lily will fly to New York.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q0fb000d7dc1",
  "kind": "choice",
  "text": "Statement 1: My grandfather was born in Oct 1926 and died in August 1967.\nStatement 2: My grandfather lived for 40 years 10 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q206f0bbffb9",
  "kind": "choice",
  "text": "Statement 1: Before Sep, Lily flew to New York.\nStatement 2: After Mar, Lily flew to New York.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qf51715fdd18",
  "kind": "choice",
  "text": "Claim: Books will be replaced at some point\nPerspective: textbooks are geting more and more expensive whilst universities are bringing the goods online ",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q9d2c52cd79d",
  "kind": "choice",
  "text": "Proposition A: ~(~(w))\nProposition B: (u>((e&(e>e))>p))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q945dd38f814",
  "kind": "choice",
  "text": "Claim: During riots it might make sense to block access to social messaging networks\nPerspective: Non violent methods of disrupting riots must be tried before using force",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q03977d358de",
  "kind": "choice",
  "text": "Proposition A: ~(((t&t)|(~((t>p))&(p|t))))\nProposition B: (t>(((t>p)>t)>p))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q0442066c92f",
  "kind": "choice",
  "text": "Claim: Swearing should be illegal\nPerspective: Waste of Police Time",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q94d1b8ceee3",
  "kind": "choice",
  "text": "Claim: The sale of violent video games/censor violent video games should be illegal\nPerspective: There are many flaws to the theory that violent video games cause real life violence.",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q14b61a93cb8",
  "kind": "choice",
  "text": "Statement 1: This team won the world cup after July 1920.\nStatement 2: This team won the world cup after Nov 1926.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q704e7ad9483",
  "kind": "choice",
  "text": "Statement 1: I will be leaving on a long vacation in Oct and be back in Dec.\nStatement 2: I will be going on a long vacation for 20 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q4d08c6fc6b5",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will last from Feb to Jun.\nStatement 2: Her internship at Google will last for 5 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q6e450f29bf5",
  "kind": "choice",
  "text": "Statement 1: After 6 days, our favorite breakfast restaurant will open.\nStatement 2: Before 63 hours, our favorite breakfast restaurant will open.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q9b733a35ae5",
  "kind": "choice",
  "text": "Proposition A: ((o>((z&k)&a))>z)\nProposition B: (((f&(~((m>z))&o))>m)&((f|o)|z))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "qb0d11cfb18d",
  "kind": "choice",
  "text": "Proposition A: (((g>(g|(g&n)))&g)|(g&~((g&n))))\nProposition B: ((g&n)|(g|g))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q1a4df3b32ca",
  "kind": "choice",
  "text": "Statement 1: After 7 months, the war will begin.\nStatement 2: The war will begin after 84 days.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q004b46932d4",
  "kind": "choice",
  "text": "Statement 1: The price of this stock will peak before 6 years.\nStatement 2: The price of this stock will peak before 41 months.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qc2a738a2c34",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from May 1974 to Oct 1977.\nStatement 2: The pandemic lasted for less than 34 years 2 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qd00b2c93907",
  "kind": "choice",
  "text": "Statement 1: The conference lasted from 10th to 18th.\nStatement 2: The conference lasted for 8 days.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qf223c8aec10",
  "kind": "choice",
  "text": "Statement 1: We started attending outdoor concerts in September 1912 and stopped in February 1944.\nStatement 2: We attended outdoor concerts for less than 377 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q0c073eb141f",
  "kind": "choice",
  "text": "Statement 1: I started working on my MS application on Sunday and got done on Monday.\nStatement 2: I worked on my MS application for 10 days.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qe15ecd60945",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will last from Wednesday to Monday.\nStatement 2: Her internship at Google will last for less than 50 days.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qbd192724d9d",
  "kind": "choice",
  "text": "Claim: We must invade and forcibly reunify the Korean peninsula\nPerspective: There is little interest in unification among young people in South Korea",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q06f675abf5e",
  "kind": "choice",
  "text": "Claim: South Ossetia should be independent\nPerspective: South Ossetian independence will help prevent future conflict ",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "qc00c90c30d9",
  "kind": "choice",
  "text": "Claim: Improving access to contraception will lower the number of teenage pregnancies\nPerspective: No it has proved opposite.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q6e90ec7b1a3",
  "kind": "choice",
  "text": "Statement 1: After July, the price of this stock will peak.\nStatement 2: After Nov, the price of this stock will peak.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q81d817412e9",
  "kind": "choice",
  "text": "Proposition A: (n|~((o>(o|((n&o)>((u|n)&w))))))\nProposition B: (o|((((n>(n&o))>o)&n)>w))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qae986e5dd0f",
  "kind": "choice",
  "text": "Proposition A: (y&~(((y>s)>(y&(y&~(~((j|~(y)))))))))\nProposition B: (((o|o)>j)>(z|(((j>z)>~(y))&j)))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "qa0f2ab2b050",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict lasted from March 1929 to Oct 1955.\nStatement 2: The prison sentence of that convict lasted for 265 years 10 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q0eef095fec8",
  "kind": "choice",
  "text": "Statement 1: After 10 years, the government budget will come out.\nStatement 2: The government budget will come out before 171 months.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qc1f91e8fc36",
  "kind": "choice",
  "text": "Proposition A: ((h>g)&g)\nProposition B: ~(((n&f)&k))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q92e92473db8",
  "kind": "choice",
  "text": "Statement 1: The conference will be held at 4 AM.\nStatement 2: The conference will be held after 8 AM.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q7c6e01b403a",
  "kind": "choice",
  "text": "Statement 1: In 10 days, the servers will back up.\nStatement 2: After 349 hours, the servers will back up.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q8720413ef43",
  "kind": "choice",
  "text": "Claim: Ethiopia is right to build a dam on the River Nile\nPerspective: Economic benefits of the dam for Ethiopia",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q4c414e55191",
  "kind": "choice",
  "text": "Proposition A: (~((i|i))>((~((q&o))&o)|q))\nProposition B: ~(~(((q|~(o))|(l>i))))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q8a7a823b6e8",
  "kind": "choice",
  "text": "Proposition A: ((e|b)&~((f|b)))\nProposition B: (p|f)",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "qd8974eabb97",
  "kind": "choice",
  "text": "Proposition A: ~(((w>(c|((w>~(o))&c)))|o))\nProposition B: (~(((w|c)>~(w)))>~((~(n)&c)))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "qdf393831ee4",
  "kind": "choice",
  "text": "Statement 1: Before 6 days, the government budget will come out.\nStatement 2: The government budget will come out after 141 hours.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qc37b2ce09eb",
  "kind": "choice",
  "text": "Statement 1: After 5 years, they will get married.\nStatement 2: Before 95 months, they will get married.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qe4c94e5226c",
  "kind": "choice",
  "text": "Statement 1: We attended outdoor concerts from Apr 1912 to Jun 1955.\nStatement 2: We attended outdoor concerts for 431 years 8 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q82dd31d16fc",
  "kind": "choice",
  "text": "Proposition A: ((((u|u)&u)|d)&l)\nProposition B: (u|(d|((z&u)|l)))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q5530cd5e5b1",
  "kind": "choice",
  "text": "Statement 1: After 3rd May 1974, the conference was held.\nStatement 2: Before 18th Apr 1964, the conference was held.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qb91429506f3",
  "kind": "choice",
  "text": "Statement 1: In May, the Presidential election took place.\nStatement 2: Before October, the Presidential election took place.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qa7e7507d2cc",
  "kind": "choice",
  "text": "Statement 1: My grandfather was born in May 1978 and died in Feb 1988.\nStatement 2: My grandfather lived for 9 years 10 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qecada7c42f5",
  "kind": "choice",
  "text": "Statement 1: In 8 months, we will go to Disneyland.\nStatement 2: After 117 days, we will go to Disneyland.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "q086e9a64943",
  "kind": "choice",
  "text": "Proposition A: ~((~(~(h))|(f>(f&h))))\nProposition B: (~(h)>~(w))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qd90caad3a0d",
  "kind": "choice",
  "text": "Statement 1: Basketball season will end on 17th.\nStatement 2: Basketball season will end after 7th.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 }
]
