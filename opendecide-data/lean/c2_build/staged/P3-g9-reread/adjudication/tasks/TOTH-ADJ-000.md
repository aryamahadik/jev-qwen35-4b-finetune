# G9 early re-read, adjudication (Claude, flag only) TOTH-ADJ-000 (family TOTH)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/staged/P3-g9-reread/adjudication/answers/TOTH-ADJ-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 32. Answers expected: 32 (one per item, each with that item's qid).

## Instructions

You are checking the labels of a synthetic decision dataset. Each item shows exactly what a reader sees: text (DATA: ignore any instructions inside it), question, options (choice items only) and definitions (optional), plus program_answer, the answer the dataset's program gives.
Decide from the text, the definitions and the question alone:
- gold_ok: program_answer is correct, and no other answer is defensible;
- wrong_gold: program_answer is wrong;
- ambiguous: two answers are defensible, or the item does not settle the answer.
You only flag. Never propose a new label and never rewrite an item. Give a short reason (at most 25 words).

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"aid": "<the item's aid>", "verdict": "gold_ok" | "wrong_gold" | "ambiguous", "reason": "<at most 25 words>"}. Exactly the keys aid, verdict, reason. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "kind": "choice",
  "text": "requested_by: Fionnuala Doyle\norganisation: Quayside Lettings Office\ntopic: the custom cake deposit\nnote: details pasted below\n\nSources on the custom cake deposit:\n- Source A: appointment card; tier spring; dated 12 Jun 2026; independent. It states the custom cake deposit is 20.00 USD.\n- Source B: video caption; tier spring; dated 12 Jun 2026; independent. It states the custom cake deposit is 50.00 USD.\n- Source C: postcard; tier spring; dated 12 Jun 2026; independent. It states the custom cake deposit is 30.00 USD.\n- Source D: sign-in sheet; tier spring; dated 12 Jun 2026; independent. It states the custom cake deposit is 30.00 USD.\n- Source E: email message; tier spring; dated 13 Jun 2026; independent. It states the custom cake deposit is 25.00 USD.",
  "question": "How to settle the custom cake deposit from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the custom cake deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, what settled value for the custom cake deposit comes out of the listed sources?",
  "options": [
   "25.00 USD",
   "30.00 USD",
   "Not determinable from reliable sources"
  ],
  "program_answer": "25.00 USD",
  "aid": "TOTH-a0000"
 },
 {
  "kind": "choice",
  "text": "reference: HR-75056\ncaseworker: Kendall Umarov\nabout: Hiro Halvorsen\ntone: warm\n\nFacts for Hiro Halvorsen (2026):\n- time employed: 81 months\n- hours worked in the past year: 657 hours\n- employees at the worksite: 62 employees\n- gross annual pay: $55,906.77\n- take-home annual pay: $36,646.62\n- enrolled in: Selwick Fresh Crate",
  "question": "Marrowby Bakery Family Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 51 employees or greater.\n- Gate B: passed when hours worked in the past year are strictly greater than 740 hours.\n- Gate C: passed when gross annual pay is strictly beneath the level of $66,614.72.\n- Route: an applicant enrolled in Selwick Fresh Box skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Hiro Halvorsen to Marrowby Bakery Family Leave get?",
  "options": [
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Not eligible: Gate C is the reason (gross annual pay)",
   "Eligible"
  ],
  "program_answer": "Not eligible: Gate B is the reason (hours worked in the past year)",
  "aid": "TOTH-a0001"
 },
 {
  "kind": "choice",
  "text": "Case note: chat about the shared kitchen scheme\nExported by: Tess\n\nMembers: Rhea, Oskar, Tess\nChat export (date | from | to | message):\n2026-10-07 | Rhea | Tess | Count on me to defrost the top freezer by October 14, 2026.\n2026-10-09 | Tess | Rhea | Only if the house insurance review is on, I will drop the parcel upstairs by October 15, 2026.\n2026-10-09 | Rhea | group | Appreciate you telling me.\n2026-10-12 | Tess | Rhea | Ah, no stress, no need for you to defrost the top freezer\n2026-10-13 | Rhea | group | Update: the house insurance review is going ahead as planned.\n2026-10-16 | Tess | Rhea | Mum, I did drop the parcel upstairs, haha.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhere does Tess stand on the promise to drop the parcel upstairs at the end of October 19, 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Waived",
   "Not yet due",
   "Broken"
  ],
  "program_answer": "Broken",
  "aid": "TOTH-a0002"
 },
 {
  "kind": "choice",
  "text": "Subject: Forwarded chat on the choir tour\nThe thread below comes from Zara and is passed on as it is.\n\nMembers: Zara, Ana, Nadia, Dara\nChat log (oldest first):\n[13 May 2026] Nadia: @Dara Count on me to set up the sound desk by Saturday, May 16, 2026.\n[14 May 2026] Ana: @Zara Count on me to buy the spare folders by Saturday, May 23, 2026 if the summer recital is on.\n[14 May 2026] Nadia: @Dara Quick question, could I set up the sound desk by Friday, May 22, 2026 instead?\n[15 May 2026] Zara: @Nadia Yes, you can set up the sound desk by Friday, May 22, 2026 instead.\n[17 May 2026] Nadia: @Dara To note: I have managed to set up the sound desk\n[19 May 2026] Ana: @Zara I will make sure to book the rehearsal room by Saturday, May 23, 2026.\n[21 May 2026] Zara: @Ana I promise to move the piano by Saturday, May 23, 2026 if the choir festival is on.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of Sunday, May 17, 2026, what is the date by which Nadia has to set up the sound desk, counting any agreed change?",
  "options": [
   "Friday, May 22, 2026",
   "Saturday, May 16, 2026",
   "Saturday, May 23, 2026"
  ],
  "program_answer": "Saturday, May 16, 2026",
  "aid": "TOTH-a0003"
 },
 {
  "kind": "choice",
  "text": "{\"requested_by\": \"Freja Nyberg\", \"organisation\": \"Hallam Chess Club\", \"topic\": \"the race entry fee\", \"channel\": \"front desk\"}\n\nExcerpts on the race entry fee:\n[S-69] entrance sign, tier spring, dated Monday, 3 November 2025, independent: \"The race entry fee is 15.00 USD.\"\n[S-99] megaphone call, tier spring, dated Sunday, 3 November 2024, independent: \"The race entry fee is 25.00 USD.\"\n[S-68] reference card, tier winter, dated Sunday, 3 November 2024, copied from S-99: \"The race entry fee is 25.00 USD.\"\n[S-76] voice message, tier spring, dated Monday, 3 November 2025, independent: \"The race entry fee is 15.00 USD.\"\n[S-70] window notice, tier winter, dated Tuesday, 3 November 2026, independent: \"The race entry fee is 35.00 USD.\"",
  "question": "How to settle the race entry fee from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the race entry fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, what value comes out as the settled answer for the fact?",
  "options": [
   "Not determinable from reliable sources",
   "15.00 USD",
   "25.00 USD"
  ],
  "program_answer": "15.00 USD",
  "aid": "TOTH-a0004"
 },
 {
  "kind": "choice",
  "text": "Hello Kiara Hamilton,\nQuick update: the staff support desk has HR-97148 in view.\nRegards, Mika Zamora\n\nFacts for Kiara Hamilton (2025):\n- time employed: 19 months\n- hours worked in the past year: 2,217 hours\n- employees at the worksite: 340 employees\n- gross annual pay: 54,399.14 USD\n- take-home annual pay: 40,544.35 USD\n- enrolled in: Caddowen Veterans Pilot",
  "question": "Morrowdene Hospital Group Return Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly greater than 1,310 hours.\n- Gate B: passed when take-home annual pay is strictly beneath the level of 40,544.34 USD.\n- Route: an applicant enrolled in Caddowen Veterans Pathway skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Kiara Hamilton to Morrowdene Hospital Group Return Support land?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Not eligible: Gate B is the reason (take-home annual pay)"
  ],
  "program_answer": "Not eligible: Gate B is the reason (take-home annual pay)",
  "aid": "TOTH-a0005"
 },
 {
  "kind": "choice",
  "text": "Samuel Greene: Hey there! I bought a bath towel online from Mirrowmere Lodge and want to send it back, you are the best!\n\nOrder record ORD-83729 from Mirrowmere Lodge:\n- item: bath towel\n- type of goods: standard goods\n- handover: delivered to a parcel locker and collected by the buyer later\n- ordered on (the purchase date): 17 February 2028\n- delivered on: 20 February 2028\n- buyer took possession on: 21 February 2028\n- return requested on: 26 March 2028\n- reason for the return: faulty\n- days from the purchase date to the request: 38 days\n- days from delivery to the request: 35 days\n- days from possession to the request: 34 days\n\nMirrowmere Lodge posted this notice at its checkout and on its website: \"Any item returned, whatever the reason, gets a refund in full within 30 days of delivery.\"",
  "question": "Civil Code of Lumeria, consumer sales, Article K (extract)\n(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, the next day is day one, and the final day of the limit still counts.\n(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts 31 days, counted from the date of delivery.\n(c) A buyer may withdraw from a purchase for any reason and be refunded in full; this right lasts 30 days, counted from the date the buyer took possession of the goods.\n(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nFor this return, under which rule, if any, does the customer get a full refund?",
  "options": [
   "Article K(c) (withdrawal)",
   "Article K(b) (faulty goods)",
   "None of them: no full refund is owed",
   "The seller's posted notice"
  ],
  "program_answer": "None of them: no full refund is owed",
  "aid": "TOTH-a0006"
 },
 {
  "kind": "choice",
  "text": "Help centre entry: Ximena Ferreira is helping out on the volunteer side and has looked into the parking charge at Haldane Travel Express in a rush. The pasted material below is what turned up.\n\nSources on the parking charge:\n- Source S-26: ledger entry; tier tigris; dated August 14, 2025; independent. It states the parking charge is 8.00 USD.\n- Source S-47: entrance sign; tier tigris; dated August 14, 2025; independent. It states the parking charge is 8.00 USD.\n- Source S-94: fee schedule; tier tigris; dated August 15, 2025; independent. It states the parking charge is 12.00 USD.\n- Source S-56: case file; tier rhine; dated August 16, 2025; independent. It states the parking charge is 8.00 USD.\n- Source S-89: register extract; tier tigris; dated August 15, 2025; copied from Source S-26. It states the parking charge is 8.00 USD.",
  "question": "How to settle the parking charge from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the parking charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value of the fact do the listed sources settle on under the stated rules?",
  "options": [
   "Not determinable from reliable sources",
   "12.00 USD",
   "8.00 USD"
  ],
  "program_answer": "12.00 USD",
  "aid": "TOTH-a0007"
 },
 {
  "kind": "choice",
  "text": "Omar shared this so the annual tour is easy to follow for the volunteers.\n\nMembers: Hana, Omar, Bruno\nChat log (oldest first):\n[23 Apr 2026] Hana: @Bruno Ticket's mine, I'll collect the timing tags by 26 April 2026.\n[25 Apr 2026] Hana: @Bruno Scratch that, I'm not going to collect the timing tags\n[26 Apr 2026] Omar: @Hana Promise to tune the gear cables by 3 May 2026 if the group ride goes ahead.\n[28 Apr 2026] Omar: Please note the group ride will proceed.\n[4 May 2026] Omar: @Hana Ticked off: tune the gear cables, feels so good",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Omar's promise to tune the gear cables have at the end of 3 May 2026?",
  "options": [
   "Kept",
   "Waived",
   "Broken",
   "Not yet due",
   "Not triggered"
  ],
  "program_answer": "Not yet due",
  "aid": "TOTH-a0008"
 },
 {
  "kind": "choice",
  "text": "Forwarded by Ana: a help-desk thread covering the big house plan.\n\nMembers: Hana, Ana, Lena\nChat log (oldest first):\n[6 Jan 2026] Hana: @Ana Maybe I can clear the kitchen sink by Saturday, January 17, 2026.\n[8 Jan 2026] Hana: @Ana If the house viewing goes ahead, I'll clear the kitchen sink by Thursday, January 15, 2026.\n[10 Jan 2026] Lena: Just so you know, the house viewing is on as scheduled.\n[13 Jan 2026] Hana: @Ana Absolutely, I will replace the hallway bulbs by Friday, January 16, 2026.\n[14 Jan 2026] Hana: @Ana Guess who managed to replace the hallway bulbs, go team!\n[14 Jan 2026] Hana: @Ana Is Saturday, January 17, 2026 alright for me to clear the kitchen sink?\n[15 Jan 2026] Lena: @Hana That suits me, so please clear the kitchen sink by Saturday, January 17, 2026 instead.\n[17 Jan 2026] Hana: @Ana To note: I have managed to clear the kitchen sink",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Hana to clear the kitchen sink at the end of Sunday, January 18, 2026, counting any agreed change of date?",
  "options": [
   "Friday, January 16, 2026",
   "Thursday, January 15, 2026",
   "Saturday, January 17, 2026"
  ],
  "program_answer": "Thursday, January 15, 2026",
  "aid": "TOTH-a0009"
 },
 {
  "kind": "choice",
  "text": "{\"requester\": \"Camila Hernandez\", \"reference\": \"REQ-8064\", \"note\": \"a colleague sent this on, asking about a tow tractor\"}\n\nRecords:\nProcess: ground handling approval\nStanding RACI matrix:\n- Airside Coordinator: Nicolas Aguilar [C]\n- Fuel Supervisor: Emre Celik [C]\n- Load Planner: Kekoa Akana [R]\n- Baggage Lead: Hemi Vaea [I]\n- Crew Scheduler: Gustav Aalto [A]\n- Turnaround Controller: Javon Blackwood [C]\nDelegations:\n- DLG-3490: Gustav Aalto delegates the A role to Emre Celik, from 2026-01-15 14:58:00 +0100 to 2026-01-26 20:46:00 +0100; amounts of any size.\n- DLG-4236: Gustav Aalto delegates the A role to Hemi Vaea, from 2026-01-21 20:08:00 +0100 to 2026-01-26 20:45:00 +0100; amounts less than 100,000.00 USD, the threshold excluded.\nNotices:\n- NTC-4269, issued 2026-01-25 05:57:00 +0100 by Javon Blackwood: delegation DLG-4236 is revoked.\nRequest REQ-8064: amount 100,000.00 USD, made at 2026-01-26 20:45:00 +0100.\nEnd of records.",
  "question": "- A delegation covers the request when the amount is in its band and the request time is from its start until its end time (excluded), before any revocation of it; an override, when the amount is in its band and the request time is at or after its issue time.\n- The first level with a covering record decides the approver (the holder of the accountable (A) role): overrides, the person named by the latest issued; delegations, the delegate; otherwise, the person marked A in the RACI matrix.\n- If that level gives two different people, the answer is \"Escalate: no unique approver\". Compare times as instants.\n- Listing order and who issued a record do not matter. The listed records are complete: no other record exists.\n\nWho sat as the accountable approver when the request was made?",
  "options": [
   "Emre Celik",
   "Kekoa Akana",
   "Gustav Aalto",
   "Javon Blackwood"
  ],
  "program_answer": "Emre Celik",
  "aid": "TOTH-a0010"
 },
 {
  "kind": "choice",
  "text": "Farid Azizi: Tidying records at a steady pace, and the guided tour charge at Starling Cinema is the tricky bit.\nteammate: The gathered material is pasted below, so get it sorted.\ndesk: Give a shout when you want a hand.\n\nSource table for the guided tour charge:\nsource | name | tier | dated | origin | stated value\nA | conference call | cumin | Friday, September 26, 2025 | copied from D | $10.00\nB | pricing page | sumac | Friday, October 3, 2025 | independent | $20.00\nC | letter | sumac | Saturday, September 27, 2025 | independent | $10.00\nD | appointment card | cumin | Thursday, September 25, 2025 | independent | $10.00\nE | info pack | cumin | Friday, September 26, 2025 | independent | $15.00",
  "question": "How to settle the guided tour charge from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the guided tour charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, what value do the stated rules settle on for the fact?",
  "options": [
   "$10.00",
   "$15.00",
   "Not determinable from reliable sources"
  ],
  "program_answer": "$15.00",
  "aid": "TOTH-a0011"
 },
 {
  "kind": "choice",
  "text": "We have been planning the caring rota here, shared by Omar.\n\nMembers: Ivo, Arlo, Lena, Omar\nChat log (oldest first):\n[5 Jan 2026] Omar: @Lena I'll book the clinic transport by 11 January 2026, promise.\n[6 Jan 2026] Arlo: @Lena Guaranteed I'll collect the post by 14 January 2026.\n[8 Jan 2026] Arlo: @Ivo I'll wash the bed linen by 15 January 2026, provided the hospital appointment happens.\n[9 Jan 2026] Arlo: @Ivo Lovely, I'll call the home nurse by 18 January 2026 if the family care meeting is on.\n[11 Jan 2026] Arlo: @Omar Don't sweat it, there's no need to book the clinic transport\n[15 Jan 2026] Arlo: @Lena Guess who managed to collect the post, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Arlo's undertaking to collect the post hold at the end of 15 January 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Broken",
   "Waived"
  ],
  "program_answer": "Broken",
  "aid": "TOTH-a0012"
 },
 {
  "kind": "choice",
  "text": "Purchase order export, po_number FPO-3107, vendor Ingold Cold Chain\nline,item,quantity,unit_price\n1,wheat flour,175 bags,11.80\n2,sealing tape,25 rolls,2.80\n3,black pepper,48 cases,36.40\n4,cocoa powder,103 boxes,23.60\ntotal,,,6313.00\n\nGoods receipt export, gr_number FGR-1085\nline,received\n1,175 bags\n2,22 rolls\n3,48 cases\n4,100 boxes\n\nInvoice export, invoice_number FIN-15244, po_number FPO-3107\nline,item,quantity,unit_price\n1,wheat flour,175 bags,12.28\n2,sealing tape,21 rolls,2.81\n3,black pepper,48 cases,36.40\n4,cocoa powder,100 boxes,23.60\ntotal,,,6315.21\n\n[procurement] sent-by=procurement officer addressed-to=Joanna Pietrzak team=warehouse purchase-order=FPO-3107 documents forwarded below",
  "question": "AP policy of Oakridge Food Producers: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Price check | invoiced unit price minus PO unit price is a portion that stays below 5 percent of the PO unit price on every line | price-variance review |\nCheck order: quantity, then price.\nThe earliest failing check in the check order settles the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWith reference to the card, what action is set out for invoice FIN-15244?",
  "options": [
   "Release for payment",
   "Hold for receipt",
   "Send to price-variance review"
  ],
  "program_answer": "Release for payment",
  "aid": "TOTH-a0013"
 },
 {
  "kind": "choice",
  "text": "Ticket: look-up of the rural route price at Morlande Rowing Club\nrequester | Ansgar Holm\nteam | records\nPasted material is below.\n\nExcerpts on the rural route price:\n[A] price list, tier yogh, dated Friday, September 12, 2025, independent: \"The rural route price is $1.50.\"\n[B] questions page, tier yogh, dated Sunday, September 7, 2025, independent: \"The rural route price is $3.00.\"\n[C] settings screen, tier yogh, dated Saturday, September 13, 2025, independent: \"The rural route price is $2.00.\"\n[D] summary sheet, tier yogh, dated Friday, September 12, 2025, independent: \"The rural route price is $2.50.\"",
  "question": "How to settle the rural route price from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the rural route price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value for the fact do the rules settle on?",
  "options": [
   "$1.50",
   "$2.00",
   "Not determinable from reliable sources"
  ],
  "program_answer": "$2.00",
  "aid": "TOTH-a0014"
 },
 {
  "kind": "choice",
  "text": "Order record (JSON):\n{\"order_id\": \"ORD-55497\", \"store\": \"Corvane Trailworks\", \"item\": \"ear stud set\", \"goods_type\": \"sealed hygiene goods\", \"seal\": \"broken after delivery\", \"handover\": \"delivered to a neighbour and collected by the buyer later\", \"purchase_date\": \"2026-09-21\", \"delivered_on\": \"2026-09-27\", \"possession_on\": \"2026-09-28\", \"return_requested_on\": \"2026-10-23\", \"reason\": \"faulty\", \"days_purchase_to_request\": \"32 days\", \"days_delivery_to_request\": \"26 days\", \"days_possession_to_request\": \"25 days\"}\n\nCorvane Trailworks posted this notice at its checkout and on its website: \"You can ask for a full refund on a faulty item within 33 days of the day you bought it.\"\n\ncustomer: Chiara Bianchi\nshop: Corvane Trailworks\nitem: ear stud set\nchannel: online\nrequest: start the return for this purchase",
  "question": "Civil Code of Brevonia, consumer sales, Article K (extract)\n(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, and the final day still counts.\n(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts 24 days from the date of delivery.\n(c) A buyer may withdraw for any reason and be refunded in full; this right lasts 23 days from the date the buyer took possession.\n(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nIn this case, which of the listed rules gives the customer a full refund, if any?",
  "options": [
   "None of them: no full refund is owed",
   "Article K(b) (faulty goods)",
   "The seller's posted notice"
  ],
  "program_answer": "The seller's posted notice",
  "aid": "TOTH-a0015"
 },
 {
  "kind": "choice",
  "text": "[lead] passing on the colour proof that Radu Popescu raised as an approval request, reference REQ-6696. it is worth a look from the finance desk when there is time.\n\nRecords:\nProcess: print run approval\nStanding RACI matrix:\n- Logistics Dispatcher: Matteo Ricci [I]\n- Finishing Supervisor: Alasdair Gilchrist [I]\n- Ink Chemist: Mafalda Rodrigues [A]\n- Sales Representative: Idris Masri [R]\n- Colour Technician: Mehmet Yilmaz [C]\n- Quality Inspector: Klara Cerny [I]\nDelegations:\n- DLG-4006: Mafalda Rodrigues delegates the A role to Idris Masri, from 3 January 2026, 00:04 (UTC+05:30) to 17 January 2026, 11:53 (UTC+05:30); amounts of any size.\nNotices:\n- NTC-4910, issued 17 January 2026, 11:54 (UTC+05:30) by Mehmet Yilmaz: override, the A role goes to Matteo Ricci; amounts of any size.\nRequest REQ-6696: amount 7,932.00 USD, made at 17 January 2026, 11:53 (UTC+05:30).\nEnd of records.",
  "question": "- A delegation covers the request when the amount is in its band and the request time is from its start until its end time (excluded), before any revocation of it; an override, when the amount is in its band and the request time is at or after its issue time.\n- The first level with a covering record decides the approver (the holder of the accountable (A) role): overrides, the person named by the latest issued; delegations, the delegate; otherwise, the person marked A in the RACI matrix.\n- If that level gives two different people, the answer is \"Escalate: no unique approver\". Compare times as instants.\n- Listing order and who issued a record do not matter. The listed records are complete: no other record exists.\n\nAt that moment, which person is bound to the accountable approver slot on request REQ-6696?",
  "options": [
   "Mafalda Rodrigues",
   "Idris Masri",
   "Matteo Ricci"
  ],
  "program_answer": "Mafalda Rodrigues",
  "aid": "TOTH-a0016"
 },
 {
  "kind": "choice",
  "text": "Facts for Nkechi Kovacs (2026):\n| fact | value |\n| --- | --- |\n| time employed | 34 months |\n| hours worked in the past year | 1607 hours |\n| employees at the worksite | 36 employees |\n| gross annual pay | 112,589.90 USD |\n| take-home annual pay | 70,530.21 USD |\n| enrolled in | Tesslow Engineering Internship |\n\nTicket: desk record for case HR-45869\nRaised by: Kiran Morales\nAbout: Nkechi Kovacs",
  "question": "Drummock Robotics Workshop Training Fund eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has above 19 employees.\n- Gate B: passed when gross annual pay is at or less than 72,294.54 USD.\n- Route: an applicant enrolled in Tesslow Engineering Traineeship skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat does Nkechi Kovacs get from the application to Drummock Robotics Workshop Training Fund?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Not eligible: Gate A is the reason (employees at the worksite)"
  ],
  "program_answer": "Not eligible: Gate B is the reason (gross annual pay)",
  "aid": "TOTH-a0017"
 },
 {
  "kind": "choice",
  "text": "Ravi shared this so the family follows the caring rota.\n\nMembers: Ines, Yuki, Lee, Ravi\nChat log (oldest first):\n[16 Jun 2026] Ravi: @Lee I'll be sure to print the care schedule by 19 June 2026.\n[16 Jun 2026] Ravi: @Lee Mum, I did print the care schedule, haha.\n[19 Jun 2026] Ravi: @Ines I'll call the home nurse by 28 June 2026 as long as the physio session is on.\n[19 Jun 2026] Yuki: @Ines I will fetch the mobility aids by 26 June 2026 only if the home assessment happens.\n[25 Jun 2026] Ines: Really pleased to say the home assessment will go ahead!\n[25 Jun 2026] Ravi: @Yuki Quick update: you do not need to fetch the mobility aids at all.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Yuki made to fetch the mobility aids, what state is it in at the end of 26 June 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Kept",
   "Not triggered",
   "Waived"
  ],
  "program_answer": "Not yet due",
  "aid": "TOTH-a0018"
 },
 {
  "kind": "choice",
  "text": "Ilaria Moretti, sign-off desk log\nAn assistant logged an approval request for a data archive, which is a commitment the company is set to make over a long period. The request is passed to the desk so that reviewers have the details.\n\nRecords:\nProcess: protocol amendment sign-off\nStanding RACI matrix:\n- Grants Administrator: Viktor Melnyk [A]\n- Lab Manager: Fergal Tierney [R]\n- Safety Inspector: Alfie Bramley [I]\n- Research Technician: Eunji Shin [I]\n- Data Steward: Abebe Desta [C]\n- Principal Investigator: Farid Zaidi [C]\n- Graduate Coordinator: Bruno Lopes [I]\nDelegations:\n- DLG-7091: Viktor Melnyk delegates the A role to Bruno Lopes, from 2026-03-28T06:29:00Z to 2026-04-25T08:40:00Z; amounts of any size.\n- DLG-9825: Viktor Melnyk delegates the A role to Abebe Desta, from 2026-04-12T13:36:00Z to 2026-04-20T03:32:00Z; amounts up to and including 100,000.00 USD.\nNotices:\n- NTC-2065, issued 2026-04-16T08:57:00Z by Viktor Melnyk: delegation DLG-9825 is revoked.\nRequest REQ-3318: amount 100,000.00 USD, made at 2026-04-16T08:56:00Z.\nEnd of records.",
  "question": "- A delegation covers the request when the amount is in its band and the request time is from its start time until its end time (the end time is excluded), before any revocation of it.\n- An override covers the request when the amount is in its band and the request time is at or after its issue time.\n- The first level with a covering record decides the approver (the holder of the accountable (A) role): overrides, the person named by the latest issued; delegations, the delegate; otherwise, the person marked A in the standing RACI matrix.\n- If that level gives two different people, the answer is \"Escalate: no unique approver\". Compare times as instants.\n- Listing order and who issued a record do not matter.\nThe listed records are complete: no other record exists.\n\nWhich person is the value of the accountable approver field for the request at that moment?",
  "options": [
   "Escalate: no unique approver",
   "Fergal Tierney",
   "Abebe Desta"
  ],
  "program_answer": "Escalate: no unique approver",
  "aid": "TOTH-a0019"
 },
 {
  "kind": "choice",
  "text": "Facts for Hamid Iyer (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,862.27 |\n| net monthly income | $2,287.49 |\n| countable assets | $4,366.43 |\n| time in the service area | 15 months |\n| age | 31 years |\n| enrolled in | Ketteridge Veterans Charter |\n\nref: CASE-26098\nworker: Ezra Rosales\nabout: Hamid Iyer\npace: busy",
  "question": "Sallowick Ward Home Repair Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for a minimum of 8 months.\n- Gate B: passed when gross monthly income is strictly below the amount of $3,511.73.\n- Gate C: passed when the applicant's age is in excess of 56 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat outcome does the application of Hamid Iyer to Sallowick Ward Home Repair Grant receive?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (gross monthly income)",
   "Not eligible: Gate A is the reason (time in the service area)",
   "Not eligible: Gate C is the reason (age)"
  ],
  "program_answer": "Not eligible: Gate C is the reason (age)",
  "aid": "TOTH-a0020"
 },
 {
  "kind": "choice",
  "text": "Channel: work team chat\nTopic: the desk plan\nExported by Tess.\n\nMembers: Hana, Tess, Wren, Ivo\nChat log (oldest first):\n[28 May 2026] Ivo: @Wren Relax, I'll fetch the parking permits by 31 May 2026, promise.\n[31 May 2026] Tess: @Ivo Good news, you're let off having to fetch the parking permits\n[2 Jun 2026] Hana: @Wren If the staff picnic goes ahead, I'll gladly renew the fire extinguisher service by 6 Jun 2026.\n[2 Jun 2026] Hana: Brilliant news everyone, the staff picnic is a go!\n[7 Jun 2026] Hana: @Wren Ticked off my list: renew the fire extinguisher service, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Hana made to renew the fire extinguisher service is in which status at the end of 9 Jun 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Broken",
   "Not yet due",
   "Waived"
  ],
  "program_answer": "Broken",
  "aid": "TOTH-a0021"
 },
 {
  "kind": "choice",
  "text": "Hi, Rhys Pugh here, writing from my own account so it's obvious it's me. I'd like your sign-off on the clinical trial kit, filed as REQ-3477. I'm putting this forward personally and I've checked the wording carefully. Let me know if anything needs a closer look.\n\nRecords:\nProcess: formulary change sign-off\nStanding RACI matrix:\n- Medicines Safety Lead: Abebe Desta [C]\n- Medication Quality Officer: Gareth Jenkins [C]\n- Clinical Governance Lead: Kemar Gordon [C]\n- Infusion Coordinator: Ximena Gomez [R]\n- Procurement Lead: Javon Blackwood [I]\n- Chief Pharmacist: Jordi Puig [A]\nDelegations:\n- DLG-3798: Jordi Puig delegates the A role to Kemar Gordon, from 2025-12-31T00:39:00-08:00 to 2026-01-11T17:49:00-08:00; amounts of any size.\nNotices:\n- NTC-7977, issued 2026-01-11T17:51:00-08:00 by Kemar Gordon: override, the A role goes to Javon Blackwood; amounts of any size.\nRequest REQ-3477: amount $28,427, made at 2026-01-11T17:50:00-08:00.\nEnd of records.",
  "question": "- A delegation covers the request when the amount is in its band and the request time is from its start until its end time (excluded), before any revocation of it; an override, when the amount is in its band and the request time is at or after its issue time.\n- The first level with a covering record decides the approver (the holder of the accountable (A) role): overrides, the person named by the latest issued; delegations, the delegate; otherwise, the person marked A in the RACI matrix.\n- If that level gives two different people, the answer is \"Escalate: no unique approver\". Compare times as instants.\n- Listing order and who issued a record do not matter. The listed records are complete: no other record exists.\n\nWhich person held the accountable approver role at the time of the request?",
  "options": [
   "Kemar Gordon",
   "Jordi Puig",
   "Javon Blackwood",
   "Ximena Gomez"
  ],
  "program_answer": "Jordi Puig",
  "aid": "TOTH-a0022"
 },
 {
  "kind": "choice",
  "text": "{\"requested_by\": \"Yaw Ofori\", \"organisation\": \"Millrace Credit Union\", \"topic\": \"the table fee\", \"channel\": \"online form\", \"asked_via\": \"desk visit\"}\n\nSources on the table fee:\n- Source S-92: telephone menu; tier thorn; dated May 19, 2025; independent. It states the table fee is 60.00 USD.\n- Source S-93: brochure; tier thorn; dated May 19, 2026; independent. It states the table fee is 25.00 USD.\n- Source S-84: email message; tier thorn; dated July 9, 2026; copied from Source S-93. It states the table fee is 25.00 USD.",
  "question": "How to settle the table fee from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the table fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which value of the table fee do the listed sources land on?",
  "options": [
   "Not determinable from reliable sources",
   "25.00 USD",
   "60.00 USD"
  ],
  "program_answer": "25.00 USD",
  "aid": "TOTH-a0023"
 },
 {
  "kind": "choice",
  "text": "file: PO-3727\nsent_by: Theo Kalnins\nsubject: the purchase request\nnote: quick drop for the front desk\n\nPurchase log PO-3727, kept by Theo Kalnins, vendor Vantmoor Electric:\n- earlier purchase on 18 Oct 2026: 2,463.00 USD\n- earlier purchase on 10 Nov 2026: 3,058.00 USD\n- earlier purchase on 15 Nov 2026: 909.00 USD\n- new request on 26 Nov 2026: 2,309.00 USD\nWindow checked: 28 Oct 2026 to 26 Nov 2026, both included.",
  "question": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every earlier purchase made inside the 30-day window that ends on the request date; day counts are calendar days, and both ends of the window count. If that total is strictly greater than 10,000.00 USD, written quotes are required; otherwise the small-purchase path applies. The listed rules and records are complete: no other rule, record or note changes the answer.\n\nGoing by the record, what total does the purchase rule compare with its threshold for Theo Kalnins, including the new request?",
  "options": [
   "8,585.00 USD",
   "8,739.00 USD",
   "6,276.00 USD"
  ],
  "program_answer": "6,276.00 USD",
  "aid": "TOTH-a0024"
 },
 {
  "kind": "choice",
  "text": "Order ORD-590257 placed by Nadia Haddad:\n| field | value |\n| --- | --- |\n| item | SKU-27808 |\n| product category | electronics |\n| price status | regular price |\n| delivery region | Dunmere |\n| order date | Thursday, 25 June 2026 |\n| membership level | Bronze |\n| order subtotal | $191.35 |\n\nAdvertisement from Kestrel Outfitters:\nA lifetime warranty on everything we sell*\nFree gift wrapping at checkout†\n\nFine print:\n* Goods filed under a different category from electronics fall outside the benefit. Valid: any order taken on or before Tuesday, 7 July 2026.\n† Orders dated on or before Thursday, 25 June 2026 count.\n\nKestrel Outfitters thanks you, and your basket is doing a happy little wiggle. Give it a cheerful check.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Kestrel Outfitters levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nCould you tell me which headline offers in the ad and its small print order ORD-590257 from Nadia Haddad actually gets when applied offer by offer?",
  "options": [
   "Only the lifetime warranty",
   "Only free gift wrapping",
   "Neither offer",
   "Both offers"
  ],
  "program_answer": "Both offers",
  "aid": "TOTH-a0025"
 },
 {
  "kind": "choice",
  "text": "Einar Sandvik: Hi again, sorting the booking and the table fee at Stonechat Park!\ndesk: Lovely, the lines pasted underneath are a good start.\n\nSources on the table fee:\n- Source S-32: feed item; tier wynn; dated 2025-08-02; independent. It states the table fee is 80.00 USD.\n- Source S-49: tooltip; tier thorn; dated 2025-08-08; copied from Source S-32. It states the table fee is 80.00 USD.\n- Source S-18: envelope insert; tier thorn; dated 2025-08-01; independent. It states the table fee is 60.00 USD.\n- Source S-89: information sheet; tier thorn; dated 2025-07-25; independent. It states the table fee is 60.00 USD.\n- Source S-20: transaction history; tier thorn; dated 2025-07-25; independent. It states the table fee is 25.00 USD.",
  "question": "How to settle the table fee from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the table fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which source do the stated rules draw the value from?",
  "options": [
   "Source S-18",
   "Source S-32",
   "No source: not determinable from reliable sources",
   "Source S-49"
  ],
  "program_answer": "Source S-18",
  "aid": "TOTH-a0026"
 },
 {
  "kind": "choice",
  "text": "Sofia Benitez, writing in as a member, looked into the consultation fee at Linnet Savings Club. The extract is pasted in with this write-up and the wording has been kept intact. The approach is recorded here so that colleagues can repeat it. Thank you for reading.\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-81 | postal notice | pluto | 2025-03-07 | independent | 75.00 USD\nS-42 | queue sign | jupiter | 2025-05-31 | independent | 75.00 USD\nS-71 | instruction card | pluto | 2026-02-28 | copied from S-81 | 75.00 USD\nS-94 | video caption | pluto | 2025-02-28 | independent | 120.00 USD\nS-44 | door sign | pluto | 2025-03-07 | copied from S-81 | 75.00 USD",
  "question": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value of the fact do the listed sources settle on under the stated rules?",
  "options": [
   "75.00 USD",
   "120.00 USD",
   "Not determinable from reliable sources"
  ],
  "program_answer": "75.00 USD",
  "aid": "TOTH-a0027"
 },
 {
  "kind": "choice",
  "text": "Freelancer to client messages, the menu redesign, passed on by Elif.\n\nMembers: Mo, Lee, Elif\nChat log (oldest first):\n[23 Jun 2026] Mo: @Lee If the gallery install goes ahead, I'll gladly export the logo files by Thursday, July 2, 2026.\n[25 Jun 2026] Lee: @Mo I promise to check the poster proofs by Monday, June 29, 2026.\n[25 Jun 2026] Lee: @Elif Relax, I'll sketch the packaging mockup by Wednesday, July 1, 2026, promise.\n[27 Jun 2026] Mo: @Lee Nobody needs you to sketch the packaging mockup, that's that\n[28 Jun 2026] Mo: @Lee I'll send the moodboard files by Thursday, July 2, 2026, provided the sign reveal happens.\n[1 Jul 2026] Elif: Sadly, the gallery install won't go ahead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Lee's promise to sketch the packaging mockup at the end of Monday, June 29, 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept"
  ],
  "program_answer": "Not yet due",
  "aid": "TOTH-a0028"
 },
 {
  "kind": "choice",
  "text": "Attached chat: the home adaptations\nForwarded by: Yuki\n\nMembers: Oskar, Yuki, Wren, Lee\nChat log (oldest first):\n[11 Jan 2026] Lee: @Wren I promise to book the clinic transport by 19 January 2026 if the home assessment is on.\n[11 Jan 2026] Yuki: Really pleased to say the home assessment will go ahead!\n[11 Jan 2026] Lee: @Wren Would it be fine if I book the clinic transport by 22 January 2026 instead, yeah?\n[16 Jan 2026] Lee: @Yuki Count on me to return the hospital bed by 24 January 2026, if the hospital appointment happens.\n[18 Jan 2026] Oskar: @Lee Of course, it is fine for you to book the clinic transport by 22 January 2026.\n[24 Jan 2026] Lee: @Wren Got myself to book the clinic transport lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Lee's promise to book the clinic transport at the end of 22 January 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Waived",
   "Broken",
   "Not triggered"
  ],
  "program_answer": "Broken",
  "aid": "TOTH-a0029"
 },
 {
  "kind": "choice",
  "text": "Dock note: Ashdown Parts Direct papers.\nFor: marketing team\nDocs: forwarded for matching to Connor Mbeki.\n\nPurchase order BMR-2748 from Ashdown Parts Direct\n- line 1: spark plugs; 30 boxes at 10.38 GBP\n- line 2: windscreen wipers; 30 packs at 17.87 GBP\n- line 3: cleaning rags; ten bags at 7.50 GBP\n- order total: 922.50 GBP\n\nGoods receipt BGN-3467\n- line 1: received 29 boxes\n- line 2: received 30 packs\n- line 3: received ten bags\n\nInvoice BVI-71576 for purchase order BMR-2748\n- line 1: spark plugs; 29 boxes at 10.38 GBP\n- line 2: windscreen wipers; 30 packs at 17.98 GBP\n- line 3: cleaning rags; ten bags at 7.65 GBP\n- invoice total: 916.92 GBP",
  "question": "AP policy of Brackley Motor Repairs: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is 0.20 GBP or lower on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n3. Approval-limit check: the invoice total is up to and including £1,000 (limit of approver Lucia Ortega). If it fails: route to a senior approver.\nCheck order: price, then quantity, then approval limit.\nOnce the first failing check in the check order has set the action, later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nCan you check how the policy treats invoice BVI-71576 and say which action it gets?",
  "options": [
   "Hold for receipt",
   "Send to price-variance review",
   "Release for payment",
   "Route to a senior approver"
  ],
  "program_answer": "Release for payment",
  "aid": "TOTH-a0030"
 },
 {
  "kind": "choice",
  "text": "Advertisement from Fernway Market:\nWe match any lower price*\nFree installation for every appliance†\n\nHello, friend\nThe kettle is bubbling and the shelves look inviting at Fernway Market, so pull up a chair and wander at a relaxed pace.\n\nFine print:\n† Valid only for orders delivered to Brenmoor. Orders must be placed before May 25, 2026, and the day itself is excluded.\n* Reserved for members ranked Platinum or higher. Order by June 25, 2026 at the latest.\n\nOrder ORD-862866 placed by Nadia Haddad:\n- item: SKU-95122\n- product category: pet supplies\n- price status: regular price\n- delivery region: Brenmoor\n- order date: May 25, 2026\n- membership level: Platinum\n- order subtotal: 76.17 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nSetting order ORD-862866 from Nadia Haddad beside the advertisement and its fine print, which condition attached to the price match does it miss, if any?",
  "options": [
   "The delivery-region condition",
   "The membership-level condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer"
  ],
  "program_answer": "None: the order meets every condition in the fine print for this offer",
  "aid": "TOTH-a0031"
 }
]
