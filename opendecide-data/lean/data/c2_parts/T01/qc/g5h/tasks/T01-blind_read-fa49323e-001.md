# G5-H blind read T01-blind_read-fa49323e-001 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g5h/answers/T01-blind_read-fa49323e-001.json

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
  "qid": "q351927cdd7",
  "kind": "yes/no",
  "text": "clerk: oh hey, what came in\nRavi Anand: got file STAY-8687 about the visa stay count here, nice and easy\ndesk: lovely, thanks, we are on it\n\nStay record STAY-8687 for Ravi Anand:\n- entry day Monday, June 7, 2027, exit day Monday, June 7, 2027 (whole stay: one day)\n- entry day Friday, July 16, 2027, exit day Saturday, September 11, 2027 (whole stay: 58 days)\n- entry day Sunday, October 3, 2027, exit day Tuesday, October 5, 2027 (whole stay: three days)\nReference date: Wednesday, October 27, 2027\nWindow checked: Wednesday, June 30, 2027 to Wednesday, October 27, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 60 days inside every moving 120-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, do the days present for Ravi Anand inside the checked window ending on the reference date exceed the stay limit?"
 },
 {
  "qid": "q4409d2e3b5",
  "kind": "yes/no",
  "text": "Memo for the front desk: Kofi Mensah sends file CASE-6324 about the appeal deadline. Grab it at your convenience, the queue is busy on this end.\n\nCase CASE-6324, party Kofi Mensah:\n- decision date: July 28, 2027\n- delivery date: August 18, 2027\n- appeal filed on: October 3, 2027\n- days from the decision date to the filing: 67 days\n- days from the delivery date to the filing: 46 days",
  "question": "Filing rule: the appeal must be filed within 46 days from whichever is later of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 46 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the appeal filed in time, on or before the final day of the filing period?"
 },
 {
  "qid": "qc1ce286184",
  "kind": "yes/no",
  "text": "Memo for the front desk: Jonas Feld sends file CASE-4173 about the appeal deadline. Grab it at your convenience, the queue is busy on this end.\n\nCase CASE-4173, party Jonas Feld:\n- decision date: 2025-10-11\n- delivery date: 2025-11-01\n- appeal filed on: 2026-01-30\n- days from the decision date to the filing: 111 days\n- days from the delivery date to the filing: 90 days",
  "question": "Filing rule: the appeal must be filed inside 90 days extending past the later of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is it true that the appeal in case CASE-4173 was not filed in time?"
 },
 {
  "qid": "q9bb04f8b2d",
  "kind": "choice",
  "text": "[intake] Aiko Brandt sends file POL-7331 about the loss claim to intake_team\n[tag] standard_handling\n\nPolicy POL-7331, holder Aiko Brandt:\n- policy start date: 21 September 2027\n- subsidence cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 18 days commencing on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 18 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich is the earliest date that this subsidence loss under policy POL-7331 would be covered?",
  "options": [
   "10 October 2027",
   "9 October 2027",
   "8 October 2027"
  ]
 },
 {
  "qid": "q6b8fba71a0",
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
  "qid": "q144b348eff",
  "kind": "choice",
  "text": "Subject: file handover\nDear duty clerk,\nThe file PO-4450 has come from Nadia Kowal about the purchase request, for your desk.\nRegards,\n\nPurchase log PO-4450, kept by Nadia Kowal, vendor Mirefield Print:\n- earlier purchase on 14 Dec 2025: $1,310.00\n- earlier purchase on 31 Dec 2025: $656.00\n- earlier purchase on 14 Jan 2026: $502.00\n- new request on 4 Feb 2026: $2,780.00\nWindow checked: 7 Dec 2025 to 4 Feb 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any figure at or above $5,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat total does the purchase rule compare with its threshold when the new request in log PO-4450 is counted in?",
  "options": [
   "$8,028.00",
   "$5,248.00"
  ]
 },
 {
  "qid": "q79342ebee4",
  "kind": "yes/no",
  "text": "clerk: routine drop coming in\nYara Haddad: file POL-1046 about the insurance claim is on its way\ndesk: understood, passing it to the intake team\n\nPolicy POL-1046, holder Yara Haddad:\n- policy start date: 2 February 2026\n- power surge damage cover: added by a rider effective 30 June 2026\n- power surge damage loss on: 19 July 2026\n- days from the policy start date to the loss: 167 days\n- days from the rider effective date to the loss: 19 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 60 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 60 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the cover rule does not pay for the power surge damage loss on policy POL-1046?"
 },
 {
  "qid": "qa46184f9ce",
  "kind": "choice",
  "text": "Desk memo: Malik Osei is sending file NTC-5661 about the response deadline to the admin team. Pick it up fast, the work is waiting.\n\nNotice NTC-5661 to Malik Osei:\n- notice date: Wednesday, 10 May 2028\n- sent by: hand delivery\n- 20 days after the notice date, before any postal add-on or closure: Tuesday, 30 May 2028\nOffice closures: Tuesday, 30 May 2028; Sunday, 4 June 2028.",
  "question": "Response rule: a response is due 20 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 5 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, on which date is the response to notice NTC-5661 due under the response rule?",
  "options": [
   "Sunday, 28 May 2028",
   "Wednesday, 31 May 2028",
   "Monday, 29 May 2028"
  ]
 },
 {
  "qid": "qdd107d4ea9",
  "kind": "choice",
  "text": "file: CASE-7220\nsent_by: Eva Marsh\nsubject: the claim deadline question\nnote: kindly routed for the intake team\n\nCase CASE-7220, party Eva Marsh:\n- inspection date: 2028-06-12\n- report date: 2028-04-28",
  "question": "Filing rule: the objection must be filed inside a span of 45 days that runs after the later of these dates: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the latest date by which the objection can be filed in time?",
  "options": [
   "2028-07-27",
   "2028-07-25",
   "2028-07-29"
  ]
 },
 {
  "qid": "qc03a38b2b5",
  "kind": "choice",
  "text": "Malik Osei: Sending file NTC-6070 about the notice response across in a hurry.\nadmin: On it, passing it along.\n\nNotice NTC-6070 to Malik Osei:\n- notice date: 27 September 2025\n- sent by: post\n- 14 days after the notice date, before any postal add-on or closure: 11 October 2025\nOffice closures: 11 October 2025; 12 October 2025; 15 October 2025.",
  "question": "Response rule: a response is due 14 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 5 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, on which date is the response to notice NTC-6070 due under the response rule?",
  "options": [
   "16 October 2025",
   "13 October 2025",
   "14 October 2025"
  ]
 },
 {
  "qid": "q44cd71a72b",
  "kind": "yes/no",
  "text": "Maya Lindgren: Kindly see file CASE-7719 about the claim deadline question below, thank you.\nclerk: Thank you, that is noted and it goes to the case team.\n\nCase CASE-7719, party Maya Lindgren:\n- invoice date: 5 Aug 2027\n- goods received date: 19 Aug 2027\n- claim filed on: 23 Aug 2027\n- days from the invoice date to the filing: eighteen days\n- days from the goods received date to the filing: four days",
  "question": "Filing rule: the claim must be filed within ten days running from the later of the dates below: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is ten days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the claim submitted too late, after the deadline?"
 },
 {
  "qid": "q8f0749f209",
  "kind": "choice",
  "text": "Aiko Brandt: Hello, I am sending file NTC-4941 about the notice response to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nNotice NTC-4941 to Aiko Brandt:\n- response due date: 26 October 2025\n- office cutoff on the due date: 2025-10-26T22:52:00+02:00\n- response sent: 2025-10-25T04:53:00+08:00 [same instant in office time: 2025-10-24T22:53:00+02:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn which date, under the receipt rule, does the office count the response from Aiko Brandt to notice NTC-4941 as received?",
  "options": [
   "October 25, 2025",
   "October 26, 2025"
  ]
 },
 {
  "qid": "q3bd049d56a",
  "kind": "yes/no",
  "text": "Tomas Lindqvist: Quick word, here is file POL-2024 about the insurance claim, I am swamped.\nservice: Thanks, I see it.\ndesk: Great, shared with the team.\n\nPolicy POL-2024, holder Tomas Lindqvist:\n- policy start date: Monday, 5 July 2027\n- glass breakage cover: part of the base policy\n- glass breakage loss on: Saturday, 7 August 2027\n- days from the policy start date to the loss: 33 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days whose clock starts running on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the cover rule does not pay for the glass breakage loss on policy POL-2024?"
 },
 {
  "qid": "q90ec743383",
  "kind": "yes/no",
  "text": "{\"file\": \"CASE-1178\", \"sent_by\": \"Paolo Greco\", \"subject\": \"the appeal deadline\", \"channel\": \"case team\"}\n\nCase CASE-1178, party Paolo Greco:\n- decision date: 7 Feb 2027\n- delivery date: 24 Mar 2027\n- appeal filed on: 24 Apr 2027\n- days from the decision date to the filing: 76 days\n- days from the delivery date to the filing: 31 days",
  "question": "Filing rule: the appeal must be filed within 30 days following the later of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Paolo Greco fail to file the appeal in case CASE-1178 by the deadline?"
 },
 {
  "qid": "q54cf1be503",
  "kind": "yes/no",
  "text": "{\"sender\": \"Ana Ruiz\", \"file\": \"CASE-3732\", \"subject\": \"the claim deadline question\", \"queue\": \"review team\", \"channel\": \"quick_handoff\"}\n\nCase CASE-3732, party Ana Ruiz:\n- invoice date: Sunday, July 6, 2025\n- goods received date: Saturday, July 19, 2025\n- claim filed on: Wednesday, July 30, 2025\n- days from the invoice date to the filing: 24 days\n- days from the goods received date to the filing: eleven days",
  "question": "Filing rule: the claim must be filed within ten days starting from the later of the dates listed below: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is ten days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, was the claim filed in time, on or before the final day of the filing period?"
 },
 {
  "qid": "qab635a92e9",
  "kind": "yes/no",
  "text": "file: NTC-6546\nsent_by: Theo Kalnins\nsubject: the reply timing question\nteam: case team\nnote: with respectful thanks\n\nNotice NTC-6546 to Theo Kalnins:\n- response due date: Sunday, October 31, 2027\n- office cutoff on the due date: 2027-10-31 13:35:00 +0900\n- response sent: 2027-11-01 07:48:00 +0200 [same instant in office time: 2027-11-01 14:48:00 +0900]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Theo Kalnins on time under the receipt rule?"
 },
 {
  "qid": "q4f246af40d",
  "kind": "yes/no",
  "text": "Internal memo: This note is about the claim deadline question. Lena Whitcombe submits file CASE-1048 to the front desk. Thanks for reading along, and cheers.\n\nCase CASE-1048, party Lena Whitcombe:\n- invoice date: May 14, 2026\n- goods received date: May 7, 2026\n- claim filed on: June 13, 2026\n- days from the invoice date to the filing: 30 days\n- days from the goods received date to the filing: 37 days",
  "question": "Filing rule: the claim must be filed within 30 days from whichever is later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the claim filed on or before the final day of the filing period?"
 },
 {
  "qid": "q7f3e54d7ec",
  "kind": "yes/no",
  "text": "Felix Ortega: file POL-9693 about the insurance claim is here.\nintake team: received, thanks.\nintake team: that is everything for this file.\n\nPolicy POL-9693, holder Felix Ortega:\n- policy start date: 2026-10-11\n- glass breakage cover: part of the base policy\n- glass breakage loss on: 2026-10-14\n- days from the policy start date to the loss: 3 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the cover rule does not pay for the glass breakage loss on policy POL-9693?"
 },
 {
  "qid": "q1472334e42",
  "kind": "yes/no",
  "text": "{\"team\": \"front desk\", \"subject\": \"the purchase request\", \"file\": \"PO-7344\", \"sent_by\": \"Jonas Feld\", \"note\": \"rapid hand off\"}\n\nPurchase log PO-7344, kept by Jonas Feld, vendor Tessaro Foods:\n- earlier purchase on Thursday, March 5, 2026: $4,491.00\n- earlier purchase on Friday, March 6, 2026: $1,474.00\n- earlier purchase on Saturday, April 4, 2026: $2,691.00\n- earlier purchase on Wednesday, May 6, 2026: $7,964.00\n- new request on Wednesday, June 3, 2026: $6,560.00\nWindow checked: Friday, March 6, 2026 to Wednesday, June 3, 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is greater than the sum of $25,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request from Jonas Feld need written quotes under the purchase rule?"
 },
 {
  "qid": "q19f53d57fe",
  "kind": "yes/no",
  "text": "Subject: forwarded papers\nDear case team,\nKindly find file STAY-6036 about the visa stay count sent in by Ana Ruiz, and thank you for your attention to it.\nYours faithfully\n\nStay record STAY-6036 for Ana Ruiz:\n- entry day 24 May 2026, exit day 25 May 2026 (whole stay: 2 days)\n- entry day 16 Jun 2026, exit day 5 Aug 2026 (whole stay: 51 days)\n- entry day 25 Aug 2026, exit day 2 Sep 2026 (whole stay: 9 days)\nReference date: 22 Sep 2026\nWindow checked: 26 May 2026 to 22 Sep 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days in each 120-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Ana Ruiz, under the stay rule, over the stay limit for the window ending on 22 Sep 2026?"
 },
 {
  "qid": "q94cf8d445b",
  "kind": "choice",
  "text": "file: LED-2010\nsent_by: Nadia Kowal\nsubject: the branch cash review\nteam: service desk\nnote: a friendly hello\n\nCash ledger LED-2010, teller Nadia Kowal:\n- Thursday, 13 July 2028: deposit of $20,267\n- Thursday, 13 July 2028: deposit of $2,140\n- Saturday, 15 July 2028: deposit of $10,657\nDay under review: Thursday, 13 July 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is equal to $15,000 or more, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, which of the day's totals in ledger LED-2010, if any, call for a cash report under the cash rule?",
  "options": [
   "Only the deposit total",
   "Both totals",
   "Only the withdrawal total",
   "Neither total"
  ]
 },
 {
  "qid": "q7b31bcdbc9",
  "kind": "choice",
  "text": "subject | the reply deadline\nfile | NTC-2462\nsent_by | Owen Pryce\nGrab it quick, the queue is busy.\n\nNotice NTC-2462 to Owen Pryce:\n- notice date: 2025-06-24\n- sent by: post\n- 30 days after the notice date, before any postal add-on or closure: 2025-07-24\nOffice closures: 2025-06-26; 2025-07-24; 2025-07-27.",
  "question": "Response rule: a response is due 30 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add two days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, which date is the deadline for the response from Owen Pryce to the notice?",
  "options": [
   "2025-07-25",
   "2025-07-26"
  ]
 },
 {
  "qid": "qf52036cd98",
  "kind": "yes/no",
  "text": "Ana Ruiz: Quick send, NTC-9361 about the response deadline.\nhelp desk: Got it.\n\nNotice NTC-9361 to Ana Ruiz:\n- response due date: 2027-06-20\n- office cutoff on the due date: 20 June 2027, 14:36 (UTC+01:00)\n- response sent: 2027-06-20T13:36:00Z [same instant in office time: 20 June 2027, 14:36 (UTC+01:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that the response from Ana Ruiz to notice NTC-9361 under the receipt rule was not on time?"
 },
 {
  "qid": "q5f107e139a",
  "kind": "yes/no",
  "text": "[service_desk] sender=Ravi Anand file=PO-1145\n[queue] subject=the purchase request hand_off_ready\n\nPurchase log PO-1145, kept by Ravi Anand, vendor Mirefield Print:\n- earlier purchase on 10 Apr 2026: $1,549.00\n- new request on 25 Apr 2026: $2,133.00\nWindow checked: 25 Feb 2026 to 25 Apr 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is $5,000.00 or greater, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request from Ravi Anand need written quotes under the purchase rule?"
 },
 {
  "qid": "q4e9e34207d",
  "kind": "yes/no",
  "text": "title | rush handoff\nrequester | Iris Vance\nfile | CASE-1317\nDropping the claim deadline question with the admin team, board is full.\n\nCase CASE-1317, party Iris Vance:\n- inspection date: 11 Sep 2026\n- report date: 11 Oct 2026\n- objection filed on: 21 Oct 2026\n- days from the inspection date to the filing: 40 days\n- days from the report date to the filing: 10 days",
  "question": "Filing rule: the objection must be filed within 9 days measured from the later of the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 9 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the objection from Iris Vance in case CASE-1317 filed on or before the final day of the filing period?"
 },
 {
  "qid": "q3c2745e1b0",
  "kind": "yes/no",
  "text": "Hana Sato: Hiya! Sending CASE-6275 about the claim deadline question, all good here.\nservice desk: Lovely, thanks for the heads up!\n\nCase CASE-6275, party Hana Sato:\n- inspection date: Thursday, October 8, 2026\n- report date: Thursday, September 24, 2026\n- objection filed on: Thursday, October 29, 2026\n- days from the inspection date to the filing: 21 days\n- days from the report date to the filing: 35 days",
  "question": "Filing rule: the objection must be filed within 28 days past the later of the dates below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the objection in case CASE-6275 filed late, after the deadline?"
 },
 {
  "qid": "q8d1372bff8",
  "kind": "choice",
  "text": "{\"file\": \"POL-8062\", \"sent_by\": \"Bruno Lacerda\", \"subject\": \"the cover question\", \"team\": \"service desk\", \"channel\": \"friendly_chat\"}\n\nPolicy POL-8062, holder Bruno Lacerda:\n- policy start date: 2026-02-22\n- power surge damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which, under the cover rule, the power surge damage loss in policy POL-8062 would be covered?",
  "options": [
   "2026-03-14",
   "2026-03-18",
   "2026-03-16"
  ]
 },
 {
  "qid": "q938a103c8d",
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
  "qid": "qa730f62f9e",
  "kind": "yes/no",
  "text": "file_ref=POL-2136 topic=the insurance claim\n[mailroom] from=Clara Weiss to=desk\n\nPolicy POL-2136, holder Clara Weiss:\n- policy start date: 6 September 2027\n- fire damage cover: part of the base policy\n- fire damage loss on: 7 September 2027\n- days from the policy start date to the loss: 1 day",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days that opens on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is it true that the fire damage loss is not covered?"
 },
 {
  "qid": "qcf91b49653",
  "kind": "choice",
  "text": "Owen Pryce: file POL-4710 about the loss claim is ready, pushing to the admin team\nclerk: on it, thanks\n\nPolicy POL-4710, holder Owen Pryce:\n- policy start date: Monday, September 28, 2026\n- theft cover: added by a rider effective Tuesday, February 9, 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 15 days whose opening count lands on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 15 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn what earliest date would a loss of this kind be covered under policy POL-4710?",
  "options": [
   "Wednesday, October 14, 2026",
   "Friday, February 26, 2027",
   "Wednesday, February 24, 2027",
   "Thursday, February 25, 2027"
  ]
 },
 {
  "qid": "q92149d8cd1",
  "kind": "yes/no",
  "text": "team: records clerk\nfile: CASE-1218\nsent_by: Owen Pryce\nsubject: the claim deadline question\nnote: with thanks\n\nCase CASE-1218, party Owen Pryce:\n- invoice date: Wednesday, 25 August 2027\n- goods received date: Wednesday, 11 August 2027\n- claim filed on: Saturday, 9 October 2027\n- days from the invoice date to the filing: 45 days\n- days from the goods received date to the filing: 59 days",
  "question": "Filing rule: the claim must be filed inside 44 days counted from the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 44 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the claim lodged by the final day of the filing period?"
 },
 {
  "qid": "qdfb56e2ceb",
  "kind": "yes/no",
  "text": "file: POL-2305\nsent_by: Omar Saleh\nsubject: the insurance claim\nteam: service desk\nnote: busy_queue\n\nPolicy POL-2305, holder Omar Saleh:\n- policy start date: 22 Jun 2026\n- storm damage cover: added by a rider effective 18 Oct 2026\n- storm damage loss on: 29 Oct 2026\n- days from the policy start date to the loss: 129 days\n- days from the rider effective date to the loss: 11 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 10 days whose opening count lands on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 10 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the loss on policy POL-2305 covered under the cover rule?"
 },
 {
  "qid": "q45f07cead3",
  "kind": "yes/no",
  "text": "origin: Eva Marsh\nitem: CASE-2218\ntopic: the claim deadline question\nteam: help desk\nchannel: intake\n\nCase CASE-2218, party Eva Marsh:\n- invoice date: 2027-05-19\n- goods received date: 2027-02-13\n- claim filed on: 2027-08-18\n- days from the invoice date to the filing: 91 days\n- days from the goods received date to the filing: 186 days",
  "question": "Filing rule: the claim must be filed within 90 days reckoned after the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid case CASE-2218 get the claim filed on or before the final day of the filing period?"
 },
 {
  "qid": "q3fd96e5a24",
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
  "qid": "qc968931d6c",
  "kind": "choice",
  "text": "{\"sent_by\": \"Lucas Brenner\", \"file\": \"CASE-7035\", \"subject\": \"the complaint filing\", \"team\": \"front desk\", \"channel\": \"chat\"}\n\nCase CASE-7035, party Lucas Brenner:\n- incident date: 8 January 2026\n- discovery date: 18 January 2026",
  "question": "Filing rule: the complaint must be filed within 60 days reckoned after the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the latest date by which the complaint can be filed in time?",
  "options": [
   "9 March 2026",
   "18 March 2026",
   "10 April 2026",
   "19 March 2026"
  ]
 },
 {
  "qid": "qe30540aeb8",
  "kind": "yes/no",
  "text": "sent_by: Aiko Brandt\nfile: PO-6300\nsubject: the purchase request\nteam: help desk\nnote: big thanks in advance\n\nPurchase log PO-6300, kept by Aiko Brandt, vendor Corvane Office:\n- earlier purchase on 2026-08-06: $1,686.00\n- earlier purchase on 2026-10-01: $577.00\n- earlier purchase on 2026-10-20: $638.00\n- new request on 2026-11-12: $965.00\nWindow checked: 2026-09-14 to 2026-11-12, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is greater than the sum of $3,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, must the purchase request in log PO-6300 for Aiko Brandt come with written quotes?"
 },
 {
  "qid": "q4cc3b06a3f",
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
  "qid": "q490fdcefb9",
  "kind": "choice",
  "text": "Desk memo: Malik Osei is sharing file STAY-7116 about the residence day count with the review team. Hey, happy to pass it along. Thanks a lot for the eye on it.\n\nStay record STAY-7116 for Malik Osei:\n- entry day Saturday, 28 March 2026, exit day Friday, 12 June 2026 (whole stay: 77 days)\nReference date: Sunday, 19 July 2026\nWindow checked: Tuesday, 21 April 2026 to Sunday, 19 July 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 45 days in any 90-day period that rolls forward day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, how many present days in record STAY-7116 sit inside the window ending on Sunday, 19 July 2026?",
  "options": [
   "52 days",
   "53 days"
  ]
 },
 {
  "qid": "qdfa5ebf057",
  "kind": "choice",
  "text": "title | kind request for the records clerk\nrequester | Bruno Lacerda\nfile | CASE-6184\nPlease find the claim deadline question attached for your review.\n\nCase CASE-6184, party Bruno Lacerda:\n- invoice date: 2028-05-21\n- goods received date: 2028-05-18",
  "question": "Filing rule: the claim must be filed inside a span of 31 days that runs after the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 31 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the latest date by which the claim can be filed in time?",
  "options": [
   "2028-06-23",
   "2028-06-22",
   "2028-06-21"
  ]
 },
 {
  "qid": "qef0096c268",
  "kind": "choice",
  "text": "{\"sent_by\": \"Ravi Anand\", \"file\": \"LED-1760\", \"subject\": \"the teller ledger review\", \"team\": \"records clerk\", \"note\": \"with courtesy\"}\n\nCash ledger LED-1760, teller Ravi Anand:\n- 25 May 2026: deposit of $1,712.00\n- 27 May 2026: withdrawal of $429.00\n- 27 May 2026: withdrawal of $445.00\n- 28 May 2026: withdrawal of $655.00\nDay under review: 27 May 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is anything strictly greater than $3,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals in ledger LED-1760 call for a cash report?",
  "options": [
   "Neither total",
   "Both totals",
   "Only the withdrawal total",
   "Only the deposit total"
  ]
 },
 {
  "qid": "q63ce16d068",
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
  "qid": "qbe5c4c158a",
  "kind": "yes/no",
  "text": "[intake] file=POL-5956 sender=Aiko Brandt regarding the insurance claim\n[note] kindly_forwarded_to=duty_clerk\n\nPolicy POL-5956, holder Aiko Brandt:\n- policy start date: June 9, 2026\n- burst pipe damage cover: added by a rider effective December 18, 2026\n- burst pipe damage loss on: March 18, 2027\n- days from the policy start date to the loss: 282 days\n- days from the rider effective date to the loss: 90 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 90 days that picks up on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 90 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid the loss happen during the waiting period of policy POL-5956, on or before its final day?"
 },
 {
  "qid": "qa070c4aac4",
  "kind": "choice",
  "text": "clerk: heads up, a new item is landing\nMaya Lindgren: file CASE-4324 about the complaint filing is going to the help desk\ndesk: understood, routing it straight away\n\nCase CASE-4324, party Maya Lindgren:\n- purchase date: 2026-10-16\n- handover date: 2026-10-02",
  "question": "Filing rule: the refund request must be filed within 30 days starting from the later of the dates listed below: the purchase date and the handover date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the final day still in time for filing the refund request in case CASE-4324?",
  "options": [
   "2026-11-27",
   "2026-11-15",
   "2026-11-16",
   "2026-11-17"
  ]
 },
 {
  "qid": "q46e05d46ad",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nClara Weiss here, sending file POL-3156 about the loss claim and hoping it brightens your desk. Big thanks to the team on this.\nCheers,\n\nPolicy POL-3156, holder Clara Weiss:\n- policy start date: Tuesday, October 5, 2027\n- glass breakage cover: added by a rider effective Monday, October 18, 2027\n- glass breakage loss on: Tuesday, November 2, 2027\n- days from the policy start date to the loss: 28 days\n- days from the rider effective date to the loss: fifteen days",
  "question": "Cover rule: a loss is covered only after a waiting period of fourteen days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is fourteen days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the glass breakage loss on policy POL-3156 covered under the cover rule?"
 },
 {
  "qid": "q9764391211",
  "kind": "yes/no",
  "text": "Subject: papers for the desk\nDear desk,\nI am passing along file NTC-1930 about the notice response, which Priya Raman has sent in with courtesy. Thank you for your help.\nWarm regards\n\nNotice NTC-1930 to Priya Raman:\n- response due date: 14 July 2028\n- office cutoff on the due date: 2028-07-14 12:42:00 +0200\n- response sent: 2028-07-14 10:42:00 +0000 [same instant in office time: 2028-07-14 12:42:00 +0200]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Priya Raman late, since the office recorded it as received after the due date under the receipt rule?"
 },
 {
  "qid": "q313b3a7ba9",
  "kind": "yes/no",
  "text": "Omar Saleh sends file POL-1108 about the cover question to the admin team. Sending this across quickly because I am tied up with other work. The full file is attached for the team. Thanks for taking it.\n\nPolicy POL-1108, holder Omar Saleh:\n- policy start date: 2026-12-21\n- theft cover: added by a rider effective 2027-06-27\n- theft loss on: 2027-08-10\n- days from the policy start date to the loss: 232 days\n- days from the rider effective date to the loss: 44 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days that opens on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is it true that the theft loss in policy POL-1108 is not covered?"
 },
 {
  "qid": "qd27c74d8c5",
  "kind": "yes/no",
  "text": "[service] file=STAY-7666 about the visa stay count came_from=Iris Vance\n[service] addressed_to=service desk, cheerful_thanks\n\nStay record STAY-7666 for Iris Vance:\n- entry day Sunday, 25 January 2026, exit day Sunday, 25 January 2026 (whole stay: 1 day)\n- entry day Monday, 9 February 2026, exit day Thursday, 19 February 2026 (whole stay: 11 days)\n- entry day Saturday, 7 March 2026, exit day Saturday, 14 March 2026 (whole stay: 8 days)\nReference date: Wednesday, 25 March 2026\nWindow checked: Sunday, 25 January 2026 to Wednesday, 25 March 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 21 days within every moving 60-day stretch. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Iris Vance over the stay limit, with more days present inside the window that ends on the reference date in file STAY-7666, under the stay rule?"
 },
 {
  "qid": "q1342adc73f",
  "kind": "yes/no",
  "text": "Desk memo: Please be advised that Felix Ortega has sent file POL-2206 concerning the cover question to the desk.\nKindly route it to the review team at your convenience. Thank you for your attention.\n\nPolicy POL-2206, holder Felix Ortega:\n- policy start date: Thursday, December 17, 2026\n- storm damage cover: added by a rider effective Thursday, July 8, 2027\n- storm damage loss on: Thursday, July 22, 2027\n- days from the policy start date to the loss: 217 days\n- days from the rider effective date to the loss: 14 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 15 days with the start date itself left out, beginning the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 15 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, is the storm damage loss for Felix Ortega covered under the cover rule?"
 },
 {
  "qid": "qe8ca08d7f1",
  "kind": "choice",
  "text": "title | routine file check\nrequester | Ana Ruiz\nfile | LED-6594\nThe teller ledger review goes to the intake team for standard handling.\n\nCash ledger LED-6594, teller Ana Ruiz:\n- 2028-08-25: deposit of $5,091.00\n- 2028-08-27: withdrawal of $10,057.00\n- 2028-08-27: deposit of $1,077.00\n- 2028-08-27: deposit of $13,924.00\n- 2028-08-27: withdrawal of $7,786.00\n- 2028-08-29: deposit of $3,625.00\nDay under review: 2028-08-27",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any total greater than $15,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nFor 2028-08-27, which of the day's totals, under the cash rule, call for a cash report?",
  "options": [
   "Neither total",
   "Both totals",
   "Only the deposit total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q1f2a3aca61",
  "kind": "yes/no",
  "text": "Subject: Little catch-up on the visa stay count\n\nHey review team,\n\nDropping file STAY-5216 off from Priya Raman, hope it lands nicely with you. Enjoy the rest of your stretch.\n\nCheers,\n\nStay record STAY-5216 for Priya Raman:\n- entry day Tuesday, December 30, 2025, exit day Saturday, January 17, 2026 (whole stay: 19 days)\n- entry day Saturday, February 7, 2026, exit day Thursday, May 7, 2026 (whole stay: 90 days)\nReference date: Sunday, July 5, 2026\nWindow checked: Sunday, March 8, 2026 to Sunday, July 5, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days in any 120-day period that rolls forward day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Priya Raman within the stay limit for file STAY-5216, with days present at most the limit, under the stay rule?"
 }
]
