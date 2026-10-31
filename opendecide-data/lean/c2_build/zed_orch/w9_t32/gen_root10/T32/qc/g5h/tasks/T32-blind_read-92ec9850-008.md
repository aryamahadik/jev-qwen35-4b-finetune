# G5-H blind read (all free-form rows) T32-blind_read-92ec9850-008 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root10/T32/qc/g5h/answers/T32-blind_read-92ec9850-008.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 29. Answers expected: 29 (one per item, each with that item's qid).

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
  "qid": "qd5969b0380",
  "kind": "choice",
  "text": "Here we plan the house rules debate together, and Sami saved this for the family.\n\nMembers: Sami, Leila, Tomas\nChat log (oldest first):\n[16 Sep 2026] Sami: @Leila I will find the loft ladder by 26 September 2026.\n[20 Sep 2026] Leila: @Tomas If the loft clearance day goes ahead, I'll gladly mend the garden gate by 25 September 2026.\n[22 Sep 2026] Sami: @Leila To my relief, I managed to find the loft ladder.\n[22 Sep 2026] Tomas: Fab, we are on for the loft clearance day as planned!\n[25 Sep 2026] Tomas: @Leila Quick update: you do not need to mend the garden gate at all.\n[27 Sep 2026] Tomas: Quick check, any update on plans to mend the garden gate?",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Leila's pledge to mend the garden gate at the end of 24 September 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Broken",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q304c1ba930",
  "kind": "choice",
  "text": "Volunteers, this is the playground project thread that Sami shared with the committee.\n\nMembers: Jonas, Sami, Tess\nChat export (date | from | to | message):\n2026-04-02 | Tess | Sami | Absolutely, I will send the newsletter drafts by 4 Apr 2026.\n2026-04-03 | Jonas | Sami | Provided the reading festival happens, I'll set up the book stall by 11 Apr 2026.\n2026-04-06 | Jonas | group | Great news, the reading festival is on!\n2026-04-06 | Tess | Jonas | You don't have to set up the book stall at all\n2026-04-07 | Jonas | Sami | Ticked off: set up the book stall, feels so good",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Jonas gave to set up the book stall have at the end of 6 Apr 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Broken",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q01b40bc34c",
  "kind": "yes/no",
  "text": "Forwarded by Jonas: a help-desk thread covering the reunion weekend.\n\nMembers: Leila, Jonas\nChat log (oldest first):\n[12 Apr 2026] Leila: Will attempt to buy the name tags by 16 Apr 2026, can't promise.\n[13 Apr 2026] Leila: @Jonas Provided the karaoke night happens, I will buy the name tags by 20 Apr 2026.\n[18 Apr 2026] Leila: Yep, the karaoke night is on as planned.\n[19 Apr 2026] Jonas: @Leila I will send the group invitations by 21 Apr 2026.\n[21 Apr 2026] Jonas: @Leila Scratch what I said, I won't send the group invitations.\n[26 Apr 2026] Leila: @Jonas Mum, I did buy the name tags, haha.",
  "question": "Is the promise to buy the name tags kept by Leila as of 23 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd717415f19",
  "kind": "choice",
  "text": "Shared by Bruno, a help-desk thread covering the guest welcome plan.\n\nMembers: Oskar, Femi, Kai, Bruno\nChat log (oldest first):\n[28 May 2026] Oskar: @Femi Promise to scrub the hot tub by 30 May 2026 if the check out clean goes ahead.\n[29 May 2026] Oskar: @Kai You can bet I'll change the lounge bulb by 1 June 2026.\n[31 May 2026] Kai: @Oskar I'll wash the beach towels by 9 June 2026, providing the summer season launch goes ahead.\n[1 Jun 2026] Bruno: Any news on plans to change the lounge bulb?\n[1 Jun 2026] Bruno: @Oskar No need to change the lounge bulb, I'm letting you off\n[1 Jun 2026] Femi: @Bruno I will make sure to wheel the bins out by 8 June 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Oskar's promise to change the lounge bulb at the end of 1 June 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qd5d8305344",
  "kind": "yes/no",
  "text": "Saved by Jonas, this talk about the summer visits is just for family.\n\nMembers: Sami, Jonas, Bruno\nChat log (oldest first):\n[18 Jun 2026] Jonas: @Sami As long as the storytime session is on, I'll teach the card game by 25 June 2026.\n[19 Jun 2026] Bruno: @Jonas Count on me to tidy the playroom by 23 June 2026 if the seaside outing is on.\n[19 Jun 2026] Jonas: @Sami As long as the garden tea party is on, I will read the bedtime story by 26 June 2026.\n[21 Jun 2026] Sami: @Bruno Relax, I'll bake the oat biscuits by 29 June 2026, promise.\n[25 Jun 2026] Sami: @Bruno Can I bake the oat biscuits by 3 July 2026 instead? I did promise, sorry.\n[29 Jun 2026] Sami: @Bruno To my relief, I managed to bake the oat biscuits.",
  "question": "By the close of 29 June 2026, is the promise Sami made to bake the oat biscuits kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q417b886ccf",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the big house plan\nFrom Lee, the thread below is passed on in its original form.\n\nMembers: Zara, Lee, Ivo\nChat log (oldest first):\n[13 Jul 2026] Ivo: @Lee I'll scrub the cellar steps by 21 Jul 2026, provided the loft clearance day happens.\n[15 Jul 2026] Ivo: @Lee See if I can bleed the attic radiators by 22 Jul 2026.\n[17 Jul 2026] Ivo: @Lee Guaranteed I'll bleed the attic radiators by 25 Jul 2026.\n[18 Jul 2026] Ivo: @Zara It's on me to oil the back door hinges by 24 Jul 2026.\n[19 Jul 2026] Ivo: Yep, the loft clearance day is on as planned.\n[19 Jul 2026] Ivo: @Lee My sincere apologies, I am unable to bleed the attic radiators.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status does the chat show for the promise Ivo made to bleed the attic radiators at the end of 21 Jul 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "qcf254dd54e",
  "kind": "choice",
  "text": "Attached chat: the new repertoire\nShared by: Lena.\n\nMembers: Ines, Lena, Oskar\nChat log (oldest first):\n[5 Aug 2026] Ines: @Oskar I will make sure to move the piano by 9 August 2026.\n[7 Aug 2026] Oskar: @Ines I assure you I'll return the library scores by 12 August 2026 if the sing along is on.\n[10 Aug 2026] Lena: Fab, we are on for the sing along as planned!\n[11 Aug 2026] Oskar: @Ines Would it be fine if I return the library scores by 14 August 2026 instead, yeah?\n[11 Aug 2026] Ines: @Oskar Of course, it is fine for you to return the library scores by 14 August 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Oskar's undertaking to return the library scores hold at the end of 12 August 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "q7ee242e871",
  "kind": "yes/no",
  "text": "Saved by Jonas, this talk about the summer visits is just for family.\n\nMembers: Sami, Jonas, Bruno\nChat log (oldest first):\n[18 Jun 2026] Jonas: @Sami As long as the storytime session is on, I'll teach the card game by 25 June 2026.\n[19 Jun 2026] Bruno: @Jonas Count on me to tidy the playroom by 23 June 2026 if the seaside outing is on.\n[19 Jun 2026] Jonas: @Sami As long as the garden tea party is on, I will read the bedtime story by 26 June 2026.\n[21 Jun 2026] Sami: @Bruno Relax, I'll bake the oat biscuits by 29 June 2026, promise.\n[25 Jun 2026] Sami: @Bruno Can I bake the oat biscuits by 3 July 2026 instead? I did promise, sorry.\n[29 Jun 2026] Sami: @Bruno To my relief, I managed to bake the oat biscuits.",
  "question": "Applying the card's rules, does Sami's promise to bake the oat biscuits count as broken, waived, not triggered or not yet due, rather than kept, as of 29 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q71f071ca17",
  "kind": "yes/no",
  "text": "Read up on the student house hunt, flatmates, as Arlo exported it.\n\nMembers: Arlo, Bruno, Dara, Kofi\nChat log (oldest first):\n[13 Sep 2026] Dara: @Kofi Provided the move in day happens, I will send the deposit receipt by 19 Sep 2026.\n[14 Sep 2026] Bruno: @Dara You can bank on me to ring the letting agent by 16 Sep 2026.\n[14 Sep 2026] Bruno: @Dara To note: I have managed to ring the letting agent\n[17 Sep 2026] Bruno: Just so you know, the move in day is on as scheduled.\n[20 Sep 2026] Dara: @Kofi For the record: I was able to send the deposit receipt",
  "question": "Would a check of the chat at the end of 22 Sep 2026 show the promise Dara made to send the deposit receipt as broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q447272777d",
  "kind": "yes/no",
  "text": "Parents and cousins, this is where we sort out the allotment expansion. Saved by Dara.\n\nMembers: Hana, Yuki, Dara\nChat log (oldest first):\n[22 Oct 2026] Dara: @Yuki I'll be sure to collect the seed potatoes by Thursday, October 29, 2026.\n[23 Oct 2026] Dara: @Yuki Think Sunday, November 1, 2026 would work if I collect the seed potatoes instead?\n[24 Oct 2026] Hana: @Dara I will deliver the surplus runner beans by Saturday, October 31, 2026 only if the plot inspection happens.\n[25 Oct 2026] Dara: Sorry, the plot inspection is off.\n[25 Oct 2026] Yuki: @Hana Promise to stake the tomato canes by Tuesday, October 27, 2026 if the harvest supper goes ahead.\n[26 Oct 2026] Dara: @Yuki Quick report: I've managed to collect the seed potatoes\n\nNote from Dara: guidance on dates in this chat is general, so they may shift without anyone's say-so.",
  "question": "Is Dara's promise to collect the seed potatoes kept on Wednesday, October 28, 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6cc0a03ec8",
  "kind": "choice",
  "text": "Omar shared this so the annual tour is easy to follow for the volunteers.\n\nMembers: Hana, Omar, Bruno\nChat log (oldest first):\n[23 Apr 2026] Hana: @Bruno Ticket's mine, I'll collect the timing tags by 26 April 2026.\n[25 Apr 2026] Hana: @Bruno Scratch that, I'm not going to collect the timing tags\n[26 Apr 2026] Omar: @Hana Promise to tune the gear cables by 3 May 2026 if the group ride goes ahead.\n[28 Apr 2026] Omar: Please note the group ride will proceed.\n[30 Apr 2026] Omar: @Hana Ticked off: tune the gear cables, feels so good\n\nRelayed by Omar from the pinned rules: promises made here need no review, because the chat itself is the record.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Omar's promise to tune the gear cables have at the end of 3 May 2026?",
  "options": [
   "Kept",
   "Waived",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qf00a01b74c",
  "kind": "choice",
  "text": "Shared by Ravi, this thread covers the documentary cut as pasted from email.\n\nMembers: Ravi, Jonas, Rhea, Leila\nChat export (date | from | to | message):\n2026-01-23 | Rhea | Jonas | You can bank on me to back up the project drives by 26 January 2026.\n2026-01-23 | Rhea | Leila | As long as the agency review call is on, I'll upload the render files by 30 January 2026.\n2026-01-25 | Ravi | Jonas | Got it, I'll label the clip folders by 30 January 2026 for sure.\n2026-01-26 | Rhea | Jonas | Guess what, I managed to back up the project drives!\n2026-01-28 | Jonas | Leila | I'll send the timeline export by 31 January 2026, provided the grading session happens.\n2026-01-30 | Rhea | group | Team, the grading session is not happening.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Rhea's promise to back up the project drives at the end of 28 January 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Not yet due",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q5bda202ff5",
  "kind": "choice",
  "text": "Volunteers, this is the sponsor search thread that Elif shared with the committee.\n\nMembers: Yuki, Rhea, Kai, Elif\nChat log (oldest first):\n[1 Sep 2026] Elif: @Kai I will pump the spare tyres by 4 September 2026 only if the group ride happens.\n[1 Sep 2026] Elif: @Kai If the mechanics clinic goes ahead, I'll print the route cards by 8 September 2026.\n[1 Sep 2026] Yuki: @Kai It's on me to fetch the bike stand by 8 September 2026.\n[2 Sep 2026] Yuki: We are dropping the group ride from the list.\n[7 Sep 2026] Rhea: @Yuki I own this, I'll collect the timing tags by 13 September 2026.\n[7 Sep 2026] Rhea: @Yuki To note: I have managed to collect the timing tags",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status does the chat show for the promise Elif made to pump the spare tyres at the end of 3 September 2026?",
  "options": [
   "Broken",
   "Kept",
   "Waived",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q01bf82097d",
  "kind": "choice",
  "text": "We are getting ready for the garden shed build, and Arlo shared this chat with us.\n\nMembers: Kofi, Arlo, Omar, Elif\nChat log (oldest first):\n[22 Sep 2026] Kofi: @Elif It's on me to build the compost bay by 1 October 2026.\n[24 Sep 2026] Omar: @Arlo Count on me to weed the carrot row by 28 September 2026 if the water tank delivery is on.\n[24 Sep 2026] Arlo: Got it, thanks a lot.\n[24 Sep 2026] Kofi: We are dropping the water tank delivery from the list.\n[26 Sep 2026] Kofi: @Omar Guaranteed I'll dig the potato patch by 4 October 2026.\n[28 Sep 2026] Kofi: @Elif Mum, I did build the compost bay, haha.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Omar doing with the promise to weed the carrot row at the end of 1 October 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "q0ebc8ec596",
  "kind": "choice",
  "text": "Attached chat: the tenancy renewal talks\nShared by: Kofi.\n\nMembers: Wren, Tomas, Kofi, Arlo\nChat log (oldest first):\n[9 Jan 2026] Kofi: @Arlo I own this, I'll wipe the cooker hood by 13 January 2026.\n[9 Jan 2026] Tomas: @Arlo As long as the flat viewing day is on, I will forward the gas bill by 16 January 2026.\n[10 Jan 2026] Arlo: @Kofi Good news, you're let off having to wipe the cooker hood\n[11 Jan 2026] Kofi: Sad to report that the flat viewing day is off.\n[11 Jan 2026] Tomas: @Arlo Think 21 January 2026 would work if I forward the gas bill instead?\n[16 Jan 2026] Arlo: @Tomas Yes, happy for you to forward the gas bill by 21 January 2026 instead.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Tomas made to forward the gas bill at the end of 17 January 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Not yet due",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "qd1410382e1",
  "kind": "yes/no",
  "text": "Subject: Chat about the gallery show\nBelow, with Oskar named as the source, is the chat as exported.\n\nMembers: Oskar, Kofi, Sami, Malik\nChat log (oldest first):\n[13 Mar 2026] Oskar: @Kofi Promise to update the icon set by 21 Mar 2026 if the print run goes ahead.\n[17 Mar 2026] Kofi: @Malik Relax, I'll collect the photo credits by 22 Mar 2026, promise.\n[19 Mar 2026] Kofi: Just so you know, the print run is on as scheduled.\n[21 Mar 2026] Oskar: @Kofi Think 25 Mar 2026 would work if I update the icon set instead?\n[21 Mar 2026] Sami: @Oskar Yes, you have the green light to update the icon set by 25 Mar 2026.\n[28 Mar 2026] Oskar: @Kofi Ta-da, I went and did it: update the icon set!",
  "question": "Under the rules on the card, is the promise Oskar made to update the icon set in a status other than broken at the end of 26 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0593c14cde",
  "kind": "yes/no",
  "text": "Exported by Ana, this is the full back and forth on the wedding weekend.\n\nMembers: Wren, Ana, Leila, Oskar\nChat log (oldest first):\n[21 Apr 2026] Oskar: @Wren Provided the ceremony walkthrough happens, I'll send the sneak peek gallery by 26 April 2026.\n[22 Apr 2026] Wren: @Leila Wish me luck, hoping to buy the candle props by 26 April 2026.\n[23 Apr 2026] Wren: @Leila Count on me to charge the flash batteries by 26 April 2026 if the rehearsal dinner is on.\n[24 Apr 2026] Wren: @Oskar You can bank on me to buy the candle props by 2 May 2026.\n[30 Apr 2026] Wren: @Oskar Quick question, could I buy the candle props by 8 May 2026 instead?\n[2 May 2026] Oskar: @Wren The original date stands, so you need to buy the candle props.",
  "question": "Does the card's rule set confirm that Wren has kept the promise to buy the candle props on 2 May 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb53e6986aa",
  "kind": "choice",
  "text": "Shared by Arlo, this is where the street watch scheme gets planned.\n\nMembers: Ravi, Tomas, Arlo\nChat log (oldest first):\n[4 Jun 2026] Tomas: @Ravi Count on me to return the ladders by 12 Jun 2026 if the parking permit visit is on.\n[5 Jun 2026] Ravi: @Arlo Count on me to lock the side gate by 13 Jun 2026.\n[6 Jun 2026] Tomas: @Arlo Count on me, I'll sweep the pavement outside by 14 Jun 2026.\n[8 Jun 2026] Ravi: Lovely, the parking permit visit is definitely happening!\n[9 Jun 2026] Ravi: @Arlo It's on me to take in the post by 13 Jun 2026.\n[12 Jun 2026] Tomas: @Ravi On my action item, may I return the ladders by 15 Jun 2026 instead?\n[12 Jun 2026] Ravi: @Tomas Yes, fine to return the ladders by 15 Jun 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, what is the deadline for Tomas to return the ladders at the end of 21 Jun 2026, with any agreed change of date counted?",
  "options": [
   "12 Jun 2026",
   "13 Jun 2026",
   "15 Jun 2026"
  ]
 },
 {
  "qid": "q31d81ab5a9",
  "kind": "choice",
  "text": "Here is the house refit, posted by Arlo for the family to read.\n\nMembers: Ravi, Lee, Ivo, Arlo\nChat export (date | from | to | message):\n2026-07-05 | Lee | Ravi | I'll pick up the grout bag by 8 July 2026, promise.\n2026-07-05 | Lee | Ravi | For the record: I was able to pick up the grout bag\n2026-07-06 | Arlo | Ivo | Lovely, I'll pay the plumbing invoice by 9 July 2026 if the boiler install visit is on.\n2026-07-08 | Lee | group | Quick heads up, the boiler install visit is scrapped.\n2026-07-11 | Arlo | Lee | I own this, I'll scrape the old wallpaper by 13 July 2026.\n2026-07-12 | Arlo | Ravi | I'll be sure to return the tile cutter by 17 July 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Arlo's promise to pay the plumbing invoice turn out at the end of 12 July 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "qe6f55f8072",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the attic conversion idea\nThe thread below comes from Mo and is passed on as it is.\n\nMembers: Mo, Tomas, Lena, Malik\nChat export (date | from | to | message):\n2026-10-19 | Tomas | group | Might be able to drop the parcel upstairs by 26 October 2026, who knows!\n2026-10-21 | Tomas | Lena | Guaranteed I'll drop the parcel upstairs by 25 October 2026.\n2026-10-21 | Tomas | Lena | Quick question, could I drop the parcel upstairs by 29 October 2026 instead?\n2026-10-22 | Mo | Malik | Only if the landlord inspection walk is on, I will sort the recycling bags by 30 October 2026.\n2026-10-24 | Malik | Tomas | I promise to defrost the top freezer by 30 October 2026.\n2026-10-25 | Tomas | Lena | For the record: I was able to drop the parcel upstairs\n2026-10-25 | Malik | Tomas | Log entry: defrost the top freezer, carried out\n2026-10-27 | Mo | Malik | Count on me to cut a spare door key by 31 October 2026 if the water tank check is on.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Tomas due to drop the parcel upstairs at the end of 22 October 2026, after any agreed rescheduling?",
  "options": [
   "30 October 2026",
   "29 October 2026",
   "25 October 2026"
  ]
 },
 {
  "qid": "q34f8f8079f",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the family history\nFrom Malik, the thread below is passed on in its original form.\n\nMembers: Rhea, Kai, Lee, Malik\nChat log (oldest first):\n[13 Aug 2026] Lee: @Rhea You can bet I'll fetch the speaker system by 17 Aug 2026.\n[15 Aug 2026] Rhea: @Lee Forget it, you won't need to fetch the speaker system\n[16 Aug 2026] Rhea: @Malik Lovely, I'll set up the slideshow laptop by 22 Aug 2026 for sure.\n[16 Aug 2026] Rhea: @Lee Count on me to print the family tree chart by 23 Aug 2026, if the grandparents visit happens.\n[21 Aug 2026] Rhea: Fab, we are on for the grandparents visit as planned!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Lee made to fetch the speaker system, what state is it in at the end of 19 Aug 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qb53b891b5a",
  "kind": "choice",
  "text": "Subject: Chat about the new repertoire\nBelow, with Bruno named as the source, is the chat as exported.\n\nMembers: Priya, Bruno, Omar\nChat log (oldest first):\n[1 Jun 2026] Bruno: @Omar I'll be sure to set up the sound desk by 2026-06-05.\n[4 Jun 2026] Omar: @Priya Ticket's mine, I'll return the library scores by 2026-06-08.\n[5 Jun 2026] Omar: @Bruno Forget it, you won't need to set up the sound desk\n[5 Jun 2026] Omar: @Bruno Provided the choir festival happens, I will fetch the choir robes by 2026-06-11.\n[6 Jun 2026] Omar: @Bruno Only if the voice test is on, I will print the song sheets by 2026-06-11.\n[8 Jun 2026] Omar: Sad to report that the choir festival is off.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of 2026-06-06, which status does Bruno have for the promise to set up the sound desk?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q03fa8f526e",
  "kind": "yes/no",
  "text": "Attached chat: the online store move\nShared by: Zara\n\nMembers: Zara, Priya, Arlo, Kai\nChat log (oldest first):\n[14 Feb 2026] Kai: @Priya I'll add the size chart by 2026-02-21 if the market day goes ahead.\n[16 Feb 2026] Priya: Brilliant news everyone, the market day is a go!\n[16 Feb 2026] Priya: @Zara Lovely, I'll fix the checkout button by 2026-02-22 for sure.\n[18 Feb 2026] Priya: @Zara I have to take back my promise to fix the checkout button.\n[23 Feb 2026] Kai: @Priya To my relief, I managed to add the size chart.",
  "question": "Has Kai broken the promise to add the size chart at the end of 2026-02-25?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6d770a7c72",
  "kind": "choice",
  "text": "Bruno forwarded this support chat about the spring campaign.\n\nMembers: Ravi, Bruno, Kofi, Ana\nChat export (date | from | to | message):\n2026-08-19 | Bruno | Ana | Count on me to fix the landing page headline by 25 August 2026.\n2026-08-19 | Bruno | Ana | On my action item, may I fix the landing page headline by 29 August 2026 instead?\n2026-08-22 | Kofi | Bruno | If the webinar rehearsal goes ahead, I'll draft the press release by 30 August 2026.\n2026-08-25 | Bruno | Ana | Guess what, I managed to fix the landing page headline!\n2026-08-25 | Kofi | group | Just so you know, the webinar rehearsal is on as scheduled.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Bruno's promise to fix the landing page headline sit at the end of 30 August 2026, exactly?",
  "options": [
   "Not yet due",
   "Kept",
   "Broken",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "qe2e5d7e328",
  "kind": "choice",
  "text": "Chat attached to a support case about the league run, shared by Malik.\n\nMembers: Malik, Hana\nChat log (oldest first):\n[16 Mar 2026] Malik: @Hana I'll pump the match balls by Saturday, March 21, 2026 if the training camp goes ahead.\n[17 Mar 2026] Malik: @Hana You can bank on me to set up the corner flags by Wednesday, March 25, 2026.\n[21 Mar 2026] Malik: @Hana Committing to wash the away kit by Thursday, March 26, 2026.\n[22 Mar 2026] Malik: @Hana To my relief, I managed to set up the corner flags.\n[23 Mar 2026] Hana: @Malik If the presentation evening goes ahead, I'll gladly book the changing room by Sunday, March 29, 2026.\n[26 Mar 2026] Hana: @Malik Relax, mate, you're not expected to wash the away kit",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Malik made to wash the away kit have at the end of Saturday, March 28, 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q79478ff25a",
  "kind": "choice",
  "text": "Team channel: the trade show push\nExported by Dara.\n\nMembers: Kofi, Greta, Mo, Dara\nChat export (date | from | to | message):\n2026-04-16 | Dara | Greta | You can bet I'll fetch the campaign budget sheet by Thursday, April 23, 2026.\n2026-04-17 | Greta | Dara | Got it, I'll draft the press release by Wednesday, April 22, 2026 for sure.\n2026-04-18 | Mo | Kofi | I will return the rented camera gear by Saturday, April 25, 2026 only if the annual review happens.\n2026-04-19 | Greta | Dara | Correction, I will not be able to draft the press release.\n2026-04-21 | Kofi | group | Afraid the annual review is called off.\n2026-04-22 | Kofi | Dara | Forget it, you won't need to fetch the campaign budget sheet",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Dara's commitment to fetch the campaign budget sheet at the end of Thursday, April 23, 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q748fb86b8a",
  "kind": "yes/no",
  "text": "Team channel export, shared by Kofi, which is about the visitor policy.\n\nMembers: Femi, Ines, Tess, Kofi\nChat log (oldest first):\n[9 Oct 2026] Kofi: @Femi Lovely, I'll book the boardroom by Thursday, 15 October 2026 if the lease viewing is on.\n[11 Oct 2026] Kofi: @Tess Count on me to return the printer toner by Monday, 19 October 2026.\n[15 Oct 2026] Kofi: @Tess I'll replace the kitchen filters by Thursday, 22 October 2026, providing the coffee morning goes ahead.\n[15 Oct 2026] Femi: @Kofi Don't sweat it, there's no need to return the printer toner\n[20 Oct 2026] Kofi: @Tess Ta-da, I went and did it: return the printer toner!",
  "question": "On Saturday, 24 October 2026 itself, has Kofi not kept the promise to return the printer toner?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa2d8dcfa64",
  "kind": "yes/no",
  "text": "Leila saved these replies from the agent on the summer lets season.\n\nMembers: Elif, Malik, Leila\nChat log (oldest first):\n[14 Apr 2026] Leila: @Elif I assure you I'll restock the guest toiletries by 19 April 2026 if the guest arrival evening is on.\n[16 Apr 2026] Malik: @Leila Hoping to change the lounge bulb by 19 April 2026, but can't promise.\n[17 Apr 2026] Malik: @Leila Absolutely, I will change the lounge bulb by 24 April 2026.\n[18 Apr 2026] Leila: On track for the guest arrival evening to happen as planned.\n[19 Apr 2026] Elif: @Malik Please don't feel you have to change the lounge bulb\n[22 Apr 2026] Malik: @Leila Ticked off my list: change the lounge bulb, yay.",
  "question": "Is the promise Malik made to change the lounge bulb not kept by 26 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q82e641ac71",
  "kind": "choice",
  "text": "We are getting ready for the family day out, and Tomas shared this chat with us.\n\nMembers: Kai, Tomas, Tess, Rhea\nChat log (oldest first):\n[24 Sep 2026] Rhea: @Kai You can bank on me to pick up the school bags by 30 Sep 2026.\n[24 Sep 2026] Kai: @Rhea Relax, mate, you're not expected to pick up the school bags\n[27 Sep 2026] Tomas: @Tess Count on me to teach the card game by 4 Oct 2026, if the puppet show happens.\n[28 Sep 2026] Tomas: @Tess Provided the school play happens, I will tidy the playroom by 2 Oct 2026.\n[29 Sep 2026] Kai: @Tomas Guaranteed I'll fetch the craft box by 6 Oct 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 1 Oct 2026, what status has Rhea's promise to pick up the school bags got?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Broken",
   "Waived"
  ]
 }
]
