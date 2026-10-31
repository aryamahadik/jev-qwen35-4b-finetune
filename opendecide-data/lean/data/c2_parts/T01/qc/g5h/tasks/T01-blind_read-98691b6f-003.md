# G5-H blind read (all free-form rows) T01-blind_read-98691b6f-003 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g5h/answers/T01-blind_read-98691b6f-003.json

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
  "qid": "qda138796bc",
  "kind": "yes/no",
  "text": "Jonas Feld sent file STAY-2500 about the visa stay count to the desk. The file is shared as part of the usual exchange. This is routine and straightforward.\n\nStay record STAY-2500 for Jonas Feld:\n- entry day Saturday, 4 April 2026, exit day Tuesday, 28 April 2026 (whole stay: 25 days)\n- entry day Monday, 18 May 2026, exit day Thursday, 21 May 2026 (whole stay: four days)\nReference date: Tuesday, 9 June 2026\nWindow checked: Saturday, 11 April 2026 to Tuesday, 9 June 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 21 days within any 60-day window that keeps moving. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does Jonas Feld have more days present in the checked window ending on Tuesday, 9 June 2026 than the stay limit?"
 },
 {
  "qid": "q17fd6ccf2f",
  "kind": "choice",
  "text": "Dear front desk,\nEva Marsh is sending file POL-7886 about the cover question. The file is attached here for your records. I appreciate the help with it.\nKind regards,\n\nPolicy POL-7886, holder Eva Marsh:\n- policy start date: 23 Mar 2026\n- flood damage cover: added by a rider effective 3 Sep 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days whose opening count lands on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which the flood damage loss in policy POL-7886 would be covered under the cover rule?",
  "options": [
   "3 Oct 2026",
   "2 Oct 2026",
   "23 Apr 2026",
   "4 Oct 2026"
  ]
 },
 {
  "qid": "q6b2ded9ab1",
  "kind": "choice",
  "text": "Theo Kalnins: file POL-5186 about the insurance claim is attached here.\ncase team: thank you, that is received.\ncase team: kind regards.\n\nPolicy POL-5186, holder Theo Kalnins:\n- policy start date: Sunday, December 12, 2027\n- glass breakage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 90 days that picks up on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 90 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on what earliest date would the glass breakage loss be covered?",
  "options": [
   "Friday, March 10, 2028",
   "Saturday, April 15, 2028",
   "Sunday, March 12, 2028"
  ]
 },
 {
  "qid": "q776da55500",
  "kind": "choice",
  "text": "Lena Whitcombe: Quick send of LED-1954 about the teller ledger review.\nservice desk: Thanks, that is in.\n\nCash ledger LED-1954, teller Lena Whitcombe:\n- Wednesday, 5 May 2027: deposit of 5,000.00 USD\n- Wednesday, 5 May 2027: withdrawal of 1,327.00 USD\n- Wednesday, 5 May 2027: withdrawal of 3,386.00 USD\n- Thursday, 6 May 2027: deposit of 2,105.00 USD\nDay under review: Wednesday, 5 May 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is anything strictly greater than 5,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, which of the day's totals for Wednesday, 5 May 2027 call for a cash report?",
  "options": [
   "Only the withdrawal total",
   "Neither total",
   "Both totals",
   "Only the deposit total"
  ]
 },
 {
  "qid": "qa6fba2cb04",
  "kind": "yes/no",
  "text": "From: Nadia Kowal\nFile: STAY-2542\nSent to: review team\nThe file about the visa stay count is shared in the usual way.\n\nStay record STAY-2542 for Nadia Kowal:\n- entry day 2025-12-03, exit day 2025-12-06 (whole stay: 4 days)\n- entry day 2025-12-24, exit day 2026-01-19 (whole stay: 27 days)\nReference date: 2026-02-05\nWindow checked: 2025-11-08 to 2026-02-05, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 30 days during any 90-day window that moves ahead. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Nadia Kowal, under the stay rule, over the stay limit for the window ending on 2026-02-05?"
 },
 {
  "qid": "q090bbfb5b7",
  "kind": "choice",
  "text": "Dear front desk,\nInes Duarte is sending file CASE-7437 about the appeal deadline. This is a routine send and the file is full. The matter is in good shape as usual.\nRegards\n\nCase CASE-7437, party Ines Duarte:\n- decision date: 22 Aug 2025\n- delivery date: 25 Aug 2025",
  "question": "Filing rule: the appeal must be filed within 45 days after the later date out of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, by which final day can Ines Duarte still file the appeal and remain in time?",
  "options": [
   "9 Oct 2025",
   "11 Oct 2025",
   "10 Oct 2025",
   "6 Oct 2025"
  ]
 },
 {
  "qid": "q7156f48ec3",
  "kind": "yes/no",
  "text": "Ravi Anand: sending STAY-1179 about the residence day count, in a rush.\nservice desk: got it, thanks.\ndesk: that is the full file.\n\nStay record STAY-1179 for Ravi Anand:\n- entry day Monday, November 23, 2026, exit day Sunday, November 29, 2026 (whole stay: 7 days)\n- entry day Monday, December 28, 2026, exit day Wednesday, January 6, 2027 (whole stay: 10 days)\n- entry day Wednesday, January 20, 2027, exit day Sunday, January 31, 2027 (whole stay: 12 days)\nReference date: Sunday, February 7, 2027\nWindow checked: Thursday, December 10, 2026 to Sunday, February 7, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 21 days inside every moving 60-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is Ravi Anand over the stay limit in record STAY-1179 when counting just the checked window that ends on the reference date?"
 },
 {
  "qid": "q0b0adf9793",
  "kind": "yes/no",
  "text": "Hi admin team, this is Sara Ilves sharing file CASE-5005 about the complaint filing. It was a pleasure to pull it together. Thanks for keeping an eye on it.\n\nCase CASE-5005, party Sara Ilves:\n- incident date: July 1, 2025\n- discovery date: June 17, 2025\n- complaint filed on: July 11, 2025\n- days from the incident date to the filing: 10 days\n- days from the discovery date to the filing: 24 days",
  "question": "Filing rule: the complaint must be filed within 21 days measured beyond the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the complaint filed by Sara Ilves in time, on or before the final day of the filing period?"
 },
 {
  "qid": "q68573b0bd8",
  "kind": "yes/no",
  "text": "Dear front desk,\nTomas Lindqvist is sending file CASE-2258 about the appeal deadline. The file is attached here for your records. I appreciate the help with it.\nKind regards,\n\nCase CASE-2258, party Tomas Lindqvist:\n- decision date: 12 Aug 2027\n- delivery date: 7 Aug 2027\n- appeal filed on: 31 Aug 2027\n- days from the decision date to the filing: 19 days\n- days from the delivery date to the filing: 24 days",
  "question": "Filing rule: the appeal must be filed within 10 days past the later of the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 10 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the appeal filed on or before the final day of the filing period?"
 },
 {
  "qid": "qc4fb7a818e",
  "kind": "yes/no",
  "text": "Internal memo for the desk.\n\nClara Weiss sends file POL-9260 about the insurance claim to the desk, with the review team copied in. Thank you for your careful work on this matter. I appreciate the effort put into it.\n\nPolicy POL-9260, holder Clara Weiss:\n- policy start date: 2027-10-11\n- power surge damage cover: added by a rider effective 2028-02-07\n- power surge damage loss on: 2028-03-23\n- days from the policy start date to the loss: 164 days\n- days from the rider effective date to the loss: 45 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days whose earliest counted day is the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, did the power surge damage loss happen inside the waiting period?"
 },
 {
  "qid": "qa67dacfaa3",
  "kind": "choice",
  "text": "From: Clara Weiss\nFile: CASE-8179\nSent to: records clerk\nThis file about the appeal deadline is sent over in a hurry. Thanks.\n\nCase CASE-8179, party Clara Weiss:\n- decision date: 26 Nov 2026\n- delivery date: 12 Oct 2026",
  "question": "Filing rule: the appeal must be filed within 10 days running from the later of the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 10 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the final day still in time for filing the appeal in case CASE-8179?",
  "options": [
   "5 Dec 2026",
   "6 Dec 2026",
   "22 Oct 2026"
  ]
 },
 {
  "qid": "q9444399d28",
  "kind": "choice",
  "text": "Dear front desk team,\n\nMy name is Mira Castell, and I am writing to send file POL-4150 about the loss claim.\n\nThe file is attached below. Thank you for your help with this matter.\n\nKind regards,\n\nPolicy POL-4150, holder Mira Castell:\n- policy start date: Thursday, 6 May 2027\n- theft cover: added by a rider effective Friday, 13 August 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date, under the cover rule, from which the theft loss would be covered?",
  "options": [
   "Saturday, 25 September 2027",
   "Sunday, 12 September 2027",
   "Monday, 13 September 2027"
  ]
 },
 {
  "qid": "q5308ec844d",
  "kind": "yes/no",
  "text": "Ana Ruiz: hi! Here is POL-4784 about the cover question.\nhelp desk: lovely, received.\nhelp desk: great, enjoy your work.\n\nPolicy POL-4784, holder Ana Ruiz:\n- policy start date: Tuesday, November 3, 2026\n- storm damage cover: added by a rider effective Saturday, January 23, 2027\n- storm damage loss on: Sunday, February 7, 2027\n- days from the policy start date to the loss: 96 days\n- days from the rider effective date to the loss: 15 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days starting with the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is the storm damage loss in policy POL-4784 covered?"
 },
 {
  "qid": "q5588aa02af",
  "kind": "yes/no",
  "text": "Dear duty clerk,\nOwen Pryce is sending file NTC-9710 about the notice response. The file is attached for your desk. Thanks in advance for your help.\nBest,\n\nNotice NTC-9710 to Owen Pryce:\n- response due date: Sunday, September 17, 2028\n- office cutoff on the due date: 2028-09-17 12:54:00 +0530\n- response sent: 2028-09-17 16:29:00 +0900 [same instant in office time: 2028-09-17 12:59:00 +0530]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the response from Owen Pryce to notice NTC-9710 late, meaning counted as received after the due date?"
 },
 {
  "qid": "qafe7f481b5",
  "kind": "choice",
  "text": "Lena Whitcombe: hey, here is POL-4449 about the insurance claim, sorry for the wait!\nservice desk: all good, got it.\nservice desk: brilliant, thanks a lot.\n\nPolicy POL-4449, holder Lena Whitcombe:\n- policy start date: Thursday, December 30, 2027\n- glass breakage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the earliest date on which the glass breakage loss for Lena Whitcombe would be covered?",
  "options": [
   "Friday, January 21, 2028",
   "Saturday, January 22, 2028",
   "Wednesday, January 19, 2028"
  ]
 },
 {
  "qid": "q4c08eb8f55",
  "kind": "yes/no",
  "text": "Sent by: Lena Whitcombe\nFile: PO-2444\nSent to: records clerk\nShort note, my queue is packed. The file is about the purchase request and is attached.\n\nPurchase log PO-2444, kept by Lena Whitcombe, vendor Corvane Office:\n- earlier purchase on 2026-06-13: $5,262.00\n- earlier purchase on 2026-09-20: $2,740.00\n- earlier purchase on 2026-10-03: $248.00\n- earlier purchase on 2026-12-02: $4,545.00\n- new request on 2026-12-15: $7,467.00\nWindow checked: 2026-09-17 to 2026-12-15, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is a figure greater than $15,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the request from Lena Whitcombe, under the purchase rule, call for written quotes in log PO-2444?"
 },
 {
  "qid": "q364e9a5162",
  "kind": "yes/no",
  "text": "Priya Raman sends file STAY-4453 about the residence day count to the desk. The file keeps to the standard format. A full copy sits with the desk too.\n\nStay record STAY-4453 for Priya Raman:\n- entry day Thursday, November 13, 2025, exit day Saturday, November 29, 2025 (whole stay: seventeen days)\n- entry day Thursday, December 11, 2025, exit day Tuesday, March 10, 2026 (whole stay: 90 days)\nReference date: Friday, May 8, 2026\nWindow checked: Friday, January 9, 2026 to Friday, May 8, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days in each 120-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Priya Raman over the stay limit, counting the days present inside the window that ends on Friday, May 8, 2026?"
 },
 {
  "qid": "q7a46690b61",
  "kind": "choice",
  "text": "Hey there, quick heads up that Eva Marsh has sent file STAY-5741 about the border stay check to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.\n\nStay record STAY-5741 for Eva Marsh:\n- entry day Wednesday, June 16, 2027, exit day Wednesday, July 14, 2027 (whole stay: 29 days)\n- entry day Monday, August 16, 2027, exit day Friday, August 27, 2027 (whole stay: twelve days)\nReference date: Friday, October 8, 2027\nWindow checked: Sunday, July 11, 2027 to Friday, October 8, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 30 days in each 90-day window that moves forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days present does Eva Marsh have inside the checked window ending on Friday, October 8, 2027?",
  "options": [
   "16 days",
   "41 days",
   "17 days"
  ]
 },
 {
  "qid": "qf081b628ec",
  "kind": "yes/no",
  "text": "Hi front desk,\nKofi Mensah sends file STAY-4085 about the border stay check as a standard copy. The file keeps to the usual format.\nRegards,\n\nStay record STAY-4085 for Kofi Mensah:\n- entry day 26 Feb 2026, exit day 13 Apr 2026 (whole stay: 47 days)\nReference date: 25 Jun 2026\nWindow checked: 28 Mar 2026 to 25 Jun 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 30 days during any 90-day window that moves ahead. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Kofi Mensah over the stay limit, with more days present inside the window that ends on the reference date in file STAY-4085, under the stay rule?"
 },
 {
  "qid": "q11732897f4",
  "kind": "yes/no",
  "text": "Hi admin team, Paolo Greco here with file PO-5680 about the purchase request. Thanks so much for helping keep everything tidy. It is a pleasure to share it with you all.\n\nPurchase log PO-5680, kept by Paolo Greco, vendor Corvane Office:\n- earlier purchase on 2027-10-29: $2,084.00\n- earlier purchase on 2028-02-22: $5,318.00\n- new request on 2028-03-14: $4,682.00\nWindow checked: 2028-01-15 to 2028-03-14, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is greater than $10,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request from Paolo Greco need written quotes under the purchase rule?"
 },
 {
  "qid": "qe92a239931",
  "kind": "yes/no",
  "text": "Yara Haddad: Sending LED-9332 about the teller ledger review, a routine send.\nintake team: Received, thanks.\n\nCash ledger LED-9332, teller Yara Haddad:\n- 5 Nov 2027: withdrawal of 7,561.00 USD\n- 6 Nov 2027: withdrawal of 15,000.00 USD\n- 6 Nov 2027: deposit of 15,000.00 USD\nDay under review: 6 Nov 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any amount that is more than 15,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is a cash report required for 6 Nov 2027 in ledger LED-9332?"
 },
 {
  "qid": "qf882be4f6e",
  "kind": "yes/no",
  "text": "Sent by: Mira Castell\nFile: CASE-7642\nSent to: records clerk\nHappy to share the file about the appeal deadline, it was fun to put together. Hope it helps with the sorting.\n\nCase CASE-7642, party Mira Castell:\n- billing date: 24 Sep 2027\n- statement date: 17 Sep 2027\n- dispute filed on: 3 Nov 2027\n- days from the billing date to the filing: 40 days\n- days from the statement date to the filing: 47 days",
  "question": "Filing rule: the dispute must be filed within 21 days measured from the later of the dates below: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the dispute filed on or before the final day of the filing period?"
 },
 {
  "qid": "q7466316725",
  "kind": "choice",
  "text": "Aiko Brandt: Hello, I am sending file NTC-4941 about the notice response to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nNotice NTC-4941 to Aiko Brandt:\n- response due date: 26 October 2025\n- office cutoff on the due date: 2025-10-26T22:52:00+02:00\n- response sent: 2025-10-25T04:53:00+08:00 [same instant in office time: 2025-10-24T22:53:00+02:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn which date, under the receipt rule, does the office count the response from Aiko Brandt to notice NTC-4941 as received?",
  "options": [
   "October 25, 2025",
   "October 26, 2025"
  ]
 },
 {
  "qid": "qcc153448b8",
  "kind": "choice",
  "text": "Eva Marsh: Quick send of POL-6838 about the insurance claim.\nservice desk: Thanks, that is in.\n\nPolicy POL-6838, holder Eva Marsh:\n- policy start date: 27 Apr 2026\n- theft cover: added by a rider effective 15 May 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days whose earliest counted day is the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date, under the cover rule, from which the theft loss would be covered?",
  "options": [
   "1 Jul 2026",
   "30 Jun 2026",
   "12 Jun 2026"
  ]
 },
 {
  "qid": "qc7a2456d1c",
  "kind": "yes/no",
  "text": "Hiya admin team, Ines Duarte has sent file STAY-6225 about the border stay check. Hope you are all well and enjoying the work. This is just a simple pass along with every bit in place. Thanks a bunch for taking it in, lovely to share this with you.\n\nStay record STAY-6225 for Ines Duarte:\n- entry day 27 May 2027, exit day 11 July 2027 (whole stay: 46 days)\nReference date: 24 August 2027\nWindow checked: 27 May 2027 to 24 August 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 45 days in every 90-day run that moves forward through time. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does Ines Duarte have more days present in the checked window ending on 24 August 2027 than the stay limit?"
 },
 {
  "qid": "q740668937d",
  "kind": "choice",
  "text": "Maya Lindgren: Quick send of CASE-9517 about the claim deadline question.\nservice desk: Thanks, that is in.\n\nCase CASE-9517, party Maya Lindgren:\n- inspection date: 25 Aug 2026\n- report date: 15 Sep 2026",
  "question": "Filing rule: the objection must be filed within fourteen days starting from the later of the dates listed below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is fourteen days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, by which final day can Maya Lindgren still file the objection and remain in time?",
  "options": [
   "5 Oct 2026",
   "29 Sep 2026",
   "28 Sep 2026"
  ]
 },
 {
  "qid": "qd192db8a46",
  "kind": "choice",
  "text": "From: Nadia Kowal\nFile: POL-8668\nSent to: review team\nThe file about the insurance claim is shared in the usual way.\n\nPolicy POL-8668, holder Nadia Kowal:\n- policy start date: 16 Dec 2026\n- glass breakage cover: added by a rider effective 25 Mar 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days that begins on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which a loss of this kind would count as covered for policy POL-8668 under the cover rule?",
  "options": [
   "12 May 2027",
   "11 May 2027",
   "10 May 2027"
  ]
 },
 {
  "qid": "qe6f1f1fd38",
  "kind": "choice",
  "text": "Hi front desk,\nMira Castell sends file STAY-6743 about the border stay check in the usual form. The file sits in the standard layout alongside the other sheets.\nRegards,\n\nStay record STAY-6743 for Mira Castell:\n- entry day Monday, July 28, 2025, exit day Monday, August 11, 2025 (whole stay: 15 days)\n- entry day Monday, September 15, 2025, exit day Thursday, October 2, 2025 (whole stay: 18 days)\nReference date: Thursday, November 6, 2025\nWindow checked: Saturday, August 9, 2025 to Thursday, November 6, 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 30 days inside any moving 90-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present for Mira Castell fall inside the checked window ending on Thursday, November 6, 2025?",
  "options": [
   "21 days",
   "33 days",
   "23 days"
  ]
 },
 {
  "qid": "q1f46ef3a0e",
  "kind": "yes/no",
  "text": "Dear front desk,\nKofi Mensah is sending file STAY-4085 about the border stay check. This is a routine send and the file is full. The matter is in good shape as usual.\nRegards\n\nStay record STAY-4085 for Kofi Mensah:\n- entry day 26 Feb 2026, exit day 13 Apr 2026 (whole stay: 47 days)\nReference date: 25 Jun 2026\nWindow checked: 28 Mar 2026 to 25 Jun 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 30 days during any 90-day window that moves ahead. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Kofi Mensah over the stay limit, with more days present inside the window that ends on the reference date in file STAY-4085, under the stay rule?"
 },
 {
  "qid": "qc8a9133c0e",
  "kind": "yes/no",
  "text": "Hey there, quick heads up that Sara Ilves has sent file STAY-8062 about the border stay check to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.\n\nStay record STAY-8062 for Sara Ilves:\n- entry day Monday, February 1, 2027, exit day Sunday, March 21, 2027 (whole stay: 49 days)\n- entry day Thursday, April 8, 2027, exit day Sunday, April 25, 2027 (whole stay: 18 days)\nReference date: Friday, May 14, 2027\nWindow checked: Sunday, February 14, 2027 to Friday, May 14, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 45 days in each 90-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Sara Ilves over the stay limit, counting the days present inside the window that ends on Friday, May 14, 2027?"
 },
 {
  "qid": "q4df420f785",
  "kind": "yes/no",
  "text": "Theo Kalnins: Hello, I am sending file POL-2302 about the cover question to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nPolicy POL-2302, holder Theo Kalnins:\n- policy start date: 2027-05-31\n- burst pipe damage cover: added by a rider effective 2027-06-10\n- burst pipe damage loss on: 2027-08-23\n- days from the policy start date to the loss: 84 days\n- days from the rider effective date to the loss: 74 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days whose opening count lands on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does the cover rule count the loss on policy POL-2302 as covered?"
 },
 {
  "qid": "q17879857f3",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nHana Sato is sending file PO-8837 about the purchase request. Writing fast, I am swamped. Attached is the file.\nThanks,\n\nPurchase log PO-8837, kept by Hana Sato, vendor Corvane Office:\n- earlier purchase on 2025-08-19: $481\n- earlier purchase on 2025-09-21: $2,461\n- new request on 2025-12-19: $540\nWindow checked: 2025-09-21 to 2025-12-19, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is strictly more than $3,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, may request PO-8837 go ahead without written quotes under the purchase rule?"
 },
 {
  "qid": "q1d4033c824",
  "kind": "choice",
  "text": "Yara Haddad: hey, here is CASE-1732 about the appeal deadline, sorry for the wait!\nservice desk: all good, got it.\nservice desk: brilliant, thanks a lot.\n\nCase CASE-1732, party Yara Haddad:\n- decision date: Monday, 6 March 2028\n- delivery date: Friday, 25 February 2028",
  "question": "Filing rule: the appeal must be filed within 60 days measured from the later of the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUntil which date, under the filing rule, may Yara Haddad file the appeal in time?",
  "options": [
   "Sunday, 7 May 2028",
   "Thursday, 4 May 2028",
   "Friday, 5 May 2028"
  ]
 },
 {
  "qid": "qadd2079481",
  "kind": "yes/no",
  "text": "File: STAY-7559\nSubject: the visa stay count\nFrom: Felix Ortega\nThis file is respectfully passed to the review team. With warm thanks for your attention.\n\nStay record STAY-7559 for Felix Ortega:\n- entry day 2026-05-22, exit day 2026-05-25 (whole stay: 4 days)\n- entry day 2026-06-03, exit day 2026-08-23 (whole stay: 82 days)\nReference date: 2026-10-09\nWindow checked: 2026-06-12 to 2026-10-09, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days within any 120-day window that keeps moving. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is Felix Ortega over the stay limit, with more days present in the checked window ending on the reference date?"
 },
 {
  "qid": "qfc4da520a4",
  "kind": "yes/no",
  "text": "Aiko Brandt: Quick send, NTC-3938 about the reply timing question.\nhelp desk: Got it.\n\nNotice NTC-3938 to Aiko Brandt:\n- response due date: October 18, 2025\n- office cutoff on the due date: 2025-10-18 13:03:00 +0900\n- response sent: 2025-10-18 14:56:00 -0300 [same instant in office time: 2025-10-19 02:56:00 +0900]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response to notice NTC-3938 on time under the receipt rule?"
 },
 {
  "qid": "q3b5a8ec2b9",
  "kind": "choice",
  "text": "File: STAY-9185\nSubject: the residence day count\nFrom: Malik Osei\nSending this straight across to the records clerk. The desk is very busy and stretched.\n\nStay record STAY-9185 for Malik Osei:\n- entry day December 20, 2025, exit day February 3, 2026 (whole stay: 46 days)\n- entry day February 26, 2026, exit day February 27, 2026 (whole stay: 2 days)\nReference date: March 19, 2026\nWindow checked: January 19, 2026 to March 19, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 21 days in any rolling 60-day window. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, how many days present for Malik Osei fall inside the checked window that ends on the reference date?",
  "options": [
   "16 days",
   "18 days",
   "17 days"
  ]
 },
 {
  "qid": "q7e7fe6cf97",
  "kind": "choice",
  "text": "Hana Sato: Hey, sending POL-8237 about the cover question, hope all is well!\nhelp desk: Lovely, thanks for sending it across.\n\nPolicy POL-8237, holder Hana Sato:\n- policy start date: 22 Dec 2026\n- fire damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 10 days whose clock starts running on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 10 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the earliest date on which the fire damage loss under policy POL-8237 would be covered?",
  "options": [
   "6 Jan 2027",
   "2 Jan 2027",
   "4 Jan 2027"
  ]
 },
 {
  "qid": "qa8ea2c0150",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nPriya Raman is sending file POL-2847 about the loss claim. Writing fast, I am swamped. Attached is the file.\nThanks,\n\nPolicy POL-2847, holder Priya Raman:\n- policy start date: Monday, 22 November 2027\n- burst pipe damage cover: part of the base policy\n- burst pipe damage loss on: Thursday, 6 January 2028\n- days from the policy start date to the loss: 45 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days with the start date itself left out, beginning the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is the burst pipe damage loss for Priya Raman covered under the cover rule?"
 },
 {
  "qid": "qe421b8c332",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nHope you are doing great! Malik Osei has sent file NTC-6006 about the reply timing question, all lovely and tidy. Just wanted to pop it in your inbox. Catch you round.\nCheers\n\nNotice NTC-6006 to Malik Osei:\n- response due date: Tuesday, 27 May 2025\n- office cutoff on the due date: 27 May 2025, 18:10 (UTC+09:00)\n- response sent: 27 May 2025, 17:05 (UTC+08:00) [same instant in office time: 27 May 2025, 18:05 (UTC+09:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Malik Osei on time under the receipt rule?"
 },
 {
  "qid": "qac2cb985ae",
  "kind": "choice",
  "text": "Yara Haddad has shared file STAY-2655 about the residence day count with the desk. The file goes in the usual way. This memo is for the file set.\n\nStay record STAY-2655 for Yara Haddad:\n- entry day 9 Aug 2027, exit day 9 Aug 2027 (whole stay: 1 day)\n- entry day 13 Aug 2027, exit day 21 Oct 2027 (whole stay: 70 days)\nReference date: 3 Jan 2028\nWindow checked: 6 Sep 2027 to 3 Jan 2028, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 60 days inside every moving 120-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days present, under the stay rule, fall inside the checked window that ends on the reference date in file STAY-2655?",
  "options": [
   "45 days",
   "46 days"
  ]
 },
 {
  "qid": "q65060d57fd",
  "kind": "choice",
  "text": "File: POL-1256\nSubject: the insurance claim\nSent by: Jonas Feld\nHey there, this goes over to the records clerk. Hope everything is going nicely for you!\n\nPolicy POL-1256, holder Jonas Feld:\n- policy start date: 2026-09-03\n- fire damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on what earliest date would the fire damage loss be covered?",
  "options": [
   "2026-09-25",
   "2026-10-03",
   "2026-09-23"
  ]
 },
 {
  "qid": "q5cb795bf7e",
  "kind": "yes/no",
  "text": "Jonas Feld sent file STAY-2500 about the visa stay count to the desk. The file is shared as part of the usual exchange. This is routine and straightforward.\n\nStay record STAY-2500 for Jonas Feld:\n- entry day Saturday, 4 April 2026, exit day Tuesday, 28 April 2026 (whole stay: 25 days)\n- entry day Monday, 18 May 2026, exit day Wednesday, 20 May 2026 (whole stay: three days)\nReference date: Tuesday, 9 June 2026\nWindow checked: Saturday, 11 April 2026 to Tuesday, 9 June 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 21 days within any 60-day window that keeps moving. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does Jonas Feld have more days present in the checked window ending on Tuesday, 9 June 2026 than the stay limit?"
 },
 {
  "qid": "qc69c2dac01",
  "kind": "yes/no",
  "text": "Sent by: Owen Pryce\nFile: PO-6374\nSent to: records clerk\nLovely to send this over, it is about the buying request. The notes are all tidy and sit nicely for the records team.\n\nPurchase log PO-6374, kept by Owen Pryce, vendor Quillon Labs:\n- earlier purchase on 10 Aug 2027: $4,818.00\n- earlier purchase on 23 Nov 2027: $3,316.00\n- earlier purchase on 24 Nov 2027: $4,805.00\n- earlier purchase on 26 Nov 2027: $1,347.00\n- new request on 23 Dec 2027: $1,406.00\nWindow checked: 24 Nov 2027 to 23 Dec 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is greater than $10,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does request PO-6374 from Owen Pryce need written quotes under the purchase rule?"
 },
 {
  "qid": "qd97a276c90",
  "kind": "choice",
  "text": "Felix Ortega: Sending POL-4673 about the cover question, short and sharp.\nservice desk: Received.\n\nPolicy POL-4673, holder Felix Ortega:\n- policy start date: 25 Jul 2027\n- subsidence cover: added by a rider effective 18 Dec 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 60 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 60 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which, under the cover rule, the subsidence loss in policy POL-4673 would be covered?",
  "options": [
   "16 Feb 2028",
   "17 Feb 2028",
   "11 Mar 2028"
  ]
 },
 {
  "qid": "q1db5645752",
  "kind": "choice",
  "text": "Dear front desk,\nMira Castell is writing to share file STAY-4433 about the residence day count with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,\n\nStay record STAY-4433 for Mira Castell:\n- entry day June 25, 2027, exit day July 13, 2027 (whole stay: 19 days)\n- entry day August 7, 2027, exit day August 11, 2027 (whole stay: 5 days)\nReference date: September 4, 2027\nWindow checked: July 7, 2027 to September 4, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 21 days during any 60-day window that moves ahead. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present fall inside the checked window that ends on September 4, 2027 for file STAY-4433?",
  "options": [
   "11 days",
   "12 days",
   "10 days"
  ]
 },
 {
  "qid": "qf108d73d92",
  "kind": "choice",
  "text": "File: STAY-9185\nSubject: the residence day count\nFrom: Malik Osei\nSending this straight across to the records clerk. The desk is very busy and stretched.\n\nStay record STAY-9185 for Malik Osei:\n- entry day December 20, 2025, exit day February 3, 2026 (whole stay: 46 days)\n- entry day February 26, 2026, exit day February 26, 2026 (whole stay: 1 day)\nReference date: March 19, 2026\nWindow checked: January 19, 2026 to March 19, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 21 days in any rolling 60-day window. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, how many days present for Malik Osei fall inside the checked window that ends on the reference date?",
  "options": [
   "16 days",
   "17 days",
   "15 days"
  ]
 },
 {
  "qid": "qcb277203c9",
  "kind": "choice",
  "text": "Dear duty clerk,\nQuick send from Omar Saleh: file LED-1068 about the cash ledger check is in. Sending it over fast as I am on the move. The attachment is full and whole. Thanks a bunch.\nKind regards\n\nCash ledger LED-1068, teller Omar Saleh:\n- Friday, August 11, 2028: deposit of $8,598\n- Friday, August 11, 2028: withdrawal of $3,291\n- Friday, August 11, 2028: deposit of $1,402\n- Friday, August 11, 2028: withdrawal of $821\n- Saturday, August 12, 2028: withdrawal of $7,898\nDay under review: Friday, August 11, 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is at or above $10,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, which of the day's totals recorded by Omar Saleh for Friday, August 11, 2028 call for a cash report?",
  "options": [
   "Only the deposit total",
   "Neither total",
   "Only the withdrawal total",
   "Both totals"
  ]
 },
 {
  "qid": "qf384392413",
  "kind": "choice",
  "text": "Malik Osei: file POL-2935 about the insurance claim is attached here.\ncase team: thank you, that is received.\ncase team: kind regards.\n\nPolicy POL-2935, holder Malik Osei:\n- policy start date: 2027-02-24\n- burst pipe damage cover: added by a rider effective 2027-06-04",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days whose opening count lands on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which a loss of this kind would count as covered for policy POL-2935 under the cover rule?",
  "options": [
   "2027-07-19",
   "2027-08-07",
   "2027-07-22",
   "2027-07-20"
  ]
 },
 {
  "qid": "q546b377efc",
  "kind": "yes/no",
  "text": "Mira Castell: Hello, I am sending file NTC-4691 about the reply timing question to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nNotice NTC-4691 to Mira Castell:\n- response due date: Thursday, 6 May 2027\n- office cutoff on the due date: 2027-05-06T19:24:00+00:00\n- response sent: 2027-05-07T05:19:00+10:00 [same instant in office time: 2027-05-06T19:19:00+00:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Mira Castell to notice NTC-4691 on time under the receipt rule?"
 },
 {
  "qid": "q2ac4c41a39",
  "kind": "yes/no",
  "text": "Sent by: Paolo Greco\nFile code: CASE-8945\nFor: review team\nThe file about the claim deadline question is passed along as usual.\n\nCase CASE-8945, party Paolo Greco:\n- invoice date: Monday, 24 April 2028\n- goods received date: Wednesday, 26 April 2028\n- claim filed on: Friday, 26 May 2028\n- days from the invoice date to the filing: 32 days\n- days from the goods received date to the filing: 30 days",
  "question": "Filing rule: the claim must be filed within 30 days measured beyond the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Paolo Greco, under the filing rule, file the claim on or before the final day?"
 }
]
