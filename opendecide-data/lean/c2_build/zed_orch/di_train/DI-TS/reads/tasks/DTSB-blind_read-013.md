# A61 DI-TS label-noise blind read DTSB-blind_read-013

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/reads/answers/DTSB-blind_read-013.json

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
  "qid": "qf4a519351d7",
  "kind": "choice",
  "text": "Claim: The United Nations has a responsibility to protect.\nPerspective: Blanket commitment creates a slippery slope of when to intervene.",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q53f97e01579",
  "kind": "choice",
  "text": "Claim: Children Should Have The Right To Vote In Elections\nPerspective: Sixteen years would be a better option in developed countries",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "q456259c0d82",
  "kind": "choice",
  "text": "Claim: The EU, USA and other western donors should not fund any Palestinian government in which terrorist organisations participate\nPerspective: Withholding funds will cause Palestine to rely on anti-Israeli regimes. ",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "qa932c65525f",
  "kind": "choice",
  "text": "Statement 1: The park opens in March and closes in July.\nStatement 2: The park is open for 40 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qb53f7dad275",
  "kind": "choice",
  "text": "Statement 1: My English class will begin after June.\nStatement 2: My English class will begin after August.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q9d04a4debab",
  "kind": "choice",
  "text": "Statement 1: Before 7 months, the price of this stock will peak.\nStatement 2: The price of this stock will peak before 185 days.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q7816a1c8f46",
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
  "qid": "qf3e7db815e8",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will begin before 17th June 1949.\nStatement 2: Her internship at Google will begin before 12th September 1939.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "qcd03781779c",
  "kind": "choice",
  "text": "Statement 1: In 7 months, the prison sentence of that convict will end.\nStatement 2: The prison sentence of that convict will end before 234 days.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q826471fa9ab",
  "kind": "choice",
  "text": "Statement 1: I posted this picture on Instagram on 3rd September 1931.\nStatement 2: I posted this picture on Instagram before 9th Apr 1902.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qb50e3ec7c6d",
  "kind": "choice",
  "text": "Claim: Actively circumventing Internet censorship is a legitimate foreign policy tool\nPerspective: It is legitimate to undermine illegitimate governments to promote human rights",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q7927b495fde",
  "kind": "choice",
  "text": "Claim: Remove the words \"under God\" from the American Pledge of Allegiance\nPerspective: “Under God” is part of American tradition and history",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "qc6990ec9437",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict will end after 1 year.\nStatement 2: Before 69 months, the prison sentence of that convict will end.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q4c5a2ee9043",
  "kind": "choice",
  "text": "Statement 1: They will get married before 9 years.\nStatement 2: They will get married before 142 months.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qecd5a723487",
  "kind": "choice",
  "text": "Statement 1: The landlord will collect rent in 7 days.\nStatement 2: After 284 hours, the landlord will collect rent.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "qcf8e6768378",
  "kind": "choice",
  "text": "Statement 1: After 4 days, a tsunami will hit the coast.\nStatement 2: A tsunami will hit the coast after 40 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q274149d4c55",
  "kind": "choice",
  "text": "Statement 1: Lily will fly to New York before 6 months.\nStatement 2: Lily will fly to New York after 246 days.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q309e32a9f23",
  "kind": "choice",
  "text": "Statement 1: Before 3 days, the failing company will issue major layoffs.\nStatement 2: The failing company will issue major layoffs after 69 hours.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q83ca63ff177",
  "kind": "choice",
  "text": "Statement 1: The conference will be held before 2 years.\nStatement 2: After 11 months, the conference will be held.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qae0934c589b",
  "kind": "choice",
  "text": "Claim: There is a need for developing tactical nuclear weapons\nPerspective: any conflict will rapidly de-escalate",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q3d27d64da58",
  "kind": "choice",
  "text": "Statement 1: In 9 years, Kendrick's album is set to drop.\nStatement 2: After 67 months, Kendrick's album is set to drop.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q08523bb068a",
  "kind": "choice",
  "text": "Proposition A: ~((u|(u|u)))\nProposition B: (u>((u>(u|(~(u)|u)))>~(u)))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qc9f3aa84ce3",
  "kind": "choice",
  "text": "Claim: The American Jobs Act should pass\nPerspective: The American Jobs Act is Not Deficit Neutral",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q0bbd904fcdb",
  "kind": "choice",
  "text": "Statement 1: The weather here is pleasant from July to January.\nStatement 2: The weather here is pleasant for less than 6 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q51dc03bfb03",
  "kind": "choice",
  "text": "Proposition A: (((((k|k)&d)|k)>(d>(k>d)))>k)\nProposition B: ((k|k)>~(((d&~(~(k)))&d)))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q64e602cda8e",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from Mar 1930 to August 1971.\nStatement 2: The pandemic lasted for less than 414 years 2 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q1ed5f3b4409",
  "kind": "choice",
  "text": "Proposition A: ~(j)\nProposition B: ~(j)",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q6d57af036a5",
  "kind": "choice",
  "text": "Statement 1: The Presidential election took place after 5th July 2000.\nStatement 2: The Presidential election took place after 3rd March 1946.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q65151c79170",
  "kind": "choice",
  "text": "Statement 1: A tsunami will hit the coast on Thursday.\nStatement 2: A tsunami will hit the coast after Tuesday.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qb84544b0cee",
  "kind": "choice",
  "text": "Claim: The use of child performers should be banned\nPerspective: It is unethical to expose children to the pressures of performing",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q8b931e5ceaf",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will begin before 1 month.\nStatement 2: Her internship at Google will begin before 154 days.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q27633ed08d4",
  "kind": "choice",
  "text": "Claim: ID cards and the National Identity Register should be scrapped\nPerspective: ID cards will lead to increased discrimination",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q67cecf1fcca",
  "kind": "choice",
  "text": "Statement 1: The war began in November 1943 and lasted until August 1970.\nStatement 2: The war lasted for 321 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q36f85000375",
  "kind": "choice",
  "text": "Statement 1: The football game will be telecasted from 9 AM to 2 PM.\nStatement 2: The football game will be telecasted for 5 hours.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q90dd3665d6c",
  "kind": "choice",
  "text": "Statement 1: The park opens on Thursday and closes on Saturday.\nStatement 2: The park is open for 3 days.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q08d33863646",
  "kind": "choice",
  "text": "Statement 1: We attended outdoor concerts from July 1959 to August 1986.\nStatement 2: We attended outdoor concerts for 325 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qb6f35ea40a0",
  "kind": "choice",
  "text": "Statement 1: The music concert will start in in August.\nStatement 2: The music concert will start in after April.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q9f62aef276e",
  "kind": "choice",
  "text": "Proposition A: ((d&~((~((d>y))&(j|l))))&~(~(d)))\nProposition B: (((~((u&d))>(y|y))>(d&y))|~(l))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qd55b35ce3f3",
  "kind": "choice",
  "text": "Statement 1: I started working on my MS application on 4th and got done on 9th.\nStatement 2: I worked on my MS application for 50 days.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qa773033ce83",
  "kind": "choice",
  "text": "Statement 1: Before 2nd Jan 1910, the Presidential election is set to take place.\nStatement 2: After 26th March 1910, the Presidential election is set to take place.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q93915596e83",
  "kind": "choice",
  "text": "Claim: Developing nations should place restrictions on rural-urban migration\nPerspective: The government has a right to make decisions in the best interest of the people",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qa677c1e77e9",
  "kind": "choice",
  "text": "Proposition A: (r&z)\nProposition B: (((e|r)|(~((v>k))&~((r>p))))&(v|z))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q6a35ac7353d",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will last from June to Apr.\nStatement 2: Her internship at Google will last for 11 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q67aa27235c0",
  "kind": "choice",
  "text": "Statement 1: The spring quarter lasts from Jul to March.\nStatement 2: The spring quarter lasts for 80 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qc4ad59f2278",
  "kind": "choice",
  "text": "Claim: All nations should ban bullfighting\nPerspective: Fighting bulls have a better quality of life than meat-producing bulls",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q4df82120c4f",
  "kind": "choice",
  "text": "Statement 1: On 27th February 1994, the prison sentence of that convict ended.\nStatement 2: After 20th Mar 1981, the prison sentence of that convict ended.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qb1d1679df14",
  "kind": "choice",
  "text": "Proposition A: ~((~(m)|(((s|f)>(b|f))|(m>f))))\nProposition B: (u>~((((f&g)&(u|f))&u)))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q3acd6073909",
  "kind": "choice",
  "text": "Claim: The War in Iraq was Worth the Cost\nPerspective: The war was illegal and the removal of Saddam should have been left to the Iraqis Yet another puppet regime is not what the Middle East needs",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "q636d502ec54",
  "kind": "choice",
  "text": "Claim: Poorer Countries Should Abandon Free Trade Agreements\nPerspective: Free trade is not Free Trade    : Labor welfare for the price of macroeconomic indicators growth",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q19d810fbf07",
  "kind": "choice",
  "text": "Statement 1: In 7 years, Michael will buy the house.\nStatement 2: Michael will buy the house before 93 months.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "q98cf8398c82",
  "kind": "choice",
  "text": "Claim: Throw Russia out of the G8\nPerspective: Simply narrows the G8 making it irrelevant",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "qec612b9396d",
  "kind": "choice",
  "text": "Statement 1: I will have dinner with my friends in 7 days.\nStatement 2: Before 152 hours, I will have dinner with my friends.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q04ac2278f9e",
  "kind": "choice",
  "text": "Statement 1: They got married on 26th May 1925.\nStatement 2: They got married before 26th Jul 1934.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q4b90173e868",
  "kind": "choice",
  "text": "Claim: A fat tax should be implemented.\nPerspective: Unhealthy food is cheaper",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q936d488927f",
  "kind": "choice",
  "text": "Statement 1: In 2 hours, this article will be published.\nStatement 2: Before 1 minutes, this article will be published.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q6187a43dd06",
  "kind": "choice",
  "text": "Proposition A: ((t|(a|t))&(a|a))\nProposition B: ((t&a)|((a>t)>~((a>t))))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qf5dde5da70c",
  "kind": "choice",
  "text": "Proposition A: ((t|(y>(a>z)))>~(~(y)))\nProposition B: (x>(~((y>y))&((y>x)|t)))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q1d7c7f44c51",
  "kind": "choice",
  "text": "Proposition A: ~(d)\nProposition B: ((~((~(d)&e))&e)>((y|(x|(x|h)))|h))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qfe4ca38e1d0",
  "kind": "choice",
  "text": "Statement 1: The country will declare martial law after 6 days.\nStatement 2: Before 256 hours, the country will declare martial law.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qc9f62658a60",
  "kind": "choice",
  "text": "Statement 1: Jake is planning to move after 7 months.\nStatement 2: Jake is planning to move after 288 days.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q8d4313d7ea0",
  "kind": "choice",
  "text": "Statement 1: My grandfather lived from November 1910 to September 1945.\nStatement 2: My grandfather lived for less than 419 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qa214c684bd3",
  "kind": "choice",
  "text": "Statement 1: Before 5 days, I will have dinner with my friends.\nStatement 2: After 219 hours, I will have dinner with my friends.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q923b62fc46b",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from March 1984 to November 1986.\nStatement 2: The pandemic lasted for 32 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q2950ac124de",
  "kind": "choice",
  "text": "Statement 1: Before Dec 1924, a tsunami hit the coast.\nStatement 2: After February 1909, a tsunami hit the coast.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qb17065ff475",
  "kind": "choice",
  "text": "Claim: The EU, USA and other western donors should not fund any Palestinian government in which terrorist organisations participate\nPerspective: The loss of funding would destabilise and radicalise Palestine. ",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "qe7d131b7dfc",
  "kind": "choice",
  "text": "Proposition A: ~((~(~(~((g|y))))>(v>~(f))))\nProposition B: (~(((((z>y)>v)|l)>(t>(g|z))))|(y|t))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "qc148ef33064",
  "kind": "choice",
  "text": "Statement 1: Before April, I started my office leave.\nStatement 2: After July, I started my office leave.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qbd43937a37c",
  "kind": "choice",
  "text": "Proposition A: ~(~(((c&v)&a)))\nProposition B: ((a|u)&((v|a)|~(((l|v)|(v>g)))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q382adffbb1f",
  "kind": "choice",
  "text": "Proposition A: ((((u|t)&(v|n))&((i&(i>a))&x))|(v&t))\nProposition B: (v|(y>n))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q31e2e8ed5f1",
  "kind": "choice",
  "text": "Proposition A: ~((c>t))\nProposition B: ((((c>r)|h)>c)>i)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "qfd13189a61d",
  "kind": "choice",
  "text": "Proposition A: ((u&h)&(((j&j)&((m&(v&h))|m))&(j>z)))\nProposition B: ((g>j)&(((m|~((i|g)))&h)|~(h)))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qf55d2739286",
  "kind": "choice",
  "text": "Proposition A: (o&(c&((o>(c|m))&(c&c))))\nProposition B: ((o&f)>(m|y))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q8d9f1e07a75",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict will end on 11th February 1927.\nStatement 2: The prison sentence of that convict will end before 1st March 2000.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qd30f9fbee3e",
  "kind": "choice",
  "text": "Statement 1: After 7 months, Lily will fly to New York.\nStatement 2: Lily will fly to New York after 230 days.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qf4da5f168d8",
  "kind": "choice",
  "text": "Statement 1: The country was under a dictatorship from 1978 to 1999.\nStatement 2: The country was under a dictatorship for less than 210 years.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qe43ef5970ae",
  "kind": "choice",
  "text": "Proposition A: ~(~(~((((m>i)>(m&q))>((v&l)>~(q))))))\nProposition B: ((n|q)>(~(m)>h))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q7fb39804d80",
  "kind": "choice",
  "text": "Statement 1: In Nov 1984, the country became a dictatorship.\nStatement 2: After Apr 1904, the country became a dictatorship.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qd46b6570ba7",
  "kind": "choice",
  "text": "Proposition A: ~(((r>f)|(k|f)))\nProposition B: ((~(r)>m)|r)",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qa33bfd700d1",
  "kind": "choice",
  "text": "Claim: Guinea-Bissau should not let itself be turned in to a front of the US’ \"war on drugs\"\nPerspective: Sacrifice of sovereignty ",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q6af08d43e90",
  "kind": "choice",
  "text": "Proposition A: (i&r)\nProposition B: (~(r)|b)",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q3e7eea5bbce",
  "kind": "choice",
  "text": "Claim: It is a good idea to lease Crimea to Russia\nPerspective: Does not provide guarantees for the protection of other Russian minorities",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q906a15f8a30",
  "kind": "choice",
  "text": "Statement 1: My grandfather was born in 1983 and died in 1993.\nStatement 2: My grandfather lived for less than 100 years.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q39532928185",
  "kind": "choice",
  "text": "Statement 1: My grandfather was born in May 1972 and died in May 1998.\nStatement 2: My grandfather lived for 26 years.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q4fc8b84720f",
  "kind": "choice",
  "text": "Statement 1: The country became a dictatorship after Monday.\nStatement 2: The country became a dictatorship before Wednesday.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qcaf65d8b7b8",
  "kind": "choice",
  "text": "Statement 1: The conference lasted from Thursday to Monday.\nStatement 2: The conference lasted for 5 days.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q158dc520dba",
  "kind": "choice",
  "text": "Proposition A: ~((~(b)>(m|g)))\nProposition B: (((b|n)&m)&(((((b|b)|g)|m)|n)>(b&m)))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q9a02827974b",
  "kind": "choice",
  "text": "Statement 1: My grandfather lived from September 1924 to June 1940.\nStatement 2: My grandfather lived for 15 years 9 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q4ab40a412da",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out after 6 years.\nStatement 2: After 20 months, the government budget will come out.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qe86292e98b6",
  "kind": "choice",
  "text": "Claim: The world must arm the Syrian rebels\nPerspective: The Free Syrian Army is outgunned",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qfaac87aa049",
  "kind": "choice",
  "text": "Statement 1: The country was under a dictatorship from February 1982 to January 1993.\nStatement 2: The country was under a dictatorship for 1310 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qb2ec164478c",
  "kind": "choice",
  "text": "Claim: Social Media should be part of the curriculum\nPerspective: Social media creates a positive atmosphere in the classroom.",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "qee4f27298a8",
  "kind": "choice",
  "text": "Statement 1: My doctor's appointment took place from 7 PM to 4 PM.\nStatement 2: My doctor's appointment took place for 21 hours.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q9dac478ea0d",
  "kind": "choice",
  "text": "Statement 1: I will start my office leave after 7 months.\nStatement 2: Before 360 days, I will start my office leave.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q3315c57e49a",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from Oct 1981 to June 1984.\nStatement 2: The pandemic lasted for 320 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qda2e1ffedef",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will begin in 6 days.\nStatement 2: After 133 hours, her internship at Google will begin.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q2af03c7a7d8",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict started in Jul and ended in Apr.\nStatement 2: The prison sentence of that convict lasted for less than 9 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qbf791cf9ea6",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out after 6 months.\nStatement 2: The government budget will come out after 315 days.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q208d7f516dc",
  "kind": "choice",
  "text": "Proposition A: ~(~(~((((d&i)>q)|(j&i)))))\nProposition B: (x>~((i&j)))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q976e361b869",
  "kind": "choice",
  "text": "Statement 1: In Sep, the country declared martial law.\nStatement 2: Before June, the country declared martial law.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 }
]
