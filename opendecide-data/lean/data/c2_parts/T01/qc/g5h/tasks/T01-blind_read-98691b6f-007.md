# G5-H blind read (all free-form rows) T01-blind_read-98691b6f-007 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g5h/answers/T01-blind_read-98691b6f-007.json

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
  "qid": "q8a2f2503ae",
  "kind": "choice",
  "text": "Hi admin team, Omar Saleh here with file CASE-2975 about the complaint filing. Thanks so much for helping keep everything tidy. It is a pleasure to share it with you all.\n\nCase CASE-2975, party Omar Saleh:\n- purchase date: 20 Apr 2028\n- handover date: 21 Mar 2028",
  "question": "Filing rule: the refund request must be filed inside 14 days reckoned from the date that falls later among the dates below: the purchase date and the handover date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 14 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the final day on which Omar Saleh can still file the refund request in case CASE-2975 and be in time?",
  "options": [
   "4 May 2028",
   "6 May 2028",
   "2 May 2028"
  ]
 },
 {
  "qid": "qe126207cd7",
  "kind": "choice",
  "text": "Mira Castell: Sending STAY-3307 about the residence day count as usual.\ncase team: Received.\n\nStay record STAY-3307 for Mira Castell:\n- entry day June 5, 2026, exit day July 22, 2026 (whole stay: 48 days)\nReference date: October 20, 2026\nWindow checked: June 23, 2026 to October 20, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days in each 120-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days present fall inside the checked window that ends on the reference date in record STAY-3307?",
  "options": [
   "30 days",
   "29 days"
  ]
 },
 {
  "qid": "qb201d2c3fd",
  "kind": "yes/no",
  "text": "Sent by: Hana Sato\nFile: POL-9833\nSent to: records clerk\nFast message from me, the inbox is overflowing. The file is about the insurance claim and is attached.\n\nPolicy POL-9833, holder Hana Sato:\n- policy start date: Wednesday, January 5, 2028\n- theft cover: added by a rider effective Monday, May 8, 2028\n- theft loss on: Friday, May 19, 2028\n- days from the policy start date to the loss: 135 days\n- days from the rider effective date to the loss: 11 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 10 days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 10 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the theft loss, under the cover rule, covered?"
 },
 {
  "qid": "q7777ba4da3",
  "kind": "yes/no",
  "text": "Theo Kalnins: Hello, I am sending file POL-2302 about the cover question to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nPolicy POL-2302, holder Theo Kalnins:\n- policy start date: 2027-05-31\n- burst pipe damage cover: added by a rider effective 2027-06-10\n- burst pipe damage loss on: 2027-06-24\n- days from the policy start date to the loss: 24 days\n- days from the rider effective date to the loss: 14 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days whose opening count lands on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does the cover rule count the loss on policy POL-2302 as covered?"
 },
 {
  "qid": "q6fe7b1df6d",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nTomas Lindqvist sends file PO-2289 about the supplier order with a cheerful hello. The file is in the usual layout and is fun to read.\nCheers,\n\nPurchase log PO-2289, kept by Tomas Lindqvist, vendor Halden Tools:\n- earlier purchase on 13 Apr 2026: 1,765.00 USD\n- earlier purchase on 29 Apr 2026: 14,208.00 USD\n- new request on 10 May 2026: 9,028.00 USD\nWindow checked: 12 Mar 2026 to 10 May 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is anything strictly greater than 25,000.00 USD, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request from Tomas Lindqvist need written quotes under the purchase rule?"
 },
 {
  "qid": "q2d5892004b",
  "kind": "choice",
  "text": "Theo Kalnins sends file PO-3727 about the purchase request to the desk. This is the regular copy in the usual layout. The desk holds the full set in the standard format. Passing it along as the usual step.\n\nPurchase log PO-3727, kept by Theo Kalnins, vendor Vantmoor Electric:\n- earlier purchase on 18 Oct 2026: 2,463.00 USD\n- earlier purchase on 10 Nov 2026: 3,058.00 USD\n- earlier purchase on 15 Nov 2026: 909.00 USD\n- new request on 26 Nov 2026: 2,309.00 USD\nWindow checked: 28 Oct 2026 to 26 Nov 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is strictly greater than 10,000.00 USD, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what total does the purchase rule compare with its threshold for Theo Kalnins, including the new request?",
  "options": [
   "8,585.00 USD",
   "8,739.00 USD",
   "6,276.00 USD"
  ]
 },
 {
  "qid": "qd96a491ad4",
  "kind": "yes/no",
  "text": "Theo Kalnins: file POL-9777 about the loss claim is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.\n\nPolicy POL-9777, holder Theo Kalnins:\n- policy start date: May 19, 2027\n- fire damage cover: added by a rider effective July 6, 2027\n- fire damage loss on: August 26, 2027\n- days from the policy start date to the loss: 99 days\n- days from the rider effective date to the loss: 51 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 10 days that begins on the next day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 10 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is the fire damage loss for Theo Kalnins covered under the cover rule?"
 },
 {
  "qid": "q76123243f3",
  "kind": "yes/no",
  "text": "Mira Castell: Hello, I am sending file NTC-4691 about the reply timing question to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nNotice NTC-4691 to Mira Castell:\n- response due date: Thursday, 6 May 2027\n- office cutoff on the due date: 2027-05-06T19:24:00+00:00\n- response sent: 2027-05-07T05:19:00+10:00 [same instant in office time: 2027-05-06T19:19:00+00:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Mira Castell, under the receipt rule, late for notice NTC-4691?"
 },
 {
  "qid": "q2a321afa12",
  "kind": "choice",
  "text": "Maya Lindgren sends file POL-8818 about the cover question to the desk. With thanks for your attention, the material is laid out with care. Respectfully yours.\n\nPolicy POL-8818, holder Maya Lindgren:\n- policy start date: 2027-08-20\n- storm damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days commencing on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich is the earliest date that this storm damage loss under policy POL-8818 would be covered?",
  "options": [
   "2027-09-04",
   "2027-09-02",
   "2027-09-03"
  ]
 },
 {
  "qid": "q7934e5e659",
  "kind": "yes/no",
  "text": "Dear front desk,\nTomas Lindqvist is writing to share file NTC-3368 about the notice response with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,\n\nNotice NTC-3368 to Tomas Lindqvist:\n- response due date: Tuesday, 29 September 2026\n- office cutoff on the due date: 2026-09-29 19:47:00 +0300\n- response sent: 2026-09-29 08:37:00 -0300 [same instant in office time: 2026-09-29 14:37:00 +0300]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Tomas Lindqvist late, since the office recorded it as received after the due date under the receipt rule?"
 },
 {
  "qid": "qf48b216f53",
  "kind": "choice",
  "text": "Dear front desk,\nMalik Osei is writing to share file POL-2484 about the loss claim with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,\n\nPolicy POL-2484, holder Malik Osei:\n- policy start date: 2027-07-14\n- fire damage cover: added by a rider effective 2027-10-02",
  "question": "Cover rule: a loss is covered only after a waiting period of 7 days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 7 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the earliest date on which this fire damage loss for Malik Osei would be covered?",
  "options": [
   "2027-10-12",
   "2027-10-11",
   "2027-10-10"
  ]
 },
 {
  "qid": "qd02131c505",
  "kind": "choice",
  "text": "File: LED-3605\nSubject: the branch cash review\nFrom: Iris Vance\nThis file goes to the review team as a routine item. It is sent in the usual way.\n\nCash ledger LED-3605, teller Iris Vance:\n- 9 Apr 2028: deposit of 8,395.00 USD\n- 10 Apr 2028: withdrawal of 7,617.00 USD\n- 11 Apr 2028: withdrawal of 7,108.00 USD\n- 11 Apr 2028: deposit of 1,051.00 USD\n- 11 Apr 2028: withdrawal of 1,036.00 USD\n- 11 Apr 2028: deposit of 4,859.00 USD\nDay under review: 11 Apr 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is 15,000.00 USD as a floor, greater than that counts, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nFor 11 Apr 2028, which of the day's totals, under the cash rule, call for a cash report?",
  "options": [
   "Neither total",
   "Both totals",
   "Only the deposit total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q9ab33a90c4",
  "kind": "yes/no",
  "text": "Hana Sato: Hello, I am sending file CASE-9581 about the appeal deadline to the case team, with thanks.\nteam: Thank you for the careful note.\nteam: Your gesture is warmly felt.\n\nCase CASE-9581, party Hana Sato:\n- billing date: September 15, 2027\n- statement date: October 6, 2027\n- dispute filed on: November 4, 2027\n- days from the billing date to the filing: 50 days\n- days from the statement date to the filing: 29 days",
  "question": "Filing rule: the dispute must be filed inside 28 days that elapses after whichever of the dates below is later: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, did Hana Sato fail to file the dispute in case CASE-9581 in time?"
 },
 {
  "qid": "q50e80cb4dd",
  "kind": "choice",
  "text": "Bruno Lacerda: file LED-6523 about the cash ledger check is attached.\ncase team: received, thanks.\ncase team: that is the whole file.\n\nCash ledger LED-6523, teller Bruno Lacerda:\n- January 20, 2026: deposit of 1,132.00 USD\n- January 22, 2026: deposit of 1,237.00 USD\n- January 22, 2026: withdrawal of 2,551.00 USD\n- January 22, 2026: deposit of 5,791.00 USD\n- January 23, 2026: withdrawal of 1,925.00 USD\nDay under review: January 22, 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is a figure of 5,000.00 USD or greater, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals on January 22, 2026 in ledger LED-6523, under the cash rule, call for a cash report?",
  "options": [
   "Only the deposit total",
   "Both totals",
   "Neither total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "qf39d25d42d",
  "kind": "yes/no",
  "text": "Sent by: Sara Ilves\nFile: POL-8734\nSent to: review team\nThank you for your attention to the file about the insurance claim. I remain grateful for the careful reading.\n\nPolicy POL-8734, holder Sara Ilves:\n- policy start date: Sunday, 3 January 2027\n- subsidence cover: added by a rider effective Thursday, 1 April 2027\n- subsidence loss on: Thursday, 15 April 2027\n- days from the policy start date to the loss: 102 days\n- days from the rider effective date to the loss: 14 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days with the start date itself left out, beginning the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the subsidence loss on policy POL-8734 covered under the cover rule?"
 },
 {
  "qid": "qdb97cad242",
  "kind": "yes/no",
  "text": "Hi front desk,\nMaya Lindgren sends file STAY-1368 about the visa stay count as a regular copy. The file follows the standard format. That covers the routine points.\nRegards,\n\nStay record STAY-1368 for Maya Lindgren:\n- entry day January 11, 2026, exit day April 24, 2026 (whole stay: 104 days)\nReference date: August 8, 2026\nWindow checked: February 10, 2026 to August 8, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 90 days in any 180-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is Maya Lindgren over the stay limit in record STAY-1368 when counting just the checked window that ends on the reference date?"
 },
 {
  "qid": "q08ad0b6654",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nHope you are doing great! Malik Osei has sent file NTC-6006 about the reply timing question, all lovely and tidy. Just wanted to pop it in your inbox. Catch you round.\nCheers\n\nNotice NTC-6006 to Malik Osei:\n- response due date: Tuesday, 27 May 2025\n- office cutoff on the due date: 27 May 2025, 18:10 (UTC+09:00)\n- response sent: 27 May 2025, 17:05 (UTC+08:00) [same instant in office time: 27 May 2025, 18:05 (UTC+09:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Malik Osei to the notice counted as received after the due date?"
 },
 {
  "qid": "qa90edfcd84",
  "kind": "yes/no",
  "text": "From: Freya Holm\nFile: STAY-5275\nSent to: review team\nI am passing on this file about the visa stay count. Thank you for your help.\n\nStay record STAY-5275 for Freya Holm:\n- entry day Sunday, March 30, 2025, exit day Thursday, May 22, 2025 (whole stay: 54 days)\n- entry day Thursday, July 3, 2025, exit day Friday, July 25, 2025 (whole stay: 23 days)\n- entry day Monday, September 8, 2025, exit day Sunday, September 21, 2025 (whole stay: 14 days)\nReference date: Saturday, October 18, 2025\nWindow checked: Tuesday, April 22, 2025 to Saturday, October 18, 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 90 days in any 180-day period that rolls forward day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is the person in file STAY-5275 over the stay limit, counting days present in the checked window ending on Saturday, October 18, 2025?"
 },
 {
  "qid": "q5903d986f6",
  "kind": "choice",
  "text": "Dear front desk,\nFreya Holm respectfully sends file STAY-5233 about the border stay check. My thanks go to you for looking at this. The file is in full and in good shape.\nYours sincerely\n\nStay record STAY-5233 for Freya Holm:\n- entry day Tuesday, November 9, 2027, exit day Wednesday, November 24, 2027 (whole stay: sixteen days)\n- entry day Saturday, December 18, 2027, exit day Thursday, December 23, 2027 (whole stay: six days)\n- entry day Tuesday, January 11, 2028, exit day Wednesday, February 9, 2028 (whole stay: 30 days)\nReference date: Tuesday, February 22, 2028\nWindow checked: Thursday, November 25, 2027 to Tuesday, February 22, 2028, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 45 days in each 90-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days present, under the stay rule, fall inside the checked window that ends on the reference date in file STAY-5233?",
  "options": [
   "38 days",
   "36 days"
  ]
 },
 {
  "qid": "qf30fbbab66",
  "kind": "yes/no",
  "text": "Aiko Brandt: sending file NTC-3386 about the response deadline, with thanks.\nintake team: thank you, this is received.\nintake team: appreciated.\n\nNotice NTC-3386 to Aiko Brandt:\n- response due date: 2027-07-04\n- office cutoff on the due date: 2027-07-04 18:48:00 +0100\n- response sent: 2027-07-04 20:43:00 +0300 [same instant in office time: 2027-07-04 18:43:00 +0100]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Aiko Brandt to notice NTC-3386 on time under the receipt rule?"
 },
 {
  "qid": "qa702f4b1b6",
  "kind": "choice",
  "text": "Hi duty clerk,\nHope you are doing great! Hana Sato has sent file POL-1205 about the loss claim, all lovely and tidy. Just wanted to pop it in your inbox. Catch you round.\nCheers\n\nPolicy POL-1205, holder Hana Sato:\n- policy start date: 26 Apr 2027\n- theft cover: added by a rider effective 19 May 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which, under the cover rule, the theft loss in policy POL-1205 would be covered?",
  "options": [
   "1 Jun 2027",
   "11 May 2027",
   "3 Jun 2027"
  ]
 },
 {
  "qid": "q97306f84c7",
  "kind": "choice",
  "text": "Sara Ilves: sending file NTC-2879 about the notice response, with thanks.\nintake team: received, thank you.\nintake team: best wishes.\n\nNotice NTC-2879 to Sara Ilves:\n- response due date: 2025-09-09\n- office cutoff on the due date: 9 September 2025, 12:30 (UTC+02:00)\n- response sent: 8 September 2025, 20:25 (UTC+10:00) [same instant in office time: 8 September 2025, 12:25 (UTC+02:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on which date does the office count the response to notice NTC-2879 as received under the receipt rule?",
  "options": [
   "September 8, 2025",
   "September 7, 2025"
  ]
 },
 {
  "qid": "qae7efd13a5",
  "kind": "yes/no",
  "text": "Hi front desk,\nFelix Ortega is sending file PO-3615 about the purchase request as routine correspondence. The file follows the standard layout. That is the full picture.\nRegards,\n\nPurchase log PO-3615, kept by Felix Ortega, vendor Vantmoor Electric:\n- earlier purchase on 5 Mar 2027: $14,064.00\n- earlier purchase on 15 Jul 2027: $8,526.00\n- earlier purchase on 19 Jul 2027: $12,611.00\n- new request on 27 Jul 2027: $3,863.00\nWindow checked: 28 Jun 2027 to 27 Jul 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is greater than $25,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request from Felix Ortega need written quotes under the purchase rule?"
 },
 {
  "qid": "q6d70976785",
  "kind": "yes/no",
  "text": "Hi front desk,\nYara Haddad sends file NTC-7025 about the reply timing question as a regular copy. The file follows the standard format. That covers the routine points.\nRegards,\n\nNotice NTC-7025 to Yara Haddad:\n- response due date: 2025-04-25\n- office cutoff on the due date: 25 April 2025, 21:02 (UTC+09:00)\n- response sent: 26 April 2025, 11:37 (UTC+02:00) [same instant in office time: 26 April 2025, 18:37 (UTC+09:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the response to notice NTC-7025 on time under the receipt rule?"
 },
 {
  "qid": "qf3d01db196",
  "kind": "yes/no",
  "text": "Sent by: Mira Castell\nFile: CASE-7642\nSent to: records clerk\nHappy to share the file about the appeal deadline, it was fun to put together. Hope it helps with the sorting.\n\nCase CASE-7642, party Mira Castell:\n- billing date: 24 Sep 2027\n- statement date: 17 Sep 2027\n- dispute filed on: 3 Nov 2027\n- days from the billing date to the filing: 40 days\n- days from the statement date to the filing: 47 days",
  "question": "Filing rule: the dispute must be filed within 40 days measured from the later of the dates below: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 40 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the dispute filed on or before the final day of the filing period?"
 },
 {
  "qid": "qafb0364b5b",
  "kind": "choice",
  "text": "Ana Ruiz: Sending STAY-8519 about the visa stay count as usual.\ncase team: Received.\n\nStay record STAY-8519 for Ana Ruiz:\n- entry day Thursday, March 11, 2027, exit day Saturday, March 20, 2027 (whole stay: ten days)\n- entry day Wednesday, April 7, 2027, exit day Thursday, May 6, 2027 (whole stay: 30 days)\n- entry day Sunday, May 23, 2027, exit day Thursday, May 27, 2027 (whole stay: five days)\nReference date: Wednesday, June 16, 2027\nWindow checked: Friday, March 19, 2027 to Wednesday, June 16, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 30 days inside every moving 90-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days present for Ana Ruiz fall inside the checked window ending on the reference date in record STAY-8519, under the stay rule?",
  "options": [
   "40 days",
   "37 days",
   "35 days",
   "38 days"
  ]
 },
 {
  "qid": "qdbfcab4672",
  "kind": "choice",
  "text": "Iris Vance sends file POL-9862 about the cover question to the desk. This is the regular version, laid out in the standard format. The desk has the full set on hand. Passing it along as usual.\n\nPolicy POL-9862, holder Iris Vance:\n- policy start date: 19 August 2026\n- fire damage cover: added by a rider effective 20 September 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of 60 days starting with the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 60 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which, under the cover rule, the fire damage loss in policy POL-9862 would be covered?",
  "options": [
   "21 November 2026",
   "19 October 2026",
   "20 November 2026",
   "18 November 2026"
  ]
 },
 {
  "qid": "q57ff379df1",
  "kind": "choice",
  "text": "Iris Vance: Sending CASE-9992 about the complaint filing as usual.\ncase team: Received.\n\nCase CASE-9992, party Iris Vance:\n- incident date: Thursday, April 1, 2027\n- discovery date: Monday, March 22, 2027",
  "question": "Filing rule: the complaint must be filed inside a span of 45 days that runs after the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, what is the latest date on which the complaint can be filed in time?",
  "options": [
   "Sunday, May 16, 2027",
   "Monday, May 17, 2027",
   "Thursday, June 3, 2027",
   "Tuesday, May 18, 2027"
  ]
 },
 {
  "qid": "q05269f2110",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nOwen Pryce is sending file STAY-4769 about the visa stay count, with the main points at the top. Quick note, I am buried under other work.\nBest,\n\nStay record STAY-4769 for Owen Pryce:\n- entry day February 6, 2027, exit day March 8, 2027 (whole stay: 31 days)\nReference date: April 2, 2027\nWindow checked: January 3, 2027 to April 2, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 30 days inside any moving 90-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, is the person in file STAY-4769 over the stay limit, with more days present in the window ending on April 2, 2027?"
 },
 {
  "qid": "qac82494b4f",
  "kind": "choice",
  "text": "Sent by: Iris Vance\nFile: CASE-7068\nSent to: records clerk\nShort note, my queue is packed. The file is about the complaint filing and is attached.\n\nCase CASE-7068, party Iris Vance:\n- purchase date: Friday, 26 February 2027\n- handover date: Friday, 19 February 2027",
  "question": "Filing rule: the refund request must be filed within 60 days after the later date out of these dates: the purchase date and the handover date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the latest day on which Iris Vance may still file the refund request in time?",
  "options": [
   "Tuesday, 20 April 2027",
   "Wednesday, 28 April 2027",
   "Tuesday, 27 April 2027"
  ]
 },
 {
  "qid": "qca42ba85df",
  "kind": "choice",
  "text": "Sara Ilves sends file STAY-3483 about the residence day count to the desk. The file keeps to the standard format. A full copy sits with the desk too.\n\nStay record STAY-3483 for Sara Ilves:\n- entry day Monday, 30 November 2026, exit day Wednesday, 16 December 2026 (whole stay: seventeen days)\n- entry day Friday, 22 January 2027, exit day Monday, 1 March 2027 (whole stay: 39 days)\nReference date: Monday, 29 March 2027\nWindow checked: Monday, 30 November 2026 to Monday, 29 March 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days within every moving 120-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present fall inside the checked window that ends on Monday, 29 March 2027 for file STAY-3483?",
  "options": [
   "56 days",
   "55 days"
  ]
 },
 {
  "qid": "q19357f32de",
  "kind": "yes/no",
  "text": "Jonas Feld sends file STAY-1899 about the residence day count to the admin team. Writing fast because I am swamped. The file is attached and the main points sit at the top. Off to other work.\n\nStay record STAY-1899 for Jonas Feld:\n- entry day 17 October 2026, exit day 21 October 2026 (whole stay: five days)\n- entry day 11 November 2026, exit day 6 December 2026 (whole stay: 26 days)\n- entry day 4 January 2027, exit day 16 January 2027 (whole stay: thirteen days)\nReference date: 17 February 2027\nWindow checked: 20 November 2026 to 17 February 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 45 days inside every 90-day stretch that moves along. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does file STAY-1899 show more days present in the checked window ending on the reference date than the limit?"
 },
 {
  "qid": "q5482525874",
  "kind": "choice",
  "text": "From: Paolo Greco\nFile: CASE-8402\nSent to: review team\nThis file about the appeal deadline is passed along with thanks for your help.\n\nCase CASE-8402, party Paolo Greco:\n- decision date: 4 February 2028\n- delivery date: 18 February 2028",
  "question": "Filing rule: the appeal must be filed inside 56 days extending past the later of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 56 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the latest date, under the filing rule, on which the appeal for case CASE-8402 can be filed in time?",
  "options": [
   "31 March 2028",
   "14 April 2028",
   "13 April 2028"
  ]
 },
 {
  "qid": "qfe0bc6617c",
  "kind": "choice",
  "text": "Sent by: Kofi Mensah\nFile: POL-5497\nSent to: records clerk\nHappy to share the file about the cover question, it was fun to put together. Hope it helps with the sorting.\n\nPolicy POL-5497, holder Kofi Mensah:\n- policy start date: 30 Jul 2026\n- fire damage cover: added by a rider effective 26 Oct 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days whose earliest counted day is the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the earliest date on which the fire damage loss would be covered?",
  "options": [
   "30 Aug 2026",
   "24 Nov 2026",
   "26 Nov 2026",
   "25 Nov 2026"
  ]
 },
 {
  "qid": "q988940c73d",
  "kind": "choice",
  "text": "Eva Marsh: Hello, I am sending file PO-2277 about the buying request to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nPurchase log PO-2277, kept by Eva Marsh, vendor Mirefield Print:\n- earlier purchase on Wednesday, 13 January 2027: 1,924.00 USD\n- earlier purchase on Monday, 26 April 2027: 125.00 USD\n- earlier purchase on Wednesday, 28 April 2027: 2,439.00 USD\n- earlier purchase on Tuesday, 25 May 2027: 56.00 USD\n- new request on Monday, 14 June 2027: 2,685.00 USD\nWindow checked: Friday, 16 April 2027 to Monday, 14 June 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is greater than 5,000.00 USD, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, what total is set against the purchase threshold when the new request PO-2277 is included?",
  "options": [
   "5,305.00 USD",
   "2,741.00 USD",
   "2,620.00 USD"
  ]
 },
 {
  "qid": "q81db339db4",
  "kind": "choice",
  "text": "From: Lucas Brenner\nFile: POL-7074\nSent to: review team\nI am passing on this file about the cover question. Thank you for your help.\n\nPolicy POL-7074, holder Lucas Brenner:\n- policy start date: 31 October 2027\n- storm damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 15 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 15 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date, under the cover rule, from which the storm damage loss would be covered?",
  "options": [
   "20 November 2027",
   "16 November 2027",
   "17 November 2027"
  ]
 },
 {
  "qid": "q026bba3128",
  "kind": "yes/no",
  "text": "Priya Raman: sending POL-2735 about the cover question, in a rush.\nservice desk: got it, thanks.\ndesk: that is the full file.\n\nPolicy POL-2735, holder Priya Raman:\n- policy start date: 2026-12-08\n- subsidence cover: added by a rider effective 2027-05-24\n- subsidence loss on: 2027-05-25\n- days from the policy start date to the loss: 168 days\n- days from the rider effective date to the loss: one day",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days whose earliest counted day is the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, did the subsidence loss for Priya Raman happen during the waiting period?"
 },
 {
  "qid": "qa8f6701745",
  "kind": "choice",
  "text": "Sent by: Ravi Anand\nFile: LED-3596\nSent to: review team\nThis is a standard note about the cash ledger check. The file is laid out as usual.\n\nCash ledger LED-3596, teller Ravi Anand:\n- 2028-06-13: withdrawal of $1,312.00\n- 2028-06-13: deposit of $2,085.00\n- 2028-06-13: withdrawal of $1,427.00\n- 2028-06-13: deposit of $916.00\n- 2028-06-15: deposit of $1,624.00\nDay under review: 2028-06-13",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is $3,000.00 bar, cleared only by more than that, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, which of the day's totals on 2028-06-13 call for a cash report?",
  "options": [
   "Only the withdrawal total",
   "Only the deposit total",
   "Both totals",
   "Neither total"
  ]
 },
 {
  "qid": "q2685ec1372",
  "kind": "choice",
  "text": "Maya Lindgren: Quick send of CASE-9517 about the claim deadline question.\nservice desk: Thanks, that is in.\n\nCase CASE-9517, party Maya Lindgren:\n- inspection date: 25 Aug 2026\n- report date: 15 Sep 2026",
  "question": "Filing rule: the objection must be filed within nineteen days starting from the later of the dates listed below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is nineteen days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, by which final day can Maya Lindgren still file the objection and remain in time?",
  "options": [
   "13 Sep 2026",
   "4 Oct 2026",
   "6 Oct 2026"
  ]
 },
 {
  "qid": "q76bca11fa5",
  "kind": "choice",
  "text": "From: Paolo Greco\nFile: CASE-8402\nSent to: review team\nThis file about the appeal deadline is passed along with thanks for your help.\n\nCase CASE-8402, party Paolo Greco:\n- decision date: 4 February 2028\n- delivery date: 18 February 2028",
  "question": "Filing rule: the appeal must be filed inside 60 days extending past the later of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the latest date, under the filing rule, on which the appeal for case CASE-8402 can be filed in time?",
  "options": [
   "4 April 2028",
   "18 April 2028",
   "16 April 2028"
  ]
 },
 {
  "qid": "q07705f985d",
  "kind": "choice",
  "text": "Lucas Brenner: sending file NTC-8606 about the notice response, with thanks.\nintake team: thank you, this is received.\nintake team: appreciated.\n\nNotice NTC-8606 to Lucas Brenner:\n- response due date: Saturday, 19 September 2026\n- office cutoff on the due date: 2026-09-19 13:12:00 +0530\n- response sent: 2026-09-17 03:37:00 -0400 [same instant in office time: 2026-09-17 13:07:00 +0530]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn which date does the office count the response from Lucas Brenner as received under the receipt rule?",
  "options": [
   "September 17, 2026",
   "September 16, 2026"
  ]
 },
 {
  "qid": "qb1c7236062",
  "kind": "yes/no",
  "text": "From: Omar Saleh\nFile: LED-9942\nSent to: review team\nThis file about the branch cash review is passed along with thanks for your help.\n\nCash ledger LED-9942, teller Omar Saleh:\n- Monday, June 29, 2026: deposit of $2,786\n- Wednesday, July 1, 2026: deposit of $1,883\nDay under review: Monday, June 29, 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any figure at or above $3,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does the cash rule let the day in ledger LED-9942 close without a cash report?"
 },
 {
  "qid": "qecc508e497",
  "kind": "choice",
  "text": "Felix Ortega: Dear team, I am forwarding file STAY-6316 about the visa stay count to the intake team.\nintake: Thank you for passing it along.\nteam: With thanks for your courtesy.\n\nStay record STAY-6316 for Felix Ortega:\n- entry day 8 March 2027, exit day 27 March 2027 (whole stay: 20 days)\n- entry day 18 April 2027, exit day 10 May 2027 (whole stay: 23 days)\n- entry day 3 June 2027, exit day 17 August 2027 (whole stay: 76 days)\nReference date: 16 September 2027\nWindow checked: 21 March 2027 to 16 September 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 90 days within every moving 180-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, how many days present for Felix Ortega fall inside the checked window ending on the reference date in file STAY-6316?",
  "options": [
   "119 days",
   "106 days",
   "107 days"
  ]
 },
 {
  "qid": "q0413a6fb1a",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nJonas Feld sends file NTC-9982 about the response deadline with a cheerful hello. The file is in the usual layout and is fun to read.\nCheers,\n\nNotice NTC-9982 to Jonas Feld:\n- response due date: 2025-06-05\n- office cutoff on the due date: 2025-06-05 21:38:00 -0500\n- response sent: 2025-06-06 05:28:00 +0100 [same instant in office time: 2025-06-05 23:28:00 -0500]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Jonas Feld on time under the receipt rule?"
 },
 {
  "qid": "q409a2472e8",
  "kind": "yes/no",
  "text": "Paolo Greco: File CASE-6871 is sent about the claim deadline question as normal.\ncase team: Received, thank you.\n\nCase CASE-6871, party Paolo Greco:\n- invoice date: 19 Jan 2027\n- goods received date: 14 Jan 2027\n- claim filed on: 19 Apr 2027\n- days from the invoice date to the filing: 90 days\n- days from the goods received date to the filing: 95 days",
  "question": "Filing rule: the claim must be filed within 90 days starting from the later of the dates listed below: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is it true that the claim in case CASE-6871 was not filed in time?"
 },
 {
  "qid": "q7018dd9b27",
  "kind": "yes/no",
  "text": "Sent by: Hana Sato\nFile: POL-9833\nSent to: records clerk\nFast message from me, the inbox is overflowing. The file is about the insurance claim and is attached.\n\nPolicy POL-9833, holder Hana Sato:\n- policy start date: Wednesday, January 5, 2028\n- theft cover: added by a rider effective Monday, May 8, 2028\n- theft loss on: Thursday, May 18, 2028\n- days from the policy start date to the loss: 134 days\n- days from the rider effective date to the loss: 10 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 10 days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 10 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the theft loss, under the cover rule, covered?"
 },
 {
  "qid": "q1f1f3624fc",
  "kind": "choice",
  "text": "Nadia Kowal has passed on file STAY-9135 about the visa stay count to the desk. This memo goes with the file so it is on hand in the usual way. Thank you for your help.\n\nStay record STAY-9135 for Nadia Kowal:\n- entry day 26 May 2026, exit day 27 May 2026 (whole stay: 2 days)\n- entry day 21 Jun 2026, exit day 5 Jul 2026 (whole stay: 15 days)\n- entry day 6 Sep 2026, exit day 16 Oct 2026 (whole stay: 41 days)\nReference date: 17 Dec 2026\nWindow checked: 21 Jun 2026 to 17 Dec 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 90 days in any 180-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present for Nadia Kowal fall inside the checked window ending on 17 Dec 2026?",
  "options": [
   "54 days",
   "56 days"
  ]
 },
 {
  "qid": "qb09d6ef749",
  "kind": "choice",
  "text": "Eva Marsh sends file PO-3616 about the purchase request to the desk. The file is set out in full with the usual headings. Thank you for your attention to this matter.\n\nPurchase log PO-3616, kept by Eva Marsh, vendor Mirefield Print:\n- earlier purchase on June 21, 2027: $8,219.00\n- earlier purchase on October 14, 2027: $6,031.00\n- earlier purchase on October 30, 2027: $1,656.00\n- new request on November 12, 2027: $9,376.00\nWindow checked: October 14, 2027 to November 12, 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is $15,000.00 or more, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich total, with the new request PO-3616 from Eva Marsh included, gets compared with the threshold under the purchase rule?",
  "options": [
   "$17,063.00",
   "$25,282.00"
  ]
 },
 {
  "qid": "qdefa7debb6",
  "kind": "choice",
  "text": "Ana Ruiz: passing along CASE-4468 about the claim deadline question.\nintake team: thanks, that is clear.\nintake team: great, thanks again.\n\nCase CASE-4468, party Ana Ruiz:\n- invoice date: 11 Jan 2026\n- goods received date: 25 Jan 2026",
  "question": "Filing rule: the claim must be filed inside a span of 21 days that runs after the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the final day on which Ana Ruiz can still file the claim in time for case CASE-4468?",
  "options": [
   "13 Feb 2026",
   "14 Feb 2026",
   "15 Feb 2026"
  ]
 },
 {
  "qid": "q68c87d9ee2",
  "kind": "choice",
  "text": "Dear duty clerk,\nTheo Kalnins is sending file NTC-7846 about the reply deadline. The file is attached for your desk. Thanks in advance for your help.\nBest,\n\nNotice NTC-7846 to Theo Kalnins:\n- notice date: Tuesday, 1 June 2027\n- sent by: hand delivery\n- 14 days after the notice date, before any postal add-on or closure: Tuesday, 15 June 2027\nOffice closures: Sunday, 13 June 2027; Tuesday, 15 June 2027; Wednesday, 16 June 2027.",
  "question": "Response rule: a response is due 14 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 3 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the due date of the response to notice NTC-7846 from Theo Kalnins under the response rule?",
  "options": [
   "Thursday, 17 June 2027",
   "Monday, 14 June 2027"
  ]
 }
]
