# G5-H blind read T01-blind_read-a705ff47-001 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T01/pilot/g5h/answers/T01-blind_read-a705ff47-001.json

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
  "qid": "q465ee76017",
  "kind": "choice",
  "text": "Subject: handover for intake\nDear intake team,\nWe are pleased to pass on file CASE-9766, sent in by Lena Whitcombe, about the appeal deadline.\nYours faithfully,\n\nCase CASE-9766, party Lena Whitcombe:\n- billing date: 2026-10-28\n- statement date: 2026-09-13",
  "question": "Filing rule: the dispute must be filed inside 30 days counted from the later of these dates: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, by which final day must the dispute be filed to still count as in time?",
  "options": [
   "2026-11-27",
   "2026-11-25",
   "2026-11-28"
  ]
 },
 {
  "qid": "q61e1b996c3",
  "kind": "choice",
  "text": "[queue] fast_intake sender=Paolo Greco\n[file] LED-2997 about the teller ledger review sent to front_desk\n\nCash ledger LED-2997, teller Paolo Greco:\n- 6 August 2028: withdrawal of 1,919.00 USD\n- 6 August 2028: deposit of 3,795.00 USD\n- 8 August 2028: deposit of 2,543.00 USD\nDay under review: 6 August 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is anything strictly greater than 5,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, which of the day's totals on 6 August 2028 call for a cash report?",
  "options": [
   "Neither total",
   "Only the deposit total",
   "Only the withdrawal total",
   "Both totals"
  ]
 },
 {
  "qid": "qe803e24470",
  "kind": "yes/no",
  "text": "file: STAY-7456 about the visa stay count\nrequester: Priya Raman\nassignee: case team\nStandard handling applies here.\n\nStay record STAY-7456 for Priya Raman:\n- entry day 31 March 2026, exit day 6 April 2026 (whole stay: 7 days)\n- entry day 27 April 2026, exit day 9 May 2026 (whole stay: 13 days)\n- entry day 26 May 2026, exit day 4 June 2026 (whole stay: 10 days)\nReference date: 28 June 2026\nWindow checked: 31 March 2026 to 28 June 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 30 days within any 90-day window that keeps moving. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, do the days present for Priya Raman inside the checked window ending on the reference date exceed the stay limit?"
 },
 {
  "qid": "qa5a5746d58",
  "kind": "yes/no",
  "text": "Memo: Just a short line, Bruno Lacerda sends file STAY-1247 about the visa stay count to the help desk. Please take it in hand at your pace.\n\nStay record STAY-1247 for Bruno Lacerda:\n- entry day Monday, 22 December 2025, exit day Wednesday, 7 January 2026 (whole stay: seventeen days)\n- entry day Thursday, 5 February 2026, exit day Tuesday, 24 February 2026 (whole stay: twenty days)\nReference date: Saturday, 21 March 2026\nWindow checked: Monday, 22 December 2025 to Saturday, 21 March 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 30 days in every 90-day run that moves forward through time. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is Bruno Lacerda over the stay limit in record STAY-1247 when counting just the checked window that ends on the reference date?"
 },
 {
  "qid": "q6cd1fe8fdc",
  "kind": "choice",
  "text": "Bruno Lacerda: sending STAY-8396 about the visa stay count, here it is.\nhelp desk: got it, thanks.\nhelp desk: that is the whole pack.\n\nStay record STAY-8396 for Bruno Lacerda:\n- entry day Friday, 6 August 2027, exit day Wednesday, 11 August 2027 (whole stay: 6 days)\n- entry day Wednesday, 25 August 2027, exit day Tuesday, 14 September 2027 (whole stay: 21 days)\n- entry day Wednesday, 13 October 2027, exit day Monday, 1 November 2027 (whole stay: 20 days)\nReference date: Friday, 3 December 2027\nWindow checked: Sunday, 5 September 2027 to Friday, 3 December 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 30 days inside every moving 90-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present for Bruno Lacerda fall inside the checked window ending on Friday, 3 December 2027?",
  "options": [
   "20 days",
   "29 days",
   "41 days",
   "30 days"
  ]
 },
 {
  "qid": "q3b5ef4fe86",
  "kind": "choice",
  "text": "Subject: File NTC-6606 for the records clerk\nHello records clerk,\nAttached is a short note from Ines Duarte about the notice response.\nBest regards,\n\nNotice NTC-6606 to Ines Duarte:\n- notice date: Monday, September 14, 2026\n- sent by: post\n- 21 days after the notice date, before any postal add-on or closure: Monday, October 5, 2026\nOffice closures: Thursday, October 8, 2026; Friday, October 9, 2026.",
  "question": "Response rule: a response is due 21 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add three days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the due date for the response from Ines Duarte to the notice under the response rule?",
  "options": [
   "Friday, October 16, 2026",
   "Saturday, October 10, 2026"
  ]
 },
 {
  "qid": "q25e3130cfd",
  "kind": "yes/no",
  "text": "[intake] Iris Vance sends file STAY-6244 about the border stay check for review_team\n[route] queue=review_team priority=busy\n\nStay record STAY-6244 for Iris Vance:\n- entry day 2027-05-05, exit day 2027-05-11 (whole stay: seven days)\n- entry day 2027-06-05, exit day 2027-06-06 (whole stay: two days)\n- entry day 2027-06-27, exit day 2027-07-24 (whole stay: 28 days)\nReference date: 2027-08-09\nWindow checked: 2027-05-12 to 2027-08-09, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 45 days in any 90-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is it true that Iris Vance is not over the stay limit?"
 },
 {
  "qid": "q72c708d30c",
  "kind": "choice",
  "text": "Subject: respectful intake\nDear case team,\nBruno Lacerda sent in file CASE-4631 about the complaint filing. Kindly give it proper attention.\nWith kind thanks,\n\nCase CASE-4631, party Bruno Lacerda:\n- incident date: 8 Apr 2026\n- discovery date: 9 Mar 2026",
  "question": "Filing rule: the complaint must be filed inside a span of 90 days that runs after the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the final day on which Bruno Lacerda can still file the complaint in case CASE-4631 and be in time?",
  "options": [
   "6 Jul 2026",
   "7 Jul 2026",
   "5 Jul 2026"
  ]
 },
 {
  "qid": "q1f7cb84153",
  "kind": "choice",
  "text": "desk: file STAY-9070 about the residence day count forwards from Mira Castell to the records clerk\nclerk: thanks, that is logged\ndesk: sounds good\n\nStay record STAY-9070 for Mira Castell:\n- entry day Wednesday, December 29, 2027, exit day Saturday, January 29, 2028 (whole stay: 32 days)\n- entry day Thursday, February 17, 2028, exit day Monday, March 13, 2028 (whole stay: 26 days)\nReference date: Sunday, April 2, 2028\nWindow checked: Tuesday, January 4, 2028 to Sunday, April 2, 2028, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 45 days in each 90-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, how many days present fall inside the checked window ending on Sunday, April 2, 2028 in file STAY-9070?",
  "options": [
   "51 days",
   "50 days",
   "26 days",
   "52 days"
  ]
 },
 {
  "qid": "qde85e9893a",
  "kind": "choice",
  "text": "Subject: quick drop\nHi service desk,\nFile CASE-9404 from Omar Saleh about the complaint filing is here, straight in for you.\nBest,\n\nCase CASE-9404, party Omar Saleh:\n- incident date: December 5, 2025\n- discovery date: November 21, 2025",
  "question": "Filing rule: the complaint must be filed within 14 days measured beyond the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 14 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, by which final day can Omar Saleh still file the complaint and remain in time?",
  "options": [
   "December 21, 2025",
   "December 20, 2025",
   "December 25, 2025",
   "December 19, 2025"
  ]
 },
 {
  "qid": "q2bd3625562",
  "kind": "yes/no",
  "text": "Subject: quick pass\nHi review team,\nAiko Brandt sent in file NTC-8359 about the notice response. Please give it a fast look and reply.\nThanks,\n\nNotice NTC-8359 to Aiko Brandt:\n- response due date: 18 September 2026\n- office cutoff on the due date: 18 September 2026, 18:30 (UTC+03:00)\n- response sent: 18 September 2026, 03:51 (UTC+02:00) [same instant in office time: 18 September 2026, 04:51 (UTC+03:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was Aiko Brandt's response on time under the receipt rule?"
 },
 {
  "qid": "qca24e78888",
  "kind": "yes/no",
  "text": "title | file POL-3063 about the insurance claim\nrequester | Theo Kalnins\nteam | records_clerk\nnote | passes along for handling\n\nPolicy POL-3063, holder Theo Kalnins:\n- policy start date: Saturday, 11 September 2027\n- storm damage cover: part of the base policy\n- storm damage loss on: Monday, 11 October 2027\n- days from the policy start date to the loss: 30 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days whose first counted day falls on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the storm damage loss on policy POL-3063 is not covered under the cover rule?"
 },
 {
  "qid": "qb7a97a8b92",
  "kind": "yes/no",
  "text": "Subject: the branch cash review, file LED-5124\nHello admin team,\nSending this in a rush from Tomas Lindqvist. Give it a look.\nBye, and thanks.\n\nCash ledger LED-5124, teller Tomas Lindqvist:\n- Wednesday, 8 December 2027: withdrawal of $1,536\n- Thursday, 9 December 2027: withdrawal of $687\n- Thursday, 9 December 2027: withdrawal of $2,314\n- Thursday, 9 December 2027: deposit of $3,450\nDay under review: Thursday, 9 December 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is greater than the sum of $3,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the cash rule let the day in ledger LED-5124 close without a cash report?"
 },
 {
  "qid": "q6edd034410",
  "kind": "yes/no",
  "text": "Nadia Kowal: File STAY-7523 is sent about the border stay check as normal.\ncase team: Received, thank you.\n\nStay record STAY-7523 for Nadia Kowal:\n- entry day 17 December 2025, exit day 25 February 2026 (whole stay: 71 days)\n- entry day 8 April 2026, exit day 27 April 2026 (whole stay: 20 days)\nReference date: 13 May 2026\nWindow checked: 15 November 2025 to 13 May 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 90 days in each 180-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does file STAY-7523 show more days present in the checked window ending on the reference date than the limit?"
 },
 {
  "qid": "q1f6cdacc34",
  "kind": "choice",
  "text": "Subject | file POL-8152 about the cover question\nFrom | Mira Castell\nKindly route this to the case team, thank you.\n\nPolicy POL-8152, holder Mira Castell:\n- policy start date: 2026-12-04\n- flood damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days with the start date itself left out, beginning the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn what earliest date would a loss of this kind be covered under policy POL-8152?",
  "options": [
   "2026-12-28",
   "2027-01-05",
   "2026-12-26"
  ]
 },
 {
  "qid": "q676bf1f7a7",
  "kind": "choice",
  "text": "{\n  \"file\": \"CASE-3783\",\n  \"sent_by\": \"Lena Whitcombe\",\n  \"subject\": \"the complaint filing\",\n  \"channel\": \"intake\"\n}\n\nCase CASE-3783, party Lena Whitcombe:\n- purchase date: 2026-12-03\n- handover date: 2026-12-10",
  "question": "Filing rule: the refund request must be filed within ten days measured beyond the later of these dates: the purchase date and the handover date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is ten days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the final day still in time for filing the refund request in case CASE-3783?",
  "options": [
   "2026-12-19",
   "2026-12-20",
   "2026-12-18"
  ]
 },
 {
  "qid": "q2f9d1bfefe",
  "kind": "choice",
  "text": "Title: file NTC-2075 about the notice response\nRequester: Ines Duarte\nKindly pass this to the duty clerk, thank you.\n\nNotice NTC-2075 to Ines Duarte:\n- notice date: 18 March 2028\n- sent by: email\n- fourteen days after the notice date, before any postal add-on or closure: 1 April 2028\nOffice closures: 1 April 2028.",
  "question": "Response rule: a response is due fourteen days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add three days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, on which date is the response from Ines Duarte to the notice due under the response rule?",
  "options": [
   "2 April 2028",
   "31 March 2028",
   "4 April 2028",
   "3 April 2028"
  ]
 },
 {
  "qid": "q353e107bfa",
  "kind": "yes/no",
  "text": "sent_by: Iris Vance\nfile: STAY-9580\nsubject: the residence day count\nteam: review\nchannel: quick_lane\n\nStay record STAY-9580 for Iris Vance:\n- entry day Thursday, 11 November 2027, exit day Tuesday, 16 November 2027 (whole stay: 6 days)\n- entry day Thursday, 2 December 2027, exit day Monday, 13 December 2027 (whole stay: 12 days)\n- entry day Thursday, 30 December 2027, exit day Saturday, 8 January 2028 (whole stay: 10 days)\nReference date: Tuesday, 18 January 2028\nWindow checked: Saturday, 20 November 2027 to Tuesday, 18 January 2028, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 21 days during any 60-day window that moves ahead. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is the person in file STAY-9580 inside the stay limit when days present in the window ending Tuesday, 18 January 2028 total at most the limit?"
 },
 {
  "qid": "qa0c4fffc25",
  "kind": "yes/no",
  "text": "Paolo Greco: file NTC-2357 about the response deadline is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.\n\nNotice NTC-2357 to Paolo Greco:\n- response due date: Sunday, December 27, 2026\n- office cutoff on the due date: 2026-12-27T12:00:00-05:00\n- response sent: 2026-12-27T22:25:00+05:30 [same instant in office time: 2026-12-27T11:55:00-05:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Paolo Greco to notice NTC-2357, under the receipt rule, counted as received on time?"
 },
 {
  "qid": "q25918ddd99",
  "kind": "choice",
  "text": "[front_desk] lovely little drop-off, file PO-3723 sent_by Felix Ortega about the buying request\n[route] cheers_from_the_desk, passing on\n\nPurchase log PO-3723, kept by Felix Ortega, vendor Quillon Labs:\n- earlier purchase on Wednesday, 7 January 2026: $3,905\n- new request on Thursday, 8 January 2026: $832\nWindow checked: Wednesday, 10 December 2025 to Thursday, 8 January 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any amount that is more than $5,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, which running total for Felix Ortega gets compared with the threshold when this new request is counted in it?",
  "options": [
   "$3,905",
   "$4,737"
  ]
 },
 {
  "qid": "q838c3fffe5",
  "kind": "yes/no",
  "text": "Title: file LED-6043 about the teller ledger review\nRequester: Ravi Anand\nSent to: admin team\nThanks a lot for the help.\n\nCash ledger LED-6043, teller Ravi Anand:\n- August 13, 2026: deposit of $579.00\n- August 13, 2026: deposit of $5,043.00\n- August 14, 2026: withdrawal of $1,504.00\nDay under review: August 13, 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is anything strictly greater than $5,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is a cash report required for August 13, 2026?"
 },
 {
  "qid": "qbfdd73aa05",
  "kind": "yes/no",
  "text": "Jonas Feld: quick drop, file LED-2289 about the cash ledger check\ndesk: got it, moving it to the help desk\nagent: busy queue, sorting it out fast\n\nCash ledger LED-2289, teller Jonas Feld:\n- Sunday, 10 October 2027: deposit of $5,986\n- Sunday, 10 October 2027: withdrawal of $1,932\n- Sunday, 10 October 2027: deposit of $119\n- Monday, 11 October 2027: withdrawal of $1,623\nDay under review: Sunday, 10 October 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is $5,000 bar, cleared only by more than that, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs a cash report, under the cash rule, required for Sunday, 10 October 2027?"
 },
 {
  "qid": "q363ee89dde",
  "kind": "yes/no",
  "text": "Title: standard entry for the border stay check\nRequester: Tomas Lindqvist\nFile: STAY-1883\nPlease route this to the case team.\n\nStay record STAY-1883 for Tomas Lindqvist:\n- entry day Thursday, 15 July 2027, exit day Wednesday, 21 July 2027 (whole stay: 7 days)\n- entry day Friday, 20 August 2027, exit day Friday, 27 August 2027 (whole stay: 8 days)\n- entry day Saturday, 25 September 2027, exit day Thursday, 14 October 2027 (whole stay: 20 days)\nReference date: Saturday, 30 October 2027\nWindow checked: Monday, 2 August 2027 to Saturday, 30 October 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 30 days in any 90-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Tomas Lindqvist over the stay limit when days present inside the window ending on the reference date number more than the limit, under the stay rule?"
 },
 {
  "qid": "qaf87eb5a0b",
  "kind": "choice",
  "text": "Dear duty clerk,\nOwen Pryce is sending file NTC-4887 about the reply timing question. It is attached here. Hope your work goes well.\nCheers,\n\nNotice NTC-4887 to Owen Pryce:\n- response due date: Saturday, 3 May 2025\n- office cutoff on the due date: 2025-05-03T15:45:00+09:00\n- response sent: 2025-05-04T20:41:00+10:00 [same instant in office time: 2025-05-04T19:41:00+09:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on which date does the office count the response to notice NTC-4887 as received under the receipt rule?",
  "options": [
   "Tuesday, 6 May 2025",
   "Monday, 5 May 2025"
  ]
 },
 {
  "qid": "q407a51bb2e",
  "kind": "yes/no",
  "text": "File STAY-6836 about the residence day count is set out below. Ines Duarte sends over the document for the intake team. Thank you for your attention.\n\nStay record STAY-6836 for Ines Duarte:\n- entry day Sunday, March 22, 2026, exit day Tuesday, April 21, 2026 (whole stay: 31 days)\n- entry day Tuesday, May 12, 2026, exit day Friday, May 15, 2026 (whole stay: 4 days)\n- entry day Tuesday, June 9, 2026, exit day Saturday, June 13, 2026 (whole stay: 5 days)\nReference date: Monday, July 6, 2026\nWindow checked: Wednesday, April 8, 2026 to Monday, July 6, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 45 days in any 90-day period that rolls forward day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Ines Duarte over the stay limit, counting the days present inside the window that ends on Monday, July 6, 2026?"
 },
 {
  "qid": "q5421794a73",
  "kind": "choice",
  "text": "Ref line: file LED-2245\nTopic line: the branch cash review\nFrom: Tomas Lindqvist\nBrisk, straight through.\n\nCash ledger LED-2245, teller Tomas Lindqvist:\n- 2025-05-16: deposit of $675\n- 2025-05-17: withdrawal of $684\n- 2025-05-17: deposit of $893\n- 2025-05-17: deposit of $1,689\n- 2025-05-17: withdrawal of $1,960\nDay under review: 2025-05-17",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any amount that is more than $3,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, for Tomas Lindqvist on 2025-05-17, which of the day's totals call for a cash report?",
  "options": [
   "Only the deposit total",
   "Both totals",
   "Neither total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q5596b3c0e8",
  "kind": "choice",
  "text": "File: PO-3317\nSubject: the purchase request\nFrom: Ines Duarte\nSending this straight across to the records clerk. The desk is very busy and stretched.\n\nPurchase log PO-3317, kept by Ines Duarte, vendor Corvane Office:\n- earlier purchase on 24 Nov 2027: $2,509.00\n- earlier purchase on 15 Feb 2028: $3,524.00\n- earlier purchase on 16 Feb 2028: $7,458.00\n- new request on 16 Mar 2028: $2,543.00\nWindow checked: 16 Feb 2028 to 16 Mar 2028, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is strictly more than $10,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what total does the purchase rule compare with its threshold for Ines Duarte, including the new request?",
  "options": [
   "$13,525.00",
   "$10,001.00"
  ]
 },
 {
  "qid": "q188c4ca06e",
  "kind": "choice",
  "text": "sent_by: Malik Osei\nfile: POL-6625\nsubject: the insurance claim\nteam: help desk\nchannel: fast_lane\n\nPolicy POL-6625, holder Malik Osei:\n- policy start date: Friday, 28 August 2026\n- burst pipe damage cover: added by a rider effective Wednesday, 2 December 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of fifteen days that begins on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is fifteen days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date, under the cover rule, from which the burst pipe damage loss would be covered?",
  "options": [
   "Thursday, 24 December 2026",
   "Saturday, 19 December 2026",
   "Friday, 18 December 2026"
  ]
 },
 {
  "qid": "q324e8e398f",
  "kind": "yes/no",
  "text": "Sent by: Clara Weiss\nFile: STAY-4973\nSent to: records clerk\nFast message from me, the inbox is overflowing. The file is about the border stay check and is attached.\n\nStay record STAY-4973 for Clara Weiss:\n- entry day 16 Jan 2028, exit day 10 Feb 2028 (whole stay: 26 days)\n- entry day 4 Mar 2028, exit day 8 Mar 2028 (whole stay: five days)\nReference date: 2 Apr 2028\nWindow checked: 4 Jan 2028 to 2 Apr 2028, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 45 days across any 90-day window that slides ahead day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Clara Weiss, under the stay rule, over the stay limit for the window ending on 2 Apr 2028?"
 },
 {
  "qid": "q2ab4aae185",
  "kind": "choice",
  "text": "service desk: Send it over, ready for it.\nDana Okafor: Here is file POL-5153, the loss claim, a rush job.\n\nPolicy POL-5153, holder Dana Okafor:\n- policy start date: 2027-08-08\n- theft cover: added by a rider effective 2027-12-25",
  "question": "Cover rule: a loss is covered only after a waiting period of fourteen days that opens on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is fourteen days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on what earliest date would Dana Okafor be covered for the theft loss?",
  "options": [
   "2028-01-09",
   "2027-08-23",
   "2028-01-08"
  ]
 },
 {
  "qid": "qd5574ff7a4",
  "kind": "yes/no",
  "text": "Iris Vance: File POL-9193 about the cover question is on its way to you.\nclerk: Fine, the usual steps apply.\nclerk: Standard handling for this material.\n\nPolicy POL-9193, holder Iris Vance:\n- policy start date: January 8, 2026\n- glass breakage cover: added by a rider effective April 10, 2026\n- glass breakage loss on: May 2, 2026\n- days from the policy start date to the loss: 114 days\n- days from the rider effective date to the loss: 22 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, is it true that the loss on policy POL-9193 is not covered?"
 },
 {
  "qid": "q4d441b3717",
  "kind": "yes/no",
  "text": "Yara Haddad: Hi there, popping file CASE-9341 over about the appeal deadline!\nagent: Lovely, thanks for that.\nagent: Happy to help, it is in good hands from here.\n\nCase CASE-9341, party Yara Haddad:\n- billing date: Wednesday, August 4, 2027\n- statement date: Wednesday, August 18, 2027\n- dispute filed on: Sunday, August 29, 2027\n- days from the billing date to the filing: 25 days\n- days from the statement date to the filing: 11 days",
  "question": "Filing rule: the dispute must be filed inside 10 days that elapses after whichever of the dates below is later: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 10 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the dispute in case CASE-9341 filed in time, on or before the final day?"
 },
 {
  "qid": "q569718cc61",
  "kind": "yes/no",
  "text": "Title | file CASE-5397 about the complaint filing\nRequester | Theo Kalnins\nRouted to | intake team\nKindly handle this at your convenience.\n\nCase CASE-5397, party Theo Kalnins:\n- incident date: 2026-12-07\n- discovery date: 2026-11-27\n- complaint filed on: 2026-12-29\n- days from the incident date to the filing: 22 days\n- days from the discovery date to the filing: 32 days",
  "question": "Filing rule: the complaint must be filed within 28 days following the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Theo Kalnins fail to file the complaint in case CASE-5397 by the deadline?"
 },
 {
  "qid": "qd7c2395f33",
  "kind": "choice",
  "text": "Desk memo: Quick heads up, Sara Ilves sent in file STAY-6080 about the visa stay count and it is in the review team's hands. Thanks for flagging it, that helps.\n\nStay record STAY-6080 for Sara Ilves:\n- entry day Friday, September 25, 2026, exit day Thursday, October 1, 2026 (whole stay: seven days)\n- entry day Tuesday, November 3, 2026, exit day Wednesday, December 2, 2026 (whole stay: 30 days)\nReference date: Wednesday, December 30, 2026\nWindow checked: Friday, October 2, 2026 to Wednesday, December 30, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 30 days inside every 90-day stretch that moves along. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days present fall inside the checked window that ends on the reference date in record STAY-6080?",
  "options": [
   "30 days",
   "29 days"
  ]
 },
 {
  "qid": "qce648716ff",
  "kind": "yes/no",
  "text": "title | the reply timing question with file NTC-7818\nrequester | Malik Osei\nteam | review_team\nnote | shares it here, thanks\n\nNotice NTC-7818 to Malik Osei:\n- response due date: 2028-08-09\n- office cutoff on the due date: 9 August 2028, 17:00 (UTC+09:00)\n- response sent: 2028-08-09T07:59:00Z [same instant in office time: 9 August 2028, 16:59 (UTC+09:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the reply to notice NTC-7818 on time under the receipt rule?"
 },
 {
  "qid": "q6559d27ca0",
  "kind": "choice",
  "text": "{\"sent_by\": \"Yara Haddad\", \"file\": \"NTC-2152\", \"subject\": \"the notice response\", \"team\": \"records_clerk\"}\n\nNotice NTC-2152 to Yara Haddad:\n- response due date: 18 February 2026\n- office cutoff on the due date: 2026-02-18 18:30:00 +0300\n- response sent: 2026-02-18 12:31:00 -0300 [same instant in office time: 2026-02-18 18:31:00 +0300]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn which date does the office treat the response to notice NTC-2152 as received under the receipt rule?",
  "options": [
   "20 February 2026",
   "19 February 2026"
  ]
 },
 {
  "qid": "q8bb255a23a",
  "kind": "choice",
  "text": "Subject: forwarded papers\nDear case team,\nKindly find file POL-7006 about the loss claim sent in by Iris Vance, and thank you for your attention to it.\nYours faithfully\n\nPolicy POL-7006, holder Iris Vance:\n- policy start date: March 24, 2026\n- fire damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 17 days commencing on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 17 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the earliest date on which this fire damage loss for Iris Vance would be covered?",
  "options": [
   "April 10, 2026",
   "April 11, 2026",
   "April 9, 2026"
  ]
 },
 {
  "qid": "qae65066601",
  "kind": "choice",
  "text": "Subject: the claim deadline question for file CASE-2639\nHi desk,\nTomas Lindqvist submits it to you in a hurry.\nThanks,\n\nCase CASE-2639, party Tomas Lindqvist:\n- inspection date: Tuesday, 23 November 2027\n- report date: Saturday, 13 November 2027",
  "question": "Filing rule: the objection must be filed inside a span of fourteen days that runs after the later of these dates: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is fourteen days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, what is the latest date on which the objection can be filed in time?",
  "options": [
   "Thursday, 9 December 2027",
   "Tuesday, 7 December 2027",
   "Wednesday, 8 December 2027",
   "Monday, 13 December 2027"
  ]
 },
 {
  "qid": "qd6705bee44",
  "kind": "yes/no",
  "text": "Desk memo: Omar Saleh is sending file STAY-4168 about the border stay check to the admin team. Pick it up fast, the work is waiting.\n\nStay record STAY-4168 for Omar Saleh:\n- entry day 2027-03-16, exit day 2027-06-12 (whole stay: 89 days)\nReference date: 2027-07-20\nWindow checked: 2027-01-22 to 2027-07-20, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 90 days in each 180-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, do the days present for Omar Saleh inside the checked window ending on the reference date exceed the stay limit?"
 },
 {
  "qid": "qac05d77705",
  "kind": "choice",
  "text": "[admin] sender=Kofi Mensah file=CASE-6009 to=admin_team\n[admin] subject=the claim deadline question sent_with_a_smile\n\nCase CASE-6009, party Kofi Mensah:\n- invoice date: 23 August 2027\n- goods received date: 22 September 2027",
  "question": "Filing rule: the claim must be filed within 21 days reckoned after the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the latest day on which Kofi Mensah may still file the claim in time?",
  "options": [
   "11 October 2027",
   "13 October 2027",
   "12 October 2027",
   "13 September 2027"
  ]
 },
 {
  "qid": "q82f56ff653",
  "kind": "yes/no",
  "text": "Freya Holm: Happy to pass on file CASE-5325 with notes on the complaint filing.\ndesk: Appreciated, this goes straight into the queue.\ndesk: Thank you for the courtesy.\n\nCase CASE-5325, party Freya Holm:\n- incident date: Thursday, 5 August 2027\n- discovery date: Tuesday, 3 August 2027\n- complaint filed on: Thursday, 28 October 2027\n- days from the incident date to the filing: 84 days\n- days from the discovery date to the filing: 86 days",
  "question": "Filing rule: the complaint must be filed within 60 days measured beyond the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHas the person failed to file the complaint for case CASE-5325 by the deadline?"
 },
 {
  "qid": "q910183b850",
  "kind": "yes/no",
  "text": "Subject: fast drop\nHi front desk,\nKofi Mensah is dropping file LED-5226 about the branch cash review with you. Keep moving.\nBest,\n\nCash ledger LED-5226, teller Kofi Mensah:\n- August 10, 2025: withdrawal of $11,743\n- August 12, 2025: deposit of $390\n- August 12, 2025: withdrawal of $5,416\n- August 12, 2025: withdrawal of $4,455\n- August 12, 2025: deposit of $12,563\n- August 13, 2025: deposit of $11,067\nDay under review: August 12, 2025",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any amount of $15,000 or above, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs a cash report required for ledger LED-5226 on the day under review?"
 },
 {
  "qid": "qc4604ba4d2",
  "kind": "choice",
  "text": "{\"author\": \"Lucas Brenner\", \"doc\": \"LED-6318\", \"subject\": \"the branch cash review\", \"team\": \"duty clerk\"}\n\nCash ledger LED-6318, teller Lucas Brenner:\n- February 8, 2027: withdrawal of $5,434.00\n- February 9, 2027: withdrawal of $5,619.00\n- February 9, 2027: withdrawal of $2,806.00\nDay under review: February 9, 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any sum more than $10,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals in ledger LED-6318 call for a cash report?",
  "options": [
   "Neither total",
   "Only the withdrawal total",
   "Both totals",
   "Only the deposit total"
  ]
 },
 {
  "qid": "qb05750e335",
  "kind": "choice",
  "text": "Freya Holm: Sending STAY-6848 about the visa stay count, routine as usual.\nintake team: Thanks, received.\n\nStay record STAY-6848 for Freya Holm:\n- entry day January 16, 2027, exit day January 31, 2027 (whole stay: 16 days)\n- entry day March 8, 2027, exit day April 17, 2027 (whole stay: 41 days)\n- entry day June 4, 2027, exit day June 13, 2027 (whole stay: 10 days)\nReference date: July 30, 2027\nWindow checked: February 1, 2027 to July 30, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 90 days in any 180-day span that moves ahead with each new day. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days present fall inside the checked window that ends on the reference date in record STAY-6848?",
  "options": [
   "49 days",
   "51 days"
  ]
 },
 {
  "qid": "q7284cf359f",
  "kind": "choice",
  "text": "{\"file\": \"STAY-3724\", \"sent_by\": \"Ines Duarte\", \"subject\": \"the visa stay count\", \"team\": \"service desk\", \"channel\": \"friendly_chat\"}\n\nStay record STAY-3724 for Ines Duarte:\n- entry day June 22, 2027, exit day August 13, 2027 (whole stay: 53 days)\n- entry day September 14, 2027, exit day October 15, 2027 (whole stay: 32 days)\nReference date: November 15, 2027\nWindow checked: July 19, 2027 to November 15, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days during any 120-day window that moves ahead. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, how many present days in record STAY-3724 sit inside the window ending on November 15, 2027?",
  "options": [
   "57 days",
   "58 days",
   "56 days",
   "59 days"
  ]
 },
 {
  "qid": "q79b8960631",
  "kind": "yes/no",
  "text": "Hana Sato: hey there, here is file CASE-1342 with the claim deadline question for you.\nfront desk: lovely, thanks for sending it over.\n\nCase CASE-1342, party Hana Sato:\n- invoice date: 29 Jun 2026\n- goods received date: 6 Jul 2026\n- claim filed on: 6 Aug 2026\n- days from the invoice date to the filing: 38 days\n- days from the goods received date to the filing: 31 days",
  "question": "Filing rule: the claim must be filed inside 31 days reckoned from the date that falls later among the dates below: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 31 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the claim from Hana Sato filed in time, on or before the final day of the filing period?"
 },
 {
  "qid": "q5873c56708",
  "kind": "choice",
  "text": "Omar Saleh: File NTC-6791 is sent about the notice response as normal.\ncase team: Received, thank you.\n\nNotice NTC-6791 to Omar Saleh:\n- notice date: 2025-06-30\n- sent by: email\n- 28 days after the notice date, before any postal add-on or closure: 2025-07-28\nOffice closures: 2025-07-28; 2025-07-29.",
  "question": "Response rule: a response is due 28 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 2 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the due date of the response to notice NTC-6791 under the response rule?",
  "options": [
   "2025-07-30",
   "2025-07-28"
  ]
 },
 {
  "qid": "q8a13839f99",
  "kind": "choice",
  "text": "file: LED-7760\nteam: front desk\nsent_by: Hana Sato\nsubject: the cash ledger check\nnote: hurry along\n\nCash ledger LED-7760, teller Hana Sato:\n- Thursday, 17 June 2027: deposit of $2,228.00\n- Saturday, 19 June 2027: withdrawal of $355.00\n- Saturday, 19 June 2027: deposit of $2,027.00\n- Saturday, 19 June 2027: withdrawal of $3,601.00\nDay under review: Saturday, 19 June 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is $3,000.00 itself excluded, only more than that counts, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, which of the day's totals on Saturday, 19 June 2027 call for a cash report?",
  "options": [
   "Both totals",
   "Only the withdrawal total",
   "Neither total",
   "Only the deposit total"
  ]
 },
 {
  "qid": "q96c8b625af",
  "kind": "choice",
  "text": "title | file CASE-2066 about the complaint filing\nrequester | Malik Osei\nqueue | records\nPlease route it to the records clerk.\n\nCase CASE-2066, party Malik Osei:\n- incident date: Friday, October 29, 2027\n- discovery date: Wednesday, October 27, 2027",
  "question": "Filing rule: the complaint must be filed inside 10 days beginning at the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 10 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, by which final day can Malik Osei still file the complaint and remain in time?",
  "options": [
   "Monday, November 8, 2027",
   "Tuesday, November 9, 2027",
   "Saturday, November 6, 2027"
  ]
 },
 {
  "qid": "q4ad640128c",
  "kind": "choice",
  "text": "[log] from=Iris Vance ref_file=POL-6452 to=records_clerk\n[log] about=the cover question routine_transfer\n\nPolicy POL-6452, holder Iris Vance:\n- policy start date: November 22, 2026\n- subsidence cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of fifteen days whose first counted day falls on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is fifteen days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date, under the cover rule, from which the subsidence loss would be covered?",
  "options": [
   "December 8, 2026",
   "December 10, 2026",
   "December 7, 2026"
  ]
 }
]
