# A61 DI-TS label-noise blind read DTSA-blind_read-047

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/reads/answers/DTSA-blind_read-047.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 73. Answers expected: 73 (one per item, each with that item's qid).

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
  "qid": "q4e0709954b7",
  "kind": "choice",
  "text": "Proposition A: (h&j)\nProposition B: ((h|(h&t))|(~(((h|e)>j))>~(((e>j)>j))))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q92a8f5c8d63",
  "kind": "choice",
  "text": "Proposition A: (((~((n>~(h)))&e)&(((c|z)&a)|h))&a)\nProposition B: (n|h)",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: No assignment of true/false to the letters makes A true while making B false."
 },
 {
  "qid": "q477dc748ea8",
  "kind": "choice",
  "text": "Statement 1: My grandfather was born in 1902 and died in 1982.\nStatement 2: My grandfather lived for less than 80 years.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q40526ad5a67",
  "kind": "choice",
  "text": "Statement 1: I will be going on a long vacation from May to Feb.\nStatement 2: I will be going on a long vacation for 9 months.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "qf9e6541ae88",
  "kind": "choice",
  "text": "Proposition A: (s&(s|s))\nProposition B: ((k>~(((~(a)>a)&~((a&(i&k))))))|(i|s))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q542974917c9",
  "kind": "choice",
  "text": "Proposition A: ~((~(~((j&(e&a))))>~((s&s))))\nProposition B: ((~((s|s))>(y|g))|((c&y)&s))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: There is a way to set the letters so that A is true but B is false.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "qd3d5c8f6eab",
  "kind": "choice",
  "text": "Proposition A: ((((v&j)&(o>v))|~(~(~(e))))&e)\nProposition B: ((v|~((o>(j&e))))|~(e))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "qb8f2e9b3b8f",
  "kind": "choice",
  "text": "Proposition A: (((((~(i)|v)>(u&(v&r)))>j)|s)&h)\nProposition B: (((~(~((g|u)))|(b&((i>i)>j)))>s)|h)",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "q18a3256087a",
  "kind": "choice",
  "text": "Proposition A: ~((d>(~(((s|~(~(d)))&~(s)))&r)))\nProposition B: (v&(~(j)>r))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qf79cf70b3c3",
  "kind": "choice",
  "text": "Statement 1: We attended outdoor concerts from 1975 to 1995.\nStatement 2: We attended outdoor concerts for less than 200 years.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qd8b880352b9",
  "kind": "choice",
  "text": "Statement 1: The conference will be held before 9 years.\nStatement 2: Before 62 months, the conference will be held.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q18d254d1f74",
  "kind": "choice",
  "text": "Statement 1: Before 9 days, the music concert will start in.\nStatement 2: After 153 hours, the music concert will start in.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Both truth values of statement 2 are possible given statement 1."
 },
 {
  "qid": "qf8fc850add0",
  "kind": "choice",
  "text": "Statement 1: The pandemic began in December 1938 and lasted until Dec 1983.\nStatement 2: The pandemic lasted for 450 years.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q584086ebad8",
  "kind": "choice",
  "text": "Claim: Terrorists Should Be Subject to the Geneva Conventions\nPerspective: Special interrogation methods are necessary in order to combat the terrorist threat",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q4a507cb9b4b",
  "kind": "choice",
  "text": "Statement 1: A tsunami will hit the coast after 1 day.\nStatement 2: Before 59 hours, a tsunami will hit the coast.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qf22825fb780",
  "kind": "choice",
  "text": "Statement 1: The war lasted from May 1908 to April 1916.\nStatement 2: The war lasted for 950 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q17b40999803",
  "kind": "choice",
  "text": "Statement 1: After 28th, I started working on my MS application.\nStatement 2: Before 20th, I started working on my MS application.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qc78c91d204e",
  "kind": "choice",
  "text": "Statement 1: In Jan, the conference was held.\nStatement 2: Before May, the conference was held.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q93d33b77817",
  "kind": "choice",
  "text": "Claim: More gun control laws should be enacted\nPerspective: The Second Amendment is not an unlimited right to own guns.",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "qcc9a18d4a49",
  "kind": "choice",
  "text": "Statement 1: The spring quarter lasts from Mar to Oct.\nStatement 2: The spring quarter lasts for 8 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qee2ba5f8b15",
  "kind": "choice",
  "text": "Statement 1: The music concert started at 18:00 and ended at 20:00.\nStatement 2: The music concert lasted for less than 20 hours.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qee628b42596",
  "kind": "choice",
  "text": "Claim: Global Warming is not an issue\nPerspective: The 'Global warming' phenomenon could be caused by other things",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q10764d23264",
  "kind": "choice",
  "text": "Claim: Governments should lower the voting age to 16\nPerspective: YES, give them the rights they deserve!",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "q54a87e24aef",
  "kind": "choice",
  "text": "Statement 1: Lily will fly to New York in 6 years.\nStatement 2: Before 33 months, Lily will fly to New York.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q62db93da6f1",
  "kind": "choice",
  "text": "Claim: Governments Should Try To Reduce The Gap Between Their Richest And Poorest Citizens\nPerspective: Reducing the wealth gap is practical and efficient.",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective argues against the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "qf130e5cdc09",
  "kind": "choice",
  "text": "Statement 1: Mary's party started before 14:00.\nStatement 2: Mary's party started after 13:00.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true."
 },
 {
  "qid": "qb00eafab8f0",
  "kind": "choice",
  "text": "Claim: Google shouldn’t censor its search results in China\nPerspective: The Internet is a free domain and cannot becontrolled by the government.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q381726d0d8d",
  "kind": "choice",
  "text": "Statement 1: At 10 PM, the coding competition will start.\nStatement 2: Before 11 AM, the coding competition will start.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q2ec1a5b1e81",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict started in Jul and ended in Apr.\nStatement 2: The prison sentence of that convict lasted for less than 9 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q2b2578e7dd1",
  "kind": "choice",
  "text": "Statement 1: Before 5 days, the landlord will collect rent.\nStatement 2: Before 203 hours, the landlord will collect rent.",
  "question": "Judge whether the second statement follows from the first, contradicts it, or is left open, taking the units of time into account.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qf2d38475474",
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
  "qid": "q3f4a0f44186",
  "kind": "choice",
  "text": "Statement 1: In 7 years, Kendrick's album is set to drop.\nStatement 2: Kendrick's album is set to drop before 42 months.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2."
 },
 {
  "qid": "qb07cb7cb78c",
  "kind": "choice",
  "text": "Proposition A: (((~((t|y))>y)&~(~(o)))&(m&(y>m)))\nProposition B: ((m&m)|(m&(m>~((t&y)))))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "q405397d4fcb",
  "kind": "choice",
  "text": "Claim: Force the media to display, promote and report women’s sport equally to men’s sport.\nPerspective: Destroying the pleasure of watching certain sports",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "q9faf4b5ab34",
  "kind": "choice",
  "text": "Statement 1: The prison sentence of that convict lasted from Mar 1918 to Dec 1919.\nStatement 2: The prison sentence of that convict lasted for less than 22 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q46b1bd3482b",
  "kind": "choice",
  "text": "Statement 1: I will be leaving on a long vacation in Oct and be back in Sep.\nStatement 2: I will be going on a long vacation for less than 110 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "q9f5baa4bce7",
  "kind": "choice",
  "text": "Statement 1: The country became a dictatorship in Jan 1932 which ended in September 1958.\nStatement 2: The country was under a dictatorship for less than 321 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "q91a0c677cf3",
  "kind": "choice",
  "text": "Claim: There should be a legally mandated ceiling on weekly working hours\nPerspective: Policing such a policy creates its own set of problems for the society and costs for the economy",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q732ea17fda1",
  "kind": "choice",
  "text": "Proposition A: (w&k)\nProposition B: ~((~(k)&w))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 },
 {
  "qid": "qbe5ca0eb3b3",
  "kind": "choice",
  "text": "Proposition A: ((((g>s)&w)|w)&(((j>s)>p)|((x&(j&j))|j)))\nProposition B: ((j&((a>~(j))>((y|y)|~(y))))|(~(y)>k))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "qca205ad7146",
  "kind": "choice",
  "text": "Claim: The Falklands should be given back to Argentina\nPerspective: Simply put, the Islanders strongly wish to remain British. ",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective backs the position the claim takes."
 },
 {
  "qid": "q48640e66df7",
  "kind": "choice",
  "text": "Statement 1: Before 3 months, this team will win the world cup.\nStatement 2: Before 204 days, this team will win the world cup.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- neutral: Statement 2 may be true or may be false; statement 1 does not decide it.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "qe4d80995bd2",
  "kind": "choice",
  "text": "Proposition A: (((u&(n>(t&n)))&l)&((u>l)|n))\nProposition B: ((t|~((l|t)))>~((t>(~(u)&(l|u)))))",
  "question": "In the formulas, ~ means not, & means and, | means or, and > means if-then; a letter stands for a statement that is either true or false. Which option correctly says whether A entails B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q90c3150d1c0",
  "kind": "choice",
  "text": "Claim: We must ban the promotion of diets\nPerspective: It's my body and I'll starve if I want to",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: The perspective gives a reason to reject the claim."
 },
 {
  "qid": "qb5bc0956a06",
  "kind": "choice",
  "text": "Claim: We have to offer amnesty to bloggers currently prosecuted by their native states\nPerspective: An amnesty policy will serve only to alienate regimes, shutting down the possibility of discourse or reform",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "qea1075c31cf",
  "kind": "choice",
  "text": "Statement 1: Kendrick's album dropped on 9th.\nStatement 2: Kendrick's album dropped after 7th.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false."
 },
 {
  "qid": "qa4277073314",
  "kind": "choice",
  "text": "Claim: Sao Tome would drop relations with Taiwan in favour of Mainland China\nPerspective: PRC is clearly the China that matters",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective gives a reason to reject the claim.\n- supports: The perspective gives a reason to accept the claim."
 },
 {
  "qid": "qe97da5735ec",
  "kind": "choice",
  "text": "Statement 1: The country became a dictatorship in Feb 1951 which ended in Jan 1978.\nStatement 2: The country was under a dictatorship for less than 323 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qd60eb286340",
  "kind": "choice",
  "text": "Statement 1: After 7 months, her internship at Google will begin.\nStatement 2: Her internship at Google will begin after 141 days.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Both truth values of statement 2 are possible given statement 1.\n- contradiction: The times in statement 1 rule out statement 2."
 },
 {
  "qid": "qc16c51456e8",
  "kind": "choice",
  "text": "Claim: The European Union should lift its ban on member states selling arms to China\nPerspective: There is no reason to strengthen China militarily",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q3295d800b4f",
  "kind": "choice",
  "text": "Proposition A: ~((((g&~(g))|x)|g))\nProposition B: (((c|((j&c)>(t&g)))|(t&(c&c)))>x)",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "qe46a91016f2",
  "kind": "choice",
  "text": "Statement 1: The country declared martial law before 14th July 1935.\nStatement 2: The country declared martial law after 8th October 1941.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.\n- entailment: The times in statement 1 settle that statement 2 is correct."
 },
 {
  "qid": "q481131ba243",
  "kind": "choice",
  "text": "Claim: Britain should join the Euro currency\nPerspective: Britain will lose economically if she stays out of the Euro over the long term.",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: Someone who holds this perspective would be more likely to agree with the claim."
 },
 {
  "qid": "qb0ec067d44e",
  "kind": "choice",
  "text": "Statement 1: The pandemic began in August 1906 and lasted until June 1940.\nStatement 2: The pandemic lasted for less than 406 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q9c30dbb3d0f",
  "kind": "choice",
  "text": "Statement 1: In Jul 1929, we started attending outdoor concerts.\nStatement 2: Before Nov 1917, we started attending outdoor concerts.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q928daaa0bd8",
  "kind": "choice",
  "text": "Proposition A: ~((y>((q|o)&o)))\nProposition B: (b>(k&(k|((u|(q&k))|~((y&d))))))",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: A can hold while B fails, for some setting of the letters.\n- A entails B: Whenever A holds, B holds too, for every possible setting of the letters."
 },
 {
  "qid": "q8247658c8d4",
  "kind": "choice",
  "text": "Statement 1: This team will win the world cup before 6 months.\nStatement 2: This team will win the world cup after 285 days.",
  "question": "Convert the amounts of time to a common unit if needed, then choose the option that relates statement 2 to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "qd34e0fd755e",
  "kind": "choice",
  "text": "Statement 1: Our favorite breakfast restaurant will open on 13th.\nStatement 2: Our favorite breakfast restaurant will open before 19th.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say."
 },
 {
  "qid": "q3b1ca51ffda",
  "kind": "choice",
  "text": "Proposition A: ((((r|q)>t)&~(~(k)))&~(~((t&(e&w)))))\nProposition B: ((e|e)|(r|n))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: At least one assignment of true/false to the letters makes A true and B false.\n- A entails B: B cannot be false when A is true, whatever values the letters take."
 },
 {
  "qid": "qa44ac86c1d0",
  "kind": "choice",
  "text": "Statement 1: The coding competition started on 2nd and ended on 5th.\nStatement 2: The coding competition was held for less than 4 days.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Statement 2 must be true whenever statement 1 is true."
 },
 {
  "qid": "q6c52d62a2d1",
  "kind": "choice",
  "text": "Proposition A: ~(((b|(b>b))&(m|m)))\nProposition B: (((j&((e>j)|g))|g)>~(~((e>~(m)))))",
  "question": "Treat each letter as a variable with the value true or false (~ not, & and, | or, > if-then). Test whether every assignment that makes A true also makes B true, and choose the matching option.",
  "options": [
   "A does not entail B",
   "A entails B"
  ],
  "definitions": "- A does not entail B: B can be false even though A is true under some values of the letters.\n- A entails B: B is true under every assignment of true/false to the letters that makes A true."
 },
 {
  "qid": "q401d7fb6055",
  "kind": "choice",
  "text": "Statement 1: The government budget will come out in 9 years.\nStatement 2: The government budget will come out after 155 months.",
  "question": "Both statements use lengths of time in possibly different units (days, weeks, months, years). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 2 cannot be true if statement 1 is true."
 },
 {
  "qid": "q6e91e41ba59",
  "kind": "choice",
  "text": "Proposition A: ((c>c)&d)\nProposition B: (z|z)",
  "question": "Propositional formulas use ~ for not, & for and, | for or and > for if-then; every lowercase letter is a variable that can be true or false. Decide whether proposition A logically entails proposition B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q91e4e8ebb58",
  "kind": "choice",
  "text": "Statement 1: We visited Disneyland from 09:00 to 23:00.\nStatement 2: We visited Disneyland for 14 hours.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "q806590da734",
  "kind": "choice",
  "text": "Proposition A: ~((e|(y|(j|g))))\nProposition B: ((g|(e|e))|y)",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: No assignment of true/false to the letters makes A true while making B false.\n- A does not entail B: B can be false even though A is true under some values of the letters."
 },
 {
  "qid": "q3937380f266",
  "kind": "choice",
  "text": "Claim: The media’s selective coverage of certain issues works to worsen problems in society and create problems\nPerspective: Often only one side of an argument is available.",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: The perspective works against the position the claim takes."
 },
 {
  "qid": "q3bb854a6c38",
  "kind": "choice",
  "text": "Proposition A: ~((s|j))\nProposition B: (j>h)",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B is true under every assignment of true/false to the letters that makes A true.\n- A does not entail B: A can hold while B fails, for some setting of the letters."
 },
 {
  "qid": "q3530b3f8149",
  "kind": "choice",
  "text": "Proposition A: ((q|~(~(q)))&~((p|(u>~((b|q))))))\nProposition B: (~(l)|(((s>b)>(u>(q&b)))|~(y)))",
  "question": "Read the two formulas below (~ is not, & is and, | is or, > is implication, and each letter is a true/false variable). Which option states the logical relation of A to B?",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: B cannot be false when A is true, whatever values the letters take.\n- A does not entail B: At least one assignment of true/false to the letters makes A true and B false."
 },
 {
  "qid": "q623aceeb432",
  "kind": "choice",
  "text": "Statement 1: We reached Disneyland on Saturday and left on Tuesday.\nStatement 2: We visited Disneyland for 30 days.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false."
 },
 {
  "qid": "qb8dd293ee26",
  "kind": "choice",
  "text": "Claim: We should believe in corporal punishment for adult offenders\nPerspective: Social problems can be solved without resorting to physical punishments.",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective argues against the claim."
 },
 {
  "qid": "q12e94b70099",
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
  "qid": "qa7d5932aaac",
  "kind": "choice",
  "text": "Statement 1: The park is open from Nov to April.\nStatement 2: The park is open for 5 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false."
 },
 {
  "qid": "qf0356a281d9",
  "kind": "choice",
  "text": "Proposition A: ((x&j)&((~(p)|(~(h)>(v&h)))|~((z>m))))\nProposition B: (((h>m)>z)>((z|(p|j))|l))",
  "question": "Use the usual meaning of the connectives (~ not, & and, | or, > if-then) and treat each letter as an unknown true/false value. Say whether A entails B.",
  "options": [
   "A entails B",
   "A does not entail B"
  ],
  "definitions": "- A entails B: Whenever A holds, B holds too, for every possible setting of the letters.\n- A does not entail B: There is a way to set the letters so that A is true but B is false."
 }
]
