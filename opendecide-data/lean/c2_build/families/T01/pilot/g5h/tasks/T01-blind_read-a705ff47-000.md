# G5-H blind read T01-blind_read-a705ff47-000 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T01/pilot/g5h/answers/T01-blind_read-a705ff47-000.json

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
  "qid": "q2599b6cd7c",
  "kind": "choice",
  "text": "clerk: heads up, a new item is landing\nHana Sato: file LED-1892 about the teller ledger review is going to the help desk\ndesk: understood, routing it straight away\n\nCash ledger LED-1892, teller Hana Sato:\n- Monday, May 3, 2027: deposit of 1,223.00 USD\n- Wednesday, May 5, 2027: deposit of 1,209.00 USD\n- Wednesday, May 5, 2027: deposit of 308.00 USD\n- Wednesday, May 5, 2027: withdrawal of 153.00 USD\n- Wednesday, May 5, 2027: withdrawal of 1,574.00 USD\nDay under review: Wednesday, May 5, 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is anything strictly greater than 3,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals in ledger LED-1892 for Wednesday, May 5, 2027 call for a cash report under the cash rule?",
  "options": [
   "Both totals",
   "Neither total",
   "Only the deposit total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q700a278cda",
  "kind": "choice",
  "text": "Desk memo: Kindly be informed that Omar Saleh has forwarded file LED-2015 concerning the cash ledger check to the records clerk.\nWe appreciate your attention.\n\nCash ledger LED-2015, teller Omar Saleh:\n- 2027-08-06: deposit of 993.00 USD\n- 2027-08-06: deposit of 2,008.00 USD\n- 2027-08-07: withdrawal of 889.00 USD\nDay under review: 2027-08-06",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any amount that is more than 3,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals in ledger LED-2015 for 2027-08-06 call for a cash report under the cash rule?",
  "options": [
   "Neither total",
   "Only the withdrawal total",
   "Both totals",
   "Only the deposit total"
  ]
 },
 {
  "qid": "q19f10154b9",
  "kind": "yes/no",
  "text": "{\"file\": \"POL-2297\", \"sent_by\": \"Ravi Anand\", \"subject\": \"the loss claim\", \"team\": \"intake team\", \"channel\": \"polite intake\"}\n\nPolicy POL-2297, holder Ravi Anand:\n- policy start date: Wednesday, September 8, 2027\n- burst pipe damage cover: added by a rider effective Friday, January 28, 2028\n- burst pipe damage loss on: Sunday, February 13, 2028\n- days from the policy start date to the loss: 158 days\n- days from the rider effective date to the loss: 16 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days whose opening day is the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the burst pipe damage loss on policy POL-2297 is not covered under the cover rule?"
 },
 {
  "qid": "q7ee52e96df",
  "kind": "choice",
  "text": "[desk] file NTC-8988 sent_by Malik Osei subject=the response deadline\n[route] standard_hand_off to_desk\n\nNotice NTC-8988 to Malik Osei:\n- notice date: 13 Sep 2027\n- sent by: email\n- fourteen days after the notice date, before any postal add-on or closure: 27 Sep 2027\nOffice closures: 16 Sep 2027.",
  "question": "Response rule: a response is due fourteen days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add three days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on which date under the response rule is the response to notice NTC-8988 due?",
  "options": [
   "27 Sep 2027",
   "29 Sep 2027",
   "25 Sep 2027"
  ]
 },
 {
  "qid": "q9ec7a51aa9",
  "kind": "choice",
  "text": "desk: the border stay check sounds fun, good to hear from you\nAna Ruiz: hey there, this brings in STAY-1636 for the admin team, happy to help\n\nStay record STAY-1636 for Ana Ruiz:\n- entry day 2027-11-28, exit day 2027-12-08 (whole stay: 11 days)\n- entry day 2027-12-15, exit day 2028-01-05 (whole stay: 22 days)\nReference date: 2028-01-27\nWindow checked: 2027-12-29 to 2028-01-27, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 14 days during any 30-day window that moves ahead. Day counts are calendar days, and entry and exit days both count as days present. Only one 30-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 14 days, and within the limit if it is 14 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days present does Ana Ruiz have inside the checked window ending on 2028-01-27?",
  "options": [
   "8 days",
   "33 days",
   "9 days"
  ]
 },
 {
  "qid": "qb7d5b1b4b5",
  "kind": "choice",
  "text": "file: POL-1677\nsent_by: Bruno Lacerda\nsubject: the insurance claim\nteam: review team\nchannel: cheerful_hello\n\nPolicy POL-1677, holder Bruno Lacerda:\n- policy start date: 2026-06-03\n- storm damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days whose opening count lands on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date, under the cover rule, from which the storm damage loss would be covered?",
  "options": [
   "2026-07-04",
   "2026-07-06",
   "2026-07-02"
  ]
 },
 {
  "qid": "qfe03459c52",
  "kind": "choice",
  "text": "{\"channel\": \"quick_drop\", \"sent_by\": \"Owen Pryce\", \"file\": \"NTC-1342\", \"subject\": \"the response deadline\", \"team\": \"admin team\"}\n\nNotice NTC-1342 to Owen Pryce:\n- notice date: Wednesday, 13 September 2028\n- sent by: hand delivery\n- 21 days after the notice date, before any postal add-on or closure: Wednesday, 4 October 2028\nOffice closures: Monday, 9 October 2028; Sunday, 15 October 2028.",
  "question": "Response rule: a response is due 21 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 5 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, on which date is the response to notice NTC-1342 due under the response rule?",
  "options": [
   "Friday, 6 October 2028",
   "Tuesday, 10 October 2028",
   "Wednesday, 4 October 2028"
  ]
 },
 {
  "qid": "q0a524202fb",
  "kind": "choice",
  "text": "file: STAY-8127\nsent_by: Tomas Lindqvist\nsubject: the visa stay count\nteam: review team\nchannel: cheerful_hello\n\nStay record STAY-8127 for Tomas Lindqvist:\n- entry day April 2, 2025, exit day June 20, 2025 (whole stay: 80 days)\n- entry day July 24, 2025, exit day August 5, 2025 (whole stay: 13 days)\n- entry day September 1, 2025, exit day September 25, 2025 (whole stay: 25 days)\nReference date: October 22, 2025\nWindow checked: April 26, 2025 to October 22, 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 90 days inside every 180-day stretch that moves along. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, how many days present for file STAY-8127 fall inside the checked window that ends on the reference date?",
  "options": [
   "93 days",
   "95 days",
   "91 days",
   "94 days"
  ]
 },
 {
  "qid": "qb97eeb9b23",
  "kind": "yes/no",
  "text": "File STAY-6836 about the residence day count is set out below. Ines Duarte sends over the document for the intake team. Thank you for your attention.\n\nStay record STAY-6836 for Ines Duarte:\n- entry day Sunday, March 22, 2026, exit day Tuesday, April 21, 2026 (whole stay: 31 days)\n- entry day Tuesday, May 12, 2026, exit day Friday, May 15, 2026 (whole stay: 4 days)\n- entry day Tuesday, June 9, 2026, exit day Monday, July 6, 2026 (whole stay: 28 days)\nReference date: Monday, July 6, 2026\nWindow checked: Wednesday, April 8, 2026 to Monday, July 6, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 45 days in any 90-day period that rolls forward day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Ines Duarte over the stay limit, counting the days present inside the window that ends on Monday, July 6, 2026?"
 },
 {
  "qid": "q8c2877954c",
  "kind": "choice",
  "text": "desk: the loss claim is on the table\nFreya Holm: here is file POL-2398 for you to read\nclerk: got it, thanks\n\nPolicy POL-2398, holder Freya Holm:\n- policy start date: Sunday, 22 August 2027\n- subsidence cover: added by a rider effective Wednesday, 9 February 2028",
  "question": "Cover rule: a loss is covered only after a waiting period of 50 days that picks up on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 50 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the earliest date on which the subsidence loss would be covered?",
  "options": [
   "Wednesday, 29 March 2028",
   "Friday, 31 March 2028",
   "Thursday, 20 April 2028"
  ]
 },
 {
  "qid": "q50e9f2455e",
  "kind": "yes/no",
  "text": "agent: Welcome, the desk is listening, go ahead.\nPaolo Greco: Thank you, calling to send file POL-1220 about the cover question to the case team.\nagent: Understood, the case team takes that from here.\n\nPolicy POL-1220, holder Paolo Greco:\n- policy start date: February 17, 2026\n- flood damage cover: part of the base policy\n- flood damage loss on: February 25, 2026\n- days from the policy start date to the loss: eight days",
  "question": "Cover rule: a loss is covered only after a waiting period of seven days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is seven days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the loss in policy POL-1220 covered when the cover rule is applied?"
 },
 {
  "qid": "q089b65d484",
  "kind": "yes/no",
  "text": "sent_by: Lucas Brenner\nfile: NTC-5724\nsubject: the notice response\nteam: review\nchannel: quick_lane\n\nNotice NTC-5724 to Lucas Brenner:\n- response due date: 21 May 2025\n- office cutoff on the due date: 21 May 2025, 16:00 (UTC+02:00)\n- response sent: 21 May 2025, 10:55 (UTC-03:00) [same instant in office time: 21 May 2025, 15:55 (UTC+02:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response to notice NTC-5724 on time under the receipt rule?"
 },
 {
  "qid": "q7df6e5f99a",
  "kind": "choice",
  "text": "Subject: routine file for the case team\nDear case team,\nFile CASE-7048 about the claim deadline question has been sent in by Lena Whitcombe. Standard handling applies.\nRegards\n\nCase CASE-7048, party Lena Whitcombe:\n- inspection date: 2026-10-19\n- report date: 2026-10-20",
  "question": "Filing rule: the objection must be filed within 21 days following the later of these dates: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUntil which date, under the filing rule, may Lena Whitcombe file the objection in time?",
  "options": [
   "2026-11-18",
   "2026-11-11",
   "2026-11-10"
  ]
 },
 {
  "qid": "q853a91eb5a",
  "kind": "choice",
  "text": "Desk memo: Eva Marsh sends file LED-7994 about the branch cash review to the records clerk. The clerk gets a copy for the shelf in the usual way. Please keep this simple.\n\nCash ledger LED-7994, teller Eva Marsh:\n- 13 October 2026: deposit of $5,450\n- 13 October 2026: withdrawal of $1,857\n- 13 October 2026: deposit of $664\n- 15 October 2026: deposit of $3,581\nDay under review: 13 October 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is a figure greater than $5,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals recorded in ledger LED-7994 call for a cash report under the cash rule?",
  "options": [
   "Both totals",
   "Neither total",
   "Only the withdrawal total",
   "Only the deposit total"
  ]
 },
 {
  "qid": "q0add45d766",
  "kind": "yes/no",
  "text": "service desk: Send it over, ready for it.\nPaolo Greco: Here is file POL-8418, the insurance claim, a rush job.\n\nPolicy POL-8418, holder Paolo Greco:\n- policy start date: 18 Jan 2027\n- glass breakage cover: part of the base policy\n- glass breakage loss on: 26 Jan 2027\n- days from the policy start date to the loss: eight days",
  "question": "Cover rule: a loss is covered only after a waiting period of ten days whose earliest counted day is the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is ten days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid the glass breakage loss in policy POL-8418 occur within the waiting period, on or before its final day, under the cover rule?"
 },
 {
  "qid": "qb4f47562d1",
  "kind": "yes/no",
  "text": "{\"file\": \"CASE-1232\", \"sent_by\": \"Tomas Lindqvist\", \"subject\": \"the claim deadline question\", \"note\": \"big thanks\", \"channel\": \"service_desk\"}\n\nCase CASE-1232, party Tomas Lindqvist:\n- invoice date: 8 Mar 2026\n- goods received date: 3 Feb 2026\n- claim filed on: 14 Mar 2026\n- days from the invoice date to the filing: 6 days\n- days from the goods received date to the filing: 39 days",
  "question": "Filing rule: the claim must be filed within 30 days running from the later of the dates below: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the claim lodged by the final day of the filing period?"
 },
 {
  "qid": "qd40370cc7d",
  "kind": "yes/no",
  "text": "title | rush handoff\nrequester | Freya Holm\nfile | STAY-5106\nDropping the border stay check with the admin team, board is full.\n\nStay record STAY-5106 for Freya Holm:\n- entry day Sunday, December 6, 2026, exit day Thursday, January 7, 2027 (whole stay: 33 days)\n- entry day Wednesday, January 13, 2027, exit day Wednesday, January 20, 2027 (whole stay: eight days)\nReference date: Sunday, January 31, 2027\nWindow checked: Saturday, January 2, 2027 to Sunday, January 31, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most fourteen days across any 30-day window that slides ahead day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 30-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than fourteen days, and within the limit if it is fourteen days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does Freya Holm have more days present in the checked window ending on Sunday, January 31, 2027 than the stay limit?"
 },
 {
  "qid": "q07e2905ac4",
  "kind": "choice",
  "text": "Lucas Brenner: Hi there, file CASE-1419 about the appeal deadline is winging its way to you!\nclerk: Lovely, the admin team sorts it out from there.\n\nCase CASE-1419, party Lucas Brenner:\n- decision date: 19 May 2026\n- delivery date: 20 May 2026",
  "question": "Filing rule: the appeal must be filed within 90 days after the later date out of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, by which final day can Lucas Brenner still file the appeal and remain in time?",
  "options": [
   "18 August 2026",
   "23 September 2026",
   "17 August 2026"
  ]
 },
 {
  "qid": "qb8faae14ae",
  "kind": "yes/no",
  "text": "sent_by: Sara Ilves\nteam: duty clerk\nchannel: formal intake\nfile: POL-7433\nsubject: the insurance claim\n\nPolicy POL-7433, holder Sara Ilves:\n- policy start date: Sunday, 6 December 2026\n- power surge damage cover: added by a rider effective Saturday, 30 January 2027\n- power surge damage loss on: Sunday, 28 February 2027\n- days from the policy start date to the loss: 84 days\n- days from the rider effective date to the loss: 29 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days starting with the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is the power surge damage loss covered under the cover rule?"
 },
 {
  "qid": "qaec4c21c00",
  "kind": "choice",
  "text": "Subject: file handover\nDear duty clerk,\nThe file LED-1537 has come from Clara Weiss about the teller ledger review, for your desk.\nRegards,\n\nCash ledger LED-1537, teller Clara Weiss:\n- April 3, 2026: withdrawal of $6,313.00\n- April 4, 2026: deposit of $303.00\n- April 4, 2026: withdrawal of $788.00\n- April 4, 2026: deposit of $4,089.00\n- April 4, 2026: withdrawal of $3,313.00\nDay under review: April 4, 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any total greater than $10,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals on April 4, 2026 in ledger LED-1537, under the cash rule, call for a cash report?",
  "options": [
   "Both totals",
   "Only the deposit total",
   "Neither total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "qe9931afc06",
  "kind": "yes/no",
  "text": "title | the reply timing question with file NTC-7818\nrequester | Malik Osei\nteam | review_team\nnote | shares it here, thanks\n\nNotice NTC-7818 to Malik Osei:\n- response due date: 2028-08-09\n- office cutoff on the due date: 9 August 2028, 17:00 (UTC+09:00)\n- response sent: 2028-08-09T12:44:00Z [same instant in office time: 9 August 2028, 21:44 (UTC+09:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the reply to notice NTC-7818 on time under the receipt rule?"
 },
 {
  "qid": "q8942040501",
  "kind": "yes/no",
  "text": "[mail] pass_along=Lena Whitcombe file=CASE-3143 queue=admin_team\n[mail] subject=the claim deadline question big_thanks\n\nCase CASE-3143, party Lena Whitcombe:\n- invoice date: 2027-02-21\n- goods received date: 2027-01-22\n- claim filed on: 2027-03-23\n- days from the invoice date to the filing: 30 days\n- days from the goods received date to the filing: 60 days",
  "question": "Filing rule: the claim must be filed within 45 days following the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is it true that the claim was not filed in time?"
 },
 {
  "qid": "q020948c089",
  "kind": "yes/no",
  "text": "service desk: Send it over, ready for it.\nOmar Saleh: Here is file STAY-2562, the residence day count, a rush job.\n\nStay record STAY-2562 for Omar Saleh:\n- entry day Tuesday, May 27, 2025, exit day Wednesday, July 23, 2025 (whole stay: 58 days)\n- entry day Thursday, August 21, 2025, exit day Wednesday, September 10, 2025 (whole stay: 21 days)\nReference date: Thursday, October 16, 2025\nWindow checked: Thursday, June 19, 2025 to Thursday, October 16, 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days in any 120-day period that rolls forward day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is Omar Saleh over the stay limit, with more days present in the checked window ending on the reference date?"
 },
 {
  "qid": "qd84e6f5b03",
  "kind": "choice",
  "text": "Kofi Mensah: here is file STAY-3307 about the border stay check, grab it fast.\nreview team: grabbing it, busy bench here.\n\nStay record STAY-3307 for Kofi Mensah:\n- entry day 2025-03-20, exit day 2025-03-25 (whole stay: 6 days)\n- entry day 2025-03-31, exit day 2025-04-08 (whole stay: 9 days)\n- entry day 2025-05-27, exit day 2025-08-17 (whole stay: 83 days)\nReference date: 2025-09-26\nWindow checked: 2025-03-31 to 2025-09-26, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 90 days in each 180-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days present fall inside the checked window that ends on the reference date in record STAY-3307?",
  "options": [
   "91 days",
   "90 days",
   "92 days"
  ]
 },
 {
  "qid": "qb7cb5d03ce",
  "kind": "choice",
  "text": "file: STAY-8365\nsent_by: Eva Marsh\nsubject: the border stay check\nteam: records\nnote: routine handoff to the clerk\n\nStay record STAY-8365 for Eva Marsh:\n- entry day August 29, 2025, exit day September 16, 2025 (whole stay: nineteen days)\n- entry day September 24, 2025, exit day October 7, 2025 (whole stay: fourteen days)\n- entry day November 22, 2025, exit day January 22, 2026 (whole stay: 62 days)\nReference date: April 1, 2026\nWindow checked: October 4, 2025 to April 1, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 90 days inside any moving 180-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present fall inside the checked window that ends on April 1, 2026 for file STAY-8365?",
  "options": [
   "66 days",
   "62 days",
   "67 days"
  ]
 },
 {
  "qid": "q69e0cb5e2f",
  "kind": "yes/no",
  "text": "Aiko Brandt: Busy send, NTC-9422 about the reply timing question.\nservice desk: Received, thanks.\n\nNotice NTC-9422 to Aiko Brandt:\n- response due date: Thursday, 20 January 2028\n- office cutoff on the due date: 20 January 2028, 15:45 (UTC+09:00)\n- response sent: 20 January 2028, 08:46 (UTC+02:00) [same instant in office time: 20 January 2028, 15:46 (UTC+09:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Aiko Brandt to notice NTC-9422 on time under the receipt rule?"
 },
 {
  "qid": "q72fbb56d46",
  "kind": "choice",
  "text": "Omar Saleh: File NTC-8888 about the notice response is on its way to you.\nclerk: Fine, the usual steps apply.\nclerk: Standard handling for this material.\n\nNotice NTC-8888 to Omar Saleh:\n- notice date: Friday, 22 September 2028\n- sent by: email\n- twenty days after the notice date, before any postal add-on or closure: Thursday, 12 October 2028\nOffice closures: Thursday, 12 October 2028; Friday, 13 October 2028.",
  "question": "Response rule: a response is due twenty days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add two days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, on which date is the response from Omar Saleh to the notice due under the response rule?",
  "options": [
   "Friday, 20 October 2028",
   "Saturday, 14 October 2028"
  ]
 },
 {
  "qid": "qefdddbfc92",
  "kind": "yes/no",
  "text": "[intake] file=CASE-5468 sender=Nadia Kowal route=admin_team\n[intake] note=the appeal deadline is on its way\n\nCase CASE-5468, party Nadia Kowal:\n- decision date: June 23, 2026\n- delivery date: June 16, 2026\n- appeal filed on: August 23, 2026\n- days from the decision date to the filing: 61 days\n- days from the delivery date to the filing: 68 days",
  "question": "Filing rule: the appeal must be filed within 60 days after the later date out of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the appeal in case CASE-5468 filed in time, on or before the final day?"
 },
 {
  "qid": "q2cc3f64692",
  "kind": "yes/no",
  "text": "title | rush handoff\nrequester | Theo Kalnins\nfile | POL-6833\nDropping the insurance claim with the admin team, board is full.\n\nPolicy POL-6833, holder Theo Kalnins:\n- policy start date: 11 Oct 2027\n- burst pipe damage cover: part of the base policy\n- burst pipe damage loss on: 19 Oct 2027\n- days from the policy start date to the loss: 8 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 7 days that picks up on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 7 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid this burst pipe damage loss, under the cover rule, happen within the waiting period?"
 },
 {
  "qid": "q7e1f8290e6",
  "kind": "choice",
  "text": "Owen Pryce: Routine send, LED-4250 about the branch cash review.\nintake team: Received, thank you.\n\nCash ledger LED-4250, teller Owen Pryce:\n- 19 December 2027: withdrawal of $4,690\n- 21 December 2027: withdrawal of $4,941\n- 21 December 2027: withdrawal of $657\n- 21 December 2027: deposit of $17,632\nDay under review: 21 December 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any sum more than $15,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, for Owen Pryce on 21 December 2027, which of the day's totals call for a cash report?",
  "options": [
   "Both totals",
   "Neither total",
   "Only the deposit total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "qbb349c45a1",
  "kind": "choice",
  "text": "Desk memo: Ravi Anand has put file STAY-7443 on the visa stay count in front of the help desk. Lovely little hand-off, thanks for picking it up. Cheers to the team.\n\nStay record STAY-7443 for Ravi Anand:\n- entry day 16 Sep 2025, exit day 30 Oct 2025 (whole stay: 45 days)\n- entry day 8 Dec 2025, exit day 9 Jan 2026 (whole stay: 33 days)\n- entry day 31 Jan 2026, exit day 13 Mar 2026 (whole stay: 42 days)\nReference date: 12 Apr 2026\nWindow checked: 15 Oct 2025 to 12 Apr 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 90 days in any 180-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, how many days present for file STAY-7443 fall inside the checked window that ends on the reference date?",
  "options": [
   "92 days",
   "120 days",
   "91 days",
   "75 days"
  ]
 },
 {
  "qid": "q394303396d",
  "kind": "choice",
  "text": "{\n  \"sent_by\": \"Felix Ortega\",\n  \"file\": \"PO-3723\",\n  \"subject\": \"the buying request\",\n  \"team\": \"review team\",\n  \"note\": \"hiya, chatting away\"\n}\n\nPurchase log PO-3723, kept by Felix Ortega, vendor Quillon Labs:\n- earlier purchase on Wednesday, 7 January 2026: $3,905\n- new request on Thursday, 8 January 2026: $1,582\nWindow checked: Wednesday, 10 December 2025 to Thursday, 8 January 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any amount that is more than $5,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, which running total for Felix Ortega gets compared with the threshold when this new request is counted in it?",
  "options": [
   "$3,905",
   "$5,487"
  ]
 },
 {
  "qid": "q4af96ccad7",
  "kind": "choice",
  "text": "Hi front desk,\nEva Marsh sends file STAY-8365 about the border stay check as a routine copy. The file follows the standard layout and sits with the desk.\nRegards,\n\nStay record STAY-8365 for Eva Marsh:\n- entry day August 29, 2025, exit day September 16, 2025 (whole stay: nineteen days)\n- entry day September 24, 2025, exit day October 7, 2025 (whole stay: fourteen days)\n- entry day November 22, 2025, exit day January 22, 2026 (whole stay: 62 days)\nReference date: April 1, 2026\nWindow checked: October 4, 2025 to April 1, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 90 days inside any moving 180-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present fall inside the checked window that ends on April 1, 2026 for file STAY-8365?",
  "options": [
   "66 days",
   "62 days",
   "67 days"
  ]
 },
 {
  "qid": "q775324dcc6",
  "kind": "choice",
  "text": "Title | file LED-2245 about the branch cash review\nRequester | Tomas Lindqvist\nTeam | review team, cheers for the review!\n\nCash ledger LED-2245, teller Tomas Lindqvist:\n- 2025-05-16: deposit of $675\n- 2025-05-17: withdrawal of $684\n- 2025-05-17: deposit of $893\n- 2025-05-17: deposit of $1,689\n- 2025-05-17: withdrawal of $2,317\nDay under review: 2025-05-17",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any amount that is more than $3,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, for Tomas Lindqvist on 2025-05-17, which of the day's totals call for a cash report?",
  "options": [
   "Only the deposit total",
   "Both totals",
   "Neither total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q1a3568591f",
  "kind": "choice",
  "text": "{\"sent_by\": \"Clara Weiss\", \"file\": \"STAY-7294\", \"subject\": \"the visa stay count\", \"team\": \"help_desk\", \"note\": \"fast_pass\"}\n\nStay record STAY-7294 for Clara Weiss:\n- entry day August 20, 2025, exit day August 25, 2025 (whole stay: 6 days)\n- entry day October 2, 2025, exit day November 8, 2025 (whole stay: 38 days)\nReference date: December 17, 2025\nWindow checked: August 20, 2025 to December 17, 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days in each 120-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, how many days present fall inside the checked window ending on December 17, 2025 in file STAY-7294?",
  "options": [
   "46 days",
   "44 days"
  ]
 },
 {
  "qid": "qa906359f61",
  "kind": "choice",
  "text": "Sent by: Bruno Lacerda\nFile: LED-8100\nSent to: records clerk\nLovely to send this over, it is about the branch cash review. The notes are all tidy and sit nicely for the records team.\n\nCash ledger LED-8100, teller Bruno Lacerda:\n- July 26, 2025: deposit of $3,260.00\n- July 26, 2025: withdrawal of $3,761.00\n- July 27, 2025: withdrawal of $1,193.00\nDay under review: July 26, 2025",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is a figure greater than $3,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals recorded in ledger LED-8100 call for a cash report under the cash rule?",
  "options": [
   "Neither total",
   "Only the withdrawal total",
   "Only the deposit total",
   "Both totals"
  ]
 },
 {
  "qid": "q70f67269a9",
  "kind": "yes/no",
  "text": "{\"file\": \"POL-1072\", \"sent_by\": \"Iris Vance\", \"subject\": \"the cover question\", \"note\": \"kindly handled by the duty clerk\", \"channel\": \"duty_intake\"}\n\nPolicy POL-1072, holder Iris Vance:\n- policy start date: Wednesday, May 5, 2027\n- fire damage cover: added by a rider effective Monday, May 17, 2027\n- fire damage loss on: Monday, June 21, 2027\n- days from the policy start date to the loss: 47 days\n- days from the rider effective date to the loss: 35 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 60 days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 60 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is this fire damage loss covered by the cover rule?"
 },
 {
  "qid": "qe20dc962bd",
  "kind": "choice",
  "text": "[triage] the notice response from Mira Castell is logged under NTC-9973 with thanks\nroute=intake_team\n\nNotice NTC-9973 to Mira Castell:\n- notice date: 1 Jul 2026\n- sent by: email\n- 20 days after the notice date, before any postal add-on or closure: 21 Jul 2026\nOffice closures: 27 Jul 2026; 31 Jul 2026.",
  "question": "Response rule: a response is due 20 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 5 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the due date of the response to notice NTC-9973 from Mira Castell under the response rule?",
  "options": [
   "20 Jul 2026",
   "19 Jul 2026",
   "21 Jul 2026"
  ]
 },
 {
  "qid": "q662f4d4b32",
  "kind": "yes/no",
  "text": "subject: the supplier order\nfile: PO-9616\nrequester: Lena Whitcombe\nnote: kindly hands in this to the desk\n\nPurchase log PO-9616, kept by Lena Whitcombe, vendor Corvane Office:\n- earlier purchase on 21 Dec 2025: 11,814.00 USD\n- earlier purchase on 28 Dec 2025: 1,441.00 USD\n- earlier purchase on 13 Jan 2026: 11,243.00 USD\n- new request on 20 Jan 2026: 12,317.00 USD\nWindow checked: 22 Dec 2025 to 20 Jan 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is 25,000.00 USD as a floor, greater than that counts, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, must the purchase request in log PO-9616 for Lena Whitcombe come with written quotes?"
 },
 {
  "qid": "q3f5f2bc32c",
  "kind": "yes/no",
  "text": "Subject: Routine send on the supplier order\n\nHello intake team,\n\nSending file PO-9013 from Clara Weiss for the usual intake steps. Standard handling is fine.\n\nRegards,\n\nPurchase log PO-9013, kept by Clara Weiss, vendor Corvane Office:\n- earlier purchase on 2026-11-10: $444\n- earlier purchase on 2026-11-14: $1,031\n- new request on 2026-12-09: $1,526\nWindow checked: 2026-11-10 to 2026-12-09, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any sum more than $3,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the request from Clara Weiss, under the purchase rule, call for written quotes in log PO-9013?"
 },
 {
  "qid": "qbce3dff783",
  "kind": "yes/no",
  "text": "Ines Duarte: Sending file NTC-7478 about the notice response to the front desk, enjoy!\ndesk: Oh lovely, thanks a ton.\n\nNotice NTC-7478 to Ines Duarte:\n- response due date: 5 May 2025\n- office cutoff on the due date: 2025-05-05 18:30:00 +0300\n- response sent: 2025-05-04 04:19:00 -0700 [same instant in office time: 2025-05-04 14:19:00 +0300]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Ines Duarte to notice NTC-7478 on time under the receipt rule?"
 },
 {
  "qid": "q54a5da3e2b",
  "kind": "choice",
  "text": "Hi admin team, this is Clara Weiss sharing file CASE-5793 about the appeal deadline. It was a pleasure to pull it together. Thanks for keeping an eye on it.\n\nCase CASE-5793, party Clara Weiss:\n- decision date: 5 Oct 2027\n- delivery date: 3 Oct 2027",
  "question": "Filing rule: the appeal must be filed within 10 days starting from the later of the dates listed below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 10 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the final day on which Clara Weiss can still file the appeal in case CASE-5793 and be in time?",
  "options": [
   "15 Oct 2027",
   "14 Oct 2027",
   "13 Oct 2027"
  ]
 },
 {
  "qid": "q437e46ff19",
  "kind": "choice",
  "text": "Title: file NTC-2842 about the notice response\nRequester: Aiko Brandt\nSent to: admin team\nThanks a lot for the help.\n\nNotice NTC-2842 to Aiko Brandt:\n- notice date: 2028-09-21\n- sent by: post\n- 21 days after the notice date, before any postal add-on or closure: 2028-10-12\nOffice closures: 2028-10-12; 2028-10-14.",
  "question": "Response rule: a response is due 21 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 2 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat, under the response rule, is the due date for the response to notice NTC-2842?",
  "options": [
   "2028-10-16",
   "2028-10-15",
   "2028-10-13"
  ]
 },
 {
  "qid": "qa575fbce9d",
  "kind": "choice",
  "text": "Title | file LED-2245 about the branch cash review\nRequester | Tomas Lindqvist\nTeam | review team, cheers for the review!\n\nCash ledger LED-2245, teller Tomas Lindqvist:\n- 2025-05-16: deposit of $675\n- 2025-05-17: withdrawal of $684\n- 2025-05-17: deposit of $893\n- 2025-05-17: deposit of $1,689\n- 2025-05-17: withdrawal of $1,960\nDay under review: 2025-05-17",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any amount that is more than $3,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, for Tomas Lindqvist on 2025-05-17, which of the day's totals call for a cash report?",
  "options": [
   "Only the deposit total",
   "Both totals",
   "Neither total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q2cf7c49876",
  "kind": "yes/no",
  "text": "[intake] sender=Ana Ruiz file=PO-2280\n[intake] subject=the buying request channel=standard_route\n\nPurchase log PO-2280, kept by Ana Ruiz, vendor Halden Tools:\n- earlier purchase on 5 Feb 2027: $5,969\n- earlier purchase on 14 May 2027: $1,597\n- earlier purchase on 7 Aug 2027: $4,095\n- new request on 11 Aug 2027: $4,309\nWindow checked: 14 May 2027 to 11 Aug 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is $10,000 as a floor, greater than that counts, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request made by Ana Ruiz need written quotes under the purchase rule?"
 },
 {
  "qid": "q76f7654de3",
  "kind": "choice",
  "text": "Yara Haddad: Pleased to forward file STAY-3134 about the residence day count\nclerk: Thank you, leave it with the records team\n\nStay record STAY-3134 for Yara Haddad:\n- entry day Friday, December 3, 2027, exit day Monday, January 17, 2028 (whole stay: 46 days)\n- entry day Thursday, February 3, 2028, exit day Friday, February 4, 2028 (whole stay: 2 days)\n- entry day Tuesday, February 22, 2028, exit day Wednesday, March 8, 2028 (whole stay: 16 days)\nReference date: Sunday, March 19, 2028\nWindow checked: Tuesday, December 21, 2027 to Sunday, March 19, 2028, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 45 days in any 90-day span that moves ahead with each new day. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, how many days present for Yara Haddad fall inside the checked window ending on the reference date in file STAY-3134?",
  "options": [
   "64 days",
   "35 days",
   "46 days"
  ]
 },
 {
  "qid": "q271002d197",
  "kind": "yes/no",
  "text": "{\"file\": \"STAY-5913\", \"sent_by\": \"Kofi Mensah\", \"subject\": \"the visa stay count\", \"note\": \"warm hello to admin\", \"channel\": \"intake\"}\n\nStay record STAY-5913 for Kofi Mensah:\n- entry day Thursday, March 18, 2027, exit day Tuesday, April 20, 2027 (whole stay: 34 days)\n- entry day Sunday, May 16, 2027, exit day Sunday, May 23, 2027 (whole stay: eight days)\nReference date: Saturday, June 12, 2027\nWindow checked: Wednesday, April 14, 2027 to Saturday, June 12, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 21 days in each 60-day window that moves forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Kofi Mensah inside the stay limit when, under the stay rule, the days present in the window ending on Saturday, June 12, 2027 number at most the limit?"
 },
 {
  "qid": "q3c627bc6c5",
  "kind": "choice",
  "text": "Subject: Little catch-up on the notice response\n\nHey review team,\n\nDropping file NTC-8659 off from Priya Raman, hope it lands nicely with you. Enjoy the rest of your stretch.\n\nCheers,\n\nNotice NTC-8659 to Priya Raman:\n- notice date: 16 September 2027\n- sent by: hand delivery\n- 20 days after the notice date, before any postal add-on or closure: 6 October 2027\nOffice closures: none.",
  "question": "Response rule: a response is due 20 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 3 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat, under the response rule, is the due date for the response to notice NTC-8659?",
  "options": [
   "5 October 2027",
   "8 October 2027",
   "6 October 2027"
  ]
 },
 {
  "qid": "q7ddb3f39ca",
  "kind": "choice",
  "text": "team: intake team\nsent_by: Lena Whitcombe\nfile: STAY-3165\nsubject: the border stay check\nnote: respectfully submitted\n\nStay record STAY-3165 for Lena Whitcombe:\n- entry day 2026-07-09, exit day 2026-07-23 (whole stay: fifteen days)\n- entry day 2026-08-03, exit day 2026-09-25 (whole stay: 54 days)\nReference date: 2026-11-23\nWindow checked: 2026-08-26 to 2026-11-23, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 30 days inside every moving 90-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present for Lena Whitcombe fall inside the checked window ending on 2026-11-23?",
  "options": [
   "0 days",
   "31 days",
   "30 days"
  ]
 },
 {
  "qid": "qfdbe437835",
  "kind": "yes/no",
  "text": "Subject: quick pass\nHi review team,\nPriya Raman sent in file PO-5187 about the purchase request. Please give it a fast look and reply.\nThanks,\n\nPurchase log PO-5187, kept by Priya Raman, vendor Vantmoor Electric:\n- earlier purchase on 7 February 2028: $504\n- earlier purchase on 4 March 2028: $2,329\n- earlier purchase on 23 March 2028: $2,007\n- new request on 2 April 2028: $664\nWindow checked: 4 March 2028 to 2 April 2028, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any total greater than $5,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request from Priya Raman in log PO-5187 need written quotes under the purchase rule?"
 }
]
