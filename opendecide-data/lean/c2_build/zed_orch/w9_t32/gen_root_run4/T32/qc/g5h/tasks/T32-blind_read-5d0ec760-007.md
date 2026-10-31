# G5-H blind read T32-blind_read-5d0ec760-007 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root/T32/qc/g5h/answers/T32-blind_read-5d0ec760-007.json

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
  "qid": "q44896e1952",
  "kind": "yes/no",
  "text": "Subject: Chat about the winter concert\nBelow is a copy that came from Hana, pasted as found.\n\nMembers: Hana, Wren, Ines, Kai\nChat log (oldest first):\n[24 Jul 2026] Hana: @Kai Only if the joint concert is on, I will return the library scores by 31 July 2026.\n[24 Jul 2026] Hana: Quick heads up, the joint concert is scrapped.\n[25 Jul 2026] Kai: @Hana You can bank on me to buy the spare folders by 1 August 2026.\n[27 Jul 2026] Ines: @Kai I'll be sure to move the piano by 30 July 2026.\n[30 Jul 2026] Ines: @Kai To my relief, I managed to move the piano.\n[4 Aug 2026] Wren: Anything new on your way to move the piano?",
  "question": "According to the rules on the card, does the promise Ines made to move the piano have any status except broken at the end of 5 August 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q98b6a0a64f",
  "kind": "yes/no",
  "text": "{\"source\": \"saved thread\", \"about\": \"the training plan\", \"owner\": \"Yuki\", \"kind\": \"chat export\"}\n\nMembers: Elif, Jonas, Arlo, Yuki\nChat log (oldest first):\n[10 Apr 2026] Yuki: @Jonas If the mechanics clinic goes ahead, I'll gladly wash the club jerseys by 16 April 2026.\n[11 Apr 2026] Elif: Team, the mechanics clinic stays on as booked.\n[14 Apr 2026] Yuki: @Elif Committing to print the route cards by 20 April 2026.\n[15 Apr 2026] Jonas: @Yuki Good news, you're let off having to print the route cards\n[16 Apr 2026] Yuki: @Jonas Got myself to wash the club jerseys lol.",
  "question": "Was the promise to wash the club jerseys from Yuki kept on 18 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6ff5b2c4df",
  "kind": "yes/no",
  "text": "Chat attached to a support case about the family day out, shared by Zara.\n\nMembers: Rhea, Zara, Bruno\nChat log (oldest first):\n[28 Mar 2026] Zara: @Rhea See if I can sort the old photo albums by 2026-04-05, no certainty.\n[30 Mar 2026] Zara: @Bruno You can bank on me to sort the old photo albums by 2026-04-03.\n[1 Apr 2026] Zara: @Rhea I will pick up the school bags by 2026-04-09.\n[3 Apr 2026] Zara: @Bruno For the record: I was able to sort the old photo albums\n[3 Apr 2026] Bruno: @Rhea As long as the school play is on, I'll read the bedtime story by 2026-04-07.\n[6 Apr 2026] Zara: On track for the school play to happen as planned.",
  "question": "Is it right to say that Zara has broken the promise to sort the old photo albums at the end of 2026-04-06?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q895d9bad90",
  "kind": "choice",
  "text": "Neighbours and renters, the flat chat, exported by Bruno, covering the vegetable plot plan.\n\nMembers: Sami, Bruno, Rhea, Jonas\nChat log (oldest first):\n[4 May 2026] Rhea: @Bruno If the water tank delivery goes ahead, I'll gladly dig the potato patch by 2026-05-11.\n[4 May 2026] Bruno: @Rhea Got it, I'll water the allotment beds by 2026-05-09 for sure.\n[6 May 2026] Jonas: Team, the water tank delivery stays on as booked.\n[6 May 2026] Bruno: @Rhea No worries, you don't need to dig the potato patch\n[9 May 2026] Rhea: @Bruno For the record: I was able to dig the potato patch",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Rhea made to dig the potato patch at the end of 2026-05-07?",
  "options": [
   "Kept",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qc7d247479d",
  "kind": "yes/no",
  "text": "Flatmates' thread\nExport of the bathroom refit, passed on by Kofi.\n\nMembers: Yuki, Kofi, Rhea\nChat export (date | from | to | message):\n2026-07-02 | Kofi | Rhea | I will measure the hallway for shelves by 11 Jul 2026 only if the damp survey inspection happens.\n2026-07-02 | Rhea | Kofi | Relax, I'll return the tile cutter by 6 Jul 2026, promise.\n2026-07-04 | Rhea | Kofi | Mind giving me until 10 Jul 2026 to return the tile cutter?\n2026-07-05 | Yuki | Rhea | Yes, happy for you to return the tile cutter by 10 Jul 2026 instead.\n2026-07-06 | Rhea | Kofi | Ticked off my list: return the tile cutter, yay.\n2026-07-07 | Rhea | group | Team, the damp survey inspection stays on as booked.",
  "question": "Does the card's rule set confirm that Rhea has kept the promise to return the tile cutter on 11 Jul 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa48c15ff0f",
  "kind": "choice",
  "text": "{\"export_type\": \"group chat export\", \"chat_topic\": \"the garden makeover\", \"saved_by\": \"Dara\"}\n\nMembers: Bruno, Dara, Mo, Tomas\nChat log (oldest first):\n[3 Jul 2026] Bruno: @Dara Count on me to hang the new curtain rail by 10 Jul 2026, if the builder quote meeting happens.\n[7 Jul 2026] Mo: @Tomas Committing to pick up the grout bag by 11 Jul 2026.\n[8 Jul 2026] Mo: Quick heads up, the builder quote meeting is scrapped.\n[8 Jul 2026] Bruno: @Dara Would it be fine if I hang the new curtain rail by 16 Jul 2026 instead, yeah?\n[8 Jul 2026] Dara: @Bruno Not moving it, hang the new curtain rail by the existing date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Bruno's promise to hang the new curtain rail stand at the end of 10 Jul 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not triggered",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q87be004857",
  "kind": "choice",
  "text": "Here's the flatmate chat that Jonas saved, about the street watch scheme.\n\nMembers: Dara, Ines, Ravi, Jonas\nChat log (oldest first):\n[14 Jan 2026] Ines: @Ravi I will sweep the pavement outside by Saturday, January 17, 2026 only if the street litter clean happens.\n[15 Jan 2026] Ravi: Great news, the street litter clean is on!\n[16 Jan 2026] Ines: @Jonas I promise to lock the side gate by Sunday, January 25, 2026.\n[16 Jan 2026] Ines: @Ravi Mind giving me until Wednesday, January 21, 2026 to sweep the pavement outside?\n[23 Jan 2026] Ines: @Jonas Quick question, could I lock the side gate by Tuesday, January 27, 2026 instead?\n[25 Jan 2026] Jonas: @Ines No change, you need to lock the side gate by the original date.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Ines's promise to sweep the pavement outside sit at the end of Sunday, January 18, 2026, exactly?",
  "options": [
   "Not triggered",
   "Broken",
   "Not yet due",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q56de76ae1d",
  "kind": "choice",
  "text": "Elif forwarded this support chat about the old house restoration.\n\nMembers: Elif, Nadia, Rhea\nChat log (oldest first):\n[20 Mar 2026] Nadia: I'm aiming to bleed the attic radiators by 27 Mar 2026, might manage it.\n[21 Mar 2026] Elif: @Rhea Absolutely, I will find the loft ladder by 24 Mar 2026.\n[22 Mar 2026] Nadia: @Rhea If the chimney sweep visit is on, I'll definitely bleed the attic radiators by 28 Mar 2026.\n[22 Mar 2026] Rhea: Really pleased to say the chimney sweep visit will go ahead!\n[23 Mar 2026] Nadia: @Rhea For the record: I was able to bleed the attic radiators\n[25 Mar 2026] Nadia: @Elif I promise to tidy the boot room by 30 Mar 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Nadia's promise to bleed the attic radiators at the end of 23 Mar 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Broken",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q8b761ba910",
  "kind": "choice",
  "text": "Work conversation on the website relaunch, saved as a file by Priya.\n\nMembers: Kai, Priya, Wren\nChat export (date | from | to | message):\n2026-10-07 | Priya | Wren | I'll see if I can fix the landing page headline by 11 October 2026.\n2026-10-09 | Kai | Wren | Count on me to fetch the campaign budget sheet by 15 October 2026, if the influencer call happens.\n2026-10-09 | Priya | Wren | I will make sure to fix the landing page headline by 14 October 2026.\n2026-10-10 | Priya | group | Sadly, the influencer call won't go ahead.\n2026-10-10 | Wren | Priya | Forget it, you won't need to fix the landing page headline\n2026-10-14 | Priya | Wren | Log entry: fix the landing page headline, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Priya's promise to fix the landing page headline receive at the end of 19 October 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Not yet due",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "qd812beef52",
  "kind": "choice",
  "text": "Pasted into the project log by Zara, the thread with a client about the big day.\n\nMembers: Femi, Lee, Ivo, Zara\nChat log (oldest first):\n[16 Jan 2026] Femi: Aiming to return the lighting stands by 29 January 2026, we'll see.\n[18 Jan 2026] Femi: @Zara Provided the bridal shower happens, I will return the lighting stands by 25 January 2026.\n[20 Jan 2026] Zara: Yep, the bridal shower is on as planned.\n[25 Jan 2026] Femi: @Zara Would it be fine if I return the lighting stands by 30 January 2026 instead, yeah?\n[25 Jan 2026] Ivo: @Femi Go ahead and return the lighting stands by 30 January 2026, that is fine.\n[29 Jan 2026] Lee: @Ivo Count on me to print the seating cards by 31 January 2026.\n[31 Jan 2026] Lee: @Ivo Is it all right if I print the seating cards by 2 February 2026 instead?\n[31 Jan 2026] Ivo: @Lee Go ahead and print the seating cards by 2 February 2026, that is fine.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Femi to return the lighting stands at the end of 6 February 2026, counting any agreed change of date?",
  "options": [
   "31 January 2026",
   "25 January 2026",
   "30 January 2026"
  ]
 },
 {
  "qid": "q3f90252890",
  "kind": "choice",
  "text": "Team channel: the visitor policy\nShared by Yuki.\n\nMembers: Yuki, Nadia, Ines, Tess\nChat log (oldest first):\n[28 Jul 2026] Yuki: @Ines Provided the annual audit happens, I'll set up the reception screen by 2 August 2026.\n[28 Jul 2026] Yuki: @Tess I'll try to return the printer toner by 1 August 2026.\n[30 Jul 2026] Yuki: @Tess Count on me to return the printer toner by 7 August 2026.\n[4 Aug 2026] Nadia: @Tess Lovely, I'll print the staff rota by 8 August 2026 for sure.\n[5 Aug 2026] Nadia: @Ines Provided the staff picnic happens, I will replace the kitchen filters by 12 August 2026.\n[7 Aug 2026] Tess: @Yuki You don't have to return the printer toner at all",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Yuki made to return the printer toner at the end of 10 August 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q5f8cdba4bd",
  "kind": "choice",
  "text": "Flatmate thread, saved by Rhea, the topic being the student house hunt.\n\nMembers: Greta, Elif, Tomas, Rhea\nChat log (oldest first):\n[12 Aug 2026] Rhea: @Elif Committing to photograph the bathroom mould by August 22, 2026.\n[14 Aug 2026] Greta: @Elif Ticket's mine, I'll ring the letting agent by August 17, 2026.\n[14 Aug 2026] Greta: @Elif I committed to ring the letting agent, can I do that by August 21, 2026 instead?\n[15 Aug 2026] Rhea: @Greta Ah, no stress, no need for you to ring the letting agent\n[17 Aug 2026] Rhea: @Elif As long as the house hunting viewing is on, I will store the spare bike by August 24, 2026.\n[22 Aug 2026] Rhea: Team, the house hunting viewing stays on as booked.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhere does Greta stand on the promise to ring the letting agent at the end of August 17, 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q43994b7281",
  "kind": "yes/no",
  "text": "{\"source\": \"saved thread\", \"about\": \"the mobile release\", \"owner\": \"Greta\", \"kind\": \"chat export\"}\n\nMembers: Greta, Nadia\nChat log (oldest first):\n[20 Mar 2026] Greta: @Nadia You can bet I'll write the release notes by 27 Mar 2026.\n[20 Mar 2026] Greta: I'll try to review the pull request by 26 Mar 2026, no promises.\n[22 Mar 2026] Greta: @Nadia I'll review the pull request by 25 Mar 2026, provided the server migration happens.\n[23 Mar 2026] Nadia: Brilliant news everyone, the server migration is a go!\n[24 Mar 2026] Greta: @Nadia Got myself to write the release notes lol.\n[1 Apr 2026] Greta: @Nadia For the record: I was able to review the pull request",
  "question": "Would you say Greta didn't keep the promise to review the pull request by the end of 29 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q020c353a6e",
  "kind": "yes/no",
  "text": "Family group chat with housemates, covering the reunion planning, exported by Ivo.\n\nMembers: Oskar, Ivo\nChat log (oldest first):\n[20 Mar 2026] Ivo: @Oskar Absolutely, I will fetch the speaker system by 23 Mar 2026.\n[23 Mar 2026] Ivo: @Oskar Lovely, I'll buy the name tags by 29 Mar 2026 if the cousin brunch is on.\n[25 Mar 2026] Ivo: @Oskar To note: I have managed to fetch the speaker system\n[26 Mar 2026] Oskar: Yep, the cousin brunch is on as planned.\n[29 Mar 2026] Ivo: @Oskar Mate, I promised, may I buy the name tags by 4 Apr 2026 instead?\n[29 Mar 2026] Ivo: @Oskar To my relief, I managed to buy the name tags.",
  "question": "Under the rules on the card, is the promise Ivo made to buy the name tags broken at the end of 1 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qff22b04b66",
  "kind": "choice",
  "text": "Project log\nClient and freelancer messages on the online store move, saved by Jonas.\n\nMembers: Jonas, Elif, Leila\nChat log (oldest first):\n[15 Jul 2026] Leila: @Jonas I will restore the old theme by 21 July 2026 only if the product photo day happens.\n[16 Jul 2026] Elif: @Jonas Absolutely, I will fetch the domain login by 18 July 2026.\n[16 Jul 2026] Elif: Yep, the product photo day is on as planned.\n[21 Jul 2026] Leila: @Jonas Can I restore the old theme by 24 July 2026 instead? I did promise, sorry.\n[21 Jul 2026] Jonas: @Leila Nah, the date's staying put, so you can restore the old theme.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Leila's promise to restore the old theme at the end of 22 July 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Not yet due",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "qa1f0a02338",
  "kind": "choice",
  "text": "Forwarded by Omar, these tenant replies are about the cottage refresh for the file.\n\nMembers: Femi, Greta, Lena, Omar\nChat log (oldest first):\n[6 Apr 2026] Omar: @Greta Promise to vacuum the holiday cottage by 14 Apr 2026 if the lettings photo shoot goes ahead.\n[7 Apr 2026] Greta: @Omar You can bet I'll leave the welcome basket by 13 Apr 2026.\n[7 Apr 2026] Femi: @Greta Good news, you're let off having to leave the welcome basket\n[13 Apr 2026] Greta: @Omar Ticked off: leave the welcome basket, feels so good\n[13 Apr 2026] Lena: Sad to report that the lettings photo shoot is off.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhere does Greta stand on the promise to leave the welcome basket at the end of 11 Apr 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q4dfd207d1b",
  "kind": "choice",
  "text": "Saved by Leila, this is the household group chat about the family history, copied in full.\n\nMembers: Leila, Greta\nChat log (oldest first):\n[28 Apr 2026] Greta: @Leila As long as the reunion lunch is on, I'll buy the name tags by 4 May 2026.\n[28 Apr 2026] Greta: Team, the reunion lunch is not happening.\n[30 Apr 2026] Leila: @Greta Relax, I'll print the family tree chart by 8 May 2026, promise.\n[6 May 2026] Leila: @Greta I committed to print the family tree chart, can I do that by 13 May 2026 instead?\n[6 May 2026] Greta: @Leila Aw no, you need to print the family tree chart by the original date!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Leila's pledge to print the family tree chart sit at the end of 6 May 2026?",
  "options": [
   "Kept",
   "Waived",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q3bc1c3754c",
  "kind": "yes/no",
  "text": "Yo flatmates, Kofi shared this chat about the speed bump plan, so chip in.\n\nMembers: Yuki, Ravi, Kofi\nChat log (oldest first):\n[8 Mar 2026] Yuki: @Kofi Promise to lend the stepladder by 16 Mar 2026 if the speed camera survey goes ahead.\n[8 Mar 2026] Kofi: We are dropping the speed camera survey from the list.\n[8 Mar 2026] Ravi: @Yuki As long as the bonfire night is on, I'll sweep the pavement outside by 10 Mar 2026.\n[11 Mar 2026] Yuki: @Ravi Count on me to take in the post by 17 Mar 2026.\n[11 Mar 2026] Ravi: @Kofi Relax, I'll lock the side gate by 14 Mar 2026 for sure.\n[13 Mar 2026] Ravi: @Kofi Got myself to lock the side gate lol.",
  "question": "Under the rules on the card, is Ravi's promise to lock the side gate broken, waived, not triggered or not yet due, rather than kept, as of 15 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q012ef7af42",
  "kind": "yes/no",
  "text": "Committee chat on the winter concert, shared by Femi with the volunteers.\n\nMembers: Femi, Tess, Malik, Mo\nChat log (oldest first):\n[19 Jul 2026] Mo: @Femi Provided the summer recital happens, I will print the song sheets by 21 July 2026.\n[19 Jul 2026] Femi: Lovely, the summer recital is definitely happening!\n[19 Jul 2026] Malik: @Femi Relax, I'll book the rehearsal room by 27 July 2026 for sure.\n[25 Jul 2026] Mo: @Femi It's on me to buy the spare folders by 1 August 2026.\n[27 Jul 2026] Malik: @Femi Quick report: I've managed to book the rehearsal room",
  "question": "Applying the card's rules, can it be said that Malik has not kept the promise to book the rehearsal room at the end of 30 July 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8975aeadb2",
  "kind": "choice",
  "text": "Omar forwarded this for the committee as we dig in on the volunteer roster.\n\nMembers: Omar, Greta, Hana, Bruno\nChat export (date | from | to | message):\n2026-03-01 | Greta | Hana | Got it, I'll return the borrowed trestle tables by 7 Mar 2026 for sure.\n2026-03-03 | Hana | Greta | Ah, no stress, no need for you to return the borrowed trestle tables\n2026-03-04 | Omar | Greta | Provided the governors meeting happens, I'll send the newsletter drafts by 6 Mar 2026.\n2026-03-04 | Greta | Hana | Guess who managed to return the borrowed trestle tables, go team!\n2026-03-05 | Hana | group | Just so you know, the governors meeting is on as scheduled.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Greta made to return the borrowed trestle tables at the end of 3 Mar 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qab4d12ba5d",
  "kind": "yes/no",
  "text": "Volunteers, Bruno shared this with you about the winter concert.\n\nMembers: Ines, Femi, Bruno\nChat log (oldest first):\n[10 Aug 2026] Ines: See if I can buy the spare folders by 20 August 2026.\n[11 Aug 2026] Femi: @Bruno If the sing along goes ahead, I'll gladly print the song sheets by 17 August 2026.\n[12 Aug 2026] Femi: @Ines If the carol concert is on, I'll definitely move the piano by 20 August 2026.\n[12 Aug 2026] Ines: @Bruno Relax, I'll buy the spare folders by 16 August 2026 for sure.\n[15 Aug 2026] Bruno: @Femi Lovely, I'll fix the stand microphones by 23 August 2026 for sure.\n[17 Aug 2026] Ines: @Bruno For the record: I was able to buy the spare folders",
  "question": "Checking the chat at the end of 20 August 2026, has Ines broken the promise to buy the spare folders?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2fd8d622cb",
  "kind": "choice",
  "text": "{\"chat\": \"exported\", \"about\": \"the balcony garden project\", \"saved_by\": \"Mo\", \"medium\": \"text\"}\n\nMembers: Nadia, Hana, Mo, Yuki\nChat export (date | from | to | message):\n2026-06-16 | Nadia | Mo | If the lease renewal call goes ahead, I'll gladly drop the bin bags off by 2026-06-21.\n2026-06-21 | Hana | Yuki | Relax, I'll remove the bathroom shelf by 2026-06-26 for sure.\n2026-06-22 | Hana | Yuki | Might I ask whether I could remove the bathroom shelf by 2026-06-30 instead?\n2026-06-24 | Hana | Nadia | Promise to email the leak photos by 2026-07-01 if the rent review meeting goes ahead.\n2026-06-25 | Nadia | Hana | Good news, you're let off having to remove the bathroom shelf",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Hana's pledge to remove the bathroom shelf at the end of 2026-06-30?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q5ebbcef12f",
  "kind": "choice",
  "text": "Team channel: the desk plan\nShared by Bruno.\n\nMembers: Yuki, Priya, Bruno\nChat log (oldest first):\n[4 Apr 2026] Yuki: @Bruno I will replace the kitchen filters by 9 April 2026.\n[4 Apr 2026] Priya: I'll try to send the expense receipts by 18 April 2026, no promises.\n[5 Apr 2026] Bruno: @Priya I will book the boardroom by 7 April 2026 only if the team lunch happens.\n[6 Apr 2026] Priya: @Bruno Absolutely, I will send the expense receipts by 14 April 2026.\n[9 Apr 2026] Priya: @Yuki Only if the coffee morning is on, I will collect the visitor badges by 15 April 2026.\n[14 Apr 2026] Priya: @Bruno For the record: I was able to send the expense receipts",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Priya's promise to send the expense receipts at the end of 20 April 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "qb49287d4b5",
  "kind": "choice",
  "text": "Chat attached to the support case about the holiday memories, shared by Lena.\n\nMembers: Kai, Lena, Bruno\nChat log (oldest first):\n[26 Oct 2026] Lena: I'll try to bake the oat biscuits by 28 Oct 2026, can't promise!\n[27 Oct 2026] Lena: @Bruno If the sleepover weekend goes ahead, I'll bake the oat biscuits by 31 Oct 2026.\n[27 Oct 2026] Kai: Really pleased to say the sleepover weekend will go ahead!\n[29 Oct 2026] Lena: @Bruno Absolutely, I will fetch the craft box by 2 Nov 2026.\n[31 Oct 2026] Lena: @Bruno Can I bake the oat biscuits by 5 Nov 2026 instead? I did promise, sorry.\n[31 Oct 2026] Kai: @Lena Yes, you have the green light to bake the oat biscuits by 5 Nov 2026.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Lena's commitment to bake the oat biscuits is in what status at the end of 28 Oct 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "q14e499eee7",
  "kind": "choice",
  "text": "Tomas saved this so we stay on the same page about the quiet street fund, mates.\n\nMembers: Tomas, Zara, Arlo\nChat log (oldest first):\n[26 Apr 2026] Zara: @Arlo I'll clear the hedge trimmings by 30 Apr 2026, provided the parking permit visit happens.\n[27 Apr 2026] Arlo: Team, the parking permit visit is not happening.\n[28 Apr 2026] Zara: @Arlo I will make sure to lock the side gate by 6 May 2026.\n[30 Apr 2026] Zara: @Arlo Mind giving me until 4 May 2026 to clear the hedge trimmings?\n[30 Apr 2026] Arlo: @Zara Nah, the date's staying put, so you can clear the hedge trimmings.\n[2 May 2026] Arlo: @Zara Please don't feel you have to lock the side gate",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Zara's promise to clear the hedge trimmings at the end of 30 Apr 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Not yet due",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q4e20d4edab",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the lab move\nThe chat below comes from Lena, copied as is for reference.\n\nMembers: Priya, Lena, Yuki\nChat log (oldest first):\n[20 Mar 2026] Yuki: @Lena Provided the thesis defence happens, I'll submit the ethics application by Thursday, March 26, 2026.\n[20 Mar 2026] Lena: Update, the thesis defence will not take place.\n[22 Mar 2026] Yuki: @Priya Guaranteed I'll return the library books by Wednesday, March 25, 2026.\n[22 Mar 2026] Priya: @Lena Lovely, I'll book the microscope slot by Saturday, March 28, 2026 if the journal club is on.\n[24 Mar 2026] Lena: @Priya Ticket's mine, I'll clean the glassware set by Monday, March 30, 2026.\n[26 Mar 2026] Yuki: @Priya Got myself to return the library books lol.",
  "question": "Is Yuki's promise to return the library books kept on Saturday, March 28, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc518fb63c6",
  "kind": "choice",
  "text": "Subject: saved chat, the platform rewrite\nBelow is the chat that Jonas saved for reference.\n\nMembers: Jonas, Oskar, Kai\nChat log (oldest first):\n[5 Aug 2026] Oskar: @Kai I'll run the security scan by Sunday, 9 August 2026, promise.\n[7 Aug 2026] Kai: @Oskar Don't sweat it, there's no need to run the security scan\n[10 Aug 2026] Jonas: @Kai If the penetration test is on, I'll definitely merge the login branch by Monday, 17 August 2026.\n[10 Aug 2026] Oskar: Lovely, the penetration test is definitely happening!\n[17 Aug 2026] Kai: @Jonas Good news, you're let off having to merge the login branch",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Jonas's pledge to merge the login branch sit at the end of Wednesday, 19 August 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not yet due",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "qe56fbaccdd",
  "kind": "choice",
  "text": "Freelancer and client exchange about the wedding weekend, saved by Ivo.\n\nMembers: Ivo, Nadia, Oskar\nChat log (oldest first):\n[19 Jul 2026] Nadia: @Oskar You can bank on me to collect the venue floor plan by 23 July 2026.\n[20 Jul 2026] Nadia: @Oskar Is it all right if I collect the venue floor plan by 29 July 2026 instead?\n[21 Jul 2026] Oskar: @Nadia Yes, all good for you to collect the venue floor plan by 29 July 2026 instead.\n[21 Jul 2026] Ivo: @Nadia Good news, you're let off having to collect the venue floor plan\n[22 Jul 2026] Oskar: @Ivo I'll charge the flash batteries by 31 July 2026 as long as the rehearsal dinner is on.\n[25 Jul 2026] Nadia: Sadly, the rehearsal dinner won't go ahead.\n[26 Jul 2026] Ivo: @Oskar Relax, I'll book the assistant photographer by 2 August 2026, promise.\n[29 Jul 2026] Nadia: @Oskar Log entry: collect the venue floor plan, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo what's the latest day Nadia has to collect the venue floor plan by at the end of 28 July 2026, given any new date people agreed to?",
  "options": [
   "23 July 2026",
   "31 July 2026",
   "29 July 2026"
  ]
 },
 {
  "qid": "q17b5172d13",
  "kind": "choice",
  "text": "Support thread for a help desk case, covering the data cleanup, saved by Arlo.\n\nMembers: Tess, Arlo\nChat log (oldest first):\n[5 May 2026] Tess: @Arlo If the server migration goes ahead, I'll gladly merge the login branch by Wednesday, 13 May 2026.\n[6 May 2026] Arlo: Just so you know, the server migration is on as scheduled.\n[7 May 2026] Tess: @Arlo I will write the release notes by Friday, 15 May 2026.\n[13 May 2026] Tess: @Arlo Got myself to merge the login branch lol.\n[15 May 2026] Arlo: @Tess Forget it, you won't need to write the release notes",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Tess's promise to merge the login branch sit at the end of Saturday, 16 May 2026, exactly?",
  "options": [
   "Broken",
   "Not yet due",
   "Waived",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "qd5a152b4f0",
  "kind": "choice",
  "text": "Shared by Dara, a help-desk thread covering the guest list.\n\nMembers: Lee, Oskar, Dara, Jonas\nChat export (date | from | to | message):\n2026-02-27 | Jonas | Dara | I will make sure to buy the candle props by 7 March 2026.\n2026-03-05 | Jonas | Dara | On my action item, may I buy the candle props by 9 March 2026 instead?\n2026-03-07 | Dara | Jonas | Yes, you can buy the candle props by 9 March 2026 if that suits you.\n2026-03-08 | Dara | Jonas | Provided the venue visit happens, I'll charge the flash batteries by 13 March 2026.\n2026-03-08 | Dara | group | Please note the venue visit will proceed.\n2026-03-09 | Jonas | Dara | Guess who managed to buy the candle props, go team!\n2026-03-10 | Oskar | Jonas | Relax, I'll pick up the album prints by 13 March 2026, promise.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Jonas due to buy the candle props at the end of 10 March 2026, after any agreed rescheduling?",
  "options": [
   "13 March 2026",
   "9 March 2026",
   "7 March 2026"
  ]
 },
 {
  "qid": "q8ea2eb71dd",
  "kind": "yes/no",
  "text": "Shared by Rhea, this work thread covers the platform rewrite.\n\nMembers: Rhea, Kofi\nChat log (oldest first):\n[13 Jul 2026] Kofi: @Rhea Provided the sprint demo happens, I will update the dependency list by Thursday, July 16, 2026.\n[14 Jul 2026] Rhea: @Kofi I'll restart the build server by Thursday, July 23, 2026 as long as the planning session is on.\n[14 Jul 2026] Kofi: @Rhea Got it, I'll fix the test runner by Friday, July 17, 2026 for sure.\n[15 Jul 2026] Rhea: @Kofi Committing to run the security scan by Sunday, July 19, 2026.\n[15 Jul 2026] Kofi: Please note the sprint demo will proceed.\n[16 Jul 2026] Rhea: @Kofi Guess what, I managed to run the security scan!",
  "question": "Under the rules on the card, is Rhea's promise to run the security scan broken, waived, not triggered or not yet due, rather than kept, as of Tuesday, July 21, 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbe190b6a67",
  "kind": "choice",
  "text": "Subject: saved chat, the platform rewrite\nBelow is the chat that Jonas saved for reference.\n\nMembers: Jonas, Oskar, Kai\nChat log (oldest first):\n[5 Aug 2026] Oskar: @Kai I'll run the security scan by Sunday, 9 August 2026, promise.\n[7 Aug 2026] Kai: @Oskar Don't sweat it, there's no need to run the security scan\n[10 Aug 2026] Jonas: @Kai If the penetration test is on, I'll definitely merge the login branch by Monday, 17 August 2026.\n[10 Aug 2026] Oskar: Lovely, the penetration test is definitely happening!\n[17 Aug 2026] Oskar: @Jonas Good news, you're let off having to merge the login branch",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Jonas's pledge to merge the login branch sit at the end of Wednesday, 19 August 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not yet due",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q8864c97d2d",
  "kind": "choice",
  "text": "Chat attached to the support case about the holiday memories, shared by Lena.\n\nMembers: Kai, Lena, Bruno\nChat log (oldest first):\n[26 Oct 2026] Lena: I'll try to bake the oat biscuits by 28 Oct 2026, can't promise!\n[27 Oct 2026] Lena: @Bruno If the sleepover weekend goes ahead, I'll bake the oat biscuits by 31 Oct 2026.\n[27 Oct 2026] Kai: Update, the sleepover weekend will not take place.\n[29 Oct 2026] Lena: @Bruno Absolutely, I will fetch the craft box by 2 Nov 2026.\n[31 Oct 2026] Lena: @Bruno Can I bake the oat biscuits by 5 Nov 2026 instead? I did promise, sorry.\n[31 Oct 2026] Kai: @Lena Yes, you have the green light to bake the oat biscuits by 5 Nov 2026.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Lena's commitment to bake the oat biscuits is in what status at the end of 28 Oct 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "q23b5cb8495",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the new kit design\nHere is a full export from Bruno, ready to read.\n\nMembers: Bruno, Oskar, Kai\nChat export (date | from | to | message):\n2026-02-24 | Bruno | Oskar | I promise to service the tandem bike by March 5, 2026.\n2026-02-24 | Kai | Bruno | Lovely, I'll return the loaned helmets by March 2, 2026 if the bike check is on.\n2026-02-27 | Kai | Bruno | Quick update: you do not need to service the tandem bike at all.\n2026-02-27 | Kai | group | Great news, the bike check is on!\n2026-03-01 | Oskar | Kai | Relax, mate, you're not expected to return the loaned helmets",
  "question": "Was the promise to return the loaned helmets from Kai kept on March 3, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qfdce836b37",
  "kind": "yes/no",
  "text": "Volunteer chat export. Saved by Greta, it covers the new repertoire.\n\nMembers: Hana, Greta, Elif\nChat log (oldest first):\n[27 Mar 2026] Elif: @Greta Lovely, I'll collect the sheet music by 4 Apr 2026 if the joint concert is on.\n[30 Mar 2026] Hana: @Greta Guaranteed I'll move the piano by 7 Apr 2026.\n[2 Apr 2026] Hana: @Greta Apologies, I'll not be able to move the piano\n[2 Apr 2026] Elif: @Hana Nobody needs you to move the piano, that's that\n[2 Apr 2026] Elif: @Greta If the choir festival goes ahead, I'll gladly return the library scores by 5 Apr 2026.",
  "question": "Has Hana kept the promise to move the piano as of 4 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q837f1de45e",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the lab move\nThe chat below comes from Lena, copied as is for reference.\n\nMembers: Priya, Lena, Yuki\nChat log (oldest first):\n[20 Mar 2026] Yuki: @Lena Provided the thesis defence happens, I'll submit the ethics application by Thursday, March 26, 2026.\n[20 Mar 2026] Lena: Update, the thesis defence will not take place.\n[22 Mar 2026] Yuki: @Priya Guaranteed I'll return the library books by Wednesday, March 25, 2026.\n[22 Mar 2026] Priya: @Lena Lovely, I'll book the microscope slot by Saturday, March 28, 2026 if the journal club is on.\n[24 Mar 2026] Lena: @Priya Ticket's mine, I'll clean the glassware set by Monday, March 30, 2026.\n[26 Mar 2026] Yuki: @Priya Got myself to return the library books lol.",
  "question": "According to the card's rules, is the promise Yuki made to return the library books not kept as of Saturday, March 28, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q978805d9f9",
  "kind": "choice",
  "text": "Subject: chat about the lodger house rules, forwarded\nThe chat follows below.\nRegards, Ivo\n\nMembers: Kai, Tess, Ivo, Yuki\nChat export (date | from | to | message):\n2026-03-27 | Tess | Kai | I'll replace the loo roll by 3 April 2026, providing the lodger farewell supper goes ahead.\n2026-03-29 | Kai | Tess | Absolutely, I will feed the house plants by 2 April 2026.\n2026-03-29 | Ivo | Kai | Please don't feel you have to feed the house plants\n2026-03-29 | Kai | Tess | I will defrost the top freezer by 7 April 2026 only if the fuse box inspection happens.\n2026-03-31 | Tess | group | Sorry all, the lodger farewell supper is called off.\n2026-04-03 | Kai | Tess | Got it, I'll drop the parcel upstairs by 9 April 2026 for sure.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Kai's promise to feed the house plants at the end of 29 March 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Broken",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "q5e48ad6424",
  "kind": "choice",
  "text": "{\"thread\": \"the kit sponsorship\", \"exported_by\": \"Kai\", \"shape\": \"group chat\"}\n\nMembers: Lena, Mo, Kai, Nadia\nChat log (oldest first):\n[29 Sep 2026] Nadia: @Mo I'll fetch the medical bag by 2 Oct 2026, promise.\n[30 Sep 2026] Nadia: @Mo Apologies, I'll not be able to fetch the medical bag\n[1 Oct 2026] Mo: Hoping to set up the corner flags by 5 Oct 2026, but can't promise.\n[2 Oct 2026] Nadia: @Mo Promise to print the team sheets by 5 Oct 2026 if the pre-season friendly goes ahead.\n[2 Oct 2026] Nadia: Just so you know, the pre-season friendly is on as scheduled.\n[3 Oct 2026] Mo: @Lena I will set up the corner flags by 7 Oct 2026.\n[4 Oct 2026] Mo: @Lena Quick question, could I set up the corner flags by 13 Oct 2026 instead?\n[4 Oct 2026] Nadia: @Mo Yes, all good for you to set up the corner flags by 13 Oct 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 4 Oct 2026, by what date does Mo have to set up the corner flags, counting any agreed change of date?",
  "options": [
   "13 Oct 2026",
   "5 Oct 2026",
   "7 Oct 2026"
  ]
 },
 {
  "qid": "qcfa1d0e0e0",
  "kind": "choice",
  "text": "Exported by Rhea, this is the full back and forth on the payment setup.\n\nMembers: Zara, Rhea, Yuki, Ivo\nChat log (oldest first):\n[25 Feb 2026] Ivo: @Rhea Relax, I'll set up the email forwarding by 4 March 2026, promise.\n[26 Feb 2026] Rhea: @Zara Count on me to renew the hosting plan by 6 March 2026, if the courier pickup happens.\n[27 Feb 2026] Ivo: @Rhea Would it be fine if I set up the email forwarding by 8 March 2026 instead, yeah?\n[27 Feb 2026] Zara: Quick heads up, the courier pickup is scrapped.\n[28 Feb 2026] Yuki: @Ivo Yes, you can set up the email forwarding by 8 March 2026 if that suits you.\n[28 Feb 2026] Zara: @Ivo You don't have to set up the email forwarding at all\n[28 Feb 2026] Yuki: @Rhea If the product photo day is on, I'll definitely test the mobile layout by 7 March 2026.\n[7 Mar 2026] Ivo: @Rhea Ticked off my list: set up the email forwarding, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo what's the latest day Ivo has to set up the email forwarding by at the end of 10 March 2026, given any new date people agreed to?",
  "options": [
   "4 March 2026",
   "8 March 2026",
   "6 March 2026"
  ]
 },
 {
  "qid": "qd16c51c5fc",
  "kind": "choice",
  "text": "{\"chat\": \"exported\", \"about\": \"the guest review drive\", \"saved_by\": \"Nadia\", \"medium\": \"text\"}\n\nMembers: Dara, Femi, Nadia\nChat log (oldest first):\n[28 Jan 2026] Dara: @Nadia You can bet I'll restock the guest toiletries by 30 Jan 2026.\n[30 Jan 2026] Nadia: @Dara I assure you I'll change the lounge bulb by 2 Feb 2026 if the summer season launch is on.\n[30 Jan 2026] Dara: Great news, the summer season launch is on!\n[1 Feb 2026] Dara: @Femi I'll be sure to vacuum the holiday cottage by 4 Feb 2026.\n[4 Feb 2026] Dara: @Femi Is 7 Feb 2026 alright for me to vacuum the holiday cottage?\n[4 Feb 2026] Femi: @Dara Yes, you can vacuum the holiday cottage by 7 Feb 2026 instead.\n[7 Feb 2026] Nadia: @Dara You don't have to vacuum the holiday cottage at all",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat's the day Dara needs to vacuum the holiday cottage by at the end of 5 Feb 2026, after any new date the group agreed on?",
  "options": [
   "4 Feb 2026",
   "2 Feb 2026",
   "7 Feb 2026"
  ]
 },
 {
  "qid": "qb79bdf0559",
  "kind": "choice",
  "text": "Shared by Arlo, this record holds tenant and landlord messages on the rent split plan.\n\nMembers: Lena, Femi, Arlo, Dara\nChat log (oldest first):\n[18 Jun 2026] Arlo: @Lena You can bank on me to return the bin rota by 28 June 2026.\n[19 Jun 2026] Femi: @Dara If the gas safety inspection goes ahead, I'll print the tenancy agreement by 27 June 2026.\n[20 Jun 2026] Lena: Sad to report that the gas safety inspection is off.\n[20 Jun 2026] Arlo: @Dara I will make sure to copy the house keys by 22 June 2026.\n[20 Jun 2026] Dara: @Arlo Nobody needs you to copy the house keys, that's that\n[21 Jun 2026] Lena: @Femi I promise to photograph the bathroom mould by 29 June 2026 if the house hunting viewing is on.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Femi's pledge to print the tenancy agreement at the end of 27 June 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Waived",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "qdde72030c1",
  "kind": "choice",
  "text": "Messages from tenants and a landlord on the spare room plan. Saved for the file by Elif.\n\nMembers: Kai, Elif, Femi, Tess\nChat export (date | from | to | message):\n2026-02-24 | Femi | Elif | Relax, I'll buy the washing powder by 1 March 2026, promise.\n2026-02-28 | Femi | Elif | I'm withdrawing my promise to buy the washing powder\n2026-02-28 | Elif | Tess | If the fuse box inspection goes ahead, I'll gladly wipe the shared kitchen counter by 3 March 2026.\n2026-03-01 | Elif | Femi | Quick update: you do not need to buy the washing powder at all.\n2026-03-02 | Kai | group | Please note the fuse box inspection will proceed.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Femi made to buy the washing powder at the end of 5 March 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not yet due",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "qd92cad95e8",
  "kind": "yes/no",
  "text": "Exported by Tess, this is the full back and forth on the honeymoon album.\n\nMembers: Tess, Kai, Jonas\nChat log (oldest first):\n[11 Mar 2026] Kai: @Jonas You can bank on me to pick up the album prints by 17 March 2026.\n[15 Mar 2026] Kai: @Jonas Mate, I promised, may I pick up the album prints by 23 March 2026 instead?\n[15 Mar 2026] Kai: @Jonas If the rehearsal dinner is on, I'll definitely book the assistant photographer by 24 March 2026.\n[16 Mar 2026] Tess: @Kai Yes, happy for you to pick up the album prints by 23 March 2026 instead.\n[21 Mar 2026] Jonas: Sadly, the rehearsal dinner is not going ahead.",
  "question": "Is the promise Kai made to pick up the album prints in a status other than broken at the end of 22 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0222ae6bc9",
  "kind": "yes/no",
  "text": "Rented flat, shared group chat, copied by Leila, filed under the flat upgrade list.\n\nMembers: Leila, Greta, Ines\nChat log (oldest first):\n[16 Aug 2026] Greta: @Ines You can bank on me to remove the bathroom shelf by 24 Aug 2026.\n[17 Aug 2026] Leila: @Greta I will bring the step stool by 22 Aug 2026 only if the flat viewing day happens.\n[19 Aug 2026] Ines: Really pleased to say the flat viewing day will go ahead!\n[21 Aug 2026] Leila: @Greta Ticked off: bring the step stool, feels so good\n[21 Aug 2026] Leila: @Ines Count on me, I'll collect the spare flat keys by 27 Aug 2026.",
  "question": "On 24 Aug 2026 itself, has Leila not kept the promise to bring the step stool?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2bc8ff8dee",
  "kind": "choice",
  "text": "Priya forwarded this for the committee as we dig in on the winter concert.\n\nMembers: Dara, Nadia, Priya, Mo\nChat log (oldest first):\n[4 Apr 2026] Mo: Maybe I can buy the spare folders by 12 Apr 2026.\n[5 Apr 2026] Priya: @Nadia Only if the carol concert is on, I will collect the sheet music by 7 Apr 2026.\n[5 Apr 2026] Dara: Just so you know, the carol concert is on as scheduled.\n[5 Apr 2026] Mo: @Dara I will buy the spare folders by 13 Apr 2026.\n[8 Apr 2026] Nadia: @Dara You can bank on me to return the library scores by 15 Apr 2026.\n[13 Apr 2026] Mo: @Dara Got myself to buy the spare folders lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Mo doing with the promise to buy the spare folders at the end of 19 Apr 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Kept",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q9947e73807",
  "kind": "choice",
  "text": "{\"chat_export\": \"the sound mix\", \"saved_by\": \"Ivo\", \"scope\": \"group chat\"}\n\nMembers: Ivo, Lee, Leila, Tomas\nChat export (date | from | to | message):\n2026-03-01 | Tomas | Leila | I'll record the voice over by 10 Mar 2026, provided the agency review call happens.\n2026-03-02 | Ivo | Tomas | I'll send the timeline export by 9 Mar 2026, providing the client screening goes ahead.\n2026-03-06 | Lee | Leila | Count on me, I'll upload the render files by 12 Mar 2026.\n2026-03-08 | Leila | group | Quick heads up, the client screening is scrapped.\n2026-03-08 | Ivo | Tomas | Quick question, could I send the timeline export by 14 Mar 2026 instead?\n2026-03-09 | Leila | Ivo | Yes, you're welcome to send the timeline export by 14 Mar 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Ivo's promise to send the timeline export sit at the end of 11 Mar 2026, exactly?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q095c412d5c",
  "kind": "choice",
  "text": "An exported family chat on the caring rota, saved by Lena, left unchanged.\n\nMembers: Jonas, Wren, Lena, Tomas\nChat log (oldest first):\n[23 Feb 2026] Wren: @Tomas You can bank on me to collect the post by 1 March 2026.\n[23 Feb 2026] Tomas: @Jonas If the hospital appointment goes ahead, I'll gladly drop off the hot meals by 25 February 2026.\n[24 Feb 2026] Lena: Sad to report that the hospital appointment is off.\n[24 Feb 2026] Jonas: @Lena I promise to fetch the mobility aids by 28 February 2026.\n[24 Feb 2026] Jonas: @Lena Update on my side: I will not fetch the mobility aids, sorry.\n[26 Feb 2026] Lena: @Wren If the family care meeting goes ahead, I'll gladly set up the medicine dispenser by 6 March 2026.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Jonas's promise to fetch the mobility aids at the end of 1 March 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q0b2e69675f",
  "kind": "yes/no",
  "text": "Subject: chat about the peer review, forwarded\nThe chat follows below.\nRegards, Hana\n\nMembers: Arlo, Mo, Tess, Hana\nChat log (oldest first):\n[20 Jan 2026] Tess: @Mo I promise to submit the ethics application by 22 Jan 2026.\n[22 Jan 2026] Mo: @Arlo I promise to clean the glassware set by 26 Jan 2026.\n[25 Jan 2026] Tess: @Mo If the thesis defence is on, I'll definitely order the reagent kit by 2 Feb 2026.\n[27 Jan 2026] Mo: @Arlo To note: I have managed to clean the glassware set\n[27 Jan 2026] Tess: @Mo As long as the journal club is on, I will book the microscope slot by 3 Feb 2026.\n[27 Jan 2026] Tess: Sadly, the journal club is not going ahead.",
  "question": "Is Mo's promise to clean the glassware set kept on 26 Jan 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe14a212fb9",
  "kind": "yes/no",
  "text": "Shared with the club committee by Mo, the chat about the winter concert.\n\nMembers: Femi, Bruno, Mo\nChat log (oldest first):\n[30 Mar 2026] Femi: @Mo I'll set up the sound desk by 6 Apr 2026 if the sing along goes ahead.\n[1 Apr 2026] Bruno: @Femi Got it, I'll book the rehearsal room by 9 Apr 2026 for sure.\n[5 Apr 2026] Mo: Fab, we are on for the sing along as planned!\n[6 Apr 2026] Femi: @Mo Might I ask whether I could set up the sound desk by 12 Apr 2026 instead?\n[6 Apr 2026] Mo: @Femi Go ahead and set up the sound desk by 12 Apr 2026, that is fine.",
  "question": "At the end of 12 Apr 2026, has Femi broken its promise to set up the sound desk?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0a214c540c",
  "kind": "yes/no",
  "text": "Shared by Ivo, an export of a household chat about the family history, as saved.\n\nMembers: Lena, Sami, Ivo, Femi\nChat log (oldest first):\n[2 Oct 2026] Ivo: @Lena Promise to send the group invitations by 9 Oct 2026 if the garden picnic goes ahead.\n[3 Oct 2026] Femi: Sad to report that the garden picnic is off.\n[6 Oct 2026] Ivo: @Sami I will buy the name tags by 14 Oct 2026.\n[7 Oct 2026] Lena: @Femi Got it, I'll print the family tree chart by 15 Oct 2026 for sure.\n[9 Oct 2026] Lena: @Sami Committing to set up the slideshow laptop by 13 Oct 2026.\n[14 Oct 2026] Ivo: @Sami For the record: I was able to buy the name tags",
  "question": "Under the rules on the card, is it true that Ivo has not kept the promise to buy the name tags as of 15 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
