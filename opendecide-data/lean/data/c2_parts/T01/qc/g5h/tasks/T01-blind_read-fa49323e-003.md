# G5-H blind read T01-blind_read-fa49323e-003 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g5h/answers/T01-blind_read-fa49323e-003.json

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
  "qid": "qf05c1fa1ff",
  "kind": "yes/no",
  "text": "Eva Marsh: With respect, sending file LED-8475 about the teller ledger review to the records clerk.\nclerk: Thank you, leave it with me, with warm gratitude.\n\nCash ledger LED-8475, teller Eva Marsh:\n- Wednesday, 6 September 2028: deposit of $4,162.00\n- Wednesday, 6 September 2028: deposit of $1,006.00\n- Wednesday, 6 September 2028: withdrawal of $1,865.00\n- Wednesday, 6 September 2028: withdrawal of $8,135.00\n- Friday, 8 September 2028: deposit of $3,400.00\nDay under review: Wednesday, 6 September 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is strictly more than $10,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that under the cash rule no cash report is needed for Wednesday, 6 September 2028?"
 },
 {
  "qid": "qd27fbe683e",
  "kind": "yes/no",
  "text": "Desk memo: Iris Vance is sending file CASE-3533 about the complaint filing to the desk for routine handling.\nIt is a standard hand-over that sits in the usual queue.\n\nCase CASE-3533, party Iris Vance:\n- incident date: Sunday, March 15, 2026\n- discovery date: Monday, March 16, 2026\n- complaint filed on: Tuesday, March 17, 2026\n- days from the incident date to the filing: 2 days\n- days from the discovery date to the filing: 1 day",
  "question": "Filing rule: the complaint must be filed inside 14 days beginning at the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 14 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid case CASE-3533 get the complaint filed on or before the final day of the filing period?"
 },
 {
  "qid": "q55c3aad42f",
  "kind": "yes/no",
  "text": "{\"file\": \"NTC-2083\", \"sent_by\": \"Dana Okafor\", \"subject\": \"the notice response\", \"team\": \"duty clerk\"}\n\nNotice NTC-2083 to Dana Okafor:\n- response due date: 29 September 2027\n- office cutoff on the due date: 29 September 2027, 22:06 (UTC+03:00)\n- response sent: 28 September 2027, 15:17 (UTC+00:00) [same instant in office time: 28 September 2027, 18:17 (UTC+03:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Dana Okafor to notice NTC-2083, under the receipt rule, counted as received on time?"
 },
 {
  "qid": "qe08c01f1b3",
  "kind": "yes/no",
  "text": "team: case team\nsent_by: Priya Raman\nfile: STAY-9369\nsubject: the residence day count\nnote: standard_handling_as_usual\n\nStay record STAY-9369 for Priya Raman:\n- entry day 14 Jun 2027, exit day 16 Jun 2027 (whole stay: 3 days)\n- entry day 1 Jul 2027, exit day 28 Jul 2027 (whole stay: 28 days)\n- entry day 20 Aug 2027, exit day 2 Sep 2027 (whole stay: 14 days)\nReference date: 22 Sep 2027\nWindow checked: 26 May 2027 to 22 Sep 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 60 days in each 120-day window that moves forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, do the days present for Priya Raman inside the checked window ending on the reference date exceed the stay limit?"
 },
 {
  "qid": "q46fe20729c",
  "kind": "yes/no",
  "text": "Desk memo: for the case team, kindly note that Malik Osei has sent in file STAY-6587 about the border stay check. With thanks in advance for your attention.\n\nStay record STAY-6587 for Malik Osei:\n- entry day 21 Jun 2025, exit day 16 Jul 2025 (whole stay: 26 days)\n- entry day 20 Aug 2025, exit day 28 Aug 2025 (whole stay: nine days)\nReference date: 23 Sep 2025\nWindow checked: 26 Jun 2025 to 23 Sep 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 30 days in any 90-day period that rolls forward day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is Malik Osei over the stay limit, with more days present in the checked window ending on the reference date?"
 },
 {
  "qid": "qefa7bd08de",
  "kind": "yes/no",
  "text": "{\"subject\": \"the response deadline\", \"sent_by\": \"Eva Marsh\", \"file\": \"NTC-2935\", \"channel\": \"intake\", \"team\": \"desk\"}\n\nNotice NTC-2935 to Eva Marsh:\n- response due date: 11 April 2027\n- office cutoff on the due date: 2027-04-11 12:38:00 -0400\n- response sent: 2027-04-11 16:39:00 +0000 [same instant in office time: 2027-04-11 12:39:00 -0400]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Eva Marsh on time under the receipt rule?"
 },
 {
  "qid": "q655ced1d17",
  "kind": "choice",
  "text": "desk: the buying request is on the table\nSara Ilves: here is file PO-8367 for you to read\nclerk: got it, thanks\n\nPurchase log PO-8367, kept by Sara Ilves, vendor Tessaro Foods:\n- earlier purchase on May 26, 2026: 158.00 USD\n- earlier purchase on May 29, 2026: 755.00 USD\n- earlier purchase on July 31, 2026: 429.00 USD\n- new request on September 12, 2026: 1,091.00 USD\nWindow checked: May 16, 2026 to September 12, 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 120-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is 3,000.00 USD bar, cleared only by more than that, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat total does the purchase rule compare with its threshold when the new request in log PO-8367 is counted in?",
  "options": [
   "2,433.00 USD",
   "1,520.00 USD"
  ]
 },
 {
  "qid": "q4e5f904519",
  "kind": "yes/no",
  "text": "Priya Raman sends file STAY-4453 about the residence day count to the desk. The file keeps to the standard format. A full copy sits with the desk too.\n\nStay record STAY-4453 for Priya Raman:\n- entry day Thursday, November 13, 2025, exit day Saturday, November 29, 2025 (whole stay: seventeen days)\n- entry day Thursday, December 11, 2025, exit day Tuesday, March 10, 2026 (whole stay: 90 days)\nReference date: Friday, May 8, 2026\nWindow checked: Friday, January 9, 2026 to Friday, May 8, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days in each 120-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Priya Raman over the stay limit, counting the days present inside the window that ends on Friday, May 8, 2026?"
 },
 {
  "qid": "q4e2d3bc8f1",
  "kind": "choice",
  "text": "Title: file POL-4339 about the loss claim\nRequester: Clara Weiss\nTeam: front desk\nSo glad to pass this along, big hugs!\n\nPolicy POL-4339, holder Clara Weiss:\n- policy start date: 29 Oct 2027\n- glass breakage cover: added by a rider effective 26 Dec 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 16 days commencing on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 16 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the earliest date on which this glass breakage loss for Clara Weiss would be covered?",
  "options": [
   "11 Jan 2028",
   "12 Jan 2028",
   "10 Jan 2028"
  ]
 },
 {
  "qid": "qf1b9116d39",
  "kind": "choice",
  "text": "Subject: intake\nDear intake team,\nFelix Ortega has sent in file LED-2762 about the branch cash review. Kindly log it when convenient.\nYours sincerely,\n\nCash ledger LED-2762, teller Felix Ortega:\n- 2026-02-13: withdrawal of $7,208.00\n- 2026-02-15: withdrawal of $3,839.00\n- 2026-02-15: withdrawal of $16,936.00\n- 2026-02-15: deposit of $21,469.00\n- 2026-02-17: deposit of $5,110.00\nDay under review: 2026-02-15",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is greater than $15,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals for 2026-02-15 in ledger LED-2762 call for a cash report?",
  "options": [
   "Only the deposit total",
   "Both totals",
   "Only the withdrawal total",
   "Neither total"
  ]
 },
 {
  "qid": "q2149198475",
  "kind": "yes/no",
  "text": "[intake] file=NTC-8034 sender=Kofi Mensah route=admin_team\n[intake] note=the reply timing question is on its way\n\nNotice NTC-8034 to Kofi Mensah:\n- response due date: 2027-03-27\n- office cutoff on the due date: 27 March 2027, 19:01 (UTC+09:00)\n- response sent: 27 March 2027, 05:03 (UTC-05:00) [same instant in office time: 27 March 2027, 19:03 (UTC+09:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the response to notice NTC-8034 on time under the receipt rule?"
 },
 {
  "qid": "qfcd6b500db",
  "kind": "yes/no",
  "text": "Desk memo: Kindly be informed that Maya Lindgren has forwarded file CASE-1581 concerning the claim deadline question to the records clerk.\nWe appreciate your attention.\n\nCase CASE-1581, party Maya Lindgren:\n- inspection date: 31 Jan 2027\n- report date: 1 Jan 2027\n- objection filed on: 4 Apr 2027\n- days from the inspection date to the filing: 63 days\n- days from the report date to the filing: 93 days",
  "question": "Filing rule: the objection must be filed within 90 days running from the later of the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the objection filed in time, on or before the final day of the filing period?"
 },
 {
  "qid": "q7dcfb6144f",
  "kind": "yes/no",
  "text": "Hana Sato: file PO-1265 about the purchase request is here\nclerk: got it, that is a normal intake\ndesk: good, sending it through to the records clerk\n\nPurchase log PO-1265, kept by Hana Sato, vendor Ostrava Parts:\n- earlier purchase on November 22, 2027: $1,774\n- earlier purchase on December 29, 2027: $11,760\n- new request on January 24, 2028: $3,239\nWindow checked: December 26, 2027 to January 24, 2028, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is equal to or more than $15,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, does the purchase rule require written quotes for the request from Hana Sato?"
 },
 {
  "qid": "q2c6e87bfb5",
  "kind": "choice",
  "text": "Subject: Quick send on the response deadline\n\nHi help desk,\n\nSending file NTC-1943 from Owen Pryce your way, quick handoff. Keep it moving.\n\nThanks,\n\nNotice NTC-1943 to Owen Pryce:\n- response due date: June 5, 2027\n- office cutoff on the due date: 5 June 2027, 12:26 (UTC-04:00)\n- response sent: 6 June 2027, 13:31 (UTC-03:00) [same instant in office time: 6 June 2027, 12:31 (UTC-04:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn which date, under the receipt rule, does the office count the response to notice NTC-1943 as received?",
  "options": [
   "2027-06-07",
   "2027-06-08"
  ]
 },
 {
  "qid": "q154a52d0b8",
  "kind": "yes/no",
  "text": "file: NTC-1189\nsent_by: Tomas Lindqvist\nsubject: the response deadline\nteam: help desk\nnote: a friendly hello from the sender\n\nNotice NTC-1189 to Tomas Lindqvist:\n- response due date: 10 July 2025\n- office cutoff on the due date: 10 July 2025, 19:03 (UTC-04:00)\n- response sent: 10 July 2025, 16:02 (UTC-07:00) [same instant in office time: 10 July 2025, 19:02 (UTC-04:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the reply from Tomas Lindqvist was not on time under the receipt rule?"
 },
 {
  "qid": "qe8a53f9889",
  "kind": "choice",
  "text": "Hana Sato sends file NTC-4740 about the response deadline to the desk. The file is set out in full with the usual headings. Thank you for your attention to this matter.\n\nNotice NTC-4740 to Hana Sato:\n- notice date: Monday, October 6, 2025\n- sent by: post\n- fourteen days after the notice date, before any postal add-on or closure: Monday, October 20, 2025\nOffice closures: Saturday, October 25, 2025; Sunday, October 26, 2025.",
  "question": "Response rule: a response is due fourteen days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add five days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, on what date is the response from Hana Sato due under the response rule?",
  "options": [
   "Monday, October 27, 2025",
   "Friday, October 24, 2025"
  ]
 },
 {
  "qid": "q56ff85b95c",
  "kind": "yes/no",
  "text": "sent_by: Jonas Feld\nfile: STAY-5408\nsubject: the visa stay count\nteam: intake team\n\nStay record STAY-5408 for Jonas Feld:\n- entry day Sunday, 5 December 2027, exit day Wednesday, 9 February 2028 (whole stay: 67 days)\nReference date: Saturday, 8 April 2028\nWindow checked: Saturday, 11 December 2027 to Saturday, 8 April 2028, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days within every moving 120-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Jonas Feld over the stay limit, with more days present inside the window that ends on the reference date in file STAY-5408, under the stay rule?"
 },
 {
  "qid": "qda71c09491",
  "kind": "yes/no",
  "text": "title | formal request\nrequester | Tomas Lindqvist\nfile | PO-9273\nWe kindly pass the purchase request along to the records clerk for your review.\n\nPurchase log PO-9273, kept by Tomas Lindqvist, vendor Brightwell Supply:\n- earlier purchase on March 11, 2027: $5,969\n- earlier purchase on April 12, 2027: $2,925\n- earlier purchase on April 13, 2027: $1,639\n- earlier purchase on May 3, 2027: $3,081\n- new request on May 17, 2027: $7,355\nWindow checked: March 19, 2027 to May 17, 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any amount that is more than $15,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, may Tomas Lindqvist proceed with request PO-9273 without written quotes?"
 },
 {
  "qid": "q3640eb49ec",
  "kind": "choice",
  "text": "Maya Lindgren: go go go, file POL-8804 is on the cover question.\nfront desk: Fast, on it.\n\nPolicy POL-8804, holder Maya Lindgren:\n- policy start date: April 13, 2026\n- power surge damage cover: added by a rider effective June 1, 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the earliest date on which the power surge damage loss would be covered?",
  "options": [
   "May 14, 2026",
   "June 30, 2026",
   "July 2, 2026",
   "July 1, 2026"
  ]
 },
 {
  "qid": "q8de08bf9ab",
  "kind": "yes/no",
  "text": "Malik Osei: Good to reach you, forwarding file LED-7001 about the branch cash review.\ndesk: Thank you, sending it through is appreciated.\n\nCash ledger LED-7001, teller Malik Osei:\n- 2026-08-13: deposit of 6,931.00 USD\n- 2026-08-13: withdrawal of 5,575.00 USD\n- 2026-08-13: deposit of 4,552.00 USD\n- 2026-08-15: withdrawal of 7,702.00 USD\nDay under review: 2026-08-13",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is a figure greater than 10,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is a cash report required for 2026-08-13?"
 },
 {
  "qid": "q9fda295d01",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nHana Sato is sending file NTC-2583 about the notice response, with the main points at the top. Quick note, I am buried under other work.\nBest,\n\nNotice NTC-2583 to Hana Sato:\n- response due date: 14 April 2026\n- office cutoff on the due date: 2026-04-14 18:25:00 +0300\n- response sent: 2026-04-14 16:30:00 +0100 [same instant in office time: 2026-04-14 18:30:00 +0300]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Hana Sato to notice NTC-2583 on time under the receipt rule?"
 },
 {
  "qid": "q10d964e8ef",
  "kind": "choice",
  "text": "Omar Saleh: Here is file NTC-2778 about the notice response for the intake team.\nagent: Understood, reviewing it.\n\nNotice NTC-2778 to Omar Saleh:\n- response due date: 28 Jul 2025\n- office cutoff on the due date: 28 July 2025, 17:34 (UTC+02:00)\n- response sent: 27 July 2025, 22:32 (UTC+03:00) [same instant in office time: 27 July 2025, 21:32 (UTC+02:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn which date does the office treat the response to notice NTC-2778 as received under the receipt rule?",
  "options": [
   "2025-07-29",
   "2025-07-28"
  ]
 },
 {
  "qid": "q462185e0d0",
  "kind": "yes/no",
  "text": "Desk memo: Iris Vance is sending file STAY-5749 about the visa stay count to the desk for routine handling.\nIt is a standard hand-over that sits in the usual queue.\n\nStay record STAY-5749 for Iris Vance:\n- entry day March 31, 2027, exit day May 30, 2027 (whole stay: 61 days)\nReference date: July 28, 2027\nWindow checked: March 31, 2027 to July 28, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days in any 120-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, do the days present for Iris Vance inside the checked window ending on the reference date exceed the stay limit?"
 },
 {
  "qid": "q0fb99c208e",
  "kind": "choice",
  "text": "Formal memo: Malik Osei has sent in file POL-9652 about the insurance claim for the case team. Kindly give this matter appropriate care.\n\nPolicy POL-9652, holder Malik Osei:\n- policy start date: Thursday, July 8, 2027\n- subsidence cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days whose clock starts running on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which, under the cover rule, the subsidence loss in policy POL-9652 would be covered?",
  "options": [
   "Friday, September 10, 2027",
   "Wednesday, August 25, 2027",
   "Monday, August 23, 2027"
  ]
 },
 {
  "qid": "q9b0726d2bc",
  "kind": "yes/no",
  "text": "Desk memo: Aiko Brandt sends file CASE-1133 about the complaint filing to the records clerk. The clerk gets a copy for the shelf in the usual way. Please keep this simple.\n\nCase CASE-1133, party Aiko Brandt:\n- incident date: 22 Feb 2027\n- discovery date: 8 Feb 2027\n- complaint filed on: 14 May 2027\n- days from the incident date to the filing: 81 days\n- days from the discovery date to the filing: 95 days",
  "question": "Filing rule: the complaint must be filed within 60 days from whichever is later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the complaint filed too late, after the final day of the filing period?"
 },
 {
  "qid": "q0aba28b423",
  "kind": "choice",
  "text": "Dana Okafor: pleased to put forward file POL-6942 about the loss claim, for the intake team\nagent: we appreciate it, kindly leave it with us\nclerk: duly logged, with respect\n\nPolicy POL-6942, holder Dana Okafor:\n- policy start date: Friday, July 24, 2026\n- subsidence cover: added by a rider effective Monday, August 17, 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of 65 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 65 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the earliest date on which the subsidence loss would be covered?",
  "options": [
   "Tuesday, November 17, 2026",
   "Friday, October 23, 2026",
   "Saturday, October 24, 2026",
   "Thursday, October 22, 2026"
  ]
 },
 {
  "qid": "q6649d22240",
  "kind": "yes/no",
  "text": "[review] file=CASE-2907 for the complaint filing, sender=Nadia Kowal\n[review] destination=review team, big_thanks\n\nCase CASE-2907, party Nadia Kowal:\n- incident date: Tuesday, June 15, 2027\n- discovery date: Wednesday, August 11, 2027\n- complaint filed on: Friday, September 17, 2027\n- days from the incident date to the filing: 94 days\n- days from the discovery date to the filing: 37 days",
  "question": "Filing rule: the complaint must be filed within 90 days counted forward from the later among these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the complaint from Nadia Kowal in case CASE-2907 filed in time, on or before the final day?"
 },
 {
  "qid": "qa77815289c",
  "kind": "yes/no",
  "text": "Malik Osei: forwarding file NTC-5443 about the reply timing question to the case team, with respect.\ncase team: thank you kindly for passing it along.\n\nNotice NTC-5443 to Malik Osei:\n- response due date: April 7, 2026\n- office cutoff on the due date: 7 April 2026, 17:43 (UTC+09:00)\n- response sent: 7 April 2026, 01:31 (UTC+00:00) [same instant in office time: 7 April 2026, 10:31 (UTC+09:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Malik Osei received on time under the receipt rule?"
 },
 {
  "qid": "qa0a38bc23a",
  "kind": "yes/no",
  "text": "title | kind request for the records clerk\nrequester | Eva Marsh\nfile | STAY-3750\nPlease find the residence day count attached for your review.\n\nStay record STAY-3750 for Eva Marsh:\n- entry day Tuesday, November 18, 2025, exit day Wednesday, December 3, 2025 (whole stay: 16 days)\n- entry day Tuesday, December 16, 2025, exit day Tuesday, January 13, 2026 (whole stay: 29 days)\n- entry day Wednesday, January 28, 2026, exit day Sunday, February 1, 2026 (whole stay: 5 days)\nReference date: Sunday, February 8, 2026\nWindow checked: Saturday, January 10, 2026 to Sunday, February 8, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 14 days in each 30-day window that moves forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 30-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 14 days, and within the limit if it is 14 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the person in file STAY-3750 over the stay limit, meaning more days present inside the checked window ending on the reference date than the limit?"
 },
 {
  "qid": "qdc5337a497",
  "kind": "yes/no",
  "text": "Desk memo: Please be advised that Hana Sato has sent file CASE-7889 concerning the complaint filing to the desk.\nKindly route it to the review team at your convenience. Thank you for your attention.\n\nCase CASE-7889, party Hana Sato:\n- incident date: 13 May 2026\n- discovery date: 6 May 2026\n- complaint filed on: 24 Jun 2026\n- days from the incident date to the filing: 42 days\n- days from the discovery date to the filing: 49 days",
  "question": "Filing rule: the complaint must be filed within 60 days measured from the later of the dates below: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the complaint in case CASE-7889 filed in time, on or before the final day?"
 },
 {
  "qid": "q45481f0983",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nAiko Brandt here with file POL-7590 about the insurance claim, and I am so glad it all came together. Hope it makes your work a little easier.\nCheers,\n\nPolicy POL-7590, holder Aiko Brandt:\n- policy start date: 21 June 2027\n- flood damage cover: part of the base policy\n- flood damage loss on: 2 July 2027\n- days from the policy start date to the loss: 11 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 10 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 10 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the flood damage loss on policy POL-7590 covered under the cover rule?"
 },
 {
  "qid": "qdd7c264e06",
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
  "qid": "qbd5f60ba2d",
  "kind": "choice",
  "text": "Hana Sato: hiya, big hello, here is file CASE-5598 about the appeal deadline for you.\nhelp desk: aww, thanks for the lovely heads-up.\n\nCase CASE-5598, party Hana Sato:\n- decision date: June 3, 2026\n- delivery date: June 4, 2026",
  "question": "Filing rule: the appeal must be filed within five days running from the later of the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is five days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, what is the latest date on which the appeal can be filed in time?",
  "options": [
   "June 9, 2026",
   "June 11, 2026",
   "June 7, 2026"
  ]
 },
 {
  "qid": "qcc44297480",
  "kind": "yes/no",
  "text": "Desk memo: Iris Vance is sending file CASE-3533 about the complaint filing to the desk for routine handling.\nIt is a standard hand-over that sits in the usual queue.\n\nCase CASE-3533, party Iris Vance:\n- incident date: Sunday, March 15, 2026\n- discovery date: Monday, March 16, 2026\n- complaint filed on: Tuesday, March 17, 2026\n- days from the incident date to the filing: 2 days\n- days from the discovery date to the filing: 1 day",
  "question": "Filing rule: the complaint must be filed inside 14 days beginning at the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 14 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the complaint filed by Iris Vance in case CASE-3533 too late, after the deadline?"
 },
 {
  "qid": "q08c979cfa9",
  "kind": "yes/no",
  "text": "Subject: file handover\nDear duty clerk,\nThe file CASE-6443 has come from Sara Ilves about the appeal deadline, for your desk.\nRegards,\n\nCase CASE-6443, party Sara Ilves:\n- billing date: 21 February 2026\n- statement date: 7 February 2026\n- dispute filed on: 22 April 2026\n- days from the billing date to the filing: 60 days\n- days from the statement date to the filing: 74 days",
  "question": "Filing rule: the dispute must be filed within 60 days after the later date out of these dates: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Sara Ilves file the dispute in case CASE-6443 in time under the filing rule?"
 },
 {
  "qid": "qb812c3e722",
  "kind": "choice",
  "text": "{\"file\": \"STAY-9496\", \"subject\": \"the residence day count\", \"sent_by\": \"Ana Ruiz\", \"team\": \"review team\", \"channel\": \"quick drop\"}\n\nStay record STAY-9496 for Ana Ruiz:\n- entry day 8 Oct 2027, exit day 20 Oct 2027 (whole stay: 13 days)\n- entry day 9 Nov 2027, exit day 21 Dec 2027 (whole stay: 43 days)\nReference date: 17 Mar 2028\nWindow checked: 19 Nov 2027 to 17 Mar 2028, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days within any 120-day window that keeps moving. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, how many present days in record STAY-9496 sit inside the window ending on 17 Mar 2028?",
  "options": [
   "33 days",
   "34 days"
  ]
 },
 {
  "qid": "q4d8ada340c",
  "kind": "choice",
  "text": "A warm hello from Dana Okafor to the front desk. File STAY-4305 is about the border stay check, coming along with a big grin. Hope things run smoothly on your side.\n\nStay record STAY-4305 for Dana Okafor:\n- entry day Friday, 1 May 2026, exit day Thursday, 21 May 2026 (whole stay: 21 days)\n- entry day Sunday, 14 June 2026, exit day Sunday, 14 June 2026 (whole stay: 1 day)\n- entry day Thursday, 25 June 2026, exit day Thursday, 2 July 2026 (whole stay: 8 days)\nReference date: Friday, 31 July 2026\nWindow checked: Sunday, 3 May 2026 to Friday, 31 July 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 45 days in any rolling 90-day window. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, how many days present for Dana Okafor fall inside the checked window ending on the reference date?",
  "options": [
   "30 days",
   "25 days",
   "28 days"
  ]
 },
 {
  "qid": "q60a40c0581",
  "kind": "yes/no",
  "text": "Kofi Mensah: Quick word, sending file STAY-2275 about the visa stay count to the review team.\nclerk: Got it, on it.\n\nStay record STAY-2275 for Kofi Mensah:\n- entry day Friday, August 27, 2027, exit day Tuesday, September 21, 2027 (whole stay: 26 days)\n- entry day Tuesday, October 19, 2027, exit day Thursday, October 28, 2027 (whole stay: 10 days)\nReference date: Monday, November 29, 2027\nWindow checked: Wednesday, September 1, 2027 to Monday, November 29, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 30 days in each 90-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, is the person in file STAY-2275 over the stay limit, with more days present in the window ending on Monday, November 29, 2027?"
 },
 {
  "qid": "q0d5b0e795f",
  "kind": "yes/no",
  "text": "{\"file\": \"PO-5112\", \"sent_by\": \"Omar Saleh\", \"subject\": \"the buying request\", \"channel\": \"quick intake\", \"team\": \"service desk\"}\n\nPurchase log PO-5112, kept by Omar Saleh, vendor Halden Tools:\n- earlier purchase on 2025-08-29: $11,689\n- earlier purchase on 2025-09-18: $13,419\n- new request on 2025-10-02: $8,539\nWindow checked: 2025-09-03 to 2025-10-02, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any sum more than $25,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request from Omar Saleh in log PO-5112 need written quotes under the purchase rule?"
 },
 {
  "qid": "q49a1a062eb",
  "kind": "choice",
  "text": "sent_by: Omar Saleh\nfile: STAY-9142\nsubject: the residence day count\nteam: admin\nnote: fast drop\n\nStay record STAY-9142 for Omar Saleh:\n- entry day 7 January 2027, exit day 9 January 2027 (whole stay: 3 days)\n- entry day 24 January 2027, exit day 10 February 2027 (whole stay: 18 days)\n- entry day 16 March 2027, exit day 25 March 2027 (whole stay: 10 days)\nReference date: 24 April 2027\nWindow checked: 25 January 2027 to 24 April 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 45 days in any 90-day period that rolls forward day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, how many days present for Omar Saleh fall inside the checked window that ends on the reference date?",
  "options": [
   "26 days",
   "25 days",
   "27 days"
  ]
 },
 {
  "qid": "qf4b6d3dffc",
  "kind": "yes/no",
  "text": "Subject: a little hello for the front desk\nHi front desk,\nHope you are doing well! Yara Haddad is sending file POL-3373 about the loss claim along, so it is ready at a convenient moment.\nWarm wishes,\n\nPolicy POL-3373, holder Yara Haddad:\n- policy start date: Wednesday, July 1, 2026\n- glass breakage cover: part of the base policy\n- glass breakage loss on: Tuesday, July 28, 2026\n- days from the policy start date to the loss: 27 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 26 days whose first counted day falls on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 26 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is the glass breakage loss covered under the cover rule?"
 },
 {
  "qid": "qeb6e2703cc",
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
  "qid": "q1e4bf221c2",
  "kind": "yes/no",
  "text": "{\"author\": \"Kofi Mensah\", \"doc\": \"POL-9658\", \"subject\": \"the insurance claim\", \"team\": \"duty clerk\"}\n\nPolicy POL-9658, holder Kofi Mensah:\n- policy start date: Tuesday, 25 August 2026\n- flood damage cover: part of the base policy\n- flood damage loss on: Monday, 9 November 2026\n- days from the policy start date to the loss: 76 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 90 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 90 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does the cover rule count the flood damage loss for Kofi Mensah as covered?"
 },
 {
  "qid": "q3bd8c98506",
  "kind": "choice",
  "text": "Nadia Kowal: Kindly passing along file NTC-8992 about the reply deadline to the desk.\ndesk: Thanks very kindly for this.\n\nNotice NTC-8992 to Nadia Kowal:\n- notice date: September 22, 2027\n- sent by: email\n- 20 days after the notice date, before any postal add-on or closure: October 12, 2027\nOffice closures: October 12, 2027; October 13, 2027.",
  "question": "Response rule: a response is due 20 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 5 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, on what date is the response from Nadia Kowal due under the response rule?",
  "options": [
   "October 10, 2027",
   "October 11, 2027",
   "October 14, 2027"
  ]
 },
 {
  "qid": "q3723d22a29",
  "kind": "yes/no",
  "text": "[service] file=POL-8088 about the insurance claim came_from=Ravi Anand\n[service] addressed_to=service desk, cheerful_thanks\n\nPolicy POL-8088, holder Ravi Anand:\n- policy start date: Friday, 11 September 2026\n- fire damage cover: part of the base policy\n- fire damage loss on: Sunday, 20 September 2026\n- days from the policy start date to the loss: nine days",
  "question": "Cover rule: a loss is covered only after a waiting period of ten days whose clock starts running on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is ten days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does the cover rule count the loss on policy POL-8088 as covered?"
 },
 {
  "qid": "q188f32d290",
  "kind": "choice",
  "text": "{\"sent_by\": \"Clara Weiss\", \"file\": \"CASE-9711\", \"subject\": \"the claim deadline question\", \"team\": \"help desk\", \"channel\": \"chat\"}\n\nCase CASE-9711, party Clara Weiss:\n- inspection date: 2027-11-18\n- report date: 2027-11-23",
  "question": "Filing rule: the objection must be filed within 65 days after the later date out of these dates: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 65 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, by which final day must the objection be filed to still count as in time?",
  "options": [
   "2028-01-27",
   "2028-01-28",
   "2028-01-26"
  ]
 },
 {
  "qid": "q22ba2803cb",
  "kind": "yes/no",
  "text": "Lucas Brenner: file NTC-1790 about the notice response goes to the desk as usual\ndesk: understood, standard path applied\n\nNotice NTC-1790 to Lucas Brenner:\n- response due date: 4 July 2026\n- office cutoff on the due date: 4 July 2026, 20:54 (UTC+03:00)\n- response sent: 6 July 2026, 06:06 (UTC+08:00) [same instant in office time: 6 July 2026, 01:06 (UTC+03:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the response from Lucas Brenner to notice NTC-1790 under the receipt rule was not on time?"
 },
 {
  "qid": "q258dbc69cc",
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
  "qid": "q472800a6b4",
  "kind": "choice",
  "text": "file: NTC-7721\nsent_by: Lucas Brenner\nsubject: the reply deadline\nteam: case team\nnote: with respectful thanks\n\nNotice NTC-7721 to Lucas Brenner:\n- notice date: 31 May 2027\n- sent by: email\n- 20 days after the notice date, before any postal add-on or closure: 20 Jun 2027\nOffice closures: 20 Jun 2027.",
  "question": "Response rule: a response is due 20 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 5 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the due date for the response from Lucas Brenner to the notice under the response rule?",
  "options": [
   "18 Jun 2027",
   "21 Jun 2027",
   "19 Jun 2027"
  ]
 },
 {
  "qid": "q1a97621daa",
  "kind": "yes/no",
  "text": "{\"file\": \"CASE-1178\", \"sent_by\": \"Paolo Greco\", \"subject\": \"the appeal deadline\", \"channel\": \"case team\"}\n\nCase CASE-1178, party Paolo Greco:\n- decision date: 7 Feb 2027\n- delivery date: 24 Mar 2027\n- appeal filed on: 24 Apr 2027\n- days from the decision date to the filing: 76 days\n- days from the delivery date to the filing: 31 days",
  "question": "Filing rule: the appeal must be filed within 30 days following the later of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the appeal from Paolo Greco in case CASE-1178 filed on or before the final day of the filing period?"
 }
]
