# G5-H blind read (all free-form rows) T01-blind_read-98691b6f-001 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g5h/answers/T01-blind_read-98691b6f-001.json

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
  "qid": "q4d9f33ced5",
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
  "qid": "q3f248ebc4a",
  "kind": "choice",
  "text": "Sent by: Dana Okafor\nFile: CASE-4236\nSent to: records clerk\nShort note, my queue is packed. The file is about the appeal deadline and is attached.\n\nCase CASE-4236, party Dana Okafor:\n- decision date: 16 Oct 2026\n- delivery date: 18 Oct 2026",
  "question": "Filing rule: the appeal must be filed within fourteen days after the later date out of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is fourteen days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the latest day on which Dana Okafor may still file the appeal in time?",
  "options": [
   "5 Nov 2026",
   "3 Nov 2026",
   "1 Nov 2026"
  ]
 },
 {
  "qid": "q0b26c72c7e",
  "kind": "yes/no",
  "text": "Dear front desk,\nPaolo Greco is sending file PO-3559 about the purchase request. The file is attached here for your records. I appreciate the help with it.\nKind regards,\n\nPurchase log PO-3559, kept by Paolo Greco, vendor Vantmoor Electric:\n- earlier purchase on Monday, 12 January 2026: $1,417.00\n- earlier purchase on Tuesday, 3 February 2026: $1,360.00\n- earlier purchase on Saturday, 21 February 2026: $1,430.00\n- new request on Friday, 13 March 2026: $2,210.00\nWindow checked: Tuesday, 13 January 2026 to Friday, 13 March 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is anything strictly greater than $5,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request made by Paolo Greco need written quotes under the purchase rule?"
 },
 {
  "qid": "qb543818293",
  "kind": "yes/no",
  "text": "Priya Raman has sent file CASE-4654 about the claim deadline question to the desk. This is a routine item and the file is attached in full. The desk is copied for completeness. This memo concerns only the sending of the file.\n\nCase CASE-4654, party Priya Raman:\n- invoice date: 2026-06-19\n- goods received date: 2026-07-10\n- claim filed on: 2026-07-31\n- days from the invoice date to the filing: 42 days\n- days from the goods received date to the filing: 21 days",
  "question": "Filing rule: the claim must be filed inside 21 days that elapses after whichever of the dates below is later: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Priya Raman, under the filing rule, file the claim on or before the final day?"
 },
 {
  "qid": "qd1f922d356",
  "kind": "choice",
  "text": "Hey there, quick heads up that Bruno Lacerda has sent file NTC-4881 about the notice response to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.\n\nNotice NTC-4881 to Bruno Lacerda:\n- notice date: 2 July 2025\n- sent by: post\n- 28 days after the notice date, before any postal add-on or closure: 30 July 2025\nOffice closures: 21 July 2025; 30 July 2025; 4 August 2025.",
  "question": "Response rule: a response is due 28 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add five days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn which date is the response from Bruno Lacerda to the notice due under the response rule?",
  "options": [
   "5 August 2025",
   "31 July 2025",
   "3 August 2025"
  ]
 },
 {
  "qid": "qeda8a10b18",
  "kind": "yes/no",
  "text": "Dear front desk,\nThis is Paolo Greco writing to share file STAY-7819 about the visa stay count. The file is attached here. I hope this finds you well.\nKind regards,\n\nStay record STAY-7819 for Paolo Greco:\n- entry day Wednesday, July 22, 2026, exit day Saturday, July 25, 2026 (whole stay: 4 days)\n- entry day Friday, August 14, 2026, exit day Saturday, October 10, 2026 (whole stay: 58 days)\nReference date: Friday, December 11, 2026\nWindow checked: Friday, August 14, 2026 to Friday, December 11, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days inside any moving 120-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Paolo Greco, under the stay rule, over the stay limit for the window ending on Friday, December 11, 2026?"
 },
 {
  "qid": "q04775af4bc",
  "kind": "yes/no",
  "text": "Dear duty clerk,\nLena Whitcombe is sending file POL-9412 about the loss claim. It is attached here. Hope your work goes well.\nCheers,\n\nPolicy POL-9412, holder Lena Whitcombe:\n- policy start date: 2027-04-08\n- burst pipe damage cover: part of the base policy\n- burst pipe damage loss on: 2027-06-05\n- days from the policy start date to the loss: 58 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days that opens on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, did the loss on policy POL-9412 happen during the waiting period?"
 },
 {
  "qid": "qd31391dd74",
  "kind": "choice",
  "text": "Hi duty clerk,\nTheo Kalnins is sending file STAY-5242 about the residence day count, with the main points at the top. Quick note, I am buried under other work.\nBest,\n\nStay record STAY-5242 for Theo Kalnins:\n- entry day August 10, 2026, exit day August 27, 2026 (whole stay: eighteen days)\n- entry day September 18, 2026, exit day October 13, 2026 (whole stay: 26 days)\n- entry day December 3, 2026, exit day December 16, 2026 (whole stay: fourteen days)\nReference date: January 15, 2027\nWindow checked: September 18, 2026 to January 15, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 60 days inside every 120-day stretch that moves along. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, how many days present for file STAY-5242 fall inside the checked window that ends on the reference date?",
  "options": [
   "58 days",
   "40 days",
   "42 days"
  ]
 },
 {
  "qid": "q938d4dc271",
  "kind": "choice",
  "text": "Dear front desk,\nThis is Aiko Brandt writing to share file CASE-9370 about the complaint filing. The file is attached here. I hope this finds you well.\nKind regards,\n\nCase CASE-9370, party Aiko Brandt:\n- purchase date: 2025-10-17\n- handover date: 2025-10-18",
  "question": "Filing rule: the refund request must be filed inside 60 days that elapses after whichever of the dates below is later: the purchase date and the handover date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the latest date by which the refund request can be filed in time?",
  "options": [
   "2025-12-16",
   "2026-01-09",
   "2025-12-17"
  ]
 },
 {
  "qid": "q6e44afa01e",
  "kind": "yes/no",
  "text": "Ana Ruiz: file CASE-6831 about the complaint filing is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.\n\nCase CASE-6831, party Ana Ruiz:\n- incident date: Tuesday, 14 September 2027\n- discovery date: Sunday, 29 August 2027\n- complaint filed on: Monday, 20 September 2027\n- days from the incident date to the filing: 6 days\n- days from the discovery date to the filing: 22 days",
  "question": "Filing rule: the complaint must be filed within 14 days from whichever is later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 14 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the complaint filed on or before the final day of the filing period?"
 },
 {
  "qid": "q3a5f98a6e7",
  "kind": "yes/no",
  "text": "Sent by: Dana Okafor\nFile: STAY-9007\nSent to: review team\nThank you for your attention to the file about the border stay check. I remain grateful for the careful reading.\n\nStay record STAY-9007 for Dana Okafor:\n- entry day 17 May 2026, exit day 1 June 2026 (whole stay: 16 days)\nReference date: 15 June 2026\nWindow checked: 17 May 2026 to 15 June 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 14 days within any 30-day window that keeps moving. Day counts are calendar days, and entry and exit days both count as days present. Only one 30-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 14 days, and within the limit if it is 14 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Dana Okafor, under the stay rule, over the stay limit for the window ending on 15 June 2026?"
 },
 {
  "qid": "q86e83ca014",
  "kind": "yes/no",
  "text": "Dear front desk team,\n\nMy name is Ines Duarte, and I am writing to send file CASE-6095 about the claim deadline question.\n\nThe file is attached below. Thank you for your help with this matter.\n\nKind regards,\n\nCase CASE-6095, party Ines Duarte:\n- inspection date: June 12, 2026\n- report date: July 12, 2026\n- objection filed on: July 26, 2026\n- days from the inspection date to the filing: 44 days\n- days from the report date to the filing: 14 days",
  "question": "Filing rule: the objection must be filed inside 14 days extending past the later of these dates: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 14 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the objection filed too late, after the final day of the filing period?"
 },
 {
  "qid": "qa6a1b1166b",
  "kind": "yes/no",
  "text": "Sent by: Clara Weiss\nFile: STAY-1237\nSent to: review team\nThe file is a routine copy about the residence day count. It follows the standard layout used by the team.\n\nStay record STAY-1237 for Clara Weiss:\n- entry day September 24, 2025, exit day October 9, 2025 (whole stay: 16 days)\n- entry day October 28, 2025, exit day December 10, 2025 (whole stay: 44 days)\nReference date: January 6, 2026\nWindow checked: September 9, 2025 to January 6, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 60 days inside every 120-day stretch that moves along. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does file STAY-1237 show more days present in the checked window ending on the reference date than the limit?"
 },
 {
  "qid": "qd60696f3d6",
  "kind": "yes/no",
  "text": "Hey there, quick heads up that Kofi Mensah has sent file NTC-2210 about the response deadline to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.\n\nNotice NTC-2210 to Kofi Mensah:\n- response due date: Monday, 22 June 2026\n- office cutoff on the due date: 22 June 2026, 19:43 (UTC-05:00)\n- response sent: 23 June 2026, 09:48 (UTC+09:00) [same instant in office time: 22 June 2026, 19:48 (UTC-05:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the response to notice NTC-2210 on time under the receipt rule?"
 },
 {
  "qid": "q57b54ed6f6",
  "kind": "yes/no",
  "text": "Sent by: Bruno Lacerda\nFile code: NTC-9540\nFor: review team\nThe file about the response deadline is passed along as usual.\n\nNotice NTC-9540 to Bruno Lacerda:\n- response due date: 23 April 2026\n- office cutoff on the due date: 23 April 2026, 17:37 (UTC+01:00)\n- response sent: 23 April 2026, 09:38 (UTC-07:00) [same instant in office time: 23 April 2026, 17:38 (UTC+01:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the reply to notice NTC-9540 on time under the receipt rule?"
 },
 {
  "qid": "q457baf83d0",
  "kind": "yes/no",
  "text": "Dana Okafor: Hey there! Sending file CASE-2544 about the appeal deadline your way, hope it helps lol.\nservice: Thanks so much, that is great.\ndesk: Awesome, we have it on screen.\n\nCase CASE-2544, party Dana Okafor:\n- billing date: 2028-01-08\n- statement date: 2028-02-07\n- dispute filed on: 2028-03-08\n- days from the billing date to the filing: 60 days\n- days from the statement date to the filing: 30 days",
  "question": "Filing rule: the dispute must be filed within 30 days following the later of these dates: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the dispute from Dana Okafor, under the filing rule, filed after the deadline?"
 },
 {
  "qid": "qc410e45c7e",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nClara Weiss here, sending file POL-3156 about the loss claim and hoping it brightens your desk. Big thanks to the team on this.\nCheers,\n\nPolicy POL-3156, holder Clara Weiss:\n- policy start date: Tuesday, October 5, 2027\n- glass breakage cover: added by a rider effective Monday, October 18, 2027\n- glass breakage loss on: Tuesday, November 2, 2027\n- days from the policy start date to the loss: 28 days\n- days from the rider effective date to the loss: fifteen days",
  "question": "Cover rule: a loss is covered only after a waiting period of fourteen days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is fourteen days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the glass breakage loss on policy POL-3156 covered under the cover rule?"
 },
 {
  "qid": "q1122153217",
  "kind": "yes/no",
  "text": "Mira Castell: Busy, but here is POL-6663 about the cover question.\nhelp desk: Received, thanks.\n\nPolicy POL-6663, holder Mira Castell:\n- policy start date: Thursday, 8 July 2027\n- fire damage cover: added by a rider effective Friday, 3 December 2027\n- fire damage loss on: Friday, 10 December 2027\n- days from the policy start date to the loss: 155 days\n- days from the rider effective date to the loss: seven days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days with the start date itself left out, beginning the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the loss on policy POL-6663 covered under the cover rule?"
 },
 {
  "qid": "qa178df8798",
  "kind": "yes/no",
  "text": "Ravi Anand: sending STAY-1179 about the residence day count, in a rush.\nservice desk: got it, thanks.\ndesk: that is the full file.\n\nStay record STAY-1179 for Ravi Anand:\n- entry day Monday, November 23, 2026, exit day Sunday, November 29, 2026 (whole stay: 7 days)\n- entry day Monday, December 28, 2026, exit day Wednesday, January 6, 2027 (whole stay: 10 days)\n- entry day Wednesday, January 20, 2027, exit day Wednesday, January 20, 2027 (whole stay: 1 day)\nReference date: Sunday, February 7, 2027\nWindow checked: Thursday, December 10, 2026 to Sunday, February 7, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 21 days inside every moving 60-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Ravi Anand inside the stay limit when, under the stay rule, the days present in the window ending on Sunday, February 7, 2027 number at most the limit?"
 },
 {
  "qid": "q6d4bab968d",
  "kind": "yes/no",
  "text": "Jonas Feld sent file STAY-2500 about the visa stay count to the desk. The file is shared as part of the usual exchange. This is routine and straightforward.\n\nStay record STAY-2500 for Jonas Feld:\n- entry day Saturday, 4 April 2026, exit day Tuesday, 28 April 2026 (whole stay: 25 days)\n- entry day Monday, 18 May 2026, exit day Wednesday, 20 May 2026 (whole stay: three days)\nReference date: Tuesday, 9 June 2026\nWindow checked: Saturday, 11 April 2026 to Tuesday, 9 June 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 21 days within any 60-day window that keeps moving. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the person in file STAY-2500 within the stay limit, meaning the days present in the checked window are at most the limit?"
 },
 {
  "qid": "q9799cf0586",
  "kind": "choice",
  "text": "Felix Ortega sends file STAY-9383 about the border stay check to the desk. The file keeps to the standard format. A full copy sits with the desk too.\n\nStay record STAY-9383 for Felix Ortega:\n- entry day 9 Oct 2027, exit day 24 Oct 2027 (whole stay: sixteen days)\n- entry day 4 Nov 2027, exit day 5 Nov 2027 (whole stay: two days)\n- entry day 15 Nov 2027, exit day 17 Nov 2027 (whole stay: three days)\nReference date: 21 Nov 2027\nWindow checked: 23 Oct 2027 to 21 Nov 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to fourteen days inside any moving 30-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 30-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than fourteen days, and within the limit if it is fourteen days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days, under the stay rule, was Felix Ortega present inside the checked window ending on 21 Nov 2027?",
  "options": [
   "8 days",
   "7 days"
  ]
 },
 {
  "qid": "q66b52b25e5",
  "kind": "yes/no",
  "text": "Theo Kalnins: sending NTC-3466 about the response deadline, here it is.\nhelp desk: got it, thanks.\nhelp desk: that is the whole pack.\n\nNotice NTC-3466 to Theo Kalnins:\n- response due date: Saturday, 27 November 2027\n- office cutoff on the due date: 2027-11-27T15:49:00-04:00\n- response sent: 2027-11-27T14:49:00-05:00 [same instant in office time: 2027-11-27T15:49:00-04:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the response to notice NTC-3466 on time under the receipt rule?"
 },
 {
  "qid": "q3255c95bd5",
  "kind": "choice",
  "text": "Eva Marsh: Hello, I am sending file CASE-7220 about the claim deadline question to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nCase CASE-7220, party Eva Marsh:\n- inspection date: 2028-06-12\n- report date: 2028-04-28",
  "question": "Filing rule: the objection must be filed inside a span of 43 days that runs after the later of these dates: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 43 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the latest date by which the objection can be filed in time?",
  "options": [
   "2028-07-27",
   "2028-06-10",
   "2028-08-10",
   "2028-07-25"
  ]
 },
 {
  "qid": "qc665f35b97",
  "kind": "yes/no",
  "text": "Sent by: Lena Whitcombe\nFile: PO-2444\nSent to: records clerk\nShort note, my queue is packed. The file is about the purchase request and is attached.\n\nPurchase log PO-2444, kept by Lena Whitcombe, vendor Corvane Office:\n- earlier purchase on 2026-06-13: $5,262.00\n- earlier purchase on 2026-09-20: $2,740.00\n- earlier purchase on 2026-10-03: $248.00\n- earlier purchase on 2026-12-02: $4,545.00\n- new request on 2026-12-15: $7,468.00\nWindow checked: 2026-09-17 to 2026-12-15, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is a figure greater than $15,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the request from Lena Whitcombe, under the purchase rule, call for written quotes in log PO-2444?"
 },
 {
  "qid": "q769828ead5",
  "kind": "choice",
  "text": "Ana Ruiz sends file CASE-7003 about the complaint filing to the admin team. Quick note, I am snowed under. The attachment carries the main points near the top. Off I go.\n\nCase CASE-7003, party Ana Ruiz:\n- incident date: December 16, 2026\n- discovery date: December 13, 2026",
  "question": "Filing rule: the complaint must be filed inside nine days reckoned from the date that falls later among the dates below: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is nine days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, what is the latest date on which the complaint can be filed in time?",
  "options": [
   "December 25, 2026",
   "December 24, 2026",
   "December 23, 2026",
   "December 22, 2026"
  ]
 },
 {
  "qid": "qe5bf3ef0a7",
  "kind": "choice",
  "text": "Internal memo for the desk.\n\nTomas Lindqvist sends file POL-5718 about the insurance claim to the desk, with the review team copied in. Thank you for your careful work on this matter. I appreciate the effort put into it.\n\nPolicy POL-5718, holder Tomas Lindqvist:\n- policy start date: Wednesday, 27 May 2026\n- glass breakage cover: added by a rider effective Saturday, 20 June 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of eleven days that begins on the next day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is eleven days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the earliest date on which the glass breakage loss under policy POL-5718 would be covered?",
  "options": [
   "Monday, 8 June 2026",
   "Saturday, 4 July 2026",
   "Thursday, 2 July 2026",
   "Tuesday, 30 June 2026"
  ]
 },
 {
  "qid": "qf877b2cf22",
  "kind": "yes/no",
  "text": "Eva Marsh: Hiya! Sending PO-4668 about the purchase request, all good here.\nservice desk: Lovely, thanks for the heads up!\n\nPurchase log PO-4668, kept by Eva Marsh, vendor Corvane Office:\n- earlier purchase on 7 May 2027: $5,788\n- earlier purchase on 26 Jul 2027: $3,002\n- new request on 5 Aug 2027: $5,009\nWindow checked: 8 May 2027 to 5 Aug 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is $10,000 as a floor, greater than that counts, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does the purchase request in log PO-4668 need written quotes under the purchase rule?"
 },
 {
  "qid": "qd8d74c2192",
  "kind": "choice",
  "text": "Internal memo for the desk.\n\nLena Whitcombe sends file POL-4658 about the insurance claim to the desk, with the review team copied in. Thank you for your careful work on this matter. I appreciate the effort put into it.\n\nPolicy POL-4658, holder Lena Whitcombe:\n- policy start date: Tuesday, June 1, 2027\n- glass breakage cover: added by a rider effective Thursday, July 29, 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 87 days that starts on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 87 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the earliest date on which the glass breakage loss under policy POL-4658 would be covered?",
  "options": [
   "Wednesday, October 27, 2027",
   "Monday, October 25, 2027",
   "Saturday, October 23, 2027",
   "Tuesday, October 26, 2027"
  ]
 },
 {
  "qid": "q9cf9614185",
  "kind": "yes/no",
  "text": "File: POL-7068\nSubject: the insurance claim\nFrom: Clara Weiss\nRespectfully passing this file on to the review team. Thank you kindly for your attention.\n\nPolicy POL-7068, holder Clara Weiss:\n- policy start date: January 19, 2027\n- glass breakage cover: part of the base policy\n- glass breakage loss on: February 18, 2027\n- days from the policy start date to the loss: 30 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days that begins on the next day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWould policy POL-7068 cover this glass breakage loss under the cover rule?"
 },
 {
  "qid": "q0063ef02a1",
  "kind": "choice",
  "text": "Dear front desk,\nRavi Anand is writing to share file CASE-2441 about the claim deadline question with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,\n\nCase CASE-2441, party Ravi Anand:\n- inspection date: Saturday, 8 November 2025\n- report date: Thursday, 9 October 2025",
  "question": "Filing rule: the objection must be filed within 90 days measured from the later of the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the latest date, under the filing rule, on which the objection for case CASE-2441 can be filed in time?",
  "options": [
   "Friday, 13 March 2026",
   "Thursday, 5 February 2026",
   "Friday, 6 February 2026"
  ]
 },
 {
  "qid": "qff66648bc1",
  "kind": "choice",
  "text": "Hi front desk,\nHana Sato sends file POL-2227 about the cover question as a regular copy. The file follows the standard format. That covers the routine points.\nRegards,\n\nPolicy POL-2227, holder Hana Sato:\n- policy start date: 2026-07-05\n- flood damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the earliest date on which the flood damage loss would be covered?",
  "options": [
   "2026-08-15",
   "2026-08-05",
   "2026-08-07"
  ]
 },
 {
  "qid": "qb9fdd52cd9",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nHope you are doing great! Felix Ortega has sent file NTC-4741 about the response deadline, all lovely and tidy. Just wanted to pop it in your inbox. Catch you round.\nCheers\n\nNotice NTC-4741 to Felix Ortega:\n- response due date: 19 April 2027\n- office cutoff on the due date: 2027-04-19T17:00:00-04:00\n- response sent: 2027-04-20T13:24:00+01:00 [same instant in office time: 2027-04-20T08:24:00-04:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the response to notice NTC-4741 late under the receipt rule, counted as received after the due date?"
 },
 {
  "qid": "qb96df77195",
  "kind": "yes/no",
  "text": "Lucas Brenner: Hello, I am sending file NTC-6208 about the response deadline to the case team, with thanks.\nteam: Thank you for the careful note.\nteam: Your gesture is warmly felt.\n\nNotice NTC-6208 to Lucas Brenner:\n- response due date: February 8, 2026\n- office cutoff on the due date: 2026-02-08T21:01:00-04:00\n- response sent: 2026-02-09T04:06:00+03:00 [same instant in office time: 2026-02-08T21:06:00-04:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Lucas Brenner received on time under the receipt rule?"
 },
 {
  "qid": "q1f7dac5ac2",
  "kind": "choice",
  "text": "Sent by: Ravi Anand\nFile: LED-3596\nSent to: review team\nThis is a standard note about the cash ledger check. The file is laid out as usual.\n\nCash ledger LED-3596, teller Ravi Anand:\n- 2028-06-13: withdrawal of $1,312.00\n- 2028-06-13: deposit of $2,085.00\n- 2028-06-13: withdrawal of $1,689.00\n- 2028-06-13: deposit of $916.00\n- 2028-06-15: deposit of $1,624.00\nDay under review: 2028-06-13",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is $3,000.00 bar, cleared only by more than that, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, which of the day's totals on 2028-06-13 call for a cash report?",
  "options": [
   "Only the withdrawal total",
   "Only the deposit total",
   "Both totals",
   "Neither total"
  ]
 },
 {
  "qid": "q259c28b662",
  "kind": "choice",
  "text": "Clara Weiss: Sending STAY-3547 about the border stay check, routine as usual.\nintake team: Thanks, received.\n\nStay record STAY-3547 for Clara Weiss:\n- entry day 2027-02-25, exit day 2027-04-02 (whole stay: 37 days)\n- entry day 2027-04-10, exit day 2027-04-11 (whole stay: 2 days)\nReference date: 2027-04-21\nWindow checked: 2027-03-23 to 2027-04-21, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 14 days in each 30-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 30-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 14 days, and within the limit if it is 14 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, how many days present fall inside the checked window ending on 2027-04-21 in file STAY-3547?",
  "options": [
   "11 days",
   "39 days",
   "13 days"
  ]
 },
 {
  "qid": "q174a33b5fe",
  "kind": "yes/no",
  "text": "Priya Raman has sent file CASE-4654 about the claim deadline question to the desk. This is a routine item and the file is attached in full. The desk is copied for completeness. This memo concerns only the sending of the file.\n\nCase CASE-4654, party Priya Raman:\n- invoice date: 2026-06-19\n- goods received date: 2026-07-10\n- claim filed on: 2026-07-31\n- days from the invoice date to the filing: 42 days\n- days from the goods received date to the filing: 21 days",
  "question": "Filing rule: the claim must be filed inside 21 days that elapses after whichever of the dates below is later: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Priya Raman fail to file the claim in case CASE-4654 by the deadline?"
 },
 {
  "qid": "qc830109ff4",
  "kind": "choice",
  "text": "Sent by: Ravi Anand\nFile code: CASE-4349\nFor: review team\nThe file about the complaint filing is passed along as usual.\n\nCase CASE-4349, party Ravi Anand:\n- incident date: Wednesday, 20 May 2026\n- discovery date: Saturday, 4 July 2026",
  "question": "Filing rule: the complaint must be filed within 28 days counted forward from the later among these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the latest date, under the filing rule, on which the complaint for case CASE-4349 can be filed in time?",
  "options": [
   "Saturday, 1 August 2026",
   "Wednesday, 17 June 2026",
   "Friday, 31 July 2026"
  ]
 },
 {
  "qid": "q0cbf4a3deb",
  "kind": "yes/no",
  "text": "Aiko Brandt: sending file NTC-3386 about the response deadline, with thanks.\nintake team: thank you, this is received.\nintake team: appreciated.\n\nNotice NTC-3386 to Aiko Brandt:\n- response due date: 2027-07-04\n- office cutoff on the due date: 2027-07-04 18:48:00 +0100\n- response sent: 2027-07-04 20:43:00 +0300 [same instant in office time: 2027-07-04 18:43:00 +0100]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, is it true that the response to notice NTC-3386 was not on time?"
 },
 {
  "qid": "qee12cdae96",
  "kind": "choice",
  "text": "Dana Okafor sends file POL-7909 about the insurance claim to the desk. The file keeps to the standard format. A full copy sits with the desk too.\n\nPolicy POL-7909, holder Dana Okafor:\n- policy start date: August 7, 2027\n- glass breakage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 60 days commencing on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 60 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the earliest date on which this glass breakage loss for Dana Okafor would be covered?",
  "options": [
   "October 5, 2027",
   "October 9, 2027",
   "October 7, 2027"
  ]
 },
 {
  "qid": "qbbc819762c",
  "kind": "yes/no",
  "text": "Omar Saleh sends file POL-1108 about the cover question to the admin team. Sending this across quickly because I am tied up with other work. The full file is attached for the team. Thanks for taking it.\n\nPolicy POL-1108, holder Omar Saleh:\n- policy start date: 2026-12-21\n- theft cover: added by a rider effective 2027-06-27\n- theft loss on: 2027-08-10\n- days from the policy start date to the loss: 232 days\n- days from the rider effective date to the loss: 44 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days that opens on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the theft loss on policy POL-1108 covered under the cover rule?"
 },
 {
  "qid": "qb53d0f3d25",
  "kind": "choice",
  "text": "Aiko Brandt: file CASE-5333 about the claim deadline question is attached.\ncase team: received, thanks.\ncase team: that is the whole file.\n\nCase CASE-5333, party Aiko Brandt:\n- invoice date: Friday, 25 December 2026\n- goods received date: Sunday, 20 December 2026",
  "question": "Filing rule: the claim must be filed inside 22 days extending past the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 22 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, by which final day must the claim be filed to still count as in time?",
  "options": [
   "Saturday, 16 January 2027",
   "Thursday, 14 January 2027",
   "Monday, 11 January 2027",
   "Friday, 15 January 2027"
  ]
 },
 {
  "qid": "q4296d2c478",
  "kind": "choice",
  "text": "Hi front desk,\nJonas Feld sends file STAY-5212 about the visa stay count as a standard copy. The file keeps to the usual format.\nRegards,\n\nStay record STAY-5212 for Jonas Feld:\n- entry day Saturday, February 28, 2026, exit day Thursday, April 2, 2026 (whole stay: 34 days)\n- entry day Monday, April 20, 2026, exit day Monday, April 27, 2026 (whole stay: eight days)\n- entry day Monday, May 25, 2026, exit day Saturday, June 13, 2026 (whole stay: twenty days)\nReference date: Saturday, July 4, 2026\nWindow checked: Saturday, March 7, 2026 to Saturday, July 4, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days in every 120-day run that moves forward through time. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, how many days present for Jonas Feld fall inside the checked window that ends on the reference date?",
  "options": [
   "55 days",
   "58 days",
   "54 days"
  ]
 },
 {
  "qid": "q2e63690abf",
  "kind": "yes/no",
  "text": "Hana Sato: Hello, I am sending file CASE-9581 about the appeal deadline to the case team, with thanks.\nteam: Thank you for the careful note.\nteam: Your gesture is warmly felt.\n\nCase CASE-9581, party Hana Sato:\n- billing date: September 15, 2027\n- statement date: October 6, 2027\n- dispute filed on: November 4, 2027\n- days from the billing date to the filing: 50 days\n- days from the statement date to the filing: 29 days",
  "question": "Filing rule: the dispute must be filed inside 28 days that elapses after whichever of the dates below is later: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the dispute from Hana Sato filed in time, on or before the final day of the filing period?"
 },
 {
  "qid": "q2f0a9f48de",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nJonas Feld sends file NTC-9982 about the response deadline with a cheerful hello. The file is in the usual layout and is fun to read.\nCheers,\n\nNotice NTC-9982 to Jonas Feld:\n- response due date: 2025-06-05\n- office cutoff on the due date: 2025-06-05 21:38:00 -0500\n- response sent: 2025-06-06 05:28:00 +0100 [same instant in office time: 2025-06-05 23:28:00 -0500]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the response to notice NTC-9982 late under the receipt rule?"
 },
 {
  "qid": "q844c09e86c",
  "kind": "choice",
  "text": "Hi front desk,\nTomas Lindqvist sends file CASE-2504 about the claim deadline question in the usual form. The file sits in the standard layout alongside the other sheets.\nRegards,\n\nCase CASE-2504, party Tomas Lindqvist:\n- inspection date: Friday, September 5, 2025\n- report date: Monday, September 8, 2025",
  "question": "Filing rule: the objection must be filed within 43 days past the later of the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 43 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, what is the latest date on which the objection can be filed in time?",
  "options": [
   "Tuesday, October 21, 2025",
   "Sunday, October 19, 2025",
   "Thursday, October 23, 2025"
  ]
 },
 {
  "qid": "q36f825bbbb",
  "kind": "yes/no",
  "text": "Kofi Mensah: sending NTC-6620 about the response deadline, here it is.\nhelp desk: got it, thanks.\nhelp desk: that is the whole pack.\n\nNotice NTC-6620 to Kofi Mensah:\n- response due date: Wednesday, September 3, 2025\n- office cutoff on the due date: 2025-09-03T16:49:00-05:00\n- response sent: 2025-09-04T03:18:00+05:30 [same instant in office time: 2025-09-03T16:48:00-05:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the response to notice NTC-6620 on time under the receipt rule?"
 },
 {
  "qid": "qab0770d42b",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nYara Haddad here, sending file STAY-3484 about the visa stay count and hoping it brightens your desk. Big thanks to the team on this.\nCheers,\n\nStay record STAY-3484 for Yara Haddad:\n- entry day 26 Mar 2027, exit day 14 Jun 2027 (whole stay: 81 days)\n- entry day 19 Jul 2027, exit day 20 Jul 2027 (whole stay: 2 days)\nReference date: 14 Aug 2027\nWindow checked: 17 Apr 2027 to 14 Aug 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days in any 120-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is Yara Haddad over the stay limit, with more days present in the checked window ending on the reference date?"
 },
 {
  "qid": "q303d022e41",
  "kind": "choice",
  "text": "Ravi Anand sends file CASE-7870 about the complaint filing to the admin team. Sending this across quickly because I am tied up with other work. The full file is attached for the team. Thanks for taking it.\n\nCase CASE-7870, party Ravi Anand:\n- incident date: 1 February 2028\n- discovery date: 18 December 2027",
  "question": "Filing rule: the complaint must be filed within fourteen days measured from the later of the dates below: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is fourteen days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the final day still in time for filing the complaint in case CASE-7870?",
  "options": [
   "16 February 2028",
   "21 February 2028",
   "14 February 2028",
   "15 February 2028"
  ]
 },
 {
  "qid": "q0a65c07c84",
  "kind": "yes/no",
  "text": "Ana Ruiz: Quick send, NTC-9361 about the response deadline.\nhelp desk: Got it.\n\nNotice NTC-9361 to Ana Ruiz:\n- response due date: 2027-06-20\n- office cutoff on the due date: 20 June 2027, 14:36 (UTC+01:00)\n- response sent: 2027-06-20T13:38:00Z [same instant in office time: 20 June 2027, 14:38 (UTC+01:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Ana Ruiz to notice NTC-9361 on time under the receipt rule?"
 },
 {
  "qid": "q512ec7bdee",
  "kind": "yes/no",
  "text": "Dear duty clerk,\nLena Whitcombe is sending file POL-9412 about the loss claim. It is attached here. Hope your work goes well.\nCheers,\n\nPolicy POL-9412, holder Lena Whitcombe:\n- policy start date: 2027-04-08\n- burst pipe damage cover: part of the base policy\n- burst pipe damage loss on: 2027-06-05\n- days from the policy start date to the loss: 58 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days that opens on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, is the burst pipe damage loss for Lena Whitcombe covered under the cover rule?"
 }
]
