# A61 DI-TS label-noise blind read DTSB-blind_read-046

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/reads/answers/DTSB-blind_read-046.json

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
  "qid": "q9cdb3031eb3",
  "kind": "choice",
  "text": "Claim: It is selfish to have more than two children\nPerspective: Personal responsibility would improve in general ",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "qe130b9c80c1",
  "kind": "choice",
  "text": "Statement 1: In 3 months, her internship at Google will begin.\nStatement 2: Her internship at Google will begin before 98 days.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q077e46cc825",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict will end after 3 months.\nStatement 2: The prison sentence of that convict will end before 61 days.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q7152304115f",
  "kind": "choice",
  "text": "Claim: EU member states should guarantee people under 25 a temporary workplace when they have been unemployed for six months\nPerspective: This policy would only serve to discriminate against unemployed people older than 25",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "qcf584330313",
  "kind": "choice",
  "text": "Statement 1: Mary's party started after 08:00.\nStatement 2: Mary's party started after 19:00.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q9fd3171c640",
  "kind": "choice",
  "text": "Statement 1: On 21st August 1960, Michael bought the house.\nStatement 2: After 26th Jul 1943, Michael bought the house.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q9c6fb1c8a4a",
  "kind": "choice",
  "text": "Statement 1: In 4 years, they will get married.\nStatement 2: They will get married after 50 months.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q0f1fa986890",
  "kind": "choice",
  "text": "Proposition A: ((w|(((o>f)|w)&i))&((m&o)&(m&p)))\nProposition B: ~(~((o>~(((p&i)&(v>(w&(u|w))))))))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q4341c242084",
  "kind": "choice",
  "text": "Statement 1: The failing company started issuing major layoffs on Saturday which ended on Sunday.\nStatement 2: The failing company issued major layoffs for 1 day.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q0aeec061e01",
  "kind": "choice",
  "text": "Statement 1: After October 1986, this article was published.\nStatement 2: After December 1992, this article was published.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "qc4bdb0c82e4",
  "kind": "choice",
  "text": "Claim: Spain should cede Ceuta and Melilla to Morocco\nPerspective: The citizens do not want to be ceded",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q5c0c5ec7d8a",
  "kind": "choice",
  "text": "Claim: There should be no permanent members of the UN Security Council\nPerspective: It would make the UNSC more effective and efficient",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "qa7b68e12e95",
  "kind": "choice",
  "text": "Statement 1: In May, Kendrick's album is set to drop.\nStatement 2: Before Feb, Kendrick's album is set to drop.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q9da148bad6d",
  "kind": "choice",
  "text": "Claim: 1-child policy for every single country in the world!\nPerspective: Personal responsibility would improve in general ",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q3715ad5dab4",
  "kind": "choice",
  "text": "Statement 1: I will leave on a long vacation after 4 months.\nStatement 2: Before 151 days, I will leave on a long vacation.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q255fedf5225",
  "kind": "choice",
  "text": "Claim: There should be a legally mandated ceiling on weekly working hours\nPerspective: The market already limits worker hours when left to its own devices, no intrusion is required.",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q2e54542f416",
  "kind": "choice",
  "text": "Statement 1: The spring quarter begins in May and ends in June.\nStatement 2: The spring quarter lasts for 10 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q347ef9130f9",
  "kind": "choice",
  "text": "Proposition A: ((g&(g&(e&w)))&((a|(w|e))&(n|~(w))))\nProposition B: ((w|~((~((i|w))>w)))>e)",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q4e8d918536e",
  "kind": "choice",
  "text": "Proposition A: ~(((q|k)&(k>k)))\nProposition B: (n>q)",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "qcb27204e039",
  "kind": "choice",
  "text": "Claim: The integration of Africa through the African Union can succeed\nPerspective: The role of leaders will prevent success",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "qe81ef37b076",
  "kind": "choice",
  "text": "Statement 1: In 8 days, the tiger will be spotted.\nStatement 2: After 100 hours, the tiger will be spotted.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q4c82b56e0bf",
  "kind": "choice",
  "text": "Statement 1: My grandfather lived from May 1935 to September 1988.\nStatement 2: My grandfather lived for 640 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q110bf3d5df8",
  "kind": "choice",
  "text": "Statement 1: Before Tuesday, my doctor's appointment was scheduled to take place.\nStatement 2: After Sunday, my doctor's appointment was scheduled to take place.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qd9d450cd6a1",
  "kind": "choice",
  "text": "Claim: Most people are a little bit gay\nPerspective: Gay people are going to hell.",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "qe8f592fede7",
  "kind": "choice",
  "text": "Proposition A: ((g|~((g&(y|n))))>~(~((n&s))))\nProposition B: ((s>n)|(~(~((g|y)))|(~(v)&(n|s))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q145b457c811",
  "kind": "choice",
  "text": "Statement 1: The weather here is pleasant from Aug to June.\nStatement 2: The weather here is pleasant for less than 10 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q68679da4633",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict started in May and ended in June.\nStatement 2: The prison sentence of that convict lasted for less than 10 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q2da2cc8e6d4",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from Sep 1946 to February 1976.\nStatement 2: The pandemic lasted for less than 29 years 5 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q20b2846d1fc",
  "kind": "choice",
  "text": "Statement 1: We will go to Disneyland after 4 years.\nStatement 2: Before 59 months, we will go to Disneyland.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q99b6e6d7ddc",
  "kind": "choice",
  "text": "Proposition A: (((x>o)|j)&o)\nProposition B: ((j>j)>((j|x)|(o>x)))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "qe1a4076a904",
  "kind": "choice",
  "text": "Claim: The UK would be better off economically outside the European Union\nPerspective: There will be £350 million more to spend a week",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "qfaabb63b7bb",
  "kind": "choice",
  "text": "Statement 1: In 6 months, the country will become a dictatorship.\nStatement 2: The country will become a dictatorship before 294 days.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q6a855ff39f2",
  "kind": "choice",
  "text": "Claim: Liberal democracies are better at providing people’s needs than non-democracies.\nPerspective: A dictatorship breeds order and it's a needed step for both development and liberal democracy",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q1fdd6e4a8a9",
  "kind": "choice",
  "text": "Claim: Disclose previous convictions in court\nPerspective: The disclosure of previous convictions could falsely characterize the defendant.  ",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "qffdb3fc3a00",
  "kind": "choice",
  "text": "Claim: We have to cut the length of copyright protection\nPerspective: Long copyright stifles creative responses to and re-workings of the original work",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "qe9790520573",
  "kind": "choice",
  "text": "Proposition A: (z|~(x))\nProposition B: ~(~(((a&d)>((z>((z>c)>z))>(x>(p|z))))))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qa7897494bef",
  "kind": "choice",
  "text": "Statement 1: The football game will be telecasted from 07:00 to 2 PM.\nStatement 2: The football game will be telecasted for 8 hours.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q22443d89a7a",
  "kind": "choice",
  "text": "Statement 1: A tsunami will hit the coast after 3 months.\nStatement 2: Before 12 days, a tsunami will hit the coast.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "qe8f3a2b2dbd",
  "kind": "choice",
  "text": "Statement 1: The war began in February 1935 and lasted until February 1998.\nStatement 2: The war lasted for less than 630 years.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q486947f11a4",
  "kind": "choice",
  "text": "Statement 1: We will ride our bikes in 5 days.\nStatement 2: Before 88 hours, we will ride our bikes.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qc462e37d575",
  "kind": "choice",
  "text": "Claim: Sao Tome would drop relations with Taiwan in favour of Mainland China\nPerspective: Economically beneficial",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "qf222eabbba5",
  "kind": "choice",
  "text": "Claim: Israel's 2008-2009 military operations against Gaza were justified\nPerspective: The military operations were proportionate to the threat: ",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q51e66f12f86",
  "kind": "choice",
  "text": "Statement 1: Before 8 months, we will go to Disneyland.\nStatement 2: We will go to Disneyland before 192 days.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q6cc4f990d89",
  "kind": "choice",
  "text": "Claim: Positive discrimination has to be used to increase diversity in university\nPerspective: Equality of opportunity",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "qff6363dc400",
  "kind": "choice",
  "text": "Statement 1: In 4 days, the price of this stock will peak.\nStatement 2: The price of this stock will peak before 103 hours.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q80884bc1266",
  "kind": "choice",
  "text": "Claim: Britain should join the Euro currency\nPerspective: Britain will lose economically if she stays out of the Euro over the long term.",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q572a49bc991",
  "kind": "choice",
  "text": "Statement 1: The park opens on Saturday and closes on Tuesday.\nStatement 2: The park is open for 3 days.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q7c41c835c59",
  "kind": "choice",
  "text": "Claim: The development of genetically modified organisms have to be banned\nPerspective: Genetically modified organisms can solve the problem of food supply in the developing world. ",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q7fd68148a0e",
  "kind": "choice",
  "text": "Proposition A: ~(((y&y)|(y&~(((y>y)>(y>y))))))\nProposition B: ((y>(y|y))&~(y))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "qe06dd2460d3",
  "kind": "choice",
  "text": "Statement 1: The country declared martial law in Jun.\nStatement 2: The country declared martial law after March.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q94abd6b0620",
  "kind": "choice",
  "text": "Proposition A: (~((~(y)|((q|q)>x)))&((y>t)>x))\nProposition B: (~(((p|p)&(~((p&p))|l)))>~(y))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q4bbe9fff570",
  "kind": "choice",
  "text": "Statement 1: The football game will be telecasted from 8 AM to 10 PM.\nStatement 2: The football game will be telecasted for 140 hours.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q6a8eef5a47e",
  "kind": "choice",
  "text": "Proposition A: ~(~(u))\nProposition B: (((u>s)|((w|(c>~(s)))>(m>c)))&(w>w))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q41ca6b83938",
  "kind": "choice",
  "text": "Statement 1: The failing company issued major layoffs before 1970.\nStatement 2: The failing company issued major layoffs before 1960.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q0b22869852d",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from Mar 1938 to Sep 1982.\nStatement 2: The pandemic lasted for less than 44 years 6 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q83718b2e96c",
  "kind": "choice",
  "text": "Claim: Quebec should secede from Canada\nPerspective: This is not the will of the people of Quebec. ",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "q1873dfd9ca9",
  "kind": "choice",
  "text": "Statement 1: The President will give a speech before 9 days.\nStatement 2: After 136 hours, the President will give a speech.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q084db286481",
  "kind": "choice",
  "text": "Statement 1: The Presidential election is set to take place before 7 years.\nStatement 2: Before 100 months, the Presidential election is set to take place.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q478c76368df",
  "kind": "choice",
  "text": "Statement 1: In 2 months, the price of this stock will peak.\nStatement 2: After 173 days, the price of this stock will peak.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q47745f2d084",
  "kind": "choice",
  "text": "Statement 1: We attended outdoor concerts from December 1952 to April 1972.\nStatement 2: We attended outdoor concerts for less than 233 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q76a10b98564",
  "kind": "choice",
  "text": "Statement 1: The country will become a dictatorship in 7 months.\nStatement 2: After 324 days, the country will become a dictatorship.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q7ef2276501f",
  "kind": "choice",
  "text": "Statement 1: A tsunami will hit the coast before 1 month.\nStatement 2: Before 110 days, a tsunami will hit the coast.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qc1144f1b845",
  "kind": "choice",
  "text": "Statement 1: We will go to Disneyland before 8 years.\nStatement 2: Before 150 months, we will go to Disneyland.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qdc7d8729b54",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict lasted from June 1930 to March 1967.\nStatement 2: The prison sentence of that convict lasted for 36 years 10 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qe25a1061ad5",
  "kind": "choice",
  "text": "Proposition A: (d&z)\nProposition B: (((f|m)|~(~(m)))|~(~(f)))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "qbbb1434c6a7",
  "kind": "choice",
  "text": "Statement 1: After 6 days, the government budget will come out.\nStatement 2: The government budget will come out before 250 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q7b362585b08",
  "kind": "choice",
  "text": "Statement 1: Lily will fly to New York before 11th Jun 1947.\nStatement 2: Lily will fly to New York before 3rd Jan 1918.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q247e7b762b0",
  "kind": "choice",
  "text": "Statement 1: The meeting will begin before 17:00.\nStatement 2: The meeting will begin before 9 AM.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q4b262597c9e",
  "kind": "choice",
  "text": "Claim: The payment of welfare benefits to parents should be tied to their children's school attendance records\nPerspective: Connecting welfare to failure of parents is unfair.",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q08db9f0e7b8",
  "kind": "choice",
  "text": "Proposition A: ~(((x>(u>e))&((z>d)|(q&g))))\nProposition B: (y|((g>u)>x))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "qd4937cbc6d6",
  "kind": "choice",
  "text": "Proposition A: ~(((x|((j|b)|v))&((((n&s)>n)&~(w))>n)))\nProposition B: ((e&v)>~(f))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q3723cc05a34",
  "kind": "choice",
  "text": "Claim: Terrorists should be subject to the Geneva Conventions\nPerspective: There are other means by which to protect the rights of terrorists without needing to apply the Geneva Conventions.",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q034a5821fee",
  "kind": "choice",
  "text": "Proposition A: ((p|(j|m))>(g&(m>e)))\nProposition B: ((c>m)|((p|j)|e))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q423e73ee747",
  "kind": "choice",
  "text": "Proposition A: ((d&(z|s))&l)\nProposition B: (((u|u)&((h|~(l))>h))>s)",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qeb3cae58607",
  "kind": "choice",
  "text": "Claim: Russia needs strong leadership\nPerspective: Corruption, an essential issue in Russia,  is due to the strong leadership",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q61890f73204",
  "kind": "choice",
  "text": "Statement 1: At 19:00, a tsunami will hit the coast.\nStatement 2: Before 14:00, a tsunami will hit the coast.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q41a54ad4289",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album is set to drop before 10 months.\nStatement 2: Before 445 days, Kendrick's album is set to drop.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q2e5b5872131",
  "kind": "choice",
  "text": "Claim: Cyberbullies must be punished with prison even if under 18\nPerspective: Should not damage a normal childhood with jail",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q28155b448a7",
  "kind": "choice",
  "text": "Proposition A: ((v|(((f&~(o))&v)>b))>(v&v))\nProposition B: (~(b)>f)",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q4c84a9163a3",
  "kind": "choice",
  "text": "Proposition A: (~((p&(m>~(m))))&~(((m>h)|(~(x)>p))))\nProposition B: (((~(~(x))>~(~(~((m&(p&c))))))&h)>x)",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "qa435f79428f",
  "kind": "choice",
  "text": "Proposition A: (l>~((w>(l|t))))\nProposition B: (v|f)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q5b32c8bb391",
  "kind": "choice",
  "text": "Statement 1: After 6 years, her internship at Google will begin.\nStatement 2: Her internship at Google will begin before 22 months.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q899705b1f1d",
  "kind": "choice",
  "text": "Statement 1: Final grades are due after 1 day.\nStatement 2: Final grades are due after 23 hours.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q230783e7e13",
  "kind": "choice",
  "text": "Statement 1: Before 4 months, Apple will release the new iPhone.\nStatement 2: Before 107 days, Apple will release the new iPhone.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q5acec328f34",
  "kind": "choice",
  "text": "Statement 1: This team will win the world cup before May.\nStatement 2: This team will win the world cup before September.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qc300589b27c",
  "kind": "choice",
  "text": "Statement 1: Basketball season lasts from May to January.\nStatement 2: Basketball season lasts for less than 9 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q4ecd21528c7",
  "kind": "choice",
  "text": "Statement 1: The football game will be telecasted from 05:00 to 4 AM.\nStatement 2: The football game will be telecasted for 24 hours.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q4111b804bfe",
  "kind": "choice",
  "text": "Claim: Personality is more important than ability\nPerspective: Ability can change, personality can't.",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q03ac558f9e1",
  "kind": "choice",
  "text": "Statement 1: The Presidential election is set to take place before 10 years.\nStatement 2: The Presidential election is set to take place after 161 months.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q6c9cd9fb3c8",
  "kind": "choice",
  "text": "Statement 1: Michael will buy the house before 5 years.\nStatement 2: Michael will buy the house before 103 months.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q59751296f3e",
  "kind": "choice",
  "text": "Proposition A: ~(i)\nProposition B: ((s>f)|((k&(r>h))&(c|~((s|i)))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q4fdd1e4eaf1",
  "kind": "choice",
  "text": "Statement 1: In 1 year, the Presidential election is set to take place.\nStatement 2: Before 44 months, the Presidential election is set to take place.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q1a3f09cb5a9",
  "kind": "choice",
  "text": "Proposition A: ((w&u)&((x&u)&((x&x)&w)))\nProposition B: ~(w)",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "qfcc8ef2477b",
  "kind": "choice",
  "text": "Proposition A: ((d&x)|~((~(t)>((t&d)>d))))\nProposition B: (((a>x)>((t>d)&x))|t)",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q68fcdd74061",
  "kind": "choice",
  "text": "Proposition A: (~((~(c)&(~((w>w))>c)))|((x&d)|(w&d)))\nProposition B: (w|~((~(x)|~((x&(c>x))))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q4f77d39a93c",
  "kind": "choice",
  "text": "Proposition A: (~((a|(q|q)))&e)\nProposition B: (b|((b>b)&w))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qdb331acdc7d",
  "kind": "choice",
  "text": "Statement 1: Before May 1990, the tiger was last spotted.\nStatement 2: Before Oct 1919, the tiger was last spotted.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q5e632812ec0",
  "kind": "choice",
  "text": "Proposition A: ~(e)\nProposition B: ((x|e)>(((e>(x&e))>e)>((e>e)>x)))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q1f5faaafc3f",
  "kind": "choice",
  "text": "Proposition A: ~((((r|v)>r)|(s|(n|r))))\nProposition B: ((r>((s|v)&(r>v)))&~(~(~(s))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 }
]
