# G5-H blind read T01-blind_read-a91a9b05-001 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T01/pilot/g5h/answers/T01-blind_read-a91a9b05-001.json

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
  "qid": "q66d183561e",
  "kind": "choice",
  "text": "team: intake team\nsent_by: Lena Whitcombe\nfile: STAY-3165\nsubject: the border stay check\nnote: respectfully submitted\n\nStay record STAY-3165 for Lena Whitcombe:\n- entry day 2026-07-09, exit day 2026-07-23 (whole stay: fifteen days)\n- entry day 2026-08-03, exit day 2026-09-25 (whole stay: 54 days)\nReference date: 2026-11-23\nWindow checked: 2026-08-26 to 2026-11-23, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 30 days inside every moving 90-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present for Lena Whitcombe fall inside the checked window ending on 2026-11-23?",
  "options": [
   "0 days",
   "31 days",
   "30 days"
  ]
 },
 {
  "qid": "q91f972a3a7",
  "kind": "choice",
  "text": "file: STAY-8127\nsent_by: Tomas Lindqvist\nsubject: the visa stay count\nteam: review team\nchannel: cheerful_hello\n\nStay record STAY-8127 for Tomas Lindqvist:\n- entry day April 2, 2025, exit day June 20, 2025 (whole stay: 80 days)\n- entry day July 24, 2025, exit day August 5, 2025 (whole stay: 13 days)\n- entry day September 1, 2025, exit day September 25, 2025 (whole stay: 25 days)\nReference date: October 22, 2025\nWindow checked: April 26, 2025 to October 22, 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 90 days inside every 180-day stretch that moves along. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, how many days present for file STAY-8127 fall inside the checked window that ends on the reference date?",
  "options": [
   "93 days",
   "95 days",
   "91 days",
   "94 days"
  ]
 },
 {
  "qid": "qa7c47fa20f",
  "kind": "yes/no",
  "text": "[intake] file=CASE-5468 sender=Nadia Kowal route=admin_team\n[intake] note=the appeal deadline is on its way\n\nCase CASE-5468, party Nadia Kowal:\n- decision date: June 23, 2026\n- delivery date: June 16, 2026\n- appeal filed on: August 23, 2026\n- days from the decision date to the filing: 61 days\n- days from the delivery date to the filing: 68 days",
  "question": "Filing rule: the appeal must be filed within 60 days after the later date out of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the appeal in case CASE-5468 filed in time, on or before the final day?"
 },
 {
  "qid": "q7984856c50",
  "kind": "choice",
  "text": "Sent by: Bruno Lacerda\nFile: LED-8100\nSent to: records clerk\nLovely to send this over, it is about the branch cash review. The notes are all tidy and sit nicely for the records team.\n\nCash ledger LED-8100, teller Bruno Lacerda:\n- July 26, 2025: deposit of $3,260.00\n- July 26, 2025: withdrawal of $3,761.00\n- July 27, 2025: withdrawal of $1,193.00\nDay under review: July 26, 2025",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is a figure greater than $3,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals recorded in ledger LED-8100 call for a cash report under the cash rule?",
  "options": [
   "Neither total",
   "Only the withdrawal total",
   "Only the deposit total",
   "Both totals"
  ]
 },
 {
  "qid": "q5cc94a098b",
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
  "qid": "q9a32ef9527",
  "kind": "choice",
  "text": "Owen Pryce: Routine send, LED-4250 about the branch cash review.\nintake team: Received, thank you.\n\nCash ledger LED-4250, teller Owen Pryce:\n- 19 December 2027: withdrawal of $4,690\n- 21 December 2027: withdrawal of $4,941\n- 21 December 2027: withdrawal of $657\n- 21 December 2027: deposit of $17,632\nDay under review: 21 December 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any sum more than $15,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, for Owen Pryce on 21 December 2027, which of the day's totals call for a cash report?",
  "options": [
   "Both totals",
   "Neither total",
   "Only the deposit total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q1208142409",
  "kind": "yes/no",
  "text": "Jonas Feld: quick drop, file LED-2289 about the cash ledger check\ndesk: got it, moving it to the help desk\nagent: busy queue, sorting it out fast\n\nCash ledger LED-2289, teller Jonas Feld:\n- Sunday, 10 October 2027: deposit of $5,986\n- Sunday, 10 October 2027: withdrawal of $1,932\n- Sunday, 10 October 2027: deposit of $119\n- Monday, 11 October 2027: withdrawal of $1,623\nDay under review: Sunday, 10 October 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is $5,000 bar, cleared only by more than that, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs a cash report, under the cash rule, required for Sunday, 10 October 2027?"
 },
 {
  "qid": "q1f121e3050",
  "kind": "yes/no",
  "text": "title | the reply timing question with file NTC-7818\nrequester | Malik Osei\nteam | review_team\nnote | shares it here, thanks\n\nNotice NTC-7818 to Malik Osei:\n- response due date: 2028-08-09\n- office cutoff on the due date: 9 August 2028, 17:00 (UTC+09:00)\n- response sent: 2028-08-09T07:59:00Z [same instant in office time: 9 August 2028, 16:59 (UTC+09:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the reply to notice NTC-7818 on time under the receipt rule?"
 },
 {
  "qid": "q2f24485fee",
  "kind": "choice",
  "text": "Omar Saleh: File NTC-6791 is sent about the notice response as normal.\ncase team: Received, thank you.\n\nNotice NTC-6791 to Omar Saleh:\n- notice date: 2025-06-30\n- sent by: email\n- 28 days after the notice date, before any postal add-on or closure: 2025-07-28\nOffice closures: 2025-07-28; 2025-07-29.",
  "question": "Response rule: a response is due 28 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 2 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the due date of the response to notice NTC-6791 under the response rule?",
  "options": [
   "2025-07-30",
   "2025-07-28"
  ]
 },
 {
  "qid": "q1634e62169",
  "kind": "choice",
  "text": "Lucas Brenner: Hi there, file CASE-1419 about the appeal deadline is winging its way to you!\nclerk: Lovely, the admin team sorts it out from there.\n\nCase CASE-1419, party Lucas Brenner:\n- decision date: 19 May 2026\n- delivery date: 20 May 2026",
  "question": "Filing rule: the appeal must be filed within 90 days after the later date out of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 90 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, by which final day can Lucas Brenner still file the appeal and remain in time?",
  "options": [
   "18 August 2026",
   "23 September 2026",
   "17 August 2026"
  ]
 },
 {
  "qid": "qd56c27f0d8",
  "kind": "choice",
  "text": "Title | file LED-2245 about the branch cash review\nRequester | Tomas Lindqvist\nTeam | review team, cheers for the review!\n\nCash ledger LED-2245, teller Tomas Lindqvist:\n- 2025-05-16: deposit of $675\n- 2025-05-17: withdrawal of $684\n- 2025-05-17: deposit of $893\n- 2025-05-17: deposit of $1,689\n- 2025-05-17: withdrawal of $2,317\nDay under review: 2025-05-17",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any amount that is more than $3,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, for Tomas Lindqvist on 2025-05-17, which of the day's totals call for a cash report?",
  "options": [
   "Only the deposit total",
   "Both totals",
   "Neither total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q58ddc75048",
  "kind": "yes/no",
  "text": "sent_by: Iris Vance\nfile: STAY-9580\nsubject: the residence day count\nteam: review\nchannel: quick_lane\n\nStay record STAY-9580 for Iris Vance:\n- entry day Thursday, 11 November 2027, exit day Tuesday, 16 November 2027 (whole stay: 6 days)\n- entry day Thursday, 2 December 2027, exit day Monday, 13 December 2027 (whole stay: 12 days)\n- entry day Thursday, 30 December 2027, exit day Saturday, 8 January 2028 (whole stay: 10 days)\nReference date: Tuesday, 18 January 2028\nWindow checked: Saturday, 20 November 2027 to Tuesday, 18 January 2028, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 21 days during any 60-day window that moves ahead. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is the person in file STAY-9580 inside the stay limit when days present in the window ending Tuesday, 18 January 2028 total at most the limit?"
 },
 {
  "qid": "q08471b670e",
  "kind": "yes/no",
  "text": "subject: the supplier order\nfile: PO-9616\nrequester: Lena Whitcombe\nnote: kindly hands in this to the desk\n\nPurchase log PO-9616, kept by Lena Whitcombe, vendor Corvane Office:\n- earlier purchase on 21 Dec 2025: 11,814.00 USD\n- earlier purchase on 28 Dec 2025: 1,441.00 USD\n- earlier purchase on 13 Jan 2026: 11,243.00 USD\n- new request on 20 Jan 2026: 12,317.00 USD\nWindow checked: 22 Dec 2025 to 20 Jan 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is 25,000.00 USD as a floor, greater than that counts, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, must the purchase request in log PO-9616 for Lena Whitcombe come with written quotes?"
 },
 {
  "qid": "q7077cc2ad4",
  "kind": "yes/no",
  "text": "[intake] sender=Ana Ruiz file=PO-2280\n[intake] subject=the buying request channel=standard_route\n\nPurchase log PO-2280, kept by Ana Ruiz, vendor Halden Tools:\n- earlier purchase on 5 Feb 2027: $5,969\n- earlier purchase on 14 May 2027: $1,597\n- earlier purchase on 7 Aug 2027: $4,095\n- new request on 11 Aug 2027: $4,309\nWindow checked: 14 May 2027 to 11 Aug 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is $10,000 as a floor, greater than that counts, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request made by Ana Ruiz need written quotes under the purchase rule?"
 },
 {
  "qid": "q76dbc3c3b0",
  "kind": "yes/no",
  "text": "Freya Holm: Happy to pass on file CASE-5325 with notes on the complaint filing.\ndesk: Appreciated, this goes straight into the queue.\ndesk: Thank you for the courtesy.\n\nCase CASE-5325, party Freya Holm:\n- incident date: Thursday, 5 August 2027\n- discovery date: Tuesday, 3 August 2027\n- complaint filed on: Thursday, 28 October 2027\n- days from the incident date to the filing: 84 days\n- days from the discovery date to the filing: 86 days",
  "question": "Filing rule: the complaint must be filed within 60 days measured beyond the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 60 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHas the person failed to file the complaint for case CASE-5325 by the deadline?"
 },
 {
  "qid": "qb8f7268083",
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
  "qid": "q7cc86c9355",
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
  "qid": "qef9830418c",
  "kind": "choice",
  "text": "Subject: routine file for the case team\nDear case team,\nFile CASE-7048 about the claim deadline question has been sent in by Lena Whitcombe. Standard handling applies.\nRegards\n\nCase CASE-7048, party Lena Whitcombe:\n- inspection date: 2026-10-19\n- report date: 2026-10-20",
  "question": "Filing rule: the objection must be filed within 21 days following the later of these dates: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUntil which date, under the filing rule, may Lena Whitcombe file the objection in time?",
  "options": [
   "2026-11-18",
   "2026-11-11",
   "2026-11-10"
  ]
 },
 {
  "qid": "qacedd18fdc",
  "kind": "yes/no",
  "text": "Title | file CASE-5397 about the complaint filing\nRequester | Theo Kalnins\nRouted to | intake team\nKindly handle this at your convenience.\n\nCase CASE-5397, party Theo Kalnins:\n- incident date: 2026-12-07\n- discovery date: 2026-11-27\n- complaint filed on: 2026-12-29\n- days from the incident date to the filing: 22 days\n- days from the discovery date to the filing: 32 days",
  "question": "Filing rule: the complaint must be filed within 28 days following the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Theo Kalnins fail to file the complaint in case CASE-5397 by the deadline?"
 },
 {
  "qid": "q9ecbb53f72",
  "kind": "yes/no",
  "text": "Iris Vance: File POL-9193 about the cover question is on its way to you.\nclerk: Fine, the usual steps apply.\nclerk: Standard handling for this material.\n\nPolicy POL-9193, holder Iris Vance:\n- policy start date: January 8, 2026\n- glass breakage cover: added by a rider effective April 10, 2026\n- glass breakage loss on: May 2, 2026\n- days from the policy start date to the loss: 114 days\n- days from the rider effective date to the loss: 22 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, is it true that the loss on policy POL-9193 is not covered?"
 },
 {
  "qid": "q5dc0379066",
  "kind": "yes/no",
  "text": "{\"file\": \"CASE-1232\", \"sent_by\": \"Tomas Lindqvist\", \"subject\": \"the claim deadline question\", \"note\": \"big thanks\", \"channel\": \"service_desk\"}\n\nCase CASE-1232, party Tomas Lindqvist:\n- invoice date: 8 Mar 2026\n- goods received date: 3 Feb 2026\n- claim filed on: 14 Mar 2026\n- days from the invoice date to the filing: 6 days\n- days from the goods received date to the filing: 39 days",
  "question": "Filing rule: the claim must be filed within 30 days running from the later of the dates below: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the claim lodged by the final day of the filing period?"
 },
 {
  "qid": "qa4a0760569",
  "kind": "choice",
  "text": "clerk: heads up, a new item is landing\nHana Sato: file LED-1892 about the teller ledger review is going to the help desk\ndesk: understood, routing it straight away\n\nCash ledger LED-1892, teller Hana Sato:\n- Monday, May 3, 2027: deposit of 1,223.00 USD\n- Wednesday, May 5, 2027: deposit of 1,209.00 USD\n- Wednesday, May 5, 2027: deposit of 308.00 USD\n- Wednesday, May 5, 2027: withdrawal of 153.00 USD\n- Wednesday, May 5, 2027: withdrawal of 1,574.00 USD\nDay under review: Wednesday, May 5, 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is anything strictly greater than 3,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals in ledger LED-1892 for Wednesday, May 5, 2027 call for a cash report under the cash rule?",
  "options": [
   "Both totals",
   "Neither total",
   "Only the deposit total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q955eb97bf8",
  "kind": "yes/no",
  "text": "[intake] Iris Vance sends file STAY-6244 about the border stay check for review_team\n[route] queue=review_team priority=busy\n\nStay record STAY-6244 for Iris Vance:\n- entry day 2027-05-05, exit day 2027-05-11 (whole stay: seven days)\n- entry day 2027-06-05, exit day 2027-06-06 (whole stay: two days)\n- entry day 2027-06-27, exit day 2027-07-24 (whole stay: 28 days)\nReference date: 2027-08-09\nWindow checked: 2027-05-12 to 2027-08-09, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 45 days in any 90-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is it true that Iris Vance is not over the stay limit?"
 },
 {
  "qid": "qb9d1a586b6",
  "kind": "choice",
  "text": "{\"sent_by\": \"Yara Haddad\", \"file\": \"NTC-2152\", \"subject\": \"the notice response\", \"team\": \"records_clerk\"}\n\nNotice NTC-2152 to Yara Haddad:\n- response due date: 18 February 2026\n- office cutoff on the due date: 2026-02-18 18:30:00 +0300\n- response sent: 2026-02-18 12:31:00 -0300 [same instant in office time: 2026-02-18 18:31:00 +0300]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn which date does the office treat the response to notice NTC-2152 as received under the receipt rule?",
  "options": [
   "20 February 2026",
   "19 February 2026"
  ]
 },
 {
  "qid": "qd2718a9fd7",
  "kind": "choice",
  "text": "Omar Saleh: File NTC-8888 about the notice response is on its way to you.\nclerk: Fine, the usual steps apply.\nclerk: Standard handling for this material.\n\nNotice NTC-8888 to Omar Saleh:\n- notice date: Friday, 22 September 2028\n- sent by: email\n- twenty days after the notice date, before any postal add-on or closure: Thursday, 12 October 2028\nOffice closures: Thursday, 12 October 2028; Friday, 13 October 2028.",
  "question": "Response rule: a response is due twenty days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add two days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, on which date is the response from Omar Saleh to the notice due under the response rule?",
  "options": [
   "Friday, 20 October 2028",
   "Saturday, 14 October 2028"
  ]
 },
 {
  "qid": "q976929b8e7",
  "kind": "yes/no",
  "text": "Subject: Routine send on the supplier order\n\nHello intake team,\n\nSending file PO-9013 from Clara Weiss for the usual intake steps. Standard handling is fine.\n\nRegards,\n\nPurchase log PO-9013, kept by Clara Weiss, vendor Corvane Office:\n- earlier purchase on 2026-11-10: $444\n- earlier purchase on 2026-11-14: $1,031\n- new request on 2026-12-09: $1,526\nWindow checked: 2026-11-10 to 2026-12-09, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any sum more than $3,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the request from Clara Weiss, under the purchase rule, call for written quotes in log PO-9013?"
 },
 {
  "qid": "q99d57e8884",
  "kind": "choice",
  "text": "Subject: File NTC-6606 for the records clerk\nHello records clerk,\nAttached is a short note from Ines Duarte about the notice response.\nBest regards,\n\nNotice NTC-6606 to Ines Duarte:\n- notice date: Monday, September 14, 2026\n- sent by: post\n- 21 days after the notice date, before any postal add-on or closure: Monday, October 5, 2026\nOffice closures: Thursday, October 8, 2026; Friday, October 9, 2026.",
  "question": "Response rule: a response is due 21 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add three days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the due date for the response from Ines Duarte to the notice under the response rule?",
  "options": [
   "Friday, October 16, 2026",
   "Saturday, October 10, 2026"
  ]
 },
 {
  "qid": "qa529f262bf",
  "kind": "choice",
  "text": "[front_desk] lovely little drop-off, file PO-3723 sent_by Felix Ortega about the buying request\n[route] cheers_from_the_desk, passing on\n\nPurchase log PO-3723, kept by Felix Ortega, vendor Quillon Labs:\n- earlier purchase on Wednesday, 7 January 2026: $3,905\n- new request on Thursday, 8 January 2026: $832\nWindow checked: Wednesday, 10 December 2025 to Thursday, 8 January 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any amount that is more than $5,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, which running total for Felix Ortega gets compared with the threshold when this new request is counted in it?",
  "options": [
   "$3,905",
   "$4,737"
  ]
 },
 {
  "qid": "q001eb96bc2",
  "kind": "yes/no",
  "text": "{\"file\": \"POL-1072\", \"sent_by\": \"Iris Vance\", \"subject\": \"the cover question\", \"note\": \"kindly handled by the duty clerk\", \"channel\": \"duty_intake\"}\n\nPolicy POL-1072, holder Iris Vance:\n- policy start date: Wednesday, May 5, 2027\n- fire damage cover: added by a rider effective Monday, May 17, 2027\n- fire damage loss on: Monday, June 21, 2027\n- days from the policy start date to the loss: 47 days\n- days from the rider effective date to the loss: 35 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 60 days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 60 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is this fire damage loss covered by the cover rule?"
 },
 {
  "qid": "q8ad48f486a",
  "kind": "choice",
  "text": "{\n  \"sent_by\": \"Felix Ortega\",\n  \"file\": \"PO-3723\",\n  \"subject\": \"the buying request\",\n  \"team\": \"review team\",\n  \"note\": \"hiya, chatting away\"\n}\n\nPurchase log PO-3723, kept by Felix Ortega, vendor Quillon Labs:\n- earlier purchase on Wednesday, 7 January 2026: $3,905\n- new request on Thursday, 8 January 2026: $1,582\nWindow checked: Wednesday, 10 December 2025 to Thursday, 8 January 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any amount that is more than $5,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, which running total for Felix Ortega gets compared with the threshold when this new request is counted in it?",
  "options": [
   "$3,905",
   "$5,487"
  ]
 },
 {
  "qid": "q8f084004da",
  "kind": "yes/no",
  "text": "Desk memo: Omar Saleh is sending file STAY-4168 about the border stay check to the admin team. Pick it up fast, the work is waiting.\n\nStay record STAY-4168 for Omar Saleh:\n- entry day 2027-03-16, exit day 2027-06-12 (whole stay: 89 days)\nReference date: 2027-07-20\nWindow checked: 2027-01-22 to 2027-07-20, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 90 days in each 180-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, do the days present for Omar Saleh inside the checked window ending on the reference date exceed the stay limit?"
 },
 {
  "qid": "q67dd56608a",
  "kind": "choice",
  "text": "Subject: file handover\nDear duty clerk,\nThe file LED-1537 has come from Clara Weiss about the teller ledger review, for your desk.\nRegards,\n\nCash ledger LED-1537, teller Clara Weiss:\n- April 3, 2026: withdrawal of $6,313.00\n- April 4, 2026: deposit of $303.00\n- April 4, 2026: withdrawal of $788.00\n- April 4, 2026: deposit of $4,089.00\n- April 4, 2026: withdrawal of $3,313.00\nDay under review: April 4, 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any total greater than $10,000.00, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals on April 4, 2026 in ledger LED-1537, under the cash rule, call for a cash report?",
  "options": [
   "Both totals",
   "Only the deposit total",
   "Neither total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q811d1bc5c8",
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
  "qid": "q6bf71bf872",
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
  "qid": "q021c96f74d",
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
  "qid": "q4158d3e88e",
  "kind": "yes/no",
  "text": "Subject: quick pass\nHi review team,\nAiko Brandt sent in file NTC-8359 about the notice response. Please give it a fast look and reply.\nThanks,\n\nNotice NTC-8359 to Aiko Brandt:\n- response due date: 18 September 2026\n- office cutoff on the due date: 18 September 2026, 18:30 (UTC+03:00)\n- response sent: 18 September 2026, 03:51 (UTC+02:00) [same instant in office time: 18 September 2026, 04:51 (UTC+03:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was Aiko Brandt's response on time under the receipt rule?"
 },
 {
  "qid": "qfcbca9b6ad",
  "kind": "yes/no",
  "text": "[mail] pass_along=Lena Whitcombe file=CASE-3143 queue=admin_team\n[mail] subject=the claim deadline question big_thanks\n\nCase CASE-3143, party Lena Whitcombe:\n- invoice date: 2027-02-21\n- goods received date: 2027-01-22\n- claim filed on: 2027-03-23\n- days from the invoice date to the filing: 30 days\n- days from the goods received date to the filing: 60 days",
  "question": "Filing rule: the claim must be filed within 45 days following the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is it true that the claim was not filed in time?"
 },
 {
  "qid": "q4007d3a18e",
  "kind": "choice",
  "text": "Desk memo: Quick heads up, Sara Ilves sent in file STAY-6080 about the visa stay count and it is in the review team's hands. Thanks for flagging it, that helps.\n\nStay record STAY-6080 for Sara Ilves:\n- entry day Friday, September 25, 2026, exit day Thursday, October 1, 2026 (whole stay: seven days)\n- entry day Tuesday, November 3, 2026, exit day Wednesday, December 2, 2026 (whole stay: 30 days)\nReference date: Wednesday, December 30, 2026\nWindow checked: Friday, October 2, 2026 to Wednesday, December 30, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 30 days inside every 90-day stretch that moves along. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days present fall inside the checked window that ends on the reference date in record STAY-6080?",
  "options": [
   "30 days",
   "29 days"
  ]
 },
 {
  "qid": "q9baf16d152",
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
  "qid": "q35e566c49e",
  "kind": "choice",
  "text": "Desk memo: Ravi Anand has put file STAY-7443 on the visa stay count in front of the help desk. Lovely little hand-off, thanks for picking it up. Cheers to the team.\n\nStay record STAY-7443 for Ravi Anand:\n- entry day 16 Sep 2025, exit day 30 Oct 2025 (whole stay: 45 days)\n- entry day 8 Dec 2025, exit day 9 Jan 2026 (whole stay: 33 days)\n- entry day 31 Jan 2026, exit day 13 Mar 2026 (whole stay: 42 days)\nReference date: 12 Apr 2026\nWindow checked: 15 Oct 2025 to 12 Apr 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 90 days in any 180-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 180-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 90 days, and within the limit if it is 90 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, how many days present for file STAY-7443 fall inside the checked window that ends on the reference date?",
  "options": [
   "92 days",
   "120 days",
   "91 days",
   "75 days"
  ]
 },
 {
  "qid": "q76c7230fb6",
  "kind": "yes/no",
  "text": "title | the reply timing question with file NTC-7818\nrequester | Malik Osei\nteam | review_team\nnote | shares it here, thanks\n\nNotice NTC-7818 to Malik Osei:\n- response due date: 2028-08-09\n- office cutoff on the due date: 9 August 2028, 17:00 (UTC+09:00)\n- response sent: 2028-08-09T12:44:00Z [same instant in office time: 9 August 2028, 21:44 (UTC+09:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the reply to notice NTC-7818 on time under the receipt rule?"
 },
 {
  "qid": "qc57109c568",
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
  "qid": "qd0cc7bd473",
  "kind": "yes/no",
  "text": "title | rush handoff\nrequester | Freya Holm\nfile | STAY-5106\nDropping the border stay check with the admin team, board is full.\n\nStay record STAY-5106 for Freya Holm:\n- entry day Sunday, December 6, 2026, exit day Thursday, January 7, 2027 (whole stay: 33 days)\n- entry day Wednesday, January 13, 2027, exit day Wednesday, January 20, 2027 (whole stay: eight days)\nReference date: Sunday, January 31, 2027\nWindow checked: Saturday, January 2, 2027 to Sunday, January 31, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most fourteen days across any 30-day window that slides ahead day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 30-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than fourteen days, and within the limit if it is fourteen days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does Freya Holm have more days present in the checked window ending on Sunday, January 31, 2027 than the stay limit?"
 },
 {
  "qid": "qc8d2bcc0e3",
  "kind": "yes/no",
  "text": "Subject: the branch cash review, file LED-5124\nHello admin team,\nSending this in a rush from Tomas Lindqvist. Give it a look.\nBye, and thanks.\n\nCash ledger LED-5124, teller Tomas Lindqvist:\n- Wednesday, 8 December 2027: withdrawal of $1,536\n- Thursday, 9 December 2027: withdrawal of $687\n- Thursday, 9 December 2027: withdrawal of $2,314\n- Thursday, 9 December 2027: deposit of $3,450\nDay under review: Thursday, 9 December 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is greater than the sum of $3,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the cash rule let the day in ledger LED-5124 close without a cash report?"
 },
 {
  "qid": "qe7764e8845",
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
  "qid": "q4cf3b98e04",
  "kind": "choice",
  "text": "File: PO-3317\nSubject: the purchase request\nFrom: Ines Duarte\nSending this straight across to the records clerk. The desk is very busy and stretched.\n\nPurchase log PO-3317, kept by Ines Duarte, vendor Corvane Office:\n- earlier purchase on 24 Nov 2027: $2,509.00\n- earlier purchase on 15 Feb 2028: $3,524.00\n- earlier purchase on 16 Feb 2028: $7,458.00\n- new request on 16 Mar 2028: $2,543.00\nWindow checked: 16 Feb 2028 to 16 Mar 2028, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is strictly more than $10,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what total does the purchase rule compare with its threshold for Ines Duarte, including the new request?",
  "options": [
   "$13,525.00",
   "$10,001.00"
  ]
 },
 {
  "qid": "q98da96c3ec",
  "kind": "yes/no",
  "text": "service desk: Send it over, ready for it.\nPaolo Greco: Here is file POL-8418, the insurance claim, a rush job.\n\nPolicy POL-8418, holder Paolo Greco:\n- policy start date: 18 Jan 2027\n- glass breakage cover: part of the base policy\n- glass breakage loss on: 26 Jan 2027\n- days from the policy start date to the loss: eight days",
  "question": "Cover rule: a loss is covered only after a waiting period of ten days whose earliest counted day is the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is ten days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid the glass breakage loss in policy POL-8418 occur within the waiting period, on or before its final day, under the cover rule?"
 },
 {
  "qid": "q9bfa7b20b5",
  "kind": "choice",
  "text": "file: POL-1677\nsent_by: Bruno Lacerda\nsubject: the insurance claim\nteam: review team\nchannel: cheerful_hello\n\nPolicy POL-1677, holder Bruno Lacerda:\n- policy start date: 2026-06-03\n- storm damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days whose opening count lands on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date, under the cover rule, from which the storm damage loss would be covered?",
  "options": [
   "2026-07-04",
   "2026-07-06",
   "2026-07-02"
  ]
 },
 {
  "qid": "qb5a6b5db0b",
  "kind": "choice",
  "text": "Yara Haddad: Pleased to forward file STAY-3134 about the residence day count\nclerk: Thank you, leave it with the records team\n\nStay record STAY-3134 for Yara Haddad:\n- entry day Friday, December 3, 2027, exit day Monday, January 17, 2028 (whole stay: 46 days)\n- entry day Thursday, February 3, 2028, exit day Friday, February 4, 2028 (whole stay: 2 days)\n- entry day Tuesday, February 22, 2028, exit day Wednesday, March 8, 2028 (whole stay: 16 days)\nReference date: Sunday, March 19, 2028\nWindow checked: Tuesday, December 21, 2027 to Sunday, March 19, 2028, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 45 days in any 90-day span that moves ahead with each new day. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, how many days present for Yara Haddad fall inside the checked window ending on the reference date in file STAY-3134?",
  "options": [
   "64 days",
   "35 days",
   "46 days"
  ]
 },
 {
  "qid": "qa90d0a2ca4",
  "kind": "yes/no",
  "text": "sent_by: Lucas Brenner\nfile: NTC-5724\nsubject: the notice response\nteam: review\nchannel: quick_lane\n\nNotice NTC-5724 to Lucas Brenner:\n- response due date: 21 May 2025\n- office cutoff on the due date: 21 May 2025, 16:00 (UTC+02:00)\n- response sent: 21 May 2025, 10:55 (UTC-03:00) [same instant in office time: 21 May 2025, 15:55 (UTC+02:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response to notice NTC-5724 on time under the receipt rule?"
 }
]
