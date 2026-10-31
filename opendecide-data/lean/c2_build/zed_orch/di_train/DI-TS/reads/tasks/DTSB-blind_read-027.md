# A61 DI-TS label-noise blind read DTSB-blind_read-027

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/reads/answers/DTSB-blind_read-027.json

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
  "qid": "qcb78637eeb4",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will last from August to June.\nStatement 2: Her internship at Google will last for 11 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qeb8056d3152",
  "kind": "choice",
  "text": "Proposition A: (v&d)\nProposition B: ~(((d>v)&(((d&d)&(d&n))&l)))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q3df0f03b58c",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out after 3 years.\nStatement 2: Before 39 months, the government budget will come out.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qadde7254d8a",
  "kind": "choice",
  "text": "Statement 1: Lily will fly to New York in 1 day.\nStatement 2: After 14 hours, Lily will fly to New York.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qd97bedc7e8b",
  "kind": "choice",
  "text": "Statement 1: In Feb 1928, this team will win the world cup.\nStatement 2: After February 1978, this team will win the world cup.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qe1d334b7a90",
  "kind": "choice",
  "text": "Statement 1: Before 19th Sep 1921, Kendrick's album is set to drop.\nStatement 2: Before 3rd Jan 1981, Kendrick's album is set to drop.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qbc7e48762bc",
  "kind": "choice",
  "text": "Statement 1: In 7 days, the price of this stock will peak.\nStatement 2: Before 285 hours, the price of this stock will peak.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q7f2ee502029",
  "kind": "choice",
  "text": "Statement 1: In 1 day, my English class will begin.\nStatement 2: My English class will begin before 1 hour.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q824c985843e",
  "kind": "choice",
  "text": "Statement 1: On 28th Aug 1917, the Presidential election took place.\nStatement 2: After 15th Jan 1901, the Presidential election took place.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q8183c91f283",
  "kind": "choice",
  "text": "Proposition A: (a&(j|j))\nProposition B: (((a|v)|(v>a))&(~(j)>o))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q54d6f92c190",
  "kind": "choice",
  "text": "Statement 1: After 10 years, the government budget will come out.\nStatement 2: The government budget will come out before 171 months.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qb880ef7695c",
  "kind": "choice",
  "text": "Statement 1: We will go to Disneyland before 5 years.\nStatement 2: After 109 months, we will go to Disneyland.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qbdae0b27282",
  "kind": "choice",
  "text": "Statement 1: They will get married after 2 years.\nStatement 2: They will get married after 7 months.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qc80bdfc98b9",
  "kind": "choice",
  "text": "Statement 1: Before Apr, basketball season ended.\nStatement 2: Before March, basketball season ended.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q1a1d058cc7b",
  "kind": "choice",
  "text": "Statement 1: The football game will be telecasted from 2 PM to 1 AM.\nStatement 2: The football game will be telecasted for 110 hours.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q3ff49399fce",
  "kind": "choice",
  "text": "Claim: Hate speech on campus has to censored\nPerspective: The marketplace of ideas",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "qa6743fdf29a",
  "kind": "choice",
  "text": "Statement 1: The country was under a dictatorship from Jun 1956 to June 1963.\nStatement 2: The country was under a dictatorship for less than 84 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qfe1fe7c2459",
  "kind": "choice",
  "text": "Claim: Fund needle exchanges\nPerspective: Needle exchanges prevent the transmission of disease",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q48f55144f9f",
  "kind": "choice",
  "text": "Statement 1: After Aug, the country became a dictatorship.\nStatement 2: After Mar, the country became a dictatorship.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qee21c548676",
  "kind": "choice",
  "text": "Statement 1: Before 5 days, I will start working on my MS application.\nStatement 2: Before 184 hours, I will start working on my MS application.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qc07f1270f67",
  "kind": "choice",
  "text": "Proposition A: (i&(w&(g&~(c))))\nProposition B: (w&(~((g|g))|w))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q831c8793604",
  "kind": "choice",
  "text": "Statement 1: In 7 years, Lily will fly to New York.\nStatement 2: Before 29 months, Lily will fly to New York.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q7dd0d79a8ea",
  "kind": "choice",
  "text": "Claim: Forced evictions are necessary for African cities to become global players.\nPerspective: Forced evictions are a natural path of development.",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "qde967f8cb81",
  "kind": "choice",
  "text": "Claim: 1-child policy for every single country in the world!\nPerspective: There would be fewer unwanted children in the world ",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "qdc1940d518b",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album is set to drop on 15th.\nStatement 2: Kendrick's album is set to drop after 6th.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qac2b8173d42",
  "kind": "choice",
  "text": "Statement 1: Jake is planning to move after 14th.\nStatement 2: Jake is planning to move before 8th.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q6dcdc926187",
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
  "qid": "qcb4fd911af7",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will begin after 10 months.\nStatement 2: Before 335 days, her internship at Google will begin.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q5777dfee522",
  "kind": "choice",
  "text": "Claim: There should be video replays for refs in football\nPerspective: Only in Top Class football - make a monitor available to the match officials for replay of 'ball over the goal line' incidents only.",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q8d582f9520e",
  "kind": "choice",
  "text": "Proposition A: ~((~((x&f))|m))\nProposition B: ((~(~(~(u)))>f)>(x&(m>m)))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q7ca2b187a96",
  "kind": "choice",
  "text": "Statement 1: This article was published after Jun 1960.\nStatement 2: This article was published before February 1962.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q563a58381ab",
  "kind": "choice",
  "text": "Statement 1: After 1927, they got married.\nStatement 2: After 1914, they got married.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q3338eac1b36",
  "kind": "choice",
  "text": "Proposition A: ~((~((((m|d)>~(u))>u))>e))\nProposition B: (((v&n)>~(~(x)))>(d>m))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q322a13bb4e1",
  "kind": "choice",
  "text": "Statement 1: Before 1 month, the music concert will start in.\nStatement 2: Before 7 days, the music concert will start in.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q997aca30eab",
  "kind": "choice",
  "text": "Statement 1: In 5 months, Jake is planning to move.\nStatement 2: Before 270 days, Jake is planning to move.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "q72f253b7579",
  "kind": "choice",
  "text": "Statement 1: I will start my office leave in 7 days.\nStatement 2: Before 140 hours, I will start my office leave.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qc5d434b23db",
  "kind": "choice",
  "text": "Claim: USA must sign the Ottawa Convention banning landmines\nPerspective: Banning Landmines is a step towards reducing the horror of war",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q0fd6419913d",
  "kind": "choice",
  "text": "Statement 1: Our favorite breakfast restaurant opens from 15:00 to 4 AM.\nStatement 2: Our favorite breakfast restaurant opens for 13 hours.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q055f395e414",
  "kind": "choice",
  "text": "Statement 1: We visited Disneyland from 19th to 22nd.\nStatement 2: We visited Disneyland for 3 days.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qdbaccf89553",
  "kind": "choice",
  "text": "Proposition A: ~(~((~(l)>l)))\nProposition B: (((n|l)|(w|n))>((z>z)>(n>w)))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q2b66fe7dd6c",
  "kind": "choice",
  "text": "Claim: Genetics is a defence to murder\nPerspective: Is this 'Sound Science' or are Defendants simply clutching at straws?",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q72efa83aec1",
  "kind": "choice",
  "text": "Statement 1: On 5th February 1973, the war began.\nStatement 2: After 13th July 1944, the war began.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q76288e36ca0",
  "kind": "choice",
  "text": "Statement 1: The park is open from May to November.\nStatement 2: The park is open for less than 6 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qdb6fe63a64d",
  "kind": "choice",
  "text": "Statement 1: At 12 PM, he left his job.\nStatement 2: Before 15:00, he left his job.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q0699978571c",
  "kind": "choice",
  "text": "Claim: ID cards and the National Identity Register should be scrapped\nPerspective: The UK is a liberal society and unused to ID cards",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q5e3203f380d",
  "kind": "choice",
  "text": "Statement 1: After 19th, I started working on my MS application.\nStatement 2: Before 12th, I started working on my MS application.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qe258143c21f",
  "kind": "choice",
  "text": "Claim: The prevalence of ‘African mercenaries’ is decreasing\nPerspective: Mercenaries are still hired by NGOs ",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "qe12727d135f",
  "kind": "choice",
  "text": "Statement 1: We went to Disneyland after 19th Dec 1920.\nStatement 2: We went to Disneyland after 5th December 1922.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q9b2bb058f92",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict will end after 5 years.\nStatement 2: The prison sentence of that convict will end after 104 months.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qbbe31ab4d88",
  "kind": "choice",
  "text": "Proposition A: (~((y|h))&~(y))\nProposition B: (~(b)>~(h))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q8267ec9314a",
  "kind": "choice",
  "text": "Statement 1: The war began in February 1927 and lasted until January 1991.\nStatement 2: The war lasted for 639 years 2 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qc534c34dd02",
  "kind": "choice",
  "text": "Proposition A: (l&~((p|n)))\nProposition B: ((n&p)>~((((p>(p&c))|((j>j)&j))&(l|p))))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qa47e3b89838",
  "kind": "choice",
  "text": "Proposition A: (~(((u|u)&u))|~((u|(u&(u&(u|u))))))\nProposition B: ~((u|(~(~(u))&u)))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "qe98c265c77a",
  "kind": "choice",
  "text": "Claim: Constitutions Should Not Give Special Recognition To Minority Groups\nPerspective: Lack of special recognition disables the acquisition of constitutional rights",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "qc02c79b7256",
  "kind": "choice",
  "text": "Proposition A: (o&(((u&u)|((o>u)>u))>~(u)))\nProposition B: ~(~(((l>~(l))>(u|l))))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qd9affd06b3d",
  "kind": "choice",
  "text": "Statement 1: Before Jul, I will start my office leave.\nStatement 2: After Jun, I will start my office leave.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q79873d67a94",
  "kind": "choice",
  "text": "Proposition A: ~(f)\nProposition B: ((n|~(((~(h)>n)>~((h>n)))))|(~(k)>f))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qa101b591602",
  "kind": "choice",
  "text": "Statement 1: After 7 days, the country will declare martial law.\nStatement 2: The country will declare martial law after 72 hours.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qeea536c5468",
  "kind": "choice",
  "text": "Statement 1: The Presidential election is set to take place before Jun.\nStatement 2: The Presidential election is set to take place after June.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q59c417bee56",
  "kind": "choice",
  "text": "Proposition A: (s&~(x))\nProposition B: ((b|(x>s))|y)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q55e01292fbd",
  "kind": "choice",
  "text": "Claim: Constitutions Should Not Give Special Recognition To Minority Groups\nPerspective: Special recognition protects and fortifies minority rights",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "q50a98f528ea",
  "kind": "choice",
  "text": "Claim: The US and its allies were justified in taking military action against Iraq following Iraq’s invasion of Kuwait\nPerspective: Precedent established that unjust aggression would not be accepted. ",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q2149bb8f19b",
  "kind": "choice",
  "text": "Proposition A: (i|i)\nProposition B: (~((u>m))>~(((g>u)|~((i|i)))))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "qf7d362bda1c",
  "kind": "choice",
  "text": "Proposition A: (~((s|s))&h)\nProposition B: ~((((q&(t>h))|(t|(p>h)))>s))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q31be1963870",
  "kind": "choice",
  "text": "Proposition A: (~((r&k))&k)\nProposition B: ((((y|e)&r)|(k>s))|((k|d)>r))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q0fa4deb8131",
  "kind": "choice",
  "text": "Claim: Arming the police is a good idea\nPerspective: Arming the police does not deal with the causes underlying violence",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q92c00f2b0db",
  "kind": "choice",
  "text": "Statement 1: Before January 1900, my grandfather was born.\nStatement 2: Before October 1975, my grandfather was born.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q5165f12536a",
  "kind": "choice",
  "text": "Statement 1: Our favorite breakfast restaurant opened before 07:00.\nStatement 2: Our favorite breakfast restaurant opened after 00:00.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "q33e181ee632",
  "kind": "choice",
  "text": "Statement 1: The country will declare martial law before 7 days.\nStatement 2: After 49 hours, the country will declare martial law.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q8e9d87b218a",
  "kind": "choice",
  "text": "Statement 1: The President gave a speech on Wednesday.\nStatement 2: The President gave a speech before Thursday.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it."
 },
 {
  "qid": "q0054b5db7e1",
  "kind": "choice",
  "text": "Proposition A: ~(((t&f)>~((n&(d>(r&t))))))\nProposition B: ~(((n&n)&d))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q24767e2dea7",
  "kind": "choice",
  "text": "Statement 1: After 2 months, Apple will release the new iPhone.\nStatement 2: Before 152 days, Apple will release the new iPhone.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q4af514cc02f",
  "kind": "choice",
  "text": "Claim: It is a good idea to lease Crimea to Russia\nPerspective: Why would Ukraine trust a lease when the previous one was violated?",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qfd330b2d231",
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
  "qid": "q5f890916fb6",
  "kind": "choice",
  "text": "Statement 1: In Jan 1989, he left his job.\nStatement 2: After May 1927, he left his job.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q98598ed7b37",
  "kind": "choice",
  "text": "Statement 1: My grandfather lived from Jan 1924 to June 1996.\nStatement 2: My grandfather lived for less than 724 years 2 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q9b05262cd30",
  "kind": "choice",
  "text": "Statement 1: The President will give a speech in 4 days.\nStatement 2: Before 32 hours, the President will give a speech.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q576f5c5e84b",
  "kind": "choice",
  "text": "Statement 1: The conference lasted from 10th to 13th.\nStatement 2: The conference lasted for less than 3 days.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q5d747e0b505",
  "kind": "choice",
  "text": "Statement 1: The park opens at 09:00 and closes at 12:00.\nStatement 2: The park is open for 30 hours.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q71260015423",
  "kind": "choice",
  "text": "Proposition A: (~(d)&((b&((k>i)&i))|(b&b)))\nProposition B: (k>(l|i))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q5816f2e9e58",
  "kind": "choice",
  "text": "Statement 1: Before 10 months, the country will declare martial law.\nStatement 2: The country will declare martial law before 293 days.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q899cc4e8400",
  "kind": "choice",
  "text": "Proposition A: (((d&(r&g))|g)&(d|d))\nProposition B: (d|(((e&d)&((c&m)>c))|b))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q8726c204e91",
  "kind": "choice",
  "text": "Statement 1: Our favorite breakfast restaurant opens from 4 AM to 2 AM.\nStatement 2: Our favorite breakfast restaurant opens for less than 23 hours.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q47c33e6f789",
  "kind": "choice",
  "text": "Statement 1: The pandemic began in Nov 1906 and lasted until Feb 1956.\nStatement 2: The pandemic lasted for less than 592 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q27998d1debb",
  "kind": "choice",
  "text": "Claim: A permanent UNSC seat with veto power must be reserved to an African country\nPerspective: Proportionality",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "qaa3ca6991a4",
  "kind": "choice",
  "text": "Statement 1: The landlord will collect rent after 7 days.\nStatement 2: After 222 hours, the landlord will collect rent.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q6c82fbe8b8d",
  "kind": "choice",
  "text": "Statement 1: The failing company issued major layoffs from 9th to 17th.\nStatement 2: The failing company issued major layoffs for 80 days.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qa9c67a2e560",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict started in December and ended in Feb.\nStatement 2: The prison sentence of that convict lasted for less than 2 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qf052594c8b6",
  "kind": "choice",
  "text": "Statement 1: I started working on my MS application in October and got done in Aug.\nStatement 2: I worked on my MS application for less than 10 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qf6cb0635215",
  "kind": "choice",
  "text": "Statement 1: Our favorite breakfast restaurant opens at 05:00 and closes at 22:00.\nStatement 2: Our favorite breakfast restaurant opens for 170 hours.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q85d3e3074e1",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict lasted from August 1938 to Jul 1972.\nStatement 2: The prison sentence of that convict lasted for less than 33 years 11 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q151376c8464",
  "kind": "choice",
  "text": "Proposition A: ~((~(l)>~(~(~((w&o))))))\nProposition B: ((~(l)|((k&k)>(l|~((u|l)))))>o)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q4a9d8a2e4cc",
  "kind": "choice",
  "text": "Statement 1: I will start my office leave on Thursday.\nStatement 2: I will start my office leave after Wednesday.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qe9c56a2dc36",
  "kind": "choice",
  "text": "Claim: India’s Ban on the Satanic Verses is justified\nPerspective: Protection of Minors",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "qd25ec34bcbb",
  "kind": "choice",
  "text": "Claim: Lesotho should be annexed by South Africa\nPerspective: South Africa will gain influence, stability and a better image on the international stage",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "qa928bd52441",
  "kind": "choice",
  "text": "Statement 1: The servers' back up will start at 6 AM and end at 7 PM.\nStatement 2: The servers will back up for 130 hours.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qd3ffdd6b70a",
  "kind": "choice",
  "text": "Proposition A: (((g&h)|~((a|(i&h))))&h)\nProposition B: ((r>(g>h))|((((~(n)>a)|g)>(r|a))&h))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q45b73f8a9ef",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album dropped on Monday.\nStatement 2: Kendrick's album dropped after Thursday.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qf3507f6d83e",
  "kind": "choice",
  "text": "Statement 1: After 6 days, her internship at Google will begin.\nStatement 2: Her internship at Google will begin after 203 hours.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 }
]
