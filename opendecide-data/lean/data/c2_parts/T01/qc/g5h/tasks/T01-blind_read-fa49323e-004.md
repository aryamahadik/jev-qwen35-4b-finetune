# G5-H blind read T01-blind_read-fa49323e-004 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g5h/answers/T01-blind_read-fa49323e-004.json

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
  "qid": "qfb8d194c78",
  "kind": "choice",
  "text": "{\"sent_by\": \"Owen Pryce\", \"file\": \"CASE-9556\", \"subject\": \"the appeal deadline\", \"channel\": \"routine_intake\", \"team\": \"desk\"}\n\nCase CASE-9556, party Owen Pryce:\n- billing date: September 17, 2026\n- statement date: October 17, 2026",
  "question": "Filing rule: the dispute must be filed within 30 days running from the later of the dates below: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the final day still in time for filing the dispute in case CASE-9556?",
  "options": [
   "November 14, 2026",
   "November 15, 2026",
   "November 16, 2026"
  ]
 },
 {
  "qid": "qfedebd429c",
  "kind": "choice",
  "text": "{\"file\": \"LED-4743\", \"sent_by\": \"Freya Holm\", \"subject\": \"the branch cash review\", \"channel\": \"case team\"}\n\nCash ledger LED-4743, teller Freya Holm:\n- Monday, May 11, 2026: deposit of $9,439\n- Tuesday, May 12, 2026: deposit of $3,986\n- Tuesday, May 12, 2026: deposit of $5,428\n- Tuesday, May 12, 2026: withdrawal of $2,495\n- Tuesday, May 12, 2026: withdrawal of $3,104\n- Wednesday, May 13, 2026: withdrawal of $8,986\nDay under review: Tuesday, May 12, 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any total greater than $15,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals on Tuesday, May 12, 2026 in ledger LED-4743, under the cash rule, call for a cash report?",
  "options": [
   "Neither total",
   "Both totals",
   "Only the deposit total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "q94ba865965",
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
  "qid": "qd55be41132",
  "kind": "yes/no",
  "text": "Requester: Felix Ortega\nFile: POL-6190\nTopic line: the insurance claim\nRoute: case team, standard queue\n\nPolicy POL-6190, holder Felix Ortega:\n- policy start date: 2027-05-09\n- storm damage cover: part of the base policy\n- storm damage loss on: 2027-06-04\n- days from the policy start date to the loss: 26 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 25 days that opens on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 25 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is this storm damage loss covered by the cover rule?"
 },
 {
  "qid": "q6f0188108a",
  "kind": "yes/no",
  "text": "[help] Kofi Mensah sent in file NTC-9055 about the response deadline\n[desk] help_desk move fast\n\nNotice NTC-9055 to Kofi Mensah:\n- response due date: November 27, 2026\n- office cutoff on the due date: 2026-11-27T22:54:00-05:00\n- response sent: 2026-11-28T11:56:00+08:00 [same instant in office time: 2026-11-27T22:56:00-05:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Kofi Mensah to notice NTC-9055 on time under the receipt rule?"
 },
 {
  "qid": "q1a85c9ba1c",
  "kind": "yes/no",
  "text": "Dear duty clerk,\nYara Haddad is sending file STAY-2376 about the residence day count. The file is attached for your desk. Thanks in advance for your help.\nBest,\n\nStay record STAY-2376 for Yara Haddad:\n- entry day September 19, 2026, exit day November 4, 2026 (whole stay: 47 days)\nReference date: November 28, 2026\nWindow checked: August 31, 2026 to November 28, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 45 days in any rolling 90-day window. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does Yara Haddad have more days present in the checked window ending on November 28, 2026 than the stay limit?"
 },
 {
  "qid": "q1093ad3b2e",
  "kind": "yes/no",
  "text": "[log] file_id=LED-8608 from=Ravi Anand\n[log] matter=the branch cash review copied_to=desk\n\nCash ledger LED-8608, teller Ravi Anand:\n- 2027-01-29: withdrawal of $5,105.00\n- 2027-01-31: withdrawal of $1,719.00\n- 2027-01-31: withdrawal of $2,325.00\nDay under review: 2027-01-31",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is $10,000.00 itself excluded, only more than that counts, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, is a cash report required for the day under review in ledger LED-8608?"
 },
 {
  "qid": "q764696c089",
  "kind": "choice",
  "text": "Theo Kalnins: Here is file POL-6964 about the loss claim for the intake team.\nagent: Understood, reviewing it.\n\nPolicy POL-6964, holder Theo Kalnins:\n- policy start date: February 6, 2027\n- glass breakage cover: added by a rider effective February 23, 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 25 days whose clock starts running on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 25 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which the glass breakage loss in policy POL-6964 would be covered under the cover rule?",
  "options": [
   "March 21, 2027",
   "March 22, 2027",
   "March 23, 2027"
  ]
 },
 {
  "qid": "qcc826a2b6d",
  "kind": "yes/no",
  "text": "Yara Haddad: Hello. I am forwarding file STAY-2376 about the residence day count. My thanks for your help.\ncase team: Thank you, the file has been received.\n\nStay record STAY-2376 for Yara Haddad:\n- entry day September 19, 2026, exit day November 4, 2026 (whole stay: 47 days)\nReference date: November 28, 2026\nWindow checked: August 31, 2026 to November 28, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 45 days in any rolling 90-day window. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does Yara Haddad have more days present in the checked window ending on November 28, 2026 than the stay limit?"
 },
 {
  "qid": "q45403deec5",
  "kind": "choice",
  "text": "Subject: File STAY-1997 about the residence day count\nDear desk,\nThis is Tomas Lindqvist passing the paperwork across to you.\nWith thanks,\n\nStay record STAY-1997 for Tomas Lindqvist:\n- entry day August 21, 2026, exit day August 25, 2026 (whole stay: five days)\n- entry day September 6, 2026, exit day October 31, 2026 (whole stay: 56 days)\n- entry day December 8, 2026, exit day December 16, 2026 (whole stay: nine days)\nReference date: January 16, 2027\nWindow checked: September 19, 2026 to January 16, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 60 days across any 120-day window that slides ahead day by day. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, how many days present fall inside the checked window ending on January 16, 2027 in file STAY-1997?",
  "options": [
   "53 days",
   "51 days",
   "52 days"
  ]
 },
 {
  "qid": "q134e1e9c37",
  "kind": "yes/no",
  "text": "clerk: oh hey, what came in\nRavi Anand: got file STAY-8687 about the visa stay count here, nice and easy\ndesk: lovely, thanks, we are on it\n\nStay record STAY-8687 for Ravi Anand:\n- entry day Monday, June 7, 2027, exit day Monday, June 7, 2027 (whole stay: one day)\n- entry day Friday, July 16, 2027, exit day Saturday, September 11, 2027 (whole stay: 58 days)\n- entry day Sunday, October 3, 2027, exit day Monday, October 4, 2027 (whole stay: two days)\nReference date: Wednesday, October 27, 2027\nWindow checked: Wednesday, June 30, 2027 to Wednesday, October 27, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 60 days inside every moving 120-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs it true that Ravi Anand is not over the stay limit in record STAY-8687 under the stay rule?"
 },
 {
  "qid": "q25850e86ef",
  "kind": "choice",
  "text": "Paolo Greco: hey there, here is file STAY-3466 with the residence day count for you.\nfront desk: lovely, thanks for sending it over.\n\nStay record STAY-3466 for Paolo Greco:\n- entry day Saturday, 5 September 2026, exit day Monday, 28 September 2026 (whole stay: 24 days)\n- entry day Friday, 6 November 2026, exit day Saturday, 5 December 2026 (whole stay: 30 days)\nReference date: Tuesday, 5 January 2027\nWindow checked: Tuesday, 8 September 2026 to Tuesday, 5 January 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days within any 120-day window that keeps moving. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, how many days present fall inside the checked window ending on Tuesday, 5 January 2027 in file STAY-3466?",
  "options": [
   "52 days",
   "53 days",
   "51 days"
  ]
 },
 {
  "qid": "q6add5f1bfa",
  "kind": "yes/no",
  "text": "Aiko Brandt: forwarding file POL-7925 about the insurance claim to the case team, with respect.\ncase team: thank you kindly for passing it along.\n\nPolicy POL-7925, holder Aiko Brandt:\n- policy start date: December 12, 2026\n- flood damage cover: part of the base policy\n- flood damage loss on: February 11, 2027\n- days from the policy start date to the loss: 61 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 60 days that starts on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 60 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, is the flood damage loss for Aiko Brandt covered under the cover rule?"
 },
 {
  "qid": "q99e9dcbacd",
  "kind": "yes/no",
  "text": "Memo for the front desk: Omar Saleh sends file CASE-4056 about the appeal deadline. Grab it at your convenience, the queue is busy on this end.\n\nCase CASE-4056, party Omar Saleh:\n- billing date: Saturday, July 25, 2026\n- statement date: Saturday, August 8, 2026\n- dispute filed on: Wednesday, August 19, 2026\n- days from the billing date to the filing: 25 days\n- days from the statement date to the filing: eleven days",
  "question": "Filing rule: the dispute must be filed within ten days measured beyond the later of these dates: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is ten days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the dispute lodged by the final day of the filing period?"
 },
 {
  "qid": "q9140c4ff13",
  "kind": "choice",
  "text": "{\n  \"sent_by\": \"Mira Castell\",\n  \"file\": \"CASE-9502\",\n  \"subject\": \"the claim deadline question\",\n  \"team\": \"duty clerk\"\n}\n\nCase CASE-9502, party Mira Castell:\n- inspection date: 19 Apr 2027\n- report date: 16 Apr 2027",
  "question": "Filing rule: the objection must be filed within 45 days measured beyond the later of these dates: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the latest day on which Mira Castell may still file the objection in time?",
  "options": [
   "3 Jun 2027",
   "4 Jun 2027",
   "21 Jun 2027",
   "5 Jun 2027"
  ]
 },
 {
  "qid": "q8f6374e472",
  "kind": "choice",
  "text": "Desk memo: for the case team, kindly note that Maya Lindgren has sent in file CASE-7055 about the claim deadline question. With thanks in advance for your attention.\n\nCase CASE-7055, party Maya Lindgren:\n- invoice date: Monday, October 13, 2025\n- goods received date: Wednesday, October 15, 2025",
  "question": "Filing rule: the claim must be filed within fourteen days after the later date out of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is fourteen days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the final day on which Maya Lindgren can still file the claim in case CASE-7055 and be in time?",
  "options": [
   "Thursday, October 30, 2025",
   "Friday, October 31, 2025",
   "Wednesday, October 29, 2025"
  ]
 },
 {
  "qid": "qa5886a5422",
  "kind": "yes/no",
  "text": "file: CASE-3680\nsent_by: Mira Castell\nsubject: the claim deadline question\nteam: intake team\nnote: standard routing\n\nCase CASE-3680, party Mira Castell:\n- inspection date: Tuesday, 16 June 2026\n- report date: Friday, 31 July 2026\n- objection filed on: Thursday, 10 September 2026\n- days from the inspection date to the filing: 86 days\n- days from the report date to the filing: 41 days",
  "question": "Filing rule: the objection must be filed inside 30 days beginning at the later of these dates: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the objection from Mira Castell, under the filing rule, filed after the deadline?"
 },
 {
  "qid": "qf0173deccc",
  "kind": "yes/no",
  "text": "Eva Marsh: Hiya! Sending PO-4668 about the purchase request, all good here.\nservice desk: Lovely, thanks for the heads up!\n\nPurchase log PO-4668, kept by Eva Marsh, vendor Corvane Office:\n- earlier purchase on 7 May 2027: $5,788\n- earlier purchase on 26 Jul 2027: $3,002\n- new request on 5 Aug 2027: $5,009\nWindow checked: 8 May 2027 to 5 Aug 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is $10,000 as a floor, greater than that counts, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does the purchase request in log PO-4668 need written quotes under the purchase rule?"
 },
 {
  "qid": "qbd11088022",
  "kind": "choice",
  "text": "{\"channel\": \"intake\", \"file\": \"CASE-6617\", \"sent_by\": \"Hana Sato\", \"subject\": \"the claim deadline question\", \"team\": \"case_team\"}\n\nCase CASE-6617, party Hana Sato:\n- inspection date: June 27, 2027\n- report date: June 26, 2027",
  "question": "Filing rule: the objection must be filed within fourteen days starting from the later of the dates listed below: the inspection date and the report date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is fourteen days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the latest day on which Hana Sato may still file the objection in time?",
  "options": [
   "July 15, 2027",
   "July 11, 2027",
   "July 12, 2027"
  ]
 },
 {
  "qid": "q5803307467",
  "kind": "choice",
  "text": "sent_by: Theo Kalnins\nfile: POL-4473\nsubject: the insurance claim\nteam: case team\nnote: with thanks\n\nPolicy POL-4473, holder Theo Kalnins:\n- policy start date: December 9, 2026\n- burst pipe damage cover: added by a rider effective February 5, 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 88 days whose opening day is the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 88 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn what earliest date would a loss of this kind be covered under policy POL-4473?",
  "options": [
   "May 3, 2027",
   "May 5, 2027",
   "May 4, 2027"
  ]
 },
 {
  "qid": "q20a2571fb9",
  "kind": "yes/no",
  "text": "[intake] file=CASE-2235 sender=Kofi Mensah regarding the claim deadline question\n[note] kindly_forwarded_to=duty_clerk\n\nCase CASE-2235, party Kofi Mensah:\n- invoice date: Tuesday, February 2, 2027\n- goods received date: Saturday, January 23, 2027\n- claim filed on: Friday, March 19, 2027\n- days from the invoice date to the filing: 45 days\n- days from the goods received date to the filing: 55 days",
  "question": "Filing rule: the claim must be filed within 45 days starting from the later of the dates listed below: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 45 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Kofi Mensah fail to file the claim in case CASE-2235 by the deadline?"
 },
 {
  "qid": "q426060806b",
  "kind": "choice",
  "text": "Memo for the duty clerk: Lucas Brenner has passed on file STAY-4800 about the visa stay count. Courteous handling is appreciated.\n\nStay record STAY-4800 for Lucas Brenner:\n- entry day Monday, September 14, 2026, exit day Thursday, September 24, 2026 (whole stay: eleven days)\n- entry day Sunday, September 27, 2026, exit day Friday, December 25, 2026 (whole stay: 90 days)\nReference date: Saturday, February 20, 2027\nWindow checked: Saturday, October 24, 2026 to Saturday, February 20, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days in any 120-day window that keeps sliding forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present fall inside the checked window that ends on Saturday, February 20, 2027 for file STAY-4800?",
  "options": [
   "63 days",
   "62 days"
  ]
 },
 {
  "qid": "qd0e7893c80",
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
  "qid": "q7adcb39703",
  "kind": "yes/no",
  "text": "Subject: quick pass-along\nHi service desk,\nQuick note: Bruno Lacerda sends file PO-6507 about the purchase request, so please grab it at your earliest convenience.\nBest,\n\nPurchase log PO-6507, kept by Bruno Lacerda, vendor Brightwell Supply:\n- earlier purchase on Saturday, January 10, 2026: $2,484\n- earlier purchase on Tuesday, January 20, 2026: $1,810\n- earlier purchase on Sunday, January 25, 2026: $227\n- new request on Monday, February 9, 2026: $2,964\nWindow checked: Sunday, January 11, 2026 to Monday, February 9, 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is greater than $5,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request from Bruno Lacerda need written quotes under the purchase rule?"
 },
 {
  "qid": "qcd21b3162a",
  "kind": "yes/no",
  "text": "Dear front desk,\nI am writing to share file PO-6112 about the purchase request, sent by Hana Sato. Thank you for reading this message. The file is in full and in good shape. With respect and thanks.\nYours faithfully\n\nPurchase log PO-6112, kept by Hana Sato, vendor Ostrava Parts:\n- earlier purchase on 20 Feb 2027: $2,968\n- earlier purchase on 21 Apr 2027: $3,654\n- new request on 12 May 2027: $1,345\nWindow checked: 13 Apr 2027 to 12 May 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is $5,000 or greater, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, may request PO-6112 go ahead without written quotes under the purchase rule?"
 },
 {
  "qid": "qe89d9e98f0",
  "kind": "yes/no",
  "text": "Subject | file POL-8410 about the cover question\nFrom | Mira Castell\nGroup | help desk\nPlease take a quick peek.\n\nPolicy POL-8410, holder Mira Castell:\n- policy start date: Sunday, November 8, 2026\n- storm damage cover: part of the base policy\n- storm damage loss on: Monday, November 23, 2026\n- days from the policy start date to the loss: fifteen days",
  "question": "Cover rule: a loss is covered only after a waiting period of fifteen days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is fifteen days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, is the storm damage loss covered under the cover rule?"
 },
 {
  "qid": "q89fc14f9cf",
  "kind": "yes/no",
  "text": "Dana Okafor: Hey there! Sending file CASE-2544 about the appeal deadline your way, hope it helps lol.\nservice: Thanks so much, that is great.\ndesk: Awesome, we have it on screen.\n\nCase CASE-2544, party Dana Okafor:\n- billing date: 2028-01-08\n- statement date: 2028-02-07\n- dispute filed on: 2028-03-08\n- days from the billing date to the filing: 60 days\n- days from the statement date to the filing: 30 days",
  "question": "Filing rule: the dispute must be filed within 30 days following the later of these dates: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 30 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the dispute from Dana Okafor, under the filing rule, filed after the deadline?"
 },
 {
  "qid": "q70c3570fe0",
  "kind": "yes/no",
  "text": "title: file PO-8281 about the buying request\nrequester: Jonas Feld\nqueue: the front desk\nFriendly hello, here it is for a look.\n\nPurchase log PO-8281, kept by Jonas Feld, vendor Mirefield Print:\n- earlier purchase on 12 Oct 2025: $10,590.00\n- new request on 9 Jan 2026: $4,410.00\nWindow checked: 12 Oct 2025 to 9 Jan 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is strictly more than $15,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does request PO-8281 need written quotes under the purchase rule?"
 },
 {
  "qid": "q9fc4131290",
  "kind": "yes/no",
  "text": "A happy note from Hana Sato to the service desk. File NTC-2033 is about the response deadline, sent with a smile. Enjoy the rest of your work.\n\nNotice NTC-2033 to Hana Sato:\n- response due date: Sunday, December 26, 2027\n- office cutoff on the due date: 26 December 2027, 21:42 (UTC-05:00)\n- response sent: 27 December 2027, 01:33 (UTC-04:00) [same instant in office time: 27 December 2027, 00:33 (UTC-05:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Hana Sato to the notice late under the receipt rule?"
 },
 {
  "qid": "q13addecded",
  "kind": "choice",
  "text": "title | file NTC-9509 about the response deadline\nrequester | Aiko Brandt\nQuick handoff, sent straight to the review team.\n\nNotice NTC-9509 to Aiko Brandt:\n- response due date: 14 June 2028\n- office cutoff on the due date: 2028-06-14 13:01:00 -0500\n- response sent: 2028-06-13 14:59:00 -0300 [same instant in office time: 2028-06-13 12:59:00 -0500]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, on which date is the response from Aiko Brandt counted as received under the receipt rule?",
  "options": [
   "14 Jun 2028",
   "13 Jun 2028"
  ]
 },
 {
  "qid": "q57fbdbd6f1",
  "kind": "choice",
  "text": "Subject: submission for the duty clerk\nDear duty clerk,\nKindly note that Iris Vance sends file POL-2449 regarding the loss claim for your attention.\nYours sincerely,\n\nPolicy POL-2449, holder Iris Vance:\n- policy start date: December 4, 2026\n- glass breakage cover: added by a rider effective June 7, 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 90 days with the start date itself left out, beginning the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 90 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich is the earliest date that this glass breakage loss under policy POL-2449 would be covered?",
  "options": [
   "October 12, 2027",
   "September 8, 2027",
   "September 6, 2027"
  ]
 },
 {
  "qid": "qad2fa1094a",
  "kind": "choice",
  "text": "file: POL-9085\nsent_by: Ravi Anand\nsubject: the cover question\nteam: review team\nchannel: cheerful_hello\n\nPolicy POL-9085, holder Ravi Anand:\n- policy start date: March 15, 2027\n- flood damage cover: added by a rider effective October 6, 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of eleven days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is eleven days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on what earliest date would Ravi Anand be covered for the flood damage loss?",
  "options": [
   "October 18, 2027",
   "March 27, 2027",
   "October 16, 2027"
  ]
 },
 {
  "qid": "qca94cbb832",
  "kind": "yes/no",
  "text": "Desk memo: Lena Whitcombe shares file PO-2917 about the purchase request with the review team. Quick look, then pass it along. Thanks.\n\nPurchase log PO-2917, kept by Lena Whitcombe, vendor Corvane Office:\n- earlier purchase on 27 April 2026: $1,404.00\n- earlier purchase on 9 May 2026: $9,143.00\n- new request on 14 August 2026: $14,454.00\nWindow checked: 17 April 2026 to 14 August 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 120-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is a figure greater than $25,000.00, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, must the request from Lena Whitcombe be backed by written quotes under the purchase rule?"
 },
 {
  "qid": "qaaa0b8e5cd",
  "kind": "choice",
  "text": "{\"file\": \"POL-7770\", \"sent_by\": \"Nadia Kowal\", \"subject\": \"the insurance claim\", \"team\": \"duty clerk\"}\n\nPolicy POL-7770, holder Nadia Kowal:\n- policy start date: Wednesday, October 6, 2027\n- subsidence cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 15 days that begins on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 15 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the earliest date on which the subsidence loss under policy POL-7770 would be covered?",
  "options": [
   "Friday, October 22, 2027",
   "Saturday, October 23, 2027",
   "Thursday, October 21, 2027"
  ]
 },
 {
  "qid": "qec27703535",
  "kind": "choice",
  "text": "sent_by: Mira Castell\nfile: CASE-4181\nsubject: the claim deadline question\nteam: case team\nnote: with thanks\n\nCase CASE-4181, party Mira Castell:\n- invoice date: December 22, 2025\n- goods received date: December 29, 2025",
  "question": "Filing rule: the claim must be filed within 58 days reckoned after the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 58 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the latest date, under the filing rule, on which the claim for case CASE-4181 can be filed in time?",
  "options": [
   "February 26, 2026",
   "February 25, 2026",
   "March 19, 2026"
  ]
 },
 {
  "qid": "qda513488ba",
  "kind": "choice",
  "text": "Desk memo: Lena Whitcombe has sent in file POL-4658 about the insurance claim for the help desk. Move on it at speed, there is a lot in the queue.\n\nPolicy POL-4658, holder Lena Whitcombe:\n- policy start date: Tuesday, June 1, 2027\n- glass breakage cover: added by a rider effective Thursday, July 29, 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 90 days that starts on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 90 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the earliest date on which the glass breakage loss under policy POL-4658 would be covered?",
  "options": [
   "Friday, October 29, 2027",
   "Thursday, October 28, 2027",
   "Saturday, October 30, 2027",
   "Tuesday, October 26, 2027"
  ]
 },
 {
  "qid": "qe48bdd4e58",
  "kind": "choice",
  "text": "Aiko Brandt: file POL-3533 about the insurance claim is attached here.\ncase team: thank you, that is received.\ncase team: that is all for this file.\n\nPolicy POL-3533, holder Aiko Brandt:\n- policy start date: December 26, 2026\n- flood damage cover: added by a rider effective March 9, 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days that begins on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which the flood damage loss in policy POL-3533 would be covered under the cover rule?",
  "options": [
   "April 2, 2027",
   "April 8, 2027",
   "March 31, 2027",
   "April 1, 2027"
  ]
 },
 {
  "qid": "q5a448fcac4",
  "kind": "yes/no",
  "text": "Clara Weiss: ringing in to send file PO-4783 about the purchase request\ndesk: thanks, logging it for the team.\n\nPurchase log PO-4783, kept by Clara Weiss, vendor Ostrava Parts:\n- earlier purchase on Wednesday, December 2, 2026: $2,166\n- earlier purchase on Wednesday, February 3, 2027: $1,124\n- earlier purchase on Tuesday, March 2, 2027: $393\n- earlier purchase on Friday, March 12, 2027: $931\n- earlier purchase on Wednesday, March 31, 2027: $1,843\n- new request on Sunday, April 4, 2027: $1,833\nWindow checked: Thursday, February 4, 2027 to Sunday, April 4, 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is a figure of $5,000 or greater, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does the purchase request in log PO-4783 need written quotes under the purchase rule?"
 },
 {
  "qid": "q0df907f8af",
  "kind": "yes/no",
  "text": "Desk memo: Tomas Lindqvist has sent over file PO-8371 about the purchase request for the admin team. Thanks a lot for the help, that is a neat little job. Give it a warm welcome.\n\nPurchase log PO-8371, kept by Tomas Lindqvist, vendor Vantmoor Electric:\n- earlier purchase on 25 Nov 2026: $5,038\n- new request on 22 Feb 2027: $1,701\nWindow checked: 25 Nov 2026 to 22 Feb 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any total greater than $10,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does request PO-8371 need written quotes under the purchase rule?"
 },
 {
  "qid": "q3b26791ba0",
  "kind": "choice",
  "text": "file: POL-5343\nsent_by: Priya Raman\nsubject: the loss claim\nteam: service desk\nnote: a friendly hello\n\nPolicy POL-5343, holder Priya Raman:\n- policy start date: Tuesday, 26 October 2027\n- theft cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 90 days starting with the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 90 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on what earliest date would the theft loss be covered?",
  "options": [
   "Monday, 24 January 2028",
   "Tuesday, 25 January 2028",
   "Thursday, 27 January 2028"
  ]
 },
 {
  "qid": "q61f3a094c6",
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
  "qid": "q566927c910",
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
  "qid": "q3d6f55e4f4",
  "kind": "yes/no",
  "text": "Bruno Lacerda: Greetings, sending file STAY-8029 about the residence day count over to the desk.\ndesk: Thank you, that is clear and appreciated.\n\nStay record STAY-8029 for Bruno Lacerda:\n- entry day Friday, 14 May 2027, exit day Thursday, 1 July 2027 (whole stay: 49 days)\nReference date: Sunday, 8 August 2027\nWindow checked: Thursday, 10 June 2027 to Sunday, 8 August 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 21 days inside every moving 60-day period. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Bruno Lacerda over the stay limit when days present inside the window ending on the reference date number more than the limit, under the stay rule?"
 },
 {
  "qid": "q839f437c4a",
  "kind": "choice",
  "text": "file: CASE-4762\nsent_by: Sara Ilves\nsubject: the appeal deadline\nteam: service desk\nnote: busy_queue\n\nCase CASE-4762, party Sara Ilves:\n- billing date: 21 Nov 2026\n- statement date: 28 Nov 2026",
  "question": "Filing rule: the dispute must be filed within 56 days after the later date out of these dates: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 56 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, by which final day must the dispute be filed to still count as in time?",
  "options": [
   "16 Jan 2027",
   "22 Jan 2027",
   "23 Jan 2027"
  ]
 },
 {
  "qid": "q6cee66aa40",
  "kind": "yes/no",
  "text": "Internal memo: the sender Malik Osei forwards file STAY-9931 about the visa stay count to the records clerk. Kindly add it to the desk log for handling, with thanks for your care.\n\nStay record STAY-9931 for Malik Osei:\n- entry day Monday, July 26, 2027, exit day Friday, September 3, 2027 (whole stay: 40 days)\n- entry day Friday, September 24, 2027, exit day Wednesday, October 13, 2027 (whole stay: twenty days)\nReference date: Monday, November 1, 2027\nWindow checked: Monday, July 5, 2027 to Monday, November 1, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 60 days in each 120-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Malik Osei over the stay limit, with more days present inside the window that ends on the reference date in file STAY-9931, under the stay rule?"
 },
 {
  "qid": "q9f15d7034c",
  "kind": "yes/no",
  "text": "Theo Kalnins: Hi, here is file CASE-3607 about the appeal deadline, with plenty of cheer.\ndesk: Lovely, thanks so much!\ndesk: That is fun to read.\n\nCase CASE-3607, party Theo Kalnins:\n- billing date: December 18, 2027\n- statement date: November 18, 2027\n- dispute filed on: January 18, 2028\n- days from the billing date to the filing: 31 days\n- days from the statement date to the filing: 61 days",
  "question": "Filing rule: the dispute must be filed within 28 days following the later of these dates: the billing date and the statement date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 28 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the dispute from Theo Kalnins in case CASE-3607 filed on or before the final day of the filing period?"
 },
 {
  "qid": "q068bdc2a53",
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
  "qid": "qb26e89155a",
  "kind": "choice",
  "text": "file: LED-1282\nsent_by: Jonas Feld\nsubject: the branch cash review\nteam: intake team\nchannel: routine_intake\n\nCash ledger LED-1282, teller Jonas Feld:\n- 2027-11-17: deposit of $3,775.00\n- 2027-11-19: withdrawal of $3,845.00\n- 2027-11-19: withdrawal of $2,340.00\n- 2027-11-19: deposit of $6,527.00\nDay under review: 2027-11-19",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is any total of $5,000.00 or greater, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals for 2027-11-19 in ledger LED-1282 call for a cash report?",
  "options": [
   "Only the deposit total",
   "Both totals",
   "Only the withdrawal total",
   "Neither total"
  ]
 },
 {
  "qid": "q36f8639e40",
  "kind": "yes/no",
  "text": "[chat] from=Freya Holm file=POL-9607 for=help_desk\n[chat] about=the cover question sent_with_love\n\nPolicy POL-9607, holder Freya Holm:\n- policy start date: 2027-02-09\n- burst pipe damage cover: part of the base policy\n- burst pipe damage loss on: 2027-04-27\n- days from the policy start date to the loss: 77 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days that starts on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs the burst pipe damage loss, under the cover rule, covered?"
 },
 {
  "qid": "qa5a361701a",
  "kind": "choice",
  "text": "Theo Kalnins sends file PO-3727 about the purchase request to the desk. This is the regular copy in the usual layout. The desk holds the full set in the standard format. Passing it along as the usual step.\n\nPurchase log PO-3727, kept by Theo Kalnins, vendor Vantmoor Electric:\n- earlier purchase on 18 Oct 2026: 2,463.00 USD\n- earlier purchase on 10 Nov 2026: 3,058.00 USD\n- earlier purchase on 15 Nov 2026: 909.00 USD\n- new request on 26 Nov 2026: 2,309.00 USD\nWindow checked: 28 Oct 2026 to 26 Nov 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is strictly greater than 10,000.00 USD, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what total does the purchase rule compare with its threshold for Theo Kalnins, including the new request?",
  "options": [
   "8,585.00 USD",
   "8,739.00 USD",
   "6,276.00 USD"
  ]
 }
]
