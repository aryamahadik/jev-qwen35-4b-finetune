# A61 DI-TS label-noise blind read DTSB-blind_read-036

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/reads/answers/DTSB-blind_read-036.json

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
  "qid": "qa92393842b9",
  "kind": "choice",
  "text": "Proposition A: ((u|u)&y)\nProposition B: ~(((e>~((e&e)))>e))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q6530cb08a6c",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will last from Tuesday to Saturday.\nStatement 2: Her internship at Google will last for less than 40 days.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q3a6dbf7b812",
  "kind": "choice",
  "text": "Claim: Russia has the right to send troops into Crimea\nPerspective: Russia should negotiate with the new government",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "qe63c8bb5c75",
  "kind": "choice",
  "text": "Proposition A: (o&((a|a)|(a&(g&g))))\nProposition B: ~((~((((~((g>o))>a)|(a>g))&o))&g))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q8678b33d144",
  "kind": "choice",
  "text": "Statement 1: Before Aug, the government budget came out.\nStatement 2: After June, the government budget came out.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qa0acafe0729",
  "kind": "choice",
  "text": "Statement 1: Lily will fly to New York in Apr.\nStatement 2: Lily will fly to New York after Aug.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q3085816ed30",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict will end before 6 years.\nStatement 2: The prison sentence of that convict will end after 114 months.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q338a7072c6c",
  "kind": "choice",
  "text": "Statement 1: The music concert lasted from 1 AM to 1 PM.\nStatement 2: The music concert lasted for 120 hours.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q9d8bba049f5",
  "kind": "choice",
  "text": "Proposition A: ~((t>((t>n)>c)))\nProposition B: ~(~(~((~((u>j))|~(((f|m)|~(j)))))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qe78e3395c8e",
  "kind": "choice",
  "text": "Statement 1: A huge power outage in the city started on Thursday and ended on Sunday.\nStatement 2: The city had a huge power outage for less than 30 days.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q248adf1a306",
  "kind": "choice",
  "text": "Statement 1: The Presidential election took place after 1907.\nStatement 2: The Presidential election took place after 1938.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qcc9157f06c3",
  "kind": "choice",
  "text": "Statement 1: In 2 days, my doctor's appointment is scheduled to take place.\nStatement 2: My doctor's appointment is scheduled to take place before 157 hours.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q00f70cec350",
  "kind": "choice",
  "text": "Statement 1: After 5 years, they will get married.\nStatement 2: Before 95 months, they will get married.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qa5a2ceb5a68",
  "kind": "choice",
  "text": "Proposition A: ~((f|h))\nProposition B: ((((y>~(f))&h)&(j&y))|~(~((f>i))))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q48dc2115f16",
  "kind": "choice",
  "text": "Claim: The United States is justified in using private military firms abroad to pursue its military objectives\nPerspective: PMCs often do not even engage in combat",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q0ed78bcca24",
  "kind": "choice",
  "text": "Proposition A: (i&~((((i&c)|~(i))&v)))\nProposition B: ((~((r|r))|u)|c)",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q6b313f107fe",
  "kind": "choice",
  "text": "Statement 1: After 18th February 1953, a tsunami hit the coast.\nStatement 2: Before 28th September 1925, a tsunami hit the coast.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q8a7ccf9972f",
  "kind": "choice",
  "text": "Claim: The ‘war on terror’ is winnable\nPerspective: We should hope so, given all the hype around it.",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q7e295637929",
  "kind": "choice",
  "text": "Statement 1: The Presidential election is set to take place before 8 years.\nStatement 2: The Presidential election is set to take place after 63 months.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qfbce3ffa83d",
  "kind": "choice",
  "text": "Proposition A: ((x&j)&((~(p)|(~(h)>(v&h)))|~((z>m))))\nProposition B: (((h>m)>z)>((z|(p|j))|l))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q13dbc059316",
  "kind": "choice",
  "text": "Statement 1: The park is open from Monday to Thursday.\nStatement 2: The park is open for less than 30 days.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q73e04c807b0",
  "kind": "choice",
  "text": "Claim: A legal qualification is worth the cost\nPerspective: Failing a law degree can be extremely costly. ",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q2e6a83a887d",
  "kind": "choice",
  "text": "Proposition A: (~(~(((~(o)&(o|o))&h)))|(o|i))\nProposition B: ((((h&(i>h))&h)|(i>(i&h)))&h)",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q6bc6e19d6ea",
  "kind": "choice",
  "text": "Statement 1: The coding competition will start after 11th.\nStatement 2: The coding competition will start before 19th.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q1957ceb2727",
  "kind": "choice",
  "text": "Proposition A: ~(((l>((k&l)&l))>q))\nProposition B: (q>((((l>l)&~(k))|(q>l))&l))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qf88760ce452",
  "kind": "choice",
  "text": "Proposition A: (~(~(((i&i)&f)))&i)\nProposition B: ~(((l|((c|m)|(f&f)))>(~((f&f))&(f|q))))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qcfd162823c9",
  "kind": "choice",
  "text": "Statement 1: After 1 month, the spring quarter will begin.\nStatement 2: The spring quarter will begin after 100 days.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q26eb984c650",
  "kind": "choice",
  "text": "Statement 1: In 7 months, the price of this stock will peak.\nStatement 2: After 83 days, the price of this stock will peak.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q63f0003d7ac",
  "kind": "choice",
  "text": "Statement 1: The war lasted from October 1901 to Jun 1986.\nStatement 2: The war lasted for less than 10160 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q54d432d70b7",
  "kind": "choice",
  "text": "Statement 1: Before Dec, I will start my office leave.\nStatement 2: Before Jul, I will start my office leave.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q85c62d70d0f",
  "kind": "choice",
  "text": "Proposition A: (k&(~(~(~(a)))&r))\nProposition B: (((~(r)|r)&r)>((~(q)>p)|(y>(k|a))))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "qfd86802a9b6",
  "kind": "choice",
  "text": "Statement 1: Before 7 days, the landlord will collect rent.\nStatement 2: Before 189 hours, the landlord will collect rent.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qdbd9592bdba",
  "kind": "choice",
  "text": "Statement 1: They will get married after 8 years.\nStatement 2: After 127 months, they will get married.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q2c5bfb37647",
  "kind": "choice",
  "text": "Statement 1: The country was under a dictatorship from Oct 1913 to January 1950.\nStatement 2: The country was under a dictatorship for 36 years 4 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q99cac1134dc",
  "kind": "choice",
  "text": "Claim: The Guantanamo Bay detention centre should be closed\nPerspective: Gauntanamo Bay is detrimental to foreign relations for United States.",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q04b54445494",
  "kind": "choice",
  "text": "Statement 1: The servers' back up will start at 01:00 and end at 07:00.\nStatement 2: The servers will back up for 60 hours.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q6da35755c91",
  "kind": "choice",
  "text": "Proposition A: ((((n&h)|~(f))&(~((f&v))&n))&(h>v))\nProposition B: (~(~((h>v)))>v)",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q27d9d77633a",
  "kind": "choice",
  "text": "Statement 1: After 9 months, the country will become a dictatorship.\nStatement 2: After 353 days, the country will become a dictatorship.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q3fe850cb6dd",
  "kind": "choice",
  "text": "Statement 1: Before 9 months, Lily will fly to New York.\nStatement 2: Before 201 days, Lily will fly to New York.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qf6248c9f9de",
  "kind": "choice",
  "text": "Proposition A: ~(~((c&~((~(q)|m)))))\nProposition B: ((q>f)>(x|f))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q99da7eac1c4",
  "kind": "choice",
  "text": "Statement 1: Mary's party lasted from 20:00 to 17:00.\nStatement 2: Mary's party lasted for 21 hours.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qc914542aa27",
  "kind": "choice",
  "text": "Statement 1: The war began in 1957 and lasted until 1999.\nStatement 2: The war lasted for 420 years.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qe527fce09b1",
  "kind": "choice",
  "text": "Proposition A: (d&(((h|d)|~(m))|((~(z)>m)&m)))\nProposition B: ((m|(m&~(d)))|(h>z))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q1abc98d95f2",
  "kind": "choice",
  "text": "Proposition A: (~((((i|(i>(f|x)))&c)>f))&x)\nProposition B: ((m|i)|x)",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qbce2e359335",
  "kind": "choice",
  "text": "Statement 1: After 2 months, the government budget will come out.\nStatement 2: After 176 days, the government budget will come out.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q75164bc73e5",
  "kind": "choice",
  "text": "Statement 1: After 2 days, I will start working on my MS application.\nStatement 2: After 4 hours, I will start working on my MS application.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qa9de3373bc6",
  "kind": "choice",
  "text": "Statement 1: The city will have a huge power outage after 6 days.\nStatement 2: Before 158 hours, the city will have a huge power outage.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q6905bc5954c",
  "kind": "choice",
  "text": "Statement 1: Before March 1976, the war began.\nStatement 2: Before March 1950, the war began.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q86850c6db32",
  "kind": "choice",
  "text": "Proposition A: ~((~((l|(c>l)))&c))\nProposition B: ((l>l)>c)",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q31153fdd7d0",
  "kind": "choice",
  "text": "Proposition A: ((~(h)|((o|h)|(h|o)))&~(h))\nProposition B: (h>o)",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q5f799af698b",
  "kind": "choice",
  "text": "Proposition A: (c&((((e|~(o))|t)&o)&((f&c)|e)))\nProposition B: (o>(~(i)|b))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q907033af80a",
  "kind": "choice",
  "text": "Statement 1: The country declared martial law before May 1910.\nStatement 2: The country declared martial law after July 1947.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q1e6fa7f6736",
  "kind": "choice",
  "text": "Proposition A: (~(((x&(s|u))|x))>(n&~(n)))\nProposition B: ((~(((n|s)&u))&(~(n)>n))|~((s&n)))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "qf89d3aca308",
  "kind": "choice",
  "text": "Statement 1: In October 1948, Michael bought the house.\nStatement 2: After May 1905, Michael bought the house.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q088617c0aeb",
  "kind": "choice",
  "text": "Claim: the teacher is always right, even when s/he is not.\nPerspective: Part of the process of growing up to realise that adults aren't always right.",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "qfb1a91c0cfc",
  "kind": "choice",
  "text": "Claim: The world has to ignore North Korean provocations\nPerspective: Ignoring North Korea wont resolve the situation",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q834485184bc",
  "kind": "choice",
  "text": "Statement 1: The price of this stock will peak before 9 years.\nStatement 2: Before 162 months, the price of this stock will peak.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q9448891ad51",
  "kind": "choice",
  "text": "Proposition A: ((~(z)&(j>y))&f)\nProposition B: ((((u>(y&~(w)))|z)>u)|y)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "qbc056e6fcd9",
  "kind": "choice",
  "text": "Statement 1: I will leave on a long vacation in 3 months.\nStatement 2: Before 19 days, I will leave on a long vacation.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qfc20c1dff3c",
  "kind": "choice",
  "text": "Statement 1: The war began in Oct 1925 and lasted until July 1931.\nStatement 2: The war lasted for less than 69 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q6229137f1b6",
  "kind": "choice",
  "text": "Claim: Violent video games cause violent crime\nPerspective: The government has a right to restrict the sale of violent video games, in order to protect law and order.",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q21ad81d7b5c",
  "kind": "choice",
  "text": "Statement 1: The war lasted from June 1903 to July 1929.\nStatement 2: The war lasted for 313 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q8916b5b0c0f",
  "kind": "choice",
  "text": "Proposition A: ((o>z)&(z&(y&d)))\nProposition B: (~(~((((d>o)&e)&t)))|y)",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q42bea10254a",
  "kind": "choice",
  "text": "Statement 1: The Presidential election is set to take place after 9 years.\nStatement 2: Before 132 months, the Presidential election is set to take place.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q8b402c7a7f2",
  "kind": "choice",
  "text": "Statement 1: Before 18th, I will have dinner with my friends.\nStatement 2: After 10th, I will have dinner with my friends.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qdaa396184ea",
  "kind": "choice",
  "text": "Claim: Police body cameras should be allowed\nPerspective: Police body cameras increase the safety of the public and the police",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q56333f84ed7",
  "kind": "choice",
  "text": "Proposition A: ~((((y|q)&~((l&(l>l))))|q))\nProposition B: ((l|q)>(y|l))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q4e127b54609",
  "kind": "choice",
  "text": "Proposition A: ~(((j|v)|y))\nProposition B: (((((b&((g&g)>j))&j)|~(g))|(g&(y>v)))&y)",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q848b3e23473",
  "kind": "choice",
  "text": "Proposition A: (((b>(b>b))|(~(j)>((o|o)|(b>j))))>~(o))\nProposition B: ((((j>j)>c)>~(~((~(b)>~(j)))))|b)",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q4cf1de58b99",
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
  "qid": "q456ae8e4c34",
  "kind": "choice",
  "text": "Proposition A: (b&u)\nProposition B: ((u|o)>(((~(((e&v)&e))|o)|i)|((o>o)>g)))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q8d486216b11",
  "kind": "choice",
  "text": "Statement 1: After September 1933, the price of this stock will peak.\nStatement 2: Before December 1994, the price of this stock will peak.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qbfa2f26adbe",
  "kind": "choice",
  "text": "Statement 1: The landlord will collect rent before 21:00.\nStatement 2: The landlord will collect rent after 19:00.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qf9b5787a6da",
  "kind": "choice",
  "text": "Proposition A: ((z&f)&f)\nProposition B: ((z>f)>f)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q989cb8800fa",
  "kind": "choice",
  "text": "Claim: Wind power should be a primary focus of future energy supply.\nPerspective: Wind energy provides for price stability in the long-term, wind will be with us for the duration",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qf7bdcfef416",
  "kind": "choice",
  "text": "Proposition A: ~(~(~((r|a))))\nProposition B: ~(n)",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "qbb3c1692569",
  "kind": "choice",
  "text": "Claim: Too much importance is placed upon correct spelling and grammar\nPerspective: Mistakes can actually be changes in the language.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q904edee8b9f",
  "kind": "choice",
  "text": "Claim: The niqab and other face coverings in schools must be banned\nPerspective: It’s a personal matter – it doesn’t concern others",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q5e336adb70c",
  "kind": "choice",
  "text": "Statement 1: On 22nd, final grades were due.\nStatement 2: Before 24th, final grades were due.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q8aa1356fbdc",
  "kind": "choice",
  "text": "Claim: Poetry should not be taught in schools\nPerspective: Education is about teaching culture, the arts, and creativity",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "qa1414c857de",
  "kind": "choice",
  "text": "Statement 1: In 9 months, Lily will fly to New York.\nStatement 2: Lily will fly to New York after 348 days.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q1076c2cb36e",
  "kind": "choice",
  "text": "Claim: People should have the right to die\nPerspective: The death of one individual has implications for others, which by definition, do not affect the suicide herself.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q740d82eeefe",
  "kind": "choice",
  "text": "Statement 1: My grandfather was born in May 1909 and died in Dec 1979.\nStatement 2: My grandfather lived for 848 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qf7a10205285",
  "kind": "choice",
  "text": "Statement 1: The park opens at 22:00 and closes at 13:00.\nStatement 2: The park is open for less than 15 hours.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qc1236102d03",
  "kind": "choice",
  "text": "Statement 1: After 2nd January 1958, the Presidential election took place.\nStatement 2: After 23rd September 1944, the Presidential election took place.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qa0953175fdd",
  "kind": "choice",
  "text": "Statement 1: After 7 months, Kendrick's album is set to drop.\nStatement 2: Kendrick's album is set to drop before 147 days.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qa6fd3b72999",
  "kind": "choice",
  "text": "Statement 1: We attended outdoor concerts from February 1913 to April 1941.\nStatement 2: We attended outdoor concerts for less than 339 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q4a758384fe4",
  "kind": "choice",
  "text": "Statement 1: After 09:00, the landlord collected rent.\nStatement 2: Before 03:00, the landlord collected rent.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q5db100313bc",
  "kind": "choice",
  "text": "Statement 1: On 16th December 1965, they will get married.\nStatement 2: After 22nd June 1967, they will get married.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q65d014307e0",
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
  "qid": "qcc0dbe90e08",
  "kind": "choice",
  "text": "Proposition A: ((((l&c)>~(l))>c)&(n&n))\nProposition B: (~((w|w))|(l|d))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qbd219663941",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict started in February 1900 and ended in December 1971.\nStatement 2: The prison sentence of that convict lasted for 862 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q13e33f7b7c9",
  "kind": "choice",
  "text": "Statement 1: Before 3 months, the park will open.\nStatement 2: After 240 days, the park will open.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q5bdf47d90a3",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out in 1958.\nStatement 2: The government budget will come out before 1917.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qac19bd48039",
  "kind": "choice",
  "text": "Statement 1: The pandemic began in 1952 and lasted until 1994.\nStatement 2: The pandemic lasted for less than 420 years.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qc3bb727d063",
  "kind": "choice",
  "text": "Statement 1: The meeting began at 01:00.\nStatement 2: The meeting began before 06:00.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qae2075c71f1",
  "kind": "choice",
  "text": "Proposition A: (n&u)\nProposition B: (~(~(n))>(p&(~(n)&n)))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q4ef8ba8fc56",
  "kind": "choice",
  "text": "Statement 1: After Sep, the city had a huge power outage.\nStatement 2: Before June, the city had a huge power outage.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qed429bf50bb",
  "kind": "choice",
  "text": "Proposition A: (((p>(p|f))>(u>(f&p)))&(f|f))\nProposition B: ((f&(f|~(f)))|u)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 }
]
