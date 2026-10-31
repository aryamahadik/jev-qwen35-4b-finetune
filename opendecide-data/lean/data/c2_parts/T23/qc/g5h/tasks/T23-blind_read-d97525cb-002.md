# G5-H blind read (all free-form rows) T23-blind_read-d97525cb-002 (family T23)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T23/qc/g5h/answers/T23-blind_read-d97525cb-002.json

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
  "qid": "qe6e1b0ea7d",
  "kind": "choice",
  "text": "Yara Haddad raised case CASE-3797 with Selkirk Logistics about a grocery order. The case is calm and routine. Background is filed below, along with the rest of the details.\n\nVersions of the shipping policy (end dates excluded):\n- SP-430: first version; in force from Sunday, January 22, 2023 to Tuesday, October 24, 2023; delivery promise: 4 days.\n- SP-230: replaces SP-430; in force from Tuesday, October 24, 2023 to Saturday, December 9, 2023; delivery promise: 5 days.\n  Transition clause of SP-230: if SP-230 would govern a case whose delivery date is before Tuesday, October 24, 2023, the version in force on that delivery date governs it instead.\n- SP-867: replaces SP-230; in force from Saturday, December 9, 2023, open-ended; delivery promise: 2 days.\n\nCase CASE-3797:\n- order date: Sunday, September 17, 2023\n- delivery date: Monday, September 18, 2023\n- complaint date: Sunday, November 26, 2023\n- decision date: Sunday, December 10, 2023\n- day count from order to delivery: 1 day\nEnd of case record.",
  "question": "Finding the version of the shipping policy that governs a case:\n- Default: the version in force on the case's complaint date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of shipping policy do the card's rules pick for case CASE-3797?",
  "options": [
   "SP-867",
   "SP-430"
  ]
 },
 {
  "qid": "q960ecfb6a8",
  "kind": "choice",
  "text": "Internal case note: Kofi Mensah raised a case with Corran Telecom about a standing desk, and it is held under CASE-7634. The tone of the message has stayed steady and the background follows.\n\nVersions of the refund policy (end dates included):\n- rev-A: first version; in force from 15 July 2023 to 7 November 2023; refund window: 60 days.\n- rev-B: replaces rev-A; in force from 8 November 2023 to 20 July 2024; refund window: 45 days.\n- rev-C: replaces rev-B; in force from 21 July 2024 to 26 September 2024; refund window: 28 days.\n- rev-D: replaces rev-C; in force from 27 September 2024, open-ended; refund window: 30 days.\n  Transition clause of rev-D: if rev-D would govern a case whose delivery date is before 27 September 2024, the version in force on that delivery date governs it instead.\n\nCase CASE-7634:\n- purchase date: 20 July 2024\n- delivery date: 14 August 2024\n- refund request date: 26 December 2024\n- decision date: 6 June 2025\n- day count from purchase to refund request: 159 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhat refund window does the governing version of refund policy set for case CASE-7634?",
  "options": [
   "45 days",
   "28 days"
  ]
 },
 {
  "qid": "qf7be0a6838",
  "kind": "yes/no",
  "text": "Internal summary for the file. Yara Haddad raised case CASE-3215 with Tamsin Fitness about a camera recording. It is a brief, formal matter and details follow.\n\nVersion table of the records retention schedule (end dates included):\nversion | replaces | in force from | in force to | retention period\nrev-A | first version | January 5, 2023 | August 18, 2023 | 365 days\nrev-B | rev-A | August 19, 2023 | February 11, 2024 | 90 days\nrev-C | rev-B | February 12, 2024 | August 17, 2024 | 730 days\nrev-D | rev-C | August 18, 2024 | open-ended | 30 days\nTransition clause of rev-B: if rev-B would govern a case whose record closure date is before August 19, 2023, the version in force on that record closure date governs it instead.\n\nCase CASE-3215:\n- record creation date: January 17, 2025\n- record closure date: June 6, 2025\n- deletion request date: July 7, 2025\n- decision date: October 12, 2025\n- day count from record closure to deletion request: 31 days\nEnd of case record.",
  "question": "Does this case fit within the retention period set by the governing version?",
  "definitions": "Finding the version of the records retention schedule that governs a case:\n- Default: the version in force on the case's record creation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the retention period when its day count from record closure to deletion request is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q1c89838c5d",
  "kind": "yes/no",
  "text": "Customer case CASE-6934 for Jonas Feld\nJonas Feld is a warm, chatty sort who has raised a case with Veridia Health about the support transcript. The case details are laid out below.\n\nVersion table of the records retention schedule (end dates included):\nversion | replaces | in force from | in force to | retention period\nv1 | first version | 1 August 2024 | 10 May 2025 | 365 days\nv2 | v1 | 11 May 2025 | 16 January 2026 | 30 days\nv3 | v2 | 17 January 2026 | open-ended | 90 days\nTransition clause of v3: if v3 would govern a case whose record creation date is before 17 January 2026, the version in force on that record creation date governs it instead.\n\nCase CASE-6934:\n- record creation date: 12 January 2026\n- record closure date: 2 February 2026\n- deletion request date: 8 April 2026\n- decision date: 15 July 2026\n- day count from record closure to deletion request: 65 days\nEnd of case record.\n\nThose earlier terms were set aside for this particular account, so the old wording is just background.",
  "question": "Is the case within the retention period set by the governing version of records retention schedule?",
  "definitions": "Finding the version of the records retention schedule that governs a case:\n- Default: the version in force on the case's record creation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the retention period when its day count from record closure to deletion request is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q4b80d90154",
  "kind": "choice",
  "text": "Kofi Mensah and the tyre order\nKofi Mensah raised case CASE-2488 with Upland Utilities about a tyre order. Mild impatience comes through, but the customer stays civil and the details follow.\n\nVersions of the shipping policy (end dates excluded):\n- v1: first version; in force from 1 Feb 2024 to 10 Mar 2024; delivery promise: 10 days.\n- v2: replaces v1; in force from 10 Mar 2024 to 14 Nov 2024; delivery promise: 5 days.\n- v3: replaces v2; in force from 14 Nov 2024, open-ended; delivery promise: 2 days.\n  Transition clause of v3: if v3 would govern a case whose order date is before 14 Nov 2024, the version in force on that order date governs it instead.\n\nCase CASE-2488:\n- order date: 1 Feb 2024\n- delivery date: 1 Feb 2024\n- complaint date: 10 Mar 2024\n- decision date: 10 Mar 2024\n- day count from order to delivery: 0 days\nEnd of case record.",
  "question": "Finding the version of the shipping policy that governs a case:\n- Default: the version in force on the case's complaint date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder shipping policy, what delivery promise does the governing version set for case CASE-2488?",
  "options": [
   "2 days",
   "5 days"
  ]
 },
 {
  "qid": "q1d4a46d0db",
  "kind": "yes/no",
  "text": "Card account concern from Nadia Kowal\nNadia Kowal raised case CASE-8444 with Veridia Health about a printer toner. A little cross, though civil, and the details follow.\n\nVersion table of the price list (end dates excluded):\nversion | replaces | in force from | in force to | price cap per unit\nPL-164 | first version | 5 Sep 2024 | 24 Dec 2024 | $29.99\nPL-228 | PL-164 | 24 Dec 2024 | 7 Mar 2025 | $19.99\nPL-630 | PL-228 | 7 Mar 2025 | open-ended | $35.00\nTransition clause of PL-228: if a version older than PL-228 would govern a case whose decision date is on or after 24 Dec 2024, PL-228 governs it instead.\n\nCase CASE-8444:\n- contract date: 5 Sep 2024\n- delivery date: 17 Dec 2024\n- invoice date: 24 Dec 2024\n- decision date: 24 Dec 2024\n- unit price charged: $13.00\nEnd of case record.",
  "question": "Is it the case that it is not the case that PL-228 does not settle this case?",
  "definitions": "Finding the version of the price list that governs a case:\n- Default: the version in force on the case's delivery date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qdd13e431eb",
  "kind": "choice",
  "text": "case: CASE-8707\ncustomer: Eva Marsh\nitem: e-bike\nEva Marsh raised a case with Corran Telecom about an e-bike. The history and details follow below in a warm and friendly way.\n\nVersions of the warranty terms (end dates excluded):\n- WT-656: first version; in force from 20 June 2023 to 24 March 2024; warranty period: 365 days.\n  Sunset clause of WT-656: if WT-656 would govern a case whose decision date is after 25 March 2024, WT-596 governs it instead.\n- WT-596: replaces WT-656; in force from 24 March 2024, open-ended; warranty period: 30 days.\n\nCase CASE-8707:\n- purchase date: 16 January 2024\n- fault date: 18 January 2024\n- claim date: 9 February 2024\n- decision date: 25 March 2024\n- day count from purchase to fault: 2 days\nEnd of case record.",
  "question": "Finding the version of the warranty terms that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of warranty terms does the card say governs case CASE-8707?",
  "options": [
   "WT-656",
   "WT-596"
  ]
 },
 {
  "qid": "q379422a64f",
  "kind": "choice",
  "text": "Priya Raman: I am ringing about my annual plan from Lindenfeld Outfitters, and I am a little cross, though I do appreciate your help.\nagent: I understand the frustration and thank you for bearing with me, and your case CASE-5395 is in front of me.\n\nChange log of the refund policy, newest entry first:\n2025-07-30 | RP-253 takes effect, replacing RP-795 | refund window: 30 days\n2024-11-17 | RP-795 takes effect as the first version | refund window: 7 days\n  Sunset clause of RP-795: if RP-795 would govern a case whose decision date is after 2025-08-01, RP-253 governs it instead.\n\nCase CASE-5395:\n- purchase date: 2025-05-11\n- delivery date: 2025-05-12\n- refund request date: 2025-05-13\n- decision date: 2025-07-30\n- day count from purchase to refund request: 2 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's refund request date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAmong the versions of the refund policy shown, which governs this case?",
  "options": [
   "RP-253",
   "RP-795"
  ]
 },
 {
  "qid": "qc206ee243f",
  "kind": "choice",
  "text": "Dear team,\nI write to raise a formal case with Corran Telecom about my annual plan. My name is Malik Osei and the case identifier is CASE-3492. I appreciate your attention, and the details are set out below.\nYours sincerely,\n\nChange log of the refund policy, newest entry first:\n2025-03-11 | RP-422 takes effect, replacing RP-200 | refund window: 10 days\n2024-07-27 | RP-200 takes effect as the first version | refund window: 90 days\n  Sunset clause of RP-200: if RP-200 would govern a case whose decision date is after 2025-10-19, RP-422 governs it instead.\n\nCase CASE-3492:\n- purchase date: 2025-11-24\n- delivery date: 2025-11-25\n- refund request date: 2025-11-29\n- decision date: 2026-04-14\n- day count from purchase to refund request: 5 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's refund request date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nGoing by the version history, what refund window is set for case CASE-3492 by the governing version of refund policy?",
  "options": [
   "90 days",
   "10 days"
  ]
 },
 {
  "qid": "qdc4c72f4ba",
  "kind": "yes/no",
  "text": "name: Sara Ilves\ncompany: Veridia Health\ncase: CASE-7647\nSara Ilves is cheerful and easy to work with, having raised a case with Veridia Health about the grocery order, and the story is set out below.\n\nVersion table of the shipping policy (end dates excluded):\nversion | replaces | in force from | in force to | delivery promise\nv1 | first version | January 24, 2023 | June 20, 2023 | 10 days\nv2 | v1 | June 20, 2023 | May 2, 2024 | 14 days\nv3 | v2 | May 2, 2024 | open-ended | 2 days\nTransition clause of v2: if a version older than v2 would govern a case whose decision date is on or after June 20, 2023, v2 governs it instead.\n\nCase CASE-7647:\n- order date: February 19, 2023\n- delivery date: February 28, 2023\n- complaint date: February 28, 2023\n- decision date: June 26, 2023\n- day count from order to delivery: 9 days\nEnd of case record.",
  "question": "Under these rules, would it be so that it is not the case that v2 does not decide this case?",
  "definitions": "Finding the version of the shipping policy that governs a case:\n- Default: the version in force on the case's complaint date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qc0bc39934b",
  "kind": "choice",
  "text": "Hello,\nMy name is Lucas Brenner and I am writing to raise a case with Tamsin Fitness about my e-bike. The matter is calm and routine, and the case is filed as CASE-2141. The details follow below.\nTake care,\n\nChange log of the warranty terms, newest entry first:\nJune 19, 2025 | v3 takes effect, replacing v2 | warranty period: 90 days\nMarch 2, 2025 | v2 takes effect, replacing v1 | warranty period: 60 days\n  Sunset clause of v2: if v2 would govern a case whose decision date is after August 13, 2025, v3 governs it instead.\nNovember 18, 2024 | v1 takes effect as the first version | warranty period: 730 days\n\nCase CASE-2141:\n- purchase date: January 20, 2025\n- fault date: January 20, 2025\n- claim date: February 6, 2025\n- decision date: April 4, 2025\n- day count from purchase to fault: 0 days\nEnd of case record.",
  "question": "Finding the version of the warranty terms that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, what warranty period does case CASE-2141 of warranty terms get from its governing version?",
  "options": [
   "730 days",
   "60 days"
  ]
 },
 {
  "qid": "q64c6265dae",
  "kind": "choice",
  "text": "Coffee grinder case for Owen Pryce\nOwen Pryce raised case CASE-2832 with Mistral Home about a camera recording. Warm greetings to you, and the full details follow.\n\nVersion table of the records retention schedule (end dates included):\nversion | replaces | in force from | in force to | retention period\nv1 | first version | 19 February 2023 | 26 September 2023 | 180 days\nv2 | v1 | 27 September 2023 | 10 July 2024 | 60 days\nv3 | v2 | 11 July 2024 | open-ended | 730 days\nTransition clause of v2: if a version older than v2 would govern a case whose decision date is on or after 27 September 2023, v2 governs it instead.\n\nCase CASE-2832:\n- record creation date: 14 August 2023\n- record closure date: 27 September 2023\n- deletion request date: 27 September 2023\n- decision date: 27 September 2023\n- day count from record closure to deletion request: 0 days\nEnd of case record.",
  "question": "Finding the version of the records retention schedule that governs a case:\n- Default: the version in force on the case's record creation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhat retention period does the records retention schedule version that governs case CASE-2832 set?",
  "options": [
   "60 days",
   "730 days"
  ]
 },
 {
  "qid": "qda5a0870c5",
  "kind": "choice",
  "text": "Hi there,\nI am reaching out about my photo editor with Brightwell Supply, which is a calm and routine matter. My name is Sara Ilves and the case is logged as CASE-3712. The rest follows in the notes below.\nThanks,\n\nVersions of the licence terms (end dates excluded):\n- LT-518: first version; in force from 17 September 2023 to 22 November 2023; device limit: 5 devices.\n- LT-321: replaces LT-518; in force from 22 November 2023, open-ended; device limit: 1 device.\n  Transition clause of LT-321: if LT-321 would govern a case whose licence purchase date is before 22 November 2023, the version in force on that licence purchase date governs it instead.\n\nCase CASE-3712:\n- licence purchase date: 21 November 2023\n- activation date: 6 March 2024\n- support request date: 18 August 2024\n- decision date: 22 October 2024\n- number of devices registered: 4 devices\nEnd of case record.",
  "question": "Finding the version of the licence terms that governs a case:\n- Default: the version in force on the case's activation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, which listed version of licence terms governs case CASE-3712?",
  "options": [
   "LT-518",
   "LT-321"
  ]
 },
 {
  "qid": "q6565f9ce8b",
  "kind": "choice",
  "text": "Yara Haddad: Hello. I am calling about my annual plan. I raised a case with Quayside Software and I am slightly irritated, but I would like a clear answer.\nagent: Hello. I have case CASE-3992 on file, so let us look at the annual plan details.\n\nChange log of the refund policy, newest entry first:\n3 August 2024 | RP-460 takes effect, replacing RP-716 | refund window: 10 days\n31 January 2024 | RP-716 takes effect, replacing RP-765 | refund window: 21 days\n15 May 2023 | RP-765 takes effect as the first version | refund window: 45 days\n\nCase CASE-3992:\n- purchase date: 2 September 2023\n- delivery date: 12 September 2023\n- refund request date: 25 November 2023\n- decision date: 28 November 2023\n- day count from purchase to refund request: 84 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- The governing version is the version in force on the case's refund request date.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nGoing by the version history, which version of the refund policy governs this case?",
  "options": [
   "RP-460",
   "RP-765"
  ]
 },
 {
  "qid": "q5ad918c682",
  "kind": "yes/no",
  "text": "Dana Okafor: Hello, I am writing to raise a case with Veridia Health about my notes app.\nsupport: Hello. This matter sits under CASE-6013 alongside the routine notes.\nDana Okafor: Lovely, thank you.\n\nChange log of the licence terms, newest entry first:\n23 July 2023 | v2 takes effect, replacing v1 | device limit: 5 devices\n10 February 2023 | v1 takes effect as the first version | device limit: 10 devices\n\nCase CASE-6013:\n- licence purchase date: 15 May 2023\n- activation date: 22 July 2023\n- support request date: 15 December 2023\n- decision date: 10 May 2024\n- number of devices registered: 15 devices\n- claim to check: the device limit for this case is 10 devices\nEnd of case record.",
  "question": "Under these rules, does the governing version support the claim to check for device limit?",
  "definitions": "Finding the version of the licence terms that governs a case:\n- The governing version is the version in force on the case's activation date.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- A claim about the device limit is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q17078a21e0",
  "kind": "yes/no",
  "text": "Ines Duarte: Hello, I am writing to raise a case with Upland Utilities about conference trip.\nsupport: Hello. Your matter is recorded as CASE-7123 and the full details are set out in order.\n\nChange log of the travel policy, newest entry first:\n22 Jan 2024 | v2 takes effect, replacing v1 | nightly hotel cap: $175.00\n7 Aug 2023 | v1 takes effect as the first version | nightly hotel cap: $200.00\n  Sunset clause of v1: if v1 would govern a case whose decision date is after 16 Feb 2024, v2 governs it instead.\n\nCase CASE-7123:\n- booking date: 14 Aug 2023\n- travel date: 28 Aug 2023\n- expense claim date: 29 Aug 2023\n- decision date: 17 Feb 2024\n- nightly rate claimed: $92.00\nEnd of case record.",
  "question": "Under these rules, would it be so that it is not the case that v1 does not decide this case?",
  "definitions": "Finding the version of the travel policy that governs a case:\n- Default: the version in force on the case's booking date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q4ebab09120",
  "kind": "choice",
  "text": "Lucas Brenner raised a case with Tamsin Fitness about a grocery order. The case is filed as CASE-8856. The history of the case and its details follow in full.\n\nVersion table of the shipping policy (end dates excluded):\nversion | replaces | in force from | in force to | delivery promise\nv1 | first version | 23 Apr 2024 | 23 Jan 2025 | 14 days\nv2 | v1 | 23 Jan 2025 | 3 Jul 2025 | 7 days\nv3 | v2 | 3 Jul 2025 | 27 Jan 2026 | 10 days\nv4 | v3 | 27 Jan 2026 | open-ended | 5 days\nTransition clause of v4: if a version older than v4 would govern a case whose decision date is on or after 27 Jan 2026, v4 governs it instead.\n\nCase CASE-8856:\n- order date: 16 Jul 2026\n- delivery date: 14 Aug 2026\n- complaint date: 24 Jan 2027\n- decision date: 5 Feb 2027\n- day count from order to delivery: 29 days\nEnd of case record.\n\nThe old terms were dropped just for this file, so read the situation as it currently stands.",
  "question": "Finding the version of the shipping policy that governs a case:\n- Default: the version in force on the case's complaint date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nGoing by the version history, what delivery promise does the governing version set for case CASE-8856?",
  "options": [
   "14 days",
   "5 days"
  ]
 },
 {
  "qid": "q90fe792a68",
  "kind": "choice",
  "text": "Sara Ilves: Hello, it is lovely to speak with you. I am calling to raise a case with Upland Utilities about my study block.\nagent: Hello, thank you for calling. Your case, CASE-9690, is right here on my screen.\n\nVersion table of the leave policy (end dates excluded):\nversion | replaces | in force from | in force to | paid leave allowance\nLP-833 | first version | Monday, 26 February 2024 | Sunday, 12 May 2024 | 10 days\nLP-517 | LP-833 | Sunday, 12 May 2024 | Thursday, 9 October 2025 | 15 days\nLP-671 | LP-517 | Thursday, 9 October 2025 | open-ended | 20 days\n\nCase CASE-9690:\n- hire date: Saturday, 2 August 2025\n- leave start date: Saturday, 16 August 2025\n- claim date: Monday, 15 September 2025\n- decision date: Thursday, 9 October 2025\n- number of leave days claimed: 11 days\nEnd of case record.",
  "question": "Finding the version of the leave policy that governs a case:\n- The governing version is the version in force on the case's hire date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, which listed version of leave policy is the governing version for case CASE-9690?",
  "options": [
   "LP-671",
   "LP-517"
  ]
 },
 {
  "qid": "qb7909e3d99",
  "kind": "choice",
  "text": "Mild frustration over language course for Nadia Kowal, CASE-3128\nNadia Kowal raised a polite case with Selkirk Logistics about a language course, and the details follow. The customer is a little annoyed but remains courteous while the matter is discussed.\n\nVersions of the refund policy (end dates included):\n- RP64: first version; in force from March 29, 2023 to October 4, 2023; refund window: 45 days.\n  Sunset clause of RP64: if RP64 would govern a case whose decision date is after February 1, 2024, RP70 governs it instead.\n- RP70: replaces RP64; in force from October 5, 2023, open-ended; refund window: 7 days.\n\nCase CASE-3128:\n- purchase date: October 3, 2023\n- delivery date: October 23, 2023\n- refund request date: October 29, 2023\n- decision date: February 1, 2024\n- day count from purchase to refund request: 26 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, which version of the refund policy is picked to govern this case?",
  "options": [
   "RP64",
   "RP70"
  ]
 },
 {
  "qid": "q6117d11f5a",
  "kind": "yes/no",
  "text": "customer: Theo Kalnins\ncase: CASE-2934\nitem: grocery order\nTheo Kalnins raised this case with Selkirk Logistics about the grocery order. Hope you are well, and the full details follow.\n\nVersion table of the shipping policy (end dates excluded):\nversion | replaces | in force from | in force to | delivery promise\nv1 | first version | January 23, 2023 | September 2, 2023 | 14 days\nv2 | v1 | September 2, 2023 | January 25, 2024 | 7 days\nv3 | v2 | January 25, 2024 | April 5, 2024 | 5 days\nv4 | v3 | April 5, 2024 | open-ended | 10 days\nTransition clause of v4: if v4 would govern a case whose delivery date is before April 5, 2024, the version in force on that delivery date governs it instead.\n\nCase CASE-2934:\n- order date: December 28, 2023\n- delivery date: January 3, 2024\n- complaint date: March 31, 2024\n- decision date: April 18, 2024\n- day count from order to delivery: 6 days\nEnd of case record.",
  "question": "Going by the version history, is this case not inside the delivery promise set by the governing version?",
  "definitions": "Finding the version of the shipping policy that governs a case:\n- Default: the version in force on the case's complaint date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the delivery promise when its day count from order to delivery is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q8303a65662",
  "kind": "choice",
  "text": "Sara Ilves: Hello, I am calling about my design suite. I raised a case with Mistral Home and I am feeling a little irritated and would value a clear explanation.\nagent: Hello. I have case CASE-9820 on file, so let us go through the design suite background.\n\nChange log of the licence terms, newest entry first:\n2024-06-11 | LT-30T takes effect, replacing LT-68Z | device limit: 1 device\n  Transition clause of LT-30T: if a version older than LT-30T would govern a case whose decision date is on or after 2024-06-11, LT-30T governs it instead.\n2024-04-06 | LT-68Z takes effect as the first version | device limit: 10 devices\n\nCase CASE-9820:\n- licence purchase date: 2024-04-11\n- activation date: 2024-04-12\n- support request date: 2024-09-17\n- decision date: 2025-03-05\n- number of devices registered: 2 devices\nEnd of case record.",
  "question": "Finding the version of the licence terms that governs a case:\n- Default: the version in force on the case's activation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nGoing by the version history, which version of the licence terms governs this case?",
  "options": [
   "LT-30T",
   "LT-68Z"
  ]
 },
 {
  "qid": "q1a46805c46",
  "kind": "yes/no",
  "text": "Dana Okafor: Hello, I am writing to raise a case with Veridia Health about my notes app.\nsupport: Hello. This matter sits under CASE-6013 alongside the routine notes.\nDana Okafor: Lovely, thank you.\n\nChange log of the licence terms, newest entry first:\n22 July 2023 | v2 takes effect, replacing v1 | device limit: 5 devices\n10 February 2023 | v1 takes effect as the first version | device limit: 10 devices\n\nCase CASE-6013:\n- licence purchase date: 15 May 2023\n- activation date: 22 July 2023\n- support request date: 15 December 2023\n- decision date: 10 May 2024\n- number of devices registered: 15 devices\n- claim to check: the device limit for this case is 10 devices\nEnd of case record.",
  "question": "Under these rules, does the governing version support the claim to check for device limit?",
  "definitions": "Finding the version of the licence terms that governs a case:\n- The governing version is the version in force on the case's activation date.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- A claim about the device limit is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q06c4afd1cd",
  "kind": "choice",
  "text": "Hi there,\nI am reaching out about my standing desk with Halvard Insurance, which is a calm and routine matter. My name is Yara Haddad and the case is logged as CASE-1739. The rest follows in the notes below.\nThanks,\n\nChange log of the refund policy, newest entry first:\nFriday, 29 December 2023 | RP-14G takes effect, replacing RP-37K | refund window: 14 days\n  Transition clause of RP-14G: if RP-14G would govern a case whose purchase date is before Friday, 29 December 2023, the version in force on that purchase date governs it instead.\nTuesday, 31 October 2023 | RP-37K takes effect, replacing RP-10T | refund window: 90 days\nSunday, 27 August 2023 | RP-10T takes effect as the first version | refund window: 28 days\n\nCase CASE-1739:\n- purchase date: Friday, 29 December 2023\n- delivery date: Wednesday, 17 January 2024\n- refund request date: Friday, 1 March 2024\n- decision date: Tuesday, 5 March 2024\n- day count from purchase to refund request: 63 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's refund request date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of refund policy governs case CASE-1739, given the rules on the card?",
  "options": [
   "RP-14G",
   "RP-10T"
  ]
 },
 {
  "qid": "qeefa264ea0",
  "kind": "choice",
  "text": "Internal case note: Kofi Mensah raised a case with Corran Telecom about a standing desk, and it is held under CASE-7634. The tone of the message has stayed steady and the background follows.\n\nVersions of the refund policy (end dates included):\n- rev-A: first version; in force from 15 July 2023 to 7 November 2023; refund window: 60 days.\n- rev-B: replaces rev-A; in force from 8 November 2023 to 19 July 2024; refund window: 45 days.\n- rev-C: replaces rev-B; in force from 20 July 2024 to 26 September 2024; refund window: 28 days.\n- rev-D: replaces rev-C; in force from 27 September 2024, open-ended; refund window: 30 days.\n  Transition clause of rev-D: if rev-D would govern a case whose delivery date is before 27 September 2024, the version in force on that delivery date governs it instead.\n\nCase CASE-7634:\n- purchase date: 20 July 2024\n- delivery date: 14 August 2024\n- refund request date: 26 December 2024\n- decision date: 6 June 2025\n- day count from purchase to refund request: 159 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhat refund window does the governing version of refund policy set for case CASE-7634?",
  "options": [
   "28 days",
   "30 days"
  ]
 },
 {
  "qid": "q10cc7e0f68",
  "kind": "choice",
  "text": "Internal case note: Ravi Anand raised a case with Veridia Health about a tyre order, and it is held under CASE-8798. The tone of the message has stayed steady and the background follows.\n\nVersions of the shipping policy (end dates excluded):\n- v1: first version; in force from Monday, 15 May 2023 to Wednesday, 13 December 2023; delivery promise: 7 days.\n- v2: replaces v1; in force from Wednesday, 13 December 2023 to Friday, 21 June 2024; delivery promise: 10 days.\n  Transition clause of v2: if v2 would govern a case whose order date is before Wednesday, 13 December 2023, the version in force on that order date governs it instead.\n- v3: replaces v2; in force from Friday, 21 June 2024, open-ended; delivery promise: 4 days.\n\nCase CASE-8798:\n- order date: Monday, 30 September 2024\n- delivery date: Sunday, 10 November 2024\n- complaint date: Thursday, 5 December 2024\n- decision date: Saturday, 10 May 2025\n- day count from order to delivery: 41 days\nEnd of case record.",
  "question": "Finding the version of the shipping policy that governs a case:\n- Default: the version in force on the case's complaint date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nGoing by the version history, what delivery promise does the governing version set for case CASE-8798?",
  "options": [
   "7 days",
   "4 days"
  ]
 },
 {
  "qid": "q9f841d1635",
  "kind": "choice",
  "text": "customer: Dana Okafor\norganisation: Lindenfeld Outfitters\ncase: CASE-4670\nDana Okafor raised this case about the camera recording. Some irritation shows, but the wording stays courteous, and the full details follow.\n\nVersion table of the records retention schedule (end dates included):\nversion | replaces | in force from | in force to | retention period\nRS-78F | first version | 12 Jul 2024 | 3 Sep 2024 | 60 days\nRS-40P | RS-78F | 4 Sep 2024 | 26 Dec 2024 | 180 days\nRS-61D | RS-40P | 27 Dec 2024 | open-ended | 30 days\nTransition clause of RS-40P: if a version older than RS-40P would govern a case whose decision date is on or after 4 Sep 2024, RS-40P governs it instead.\n\nCase CASE-4670:\n- record creation date: 20 Dec 2025\n- record closure date: 17 Jan 2026\n- deletion request date: 20 Feb 2026\n- decision date: 20 Feb 2026\n- day count from record closure to deletion request: 34 days\nEnd of case record.",
  "question": "Finding the version of the records retention schedule that governs a case:\n- Default: the version in force on the case's record creation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of records retention schedule governs case CASE-4670 after the card's rules are followed?",
  "options": [
   "RS-61D",
   "RS-40P"
  ]
 },
 {
  "qid": "qe9f3f5fb56",
  "kind": "choice",
  "text": "Dear team,\nI write to raise a formal case with Mistral Home about my savings account. My name is Ana Ruiz and the case identifier is CASE-7148. I appreciate your attention, and the details are set out below.\nYours sincerely,\n\nChange log of the fee schedule, newest entry first:\nWednesday, March 5, 2025 | FS-68F takes effect, replacing FS-17J | fee cap: $40.00\nTuesday, November 19, 2024 | FS-17J takes effect as the first version | fee cap: $20.00\n  Sunset clause of FS-17J: if FS-17J would govern a case whose decision date is after Tuesday, September 16, 2025, FS-68F governs it instead.\n\nCase CASE-7148:\n- account opening date: Thursday, January 30, 2025\n- billing date: Sunday, February 16, 2025\n- dispute date: Thursday, June 5, 2025\n- decision date: Monday, October 20, 2025\n- fee charged: $22.00\nEnd of case record.",
  "question": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's billing date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of fee schedule governs case CASE-7148, given the rules on the card?",
  "options": [
   "FS-68F",
   "FS-17J"
  ]
 },
 {
  "qid": "q1447f1219f",
  "kind": "choice",
  "text": "case: CASE-7189\ncustomer: Nadia Kowal\nitem: meal kit plan\nThe customer wrote to Upland Utilities about the meal kit plan in a bright and upbeat way. All involved are pleased to take the matter forward.\n\nVersions of the subscription terms (end dates included):\n- ST-792: first version; in force from 2024-10-07 to 2025-05-18; free cancellation period: 3 days.\n  Sunset clause of ST-792: if ST-792 would govern a case whose decision date is after 2025-10-07, ST-458 governs it instead.\n- ST-458: replaces ST-792; in force from 2025-05-19, open-ended; free cancellation period: 5 days.\n\nCase CASE-7189:\n- sign-up date: 2025-01-15\n- renewal date: 2025-02-26\n- cancellation date: 2025-03-21\n- decision date: 2025-10-08\n- day count from sign-up to cancellation: 65 days\nEnd of case record.",
  "question": "Finding the version of the subscription terms that governs a case:\n- Default: the version in force on the case's renewal date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAcross the subscription terms versions, which version governs case CASE-7189?",
  "options": [
   "ST-458",
   "ST-792"
  ]
 },
 {
  "qid": "q1c95c09b72",
  "kind": "choice",
  "text": "Routine matter logged for internal use. Mira Castell raised case CASE-7594 with Tamsin Fitness about a streaming plan. The mood is calm, and the case details follow below.\n\nVersion table of the subscription terms (end dates included):\nversion | replaces | in force from | in force to | free cancellation period\nrev-A | first version | 28 April 2024 | 17 September 2024 | 14 days\nrev-B | rev-A | 18 September 2024 | 6 April 2025 | 21 days\nrev-C | rev-B | 7 April 2025 | 6 January 2026 | 30 days\nrev-D | rev-C | 7 January 2026 | open-ended | 7 days\nTransition clause of rev-B: if rev-B would govern a case whose sign-up date is before 18 September 2024, the version in force on that sign-up date governs it instead.\n\nCase CASE-7594:\n- sign-up date: 18 September 2024\n- renewal date: 20 October 2024\n- cancellation date: 7 November 2024\n- decision date: 15 November 2024\n- day count from sign-up to cancellation: 50 days\nEnd of case record.",
  "question": "Finding the version of the subscription terms that governs a case:\n- Default: the version in force on the case's renewal date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, which free cancellation period does the governing version of subscription terms set for case CASE-7594?",
  "options": [
   "14 days",
   "21 days"
  ]
 },
 {
  "qid": "q86e3008c75",
  "kind": "yes/no",
  "text": "Gym membership case for Kofi Mensah\nKofi Mensah raised a case with Pembroke Travel about a merchant account, filed as CASE-6475. The history and details are set out below, and the customer is a little frustrated but polite.\n\nVersion table of the fee schedule (end dates included):\nversion | replaces | in force from | in force to | fee cap\nFS-850 | first version | October 7, 2024 | July 11, 2025 | $20.00\nFS-704 | FS-850 | July 12, 2025 | October 20, 2025 | $50.00\nFS-171 | FS-704 | October 21, 2025 | open-ended | $25.00\nTransition clause of FS-171: if FS-171 would govern a case whose account opening date is before October 21, 2025, the version in force on that account opening date governs it instead.\n\nCase CASE-6475:\n- account opening date: September 25, 2025\n- billing date: February 19, 2026\n- dispute date: May 15, 2026\n- decision date: June 13, 2026\n- fee charged: $50.01\nEnd of case record.",
  "question": "Is this case not within the fee cap the governing version sets, for case CASE-6475?",
  "definitions": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's dispute date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the fee cap when its fee charged is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q74b6e38951",
  "kind": "choice",
  "text": "customer: Aiko Brandt\ncompany: Mistral Home\ncase: CASE-7816\nAiko Brandt is a little irritated but polite and has raised a case with Mistral Home about the card account.\n\nVersions of the fee schedule (end dates included):\n- FS-62X: first version; in force from 15 Nov 2024 to 22 Aug 2025; fee cap: $20.00.\n- FS-95G: replaces FS-62X; in force from 23 Aug 2025 to 28 Mar 2026; fee cap: $35.00.\n- FS-26J: replaces FS-95G; in force from 29 Mar 2026 to 12 Jan 2027; fee cap: $40.00.\n  Transition clause of FS-26J: if FS-26J would govern a case whose account opening date is before 29 Mar 2026, the version in force on that account opening date governs it instead.\n- FS-66R: replaces FS-26J; in force from 13 Jan 2027, open-ended; fee cap: $25.00.\n\nCase CASE-7816:\n- account opening date: 7 Jan 2026\n- billing date: 23 Jul 2026\n- dispute date: 6 Nov 2026\n- decision date: 19 Dec 2026\n- fee charged: $90.00\nEnd of case record.",
  "question": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's dispute date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of fee schedule governs case CASE-7816 after the card's rules are followed?",
  "options": [
   "FS-95G",
   "FS-26J"
  ]
 },
 {
  "qid": "q53e50e2223",
  "kind": "choice",
  "text": "Dana Okafor has raised a case with Lindenfeld Outfitters about a camera recording, filed as CASE-4670. The background and details of the matter follow in this file. Matters of this kind are set out formally and briefly.\n\nVersion table of the records retention schedule (end dates included):\nversion | replaces | in force from | in force to | retention period\nRS-78F | first version | 12 Jul 2024 | 3 Sep 2024 | 60 days\nRS-40P | RS-78F | 4 Sep 2024 | 20 Feb 2026 | 180 days\nRS-61D | RS-40P | 21 Feb 2026 | open-ended | 30 days\nTransition clause of RS-40P: if a version older than RS-40P would govern a case whose decision date is on or after 4 Sep 2024, RS-40P governs it instead.\n\nCase CASE-4670:\n- record creation date: 20 Dec 2025\n- record closure date: 17 Jan 2026\n- deletion request date: 20 Feb 2026\n- decision date: 20 Feb 2026\n- day count from record closure to deletion request: 34 days\nEnd of case record.",
  "question": "Finding the version of the records retention schedule that governs a case:\n- Default: the version in force on the case's record creation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of records retention schedule governs case CASE-4670 after the card's rules are followed?",
  "options": [
   "RS-40P",
   "RS-61D"
  ]
 },
 {
  "qid": "q8a3546edc6",
  "kind": "yes/no",
  "text": "Formal record: Tomas Lindqvist raised case CASE-9141 with Veridia Health about a client visit. Matter recorded briefly for internal use. Full details follow in the case file.\n\nVersions of the travel policy (end dates included):\n- TP-157: first version; in force from 2023-12-11 to 2024-06-11; nightly hotel cap: 250.00 USD.\n  Sunset clause of TP-157: if TP-157 would govern a case whose decision date is after 2025-02-10, TP-866 governs it instead.\n- TP-866: replaces TP-157; in force from 2024-06-12, open-ended; nightly hotel cap: 200.00 USD.\n\nCase CASE-9141:\n- booking date: 2024-06-12\n- travel date: 2024-06-18\n- expense claim date: 2024-12-22\n- decision date: 2024-12-23\n- nightly rate claimed: 166.00 USD\nEnd of case record.",
  "question": "Going by the version history, is the governing version for case CASE-9141 in travel policy exactly TP-866?",
  "definitions": "Finding the version of the travel policy that governs a case:\n- Default: the version in force on the case's booking date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q478c5c5b08",
  "kind": "yes/no",
  "text": "name: Aiko Brandt\ncompany: Lindenfeld Outfitters\ncase: CASE-3927\nAiko Brandt is somewhat exasperated but polite, having raised a case with Lindenfeld Outfitters about the language course. The full background follows.\n\nVersions of the refund policy (end dates included):\n- v1: first version; in force from Monday, March 4, 2024 to Monday, September 23, 2024; refund window: 10 days.\n- v2: replaces v1; in force from Tuesday, September 24, 2024 to Monday, March 17, 2025; refund window: 90 days.\n- v3: replaces v2; in force from Tuesday, March 18, 2025, open-ended; refund window: 21 days.\n  Transition clause of v3: if v3 would govern a case whose purchase date is before Tuesday, March 18, 2025, the version in force on that purchase date governs it instead.\n\nCase CASE-3927:\n- purchase date: Thursday, October 31, 2024\n- delivery date: Friday, November 1, 2024\n- refund request date: Saturday, November 2, 2024\n- decision date: Friday, May 16, 2025\n- day count from purchase to refund request: 2 days\nEnd of case record.",
  "question": "Under these rules, does v2 not govern case CASE-3927 of refund policy?",
  "definitions": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q3be5b3b07f",
  "kind": "choice",
  "text": "Client visit case for Malik Osei\nMalik Osei raised case CASE-8061 with Lindenfeld Outfitters about a news subscription. A touch of frustration shows, but the wording is courteous throughout.\n\nVersions of the subscription terms (end dates included):\n- v1: first version; in force from Tuesday, 5 March 2024 to Friday, 23 August 2024; free cancellation period: 7 days.\n- v2: replaces v1; in force from Saturday, 24 August 2024 to Thursday, 21 November 2024; free cancellation period: 14 days.\n- v3: replaces v2; in force from Friday, 22 November 2024 to Tuesday, 27 May 2025; free cancellation period: 5 days.\n  Sunset clause of v3: if v3 would govern a case whose decision date is after Wednesday, 28 May 2025, v4 governs it instead.\n- v4: replaces v3; in force from Wednesday, 28 May 2025, open-ended; free cancellation period: 3 days.\n\nCase CASE-8061:\n- sign-up date: Saturday, 8 February 2025\n- renewal date: Monday, 17 February 2025\n- cancellation date: Tuesday, 18 February 2025\n- decision date: Thursday, 29 May 2025\n- day count from sign-up to cancellation: 10 days\nEnd of case record.",
  "question": "Finding the version of the subscription terms that governs a case:\n- Default: the version in force on the case's renewal date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich free cancellation period would the governing version of subscription terms assign to case CASE-8061?",
  "options": [
   "5 days",
   "3 days"
  ]
 },
 {
  "qid": "q18e1ce4150",
  "kind": "choice",
  "text": "case: CASE-8982\ncontact: Lena Whitcombe\nitem: family visit\nA polite but slightly irritated case was raised with Tamsin Fitness about the family visit. The details follow in the usual way.\n\nVersions of the leave policy (end dates excluded):\n- LP-22W: first version; in force from 18 Oct 2023 to 27 Jun 2024; paid leave allowance: 15 days.\n- LP-64C: replaces LP-22W; in force from 27 Jun 2024 to 23 Oct 2024; paid leave allowance: 10 days.\n- LP-80K: replaces LP-64C; in force from 23 Oct 2024 to 28 Jan 2025; paid leave allowance: 30 days.\n  Sunset clause of LP-80K: if LP-80K would govern a case whose decision date is after 4 Aug 2025, LP-15G governs it instead.\n- LP-15G: replaces LP-80K; in force from 28 Jan 2025, open-ended; paid leave allowance: 20 days.\n\nCase CASE-8982:\n- hire date: 10 Nov 2024\n- leave start date: 11 Nov 2024\n- claim date: 21 Nov 2024\n- decision date: 4 Aug 2025\n- number of leave days claimed: 28 days\nEnd of case record.",
  "question": "Finding the version of the leave policy that governs a case:\n- Default: the version in force on the case's hire date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nFor case CASE-8982, which version of leave policy governs according to the card?",
  "options": [
   "LP-80K",
   "LP-22W"
  ]
 },
 {
  "qid": "qb8265eaee4",
  "kind": "choice",
  "text": "Nadia Kowal: Hello. I raised a case with Selkirk Logistics about my conference trip, and I would like it looked into.\nsupport: Hello. I have case CASE-4162 on file and the conference trip details follow.\n\nChange log of the travel policy, newest entry first:\n2024-10-18 | TP-881 takes effect, replacing TP-984 | nightly hotel cap: $250.00\n2024-03-27 | TP-984 takes effect, replacing TP-908 | nightly hotel cap: $150.00\n  Sunset clause of TP-984: if TP-984 would govern a case whose decision date is after 2025-04-29, TP-881 governs it instead.\n2023-07-19 | TP-908 takes effect as the first version | nightly hotel cap: $120.00\n\nCase CASE-4162:\n- booking date: 2024-08-01\n- travel date: 2024-09-19\n- expense claim date: 2024-12-26\n- decision date: 2025-04-29\n- nightly rate claimed: $354.00\nEnd of case record.",
  "question": "Finding the version of the travel policy that governs a case:\n- Default: the version in force on the case's booking date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, which version of travel policy is the controlling version for case CASE-4162?",
  "options": [
   "TP-984",
   "TP-908"
  ]
 },
 {
  "qid": "qf8a1882dd3",
  "kind": "yes/no",
  "text": "Customer case CASE-6934 for Jonas Feld\nJonas Feld is a warm, chatty sort who has raised a case with Veridia Health about the support transcript. The case details are laid out below.\n\nVersion table of the records retention schedule (end dates included):\nversion | replaces | in force from | in force to | retention period\nv1 | first version | 1 August 2024 | 12 January 2026 | 365 days\nv2 | v1 | 13 January 2026 | 16 January 2026 | 30 days\nv3 | v2 | 17 January 2026 | open-ended | 90 days\nTransition clause of v3: if v3 would govern a case whose record creation date is before 17 January 2026, the version in force on that record creation date governs it instead.\n\nCase CASE-6934:\n- record creation date: 12 January 2026\n- record closure date: 2 February 2026\n- deletion request date: 8 April 2026\n- decision date: 15 July 2026\n- day count from record closure to deletion request: 65 days\nEnd of case record.",
  "question": "Is the case within the retention period set by the governing version of records retention schedule?",
  "definitions": "Finding the version of the records retention schedule that governs a case:\n- Default: the version in force on the case's record creation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the retention period when its day count from record closure to deletion request is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qa0c07af584",
  "kind": "choice",
  "text": "Dear Hana Sato,\nThank you for raising case CASE-2513 with Mistral Home about your client visit. This is a routine matter, and the full details follow below.\nKind regards\n\nVersions of the travel policy (end dates included):\n- v1: first version; in force from August 18, 2023 to July 1, 2024; nightly hotel cap: $200.00.\n- v2: replaces v1; in force from July 2, 2024, open-ended; nightly hotel cap: $150.00.\n\nCase CASE-2513:\n- booking date: July 1, 2024\n- travel date: January 4, 2025\n- expense claim date: June 30, 2025\n- decision date: August 26, 2025\n- nightly rate claimed: $97.00\nEnd of case record.",
  "question": "Finding the version of the travel policy that governs a case:\n- The governing version is the version in force on the case's booking date.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhat setting for the nightly hotel cap does the governing version of travel policy specify for case CASE-2513?",
  "options": [
   "$150.00",
   "$200.00"
  ]
 },
 {
  "qid": "q024fc2eb18",
  "kind": "choice",
  "text": "Nadia Kowal: Hi there, I am calling about my camera bag. I raised a case with Veridia Health and I wanted to say thank you for taking it on.\nagent: Hello there, so good to speak with you. I have case CASE-4270 on file, so let us go through the camera bag together.\n\nChange log of the refund policy, newest entry first:\nMarch 26, 2024 | RP-45X takes effect, replacing RP-15J | refund window: 60 days\nDecember 23, 2023 | RP-15J takes effect, replacing RP-31K | refund window: 10 days\n  Sunset clause of RP-15J: if RP-15J would govern a case whose decision date is after April 8, 2024, RP-45X governs it instead.\nOctober 13, 2023 | RP-31K takes effect as the first version | refund window: 90 days\n\nCase CASE-4270:\n- purchase date: October 13, 2023\n- delivery date: October 13, 2023\n- refund request date: December 22, 2023\n- decision date: June 22, 2024\n- day count from purchase to refund request: 70 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's refund request date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, which version of the refund policy takes precedence for this case?",
  "options": [
   "RP-45X",
   "RP-31K"
  ]
 },
 {
  "qid": "qb40bf2f8d9",
  "kind": "yes/no",
  "text": "case: CASE-1356\ncustomer: Tomas Lindqvist\nitem: support transcript\nThe customer kindly raised a case with Selkirk Logistics about the support transcript, and the details follow. The tone of the message is upbeat and cheerful throughout.\n\nVersions of the records retention schedule (end dates included):\n- RS-319: first version; in force from 4 Oct 2024 to 22 Jul 2025; retention period: 365 days.\n- RS-678: replaces RS-319; in force from 23 Jul 2025 to 12 Jan 2026; retention period: 730 days.\n- RS-745: replaces RS-678; in force from 13 Jan 2026, open-ended; retention period: 90 days.\n  Transition clause of RS-745: if a version older than RS-745 would govern a case whose decision date is on or after 13 Jan 2026, RS-745 governs it instead.\n\nCase CASE-1356:\n- record creation date: 17 Jun 2025\n- record closure date: 18 Oct 2025\n- deletion request date: 12 Nov 2025\n- decision date: 12 Jan 2026\n- day count from record closure to deletion request: 25 days\nEnd of case record.",
  "question": "According to the card, does RS-745 turn out to be the governing version for case CASE-1356 of records retention schedule?",
  "definitions": "Finding the version of the records retention schedule that governs a case:\n- Default: the version in force on the case's record closure date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q824462ecc7",
  "kind": "yes/no",
  "text": "Hello,\nMy name is Ana Ruiz and I am writing to raise a case with Upland Utilities about my design suite. The matter is routine and the history follows below under CASE-5446.\nBest regards,\n\nVersions of the licence terms (end dates excluded):\n- LT-584: first version; in force from May 25, 2024 to October 28, 2024; device limit: 1 device.\n- LT-891: replaces LT-584; in force from October 28, 2024, open-ended; device limit: 3 devices.\n  Transition clause of LT-891: if LT-891 would govern a case whose activation date is before October 28, 2024, the version in force on that activation date governs it instead.\n\nCase CASE-5446:\n- licence purchase date: October 23, 2024\n- activation date: October 28, 2024\n- support request date: December 19, 2024\n- decision date: December 19, 2024\n- number of devices registered: 2 devices\nEnd of case record.",
  "question": "Is it the case that it is not the case that LT-584 does not settle this case?",
  "definitions": "Finding the version of the licence terms that governs a case:\n- Default: the version in force on the case's activation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q5f292842a5",
  "kind": "yes/no",
  "text": "Customer case CASE-7838 for Priya Raman\nPriya Raman is a warm, chatty sort who has raised a case with Mistral Home about the language course. The case details are laid out below.\n\nVersions of the refund policy (end dates included):\n- rev-A: first version; in force from 2023-03-21 to 2023-12-04; refund window: 14 days.\n- rev-B: replaces rev-A; in force from 2023-12-05, open-ended; refund window: 10 days.\n  Transition clause of rev-B: if a version older than rev-B would govern a case whose decision date is on or after 2023-12-05, rev-B governs it instead.\n\nCase CASE-7838:\n- purchase date: 2023-10-03\n- delivery date: 2023-12-04\n- refund request date: 2023-12-04\n- decision date: 2023-12-04\n- day count from purchase to refund request: 62 days\nEnd of case record.",
  "question": "According to the card, is rev-B the version that governs this case?",
  "definitions": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qc46e6b2296",
  "kind": "choice",
  "text": "Sara Ilves and the meal kit plan\nSara Ilves raised case CASE-9844 with Brightwell Supply about a meal kit plan. Mild impatience comes through, but the customer stays civil and the details follow.\n\nVersions of the subscription terms (end dates included):\n- ST-657: first version; in force from Tuesday, 14 May 2024 to Sunday, 9 February 2025; free cancellation period: 3 days.\n- ST-413: replaces ST-657; in force from Monday, 10 February 2025 to Wednesday, 4 June 2025; free cancellation period: 7 days.\n- ST-725: replaces ST-413; in force from Thursday, 5 June 2025, open-ended; free cancellation period: 5 days.\n  Transition clause of ST-725: if a version older than ST-725 would govern a case whose decision date is on or after Thursday, 5 June 2025, ST-725 governs it instead.\n\nCase CASE-9844:\n- sign-up date: Friday, 5 September 2025\n- renewal date: Tuesday, 7 October 2025\n- cancellation date: Monday, 27 October 2025\n- decision date: Friday, 20 March 2026\n- day count from sign-up to cancellation: 52 days\nEnd of case record.",
  "question": "Finding the version of the subscription terms that governs a case:\n- Default: the version in force on the case's renewal date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nGoing by the version history, what free cancellation period does the governing version set for case CASE-9844 in subscription terms?",
  "options": [
   "5 days",
   "3 days"
  ]
 },
 {
  "qid": "qd21218554f",
  "kind": "yes/no",
  "text": "Tomas Lindqvist: Hi there, I am calling about my printer toner. I raised case CASE-6093 with Brightwell Supply, and it is nice to be in touch.\nagent: Hi Tomas Lindqvist, so good to speak with you. The full details follow.\n\nVersion table of the price list (end dates excluded):\nversion | replaces | in force from | in force to | price cap per unit\nv1 | first version | 17 Nov 2023 | 11 Jun 2024 | 12.50 USD\nv2 | v1 | 11 Jun 2024 | 29 Jan 2025 | 14.99 USD\nv3 | v2 | 29 Jan 2025 | 6 Sep 2025 | 35.00 USD\nv4 | v3 | 6 Sep 2025 | open-ended | 29.99 USD\n\nCase CASE-6093:\n- contract date: 17 Nov 2023\n- delivery date: 29 Dec 2023\n- invoice date: 1 Jan 2024\n- decision date: 23 Jan 2024\n- unit price charged: 15.00 USD\n- claim to check: the price cap per unit for this case is 12.50 USD\nEnd of case record.",
  "question": "Going by the version history, does the governing version support the claim recorded for case CASE-6093?",
  "definitions": "Finding the version of the price list that governs a case:\n- The governing version is the version in force on the case's delivery date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- A claim about the price cap per unit is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q73fc92b78d",
  "kind": "yes/no",
  "text": "Malik Osei: Hello, I wish to make a formal note about my antivirus licence from Tamsin Fitness.\nsupport: Hello. The case CASE-4071 has been filed and the antivirus licence background is being gathered.\n\nChange log of the licence terms, newest entry first:\nMarch 14, 2024 | LT-478 takes effect, replacing LT-500 | device limit: 2 devices\nMay 7, 2023 | LT-500 takes effect as the first version | device limit: 3 devices\n  Sunset clause of LT-500: if LT-500 would govern a case whose decision date is after April 4, 2024, LT-478 governs it instead.\n\nCase CASE-4071:\n- licence purchase date: May 7, 2023\n- activation date: May 12, 2023\n- support request date: May 12, 2023\n- decision date: April 11, 2024\n- number of devices registered: 2 devices\nEnd of case record.",
  "question": "Does the quantity in case CASE-4071 exceed the device limit set by the governing version of licence terms?",
  "definitions": "Finding the version of the licence terms that governs a case:\n- Default: the version in force on the case's activation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the device limit when its number of devices registered is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qf554de1acf",
  "kind": "yes/no",
  "text": "Internal case note: Ana Ruiz raised a formal case with Corran Telecom about a laptop. The case is recorded under CASE-6641. Background details follow in brief, set out in a concise and orderly format.\n\nVersions of the warranty terms (end dates excluded):\n- WT-970: first version; in force from Monday, March 18, 2024 to Sunday, January 19, 2025; warranty period: 60 days.\n- WT-932: replaces WT-970; in force from Sunday, January 19, 2025 to Friday, August 8, 2025; warranty period: 365 days.\n- WT-181: replaces WT-932; in force from Friday, August 8, 2025, open-ended; warranty period: 730 days.\n\nCase CASE-6641:\n- purchase date: Thursday, December 4, 2025\n- fault date: Saturday, February 14, 2026\n- claim date: Saturday, February 21, 2026\n- decision date: Sunday, May 3, 2026\n- day count from purchase to fault: 72 days\nEnd of case record.",
  "question": "Is WT-181 the governing version for the case CASE-6641 recorded under warranty terms?",
  "definitions": "Finding the version of the warranty terms that governs a case:\n- The governing version is the version in force on the case's fault date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q9224a67dd3",
  "kind": "choice",
  "text": "customer: Lena Whitcombe\ncompany: Veridia Health\ncase: CASE-4903\nLena Whitcombe is a little irritated but polite and has raised a case with Veridia Health about the camera bag.\n\nVersions of the refund policy (end dates included):\n- RP-570: first version; in force from 18 April 2024 to 4 January 2025; refund window: 7 days.\n- RP-307: replaces RP-570; in force from 5 January 2025, open-ended; refund window: 14 days.\n  Transition clause of RP-307: if RP-307 would govern a case whose delivery date is before 5 January 2025, the version in force on that delivery date governs it instead.\n\nCase CASE-4903:\n- purchase date: 2 September 2024\n- delivery date: 5 November 2024\n- refund request date: 4 January 2025\n- decision date: 22 March 2025\n- day count from purchase to refund request: 124 days\nEnd of case record.",
  "question": "Finding the version of the refund policy that governs a case:\n- Default: the version in force on the case's refund request date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAmong the versions of refund policy, which governs case CASE-4903?",
  "options": [
   "RP-307",
   "RP-570"
  ]
 },
 {
  "qid": "q4abf4e768a",
  "kind": "choice",
  "text": "Formal record: Jonas Feld raised case CASE-3447 with Quayside Software about a payroll record. Matter recorded briefly for internal use. Full details follow in the case file.\n\nVersions of the records retention schedule (end dates included):\n- RS21: first version; in force from April 16, 2024 to October 1, 2024; retention period: 365 days.\n- RS92: replaces RS21; in force from October 2, 2024, open-ended; retention period: 180 days.\n\nCase CASE-3447:\n- record creation date: October 2, 2024\n- record closure date: October 2, 2024\n- deletion request date: October 30, 2024\n- decision date: November 21, 2024\n- day count from record closure to deletion request: 28 days\nEnd of case record.",
  "question": "Finding the version of the records retention schedule that governs a case:\n- The governing version is the version in force on the case's record closure date.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, which listed version of records retention schedule is the governing version for case CASE-3447?",
  "options": [
   "RS21",
   "RS92"
  ]
 },
 {
  "qid": "q2bde512402",
  "kind": "yes/no",
  "text": "Customer case CASE-3052 for Sara Ilves\nSara Ilves has very kindly raised a case with Veridia Health about the washing machine. Everything relevant is set out below, with the story told in order.\n\nVersions of the warranty terms (end dates excluded):\n- WT-991: first version; in force from 2023-02-25 to 2023-07-19; warranty period: 30 days.\n- WT-251: replaces WT-991; in force from 2023-07-19 to 2024-03-03; warranty period: 365 days.\n  Transition clause of WT-251: if WT-251 would govern a case whose fault date is before 2023-07-19, the version in force on that fault date governs it instead.\n- WT-183: replaces WT-251; in force from 2024-03-03, open-ended; warranty period: 90 days.\n\nCase CASE-3052:\n- purchase date: 2023-06-27\n- fault date: 2023-07-19\n- claim date: 2023-08-01\n- decision date: 2023-10-23\n- day count from purchase to fault: 22 days\n- claim to check: the warranty period for this case is 90 days\nEnd of case record.",
  "question": "Does the claim to check for this case match the value set by the governing version?",
  "definitions": "Finding the version of the warranty terms that governs a case:\n- Default: the version in force on the case's fault date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- A claim about the warranty period is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 }
]
