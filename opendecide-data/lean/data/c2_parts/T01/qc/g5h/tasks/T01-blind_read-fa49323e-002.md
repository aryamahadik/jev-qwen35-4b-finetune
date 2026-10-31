# G5-H blind read T01-blind_read-fa49323e-002 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g5h/answers/T01-blind_read-fa49323e-002.json

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
  "qid": "qee6088a7d0",
  "kind": "choice",
  "text": "Ines Duarte: Hello. I am forwarding file CASE-9844 about the appeal deadline. My thanks for your help.\ncase team: Thank you, the file has been received.\n\nCase CASE-9844, party Ines Duarte:\n- decision date: 27 December 2025\n- delivery date: 30 December 2025",
  "question": "Filing rule: the appeal must be filed within 28 days measured from the later of the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the final day on which Ines Duarte can still file the appeal in time for case CASE-9844?",
  "options": [
   "27 January 2026",
   "25 January 2026",
   "26 January 2026",
   "24 January 2026"
  ]
 },
 {
  "qid": "qf8ee2cb1ea",
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
  "qid": "qd9e83e6b00",
  "kind": "yes/no",
  "text": "Ticket title: file STAY-9707 about the visa stay count\nRaised by: Iris Vance\nAssigned to: help desk\nCheers for taking a glance at this.\n\nStay record STAY-9707 for Iris Vance:\n- entry day Monday, June 15, 2026, exit day Friday, August 28, 2026 (whole stay: 75 days)\nReference date: Sunday, September 20, 2026\nWindow checked: Sunday, May 24, 2026 to Sunday, September 20, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days inside any moving 120-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is the person in record STAY-9707 within the stay limit, with the limit itself counting as within?"
 },
 {
  "qid": "qf80393ecc5",
  "kind": "yes/no",
  "text": "Desk memo: Ana Ruiz sends file CASE-6727 about the complaint filing to the service desk. Quick heads-up, the queue is swamped. Pick it up fast.\n\nCase CASE-6727, party Ana Ruiz:\n- incident date: Wednesday, January 28, 2026\n- discovery date: Wednesday, February 18, 2026\n- complaint filed on: Wednesday, March 11, 2026\n- days from the incident date to the filing: 42 days\n- days from the discovery date to the filing: 21 days",
  "question": "Filing rule: the complaint must be filed within 21 days measured beyond the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid case CASE-6727 get the complaint filed on or before the final day of the filing period?"
 },
 {
  "qid": "q6a90c7bc73",
  "kind": "yes/no",
  "text": "{\"sender\": \"Lena Whitcombe\", \"file\": \"POL-8260\", \"subject\": \"the insurance claim\", \"queue\": \"review team\", \"channel\": \"quick_handoff\"}\n\nPolicy POL-8260, holder Lena Whitcombe:\n- policy start date: September 12, 2027\n- fire damage cover: part of the base policy\n- fire damage loss on: December 11, 2027\n- days from the policy start date to the loss: 90 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 90 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 90 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does the cover rule count the fire damage loss for Lena Whitcombe as covered?"
 },
 {
  "qid": "q2bf0f1e2b8",
  "kind": "yes/no",
  "text": "{\"channel\": \"intake\", \"file\": \"POL-2191\", \"sent_by\": \"Bruno Lacerda\", \"subject\": \"the cover question\", \"team\": \"case_team\"}\n\nPolicy POL-2191, holder Bruno Lacerda:\n- policy start date: Tuesday, February 10, 2026\n- glass breakage cover: part of the base policy\n- glass breakage loss on: Tuesday, April 14, 2026\n- days from the policy start date to the loss: 63 days",
  "question": "Cover rule: a loss is covered only after a waiting period of fifteen days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is fifteen days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is it true that the glass breakage loss is not covered?"
 },
 {
  "qid": "qfc55b94ada",
  "kind": "yes/no",
  "text": "{\"sent_by\": \"Eva Marsh\", \"file\": \"POL-3384\", \"subject\": \"the loss claim\", \"team\": \"records clerk\", \"note\": \"with courtesy\"}\n\nPolicy POL-3384, holder Eva Marsh:\n- policy start date: 18 April 2027\n- power surge damage cover: part of the base policy\n- power surge damage loss on: 26 April 2027\n- days from the policy start date to the loss: 8 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 7 days that opens on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 7 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does the cover rule count the power surge damage loss for Eva Marsh as covered?"
 },
 {
  "qid": "q1eca3c6906",
  "kind": "yes/no",
  "text": "Dear front desk,\nI am writing to share file PO-6112 about the purchase request, sent by Hana Sato. Thank you for reading this message. The file is in full and in good shape. With respect and thanks.\nYours faithfully\n\nPurchase log PO-6112, kept by Hana Sato, vendor Ostrava Parts:\n- earlier purchase on 20 Feb 2027: $2,968\n- earlier purchase on 21 Apr 2027: $3,654\n- new request on 12 May 2027: $1,345\nWindow checked: 13 Apr 2027 to 12 May 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is $5,000 or greater, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, must the purchase request in log PO-6112 for Hana Sato come with written quotes?"
 },
 {
  "qid": "q8d61b90f65",
  "kind": "yes/no",
  "text": "Internal memo: Ines Duarte sends file LED-8704 about the teller ledger review to the desk. Standard routing applies, and the desk takes it from the usual pile.\n\nCash ledger LED-8704, teller Ines Duarte:\n- Thursday, 9 October 2025: deposit of $2,623.00\n- Saturday, 11 October 2025: withdrawal of $3,486.00\n- Saturday, 11 October 2025: deposit of $3,352.00\n- Saturday, 11 October 2025: withdrawal of $85.00\nDay under review: Saturday, 11 October 2025",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any total greater than $5,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs a cash report, under the cash rule, required for Saturday, 11 October 2025?"
 },
 {
  "qid": "qaf90f0b57b",
  "kind": "choice",
  "text": "team: records clerk\nfile: NTC-5766\nsent_by: Malik Osei\nsubject: the notice response\nnote: with thanks\n\nNotice NTC-5766 to Malik Osei:\n- response due date: Tuesday, June 2, 2026\n- office cutoff on the due date: 2026-06-02T15:06:00+03:00\n- response sent: 2026-05-31T21:11:00+09:00 [same instant in office time: 2026-05-31T15:11:00+03:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on which date does the office count the response to notice NTC-5766 as received under the receipt rule?",
  "options": [
   "31 May 2026",
   "1 Jun 2026"
  ]
 },
 {
  "qid": "qea7f9dde83",
  "kind": "yes/no",
  "text": "title | formal request\nrequester | Lucas Brenner\nfile | POL-8893\nWe kindly pass the cover question along to the records clerk for your review.\n\nPolicy POL-8893, holder Lucas Brenner:\n- policy start date: 23 November 2026\n- storm damage cover: added by a rider effective 26 April 2027\n- storm damage loss on: 17 May 2027\n- days from the policy start date to the loss: 175 days\n- days from the rider effective date to the loss: 21 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days that starts on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, did the loss on policy POL-8893 happen during the waiting period?"
 },
 {
  "qid": "q796b51070c",
  "kind": "yes/no",
  "text": "Desk memo: Dana Okafor is sending file POL-6649 about the cover question to the desk for routine handling.\nIt is a standard hand-over that sits in the usual queue.\n\nPolicy POL-6649, holder Dana Okafor:\n- policy start date: 16 April 2027\n- theft cover: added by a rider effective 20 July 2027\n- theft loss on: 27 August 2027\n- days from the policy start date to the loss: 133 days\n- days from the rider effective date to the loss: 38 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 7 days whose earliest counted day is the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 7 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that, under the cover rule, the theft loss is not covered?"
 },
 {
  "qid": "qc13d0e6211",
  "kind": "yes/no",
  "text": "Aiko Brandt: Dear team, I am forwarding file POL-5347 about the cover question to the intake team.\nintake: Thank you for passing it along.\nteam: With thanks for your courtesy.\n\nPolicy POL-5347, holder Aiko Brandt:\n- policy start date: September 27, 2027\n- glass breakage cover: added by a rider effective April 19, 2028\n- glass breakage loss on: May 10, 2028\n- days from the policy start date to the loss: 226 days\n- days from the rider effective date to the loss: 21 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, did the glass breakage loss for Aiko Brandt happen during the waiting period?"
 },
 {
  "qid": "q7a276675ad",
  "kind": "choice",
  "text": "Desk memo: Iris Vance is holding file CASE-5312 about the complaint filing for the front desk. Hand it straight to the clerk on the bench. Keep it moving, the queue is stacked.\n\nCase CASE-5312, party Iris Vance:\n- incident date: January 17, 2026\n- discovery date: December 3, 2025",
  "question": "Filing rule: the complaint must be filed inside a span of 21 days that runs after the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, by which final day can Iris Vance still file the complaint and remain in time?",
  "options": [
   "December 24, 2025",
   "February 7, 2026",
   "February 6, 2026"
  ]
 },
 {
  "qid": "qb51b596251",
  "kind": "yes/no",
  "text": "Subject: file POL-6690 about the insurance claim\nSender: Aiko Brandt\nSent to: intake team\nKindly review at your convenience.\n\nPolicy POL-6690, holder Aiko Brandt:\n- policy start date: Saturday, April 25, 2026\n- subsidence cover: part of the base policy\n- subsidence loss on: Friday, May 8, 2026\n- days from the policy start date to the loss: 13 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days whose first counted day falls on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does the cover rule count the subsidence loss for Aiko Brandt as covered?"
 },
 {
  "qid": "q55b215b6fb",
  "kind": "choice",
  "text": "[desk] busy_run: from=Lucas Brenner file=POL-9068 to=admin_team\n[desk] topic=the loss claim pushed_through\n\nPolicy POL-9068, holder Lucas Brenner:\n- policy start date: Monday, October 5, 2026\n- burst pipe damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 42 days whose first counted day falls on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 42 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on what earliest date would the burst pipe damage loss be covered?",
  "options": [
   "Wednesday, November 18, 2026",
   "Tuesday, November 17, 2026",
   "Thursday, December 3, 2026"
  ]
 },
 {
  "qid": "q56f6bf42d2",
  "kind": "yes/no",
  "text": "Nadia Kowal: Sending PO-4766 about the purchase request as usual.\ncase team: Received.\n\nPurchase log PO-4766, kept by Nadia Kowal, vendor Brightwell Supply:\n- earlier purchase on Tuesday, 26 August 2025: 5,972.00 USD\n- earlier purchase on Saturday, 20 December 2025: 6,162.00 USD\n- new request on Tuesday, 24 February 2026: 3,839.00 USD\nWindow checked: Thursday, 27 November 2025 to Tuesday, 24 February 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any total greater than 10,000.00 USD, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the request from Nadia Kowal, under the purchase rule, call for written quotes in log PO-4766?"
 },
 {
  "qid": "qef9088c79b",
  "kind": "yes/no",
  "text": "Ana Ruiz: Hello, I am sending file NTC-8765 about the notice response to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nNotice NTC-8765 to Ana Ruiz:\n- response due date: 5 December 2025\n- office cutoff on the due date: 5 December 2025, 13:20 (UTC+02:00)\n- response sent: 4 December 2025, 08:39 (UTC+03:00) [same instant in office time: 4 December 2025, 07:39 (UTC+02:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Ana Ruiz to notice NTC-8765 on time under the receipt rule?"
 },
 {
  "qid": "q60c8300778",
  "kind": "yes/no",
  "text": "review: Send it through, we are rolling fast here.\nMira Castell: Dropping file POL-8794 about the loss claim with the review team, moving quick.\n\nPolicy POL-8794, holder Mira Castell:\n- policy start date: 2026-05-24\n- fire damage cover: part of the base policy\n- fire damage loss on: 2026-08-22\n- days from the policy start date to the loss: 90 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 90 days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 90 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, did the loss on policy POL-8794 happen during the waiting period?"
 },
 {
  "qid": "qe0425637f2",
  "kind": "yes/no",
  "text": "Subject: a friendly send\nHi admin team,\nHere is file CASE-3822 about the appeal deadline from Hana Sato. Hope you are well!\nWarmly\n\nCase CASE-3822, party Hana Sato:\n- decision date: 2028-05-14\n- delivery date: 2028-04-23\n- appeal filed on: 2028-05-19\n- days from the decision date to the filing: 5 days\n- days from the delivery date to the filing: 26 days",
  "question": "Filing rule: the appeal must be filed within 21 days after the later date out of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the appeal in case CASE-3822 filed in time, on or before the final day?"
 },
 {
  "qid": "q52fff7acd0",
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
  "qid": "q546c72a2a3",
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
  "qid": "q00f44c8fac",
  "kind": "yes/no",
  "text": "Desk memo: Bruno Lacerda sends file PO-1006 about the purchase request to the intake team as part of the usual flow.\nThe intake team takes it from there.\n\nPurchase log PO-1006, kept by Bruno Lacerda, vendor Vantmoor Electric:\n- earlier purchase on December 29, 2025: $547\n- earlier purchase on February 12, 2026: $757\n- earlier purchase on March 31, 2026: $124\n- earlier purchase on April 8, 2026: $430\n- earlier purchase on May 14, 2026: $833\n- new request on June 13, 2026: $1,613\nWindow checked: February 14, 2026 to June 13, 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 120-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any sum more than $3,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request from Bruno Lacerda in log PO-1006 need written quotes under the purchase rule?"
 },
 {
  "qid": "q4235592bc5",
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
  "qid": "q8d5e8d6dfa",
  "kind": "yes/no",
  "text": "Dear front desk,\nTomas Lindqvist is sending file CASE-2258 about the appeal deadline. The file is attached here for your records. I appreciate the help with it.\nKind regards,\n\nCase CASE-2258, party Tomas Lindqvist:\n- decision date: 12 Aug 2027\n- delivery date: 7 Aug 2027\n- appeal filed on: 31 Aug 2027\n- days from the decision date to the filing: 19 days\n- days from the delivery date to the filing: 24 days",
  "question": "Filing rule: the appeal must be filed within 10 days past the later of the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 10 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Tomas Lindqvist, under the filing rule, fail to file the appeal in time?"
 },
 {
  "qid": "q5846c234c3",
  "kind": "yes/no",
  "text": "Kofi Mensah: yo, file NTC-1055 about the reply timing question just arrived with the help desk\nhelp desk: ahh cool, thanks heaps, that is a relief\n\nNotice NTC-1055 to Kofi Mensah:\n- response due date: Friday, 29 October 2027\n- office cutoff on the due date: 2027-10-29T19:31:00+09:00\n- response sent: 2027-10-29T11:56:00Z [same instant in office time: 2027-10-29T20:56:00+09:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Kofi Mensah to the notice late under the receipt rule?"
 },
 {
  "qid": "q7f240a84fb",
  "kind": "choice",
  "text": "Lucas Brenner: sending file NTC-8606 about the notice response, with thanks.\nintake team: thank you, this is received.\nintake team: appreciated.\n\nNotice NTC-8606 to Lucas Brenner:\n- response due date: Saturday, 19 September 2026\n- office cutoff on the due date: 2026-09-19 13:12:00 +0530\n- response sent: 2026-09-17 03:37:00 -0400 [same instant in office time: 2026-09-17 13:07:00 +0530]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn which date does the office count the response from Lucas Brenner as received under the receipt rule?",
  "options": [
   "September 17, 2026",
   "September 16, 2026"
  ]
 },
 {
  "qid": "qdf941a388f",
  "kind": "yes/no",
  "text": "title | kind request for the records clerk\nrequester | Malik Osei\nfile | STAY-1120\nPlease find the visa stay count attached for your review.\n\nStay record STAY-1120 for Malik Osei:\n- entry day 9 February 2027, exit day 24 February 2027 (whole stay: sixteen days)\n- entry day 27 February 2027, exit day 28 April 2027 (whole stay: 61 days)\nReference date: 26 June 2027\nWindow checked: 27 February 2027 to 26 June 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days in every 120-day run that moves forward through time. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the person in file STAY-1120 over the stay limit, meaning more days present inside the checked window ending on the reference date than the limit?"
 },
 {
  "qid": "q57194de3d5",
  "kind": "yes/no",
  "text": "Subject: Little catch-up on the notice response\n\nHey review team,\n\nDropping file NTC-5677 off from Dana Okafor, hope it lands nicely with you. Enjoy the rest of your stretch.\n\nCheers,\n\nNotice NTC-5677 to Dana Okafor:\n- response due date: 11 August 2027\n- office cutoff on the due date: 2027-08-11 20:15:00 +0300\n- response sent: 2027-08-11 14:10:00 -0300 [same instant in office time: 2027-08-11 20:10:00 +0300]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Dana Okafor to notice NTC-5677 on time under the receipt rule?"
 },
 {
  "qid": "q6a1f98b6cb",
  "kind": "yes/no",
  "text": "[intake] Dana Okafor sends file NTC-6683 about the notice response to intake_team\n[tag] standard_handling\n\nNotice NTC-6683 to Dana Okafor:\n- response due date: Saturday, 27 November 2027\n- office cutoff on the due date: 2027-11-27T20:05:00+05:30\n- response sent: 2027-11-28T18:28:00+03:00 [same instant in office time: 2027-11-28T20:58:00+05:30]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Dana Okafor on time under the receipt rule?"
 },
 {
  "qid": "q3586ca762b",
  "kind": "yes/no",
  "text": "Ana Ruiz: file CASE-6831 about the complaint filing is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.\n\nCase CASE-6831, party Ana Ruiz:\n- incident date: Tuesday, 14 September 2027\n- discovery date: Sunday, 29 August 2027\n- complaint filed on: Monday, 20 September 2027\n- days from the incident date to the filing: 6 days\n- days from the discovery date to the filing: 22 days",
  "question": "Filing rule: the complaint must be filed within 14 days from whichever is later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 14 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the complaint filed on or before the final day of the filing period?"
 },
 {
  "qid": "qdfbf8908e5",
  "kind": "choice",
  "text": "from: Iris Vance\nfile: CASE-9992\nsubject: the complaint filing\nroute: service_desk\nlane: fast\n\nCase CASE-9992, party Iris Vance:\n- incident date: Thursday, April 1, 2027\n- discovery date: Monday, March 22, 2027",
  "question": "Filing rule: the complaint must be filed inside a span of 45 days that runs after the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, what is the latest date on which the complaint can be filed in time?",
  "options": [
   "Sunday, May 16, 2027",
   "Monday, May 17, 2027",
   "Thursday, June 3, 2027",
   "Tuesday, May 18, 2027"
  ]
 },
 {
  "qid": "qc043bacdde",
  "kind": "yes/no",
  "text": "file: NTC-3451\nsent_by: Freya Holm\nsubject: the reply timing question\nteam: service desk\nnote: a friendly hello\n\nNotice NTC-3451 to Freya Holm:\n- response due date: September 3, 2028\n- office cutoff on the due date: 2028-09-03T16:56:00Z\n- response sent: 3 September 2028, 10:01 (UTC-07:00) [same instant in office time: 2028-09-03T17:01:00Z]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Freya Holm to notice NTC-3451 on time under the receipt rule?"
 },
 {
  "qid": "qc13e3583a1",
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
  "qid": "qa2a2183706",
  "kind": "yes/no",
  "text": "sent_by: Clara Weiss\nsubject: the appeal deadline\nfile: CASE-5450\nteam: records clerk\nnote: kind regards\n\nCase CASE-5450, party Clara Weiss:\n- decision date: May 11, 2028\n- delivery date: May 13, 2028\n- appeal filed on: June 27, 2028\n- days from the decision date to the filing: 47 days\n- days from the delivery date to the filing: 45 days",
  "question": "Filing rule: the appeal must be filed within 45 days after the later date out of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, did Clara Weiss fail to file the appeal by the deadline?"
 },
 {
  "qid": "q9d6e0ace76",
  "kind": "yes/no",
  "text": "subject: the cash ledger check\nteam: review_team\nsent_by: Aiko Brandt\nfile: LED-1517\n\nCash ledger LED-1517, teller Aiko Brandt:\n- Friday, August 15, 2025: withdrawal of $11,374\n- Sunday, August 17, 2025: deposit of $2,307\n- Sunday, August 17, 2025: deposit of $11,097\n- Sunday, August 17, 2025: withdrawal of $9,231\n- Sunday, August 17, 2025: withdrawal of $5,770\nDay under review: Sunday, August 17, 2025",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is greater than the sum of $15,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs a cash report required for ledger LED-1517 on the day under review?"
 },
 {
  "qid": "q2d802de08b",
  "kind": "yes/no",
  "text": "Subject: hello again\nHi review team,\nQuick note: Dana Okafor sent in file STAY-9007 about the border stay check, so have a look when you like.\nTake care,\n\nStay record STAY-9007 for Dana Okafor:\n- entry day 17 May 2026, exit day 30 May 2026 (whole stay: 14 days)\nReference date: 15 June 2026\nWindow checked: 17 May 2026 to 15 June 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 14 days within any 30-day window that keeps moving. Day counts are calendar days, and entry and exit days both count as days present. Only one 30-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 14 days, and within the limit if it is 14 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Dana Okafor, under the stay rule, over the stay limit for the window ending on 15 June 2026?"
 },
 {
  "qid": "qcad1f9eef4",
  "kind": "choice",
  "text": "{\"file\": \"LED-4785\", \"sent_by\": \"Lucas Brenner\", \"subject\": \"the cash ledger check\", \"channel\": \"formal_intake\", \"team\": \"the desk\"}\n\nCash ledger LED-4785, teller Lucas Brenner:\n- Tuesday, 15 December 2026: withdrawal of $2,958\n- Wednesday, 16 December 2026: deposit of $1,710\n- Wednesday, 16 December 2026: withdrawal of $2,030\n- Wednesday, 16 December 2026: deposit of $11,471\n- Wednesday, 16 December 2026: withdrawal of $2,323\n- Thursday, 17 December 2026: deposit of $7,261\nDay under review: Wednesday, 16 December 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is greater than the sum of $10,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals in ledger LED-4785 for Wednesday, 16 December 2026 call for a cash report under the cash rule?",
  "options": [
   "Both totals",
   "Neither total",
   "Only the deposit total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q795e30e57d",
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
  "qid": "q191ffbfc57",
  "kind": "yes/no",
  "text": "Tomas Lindqvist: Routine send, NTC-3682 about the reply timing question.\nintake team: Received, thank you.\n\nNotice NTC-3682 to Tomas Lindqvist:\n- response due date: 12 September 2028\n- office cutoff on the due date: 2028-09-12T22:26:00+09:00\n- response sent: 2028-09-12T00:17:00-05:00 [same instant in office time: 2028-09-12T14:17:00+09:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the response from Tomas Lindqvist to notice NTC-3682 late, meaning counted as received after the due date?"
 },
 {
  "qid": "q34b34535c1",
  "kind": "yes/no",
  "text": "Title | file NTC-7386 about the response deadline\nRequester | Clara Weiss\nTo | records clerk\nThank you kindly for the careful handling.\n\nNotice NTC-7386 to Clara Weiss:\n- response due date: 2026-10-19\n- office cutoff on the due date: 2026-10-19 20:54:00 -0500\n- response sent: 2026-10-20 07:12:00 -0700 [same instant in office time: 2026-10-20 09:12:00 -0500]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is it true that the response from Clara Weiss was not on time?"
 },
 {
  "qid": "qcf6f35692d",
  "kind": "yes/no",
  "text": "subject: the response deadline\nteam: review_team\nsent_by: Iris Vance\nfile: NTC-5502\n\nNotice NTC-5502 to Iris Vance:\n- response due date: 2025-08-20\n- office cutoff on the due date: 2025-08-20 13:19:00 +0100\n- response sent: 2025-08-20 09:23:00 -0300 [same instant in office time: 2025-08-20 13:23:00 +0100]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Iris Vance to notice NTC-5502 on time under the receipt rule?"
 },
 {
  "qid": "qc9e8e36b54",
  "kind": "yes/no",
  "text": "sent_by: Aiko Brandt\nfile: CASE-2194\nsubject: the appeal deadline\nteam: admin team\nchannel: friendly chat\n\nCase CASE-2194, party Aiko Brandt:\n- decision date: 2 Jul 2028\n- delivery date: 1 Jul 2028\n- appeal filed on: 20 Aug 2028\n- days from the decision date to the filing: 49 days\n- days from the delivery date to the filing: 50 days",
  "question": "Filing rule: the appeal must be filed within 28 days measured from the later of the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the appeal from Aiko Brandt in case CASE-2194 filed on or before the final day of the filing period?"
 },
 {
  "qid": "q8260b7439f",
  "kind": "choice",
  "text": "Nadia Kowal: file NTC-2842 about the reply timing question goes to the desk as usual\ndesk: understood, standard path applied\n\nNotice NTC-2842 to Nadia Kowal:\n- response due date: 2027-09-30\n- office cutoff on the due date: 30 September 2027, 18:44 (UTC+00:00)\n- response sent: 27 September 2027, 21:39 (UTC+03:00) [same instant in office time: 27 September 2027, 18:39 (UTC+00:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on which date does the office count the response to notice NTC-2842 as received under the receipt rule?",
  "options": [
   "27 Sep 2027",
   "26 Sep 2027"
  ]
 },
 {
  "qid": "q35b290cb06",
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
  "qid": "q89a12b8ae9",
  "kind": "yes/no",
  "text": "{\"file\": \"STAY-4131\", \"sent_by\": \"Bruno Lacerda\", \"subject\": \"the visa stay count\", \"team\": \"intake team\", \"note\": \"with kind regards\"}\n\nStay record STAY-4131 for Bruno Lacerda:\n- entry day 4 Oct 2026, exit day 10 Oct 2026 (whole stay: seven days)\n- entry day 5 Nov 2026, exit day 28 Dec 2026 (whole stay: 54 days)\nReference date: 29 Dec 2026\nWindow checked: 1 Sep 2026 to 29 Dec 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days within any 120-day window that keeps moving. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, do the days present for Bruno Lacerda inside the checked window ending on the reference date exceed the stay limit?"
 },
 {
  "qid": "q36cffee7ab",
  "kind": "choice",
  "text": "[review] file=LED-4515 for the branch cash review, sender=Lena Whitcombe\n[review] destination=review team, big_thanks\n\nCash ledger LED-4515, teller Lena Whitcombe:\n- 1 April 2025: deposit of 8,593.00 USD\n- 1 April 2025: deposit of 1,407.00 USD\n- 1 April 2025: withdrawal of 10,070.00 USD\n- 1 April 2025: withdrawal of 3,232.00 USD\n- 2 April 2025: withdrawal of 4,307.00 USD\nDay under review: 1 April 2025",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any sum more than 10,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nFor 1 April 2025, which of the day's totals, under the cash rule, call for a cash report?",
  "options": [
   "Both totals",
   "Only the withdrawal total",
   "Neither total",
   "Only the deposit total"
  ]
 },
 {
  "qid": "q72a224be52",
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
  "qid": "q55a043364d",
  "kind": "choice",
  "text": "File STAY-8939 about the residence day count is set out below. Sara Ilves sends over the document for the intake team. Thank you for your attention.\n\nStay record STAY-8939 for Sara Ilves:\n- entry day Saturday, 2 October 2027, exit day Monday, 18 October 2027 (whole stay: seventeen days)\n- entry day Sunday, 14 November 2027, exit day Tuesday, 21 December 2027 (whole stay: 38 days)\nReference date: Saturday, 8 January 2028\nWindow checked: Monday, 11 October 2027 to Saturday, 8 January 2028, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 45 days in any 90-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present fall inside the checked window that ends on Saturday, 8 January 2028 for file STAY-8939?",
  "options": [
   "46 days",
   "48 days"
  ]
 },
 {
  "qid": "q2d50aefa17",
  "kind": "yes/no",
  "text": "Desk memo: Please be advised that Felix Ortega has sent file POL-2206 concerning the cover question to the desk.\nKindly route it to the review team at your convenience. Thank you for your attention.\n\nPolicy POL-2206, holder Felix Ortega:\n- policy start date: Thursday, December 17, 2026\n- storm damage cover: added by a rider effective Thursday, July 8, 2027\n- storm damage loss on: Thursday, July 22, 2027\n- days from the policy start date to the loss: 217 days\n- days from the rider effective date to the loss: 14 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 15 days with the start date itself left out, beginning the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 15 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is it true that the storm damage loss in policy POL-2206 is not covered?"
 }
]
