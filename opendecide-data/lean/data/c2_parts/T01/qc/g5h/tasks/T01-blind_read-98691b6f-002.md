# G5-H blind read (all free-form rows) T01-blind_read-98691b6f-002 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g5h/answers/T01-blind_read-98691b6f-002.json

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
  "qid": "q450a8b53d0",
  "kind": "choice",
  "text": "Ana Ruiz sends file CASE-7003 about the complaint filing to the admin team. Quick note, I am snowed under. The attachment carries the main points near the top. Off I go.\n\nCase CASE-7003, party Ana Ruiz:\n- incident date: December 16, 2026\n- discovery date: December 13, 2026",
  "question": "Filing rule: the complaint must be filed inside fourteen days reckoned from the date that falls later among the dates below: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is fourteen days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, what is the latest date on which the complaint can be filed in time?",
  "options": [
   "December 30, 2026",
   "December 28, 2026",
   "December 27, 2026",
   "December 29, 2026"
  ]
 },
 {
  "qid": "qa6e099abe1",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nPriya Raman is sending file POL-2847 about the loss claim. Writing fast, I am swamped. Attached is the file.\nThanks,\n\nPolicy POL-2847, holder Priya Raman:\n- policy start date: Monday, 22 November 2027\n- burst pipe damage cover: part of the base policy\n- burst pipe damage loss on: Thursday, 6 January 2028\n- days from the policy start date to the loss: 45 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days with the start date itself left out, beginning the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is it true that the burst pipe damage loss for Priya Raman is not covered?"
 },
 {
  "qid": "qb63d82b790",
  "kind": "yes/no",
  "text": "Jonas Feld: file NTC-3877 about the response deadline is here.\nintake team: received, thanks.\nintake team: that is everything for this file.\n\nNotice NTC-3877 to Jonas Feld:\n- response due date: Sunday, June 4, 2028\n- office cutoff on the due date: 2028-06-04 18:53:00 +0100\n- response sent: 2028-06-04 13:48:00 -0400 [same instant in office time: 2028-06-04 18:48:00 +0100]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the response from Jonas Feld to notice NTC-3877 under the receipt rule was not on time?"
 },
 {
  "qid": "q510721cfe1",
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
  "qid": "q4c70bf00d3",
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
  "qid": "q2d1fe4ca2c",
  "kind": "choice",
  "text": "Dear front desk,\nI am writing to share file NTC-1648 about the response deadline, sent by Paolo Greco. Thank you for reading this message. The file is in full and in good shape. With respect and thanks.\nYours faithfully\n\nNotice NTC-1648 to Paolo Greco:\n- notice date: March 29, 2028\n- sent by: post\n- 14 days after the notice date, before any postal add-on or closure: April 12, 2028\nOffice closures: none.",
  "question": "Response rule: a response is due 14 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 5 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the due date for the response from Paolo Greco to the notice under the response rule?",
  "options": [
   "April 15, 2028",
   "April 17, 2028",
   "April 16, 2028"
  ]
 },
 {
  "qid": "q1c0f7870cf",
  "kind": "yes/no",
  "text": "Tomas Lindqvist: Dear team, I am forwarding file POL-5670 about the insurance claim to the intake team.\nintake: Thank you for passing it along.\nteam: With thanks for your courtesy.\n\nPolicy POL-5670, holder Tomas Lindqvist:\n- policy start date: Saturday, 23 October 2027\n- burst pipe damage cover: added by a rider effective Friday, 5 May 2028\n- burst pipe damage loss on: Monday, 5 June 2028\n- days from the policy start date to the loss: 226 days\n- days from the rider effective date to the loss: 31 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days commencing on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the burst pipe damage loss under policy POL-5670 within the waiting period?"
 },
 {
  "qid": "qdae437d5ed",
  "kind": "yes/no",
  "text": "Hana Sato is passing along file LED-2187 about the branch cash review to the admin team. The file is short and goes straight to the pile. It is a quick, friendly handover.\n\nCash ledger LED-2187, teller Hana Sato:\n- 20 May 2026: withdrawal of $1,662.00\n- 20 May 2026: withdrawal of $8,337.00\n- 20 May 2026: deposit of $7,795.00\n- 22 May 2026: deposit of $7,113.00\nDay under review: 20 May 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is $10,000.00 or above, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs a cash report required for ledger LED-2187 on the day under review?"
 },
 {
  "qid": "qe9a71fbf3e",
  "kind": "yes/no",
  "text": "File: CASE-6413\nSubject: the complaint filing\nSent by: Clara Weiss\nHey there, this goes over to the records clerk. Hope everything is going nicely for you!\n\nCase CASE-6413, party Clara Weiss:\n- incident date: Friday, October 17, 2025\n- discovery date: Friday, October 3, 2025\n- complaint filed on: Monday, November 3, 2025\n- days from the incident date to the filing: 17 days\n- days from the discovery date to the filing: 31 days",
  "question": "Filing rule: the complaint must be filed inside 14 days counted from the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 14 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the complaint from Clara Weiss in case CASE-6413 filed on or before the final day of the filing period?"
 },
 {
  "qid": "q6cb4ef591b",
  "kind": "yes/no",
  "text": "Bruno Lacerda: Busy desk, sending STAY-9105 about the residence day count, straight over.\nhelp desk: In hand.\n\nStay record STAY-9105 for Bruno Lacerda:\n- entry day June 22, 2026, exit day July 6, 2026 (whole stay: fifteen days)\n- entry day July 24, 2026, exit day August 3, 2026 (whole stay: eleven days)\n- entry day August 20, 2026, exit day September 12, 2026 (whole stay: 24 days)\nReference date: September 26, 2026\nWindow checked: May 30, 2026 to September 26, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days in every 120-day run that moves forward through time. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Bruno Lacerda over the stay limit, with more days present inside the window that ends on the reference date in file STAY-9105, under the stay rule?"
 },
 {
  "qid": "qde0ec97a9b",
  "kind": "yes/no",
  "text": "Aiko Brandt: Dear team, I am forwarding file POL-5347 about the cover question to the intake team.\nintake: Thank you for passing it along.\nteam: With thanks for your courtesy.\n\nPolicy POL-5347, holder Aiko Brandt:\n- policy start date: September 27, 2027\n- glass breakage cover: added by a rider effective April 19, 2028\n- glass breakage loss on: May 10, 2028\n- days from the policy start date to the loss: 226 days\n- days from the rider effective date to the loss: 21 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is the glass breakage loss covered under the cover rule?"
 },
 {
  "qid": "q95750181d4",
  "kind": "choice",
  "text": "From: Lucas Brenner\nFile: POL-5479\nSent to: review team\nThe file about the cover question is shared in the usual way.\n\nPolicy POL-5479, holder Lucas Brenner:\n- policy start date: Sunday, 11 July 2027\n- storm damage cover: added by a rider effective Thursday, 11 November 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days that begins on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the earliest date on which the storm damage loss would be covered?",
  "options": [
   "Friday, 3 December 2027",
   "Wednesday, 1 December 2027",
   "Thursday, 2 December 2027"
  ]
 },
 {
  "qid": "q800518e8bd",
  "kind": "choice",
  "text": "Dana Okafor: Hi, here is file POL-8252 about the insurance claim, with plenty of cheer.\ndesk: Lovely, thanks so much!\ndesk: That is fun to read.\n\nPolicy POL-8252, holder Dana Okafor:\n- policy start date: 29 November 2027\n- burst pipe damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days that begins on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which the burst pipe damage loss in policy POL-8252 would be covered under the cover rule?",
  "options": [
   "12 January 2028",
   "14 January 2028",
   "13 January 2028"
  ]
 },
 {
  "qid": "qb35a9683f8",
  "kind": "choice",
  "text": "Dear duty clerk,\nMaya Lindgren is sending file STAY-7013 about the border stay check. It is attached here. Hope your work goes well.\nCheers,\n\nStay record STAY-7013 for Maya Lindgren:\n- entry day 24 June 2025, exit day 6 August 2025 (whole stay: 44 days)\n- entry day 3 September 2025, exit day 22 September 2025 (whole stay: 20 days)\nReference date: 21 October 2025\nWindow checked: 24 July 2025 to 21 October 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 30 days during any 90-day window that moves ahead. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, how many days present for file STAY-7013 fall inside the checked window that ends on the reference date?",
  "options": [
   "34 days",
   "64 days",
   "36 days"
  ]
 },
 {
  "qid": "qf237ba8f91",
  "kind": "yes/no",
  "text": "Theo Kalnins: sending LED-5912 about the branch cash review, fast and short.\nhelp desk: okay, got it.\nhelp desk: thanks, that is the whole thing.\n\nCash ledger LED-5912, teller Theo Kalnins:\n- Friday, 14 April 2028: deposit of 15,135.00 USD\n- Friday, 14 April 2028: withdrawal of 15,000.00 USD\n- Friday, 14 April 2028: deposit of 1,527.00 USD\n- Sunday, 16 April 2028: deposit of 3,613.00 USD\nDay under review: Friday, 14 April 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is 15,000.00 USD or more, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, is a cash report required for the day under review in ledger LED-5912?"
 },
 {
  "qid": "qe0093bc60e",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nHana Sato is sending file NTC-2583 about the notice response, with the main points at the top. Quick note, I am buried under other work.\nBest,\n\nNotice NTC-2583 to Hana Sato:\n- response due date: 14 April 2026\n- office cutoff on the due date: 2026-04-14 18:25:00 +0300\n- response sent: 2026-04-14 16:30:00 +0100 [same instant in office time: 2026-04-14 18:30:00 +0300]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Hana Sato to the notice counted as received after the due date?"
 },
 {
  "qid": "qcf95087d80",
  "kind": "yes/no",
  "text": "Sent by: Clara Weiss\nFile: NTC-2502\nSent to: review team\nThank you for your attention to the file about the response deadline. I remain grateful for the careful reading.\n\nNotice NTC-2502 to Clara Weiss:\n- response due date: Sunday, December 13, 2026\n- office cutoff on the due date: 13 December 2026, 18:10 (UTC-04:00)\n- response sent: 14 December 2026, 03:35 (UTC+05:30) [same instant in office time: 13 December 2026, 18:05 (UTC-04:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Clara Weiss to notice NTC-2502 on time under the receipt rule?"
 },
 {
  "qid": "qb6e36a51fc",
  "kind": "choice",
  "text": "Omar Saleh sends file CASE-7142 about the appeal deadline to the desk. The file is set out in full with the usual headings. Thank you for your attention to this matter.\n\nCase CASE-7142, party Omar Saleh:\n- billing date: Tuesday, 25 May 2027\n- statement date: Saturday, 15 May 2027",
  "question": "Filing rule: the dispute must be filed within 59 days measured beyond the later of these dates: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 59 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the final day on which Omar Saleh can still file the dispute in time for case CASE-7142?",
  "options": [
   "Thursday, 22 July 2027",
   "Friday, 23 July 2027",
   "Wednesday, 21 July 2027"
  ]
 },
 {
  "qid": "q36b3cf9392",
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
  "qid": "q2aa74c81b0",
  "kind": "choice",
  "text": "Theo Kalnins: Sending CASE-9038 about the appeal deadline as usual.\ncase team: Received.\n\nCase CASE-9038, party Theo Kalnins:\n- decision date: 10 Mar 2028\n- delivery date: 25 Feb 2028",
  "question": "Filing rule: the appeal must be filed inside thirteen days reckoned from the date that falls later among the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is thirteen days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the latest date by which the appeal can be filed in time?",
  "options": [
   "24 Mar 2028",
   "23 Mar 2028",
   "25 Mar 2028"
  ]
 },
 {
  "qid": "q04d9b988e1",
  "kind": "choice",
  "text": "Kofi Mensah: Greetings, I am sending file CASE-1226 about the complaint filing for your kind attention.\ncase team: Thank you very much, it has been received.\n\nCase CASE-1226, party Kofi Mensah:\n- incident date: Wednesday, September 17, 2025\n- discovery date: Thursday, September 18, 2025",
  "question": "Filing rule: the complaint must be filed within 28 days past the later of the dates below: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the final day on which Kofi Mensah can still file the complaint in time for case CASE-1226?",
  "options": [
   "Thursday, October 16, 2025",
   "Saturday, October 18, 2025",
   "Tuesday, October 28, 2025"
  ]
 },
 {
  "qid": "qce835defbb",
  "kind": "yes/no",
  "text": "Bruno Lacerda: sending file STAY-8529 about the visa stay count, with thanks.\nintake team: thank you, this is received.\nintake team: appreciated.\n\nStay record STAY-8529 for Bruno Lacerda:\n- entry day 15 Jul 2025, exit day 20 Sep 2025 (whole stay: 68 days)\nReference date: 11 Dec 2025\nWindow checked: 14 Aug 2025 to 11 Dec 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days in any 120-day span that moves ahead with each new day. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, is the person in file STAY-8529 over the stay limit, with more days present in the window ending on 11 Dec 2025?"
 },
 {
  "qid": "qba2417d9b0",
  "kind": "choice",
  "text": "Dear front desk,\nInes Duarte is sending file CASE-7437 about the appeal deadline. This is a routine send and the file is full. The matter is in good shape as usual.\nRegards\n\nCase CASE-7437, party Ines Duarte:\n- decision date: 22 Aug 2025\n- delivery date: 25 Aug 2025",
  "question": "Filing rule: the appeal must be filed within 40 days after the later date out of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 40 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, by which final day can Ines Duarte still file the appeal and remain in time?",
  "options": [
   "4 Oct 2025",
   "5 Oct 2025",
   "2 Oct 2025",
   "6 Oct 2025"
  ]
 },
 {
  "qid": "q6e51d4655a",
  "kind": "choice",
  "text": "File: CASE-1693\nSubject: the claim deadline question\nFrom: Malik Osei\nHey there, this is heading off to the records clerk with a smile. Hope you are having a fun run of things!\n\nCase CASE-1693, party Malik Osei:\n- invoice date: 10 Sep 2026\n- goods received date: 10 Oct 2026",
  "question": "Filing rule: the claim must be filed inside 10 days extending past the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 10 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the final day on which Malik Osei can still file the claim in time for case CASE-1693?",
  "options": [
   "20 Sep 2026",
   "20 Oct 2026",
   "19 Oct 2026"
  ]
 },
 {
  "qid": "q031bf90cf4",
  "kind": "choice",
  "text": "Theo Kalnins: Hi there, sending POL-5910 about the loss claim, hope the rest is lovely!\nhelp desk: Lovely, thanks a bunch!\n\nPolicy POL-5910, holder Theo Kalnins:\n- policy start date: Sunday, September 26, 2027\n- power surge damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of fifteen days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is fifteen days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which the power surge damage loss in policy POL-5910 would be covered under the cover rule?",
  "options": [
   "Monday, October 11, 2027",
   "Thursday, October 14, 2027",
   "Tuesday, October 12, 2027"
  ]
 },
 {
  "qid": "q78a4ff38fa",
  "kind": "choice",
  "text": "Maya Lindgren has shared file LED-9060 about the branch cash review with the desk. The file goes in the usual way. This memo is for the file set.\n\nCash ledger LED-9060, teller Maya Lindgren:\n- Tuesday, October 27, 2026: withdrawal of $3,131.00\n- Tuesday, October 27, 2026: withdrawal of $1,869.00\n- Tuesday, October 27, 2026: deposit of $7,212.00\n- Thursday, October 29, 2026: deposit of $3,814.00\nDay under review: Tuesday, October 27, 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is anything strictly greater than $5,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals in ledger LED-9060 call for a cash report?",
  "options": [
   "Only the withdrawal total",
   "Both totals",
   "Only the deposit total",
   "Neither total"
  ]
 },
 {
  "qid": "qc7dd4f1a8a",
  "kind": "choice",
  "text": "Dear duty clerk,\nQuick send from Lucas Brenner: file CASE-9203 about the complaint filing is in. Sending it over fast as I am on the move. The attachment is full and whole. Thanks a bunch.\nKind regards\n\nCase CASE-9203, party Lucas Brenner:\n- incident date: 2027-02-27\n- discovery date: 2027-02-24",
  "question": "Filing rule: the complaint must be filed inside 90 days beginning at the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, until which final day may Lucas Brenner file the complaint and still be in time?",
  "options": [
   "2027-05-27",
   "2027-05-26",
   "2027-05-25",
   "2027-05-28"
  ]
 },
 {
  "qid": "qeb2abe1f75",
  "kind": "choice",
  "text": "Hi duty clerk,\nBruno Lacerda is sending file POL-3957 about the cover question, with the main points at the top. Quick note, I am buried under other work.\nBest,\n\nPolicy POL-3957, holder Bruno Lacerda:\n- policy start date: March 6, 2026\n- power surge damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of fifteen days starting with the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is fifteen days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the earliest date on which this power surge damage loss would be covered?",
  "options": [
   "March 20, 2026",
   "March 22, 2026",
   "March 21, 2026"
  ]
 },
 {
  "qid": "q497de8e111",
  "kind": "choice",
  "text": "Felix Ortega: hey, here is LED-6004 about the branch cash review, sorry for the wait!\nservice desk: all good, got it.\nservice desk: brilliant, thanks a lot.\n\nCash ledger LED-6004, teller Felix Ortega:\n- Sunday, 23 May 2027: deposit of $2,878\n- Sunday, 23 May 2027: deposit of $3,602\n- Sunday, 23 May 2027: withdrawal of $4,662\n- Sunday, 23 May 2027: withdrawal of $1,669\n- Tuesday, 25 May 2027: deposit of $2,555\nDay under review: Sunday, 23 May 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is a figure greater than $5,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, which of the day's totals for Sunday, 23 May 2027 call for a cash report?",
  "options": [
   "Only the withdrawal total",
   "Only the deposit total",
   "Neither total",
   "Both totals"
  ]
 },
 {
  "qid": "q580c5d80b6",
  "kind": "yes/no",
  "text": "Ana Ruiz: Hello, I am sending file NTC-8765 about the notice response to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nNotice NTC-8765 to Ana Ruiz:\n- response due date: 5 December 2025\n- office cutoff on the due date: 5 December 2025, 13:20 (UTC+02:00)\n- response sent: 4 December 2025, 08:39 (UTC+03:00) [same instant in office time: 4 December 2025, 07:39 (UTC+02:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the response from Ana Ruiz to notice NTC-8765 late, meaning counted as received after the due date?"
 },
 {
  "qid": "qa295da9ce2",
  "kind": "choice",
  "text": "File: LED-1066\nSubject: the cash ledger check\nFrom: Owen Pryce\nRespectfully passing this file on to the review team. Thank you kindly for your attention.\n\nCash ledger LED-1066, teller Owen Pryce:\n- 2027-11-15: withdrawal of $2,683.00\n- 2027-11-15: withdrawal of $10,313.00\n- 2027-11-15: deposit of $1,282.00\n- 2027-11-15: deposit of $3,445.00\n- 2027-11-16: withdrawal of $5,477.00\nDay under review: 2027-11-15",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is greater than $10,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, which of the day's totals for Owen Pryce on 2027-11-15 call for a cash report?",
  "options": [
   "Both totals",
   "Only the withdrawal total",
   "Neither total",
   "Only the deposit total"
  ]
 },
 {
  "qid": "qf248674c97",
  "kind": "yes/no",
  "text": "Felix Ortega: file POL-9693 about the insurance claim is here.\nintake team: received, thanks.\nintake team: that is everything for this file.\n\nPolicy POL-9693, holder Felix Ortega:\n- policy start date: 2026-10-11\n- glass breakage cover: part of the base policy\n- glass breakage loss on: 2026-10-26\n- days from the policy start date to the loss: 15 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWould policy POL-9693 cover this glass breakage loss under the cover rule?"
 },
 {
  "qid": "q25b662ffab",
  "kind": "yes/no",
  "text": "Omar Saleh has sent file CASE-4574 about the complaint filing to the admin team. It is a friendly little bundle for the admin desks. Thanks for the lovely teamwork.\n\nCase CASE-4574, party Omar Saleh:\n- purchase date: 5 July 2027\n- handover date: 10 July 2027\n- refund request filed on: 10 August 2027\n- days from the purchase date to the filing: 36 days\n- days from the handover date to the filing: 31 days",
  "question": "Filing rule: the refund request must be filed inside fourteen days counted from the later of these dates: the purchase date and the handover date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is fourteen days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the refund request in case CASE-4574 filed late, after the final day of the filing period?"
 },
 {
  "qid": "q173312c9bf",
  "kind": "yes/no",
  "text": "Clara Weiss: Hey, sending CASE-9311 about the claim deadline question, hope all is well!\nhelp desk: Lovely, thanks for sending it across.\n\nCase CASE-9311, party Clara Weiss:\n- invoice date: 2026-03-01\n- goods received date: 2026-03-03\n- claim filed on: 2026-03-24\n- days from the invoice date to the filing: 23 days\n- days from the goods received date to the filing: 21 days",
  "question": "Filing rule: the claim must be filed within 21 days reckoned after the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the claim filed on or before the final day of the filing period?"
 },
 {
  "qid": "qcce661bfea",
  "kind": "yes/no",
  "text": "Hey there, quick heads up that Kofi Mensah has sent file NTC-2210 about the response deadline to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.\n\nNotice NTC-2210 to Kofi Mensah:\n- response due date: Monday, 22 June 2026\n- office cutoff on the due date: 22 June 2026, 19:43 (UTC-05:00)\n- response sent: 23 June 2026, 09:48 (UTC+09:00) [same instant in office time: 22 June 2026, 19:48 (UTC-05:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the response to notice NTC-2210 late under the receipt rule, counted as received after the due date?"
 },
 {
  "qid": "qff0317c98a",
  "kind": "choice",
  "text": "Internal memo for the desk.\n\nLena Whitcombe sends file POL-4658 about the insurance claim to the desk, with the review team copied in. Thank you for your careful work on this matter. I appreciate the effort put into it.\n\nPolicy POL-4658, holder Lena Whitcombe:\n- policy start date: Tuesday, June 1, 2027\n- glass breakage cover: added by a rider effective Thursday, July 29, 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 90 days that starts on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 90 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the earliest date on which the glass breakage loss under policy POL-4658 would be covered?",
  "options": [
   "Friday, October 29, 2027",
   "Thursday, October 28, 2027",
   "Saturday, October 30, 2027",
   "Tuesday, October 26, 2027"
  ]
 },
 {
  "qid": "q06e9f879eb",
  "kind": "choice",
  "text": "Aiko Brandt: file CASE-5333 about the claim deadline question is attached.\ncase team: received, thanks.\ncase team: that is the whole file.\n\nCase CASE-5333, party Aiko Brandt:\n- invoice date: Friday, 25 December 2026\n- goods received date: Sunday, 20 December 2026",
  "question": "Filing rule: the claim must be filed inside 21 days extending past the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, by which final day must the claim be filed to still count as in time?",
  "options": [
   "Friday, 15 January 2027",
   "Thursday, 14 January 2027",
   "Wednesday, 13 January 2027",
   "Sunday, 10 January 2027"
  ]
 },
 {
  "qid": "qd9361e3604",
  "kind": "yes/no",
  "text": "Hi admin team, Paolo Greco here with file PO-5680 about the purchase request. Thanks so much for helping keep everything tidy. It is a pleasure to share it with you all.\n\nPurchase log PO-5680, kept by Paolo Greco, vendor Corvane Office:\n- earlier purchase on 2027-10-29: $2,084.00\n- earlier purchase on 2028-02-22: $5,318.00\n- new request on 2028-03-14: $5,261.00\nWindow checked: 2028-01-15 to 2028-03-14, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is greater than $10,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request from Paolo Greco need written quotes under the purchase rule?"
 },
 {
  "qid": "q8d78deb380",
  "kind": "yes/no",
  "text": "From: Nadia Kowal\nFile: STAY-2542\nSent to: review team\nThe file about the visa stay count is shared in the usual way.\n\nStay record STAY-2542 for Nadia Kowal:\n- entry day 2025-12-03, exit day 2025-12-06 (whole stay: 4 days)\n- entry day 2025-12-24, exit day 2026-01-19 (whole stay: 27 days)\nReference date: 2026-02-05\nWindow checked: 2025-11-08 to 2026-02-05, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 30 days during any 90-day window that moves ahead. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the person in file STAY-2542 is not over the stay limit?"
 },
 {
  "qid": "qae8a7da68d",
  "kind": "choice",
  "text": "Felix Ortega: Sending POL-9635 about the loss claim, a routine send.\nintake team: Received, thanks.\n\nPolicy POL-9635, holder Felix Ortega:\n- policy start date: Wednesday, 20 October 2027\n- glass breakage cover: added by a rider effective Saturday, 22 April 2028",
  "question": "Cover rule: a loss is covered only after a waiting period of 60 days whose earliest counted day is the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 60 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which a loss of this kind would count as covered for policy POL-9635 under the cover rule?",
  "options": [
   "Wednesday, 21 June 2028",
   "Thursday, 22 June 2028",
   "Monday, 20 December 2027",
   "Tuesday, 20 June 2028"
  ]
 },
 {
  "qid": "q646826f716",
  "kind": "choice",
  "text": "Freya Holm sends file STAY-1696 about the visa stay count to the desk. This is the regular version, laid out in the standard format. The desk has the full set on hand. Passing it along as usual.\n\nStay record STAY-1696 for Freya Holm:\n- entry day August 27, 2027, exit day September 18, 2027 (whole stay: 23 days)\n- entry day October 23, 2027, exit day November 22, 2027 (whole stay: 31 days)\n- entry day January 6, 2028, exit day January 9, 2028 (whole stay: 4 days)\nReference date: February 27, 2028\nWindow checked: September 1, 2027 to February 27, 2028, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 90 days in any 180-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days, under the stay rule, was Freya Holm present inside the checked window ending on February 27, 2028?",
  "options": [
   "35 days",
   "52 days",
   "53 days"
  ]
 },
 {
  "qid": "qef8bcef5b2",
  "kind": "yes/no",
  "text": "Nadia Kowal: Sending PO-4766 about the purchase request as usual.\ncase team: Received.\n\nPurchase log PO-4766, kept by Nadia Kowal, vendor Brightwell Supply:\n- earlier purchase on Tuesday, 26 August 2025: 5,972.00 USD\n- earlier purchase on Saturday, 20 December 2025: 6,162.00 USD\n- new request on Tuesday, 24 February 2026: 3,839.00 USD\nWindow checked: Thursday, 27 November 2025 to Tuesday, 24 February 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any total greater than 10,000.00 USD, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the request from Nadia Kowal, under the purchase rule, call for written quotes in log PO-4766?"
 },
 {
  "qid": "qac03b46448",
  "kind": "yes/no",
  "text": "Sent by: Paolo Greco\nFile: STAY-6488\nSent to: review team\nThank you for your attention to the file about the residence day count. I remain grateful for the careful reading.\n\nStay record STAY-6488 for Paolo Greco:\n- entry day Tuesday, 12 May 2026, exit day Friday, 29 May 2026 (whole stay: 18 days)\n- entry day Sunday, 31 May 2026, exit day Monday, 20 July 2026 (whole stay: 51 days)\n- entry day Sunday, 23 August 2026, exit day Thursday, 27 August 2026 (whole stay: 5 days)\nReference date: Sunday, 27 September 2026\nWindow checked: Sunday, 31 May 2026 to Sunday, 27 September 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 60 days in any rolling 120-day window. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does file STAY-6488 show more days present in the checked window ending on the reference date than the limit?"
 },
 {
  "qid": "qfcaf7ea158",
  "kind": "choice",
  "text": "Dear front desk,\nRavi Anand is writing to share file CASE-2441 about the claim deadline question with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,\n\nCase CASE-2441, party Ravi Anand:\n- inspection date: Saturday, 8 November 2025\n- report date: Thursday, 9 October 2025",
  "question": "Filing rule: the objection must be filed within 95 days measured from the later of the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 95 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the latest date, under the filing rule, on which the objection for case CASE-2441 can be filed in time?",
  "options": [
   "Monday, 9 February 2026",
   "Friday, 20 March 2026",
   "Wednesday, 11 February 2026"
  ]
 },
 {
  "qid": "q5130a157fe",
  "kind": "yes/no",
  "text": "Dear front desk,\nPaolo Greco is sending file PO-3559 about the purchase request. The file is attached here for your records. I appreciate the help with it.\nKind regards,\n\nPurchase log PO-3559, kept by Paolo Greco, vendor Vantmoor Electric:\n- earlier purchase on Monday, 12 January 2026: $1,417.00\n- earlier purchase on Tuesday, 3 February 2026: $1,360.00\n- earlier purchase on Saturday, 21 February 2026: $1,430.00\n- new request on Friday, 13 March 2026: $2,211.00\nWindow checked: Tuesday, 13 January 2026 to Friday, 13 March 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is anything strictly greater than $5,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request made by Paolo Greco need written quotes under the purchase rule?"
 },
 {
  "qid": "q36490b3eb6",
  "kind": "choice",
  "text": "Nadia Kowal: hi there, here is LED-1667 about the teller ledger review.\nhelp desk: thanks a bunch, got it.\nhelp desk: take care.\n\nCash ledger LED-1667, teller Nadia Kowal:\n- 12 July 2027: withdrawal of $3,925.00\n- 12 July 2027: withdrawal of $1,076.00\n- 12 July 2027: deposit of $6,915.00\n- 13 July 2027: deposit of $3,897.00\nDay under review: 12 July 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is strictly more than $5,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals in ledger LED-1667 call for a cash report?",
  "options": [
   "Both totals",
   "Only the deposit total",
   "Neither total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q7abe91d2c3",
  "kind": "choice",
  "text": "Sent by: Freya Holm\nFile: POL-2993\nSent to: review team\nThis is a standard note about the loss claim. The file is laid out as usual.\n\nPolicy POL-2993, holder Freya Holm:\n- policy start date: 22 February 2026\n- burst pipe damage cover: added by a rider effective 1 July 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of 28 days whose clock starts running on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 28 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the earliest date on which the burst pipe damage loss for Freya Holm would be covered?",
  "options": [
   "1 August 2026",
   "30 July 2026",
   "31 July 2026"
  ]
 },
 {
  "qid": "q322ebb2d0a",
  "kind": "choice",
  "text": "Dear front desk,\nDana Okafor is writing to share file NTC-2057 about the reply deadline with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,\n\nNotice NTC-2057 to Dana Okafor:\n- notice date: 28 August 2028\n- sent by: post\n- 21 days after the notice date, before any postal add-on or closure: 18 September 2028\nOffice closures: 9 September 2028; 18 September 2028; 20 September 2028.",
  "question": "Response rule: a response is due 21 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 2 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, which date is the deadline for the response from Dana Okafor to the notice?",
  "options": [
   "19 September 2028",
   "21 September 2028"
  ]
 },
 {
  "qid": "q4d16be3b64",
  "kind": "yes/no",
  "text": "Ana Ruiz: Hello, I am sending file NTC-8765 about the notice response to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nNotice NTC-8765 to Ana Ruiz:\n- response due date: 5 December 2025\n- office cutoff on the due date: 5 December 2025, 13:20 (UTC+02:00)\n- response sent: 4 December 2025, 08:39 (UTC+03:00) [same instant in office time: 4 December 2025, 07:39 (UTC+02:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Ana Ruiz to notice NTC-8765 on time under the receipt rule?"
 },
 {
  "qid": "qee5f82c136",
  "kind": "choice",
  "text": "Ines Duarte: Hello. I am forwarding file CASE-9844 about the appeal deadline. My thanks for your help.\ncase team: Thank you, the file has been received.\n\nCase CASE-9844, party Ines Duarte:\n- decision date: 27 December 2025\n- delivery date: 30 December 2025",
  "question": "Filing rule: the appeal must be filed within 30 days measured from the later of the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the final day on which Ines Duarte can still file the appeal in time for case CASE-9844?",
  "options": [
   "29 January 2026",
   "28 January 2026",
   "26 January 2026",
   "27 January 2026"
  ]
 }
]
