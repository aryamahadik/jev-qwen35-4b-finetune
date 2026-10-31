# G5-H blind read T20-blind_read-7a308f25-001 (family T20)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T20/pilot_i3/g5h/answers/T20-blind_read-7a308f25-001.json

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
  "qid": "qf8a6c87dee",
  "kind": "yes/no",
  "text": "Draft of the review document.\nAuthor: Yannick Kaminsky\nRecipient: Mattock squad\nThe incident record is attached.\n\nIncident INC-8861 on email:\n- opened: 16 February 2026, 05:35 (UTC+02:00)\n- users affected: 4362 users\n- urgency reported: cosmetic\n- customer data exposed: no\n- acknowledged: 16 February 2026, 06:27 (UTC+02:00)\n- check time: 16 February 2026, 06:57 (UTC+02:00)\n- minutes from opening to the check: 82\n- minutes from opening to the acknowledgement: 52\nCritical services: chat, login\nMaintenance window: 16 February 2026, 05:36 (UTC+02:00) to 16 February 2026, 06:14 (UTC+02:00)",
  "question": "Having applied the card's rules, can we say that incident INC-8861 reaches SEV2 as of the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV1, SEV3; partial SEV3, SEV2, SEV4; minimal SEV4, SEV3, SEV4.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 60 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: one level more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qf5e16fb7dd",
  "kind": "yes/no",
  "text": "from: Wilhelmina Ismail\nfor: Zorrel crew\ndetails follow\n\nIncident INC-5544 on email:\n- opened: 23 February 2026, 11:05 (UTC-05:00)\n- users affected: 42 users\n- urgency reported: outage\n- customer data exposed: no\n- acknowledged: not acknowledged\n- check time: 23 February 2026, 17:49 (UTC+01:00)\nCritical services: payments, chat\nMaintenance window: 23 February 2026, 11:39 (UTC-05:00) to 23 February 2026, 13:59 (UTC-05:00)",
  "question": "Is it not the case that incident INC-5544 does not reach SEV3 at the check time?",
  "definitions": "SEV1 most severe, SEV4 least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV4, SEV2, SEV1; partial SEV4, SEV2, SEV2; minimal SEV4, SEV3, SEV3.\nIn order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4; no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 45 minutes after opening; each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV2 or more severe.\nTimes are whole minutes at fixed UTC offsets, compared as points in time.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q4d17736a5e",
  "kind": "choice",
  "text": "Forwarded for Corrowen desk, written by Corentin Orellana. Details are attached.\n\nIncident INC-8529 on search:\n- opened: 2026-09-22 22:20:00 +0100\n- users affected: 3,295 users\n- urgency reported: degraded\n- customer data exposed: no\n- acknowledged: 2026-09-22 22:31:00 +0100\n- check time: 2026-09-22 22:36:00 +0100\n- minutes from opening to the check: 16\n- minutes from opening to the acknowledgement: 11\nCritical services: reports, chat\nMaintenance window: 2026-09-22 20:30:00 +0100 to 2026-09-22 23:41:00 +0100",
  "question": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV2, SEV1; partial SEV4, SEV3, SEV2; minimal SEV4, SEV4, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 15 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV2 or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nWhich level holds for incident INC-8529 at the check time, going by the card?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "q5709db0600",
  "kind": "yes/no",
  "text": "Warm greetings to Corrowen desk, from Corentin Orellana at a neighbouring department.\nKindly find the incident record attached, and please see the details below.\n\nIncident INC-2061 on checkout:\n- opened: 2026-04-29 05:25:00 +0530\n- users affected: 1385 users\n- urgency reported: cosmetic\n- customer data exposed: no\n- acknowledged: 2026-04-29 05:58:00 +0530\n- check time: 2026-04-29 07:14:00 +0530\n- minutes from opening to the check: 109\n- minutes from opening to the acknowledgement: 33\nCritical services: search, storage\nMaintenance window: 2026-04-28 23:58:00 +0530 to 2026-04-29 03:55:00 +0530",
  "question": "Is it true, for a new on-call engineer, that incident INC-2061 sits at SEV4 or less severe at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV4, SEV1, SEV2; partial SEV4, SEV2, SEV2; minimal SEV4, SEV3, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 45 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: one level more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qa0fb12b10e",
  "kind": "yes/no",
  "text": "Ayesha Mottram kindly forwards this for Drumlin squad\nthe record is pasted below\n\nIncident INC-9189 on chat:\n- opened: 2026-09-13T05:55:00-05:00\n- users affected: eighteen users\n- urgency reported: degraded\n- customer data exposed: no\n- acknowledged: 2026-09-13T06:08:00-05:00\n- check time: 2026-09-13T06:14:00-05:00\n- minutes from opening to the check: nineteen\n- minutes from opening to the acknowledgement: thirteen\nCritical services: reports, email\nMaintenance window: 2026-09-13T05:30:00-05:00 to 2026-09-13T08:23:00-05:00",
  "question": "Does applying the card's rules to incident INC-9189 produce a level that reaches SEV3 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 250 or more users, partial if 25 or more but fewer than 250, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV1, SEV3; partial SEV2, SEV3, SEV4; minimal SEV3, SEV4, SEV4.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 15 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV2 or more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q929a83005c",
  "kind": "yes/no",
  "text": "Hi Zinnia desk,\nHanding across from Ngaio Abrahams.\nDetails are pasted beneath.\nCheers\n\nIncident INC-6712 on payments:\n- opened: 2026-02-04T17:00:00+01:00\n- users affected: 1,001 users\n- urgency reported: outage\n- customer data exposed: no\n- acknowledged: 2026-02-04T17:17:00+01:00\n- check time: 2026-02-04T17:47:00+01:00\n- minutes from opening to the check: 47\n- minutes from opening to the acknowledgement: 17\nCritical services: checkout, search\nMaintenance window: 2026-02-04T16:45:00+01:00 to 2026-02-04T17:04:00+01:00",
  "question": "Being new to on-call, would you say incident INC-6712 doesn't reach SEV3 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 1,000 or more users, partial if 100 or more but fewer than 1,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV1, SEV1; partial SEV4, SEV2, SEV3; minimal SEV4, SEV3, SEV4.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 30 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV2 or more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qe419c6dfb3",
  "kind": "yes/no",
  "text": "Cobnut unit: take this\nfrom Winifred Imanov, details follow\n\nIncident INC-8616 on chat:\n| field | value |\n|---|---|\n| opened | 2026-06-25T00:35:00Z |\n| users affected | 1227 users |\n| urgency reported | degraded |\n| customer data exposed | no |\n| acknowledged | 2026-06-25T00:44:00Z |\n| check time | 2026-06-25T02:04:00Z |\n| minutes from opening to the check | 89 |\n| minutes from opening to the acknowledgement | 9 |\nCritical services: checkout, login\nMaintenance window: 2026-06-24T22:50:00Z to 2026-06-25T01:03:00Z",
  "question": "Is it true that incident INC-8616 fails to reach SEV3 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV3, SEV1; partial SEV3, SEV4, SEV1; minimal SEV3, SEV4, SEV2.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 30 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV1.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q4d5332e6a0",
  "kind": "yes/no",
  "text": "To Chickweed desk,\nThis formal notice is from Katalin Xuereb, and the incident record is enclosed for your review.\nRespectfully\n\nIncident INC-4653 on search:\n- opened: 2026-09-20 14:40:00 -0300\n- users affected: 427 users\n- urgency reported: outage\n- customer data exposed: no\n- acknowledged: 2026-09-20 15:06:00 -0300\n- check time: 2026-09-20 15:16:00 -0300\n- minutes from opening to the check: 36\n- minutes from opening to the acknowledgement: 26\nCritical services: checkout, login\nMaintenance window: 2026-09-20 12:55:00 -0300 to 2026-09-20 16:44:00 -0300",
  "question": "Being new to on-call, would you say incident INC-4653 fails to reach SEV3 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV3, SEV1; partial SEV3, SEV4, SEV2; minimal SEV4, SEV4, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 30 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV1.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q749461cef6",
  "kind": "choice",
  "text": "Filed by Wojtek Jaworski, sent on to Gantry crew, record attached.\n\nIncident INC-8088 on search:\n- opened: 20 February 2026, 03:10 (UTC+02:00)\n- users affected: 799 users\n- urgency reported: degraded\n- customer data exposed: no\n- acknowledged: 20 February 2026, 04:10 (UTC+02:00)\n- check time: 20 February 2026, 04:17 (UTC+02:00)\n- minutes from opening to the check: 67\n- minutes from opening to the acknowledgement: 60\nCritical services: login, payments\nMaintenance window: 20 February 2026, 02:32 (UTC+02:00) to 20 February 2026, 03:10 (UTC+02:00)",
  "question": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV1, SEV1; partial SEV4, SEV3, SEV2; minimal SEV4, SEV4, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 45 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV1.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nBriefly, under the card's rules, which severity is incident INC-8088 at the check time?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "qea232f9944",
  "kind": "yes/no",
  "text": "Yrsa Kerrigan here, with a short draft for Fardel watch. The details are attached.\n\nIncident INC-3298 on search:\n- opened: 2 April 2026, 16:20 (UTC+05:30)\n- users affected: 1,642 users\n- urgency reported: cosmetic\n- customer data exposed: no\n- acknowledged: 2 April 2026, 20:00 (UTC+09:00)\n- check time: 2 April 2026, 20:50 (UTC+09:00)\nCritical services: email, storage\nMaintenance window: none declared",
  "question": "For a newcomer on the rota, is it the case that incident INC-3298 does not reach SEV2 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 1,000 or more users, partial if 100 or more but fewer than 1,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV1, SEV1; partial SEV4, SEV3, SEV2; minimal SEV4, SEV4, SEV3.\nThen, in order:\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 30 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV1.\nTimes are whole minutes at fixed UTC offsets, compared as points in time.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q5b2c4dcbc4",
  "kind": "yes/no",
  "text": "to: Eskerline cell\nfrom: Ximena Jurado\nalert: thanks, the record is pasted below\n\nIncident INC-5943 on search:\n- opened: 2026-05-02 22:15:00 +0100\n- users affected: 694 users\n- urgency reported: degraded\n- customer data exposed: no\n- acknowledged: 2026-05-03 03:04:00 +0530\n- check time: 2026-05-03 04:21:00 +0530\nCritical services: checkout, reports\nMaintenance window: 2026-05-02 22:24:00 +0100 to 2026-05-03 00:34:00 +0100",
  "question": "Would the card put incident INC-5943 at a level of SEV3 or more severe at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV1, SEV3; partial SEV3, SEV1, SEV4; minimal SEV3, SEV2, SEV4.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 45 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV1.\nTimes are whole minutes at fixed UTC offsets, compared as points in time.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q40c58b39bc",
  "kind": "choice",
  "text": "Brief from Zeljka Lindahl for Mattock squad. Full record attached.\n\nIncident INC-8026 on email:\n- opened: 2026-10-02 11:05:00 +0200\n- users affected: 99 users\n- urgency reported: degraded\n- customer data exposed: yes\n- acknowledged: not acknowledged\n- check time: 2026-10-02T09:13:00Z\nCritical services: search, storage\nMaintenance window: 2026-10-02 10:00:00 +0200 to 2026-10-02 13:07:00 +0200",
  "question": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 1,000 or more users, partial if 100 or more but fewer than 1,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV1, SEV2; partial SEV4, SEV1, SEV3; minimal SEV4, SEV2, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 60 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV2 or more severe.\nTimes are whole minutes at fixed UTC offsets, compared as points in time.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nIn short, as of the check time, which severity sits on incident INC-8026 under the card?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "q446683b618",
  "kind": "yes/no",
  "text": "Routing note: Ulric Ilyasova to Nutmeg cell.\nThe incident record follows.\n\nIncident INC-6339 on search:\n- opened: 2026-04-05T12:50:00+02:00\n- users affected: 18 users\n- urgency reported: degraded\n- customer data exposed: no\n- acknowledged: 2026-04-05T05:55:00-05:00\n- check time: 2026-04-05T05:59:00-05:00\nCritical services: chat, checkout\nMaintenance window: 2026-04-05T10:58:00+02:00 to 2026-04-05T12:20:00+02:00",
  "question": "Would incident INC-6339 count as SEV3 or more severe as of the check time, according to the card's rules?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 1,000 or more users, partial if 100 or more but fewer than 1,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV3, SEV2; partial SEV1, SEV4, SEV3; minimal SEV2, SEV4, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 20 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV1.\nTimes are whole minutes at fixed UTC offsets, compared as points in time.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q3cd0836850",
  "kind": "choice",
  "text": "Respectfully routed to Ferrule watch by Saoirse Feldmann.\nThe full record is attached.\n\nIncident INC-8436 on search:\n- opened: 17 February 2026, 12:45 (UTC+09:00)\n- users affected: 459 users\n- urgency reported: cosmetic\n- customer data exposed: no\n- acknowledged: 17 February 2026, 13:03 (UTC+09:00)\n- check time: 17 February 2026, 13:08 (UTC+09:00)\n- minutes from opening to the check: 23\n- minutes from opening to the acknowledgement: eighteen\nCritical services: login, chat\nMaintenance window: 17 February 2026, 13:55 (UTC+09:00) to 17 February 2026, 16:09 (UTC+09:00)",
  "question": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 1,000 or more users, partial if 100 or more but fewer than 1,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV1, SEV1; partial SEV4, SEV3, SEV2; minimal SEV4, SEV4, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 15 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: one level more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nWhich severity level does the card's rule set assign to incident INC-8436 as of the check time?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "q8173d6a1ba",
  "kind": "choice",
  "text": "Bot relay. Added by Paulina Esposito. For Mallard squad. Record below.\n\nIncident INC-4976 on checkout:\n| field | value |\n|---|---|\n| opened | 2026-07-24 13:00:00 +0900 |\n| users affected | 2043 users |\n| urgency reported | degraded |\n| customer data exposed | no |\n| acknowledged | 2026-07-24 13:20:00 +0900 |\n| check time | 2026-07-24 14:19:00 +0900 |\n| minutes from opening to the check | 79 |\n| minutes from opening to the acknowledgement | twenty |\nCritical services: storage, email\nMaintenance window: none declared",
  "question": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV2, SEV1; partial SEV4, SEV3, SEV2; minimal SEV4, SEV4, SEV3.\nThen, in order:\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 30 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV2 or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nUsing the card's rules, what severity level must be recorded for incident INC-4976 at the check time?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "q6845c8d052",
  "kind": "choice",
  "text": "Dear colleagues on Sorrel squad, this is Deepak Pruitt writing to you from a neighbouring department, with thanks in good faith.\nThe incident record follows below, kindly laid out for your reading.\n\nIncident INC-7836 on chat:\n- opened: 2026-06-29T21:10:00-05:00\n- users affected: zero users\n- urgency reported: cosmetic\n- customer data exposed: no\n- acknowledged: 2026-06-29T21:18:00-05:00\n- check time: 2026-06-29T21:23:00-05:00\n- minutes from opening to the check: thirteen\n- minutes from opening to the acknowledgement: eight\nCritical services: storage, chat\nMaintenance window: 2026-06-29T15:59:00-05:00 to 2026-06-29T19:40:00-05:00",
  "question": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV3, SEV2; partial SEV1, SEV4, SEV3; minimal SEV2, SEV4, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 45 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV1.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nAs a new on-call engineer, could you tell me what level incident INC-7836 holds as of the check time under the card's rules?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "q7c006f9a09",
  "kind": "yes/no",
  "text": "Handover note from Rasmus Dvorsky to Quillet rota, recorded in the runbook.\nThe incident record follows below.\n\nIncident INC-8248 on payments:\n| field | value |\n|---|---|\n| opened | 23 January 2026, 13:25 (UTC+01:00) |\n| users affected | 95 users |\n| urgency reported | cosmetic |\n| customer data exposed | no |\n| acknowledged | not acknowledged |\n| check time | 23 January 2026, 13:54 (UTC+01:00) |\n| minutes from opening to the check | 29 |\nCritical services: email, storage\nMaintenance window: 23 January 2026, 13:59 (UTC+01:00) to 23 January 2026, 15:33 (UTC+01:00)",
  "question": "As a new on-call engineer, do you find that incident INC-8248 fails to reach SEV3 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV2, SEV3; partial SEV1, SEV3, SEV4; minimal SEV2, SEV3, SEV4.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 30 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: one level more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qb453562ddf",
  "kind": "yes/no",
  "text": "Sent by: Saoirse Feldmann\nSent to: Cinderlane squad\nSubject: transfer of record\nDetails: see the record below.\n\nIncident INC-2014 on chat:\n| field | value |\n|---|---|\n| opened | 2026-04-28T03:40:00+05:30 |\n| users affected | 1291 users |\n| urgency reported | outage |\n| customer data exposed | no |\n| acknowledged | 2026-04-28T03:49:00+05:30 |\n| check time | 2026-04-28T04:19:00+05:30 |\n| minutes from opening to the check | 39 |\n| minutes from opening to the acknowledgement | 9 |\nCritical services: payments, checkout\nMaintenance window: 2026-04-28T05:20:00+05:30 to 2026-04-28T09:19:00+05:30",
  "question": "Do the rules on the card show that incident INC-2014 reaches SEV3 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 1,000 or more users, partial if 100 or more but fewer than 1,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV4, SEV1, SEV2; partial SEV4, SEV2, SEV2; minimal SEV4, SEV3, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 15 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV1.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qa140c99056",
  "kind": "yes/no",
  "text": "From: Ximena Jurado\nTo: Eskerline cell\nHandover details are attached.\n\nIncident INC-5691 on payments:\n- opened: 16 January 2026, 18:00 (UTC+00:00)\n- users affected: 4791 users\n- urgency reported: outage\n- customer data exposed: no\n- acknowledged: 16 January 2026, 18:15 (UTC+00:00)\n- check time: 16 January 2026, 18:23 (UTC+00:00)\n- minutes from opening to the check: 23\n- minutes from opening to the acknowledgement: 15\nCritical services: storage, login\nMaintenance window: none declared",
  "question": "Honestly, is the card's verdict that incident INC-5691 reaches SEV3 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV4, SEV2; partial SEV2, SEV4, SEV2; minimal SEV3, SEV4, SEV3.\nThen, in order:\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 15 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV1.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q1e7e4336d2",
  "kind": "choice",
  "text": "From: Corentin Orellana\nTo: Corrowen desk\nNotes and record follow below.\n\nIncident INC-5567 on payments:\n- opened: 2026-04-18T04:35:00+09:00\n- users affected: 11 users\n- urgency reported: outage\n- customer data exposed: no\n- acknowledged: 2026-04-18T04:48:00+09:00\n- check time: 2026-04-18T05:10:00+09:00\n- minutes from opening to the check: 35\n- minutes from opening to the acknowledgement: 13\nCritical services: email, storage\nMaintenance window: 2026-04-18T05:08:00+09:00 to 2026-04-18T07:19:00+09:00",
  "question": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 250 or more users, partial if 25 or more but fewer than 250, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV2, SEV1; partial SEV4, SEV3, SEV2; minimal SEV4, SEV4, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 20 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV1.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nWhat level do the card's rules say incident INC-5567 has as of the check time?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "qe98bf06519",
  "kind": "yes/no",
  "text": "For Bellfounder desk from Ursel Gorczyca: record follows.\n\nIncident INC-2059 on login:\n| field | value |\n|---|---|\n| opened | 2026-09-04T08:50:00-05:00 |\n| users affected | 7 users |\n| urgency reported | outage |\n| customer data exposed | no |\n| acknowledged | not acknowledged |\n| check time | 2026-09-04T09:24:00-05:00 |\n| minutes from opening to the check | 34 |\nCritical services: payments, chat\nMaintenance window: none declared",
  "question": "At the check time, is it not true that incident INC-2059 does not reach SEV3?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 1,000 or more users, partial if 100 or more but fewer than 1,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV1, SEV3; partial SEV3, SEV2, SEV4; minimal SEV4, SEV3, SEV4.\nThen, in order:\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 45 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV2 or more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qcfd49a676b",
  "kind": "yes/no",
  "text": "Fardel watch, message from Ximena Jurado: the incident record is attached.\n\nIncident INC-8031 on reports:\n- opened: 2026-04-12T14:30:00+01:00\n- users affected: 1,000 users\n- urgency reported: degraded\n- customer data exposed: no\n- acknowledged: 2026-04-12T14:59:00+01:00\n- check time: 2026-04-12T15:29:00+01:00\n- minutes from opening to the check: 59\n- minutes from opening to the acknowledgement: 29\nCritical services: chat, search\nMaintenance window: none declared",
  "question": "Could a newcomer confirm that incident INC-8031 fails to reach SEV2 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 1,000 or more users, partial if 100 or more but fewer than 1,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV2, SEV3; partial SEV2, SEV3, SEV4; minimal SEV3, SEV4, SEV4.\nThen, in order:\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 30 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: one level more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q1434a727c3",
  "kind": "yes/no",
  "text": "Warm hellos to Dunmarrow unit from Bruna Nemeth, and the details of the review follow beneath.\n\nIncident INC-7757 on storage:\n- opened: 17 June 2026, 22:00 (UTC+02:00)\n- users affected: 785 users\n- urgency reported: outage\n- customer data exposed: yes\n- acknowledged: 17 June 2026, 21:07 (UTC+01:00)\n- check time: 17 June 2026, 21:34 (UTC+01:00)\nCritical services: login, checkout\nMaintenance window: 17 June 2026, 20:40 (UTC+02:00) to 18 June 2026, 00:30 (UTC+02:00)",
  "question": "As a newcomer starting in on-call work, is incident INC-7757 at SEV3 or less severe as of the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 1,000 or more users, partial if 100 or more but fewer than 1,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV4, SEV1; partial SEV2, SEV4, SEV2; minimal SEV3, SEV4, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 15 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: one level more severe.\nTimes are whole minutes at fixed UTC offsets, compared as points in time.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q9c1549e091",
  "kind": "yes/no",
  "text": "Gaspar Sokolov here, sending this over to Jorvell desk with the details below. Happy to help with questions.\n\nIncident INC-8724 on reports:\n| field | value |\n|---|---|\n| opened | 31 October 2026, 06:05 (UTC-03:00) |\n| users affected | 186 users |\n| urgency reported | degraded |\n| customer data exposed | no |\n| acknowledged | 31 October 2026, 06:26 (UTC-03:00) |\n| check time | 31 October 2026, 07:13 (UTC-03:00) |\n| minutes from opening to the check | 68 |\n| minutes from opening to the acknowledgement | 21 |\nCritical services: login, chat\nMaintenance window: 31 October 2026, 02:50 (UTC-03:00) to 31 October 2026, 06:05 (UTC-03:00)",
  "question": "For a newcomer on the rota, is it the case that incident INC-8724 does not reach SEV2 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV1, SEV3; partial SEV3, SEV2, SEV4; minimal SEV4, SEV3, SEV4.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 30 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV2 or more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qf966d05114",
  "kind": "yes/no",
  "text": "heads-up: Zabrine crew\nfrom: Hiroshi Upadhyay\nnote: incident record attached, thank you\n\nIncident INC-6416 on chat:\n- opened: 2026-01-06T19:05:00Z\n- users affected: 189 users\n- urgency reported: outage\n- customer data exposed: no\n- acknowledged: not acknowledged\n- check time: 2026-01-06T19:42:00Z\n- minutes from opening to the check: 37\nCritical services: reports, login\nMaintenance window: 2026-01-06T18:15:00Z to 2026-01-06T19:15:00Z",
  "question": "Is it not true that, as of the check time, incident INC-6416 does not reach SEV3?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 250 or more users, partial if 25 or more but fewer than 250, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV2, SEV1; partial SEV4, SEV3, SEV1; minimal SEV4, SEV3, SEV2.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 45 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV2 or more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q1edb65f024",
  "kind": "yes/no",
  "text": "Subject: draft update\nFor Zinnia desk, from Ngaio Abrahams. See the record.\n\nIncident INC-2055 on payments:\n- opened: 30 September 2026, 22:55 (UTC+09:00)\n- users affected: 562 users\n- urgency reported: outage\n- customer data exposed: no\n- acknowledged: 30 September 2026, 23:22 (UTC+09:00)\n- check time: 1 October 2026, 00:43 (UTC+09:00)\n- minutes from opening to the check: 108\n- minutes from opening to the acknowledgement: 27\nCritical services: checkout, reports\nMaintenance window: none declared",
  "question": "Could a newcomer confirm that incident INC-2055 fails to reach SEV3 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV1, SEV3; partial SEV2, SEV3, SEV4; minimal SEV3, SEV4, SEV4.\nThen, in order:\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 45 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV2 or more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q0aa8602d87",
  "kind": "choice",
  "text": "Hi Arkwold rota,\nSending this over from Winifred Imanov.\nThe incident record and details are attached.\nCheers\n\nIncident INC-8503 on checkout:\n| field | value |\n|---|---|\n| opened | 2026-08-27 00:35:00 +0900 |\n| users affected | 64 users |\n| urgency reported | outage |\n| customer data exposed | no |\n| acknowledged | 2026-08-27 01:03:00 +0900 |\n| check time | 2026-08-27 02:19:00 +0900 |\n| minutes from opening to the check | 104 |\n| minutes from opening to the acknowledgement | 28 |\nCritical services: login, search\nMaintenance window: 2026-08-26 23:55:00 +0900 to 2026-08-27 02:55:00 +0900",
  "question": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 1,000 or more users, partial if 100 or more but fewer than 1,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV4, SEV2, SEV1; partial SEV4, SEV2, SEV2; minimal SEV4, SEV3, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 60 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV2 or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nUsing the card, what level is incident INC-8503 at the check time?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "q462551664d",
  "kind": "choice",
  "text": "Handover note from Kiran Pembrick to Wrenhald cell, recorded in the runbook.\nThe incident record follows below.\n\nIncident INC-1655 on reports:\n| field | value |\n|---|---|\n| opened | 30 October 2026, 17:40 (UTC+02:00) |\n| users affected | 219 users |\n| urgency reported | degraded |\n| customer data exposed | yes |\n| acknowledged | 30 October 2026, 18:43 (UTC+02:00) |\n| check time | 30 October 2026, 19:31 (UTC+02:00) |\n| minutes from opening to the check | 111 |\n| minutes from opening to the acknowledgement | 63 |\nCritical services: login, search\nMaintenance window: 30 October 2026, 18:09 (UTC+02:00) to 30 October 2026, 20:12 (UTC+02:00)",
  "question": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV2, SEV4; partial SEV2, SEV2, SEV4; minimal SEV3, SEV3, SEV4.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 60 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: one level more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nSo going by the card, what level has incident INC-1655 landed on at the check time?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "q3bf0610ba0",
  "kind": "yes/no",
  "text": "Passing this along to Ismere cell, written by Hafsa Havelin. Record attached.\n\nIncident INC-2224 on reports:\n- opened: 24 August 2026, 09:55 (UTC+02:00)\n- users affected: 1,324 users\n- urgency reported: degraded\n- customer data exposed: no\n- acknowledged: 24 August 2026, 10:09 (UTC+02:00)\n- check time: 24 August 2026, 10:23 (UTC+02:00)\n- minutes from opening to the check: 28\n- minutes from opening to the acknowledgement: 14\nCritical services: checkout, email\nMaintenance window: none declared",
  "question": "New on-call engineer here: does incident INC-2224 fail to reach SEV3 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV3, SEV1; partial SEV3, SEV4, SEV2; minimal SEV4, SEV4, SEV3.\nThen, in order:\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 20 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV1.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qe4b4321a4d",
  "kind": "yes/no",
  "text": "note from Yrsa Kerrigan, kindly directed to Drumlin squad\nrecord attached for your review\n\nIncident INC-6805 on payments:\n- opened: 2026-04-26 04:10:00 +0530\n- users affected: nine users\n- urgency reported: outage\n- customer data exposed: no\n- acknowledged: 2026-04-25 22:52:00 +0000\n- check time: 2026-04-25 23:32:00 +0000\nCritical services: login, checkout\nMaintenance window: 2026-04-26 02:35:00 +0530 to 2026-04-26 06:00:00 +0530",
  "question": "Simply put, does incident INC-6805 reach SEV3 as of the check time, per the card's rules?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 250 or more users, partial if 25 or more but fewer than 250, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV1, SEV3; partial SEV3, SEV1, SEV4; minimal SEV3, SEV2, SEV4.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 20 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV1.\nTimes are whole minutes at fixed UTC offsets, compared as points in time.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qebe2b6d21f",
  "kind": "choice",
  "text": "handover notice for Mallard squad\nsubmitted by Ottavio Dressler, record enclosed\n\nIncident INC-2701 on payments:\n| field | value |\n|---|---|\n| opened | 2026-05-24T23:50:00+02:00 |\n| users affected | 1322 users |\n| urgency reported | degraded |\n| customer data exposed | no |\n| acknowledged | 2026-05-25T00:07:00+02:00 |\n| check time | 2026-05-25T00:17:00+02:00 |\n| minutes from opening to the check | 27 |\n| minutes from opening to the acknowledgement | seventeen |\nCritical services: reports, storage\nMaintenance window: 2026-05-24T21:16:00+02:00 to 2026-05-24T23:20:00+02:00",
  "question": "SEV1 most severe, SEV4 least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV1, SEV3; partial SEV3, SEV1, SEV4; minimal SEV3, SEV2, SEV4.\nIn order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4; no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 20 minutes after opening; each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV1.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nAs a new on-call engineer, could you tell me what level incident INC-2701 holds as of the check time under the card's rules?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "qb2b271e8b1",
  "kind": "yes/no",
  "text": "to: Mattock squad\nspotted by Yannick Kaminsky, details pasted below, cheers!\n\nIncident INC-2409 on reports:\n- opened: 2026-01-30T18:25:00+01:00\n- users affected: 35 users\n- urgency reported: cosmetic\n- customer data exposed: no\n- acknowledged: 2026-01-30T18:40:00+01:00\n- check time: 2026-01-30T19:22:00+01:00\n- minutes from opening to the check: 57\n- minutes from opening to the acknowledgement: 15\nCritical services: payments, search\nMaintenance window: 2026-01-30T16:00:00+01:00 to 2026-01-30T18:25:00+01:00",
  "question": "Is it fair to say incident INC-2409 reaches SEV3 as of the check time under the card?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV2, SEV3; partial SEV2, SEV3, SEV4; minimal SEV3, SEV4, SEV4.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 15 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV1.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q6ef771bac6",
  "kind": "yes/no",
  "text": "to: Dimmorrow cell\nfrom: Quenton Dombrowski\nnote: lovely to flag this, record below\n\nIncident INC-5364 on email:\n| field | value |\n|---|---|\n| opened | 2026-06-23T22:25:00-03:00 |\n| users affected | 127 users |\n| urgency reported | degraded |\n| customer data exposed | no |\n| acknowledged | 2026-06-23T22:54:00-03:00 |\n| check time | 2026-06-23T23:50:00-03:00 |\n| minutes from opening to the check | 85 |\n| minutes from opening to the acknowledgement | 29 |\nCritical services: payments, chat\nMaintenance window: none declared",
  "question": "So does incident INC-5364 reach SEV3 at the check time, going by the card?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV3, SEV1; partial SEV3, SEV4, SEV2; minimal SEV4, SEV4, SEV3.\nThen, in order:\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 30 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: one level more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q5fa65abb2d",
  "kind": "yes/no",
  "text": "This review document is being drafted by Matthias Zaleski for Mallard squad, and the incident record is pasted below.\n\nIncident INC-9489 on search:\n| field | value |\n|---|---|\n| opened | 2026-10-16 06:00:00 +0900 |\n| users affected | 8 users |\n| urgency reported | cosmetic |\n| customer data exposed | yes |\n| acknowledged | 2026-10-16 06:03:00 +0900 |\n| check time | 2026-10-16 06:22:00 +0900 |\n| minutes from opening to the check | 22 |\n| minutes from opening to the acknowledgement | 3 |\nCritical services: email, chat\nMaintenance window: none declared",
  "question": "Is incident INC-9489 at SEV4 or less severe at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV2, SEV3; partial SEV2, SEV3, SEV4; minimal SEV3, SEV4, SEV4.\nThen, in order:\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 15 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: one level more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qc214760a42",
  "kind": "yes/no",
  "text": "Raised by: Tobiah Ilunga\nAssigned to: Quillan guild\nSubject: hand-off\nNote: we are grateful for your help, and the record is attached.\n\nIncident INC-9347 on search:\n- opened: 7 April 2026, 18:30 (UTC+01:00)\n- users affected: 40 users\n- urgency reported: degraded\n- customer data exposed: no\n- acknowledged: 7 April 2026, 19:04 (UTC+01:00)\n- check time: 7 April 2026, 20:31 (UTC+01:00)\n- minutes from opening to the check: 121\n- minutes from opening to the acknowledgement: 34\nCritical services: storage, checkout\nMaintenance window: none declared",
  "question": "Simply put, does incident INC-9347 reach SEV3 as of the check time, per the card's rules?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV1, SEV1; partial SEV4, SEV3, SEV2; minimal SEV4, SEV4, SEV3.\nThen, in order:\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 60 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV1.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qb59c392de3",
  "kind": "yes/no",
  "text": "For Tinderwick unit from Maelys Zarnecki: record follows.\n\nIncident INC-7068 on reports:\n- opened: 10 January 2026, 22:50 (UTC-05:00)\n- users affected: 499 users\n- urgency reported: outage\n- customer data exposed: no\n- acknowledged: not acknowledged\n- check time: 10 January 2026, 23:03 (UTC-05:00)\n- minutes from opening to the check: thirteen\nCritical services: payments, storage\nMaintenance window: 10 January 2026, 19:56 (UTC-05:00) to 10 January 2026, 22:50 (UTC-05:00)",
  "question": "Is incident INC-7068 classed as SEV3 or more severe at the check time, as set out in the card's rules?",
  "definitions": "SEV1 most severe, SEV4 least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV4, SEV1; partial SEV2, SEV4, SEV2; minimal SEV3, SEV4, SEV3.\nIn order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4; no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 15 minutes after opening; each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: one level more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q9aad98bbe3",
  "kind": "yes/no",
  "text": "Hi Rookery unit, thanks for picking this up. Handoff from Elowen Quarrell, the full record is attached below.\n\nIncident INC-6502 on email:\n- opened: 2026-05-19T19:35:00Z\n- users affected: 249 users\n- urgency reported: degraded\n- customer data exposed: no\n- acknowledged: 2026-05-19T19:56:00Z\n- check time: 2026-05-19T20:49:00Z\n- minutes from opening to the check: 74\n- minutes from opening to the acknowledgement: 21\nCritical services: login, search\nMaintenance window: 2026-05-19T19:15:00Z to 2026-05-19T20:31:00Z",
  "question": "Is it fair to say incident INC-6502 reaches SEV2 as of the check time under the card?",
  "definitions": "SEV1 most severe, SEV4 least.\nImpact: wide if 250 or more users, partial if 25 or more but fewer than 250, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV1, SEV1; partial SEV4, SEV2, SEV3; minimal SEV4, SEV3, SEV4.\nIn order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4; no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 30 minutes after opening; each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV1.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q48345a3ab3",
  "kind": "yes/no",
  "text": "assigned to: Mistrel cell\nfrom: Nasrin Zeidler\nrecord below\n\nIncident INC-3417 on payments:\n| field | value |\n|---|---|\n| opened | 2026-03-08T23:00:00+09:00 |\n| users affected | 475 users |\n| urgency reported | outage |\n| customer data exposed | no |\n| acknowledged | 2026-03-08T23:13:00+09:00 |\n| check time | 2026-03-09T01:02:00+09:00 |\n| minutes from opening to the check | 122 |\n| minutes from opening to the acknowledgement | 13 |\nCritical services: chat, email\nMaintenance window: 2026-03-08T19:01:00+09:00 to 2026-03-08T23:00:00+09:00",
  "question": "For a newcomer on the rota, is it the case that incident INC-3417 does not reach SEV3 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 1,000 or more users, partial if 100 or more but fewer than 1,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV2, SEV1; partial SEV4, SEV3, SEV1; minimal SEV4, SEV3, SEV2.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 45 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV1.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q89fc158079",
  "kind": "yes/no",
  "text": "For Tinderwick unit from Maelys Zarnecki: record follows.\n\nIncident INC-7068 on reports:\n- opened: 10 January 2026, 22:50 (UTC-05:00)\n- users affected: 499 users\n- urgency reported: degraded\n- customer data exposed: no\n- acknowledged: not acknowledged\n- check time: 10 January 2026, 23:03 (UTC-05:00)\n- minutes from opening to the check: thirteen\nCritical services: payments, storage\nMaintenance window: 10 January 2026, 19:56 (UTC-05:00) to 10 January 2026, 22:50 (UTC-05:00)",
  "question": "Is incident INC-7068 classed as SEV3 or more severe at the check time, as set out in the card's rules?",
  "definitions": "SEV1 most severe, SEV4 least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV4, SEV1; partial SEV2, SEV4, SEV2; minimal SEV3, SEV4, SEV3.\nIn order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4; no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 15 minutes after opening; each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: one level more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q7c578e3dec",
  "kind": "choice",
  "text": "Relay note: Rafaela Dumont entry, for Galdra squad. Record attached.\n\nIncident INC-5192 on checkout:\n| field | value |\n|---|---|\n| opened | 2026-09-28T02:35:00+09:00 |\n| users affected | 11 users |\n| urgency reported | cosmetic |\n| customer data exposed | no |\n| acknowledged | not acknowledged |\n| check time | 2026-09-28T04:34:00+09:00 |\n| minutes from opening to the check | 119 |\nCritical services: login, email\nMaintenance window: 2026-09-27T23:01:00+09:00 to 2026-09-28T02:05:00+09:00",
  "question": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 250 or more users, partial if 25 or more but fewer than 250, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV3, SEV1; partial SEV3, SEV4, SEV1; minimal SEV3, SEV4, SEV2.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 60 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: one level more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nIn short, as of the check time, which severity sits on incident INC-5192 under the card?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "qea0730b3b8",
  "kind": "choice",
  "text": "Subject: handover\nAssigned team: Whinmoor cell, raised by Adaeze Nieminen. Please see the incident details pasted below.\n\nIncident INC-9154 on chat:\n| field | value |\n|---|---|\n| opened | 2026-04-26T08:25:00+02:00 |\n| users affected | 12 users |\n| urgency reported | degraded |\n| customer data exposed | yes |\n| acknowledged | 2026-04-26T08:27:00+02:00 |\n| check time | 2026-04-26T09:10:00+02:00 |\n| minutes from opening to the check | 45 |\n| minutes from opening to the acknowledgement | 2 |\nCritical services: search, login\nMaintenance window: 2026-04-26T08:56:00+02:00 to 2026-04-26T10:12:00+02:00",
  "question": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV1, SEV3; partial SEV3, SEV2, SEV4; minimal SEV4, SEV3, SEV4.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 20 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV2 or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nWhere does the card put incident INC-9154 as far as level goes at the check time?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "qe3f5a1274d",
  "kind": "yes/no",
  "text": "Dear Corrowen desk,\nThis message is sent by Ambrose Mahlangu, and the incident record is set out below.\nYours faithfully\n\nIncident INC-2959 on login:\n- opened: 23 May 2026, 01:40 (UTC+09:00)\n- users affected: 0 users\n- urgency reported: outage\n- customer data exposed: no\n- acknowledged: 22 May 2026, 23:11 (UTC+05:30)\n- check time: 22 May 2026, 23:11 (UTC+05:30)\nCritical services: reports, storage\nMaintenance window: 22 May 2026, 22:01 (UTC+09:00) to 23 May 2026, 01:40 (UTC+09:00)",
  "question": "Going by the card, does incident INC-2959 reach SEV3 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV3, SEV1; partial SEV3, SEV4, SEV2; minimal SEV4, SEV4, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 20 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV1.\nTimes are whole minutes at fixed UTC offsets, compared as points in time.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qfa1899d8cb",
  "kind": "yes/no",
  "text": "Mattock squad: Benedykt Sundgren here. Record and details below.\n\nIncident INC-6356 on login:\n- opened: 18 August 2026, 01:35 (UTC-05:00)\n- users affected: 250 users\n- urgency reported: cosmetic\n- customer data exposed: no\n- acknowledged: not acknowledged\n- check time: 18 August 2026, 02:03 (UTC-05:00)\n- minutes from opening to the check: 28\nCritical services: email, payments\nMaintenance window: 18 August 2026, 00:40 (UTC-05:00) to 18 August 2026, 02:28 (UTC-05:00)",
  "question": "For a newcomer on the rota, is it the case that incident INC-6356 does not reach SEV3 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 250 or more users, partial if 25 or more but fewer than 250, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV4, SEV2, SEV1; partial SEV4, SEV2, SEV2; minimal SEV4, SEV3, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 45 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: one level more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qb0e202d8af",
  "kind": "yes/no",
  "text": "Yehudit Kuchar spotted this, and the record for Yarnwood watch is attached below.\n\nIncident INC-1429 on checkout:\n- opened: 2026-05-14 08:30:00 +0200\n- users affected: 499 users\n- urgency reported: cosmetic\n- customer data exposed: no\n- acknowledged: 2026-05-14 09:00:00 +0200\n- check time: 2026-05-14 09:00:00 +0200\n- minutes from opening to the check: 30\n- minutes from opening to the acknowledgement: 30\nCritical services: payments, login\nMaintenance window: 2026-05-14 08:15:00 +0200 to 2026-05-14 09:04:00 +0200",
  "question": "Under the card's rules, does incident INC-1429 reach SEV2 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV1, SEV1; partial SEV4, SEV2, SEV3; minimal SEV4, SEV3, SEV4.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 30 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV1.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q4d2f2a66e4",
  "kind": "yes/no",
  "text": "for: Knapweed desk\nforwarded by: Nanami Achterberg\nfull details follow in the record\n\nIncident INC-8926 on email:\n| field | value |\n|---|---|\n| opened | 9 August 2026, 07:10 (UTC+09:00) |\n| users affected | 1304 users |\n| urgency reported | outage |\n| customer data exposed | no |\n| acknowledged | 9 August 2026, 07:47 (UTC+09:00) |\n| check time | 9 August 2026, 09:01 (UTC+09:00) |\n| minutes from opening to the check | 111 |\n| minutes from opening to the acknowledgement | 37 |\nCritical services: storage, login\nMaintenance window: 9 August 2026, 06:35 (UTC+09:00) to 9 August 2026, 09:05 (UTC+09:00)",
  "question": "Is it true that incident INC-8926 does not reach SEV3 at the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV3, SEV1, SEV1; partial SEV4, SEV3, SEV2; minimal SEV4, SEV4, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 45 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV1.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qb46b4972f6",
  "kind": "choice",
  "text": "Submitted by: Kiran Pembrick\nAddressed to: Sablevane squad\nSubject: handover\nDetails: thank you for your attention; the record follows.\n\nIncident INC-6004 on email:\n- opened: 2026-08-24T02:45:00Z\n- users affected: 382 users\n- urgency reported: degraded\n- customer data exposed: no\n- acknowledged: 2026-08-24 05:31:00 +0200\n- check time: 2026-08-24 05:45:00 +0200\nCritical services: checkout, storage\nMaintenance window: none declared",
  "question": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 1,000 or more users, partial if 100 or more but fewer than 1,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV4, SEV1; partial SEV2, SEV4, SEV2; minimal SEV3, SEV4, SEV3.\nThen, in order:\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 60 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV2 or more severe.\nTimes are whole minutes at fixed UTC offsets, compared as points in time.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nUsing the card's rules, what severity level must be recorded for incident INC-6004 at the check time?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "q1789d84d97",
  "kind": "yes/no",
  "text": "Who: Gunnhild Strudwick\nWhere: Sorrel squad\nSubject: handover\nFile: attached.\n\nIncident INC-8431 on chat:\n- opened: 2026-06-20 19:10:00 +0000\n- users affected: 17 users\n- urgency reported: outage\n- customer data exposed: no\n- acknowledged: 2026-06-20 14:26:00 -0500\n- check time: 2026-06-20 14:41:00 -0500\nCritical services: email, checkout\nMaintenance window: none declared",
  "question": "Under these rules, is it not the case that incident INC-8431 does not reach SEV2 as of the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV1, SEV2, SEV3; partial SEV1, SEV3, SEV4; minimal SEV2, SEV3, SEV4.\nThen, in order:\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 30 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: SEV1.\nTimes are whole minutes at fixed UTC offsets, compared as points in time.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qbcd39f55c7",
  "kind": "yes/no",
  "text": "Dear Hasterell guild,\nThis message is sent by Evander Quesada, and the incident record is set out below.\nYours faithfully\n\nIncident INC-4006 on storage:\n| field | value |\n|---|---|\n| opened | 2026-09-01T14:20:00-05:00 |\n| users affected | 499 users |\n| urgency reported | cosmetic |\n| customer data exposed | no |\n| acknowledged | 2026-09-01T14:26:00-05:00 |\n| check time | 2026-09-01T14:38:00-05:00 |\n| minutes from opening to the check | 18 |\n| minutes from opening to the acknowledgement | 6 |\nCritical services: login, chat\nMaintenance window: none declared",
  "question": "Under these rules, is it not the case that incident INC-4006 does not reach SEV3 as of the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV1, SEV3; partial SEV3, SEV1, SEV4; minimal SEV3, SEV2, SEV4.\nThen, in order:\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 15 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV1.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qb866d8124c",
  "kind": "choice",
  "text": "from Xiomara Jessop to Yarnwood watch\nrecord pasted below\n\nIncident INC-3719 on email:\n- opened: 2026-03-30T06:05:00+00:00\n- users affected: 361 users\n- urgency reported: cosmetic\n- customer data exposed: no\n- acknowledged: 2026-03-30T06:20:00+00:00\n- check time: 2026-03-30T06:25:00+00:00\n- minutes from opening to the check: twenty\n- minutes from opening to the acknowledgement: fifteen\nCritical services: checkout, search\nMaintenance window: 2026-03-30T05:20:00+00:00 to 2026-03-30T08:40:00+00:00",
  "question": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 500 or more users, partial if 50 or more but fewer than 500, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV1, SEV3; partial SEV3, SEV1, SEV4; minimal SEV3, SEV2, SEV4.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 20 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed with wide impact: SEV2 or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer.\n\nNew on-call here, so what severity does the card's rule set give incident INC-3719 at the check time?",
  "options": [
   "SEV1",
   "SEV2",
   "SEV3",
   "SEV4"
  ]
 },
 {
  "qid": "q6ab0295207",
  "kind": "yes/no",
  "text": "Hello Valerian cell! Passing this to you from Thora Farrimond, details attached. Thank you!\n\nIncident INC-7948 on chat:\n- opened: 10 February 2026, 14:15 (UTC-03:00)\n- users affected: 1,999 users\n- urgency reported: outage\n- customer data exposed: no\n- acknowledged: 10 February 2026, 14:17 (UTC-03:00)\n- check time: 10 February 2026, 15:42 (UTC-03:00)\n- minutes from opening to the check: 87\n- minutes from opening to the acknowledgement: 2\nCritical services: checkout, email\nMaintenance window: 10 February 2026, 13:15 (UTC-03:00) to 10 February 2026, 14:43 (UTC-03:00)",
  "question": "Concerning incident INC-7948, does it fail to reach SEV3 as of the check time?",
  "definitions": "SEV1 is the most severe, SEV4 the least.\nImpact: wide if 2,000 or more users, partial if 200 or more but fewer than 2,000, otherwise minimal.\nBase severity (outage, degraded, cosmetic): wide SEV2, SEV3, SEV1; partial SEV3, SEV4, SEV2; minimal SEV4, SEV4, SEV3.\nThen, in order:\nIf opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.\nIf the service is on the critical list and less severe than SEV2: SEV2.\nA step falls due at each full 30 minutes after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\nIf customer data was exposed: one level more severe.\nAn incident reaches a level when its severity is that level or more severe.\nThe incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer."
 }
]
