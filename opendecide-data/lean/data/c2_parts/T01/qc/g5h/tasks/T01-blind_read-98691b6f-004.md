# G5-H blind read (all free-form rows) T01-blind_read-98691b6f-004 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g5h/answers/T01-blind_read-98691b6f-004.json

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
  "qid": "q63e78e9c43",
  "kind": "yes/no",
  "text": "Theo Kalnins: file POL-9777 about the loss claim is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.\n\nPolicy POL-9777, holder Theo Kalnins:\n- policy start date: May 19, 2027\n- fire damage cover: added by a rider effective July 6, 2027\n- fire damage loss on: August 26, 2027\n- days from the policy start date to the loss: 99 days\n- days from the rider effective date to the loss: 51 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 10 days that begins on the next day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 10 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid this fire damage loss, under the cover rule, happen within the waiting period?"
 },
 {
  "qid": "qcb1dd7b326",
  "kind": "choice",
  "text": "Omar Saleh sends file CASE-7142 about the appeal deadline to the desk. The file is set out in full with the usual headings. Thank you for your attention to this matter.\n\nCase CASE-7142, party Omar Saleh:\n- billing date: Tuesday, 25 May 2027\n- statement date: Saturday, 15 May 2027",
  "question": "Filing rule: the dispute must be filed within 60 days measured beyond the later of these dates: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the final day on which Omar Saleh can still file the dispute in time for case CASE-7142?",
  "options": [
   "Wednesday, 14 July 2027",
   "Saturday, 24 July 2027",
   "Thursday, 22 July 2027"
  ]
 },
 {
  "qid": "q601c411044",
  "kind": "yes/no",
  "text": "File: CASE-2566\nSubject: the claim deadline question\nFrom: Lucas Brenner\nQuick send to the records clerk. The desk is swamped, sorry for the speed.\n\nCase CASE-2566, party Lucas Brenner:\n- invoice date: November 16, 2025\n- goods received date: November 14, 2025\n- claim filed on: February 15, 2026\n- days from the invoice date to the filing: 91 days\n- days from the goods received date to the filing: 93 days",
  "question": "Filing rule: the claim must be filed inside 90 days beginning at the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Lucas Brenner, under the filing rule, file the claim on or before the final day?"
 },
 {
  "qid": "q623c6abf3c",
  "kind": "yes/no",
  "text": "Hana Sato: Sending STAY-6864 about the visa stay count, short and sharp.\nservice desk: Received.\n\nStay record STAY-6864 for Hana Sato:\n- entry day 2027-05-10, exit day 2027-06-18 (whole stay: 40 days)\n- entry day 2027-07-05, exit day 2027-07-09 (whole stay: five days)\n- entry day 2027-07-23, exit day 2027-08-15 (whole stay: 24 days)\nReference date: 2027-08-26\nWindow checked: 2027-04-29 to 2027-08-26, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days inside any moving 120-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is Hana Sato over the stay limit in record STAY-6864 when counting just the checked window that ends on the reference date?"
 },
 {
  "qid": "q5ca00ed710",
  "kind": "choice",
  "text": "From: Ines Duarte\nFile: CASE-6317\nSent to: review team\nThe file about the claim deadline question is shared as usual.\n\nCase CASE-6317, party Ines Duarte:\n- invoice date: 8 July 2026\n- goods received date: 11 July 2026",
  "question": "Filing rule: the claim must be filed inside 45 days extending past the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, by which final day must the claim be filed to still count as in time?",
  "options": [
   "24 August 2026",
   "22 August 2026",
   "25 August 2026"
  ]
 },
 {
  "qid": "q7e15ddac4c",
  "kind": "choice",
  "text": "Owen Pryce: Quick word, here is file POL-9568 about the insurance claim, I am swamped.\nservice: Thanks, I see it.\ndesk: Great, shared with the team.\n\nPolicy POL-9568, holder Owen Pryce:\n- policy start date: 11 March 2027\n- theft cover: added by a rider effective 29 April 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days that starts on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the earliest date on which the theft loss for Owen Pryce would be covered?",
  "options": [
   "20 May 2027",
   "23 May 2027",
   "29 May 2027",
   "21 May 2027"
  ]
 },
 {
  "qid": "qa8429b836e",
  "kind": "yes/no",
  "text": "From: Kofi Mensah\nFile: NTC-7479\nSent to: review team\nThe file about the response deadline is shared in the usual way.\n\nNotice NTC-7479 to Kofi Mensah:\n- response due date: Thursday, May 4, 2028\n- office cutoff on the due date: 4 May 2028, 15:36 (UTC-05:00)\n- response sent: 4 May 2028, 23:37 (UTC+03:00) [same instant in office time: 4 May 2028, 15:37 (UTC-05:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Kofi Mensah to notice NTC-7479, under the receipt rule, counted as received on time?"
 },
 {
  "qid": "q1b73ae79ae",
  "kind": "yes/no",
  "text": "Maya Lindgren: Hey, sending case file NTC-4476 about the response deadline, hope it brightens the room.\ndesk: That is a lovely note, thanks!\ndesk: Good fun, I enjoyed reading it.\n\nNotice NTC-4476 to Maya Lindgren:\n- response due date: Saturday, July 26, 2025\n- office cutoff on the due date: 26 July 2025, 22:14 (UTC-04:00)\n- response sent: 2025-07-25T14:27:00Z [same instant in office time: 25 July 2025, 10:27 (UTC-04:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Maya Lindgren late, since the office recorded it as received after the due date under the receipt rule?"
 },
 {
  "qid": "q4e26b1531b",
  "kind": "yes/no",
  "text": "Paolo Greco: File CASE-6871 is sent about the claim deadline question as normal.\ncase team: Received, thank you.\n\nCase CASE-6871, party Paolo Greco:\n- invoice date: 19 Jan 2027\n- goods received date: 14 Jan 2027\n- claim filed on: 19 Apr 2027\n- days from the invoice date to the filing: 90 days\n- days from the goods received date to the filing: 95 days",
  "question": "Filing rule: the claim must be filed within 90 days starting from the later of the dates listed below: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the claim from Paolo Greco filed in time, on or before the final day of the filing period?"
 },
 {
  "qid": "q5c1b8cd11f",
  "kind": "choice",
  "text": "Hi front desk,\nMira Castell sends file STAY-6743 about the border stay check in the usual form. The file sits in the standard layout alongside the other sheets.\nRegards,\n\nStay record STAY-6743 for Mira Castell:\n- entry day Monday, July 28, 2025, exit day Monday, August 11, 2025 (whole stay: 15 days)\n- entry day Monday, September 15, 2025, exit day Sunday, October 5, 2025 (whole stay: 21 days)\nReference date: Thursday, November 6, 2025\nWindow checked: Saturday, August 9, 2025 to Thursday, November 6, 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 30 days inside any moving 90-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present for Mira Castell fall inside the checked window ending on Thursday, November 6, 2025?",
  "options": [
   "24 days",
   "26 days",
   "36 days"
  ]
 },
 {
  "qid": "qa97e10d10f",
  "kind": "choice",
  "text": "Eva Marsh: Hey there! Sending file STAY-1249 about the border stay check your way, hope it helps lol.\nservice: Thanks so much, that is great.\ndesk: Awesome, we have it on screen.\n\nStay record STAY-1249 for Eva Marsh:\n- entry day Monday, August 30, 2027, exit day Tuesday, September 7, 2027 (whole stay: nine days)\n- entry day Thursday, October 21, 2027, exit day Tuesday, November 2, 2027 (whole stay: thirteen days)\n- entry day Sunday, November 21, 2027, exit day Friday, December 10, 2027 (whole stay: twenty days)\nReference date: Thursday, December 23, 2027\nWindow checked: Saturday, September 25, 2027 to Thursday, December 23, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 30 days in any 90-day period that rolls forward day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days, under the stay rule, was Eva Marsh present inside the checked window ending on Thursday, December 23, 2027?",
  "options": [
   "31 days",
   "33 days"
  ]
 },
 {
  "qid": "q51d2a51302",
  "kind": "choice",
  "text": "Hey there, quick heads up that Yara Haddad has sent file STAY-8536 about the residence day count to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.\n\nStay record STAY-8536 for Yara Haddad:\n- entry day 2027-04-17, exit day 2027-05-13 (whole stay: 27 days)\n- entry day 2027-05-28, exit day 2027-05-28 (whole stay: one day)\n- entry day 2027-06-09, exit day 2027-06-26 (whole stay: eighteen days)\nReference date: 2027-07-08\nWindow checked: 2027-05-10 to 2027-07-08, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 21 days within any 60-day window that keeps moving. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, how many days present for file STAY-8536 fall inside the checked window that ends on the reference date?",
  "options": [
   "19 days",
   "23 days",
   "20 days"
  ]
 },
 {
  "qid": "qf344ab4b7e",
  "kind": "yes/no",
  "text": "Dear duty clerk,\nOwen Pryce is sending file NTC-9710 about the notice response. The file is attached for your desk. Thanks in advance for your help.\nBest,\n\nNotice NTC-9710 to Owen Pryce:\n- response due date: Sunday, September 17, 2028\n- office cutoff on the due date: 2028-09-17 12:54:00 +0530\n- response sent: 2028-09-17 16:20:00 +0900 [same instant in office time: 2028-09-17 12:50:00 +0530]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the response to notice NTC-9710 given by Owen Pryce on time under the receipt rule?"
 },
 {
  "qid": "qb00cc4d5d0",
  "kind": "choice",
  "text": "Bruno Lacerda has passed on file POL-5945 about the cover question to the desk. This memo goes with the file so it is on hand in the usual way. Thank you for your help.\n\nPolicy POL-5945, holder Bruno Lacerda:\n- policy start date: Saturday, 27 June 2026\n- theft cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 44 days starting with the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 44 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn what earliest date would a loss of this kind be covered under policy POL-5945?",
  "options": [
   "Tuesday, 11 August 2026",
   "Sunday, 9 August 2026",
   "Monday, 10 August 2026"
  ]
 },
 {
  "qid": "qce62cbad18",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nBruno Lacerda is sending file LED-5772 about the teller ledger review, with the main points at the top. Quick note, I am buried under other work.\nBest,\n\nCash ledger LED-5772, teller Bruno Lacerda:\n- April 23, 2027: deposit of $7,556\n- April 23, 2027: withdrawal of $8,846\n- April 23, 2027: withdrawal of $6,154\n- April 23, 2027: deposit of $10,133\n- April 25, 2027: deposit of $4,267\nDay under review: April 23, 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is strictly more than $15,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the cash rule call for a cash report on April 23, 2027 in ledger LED-5772?"
 },
 {
  "qid": "qec8d48d9f2",
  "kind": "choice",
  "text": "Freya Holm: Hiya! Sending POL-1588 about the cover question, all good here.\nservice desk: Lovely, thanks for the heads up!\n\nPolicy POL-1588, holder Freya Holm:\n- policy start date: 2026-05-25\n- storm damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 7 days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 7 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the earliest date on which a loss of this kind would be covered under policy POL-1588?",
  "options": [
   "2026-06-02",
   "2026-05-31",
   "2026-06-03"
  ]
 },
 {
  "qid": "qfc94ed3d49",
  "kind": "choice",
  "text": "Theo Kalnins: Sending CASE-9038 about the appeal deadline as usual.\ncase team: Received.\n\nCase CASE-9038, party Theo Kalnins:\n- decision date: 10 Mar 2028\n- delivery date: 25 Feb 2028",
  "question": "Filing rule: the appeal must be filed inside ten days reckoned from the date that falls later among the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is ten days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the latest date by which the appeal can be filed in time?",
  "options": [
   "24 Mar 2028",
   "20 Mar 2028",
   "22 Mar 2028"
  ]
 },
 {
  "qid": "q1a7f533dd0",
  "kind": "choice",
  "text": "Sent by: Iris Vance\nFile: LED-8222\nSent to: records clerk\nHappy to share the file about the cash ledger check, it was fun to put together. Hope it helps with the sorting.\n\nCash ledger LED-8222, teller Iris Vance:\n- 7 September 2027: withdrawal of 1,560.00 USD\n- 8 September 2027: deposit of 1,194.00 USD\n- 8 September 2027: deposit of 2,358.00 USD\n- 8 September 2027: withdrawal of 1,555.00 USD\nDay under review: 8 September 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any figure at or above 3,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, for Iris Vance on 8 September 2027, which of the day's totals call for a cash report?",
  "options": [
   "Only the withdrawal total",
   "Only the deposit total",
   "Neither total",
   "Both totals"
  ]
 },
 {
  "qid": "q40d621b358",
  "kind": "choice",
  "text": "Lucas Brenner has sent file CASE-7881 about the claim deadline question to the desk. This is a routine item and the file is attached in full. The desk is copied for completeness. This memo concerns only the sending of the file.\n\nCase CASE-7881, party Lucas Brenner:\n- inspection date: 18 Jan 2028\n- report date: 8 Jan 2028",
  "question": "Filing rule: the objection must be filed inside 90 days extending past the later of these dates: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the latest date, under the filing rule, on which the objection for case CASE-7881 can be filed in time?",
  "options": [
   "17 Apr 2028",
   "18 Apr 2028",
   "23 May 2028"
  ]
 },
 {
  "qid": "qd1f6de97a4",
  "kind": "choice",
  "text": "Dear front desk,\nMalik Osei is writing to share file NTC-3197 about the response deadline with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,\n\nNotice NTC-3197 to Malik Osei:\n- notice date: 2 July 2027\n- sent by: post\n- 14 days after the notice date, before any postal add-on or closure: 16 July 2027\nOffice closures: 16 July 2027; 19 July 2027; 20 July 2027.",
  "question": "Response rule: a response is due 14 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 3 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, on what date is the response from Malik Osei due under the response rule?",
  "options": [
   "21 July 2027",
   "18 July 2027"
  ]
 },
 {
  "qid": "q829fd0ba8f",
  "kind": "yes/no",
  "text": "Sent by: Bruno Lacerda\nFile code: NTC-9540\nFor: review team\nThe file about the response deadline is passed along as usual.\n\nNotice NTC-9540 to Bruno Lacerda:\n- response due date: 23 April 2026\n- office cutoff on the due date: 23 April 2026, 17:37 (UTC+01:00)\n- response sent: 23 April 2026, 09:36 (UTC-07:00) [same instant in office time: 23 April 2026, 17:36 (UTC+01:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the reply to notice NTC-9540 on time under the receipt rule?"
 },
 {
  "qid": "qe7b2032ab7",
  "kind": "choice",
  "text": "Dear duty clerk,\nFelix Ortega here, sending file LED-5112 about the branch cash review. Very busy stretch on this end. The file is full and sent over fast. Thanks, speedy as ever.\nBest\n\nCash ledger LED-5112, teller Felix Ortega:\n- 2027-11-08: deposit of $1,665\n- 2027-11-09: deposit of $732\nDay under review: 2027-11-09",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is $3,000 or more, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, which of the day's totals on 2027-11-09 call for a cash report?",
  "options": [
   "Only the deposit total",
   "Neither total",
   "Only the withdrawal total",
   "Both totals"
  ]
 },
 {
  "qid": "q57c48412f1",
  "kind": "choice",
  "text": "Sender: Dana Okafor\nFile: CASE-1900\nTo: records clerk\nThe file about the appeal deadline is attached. Sending it on in a hurry.\n\nCase CASE-1900, party Dana Okafor:\n- decision date: Friday, 17 September 2027\n- delivery date: Monday, 1 November 2027",
  "question": "Filing rule: the appeal must be filed inside 21 days beginning at the later of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, until which final day may Dana Okafor file the appeal and still be in time?",
  "options": [
   "Monday, 22 November 2027",
   "Tuesday, 23 November 2027",
   "Saturday, 20 November 2027"
  ]
 },
 {
  "qid": "q9581993323",
  "kind": "yes/no",
  "text": "Sent by: Mira Castell\nFile: CASE-7642\nSent to: records clerk\nHappy to share the file about the appeal deadline, it was fun to put together. Hope it helps with the sorting.\n\nCase CASE-7642, party Mira Castell:\n- billing date: 24 Sep 2027\n- statement date: 17 Sep 2027\n- dispute filed on: 3 Nov 2027\n- days from the billing date to the filing: 40 days\n- days from the statement date to the filing: 47 days",
  "question": "Filing rule: the dispute must be filed within 21 days measured from the later of the dates below: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is it true that the dispute was not filed in time?"
 },
 {
  "qid": "qa2e0096131",
  "kind": "yes/no",
  "text": "Aiko Brandt: Hiya! Sending POL-8694 about the insurance claim, all good here.\nservice desk: Lovely, thanks for the heads up!\n\nPolicy POL-8694, holder Aiko Brandt:\n- policy start date: 2026-04-14\n- storm damage cover: part of the base policy\n- storm damage loss on: 2026-05-29\n- days from the policy start date to the loss: 45 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is the storm damage loss for Aiko Brandt covered under the cover rule?"
 },
 {
  "qid": "qf2e3a8b3c4",
  "kind": "yes/no",
  "text": "Dear front desk,\nBruno Lacerda is sending file LED-2566 about the teller ledger review. This is a routine send and the file is full. The matter is in good shape as usual.\nRegards\n\nCash ledger LED-2566, teller Bruno Lacerda:\n- Sunday, September 3, 2028: withdrawal of 10,000.00 USD\n- Tuesday, September 5, 2028: withdrawal of 3,760.00 USD\nDay under review: Sunday, September 3, 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is greater than 10,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is a cash report required for Sunday, September 3, 2028 in ledger LED-2566?"
 },
 {
  "qid": "q8935f429ce",
  "kind": "yes/no",
  "text": "From: Omar Saleh\nFile: LED-9942\nSent to: review team\nThis file about the branch cash review is passed along with thanks for your help.\n\nCash ledger LED-9942, teller Omar Saleh:\n- Monday, June 29, 2026: deposit of $2,786\n- Wednesday, July 1, 2026: deposit of $1,883\nDay under review: Monday, June 29, 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any figure at or above $3,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is a cash report required for Monday, June 29, 2026 in the case of Omar Saleh?"
 },
 {
  "qid": "q839cfcf901",
  "kind": "yes/no",
  "text": "From: Ines Duarte\nFile: STAY-3942\nSent to: review team\nThis file about the border stay check is passed along with thanks for your help.\n\nStay record STAY-3942 for Ines Duarte:\n- entry day 9 January 2027, exit day 26 March 2027 (whole stay: 77 days)\n- entry day 7 May 2027, exit day 16 May 2027 (whole stay: 10 days)\n- entry day 17 June 2027, exit day 15 July 2027 (whole stay: 29 days)\nReference date: 2 August 2027\nWindow checked: 4 February 2027 to 2 August 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 90 days in any 180-day period that rolls forward day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does Ines Duarte have more days present in the checked window ending on 2 August 2027 than the stay limit?"
 },
 {
  "qid": "q75d0e09c42",
  "kind": "yes/no",
  "text": "Clara Weiss: Dear team, I am forwarding file LED-8656 about the cash ledger check to the intake team.\nintake: Thank you for passing it along.\nteam: With thanks for your courtesy.\n\nCash ledger LED-8656, teller Clara Weiss:\n- 16 May 2025: withdrawal of $8,904\n- 18 May 2025: withdrawal of $16,354\n- 19 May 2025: deposit of $9,867\nDay under review: 18 May 2025",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is anything strictly greater than $15,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is a cash report required for 18 May 2025?"
 },
 {
  "qid": "q6da82d9f42",
  "kind": "yes/no",
  "text": "Aiko Brandt: Hiya! Sending POL-8694 about the insurance claim, all good here.\nservice desk: Lovely, thanks for the heads up!\n\nPolicy POL-8694, holder Aiko Brandt:\n- policy start date: 2026-04-14\n- storm damage cover: part of the base policy\n- storm damage loss on: 2026-05-29\n- days from the policy start date to the loss: 45 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid the storm damage loss in policy POL-8694 occur within the waiting period, on or before its final day, under the cover rule?"
 },
 {
  "qid": "qb7a345f06a",
  "kind": "choice",
  "text": "Sent by: Owen Pryce\nFile: NTC-6448\nSent to: review team\nThank you for your attention to the file about the response deadline. I remain grateful for the careful reading.\n\nNotice NTC-6448 to Owen Pryce:\n- response due date: 15 February 2027\n- office cutoff on the due date: 2027-02-15T22:11:00-05:00\n- response sent: 2027-02-13T13:16:00+10:00 [same instant in office time: 2027-02-12T22:16:00-05:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, which date counts as the receipt date for the response from Owen Pryce?",
  "options": [
   "February 13, 2027",
   "February 12, 2027"
  ]
 },
 {
  "qid": "q8f0c3603aa",
  "kind": "yes/no",
  "text": "Omar Saleh has sent file CASE-4574 about the complaint filing to the admin team. It is a friendly little bundle for the admin desks. Thanks for the lovely teamwork.\n\nCase CASE-4574, party Omar Saleh:\n- purchase date: 5 July 2027\n- handover date: 10 July 2027\n- refund request filed on: 10 August 2027\n- days from the purchase date to the filing: 36 days\n- days from the handover date to the filing: 31 days",
  "question": "Filing rule: the refund request must be filed inside fourteen days counted from the later of these dates: the purchase date and the handover date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is fourteen days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the refund request from Omar Saleh in case CASE-4574 filed on or before the final day of the filing period?"
 },
 {
  "qid": "q72a50317aa",
  "kind": "yes/no",
  "text": "Mira Castell: Sending CASE-4754 about the complaint filing, a routine send.\nintake team: Received, thanks.\n\nCase CASE-4754, party Mira Castell:\n- incident date: Saturday, 19 July 2025\n- discovery date: Thursday, 17 July 2025\n- complaint filed on: Wednesday, 30 July 2025\n- days from the incident date to the filing: 11 days\n- days from the discovery date to the filing: 13 days",
  "question": "Filing rule: the complaint must be filed within 10 days past the later of the dates below: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 10 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the complaint lodged by the final day of the filing period?"
 },
 {
  "qid": "q91d45d66ed",
  "kind": "yes/no",
  "text": "From: Kofi Mensah\nFile: NTC-7479\nSent to: review team\nThe file about the response deadline is shared in the usual way.\n\nNotice NTC-7479 to Kofi Mensah:\n- response due date: Thursday, May 4, 2028\n- office cutoff on the due date: 4 May 2028, 15:36 (UTC-05:00)\n- response sent: 4 May 2028, 23:32 (UTC+03:00) [same instant in office time: 4 May 2028, 15:32 (UTC-05:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Kofi Mensah to notice NTC-7479, under the receipt rule, counted as received on time?"
 },
 {
  "qid": "q44f929110b",
  "kind": "choice",
  "text": "Ines Duarte: file CASE-6659 about the appeal deadline is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.\n\nCase CASE-6659, party Ines Duarte:\n- billing date: 24 August 2027\n- statement date: 31 August 2027",
  "question": "Filing rule: the dispute must be filed within 90 days running from the later of the dates below: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, by which final day must the dispute be filed to still count as in time?",
  "options": [
   "29 November 2027",
   "4 January 2028",
   "1 December 2027",
   "30 November 2027"
  ]
 },
 {
  "qid": "q6870c94e7f",
  "kind": "yes/no",
  "text": "Ravi Anand: sending STAY-1179 about the residence day count, in a rush.\nservice desk: got it, thanks.\ndesk: that is the full file.\n\nStay record STAY-1179 for Ravi Anand:\n- entry day Monday, November 23, 2026, exit day Sunday, November 29, 2026 (whole stay: 7 days)\n- entry day Monday, December 28, 2026, exit day Wednesday, January 6, 2027 (whole stay: 10 days)\n- entry day Wednesday, January 20, 2027, exit day Wednesday, January 20, 2027 (whole stay: 1 day)\nReference date: Sunday, February 7, 2027\nWindow checked: Thursday, December 10, 2026 to Sunday, February 7, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 21 days inside every moving 60-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is Ravi Anand over the stay limit in record STAY-1179 when counting just the checked window that ends on the reference date?"
 },
 {
  "qid": "q7c1adbbecd",
  "kind": "yes/no",
  "text": "Ana Ruiz has sent file STAY-7389 about the border stay check to the desk. This is a routine item and the file is attached in full. The desk is copied for completeness. This memo concerns only the sending of the file.\n\nStay record STAY-7389 for Ana Ruiz:\n- entry day Monday, 17 May 2027, exit day Friday, 11 June 2027 (whole stay: 26 days)\n- entry day Wednesday, 30 June 2027, exit day Wednesday, 30 June 2027 (whole stay: one day)\n- entry day Tuesday, 20 July 2027, exit day Wednesday, 11 August 2027 (whole stay: 23 days)\nReference date: Thursday, 26 August 2027\nWindow checked: Saturday, 29 May 2027 to Thursday, 26 August 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 30 days inside any moving 90-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is it true that Ana Ruiz is not over the stay limit in the window ending on the reference date?"
 },
 {
  "qid": "qa4f40b3cfa",
  "kind": "choice",
  "text": "Maya Lindgren has shared file LED-9060 about the branch cash review with the desk. The file goes in the usual way. This memo is for the file set.\n\nCash ledger LED-9060, teller Maya Lindgren:\n- Tuesday, October 27, 2026: withdrawal of $3,132.00\n- Tuesday, October 27, 2026: withdrawal of $1,869.00\n- Tuesday, October 27, 2026: deposit of $7,212.00\n- Thursday, October 29, 2026: deposit of $3,814.00\nDay under review: Tuesday, October 27, 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is anything strictly greater than $5,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals in ledger LED-9060 call for a cash report?",
  "options": [
   "Only the withdrawal total",
   "Both totals",
   "Only the deposit total",
   "Neither total"
  ]
 },
 {
  "qid": "q680bd9d0a7",
  "kind": "yes/no",
  "text": "Ana Ruiz: Hello, I am sending file NTC-8765 about the notice response to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nNotice NTC-8765 to Ana Ruiz:\n- response due date: 5 December 2025\n- office cutoff on the due date: 5 December 2025, 13:20 (UTC+02:00)\n- response sent: 5 December 2025, 14:22 (UTC+03:00) [same instant in office time: 5 December 2025, 13:22 (UTC+02:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Ana Ruiz to notice NTC-8765 on time under the receipt rule?"
 },
 {
  "qid": "q5dfe5eef2e",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nHope you are doing great! Felix Ortega has sent file NTC-4741 about the response deadline, all lovely and tidy. Just wanted to pop it in your inbox. Catch you round.\nCheers\n\nNotice NTC-4741 to Felix Ortega:\n- response due date: 19 April 2027\n- office cutoff on the due date: 2027-04-19T17:00:00-04:00\n- response sent: 2027-04-19T21:57:00+01:00 [same instant in office time: 2027-04-19T16:57:00-04:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Felix Ortega received on time under the receipt rule?"
 },
 {
  "qid": "qb102cd5614",
  "kind": "yes/no",
  "text": "Paolo Greco: file CASE-3754 about the complaint filing is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.\n\nCase CASE-3754, party Paolo Greco:\n- purchase date: Friday, 17 September 2027\n- handover date: Sunday, 12 September 2027\n- refund request filed on: Friday, 1 October 2027\n- days from the purchase date to the filing: fourteen days\n- days from the handover date to the filing: nineteen days",
  "question": "Filing rule: the refund request must be filed within fourteen days measured from the later of the dates below: the purchase date and the handover date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is fourteen days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Paolo Greco, under the filing rule, fail to file the refund request in time?"
 },
 {
  "qid": "qdd5423a0a1",
  "kind": "yes/no",
  "text": "Priya Raman has sent file CASE-4654 about the claim deadline question to the desk. This is a routine item and the file is attached in full. The desk is copied for completeness. This memo concerns only the sending of the file.\n\nCase CASE-4654, party Priya Raman:\n- invoice date: 2026-06-19\n- goods received date: 2026-07-10\n- claim filed on: 2026-08-01\n- days from the invoice date to the filing: 43 days\n- days from the goods received date to the filing: 22 days",
  "question": "Filing rule: the claim must be filed inside 21 days that elapses after whichever of the dates below is later: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Priya Raman, under the filing rule, file the claim on or before the final day?"
 },
 {
  "qid": "q297e34d6d6",
  "kind": "yes/no",
  "text": "Ana Ruiz: Hi, here is file CASE-5863 about the appeal deadline, with plenty of cheer.\ndesk: Lovely, thanks so much!\ndesk: That is fun to read.\n\nCase CASE-5863, party Ana Ruiz:\n- decision date: Tuesday, 27 July 2027\n- delivery date: Sunday, 27 June 2027\n- appeal filed on: Wednesday, 28 July 2027\n- days from the decision date to the filing: 1 day\n- days from the delivery date to the filing: 31 days",
  "question": "Filing rule: the appeal must be filed inside 14 days that elapses after whichever of the dates below is later: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 14 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the appeal from Ana Ruiz in case CASE-5863 filed in time, on or before the final day?"
 },
 {
  "qid": "qdfe4fb7a38",
  "kind": "choice",
  "text": "Sara Ilves: Greetings, I am sending file NTC-3847 about the response deadline for your kind attention.\ncase team: Thank you very much, it has been received.\n\nNotice NTC-3847 to Sara Ilves:\n- response due date: 2028-04-04\n- office cutoff on the due date: 2028-04-04 12:15:00 +0100\n- response sent: 2028-04-05 08:47:00 -0300 [same instant in office time: 2028-04-05 12:47:00 +0100]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn which date does the office treat the response to notice NTC-3847 as received under the receipt rule?",
  "options": [
   "April 6, 2028",
   "April 4, 2028"
  ]
 },
 {
  "qid": "q89bc2c6415",
  "kind": "yes/no",
  "text": "Paolo Greco: file CASE-3754 about the complaint filing is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.\n\nCase CASE-3754, party Paolo Greco:\n- purchase date: Friday, 17 September 2027\n- handover date: Sunday, 12 September 2027\n- refund request filed on: Friday, 1 October 2027\n- days from the purchase date to the filing: fourteen days\n- days from the handover date to the filing: nineteen days",
  "question": "Filing rule: the refund request must be filed within fourteen days measured from the later of the dates below: the purchase date and the handover date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is fourteen days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the refund request from Paolo Greco filed in time, on or before the final day of the filing period?"
 },
 {
  "qid": "q5b2d635ab1",
  "kind": "yes/no",
  "text": "Ana Ruiz: file CASE-6831 about the complaint filing is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.\n\nCase CASE-6831, party Ana Ruiz:\n- incident date: Tuesday, 14 September 2027\n- discovery date: Sunday, 29 August 2027\n- complaint filed on: Monday, 20 September 2027\n- days from the incident date to the filing: 6 days\n- days from the discovery date to the filing: 22 days",
  "question": "Filing rule: the complaint must be filed within 14 days from whichever is later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 14 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Ana Ruiz, under the filing rule, fail to file the complaint in time?"
 },
 {
  "qid": "q5a4e97cb0d",
  "kind": "yes/no",
  "text": "Lena Whitcombe: Sending POL-9829 about the loss claim, a routine send.\nintake team: Received, thanks.\n\nPolicy POL-9829, holder Lena Whitcombe:\n- policy start date: 31 August 2026\n- power surge damage cover: added by a rider effective 9 February 2027\n- power surge damage loss on: 11 May 2027\n- days from the policy start date to the loss: 253 days\n- days from the rider effective date to the loss: 91 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 90 days starting with the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 90 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the power surge damage loss on policy POL-9829 is not covered under the cover rule?"
 },
 {
  "qid": "q5de66919bb",
  "kind": "choice",
  "text": "Maya Lindgren is sending file POL-2835 about the cover question to the admin team. It goes out in a hurry, with the attached pages in place. Thanks in advance.\n\nPolicy POL-2835, holder Maya Lindgren:\n- policy start date: 24 May 2026\n- flood damage cover: added by a rider effective 2 December 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on what earliest date would the flood damage loss be covered?",
  "options": [
   "3 January 2027",
   "2 January 2027",
   "14 January 2027"
  ]
 },
 {
  "qid": "qae5beb5eea",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nClara Weiss here, sending file POL-3156 about the loss claim and hoping it brightens your desk. Big thanks to the team on this.\nCheers,\n\nPolicy POL-3156, holder Clara Weiss:\n- policy start date: Tuesday, October 5, 2027\n- glass breakage cover: added by a rider effective Monday, October 18, 2027\n- glass breakage loss on: Monday, November 1, 2027\n- days from the policy start date to the loss: 27 days\n- days from the rider effective date to the loss: fourteen days",
  "question": "Cover rule: a loss is covered only after a waiting period of fourteen days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is fourteen days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the glass breakage loss on policy POL-3156 covered under the cover rule?"
 },
 {
  "qid": "q2e813639f8",
  "kind": "choice",
  "text": "Priya Raman: sending CASE-9814 about the complaint filing, in a rush.\nservice desk: got it, thanks.\nservice desk: good work, cheers.\n\nCase CASE-9814, party Priya Raman:\n- incident date: May 23, 2028\n- discovery date: May 13, 2028",
  "question": "Filing rule: the complaint must be filed within 45 days after the later date out of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the latest date by which the complaint can be filed in time?",
  "options": [
   "July 8, 2028",
   "July 7, 2028",
   "July 9, 2028",
   "July 25, 2028"
  ]
 }
]
