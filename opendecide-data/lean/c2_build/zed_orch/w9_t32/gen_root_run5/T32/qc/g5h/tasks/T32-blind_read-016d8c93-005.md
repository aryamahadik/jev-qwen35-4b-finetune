# G5-H blind read T32-blind_read-016d8c93-005 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root/T32/qc/g5h/answers/T32-blind_read-016d8c93-005.json

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
  "qid": "q37321cc154",
  "kind": "choice",
  "text": "Attached chat: the new kit design\nShared by: Wren.\n\nMembers: Rhea, Oskar, Wren\nChat log (oldest first):\n[6 Mar 2026] Wren: @Oskar Promise to pump the spare tyres by Saturday, 14 March 2026 if the bike check goes ahead.\n[7 Mar 2026] Rhea: @Oskar Ticket's mine, I'll collect the timing tags by Wednesday, 11 March 2026.\n[8 Mar 2026] Oskar: @Rhea I'll stock the energy gels by Saturday, 14 March 2026 as long as the club sportive is on.\n[10 Mar 2026] Wren: @Rhea Count on me to wash the club jerseys by Friday, 13 March 2026.\n[11 Mar 2026] Wren: @Rhea For the record: I was able to wash the club jerseys",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Wren gave to wash the club jerseys have at the end of Sunday, 15 March 2026?",
  "options": [
   "Broken",
   "Kept",
   "Waived",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q2f6ebe4681",
  "kind": "yes/no",
  "text": "This export holds the messages about the reunion planning, which Kai saved.\n\nMembers: Kai, Ravi, Leila, Sami\nChat log (oldest first):\n[9 Mar 2026] Ravi: @Kai I'll try to send the group invitations by 15 Mar 2026, no promises.\n[10 Mar 2026] Ravi: @Sami I will send the group invitations by 17 Mar 2026.\n[12 Mar 2026] Sami: @Kai I assure you I'll print the family tree chart by 20 Mar 2026 if the reunion lunch is on.\n[13 Mar 2026] Kai: @Leila I'll fetch the speaker system by 18 Mar 2026 as long as the garden picnic is on.\n[14 Mar 2026] Kai: @Ravi Nobody needs you to send the group invitations, that's that\n[20 Mar 2026] Ravi: @Sami To my relief, I managed to send the group invitations.",
  "question": "At the end of 21 Mar 2026, is Ravi's promise to send the group invitations broken, waived, not triggered or not yet due, rather than kept?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4ff8ea4a2b",
  "kind": "choice",
  "text": "Shared by Mo, this thread covers the online store move as pasted from email.\n\nMembers: Wren, Ivo, Sami, Mo\nChat log (oldest first):\n[13 Oct 2026] Mo: @Sami Ticket's mine, I'll fetch the domain login by 16 Oct 2026.\n[13 Oct 2026] Mo: @Sami Mate, I promised, may I fetch the domain login by 19 Oct 2026 instead?\n[14 Oct 2026] Ivo: @Wren If the pop up stall is on, I'll definitely add the size chart by 22 Oct 2026.\n[15 Oct 2026] Ivo: @Sami I'll set up the email forwarding by 21 Oct 2026, provided the market day happens.\n[16 Oct 2026] Sami: @Mo Don't sweat it, there's no need to fetch the domain login",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Mo made to fetch the domain login, what state is it in at the end of 21 Oct 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Broken",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q75cfe3f523",
  "kind": "yes/no",
  "text": "{\"saved_copy\": \"the loft conversion\", \"keeper\": \"Priya\", \"medium\": \"chat transcript\"}\n\nMembers: Ivo, Femi, Ines, Priya\nChat export (date | from | to | message):\n2026-02-01 | Ines | Ivo | Relax, I'll collect the sanding pads by 5 February 2026, promise.\n2026-02-03 | Ines | Femi | I'll scrape the old wallpaper by 5 February 2026, providing the boiler install visit goes ahead.\n2026-02-03 | Priya | group | Please note the boiler install visit will proceed.\n2026-02-04 | Ines | Femi | Got it, I'll hang the new curtain rail by 7 February 2026 for sure.\n2026-02-07 | Ines | Priya | I will pick up the grout bag by 16 February 2026 only if the damp survey inspection happens.\n2026-02-07 | Femi | Ines | No worries, you don't need to hang the new curtain rail",
  "question": "At the end of 7 February 2026, has the promise Ines made to hang the new curtain rail been broken?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1ebd3b248b",
  "kind": "yes/no",
  "text": "The family thread was saved by Sami, and its subject is the vegetable plot plan.\n\nMembers: Sami, Ana, Lena, Omar\nChat log (oldest first):\n[30 Oct 2026] Lena: @Sami I own this, I'll stake the tomato canes by November 1, 2026.\n[30 Oct 2026] Lena: @Sami Log entry: stake the tomato canes, carried out\n[3 Nov 2026] Ana: @Sami If the plot inspection is on, I'll definitely deliver the surplus runner beans by November 7, 2026.\n[3 Nov 2026] Sami: Yay, the plot inspection is all set to go!\n[10 Nov 2026] Ana: @Sami Ticked off: deliver the surplus runner beans, feels so good",
  "question": "Under the rules on the card, is the promise Ana made to deliver the surplus runner beans in a status other than broken at the end of November 9, 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd9141b7ff4",
  "kind": "yes/no",
  "text": "Subject: chat about the sponsor search, forwarded\nThe chat follows below.\nRegards, Bruno\n\nMembers: Tess, Bruno, Ravi\nChat log (oldest first):\n[16 Jan 2026] Bruno: @Ravi Relax, I'll pump the spare tyres by 18 Jan 2026 for sure.\n[16 Jan 2026] Ravi: @Tess I own this, I'll fetch the bike stand by 22 Jan 2026.\n[21 Jan 2026] Ravi: @Tess Lovely, I'll service the tandem bike by 28 Jan 2026 if the group ride is on.\n[22 Jan 2026] Bruno: Fab, we are on for the group ride as planned!\n[22 Jan 2026] Ravi: @Tess Ticked off: fetch the bike stand, feels so good",
  "question": "At the end of 28 Jan 2026, is Ravi's promise to fetch the bike stand broken, waived, not triggered or not yet due, rather than kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q35fa3b7a48",
  "kind": "choice",
  "text": "Household chat saved by Bruno, with the cottage refresh at its heart.\n\nMembers: Yuki, Omar, Rhea, Bruno\nChat log (oldest first):\n[17 Feb 2026] Omar: @Yuki You can bank on me to collect the bed linen by 25 Feb 2026.\n[24 Feb 2026] Rhea: @Omar Provided the guest arrival evening happens, I'll restock the guest toiletries by 1 Mar 2026.\n[25 Feb 2026] Omar: @Yuki Any chance I can collect the bed linen by 28 Feb 2026 instead?\n[25 Feb 2026] Bruno: @Omar Revised deadline is 28 Feb 2026, so you can collect the bed linen.\n[25 Feb 2026] Rhea: @Omar Forget it, you won't need to collect the bed linen\n[27 Feb 2026] Omar: @Yuki To note: I have managed to collect the bed linen\n[1 Mar 2026] Omar: @Yuki Provided the pool safety inspection happens, I'll wheel the bins out by 5 Mar 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 26 Feb 2026, by what date does Omar have to collect the bed linen, counting any agreed change of date?",
  "options": [
   "25 Feb 2026",
   "28 Feb 2026",
   "1 Mar 2026"
  ]
 },
 {
  "qid": "q14ff5ee40a",
  "kind": "yes/no",
  "text": "Subject: the payment setup, chat copy\nPassed along by Elif, with the full chat below.\n\nMembers: Lena, Greta, Elif\nChat log (oldest first):\n[12 Jul 2026] Elif: @Greta It's on me to restore the old theme by Monday, 20 July 2026.\n[13 Jul 2026] Greta: @Elif Promise to renew the hosting plan by Wednesday, 22 July 2026 if the pop up stall goes ahead.\n[13 Jul 2026] Greta: Great news, the pop up stall is on!\n[15 Jul 2026] Lena: @Elif Good news, you're let off having to restore the old theme\n[17 Jul 2026] Elif: @Greta Ticket's mine, I'll add the size chart by Thursday, 23 July 2026.\n[21 Jul 2026] Elif: @Greta Gutted to say I won't add the size chart, sorry team",
  "question": "Under the rules on the card, is the promise Elif made to add the size chart broken at the end of Tuesday, 21 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qcc1dce1b87",
  "kind": "choice",
  "text": "Household group messages for the front garden scheme were passed along by Ravi.\n\nMembers: Bruno, Ravi, Wren\nChat log (oldest first):\n[16 Jul 2026] Ravi: @Wren Lovely, I'll feed the cat across the road by 19 July 2026 for sure.\n[17 Jul 2026] Wren: @Ravi Provided the road works meeting happens, I'll take in the post by 20 July 2026.\n[18 Jul 2026] Ravi: Sorry, the road works meeting is off.\n[19 Jul 2026] Ravi: @Wren To note: I have managed to feed the cat across the road\n[20 Jul 2026] Wren: @Bruno I promise to walk the old spaniel by 24 July 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Ravi's promise to feed the cat across the road at the end of 21 July 2026?",
  "options": [
   "Kept",
   "Waived",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qc01cb52e99",
  "kind": "choice",
  "text": "Subject: Chat about the vegetable plot plan\nBelow is a copy that came from Zara, pasted as found.\n\nMembers: Kai, Ana, Yuki, Zara\nChat log (oldest first):\n[6 Oct 2026] Yuki: @Zara As long as the village flower show is on, I will sharpen the hand hoe by 13 October 2026.\n[6 Oct 2026] Kai: Sorry all, the village flower show is called off.\n[7 Oct 2026] Zara: @Yuki Got it, I'll sow the broad beans by 10 October 2026 for sure.\n[10 Oct 2026] Zara: @Yuki I regret to say that I shall not sow the broad beans.\n[10 Oct 2026] Ana: @Zara Relax, mate, you're not expected to sow the broad beans",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Zara's pledge to sow the broad beans at the end of 15 October 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q3d5268877d",
  "kind": "choice",
  "text": "Saved by Lena, this is the household group chat about the caring rota, copied in full.\n\nMembers: Lee, Lena, Nadia\nChat log (oldest first):\n[25 Aug 2026] Nadia: @Lena Count on me to pick up the repeat prescription by Tuesday, 1 September 2026, if the carer handover happens.\n[27 Aug 2026] Lena: @Lee Count on me to call the home nurse by Saturday, 29 August 2026.\n[27 Aug 2026] Lena: Just so you know, the carer handover is on as scheduled.\n[28 Aug 2026] Lee: @Lena Quick update: you do not need to call the home nurse at all.\n[29 Aug 2026] Lee: @Nadia No worries, you don't need to pick up the repeat prescription",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Nadia's promise to pick up the repeat prescription at the end of Monday, 31 August 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "qbab55a998e",
  "kind": "choice",
  "text": "Team thread shared by Yuki, covering the desk plan in the channel.\n\nMembers: Ana, Kai, Yuki\nChat export (date | from | to | message):\n2026-10-02 | Kai | Ana | I'll return the printer toner by 11 October 2026, providing the staff picnic goes ahead.\n2026-10-04 | Ana | Kai | Count on me to set up the reception screen by 9 October 2026 if the coffee morning is on.\n2026-10-05 | Kai | Ana | Got it, I'll book the boardroom by 10 October 2026 for sure.\n2026-10-07 | Yuki | Kai | You can bet I'll fetch the parking permits by 13 October 2026.\n2026-10-10 | Kai | Ana | Got myself to book the boardroom lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of 14 October 2026, which status does Kai have for the promise to book the boardroom?",
  "options": [
   "Broken",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q2619d9334f",
  "kind": "choice",
  "text": "Flatmates' thread\nExport of the flat upgrade list, passed on by Wren.\n\nMembers: Kofi, Wren\nChat log (oldest first):\n[5 Sep 2026] Wren: @Kofi It's on me to forward the gas bill by 13 Sep 2026.\n[7 Sep 2026] Kofi: @Wren Absolutely, I will measure the kitchen for fridge by 14 Sep 2026.\n[7 Sep 2026] Wren: @Kofi You can bank on me to read the meter readings by 15 Sep 2026.\n[8 Sep 2026] Wren: @Kofi Might I ask whether I could forward the gas bill by 16 Sep 2026 instead?\n[9 Sep 2026] Wren: @Kofi If the rent review meeting goes ahead, I'll remove the bathroom shelf by 15 Sep 2026.\n[11 Sep 2026] Wren: @Kofi No need to measure the kitchen for fridge, I'm letting you off\n[13 Sep 2026] Wren: Sorry all, the rent review meeting is not happening.\n[13 Sep 2026] Wren: @Kofi For the record: I was able to forward the gas bill",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules, when is the date by which Wren has to forward the gas bill at the end of 18 Sep 2026, allowing for any agreed change?",
  "options": [
   "14 Sep 2026",
   "13 Sep 2026",
   "16 Sep 2026"
  ]
 },
 {
  "qid": "q8d4efabcdf",
  "kind": "choice",
  "text": "Plain copy of a family thread on the care plan, passed on by Hana.\n\nMembers: Tomas, Hana, Ravi, Jonas\nChat log (oldest first):\n[27 Jul 2026] Ravi: @Jonas Committing to call the home nurse by 5 Aug 2026.\n[31 Jul 2026] Hana: @Jonas Promise to set up the medicine dispenser by 5 Aug 2026 if the eye test goes ahead.\n[31 Jul 2026] Ravi: @Hana Count on me, I'll print the care schedule by 8 Aug 2026.\n[2 Aug 2026] Ravi: Really pleased to say the eye test will go ahead!\n[3 Aug 2026] Jonas: @Ravi Nobody needs you to call the home nurse, that's that\n[6 Aug 2026] Ravi: @Hana On my action item, may I print the care schedule by 14 Aug 2026 instead?\n[7 Aug 2026] Hana: @Ravi Oh hun, I can't budge, so print the care schedule by the old date!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs things stand at the end of 10 Aug 2026, which date is the deadline for Ravi to print the care schedule, with any agreed change applied?",
  "options": [
   "8 Aug 2026",
   "14 Aug 2026",
   "5 Aug 2026"
  ]
 },
 {
  "qid": "qb55749b473",
  "kind": "yes/no",
  "text": "Forwarded by Leila, these tenant replies are about the summer lets season for the file.\n\nMembers: Leila, Wren, Dara\nChat log (oldest first):\n[25 May 2026] Dara: @Leila Count on me, I'll wheel the bins out by 2026-05-28.\n[26 May 2026] Wren: @Leila If the guest arrival evening goes ahead, I'll restock the guest toiletries by 2026-06-02.\n[28 May 2026] Dara: @Leila Mate, I promised, may I wheel the bins out by 2026-06-01 instead?\n[28 May 2026] Leila: @Dara Yes, you can wheel the bins out by 2026-06-01 if that suits you.\n[1 Jun 2026] Leila: Update, the guest arrival evening will not take place.",
  "question": "According to the rules on the card, does the promise Wren made to restock the guest toiletries have any status except broken at the end of 2026-06-02?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q55de28cbc5",
  "kind": "choice",
  "text": "Freelance thread record, the online store move, shared by Elif.\n\nMembers: Rhea, Bruno, Femi, Elif\nChat log (oldest first):\n[27 May 2026] Bruno: Will attempt to add the size chart by 4 June 2026, can't promise.\n[27 May 2026] Rhea: @Femi Count on me to send the stock spreadsheet by 3 June 2026.\n[29 May 2026] Bruno: @Elif I'll add the size chart by 5 June 2026 as long as the market day is on.\n[31 May 2026] Femi: Afraid the market day is called off.\n[31 May 2026] Rhea: @Femi Quick question, could I send the stock spreadsheet by 7 June 2026 instead?\n[2 Jun 2026] Femi: @Rhea No new date, so please send the stock spreadsheet by the date given.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Bruno's commitment to add the size chart have at the end of 9 June 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not triggered",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qb08b32daf4",
  "kind": "yes/no",
  "text": "Chat attached to a support case about the campaign edit, shared by Ivo.\n\nMembers: Oskar, Malik, Greta, Ivo\nChat export (date | from | to | message):\n2026-06-29 | Ivo | Greta | Lovely, I'll send the colour notes by 3 July 2026 for sure.\n2026-06-29 | Ivo | Greta | Scratch that, I'm not going to send the colour notes\n2026-07-02 | Greta | Ivo | If the voiceover session goes ahead, I'll upload the render files by 7 July 2026.\n2026-07-03 | Malik | Ivo | If the agency review call goes ahead, I'll fetch the raw footage by 6 July 2026.\n2026-07-05 | Oskar | group | Team, the agency review call stays on as booked.\n2026-07-07 | Malik | Ivo | For the record: I was able to fetch the raw footage",
  "question": "By the close of 9 July 2026, is the promise Malik made to fetch the raw footage kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q50571e6855",
  "kind": "yes/no",
  "text": "Export from the support queue, covering the lab move; passed on by Mo.\n\nMembers: Tess, Omar, Nadia, Mo\nChat log (oldest first):\n[14 Apr 2026] Mo: @Tess Absolutely, I will submit the ethics application by 17 April 2026.\n[14 Apr 2026] Nadia: I'll try to book the microscope slot by 17 April 2026.\n[16 Apr 2026] Nadia: @Omar I'll book the microscope slot by 19 April 2026, provided the conference trip happens.\n[18 Apr 2026] Tess: Fab, we are on for the conference trip as planned!\n[18 Apr 2026] Nadia: @Omar Mind giving me until 23 April 2026 to book the microscope slot?\n[19 Apr 2026] Tess: @Nadia Ah, no stress, no need for you to book the microscope slot",
  "question": "Does the card's rule set show that Nadia has not kept the promise to book the microscope slot at the end of 24 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc246eb5b28",
  "kind": "yes/no",
  "text": "Support: help desk chat\nSubject: the training plan\nSaved by: Kofi\n\nMembers: Femi, Kofi, Yuki\nChat log (oldest first):\n[27 Apr 2026] Femi: @Yuki Count on me to return the loaned helmets by 5 May 2026.\n[1 May 2026] Femi: @Yuki I will fetch the bike stand by 8 May 2026 only if the hill climb happens.\n[4 May 2026] Kofi: @Femi Good news, you're let off having to return the loaned helmets\n[7 May 2026] Yuki: Sad to report that the hill climb is off.\n[10 May 2026] Femi: @Yuki Mum, I did return the loaned helmets, haha.",
  "question": "According to the rules on the card, does the promise Femi made to return the loaned helmets have any status except broken at the end of 9 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc257ff1178",
  "kind": "yes/no",
  "text": "Shared by Malik, this back and forth with the client covers the online store move.\n\nMembers: Jonas, Zara, Wren, Malik\nChat log (oldest first):\n[24 Apr 2026] Jonas: @Zara You can bank on me to renew the hosting plan by 30 April 2026.\n[25 Apr 2026] Jonas: @Malik I promise to fix the checkout button by 29 April 2026 if the stock count is on.\n[29 Apr 2026] Malik: @Zara I'll update the product photos by 3 May 2026 if the market day goes ahead.\n[29 Apr 2026] Jonas: Team, the market day stays on as booked.\n[30 Apr 2026] Jonas: @Zara Is 2 May 2026 alright for me to renew the hosting plan?\n[30 Apr 2026] Zara: @Jonas Fine by me, you can renew the hosting plan by 2 May 2026.",
  "question": "Is the promise Malik made to update the product photos not kept by 2 May 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q724ad15860",
  "kind": "choice",
  "text": "Greta saved these replies from the agent on the autumn term budget.\n\nMembers: Yuki, Omar, Leila, Greta\nChat log (oldest first):\n[26 Oct 2026] Leila: @Greta Count on me to print the tenancy agreement by 31 Oct 2026.\n[26 Oct 2026] Omar: @Leila You don't have to print the tenancy agreement at all\n[27 Oct 2026] Leila: @Omar Count on me, I'll send the deposit receipt by 5 Nov 2026.\n[28 Oct 2026] Yuki: @Leila As long as the agent inventory walk is on, I'll forward the inventory photos by 4 Nov 2026.\n[1 Nov 2026] Yuki: Sorry all, the agent inventory walk is called off.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Yuki's promise to forward the inventory photos at the end of 5 Nov 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Not yet due",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q757a8bfc63",
  "kind": "choice",
  "text": "Subject: Chat about the home adaptations\nThe copy from Lee follows below as a plain record.\n\nMembers: Omar, Oskar, Elif, Lee\nChat log (oldest first):\n[6 Feb 2026] Oskar: @Elif Only if the hospital appointment is on, I will call the home nurse by 14 February 2026.\n[8 Feb 2026] Elif: @Oskar As long as the physio session is on, I will print the care schedule by 14 February 2026.\n[8 Feb 2026] Elif: @Omar It's on me to book the clinic transport by 13 February 2026.\n[10 Feb 2026] Omar: @Elif Good news, you're let off having to book the clinic transport\n[10 Feb 2026] Elif: Yay, the hospital appointment is all set to go!\n[10 Feb 2026] Lee: @Elif I own this, I'll collect the post by 19 February 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Elif made to book the clinic transport at the end of 14 February 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Kept",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qd5ff196a58",
  "kind": "yes/no",
  "text": "{\"saved_copy\": \"the loft conversion\", \"keeper\": \"Priya\", \"medium\": \"chat transcript\"}\n\nMembers: Ivo, Femi, Ines, Priya\nChat export (date | from | to | message):\n2026-02-01 | Ines | Ivo | Relax, I'll collect the sanding pads by 5 February 2026, promise.\n2026-02-03 | Ines | Femi | I'll scrape the old wallpaper by 5 February 2026, providing the boiler install visit goes ahead.\n2026-02-03 | Priya | group | Please note the boiler install visit will proceed.\n2026-02-04 | Ines | Femi | Got it, I'll hang the new curtain rail by 7 February 2026 for sure.\n2026-02-07 | Ines | Priya | I will pick up the grout bag by 16 February 2026 only if the damp survey inspection happens.\n2026-02-07 | Femi | Ines | No worries, you don't need to hang the new curtain rail",
  "question": "Is it true that the promise Ines made to hang the new curtain rail has not been broken at the end of 7 February 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q92902f1756",
  "kind": "yes/no",
  "text": "Forwarded by Malik, this thread on the office refit stays attached to the ticket.\n\nMembers: Elif, Bruno, Malik, Wren\nChat log (oldest first):\n[14 Apr 2026] Bruno: @Malik If the lease viewing goes ahead, I'll renew the fire extinguisher service by 21 April 2026.\n[14 Apr 2026] Wren: Update: the lease viewing is going ahead as planned.\n[15 Apr 2026] Malik: Just checking in, did you manage to renew the fire extinguisher service?\n[16 Apr 2026] Wren: @Bruno Count on me, I'll return the printer toner by 20 April 2026.\n[20 Apr 2026] Elif: @Malik Got it, I'll print the staff rota by 28 April 2026 for sure.\n[20 Apr 2026] Bruno: @Malik Got myself to renew the fire extinguisher service lol.",
  "question": "Was the promise to renew the fire extinguisher service from Bruno kept on 25 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6035015e88",
  "kind": "yes/no",
  "text": "Subject: export of the group chat on the gallery show\nHere is the chat as saved by Bruno, pasted below.\n\nMembers: Bruno, Tomas\nChat log (oldest first):\n[14 Jan 2026] Tomas: @Bruno I'll mail the business cards by 20 Jan 2026 if the sign reveal goes ahead.\n[15 Jan 2026] Tomas: @Bruno Relax, I'll upload the sticker artwork by 18 Jan 2026, promise.\n[15 Jan 2026] Tomas: @Bruno Guess what, I managed to upload the sticker artwork!\n[15 Jan 2026] Tomas: On track for the sign reveal to happen as planned.\n[16 Jan 2026] Tomas: @Bruno Ta-da, I went and did it: mail the business cards!",
  "question": "According to the rules on the card, does the promise Tomas made to mail the business cards have any status except broken at the end of 17 Jan 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q624e580321",
  "kind": "choice",
  "text": "Subject: forwarded chat, the balcony garden project\nWord for word, the text below came from the saved copy.\nBest, Jonas\n\nMembers: Bruno, Jonas, Ravi\nChat log (oldest first):\n[15 Mar 2026] Bruno: @Ravi Provided the flat viewing day happens, I'll email the leak photos by 19 Mar 2026.\n[15 Mar 2026] Bruno: @Ravi I'll ring the flat repair line by 22 Mar 2026, promise.\n[18 Mar 2026] Jonas: @Bruno Guaranteed I'll drop the bin bags off by 24 Mar 2026.\n[19 Mar 2026] Jonas: @Bruno I'll forward the gas bill by 21 Mar 2026, provided the electrics safety check happens.\n[20 Mar 2026] Bruno: @Ravi Mum, I did ring the flat repair line, haha.\n[24 Mar 2026] Bruno: @Jonas Forget it, you won't need to drop the bin bags off",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Jonas's promise to drop the bin bags off at the end of 29 Mar 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qa46f703e63",
  "kind": "yes/no",
  "text": "Flat chat export, saved by Ana\nCovers the balcony garden project, shared among the housemates.\n\nMembers: Oskar, Ana\nChat log (oldest first):\n[24 Jun 2026] Ana: @Oskar I'll ring the flat repair line by Friday, 26 June 2026 if the boiler annual check goes ahead.\n[24 Jun 2026] Oskar: Team, the boiler annual check is not happening.\n[25 Jun 2026] Ana: @Oskar Count on me to collect the spare flat keys by Sunday, 28 June 2026.\n[25 Jun 2026] Ana: @Oskar Quick question, could I collect the spare flat keys by Saturday, 4 July 2026 instead?\n[26 Jun 2026] Ana: @Oskar Guess what, I managed to collect the spare flat keys!\n[27 Jun 2026] Oskar: @Ana I promise to measure the kitchen for fridge by Wednesday, 1 July 2026.",
  "question": "Has Ana kept the promise to collect the spare flat keys as of Sunday, 28 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qcb44067b2c",
  "kind": "yes/no",
  "text": "Ivo shared this so the allotment expansion is easy to find, flatmates.\n\nMembers: Ivo, Ines, Jonas\nChat log (oldest first):\n[4 Jul 2026] Ines: @Jonas You can bank on me to build the compost bay by Monday, 6 July 2026.\n[5 Jul 2026] Ines: @Ivo I promise to weed the carrot row by Thursday, 9 July 2026.\n[6 Jul 2026] Ivo: Where are you up to with plans to weed the carrot row?\n[7 Jul 2026] Jonas: @Ivo Lovely, I'll sow the broad beans by Saturday, 11 July 2026 if the harvest supper is on.\n[8 Jul 2026] Ines: @Jonas Provided the allotment site visit happens, I will sharpen the hand hoe by Wednesday, 15 July 2026.\n[9 Jul 2026] Ines: @Ivo For the record: I was able to weed the carrot row",
  "question": "Going by the card's rules, does Ines not keep the promise to weed the carrot row at the end of Friday, 10 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qabaf4b76ea",
  "kind": "choice",
  "text": "Saved by Femi: a freelancer's exchange with a client over the holiday catalogue.\n\nMembers: Sami, Malik, Femi\nChat log (oldest first):\n[26 Jun 2026] Malik: @Femi Lovely, I'll restore the old theme by 29 June 2026 if the courier pickup is on.\n[29 Jun 2026] Sami: @Femi Count on me to set up the email forwarding by 7 July 2026.\n[29 Jun 2026] Sami: @Malik I'll update the product photos by 3 July 2026 if the stock count goes ahead.\n[1 Jul 2026] Sami: Sadly, the stock count is not going ahead.\n[2 Jul 2026] Sami: @Malik Count on me, I'll fix the checkout button by 8 July 2026.\n[9 Jul 2026] Sami: @Femi Log entry: set up the email forwarding, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Sami gave to update the product photos have at the end of 5 July 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Broken",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "q066a02401f",
  "kind": "yes/no",
  "text": "We are getting ready for the allotment expansion, and Dara shared this chat with us.\n\nMembers: Ana, Dara, Ines\nChat log (oldest first):\n[12 May 2026] Ines: @Ana Might manage to weed the carrot row by 22 May 2026, who knows.\n[12 May 2026] Ana: @Ines Count on me, I'll collect the seed potatoes by 20 May 2026.\n[14 May 2026] Ines: @Dara You can bank on me to weed the carrot row by 18 May 2026.\n[17 May 2026] Ines: @Ana Count on me to sharpen the hand hoe by 19 May 2026, if the village flower show happens.\n[17 May 2026] Dara: Fab, we are on for the village flower show as planned!\n[18 May 2026] Ines: @Dara To note: I have managed to weed the carrot row",
  "question": "On the card, was Ines's promise to weed the carrot row broken, waived, not triggered or not yet due, rather than kept, at the end of 18 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa0ad42e01e",
  "kind": "yes/no",
  "text": "Support: help desk chat\nSubject: the care plan\nSaved by: Lee\n\nMembers: Leila, Lee, Nadia, Zara\nChat log (oldest first):\n[25 Jul 2026] Nadia: @Leila You can bet I'll call the home nurse by 29 July 2026.\n[26 Jul 2026] Lee: @Nadia It's on me to book the clinic transport by 3 August 2026.\n[26 Jul 2026] Leila: @Nadia Count on me to print the care schedule by 1 August 2026 if the family care meeting is on.\n[31 Jul 2026] Zara: Yay, the family care meeting is all set to go!\n[1 Aug 2026] Leila: @Nadia Gutted to say I won't print the care schedule, sorry team",
  "question": "By the close of 4 August 2026, is the promise Leila made to print the care schedule kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8ffd833877",
  "kind": "choice",
  "text": "Household chat saved by Tomas, with the kitchen refit at its heart.\n\nMembers: Tomas, Priya, Ravi\nChat log (oldest first):\n[9 Apr 2026] Tomas: @Ravi If the boiler annual check goes ahead, I'll wipe the cooker hood by 12 April 2026.\n[11 Apr 2026] Priya: @Tomas I will ring the flat repair line by 16 April 2026.\n[12 Apr 2026] Ravi: @Priya Absolutely, I will email the leak photos by 19 April 2026.\n[13 Apr 2026] Ravi: @Tomas As long as the window cleaner visit is on, I'll measure the kitchen for fridge by 21 April 2026.\n[15 Apr 2026] Ravi: @Priya Guess what, I managed to email the leak photos!\n[17 Apr 2026] Priya: @Tomas Ta-da, I went and did it: ring the flat repair line!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Priya gave to ring the flat repair line have at the end of 20 April 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Broken",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "qffe8ad8233",
  "kind": "choice",
  "text": "Subject: Chat about the packing plan\nBelow is a copy that came from Oskar, pasted as found.\n\nMembers: Ines, Oskar, Tomas, Ivo\nChat export (date | from | to | message):\n2026-08-14 | Oskar | Ines | Count on me to send the packing list by 24 Aug 2026 if the guided tour is on.\n2026-08-17 | Ivo | Tomas | Guaranteed I'll check the passport copies by 20 Aug 2026.\n2026-08-18 | Ines | Tomas | Lovely, I'll pack the travel adaptors by 25 Aug 2026 if the beach picnic is on.\n2026-08-20 | Ivo | Tomas | Is it all right if I check the passport copies by 23 Aug 2026 instead?\n2026-08-20 | Ines | Ivo | Revised deadline is 23 Aug 2026, so you can check the passport copies.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Ivo made to check the passport copies at the end of 20 Aug 2026?",
  "options": [
   "Waived",
   "Broken",
   "Kept",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q3fa75ad851",
  "kind": "yes/no",
  "text": "Posted by Greta from the work channel: the grant renewal.\n\nMembers: Jonas, Lena, Greta\nChat log (oldest first):\n[23 Apr 2026] Greta: @Lena I promise to scan the field notes by 25 Apr 2026 if the grant panel is on.\n[25 Apr 2026] Jonas: @Greta I'll book the microscope slot by 28 Apr 2026, providing the conference trip goes ahead.\n[25 Apr 2026] Greta: On track for the conference trip to happen as planned.\n[27 Apr 2026] Greta: @Jonas Got it, I'll fetch the grant forms by 3 May 2026 for sure.\n[3 May 2026] Greta: @Jonas Is 8 May 2026 alright for me to fetch the grant forms?\n[3 May 2026] Jonas: @Greta The original date stands, so you need to fetch the grant forms.",
  "question": "On 29 Apr 2026, would you say Jonas kept the promise to book the microscope slot, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1bf740f4c0",
  "kind": "yes/no",
  "text": "{\"saved_copy\": \"the visitor policy\", \"keeper\": \"Sami\", \"medium\": \"chat transcript\"}\n\nMembers: Sami, Jonas, Lee, Nadia\nChat log (oldest first):\n[26 Jun 2026] Nadia: @Jonas Guaranteed I'll set up the reception screen by Monday, 29 June 2026.\n[28 Jun 2026] Lee: @Nadia Provided the team lunch happens, I'll book the boardroom by Tuesday, 30 June 2026.\n[28 Jun 2026] Jonas: Update, the team lunch will not take place.\n[29 Jun 2026] Jonas: @Lee I will make sure to renew the fire extinguisher service by Tuesday, 7 July 2026.\n[30 Jun 2026] Nadia: @Jonas I'll print the staff rota by Thursday, 2 July 2026, provided the lease viewing happens.\n[7 Jul 2026] Jonas: @Lee To my relief, I managed to renew the fire extinguisher service.",
  "question": "Under the rules on the card, is the promise Jonas made to renew the fire extinguisher service kept as of Saturday, 11 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qed71047c68",
  "kind": "yes/no",
  "text": "Subject: Chat about the street watch scheme\nBelow is a copy that came from Wren, pasted as found.\n\nMembers: Ana, Malik, Lena, Wren\nChat log (oldest first):\n[20 Mar 2026] Ana: Maybe I can return the ladders by Monday, 30 March 2026.\n[21 Mar 2026] Ana: @Wren I'll return the ladders by Thursday, 26 March 2026, providing the hedge trimming day goes ahead.\n[22 Mar 2026] Lena: @Wren Relax, I'll feed the cat across the road by Monday, 30 March 2026, promise.\n[23 Mar 2026] Ana: Yay, the hedge trimming day is all set to go!\n[23 Mar 2026] Ana: @Wren Is it all right if I return the ladders by Sunday, 29 March 2026 instead?\n[23 Mar 2026] Wren: @Ana Not moving it, return the ladders by the existing date.",
  "question": "Is the promise Ana made to return the ladders something that has not been broken at the end of Thursday, 26 March 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3c41ed9d66",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the sound mix\nFrom Femi, the thread below is passed on in its original form.\n\nMembers: Kai, Ivo, Femi\nChat log (oldest first):\n[28 Sep 2026] Kai: @Femi Absolutely, I will send the colour notes by October 3, 2026.\n[1 Oct 2026] Ivo: @Femi I'll be sure to back up the project drives by October 8, 2026.\n[2 Oct 2026] Femi: @Ivo Ah, no stress, no need for you to back up the project drives\n[2 Oct 2026] Ivo: @Femi Count on me to label the clip folders by October 4, 2026, if the client screening happens.\n[2 Oct 2026] Kai: Brilliant news everyone, the client screening is a go!\n[3 Oct 2026] Kai: @Femi If the voiceover session goes ahead, I'll gladly ship the hard drive by October 9, 2026.",
  "question": "Did Ivo keep the promise to back up the project drives on October 6, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd7ff1e86bf",
  "kind": "choice",
  "text": "Export from the shared home\nAbout the kitchen garden project, sent over by Zara.\n\nMembers: Leila, Hana, Zara, Kofi\nChat log (oldest first):\n[17 Sep 2026] Zara: @Leila Committing to sow the broad beans by Friday, 25 September 2026.\n[18 Sep 2026] Zara: @Leila Any chance I can sow the broad beans by Thursday, 1 October 2026 instead?\n[19 Sep 2026] Kofi: @Zara Yes, all good for you to sow the broad beans by Thursday, 1 October 2026 instead.\n[21 Sep 2026] Zara: @Hana You can bank on me to sharpen the hand hoe by Monday, 28 September 2026.\n[22 Sep 2026] Hana: @Zara If the allotment site visit is on, I'll definitely fix the shed door by Monday, 28 September 2026.\n[23 Sep 2026] Zara: Update, the allotment site visit will not take place.\n[26 Sep 2026] Zara: @Leila Mum, I did sow the broad beans, haha.\n[28 Sep 2026] Leila: @Zara Don't sweat it, there's no need to sharpen the hand hoe",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Zara due to sow the broad beans at the end of Sunday, 4 October 2026, after any agreed rescheduling?",
  "options": [
   "Friday, 25 September 2026",
   "Thursday, 1 October 2026",
   "Monday, 28 September 2026"
  ]
 },
 {
  "qid": "qf5c376e599",
  "kind": "choice",
  "text": "Posted by Dara from the work channel, the field survey thread.\n\nMembers: Mo, Dara, Nadia\nChat log (oldest first):\n[11 Apr 2026] Nadia: @Mo Count on me, I'll book the microscope slot by 13 Apr 2026.\n[11 Apr 2026] Nadia: @Mo Would it be fine if I book the microscope slot by 15 Apr 2026 instead, yeah?\n[11 Apr 2026] Mo: @Nadia Nah, the date's staying put, so you can book the microscope slot.\n[12 Apr 2026] Nadia: @Dara Promise to collect the lab samples by 16 Apr 2026 if the safety inspection goes ahead.\n[13 Apr 2026] Dara: Scrapping the safety inspection, apologies to all.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Nadia's promise to collect the lab samples at the end of 17 Apr 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q2f4811a3ff",
  "kind": "yes/no",
  "text": "Subject: Chat about the garden makeover\nBelow, with Priya named as the source, is the chat as exported.\n\nMembers: Priya, Ivo, Ravi, Yuki\nChat export (date | from | to | message):\n2026-04-04 | Priya | Yuki | Lovely, I'll measure the hallway for shelves by 8 Apr 2026 if the mortgage valuation visit is on.\n2026-04-05 | Priya | Yuki | Guaranteed I'll print the floor plan by 9 Apr 2026.\n2026-04-07 | Ravi | Ivo | I will make sure to pay the plumbing invoice by 10 Apr 2026.\n2026-04-09 | Priya | Yuki | Scratch what I said, I won't print the floor plan.\n2026-04-09 | Ravi | Priya | No worries, you don't need to print the floor plan\n2026-04-11 | Ivo | Yuki | I promise to fetch the paint samples by 14 Apr 2026 if the builder quote meeting is on.",
  "question": "Applying the rules on the card, has Priya kept the promise to print the floor plan as of 13 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1e18cf567f",
  "kind": "yes/no",
  "text": "A short note above messages between tenants and the landlord about the flatmate contract terms, saved by Leila.\n\nMembers: Leila, Hana, Jonas, Kofi\nChat log (oldest first):\n[10 Oct 2026] Kofi: @Hana Committing to print the tenancy agreement by 17 Oct 2026.\n[13 Oct 2026] Jonas: @Leila Count on me to copy the house keys by 15 Oct 2026, if the move in day happens.\n[15 Oct 2026] Hana: @Kofi Count on me, I'll collect the parcel from porch by 21 Oct 2026.\n[15 Oct 2026] Jonas: @Leila As long as the check in visit is on, I'll store the spare bike by 17 Oct 2026.\n[15 Oct 2026] Jonas: Really pleased to say the check in visit will go ahead!\n[21 Oct 2026] Hana: @Kofi Ta-da, I went and did it: collect the parcel from porch!",
  "question": "According to the card's rules, is the promise Hana made to collect the parcel from porch not kept as of 24 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe3adb40f4c",
  "kind": "choice",
  "text": "Project log\nClient and freelancer messages on the rebrand package, saved by Kofi.\n\nMembers: Priya, Omar, Kofi\nChat log (oldest first):\n[26 Oct 2026] Kofi: @Priya I'll sketch the packaging mockup by 28 October 2026, provided the print run happens.\n[27 Oct 2026] Omar: @Kofi Lovely, I'll pick the colour swatches by 4 November 2026 if the shop fitting is on.\n[29 Oct 2026] Priya: @Omar I will make sure to upload the sticker artwork by 1 November 2026.\n[29 Oct 2026] Kofi: @Priya I assure you I'll mail the business cards by 6 November 2026 if the brand review call is on.\n[1 Nov 2026] Kofi: @Priya You are released, no requirement to upload the sticker artwork.\n[1 Nov 2026] Priya: @Omar Ticked off my list: upload the sticker artwork, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Priya's commitment to upload the sticker artwork is in what status at the end of 3 November 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q4b04b9a241",
  "kind": "choice",
  "text": "Housemates' chat about the house rules debate, saved on Bruno's device.\n\nMembers: Bruno, Malik, Rhea\nChat log (oldest first):\n[21 Jan 2026] Rhea: @Malik Lovely, I'll scrub the cellar steps by Friday, 30 January 2026 for sure.\n[21 Jan 2026] Bruno: @Rhea I will bleed the attic radiators by Sunday, 25 January 2026 only if the heritage fete happens.\n[22 Jan 2026] Malik: Team, the heritage fete is not happening.\n[22 Jan 2026] Bruno: @Rhea Think Thursday, 29 January 2026 would work if I bleed the attic radiators instead?\n[23 Jan 2026] Rhea: @Bruno Yes, you can bleed the attic radiators by Thursday, 29 January 2026 if that suits you.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Bruno's promise to bleed the attic radiators at the end of Wednesday, 28 January 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q2e059d6edb",
  "kind": "choice",
  "text": "Export from the support queue, covering the payment setup; passed on by Kofi.\n\nMembers: Kofi, Ana, Femi, Jonas\nChat log (oldest first):\n[23 Jun 2026] Jonas: @Kofi I'll print the packing slips by Thursday, 25 June 2026, provided the courier pickup happens.\n[24 Jun 2026] Jonas: @Femi If the stock count goes ahead, I'll update the product photos by Saturday, 27 June 2026.\n[24 Jun 2026] Femi: Sad to report that the stock count is off.\n[25 Jun 2026] Ana: @Kofi You can bank on me to renew the hosting plan by Sunday, 28 June 2026.\n[27 Jun 2026] Jonas: @Kofi Count on me to restore the old theme by Saturday, 4 July 2026.\n[29 Jun 2026] Jonas: @Kofi To note: I have managed to restore the old theme",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Jonas's pledge to update the product photos at the end of Wednesday, 24 June 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Broken",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q06d60ac92c",
  "kind": "yes/no",
  "text": "{\"chat_export\": \"the visitor policy\", \"saved_by\": \"Zara\", \"scope\": \"group chat\"}\n\nMembers: Lee, Zara, Tess, Leila\nChat log (oldest first):\n[8 May 2026] Tess: @Zara If the annual audit goes ahead, I'll gladly set up the reception screen by 2026-05-15.\n[12 May 2026] Lee: @Zara If the lease viewing is on, I'll definitely replace the kitchen filters by 2026-05-17.\n[13 May 2026] Tess: @Zara Lovely, I'll print the staff rota by 2026-05-21 for sure.\n[16 May 2026] Zara: Really pleased to say the lease viewing will go ahead!\n[17 May 2026] Lee: @Zara On my action item, may I replace the kitchen filters by 2026-05-19 instead?\n[17 May 2026] Lee: @Zara To note: I have managed to replace the kitchen filters",
  "question": "Does Lee's promise to replace the kitchen filters hold up as kept at the end of 2026-05-19, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qae2fa03f66",
  "kind": "yes/no",
  "text": "Support thread for a help desk case, covering the rebrand package, saved by Leila.\n\nMembers: Leila, Wren, Kofi\nChat log (oldest first):\n[3 Aug 2026] Kofi: @Leila I will make sure to check the poster proofs by 6 August 2026.\n[4 Aug 2026] Wren: @Kofi Got it, I'll sketch the packaging mockup by 7 August 2026 for sure.\n[7 Aug 2026] Kofi: Hey, any luck with trying to sketch the packaging mockup?\n[7 Aug 2026] Leila: @Wren Provided the brand review call happens, I'll fetch the brand fonts by 12 August 2026.\n[7 Aug 2026] Wren: @Kofi Ticked off my list: sketch the packaging mockup, yay.\n[8 Aug 2026] Wren: Great news, the brand review call is on!",
  "question": "Would you say Wren kept the promise to sketch the packaging mockup at the end of 8 August 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qee630e588b",
  "kind": "yes/no",
  "text": "Committee chat on the playground project, shared by Yuki with the volunteers.\n\nMembers: Oskar, Yuki, Jonas, Tess\nChat export (date | from | to | message):\n2026-03-27 | Tess | Yuki | I'll set up the book stall by 29 Mar 2026, promise.\n2026-03-28 | Oskar | Yuki | I will make sure to send the newsletter drafts by 5 Apr 2026.\n2026-03-29 | Yuki | Jonas | Provided the clothes swap happens, I will return the borrowed trestle tables by 3 Apr 2026.\n2026-04-02 | Tess | group | Update, the clothes swap will not take place.\n2026-04-05 | Oskar | Yuki | Got myself to send the newsletter drafts lol.",
  "question": "Has Oskar not kept the promise to send the newsletter drafts at the end of 5 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd34e3863a4",
  "kind": "yes/no",
  "text": "Support thread for a help desk case, covering the loft conversion, saved by Ravi.\n\nMembers: Jonas, Bruno, Kai, Ravi\nChat export (date | from | to | message):\n2026-04-15 | Ravi | Kai | I'll sweep the dust from stairs by 23 Apr 2026 if the damp survey inspection goes ahead.\n2026-04-15 | Bruno | Ravi | You can bank on me to pay the plumbing invoice by 24 Apr 2026.\n2026-04-17 | Ravi | Kai | Count on me to measure the hallway for shelves by 24 Apr 2026, if the removal van arrival happens.\n2026-04-22 | Ravi | group | We are dropping the damp survey inspection from the list.\n2026-04-22 | Ravi | Kai | Quick question, could I sweep the dust from stairs by 26 Apr 2026 instead?\n2026-04-22 | Kai | Ravi | Yes, all good for you to sweep the dust from stairs by 26 Apr 2026 instead.",
  "question": "Going by the card's rules, does Ravi not keep the promise to sweep the dust from stairs at the end of 23 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc88e86d61a",
  "kind": "choice",
  "text": "Messages with the letting agent about the attic conversion idea, saved by Wren for the rental file.\n\nMembers: Wren, Tomas, Lena, Leila\nChat export (date | from | to | message):\n2026-04-26 | Leila | Wren | I'll replace the loo roll by 4 May 2026 as long as the lodger house supper is on.\n2026-04-28 | Leila | group | Sorry, the lodger house supper is off.\n2026-04-29 | Tomas | Wren | Guaranteed I'll sort the recycling bags by 5 May 2026.\n2026-04-29 | Leila | Tomas | Please don't feel you have to sort the recycling bags\n2026-05-01 | Lena | Tomas | Absolutely, I will stock the spice rack by 9 May 2026.\n2026-05-01 | Lena | Tomas | I need to take back my commitment to stock the spice rack.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Leila's promise to replace the loo roll at the end of 5 May 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Broken",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q2ebcb7e22f",
  "kind": "choice",
  "text": "Export from the shared home\nAbout the kitchen garden project, sent over by Zara.\n\nMembers: Leila, Hana, Zara, Kofi\nChat log (oldest first):\n[17 Sep 2026] Zara: @Leila Committing to sow the broad beans by Friday, 25 September 2026.\n[18 Sep 2026] Zara: @Leila Any chance I can sow the broad beans by Thursday, 1 October 2026 instead?\n[19 Sep 2026] Leila: @Zara Yes, all good for you to sow the broad beans by Thursday, 1 October 2026 instead.\n[21 Sep 2026] Zara: @Hana You can bank on me to sharpen the hand hoe by Monday, 28 September 2026.\n[22 Sep 2026] Hana: @Zara If the allotment site visit is on, I'll definitely fix the shed door by Monday, 28 September 2026.\n[23 Sep 2026] Zara: Update, the allotment site visit will not take place.\n[26 Sep 2026] Zara: @Leila Mum, I did sow the broad beans, haha.\n[28 Sep 2026] Leila: @Zara Don't sweat it, there's no need to sharpen the hand hoe",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Zara due to sow the broad beans at the end of Sunday, 4 October 2026, after any agreed rescheduling?",
  "options": [
   "Friday, 25 September 2026",
   "Monday, 28 September 2026",
   "Thursday, 1 October 2026"
  ]
 }
]
