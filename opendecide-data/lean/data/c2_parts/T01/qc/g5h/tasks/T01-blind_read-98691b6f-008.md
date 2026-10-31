# G5-H blind read (all free-form rows) T01-blind_read-98691b6f-008 (family T01)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T01/qc/g5h/answers/T01-blind_read-98691b6f-008.json

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
  "qid": "qb495c9a97f",
  "kind": "choice",
  "text": "Bruno Lacerda has passed on file POL-5945 about the cover question to the desk. This memo goes with the file so it is on hand in the usual way. Thank you for your help.\n\nPolicy POL-5945, holder Bruno Lacerda:\n- policy start date: Saturday, 27 June 2026\n- theft cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days starting with the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn what earliest date would a loss of this kind be covered under policy POL-5945?",
  "options": [
   "Wednesday, 12 August 2026",
   "Tuesday, 11 August 2026",
   "Monday, 10 August 2026"
  ]
 },
 {
  "qid": "q77d38a82e0",
  "kind": "choice",
  "text": "Kofi Mensah: sending POL-9450 about the cover question, in a rush.\nservice desk: got it, thanks.\nservice desk: good work, cheers.\n\nPolicy POL-9450, holder Kofi Mensah:\n- policy start date: July 29, 2026\n- power surge damage cover: added by a rider effective October 28, 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of fourteen days that opens on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is fourteen days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on what earliest date would the power surge damage loss be covered?",
  "options": [
   "November 12, 2026",
   "November 11, 2026",
   "August 13, 2026",
   "November 10, 2026"
  ]
 },
 {
  "qid": "q5282db71b0",
  "kind": "yes/no",
  "text": "Maya Lindgren: Hey, sending case file NTC-4476 about the response deadline, hope it brightens the room.\ndesk: That is a lovely note, thanks!\ndesk: Good fun, I enjoyed reading it.\n\nNotice NTC-4476 to Maya Lindgren:\n- response due date: Saturday, July 26, 2025\n- office cutoff on the due date: 26 July 2025, 22:14 (UTC-04:00)\n- response sent: 2025-07-25T14:27:00Z [same instant in office time: 25 July 2025, 10:27 (UTC-04:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response from Maya Lindgren on time under the receipt rule?"
 },
 {
  "qid": "qd12cc986e7",
  "kind": "yes/no",
  "text": "Ines Duarte: Busy, but here is PO-5018 about the purchase request.\nhelp desk: Received, thanks.\n\nPurchase log PO-5018, kept by Ines Duarte, vendor Brightwell Supply:\n- earlier purchase on Sunday, November 2, 2025: 831.00 USD\n- earlier purchase on Thursday, November 13, 2025: 968.00 USD\n- earlier purchase on Sunday, November 16, 2025: 512.00 USD\n- earlier purchase on Monday, December 1, 2025: 267.00 USD\n- new request on Sunday, January 4, 2026: 1,974.00 USD\nWindow checked: Thursday, November 6, 2025 to Sunday, January 4, 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is strictly more than 3,000.00 USD, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does request PO-5018 from Ines Duarte need written quotes under the purchase rule?"
 },
 {
  "qid": "q7c09bc405a",
  "kind": "yes/no",
  "text": "From: Bruno Lacerda\nFile: PO-1339\nSent to: review team\nThe file about the purchase request is shared as usual.\n\nPurchase log PO-1339, kept by Bruno Lacerda, vendor Brightwell Supply:\n- earlier purchase on 9 Sep 2025: 7,851.00 USD\n- earlier purchase on 4 Oct 2025: 6,745.00 USD\n- earlier purchase on 1 Nov 2025: 7,775.00 USD\n- new request on 7 Dec 2025: 2,629.00 USD\nWindow checked: 9 Sep 2025 to 7 Dec 2025, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is any total greater than 25,000.00 USD, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does the purchase request in log PO-1339 need written quotes under the purchase rule?"
 },
 {
  "qid": "q24a1896b55",
  "kind": "yes/no",
  "text": "Hana Sato: Routine send, NTC-6326 about the notice response.\ncase team: Thanks, received.\n\nNotice NTC-6326 to Hana Sato:\n- response due date: 2027-12-13\n- office cutoff on the due date: 13 December 2027, 16:44 (UTC+03:00)\n- response sent: 13 December 2027, 22:44 (UTC+09:00) [same instant in office time: 13 December 2027, 16:44 (UTC+03:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWas the response to notice NTC-6326 on time under the receipt rule?"
 },
 {
  "qid": "q4cac13c280",
  "kind": "choice",
  "text": "Dear front desk,\nMira Castell is writing to share file STAY-4433 about the residence day count with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,\n\nStay record STAY-4433 for Mira Castell:\n- entry day June 25, 2027, exit day July 13, 2027 (whole stay: 19 days)\n- entry day August 7, 2027, exit day August 10, 2027 (whole stay: 4 days)\nReference date: September 4, 2027\nWindow checked: July 7, 2027 to September 4, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 21 days during any 60-day window that moves ahead. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, how many days present fall inside the checked window that ends on September 4, 2027 for file STAY-4433?",
  "options": [
   "23 days",
   "11 days"
  ]
 },
 {
  "qid": "q466229ad8b",
  "kind": "yes/no",
  "text": "Hey there, quick heads up that Kofi Mensah has sent file NTC-2210 about the response deadline to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.\n\nNotice NTC-2210 to Kofi Mensah:\n- response due date: Monday, 22 June 2026\n- office cutoff on the due date: 22 June 2026, 19:43 (UTC-05:00)\n- response sent: 23 June 2026, 09:39 (UTC+09:00) [same instant in office time: 22 June 2026, 19:39 (UTC-05:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the response to notice NTC-2210 on time under the receipt rule?"
 },
 {
  "qid": "q71d732998f",
  "kind": "choice",
  "text": "Dear front desk,\nMalik Osei is writing to share file POL-2484 about the loss claim with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,\n\nPolicy POL-2484, holder Malik Osei:\n- policy start date: 2027-07-14\n- fire damage cover: added by a rider effective 2027-10-02",
  "question": "Cover rule: a loss is covered only after a waiting period of 10 days that runs from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 10 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the earliest date on which this fire damage loss for Malik Osei would be covered?",
  "options": [
   "2027-10-15",
   "2027-10-16",
   "2027-10-13"
  ]
 },
 {
  "qid": "qc969f443e9",
  "kind": "yes/no",
  "text": "Ana Ruiz: Hello, I am sending file STAY-2797 about the visa stay count. My thanks in advance.\nintake team: Thank you, this has been received with care.\n\nStay record STAY-2797 for Ana Ruiz:\n- entry day Friday, July 31, 2026, exit day Saturday, August 1, 2026 (whole stay: 2 days)\n- entry day Wednesday, August 26, 2026, exit day Saturday, October 10, 2026 (whole stay: 46 days)\nReference date: Saturday, December 5, 2026\nWindow checked: Monday, September 7, 2026 to Saturday, December 5, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 30 days within any 90-day window that keeps moving. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Ana Ruiz inside the stay limit when, under the stay rule, the days present in the window ending on Saturday, December 5, 2026 number at most the limit?"
 },
 {
  "qid": "q07a2e26149",
  "kind": "yes/no",
  "text": "Maya Lindgren sends file STAY-7224 about the visa stay count to the admin team. Sending this across quickly because I am tied up with other work. The full file is attached for the team. Thanks for taking it.\n\nStay record STAY-7224 for Maya Lindgren:\n- entry day 3 Oct 2026, exit day 31 Oct 2026 (whole stay: 29 days)\n- entry day 22 Nov 2026, exit day 9 Dec 2026 (whole stay: eighteen days)\n- entry day 31 Dec 2026, exit day 12 Jan 2027 (whole stay: thirteen days)\nReference date: 27 Jan 2027\nWindow checked: 30 Oct 2026 to 27 Jan 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 30 days inside every 90-day stretch that moves along. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Maya Lindgren, under the stay rule, over the stay limit for the window ending on 27 Jan 2027?"
 },
 {
  "qid": "qf71237937d",
  "kind": "choice",
  "text": "Hi admin team, Aiko Brandt here with file LED-1198 about the cash ledger check. Thanks so much for helping keep everything tidy. It is a pleasure to share it with you all.\n\nCash ledger LED-1198, teller Aiko Brandt:\n- 2028-02-04: withdrawal of 3,627.00 USD\n- 2028-02-04: withdrawal of 6,242.00 USD\n- 2028-02-06: deposit of 3,640.00 USD\n- 2028-02-06: withdrawal of 3,952.00 USD\n- 2028-02-06: deposit of 2,489.00 USD\n- 2028-02-06: withdrawal of 11,048.00 USD\nDay under review: 2028-02-06",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is strictly more than 15,000.00 USD, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals in ledger LED-1198 for 2028-02-06 call for a cash report under the cash rule?",
  "options": [
   "Only the withdrawal total",
   "Both totals",
   "Neither total",
   "Only the deposit total"
  ]
 },
 {
  "qid": "q9b05cd5048",
  "kind": "yes/no",
  "text": "Dear front desk,\nSara Ilves is sending file STAY-5241 about the residence day count. The file is attached here for your records. I appreciate the help with it.\nKind regards,\n\nStay record STAY-5241 for Sara Ilves:\n- entry day July 4, 2027, exit day July 15, 2027 (whole stay: 12 days)\n- entry day August 5, 2027, exit day September 13, 2027 (whole stay: 40 days)\n- entry day September 30, 2027, exit day October 18, 2027 (whole stay: 19 days)\nReference date: November 15, 2027\nWindow checked: August 18, 2027 to November 15, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 45 days inside every 90-day stretch that moves along. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does file STAY-5241 show more days present in the checked window ending on the reference date than the limit?"
 },
 {
  "qid": "q823d6df928",
  "kind": "yes/no",
  "text": "Lucas Brenner: Hello, I am sending file NTC-6208 about the response deadline to the case team, with thanks.\nteam: Thank you for the careful note.\nteam: Your gesture is warmly felt.\n\nNotice NTC-6208 to Lucas Brenner:\n- response due date: February 8, 2026\n- office cutoff on the due date: 2026-02-08T21:01:00-04:00\n- response sent: 2026-02-09T04:01:00+03:00 [same instant in office time: 2026-02-08T21:01:00-04:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Lucas Brenner received on time under the receipt rule?"
 },
 {
  "qid": "qdd806b7863",
  "kind": "yes/no",
  "text": "Felix Ortega: file POL-9693 about the insurance claim is here.\nintake team: received, thanks.\nintake team: that is everything for this file.\n\nPolicy POL-9693, holder Felix Ortega:\n- policy start date: 2026-10-11\n- glass breakage cover: part of the base policy\n- glass breakage loss on: 2026-10-14\n- days from the policy start date to the loss: 3 days",
  "question": "Cover rule: a loss is covered only after a waiting period of 14 days in which counting begins the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 14 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWould policy POL-9693 cover this glass breakage loss under the cover rule?"
 },
 {
  "qid": "qf22f4eb974",
  "kind": "yes/no",
  "text": "Aiko Brandt: Hey, sending case file STAY-1506 about the visa stay count, hope it brightens the room.\ndesk: That is a lovely note, thanks!\ndesk: Good fun, I enjoyed reading it.\n\nStay record STAY-1506 for Aiko Brandt:\n- entry day September 5, 2025, exit day October 11, 2025 (whole stay: 37 days)\n- entry day October 31, 2025, exit day October 31, 2025 (whole stay: one day)\nReference date: November 20, 2025\nWindow checked: August 23, 2025 to November 20, 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 30 days inside every 90-day stretch that moves along. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does Aiko Brandt have more days present in the checked window ending on November 20, 2025 than the stay limit?"
 },
 {
  "qid": "qbf9da554be",
  "kind": "yes/no",
  "text": "Hey there, quick heads up that Sara Ilves has sent file STAY-8062 about the border stay check to the admin team. Hope everyone is doing well! The file is all tidy and in good shape, so it is easy to pick up. Thanks a lot for keeping things moving along.\n\nStay record STAY-8062 for Sara Ilves:\n- entry day Monday, February 1, 2027, exit day Sunday, March 21, 2027 (whole stay: 49 days)\n- entry day Thursday, April 8, 2027, exit day Friday, April 16, 2027 (whole stay: 9 days)\nReference date: Friday, May 14, 2027\nWindow checked: Sunday, February 14, 2027 to Friday, May 14, 2027, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 45 days in each 90-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 45 days, and within the limit if it is 45 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nIs Sara Ilves over the stay limit, counting the days present inside the window that ends on Friday, May 14, 2027?"
 },
 {
  "qid": "q1c8f8ea34f",
  "kind": "choice",
  "text": "Felix Ortega: hey, here is LED-6004 about the branch cash review, sorry for the wait!\nservice desk: all good, got it.\nservice desk: brilliant, thanks a lot.\n\nCash ledger LED-6004, teller Felix Ortega:\n- Sunday, 23 May 2027: deposit of $2,878\n- Sunday, 23 May 2027: deposit of $3,602\n- Sunday, 23 May 2027: withdrawal of $3,331\n- Sunday, 23 May 2027: withdrawal of $1,669\n- Tuesday, 25 May 2027: deposit of $2,555\nDay under review: Sunday, 23 May 2027",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is a figure greater than $5,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, which of the day's totals for Sunday, 23 May 2027 call for a cash report?",
  "options": [
   "Only the withdrawal total",
   "Only the deposit total",
   "Neither total",
   "Both totals"
  ]
 },
 {
  "qid": "q8341760622",
  "kind": "yes/no",
  "text": "Eva Marsh: Hiya! Sending PO-4668 about the purchase request, all good here.\nservice desk: Lovely, thanks for the heads up!\n\nPurchase log PO-4668, kept by Eva Marsh, vendor Corvane Office:\n- earlier purchase on 27 Jun 2027: $5,788\n- earlier purchase on 26 Jul 2027: $3,002\n- new request on 5 Aug 2027: $5,009\nWindow checked: 8 May 2027 to 5 Aug 2027, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is $10,000 as a floor, greater than that counts, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, does the purchase request in log PO-4668 need written quotes under the purchase rule?"
 },
 {
  "qid": "qb3c4901dbc",
  "kind": "choice",
  "text": "Aiko Brandt: I am sending file NTC-9805 about the response deadline, with thanks.\nintake team: thank you, received.\nintake team: kind regards.\n\nNotice NTC-9805 to Aiko Brandt:\n- notice date: Tuesday, 1 August 2028\n- sent by: email\n- 20 days after the notice date, before any postal add-on or closure: Monday, 21 August 2028\nOffice closures: Monday, 21 August 2028.",
  "question": "Response rule: a response is due 20 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 3 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, on which date is the response to notice NTC-9805 due under the response rule?",
  "options": [
   "Thursday, 24 August 2028",
   "Saturday, 19 August 2028",
   "Tuesday, 22 August 2028"
  ]
 },
 {
  "qid": "qcceef4d74e",
  "kind": "choice",
  "text": "Sent by: Freya Holm\nFile: POL-2993\nSent to: review team\nThis is a standard note about the loss claim. The file is laid out as usual.\n\nPolicy POL-2993, holder Freya Holm:\n- policy start date: 22 February 2026\n- burst pipe damage cover: added by a rider effective 1 July 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days whose clock starts running on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what is the earliest date on which the burst pipe damage loss for Freya Holm would be covered?",
  "options": [
   "3 August 2026",
   "1 August 2026",
   "2 August 2026"
  ]
 },
 {
  "qid": "q5c9c6c29d1",
  "kind": "choice",
  "text": "Yara Haddad: file CASE-4276 about the claim deadline question is here.\nintake team: received, thanks.\nintake team: that is everything for this file.\n\nCase CASE-4276, party Yara Haddad:\n- invoice date: Sunday, 25 January 2026\n- goods received date: Friday, 30 January 2026",
  "question": "Filing rule: the claim must be filed within 33 days starting from the later of the dates listed below: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 33 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the latest date by which the claim can be filed in time?",
  "options": [
   "Wednesday, 18 March 2026",
   "Wednesday, 4 March 2026",
   "Friday, 6 March 2026",
   "Thursday, 5 March 2026"
  ]
 },
 {
  "qid": "q892a8ded81",
  "kind": "choice",
  "text": "Dear duty clerk,\nDana Okafor is sending file POL-8252 about the insurance claim. It is attached here. Hope your work goes well.\nCheers,\n\nPolicy POL-8252, holder Dana Okafor:\n- policy start date: 29 November 2027\n- burst pipe damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days that begins on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which the burst pipe damage loss in policy POL-8252 would be covered under the cover rule?",
  "options": [
   "12 January 2028",
   "14 January 2028",
   "13 January 2028"
  ]
 },
 {
  "qid": "q5b81a23e5e",
  "kind": "yes/no",
  "text": "Jonas Feld: Hello, I am sending file NTC-2028 about the reply timing question to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nNotice NTC-2028 to Jonas Feld:\n- response due date: 2027-09-05\n- office cutoff on the due date: 5 September 2027, 22:57 (UTC+09:00)\n- response sent: 6 September 2027, 02:44 (UTC+03:00) [same instant in office time: 6 September 2027, 08:44 (UTC+09:00)]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Jonas Feld received on time under the receipt rule?"
 },
 {
  "qid": "q87dd7a5e13",
  "kind": "choice",
  "text": "Dear duty clerk,\nQuick send from Omar Saleh: file LED-1068 about the cash ledger check is in. Sending it over fast as I am on the move. The attachment is full and whole. Thanks a bunch.\nKind regards\n\nCash ledger LED-1068, teller Omar Saleh:\n- Friday, August 11, 2028: deposit of $2,251\n- Friday, August 11, 2028: withdrawal of $3,291\n- Friday, August 11, 2028: deposit of $1,402\n- Friday, August 11, 2028: withdrawal of $821\n- Saturday, August 12, 2028: withdrawal of $7,898\nDay under review: Friday, August 11, 2028",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is at or above $10,000, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, which of the day's totals recorded by Omar Saleh for Friday, August 11, 2028 call for a cash report?",
  "options": [
   "Only the deposit total",
   "Neither total",
   "Only the withdrawal total",
   "Both totals"
  ]
 },
 {
  "qid": "q6d893b44f0",
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
  "qid": "qec29b8ecd0",
  "kind": "choice",
  "text": "Sent by: Dana Okafor\nFile: CASE-4236\nSent to: records clerk\nShort note, my queue is packed. The file is about the appeal deadline and is attached.\n\nCase CASE-4236, party Dana Okafor:\n- decision date: 16 Oct 2026\n- delivery date: 18 Oct 2026",
  "question": "Filing rule: the appeal must be filed within twelve days after the later date out of these dates: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is twelve days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, what is the latest day on which Dana Okafor may still file the appeal in time?",
  "options": [
   "1 Nov 2026",
   "3 Nov 2026",
   "30 Oct 2026"
  ]
 },
 {
  "qid": "qd850a2248b",
  "kind": "choice",
  "text": "Dear duty clerk,\nMaya Lindgren is sending file STAY-7013 about the border stay check. It is attached here. Hope your work goes well.\nCheers,\n\nStay record STAY-7013 for Maya Lindgren:\n- entry day 24 June 2025, exit day 6 August 2025 (whole stay: 44 days)\n- entry day 3 September 2025, exit day 23 September 2025 (whole stay: 21 days)\nReference date: 21 October 2025\nWindow checked: 24 July 2025 to 21 October 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 30 days during any 90-day window that moves ahead. Day counts are calendar days, and entry and exit days both count as days present. Only one 90-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 30 days, and within the limit if it is 30 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, how many days present for file STAY-7013 fall inside the checked window that ends on the reference date?",
  "options": [
   "35 days",
   "37 days",
   "36 days"
  ]
 },
 {
  "qid": "qe26928d271",
  "kind": "choice",
  "text": "Hi duty clerk,\nDana Okafor is sending file STAY-2382 about the visa stay count, with the main points at the top. Quick note, I am buried under other work.\nBest,\n\nStay record STAY-2382 for Dana Okafor:\n- entry day 16 Aug 2025, exit day 29 Aug 2025 (whole stay: 14 days)\n- entry day 10 Sep 2025, exit day 9 Oct 2025 (whole stay: 30 days)\nReference date: 15 Nov 2025\nWindow checked: 17 Sep 2025 to 15 Nov 2025, both included.",
  "question": "Stay rule: the person named in the record may be present on a maximum of 21 days in each 60-day window that rolls forward. Day counts are calendar days, and entry and exit days both count as days present. Only one 60-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 21 days, and within the limit if it is 21 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nHow many days, under the stay rule, was Dana Okafor present inside the checked window ending on 15 Nov 2025?",
  "options": [
   "23 days",
   "22 days"
  ]
 },
 {
  "qid": "qca51a719c3",
  "kind": "yes/no",
  "text": "Dear front desk,\nTomas Lindqvist is sending file CASE-2258 about the appeal deadline. The file is attached here for your records. I appreciate the help with it.\nKind regards,\n\nCase CASE-2258, party Tomas Lindqvist:\n- decision date: 12 Aug 2027\n- delivery date: 7 Aug 2027\n- appeal filed on: 31 Aug 2027\n- days from the decision date to the filing: 19 days\n- days from the delivery date to the filing: 24 days",
  "question": "Filing rule: the appeal must be filed within 10 days past the later of the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 10 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDid Tomas Lindqvist, under the filing rule, fail to file the appeal in time?"
 },
 {
  "qid": "qd44c70ac6f",
  "kind": "choice",
  "text": "Theo Kalnins: file POL-5186 about the insurance claim is attached here.\ncase team: thank you, that is received.\ncase team: kind regards.\n\nPolicy POL-5186, holder Theo Kalnins:\n- policy start date: Sunday, December 12, 2027\n- glass breakage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 93 days that picks up on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 93 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, on what earliest date would the glass breakage loss be covered?",
  "options": [
   "Thursday, March 16, 2028",
   "Tuesday, March 14, 2028",
   "Wednesday, March 15, 2028"
  ]
 },
 {
  "qid": "qac18072261",
  "kind": "yes/no",
  "text": "Mira Castell: Busy, but here is POL-6663 about the cover question.\nhelp desk: Received, thanks.\n\nPolicy POL-6663, holder Mira Castell:\n- policy start date: Thursday, 8 July 2027\n- fire damage cover: added by a rider effective Friday, 3 December 2027\n- fire damage loss on: Friday, 10 December 2027\n- days from the policy start date to the loss: 155 days\n- days from the rider effective date to the loss: seven days",
  "question": "Cover rule: a loss is covered only after a waiting period of 45 days with the start date itself left out, beginning the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 45 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, did the fire damage loss for Mira Castell happen during the waiting period?"
 },
 {
  "qid": "q413c7beb5e",
  "kind": "choice",
  "text": "Bruno Lacerda: file LED-6523 about the cash ledger check is attached.\ncase team: received, thanks.\ncase team: that is the whole file.\n\nCash ledger LED-6523, teller Bruno Lacerda:\n- January 20, 2026: deposit of 1,132.00 USD\n- January 22, 2026: deposit of 1,237.00 USD\n- January 22, 2026: withdrawal of 5,000.00 USD\n- January 22, 2026: deposit of 5,791.00 USD\n- January 23, 2026: withdrawal of 1,925.00 USD\nDay under review: January 22, 2026",
  "question": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never net one against the other, and never mix days. A cash report is required for a day if its deposit total or its withdrawal total is a figure of 5,000.00 USD or greater, and not otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhich of the day's totals on January 22, 2026 in ledger LED-6523, under the cash rule, call for a cash report?",
  "options": [
   "Only the deposit total",
   "Both totals",
   "Neither total",
   "Only the withdrawal total"
  ]
 },
 {
  "qid": "qe3a0d853ec",
  "kind": "choice",
  "text": "Iris Vance sends file POL-9862 about the cover question to the desk. This is the regular version, laid out in the standard format. The desk has the full set on hand. Passing it along as usual.\n\nPolicy POL-9862, holder Iris Vance:\n- policy start date: 19 August 2026\n- fire damage cover: added by a rider effective 20 September 2026",
  "question": "Cover rule: a loss is covered only after a waiting period of 65 days starting with the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 65 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which, under the cover rule, the fire damage loss in policy POL-9862 would be covered?",
  "options": [
   "24 October 2026",
   "19 December 2026",
   "25 November 2026",
   "24 November 2026"
  ]
 },
 {
  "qid": "qbf40c0473b",
  "kind": "choice",
  "text": "Dear front desk,\nDana Okafor is writing to share file NTC-2057 about the reply deadline with your team. The file is set out in full for your use. I am grateful for your attention to this matter.\nYours sincerely,\n\nNotice NTC-2057 to Dana Okafor:\n- notice date: 28 August 2028\n- sent by: hand delivery\n- 21 days after the notice date, before any postal add-on or closure: 18 September 2028\nOffice closures: 9 September 2028; 18 September 2028; 20 September 2028.",
  "question": "Response rule: a response is due 21 days after the notice date, counted in calendar days with the notice date as day zero. If the notice was sent by post, add 2 days to that date. The date this gives is the day reached. If the day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise the day reached is the due date. The office is open on every day except the listed closures. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, which date is the deadline for the response from Dana Okafor to the notice?",
  "options": [
   "16 September 2028",
   "19 September 2028",
   "21 September 2028"
  ]
 },
 {
  "qid": "q7037dd0854",
  "kind": "choice",
  "text": "Iris Vance: Sending POL-8085 about the cover question, routine as usual.\nintake team: Thanks, received.\n\nPolicy POL-8085, holder Iris Vance:\n- policy start date: November 3, 2026\n- storm damage cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 21 days commencing on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 21 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which a loss of this kind would count as covered for policy POL-8085 under the cover rule?",
  "options": [
   "November 23, 2026",
   "November 25, 2026",
   "November 26, 2026"
  ]
 },
 {
  "qid": "q80074b2b43",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nHana Sato is sending file NTC-2583 about the notice response, with the main points at the top. Quick note, I am buried under other work.\nBest,\n\nNotice NTC-2583 to Hana Sato:\n- response due date: 14 April 2026\n- office cutoff on the due date: 2026-04-14 18:25:00 +0300\n- response sent: 2026-04-14 16:24:00 +0100 [same instant in office time: 2026-04-14 18:24:00 +0300]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, was the response from Hana Sato to notice NTC-2583 on time under the receipt rule?"
 },
 {
  "qid": "q1fac25c404",
  "kind": "yes/no",
  "text": "Hi admin team, this is Sara Ilves sharing file CASE-5005 about the complaint filing. It was a pleasure to pull it together. Thanks for keeping an eye on it.\n\nCase CASE-5005, party Sara Ilves:\n- incident date: July 1, 2025\n- discovery date: June 17, 2025\n- complaint filed on: July 11, 2025\n- days from the incident date to the filing: 10 days\n- days from the discovery date to the filing: 24 days",
  "question": "Filing rule: the complaint must be filed within 21 days measured beyond the later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, did Sara Ilves fail to file the complaint by the deadline?"
 },
 {
  "qid": "qbab60d33de",
  "kind": "yes/no",
  "text": "Ana Ruiz: file CASE-6831 about the complaint filing is with you.\nintake team: thanks, that is received.\nintake team: all pages are in, thanks.\n\nCase CASE-6831, party Ana Ruiz:\n- incident date: Tuesday, 14 September 2027\n- discovery date: Sunday, 29 August 2027\n- complaint filed on: Monday, 20 September 2027\n- days from the incident date to the filing: 6 days\n- days from the discovery date to the filing: 22 days",
  "question": "Filing rule: the complaint must be filed within 5 days from whichever is later of these dates: the incident date and the discovery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 5 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, was the complaint filed on or before the final day of the filing period?"
 },
 {
  "qid": "qecbdf35129",
  "kind": "choice",
  "text": "Aiko Brandt: Hello, I am sending file NTC-4941 about the notice response to the intake team, with thanks.\nintake: Thank you very much for your message.\nteam: Your kindness is appreciated.\n\nNotice NTC-4941 to Aiko Brandt:\n- response due date: 26 October 2025\n- office cutoff on the due date: 2025-10-26T22:52:00+02:00\n- response sent: 2025-10-25T04:49:00+08:00 [same instant in office time: 2025-10-24T22:49:00+02:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nOn which date, under the receipt rule, does the office count the response from Aiko Brandt to notice NTC-4941 as received?",
  "options": [
   "October 24, 2025",
   "October 25, 2025"
  ]
 },
 {
  "qid": "q64896e6a93",
  "kind": "choice",
  "text": "Hi front desk,\nJonas Feld sends file STAY-5212 about the visa stay count as a standard copy. The file keeps to the usual format.\nRegards,\n\nStay record STAY-5212 for Jonas Feld:\n- entry day Saturday, February 28, 2026, exit day Thursday, April 2, 2026 (whole stay: 34 days)\n- entry day Monday, April 20, 2026, exit day Monday, April 27, 2026 (whole stay: eight days)\n- entry day Monday, May 25, 2026, exit day Tuesday, June 16, 2026 (whole stay: 23 days)\nReference date: Saturday, July 4, 2026\nWindow checked: Saturday, March 7, 2026 to Saturday, July 4, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on up to 60 days in every 120-day run that moves forward through time. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, how many days present for Jonas Feld fall inside the checked window that ends on the reference date?",
  "options": [
   "58 days",
   "61 days",
   "31 days"
  ]
 },
 {
  "qid": "q3c05f02596",
  "kind": "yes/no",
  "text": "Sent by: Clara Weiss\nFile: STAY-1237\nSent to: review team\nThe file is a routine copy about the residence day count. It follows the standard layout used by the team.\n\nStay record STAY-1237 for Clara Weiss:\n- entry day September 24, 2025, exit day October 9, 2025 (whole stay: 16 days)\n- entry day October 28, 2025, exit day December 11, 2025 (whole stay: 45 days)\nReference date: January 6, 2026\nWindow checked: September 9, 2025 to January 6, 2026, both included.",
  "question": "Stay rule: the person named in the record may be present on at most 60 days inside every 120-day stretch that moves along. Day counts are calendar days, and entry and exit days both count as days present. Only one 120-day window is checked: the one that ends on the reference date, both ends included; its first day is printed with the record. The person is over the limit if the number of days present inside that window is more than 60 days, and within the limit if it is 60 days or fewer. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, does file STAY-1237 show more days present in the checked window ending on the reference date than the limit?"
 },
 {
  "qid": "q4de178886f",
  "kind": "choice",
  "text": "Felix Ortega: Hey there! Sending file NTC-2874 about the notice response your way, hope it helps lol.\nservice: Thanks so much, that is great.\ndesk: Awesome, we have it on screen.\n\nNotice NTC-2874 to Felix Ortega:\n- response due date: 3 Jun 2026\n- office cutoff on the due date: 2026-06-03T12:17:00+03:00\n- response sent: 2026-06-03T07:56:00+02:00 [same instant in office time: 2026-06-03T08:56:00+03:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, on what date does the office count the response to notice NTC-2874 as received under the receipt rule?",
  "options": [
   "June 3, 2026",
   "June 2, 2026"
  ]
 },
 {
  "qid": "q65921062b2",
  "kind": "choice",
  "text": "Yara Haddad: hey, here is CASE-1732 about the appeal deadline, sorry for the wait!\nservice desk: all good, got it.\nservice desk: brilliant, thanks a lot.\n\nCase CASE-1732, party Yara Haddad:\n- decision date: Monday, 6 March 2028\n- delivery date: Friday, 25 February 2028",
  "question": "Filing rule: the appeal must be filed within 56 days measured from the later of the dates below: the decision date and the delivery date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 56 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUntil which date, under the filing rule, may Yara Haddad file the appeal in time?",
  "options": [
   "Wednesday, 3 May 2028",
   "Saturday, 29 April 2028",
   "Monday, 1 May 2028"
  ]
 },
 {
  "qid": "qebeac24e1b",
  "kind": "choice",
  "text": "Omar Saleh: hey, here is POL-3378 about the cover question, sorry for the wait!\nservice desk: all good, got it.\nservice desk: brilliant, thanks a lot.\n\nPolicy POL-3378, holder Omar Saleh:\n- policy start date: Friday, 25 June 2027\n- theft cover: added by a rider effective Monday, 22 November 2027",
  "question": "Cover rule: a loss is covered only after a waiting period of 15 days counted from the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 15 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nWhat is the earliest date on which the theft loss in policy POL-3378 would be covered under the cover rule?",
  "options": [
   "Tuesday, 7 December 2027",
   "Monday, 6 December 2027",
   "Wednesday, 8 December 2027",
   "Sunday, 11 July 2027"
  ]
 },
 {
  "qid": "q783f161940",
  "kind": "yes/no",
  "text": "Clara Weiss: Hey, sending CASE-9311 about the claim deadline question, hope all is well!\nhelp desk: Lovely, thanks for sending it across.\n\nCase CASE-9311, party Clara Weiss:\n- invoice date: 2026-03-01\n- goods received date: 2026-03-03\n- claim filed on: 2026-03-25\n- days from the invoice date to the filing: 24 days\n- days from the goods received date to the filing: 22 days",
  "question": "Filing rule: the claim must be filed within 21 days reckoned after the later of these dates: the invoice date and the goods received date. Day zero is the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the period is 21 days after day zero. A filing made on any day up to and including that final day is in time; a filing after it is late. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nAccording to the rule card, did the person fail to file the claim in time?"
 },
 {
  "qid": "qfd63f90dd9",
  "kind": "yes/no",
  "text": "Hi duty clerk,\nHana Sato is sending file PO-8837 about the purchase request. Writing fast, I am swamped. Attached is the file.\nThanks,\n\nPurchase log PO-8837, kept by Hana Sato, vendor Corvane Office:\n- earlier purchase on 2025-08-19: $481\n- earlier purchase on 2025-09-21: $2,461\n- new request on 2025-12-19: $540\nWindow checked: 2025-09-21 to 2025-12-19, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 90-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is strictly more than $3,000, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nDoes the purchase request made by Hana Sato need written quotes under the purchase rule?"
 },
 {
  "qid": "qacb1dcac01",
  "kind": "yes/no",
  "text": "Tomas Lindqvist: Routine send, NTC-3682 about the reply timing question.\nintake team: Received, thank you.\n\nNotice NTC-3682 to Tomas Lindqvist:\n- response due date: 12 September 2028\n- office cutoff on the due date: 2028-09-12T22:26:00+09:00\n- response sent: 2028-09-12T00:17:00-05:00 [same instant in office time: 2028-09-12T14:17:00+09:00]",
  "question": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on or before the due date, and late otherwise. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, was the response to notice NTC-3682 on time under the receipt rule?"
 },
 {
  "qid": "q53ba3948a3",
  "kind": "yes/no",
  "text": "Lucas Brenner sends file PO-4523 about the supplier order to the desk. With thanks for your attention, the material is laid out with care. Respectfully yours.\n\nPurchase log PO-4523, kept by Lucas Brenner, vendor Ostrava Parts:\n- earlier purchase on January 19, 2026: $432\n- earlier purchase on April 12, 2026: $2,792\n- new request on June 10, 2026: $658\nWindow checked: April 12, 2026 to June 10, 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 60-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is $3,000 itself excluded, only more than that counts, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nUnder the card's rule, is it true that written quotes are not needed for the request from Lucas Brenner in log PO-4523?"
 },
 {
  "qid": "qacfadd5690",
  "kind": "choice",
  "text": "Iris Vance: I am sending file POL-9430 about the loss claim, with thanks.\nintake team: thank you, received.\nintake team: kind regards.\n\nPolicy POL-9430, holder Iris Vance:\n- policy start date: 2027-01-29\n- subsidence cover: part of the base policy",
  "question": "Cover rule: a loss is covered only after a waiting period of 30 days whose first counted day falls on the day after its start date. That start date is the policy start date or, for a peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is 30 days after the start date. A loss that happens after that final day is covered; a loss on or before it is not. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nBased on the card and the record, what is the earliest date on which this subsidence loss for Iris Vance would be covered?",
  "options": [
   "2027-02-28",
   "2027-02-27",
   "2027-03-01"
  ]
 }
]
