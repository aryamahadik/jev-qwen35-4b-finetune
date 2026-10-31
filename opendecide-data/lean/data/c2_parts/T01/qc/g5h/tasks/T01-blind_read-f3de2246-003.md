# G5-H blind read T01-blind_read-f3de2246-003 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g5h/answers/T01-blind_read-f3de2246-003.json

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
  "qid": "qb6841d0211",
  "kind": "yes/no",
  "text": "Malik Osei: forwarding file NTC-5443 about the reply timing question to the case team, with respect.\ncase team: thank you kindly for passing it along.\n\nNotice NTC-5443 to Malik Osei:\n- response due date: April 7, 2026\n- office cutoff on the due date: 7 April 2026, 17:43 (UTC+09:00)\n- response sent: 7 April 2026, 01:31 (UTC+00:00) [same instant in office time: 7 April 2026, 10:31 (UTC+09:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Malik Osei received on time under the receipt rule?"
 },
 {
  "qid": "q685a45c1f8",
  "kind": "choice",
  "text": "Desk memo: Ines Duarte has sent in file LED-9100 about the branch cash review for the help desk. Move on it at speed, there is a lot in the queue.\n\nCash ledger LED-9100, teller Ines Duarte:\n- 28 December 2027: withdrawal of $3,000\n- 28 December 2027: deposit of $4,178\n- 30 December 2027: deposit of $1,807\nDay under review: 28 December 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any sum more than $3,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals in ledger LED-9100 for 28 December 2027 call for a cash report under the cash rule?",
  "options": [
   "Both totals",
   "Only the deposit total",
   "Only the withdrawal total",
   "Neither total"
  ]
 },
 {
  "qid": "q585b219471",
  "kind": "yes/no",
  "text": "Desk memo: Please be advised that Hana Sato has sent file CASE-7889 concerning the complaint filing to the desk.\nKindly route it to the review team at your convenience. Thank you for your attention.\n\nCase CASE-7889, party Hana Sato:\n- incident date: 13 May 2026\n- discovery date: 6 May 2026\n- complaint filed on: 24 Jun 2026\n- days from the incident date to the filing: 42 days\n- days from the discovery date to the filing: 49 days",
  "question": "Filing rule: the complaint must be filed within 60 days measured from the later of the dates below: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the complaint in case CASE-7889 filed in time, on or before the final day?"
 },
 {
  "qid": "q457513c5c6",
  "kind": "yes/no",
  "text": "clerk: Duty line here, kindly speak freely.\nAna Ruiz: Thank you, passing on file POL-9783 about the insurance claim to the duty clerk.\nclerk: Certainly, that is in good hands.\n\nPolicy POL-9783, holder Ana Ruiz:\n- policy start date: 26 Jul 2026\n- theft cover: part of the base policy\n- theft loss on: 31 Jul 2026\n- days from the policy start date to the loss: 5 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 15 days that begins on the next day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 15 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the theft loss under policy POL-9783 within the waiting period?"
 },
 {
  "qid": "qab8b72ac19",
  "kind": "choice",
  "text": "Lucas Brenner: sending file NTC-8606 about the notice response, with thanks.\nintake team: thank you, this is received.\nintake team: appreciated.\n\nNotice NTC-8606 to Lucas Brenner:\n- response due date: Saturday, 19 September 2026\n- office cutoff on the due date: 2026-09-19 13:12:00 +0530\n- response sent: 2026-09-17 03:37:00 -0400 [same instant in office time: 2026-09-17 13:07:00 +0530]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn which date does the office count the response from Lucas Brenner as received under the receipt rule?",
  "options": [
   "September 17, 2026",
   "September 16, 2026"
  ]
 },
 {
  "qid": "qe69e20d306",
  "kind": "yes/no",
  "text": "Hana Sato: file PO-1265 about the purchase request is here\nclerk: got it, that is a normal intake\ndesk: good, sending it through to the records clerk\n\nPurchase log PO-1265, kept by Hana Sato, vendor Ostrava Parts:\n- earlier purchase on November 22, 2027: $1,774\n- earlier purchase on December 29, 2027: $11,760\n- new request on January 24, 2028: $3,239\nWindow checked: December 26, 2027 to January 24, 2028, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is equal to or more than $15,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, does the purchase rule require written quotes for the request from Hana Sato?"
 },
 {
  "qid": "q7d5e04495a",
  "kind": "yes/no",
  "text": "sent_by: Jonas Feld\nfile: STAY-5408\nsubject: the visa stay count\nteam: intake team\n\nStay record STAY-5408 for Jonas Feld:\n- entry day Sunday, 5 December 2027, exit day Wednesday, 9 February 2028 (whole stay: 67 days)\nReference date: Saturday, 8 April 2028\nWindow checked: Saturday, 11 December 2027 to Saturday, 8 April 2028, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days within every moving 120-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Jonas Feld over the stay limit, with more days present inside the window that ends on the reference date in file STAY-5408, under the stay rule?"
 },
 {
  "qid": "q8c3e3df4ce",
  "kind": "choice",
  "text": "Malik Osei: Sending file NTC-6070 about the notice response across in a hurry.\nadmin: On it, passing it along.\n\nNotice NTC-6070 to Malik Osei:\n- notice date: 27 September 2025\n- sent by: post\n- 14 days after the notice date, before any postal add-on or closure: 11 October 2025\nOffice closures: 11 October 2025; 12 October 2025; 15 October 2025.",
  "question": "Response rule: a response is due 14 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 5 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, on which date is the response to notice NTC-6070 due under the response rule?",
  "options": [
   "16 October 2025",
   "13 October 2025",
   "14 October 2025"
  ]
 },
 {
  "qid": "q5c3a8ec667",
  "kind": "choice",
  "text": "Subject: file handover\nDear duty clerk,\nThe file PO-4450 has come from Nadia Kowal about the purchase request, for your desk.\nRegards,\n\nPurchase log PO-4450, kept by Nadia Kowal, vendor Mirefield Print:\n- earlier purchase on 14 Dec 2025: $1,310.00\n- earlier purchase on 31 Dec 2025: $656.00\n- earlier purchase on 14 Jan 2026: $502.00\n- new request on 4 Feb 2026: $2,780.00\nWindow checked: 7 Dec 2025 to 4 Feb 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any figure at or above $5,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat total does the purchase rule compare with its threshold when the new request in log PO-4450 is counted in?",
  "options": [
   "$8,028.00",
   "$5,248.00"
  ]
 },
 {
  "qid": "qc9b59c5bcc",
  "kind": "yes/no",
  "text": "title | formal request\nrequester | Lucas Brenner\nfile | POL-8893\nWe kindly pass the cover question along to the records clerk for your review.\n\nPolicy POL-8893, holder Lucas Brenner:\n- policy start date: 23 November 2026\n- storm damage cover: added by a rider effective 26 April 2027\n- storm damage loss on: 17 May 2027\n- days from the policy start date to the loss: 175 days\n- days from the rider effective date to the loss: 21 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days that starts on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, did the loss on policy POL-8893 happen during the waiting period?"
 },
 {
  "qid": "qeb6b5f13fe",
  "kind": "choice",
  "text": "[records] file=LED-3605 from Iris Vance regarding the branch cash review\n[records] message_for=the records clerk, with_warm_respect\n\nCash ledger LED-3605, teller Iris Vance:\n- 9 Apr 2028: deposit of 8,395.00 USD\n- 10 Apr 2028: withdrawal of 7,617.00 USD\n- 11 Apr 2028: withdrawal of 7,108.00 USD\n- 11 Apr 2028: deposit of 1,051.00 USD\n- 11 Apr 2028: withdrawal of 1,036.00 USD\n- 11 Apr 2028: deposit of 4,859.00 USD\nDay under review: 11 Apr 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is 15,000.00 USD as a floor, greater than that counts, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nFor 11 Apr 2028, which of the day's totals, under the cash rule, call for a cash report?",
  "options": [
   "Neither total",
   "Both totals",
   "Only the deposit total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q06210cbf9c",
  "kind": "yes/no",
  "text": "Subject: quick pass-along\nHi service desk,\nQuick note: Bruno Lacerda sends file PO-6507 about the purchase request, so please grab it at your earliest convenience.\nBest,\n\nPurchase log PO-6507, kept by Bruno Lacerda, vendor Brightwell Supply:\n- earlier purchase on Saturday, January 10, 2026: $2,484\n- earlier purchase on Tuesday, January 20, 2026: $1,810\n- earlier purchase on Sunday, January 25, 2026: $227\n- new request on Monday, February 9, 2026: $2,964\nWindow checked: Sunday, January 11, 2026 to Monday, February 9, 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is greater than $5,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request from Bruno Lacerda need written quotes under the purchase rule?"
 },
 {
  "qid": "qf2e6e7768c",
  "kind": "yes/no",
  "text": "Ana Ruiz: file CASE-6831 about the complaint filing is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.\n\nCase CASE-6831, party Ana Ruiz:\n- incident date: Tuesday, 14 September 2027\n- discovery date: Sunday, 29 August 2027\n- complaint filed on: Monday, 20 September 2027\n- days from the incident date to the filing: 6 days\n- days from the discovery date to the filing: 22 days",
  "question": "Filing rule: the complaint must be filed within 14 days from whichever is later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 14 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the complaint filed on or before the final day of the filing period?"
 },
 {
  "qid": "q1a1993e4f0",
  "kind": "yes/no",
  "text": "Hana Sato: Hiya! Sending CASE-6275 about the claim deadline question, all good here.\nservice desk: Lovely, thanks for the heads up!\n\nCase CASE-6275, party Hana Sato:\n- inspection date: Thursday, October 8, 2026\n- report date: Thursday, September 24, 2026\n- objection filed on: Thursday, October 29, 2026\n- days from the inspection date to the filing: 21 days\n- days from the report date to the filing: 35 days",
  "question": "Filing rule: the objection must be filed within 28 days past the later of the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the objection in case CASE-6275 filed late, after the deadline?"
 },
 {
  "qid": "qb3abf51ea1",
  "kind": "yes/no",
  "text": "Desk memo: Aiko Brandt sends file CASE-1133 about the complaint filing to the records clerk. The clerk gets a copy for the shelf in the usual way. Please keep this simple.\n\nCase CASE-1133, party Aiko Brandt:\n- incident date: 22 Feb 2027\n- discovery date: 8 Feb 2027\n- complaint filed on: 14 May 2027\n- days from the incident date to the filing: 81 days\n- days from the discovery date to the filing: 95 days",
  "question": "Filing rule: the complaint must be filed within 60 days from whichever is later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the complaint filed too late, after the final day of the filing period?"
 },
 {
  "qid": "q61134bffe8",
  "kind": "yes/no",
  "text": "Memo for the front desk: Kofi Mensah sends file CASE-6324 about the appeal deadline. Grab it at your convenience, the queue is busy on this end.\n\nCase CASE-6324, party Kofi Mensah:\n- decision date: July 28, 2027\n- delivery date: August 18, 2027\n- appeal filed on: October 3, 2027\n- days from the decision date to the filing: 67 days\n- days from the delivery date to the filing: 46 days",
  "question": "Filing rule: the appeal must be filed within 45 days from whichever is later of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the appeal filed in time, on or before the final day of the filing period?"
 },
 {
  "qid": "qaa490e78c8",
  "kind": "yes/no",
  "text": "Tomas Lindqvist: Quick word, here is file POL-2024 about the insurance claim, I am swamped.\nservice: Thanks, I see it.\ndesk: Great, shared with the team.\n\nPolicy POL-2024, holder Tomas Lindqvist:\n- policy start date: Monday, 5 July 2027\n- glass breakage cover: part of the base policy\n- glass breakage loss on: Saturday, 7 August 2027\n- days from the policy start date to the loss: 33 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days whose clock starts running on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, is the glass breakage loss for Tomas Lindqvist covered under the cover rule?"
 },
 {
  "qid": "qe6b030673c",
  "kind": "yes/no",
  "text": "team: case team\nsent_by: Priya Raman\nfile: STAY-9369\nsubject: the residence day count\nnote: standard_handling_as_usual\n\nStay record STAY-9369 for Priya Raman:\n- entry day 14 Jun 2027, exit day 16 Jun 2027 (whole stay: 3 days)\n- entry day 1 Jul 2027, exit day 28 Jul 2027 (whole stay: 28 days)\n- entry day 20 Aug 2027, exit day 2 Sep 2027 (whole stay: 14 days)\nReference date: 22 Sep 2027\nWindow checked: 26 May 2027 to 22 Sep 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 60 days in each 120-day window that moves forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, do the days present for Priya Raman inside the checked window ending on the reference date exceed the stay limit?"
 },
 {
  "qid": "qf68306b97e",
  "kind": "yes/no",
  "text": "Dear front desk,\nTomas Lindqvist is sending file CASE-2258 about the appeal deadline. The file is attached here for your records. I appreciate the help with it.\nKind regards,\n\nCase CASE-2258, party Tomas Lindqvist:\n- decision date: 12 Aug 2027\n- delivery date: 7 Aug 2027\n- appeal filed on: 31 Aug 2027\n- days from the decision date to the filing: 19 days\n- days from the delivery date to the filing: 24 days",
  "question": "Filing rule: the appeal must be filed within 10 days past the later of the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 10 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Tomas Lindqvist, under the filing rule, fail to file the appeal in time?"
 },
 {
  "qid": "q5a2c4c0d69",
  "kind": "choice",
  "text": "file: POL-6835\nsent_by: Nadia Kowal\nsubject: the cover question\nto: duty clerk\n\nPolicy POL-6835, holder Nadia Kowal:\n- policy start date: November 20, 2027\n- storm damage cover: added by a rider effective December 28, 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 48 days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 48 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which a loss of this kind would count as covered for policy POL-6835 under the cover rule?",
  "options": [
   "March 4, 2028",
   "February 16, 2028",
   "February 15, 2028",
   "February 17, 2028"
  ]
 },
 {
  "qid": "q21a8b19d94",
  "kind": "yes/no",
  "text": "clerk: routine drop coming in\nYara Haddad: file POL-1046 about the insurance claim is on its way\ndesk: understood, passing it to the intake team\n\nPolicy POL-1046, holder Yara Haddad:\n- policy start date: 2 February 2026\n- power surge damage cover: added by a rider effective 30 June 2026\n- power surge damage loss on: 19 July 2026\n- days from the policy start date to the loss: 167 days\n- days from the rider effective date to the loss: 19 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 60 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 60 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the cover rule does not pay for the power surge damage loss on policy POL-1046?"
 },
 {
  "qid": "qf86feb368a",
  "kind": "choice",
  "text": "Nadia Kowal: Kindly passing along file NTC-8992 about the reply deadline to the desk.\ndesk: Thanks very kindly for this.\n\nNotice NTC-8992 to Nadia Kowal:\n- notice date: September 22, 2027\n- sent by: email\n- 20 days after the notice date, before any postal add-on or closure: October 12, 2027\nOffice closures: October 12, 2027; October 13, 2027.",
  "question": "Response rule: a response is due 20 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 5 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, on what date is the response from Nadia Kowal due under the response rule?",
  "options": [
   "October 10, 2027",
   "October 11, 2027",
   "October 14, 2027"
  ]
 },
 {
  "qid": "q2d2624c971",
  "kind": "choice",
  "text": "Hi admin team, Aiko Brandt here with file LED-1198 about the cash ledger check. Thanks so much for helping keep everything tidy. It is a pleasure to share it with you all.\n\nCash ledger LED-1198, teller Aiko Brandt:\n- 2028-02-04: withdrawal of 3,627.00 USD\n- 2028-02-04: withdrawal of 6,242.00 USD\n- 2028-02-06: deposit of 3,640.00 USD\n- 2028-02-06: withdrawal of 3,952.00 USD\n- 2028-02-06: deposit of 2,489.00 USD\n- 2028-02-06: withdrawal of 11,049.00 USD\nDay under review: 2028-02-06",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is strictly more than 15,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals in ledger LED-1198 for 2028-02-06 call for a cash report under the cash rule?",
  "options": [
   "Only the withdrawal total",
   "Both totals",
   "Neither total",
   "Only the deposit total"
  ]
 },
 {
  "qid": "qb7558382ae",
  "kind": "yes/no",
  "text": "{\"subject\": \"the response deadline\", \"sent_by\": \"Eva Marsh\", \"file\": \"NTC-2935\", \"channel\": \"intake\", \"team\": \"desk\"}\n\nNotice NTC-2935 to Eva Marsh:\n- response due date: 11 April 2027\n- office cutoff on the due date: 2027-04-11 12:38:00 -0400\n- response sent: 2027-04-11 16:39:00 +0000 [same instant in office time: 2027-04-11 12:39:00 -0400]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Eva Marsh on time under the receipt rule?"
 },
 {
  "qid": "q2d00f0d90a",
  "kind": "choice",
  "text": "[records] file=PO-1520 from Ravi Anand regarding the supplier order\n[records] message_for=the records clerk, with_warm_respect\n\nPurchase log PO-1520, kept by Ravi Anand, vendor Quillon Labs:\n- earlier purchase on 10 Jan 2028: $120.00\n- earlier purchase on 23 Jan 2028: $324.00\n- earlier purchase on 14 Feb 2028: $374.00\n- new request on 3 Apr 2028: $1,219.00\nWindow checked: 5 Jan 2028 to 3 Apr 2028, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is $3,000.00 bar, cleared only by more than that, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what total does the purchase rule test against its threshold for log PO-1520, counting the new request too?",
  "options": [
   "$2,037.00",
   "$3,256.00"
  ]
 },
 {
  "qid": "q610dbd1563",
  "kind": "yes/no",
  "text": "Desk memo: Please be advised that Felix Ortega has sent file POL-2206 concerning the cover question to the desk.\nKindly route it to the review team at your convenience. Thank you for your attention.\n\nPolicy POL-2206, holder Felix Ortega:\n- policy start date: Thursday, December 17, 2026\n- storm damage cover: added by a rider effective Thursday, July 8, 2027\n- storm damage loss on: Thursday, July 22, 2027\n- days from the policy start date to the loss: 217 days\n- days from the rider effective date to the loss: 14 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 15 days with the start date itself left out, beginning the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 15 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is it true that the storm damage loss in policy POL-2206 is not covered?"
 },
 {
  "qid": "q028ed65742",
  "kind": "yes/no",
  "text": "clerk: oh hey, what came in\nRavi Anand: got file STAY-8687 about the visa stay count here, nice and easy\ndesk: lovely, thanks, we are on it\n\nStay record STAY-8687 for Ravi Anand:\n- entry day Monday, June 7, 2027, exit day Monday, June 7, 2027 (whole stay: one day)\n- entry day Friday, July 16, 2027, exit day Saturday, September 11, 2027 (whole stay: 58 days)\n- entry day Sunday, October 3, 2027, exit day Tuesday, October 5, 2027 (whole stay: three days)\nReference date: Wednesday, October 27, 2027\nWindow checked: Wednesday, June 30, 2027 to Wednesday, October 27, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 60 days inside every moving 120-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, do the days present for Ravi Anand inside the checked window ending on the reference date exceed the stay limit?"
 },
 {
  "qid": "q797aad12d0",
  "kind": "yes/no",
  "text": "subject: the complaint filing\nsent_by: Clara Weiss\nfile: CASE-6356\nchannel: intake\nnote: happy_to_help\n\nCase CASE-6356, party Clara Weiss:\n- purchase date: 10 August 2027\n- handover date: 24 August 2027\n- refund request filed on: 11 September 2027\n- days from the purchase date to the filing: 32 days\n- days from the handover date to the filing: 18 days",
  "question": "Filing rule: the refund request must be filed inside 17 days that elapses after whichever of the dates below is later: the purchase date and the handover date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 17 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the refund request filed in time, on or before the final day of the filing period?"
 },
 {
  "qid": "qf8ea791b8b",
  "kind": "yes/no",
  "text": "file: POL-7555\nsent_by: Freya Holm\nsubject: the loss claim\nteam: service desk\nnote: busy_queue\n\nPolicy POL-7555, holder Freya Holm:\n- policy start date: 11 March 2027\n- glass breakage cover: added by a rider effective 12 June 2027\n- glass breakage loss on: 23 July 2027\n- days from the policy start date to the loss: 134 days\n- days from the rider effective date to the loss: 41 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 60 days with the start date itself left out, beginning the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 60 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the glass breakage loss on policy POL-7555 covered under the cover rule?"
 },
 {
  "qid": "qa0a9c7c729",
  "kind": "choice",
  "text": "Desk memo: Malik Osei is sending file NTC-5661 about the response deadline to the admin team. Pick it up fast, the work is waiting.\n\nNotice NTC-5661 to Malik Osei:\n- notice date: Wednesday, 10 May 2028\n- sent by: hand delivery\n- 20 days after the notice date, before any postal add-on or closure: Tuesday, 30 May 2028\nOffice closures: Tuesday, 30 May 2028; Sunday, 4 June 2028.",
  "question": "Response rule: a response is due 20 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 5 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, on which date is the response to notice NTC-5661 due under the response rule?",
  "options": [
   "Sunday, 28 May 2028",
   "Wednesday, 31 May 2028",
   "Monday, 29 May 2028"
  ]
 },
 {
  "qid": "q3dc8365a94",
  "kind": "yes/no",
  "text": "[intake] file=CASE-2235 sender=Kofi Mensah regarding the claim deadline question\n[note] kindly_forwarded_to=duty_clerk\n\nCase CASE-2235, party Kofi Mensah:\n- invoice date: Tuesday, February 2, 2027\n- goods received date: Saturday, January 23, 2027\n- claim filed on: Friday, March 19, 2027\n- days from the invoice date to the filing: 45 days\n- days from the goods received date to the filing: 55 days",
  "question": "Filing rule: the claim must be filed within 45 days starting from the later of the dates listed below: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Kofi Mensah fail to file the claim in case CASE-2235 by the deadline?"
 },
 {
  "qid": "qb6c3796525",
  "kind": "choice",
  "text": "file: CASE-4762\nsent_by: Sara Ilves\nsubject: the appeal deadline\nteam: service desk\nnote: busy_queue\n\nCase CASE-4762, party Sara Ilves:\n- billing date: 21 Nov 2026\n- statement date: 28 Nov 2026",
  "question": "Filing rule: the dispute must be filed within 56 days after the later date out of these dates: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 56 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, by which final day must the dispute be filed to still count as in time?",
  "options": [
   "16 Jan 2027",
   "22 Jan 2027",
   "23 Jan 2027"
  ]
 },
 {
  "qid": "q2d92b3be4b",
  "kind": "yes/no",
  "text": "Paolo Greco: Kind greetings, file POL-5396 about the insurance claim is sent in for your review\nclerk: Thank you, we value this\ndesk: kindly passed on to the records clerk\n\nPolicy POL-5396, holder Paolo Greco:\n- policy start date: 2027-12-08\n- burst pipe damage cover: part of the base policy\n- burst pipe damage loss on: 2027-12-15\n- days from the policy start date to the loss: 7 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days whose clock starts running on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the burst pipe damage loss on policy POL-5396 covered under the cover rule?"
 },
 {
  "qid": "q56e63e621c",
  "kind": "yes/no",
  "text": "Subject: Little catch-up on the notice response\n\nHey review team,\n\nDropping file NTC-5677 off from Dana Okafor, hope it lands nicely with you. Enjoy the rest of your stretch.\n\nCheers,\n\nNotice NTC-5677 to Dana Okafor:\n- response due date: 11 August 2027\n- office cutoff on the due date: 2027-08-11 20:15:00 +0300\n- response sent: 2027-08-11 14:10:00 -0300 [same instant in office time: 2027-08-11 20:10:00 +0300]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Dana Okafor to notice NTC-5677 on time under the receipt rule?"
 },
 {
  "qid": "qe9a8ce14e9",
  "kind": "yes/no",
  "text": "Subject: file handover\nDear duty clerk,\nThe file CASE-6443 has come from Sara Ilves about the appeal deadline, for your desk.\nRegards,\n\nCase CASE-6443, party Sara Ilves:\n- billing date: 21 February 2026\n- statement date: 7 February 2026\n- dispute filed on: 22 April 2026\n- days from the billing date to the filing: 60 days\n- days from the statement date to the filing: 74 days",
  "question": "Filing rule: the dispute must be filed within 60 days after the later date out of these dates: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Sara Ilves file the dispute in case CASE-6443 in time under the filing rule?"
 },
 {
  "qid": "q5c98b76bc6",
  "kind": "yes/no",
  "text": "A happy note from Hana Sato to the service desk. File NTC-2033 is about the response deadline, sent with a smile. Enjoy the rest of your work.\n\nNotice NTC-2033 to Hana Sato:\n- response due date: Sunday, December 26, 2027\n- office cutoff on the due date: 26 December 2027, 21:42 (UTC-05:00)\n- response sent: 27 December 2027, 01:33 (UTC-04:00) [same instant in office time: 27 December 2027, 00:33 (UTC-05:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Hana Sato to the notice late under the receipt rule?"
 },
 {
  "qid": "q335ddb25ce",
  "kind": "yes/no",
  "text": "Jonas Feld: file NTC-3877 about the response deadline is here.\nintake team: received, thanks.\nintake team: that is everything for this file.\n\nNotice NTC-3877 to Jonas Feld:\n- response due date: Sunday, June 4, 2028\n- office cutoff on the due date: 2028-06-04 18:53:00 +0100\n- response sent: 2028-06-04 13:48:00 -0400 [same instant in office time: 2028-06-04 18:48:00 +0100]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the response from Jonas Feld to notice NTC-3877 under the receipt rule was not on time?"
 },
 {
  "qid": "q1f5b7d298b",
  "kind": "choice",
  "text": "[log] from=Aiko Brandt ref_file=POL-8414 to=records_clerk\n[log] about=the insurance claim routine_transfer\n\nPolicy POL-8414, holder Aiko Brandt:\n- policy start date: January 7, 2027\n- power surge damage cover: added by a rider effective July 15, 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of seven days that picks up on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is seven days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on what earliest date would the power surge damage loss be covered?",
  "options": [
   "July 23, 2027",
   "January 15, 2027",
   "July 22, 2027"
  ]
 },
 {
  "qid": "q481297df43",
  "kind": "choice",
  "text": "sent_by: Mira Castell\nfile: CASE-4181\nsubject: the claim deadline question\nteam: case team\nnote: with thanks\n\nCase CASE-4181, party Mira Castell:\n- invoice date: December 22, 2025\n- goods received date: December 29, 2025",
  "question": "Filing rule: the claim must be filed within 58 days reckoned after the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 58 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the latest date, under the filing rule, on which the claim for case CASE-4181 can be filed in time?",
  "options": [
   "February 26, 2026",
   "February 25, 2026",
   "March 19, 2026"
  ]
 },
 {
  "qid": "qef8cd584c8",
  "kind": "yes/no",
  "text": "file: NTC-3451\nsent_by: Freya Holm\nsubject: the reply timing question\nteam: service desk\nnote: a friendly hello\n\nNotice NTC-3451 to Freya Holm:\n- response due date: September 3, 2028\n- office cutoff on the due date: 2028-09-03T16:56:00Z\n- response sent: 3 September 2028, 10:01 (UTC-07:00) [same instant in office time: 2028-09-03T17:01:00Z]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Freya Holm to notice NTC-3451 on time under the receipt rule?"
 },
 {
  "qid": "q13ac2d1619",
  "kind": "choice",
  "text": "Lucas Brenner: with respect, my note sends over LED-9218 about the cash ledger check\nclerk: thank you, it is in good hands\n\nCash ledger LED-9218, teller Lucas Brenner:\n- January 20, 2027: withdrawal of $704.00\n- January 22, 2027: withdrawal of $1,372.00\n- January 22, 2027: withdrawal of $1,628.00\n- January 22, 2027: deposit of $408.00\n- January 22, 2027: deposit of $205.00\n- January 24, 2027: withdrawal of $2,124.00\nDay under review: January 22, 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any total greater than $3,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, which of the day's totals for January 22, 2027 call for a cash report?",
  "options": [
   "Only the deposit total",
   "Neither total",
   "Only the withdrawal total",
   "Both totals"
  ]
 },
 {
  "qid": "qa6b9814b4c",
  "kind": "yes/no",
  "text": "Internal memo: This note is about the claim deadline question. Lena Whitcombe submits file CASE-1048 to the front desk. Thanks for reading along, and cheers.\n\nCase CASE-1048, party Lena Whitcombe:\n- invoice date: May 14, 2026\n- goods received date: May 7, 2026\n- claim filed on: June 13, 2026\n- days from the invoice date to the filing: 30 days\n- days from the goods received date to the filing: 37 days",
  "question": "Filing rule: the claim must be filed within 30 days from whichever is later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the claim filed on or before the final day of the filing period?"
 },
 {
  "qid": "q480277d260",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nHana Sato is sending file NTC-2583 about the notice response, with the main points at the top. Quick note, I am buried under other work.\nBest,\n\nNotice NTC-2583 to Hana Sato:\n- response due date: 14 April 2026\n- office cutoff on the due date: 2026-04-14 18:25:00 +0300\n- response sent: 2026-04-14 16:30:00 +0100 [same instant in office time: 2026-04-14 18:30:00 +0300]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Hana Sato to notice NTC-2583 on time under the receipt rule?"
 },
 {
  "qid": "q3b3c686742",
  "kind": "yes/no",
  "text": "file: NTC-6546\nsent_by: Theo Kalnins\nsubject: the reply timing question\nteam: case team\nnote: with respectful thanks\n\nNotice NTC-6546 to Theo Kalnins:\n- response due date: Sunday, October 31, 2027\n- office cutoff on the due date: 2027-10-31 13:35:00 +0900\n- response sent: 2027-11-01 07:48:00 +0200 [same instant in office time: 2027-11-01 14:48:00 +0900]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Theo Kalnins on time under the receipt rule?"
 },
 {
  "qid": "qf76e6e6e5e",
  "kind": "yes/no",
  "text": "file_ref=POL-2136 topic=the insurance claim\n[mailroom] from=Clara Weiss to=desk\n\nPolicy POL-2136, holder Clara Weiss:\n- policy start date: 6 September 2027\n- fire damage cover: part of the base policy\n- fire damage loss on: 7 September 2027\n- days from the policy start date to the loss: 1 day",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days that opens on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is this fire damage loss covered by the cover rule?"
 },
 {
  "qid": "q7ec18e67ff",
  "kind": "yes/no",
  "text": "Omar Saleh: Kindly see file CASE-7095 about the complaint filing below, thank you.\nclerk: Thank you, that is noted and it goes to the case team.\n\nCase CASE-7095, party Omar Saleh:\n- incident date: Monday, May 22, 2028\n- discovery date: Monday, June 12, 2028\n- complaint filed on: Saturday, July 22, 2028\n- days from the incident date to the filing: 61 days\n- days from the discovery date to the filing: 40 days",
  "question": "Filing rule: the complaint must be filed inside 28 days that elapses after whichever of the dates below is later: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the complaint filed too late, after the final day of the filing period?"
 },
 {
  "qid": "q6ae73afcb9",
  "kind": "choice",
  "text": "clerk: heads up, a new item is landing\nMaya Lindgren: file CASE-4324 about the complaint filing is going to the help desk\ndesk: understood, routing it straight away\n\nCase CASE-4324, party Maya Lindgren:\n- purchase date: 2026-10-16\n- handover date: 2026-10-02",
  "question": "Filing rule: the refund request must be filed within 30 days starting from the later of the dates listed below: the purchase date and the handover date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the final day still in time for filing the refund request in case CASE-4324?",
  "options": [
   "2026-11-27",
   "2026-11-15",
   "2026-11-16",
   "2026-11-17"
  ]
 },
 {
  "qid": "q68fa9354f8",
  "kind": "choice",
  "text": "file: LED-2010\nsent_by: Nadia Kowal\nsubject: the branch cash review\nteam: service desk\nnote: a friendly hello\n\nCash ledger LED-2010, teller Nadia Kowal:\n- Thursday, 13 July 2028: deposit of $20,267\n- Thursday, 13 July 2028: deposit of $2,140\n- Saturday, 15 July 2028: deposit of $10,657\nDay under review: Thursday, 13 July 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is equal to $15,000 or more, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, which of the day's totals in ledger LED-2010, if any, call for a cash report under the cash rule?",
  "options": [
   "Only the deposit total",
   "Both totals",
   "Only the withdrawal total",
   "Neither total"
  ]
 },
 {
  "qid": "qb2a469f2ec",
  "kind": "yes/no",
  "text": "Subject: formal intake\nDear records clerk,\nEva Marsh sent in file STAY-5826 about the visa stay count for your attention. It is passed along with respect.\nKind regards,\n\nStay record STAY-5826 for Eva Marsh:\n- entry day Monday, June 9, 2025, exit day Tuesday, June 17, 2025 (whole stay: nine days)\n- entry day Monday, June 30, 2025, exit day Monday, June 30, 2025 (whole stay: one day)\n- entry day Wednesday, July 30, 2025, exit day Wednesday, August 27, 2025 (whole stay: 29 days)\nReference date: Saturday, September 27, 2025\nWindow checked: Monday, June 30, 2025 to Saturday, September 27, 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 30 days inside every moving 90-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Eva Marsh, under the stay rule, over the stay limit for the window ending on Saturday, September 27, 2025?"
 },
 {
  "qid": "q108f3b1567",
  "kind": "choice",
  "text": "Hana Sato sends file NTC-4740 about the response deadline to the desk. The file is set out in full with the usual headings. Thank you for your attention to this matter.\n\nNotice NTC-4740 to Hana Sato:\n- notice date: Monday, October 6, 2025\n- sent by: post\n- fourteen days after the notice date, before any postal add-on or closure: Monday, October 20, 2025\nOffice closures: Saturday, October 25, 2025; Sunday, October 26, 2025.",
  "question": "Response rule: a response is due fourteen days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add five days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, on what date is the response from Hana Sato due under the response rule?",
  "options": [
   "Monday, October 27, 2025",
   "Friday, October 24, 2025"
  ]
 }
]
