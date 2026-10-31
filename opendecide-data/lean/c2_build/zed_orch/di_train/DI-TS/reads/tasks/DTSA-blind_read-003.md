# A61 DI-TS label-noise blind read DTSA-blind_read-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/reads/answers/DTSA-blind_read-003.json

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
  "qid": "qab46d38e77e",
  "kind": "choice",
  "text": "Claim: We have to offer amnesty to bloggers currently prosecuted by their native states\nPerspective: These people are under serious threat for their pursuit of justice",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q1700e6ae1c5",
  "kind": "choice",
  "text": "Statement 1: Before 1 month, the war will begin.\nStatement 2: Before 43 days, the war will begin.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q58907dd58fe",
  "kind": "choice",
  "text": "Proposition A: ((b|l)|(l|l))\nProposition B: (~(~(~(m)))>((b|m)>m))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q7c6c5c241fb",
  "kind": "choice",
  "text": "Statement 1: The price of this stock will peak before 9 days.\nStatement 2: After 296 hours, the price of this stock will peak.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q5416881001b",
  "kind": "choice",
  "text": "Claim: Hosting the world cup is beneficial\nPerspective: Financially costly for the hosts",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q1928d486978",
  "kind": "choice",
  "text": "Statement 1: I will start working on my MS application at 6 PM.\nStatement 2: I will start working on my MS application after 12 PM.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q68483e87b0e",
  "kind": "choice",
  "text": "Proposition A: ~((~((((d|d)|u)>t))|((h>k)|b)))\nProposition B: (u|(i&((((u>b)|i)&b)&(k|d))))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q187a67ee6e0",
  "kind": "choice",
  "text": "Statement 1: Before 8 days, the prison sentence of that convict will end.\nStatement 2: The prison sentence of that convict will end after 216 hours.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qc0dfe5f6ba4",
  "kind": "choice",
  "text": "Claim: Cut aid to African states that criminalise homosexuality\nPerspective: Western Money, Western Discretion",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "qbe94d6ee89c",
  "kind": "choice",
  "text": "Claim: The glass ceiling for women still exists\nPerspective: Women are getting the most prestigious of jobs now",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "qf21bb136c48",
  "kind": "choice",
  "text": "Statement 1: We will ride our bikes before 1 day.\nStatement 2: After 20 hours, we will ride our bikes.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q4907cb53822",
  "kind": "choice",
  "text": "Claim: The health benefits of genetically modified foods outweigh their risks\nPerspective: If we allow GM foods, where will science stop?",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q70dedf0c56e",
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
  "qid": "q4fe44aad32e",
  "kind": "choice",
  "text": "Statement 1: They got married in Jul 1970.\nStatement 2: They got married after October 1983.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q0e6487ae3e2",
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
  "qid": "q23e284b1bf3",
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
  "qid": "q96ff0a01307",
  "kind": "choice",
  "text": "Statement 1: The city will have a huge power outage after 6 days.\nStatement 2: Before 158 hours, the city will have a huge power outage.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qd1b4773b336",
  "kind": "choice",
  "text": "Statement 1: After 6 years, the conference will be held.\nStatement 2: The conference will be held before 84 months.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qf8d5bb4db86",
  "kind": "choice",
  "text": "Statement 1: The weather here is pleasant from January to Oct.\nStatement 2: The weather here is pleasant for less than 9 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qba0b98da015",
  "kind": "choice",
  "text": "Statement 1: A huge power outage in the city started at 11:00 and ended at 06:00.\nStatement 2: The city had a huge power outage for less than 190 hours.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q73b7036eafc",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict started in Aug 1933 and ended in Oct 1977.\nStatement 2: The prison sentence of that convict lasted for less than 44 years 2 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qc0496fd9f28",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will last from Nov to Jun.\nStatement 2: Her internship at Google will last for 7 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q54dc9e20c58",
  "kind": "choice",
  "text": "Statement 1: In Nov 1965, they will get married.\nStatement 2: After Dec 1945, they will get married.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qd6652ac424e",
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
  "qid": "q4beb6086d0e",
  "kind": "choice",
  "text": "Statement 1: We attended outdoor concerts from November 1913 to Sep 1958.\nStatement 2: We attended outdoor concerts for less than 539 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q139da2db29d",
  "kind": "choice",
  "text": "Claim: The United States should maintain its embargo against Cuba\nPerspective: The embargo enables the United States to apply pressure on the Cuban government to improve human rights. ",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q514f61380b3",
  "kind": "choice",
  "text": "Claim: The world should go vegan\nPerspective: Vegetarians live longer. ",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "qa7960a2812e",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict will end in July.\nStatement 2: The prison sentence of that convict will end after June.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q20b4303bfa3",
  "kind": "choice",
  "text": "Proposition A: ((~((p|p))|(j|(t|t)))&p)\nProposition B: (((j>j)&~((r>m)))|(((p|(r|r))>m)|(a&a)))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q43effe054bb",
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
  "qid": "qf52bbeb6ebd",
  "kind": "choice",
  "text": "Claim: Social networking sites are good for our society\nPerspective: Social media helps people who are socially isolated or shy connect with other people.",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "qaa62a1b1b05",
  "kind": "choice",
  "text": "Statement 1: We attended outdoor concerts from January to December.\nStatement 2: We attended outdoor concerts for 12 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qe684829242f",
  "kind": "choice",
  "text": "Statement 1: At 00:00, our favorite breakfast restaurant opened.\nStatement 2: After 10 AM, our favorite breakfast restaurant opened.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qad3c910f05d",
  "kind": "choice",
  "text": "Proposition A: (~(k)&(q&((x&((q|x)>(k>z)))&c)))\nProposition B: (~((a>(x|((f|(z>k))|k))))|a)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qba85fddc95d",
  "kind": "choice",
  "text": "Proposition A: ((((t>t)>t)&s)&~(~((y|((t|o)|(o|s))))))\nProposition B: ~(((t>(o&~(s)))|~((t|s))))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qa20459a9d47",
  "kind": "choice",
  "text": "Statement 1: The park opens at 09:00 and closes at 17:00.\nStatement 2: The park is open for less than 80 hours.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q4b0b7683201",
  "kind": "choice",
  "text": "Statement 1: In 3 days, Michael will reach my house.\nStatement 2: Michael will reach my house after 33 hours.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q8cca6723d70",
  "kind": "choice",
  "text": "Statement 1: The pandemic began in Apr 1941 and lasted until Jan 1967.\nStatement 2: The pandemic lasted for less than 257 years 6 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q83b2884896d",
  "kind": "choice",
  "text": "Claim: Build the Grand Inga Dam\nPerspective: Such a big project is beyond DRC’s capacity",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "q2614ce2fbf6",
  "kind": "choice",
  "text": "Proposition A: ((o>a)>o)\nProposition B: ((l>o)&(l>(l>((a|(x>l))>(a>o)))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q330d34c1a84",
  "kind": "choice",
  "text": "Claim: Internet access is a human right\nPerspective: The music and film industries are suffering due to file-sharing.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q0bdbc3b0f97",
  "kind": "choice",
  "text": "Statement 1: My English class begins at 4 PM and ends at 6 AM.\nStatement 2: My English class is scheduled for less than 15 hours.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q073124f25d0",
  "kind": "choice",
  "text": "Statement 1: In 6 months, the failing company will issue major layoffs.\nStatement 2: After 179 days, the failing company will issue major layoffs.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q8c5802d5f34",
  "kind": "choice",
  "text": "Proposition A: ~((j>(((t>s)|t)&~(s))))\nProposition B: ((w&(s>n))>j)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q6e23f67e251",
  "kind": "choice",
  "text": "Claim: Same sex relationships should have the same legal status as heterosexual relationships under EU law\nPerspective: Marriage is about more than procreation, therefore gay couples should not be denied the right to marry due to their biology.",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "qea4e029cab4",
  "kind": "choice",
  "text": "Statement 1: The coding competition started on Wednesday and ended on Monday.\nStatement 2: The coding competition was held for 50 days.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q0458a9f7978",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will last from May to November.\nStatement 2: Her internship at Google will last for less than 6 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q6bc16fe0417",
  "kind": "choice",
  "text": "Statement 1: In Mar 1968, the conference was held.\nStatement 2: Before April 1998, the conference was held.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qbecc6d69a7b",
  "kind": "choice",
  "text": "Statement 1: Before Mar 1962, our favorite breakfast restaurant opened.\nStatement 2: After Nov 1975, our favorite breakfast restaurant opened.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qccc362b4a68",
  "kind": "choice",
  "text": "Statement 1: In Nov, the music concert started.\nStatement 2: After October, the music concert started.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qc6b604ef06d",
  "kind": "choice",
  "text": "Claim: Unemployment benefit should be paid in the form of vouchers for food, shelter and the basics of life\nPerspective: Maintaining Status Quo would Boost the Economy and Reduce Unemployment Rate",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q5389eaf843d",
  "kind": "choice",
  "text": "Statement 1: In 10 years, Michael will buy the house.\nStatement 2: After 166 months, Michael will buy the house.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qa4d72819c4b",
  "kind": "choice",
  "text": "Claim: We must ban the promotion of diets\nPerspective: Banning advertising won't work",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q93e451570e0",
  "kind": "choice",
  "text": "Statement 1: The war began in Mar 1942 and lasted until Dec 1973.\nStatement 2: The war lasted for 382 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q57724689f6b",
  "kind": "choice",
  "text": "Statement 1: On 19th February 1991, the conference was held.\nStatement 2: After 10th Apr 1985, the conference was held.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qcf69cae79e6",
  "kind": "choice",
  "text": "Statement 1: A tsunami will hit the coast after July.\nStatement 2: A tsunami will hit the coast before September.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q22da8287020",
  "kind": "choice",
  "text": "Proposition A: ((d&(z|s))&l)\nProposition B: (((u|u)&((h|~(l))>h))>s)",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qeb59faef6f0",
  "kind": "choice",
  "text": "Claim: Death penalty is justified\nPerspective: The penalty of death is a crime deterrent.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q135193247fa",
  "kind": "choice",
  "text": "Statement 1: My doctor's appointment is scheduled to take place before 4 AM.\nStatement 2: My doctor's appointment is scheduled to take place before 11 AM.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qa6b137ea047",
  "kind": "choice",
  "text": "Statement 1: Michael will buy the house on 11th December 1919.\nStatement 2: Michael will buy the house after 5th Aug 1935.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qebb47953767",
  "kind": "choice",
  "text": "Proposition A: ((v&t)&t)\nProposition B: (((f|((x|a)&~(l)))>~(~((x|t))))|(l>v))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q3be57de4664",
  "kind": "choice",
  "text": "Statement 1: The conference lasted from Wednesday to Tuesday.\nStatement 2: The conference lasted for 6 days.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qc8bb72cfc8e",
  "kind": "choice",
  "text": "Claim: A fat tax should be implemented.\nPerspective: A fat tax levels out the playing field for healthier food",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q99a79eed46c",
  "kind": "choice",
  "text": "Statement 1: Before 7 years, they will get married.\nStatement 2: They will get married after 32 months.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q70d09837a47",
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
  "qid": "q43690581d96",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album is set to drop after 1989.\nStatement 2: Kendrick's album is set to drop after 1983.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "qe2149b2e68b",
  "kind": "choice",
  "text": "Statement 1: Before May, the Presidential election took place.\nStatement 2: After April, the Presidential election took place.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q792e43718b3",
  "kind": "choice",
  "text": "Statement 1: The pandemic began in Apr 1913 and lasted until Jan 1923.\nStatement 2: The pandemic lasted for less than 9 years 9 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q009bf9d14f5",
  "kind": "choice",
  "text": "Claim: It is crucial to support the development of a missile defence system\nPerspective: As a matter of principle, every country, including the United States, has the right to defend itself to the best of its technological and economic ability",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q6ae42fb3639",
  "kind": "choice",
  "text": "Proposition A: (~(~(z))|((z|z)&~(~(i))))\nProposition B: (z|~(~(i)))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qfde2dde5e6d",
  "kind": "choice",
  "text": "Claim: Unilateral nuclear disarmament is the best way to create a safer world\nPerspective: Nuclear waste disposal is rarely safe/efficient; it is too much to expect a sqeaky clean disposal/disarmament of nuclear weapons  ",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q2b9e4e1158b",
  "kind": "choice",
  "text": "Statement 1: The park is open from Friday to Thursday.\nStatement 2: The park is open for less than 6 days.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qaf76b496ee7",
  "kind": "choice",
  "text": "Proposition A: (~(c)&((o&f)>((x>~(c))&(~(c)>~(p)))))\nProposition B: (((o&(f>o))&((c&f)&(x>o)))>(y|y))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qa1d814a0476",
  "kind": "choice",
  "text": "Claim: Net neutrality should be restored\nPerspective: Net neutrality provides for the free circulation of data and services.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q38d87de987f",
  "kind": "choice",
  "text": "Claim: Students should have to wear school uniforms\nPerspective: Creates a sense of equality",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "qc77eda09be9",
  "kind": "choice",
  "text": "Statement 1: My grandfather was born in October 1909 and died in July 1972.\nStatement 2: My grandfather lived for 753 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q6960432f607",
  "kind": "choice",
  "text": "Statement 1: I worked on my MS application from 5th to 28th.\nStatement 2: I worked on my MS application for 23 days.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qfe5302ad294",
  "kind": "choice",
  "text": "Statement 1: After 10 days, the failing company will issue major layoffs.\nStatement 2: The failing company will issue major layoffs before 177 hours.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q5de7d99078d",
  "kind": "choice",
  "text": "Claim: We should detain terror suspects without trial\nPerspective: The war on terror is not an armed conflict, and therefore internment without trial is illegal.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "qbae0556863a",
  "kind": "choice",
  "text": "Statement 1: The coding competition will start in 6 days.\nStatement 2: After 188 hours, the coding competition will start.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q442390ccfb0",
  "kind": "choice",
  "text": "Proposition A: (r&(r&~(c)))\nProposition B: (f|((~(c)>f)&~(((((q>c)>c)&l)|(v>l)))))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q15be7f47e11",
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
  "qid": "q3a7a4bab6c1",
  "kind": "choice",
  "text": "Statement 1: Our favorite breakfast restaurant opened before 6th January 1984.\nStatement 2: Our favorite breakfast restaurant opened after 24th June 1949.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q9d60798d2d4",
  "kind": "choice",
  "text": "Claim: Receiving multiple vaccines are safe\nPerspective: All vaccinations are tested rigorously before they are approved, and tracked afterwards ",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q2b3f8db7d57",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album dropped before 17th Aug 1980.\nStatement 2: Kendrick's album dropped before 15th May 1986.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q7178bfb3f07",
  "kind": "choice",
  "text": "Proposition A: ~(((c>(w&s))|(m&~(m))))\nProposition B: (((u>s)|((w|(c>~(s)))>(m>c)))&(w>w))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q2b443d6af76",
  "kind": "choice",
  "text": "Statement 1: The conference will be held before 2 years.\nStatement 2: After 11 months, the conference will be held.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q6c12ba4029c",
  "kind": "choice",
  "text": "Statement 1: We will go to Disneyland after 8 years.\nStatement 2: Before 78 months, we will go to Disneyland.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q71e92dc79ef",
  "kind": "choice",
  "text": "Statement 1: Before August, the pandemic began.\nStatement 2: After May, the pandemic began.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q50f239bc8ca",
  "kind": "choice",
  "text": "Statement 1: Before 9 years, Michael will buy the house.\nStatement 2: After 54 months, Michael will buy the house.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qe34e59f45ae",
  "kind": "choice",
  "text": "Proposition A: (~((v&~(~(x))))&~((b>~(g))))\nProposition B: (i|~((x|g)))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qddd3f3a5151",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out on 19th November 1979.\nStatement 2: The government budget will come out after 19th March 1985.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q674a006266c",
  "kind": "choice",
  "text": "Proposition A: ~((~((m>e))>(c>~((~(p)>(a>e))))))\nProposition B: (h|(~(~((m>c)))>a))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qe1342beb235",
  "kind": "choice",
  "text": "Statement 1: The park is open from 23rd to 25th.\nStatement 2: The park is open for 3 days.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q8c9b7c512ba",
  "kind": "choice",
  "text": "Statement 1: The country will declare martial law after 3 days.\nStatement 2: The country will declare martial law before 14 hours.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q45c0bccbfe5",
  "kind": "choice",
  "text": "Statement 1: My doctor's appointment took place from 07:00 to 20:00.\nStatement 2: My doctor's appointment took place for less than 13 hours.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q1f0222eb7d4",
  "kind": "choice",
  "text": "Proposition A: (c&((y|g)>~(~(y))))\nProposition B: ((~(c)>k)|y)",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q7240442b87f",
  "kind": "choice",
  "text": "Statement 1: The country was under a dictatorship from 1933 to 1986.\nStatement 2: The country was under a dictatorship for 530 years.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qffed9e2e178",
  "kind": "choice",
  "text": "Statement 1: The failing company started issuing major layoffs on 25th which ended on 27th.\nStatement 2: The failing company issued major layoffs for less than 2 days.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 }
]
