# G5-H blind read T23-blind_read-7998b64f-002 (family T23)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T23/qc/g5h/answers/T23-blind_read-7998b64f-002.json

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
  "qid": "qbf8f525453",
  "kind": "choice",
  "text": "name: Tomas Lindqvist\ncompany: Veridia Health\ncase: CASE-3439\nTomas Lindqvist is somewhat exasperated but polite, having raised a case with Veridia Health about the current account. The full background follows.\n\nVersion table of the fee schedule (end dates included):\nversion | replaces | in force from | in force to | fee cap\nFS-32T | first version | Monday, 6 March 2023 | Friday, 28 April 2023 | 50.00 USD\nFS-56K | FS-32T | Saturday, 29 April 2023 | Tuesday, 6 June 2023 | 15.00 USD\nFS-16B | FS-56K | Wednesday, 7 June 2023 | open-ended | 75.00 USD\nTransition clause of FS-16B: if FS-16B would govern a case whose account opening date is before Wednesday, 7 June 2023, the version in force on that account opening date governs it instead.\n\nCase CASE-3439:\n- account opening date: Wednesday, 7 June 2023\n- billing date: Sunday, 24 March 2024\n- dispute date: Monday, 15 April 2024\n- decision date: Sunday, 29 September 2024\n- fee charged: 18.00 USD\nEnd of case record.",
  "question": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's dispute date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of fee schedule do the card's rules pick for case CASE-3439?",
  "options": [
   "FS-16B",
   "FS-32T"
  ]
 },
 {
  "qid": "q3163d11be6",
  "kind": "choice",
  "text": "Sara Ilves: Sorry to bother you, this is about a design suite from Pembroke Travel, reference CASE-3677.\nagent: Of course, the history and case details are pasted below.\n\nChange log of the licence terms, newest entry first:\n2026-11-11 | v3 takes effect, replacing v2 | device limit: 1 device\n2024-12-03 | v2 takes effect, replacing v1 | device limit: 10 devices\n  Transition clause of v2: if a version older than v2 would govern a case whose decision date is on or after 2024-12-03, v2 governs it instead.\n2024-07-09 | v1 takes effect as the first version | device limit: 3 devices\n\nCase CASE-3677:\n- licence purchase date: 2026-06-03\n- activation date: 2026-11-10\n- support request date: 2026-11-16\n- decision date: 2026-12-05\n- number of devices registered: 1 device\nEnd of case record.",
  "question": "Finding the version of the licence terms that governs a case:\n- Default: the version in force on the case's activation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, what device limit does the governing version set for this case?",
  "options": [
   "3 devices",
   "10 devices"
  ]
 },
 {
  "qid": "q97c77eae71",
  "kind": "yes/no",
  "text": "{\"customer\": \"Malik Osei\", \"company\": \"Quayside Software\", \"topic\": \"office chair\", \"team\": \"customer support desk\", \"note\": \"routine check, reference CASE-2069, history and case details follow\"}\n\nVersions of the price list (end dates excluded):\n- PL-316: first version; in force from Sunday, 19 March 2023 to Saturday, 18 November 2023; price cap per unit: $14.99.\n- PL-974: replaces PL-316; in force from Saturday, 18 November 2023 to Wednesday, 25 September 2024; price cap per unit: $29.99.\n- PL-304: replaces PL-974; in force from Wednesday, 25 September 2024, open-ended; price cap per unit: $19.99.\n\nCase CASE-2069:\n- contract date: Tuesday, 3 September 2024\n- delivery date: Tuesday, 24 September 2024\n- invoice date: Wednesday, 25 September 2024\n- decision date: Tuesday, 18 March 2025\n- unit price charged: $20.00\nEnd of case record.",
  "question": "According to the card, is case CASE-2069 within the price cap per unit set by the governing version of price list?",
  "definitions": "Finding the version of the price list that governs a case:\n- The governing version is the version in force on the case's invoice date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- The case is within the price cap per unit when its unit price charged is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q2efb0ebedf",
  "kind": "choice",
  "text": "Dana Okafor: Hi, stuck with the site audit from Veridia Health, so please help from IT.\nsupport: Lovely, IT here. The history and the case details are pasted below.\n\nChange log of the travel policy, newest entry first:\n12 August 2024 | TP-683 takes effect, replacing TP-696 | nightly hotel cap: 120.00 USD\n  Transition clause of TP-683: if TP-683 would govern a case whose booking date is before 12 August 2024, the version in force on that booking date governs it instead.\n29 September 2023 | TP-696 takes effect as the first version | nightly hotel cap: 250.00 USD\n\nCase CASE-8992:\n- booking date: 13 October 2023\n- travel date: 27 October 2023\n- expense claim date: 31 January 2024\n- decision date: 27 February 2024\n- nightly rate claimed: 163.00 USD\nEnd of case record.",
  "question": "Finding the version of the travel policy that governs a case:\n- Default: the version in force on the case's booking date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nFor case CASE-8992, which version of travel policy governs according to the card?",
  "options": [
   "TP-696",
   "TP-683"
  ]
 },
 {
  "qid": "q6110c7b81c",
  "kind": "choice",
  "text": "Subject: Your accounts file\nDear Priya Raman,\nYou raised a case with Quayside Software about a merchant account, and the history and case details are set out below.\nKind regards.\n\nChange log of the fee schedule, newest entry first:\nWednesday, December 25, 2024 | FS-410 takes effect, replacing FS-166 | fee cap: $40.00\n  Transition clause of FS-410: if a version older than FS-410 would govern a case whose decision date is on or after Wednesday, December 25, 2024, FS-410 governs it instead.\nFriday, June 21, 2024 | FS-166 takes effect as the first version | fee cap: $75.00\n\nCase CASE-7234:\n- account opening date: Thursday, October 3, 2024\n- billing date: Friday, October 25, 2024\n- dispute date: Monday, November 4, 2024\n- decision date: Monday, November 25, 2024\n- fee charged: $21.00\nEnd of case record.",
  "question": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's billing date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nGoing by the version history, what fee cap does the governing version set for case CASE-7234?",
  "options": [
   "$75.00",
   "$40.00"
  ]
 },
 {
  "qid": "q85369f50f5",
  "kind": "choice",
  "text": "Raising a service matter at the counter\nKofi Mensah raised a case with Mistral Home about the grocery order, reference CASE-1332. The history and the case details are pasted below.\n\nVersions of the shipping policy (end dates excluded):\n- SP29: first version; in force from November 24, 2023 to July 16, 2024; delivery promise: 14 days.\n- SP94: replaces SP29; in force from July 16, 2024 to October 8, 2024; delivery promise: 4 days.\n- SP62: replaces SP94; in force from October 8, 2024, open-ended; delivery promise: 3 days.\n  Transition clause of SP62: if SP62 would govern a case whose delivery date is before October 8, 2024, the version in force on that delivery date governs it instead.\n\nCase CASE-1332:\n- order date: October 8, 2024\n- delivery date: October 8, 2024\n- complaint date: June 27, 2025\n- decision date: October 28, 2025\n- day count from order to delivery: 0 days\nEnd of case record.",
  "question": "Finding the version of the shipping policy that governs a case:\n- Default: the version in force on the case's complaint date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, which version of the shipping policy governs this case?",
  "options": [
   "SP29",
   "SP62"
  ]
 },
 {
  "qid": "qd7d75f17ff",
  "kind": "choice",
  "text": "Subject: Your case about the merchant account\nHi Ana Ruiz,\nThe Upland Utilities customer care team has your message. The history and the case details are pasted below.\nTake care.\n\nChange log of the fee schedule, newest entry first:\nMarch 27, 2024 | FS-92M takes effect, replacing FS-94C | fee cap: 75.00 USD\n  Transition clause of FS-92M: if FS-92M would govern a case whose account opening date is before March 27, 2024, the version in force on that account opening date governs it instead.\nJanuary 18, 2024 | FS-94C takes effect as the first version | fee cap: 35.00 USD\n\nCase CASE-3924:\n- account opening date: March 27, 2024\n- billing date: March 31, 2024\n- dispute date: April 12, 2024\n- decision date: April 21, 2024\n- fee charged: 71.00 USD\nEnd of case record.",
  "question": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's billing date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of fee schedule does the card say governs case CASE-3924?",
  "options": [
   "FS-92M",
   "FS-94C"
  ]
 },
 {
  "qid": "q6ffa5c302c",
  "kind": "yes/no",
  "text": "customer: Lucas Brenner\ncompany: Corran Telecom\ntopic: e-bike\nteam: returns desk at a warehouse\nnote: sorry to chase, reference CASE-9311\n\nVersions of the warranty terms (end dates excluded):\n- v1: first version; in force from March 12, 2024 to June 30, 2025; warranty period: 90 days.\n- v2: replaces v1; in force from June 30, 2025, open-ended; warranty period: 365 days.\n\nCase CASE-9311:\n- purchase date: April 20, 2025\n- fault date: June 29, 2025\n- claim date: September 26, 2025\n- decision date: October 9, 2025\n- day count from purchase to fault: 70 days\nEnd of case record.",
  "question": "Is v2 the version that governs this case?",
  "definitions": "Finding the version of the warranty terms that governs a case:\n- The governing version is the version in force on the case's fault date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q72618e7a44",
  "kind": "choice",
  "text": "{\"customer\": \"Tomas Lindqvist\", \"company\": \"Veridia Health\", \"topic\": \"summer trip\", \"team\": \"back office\", \"note\": \"reference CASE-5591\"}\n\nVersion table of the leave policy (end dates excluded):\nversion | replaces | in force from | in force to | paid leave allowance\nLP-269 | first version | 27 June 2023 | 14 November 2023 | 15 days\nLP-764 | LP-269 | 14 November 2023 | 8 March 2024 | 20 days\nLP-593 | LP-764 | 8 March 2024 | 22 May 2024 | 10 days\nLP-228 | LP-593 | 22 May 2024 | open-ended | 12 days\nSunset clause of LP-593: if LP-593 would govern a case whose decision date is after 21 September 2024, LP-228 governs it instead.\n\nCase CASE-5591:\n- hire date: 14 November 2023\n- leave start date: 16 November 2023\n- claim date: 9 February 2024\n- decision date: 7 March 2024\n- number of leave days claimed: 18 days\nEnd of case record.",
  "question": "Finding the version of the leave policy that governs a case:\n- Default: the version in force on the case's hire date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, what paid leave allowance does the governing version set for this case?",
  "options": [
   "20 days",
   "15 days"
  ]
 },
 {
  "qid": "q221bda1d11",
  "kind": "choice",
  "text": "HR desk note: routine entry for Aiko Brandt at Brightwell Supply about a payroll record, with reference CASE-5137 and the history pasted below.\n\nVersion table of the records retention schedule (end dates included):\nversion | replaces | in force from | in force to | retention period\nRS-953 | first version | March 19, 2024 | January 15, 2025 | 90 days\nRS-525 | RS-953 | January 16, 2025 | July 19, 2025 | 730 days\nRS-268 | RS-525 | July 20, 2025 | open-ended | 30 days\nTransition clause of RS-525: if a version older than RS-525 would govern a case whose decision date is on or after January 16, 2025, RS-525 governs it instead.\n\nCase CASE-5137:\n- record creation date: May 20, 2024\n- record closure date: May 20, 2024\n- deletion request date: September 18, 2024\n- decision date: March 28, 2025\n- day count from record closure to deletion request: 121 days\nEnd of case record.",
  "question": "Finding the version of the records retention schedule that governs a case:\n- Default: the version in force on the case's record creation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhat setting for the retention period does the governing version of records retention schedule specify for case CASE-5137?",
  "options": [
   "730 days",
   "90 days"
  ]
 },
 {
  "qid": "q8b774f84ac",
  "kind": "choice",
  "text": "Aiko Brandt: Hi, I am calling about my grocery order. I raised a case with Tamsin Fitness and I am a little frustrated, though I would like a clear explanation.\nagent: Thanks for getting in touch. I have case CASE-3842 on file, so tell me more about the grocery order.\n\nVersions of the shipping policy (end dates excluded):\n- SP-920: first version; in force from Friday, November 29, 2024 to Tuesday, September 2, 2025; delivery promise: 10 days.\n- SP-759: replaces SP-920; in force from Tuesday, September 2, 2025 to Friday, March 20, 2026; delivery promise: 4 days.\n  Transition clause of SP-759: if SP-759 would govern a case whose delivery date is before Tuesday, September 2, 2025, the version in force on that delivery date governs it instead.\n- SP-386: replaces SP-759; in force from Friday, March 20, 2026, open-ended; delivery promise: 14 days.\n\nCase CASE-3842:\n- order date: Tuesday, September 2, 2025\n- delivery date: Wednesday, September 3, 2025\n- complaint date: Wednesday, February 18, 2026\n- decision date: Monday, March 2, 2026\n- day count from order to delivery: 1 day\nEnd of case record.",
  "question": "Finding the version of the shipping policy that governs a case:\n- Default: the version in force on the case's complaint date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhat delivery promise does the shipping policy version that governs case CASE-3842 set?",
  "options": [
   "14 days",
   "4 days"
  ]
 },
 {
  "qid": "q391f7b2a16",
  "kind": "yes/no",
  "text": "Subject: Your summer trip enquiry\nHello Owen Pryce,\nThank you for writing to the Selkirk Logistics support inbox. The history and the case details are pasted below.\nKind regards.\n\nChange log of the leave policy, newest entry first:\nMonday, December 30, 2024 | v3 takes effect, replacing v2 | paid leave allowance: 10 days\nWednesday, September 18, 2024 | v2 takes effect, replacing v1 | paid leave allowance: 20 days\nSunday, June 2, 2024 | v1 takes effect as the first version | paid leave allowance: 30 days\n\nCase CASE-4788:\n- hire date: Sunday, June 2, 2024\n- leave start date: Sunday, June 2, 2024\n- claim date: Tuesday, September 17, 2024\n- decision date: Tuesday, September 17, 2024\n- number of leave days claimed: 25 days\n- claim to check: the paid leave allowance for this case is 20 days\nEnd of case record.",
  "question": "Going by the version history, does the claim to check in the case record agree with the value the governing version sets?",
  "definitions": "Finding the version of the leave policy that governs a case:\n- The governing version is the version in force on the case's claim date.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- A claim about the paid leave allowance is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qb9c9340e2c",
  "kind": "yes/no",
  "text": "customer: Owen Pryce\ncompany: Corran Telecom\ntopic: standing desk\nteam: IT help desk\nnote: set out below, history and case details in full\n\nVersions of the refund policy (end dates included):\n- rev-A: first version; in force from Wednesday, July 17, 2024 to Thursday, November 7, 2024; refund window: 14 days.\n- rev-B: replaces rev-A; in force from Friday, November 8, 2024 to Thursday, July 17, 2025; refund window: 45 days.\n- rev-C: replaces rev-B; in force from Friday, July 18, 2025, open-ended; refund window: 28 days.\n\nCase CASE-5406:\n- purchase date: Saturday, May 24, 2025\n- delivery date: Tuesday, June 3, 2025\n- refund request date: Wednesday, July 2, 2025\n- decision date: Friday, July 18, 2025\n- day count from purchase to refund request: 39 days\nEnd of case record.",
  "question": "Does it hold that it is not the case that rev-C does not decide the outcome for case CASE-5406?",
  "definitions": "Finding the version of the refund policy that governs a case:\n- The governing version is the version in force on the case's purchase date.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qc1b8ecb7fc",
  "kind": "choice",
  "text": "customer: Eva Marsh\ncompany: Veridia Health\ntopic: sofa order\nchannel: web form\nnote: routine history and case details are pasted below\n\nVersions of the shipping policy (end dates excluded):\n- SP12: first version; in force from 9 Mar 2024 to 21 Nov 2024; delivery promise: 2 days.\n- SP54: replaces SP12; in force from 21 Nov 2024 to 18 Mar 2025; delivery promise: 14 days.\n  Transition clause of SP54: if a version older than SP54 would govern a case whose decision date is on or after 21 Nov 2024, SP54 governs it instead.\n- SP38: replaces SP54; in force from 18 Mar 2025 to 26 Jun 2025; delivery promise: 5 days.\n- SP44: replaces SP38; in force from 26 Jun 2025, open-ended; delivery promise: 3 days.\n\nCase CASE-9618:\n- order date: 9 Mar 2024\n- delivery date: 9 Mar 2024\n- complaint date: 19 Mar 2024\n- decision date: 20 Nov 2024\n- day count from order to delivery: 0 days\nEnd of case record.",
  "question": "Finding the version of the shipping policy that governs a case:\n- Default: the version in force on the case's complaint date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nGoing by the version history, which version governs case CASE-9618 under shipping policy?",
  "options": [
   "SP44",
   "SP12"
  ]
 },
 {
  "qid": "qfc1c0608f0",
  "kind": "yes/no",
  "text": "Dana Okafor: Hello there, just ringing about case CASE-9473 with Pembroke Travel for a design suite.\nagent: Good to hear from you. The history and the case details are pasted below.\n\nChange log of the licence terms, newest entry first:\n2023-10-03 | LT-131 takes effect, replacing LT-410 | device limit: 10 devices\n2023-06-16 | LT-410 takes effect as the first version | device limit: 5 devices\n  Sunset clause of LT-410: if LT-410 would govern a case whose decision date is after 2024-03-24, LT-131 governs it instead.\n\nCase CASE-9473:\n- licence purchase date: 2023-07-22\n- activation date: 2024-01-22\n- support request date: 2024-01-23\n- decision date: 2024-02-19\n- number of devices registered: 8 devices\nEnd of case record.",
  "question": "Does it hold that it is not the case that LT-131 does not decide the outcome for case CASE-9473?",
  "definitions": "Finding the version of the licence terms that governs a case:\n- Default: the version in force on the case's activation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qdb29e6f4f8",
  "kind": "choice",
  "text": "{\"customer\": \"Sara Ilves\", \"company\": \"Tamsin Fitness\", \"topic\": \"laptop\", \"team\": \"accounts\", \"note\": \"history follows, polite but a bit annoyed\"}\n\nVersions of the warranty terms (end dates excluded):\n- rev-A: first version; in force from 25 Sep 2024 to 3 Mar 2025; warranty period: 365 days.\n- rev-B: replaces rev-A; in force from 3 Mar 2025, open-ended; warranty period: 90 days.\n  Transition clause of rev-B: if rev-B would govern a case whose purchase date is before 3 Mar 2025, the version in force on that purchase date governs it instead.\n\nCase CASE-5367:\n- purchase date: 25 Sep 2024\n- fault date: 24 Oct 2024\n- claim date: 1 Feb 2025\n- decision date: 30 Apr 2025\n- day count from purchase to fault: 29 days\nEnd of case record.",
  "question": "Finding the version of the warranty terms that governs a case:\n- Default: the version in force on the case's fault date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAcross the warranty terms history, which warranty period is the governing version setting for case CASE-5367?",
  "options": [
   "90 days",
   "365 days"
  ]
 },
 {
  "qid": "q2a9a525a3c",
  "kind": "choice",
  "text": "Tomas Lindqvist: Hi, phoning the call centre about the sofa order from Mistral Home, reference CASE-3924.\nsupport: Hello, the history and the case details are pasted below.\n\nVersion table of the shipping policy (end dates excluded):\nversion | replaces | in force from | in force to | delivery promise\nSP-461 | first version | 2024-11-08 | 2025-06-17 | 5 days\nSP-634 | SP-461 | 2025-06-17 | 2025-12-17 | 3 days\nSP-836 | SP-634 | 2025-12-17 | 2026-06-08 | 14 days\nSP-811 | SP-836 | 2026-06-08 | open-ended | 2 days\n\nCase CASE-3924:\n- order date: 2027-01-21\n- delivery date: 2027-01-21\n- complaint date: 2027-04-15\n- decision date: 2027-04-28\n- day count from order to delivery: 0 days\nEnd of case record.",
  "question": "Finding the version of the shipping policy that governs a case:\n- The governing version is the version in force on the case's complaint date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, which version of shipping policy is the controlling version for case CASE-3924?",
  "options": [
   "SP-461",
   "SP-811"
  ]
 },
 {
  "qid": "q88b197adfb",
  "kind": "choice",
  "text": "Staff queries at HR\nDana Okafor raised a case with Corran Telecom about their antivirus licence under reference CASE-8465, and the history and case details are pasted below.\n\nVersions of the licence terms (end dates excluded):\n- LT-334: first version; in force from May 16, 2023 to November 3, 2023; device limit: 3 devices.\n- LT-748: replaces LT-334; in force from November 3, 2023, open-ended; device limit: 2 devices.\n  Transition clause of LT-748: if a version older than LT-748 would govern a case whose decision date is on or after November 3, 2023, LT-748 governs it instead.\n\nCase CASE-8465:\n- licence purchase date: May 16, 2023\n- activation date: July 6, 2023\n- support request date: July 7, 2023\n- decision date: November 3, 2023\n- number of devices registered: 2 devices\nEnd of case record.",
  "question": "Finding the version of the licence terms that governs a case:\n- Default: the version in force on the case's activation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, which listed version of licence terms governs case CASE-8465?",
  "options": [
   "LT-748",
   "LT-334"
  ]
 },
 {
  "qid": "q717e8e0be7",
  "kind": "choice",
  "text": "Subject: Quick thanks\nDear Mira Castell,\nThank you for getting in touch with Upland Utilities about case CASE-2893 and the cable reel. The history and the case details are pasted below.\nKind regards.\n\nVersion table of the price list (end dates excluded):\nversion | replaces | in force from | in force to | price cap per unit\nPL-36C | first version | 5 May 2023 | 4 Jul 2023 | 19.99 USD\nPL-38R | PL-36C | 4 Jul 2023 | 29 Jan 2024 | 29.99 USD\nPL-50P | PL-38R | 29 Jan 2024 | open-ended | 12.50 USD\nTransition clause of PL-50P: if a version older than PL-50P would govern a case whose decision date is on or after 29 Jan 2024, PL-50P governs it instead.\n\nCase CASE-2893:\n- contract date: 9 Jun 2023\n- delivery date: 25 Jun 2023\n- invoice date: 18 Dec 2023\n- decision date: 28 Jan 2024\n- unit price charged: 3.00 USD\nEnd of case record.",
  "question": "Finding the version of the price list that governs a case:\n- Default: the version in force on the case's delivery date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAcross the price list versions, which version governs case CASE-2893?",
  "options": [
   "PL-36C",
   "PL-38R"
  ]
 },
 {
  "qid": "qb73594e10f",
  "kind": "choice",
  "text": "Subject: Your visit about a card account\nHi Dana Okafor,\nThank you for coming to the Veridia Health service counter about reference CASE-7594. The history and the case details are pasted below.\nThanks again.\n\nChange log of the fee schedule, newest entry first:\n2 Nov 2023 | FS-940 takes effect, replacing FS-428 | fee cap: $50.00\n12 Jul 2023 | FS-428 takes effect, replacing FS-274 | fee cap: $40.00\n  Transition clause of FS-428: if FS-428 would govern a case whose account opening date is before 12 Jul 2023, the version in force on that account opening date governs it instead.\n17 Feb 2023 | FS-274 takes effect as the first version | fee cap: $15.00\n\nCase CASE-7594:\n- account opening date: 19 Sep 2024\n- billing date: 24 Dec 2024\n- dispute date: 26 Dec 2024\n- decision date: 26 Dec 2024\n- fee charged: $24.00\nEnd of case record.",
  "question": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's billing date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, what fee cap is set for case CASE-7594 by the governing version of fee schedule?",
  "options": [
   "$15.00",
   "$50.00"
  ]
 },
 {
  "qid": "qbfc14f3e1c",
  "kind": "yes/no",
  "text": "Hello,\nMy name is Ana Ruiz and I am writing to raise a case with Upland Utilities about my design suite. The matter is routine and the history follows below under CASE-5446.\nBest regards,\n\nVersions of the licence terms (end dates excluded):\n- LT-584: first version; in force from May 25, 2024 to October 28, 2024; device limit: 1 device.\n- LT-891: replaces LT-584; in force from October 28, 2024, open-ended; device limit: 3 devices.\n  Transition clause of LT-891: if LT-891 would govern a case whose activation date is before October 28, 2024, the version in force on that activation date governs it instead.\n\nCase CASE-5446:\n- licence purchase date: October 23, 2024\n- activation date: October 28, 2024\n- support request date: December 19, 2024\n- decision date: December 19, 2024\n- number of devices registered: 2 devices\nEnd of case record.",
  "question": "Is it the case that it is not the case that LT-584 does not settle this case?",
  "definitions": "Finding the version of the licence terms that governs a case:\n- Default: the version in force on the case's activation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qc3c41a0278",
  "kind": "choice",
  "text": "{\"customer\": \"Ines Duarte\", \"company\": \"Veridia Health\", \"topic\": \"grocery order\", \"team\": \"accounts\", \"note\": \"history follows, polite but a bit annoyed\"}\n\nVersions of the shipping policy (end dates excluded):\n- SP-104: first version; in force from Wednesday, 3 January 2024 to Friday, 26 April 2024; delivery promise: 10 days.\n- SP-707: replaces SP-104; in force from Friday, 26 April 2024 to Tuesday, 5 November 2024; delivery promise: 4 days.\n- SP-145: replaces SP-707; in force from Tuesday, 5 November 2024, open-ended; delivery promise: 7 days.\n\nCase CASE-4189:\n- order date: Friday, 23 February 2024\n- delivery date: Sunday, 31 March 2024\n- complaint date: Thursday, 25 April 2024\n- decision date: Tuesday, 7 May 2024\n- day count from order to delivery: 37 days\nEnd of case record.",
  "question": "Finding the version of the shipping policy that governs a case:\n- The governing version is the version in force on the case's complaint date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nFor case CASE-4189, which version of shipping policy governs according to the card?",
  "options": [
   "SP-145",
   "SP-104"
  ]
 },
 {
  "qid": "qf762c96a48",
  "kind": "yes/no",
  "text": "{\"customer\": \"Hana Sato\", \"company\": \"Pembroke Travel\", \"topic\": \"payroll record\", \"channel\": \"live chat\", \"note\": \"lovely to help, history and case details are pasted below\"}\n\nVersion table of the records retention schedule (end dates included):\nversion | replaces | in force from | in force to | retention period\nv1 | first version | Saturday, 31 August 2024 | Wednesday, 4 December 2024 | 365 days\nv2 | v1 | Thursday, 5 December 2024 | Tuesday, 14 October 2025 | 90 days\nv3 | v2 | Wednesday, 15 October 2025 | open-ended | 180 days\nTransition clause of v3: if a version older than v3 would govern a case whose decision date is on or after Wednesday, 15 October 2025, v3 governs it instead.\n\nCase CASE-9167:\n- record creation date: Tuesday, 31 December 2024\n- record closure date: Tuesday, 4 February 2025\n- deletion request date: Wednesday, 26 March 2025\n- decision date: Wednesday, 15 October 2025\n- day count from record closure to deletion request: 50 days\nEnd of case record.",
  "question": "According to the card, is it so that it is not the case that v2 does not govern this case?",
  "definitions": "Finding the version of the records retention schedule that governs a case:\n- Default: the version in force on the case's record creation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qbe35939d09",
  "kind": "yes/no",
  "text": "Subject: IT help desk matter about an e-bike\nDear Nadia Kowal,\nPembroke Travel logged your query about the e-bike on the IT help desk. The history and the case details are pasted below.\nRegards.\n\nChange log of the warranty terms, newest entry first:\nJuly 24, 2024 | v3 takes effect, replacing v2 | warranty period: 180 days\n  Transition clause of v3: if v3 would govern a case whose purchase date is before July 24, 2024, the version in force on that purchase date governs it instead.\nMay 16, 2024 | v2 takes effect, replacing v1 | warranty period: 365 days\nMarch 16, 2024 | v1 takes effect as the first version | warranty period: 30 days\n\nCase CASE-6032:\n- purchase date: May 15, 2024\n- fault date: August 4, 2024\n- claim date: August 31, 2024\n- decision date: December 28, 2024\n- day count from purchase to fault: 81 days\nEnd of case record.",
  "question": "According to the card, is case CASE-6032 not within the warranty period set by the governing version of warranty terms?",
  "definitions": "Finding the version of the warranty terms that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the warranty period when its day count from purchase to fault is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q17145bfb53",
  "kind": "yes/no",
  "text": "Calls about a safety boot, reference CASE-9794\nThe Redfern Bank call centre heard from Kofi Mensah about this matter. The history and the case details follow below in a calm, routine way.\n\nVersions of the price list (end dates excluded):\n- PL-488: first version; in force from September 6, 2024 to March 19, 2025; price cap per unit: 29.99 USD.\n- PL-407: replaces PL-488; in force from March 19, 2025 to January 23, 2026; price cap per unit: 19.99 USD.\n- PL-408: replaces PL-407; in force from January 23, 2026, open-ended; price cap per unit: 12.50 USD.\n\nCase CASE-9794:\n- contract date: October 9, 2025\n- delivery date: January 19, 2026\n- invoice date: January 23, 2026\n- decision date: May 5, 2026\n- unit price charged: 12.51 USD\nEnd of case record.",
  "question": "In case CASE-9794, is the quantity within the price cap per unit set by the governing version?",
  "definitions": "Finding the version of the price list that governs a case:\n- The governing version is the version in force on the case's invoice date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- The case is within the price cap per unit when its unit price charged is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q201babf4fb",
  "kind": "yes/no",
  "text": "customer: Kofi Mensah\ncompany: Brightwell Supply\ntopic: printer toner\nteam: accounts\nnote: the history and case details are pasted in order below\n\nVersions of the price list (end dates excluded):\n- PL-433: first version; in force from 2023-07-01 to 2024-01-28; price cap per unit: 12.50 USD.\n  Sunset clause of PL-433: if PL-433 would govern a case whose decision date is after 2024-07-26, PL-988 governs it instead.\n- PL-988: replaces PL-433; in force from 2024-01-28 to 2024-09-16; price cap per unit: 24.00 USD.\n- PL-926: replaces PL-988; in force from 2024-09-16, open-ended; price cap per unit: 35.00 USD.\n\nCase CASE-4563:\n- contract date: 2023-08-15\n- delivery date: 2023-09-08\n- invoice date: 2023-09-13\n- decision date: 2024-07-27\n- unit price charged: 24.01 USD\nEnd of case record.\n\nEarlier terms were carved out just for this person, leaving the everyday wording to everyone else.",
  "question": "Does case CASE-4563 sit inside the price cap per unit that the governing version of price list sets?",
  "definitions": "Finding the version of the price list that governs a case:\n- Default: the version in force on the case's invoice date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the price cap per unit when its unit price charged is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qca6663c1fd",
  "kind": "choice",
  "text": "Internal summary for the file. Ravi Anand raised case CASE-3882 with Pembroke Travel about a conference trip. It is a brief, formal matter and details follow.\n\nVersions of the travel policy (end dates included):\n- v1: first version; in force from Tuesday, July 9, 2024 to Saturday, May 17, 2025; nightly hotel cap: 120.00 USD.\n- v2: replaces v1; in force from Sunday, May 18, 2025 to Tuesday, September 16, 2025; nightly hotel cap: 250.00 USD.\n- v3: replaces v2; in force from Wednesday, September 17, 2025, open-ended; nightly hotel cap: 200.00 USD.\n  Transition clause of v3: if v3 would govern a case whose booking date is before Wednesday, September 17, 2025, the version in force on that booking date governs it instead.\n\nCase CASE-3882:\n- booking date: Tuesday, September 16, 2025\n- travel date: Thursday, October 2, 2025\n- expense claim date: Thursday, October 23, 2025\n- decision date: Sunday, February 15, 2026\n- nightly rate claimed: 157.00 USD\nEnd of case record.",
  "question": "Finding the version of the travel policy that governs a case:\n- Default: the version in force on the case's booking date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhat nightly hotel cap does the governing version of travel policy set for case CASE-3882?",
  "options": [
   "$200.00",
   "$250.00"
  ]
 },
 {
  "qid": "qeca78bfea9",
  "kind": "yes/no",
  "text": "customer: Kofi Mensah\ncompany: Pembroke Travel\ntopic: card account\nreference: CASE-3539\nnote: sorry for the bother\n\nVersions of the fee schedule (end dates included):\n- v1: first version; in force from 22 Mar 2023 to 14 Dec 2023; fee cap: 15.00 USD.\n- v2: replaces v1; in force from 15 Dec 2023 to 13 Aug 2024; fee cap: 20.00 USD.\n  Transition clause of v2: if v2 would govern a case whose billing date is before 15 Dec 2023, the version in force on that billing date governs it instead.\n- v3: replaces v2; in force from 14 Aug 2024, open-ended; fee cap: 75.00 USD.\n\nCase CASE-3539:\n- account opening date: 4 Sep 2023\n- billing date: 14 Dec 2023\n- dispute date: 14 Jul 2024\n- decision date: 6 Aug 2024\n- fee charged: 23.00 USD\n- claim to check: the fee cap for this case is 20.00 USD\nEnd of case record.",
  "question": "Going by the version history, does the claim to check in case CASE-3539 give the same fee cap the governing version of fee schedule sets?",
  "definitions": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's dispute date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- A claim about the fee cap is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q6bb9acfab1",
  "kind": "choice",
  "text": "Accounts help, gladly given\nMalik Osei raised a case with Lindenfeld Outfitters about their payroll record, and the history and case details follow below.\n\nVersions of the records retention schedule (end dates included):\n- rev-A: first version; in force from April 9, 2024 to February 4, 2025; retention period: 60 days.\n- rev-B: replaces rev-A; in force from February 5, 2025, open-ended; retention period: 730 days.\n  Transition clause of rev-B: if rev-B would govern a case whose record creation date is before February 5, 2025, the version in force on that record creation date governs it instead.\n\nCase CASE-9672:\n- record creation date: February 5, 2025\n- record closure date: December 19, 2025\n- deletion request date: April 1, 2026\n- decision date: April 1, 2026\n- day count from record closure to deletion request: 103 days\nEnd of case record.",
  "question": "Finding the version of the records retention schedule that governs a case:\n- Default: the version in force on the case's record closure date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nGoing by the version history, what retention period is set for case CASE-9672 by the governing version of records retention schedule?",
  "options": [
   "60 days",
   "730 days"
  ]
 },
 {
  "qid": "qb3a0d22c2b",
  "kind": "yes/no",
  "text": "Subject: Your case about the house move\nHi Priya Raman,\nThe Pembroke Travel customer care team has your message. The history and the case details are pasted below.\nTake care.\n\nChange log of the leave policy, newest entry first:\n2023-11-02 | rev-C takes effect, replacing rev-B | paid leave allowance: 30 days\n2023-06-03 | rev-B takes effect, replacing rev-A | paid leave allowance: 12 days\n2023-02-10 | rev-A takes effect as the first version | paid leave allowance: 25 days\n\nCase CASE-3739:\n- hire date: 2023-07-24\n- leave start date: 2024-01-26\n- claim date: 2024-05-05\n- decision date: 2024-05-06\n- number of leave days claimed: 28 days\nEnd of case record.",
  "question": "Under these rules, is case CASE-3739 within the paid leave allowance that the governing version of leave policy sets?",
  "definitions": "Finding the version of the leave policy that governs a case:\n- The governing version is the version in force on the case's claim date.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- The case is within the paid leave allowance when its number of leave days claimed is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q568515a1a5",
  "kind": "choice",
  "text": "Jonas Feld: Please take a look at the printer toner under reference CASE-7427.\nsupport: Noted, and the history for Quayside Software is pasted here in full.\n\nVersion table of the price list (end dates excluded):\nversion | replaces | in force from | in force to | price cap per unit\nPL-783 | first version | August 6, 2023 | December 1, 2023 | $24.00\nPL-274 | PL-783 | December 1, 2023 | October 4, 2024 | $14.99\nPL-956 | PL-274 | October 4, 2024 | open-ended | $19.99\n\nCase CASE-7427:\n- contract date: March 15, 2025\n- delivery date: March 27, 2025\n- invoice date: April 15, 2025\n- decision date: September 27, 2025\n- unit price charged: $5.00\nEnd of case record.",
  "question": "Finding the version of the price list that governs a case:\n- The governing version is the version in force on the case's delivery date.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, which version of price list governs the case with reference CASE-7427?",
  "options": [
   "PL-783",
   "PL-956"
  ]
 },
 {
  "qid": "q87ef1d8d86",
  "kind": "choice",
  "text": "Customer case CASE-7621 for Jonas Feld\nJonas Feld is a little put out, but polite, having raised a case with Tamsin Fitness about the office chair. The full history of the matter sits below.\n\nVersion table of the price list (end dates excluded):\nversion | replaces | in force from | in force to | price cap per unit\nv1 | first version | 7 Apr 2023 | 2 Jan 2024 | $29.99\nv2 | v1 | 2 Jan 2024 | 17 Aug 2024 | $24.00\nv3 | v2 | 17 Aug 2024 | 4 Dec 2024 | $35.00\nv4 | v3 | 4 Dec 2024 | open-ended | $12.50\nTransition clause of v4: if v4 would govern a case whose delivery date is before 4 Dec 2024, the version in force on that delivery date governs it instead.\n\nCase CASE-7621:\n- contract date: 1 May 2025\n- delivery date: 1 May 2025\n- invoice date: 2 May 2025\n- decision date: 26 Jul 2025\n- unit price charged: $8.00\nEnd of case record.\n\nThis customer's earlier terms were lifted off the books for their own file alone.",
  "question": "Finding the version of the price list that governs a case:\n- Default: the version in force on the case's delivery date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, what price cap per unit is set for case CASE-7621 by the governing version of price list?",
  "options": [
   "$12.50",
   "$29.99"
  ]
 },
 {
  "qid": "q2c17699a84",
  "kind": "choice",
  "text": "Owen Pryce: Hi, stuck with the card account from Mistral Home, so please help from IT.\nsupport: Lovely, IT here. The history and the case details are pasted below.\n\nChange log of the fee schedule, newest entry first:\nTuesday, 27 February 2024 | FS-64P takes effect, replacing FS-82M | fee cap: $20.00\n  Transition clause of FS-64P: if a version older than FS-64P would govern a case whose decision date is on or after Tuesday, 27 February 2024, FS-64P governs it instead.\nThursday, 11 January 2024 | FS-82M takes effect as the first version | fee cap: $75.00\n\nCase CASE-1060:\n- account opening date: Sunday, 25 February 2024\n- billing date: Monday, 26 February 2024\n- dispute date: Monday, 26 February 2024\n- decision date: Tuesday, 27 February 2024\n- fee charged: $170.00\nEnd of case record.",
  "question": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's billing date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich version of fee schedule governs the fee cap rule for case CASE-1060?",
  "options": [
   "FS-64P",
   "FS-82M"
  ]
 },
 {
  "qid": "q1b37e3d5a5",
  "kind": "yes/no",
  "text": "Jonas Feld: A bit annoyed about the grocery order from Selkirk Logistics on this call centre line, reference CASE-6459, though polite.\nagent: Fair enough, the history and the case details are pasted below.\n\nVersions of the shipping policy (end dates excluded):\n- rev-A: first version; in force from Wednesday, June 7, 2023 to Monday, September 4, 2023; delivery promise: 10 days.\n- rev-B: replaces rev-A; in force from Monday, September 4, 2023 to Saturday, April 27, 2024; delivery promise: 3 days.\n- rev-C: replaces rev-B; in force from Saturday, April 27, 2024, open-ended; delivery promise: 4 days.\n  Transition clause of rev-C: if rev-C would govern a case whose order date is before Saturday, April 27, 2024, the version in force on that order date governs it instead.\n\nCase CASE-6459:\n- order date: Thursday, October 19, 2023\n- delivery date: Monday, October 23, 2023\n- complaint date: Wednesday, December 4, 2024\n- decision date: Wednesday, May 7, 2025\n- day count from order to delivery: 4 days\nEnd of case record.",
  "question": "According to the card, is this case within the delivery promise set by the governing version?",
  "definitions": "Finding the version of the shipping policy that governs a case:\n- Default: the version in force on the case's complaint date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the delivery promise when its day count from order to delivery is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qbb17c873a8",
  "kind": "yes/no",
  "text": "Aiko Brandt: Calling about the coffee grinder from Mistral Home, thank you for taking it.\nagent: Understood, the history and case details are pasted below for this call.\n\nChange log of the warranty terms, newest entry first:\n2025-02-08 | v2 takes effect, replacing v1 | warranty period: 730 days\n  Transition clause of v2: if a version older than v2 would govern a case whose decision date is on or after 2025-02-08, v2 governs it instead.\n2024-11-25 | v1 takes effect as the first version | warranty period: 180 days\n\nCase CASE-1618:\n- purchase date: 2025-01-31\n- fault date: 2025-02-07\n- claim date: 2025-02-07\n- decision date: 2025-02-07\n- day count from purchase to fault: 7 days\n- claim to check: the warranty period for this case is 730 days\nEnd of case record.",
  "question": "Does the claim to check for this case match the value set by the governing version?",
  "definitions": "Finding the version of the warranty terms that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- A claim about the warranty period is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q204e34ff67",
  "kind": "yes/no",
  "text": "Hana Sato: Ringing the member services desk about an e-bike from Tamsin Fitness.\nagent: Noted, the history and case details are pasted below.\n\nChange log of the warranty terms, newest entry first:\nWednesday, 27 November 2024 | v2 takes effect, replacing v1 | warranty period: 30 days\nFriday, 15 March 2024 | v1 takes effect as the first version | warranty period: 90 days\n\nCase CASE-8350:\n- purchase date: Tuesday, 29 October 2024\n- fault date: Tuesday, 21 January 2025\n- claim date: Sunday, 3 August 2025\n- decision date: Saturday, 1 November 2025\n- day count from purchase to fault: 84 days\n- claim to check: the warranty period for this case is 90 days\nEnd of case record.",
  "question": "Does the governing version of warranty terms agree with the claim about the warranty period in the record for case CASE-8350?",
  "definitions": "Finding the version of the warranty terms that governs a case:\n- The governing version is the version in force on the case's purchase date.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- A claim about the warranty period is supported when it states the governing version's value, and contradicted otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q01b75e251a",
  "kind": "yes/no",
  "text": "Subject: Your case at the service counter\nDear Priya Raman,\nLovely to hear from you about a coffee grinder with Veridia Health, and the history is pasted below for reference CASE-7138.\nWarm thanks.\n\nChange log of the warranty terms, newest entry first:\nSaturday, July 1, 2023 | rev-B takes effect, replacing rev-A | warranty period: 30 days\n  Transition clause of rev-B: if rev-B would govern a case whose purchase date is before Saturday, July 1, 2023, the version in force on that purchase date governs it instead.\nMonday, May 15, 2023 | rev-A takes effect as the first version | warranty period: 730 days\n\nCase CASE-7138:\n- purchase date: Friday, June 30, 2023\n- fault date: Tuesday, December 26, 2023\n- claim date: Wednesday, February 7, 2024\n- decision date: Sunday, April 21, 2024\n- day count from purchase to fault: 179 days\nEnd of case record.",
  "question": "Under these rules, would it be so that it is not the case that rev-A does not decide this case?",
  "definitions": "Finding the version of the warranty terms that governs a case:\n- Default: the version in force on the case's purchase date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qf2c9b97a00",
  "kind": "yes/no",
  "text": "Subject: Your visit about a coffee grinder\nHi Jonas Feld,\nThank you for coming to the Lindenfeld Outfitters service counter about reference CASE-7104. The history and the case details are pasted below.\nThanks again.\n\nVersions of the warranty terms (end dates excluded):\n- v1: first version; in force from Wednesday, October 25, 2023 to Wednesday, June 5, 2024; warranty period: 365 days.\n  Sunset clause of v1: if v1 would govern a case whose decision date is after Saturday, March 8, 2025, v2 governs it instead.\n- v2: replaces v1; in force from Wednesday, June 5, 2024, open-ended; warranty period: 730 days.\n\nCase CASE-7104:\n- purchase date: Monday, January 27, 2025\n- fault date: Monday, January 27, 2025\n- claim date: Monday, January 27, 2025\n- decision date: Wednesday, July 30, 2025\n- day count from purchase to fault: 0 days\nEnd of case record.",
  "question": "Is the quantity within the warranty period set by the governing version of warranty terms for case CASE-7104?",
  "definitions": "Finding the version of the warranty terms that governs a case:\n- Default: the version in force on the case's fault date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the warranty period when its day count from purchase to fault is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qe05aebe90f",
  "kind": "yes/no",
  "text": "Ines Duarte: Hello, I am writing to raise a case with Upland Utilities about conference trip.\nsupport: Hello. Your matter is recorded as CASE-7123 and the full details are set out in order.\n\nChange log of the travel policy, newest entry first:\n22 Jan 2024 | v2 takes effect, replacing v1 | nightly hotel cap: $175.00\n7 Aug 2023 | v1 takes effect as the first version | nightly hotel cap: $200.00\n  Sunset clause of v1: if v1 would govern a case whose decision date is after 16 Feb 2024, v2 governs it instead.\n\nCase CASE-7123:\n- booking date: 14 Aug 2023\n- travel date: 28 Aug 2023\n- expense claim date: 29 Aug 2023\n- decision date: 17 Feb 2024\n- nightly rate claimed: $92.00\nEnd of case record.",
  "question": "Under these rules, would it be so that it is not the case that v1 does not decide this case?",
  "definitions": "Finding the version of the travel policy that governs a case:\n- Default: the version in force on the case's booking date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q58892095e1",
  "kind": "choice",
  "text": "customer: Yara Haddad\ncompany: Brightwell Supply\ntopic: printer toner\nRoutine contact from the regional office, history and case details follow below.\n\nVersions of the price list (end dates excluded):\n- v1: first version; in force from Sunday, February 19, 2023 to Sunday, April 23, 2023; price cap per unit: $24.00.\n- v2: replaces v1; in force from Sunday, April 23, 2023, open-ended; price cap per unit: $29.99.\n  Transition clause of v2: if a version older than v2 would govern a case whose decision date is on or after Sunday, April 23, 2023, v2 governs it instead.\n\nCase CASE-4507:\n- contract date: Sunday, February 19, 2023\n- delivery date: Sunday, February 19, 2023\n- invoice date: Monday, February 27, 2023\n- decision date: Saturday, April 22, 2023\n- unit price charged: $24.00\nEnd of case record.",
  "question": "Finding the version of the price list that governs a case:\n- Default: the version in force on the case's invoice date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, what price cap per unit does case CASE-4507 of price list get from its governing version?",
  "options": [
   "$29.99",
   "$24.00"
  ]
 },
 {
  "qid": "q6376147b1f",
  "kind": "choice",
  "text": "Service note: Ines Duarte raised a case with Halvard Insurance about a study block, and it is lovely to have them on file. The history and case details are pasted below, so please read them with care.\n\nVersion table of the leave policy (end dates excluded):\nversion | replaces | in force from | in force to | paid leave allowance\nrev-A | first version | Friday, 2 August 2024 | Monday, 17 February 2025 | 12 days\nrev-B | rev-A | Monday, 17 February 2025 | Monday, 18 August 2025 | 25 days\nrev-C | rev-B | Monday, 18 August 2025 | open-ended | 30 days\nTransition clause of rev-C: if rev-C would govern a case whose leave start date is before Monday, 18 August 2025, the version in force on that leave start date governs it instead.\n\nCase CASE-9886:\n- hire date: Wednesday, 22 January 2025\n- leave start date: Thursday, 23 January 2025\n- claim date: Sunday, 16 February 2025\n- decision date: Friday, 21 February 2025\n- number of leave days claimed: 12 days\nEnd of case record.",
  "question": "Finding the version of the leave policy that governs a case:\n- Default: the version in force on the case's hire date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nAccording to the card, which paid leave allowance does the governing version of leave policy set for case CASE-9886?",
  "options": [
   "25 days",
   "12 days"
  ]
 },
 {
  "qid": "q717dd5990a",
  "kind": "yes/no",
  "text": "Priya Raman: Honestly, my antivirus licence keeps being a nuisance.\nsupport: Understood. The history and the case details are pasted below for the Quayside Software branch.\n\nChange log of the licence terms, newest entry first:\nWednesday, December 3, 2025 | rev-C takes effect, replacing rev-B | device limit: 3 devices\n  Transition clause of rev-C: if rev-C would govern a case whose licence purchase date is before Wednesday, December 3, 2025, the version in force on that licence purchase date governs it instead.\nFriday, February 7, 2025 | rev-B takes effect, replacing rev-A | device limit: 5 devices\nSunday, April 14, 2024 | rev-A takes effect as the first version | device limit: 10 devices\n\nCase CASE-2530:\n- licence purchase date: Tuesday, December 2, 2025\n- activation date: Thursday, November 26, 2026\n- support request date: Friday, November 27, 2026\n- decision date: Saturday, December 12, 2026\n- number of devices registered: 2 devices\nEnd of case record.",
  "question": "For case CASE-2530, is rev-C the version that governs?",
  "definitions": "Finding the version of the licence terms that governs a case:\n- Default: the version in force on the case's activation date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q8a074f5e09",
  "kind": "choice",
  "text": "Back office note: the family visit that Tomas Lindqvist raised with Quayside Software sits under reference CASE-4737, and the history is pasted below.\n\nChange log of the leave policy, newest entry first:\nMonday, 4 November 2024 | LP-281 takes effect, replacing LP-435 | paid leave allowance: 25 days\n  Transition clause of LP-281: if a version older than LP-281 would govern a case whose decision date is on or after Monday, 4 November 2024, LP-281 governs it instead.\nTuesday, 9 January 2024 | LP-435 takes effect as the first version | paid leave allowance: 12 days\n\nCase CASE-4737:\n- hire date: Thursday, 16 May 2024\n- leave start date: Thursday, 16 May 2024\n- claim date: Friday, 17 May 2024\n- decision date: Friday, 27 December 2024\n- number of leave days claimed: 34 days\nEnd of case record.",
  "question": "Finding the version of the leave policy that governs a case:\n- Default: the version in force on the case's claim date; \"would govern\" in a clause means this default.\n- A version is in force from its start date until the version that replaces it takes effect, and on that start date the new version is in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nGoing by the version history, which version does the card pick for case CASE-4737?",
  "options": [
   "LP-281",
   "LP-435"
  ]
 },
 {
  "qid": "q1cfe739a7f",
  "kind": "yes/no",
  "text": "customer: Sara Ilves\ncompany: Tamsin Fitness\ntopic: support transcript\nWarm thanks for getting in touch, reference CASE-6934, with the history and case details pasted below.\n\nVersions of the records retention schedule (end dates included):\n- RS-212: first version; in force from 18 Nov 2024 to 11 Mar 2025; retention period: 60 days.\n- RS-796: replaces RS-212; in force from 12 Mar 2025 to 26 Dec 2025; retention period: 90 days.\n  Transition clause of RS-796: if RS-796 would govern a case whose record creation date is before 12 Mar 2025, the version in force on that record creation date governs it instead.\n- RS-488: replaces RS-796; in force from 27 Dec 2025, open-ended; retention period: 730 days.\n\nCase CASE-6934:\n- record creation date: 11 Mar 2025\n- record closure date: 27 Oct 2025\n- deletion request date: 27 Dec 2025\n- decision date: 19 Mar 2026\n- day count from record closure to deletion request: 61 days\nEnd of case record.",
  "question": "Is case CASE-6934 not within the retention period set by the governing version?",
  "definitions": "Finding the version of the records retention schedule that governs a case:\n- Default: the version in force on the case's record closure date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the retention period when its day count from record closure to deletion request is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "qd596890992",
  "kind": "yes/no",
  "text": "Lucas Brenner: Hi, I am writing to raise a case with Pembroke Travel about the client visit.\nsupport: Hello. The case is logged under CASE-6105 and the usual details follow.\nLucas Brenner: Thanks, that is everything for this call.\n\nVersions of the travel policy (end dates included):\n- v1: first version; in force from 10 Oct 2023 to 3 Jul 2024; nightly hotel cap: $150.00.\n- v2: replaces v1; in force from 4 Jul 2024, open-ended; nightly hotel cap: $200.00.\n  Transition clause of v2: if a version older than v2 would govern a case whose decision date is on or after 4 Jul 2024, v2 governs it instead.\n\nCase CASE-6105:\n- booking date: 10 Mar 2024\n- travel date: 3 Jul 2024\n- expense claim date: 3 Jul 2024\n- decision date: 3 Jul 2024\n- nightly rate claimed: $380.00\nEnd of case record.",
  "question": "Is v1 the governing version for the case CASE-6105 recorded under travel policy?",
  "definitions": "Finding the version of the travel policy that governs a case:\n- Default: the version in force on the case's booking date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 },
 {
  "qid": "q22ba5e021b",
  "kind": "choice",
  "text": "Support note: reference CASE-3266 covers Nadia Kowal, who wrote to Veridia Health about their meal kit plan. The history sits beneath this note.\n\nVersions of the subscription terms (end dates included):\n- ST-651: first version; in force from 2023-08-03 to 2024-05-07; free cancellation period: 21 days.\n- ST-791: replaces ST-651; in force from 2024-05-08 to 2024-08-17; free cancellation period: 14 days.\n- ST-928: replaces ST-791; in force from 2024-08-18 to 2025-03-16; free cancellation period: 7 days.\n- ST-392: replaces ST-928; in force from 2025-03-17, open-ended; free cancellation period: 30 days.\n\nCase CASE-3266:\n- sign-up date: 2024-02-25\n- renewal date: 2024-05-08\n- cancellation date: 2024-05-25\n- decision date: 2024-10-27\n- day count from sign-up to cancellation: 90 days\nEnd of case record.",
  "question": "Finding the version of the subscription terms that governs a case:\n- The governing version is the version in force on the case's renewal date.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nGoing by the version history, which version of subscription terms ends up governing case CASE-3266?",
  "options": [
   "ST-791",
   "ST-928"
  ]
 },
 {
  "qid": "q2fe79b4263",
  "kind": "choice",
  "text": "Gym membership case for Lena Whitcombe\nLena Whitcombe raised a case with Upland Utilities about a card account, filed as CASE-9443. The history and details are set out below, and the customer is a little frustrated but polite.\n\nVersion table of the fee schedule (end dates included):\nversion | replaces | in force from | in force to | fee cap\nrev-A | first version | Sunday, 5 March 2023 | Wednesday, 7 February 2024 | $50.00\nrev-B | rev-A | Thursday, 8 February 2024 | Tuesday, 25 June 2024 | $35.00\nrev-C | rev-B | Wednesday, 26 June 2024 | open-ended | $75.00\nTransition clause of rev-C: if a version older than rev-C would govern a case whose decision date is on or after Wednesday, 26 June 2024, rev-C governs it instead.\n\nCase CASE-9443:\n- account opening date: Sunday, 28 January 2024\n- billing date: Wednesday, 7 February 2024\n- dispute date: Wednesday, 7 February 2024\n- decision date: Tuesday, 25 June 2024\n- fee charged: $41.00\nEnd of case record.",
  "question": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's dispute date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder fee schedule, what fee cap does the governing version set for case CASE-9443?",
  "options": [
   "$75.00",
   "$50.00"
  ]
 },
 {
  "qid": "q1602de4241",
  "kind": "choice",
  "text": "Subject: Support inbox message\nHello Priya Raman,\nThis message concerns your cable reel with Halvard Insurance, and the history sits below this text.\nKind thanks.\n\nVersions of the price list (end dates excluded):\n- v1: first version; in force from Saturday, 21 September 2024 to Wednesday, 8 January 2025; price cap per unit: 24.00 USD.\n- v2: replaces v1; in force from Wednesday, 8 January 2025, open-ended; price cap per unit: 12.50 USD.\n  Transition clause of v2: if a version older than v2 would govern a case whose decision date is on or after Wednesday, 8 January 2025, v2 governs it instead.\n\nCase CASE-6090:\n- contract date: Saturday, 21 September 2024\n- delivery date: Saturday, 21 September 2024\n- invoice date: Wednesday, 8 January 2025\n- decision date: Monday, 24 February 2025\n- unit price charged: 20.00 USD\nEnd of case record.",
  "question": "Finding the version of the price list that governs a case:\n- Default: the version in force on the case's invoice date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, what price cap per unit does case CASE-6090 of price list get from its governing version?",
  "options": [
   "$12.50",
   "$24.00"
  ]
 },
 {
  "qid": "qa6eba3e963",
  "kind": "choice",
  "text": "customer: Jonas Feld\ncompany: Veridia Health\nreference: CASE-1074\ntopic: safety boot\nA polite but mildly annoyed caller at the call centre, with the history and the case details pasted below.\n\nVersion table of the price list (end dates excluded):\nversion | replaces | in force from | in force to | price cap per unit\nPL-912 | first version | 21 November 2024 | 16 May 2025 | 29.99 USD\nPL-720 | PL-912 | 16 May 2025 | 28 February 2026 | 12.50 USD\nPL-478 | PL-720 | 28 February 2026 | 5 August 2026 | 14.99 USD\nPL-227 | PL-478 | 5 August 2026 | open-ended | 19.99 USD\nTransition clause of PL-720: if PL-720 would govern a case whose contract date is before 16 May 2025, the version in force on that contract date governs it instead.\n\nCase CASE-1074:\n- contract date: 24 February 2025\n- delivery date: 26 February 2026\n- invoice date: 26 February 2026\n- decision date: 19 June 2026\n- unit price charged: 65.00 USD\nEnd of case record.",
  "question": "Finding the version of the price list that governs a case:\n- Default: the version in force on the case's delivery date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nUnder these rules, which listed version of price list is the governing version for case CASE-1074?",
  "options": [
   "PL-478",
   "PL-912"
  ]
 },
 {
  "qid": "q880c4a0f85",
  "kind": "yes/no",
  "text": "Desk note: Owen Pryce is following up on a summer trip with Lindenfeld Outfitters, logged as CASE-9049, and the history sits below.\n\nVersion table of the leave policy (end dates excluded):\nversion | replaces | in force from | in force to | paid leave allowance\nv1 | first version | 2024-10-06 | 2025-06-11 | 12 days\nv2 | v1 | 2025-06-11 | 2025-12-17 | 30 days\nv3 | v2 | 2025-12-17 | 2026-04-01 | 15 days\nv4 | v3 | 2026-04-01 | open-ended | 20 days\nTransition clause of v4: if v4 would govern a case whose leave start date is before 2026-04-01, the version in force on that leave start date governs it instead.\n\nCase CASE-9049:\n- hire date: 2027-04-20\n- leave start date: 2027-04-27\n- claim date: 2027-04-27\n- decision date: 2027-05-26\n- number of leave days claimed: 20 days\nEnd of case record.",
  "question": "Is it the card's view that it is not the case that this case does not fall within the paid leave allowance under leave policy?",
  "definitions": "Finding the version of the leave policy that governs a case:\n- Default: the version in force on the case's hire date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through the day before its end date; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\n- The case is within the paid leave allowance when its number of leave days claimed is at most the governing version's value, and outside it otherwise.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists."
 }
]
