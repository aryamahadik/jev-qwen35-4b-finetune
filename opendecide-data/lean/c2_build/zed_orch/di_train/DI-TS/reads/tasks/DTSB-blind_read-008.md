# A61 DI-TS label-noise blind read DTSB-blind_read-008

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/reads/answers/DTSB-blind_read-008.json

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
  "qid": "q8da0104aad5",
  "kind": "choice",
  "text": "Proposition A: (a&~(~(((m&(o|s))>~(a)))))\nProposition B: (k|a)",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q81132d47808",
  "kind": "choice",
  "text": "Statement 1: Before 25th, Lily flew to New York.\nStatement 2: After 19th, Lily flew to New York.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qda19ac6d46d",
  "kind": "choice",
  "text": "Claim: Parents of obese children be prosecuted with neglect\nPerspective: Ignoring the countless warnings about the dangers surrounding obesity is neglect and neglecting a child is a prosecutable offence",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q89d49d9f2cb",
  "kind": "choice",
  "text": "Statement 1: The meeting began at 23:00 and got over at 22:00.\nStatement 2: The meeting lasted for 230 hours.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q3accdf20e3e",
  "kind": "choice",
  "text": "Proposition A: (j&~(~((~(~((d>e)))>d))))\nProposition B: (((j>n)&(~(b)|e))>(x>((u&e)|(d>n))))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qa99808f1a2b",
  "kind": "choice",
  "text": "Statement 1: The pandemic began in Apr 1941 and lasted until Jan 1967.\nStatement 2: The pandemic lasted for less than 257 years 6 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qcc5d8d554b6",
  "kind": "choice",
  "text": "Statement 1: We started attending outdoor concerts in June and stopped in Jul.\nStatement 2: We attended outdoor concerts for 2 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qe8395d465ca",
  "kind": "choice",
  "text": "Statement 1: The city will have a huge power outage in 1 day.\nStatement 2: After 51 hours, the city will have a huge power outage.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q3c9b0fd06f8",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict lasted from January 1910 to January 1930.\nStatement 2: The prison sentence of that convict lasted for less than 240 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q6ceac7d92f0",
  "kind": "choice",
  "text": "Statement 1: Before 9 days, her internship at Google will begin.\nStatement 2: After 231 hours, her internship at Google will begin.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qc1317dfc404",
  "kind": "choice",
  "text": "Claim: We have lost the true meaning of Christmas\nPerspective: Jesus is Becoming Irrelevant to Christmas",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q26e000fc511",
  "kind": "choice",
  "text": "Proposition A: ~(((~(x)|((x&(x|e))|((x>e)&e)))&e))\nProposition B: (((~((e&e))|e)|~(~(e)))&x)",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q2317b0eb68b",
  "kind": "choice",
  "text": "Claim: Internet access is a human right\nPerspective: These people are breaking the law and need to be punished.",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q2eac86d6f54",
  "kind": "choice",
  "text": "Claim: Social Security should be privatized \nPerspective: Private accounts would allow benefits to be inherited. ",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "qb65bbdea988",
  "kind": "choice",
  "text": "Proposition A: ((w&(m|(m|m)))&x)\nProposition B: ~(((m|a)&(m&x)))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q8ccee4fa978",
  "kind": "choice",
  "text": "Proposition A: (y&(i&y))\nProposition B: ~((~((i&i))>i))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q82192955675",
  "kind": "choice",
  "text": "Statement 1: The servers will back up after 5 AM.\nStatement 2: The servers will back up after 01:00.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qb0a0a51ea9d",
  "kind": "choice",
  "text": "Statement 1: After 10 days, the park will open.\nStatement 2: The park will open after 341 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q3618e04e881",
  "kind": "choice",
  "text": "Proposition A: ((((u&j)&(i|u))|e)|~(~((l&e))))\nProposition B: ((~(a)&(j|l))>(e>l))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q0d811a4fdda",
  "kind": "choice",
  "text": "Statement 1: In Feb, the tiger will be spotted.\nStatement 2: Before Aug, the tiger will be spotted.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qfc95d526ed6",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from October 1933 to June 1943.\nStatement 2: The pandemic lasted for 9 years 8 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qea2ce0ac4a1",
  "kind": "choice",
  "text": "Statement 1: After 24th Mar 1988, the prison sentence of that convict ended.\nStatement 2: Before 3rd Jan 1995, the prison sentence of that convict ended.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qc22113ce26e",
  "kind": "choice",
  "text": "Statement 1: Michael will buy the house after September.\nStatement 2: Michael will buy the house before September.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q798c8b86c8a",
  "kind": "choice",
  "text": "Statement 1: After 13:00, we rode our bikes.\nStatement 2: Before 5 AM, we rode our bikes.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q73548a89c9a",
  "kind": "choice",
  "text": "Proposition A: ((t>i)&((t>((v>v)&q))&d))\nProposition B: (~(v)>((b|d)|(~((d|v))&(b|t))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q6555a69112a",
  "kind": "choice",
  "text": "Statement 1: Before 1 month, Lily will fly to New York.\nStatement 2: Before 138 days, Lily will fly to New York.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q978ffe687a5",
  "kind": "choice",
  "text": "Statement 1: A huge power outage in the city started at 11:00 and ended at 06:00.\nStatement 2: The city had a huge power outage for less than 190 hours.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qd03f59fcc87",
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
  "qid": "q11e5ea0b2bc",
  "kind": "choice",
  "text": "Statement 1: He left his job after 16th Apr 1909.\nStatement 2: He left his job before 27th December 1993.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qc838ecc55a4",
  "kind": "choice",
  "text": "Proposition A: ((l&f)&(j&~((f>(q|((n|j)>t))))))\nProposition B: ((y&(n>m))>~(((q>(q|f))&n)))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q53d9f66512d",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict started in 1909 and ended in 1960.\nStatement 2: The prison sentence of that convict lasted for less than 51 years.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q6c872ebba28",
  "kind": "choice",
  "text": "Statement 1: After 7 years, we will go to Disneyland.\nStatement 2: We will go to Disneyland before 54 months.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q6a5b831410a",
  "kind": "choice",
  "text": "Statement 1: After 7 months, the prison sentence of that convict will end.\nStatement 2: Before 124 days, the prison sentence of that convict will end.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q09638396934",
  "kind": "choice",
  "text": "Statement 1: Michael reached my house at 08:00 and left at 10:00.\nStatement 2: Michael visited my house for 20 hours.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q0140c043c8f",
  "kind": "choice",
  "text": "Statement 1: Before 1 year, the government budget will come out.\nStatement 2: The government budget will come out after 19 months.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q1d35af5d201",
  "kind": "choice",
  "text": "Statement 1: Final grades are due after 8 days.\nStatement 2: Final grades are due after 198 hours.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q02b4d6b6c4d",
  "kind": "choice",
  "text": "Claim: We should detain terror suspects without trial\nPerspective: Internment without trial exacerbates the antagonism of enemies and subsequent risk to civilians.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "qb310c59a978",
  "kind": "choice",
  "text": "Claim: Russia is a land of democracy (not autocracy)\nPerspective: Corruption, an essential issue in Russia,  is due to the strong leadership",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q6c48a26d7d6",
  "kind": "choice",
  "text": "Statement 1: The park will open in 1 day.\nStatement 2: Before 4 hours, the park will open.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qe360ef27328",
  "kind": "choice",
  "text": "Claim: The world has to ignore North Korean provocations\nPerspective: North Korea is an unresolved conflict it can’t simply be ignored",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q0af3c08ef64",
  "kind": "choice",
  "text": "Statement 1: After Jun, the Presidential election took place.\nStatement 2: Before Dec, the Presidential election took place.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "qcc71ddf0dfb",
  "kind": "choice",
  "text": "Statement 1: Before June, the prison sentence of that convict will end.\nStatement 2: Before August, the prison sentence of that convict will end.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q4fd704b8ccb",
  "kind": "choice",
  "text": "Statement 1: My grandfather lived from Dec 1920 to Oct 1980.\nStatement 2: My grandfather lived for less than 719 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qc4b7a806b0d",
  "kind": "choice",
  "text": "Claim: We should be investing in public transport\nPerspective: it is the environmentally friendly thing to do",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "qcc1b5efeb79",
  "kind": "choice",
  "text": "Claim: Junk Food Should Be Banned\nPerspective: A healthy diet starts from home and starts early. ",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q016fd81a9a1",
  "kind": "choice",
  "text": "Statement 1: The war began in 1955 and lasted until 1978.\nStatement 2: The war lasted for 23 years.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q20d30d9d1cc",
  "kind": "choice",
  "text": "Proposition A: (((b>d)|g)&d)\nProposition B: (r&(~(~(d))>((d|d)>(~((b|p))>~(p)))))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qc85611f9c62",
  "kind": "choice",
  "text": "Statement 1: I worked on my MS application from March to October.\nStatement 2: I worked on my MS application for less than 7 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q8374f8983f2",
  "kind": "choice",
  "text": "Statement 1: I will leave on a long vacation in February.\nStatement 2: I will leave on a long vacation before March.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q16dd733efd0",
  "kind": "choice",
  "text": "Statement 1: I will start my office leave on Thursday and be back on Friday.\nStatement 2: I will be on my office leave for less than 2 days.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qb5572a05503",
  "kind": "choice",
  "text": "Statement 1: The pleasant weather here starts in September and ends in Apr.\nStatement 2: The weather here is pleasant for 70 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qa682a1f3a6b",
  "kind": "choice",
  "text": "Statement 1: After Oct 1989, they will get married.\nStatement 2: Before May 1979, they will get married.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q6fb94fdd6a6",
  "kind": "choice",
  "text": "Proposition A: ((q|w)&(q&(~(r)&i)))\nProposition B: ((w&~(v))>r)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qaf49fda147b",
  "kind": "choice",
  "text": "Statement 1: I worked on my MS application from 5th to 28th.\nStatement 2: I worked on my MS application for 23 days.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qb8b96ef7845",
  "kind": "choice",
  "text": "Claim: It is important to use a graduated response to combat unauthorised file-sharing of copyrighted material\nPerspective: The graduated response is a violation of the basic right to due process",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q4bd3edda708",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will start in Oct and end in Jan.\nStatement 2: Her internship at Google will last for less than 4 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q43c9a071cd4",
  "kind": "choice",
  "text": "Proposition A: (b&a)\nProposition B: (g>(a&g))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qd002401c39f",
  "kind": "choice",
  "text": "Claim: Intellectual property rights have to be abolished\nPerspective: Firms and individuals misallocate resources trying to race others to the same goal, and spend resources stealing from one another:",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q416d33b0f0a",
  "kind": "choice",
  "text": "Statement 1: The failing company issued major layoffs after 10th.\nStatement 2: The failing company issued major layoffs after 19th.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q333eb44b21c",
  "kind": "choice",
  "text": "Claim: Climate Change is the end of the world\nPerspective: The significant bulk of scientific research says it is happening",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "q87484aa35f5",
  "kind": "choice",
  "text": "Statement 1: After July, the Presidential election took place.\nStatement 2: After Feb, the Presidential election took place.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qffbefbf9271",
  "kind": "choice",
  "text": "Statement 1: The conference will be held in 3 years.\nStatement 2: The conference will be held before 83 months.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q5b7e53e17c7",
  "kind": "choice",
  "text": "Statement 1: The country was under a dictatorship from Mar 1921 to Sep 1985.\nStatement 2: The country was under a dictatorship for less than 7740 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qbfd510a1ce3",
  "kind": "choice",
  "text": "Proposition A: ((~(s)&y)&~((h&~(((y|a)&(v|v))))))\nProposition B: (y|~(((x|x)&s)))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q0999377c6a5",
  "kind": "choice",
  "text": "Statement 1: Basketball season will end in 9 months.\nStatement 2: Basketball season will end after 356 days.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q2cd9329f5af",
  "kind": "choice",
  "text": "Statement 1: Before 1944, the failing company issued major layoffs.\nStatement 2: Before 1964, the failing company issued major layoffs.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q033b8c9b53b",
  "kind": "choice",
  "text": "Statement 1: In 10 years, Michael will buy the house.\nStatement 2: After 166 months, Michael will buy the house.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qf8d326a36f0",
  "kind": "choice",
  "text": "Statement 1: After 10 years, Kendrick's album is set to drop.\nStatement 2: Kendrick's album is set to drop before 94 months.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qbc3f6e4a7c8",
  "kind": "choice",
  "text": "Proposition A: ((~((p&k))|~(p))>(k|y))\nProposition B: (((~(p)|z)>(~((y>k))>k))>((y|k)|z))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q507f762079b",
  "kind": "choice",
  "text": "Statement 1: The weather here is pleasant from May to September.\nStatement 2: The weather here is pleasant for less than 5 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q3bcab9158e2",
  "kind": "choice",
  "text": "Statement 1: This article was published in 1906.\nStatement 2: This article was published after 1925.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "qf06caccdabf",
  "kind": "choice",
  "text": "Statement 1: Basketball season starts in August and ends in January.\nStatement 2: Basketball season lasts for less than 6 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q83086f06f8b",
  "kind": "choice",
  "text": "Statement 1: After 9 AM, the government budget will come out.\nStatement 2: After 03:00, the government budget will come out.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q234872d8751",
  "kind": "choice",
  "text": "Statement 1: After 10 years, we will go to Disneyland.\nStatement 2: We will go to Disneyland after 102 months.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qff9cd4071d1",
  "kind": "choice",
  "text": "Statement 1: The President will give a speech after 3 days.\nStatement 2: The President will give a speech after 38 hours.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q1458102d5bf",
  "kind": "choice",
  "text": "Statement 1: The servers will back up from 1 AM to 10 PM.\nStatement 2: The servers will back up for 22 hours.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qf4b48db1764",
  "kind": "choice",
  "text": "Statement 1: We will go to Disneyland in 5 years.\nStatement 2: Before 39 months, we will go to Disneyland.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qf980edaec68",
  "kind": "choice",
  "text": "Proposition A: ((~(~((n&((o>s)|o))))&v)&s)\nProposition B: (~(n)&~(((o>(s>n))>v)))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "qf449febd8aa",
  "kind": "choice",
  "text": "Statement 1: The country became a dictatorship in Feb 1903 which ended in January 1927.\nStatement 2: The country was under a dictatorship for 239 years 2 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qff65d54da4a",
  "kind": "choice",
  "text": "Claim: Using Rewards to Motivate Students\nPerspective: Rewards are relatively ineffective for motivating students",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "qcd9f116a460",
  "kind": "choice",
  "text": "Proposition A: ((g&(u|g))&~(~(p)))\nProposition B: ~(~(p))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "qe834f28a103",
  "kind": "choice",
  "text": "Statement 1: On 16th, the government budget came out.\nStatement 2: After 14th, the government budget came out.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qb4f147c364b",
  "kind": "choice",
  "text": "Statement 1: Before 12 AM, Michael will reach my house.\nStatement 2: Before 08:00, Michael will reach my house.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qc188d334729",
  "kind": "choice",
  "text": "Statement 1: The country became a dictatorship in April 1946 which ended in March 1956.\nStatement 2: The country was under a dictatorship for 99 years 2 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qb6f57a99246",
  "kind": "choice",
  "text": "Proposition A: (((u|l)&(b&o))|(i>b))\nProposition B: ~((~((((t>((g>t)&o))|b)|~(u)))&(i&g)))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q7248328cdc5",
  "kind": "choice",
  "text": "Claim: Religious freedom abroad should be one of the primary foreign policy concerns for any country\nPerspective: Concentrating on religious freedom is too narrow, instead human rights in general should be considered",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q1d2cc993d1f",
  "kind": "choice",
  "text": "Proposition A: ((c>t)&(((c|t)>a)&~((c&t))))\nProposition B: (y|(~((c&y))&(((c|~(d))&(c|d))&c)))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q396a9c28ae1",
  "kind": "choice",
  "text": "Statement 1: The country became a dictatorship in May 1924 which ended in May 1954.\nStatement 2: The country was under a dictatorship for less than 360 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q628afacb405",
  "kind": "choice",
  "text": "Statement 1: The country was under a dictatorship from Feb 1918 to Aug 1991.\nStatement 2: The country was under a dictatorship for less than 73 years 7 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qdf42e7433f1",
  "kind": "choice",
  "text": "Statement 1: After 8th May 1959, they will get married.\nStatement 2: Before 1st March 1940, they will get married.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qf7b9803c323",
  "kind": "choice",
  "text": "Proposition A: (h&h)\nProposition B: ((g|h)>(r>h))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q69b6cc8ac04",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from 1924 to 1926.\nStatement 2: The pandemic lasted for less than 3 years.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q4886cba83d8",
  "kind": "choice",
  "text": "Statement 1: My grandfather was born before March.\nStatement 2: My grandfather was born after February.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q1b34b9c0fd4",
  "kind": "choice",
  "text": "Statement 1: Lily will fly to New York after 9 months.\nStatement 2: Before 423 days, Lily will fly to New York.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q6079b9480e0",
  "kind": "choice",
  "text": "Statement 1: After Oct, the spring quarter began.\nStatement 2: After May, the spring quarter began.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qdb50d75e403",
  "kind": "choice",
  "text": "Statement 1: Lily flew to New York after Jul 1908.\nStatement 2: Lily flew to New York before July 1931.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q5edc6c7eef1",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from Apr 1924 to Jul 1930.\nStatement 2: The pandemic lasted for 76 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q717670b097a",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album is set to drop after 5 years.\nStatement 2: Kendrick's album is set to drop after 41 months.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q0d68cdcc1ba",
  "kind": "choice",
  "text": "Statement 1: My grandfather was born in Jul 1963 and died in April 1984.\nStatement 2: My grandfather lived for 2490 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 }
]
