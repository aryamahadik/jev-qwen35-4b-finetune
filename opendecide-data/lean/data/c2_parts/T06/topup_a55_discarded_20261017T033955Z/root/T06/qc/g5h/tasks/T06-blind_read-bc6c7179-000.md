# G5-H blind read (all free-form rows) T06-blind_read-bc6c7179-000 (family T06)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T06/topup_a55/root/T06/qc/g5h/answers/T06-blind_read-bc6c7179-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 16. Answers expected: 16 (one per item, each with that item's qid).

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
  "qid": "q173d98eec8",
  "kind": "choice",
  "text": "Dear Kettlecrumb Bakehouse team,\nI am writing to send the fountain pen back to you. I bought it online on your website.\nYours sincerely, Ravi Subramanian\n\nOrder record ORD-58839 from Kettlecrumb Bakehouse:\n- item: fountain pen\n- type of goods: standard goods\n- handover: delivered to a parcel locker and collected by the buyer later\n- ordered on (the purchase date): Monday, October 25, 2027\n- delivered on: Friday, October 29, 2027\n- buyer took possession on: Sunday, October 31, 2027\n- return requested on: Tuesday, November 16, 2027\n- reason for the return: change of mind\n- days from the purchase date to the request: 22 days\n- days from delivery to the request: 18 days\n- days from possession to the request: 16 days\n\nKettlecrumb Bakehouse posted this notice at its checkout and on its website: \"We give a full refund on any item returned for any reason, within 30 days of the delivery date.\"",
  "question": "Consumer Sales Act of Orlevia (excerpt)\nSection I (counting days). A right is used on the day the buyer asks for it. A period in this Act or in a store notice runs in calendar days from an event: the event's day is day zero, the next day is day one, and the period includes its last day.\nSection II (faulty goods). A buyer may reject faulty goods and get a full refund within 30 days from the delivery date.\nSection III (withdrawal). A buyer may withdraw from a purchase for any reason and get a full refund within 10 days from the day the buyer took possession of the goods. Section III does not cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions do not limit Section II.\nSection IV (store notices). A store notice cannot remove or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nIn this case, on which day does the period of the right the law gives the customer to withdraw for any reason end?",
  "options": [
   "Wednesday, November 10, 2027",
   "Thursday, November 4, 2027",
   "Tuesday, November 9, 2027"
  ]
 },
 {
  "qid": "qc107e22902",
  "kind": "yes/no",
  "text": "Ferrowby Cheese House posted this notice at its checkout and on its website: \"Change of mind: full refund within 5 days of purchase.\"\n\nDev Chaudhary: Greetings. I bought the study planner online on the Ferrowby Cheese House website and I wish to send it back. Kindly assist me with the return.\n\nOrder record ORD-66798 from Ferrowby Cheese House:\n- item: study planner\n- type of goods: standard goods\n- handover: handed to the buyer at delivery\n- ordered on (the purchase date): 2028-02-14\n- delivered on: 2028-02-18\n- buyer took possession on: 2028-02-18\n- return requested on: 2028-03-03\n- reason for the return: change of mind\n- days from the purchase date to the request: 18 days\n- days from delivery to the request: 14 days\n- days from possession to the request: 14 days",
  "question": "In this case, is it true that no full refund is due to the customer?",
  "definitions": "Civil Code of Brevonia, consumer sales, Article K (extract)\n(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, the next day is day one, and the final day of the limit still counts.\n(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts 21 days, counted from the date of delivery.\n(c) A buyer may withdraw from a purchase for any reason and be refunded in full; this right lasts 14 days, counted from the date the buyer took possession of the goods.\n(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case."
 },
 {
  "qid": "q5e082b1c20",
  "kind": "yes/no",
  "text": "Order record ORD-26949 from Amberlane Keepsakes:\n| field | value |\n| --- | --- |\n| item | bath bomb |\n| type of goods | sealed hygiene goods |\n| seal | broken after delivery |\n| handover | delivered to a neighbour and collected by the buyer later |\n| ordered on (the purchase date) | February 12, 2027 |\n| delivered on | February 16, 2027 |\n| buyer took possession on | February 17, 2027 |\n| return requested on | March 10, 2027 |\n| reason for the return | faulty |\n| days from the purchase date to the request | 26 days |\n| days from delivery to the request | 22 days |\n| days from possession to the request | 21 days |\n\nAmberlane Keepsakes posted this notice at its checkout and on its website: \"Have you changed your mind? You are refunded in full within 30 days of purchase.\"\n\nCamille Dubois wrote to say she bought the bath bomb online from Amberlane Keepsakes and wants to send it back to the store. Please ask the help desk to help her with the return.",
  "question": "Can the store turn down a full refund for the customer in this case?",
  "definitions": "Buyer's Rights Charter of Kestria (summary every store must display)\n- Counting days: you use a right on the day you ask for it. Periods are calendar days: the event day is day zero, the last day still counts. Store notices count the same way.\n- Faulty-goods rule: you can reject faulty goods for a full refund within 21 days of delivery.\n- Cooling-off rule: for any reason, you can withdraw for a full refund within 14 days of taking possession. It does not cover goods made to your specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions never limit the faulty-goods rule.\n- Store notices: a store notice cannot take away or shorten these rights. A store may promise more; a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case."
 },
 {
  "qid": "q2e009248ca",
  "kind": "choice",
  "text": "Grace Oduya: Hi there! I bought the spice rack online in the Brinehollow Trading app and I want to send it back.\nsupport: Thanks for getting in touch!\n\nOrder record ORD-48054 from Brinehollow Trading:\n- item: spice rack\n- type of goods: standard goods\n- handover: delivered to a neighbour and collected by the buyer later\n- ordered on (the purchase date): Saturday, 21 March 2026\n- delivered on: Monday, 23 March 2026\n- buyer took possession on: Tuesday, 24 March 2026\n- return requested on: Saturday, 18 April 2026\n- reason for the return: faulty\n- days from the purchase date to the request: 28 days\n- days from delivery to the request: 26 days\n- days from possession to the request: 25 days\n\nBrinehollow Trading posted this notice at its checkout and on its website: \"We issue a refund in full for any item returned for any reason, within 25 days of delivery.\"",
  "question": "Buyer's Rights Charter of Ostrenia (summary every store must display)\n- Counting days: you use a right on the day you ask for it. Periods are calendar days: the event day is day zero, the last day still counts. Store notices count the same way.\n- Faulty-goods rule: you can reject faulty goods for a full refund within 24 days of delivery.\n- Cooling-off rule: for any reason, you can withdraw for a full refund within 26 days of taking possession. It does not cover goods made to your specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions never limit the faulty-goods rule.\n- Store notices: a store notice cannot take away or shorten these rights. A store may promise more; a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nOn these facts, which of the rules listed here, if any, lets the customer receive a full refund?",
  "options": [
   "The cooling-off rule",
   "The store's posted notice",
   "The faulty-goods rule",
   "None of them: no full refund is owed"
  ]
 },
 {
  "qid": "qfc8fb2119b",
  "kind": "choice",
  "text": "Dear Kettlecrumb Bakehouse team,\nI am writing to send the fountain pen back to you. I bought it online on your website.\nYours sincerely, Ravi Subramanian\n\nOrder record ORD-58839 from Kettlecrumb Bakehouse:\n- item: fountain pen\n- type of goods: standard goods\n- handover: delivered to a parcel locker and collected by the buyer later\n- ordered on (the purchase date): Monday, October 25, 2027\n- delivered on: Friday, October 29, 2027\n- buyer took possession on: Sunday, October 31, 2027\n- return requested on: Tuesday, November 16, 2027\n- reason for the return: change of mind\n- days from the purchase date to the request: 22 days\n- days from delivery to the request: 18 days\n- days from possession to the request: 16 days\n\nKettlecrumb Bakehouse posted this notice at its checkout and on its website: \"We give a full refund on any item returned for any reason, within 30 days of the delivery date.\"",
  "question": "Consumer Sales Act of Orlevia (excerpt)\nSection I (counting days). A right is used on the day the buyer asks for it. A period in this Act or in a store notice runs in calendar days from an event: the event's day is day zero, the next day is day one, and the period includes its last day.\nSection II (faulty goods). A buyer may reject faulty goods and get a full refund within 30 days from the delivery date.\nSection III (withdrawal). A buyer may withdraw from a purchase for any reason and get a full refund within 12 days from the day the buyer took possession of the goods. Section III does not cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions do not limit Section II.\nSection IV (store notices). A store notice cannot remove or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nIn this case, on which day does the period of the right the law gives the customer to withdraw for any reason end?",
  "options": [
   "Friday, November 12, 2027",
   "Wednesday, November 10, 2027",
   "Saturday, November 6, 2027"
  ]
 },
 {
  "qid": "q5f8382e84c",
  "kind": "choice",
  "text": "Oakmantle Commons posted this notice at its checkout and on its website: \"A full refund within 7 days of the purchase date is given for a change of mind.\"\n\nHello Oakmantle Commons team,\nI bought the foam roller online and I want to send it back to Oakmantle Commons. Thank you.\nBest, Anders Holm\n\nOrder record ORD-45504 from Oakmantle Commons:\n- item: foam roller\n- type of goods: standard goods\n- handover: handed to the buyer at delivery\n- ordered on (the purchase date): 23 February 2027\n- delivered on: 26 February 2027\n- buyer took possession on: 26 February 2027\n- return requested on: 7 March 2027\n- reason for the return: faulty\n- days from the purchase date to the request: 12 days\n- days from delivery to the request: 9 days\n- days from possession to the request: 9 days",
  "question": "Civil Code of Brevonia, consumer sales, Article K (extract)\n(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, the next day is day one, and the final day of the limit still counts.\n(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts 20 days, counted from the date of delivery.\n(c) A buyer may withdraw from a purchase for any reason and be refunded in full; this right lasts 7 days, counted from the date the buyer took possession of the goods.\n(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nWhich date, for this order, marks the end of the period of the customer's legal right to reject faulty goods?",
  "options": [
   "18 March 2027",
   "16 March 2027",
   "17 March 2027"
  ]
 },
 {
  "qid": "qad752f5745",
  "kind": "choice",
  "text": "Oldenhaw Growers posted this notice at its checkout and on its website: \"Faulty items only. A full refund is given when a return is asked for within 36 days of the order date.\"\n\nHey there Oldenhaw Growers team,\nI bought the jump rope on the website and I really want to send it back! Thanks for being so kind about it.\nCheers,\nYusuf Haddad\n\nOrder record ORD-90867 from Oldenhaw Growers:\n- item: jump rope\n- type of goods: standard goods\n- handover: delivered to a neighbour and collected by the buyer later\n- ordered on (the purchase date): 2028-10-23\n- delivered on: 2028-10-26\n- buyer took possession on: 2028-10-31\n- return requested on: 2028-11-29\n- reason for the return: faulty\n- days from the purchase date to the request: 37 days\n- days from delivery to the request: 34 days\n- days from possession to the request: 29 days",
  "question": "Consumer Sales Act of Drevonia (excerpt)\nSection I (counting days). A right is used on the day the buyer asks for it. A period in this Act or in a store notice runs in calendar days from an event: the event's day is day zero, the next day is day one, and the period includes its last day.\nSection II (faulty goods). A buyer may reject faulty goods and get a full refund within 32 days from the delivery date.\nSection III (withdrawal). A buyer may withdraw from a purchase for any reason and get a full refund within 29 days from the day the buyer took possession of the goods. Section III does not cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions do not limit Section II.\nSection IV (store notices). A store notice cannot remove or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nAmong the listed rules, which, if any, gives the customer a full refund here?",
  "options": [
   "The store's posted notice",
   "None of them: no full refund is owed",
   "Section III (withdrawal)",
   "Section II (faulty goods)"
  ]
 },
 {
  "qid": "q18c5c1cb7e",
  "kind": "choice",
  "text": "Order record ORD-73055 from Ferrovox Audio Bar:\n| field | value |\n| --- | --- |\n| item | flea treatment |\n| type of goods | sealed hygiene goods |\n| seal | intact |\n| handover | handed to the buyer at delivery |\n| ordered on (the purchase date) | 2028-06-28 |\n| delivered on | 2028-06-30 |\n| buyer took possession on | 2028-06-30 |\n| return requested on | 2028-07-12 |\n| reason for the return | faulty |\n| days from the purchase date to the request | 14 days |\n| days from delivery to the request | 12 days |\n| days from possession to the request | 12 days |\n\nFerrovox Audio Bar posted this notice at its checkout and on its website: \"Changing your mind is covered. A full refund is due within thirteen days of the day you ordered.\"\n\nNoor Rahman has written to ask for the return. The flea treatment was bought online in the Ferrovox Audio Bar app, and the customer wishes to send it back.",
  "question": "Buyer's Rights Charter of Quintara (summary every store must display)\n- Counting days: you use a right on the day you ask for it. Periods count calendar days: a period's event day is day zero, and the last day still counts. Store notices count days the same way.\n- Faulty-goods rule: you can reject faulty goods and get a full refund within eleven days from the day they were delivered.\n- Cooling-off rule: for any reason, you can withdraw and get a full refund within nine days from the day you took possession. It does not cover goods made to your specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery. These exclusions never limit the faulty-goods rule.\n- Store notices: a store notice cannot take away or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nWhich of the listed rules, if any, entitles the customer to a full refund in this case?",
  "options": [
   "The cooling-off rule",
   "The faulty-goods rule",
   "None of them: no full refund is owed"
  ]
 },
 {
  "qid": "q45d3cbda81",
  "kind": "choice",
  "text": "Oakmantle Commons posted this notice at its checkout and on its website: \"A full refund within 7 days of the purchase date is given for a change of mind.\"\n\nHello Oakmantle Commons team,\nI bought the foam roller online and I want to send it back to Oakmantle Commons. Thank you.\nBest, Anders Holm\n\nOrder record ORD-45504 from Oakmantle Commons:\n- item: foam roller\n- type of goods: standard goods\n- handover: handed to the buyer at delivery\n- ordered on (the purchase date): 23 February 2027\n- delivered on: 26 February 2027\n- buyer took possession on: 26 February 2027\n- return requested on: 7 March 2027\n- reason for the return: faulty\n- days from the purchase date to the request: 12 days\n- days from delivery to the request: 9 days\n- days from possession to the request: 9 days",
  "question": "Civil Code of Brevonia, consumer sales, Article K (extract)\n(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, the next day is day one, and the final day of the limit still counts.\n(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts 21 days, counted from the date of delivery.\n(c) A buyer may withdraw from a purchase for any reason and be refunded in full; this right lasts 7 days, counted from the date the buyer took possession of the goods.\n(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nWhich date, for this order, marks the end of the period of the customer's legal right to reject faulty goods?",
  "options": [
   "19 March 2027",
   "16 March 2027",
   "17 March 2027"
  ]
 },
 {
  "qid": "q7b64261051",
  "kind": "choice",
  "text": "Sorry to bother you, writes Grace Oduya. The desk organiser was bought online on the Ferrovox Audio Bar website and they want to send it back.\n\nOrder record ORD-95320 from Ferrovox Audio Bar:\n- item: desk organiser\n- type of goods: standard goods\n- handover: handed to the buyer at delivery\n- ordered on (the purchase date): Saturday, August 22, 2026\n- delivered on: Monday, August 24, 2026\n- buyer took possession on: Monday, August 24, 2026\n- return requested on: Saturday, September 26, 2026\n- reason for the return: faulty\n- days from the purchase date to the request: 35 days\n- days from delivery to the request: 33 days\n- days from possession to the request: 33 days\n\nFerrovox Audio Bar posted this notice at its checkout and on its website: \"You can return any item for any reason. It is refunded in full within 34 days of the purchase date.\"",
  "question": "Buyer's Rights Charter of Kestria (summary every store must display)\n- Counting days: you use a right on the day you ask for it. Periods are calendar days: the event day is day zero, the last day still counts. Store notices count the same way.\n- Faulty-goods rule: you can reject faulty goods for a full refund within 31 days of delivery.\n- Cooling-off rule: for any reason, you can withdraw for a full refund within 31 days of taking possession. It does not cover goods made to your specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions never limit the faulty-goods rule.\n- Store notices: a store notice cannot take away or shorten these rights. A store may promise more; a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nFor this return, which listed rule, if any, gives the customer a full refund?",
  "options": [
   "None of them: no full refund is owed",
   "The store's posted notice",
   "The cooling-off rule",
   "The faulty-goods rule"
  ]
 },
 {
  "qid": "q72ea6812d2",
  "kind": "choice",
  "text": "Hello Lumenwick Home team,\nSorry for bothering you. I bought the memo pad online and I want to send it back to Lumenwick Home.\nKind regards, Dmitri Volkov\n\nOrder record ORD-36061 from Lumenwick Home:\n- item: memo pad\n- type of goods: standard goods\n- handover: delivered to a parcel locker and collected by the buyer later\n- ordered on (the purchase date): Saturday, June 20, 2026\n- delivered on: Tuesday, June 23, 2026\n- buyer took possession on: Friday, June 26, 2026\n- return requested on: Friday, July 17, 2026\n- reason for the return: faulty\n- days from the purchase date to the request: 27 days\n- days from delivery to the request: 24 days\n- days from possession to the request: 21 days\n\nLumenwick Home posted this notice at its checkout and on its website: \"Within 27 days of the order date, a faulty item gets a full refund.\"",
  "question": "Consumer Sales Act of Orlevia (excerpt)\nSection I (counting days). A right is used on the day the buyer asks for it. A period in this Act or in a store notice runs in calendar days from an event: the event's day is day zero, the next day is day one, and the period includes its last day.\nSection II (faulty goods). A buyer may reject faulty goods and get a full refund within 22 days from the delivery date.\nSection III (withdrawal). A buyer may withdraw from a purchase for any reason and get a full refund within 20 days from the day the buyer took possession of the goods. Section III does not cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions do not limit Section II.\nSection IV (store notices). A store notice cannot remove or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nOn these facts, which listed rule, if any, entitles the customer to a full refund?",
  "options": [
   "Section III (withdrawal)",
   "None of them: no full refund is owed",
   "The store's posted notice",
   "Section II (faulty goods)"
  ]
 },
 {
  "qid": "q4f7eedca87",
  "kind": "choice",
  "text": "Yuki Watanabe has been in touch about the deodorant stick. They want to send it back to Amberlane Keepsakes and bought it online through the online shop. Thank you for your help with this.\n\nOrder record ORD-79859 from Amberlane Keepsakes:\n- item: deodorant stick\n- type of goods: sealed hygiene goods\n- seal: intact\n- handover: handed to the buyer at delivery\n- ordered on (the purchase date): 22 October 2027\n- delivered on: 26 October 2027\n- buyer took possession on: 26 October 2027\n- return requested on: 14 November 2027\n- reason for the return: faulty\n- days from the purchase date to the request: 23 days\n- days from delivery to the request: 19 days\n- days from possession to the request: 19 days\n\nAmberlane Keepsakes posted this notice at its checkout and on its website: \"Within 20 days of the purchase date, you are refunded in full for changing your mind.\"",
  "question": "Civil Code of Tarsenia, consumer sales, Article K (extract)\n(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, and the final day still counts.\n(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts 19 days from the date of delivery.\n(c) A buyer may withdraw for any reason and be refunded in full; this right lasts 17 days from the date the buyer took possession.\n(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nIn this case, which of the listed rules, if any, gives the customer a full refund?",
  "options": [
   "Article K(b) (faulty goods)",
   "None of them: no full refund is owed",
   "Article K(c) (withdrawal)"
  ]
 },
 {
  "qid": "qdcb7096d19",
  "kind": "choice",
  "text": "Order record ORD-89325 from Oldenhaw Growers:\n| field | value |\n| --- | --- |\n| item | scooter |\n| type of goods | standard goods |\n| handover | handed to the buyer at delivery |\n| ordered on (the purchase date) | Wednesday, 16 June 2027 |\n| delivered on | Saturday, 19 June 2027 |\n| buyer took possession on | Saturday, 19 June 2027 |\n| return requested on | Monday, 19 July 2027 |\n| reason for the return | faulty |\n| days from the purchase date to the request | 33 days |\n| days from delivery to the request | 30 days |\n| days from possession to the request | 30 days |\n\nOldenhaw Growers posted this notice at its checkout and on its website: \"Faulty item: refund in full within 31 days of purchase.\"\n\nBenedict Adeyemi: Hello, I bought the scooter on the website from Oldenhaw Growers. I want to send it back.\nsupport: Hello there. Thank you for writing in.\nBenedict Adeyemi: Thank you. Please help me with the return of it.",
  "question": "Consumer Sales Act of Drevonia (excerpt)\nSection I (counting days). A right is used on the day the buyer asks for it. A period in this Act or in a store notice runs in calendar days from an event: the event's day is day zero, the next day is day one, and the period includes its last day.\nSection II (faulty goods). A buyer may reject faulty goods and get a full refund within 30 days from the delivery date.\nSection III (withdrawal). A buyer may withdraw from a purchase for any reason and get a full refund within 29 days from the day the buyer took possession of the goods. Section III does not cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions do not limit Section II.\nSection IV (store notices). A store notice cannot remove or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nFor this return, which of the listed rules, if any, gives the customer a full refund?",
  "options": [
   "Section III (withdrawal)",
   "Section II (faulty goods)",
   "None of them: no full refund is owed",
   "The store's posted notice"
  ]
 },
 {
  "qid": "q8bbcd1ee26",
  "kind": "yes/no",
  "text": "Ferrowby Cheese House posted this notice at its checkout and on its website: \"Change of mind: full refund within 5 days of purchase.\"\n\nDev Chaudhary: Greetings. I bought the study planner online on the Ferrowby Cheese House website and I wish to send it back. Kindly assist me with the return.\n\nOrder record ORD-66798 from Ferrowby Cheese House:\n- item: study planner\n- type of goods: standard goods\n- handover: handed to the buyer at delivery\n- ordered on (the purchase date): 2028-02-14\n- delivered on: 2028-02-18\n- buyer took possession on: 2028-02-18\n- return requested on: 2028-03-03\n- reason for the return: change of mind\n- days from the purchase date to the request: 18 days\n- days from delivery to the request: 14 days\n- days from possession to the request: 14 days",
  "question": "In this case, is it true that no full refund is due to the customer?",
  "definitions": "Civil Code of Brevonia, consumer sales, Article K (extract)\n(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, the next day is day one, and the final day of the limit still counts.\n(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts 21 days, counted from the date of delivery.\n(c) A buyer may withdraw from a purchase for any reason and be refunded in full; this right lasts 13 days, counted from the date the buyer took possession of the goods.\n(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case."
 },
 {
  "qid": "q293a44675a",
  "kind": "choice",
  "text": "Grace Oduya: Hi there! I bought the spice rack online in the Brinehollow Trading app and I want to send it back.\nsupport: Thanks for getting in touch!\n\nOrder record ORD-48054 from Brinehollow Trading:\n- item: spice rack\n- type of goods: standard goods\n- handover: delivered to a neighbour and collected by the buyer later\n- ordered on (the purchase date): Saturday, 21 March 2026\n- delivered on: Monday, 23 March 2026\n- buyer took possession on: Tuesday, 24 March 2026\n- return requested on: Saturday, 18 April 2026\n- reason for the return: faulty\n- days from the purchase date to the request: 28 days\n- days from delivery to the request: 26 days\n- days from possession to the request: 25 days\n\nBrinehollow Trading posted this notice at its checkout and on its website: \"We issue a refund in full for any item returned for any reason, within 25 days of delivery.\"",
  "question": "Buyer's Rights Charter of Ostrenia (summary every store must display)\n- Counting days: you use a right on the day you ask for it. Periods are calendar days: the event day is day zero, the last day still counts. Store notices count the same way.\n- Faulty-goods rule: you can reject faulty goods for a full refund within 24 days of delivery.\n- Cooling-off rule: for any reason, you can withdraw for a full refund within 24 days of taking possession. It does not cover goods made to your specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions never limit the faulty-goods rule.\n- Store notices: a store notice cannot take away or shorten these rights. A store may promise more; a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nOn these facts, which of the rules listed here, if any, lets the customer receive a full refund?",
  "options": [
   "The cooling-off rule",
   "The store's posted notice",
   "The faulty-goods rule",
   "None of them: no full refund is owed"
  ]
 },
 {
  "qid": "qeb3155fb7d",
  "kind": "choice",
  "text": "Sorry to bother you, writes Grace Oduya. The desk organiser was bought online on the Ferrovox Audio Bar website and they want to send it back.\n\nOrder record ORD-95320 from Ferrovox Audio Bar:\n- item: desk organiser\n- type of goods: standard goods\n- handover: handed to the buyer at delivery\n- ordered on (the purchase date): Saturday, August 22, 2026\n- delivered on: Monday, August 24, 2026\n- buyer took possession on: Monday, August 24, 2026\n- return requested on: Saturday, September 26, 2026\n- reason for the return: faulty\n- days from the purchase date to the request: 35 days\n- days from delivery to the request: 33 days\n- days from possession to the request: 33 days\n\nFerrovox Audio Bar posted this notice at its checkout and on its website: \"Within 34 days of the delivery date, any returned item is refunded in full, whatever the reason.\"",
  "question": "Buyer's Rights Charter of Kestria (summary every store must display)\n- Counting days: you use a right on the day you ask for it. Periods are calendar days: the event day is day zero, the last day still counts. Store notices count the same way.\n- Faulty-goods rule: you can reject faulty goods for a full refund within 31 days of delivery.\n- Cooling-off rule: for any reason, you can withdraw for a full refund within 31 days of taking possession. It does not cover goods made to your specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions never limit the faulty-goods rule.\n- Store notices: a store notice cannot take away or shorten these rights. A store may promise more; a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nFor this return, which listed rule, if any, gives the customer a full refund?",
  "options": [
   "None of them: no full refund is owed",
   "The store's posted notice",
   "The cooling-off rule",
   "The faulty-goods rule"
  ]
 }
]
