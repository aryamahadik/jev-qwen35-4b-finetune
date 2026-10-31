# G5-H blind read (all free-form rows) T01-blind_read-98691b6f-005 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g5h/answers/T01-blind_read-98691b6f-005.json

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
  "qid": "qdf9ef9a6e1",
  "kind": "yes/no",
  "text": "Felix Ortega: Quick send of POL-9693 about the insurance claim.\nservice desk: Thanks, that is in.\n\nPolicy POL-9693, holder Felix Ortega:\n- policy start date: 2026-10-11\n- glass breakage cover: part of the base policy\n- glass breakage loss on: 2026-10-14\n- days from the policy start date to the loss: 3 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWould policy POL-9693 cover this glass breakage loss under the cover rule?"
 },
 {
  "qid": "qd7a22106ae",
  "kind": "yes/no",
  "text": "Dear duty clerk,\nOwen Pryce is sending file NTC-9710 about the notice response. The file is attached for your desk. Thanks in advance for your help.\nBest,\n\nNotice NTC-9710 to Owen Pryce:\n- response due date: Sunday, September 17, 2028\n- office cutoff on the due date: 2028-09-17 12:54:00 +0530\n- response sent: 2028-09-17 16:29:00 +0900 [same instant in office time: 2028-09-17 12:59:00 +0530]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the response to notice NTC-9710 given by Owen Pryce on time under the receipt rule?"
 },
 {
  "qid": "q0e518fdd27",
  "kind": "choice",
  "text": "Theo Kalnins: Routine send, NTC-9062 about the response deadline.\nintake team: Received, thank you.\n\nNotice NTC-9062 to Theo Kalnins:\n- notice date: 8 Mar 2027\n- sent by: post\n- 20 days after the notice date, before any postal add-on or closure: 28 Mar 2027\nOffice closures: 28 Mar 2027; 31 Mar 2027.",
  "question": "Response rule: a response is due 20 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 3 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on which date is the response from Theo Kalnins to notice NTC-9062 due under the response rule?",
  "options": [
   "2 Apr 2027",
   "1 Apr 2027",
   "30 Mar 2027"
  ]
 },
 {
  "qid": "qa25bac7d09",
  "kind": "choice",
  "text": "Sent by: Lena Whitcombe\nFile: LED-1907\nSent to: records clerk\nHappy to share the file about the teller ledger review, it was fun to put together. Hope it helps with the sorting.\n\nCash ledger LED-1907, teller Lena Whitcombe:\n- Friday, June 18, 2027: withdrawal of $1,170.00\n- Friday, June 18, 2027: withdrawal of $3,830.00\n- Friday, June 18, 2027: deposit of $4,641.00\n- Friday, June 18, 2027: deposit of $2,073.00\n- Sunday, June 20, 2027: deposit of $1,742.00\nDay under review: Friday, June 18, 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is greater than $5,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nFor Friday, June 18, 2027, which of the day's totals, under the cash rule, call for a cash report?",
  "options": [
   "Neither total",
   "Both totals",
   "Only the withdrawal total",
   "Only the deposit total"
  ]
 },
 {
  "qid": "q9eeafc4dad",
  "kind": "yes/no",
  "text": "Sent by: Clara Weiss\nFile: NTC-2502\nSent to: review team\nThank you for your attention to the file about the response deadline. I remain grateful for the careful reading.\n\nNotice NTC-2502 to Clara Weiss:\n- response due date: Sunday, December 13, 2026\n- office cutoff on the due date: 13 December 2026, 18:10 (UTC-04:00)\n- response sent: 14 December 2026, 03:35 (UTC+05:30) [same instant in office time: 13 December 2026, 18:05 (UTC-04:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the response to notice NTC-2502 late under the receipt rule, counted as received after the due date?"
 },
 {
  "qid": "qa81003ce3f",
  "kind": "choice",
  "text": "Jonas Feld has sent file LED-1504 about the teller ledger review to the admin team. It is a friendly little bundle for the admin desks. Thanks for the lovely teamwork.\n\nCash ledger LED-1504, teller Jonas Feld:\n- 2 February 2028: withdrawal of $3,805.00\n- 4 February 2028: deposit of $6,532.00\n- 4 February 2028: withdrawal of $4,881.00\n- 4 February 2028: withdrawal of $119.00\n- 4 February 2028: deposit of $570.00\n- 5 February 2028: withdrawal of $2,524.00\nDay under review: 4 February 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is $5,000.00 as a floor, greater than that counts, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals on 4 February 2028 in ledger LED-1504, under the cash rule, call for a cash report?",
  "options": [
   "Both totals",
   "Only the withdrawal total",
   "Neither total",
   "Only the deposit total"
  ]
 },
 {
  "qid": "qb6ae02070c",
  "kind": "yes/no",
  "text": "Hana Sato: Hiya! Sending CASE-6275 about the claim deadline question, all good here.\nservice desk: Lovely, thanks for the heads up!\n\nCase CASE-6275, party Hana Sato:\n- inspection date: Thursday, October 8, 2026\n- report date: Thursday, September 24, 2026\n- objection filed on: Thursday, October 29, 2026\n- days from the inspection date to the filing: 21 days\n- days from the report date to the filing: 35 days",
  "question": "Filing rule: the objection must be filed within 28 days past the later of the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the objection in case CASE-6275 filed late, after the deadline?"
 },
 {
  "qid": "q888c147b91",
  "kind": "choice",
  "text": "Theo Kalnins: Hi, here is file CASE-4542 about the claim deadline question, with plenty of cheer.\ndesk: Lovely, thanks so much!\ndesk: That is fun to read.\n\nCase CASE-4542, party Theo Kalnins:\n- inspection date: Monday, March 6, 2028\n- report date: Saturday, February 5, 2028",
  "question": "Filing rule: the objection must be filed inside a span of 28 days that runs after the later of these dates: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the latest day on which Theo Kalnins may still file the objection in time?",
  "options": [
   "Saturday, April 1, 2028",
   "Monday, April 3, 2028",
   "Wednesday, April 5, 2028",
   "Tuesday, April 4, 2028"
  ]
 },
 {
  "qid": "qf62df6f242",
  "kind": "yes/no",
  "text": "Tomas Lindqvist: Quick word, here is file POL-2024 about the insurance claim, I am swamped.\nservice: Thanks, I see it.\ndesk: Great, shared with the team.\n\nPolicy POL-2024, holder Tomas Lindqvist:\n- policy start date: Monday, 5 July 2027\n- glass breakage cover: part of the base policy\n- glass breakage loss on: Saturday, 7 August 2027\n- days from the policy start date to the loss: 33 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 33 days whose clock starts running on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 33 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, is the glass breakage loss for Tomas Lindqvist covered under the cover rule?"
 },
 {
  "qid": "q1e0f76d299",
  "kind": "choice",
  "text": "Dear duty clerk,\nDana Okafor is sending file POL-8252 about the insurance claim. It is attached here. Hope your work goes well.\nCheers,\n\nPolicy POL-8252, holder Dana Okafor:\n- policy start date: 29 November 2027\n- burst pipe damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 47 days that begins on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 47 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which the burst pipe damage loss in policy POL-8252 would be covered under the cover rule?",
  "options": [
   "15 January 2028",
   "16 January 2028",
   "14 January 2028"
  ]
 },
 {
  "qid": "q7982ccaead",
  "kind": "choice",
  "text": "Felix Ortega: Hey, sending case file POL-9991 about the insurance claim, hope it brightens the room.\ndesk: That is a lovely note, thanks!\ndesk: Good fun, I enjoyed reading it.\n\nPolicy POL-9991, holder Felix Ortega:\n- policy start date: 31 July 2027\n- fire damage cover: added by a rider effective 3 January 2028",
  "question": "Cover rule: a loss is covered only after a waiting period of 34 days that begins on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 34 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the earliest date on which the fire damage loss for Felix Ortega would be covered?",
  "options": [
   "7 February 2028",
   "4 September 2027",
   "5 February 2028"
  ]
 },
 {
  "qid": "qd239f11854",
  "kind": "choice",
  "text": "File: CASE-4152\nSubject: the claim deadline question\nSent by: Iris Vance\nHey there, this goes over to the records clerk. Hope everything is going nicely for you!\n\nCase CASE-4152, party Iris Vance:\n- inspection date: 31 Oct 2025\n- report date: 30 Oct 2025",
  "question": "Filing rule: the objection must be filed within ten days running from the later of the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is ten days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, by which final day must the objection be filed to still count as in time?",
  "options": [
   "12 Nov 2025",
   "11 Nov 2025",
   "10 Nov 2025"
  ]
 },
 {
  "qid": "q802afb5a2a",
  "kind": "choice",
  "text": "From: Paolo Greco\nFile: LED-6126\nSent to: records clerk\nThis file about the teller ledger review is sent over in a hurry. Thanks.\n\nCash ledger LED-6126, teller Paolo Greco:\n- Saturday, 19 February 2028: withdrawal of $1,683.00\n- Saturday, 19 February 2028: deposit of $5,000.00\n- Saturday, 19 February 2028: withdrawal of $569.00\n- Sunday, 20 February 2028: withdrawal of $2,451.00\nDay under review: Saturday, 19 February 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is strictly more than $5,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, which of the day's totals in ledger LED-6126, if any, call for a cash report under the cash rule?",
  "options": [
   "Both totals",
   "Only the withdrawal total",
   "Only the deposit total",
   "Neither total"
  ]
 },
 {
  "qid": "q3f32baefec",
  "kind": "choice",
  "text": "Felix Ortega: hi! Here is CASE-8280 about the appeal deadline.\nhelp desk: lovely, received.\nhelp desk: great, enjoy your work.\n\nCase CASE-8280, party Felix Ortega:\n- decision date: 10 May 2026\n- delivery date: 26 Apr 2026",
  "question": "Filing rule: the appeal must be filed inside 28 days that elapses after whichever of the dates below is later: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, by which final day must the appeal be filed to still count as in time?",
  "options": [
   "24 May 2026",
   "6 Jun 2026",
   "5 Jun 2026",
   "7 Jun 2026"
  ]
 },
 {
  "qid": "q38c389dd3c",
  "kind": "choice",
  "text": "Kofi Mensah: Greetings, I am sending file CASE-1226 about the complaint filing for your kind attention.\ncase team: Thank you very much, it has been received.\n\nCase CASE-1226, party Kofi Mensah:\n- incident date: Wednesday, September 17, 2025\n- discovery date: Thursday, September 18, 2025",
  "question": "Filing rule: the complaint must be filed within 31 days past the later of the dates below: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 31 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the final day on which Kofi Mensah can still file the complaint in time for case CASE-1226?",
  "options": [
   "Sunday, October 19, 2025",
   "Friday, October 31, 2025",
   "Monday, October 20, 2025"
  ]
 },
 {
  "qid": "q7b96b68cd0",
  "kind": "yes/no",
  "text": "File: POL-4121\nSubject: the insurance claim\nSent by: Kofi Mensah\nHey there, this goes over to the records clerk. Hope everything is going nicely for you!\n\nPolicy POL-4121, holder Kofi Mensah:\n- policy start date: 2027-07-01\n- burst pipe damage cover: part of the base policy\n- burst pipe damage loss on: 2027-07-11\n- days from the policy start date to the loss: 10 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 10 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 10 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is the burst pipe damage loss covered under the cover rule?"
 },
 {
  "qid": "q7b81bb7b1f",
  "kind": "yes/no",
  "text": "Freya Holm: file PO-2372 about the purchase request is attached here.\ncase team: thank you, that is received.\ncase team: kind regards.\n\nPurchase log PO-2372, kept by Freya Holm, vendor Brightwell Supply:\n- earlier purchase on Wednesday, August 20, 2025: $6,603.00\n- new request on Saturday, November 29, 2025: $3,398.00\nWindow checked: Saturday, August 2, 2025 to Saturday, November 29, 2025, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 120-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is a figure greater than $10,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request from Freya Holm in log PO-2372 need written quotes under the purchase rule?"
 },
 {
  "qid": "q975a5e936d",
  "kind": "yes/no",
  "text": "Tomas Lindqvist: Quick word, here is file POL-2024 about the insurance claim, I am swamped.\nservice: Thanks, I see it.\ndesk: Great, shared with the team.\n\nPolicy POL-2024, holder Tomas Lindqvist:\n- policy start date: Monday, 5 July 2027\n- glass breakage cover: part of the base policy\n- glass breakage loss on: Saturday, 7 August 2027\n- days from the policy start date to the loss: 33 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days whose clock starts running on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the cover rule does not pay for the glass breakage loss on policy POL-2024?"
 },
 {
  "qid": "qcd92e584f3",
  "kind": "yes/no",
  "text": "Theo Kalnins: Hi, here is file CASE-3607 about the appeal deadline, with plenty of cheer.\ndesk: Lovely, thanks so much!\ndesk: That is fun to read.\n\nCase CASE-3607, party Theo Kalnins:\n- billing date: December 18, 2027\n- statement date: November 18, 2027\n- dispute filed on: January 18, 2028\n- days from the billing date to the filing: 31 days\n- days from the statement date to the filing: 61 days",
  "question": "Filing rule: the dispute must be filed within 31 days following the later of these dates: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 31 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the dispute from Theo Kalnins in case CASE-3607 filed on or before the final day of the filing period?"
 },
 {
  "qid": "q3d1fb9a7a9",
  "kind": "yes/no",
  "text": "Dear front desk,\nRavi Anand respectfully sends file STAY-5422 about the border stay check. My thanks go to you for looking at this. The file is in full and in good shape.\nYours sincerely\n\nStay record STAY-5422 for Ravi Anand:\n- entry day July 16, 2025, exit day July 26, 2025 (whole stay: eleven days)\n- entry day September 19, 2025, exit day October 18, 2025 (whole stay: 30 days)\nReference date: November 13, 2025\nWindow checked: August 16, 2025 to November 13, 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 45 days in any 90-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Ravi Anand over the stay limit when days present inside the window ending on the reference date number more than the limit, under the stay rule?"
 },
 {
  "qid": "q92931ab742",
  "kind": "yes/no",
  "text": "Ines Duarte: Hey there! Sending file STAY-3133 about the visa stay count your way, hope it helps lol.\nservice: Thanks so much, that is great.\ndesk: Awesome, we have it on screen.\n\nStay record STAY-3133 for Ines Duarte:\n- entry day 2027-05-03, exit day 2027-05-10 (whole stay: eight days)\n- entry day 2027-05-12, exit day 2027-07-26 (whole stay: 76 days)\nReference date: 2027-09-18\nWindow checked: 2027-05-22 to 2027-09-18, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 60 days inside every 120-day stretch that moves along. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is the person in file STAY-3133 over the stay limit, counting days present in the checked window ending on 2027-09-18?"
 },
 {
  "qid": "q694e655d51",
  "kind": "choice",
  "text": "Iris Vance is sending file CASE-5131 about the claim deadline question to the admin team. It goes out in a hurry, with the attached pages in place. Thanks in advance.\n\nCase CASE-5131, party Iris Vance:\n- inspection date: Monday, 18 August 2025\n- report date: Saturday, 19 July 2025",
  "question": "Filing rule: the objection must be filed within 45 days counted forward from the later among these dates: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the latest date by which the objection can be filed in time?",
  "options": [
   "Friday, 3 October 2025",
   "Monday, 20 October 2025",
   "Saturday, 4 October 2025",
   "Thursday, 2 October 2025"
  ]
 },
 {
  "qid": "q8616acb44a",
  "kind": "choice",
  "text": "Bruno Lacerda is sending file CASE-2912 about the appeal deadline to the admin team. It goes out fast, so the file sits near the top of the pile. Thanks for handling it.\n\nCase CASE-2912, party Bruno Lacerda:\n- decision date: 3 August 2027\n- delivery date: 24 July 2027",
  "question": "Filing rule: the appeal must be filed inside 21 days counted from the later of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, what is the latest date on which the appeal can be filed in time?",
  "options": [
   "25 August 2027",
   "1 September 2027",
   "24 August 2027",
   "26 August 2027"
  ]
 },
 {
  "qid": "q292dd31d94",
  "kind": "yes/no",
  "text": "Omar Saleh: Quick send, PO-8406 about the supplier order.\nhelp desk: Got it.\n\nPurchase log PO-8406, kept by Omar Saleh, vendor Quillon Labs:\n- earlier purchase on 2026-06-15: 890.00 USD\n- earlier purchase on 2026-06-29: 560.00 USD\n- new request on 2026-07-13: 1,088.00 USD\nWindow checked: 2026-06-14 to 2026-07-13, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is 3,000.00 USD itself excluded, only more than that counts, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, must the request from Omar Saleh be backed by written quotes under the purchase rule?"
 },
 {
  "qid": "q8dc07882b7",
  "kind": "choice",
  "text": "Jonas Feld has sent file LED-1504 about the teller ledger review to the admin team. It is a friendly little bundle for the admin desks. Thanks for the lovely teamwork.\n\nCash ledger LED-1504, teller Jonas Feld:\n- 2 February 2028: withdrawal of $3,805.00\n- 4 February 2028: deposit of $6,532.00\n- 4 February 2028: withdrawal of $6,699.00\n- 4 February 2028: withdrawal of $119.00\n- 4 February 2028: deposit of $570.00\n- 5 February 2028: withdrawal of $2,524.00\nDay under review: 4 February 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is $5,000.00 as a floor, greater than that counts, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals on 4 February 2028 in ledger LED-1504, under the cash rule, call for a cash report?",
  "options": [
   "Both totals",
   "Only the withdrawal total",
   "Neither total",
   "Only the deposit total"
  ]
 },
 {
  "qid": "qa1f5dcea52",
  "kind": "choice",
  "text": "Eva Marsh: Hello, I am sending file LED-8525 about the cash ledger check to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nCash ledger LED-8525, teller Eva Marsh:\n- Monday, August 24, 2026: withdrawal of $3,568.00\n- Tuesday, August 25, 2026: deposit of $920.00\n- Tuesday, August 25, 2026: withdrawal of $219.00\n- Tuesday, August 25, 2026: deposit of $2,921.00\n- Tuesday, August 25, 2026: withdrawal of $2,977.00\n- Thursday, August 27, 2026: deposit of $3,236.00\nDay under review: Tuesday, August 25, 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any total of $5,000.00 or greater, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, which of the day's totals for Tuesday, August 25, 2026 call for a cash report?",
  "options": [
   "Only the deposit total",
   "Only the withdrawal total",
   "Both totals",
   "Neither total"
  ]
 },
 {
  "qid": "q266bc0a1f9",
  "kind": "choice",
  "text": "Hana Sato sends file NTC-4740 about the response deadline to the desk. The file is set out in full with the usual headings. Thank you for your attention to this matter.\n\nNotice NTC-4740 to Hana Sato:\n- notice date: Monday, October 6, 2025\n- sent by: post\n- fourteen days after the notice date, before any postal add-on or closure: Monday, October 20, 2025\nOffice closures: Saturday, October 25, 2025; Sunday, October 26, 2025.",
  "question": "Response rule: a response is due fourteen days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add five days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, on what date is the response from Hana Sato due under the response rule?",
  "options": [
   "Monday, October 27, 2025",
   "Friday, October 24, 2025"
  ]
 },
 {
  "qid": "qa0bfca0546",
  "kind": "choice",
  "text": "Felix Ortega: hi! Here is CASE-8280 about the appeal deadline.\nhelp desk: lovely, received.\nhelp desk: great, enjoy your work.\n\nCase CASE-8280, party Felix Ortega:\n- decision date: 10 May 2026\n- delivery date: 26 Apr 2026",
  "question": "Filing rule: the appeal must be filed inside 24 days that elapses after whichever of the dates below is later: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 24 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, by which final day must the appeal be filed to still count as in time?",
  "options": [
   "2 Jun 2026",
   "1 Jun 2026",
   "20 May 2026",
   "3 Jun 2026"
  ]
 },
 {
  "qid": "qd7a19e623c",
  "kind": "choice",
  "text": "Lucas Brenner is sending file LED-8708 about the teller ledger review to the admin team. It goes out fast, so the file sits near the top of the pile. Thanks for handling it.\n\nCash ledger LED-8708, teller Lucas Brenner:\n- 22 Jul 2026: withdrawal of $1,323\n- 22 Jul 2026: deposit of $1,088\n- 22 Jul 2026: deposit of $653\n- 24 Jul 2026: deposit of $1,531\nDay under review: 22 Jul 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is strictly more than $3,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, which of the day's totals recorded by Lucas Brenner for 22 Jul 2026 call for a cash report?",
  "options": [
   "Neither total",
   "Only the deposit total",
   "Both totals",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "qdbe2435cf3",
  "kind": "choice",
  "text": "Hi front desk,\nInes Duarte sends file CASE-9404 about the claim deadline question in the usual form. The file sits in the standard layout alongside the other sheets.\nRegards,\n\nCase CASE-9404, party Ines Duarte:\n- invoice date: April 8, 2026\n- goods received date: April 7, 2026",
  "question": "Filing rule: the claim must be filed inside a span of 21 days that runs after the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the final day on which Ines Duarte can still file the claim in time for case CASE-9404?",
  "options": [
   "April 29, 2026",
   "April 28, 2026",
   "April 27, 2026"
  ]
 },
 {
  "qid": "qf77a2b0694",
  "kind": "yes/no",
  "text": "Yara Haddad: Hello. I am forwarding file STAY-2376 about the residence day count. My thanks for your help.\ncase team: Thank you, the file has been received.\n\nStay record STAY-2376 for Yara Haddad:\n- entry day September 19, 2026, exit day November 4, 2026 (whole stay: 47 days)\nReference date: November 28, 2026\nWindow checked: August 31, 2026 to November 28, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 45 days in any rolling 90-day window. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does Yara Haddad have more days present in the checked window ending on November 28, 2026 than the stay limit?"
 },
 {
  "qid": "q13bfd35595",
  "kind": "choice",
  "text": "Yara Haddad: file CASE-4276 about the claim deadline question is here.\nintake team: received, thanks.\nintake team: that is everything for this file.\n\nCase CASE-4276, party Yara Haddad:\n- invoice date: Sunday, 25 January 2026\n- goods received date: Friday, 30 January 2026",
  "question": "Filing rule: the claim must be filed within 28 days starting from the later of the dates listed below: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the latest date by which the claim can be filed in time?",
  "options": [
   "Wednesday, 11 March 2026",
   "Friday, 27 February 2026",
   "Saturday, 28 February 2026",
   "Sunday, 1 March 2026"
  ]
 },
 {
  "qid": "q4bc17afdb2",
  "kind": "choice",
  "text": "Dear front desk,\nDana Okafor is sending file STAY-6924 about the residence day count. The file is attached here for your records. I appreciate the help with it.\nKind regards,\n\nStay record STAY-6924 for Dana Okafor:\n- entry day November 4, 2025, exit day November 14, 2025 (whole stay: 11 days)\n- entry day December 14, 2025, exit day January 7, 2026 (whole stay: 25 days)\nReference date: January 31, 2026\nWindow checked: October 4, 2025 to January 31, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days during any 120-day window that moves ahead. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, how many days present for Dana Okafor fall inside the checked window ending on the reference date?",
  "options": [
   "36 days",
   "38 days"
  ]
 },
 {
  "qid": "qd2f29b1534",
  "kind": "choice",
  "text": "Sent by: Hana Sato\nFile: STAY-7060\nSent to: records clerk\nLovely to send this over, it is about the residence day count. The notes are all tidy and sit nicely for the records team.\n\nStay record STAY-7060 for Hana Sato:\n- entry day 13 November 2026, exit day 4 January 2027 (whole stay: 53 days)\n- entry day 11 February 2027, exit day 3 March 2027 (whole stay: 21 days)\nReference date: 7 April 2027\nWindow checked: 9 December 2026 to 7 April 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days in each 120-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, how many days present for Hana Sato fall inside the checked window that ends on the reference date?",
  "options": [
   "48 days",
   "46 days",
   "49 days"
  ]
 },
 {
  "qid": "q21036fed6a",
  "kind": "yes/no",
  "text": "Hiya admin team, Ines Duarte has sent file STAY-6225 about the border stay check. Hope you are all well and enjoying the work. This is just a simple pass along with every bit in place. Thanks a bunch for taking it in, lovely to share this with you.\n\nStay record STAY-6225 for Ines Duarte:\n- entry day 27 May 2027, exit day 10 July 2027 (whole stay: 45 days)\nReference date: 24 August 2027\nWindow checked: 27 May 2027 to 24 August 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 45 days in every 90-day run that moves forward through time. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does Ines Duarte have more days present in the checked window ending on 24 August 2027 than the stay limit?"
 },
 {
  "qid": "q581399785d",
  "kind": "yes/no",
  "text": "Tomas Lindqvist: Dear team, I am forwarding file POL-5670 about the insurance claim to the intake team.\nintake: Thank you for passing it along.\nteam: With thanks for your courtesy.\n\nPolicy POL-5670, holder Tomas Lindqvist:\n- policy start date: Saturday, 23 October 2027\n- burst pipe damage cover: added by a rider effective Friday, 5 May 2028\n- burst pipe damage loss on: Monday, 5 June 2028\n- days from the policy start date to the loss: 226 days\n- days from the rider effective date to the loss: 31 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days commencing on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does the cover rule count the loss on policy POL-5670 as covered?"
 },
 {
  "qid": "qae6bbb6da7",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nAiko Brandt here with file POL-7590 about the insurance claim, and I am so glad it all came together. Hope it makes your work a little easier.\nCheers,\n\nPolicy POL-7590, holder Aiko Brandt:\n- policy start date: 21 June 2027\n- flood damage cover: part of the base policy\n- flood damage loss on: 2 July 2027\n- days from the policy start date to the loss: 11 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 10 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 10 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the flood damage loss on policy POL-7590 covered under the cover rule?"
 },
 {
  "qid": "qe1e3c38488",
  "kind": "choice",
  "text": "Ravi Anand sends file CASE-3434 about the claim deadline question to the desk. The file keeps to the standard format. A full copy sits with the desk too.\n\nCase CASE-3434, party Ravi Anand:\n- inspection date: 2026-11-07\n- report date: 2026-10-31",
  "question": "Filing rule: the objection must be filed within 14 days running from the later of the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 14 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, by which final day must the objection be filed to still count as in time?",
  "options": [
   "2026-11-19",
   "2026-11-21",
   "2026-11-14",
   "2026-11-20"
  ]
 },
 {
  "qid": "q1bd10da7e5",
  "kind": "yes/no",
  "text": "Dear front desk,\nI am writing to share file PO-6112 about the purchase request, sent by Hana Sato. Thank you for reading this message. The file is in full and in good shape. With respect and thanks.\nYours faithfully\n\nPurchase log PO-6112, kept by Hana Sato, vendor Ostrava Parts:\n- earlier purchase on 20 Feb 2027: $2,968\n- earlier purchase on 21 Apr 2027: $3,654\n- new request on 12 May 2027: $1,345\nWindow checked: 13 Apr 2027 to 12 May 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is $5,000 or greater, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, may request PO-6112 go ahead without written quotes under the purchase rule?"
 },
 {
  "qid": "q61474250eb",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nHope you are doing great! Felix Ortega has sent file NTC-4741 about the response deadline, all lovely and tidy. Just wanted to pop it in your inbox. Catch you round.\nCheers\n\nNotice NTC-4741 to Felix Ortega:\n- response due date: 19 April 2027\n- office cutoff on the due date: 2027-04-19T17:00:00-04:00\n- response sent: 2027-04-20T13:24:00+01:00 [same instant in office time: 2027-04-20T08:24:00-04:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Felix Ortega received on time under the receipt rule?"
 },
 {
  "qid": "q9f882c6039",
  "kind": "yes/no",
  "text": "Ana Ruiz: Quick send, NTC-9361 about the response deadline.\nhelp desk: Got it.\n\nNotice NTC-9361 to Ana Ruiz:\n- response due date: 2027-06-20\n- office cutoff on the due date: 20 June 2027, 14:36 (UTC+01:00)\n- response sent: 2027-06-20T13:36:00Z [same instant in office time: 20 June 2027, 14:36 (UTC+01:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Ana Ruiz to notice NTC-9361 on time under the receipt rule?"
 },
 {
  "qid": "q39a5c1e746",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nYara Haddad here with file NTC-6951 about the notice response, and I am so glad it all came together. Hope it makes your work a little easier.\nCheers,\n\nNotice NTC-6951 to Yara Haddad:\n- response due date: 13 April 2028\n- office cutoff on the due date: 13 April 2028, 22:25 (UTC+03:00)\n- response sent: 13 April 2028, 13:18 (UTC-04:00) [same instant in office time: 13 April 2028, 20:18 (UTC+03:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Yara Haddad to notice NTC-6951, under the receipt rule, counted as received on time?"
 },
 {
  "qid": "q168c7e87a4",
  "kind": "choice",
  "text": "Clara Weiss: Respectfully, I am passing file PO-4562 about the supplier order to the case team.\nteam: Thank you for the note.\nteam: The care shown is much appreciated.\n\nPurchase log PO-4562, kept by Clara Weiss, vendor Ostrava Parts:\n- earlier purchase on March 29, 2026: $2,924\n- earlier purchase on March 31, 2026: $834\n- earlier purchase on April 14, 2026: $284\n- earlier purchase on April 25, 2026: $1,433\n- earlier purchase on June 29, 2026: $521\n- new request on August 11, 2026: $2,323\nWindow checked: April 14, 2026 to August 11, 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 120-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is greater than $5,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, which running total for Clara Weiss gets compared with the threshold when this new request is counted in it?",
  "options": [
   "$4,561",
   "$8,319",
   "$6,884"
  ]
 },
 {
  "qid": "q01e1046944",
  "kind": "yes/no",
  "text": "Nadia Kowal: file PO-9303 about the supplier order is attached here.\ncase team: thank you, that is received.\ncase team: that is all for this file.\n\nPurchase log PO-9303, kept by Nadia Kowal, vendor Ostrava Parts:\n- earlier purchase on Friday, May 7, 2027: $4,324\n- earlier purchase on Tuesday, May 18, 2027: $5,604\n- earlier purchase on Wednesday, June 2, 2027: $10,443\n- new request on Wednesday, June 16, 2027: $8,954\nWindow checked: Tuesday, May 18, 2027 to Wednesday, June 16, 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is anything strictly greater than $25,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does request PO-9303 from Nadia Kowal need written quotes under the purchase rule?"
 },
 {
  "qid": "q2a61ab4ba0",
  "kind": "yes/no",
  "text": "Omar Saleh: Sending CASE-1227 about the complaint filing, a routine send.\nintake team: Received, thanks.\n\nCase CASE-1227, party Omar Saleh:\n- purchase date: Monday, 22 March 2027\n- handover date: Friday, 19 March 2027\n- refund request filed on: Sunday, 6 June 2027\n- days from the purchase date to the filing: 76 days\n- days from the handover date to the filing: 79 days",
  "question": "Filing rule: the refund request must be filed inside 45 days reckoned from the date that falls later among the dates below: the purchase date and the handover date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the refund request from Omar Saleh in case CASE-1227 filed on or before the final day of the filing period?"
 },
 {
  "qid": "qafce413d5b",
  "kind": "choice",
  "text": "Sender: Nadia Kowal\nFile: POL-3778\nTo: records clerk\nThe file about the cover question is attached. Sending it on in a hurry.\n\nPolicy POL-3778, holder Nadia Kowal:\n- policy start date: 2027-08-18\n- flood damage cover: added by a rider effective 2027-12-17",
  "question": "Cover rule: a loss is covered only after a waiting period of 10 days whose first counted day falls on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 10 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the earliest date on which a loss of this kind would be covered under policy POL-3778?",
  "options": [
   "2027-12-28",
   "2027-12-27",
   "2027-08-29",
   "2027-12-26"
  ]
 },
 {
  "qid": "q4a8f829ef6",
  "kind": "choice",
  "text": "Hi front desk,\nBruno Lacerda is sending file NTC-4934 about the response deadline as routine correspondence. The file follows the standard layout. That is the full picture.\nRegards,\n\nNotice NTC-4934 to Bruno Lacerda:\n- response due date: Wednesday, June 23, 2027\n- office cutoff on the due date: 23 June 2027, 18:51 (UTC-05:00)\n- response sent: 21 June 2027, 08:56 (UTC+09:00) [same instant in office time: 20 June 2027, 18:56 (UTC-05:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on which date does the office count the response from Bruno Lacerda to notice NTC-4934 as received under the receipt rule?",
  "options": [
   "2027-06-21",
   "2027-06-20"
  ]
 },
 {
  "qid": "q94f619baa1",
  "kind": "choice",
  "text": "Sent by: Lena Whitcombe\nFile: LED-1907\nSent to: records clerk\nHappy to share the file about the teller ledger review, it was fun to put together. Hope it helps with the sorting.\n\nCash ledger LED-1907, teller Lena Whitcombe:\n- Friday, June 18, 2027: withdrawal of $1,170.00\n- Friday, June 18, 2027: withdrawal of $3,831.00\n- Friday, June 18, 2027: deposit of $4,641.00\n- Friday, June 18, 2027: deposit of $2,073.00\n- Sunday, June 20, 2027: deposit of $1,742.00\nDay under review: Friday, June 18, 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is greater than $5,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nFor Friday, June 18, 2027, which of the day's totals, under the cash rule, call for a cash report?",
  "options": [
   "Neither total",
   "Both totals",
   "Only the withdrawal total",
   "Only the deposit total"
  ]
 },
 {
  "qid": "q732be5cc79",
  "kind": "yes/no",
  "text": "Hana Sato: Hiya! Sending CASE-6275 about the claim deadline question, all good here.\nservice desk: Lovely, thanks for the heads up!\n\nCase CASE-6275, party Hana Sato:\n- inspection date: Thursday, October 8, 2026\n- report date: Thursday, September 24, 2026\n- objection filed on: Thursday, October 29, 2026\n- days from the inspection date to the filing: 21 days\n- days from the report date to the filing: 35 days",
  "question": "Filing rule: the objection must be filed within 28 days past the later of the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the objection from Hana Sato in case CASE-6275 filed on or before the final day of the filing period?"
 },
 {
  "qid": "qb2e0990c9c",
  "kind": "yes/no",
  "text": "From: Paolo Greco\nFile: POL-7349\nSent to: records clerk\nHi there, here is the file about the insurance claim. Hope all is well with you!\n\nPolicy POL-7349, holder Paolo Greco:\n- policy start date: June 10, 2027\n- flood damage cover: added by a rider effective August 6, 2027\n- flood damage loss on: September 21, 2027\n- days from the policy start date to the loss: 103 days\n- days from the rider effective date to the loss: 46 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days that starts on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the loss on policy POL-7349 covered under the cover rule?"
 }
]
