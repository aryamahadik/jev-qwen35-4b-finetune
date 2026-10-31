# G5-H blind read T01-blind_read-f3de2246-002 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g5h/answers/T01-blind_read-f3de2246-002.json

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
  "qid": "qbf1c07a319",
  "kind": "choice",
  "text": "Memo to the desk: Owen Pryce has forwarded file POL-5442 about the insurance claim. The desk is thanked in advance for its attention.\n\nPolicy POL-5442, holder Owen Pryce:\n- policy start date: 11 May 2027\n- fire damage cover: added by a rider effective 9 Oct 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days that picks up on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the earliest date on which this fire damage loss for Owen Pryce would be covered?",
  "options": [
   "22 Oct 2027",
   "24 Oct 2027",
   "26 May 2027"
  ]
 },
 {
  "qid": "qe40b0c49b7",
  "kind": "yes/no",
  "text": "Memo: Yara Haddad has sent in file POL-7627 about the insurance claim. It goes to the records clerk for routine handling.\n\nPolicy POL-7627, holder Yara Haddad:\n- policy start date: Monday, 8 November 2027\n- flood damage cover: part of the base policy\n- flood damage loss on: Friday, 12 November 2027\n- days from the policy start date to the loss: 4 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 7 days that starts on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 7 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the flood damage loss under policy POL-7627 within the waiting period?"
 },
 {
  "qid": "q8fc61f8a71",
  "kind": "yes/no",
  "text": "Eva Marsh: Hiya! Sending PO-4668 about the purchase request, all good here.\nservice desk: Lovely, thanks for the heads up!\n\nPurchase log PO-4668, kept by Eva Marsh, vendor Corvane Office:\n- earlier purchase on 7 May 2027: $5,788\n- earlier purchase on 26 Jul 2027: $3,002\n- new request on 5 Aug 2027: $5,009\nWindow checked: 8 May 2027 to 5 Aug 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is $10,000 as a floor, greater than that counts, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does the purchase request in log PO-4668 need written quotes under the purchase rule?"
 },
 {
  "qid": "q2a811dc750",
  "kind": "yes/no",
  "text": "Subject: hello again\nHi review team,\nQuick note: Dana Okafor sent in file STAY-9007 about the border stay check, so have a look when you like.\nTake care,\n\nStay record STAY-9007 for Dana Okafor:\n- entry day 17 May 2026, exit day 30 May 2026 (whole stay: 14 days)\nReference date: 15 June 2026\nWindow checked: 17 May 2026 to 15 June 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 14 days within any 30-day window that keeps moving. Day counts are calendar days, and entry and exit days both count as days present. Only one 30-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 14 days, and within the limit if it is 14 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Dana Okafor, under the stay rule, over the stay limit for the window ending on 15 June 2026?"
 },
 {
  "qid": "q023114ecde",
  "kind": "choice",
  "text": "Omar Saleh: file POL-5318 about the insurance claim is here.\nintake team: received, thanks.\nintake team: that is everything for this file.\n\nPolicy POL-5318, holder Omar Saleh:\n- policy start date: 2027-10-29\n- power surge damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 88 days that starts on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 88 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the earliest date on which a loss of this kind would be covered under policy POL-5318?",
  "options": [
   "2028-01-28",
   "2028-01-26",
   "2028-01-27"
  ]
 },
 {
  "qid": "q2fcc51d709",
  "kind": "yes/no",
  "text": "Desk memo: Felix Ortega respectfully sends file NTC-4583 about the notice response to the duty clerk. Kindly place it in the duty queue. We thank you in advance.\n\nNotice NTC-4583 to Felix Ortega:\n- response due date: September 1, 2027\n- office cutoff on the due date: 2027-09-01T17:30:00+03:00\n- response sent: 2027-09-01T19:59:00+05:30 [same instant in office time: 2027-09-01T17:29:00+03:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Felix Ortega to notice NTC-4583 on time under the receipt rule?"
 },
 {
  "qid": "qf0706f7f4f",
  "kind": "yes/no",
  "text": "Priya Raman sends file STAY-4453 about the residence day count to the desk. The file keeps to the standard format. A full copy sits with the desk too.\n\nStay record STAY-4453 for Priya Raman:\n- entry day Thursday, November 13, 2025, exit day Saturday, November 29, 2025 (whole stay: seventeen days)\n- entry day Thursday, December 11, 2025, exit day Tuesday, March 10, 2026 (whole stay: 90 days)\nReference date: Friday, May 8, 2026\nWindow checked: Friday, January 9, 2026 to Friday, May 8, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days in each 120-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Priya Raman over the stay limit, counting the days present inside the window that ends on Friday, May 8, 2026?"
 },
 {
  "qid": "qaaee292a21",
  "kind": "choice",
  "text": "title | file NTC-9509 about the response deadline\nrequester | Aiko Brandt\nQuick handoff, sent straight to the review team.\n\nNotice NTC-9509 to Aiko Brandt:\n- response due date: 14 June 2028\n- office cutoff on the due date: 2028-06-14 13:01:00 -0500\n- response sent: 2028-06-13 14:59:00 -0300 [same instant in office time: 2028-06-13 12:59:00 -0500]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, on which date is the response from Aiko Brandt counted as received under the receipt rule?",
  "options": [
   "14 Jun 2028",
   "13 Jun 2028"
  ]
 },
 {
  "qid": "q976b304b9d",
  "kind": "yes/no",
  "text": "review: Send it through, we are rolling fast here.\nMira Castell: Dropping file POL-8794 about the loss claim with the review team, moving quick.\n\nPolicy POL-8794, holder Mira Castell:\n- policy start date: 2026-05-24\n- fire damage cover: part of the base policy\n- fire damage loss on: 2026-08-22\n- days from the policy start date to the loss: 90 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 90 days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 90 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, did the loss on policy POL-8794 happen during the waiting period?"
 },
 {
  "qid": "qb4e9228547",
  "kind": "yes/no",
  "text": "Desk memo: Bruno Lacerda sends file PO-1006 about the purchase request to the intake team as part of the usual flow.\nThe intake team takes it from there.\n\nPurchase log PO-1006, kept by Bruno Lacerda, vendor Vantmoor Electric:\n- earlier purchase on December 29, 2025: $547\n- earlier purchase on February 14, 2026: $757\n- earlier purchase on March 31, 2026: $124\n- earlier purchase on April 8, 2026: $430\n- earlier purchase on May 14, 2026: $833\n- new request on June 13, 2026: $1,613\nWindow checked: February 14, 2026 to June 13, 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 120-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any sum more than $3,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request from Bruno Lacerda in log PO-1006 need written quotes under the purchase rule?"
 },
 {
  "qid": "q98bdf607e4",
  "kind": "choice",
  "text": "Lucas Brenner: Sending file LED-2719 about the branch cash review to the front desk, enjoy!\ndesk: Oh lovely, thanks a ton.\n\nCash ledger LED-2719, teller Lucas Brenner:\n- Thursday, January 15, 2026: deposit of $2,503.00\n- Thursday, January 15, 2026: withdrawal of $1,076.00\n- Thursday, January 15, 2026: withdrawal of $3,615.00\n- Friday, January 16, 2026: deposit of $1,681.00\n- Saturday, January 17, 2026: deposit of $3,916.00\nDay under review: Thursday, January 15, 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is a sum of $5,000.00 or more, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nFor Thursday, January 15, 2026, which of the day's totals, under the cash rule, call for a cash report?",
  "options": [
   "Only the deposit total",
   "Neither total",
   "Both totals",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q0d2251e71c",
  "kind": "choice",
  "text": "team: help desk\nsent_by: Mira Castell\nfile: CASE-3103\nsubject: the appeal deadline\nnote: in a rush\n\nCase CASE-3103, party Mira Castell:\n- decision date: September 28, 2027\n- delivery date: October 1, 2027",
  "question": "Filing rule: the appeal must be filed within 47 days counted forward from the later among these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 47 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUntil which date, under the filing rule, may Mira Castell file the appeal in time?",
  "options": [
   "November 14, 2027",
   "November 19, 2027",
   "November 17, 2027"
  ]
 },
 {
  "qid": "qbc4c28ffe7",
  "kind": "choice",
  "text": "Subject: quick pass-along\nHi service desk,\nQuick note: Lena Whitcombe sends file CASE-5286 about the appeal deadline, so please grab it at your earliest convenience.\nBest,\n\nCase CASE-5286, party Lena Whitcombe:\n- decision date: Thursday, April 27, 2028\n- delivery date: Tuesday, April 25, 2028",
  "question": "Filing rule: the appeal must be filed inside 90 days reckoned from the date that falls later among the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUntil which date, under the filing rule, may Lena Whitcombe file the appeal in time?",
  "options": [
   "Wednesday, July 26, 2028",
   "Tuesday, July 25, 2028",
   "Monday, July 24, 2028"
  ]
 },
 {
  "qid": "q685723a01a",
  "kind": "yes/no",
  "text": "Internal memo: a quick note for the front desk. File NTC-9051 about the response deadline is coming from Felix Ortega, moving fast.\n\nNotice NTC-9051 to Felix Ortega:\n- response due date: 14 June 2026\n- office cutoff on the due date: 2026-06-14 12:30:00 +0100\n- response sent: 2026-06-14 14:25:00 +0300 [same instant in office time: 2026-06-14 12:25:00 +0100]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the response to notice NTC-9051 late under the receipt rule?"
 },
 {
  "qid": "qfc5b4ea38f",
  "kind": "choice",
  "text": "[service] file=POL-2001 about the insurance claim came_from=Yara Haddad\n[service] addressed_to=service desk, cheerful_thanks\n\nPolicy POL-2001, holder Yara Haddad:\n- policy start date: Friday, 29 October 2027\n- fire damage cover: added by a rider effective Sunday, 12 December 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 10 days whose first counted day falls on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 10 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on what earliest date would Yara Haddad be covered for the fire damage loss?",
  "options": [
   "Thursday, 23 December 2027",
   "Tuesday, 9 November 2027",
   "Tuesday, 21 December 2027"
  ]
 },
 {
  "qid": "q17e3be233f",
  "kind": "yes/no",
  "text": "Theo Kalnins: file POL-9777 about the loss claim is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.\n\nPolicy POL-9777, holder Theo Kalnins:\n- policy start date: May 19, 2027\n- fire damage cover: added by a rider effective July 6, 2027\n- fire damage loss on: August 26, 2027\n- days from the policy start date to the loss: 99 days\n- days from the rider effective date to the loss: 51 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 10 days that begins on the next day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 10 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is the fire damage loss for Theo Kalnins covered under the cover rule?"
 },
 {
  "qid": "q48affc1aee",
  "kind": "yes/no",
  "text": "Subject | file POL-8410 about the cover question\nFrom | Mira Castell\nGroup | help desk\nPlease take a quick peek.\n\nPolicy POL-8410, holder Mira Castell:\n- policy start date: Sunday, November 8, 2026\n- storm damage cover: part of the base policy\n- storm damage loss on: Monday, November 23, 2026\n- days from the policy start date to the loss: fifteen days",
  "question": "Cover rule: a loss is covered only after a waiting period of fifteen days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is fifteen days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is the storm damage loss covered under the cover rule?"
 },
 {
  "qid": "q767bc75939",
  "kind": "choice",
  "text": "Subject: Routine send on the loss claim\n\nHello intake team,\n\nSending file POL-1776 from Ines Duarte for the usual intake steps. Standard handling is fine.\n\nRegards,\n\nPolicy POL-1776, holder Ines Duarte:\n- policy start date: Tuesday, 6 January 2026\n- power surge damage cover: added by a rider effective Monday, 4 May 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days that starts on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the earliest date on which the power surge damage loss under policy POL-1776 would be covered?",
  "options": [
   "Tuesday, 26 May 2026",
   "Sunday, 24 May 2026",
   "Wednesday, 27 May 2026",
   "Thursday, 28 May 2026"
  ]
 },
 {
  "qid": "q403b8e3937",
  "kind": "choice",
  "text": "[intake] file=CASE-7498 sender=Dana Okafor regarding the appeal deadline\n[note] kindly_forwarded_to=duty_clerk\n\nCase CASE-7498, party Dana Okafor:\n- decision date: June 24, 2027\n- delivery date: June 19, 2027",
  "question": "Filing rule: the appeal must be filed within 30 days measured from the later of the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUntil which date, under the filing rule, may Dana Okafor file the appeal in time?",
  "options": [
   "July 24, 2027",
   "July 22, 2027",
   "July 26, 2027"
  ]
 },
 {
  "qid": "qdb1f7fcfb7",
  "kind": "choice",
  "text": "Hi front desk,\nTomas Lindqvist sends file CASE-2504 about the claim deadline question in the usual form. The file sits in the standard layout alongside the other sheets.\nRegards,\n\nCase CASE-2504, party Tomas Lindqvist:\n- inspection date: Friday, September 5, 2025\n- report date: Monday, September 8, 2025",
  "question": "Filing rule: the objection must be filed within 45 days past the later of the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, what is the latest date on which the objection can be filed in time?",
  "options": [
   "Thursday, October 23, 2025",
   "Saturday, October 25, 2025",
   "Wednesday, October 22, 2025"
  ]
 },
 {
  "qid": "qe52f5514b6",
  "kind": "yes/no",
  "text": "Internal memo: the sender Malik Osei forwards file STAY-9931 about the visa stay count to the records clerk. Kindly add it to the desk log for handling, with thanks for your care.\n\nStay record STAY-9931 for Malik Osei:\n- entry day Monday, July 26, 2027, exit day Friday, September 3, 2027 (whole stay: 40 days)\n- entry day Friday, September 24, 2027, exit day Wednesday, October 13, 2027 (whole stay: twenty days)\nReference date: Monday, November 1, 2027\nWindow checked: Monday, July 5, 2027 to Monday, November 1, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days in each 120-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Malik Osei over the stay limit, with more days present inside the window that ends on the reference date in file STAY-9931, under the stay rule?"
 },
 {
  "qid": "qae4d4c64a2",
  "kind": "yes/no",
  "text": "Clara Weiss: ringing in to send file PO-4783 about the purchase request\ndesk: thanks, logging it for the team.\n\nPurchase log PO-4783, kept by Clara Weiss, vendor Ostrava Parts:\n- earlier purchase on Wednesday, December 2, 2026: $2,166\n- earlier purchase on Wednesday, February 3, 2027: $1,124\n- earlier purchase on Tuesday, March 2, 2027: $393\n- earlier purchase on Friday, March 12, 2027: $931\n- earlier purchase on Wednesday, March 31, 2027: $1,843\n- new request on Sunday, April 4, 2027: $1,833\nWindow checked: Thursday, February 4, 2027 to Sunday, April 4, 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is a figure of $5,000 or greater, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does the purchase request in log PO-4783 need written quotes under the purchase rule?"
 },
 {
  "qid": "q4123312a63",
  "kind": "choice",
  "text": "[routing] from=Owen Pryce file=LED-7339 about=\"the cash ledger check\" to=duty_clerk\n[log] entry_added_for_intake_queue\n\nCash ledger LED-7339, teller Owen Pryce:\n- Saturday, 25 April 2026: deposit of 4,415.00 USD\n- Saturday, 25 April 2026: withdrawal of 1,103.00 USD\n- Saturday, 25 April 2026: withdrawal of 1,897.00 USD\n- Sunday, 26 April 2026: deposit of 911.00 USD\nDay under review: Saturday, 25 April 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any sum more than 3,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, which of the day's totals in ledger LED-7339, if any, call for a cash report under the cash rule?",
  "options": [
   "Only the deposit total",
   "Neither total",
   "Only the withdrawal total",
   "Both totals"
  ]
 },
 {
  "qid": "q2a610e8160",
  "kind": "yes/no",
  "text": "file: NTC-1189\nsent_by: Tomas Lindqvist\nsubject: the response deadline\nteam: help desk\nnote: a friendly hello from the sender\n\nNotice NTC-1189 to Tomas Lindqvist:\n- response due date: 10 July 2025\n- office cutoff on the due date: 10 July 2025, 19:03 (UTC-04:00)\n- response sent: 10 July 2025, 16:02 (UTC-07:00) [same instant in office time: 10 July 2025, 19:02 (UTC-04:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Tomas Lindqvist to notice NTC-1189, under the receipt rule, counted as received on time?"
 },
 {
  "qid": "q73e5b9cc21",
  "kind": "yes/no",
  "text": "Hey there, quick heads up that Kofi Mensah has sent file NTC-2210 about the response deadline to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.\n\nNotice NTC-2210 to Kofi Mensah:\n- response due date: Monday, 22 June 2026\n- office cutoff on the due date: 22 June 2026, 19:43 (UTC-05:00)\n- response sent: 23 June 2026, 09:39 (UTC+09:00) [same instant in office time: 22 June 2026, 19:39 (UTC-05:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the response to notice NTC-2210 on time under the receipt rule?"
 },
 {
  "qid": "q6187be14d2",
  "kind": "yes/no",
  "text": "title: file CASE-8213 about the claim deadline question\nrequester: Iris Vance\nThank you kindly for taking this on for the case team.\n\nCase CASE-8213, party Iris Vance:\n- inspection date: 12 October 2025\n- report date: 15 October 2025\n- objection filed on: 25 October 2025\n- days from the inspection date to the filing: 13 days\n- days from the report date to the filing: 10 days",
  "question": "Filing rule: the objection must be filed inside 9 days reckoned from the date that falls later among the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 9 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Iris Vance, under the filing rule, file the objection on or before the final day?"
 },
 {
  "qid": "q39848458c5",
  "kind": "choice",
  "text": "Desk memo: quick note for the admin team, Jonas Feld sent in file POL-9252 about the cover question. Put it in the pile and move on.\n\nPolicy POL-9252, holder Jonas Feld:\n- policy start date: Saturday, July 11, 2026\n- storm damage cover: added by a rider effective Tuesday, August 11, 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of 16 days that opens on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 16 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on what earliest date would the storm damage loss be covered?",
  "options": [
   "Wednesday, August 26, 2026",
   "Tuesday, July 28, 2026",
   "Friday, August 28, 2026"
  ]
 },
 {
  "qid": "q9989e2ee05",
  "kind": "yes/no",
  "text": "[front_desk] lovely little drop-off, file PO-6544 sent_by Ravi Anand about the buying request\n[route] cheers_from_the_desk, passing on\n\nPurchase log PO-6544, kept by Ravi Anand, vendor Quillon Labs:\n- earlier purchase on 2027-03-28: $18,391\n- new request on 2027-03-31: $6,610\nWindow checked: 2027-01-31 to 2027-03-31, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any amount that is more than $25,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, does the purchase rule require written quotes for the request from Ravi Anand?"
 },
 {
  "qid": "q6ba561f88a",
  "kind": "choice",
  "text": "Priya Raman: Hiya! Sending PO-7950 about the buying request, all good here.\nservice desk: Lovely, thanks for the heads up!\n\nPurchase log PO-7950, kept by Priya Raman, vendor Quillon Labs:\n- earlier purchase on Monday, September 22, 2025: $1,559\n- earlier purchase on Wednesday, October 1, 2025: $1,296\n- earlier purchase on Monday, December 8, 2025: $367\n- new request on Wednesday, January 28, 2026: $1,751\nWindow checked: Wednesday, October 1, 2025 to Wednesday, January 28, 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 120-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is a figure greater than $3,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat total for Priya Raman is compared with the threshold when a new request is included in that total under the purchase rule?",
  "options": [
   "$2,118",
   "$3,414",
   "$1,663"
  ]
 },
 {
  "qid": "qcfd220ee82",
  "kind": "yes/no",
  "text": "Kofi Mensah: yo, file NTC-1055 about the reply timing question just arrived with the help desk\nhelp desk: ahh cool, thanks heaps, that is a relief\n\nNotice NTC-1055 to Kofi Mensah:\n- response due date: Friday, 29 October 2027\n- office cutoff on the due date: 2027-10-29T19:31:00+09:00\n- response sent: 2027-10-29T11:56:00Z [same instant in office time: 2027-10-29T20:56:00+09:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Kofi Mensah to the notice late under the receipt rule?"
 },
 {
  "qid": "qdc2f8cd7d7",
  "kind": "choice",
  "text": "{\"sent_by\": \"Yara Haddad\", \"file\": \"CASE-6427\", \"subject\": \"the claim deadline question\", \"channel\": \"routine_intake\", \"team\": \"desk\"}\n\nCase CASE-6427, party Yara Haddad:\n- inspection date: Thursday, March 18, 2027\n- report date: Saturday, March 13, 2027",
  "question": "Filing rule: the objection must be filed within 30 days from whichever is later of these dates: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the latest date, under the filing rule, on which the objection for case CASE-6427 can be filed in time?",
  "options": [
   "Sunday, April 18, 2027",
   "Saturday, April 17, 2027",
   "Monday, April 12, 2027"
  ]
 },
 {
  "qid": "qfb52b38424",
  "kind": "yes/no",
  "text": "Subject: forwarded papers\nDear case team,\nKindly find file STAY-6036 about the visa stay count sent in by Ana Ruiz, and thank you for your attention to it.\nYours faithfully\n\nStay record STAY-6036 for Ana Ruiz:\n- entry day 24 May 2026, exit day 25 May 2026 (whole stay: 2 days)\n- entry day 16 Jun 2026, exit day 5 Aug 2026 (whole stay: 51 days)\n- entry day 25 Aug 2026, exit day 2 Sep 2026 (whole stay: 9 days)\nReference date: 22 Sep 2026\nWindow checked: 26 May 2026 to 22 Sep 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days in each 120-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Ana Ruiz, under the stay rule, over the stay limit for the window ending on 22 Sep 2026?"
 },
 {
  "qid": "qd5e65aa199",
  "kind": "choice",
  "text": "Subject: happy drop for the review team\nHi review team,\nGreat stuff, Ines Duarte sent file CASE-6376 about the claim deadline question your way!\nCheers,\n\nCase CASE-6376, party Ines Duarte:\n- inspection date: 1 September 2025\n- report date: 22 August 2025",
  "question": "Filing rule: the objection must be filed within 28 days past the later of the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, until which final day may Ines Duarte file the objection and still be in time?",
  "options": [
   "9 October 2025",
   "29 September 2025",
   "30 September 2025",
   "1 October 2025"
  ]
 },
 {
  "qid": "q6a59f993ed",
  "kind": "yes/no",
  "text": "Dear front desk,\nBruno Lacerda is sending file LED-2566 about the teller ledger review. This is a routine send and the file is full. The matter is in good shape as usual.\nRegards\n\nCash ledger LED-2566, teller Bruno Lacerda:\n- Sunday, September 3, 2028: withdrawal of 13,640.00 USD\n- Tuesday, September 5, 2028: withdrawal of 3,760.00 USD\nDay under review: Sunday, September 3, 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is greater than 10,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is a cash report required for Sunday, September 3, 2028 in ledger LED-2566?"
 },
 {
  "qid": "qb977867aae",
  "kind": "yes/no",
  "text": "Bruno Lacerda: Greetings, sending file STAY-8029 about the residence day count over to the desk.\ndesk: Thank you, that is clear and appreciated.\n\nStay record STAY-8029 for Bruno Lacerda:\n- entry day Friday, 14 May 2027, exit day Thursday, 1 July 2027 (whole stay: 49 days)\nReference date: Sunday, 8 August 2027\nWindow checked: Thursday, 10 June 2027 to Sunday, 8 August 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 21 days inside every moving 60-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Bruno Lacerda over the stay limit when days present inside the window ending on the reference date number more than the limit, under the stay rule?"
 },
 {
  "qid": "q0fdef00746",
  "kind": "yes/no",
  "text": "file: NTC-1189\nsent_by: Tomas Lindqvist\nsubject: the response deadline\nteam: help desk\nnote: a friendly hello from the sender\n\nNotice NTC-1189 to Tomas Lindqvist:\n- response due date: 10 July 2025\n- office cutoff on the due date: 10 July 2025, 19:03 (UTC-04:00)\n- response sent: 10 July 2025, 16:02 (UTC-07:00) [same instant in office time: 10 July 2025, 19:02 (UTC-04:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the reply from Tomas Lindqvist was not on time under the receipt rule?"
 },
 {
  "qid": "q54a19c6ad0",
  "kind": "yes/no",
  "text": "Nadia Kowal: Pleased to forward file NTC-4314 about the reply timing question\nclerk: Thank you, leave it with the records team\n\nNotice NTC-4314 to Nadia Kowal:\n- response due date: Saturday, August 19, 2028\n- office cutoff on the due date: 2028-08-19 13:04:00 +0900\n- response sent: 2028-08-18 21:09:00 -0700 [same instant in office time: 2028-08-19 13:09:00 +0900]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the reply to notice NTC-4314 on time under the receipt rule?"
 },
 {
  "qid": "q875f6b8f13",
  "kind": "choice",
  "text": "desk: what have you got\nMira Castell: file CASE-1549 about the complaint filing, sending it over, go ahead.\n\nCase CASE-1549, party Mira Castell:\n- incident date: Friday, 5 September 2025\n- discovery date: Friday, 26 September 2025",
  "question": "Filing rule: the complaint must be filed inside 45 days beginning at the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the latest day on which Mira Castell may still file the complaint in time?",
  "options": [
   "Monday, 10 November 2025",
   "Friday, 28 November 2025",
   "Wednesday, 12 November 2025",
   "Tuesday, 11 November 2025"
  ]
 },
 {
  "qid": "q2bc92e4416",
  "kind": "yes/no",
  "text": "origin: Eva Marsh\nitem: CASE-2218\ntopic: the claim deadline question\nteam: help desk\nchannel: intake\n\nCase CASE-2218, party Eva Marsh:\n- invoice date: 2027-05-19\n- goods received date: 2027-02-13\n- claim filed on: 2027-08-18\n- days from the invoice date to the filing: 91 days\n- days from the goods received date to the filing: 186 days",
  "question": "Filing rule: the claim must be filed within 90 days reckoned after the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid case CASE-2218 get the claim filed on or before the final day of the filing period?"
 },
 {
  "qid": "q97f7287f62",
  "kind": "choice",
  "text": "subject | the reply deadline\nfile | NTC-2462\nsent_by | Owen Pryce\nGrab it quick, the queue is busy.\n\nNotice NTC-2462 to Owen Pryce:\n- notice date: 2025-06-24\n- sent by: post\n- 30 days after the notice date, before any postal add-on or closure: 2025-07-24\nOffice closures: 2025-06-26; 2025-07-24; 2025-07-27.",
  "question": "Response rule: a response is due 30 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add two days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, which date is the deadline for the response from Owen Pryce to the notice?",
  "options": [
   "2025-07-25",
   "2025-07-26"
  ]
 },
 {
  "qid": "q15e1d2db05",
  "kind": "yes/no",
  "text": "Aiko Brandt: Dear team, I am forwarding file POL-5347 about the cover question to the intake team.\nintake: Thank you for passing it along.\nteam: With thanks for your courtesy.\n\nPolicy POL-5347, holder Aiko Brandt:\n- policy start date: September 27, 2027\n- glass breakage cover: added by a rider effective April 19, 2028\n- glass breakage loss on: May 10, 2028\n- days from the policy start date to the loss: 226 days\n- days from the rider effective date to the loss: 21 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, did the glass breakage loss for Aiko Brandt happen during the waiting period?"
 },
 {
  "qid": "q4efcbe959a",
  "kind": "choice",
  "text": "{\"sent_by\": \"Owen Pryce\", \"file\": \"CASE-9556\", \"subject\": \"the appeal deadline\", \"channel\": \"routine_intake\", \"team\": \"desk\"}\n\nCase CASE-9556, party Owen Pryce:\n- billing date: September 17, 2026\n- statement date: October 17, 2026",
  "question": "Filing rule: the dispute must be filed within 34 days running from the later of the dates below: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 34 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the final day still in time for filing the dispute in case CASE-9556?",
  "options": [
   "November 19, 2026",
   "November 20, 2026",
   "November 18, 2026",
   "October 21, 2026"
  ]
 },
 {
  "qid": "q84a92acd1c",
  "kind": "choice",
  "text": "Memo for the duty clerk: Lucas Brenner has passed on file STAY-4800 about the visa stay count. Courteous handling is appreciated.\n\nStay record STAY-4800 for Lucas Brenner:\n- entry day Monday, September 14, 2026, exit day Thursday, September 24, 2026 (whole stay: eleven days)\n- entry day Sunday, September 27, 2026, exit day Friday, December 25, 2026 (whole stay: 90 days)\nReference date: Saturday, February 20, 2027\nWindow checked: Saturday, October 24, 2026 to Saturday, February 20, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days in any 120-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present fall inside the checked window that ends on Saturday, February 20, 2027 for file STAY-4800?",
  "options": [
   "63 days",
   "62 days"
  ]
 },
 {
  "qid": "q35e36cbffa",
  "kind": "yes/no",
  "text": "Felix Ortega: file POL-9693 about the insurance claim is here.\nintake team: received, thanks.\nintake team: that is everything for this file.\n\nPolicy POL-9693, holder Felix Ortega:\n- policy start date: 2026-10-11\n- glass breakage cover: part of the base policy\n- glass breakage loss on: 2026-10-14\n- days from the policy start date to the loss: 3 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the cover rule does not pay for the glass breakage loss on policy POL-9693?"
 },
 {
  "qid": "q1fade5c3f0",
  "kind": "choice",
  "text": "Subject: Quick send on the response deadline\n\nHi help desk,\n\nSending file NTC-1943 from Owen Pryce your way, quick handoff. Keep it moving.\n\nThanks,\n\nNotice NTC-1943 to Owen Pryce:\n- response due date: June 5, 2027\n- office cutoff on the due date: 5 June 2027, 12:26 (UTC-04:00)\n- response sent: 6 June 2027, 13:31 (UTC-03:00) [same instant in office time: 6 June 2027, 12:31 (UTC-04:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn which date, under the receipt rule, does the office count the response to notice NTC-1943 as received?",
  "options": [
   "2027-06-07",
   "2027-06-08"
  ]
 },
 {
  "qid": "q27dad2db8a",
  "kind": "yes/no",
  "text": "{\"file\": \"CASE-1178\", \"sent_by\": \"Paolo Greco\", \"subject\": \"the appeal deadline\", \"channel\": \"case team\"}\n\nCase CASE-1178, party Paolo Greco:\n- decision date: 7 Feb 2027\n- delivery date: 24 Mar 2027\n- appeal filed on: 24 Apr 2027\n- days from the decision date to the filing: 76 days\n- days from the delivery date to the filing: 31 days",
  "question": "Filing rule: the appeal must be filed within 30 days following the later of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Paolo Greco fail to file the appeal in case CASE-1178 by the deadline?"
 },
 {
  "qid": "q403631c43a",
  "kind": "yes/no",
  "text": "Memo for the front desk: Jonas Feld sends file CASE-4173 about the appeal deadline. Grab it at your convenience, the queue is busy on this end.\n\nCase CASE-4173, party Jonas Feld:\n- decision date: 2025-10-11\n- delivery date: 2025-11-01\n- appeal filed on: 2026-01-30\n- days from the decision date to the filing: 111 days\n- days from the delivery date to the filing: 90 days",
  "question": "Filing rule: the appeal must be filed inside 90 days extending past the later of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is it true that the appeal in case CASE-4173 was not filed in time?"
 },
 {
  "qid": "qc683d3171e",
  "kind": "choice",
  "text": "[log] from=Owen Pryce ref_file=CASE-8955 to=records_clerk\n[log] about=the appeal deadline routine_transfer\n\nCase CASE-8955, party Owen Pryce:\n- decision date: 24 Mar 2027\n- delivery date: 3 Mar 2027",
  "question": "Filing rule: the appeal must be filed inside 46 days reckoned from the date that falls later among the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 46 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, by which final day can Owen Pryce still file the appeal and remain in time?",
  "options": [
   "9 May 2027",
   "18 Apr 2027",
   "8 May 2027"
  ]
 },
 {
  "qid": "qab33ec632f",
  "kind": "yes/no",
  "text": "[help] Kofi Mensah sent in file NTC-9055 about the response deadline\n[desk] help_desk move fast\n\nNotice NTC-9055 to Kofi Mensah:\n- response due date: November 27, 2026\n- office cutoff on the due date: 2026-11-27T22:54:00-05:00\n- response sent: 2026-11-28T11:56:00+08:00 [same instant in office time: 2026-11-27T22:56:00-05:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Kofi Mensah to notice NTC-9055 on time under the receipt rule?"
 },
 {
  "qid": "q7f4bb3a002",
  "kind": "yes/no",
  "text": "title | kind request for the records clerk\nrequester | Malik Osei\nfile | STAY-1120\nPlease find the visa stay count attached for your review.\n\nStay record STAY-1120 for Malik Osei:\n- entry day 9 February 2027, exit day 24 February 2027 (whole stay: sixteen days)\n- entry day 27 February 2027, exit day 28 April 2027 (whole stay: 61 days)\nReference date: 26 June 2027\nWindow checked: 27 February 2027 to 26 June 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days in every 120-day run that moves forward through time. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the person in file STAY-1120 over the stay limit, meaning more days present inside the checked window ending on the reference date than the limit?"
 }
]
