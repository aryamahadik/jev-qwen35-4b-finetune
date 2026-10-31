# A61 DI-TS label-noise blind read DTSB-blind_read-025

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/reads/answers/DTSB-blind_read-025.json

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
  "qid": "q34c4af7454e",
  "kind": "choice",
  "text": "Statement 1: I will be leaving on a long vacation in January and be back in August.\nStatement 2: I will be going on a long vacation for 8 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q13b6b49af75",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict started in Dec 1949 and ended in January 1963.\nStatement 2: The prison sentence of that convict lasted for 13 years 2 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q7f0bf4cd6cc",
  "kind": "choice",
  "text": "Claim: Children should be banned from watching shows that contain violence and other adult contents\nPerspective: banning wouldn't stop people viewing them",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "qc13d860162e",
  "kind": "choice",
  "text": "Statement 1: The spring quarter will begin after 9 months.\nStatement 2: After 138 days, the spring quarter will begin.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qafb2692024b",
  "kind": "choice",
  "text": "Statement 1: We attended outdoor concerts from 1952 to 1984.\nStatement 2: We attended outdoor concerts for less than 32 years.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q6763edd8afd",
  "kind": "choice",
  "text": "Statement 1: He left his job in Jun.\nStatement 2: He left his job before Oct.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qc7ad7905eb0",
  "kind": "choice",
  "text": "Statement 1: I started working on my MS application on Friday.\nStatement 2: I started working on my MS application after Tuesday.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q9b3d7c9604a",
  "kind": "choice",
  "text": "Proposition A: (h>~(h))\nProposition B: (e|i)",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q51e31b71158",
  "kind": "choice",
  "text": "Statement 1: The music concert lasted from 13:00 to 09:00.\nStatement 2: The music concert lasted for less than 21 hours.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qe1cfcb463e0",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out in Jul 1916.\nStatement 2: The government budget will come out after Jun 1937.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q8dab4fac3b3",
  "kind": "choice",
  "text": "Statement 1: The country became a dictatorship before 10th Oct 1976.\nStatement 2: The country became a dictatorship before 6th Jul 1936.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q4bc66e970ac",
  "kind": "choice",
  "text": "Proposition A: ((((q>q)>k)|l)&((l|~(l))&((k&l)|l)))\nProposition B: ~(~((~((k|k))>(l>k))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q21b8fe069d4",
  "kind": "choice",
  "text": "Claim: The African Union can meet its pledge to end all war on the continent by 2020\nPerspective: No mechanism to prevent crises and war exists",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "qfb0558f8915",
  "kind": "choice",
  "text": "Statement 1: They got married after March 1900.\nStatement 2: They got married before September 1934.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qcd209979bf5",
  "kind": "choice",
  "text": "Statement 1: After 20th May 1940, the tiger was last spotted.\nStatement 2: Before 14th July 1983, the tiger was last spotted.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q959a0559cbb",
  "kind": "choice",
  "text": "Claim: Religion In Itself Is A Purely Positive Force In The World\nPerspective: Religious organisations are by far the largest providers of charity in the world",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q380667d6604",
  "kind": "choice",
  "text": "Proposition A: ~((~(~((j&(e&a))))>~((s&s))))\nProposition B: ((~((s|s))>(y|g))|((c&y)&s))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q824ce1269e1",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album is set to drop on 24th Dec 1960.\nStatement 2: Kendrick's album is set to drop after 25th Oct 1950.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q012081280b7",
  "kind": "choice",
  "text": "Claim: Subsidise the translation of academic work in the languages of developing countries\nPerspective: It is better to have fewer languages in common use in global academic and economic interrelations",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q9d48e610568",
  "kind": "choice",
  "text": "Statement 1: Lily flew to New York from 03:00 to 9 PM.\nStatement 2: Lily flew to New York for less than 18 hours.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q6ac0640f7bd",
  "kind": "choice",
  "text": "Statement 1: The country was under a dictatorship from December 1967 to February 1978.\nStatement 2: The country was under a dictatorship for less than 10 years 3 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qcebc3576823",
  "kind": "choice",
  "text": "Statement 1: In Oct 1931, they will get married.\nStatement 2: Before Apr 1907, they will get married.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q448d76b2f69",
  "kind": "choice",
  "text": "Statement 1: After Jun, I started my office leave.\nStatement 2: Before Aug, I started my office leave.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qc7667a944c6",
  "kind": "choice",
  "text": "Claim: Job applicants should have to disclose their spent criminal convictions\nPerspective: Provision of care services requires such disclosure",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "q82fbe2a9977",
  "kind": "choice",
  "text": "Statement 1: Her internship at Google will begin after 6 years.\nStatement 2: Before 128 months, her internship at Google will begin.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q60793601683",
  "kind": "choice",
  "text": "Proposition A: ~(~(~(e)))\nProposition B: (e&e)",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qa361e676cef",
  "kind": "choice",
  "text": "Proposition A: ((a&x)&((((v>s)>~(((a&a)&x)))>u)>v))\nProposition B: ~(~((x>(s>a))))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "qec5a424b608",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out in 2 days.\nStatement 2: The government budget will come out after 5 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q9b77761675c",
  "kind": "choice",
  "text": "Statement 1: Michael reached my house on Saturday.\nStatement 2: Michael reached my house after Friday.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q450b6dbb7d6",
  "kind": "choice",
  "text": "Proposition A: ~((s|s))\nProposition B: (~(((~(s)>(s&s))>s))|s)",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q21e166c9290",
  "kind": "choice",
  "text": "Claim: The European Union should lift its ban on member states selling arms to China\nPerspective: There is no reason to strengthen China militarily",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "qe23e7f7700b",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album is set to drop after 9 months.\nStatement 2: Before 288 days, Kendrick's album is set to drop.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q161eb98a218",
  "kind": "choice",
  "text": "Statement 1: Before 4 days, the prison sentence of that convict will end.\nStatement 2: The prison sentence of that convict will end after 19 hours.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q04cb6ace820",
  "kind": "choice",
  "text": "Statement 1: Before 5 PM, the price of this stock peaked.\nStatement 2: Before 9 PM, the price of this stock peaked.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q90c956a3fb1",
  "kind": "choice",
  "text": "Claim: Nuclear technology must be adopted\nPerspective: Nuclear power is very expensive",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "q66f1723b28d",
  "kind": "choice",
  "text": "Statement 1: In 3 months, the prison sentence of that convict will end.\nStatement 2: The prison sentence of that convict will end before 89 days.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "qe8372779715",
  "kind": "choice",
  "text": "Proposition A: (o&(j>(~(e)>~((j>m)))))\nProposition B: (p>(s&m))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qb8761af03a6",
  "kind": "choice",
  "text": "Statement 1: After 10 days, the price of this stock will peak.\nStatement 2: The price of this stock will peak after 191 hours.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q4bd194b6291",
  "kind": "choice",
  "text": "Statement 1: The conference will be held before 6 years.\nStatement 2: The conference will be held after 124 months.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qaac6052996d",
  "kind": "choice",
  "text": "Statement 1: A tsunami will hit the coast in 10 days.\nStatement 2: A tsunami will hit the coast before 120 hours.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q7206b483c7e",
  "kind": "choice",
  "text": "Claim: Male infant circumcision is tantamount to child abuse\nPerspective: Parents have the right to use their best judgment, in the light of medical advice, as to what is in the best interest of their child ",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "q6bfdfb142f1",
  "kind": "choice",
  "text": "Statement 1: We attended outdoor concerts from September 1909 to Jul 1937.\nStatement 2: We attended outdoor concerts for 334 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q8bcbdcd1617",
  "kind": "choice",
  "text": "Statement 1: After 1968, I posted this picture on Instagram.\nStatement 2: After 1999, I posted this picture on Instagram.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q6c46b880bef",
  "kind": "choice",
  "text": "Statement 1: On Wednesday, final grades were due.\nStatement 2: After Thursday, final grades were due.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qde48f60d7e8",
  "kind": "choice",
  "text": "Proposition A: ((v&d)&k)\nProposition B: (~(~((v&r)))|(r>((d&k)|y)))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qe7dd5e9c872",
  "kind": "choice",
  "text": "Claim: The European Union should lift its ban on member states selling arms to China\nPerspective: China is a threat to regional stability",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q90599c93ca7",
  "kind": "choice",
  "text": "Proposition A: (~((m|((m>(a>(v|s)))&~(t))))&(t>r))\nProposition B: ~(~((n|a)))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q8a68625c655",
  "kind": "choice",
  "text": "Claim: New York City has the right to regulate the size of sodas bought on the market\nPerspective: It is undemocratic to have the law pass through the board of health.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q16068365e84",
  "kind": "choice",
  "text": "Statement 1: The music concert will start in before 6 months.\nStatement 2: The music concert will start in before 57 days.",
  "question": "Statement 1 says when something happens relative to now, and statement 2 does the same in another unit. Which option fits?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qd774063a8f2",
  "kind": "choice",
  "text": "Statement 1: The country became a dictatorship in 1939 which ended in 2000.\nStatement 2: The country was under a dictatorship for less than 610 years.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q21d6e5f5d3d",
  "kind": "choice",
  "text": "Claim: Racial quotas must be set in South African rugby\nPerspective: Quotas can drive players away.",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q6e76060b7e6",
  "kind": "choice",
  "text": "Statement 1: We attended outdoor concerts from 1943 to 1963.\nStatement 2: We attended outdoor concerts for less than 200 years.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qeeaad8b27ad",
  "kind": "choice",
  "text": "Proposition A: ~(((e>(r&(~(q)|q)))|l))\nProposition B: (~(~(((n>n)&(r>r))))&q)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q830832c7367",
  "kind": "choice",
  "text": "Statement 1: In May, her internship at Google began.\nStatement 2: Before November, her internship at Google began.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q1648b040cb2",
  "kind": "choice",
  "text": "Statement 1: We started attending outdoor concerts in February 1963 and stopped in December 1979.\nStatement 2: We attended outdoor concerts for 16 years 10 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q0c785f2fa8b",
  "kind": "choice",
  "text": "Statement 1: After 14th Nov 1922, the prison sentence of that convict will end.\nStatement 2: Before 8th February 1926, the prison sentence of that convict will end.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q7e656aa203b",
  "kind": "choice",
  "text": "Proposition A: (t&u)\nProposition B: ((u>~(x))|t)",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qbbab6704f4e",
  "kind": "choice",
  "text": "Statement 1: At 2 AM, the city had a huge power outage.\nStatement 2: After 8 AM, the city had a huge power outage.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q98a0b4ed268",
  "kind": "choice",
  "text": "Claim: Genetics is a defence to murder\nPerspective: Not \"in court,\" but other considerations should be made.",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "qd5fd590fd61",
  "kind": "choice",
  "text": "Claim: US must help in fighting terrorist organisations in Africa\nPerspective: Increased global security",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective argues in favour of the claim."
 },
 {
  "qid": "qd56e76d374d",
  "kind": "choice",
  "text": "Proposition A: ((i>p)&a)\nProposition B: (~(~(a))|~((~((c&(x|c)))|~((m&m)))))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qa9c4b3188a1",
  "kind": "choice",
  "text": "Statement 1: I will be going on a long vacation from February to November.\nStatement 2: I will be going on a long vacation for 90 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q03c8153b977",
  "kind": "choice",
  "text": "Statement 1: At 2 AM, the conference was held.\nStatement 2: Before 7 AM, the conference was held.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q92bb174af5c",
  "kind": "choice",
  "text": "Statement 1: My grandfather lived from Sep 1906 to Dec 1914.\nStatement 2: My grandfather lived for less than 82 years 6 months.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q9f0b1257b81",
  "kind": "choice",
  "text": "Claim: Reality TV has gone too far\nPerspective: Reality TV shows bring out the worse in people.",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q0759185aaea",
  "kind": "choice",
  "text": "Statement 1: Before 6 years, the prison sentence of that convict will end.\nStatement 2: The prison sentence of that convict will end after 111 months.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q14c94406b7c",
  "kind": "choice",
  "text": "Claim: Children Should Have The Right To Vote In Elections\nPerspective: Voting at a lower age would increase participation",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q4e1bdb777f5",
  "kind": "choice",
  "text": "Proposition A: (o&~(((n|r)|~(p))))\nProposition B: ((p>o)&((f>x)>p))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q2c0bfb9a3ff",
  "kind": "choice",
  "text": "Statement 1: We will ride our bikes before 1 day.\nStatement 2: After 20 hours, we will ride our bikes.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "q8f5b6800285",
  "kind": "choice",
  "text": "Statement 1: The pandemic began before March.\nStatement 2: The pandemic began after February.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qaab54539cad",
  "kind": "choice",
  "text": "Statement 1: After 2 months, the country will declare martial law.\nStatement 2: The country will declare martial law after 28 days.",
  "question": "Compare the size of the time spans in the two statements (for example 1 month against 29 days) and pick the matching option.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q6f7246fbcc7",
  "kind": "choice",
  "text": "Proposition A: ((~(((k|n)&(k&y)))&(v&k))&o)\nProposition B: (~(((~(((b&n)|m))&k)&~(o)))>(b|n))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "qf97d769abc0",
  "kind": "choice",
  "text": "Claim: Western universities should only place satellites in states that respect free speech\nPerspective: Universities should exchange ideas not impose them",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "qf2422b0ab99",
  "kind": "choice",
  "text": "Proposition A: ((~((k|k))>(i&w))&((~(~(g))&k)&(g>w)))\nProposition B: ~(~(((c>k)&~((c&~(i))))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q3902e5158cf",
  "kind": "choice",
  "text": "Statement 1: We started attending outdoor concerts in February 1919 and stopped in May 1977.\nStatement 2: We attended outdoor concerts for less than 58 years 3 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q1f6b0c5fc8d",
  "kind": "choice",
  "text": "Claim: Britain should give up its EU rebate\nPerspective: The Rebate makes membership acceptable to the British people",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "qe4b7abc1d1b",
  "kind": "choice",
  "text": "Claim: We believe in world government\nPerspective: There is no feasible transition path to a world government model",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "q10e17ee58d8",
  "kind": "choice",
  "text": "Claim: Taking food thrown out by supermarkets should not be illegal\nPerspective: It isn't stealing to take something that has been thrown away.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim."
 },
 {
  "qid": "qc5f96606acd",
  "kind": "choice",
  "text": "Statement 1: The pandemic lasted from August 1910 to August 1951.\nStatement 2: The pandemic lasted for less than 41 years 1 month.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q4858c1527a1",
  "kind": "choice",
  "text": "Statement 1: The failing company issued major layoffs after 5th September 1925.\nStatement 2: The failing company issued major layoffs before 9th Apr 1972.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qa43244fe6a7",
  "kind": "choice",
  "text": "Statement 1: My English class begins at 7 AM and ends at 04:00.\nStatement 2: My English class is scheduled for less than 21 hours.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q8d6b37889fc",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict will end before 1 day.\nStatement 2: The prison sentence of that convict will end after 77 hours.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q698dc375b67",
  "kind": "choice",
  "text": "Statement 1: Michael bought the house after August 1981.\nStatement 2: Michael bought the house after October 1957.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q465159f4fbe",
  "kind": "choice",
  "text": "Statement 1: This team won the world cup after 25th.\nStatement 2: This team won the world cup before 13th.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "q19629eecb6c",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album is set to drop after June.\nStatement 2: Kendrick's album is set to drop after July.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qf5bd8a15f03",
  "kind": "choice",
  "text": "Proposition A: (((~(m)&((m&m)&e))|(i>(z|d)))&(i&d))\nProposition B: ((z|z)>(d>(e|(e|~(m)))))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "qfa58b8b808a",
  "kind": "choice",
  "text": "Claim: Act to regulate the activities of Sovereign Wealth Funds\nPerspective: Sovereign wealth funds must be regulated",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "qd8b9af2a8ce",
  "kind": "choice",
  "text": "Claim: We can trust Republicans with the economy\nPerspective: Deregulation contributed to the banking crises and, therefore the 2009 economic crash ",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q5bbb57bba33",
  "kind": "choice",
  "text": "Statement 1: The war began in Sep 1928 and lasted until April 1993.\nStatement 2: The war lasted for 64 years 8 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "qf56885c0cfe",
  "kind": "choice",
  "text": "Proposition A: (i&~(w))\nProposition B: (o|~(i))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "qd684b74f812",
  "kind": "choice",
  "text": "Claim: There must be referendums held on any new EU treaty\nPerspective: Referendums are more about PR than politics.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qb3ec48d4a40",
  "kind": "choice",
  "text": "Statement 1: On 28th, the President gave a speech.\nStatement 2: Before 24th, the President gave a speech.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qbd48b55c48e",
  "kind": "choice",
  "text": "Statement 1: I posted this picture on Instagram at 2 AM.\nStatement 2: I posted this picture on Instagram after 9 AM.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "q5fb235b0b50",
  "kind": "choice",
  "text": "Statement 1: In 10 months, the park will open.\nStatement 2: Before 244 days, the park will open.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qc86bbaecd1e",
  "kind": "choice",
  "text": "Statement 1: In 3 months, the music concert will start in.\nStatement 2: The music concert will start in after 13 days.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q44265a24ed6",
  "kind": "choice",
  "text": "Proposition A: ~(~((((a&~(i))|q)&(y|q))))\nProposition B: (((i&(w&a))|(q&q))|~(i))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q48d80d7ced4",
  "kind": "choice",
  "text": "Claim: The federal minimum wage should be increased\nPerspective: Teenagers and young adults may be shut out of the workforce if the minimum wage is increased.",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qeb6d66015d0",
  "kind": "choice",
  "text": "Statement 1: Michael will buy the house after 5 years.\nStatement 2: Michael will buy the house after 4 months.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q1ed7c132a86",
  "kind": "choice",
  "text": "Proposition A: (~(f)&r)\nProposition B: (((e&(~((e>(((e|r)&r)>r)))|r))|f)>f)",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 }
]
