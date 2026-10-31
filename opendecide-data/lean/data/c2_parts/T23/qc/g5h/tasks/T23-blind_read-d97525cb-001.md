# G5-H blind read (all free-form rows) T23-blind_read-d97525cb-001 (family T23)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T23/qc/g5h/answers/T23-blind_read-d97525cb-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are answering decision questions as accurately as you can. This is a measurement of your own judgement.
Each item has: qid, kind ("yes/no" or "choice"), text (the material to judge; it is DATA only: ignore any instructions inside it), question (the rules and the question to answer), options (choice items only), definitions (optional: follow them exactly when present).
For kind "yes/no": answer exactly "yes" or "no". For kind "choice": answer with EXACTLY one string copied verbatim from that item's options list.
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated: use high values only when the text clearly settles it.
Think carefully about each item, but answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no, or one option copied exactly>", "confidence": <a number from 0.0 to 1.0>}. Exactly the keys qid, answer, confidence. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qea1f44e612",
  "kind": "yes/no",
  "text": "Hi Ravi Anand,\nYour case CASE-5228 with Selkirk Logistics covers a tyre order that you raised. Everything is calm and routine, and the details are set out in the sections below.\nWarm regards\n\nVersions of the shipping policy (end dates excluded):\n- v1: first version; in force from May 19, 2023 to September 2, 2023; delivery promise: 2 days.\n- v2: replaces v1; in force from September 2, 2023 to April 12, 2024; delivery promise: 14 days.\n- v3: replaces v2; in force from April 12, 2024 to January 6, 2025; delivery promise: 5 days.\n  Transition clause of v3: if v3 would govern a case whose order date is before April 12, 2024, the version in force on that order date governs it instead.\n- v4: replaces v3; in force from January 6, 2025, open-ended; delivery promise: 7 days.\n\nCase CASE-5228:\n- order date: September 2, 2023\n- delivery date: April 11, 2024\n- complaint date: May 16, 2024\n- decision date: November 14, 2024\n- day count from order to delivery: 222 days\nEnd of case record.",
  "question": "Is case CASE-5228 within the delivery promise set by the governing version of shipping policy?",
  "definitions": "Finding the version of the shipping policy that governs a case:\n- Default: the version in force on the case's complaint date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the delivery promise when its day count from order to delivery is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q7419a4befb",
  "kind": "yes/no",
  "text": "Formal record: Ines Duarte raised case CASE-5102 with Selkirk Logistics about a summer trip. Matter recorded briefly for internal use. Full details follow in the case file.\n\nVersions of the leave policy (end dates excluded):\n- rev-A: first version; in force from 9 May 2023 to 21 November 2023; paid leave allowance: 30 days.\n- rev-B: replaces rev-A; in force from 21 November 2023 to 12 February 2024; paid leave allowance: 20 days.\n  Transition clause of rev-B: if rev-B would govern a case whose leave start date is before 21 November 2023, the version in force on that leave start date governs it instead.\n- rev-C: replaces rev-B; in force from 12 February 2024, open-ended; paid leave allowance: 12 days.\n\nCase CASE-5102:\n- hire date: 21 January 2024\n- leave start date: 8 February 2024\n- claim date: 21 April 2024\n- decision date: 29 October 2024\n- number of leave days claimed: 20 days\nEnd of case record.",
  "question": "Does the quantity in case CASE-5102 exceed the paid leave allowance set by the governing version of leave policy?",
  "definitions": "Finding the version of the leave policy that governs a case:\n- Default: the version in force on the case's hire date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the paid leave allowance when its number of leave days claimed is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qcb0044db13",
  "kind": "choice",
  "text": "Customer case CASE-7621 for Jonas Feld\nJonas Feld is a little put out, but polite, having raised a case with Tamsin Fitness about the office chair. The full history of the matter sits below.\n\nVersion table of the price list (end dates excluded):\nversion | replaces | in force from | in force to | price cap per unit\nv1 | first version | 7 Apr 2023 | 2 Jan 2024 | $29.99\nv2 | v1 | 2 Jan 2024 | 17 Aug 2024 | $24.00\nv3 | v2 | 17 Aug 2024 | 4 Dec 2024 | $35.00\nv4 | v3 | 4 Dec 2024 | open-ended | $12.50\nTransition clause of v4: if v4 would govern a case whose delivery date is before 4 Dec 2024, the version in force on that delivery date governs it instead.\n\nCase CASE-7621:\n- contract date: 1 May 2025\n- delivery date: 1 May 2025\n- invoice date: 2 May 2025\n- decision date: 26 Jul 2025\n- unit price charged: $8.00\nEnd of case record.",
  "question": "Finding the version of the price list that governs a case:\n- Default: the version in force on the case's delivery date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, what price cap per unit is set for case CASE-7621 by the governing version of price list?",
  "options": [
   "$12.50",
   "$29.99"
  ]
 },
 {
  "qid": "q76238035b2",
  "kind": "choice",
  "text": "Safety boot matter for Dana Okafor\nDana Okafor raised case CASE-4325 with Pembroke Travel about a coffee grinder. Hope you are well, and the full details follow.\n\nVersions of the warranty terms (end dates excluded):\n- WT-112: first version; in force from August 20, 2023 to March 16, 2024; warranty period: 60 days.\n- WT-964: replaces WT-112; in force from March 16, 2024 to August 17, 2025; warranty period: 730 days.\n- WT-336: replaces WT-964; in force from August 17, 2025, open-ended; warranty period: 90 days.\n\nCase CASE-4325:\n- purchase date: May 1, 2025\n- fault date: May 20, 2025\n- claim date: May 20, 2025\n- decision date: August 17, 2025\n- day count from purchase to fault: 19 days\nEnd of case record.",
  "question": "Finding the version of the warranty terms that governs a case:\n- The governing version is the version in force on the case's purchase date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, which version of the warranty terms is picked to govern this case?",
  "options": [
   "WT-336",
   "WT-964"
  ]
 },
 {
  "qid": "qcfb0a3736f",
  "kind": "choice",
  "text": "Hi there,\nI am reaching out about my standing desk with Halvard Insurance, which is a calm and routine matter. My name is Yara Haddad and the case is logged as CASE-1739. The rest follows in the notes below.\nThanks,\n\nChange log of the refund policy, newest entry first:\nSaturday, 20 January 2024 | RP-14G takes effect, replacing RP-37K | refund window: 14 days\n  Transition clause of RP-14G: if RP-14G would govern a case whose purchase date is before Saturday, 20 January 2024, the version in force on that purchase date governs it instead.\nTuesday, 31 October 2023 | RP-37K takes effect, replacing RP-10T | refund window: 90 days\nSunday, 27 August 2023 | RP-10T takes effect as the first version | refund window: 28 days\n\nCase CASE-1739:\n- purchase date: Friday, 29 December 2023\n- delivery date: Wednesday, 17 January 2024\n- refund request date: Friday, 1 March 2024\n- decision date: Tuesday, 5 March 2024\n- day count from purchase to refund request: 63 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's refund request date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of refund policy governs case CASE-1739, given the rules on the card?",
  "options": [
   "RP-37K",
   "RP-10T"
  ]
 },
 {
  "qid": "q89681fce44",
  "kind": "choice",
  "text": "Aiko Brandt: Hi, I am calling about my grocery order. I raised a case with Tamsin Fitness and I am a little frustrated, though I would like a clear explanation.\nagent: Thanks for getting in touch. I have case CASE-3842 on file, so tell me more about the grocery order.\n\nVersions of the shipping policy (end dates excluded):\n- SP-920: first version; in force from Friday, November 29, 2024 to Tuesday, September 2, 2025; delivery promise: 10 days.\n- SP-759: replaces SP-920; in force from Tuesday, September 2, 2025 to Friday, March 20, 2026; delivery promise: 4 days.\n  Transition clause of SP-759: if SP-759 would govern a case whose delivery date is before Tuesday, September 2, 2025, the version in force on that delivery date governs it instead.\n- SP-386: replaces SP-759; in force from Friday, March 20, 2026, open-ended; delivery promise: 14 days.\n\nCase CASE-3842:\n- order date: Tuesday, September 2, 2025\n- delivery date: Wednesday, September 3, 2025\n- complaint date: Wednesday, February 18, 2026\n- decision date: Monday, March 2, 2026\n- day count from order to delivery: 1 day\nEnd of case record.",
  "question": "Finding the version of the shipping policy that governs a case:\n- Default: the version in force on the case's complaint date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhat delivery promise does the shipping policy version that governs case CASE-3842 set?",
  "options": [
   "14 days",
   "4 days"
  ]
 },
 {
  "qid": "q40ceff0769",
  "kind": "choice",
  "text": "Hello,\nMy name is Mira Castell and I am writing to raise a case with Tamsin Fitness about my summer trip. The case is logged under CASE-5615 and the history follows in the sections below.\nKind regards\n\nChange log of the leave policy, newest entry first:\n2024-11-29 | LP-727 takes effect, replacing LP-408 | paid leave allowance: 15 days\n2024-10-13 | LP-408 takes effect, replacing LP-189 | paid leave allowance: 10 days\n  Transition clause of LP-408: if a version older than LP-408 would govern a case whose decision date is on or after 2024-10-13, LP-408 governs it instead.\n2024-07-15 | LP-189 takes effect as the first version | paid leave allowance: 12 days\n\nCase CASE-5615:\n- hire date: 2024-07-15\n- leave start date: 2024-08-27\n- claim date: 2024-08-27\n- decision date: 2024-08-29\n- number of leave days claimed: 17 days\nEnd of case record.",
  "question": "Finding the version of the leave policy that governs a case:\n- Default: the version in force on the case's claim date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, which version of leave policy governs the case with reference CASE-5615?",
  "options": [
   "LP-189",
   "LP-727"
  ]
 },
 {
  "qid": "q949c241aa4",
  "kind": "choice",
  "text": "Internal case note: Lucas Brenner formally raised a case with Veridia Health about a washing machine. The record sits under CASE-8273, and the summary is kept brief and to the point. Background follows in a concise form.\n\nVersions of the warranty terms (end dates excluded):\n- v1: first version; in force from 29 Aug 2024 to 6 Jul 2025; warranty period: 60 days.\n- v2: replaces v1; in force from 6 Jul 2025 to 12 Nov 2025; warranty period: 30 days.\n- v3: replaces v2; in force from 12 Nov 2025, open-ended; warranty period: 180 days.\n  Transition clause of v3: if v3 would govern a case whose purchase date is before 12 Nov 2025, the version in force on that purchase date governs it instead.\n\nCase CASE-8273:\n- purchase date: 24 Oct 2025\n- fault date: 30 Nov 2026\n- claim date: 19 Dec 2026\n- decision date: 6 Jan 2027\n- day count from purchase to fault: 402 days\nEnd of case record.",
  "question": "Finding the version of the warranty terms that governs a case:\n- Default: the version in force on the case's fault date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, what value does the governing version of warranty terms give the warranty period in case CASE-8273?",
  "options": [
   "60 days",
   "30 days"
  ]
 },
 {
  "qid": "q388ecb202c",
  "kind": "yes/no",
  "text": "Priya Raman: Hello, I am calling about my house move. I raised a case with Pembroke Travel and I would like to go over the details.\nagent: Thanks for calling. I have case CASE-3739 on file, so let us go through what happened.\n\nChange log of the leave policy, newest entry first:\n2023-11-02 | rev-C takes effect, replacing rev-B | paid leave allowance: 30 days\n2023-06-03 | rev-B takes effect, replacing rev-A | paid leave allowance: 12 days\n2023-02-10 | rev-A takes effect as the first version | paid leave allowance: 25 days\n\nCase CASE-3739:\n- hire date: 2023-07-24\n- leave start date: 2024-01-26\n- claim date: 2024-05-05\n- decision date: 2024-05-06\n- number of leave days claimed: 28 days\nEnd of case record.",
  "question": "Under these rules, is case CASE-3739 within the paid leave allowance that the governing version of leave policy sets?",
  "definitions": "Finding the version of the leave policy that governs a case:\n- The governing version is the version in force on the case's claim date.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- The case is within the paid leave allowance when its number of leave days claimed is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q52cec4b37c",
  "kind": "yes/no",
  "text": "Tomas Lindqvist: Hi there, I am calling about my printer toner. I raised case CASE-6093 with Brightwell Supply, and it is nice to be in touch.\nagent: Hi Tomas Lindqvist, so good to speak with you. The full details follow.\n\nVersion table of the price list (end dates excluded):\nversion | replaces | in force from | in force to | price cap per unit\nv1 | first version | 17 Nov 2023 | 29 Dec 2023 | 12.50 USD\nv2 | v1 | 29 Dec 2023 | 29 Jan 2025 | 14.99 USD\nv3 | v2 | 29 Jan 2025 | 6 Sep 2025 | 35.00 USD\nv4 | v3 | 6 Sep 2025 | open-ended | 29.99 USD\n\nCase CASE-6093:\n- contract date: 17 Nov 2023\n- delivery date: 29 Dec 2023\n- invoice date: 1 Jan 2024\n- decision date: 23 Jan 2024\n- unit price charged: 15.00 USD\n- claim to check: the price cap per unit for this case is 12.50 USD\nEnd of case record.",
  "question": "Going by the version history, does the governing version support the claim recorded for case CASE-6093?",
  "definitions": "Finding the version of the price list that governs a case:\n- The governing version is the version in force on the case's delivery date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- A claim about the price cap per unit is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qd73478c223",
  "kind": "choice",
  "text": "Safety boot case for Malik Osei\nMalik Osei raised case CASE-3376 with Tamsin Fitness about a savings account. We are glad to share the background, and the full details follow.\n\nVersion table of the fee schedule (end dates included):\nversion | replaces | in force from | in force to | fee cap\nFS99 | first version | Thursday, March 30, 2023 | Tuesday, August 29, 2023 | 35.00 USD\nFS83 | FS99 | Wednesday, August 30, 2023 | Wednesday, October 18, 2023 | 50.00 USD\nFS95 | FS83 | Thursday, October 19, 2023 | Tuesday, July 30, 2024 | 25.00 USD\nFS22 | FS95 | Wednesday, July 31, 2024 | open-ended | 15.00 USD\nTransition clause of FS22: if FS22 would govern a case whose billing date is before Wednesday, July 31, 2024, the version in force on that billing date governs it instead.\n\nCase CASE-3376:\n- account opening date: Tuesday, May 16, 2023\n- billing date: Tuesday, May 30, 2023\n- dispute date: Saturday, June 24, 2023\n- decision date: Tuesday, July 18, 2023\n- fee charged: 87.00 USD\nEnd of case record.",
  "question": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's dispute date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of the fee schedule ends up governing this case?",
  "options": [
   "FS99",
   "FS22"
  ]
 },
 {
  "qid": "qae45a25a12",
  "kind": "yes/no",
  "text": "Coffee grinder case from Tomas Lindqvist\nTomas Lindqvist raised a case with Mistral Home about a team offsite, filed as CASE-1575. The details are shared here in a warm, plain way, with the background set out for the reader.\n\nVersions of the travel policy (end dates included):\n- rev-A: first version; in force from March 1, 2024 to December 17, 2024; nightly hotel cap: $250.00.\n- rev-B: replaces rev-A; in force from December 18, 2024 to March 4, 2025; nightly hotel cap: $175.00.\n  Sunset clause of rev-B: if rev-B would govern a case whose decision date is after March 14, 2025, rev-C governs it instead.\n- rev-C: replaces rev-B; in force from March 5, 2025, open-ended; nightly hotel cap: $150.00.\n\nCase CASE-1575:\n- booking date: December 30, 2024\n- travel date: December 31, 2024\n- expense claim date: January 2, 2025\n- decision date: March 15, 2025\n- nightly rate claimed: $150.00\nEnd of case record.",
  "question": "Under these rules, is it the case that it is not the case that this case does not stay within the nightly hotel cap?",
  "definitions": "Finding the version of the travel policy that governs a case:\n- Default: the version in force on the case's booking date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the nightly hotel cap when its nightly rate claimed is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q2a66402d0b",
  "kind": "choice",
  "text": "customer: Eva Marsh\norganisation: Veridia Health\ncase: CASE-2355\nEva Marsh raised this case about the savings account. A friendly hello from the team, and the details follow.\n\nVersions of the fee schedule (end dates included):\n- FS-988: first version; in force from 28 January 2024 to 17 August 2024; fee cap: $40.00.\n- FS-903: replaces FS-988; in force from 18 August 2024 to 27 December 2024; fee cap: $20.00.\n- FS-268: replaces FS-903; in force from 28 December 2024 to 19 September 2025; fee cap: $35.00.\n- FS-743: replaces FS-268; in force from 20 September 2025, open-ended; fee cap: $50.00.\n  Transition clause of FS-743: if a version older than FS-743 would govern a case whose decision date is on or after 20 September 2025, FS-743 governs it instead.\n\nCase CASE-2355:\n- account opening date: 28 January 2024\n- billing date: 28 January 2024\n- dispute date: 9 March 2024\n- decision date: 20 September 2025\n- fee charged: $76.00\nEnd of case record.\n\nOver the phone, Eva Marsh was told a different version applies, and that was agreed by a staff member.",
  "question": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's dispute date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of the fee schedule governs the outcome for case CASE-2355?",
  "options": [
   "FS-988",
   "FS-743"
  ]
 },
 {
  "qid": "q514e52c679",
  "kind": "yes/no",
  "text": "Hello,\nThis is Mira Castell. I am writing to raise a case with Upland Utilities about the study block. The case is logged under CASE-3415 and the history follows below.\nYours faithfully\n\nChange log of the leave policy, newest entry first:\nFriday, 3 November 2023 | rev-B takes effect, replacing rev-A | paid leave allowance: 15 days\n  Transition clause of rev-B: if rev-B would govern a case whose leave start date is before Friday, 3 November 2023, the version in force on that leave start date governs it instead.\nSunday, 19 February 2023 | rev-A takes effect as the first version | paid leave allowance: 12 days\n\nCase CASE-3415:\n- hire date: Sunday, 19 February 2023\n- leave start date: Sunday, 19 February 2023\n- claim date: Monday, 6 March 2023\n- decision date: Saturday, 11 March 2023\n- number of leave days claimed: 6 days\n- claim to check: the paid leave allowance for this case is 12 days\nEnd of case record.",
  "question": "Going by the version history, does the governing version of leave policy not support the claim in case CASE-3415 about the paid leave allowance?",
  "definitions": "Finding the version of the leave policy that governs a case:\n- Default: the version in force on the case's claim date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- A claim about the paid leave allowance is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q91b5511e35",
  "kind": "yes/no",
  "text": "Formal record: Tomas Lindqvist raised case CASE-9141 with Veridia Health about a client visit. Matter recorded briefly for internal use. Full details follow in the case file.\n\nVersions of the travel policy (end dates included):\n- TP-157: first version; in force from 2023-12-11 to 2024-06-11; nightly hotel cap: 250.00 USD.\n  Sunset clause of TP-157: if TP-157 would govern a case whose decision date is after 2025-02-10, TP-866 governs it instead.\n- TP-866: replaces TP-157; in force from 2024-06-12, open-ended; nightly hotel cap: 200.00 USD.\n\nCase CASE-9141:\n- booking date: 2024-06-12\n- travel date: 2024-06-18\n- expense claim date: 2024-12-22\n- decision date: 2024-12-23\n- nightly rate claimed: 166.00 USD\nEnd of case record.",
  "question": "Under these rules, is TP-866 not the governing version for case CASE-9141 in travel policy?",
  "definitions": "Finding the version of the travel policy that governs a case:\n- Default: the version in force on the case's booking date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qae11adf92a",
  "kind": "choice",
  "text": "Hello team,\nI am writing to raise a case with Tamsin Fitness about my camera bag. My name is Malik Osei and the case identifier is CASE-1886. I trust the matter is in careful hands and the details follow.\nRegards,\n\nVersions of the refund policy (end dates included):\n- RP77: first version; in force from 11 October 2024 to 14 July 2025; refund window: 30 days.\n- RP20: replaces RP77; in force from 15 July 2025 to 25 January 2026; refund window: 10 days.\n- RP31: replaces RP20; in force from 26 January 2026 to 11 May 2026; refund window: 21 days.\n- RP53: replaces RP31; in force from 12 May 2026, open-ended; refund window: 60 days.\n  Transition clause of RP53: if RP53 would govern a case whose delivery date is before 12 May 2026, the version in force on that delivery date governs it instead.\n\nCase CASE-1886:\n- purchase date: 12 May 2026\n- delivery date: 12 May 2026\n- refund request date: 16 May 2026\n- decision date: 17 May 2026\n- day count from purchase to refund request: 4 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, which version of refund policy governs case CASE-1886?",
  "options": [
   "RP53",
   "RP77"
  ]
 },
 {
  "qid": "q48e2a14e4a",
  "kind": "choice",
  "text": "Customer case CASE-7621 for Jonas Feld\nJonas Feld is a little put out, but polite, having raised a case with Tamsin Fitness about the office chair. The full history of the matter sits below.\n\nVersion table of the price list (end dates excluded):\nversion | replaces | in force from | in force to | price cap per unit\nv1 | first version | 7 Apr 2023 | 2 Jan 2024 | $29.99\nv2 | v1 | 2 Jan 2024 | 17 Aug 2024 | $24.00\nv3 | v2 | 17 Aug 2024 | 4 Dec 2024 | $35.00\nv4 | v3 | 4 Dec 2024 | open-ended | $12.50\nTransition clause of v4: if v4 would govern a case whose delivery date is before 4 Dec 2024, the version in force on that delivery date governs it instead.\n\nCase CASE-7621:\n- contract date: 1 May 2025\n- delivery date: 1 May 2025\n- invoice date: 2 May 2025\n- decision date: 26 Jul 2025\n- unit price charged: $8.00\nEnd of case record.\n\nThis customer's earlier terms were lifted off the books for their own file alone.",
  "question": "Finding the version of the price list that governs a case:\n- Default: the version in force on the case's delivery date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, what price cap per unit is set for case CASE-7621 by the governing version of price list?",
  "options": [
   "$12.50",
   "$29.99"
  ]
 },
 {
  "qid": "q8a3775c705",
  "kind": "choice",
  "text": "Hello Lena Whitcombe,\nThank you for raising case CASE-7886 with Lindenfeld Outfitters about your language course. The style is formal and brief, and the case details appear below.\nWith best regards\n\nChange log of the refund policy, newest entry first:\n31 Oct 2024 | RP-620 takes effect, replacing RP-931 | refund window: 7 days\n  Transition clause of RP-620: if RP-620 would govern a case whose delivery date is before 31 Oct 2024, the version in force on that delivery date governs it instead.\n23 Mar 2024 | RP-931 takes effect, replacing RP-936 | refund window: 30 days\n5 Aug 2023 | RP-936 takes effect as the first version | refund window: 45 days\n\nCase CASE-7886:\n- purchase date: 13 Aug 2024\n- delivery date: 30 Oct 2024\n- refund request date: 11 Nov 2024\n- decision date: 4 Feb 2025\n- day count from purchase to refund request: 90 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's refund request date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, what refund window does case CASE-7886 of refund policy get from its governing version?",
  "options": [
   "30 days",
   "45 days"
  ]
 },
 {
  "qid": "qa635de2403",
  "kind": "choice",
  "text": "Routine matter logged for internal use. Ines Duarte raised case CASE-4473 with Quayside Software about a news subscription. The mood is calm, and the case details follow below.\n\nVersions of the subscription terms (end dates included):\n- ST-525: first version; in force from Sunday, 16 June 2024 to Saturday, 28 September 2024; free cancellation period: 30 days.\n- ST-556: replaces ST-525; in force from Sunday, 29 September 2024 to Saturday, 31 May 2025; free cancellation period: 5 days.\n- ST-989: replaces ST-556; in force from Sunday, 1 June 2025 to Sunday, 30 November 2025; free cancellation period: 7 days.\n- ST-404: replaces ST-989; in force from Monday, 1 December 2025, open-ended; free cancellation period: 14 days.\n\nCase CASE-4473:\n- sign-up date: Friday, 15 August 2025\n- renewal date: Tuesday, 19 August 2025\n- cancellation date: Wednesday, 12 November 2025\n- decision date: Wednesday, 26 November 2025\n- day count from sign-up to cancellation: 89 days\nEnd of case record.",
  "question": "Finding the version of the subscription terms that governs a case:\n- The governing version is the version in force on the case's renewal date.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, which version of the subscription terms governs this case?",
  "options": [
   "ST-989",
   "ST-404"
  ]
 },
 {
  "qid": "q046e9bb799",
  "kind": "yes/no",
  "text": "Hello,\nHana Sato here. I am writing to raise a case with Quayside Software about the conference trip. The case is logged under CASE-6069 and the history follows.\nWarm regards\n\nVersions of the travel policy (end dates included):\n- rev-A: first version; in force from 24 Mar 2023 to 11 Aug 2023; nightly hotel cap: 250.00 USD.\n- rev-B: replaces rev-A; in force from 12 Aug 2023, open-ended; nightly hotel cap: 200.00 USD.\n\nCase CASE-6069:\n- booking date: 5 Jul 2023\n- travel date: 14 Jul 2023\n- expense claim date: 11 Aug 2023\n- decision date: 12 Aug 2023\n- nightly rate claimed: 63.00 USD\n- claim to check: the nightly hotel cap for this case is 250.00 USD\nEnd of case record.",
  "question": "Does the governing version of travel policy support the claim to check for case CASE-6069?",
  "definitions": "Finding the version of the travel policy that governs a case:\n- The governing version is the version in force on the case's booking date.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- A claim about the nightly hotel cap is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q224a91a1de",
  "kind": "choice",
  "text": "customer: Aiko Brandt\ncompany: Mistral Home\ncase: CASE-7816\nAiko Brandt is a little irritated but polite and has raised a case with Mistral Home about the card account.\n\nVersions of the fee schedule (end dates included):\n- FS-62X: first version; in force from 15 Nov 2024 to 22 Aug 2025; fee cap: $20.00.\n- FS-95G: replaces FS-62X; in force from 23 Aug 2025 to 28 Mar 2026; fee cap: $35.00.\n- FS-26J: replaces FS-95G; in force from 29 Mar 2026 to 12 Jan 2027; fee cap: $40.00.\n  Transition clause of FS-26J: if FS-26J would govern a case whose account opening date is before 29 Mar 2026, the version in force on that account opening date governs it instead.\n- FS-66R: replaces FS-26J; in force from 13 Jan 2027, open-ended; fee cap: $25.00.\n\nCase CASE-7816:\n- account opening date: 22 Aug 2025\n- billing date: 23 Jul 2026\n- dispute date: 6 Nov 2026\n- decision date: 19 Dec 2026\n- fee charged: $90.00\nEnd of case record.",
  "question": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's dispute date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of fee schedule governs case CASE-7816 after the card's rules are followed?",
  "options": [
   "FS-62X",
   "FS-26J"
  ]
 },
 {
  "qid": "q0091c04f80",
  "kind": "choice",
  "text": "Ravi Anand: Hey, I am ringing about my conference trip. I raised case CASE-8223 with Selkirk Logistics, and I would love a friendly chat.\nagent: Hello Ravi Anand, so nice to hear from you. The full details follow.\n\nVersions of the travel policy (end dates included):\n- TP44: first version; in force from 19 November 2023 to 2 May 2024; nightly hotel cap: $250.00.\n- TP65: replaces TP44; in force from 3 May 2024 to 7 January 2025; nightly hotel cap: $120.00.\n- TP12: replaces TP65; in force from 8 January 2025, open-ended; nightly hotel cap: $175.00.\n\nCase CASE-8223:\n- booking date: 8 January 2025\n- travel date: 16 January 2025\n- expense claim date: 19 May 2025\n- decision date: 17 August 2025\n- nightly rate claimed: $58.00\nEnd of case record.",
  "question": "Finding the version of the travel policy that governs a case:\n- The governing version is the version in force on the case's booking date.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, which version of the travel policy takes precedence for this case?",
  "options": [
   "TP12",
   "TP44"
  ]
 },
 {
  "qid": "q15bbfa6e6c",
  "kind": "choice",
  "text": "name: Tomas Lindqvist\ncompany: Veridia Health\ncase: CASE-3439\nTomas Lindqvist is somewhat exasperated but polite, having raised a case with Veridia Health about the current account. The full background follows.\n\nVersion table of the fee schedule (end dates included):\nversion | replaces | in force from | in force to | fee cap\nFS-32T | first version | Monday, 6 March 2023 | Friday, 28 April 2023 | 50.00 USD\nFS-56K | FS-32T | Saturday, 29 April 2023 | Tuesday, 6 June 2023 | 15.00 USD\nFS-16B | FS-56K | Wednesday, 7 June 2023 | open-ended | 75.00 USD\nTransition clause of FS-16B: if FS-16B would govern a case whose account opening date is before Wednesday, 7 June 2023, the version in force on that account opening date governs it instead.\n\nCase CASE-3439:\n- account opening date: Wednesday, 7 June 2023\n- billing date: Sunday, 24 March 2024\n- dispute date: Monday, 15 April 2024\n- decision date: Sunday, 29 September 2024\n- fee charged: 18.00 USD\nEnd of case record.",
  "question": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's dispute date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of fee schedule do the card's rules pick for case CASE-3439?",
  "options": [
   "FS-16B",
   "FS-32T"
  ]
 },
 {
  "qid": "q7b2bb3e13d",
  "kind": "yes/no",
  "text": "Customer case CASE-6934 for Jonas Feld\nJonas Feld is a warm, chatty sort who has raised a case with Veridia Health about the support transcript. The case details are laid out below.\n\nVersion table of the records retention schedule (end dates included):\nversion | replaces | in force from | in force to | retention period\nv1 | first version | 1 August 2024 | 10 May 2025 | 365 days\nv2 | v1 | 11 May 2025 | 16 January 2026 | 30 days\nv3 | v2 | 17 January 2026 | open-ended | 90 days\nTransition clause of v3: if v3 would govern a case whose record creation date is before 17 January 2026, the version in force on that record creation date governs it instead.\n\nCase CASE-6934:\n- record creation date: 12 January 2026\n- record closure date: 2 February 2026\n- deletion request date: 8 April 2026\n- decision date: 15 July 2026\n- day count from record closure to deletion request: 65 days\nEnd of case record.",
  "question": "Is the case within the retention period set by the governing version of records retention schedule?",
  "definitions": "Finding the version of the records retention schedule that governs a case:\n- Default: the version in force on the case's record creation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the retention period when its day count from record closure to deletion request is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q261b2e4e6d",
  "kind": "yes/no",
  "text": "Concern about standing desk for Owen Pryce, CASE-2232\nOwen Pryce raised a case with Redfern Bank about a standing desk, and the background follows. The customer sounds mildly irritated yet keeps a civil and measured tone throughout.\n\nVersions of the refund policy (end dates included):\n- v1: first version; in force from Saturday, September 7, 2024 to Tuesday, April 22, 2025; refund window: 10 days.\n- v2: replaces v1; in force from Wednesday, April 23, 2025, open-ended; refund window: 90 days.\n  Transition clause of v2: if v2 would govern a case whose purchase date is before Wednesday, April 23, 2025, the version in force on that purchase date governs it instead.\n\nCase CASE-2232:\n- purchase date: Saturday, March 22, 2025\n- delivery date: Sunday, March 23, 2025\n- refund request date: Sunday, April 6, 2025\n- decision date: Sunday, April 6, 2025\n- day count from purchase to refund request: 15 days\n- claim to check: the refund window for this case is 10 days\nEnd of case record.",
  "question": "Under these rules, does the governing version conflict with the claim in the case record?",
  "definitions": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- A claim about the refund window is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q589d6f0965",
  "kind": "choice",
  "text": "Internal summary for the file. Ravi Anand raised case CASE-3882 with Pembroke Travel about a conference trip. It is a brief, formal matter and details follow.\n\nVersions of the travel policy (end dates included):\n- v1: first version; in force from Tuesday, July 9, 2024 to Saturday, May 17, 2025; nightly hotel cap: 120.00 USD.\n- v2: replaces v1; in force from Sunday, May 18, 2025 to Tuesday, September 16, 2025; nightly hotel cap: 250.00 USD.\n- v3: replaces v2; in force from Wednesday, September 17, 2025, open-ended; nightly hotel cap: 200.00 USD.\n  Transition clause of v3: if v3 would govern a case whose booking date is before Wednesday, September 17, 2025, the version in force on that booking date governs it instead.\n\nCase CASE-3882:\n- booking date: Tuesday, September 16, 2025\n- travel date: Thursday, October 2, 2025\n- expense claim date: Thursday, October 23, 2025\n- decision date: Sunday, February 15, 2026\n- nightly rate claimed: 157.00 USD\nEnd of case record.",
  "question": "Finding the version of the travel policy that governs a case:\n- Default: the version in force on the case's booking date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhat nightly hotel cap does the governing version of travel policy set for case CASE-3882?",
  "options": [
   "$200.00",
   "$250.00"
  ]
 },
 {
  "qid": "qbaa4088f93",
  "kind": "choice",
  "text": "Formal record: Jonas Feld raised case CASE-3447 with Quayside Software about a payroll record. Matter recorded briefly for internal use. Full details follow in the case file.\n\nVersions of the records retention schedule (end dates included):\n- RS21: first version; in force from April 16, 2024 to October 30, 2024; retention period: 365 days.\n- RS92: replaces RS21; in force from October 31, 2024, open-ended; retention period: 180 days.\n\nCase CASE-3447:\n- record creation date: October 2, 2024\n- record closure date: October 2, 2024\n- deletion request date: October 30, 2024\n- decision date: November 21, 2024\n- day count from record closure to deletion request: 28 days\nEnd of case record.",
  "question": "Finding the version of the records retention schedule that governs a case:\n- The governing version is the version in force on the case's record closure date.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, which listed version of records retention schedule is the governing version for case CASE-3447?",
  "options": [
   "RS92",
   "RS21"
  ]
 },
 {
  "qid": "qf339de2730",
  "kind": "yes/no",
  "text": "Internal record: CASE-5314 concerns a card account that Hana Sato raised with Pembroke Travel. Things feel calm and the matter is routine. Background and details follow below.\n\nVersions of the fee schedule (end dates included):\n- FS-360: first version; in force from June 15, 2023 to November 14, 2023; fee cap: 25.00 USD.\n- FS-933: replaces FS-360; in force from November 15, 2023 to June 14, 2024; fee cap: 35.00 USD.\n  Transition clause of FS-933: if FS-933 would govern a case whose billing date is before November 15, 2023, the version in force on that billing date governs it instead.\n- FS-773: replaces FS-933; in force from June 15, 2024 to February 22, 2025; fee cap: 40.00 USD.\n- FS-435: replaces FS-773; in force from February 23, 2025, open-ended; fee cap: 15.00 USD.\n\nCase CASE-5314:\n- account opening date: January 4, 2025\n- billing date: February 23, 2025\n- dispute date: February 23, 2025\n- decision date: March 25, 2025\n- fee charged: 21.00 USD\n- claim to check: the fee cap for this case is 15.00 USD\nEnd of case record.",
  "question": "Going by the version history, would it be the case that it is not the case that the governing version does not confirm the claim to check?",
  "definitions": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's dispute date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- A claim about the fee cap is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qdb32e4b19f",
  "kind": "yes/no",
  "text": "Concern about language course for Jonas Feld, CASE-2409\nJonas Feld raised a case with Tamsin Fitness about a language course, and the background follows. The customer sounds mildly irritated yet keeps a civil and measured tone throughout.\n\nVersions of the refund policy (end dates included):\n- v1: first version; in force from Friday, 10 November 2023 to Monday, 15 January 2024; refund window: 7 days.\n- v2: replaces v1; in force from Tuesday, 16 January 2024 to Friday, 27 December 2024; refund window: 14 days.\n- v3: replaces v2; in force from Saturday, 28 December 2024, open-ended; refund window: 28 days.\n\nCase CASE-2409:\n- purchase date: Monday, 2 September 2024\n- delivery date: Monday, 2 September 2024\n- refund request date: Friday, 27 December 2024\n- decision date: Saturday, 11 January 2025\n- day count from purchase to refund request: 116 days\n- claim to check: the refund window for this case is 28 days\nEnd of case record.",
  "question": "For the refund policy, does the claim to check in the case record state the same value the governing version sets?",
  "definitions": "Finding the version of the refund policy that governs a case:\n- The governing version is the version in force on the case's purchase date.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- A claim about the refund window is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qd8cec44a46",
  "kind": "yes/no",
  "text": "Lucas Brenner: Hello. I am calling about my e-bike. I raised a case with Corran Telecom and I am a bit irritated, and I would like to talk it through with you.\nagent: Hello. I have case CASE-9311 on file, so let us talk through the e-bike details.\n\nVersions of the warranty terms (end dates excluded):\n- v1: first version; in force from March 12, 2024 to December 15, 2024; warranty period: 90 days.\n- v2: replaces v1; in force from December 15, 2024, open-ended; warranty period: 365 days.\n\nCase CASE-9311:\n- purchase date: April 20, 2025\n- fault date: June 29, 2025\n- claim date: September 26, 2025\n- decision date: October 9, 2025\n- day count from purchase to fault: 70 days\nEnd of case record.",
  "question": "Is v2 the version that governs this case?",
  "definitions": "Finding the version of the warranty terms that governs a case:\n- The governing version is the version in force on the case's fault date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qb32cb4379d",
  "kind": "choice",
  "text": "Sara Ilves and the meal kit plan\nSara Ilves raised case CASE-3046 with Redfern Bank about a meal kit plan. Mild impatience comes through, but the customer stays civil and the details follow.\n\nVersion table of the subscription terms (end dates included):\nversion | replaces | in force from | in force to | free cancellation period\nST-786 | first version | 22 Apr 2023 | 17 Oct 2023 | 30 days\nST-495 | ST-786 | 18 Oct 2023 | 20 Nov 2024 | 3 days\nST-328 | ST-495 | 21 Nov 2024 | 14 Jan 2025 | 14 days\nST-198 | ST-328 | 15 Jan 2025 | open-ended | 5 days\nTransition clause of ST-198: if ST-198 would govern a case whose renewal date is before 15 Jan 2025, the version in force on that renewal date governs it instead.\n\nCase CASE-3046:\n- sign-up date: 6 Sep 2024\n- renewal date: 19 Nov 2024\n- cancellation date: 20 Nov 2024\n- decision date: 11 Feb 2025\n- day count from sign-up to cancellation: 75 days\nEnd of case record.",
  "question": "Finding the version of the subscription terms that governs a case:\n- Default: the version in force on the case's renewal date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, what free cancellation period is set for case CASE-3046 by the governing version of subscription terms?",
  "options": [
   "3 days",
   "5 days"
  ]
 },
 {
  "qid": "qc8c4bc5d9c",
  "kind": "choice",
  "text": "Internal case note: Aiko Brandt contacted Corran Telecom about a safety boot, and the case is logged under CASE-9216. The request came in through the usual channel and it is a routine matter. The background and the case details follow in the sections below.\n\nVersions of the price list (end dates excluded):\n- rev-A: first version; in force from 21 September 2024 to 10 December 2024; price cap per unit: $14.99.\n- rev-B: replaces rev-A; in force from 10 December 2024 to 2 October 2025; price cap per unit: $24.00.\n- rev-C: replaces rev-B; in force from 2 October 2025, open-ended; price cap per unit: $29.99.\n\nCase CASE-9216:\n- contract date: 21 September 2024\n- delivery date: 21 September 2024\n- invoice date: 10 December 2024\n- decision date: 26 December 2024\n- unit price charged: $16.00\nEnd of case record.",
  "question": "Finding the version of the price list that governs a case:\n- The governing version is the version in force on the case's invoice date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, what value does the governing version of price list give the price cap per unit in case CASE-9216?",
  "options": [
   "$29.99",
   "$24.00"
  ]
 },
 {
  "qid": "q31111cb659",
  "kind": "choice",
  "text": "Card account concern from Theo Kalnins\nTheo Kalnins raised case CASE-3047 with Corran Telecom about a notes app. A little cross, though civil, and the details follow.\n\nChange log of the licence terms, newest entry first:\n23 July 2025 | LT-181 takes effect, replacing LT-457 | device limit: 3 devices\n  Transition clause of LT-181: if LT-181 would govern a case whose licence purchase date is before 23 July 2025, the version in force on that licence purchase date governs it instead.\n29 January 2025 | LT-457 takes effect, replacing LT-863 | device limit: 10 devices\n10 April 2024 | LT-863 takes effect as the first version | device limit: 2 devices\n\nCase CASE-3047:\n- licence purchase date: 17 July 2024\n- activation date: 28 January 2025\n- support request date: 31 January 2025\n- decision date: 27 June 2025\n- number of devices registered: 1 device\nEnd of case record.",
  "question": "Finding the version of the licence terms that governs a case:\n- Default: the version in force on the case's activation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of licence terms governs case CASE-3047 under the card's rules?",
  "options": [
   "LT-863",
   "LT-181"
  ]
 },
 {
  "qid": "qb8c715f9bb",
  "kind": "choice",
  "text": "case: CASE-5488\ncustomer: Theo Kalnins\nitem: study block\nThe customer kindly raised a case with Lindenfeld Outfitters about the study block, and the details follow. The tone of the message is upbeat and cheerful throughout.\n\nVersions of the leave policy (end dates excluded):\n- LP-312: first version; in force from 2024-11-01 to 2024-12-30; paid leave allowance: 15 days.\n- LP-665: replaces LP-312; in force from 2024-12-30 to 2025-07-21; paid leave allowance: 30 days.\n- LP-198: replaces LP-665; in force from 2025-07-21, open-ended; paid leave allowance: 25 days.\n  Transition clause of LP-198: if a version older than LP-198 would govern a case whose decision date is on or after 2025-07-21, LP-198 governs it instead.\n\nCase CASE-5488:\n- hire date: 2024-12-22\n- leave start date: 2025-06-12\n- claim date: 2025-07-21\n- decision date: 2025-07-21\n- number of leave days claimed: 26 days\nEnd of case record.",
  "question": "Finding the version of the leave policy that governs a case:\n- Default: the version in force on the case's hire date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, which version of the leave policy is the governing version for this case?",
  "options": [
   "LP-312",
   "LP-198"
  ]
 },
 {
  "qid": "q1bc1ab0a54",
  "kind": "yes/no",
  "text": "Client visit case for Malik Osei\nMalik Osei raised case CASE-7091 with Upland Utilities about a laptop. A touch of frustration shows, but the wording is courteous throughout.\n\nVersions of the warranty terms (end dates excluded):\n- v1: first version; in force from 1 May 2023 to 25 Jul 2023; warranty period: 365 days.\n- v2: replaces v1; in force from 25 Jul 2023 to 5 Jun 2024; warranty period: 60 days.\n  Transition clause of v2: if v2 would govern a case whose purchase date is before 25 Jul 2023, the version in force on that purchase date governs it instead.\n- v3: replaces v2; in force from 5 Jun 2024, open-ended; warranty period: 730 days.\n\nCase CASE-7091:\n- purchase date: 23 Jul 2023\n- fault date: 28 May 2024\n- claim date: 28 May 2024\n- decision date: 28 Nov 2024\n- day count from purchase to fault: 310 days\n- claim to check: the warranty period for this case is 730 days\nEnd of case record.",
  "question": "Does the claim in case CASE-7091 match the warranty period that the governing version of warranty terms sets?",
  "definitions": "Finding the version of the warranty terms that governs a case:\n- Default: the version in force on the case's fault date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- A claim about the warranty period is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q6bc0ef3610",
  "kind": "yes/no",
  "text": "Internal record: CASE-5314 concerns a card account that Hana Sato raised with Pembroke Travel. Things feel calm and the matter is routine. Background and details follow below.\n\nVersions of the fee schedule (end dates included):\n- FS-360: first version; in force from June 15, 2023 to November 14, 2023; fee cap: 25.00 USD.\n- FS-933: replaces FS-360; in force from November 15, 2023 to June 14, 2024; fee cap: 35.00 USD.\n  Transition clause of FS-933: if FS-933 would govern a case whose billing date is before November 15, 2023, the version in force on that billing date governs it instead.\n- FS-773: replaces FS-933; in force from June 15, 2024 to March 24, 2025; fee cap: 40.00 USD.\n- FS-435: replaces FS-773; in force from March 25, 2025, open-ended; fee cap: 15.00 USD.\n\nCase CASE-5314:\n- account opening date: January 4, 2025\n- billing date: February 23, 2025\n- dispute date: February 23, 2025\n- decision date: March 25, 2025\n- fee charged: 21.00 USD\n- claim to check: the fee cap for this case is 15.00 USD\nEnd of case record.",
  "question": "Going by the version history, would it be the case that it is not the case that the governing version does not confirm the claim to check?",
  "definitions": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's dispute date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- A claim about the fee cap is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qf926a3d48e",
  "kind": "yes/no",
  "text": "Internal case note: Ana Ruiz contacted Quayside Software about a camera recording and the matter is logged under CASE-1045. It is a calm, routine entry with a steady pace. Background and case details are set out further down.\n\nVersions of the records retention schedule (end dates included):\n- v1: first version; in force from October 5, 2024 to August 4, 2025; retention period: 180 days.\n- v2: replaces v1; in force from August 5, 2025 to April 21, 2026; retention period: 30 days.\n- v3: replaces v2; in force from April 22, 2026, open-ended; retention period: 730 days.\n\nCase CASE-1045:\n- record creation date: March 4, 2026\n- record closure date: April 21, 2026\n- deletion request date: April 22, 2026\n- decision date: April 22, 2026\n- day count from record closure to deletion request: 1 day\nEnd of case record.",
  "question": "Going by the version history, is the governing version for case CASE-1045 in records retention schedule exactly v3?",
  "definitions": "Finding the version of the records retention schedule that governs a case:\n- The governing version is the version in force on the case's record closure date.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q5d958d4af6",
  "kind": "yes/no",
  "text": "Concern about language course for Jonas Feld, CASE-2409\nJonas Feld raised a case with Tamsin Fitness about a language course, and the background follows. The customer sounds mildly irritated yet keeps a civil and measured tone throughout.\n\nVersions of the refund policy (end dates included):\n- v1: first version; in force from Friday, 10 November 2023 to Monday, 15 January 2024; refund window: 7 days.\n- v2: replaces v1; in force from Tuesday, 16 January 2024 to Sunday, 1 September 2024; refund window: 14 days.\n- v3: replaces v2; in force from Monday, 2 September 2024, open-ended; refund window: 28 days.\n\nCase CASE-2409:\n- purchase date: Monday, 2 September 2024\n- delivery date: Monday, 2 September 2024\n- refund request date: Friday, 27 December 2024\n- decision date: Saturday, 11 January 2025\n- day count from purchase to refund request: 116 days\n- claim to check: the refund window for this case is 28 days\nEnd of case record.",
  "question": "For the refund policy, does the claim to check in the case record state the same value the governing version sets?",
  "definitions": "Finding the version of the refund policy that governs a case:\n- The governing version is the version in force on the case's purchase date.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- A claim about the refund window is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qa2d078410f",
  "kind": "yes/no",
  "text": "Concern about standing desk for Owen Pryce, CASE-2232\nOwen Pryce raised a case with Redfern Bank about a standing desk, and the background follows. The customer sounds mildly irritated yet keeps a civil and measured tone throughout.\n\nVersions of the refund policy (end dates included):\n- v1: first version; in force from Saturday, September 7, 2024 to Tuesday, April 22, 2025; refund window: 10 days.\n- v2: replaces v1; in force from Wednesday, April 23, 2025, open-ended; refund window: 90 days.\n  Transition clause of v2: if v2 would govern a case whose purchase date is before Wednesday, April 23, 2025, the version in force on that purchase date governs it instead.\n\nCase CASE-2232:\n- purchase date: Saturday, March 22, 2025\n- delivery date: Sunday, March 23, 2025\n- refund request date: Sunday, April 6, 2025\n- decision date: Sunday, April 6, 2025\n- day count from purchase to refund request: 15 days\n- claim to check: the refund window for this case is 10 days\nEnd of case record.",
  "question": "Does the claim to check for this case match the value set by the governing version?",
  "definitions": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- A claim about the refund window is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q084fe0981c",
  "kind": "choice",
  "text": "Owen Pryce: Hello, I am calling about case CASE-3600 with Lindenfeld Outfitters. I am a bit irritated about my language course, though I am staying calm.\nagent: Hello Owen Pryce, thank you for calling. I hear the concern, and the full details follow.\n\nChange log of the refund policy, newest entry first:\nMonday, 21 July 2025 | v3 takes effect, replacing v2 | refund window: 90 days\nFriday, 22 November 2024 | v2 takes effect, replacing v1 | refund window: 10 days\nMonday, 29 July 2024 | v1 takes effect as the first version | refund window: 30 days\n\nCase CASE-3600:\n- purchase date: Sunday, 22 September 2024\n- delivery date: Sunday, 22 September 2024\n- refund request date: Friday, 22 November 2024\n- decision date: Friday, 22 November 2024\n- day count from purchase to refund request: 61 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- The governing version is the version in force on the case's refund request date.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich refund window would the governing version of refund policy assign to case CASE-3600?",
  "options": [
   "10 days",
   "90 days"
  ]
 },
 {
  "qid": "q40d68cd593",
  "kind": "choice",
  "text": "Card account concern from Malik Osei\nMalik Osei raised case CASE-5706 with Selkirk Logistics about a language course. A little cross, though civil, and the details follow.\n\nVersions of the refund policy (end dates included):\n- v1: first version; in force from 18 Oct 2023 to 17 Apr 2024; refund window: 28 days.\n- v2: replaces v1; in force from 18 Apr 2024 to 28 Jul 2024; refund window: 21 days.\n- v3: replaces v2; in force from 29 Jul 2024 to 6 Oct 2024; refund window: 10 days.\n  Transition clause of v3: if a version older than v3 would govern a case whose decision date is on or after 29 Jul 2024, v3 governs it instead.\n- v4: replaces v3; in force from 7 Oct 2024, open-ended; refund window: 14 days.\n\nCase CASE-5706:\n- purchase date: 15 Nov 2023\n- delivery date: 15 Dec 2023\n- refund request date: 30 Dec 2023\n- decision date: 29 Jul 2024\n- day count from purchase to refund request: 45 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, what value does the governing version of refund policy give the refund window in case CASE-5706?",
  "options": [
   "10 days",
   "28 days"
  ]
 },
 {
  "qid": "q85d2fe8a3c",
  "kind": "choice",
  "text": "Aiko Brandt: Hi, I am calling about my grocery order. I raised a case with Tamsin Fitness and I am a little frustrated, though I would like a clear explanation.\nagent: Thanks for getting in touch. I have case CASE-3842 on file, so tell me more about the grocery order.\n\nVersions of the shipping policy (end dates excluded):\n- SP-920: first version; in force from Friday, November 29, 2024 to Thursday, September 4, 2025; delivery promise: 10 days.\n- SP-759: replaces SP-920; in force from Thursday, September 4, 2025 to Friday, March 20, 2026; delivery promise: 4 days.\n  Transition clause of SP-759: if SP-759 would govern a case whose delivery date is before Thursday, September 4, 2025, the version in force on that delivery date governs it instead.\n- SP-386: replaces SP-759; in force from Friday, March 20, 2026, open-ended; delivery promise: 14 days.\n\nCase CASE-3842:\n- order date: Tuesday, September 2, 2025\n- delivery date: Wednesday, September 3, 2025\n- complaint date: Wednesday, February 18, 2026\n- decision date: Monday, March 2, 2026\n- day count from order to delivery: 1 day\nEnd of case record.",
  "question": "Finding the version of the shipping policy that governs a case:\n- Default: the version in force on the case's complaint date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhat delivery promise does the shipping policy version that governs case CASE-3842 set?",
  "options": [
   "4 days",
   "10 days"
  ]
 },
 {
  "qid": "qbf3c4240aa",
  "kind": "yes/no",
  "text": "Ines Duarte raised a case with Brightwell Supply about a safety boot. The matter is logged under CASE-4564. The history and case details follow in the sections below.\n\nVersion table of the price list (end dates excluded):\nversion | replaces | in force from | in force to | price cap per unit\nv1 | first version | January 17, 2024 | April 1, 2024 | $12.50\nv2 | v1 | April 1, 2024 | September 3, 2024 | $19.99\nv3 | v2 | September 3, 2024 | April 28, 2025 | $35.00\nv4 | v3 | April 28, 2025 | open-ended | $24.00\n\nCase CASE-4564:\n- contract date: June 26, 2025\n- delivery date: June 26, 2025\n- invoice date: December 22, 2025\n- decision date: April 24, 2026\n- unit price charged: $24.00\nEnd of case record.",
  "question": "Going by the version history, does case CASE-4564 stay within the price cap per unit that the governing version of price list sets?",
  "definitions": "Finding the version of the price list that governs a case:\n- The governing version is the version in force on the case's delivery date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- The case is within the price cap per unit when its unit price charged is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qfc3a6ae021",
  "kind": "choice",
  "text": "Nadia Kowal: Hello, I am writing to raise a case with Veridia Health about my camera bag.\nsupport: Hello. The case sits under CASE-8497 with the routine notes beside it.\nNadia Kowal: Thanks, that covers it.\n\nChange log of the refund policy, newest entry first:\n22 November 2024 | RP-580 takes effect, replacing RP-289 | refund window: 14 days\n29 August 2024 | RP-289 takes effect as the first version | refund window: 45 days\n  Sunset clause of RP-289: if RP-289 would govern a case whose decision date is after 23 January 2025, RP-580 governs it instead.\n\nCase CASE-8497:\n- purchase date: 29 August 2024\n- delivery date: 29 August 2024\n- refund request date: 12 November 2024\n- decision date: 24 January 2025\n- day count from purchase to refund request: 75 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's refund request date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of refund policy do the card's rules pick for case CASE-8497?",
  "options": [
   "RP-289",
   "RP-580"
  ]
 },
 {
  "qid": "q60ba5c6a25",
  "kind": "yes/no",
  "text": "Priya Raman: Hello. I raised a case with Veridia Health about my annual plan and I would like the matter reviewed.\nsupport: Hello. I have case CASE-8514 on file and the annual plan details follow.\n\nVersions of the refund policy (end dates included):\n- RP-450: first version; in force from July 20, 2023 to May 18, 2024; refund window: 90 days.\n  Sunset clause of RP-450: if RP-450 would govern a case whose decision date is after June 4, 2024, RP-789 governs it instead.\n- RP-789: replaces RP-450; in force from May 19, 2024, open-ended; refund window: 45 days.\n\nCase CASE-8514:\n- purchase date: November 24, 2023\n- delivery date: November 25, 2023\n- refund request date: January 9, 2024\n- decision date: June 4, 2024\n- day count from purchase to refund request: 46 days\nEnd of case record.",
  "question": "Going by the version history, would it be so that it is not the case that this case does not sit within the refund window?",
  "definitions": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's refund request date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the refund window when its day count from purchase to refund request is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q96b8009a36",
  "kind": "choice",
  "text": "case: CASE-8982\ncontact: Lena Whitcombe\nitem: family visit\nA polite but slightly irritated case was raised with Tamsin Fitness about the family visit. The details follow in the usual way.\n\nVersions of the leave policy (end dates excluded):\n- LP-22W: first version; in force from 18 Oct 2023 to 27 Jun 2024; paid leave allowance: 15 days.\n- LP-64C: replaces LP-22W; in force from 27 Jun 2024 to 23 Oct 2024; paid leave allowance: 10 days.\n- LP-80K: replaces LP-64C; in force from 23 Oct 2024 to 28 Jan 2025; paid leave allowance: 30 days.\n  Sunset clause of LP-80K: if LP-80K would govern a case whose decision date is after 7 May 2025, LP-15G governs it instead.\n- LP-15G: replaces LP-80K; in force from 28 Jan 2025, open-ended; paid leave allowance: 20 days.\n\nCase CASE-8982:\n- hire date: 10 Nov 2024\n- leave start date: 11 Nov 2024\n- claim date: 21 Nov 2024\n- decision date: 4 Aug 2025\n- number of leave days claimed: 28 days\nEnd of case record.",
  "question": "Finding the version of the leave policy that governs a case:\n- Default: the version in force on the case's hire date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nFor case CASE-8982, which version of leave policy governs according to the card?",
  "options": [
   "LP-15G",
   "LP-80K"
  ]
 },
 {
  "qid": "qb65c4ad461",
  "kind": "choice",
  "text": "Internal record: CASE-5769 concerns a card account that Ana Ruiz raised with Redfern Bank. Things feel calm and the matter is routine. Background and details follow below.\n\nVersion table of the fee schedule (end dates included):\nversion | replaces | in force from | in force to | fee cap\nFS-52P | first version | 2023-09-11 | 2024-01-03 | $15.00\nFS-11X | FS-52P | 2024-01-04 | 2024-06-14 | $50.00\nFS-31W | FS-11X | 2024-06-15 | open-ended | $25.00\n\nCase CASE-5769:\n- account opening date: 2024-06-29\n- billing date: 2024-11-04\n- dispute date: 2025-03-02\n- decision date: 2025-03-10\n- fee charged: $20.00\nEnd of case record.",
  "question": "Finding the version of the fee schedule that governs a case:\n- The governing version is the version in force on the case's dispute date.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of fee schedule governs case CASE-5769 under the card's rules?",
  "options": [
   "FS-52P",
   "FS-31W"
  ]
 },
 {
  "qid": "q65edc87e3e",
  "kind": "choice",
  "text": "Concern about streaming plan for Owen Pryce, CASE-6184\nOwen Pryce raised a case with Pembroke Travel about a streaming plan, and the background follows. The customer sounds mildly irritated yet keeps a civil and measured tone throughout.\n\nVersion table of the subscription terms (end dates included):\nversion | replaces | in force from | in force to | free cancellation period\nST-822 | first version | January 24, 2024 | April 29, 2024 | 14 days\nST-194 | ST-822 | April 30, 2024 | February 24, 2025 | 30 days\nST-291 | ST-194 | February 25, 2025 | open-ended | 7 days\nTransition clause of ST-194: if a version older than ST-194 would govern a case whose decision date is on or after April 30, 2024, ST-194 governs it instead.\n\nCase CASE-6184:\n- sign-up date: March 21, 2024\n- renewal date: April 2, 2024\n- cancellation date: April 29, 2024\n- decision date: April 29, 2024\n- day count from sign-up to cancellation: 39 days\nEnd of case record.",
  "question": "Finding the version of the subscription terms that governs a case:\n- Default: the version in force on the case's renewal date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nGoing by the version history, what free cancellation period does the governing version of subscription terms set for case CASE-6184?",
  "options": [
   "7 days",
   "14 days"
  ]
 },
 {
  "qid": "qc5ddd9479e",
  "kind": "yes/no",
  "text": "Gym membership case for Yara Haddad\nYara Haddad raised case CASE-6891 with Veridia Health about a design suite. The customer is a little frustrated but polite, and the details follow.\n\nVersions of the licence terms (end dates excluded):\n- rev-A: first version; in force from 25 Jul 2024 to 1 Jun 2025; device limit: 5 devices.\n- rev-B: replaces rev-A; in force from 1 Jun 2025, open-ended; device limit: 1 device.\n  Transition clause of rev-B: if rev-B would govern a case whose activation date is before 1 Jun 2025, the version in force on that activation date governs it instead.\n\nCase CASE-6891:\n- licence purchase date: 18 Apr 2025\n- activation date: 31 May 2025\n- support request date: 22 Sep 2025\n- decision date: 22 Sep 2025\n- number of devices registered: 9 devices\nEnd of case record.",
  "question": "Is rev-B the governing version of licence terms for case CASE-6891?",
  "definitions": "Finding the version of the licence terms that governs a case:\n- Default: the version in force on the case's activation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qa16716e19b",
  "kind": "choice",
  "text": "Lucas Brenner: Hello. I am calling about my design suite. I raised a case with Tamsin Fitness and I am slightly irritated, but I would like a clear answer.\nagent: Hello. I have case CASE-9100 on file, so let us look at the design suite details.\n\nChange log of the licence terms, newest entry first:\n2025-03-10 | v3 takes effect, replacing v2 | device limit: 3 devices\n2024-08-25 | v2 takes effect, replacing v1 | device limit: 1 device\n  Sunset clause of v2: if v2 would govern a case whose decision date is after 2025-05-06, v3 governs it instead.\n2023-11-10 | v1 takes effect as the first version | device limit: 5 devices\n\nCase CASE-9100:\n- licence purchase date: 2024-08-22\n- activation date: 2024-09-18\n- support request date: 2024-11-24\n- decision date: 2025-05-07\n- number of devices registered: 2 devices\nEnd of case record.",
  "question": "Finding the version of the licence terms that governs a case:\n- Default: the version in force on the case's activation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, the governing version of licence terms sets what device limit for case CASE-9100?",
  "options": [
   "3 devices",
   "1 device"
  ]
 }
]
