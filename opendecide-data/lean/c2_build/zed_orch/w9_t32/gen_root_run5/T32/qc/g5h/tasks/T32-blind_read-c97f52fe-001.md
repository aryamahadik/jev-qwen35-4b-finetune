# G5-H blind read (all free-form rows) T32-blind_read-c97f52fe-001 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root/T32/qc/g5h/answers/T32-blind_read-c97f52fe-001.json

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
  "qid": "q0074148ab2",
  "kind": "choice",
  "text": "Mo saved this exchange with the client about the big day.\n\nMembers: Hana, Omar, Mo, Tess\nChat log (oldest first):\n[30 Sep 2026] Mo: @Tess I'll try to charge the flash batteries by 3 Oct 2026.\n[1 Oct 2026] Mo: @Hana Committing to charge the flash batteries by 7 Oct 2026.\n[2 Oct 2026] Mo: @Hana Mind giving me until 11 Oct 2026 to charge the flash batteries?\n[4 Oct 2026] Omar: @Mo Yes, happy for you to charge the flash batteries by 11 Oct 2026 instead.\n[5 Oct 2026] Mo: @Omar If the ceremony walkthrough goes ahead, I'll gladly send the sneak peek gallery by 9 Oct 2026.\n[6 Oct 2026] Omar: @Mo Quick update: you do not need to charge the flash batteries at all.\n[8 Oct 2026] Mo: Sadly, the ceremony walkthrough won't go ahead.\n[10 Oct 2026] Mo: @Hana Got myself to charge the flash batteries lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Mo supposed to charge the flash batteries by, going by the chat at the end of 6 Oct 2026 and any agreed changes?",
  "options": [
   "9 Oct 2026",
   "7 Oct 2026",
   "11 Oct 2026"
  ]
 },
 {
  "qid": "q3fee71dcd0",
  "kind": "yes/no",
  "text": "Forwarded by Kai: a help-desk thread covering the peer review.\n\nMembers: Tess, Kai, Jonas\nChat log (oldest first):\n[8 Apr 2026] Jonas: @Tess Got it, I'll collect the lab samples by 12 April 2026 for sure.\n[8 Apr 2026] Tess: @Jonas I'll submit the ethics application by 15 April 2026, providing the grant panel goes ahead.\n[9 Apr 2026] Kai: On track for the grant panel to happen as planned.\n[9 Apr 2026] Kai: @Tess Please don't feel you have to submit the ethics application\n[13 Apr 2026] Tess: @Jonas To note: I have managed to submit the ethics application",
  "question": "Would a check of the chat at the end of 10 April 2026 show the promise Tess made to submit the ethics application as broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd2449f7911",
  "kind": "yes/no",
  "text": "Yo flatmates, Kofi shared this chat about the speed bump plan, so chip in.\n\nMembers: Yuki, Ravi, Kofi\nChat log (oldest first):\n[8 Mar 2026] Yuki: @Kofi Promise to lend the stepladder by 16 Mar 2026 if the speed camera survey goes ahead.\n[8 Mar 2026] Kofi: We are dropping the speed camera survey from the list.\n[8 Mar 2026] Ravi: @Yuki As long as the bonfire night is on, I'll sweep the pavement outside by 10 Mar 2026.\n[11 Mar 2026] Yuki: @Ravi Count on me to take in the post by 17 Mar 2026.\n[11 Mar 2026] Ravi: @Kofi Relax, I'll lock the side gate by 14 Mar 2026 for sure.\n[13 Mar 2026] Ravi: @Kofi Got myself to lock the side gate lol.",
  "question": "Under the rules on the card, is Ravi's promise to lock the side gate broken, waived, not triggered or not yet due, rather than kept, as of 15 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8d4cb07916",
  "kind": "choice",
  "text": "Team channel: the field survey\nShared by: Wren.\n\nMembers: Zara, Ravi, Wren, Ana\nChat log (oldest first):\n[18 Apr 2026] Ravi: @Wren I promise to book the microscope slot by 27 Apr 2026 if the journal club is on.\n[18 Apr 2026] Zara: Lovely, the journal club is definitely happening!\n[21 Apr 2026] Ana: @Zara Count on me, I'll order the reagent kit by 30 Apr 2026.\n[23 Apr 2026] Wren: @Ravi Count on me, I'll return the library books by 1 May 2026.\n[23 Apr 2026] Ravi: Thanks lovely, got it!\n[25 Apr 2026] Wren: @Ravi Think 3 May 2026 would work if I return the library books instead?\n[27 Apr 2026] Ana: @Wren Revised deadline is 3 May 2026, so you can return the library books.\n[29 Apr 2026] Wren: @Ravi Quick report: I've managed to return the library books\n\nTip from the tidier: each commitment here was rechecked and lines up with what Wren agreed to.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat's the day Wren needs to return the library books by at the end of 12 May 2026, after any new date the group agreed on?",
  "options": [
   "1 May 2026",
   "3 May 2026",
   "30 Apr 2026"
  ]
 },
 {
  "qid": "q5314040dbb",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the caring rota\nThis export came from Tomas and is pasted in full below.\n\nMembers: Tomas, Dara, Wren, Lee\nChat log (oldest first):\n[3 Oct 2026] Dara: @Lee It's on me to fetch the mobility aids by Sunday, October 11, 2026.\n[5 Oct 2026] Wren: @Tomas Promise to call the home nurse by Monday, October 12, 2026 if the carer handover goes ahead.\n[5 Oct 2026] Tomas: @Dara Good news, you're let off having to fetch the mobility aids\n[6 Oct 2026] Tomas: @Lee I will book the clinic transport by Monday, October 12, 2026 only if the eye test happens.\n[6 Oct 2026] Dara: @Lee Got myself to fetch the mobility aids lol.\n[8 Oct 2026] Wren: @Lee I'll collect the post by Thursday, October 15, 2026 as long as the physio session is on.",
  "question": "Is the promise Dara made to fetch the mobility aids not kept by Sunday, October 11, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q77263833b1",
  "kind": "choice",
  "text": "Priya forwarded this support chat about the family day out.\n\nMembers: Zara, Priya, Tomas\nChat log (oldest first):\n[27 Jan 2026] Priya: @Zara Provided the seaside outing happens, I'll walk the dog by 2 Feb 2026.\n[27 Jan 2026] Tomas: @Priya Promise to fetch the craft box by 3 Feb 2026 if the school play goes ahead.\n[28 Jan 2026] Priya: @Tomas I own this, I'll read the bedtime story by 5 Feb 2026.\n[30 Jan 2026] Priya: @Tomas Correction, I will not be able to read the bedtime story.\n[1 Feb 2026] Tomas: @Zara I'll pick up the school bags by 10 Feb 2026 as long as the garden tea party is on.\n[3 Feb 2026] Tomas: @Priya You don't have to read the bedtime story at all",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Priya's promise to read the bedtime story at the end of 4 Feb 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Waived",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q682f2a1308",
  "kind": "yes/no",
  "text": "Client thread on the online store move, saved by Leila for the project log.\n\nMembers: Ana, Leila, Malik\nChat log (oldest first):\n[14 Jun 2026] Ana: @Malik I will make sure to restore the old theme by 21 Jun 2026.\n[15 Jun 2026] Malik: @Ana No worries, you don't need to restore the old theme\n[16 Jun 2026] Ana: @Leila Count on me to update the product photos by 23 Jun 2026 if the stock count is on.\n[17 Jun 2026] Malik: @Ana I'll be sure to set up the email forwarding by 24 Jun 2026.\n[17 Jun 2026] Malik: Yay, the stock count is all set to go!",
  "question": "Going by the card's rules, does Ana keep the promise to update the product photos at the end of 24 Jun 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6126c80c02",
  "kind": "yes/no",
  "text": "Forwarded by Rhea: a help-desk thread covering the online store move.\n\nMembers: Rhea, Tess, Jonas, Omar\nChat log (oldest first):\n[19 Apr 2026] Jonas: @Tess I'll restore the old theme by 23 Apr 2026 if the product photo day goes ahead.\n[19 Apr 2026] Tess: On track for the product photo day to happen as planned.\n[21 Apr 2026] Tess: Hey, any luck with trying to restore the old theme?\n[22 Apr 2026] Rhea: @Tess Got it, I'll update the product photos by 27 Apr 2026 for sure.\n[24 Apr 2026] Rhea: @Tess Quick question, could I update the product photos by 2 May 2026 instead?\n[25 Apr 2026] Tess: @Rhea No, you need to update the product photos by the original date.",
  "question": "Going by the card's rules, does Jonas not keep the promise to restore the old theme at the end of 20 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q746fbe8093",
  "kind": "choice",
  "text": "Kai shared this channel export, covering the staff handbook for the team.\n\nMembers: Ines, Kai, Oskar\nChat log (oldest first):\n[8 Jul 2026] Ines: @Oskar As long as the coffee morning is on, I will fetch the parking permits by Thursday, July 16, 2026.\n[12 Jul 2026] Oskar: @Kai I will make sure to print the staff rota by Saturday, July 18, 2026.\n[12 Jul 2026] Kai: Cheers, noted.\n[13 Jul 2026] Ines: @Kai I will make sure to return the printer toner by Wednesday, July 15, 2026.\n[13 Jul 2026] Oskar: Sorry, the coffee morning is off.\n[18 Jul 2026] Oskar: @Kai Quick report: I've managed to print the staff rota",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of Wednesday, July 22, 2026, what status has Oskar's promise to print the staff rota got?",
  "options": [
   "Broken",
   "Not triggered",
   "Not yet due",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q8427a811d4",
  "kind": "choice",
  "text": "Mo saved this so we stay on the same page about the house refit, mates.\n\nMembers: Wren, Malik, Mo\nChat export (date | from | to | message):\n2026-06-25 | Wren | Mo | I assure you I'll measure the hallway for shelves by Wednesday, July 1, 2026 if the removal van arrival is on.\n2026-06-27 | Malik | group | Quick heads up, the removal van arrival is scrapped.\n2026-06-30 | Wren | Malik | I own this, I'll sweep the dust from stairs by Sunday, July 5, 2026.\n2026-07-01 | Wren | Mo | You can bank on me to pick up the grout bag by Friday, July 3, 2026.\n2026-07-01 | Malik | group | Update on your plan to sweep the dust from stairs?\n2026-07-04 | Wren | Malik | Is Thursday, July 9, 2026 alright for me to sweep the dust from stairs?\n2026-07-05 | Malik | Wren | Yes, you're welcome to sweep the dust from stairs by Thursday, July 9, 2026 instead.\n2026-07-06 | Wren | Malik | To my relief, I managed to sweep the dust from stairs.\n\nModerator ruling: promises in this group count as fine for the record, and the copy shared by Mo confirms it.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Wren supposed to sweep the dust from stairs by, going by the chat at the end of Sunday, July 12, 2026 and any agreed changes?",
  "options": [
   "Sunday, July 5, 2026",
   "Friday, July 3, 2026",
   "Thursday, July 9, 2026"
  ]
 },
 {
  "qid": "q16c9b66c02",
  "kind": "yes/no",
  "text": "Elif shared this exchange with the client about the documentary cut.\n\nMembers: Greta, Elif, Oskar, Tess\nChat export (date | from | to | message):\n2026-09-08 | Elif | Greta | I'll send the colour notes by Sunday, September 13, 2026 as long as the shoot day is on.\n2026-09-10 | Tess | Oskar | Count on me to order the stock music licence by Friday, September 18, 2026.\n2026-09-11 | Oskar | Greta | Promise to record the voice over by Sunday, September 20, 2026 if the client screening goes ahead.\n2026-09-12 | Tess | Oskar | I will fetch the raw footage by Saturday, September 19, 2026.\n2026-09-14 | Oskar | Tess | Nobody needs you to fetch the raw footage, that's that\n2026-09-17 | Tess | group | Team, the client screening is not happening.",
  "question": "Using the rules on the card, is it true that Tess has not broken the promise to fetch the raw footage at the end of Saturday, September 19, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc8e130c537",
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
  "qid": "q86150c0dbe",
  "kind": "yes/no",
  "text": "Mo forwarded this support chat, which is about the honeymoon album.\n\nMembers: Greta, Mo, Yuki\nChat log (oldest first):\n[18 Oct 2026] Mo: @Yuki Count on me to print the seating cards by 23 Oct 2026.\n[18 Oct 2026] Mo: @Yuki Update on my side: I will not print the seating cards, sorry.\n[19 Oct 2026] Yuki: @Greta I promise to pick up the album prints by 28 Oct 2026 if the cake tasting is on.\n[19 Oct 2026] Mo: Brilliant news everyone, the cake tasting is a go!\n[23 Oct 2026] Greta: @Yuki Relax, I'll fetch the spare memory cards by 30 Oct 2026, promise.",
  "question": "Under the rules on the card, is the promise Mo made to print the seating cards broken at the end of 20 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0cbfab4e51",
  "kind": "choice",
  "text": "Zara shared this support thread, which is about the winter concert.\n\nMembers: Kofi, Oskar, Arlo, Zara\nChat log (oldest first):\n[27 Jan 2026] Oskar: @Kofi As long as the sing along is on, I will fetch the choir robes by Wednesday, 4 February 2026.\n[31 Jan 2026] Zara: @Arlo Count on me, I'll print the song sheets by Saturday, 7 February 2026.\n[1 Feb 2026] Oskar: Sadly, the sing along won't go ahead.\n[2 Feb 2026] Oskar: @Kofi Would it be fine if I fetch the choir robes by Monday, 9 February 2026 instead, yeah?\n[4 Feb 2026] Kofi: @Oskar Nah, that deadline counts, mate, so please fetch the choir robes!\n[7 Feb 2026] Kofi: @Zara You are released, no requirement to print the song sheets.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Oskar doing with the promise to fetch the choir robes at the end of Thursday, 5 February 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Kept",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q96810903b6",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the annual tour\nFrom Yuki, the thread below is shared as it stands.\n\nMembers: Yuki, Malik, Ines\nChat export (date | from | to | message):\n2026-03-12 | Yuki | Ines | You can bet I'll set up the feed stop by 14 March 2026.\n2026-03-15 | Yuki | Ines | I'll service the tandem bike by 21 March 2026, providing the hill climb goes ahead.\n2026-03-15 | Yuki | group | Sorry, the hill climb is off.\n2026-03-17 | Yuki | Ines | Would it be fine if I service the tandem bike by 26 March 2026 instead, yeah?\n2026-03-18 | Ines | Yuki | We are holding the date on record, so service the tandem bike by it.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhere does Yuki stand on the promise to service the tandem bike at the end of 22 March 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q57f68556ff",
  "kind": "yes/no",
  "text": "We have been planning the old house restoration here, shared by Mo.\n\nMembers: Ravi, Mo\nChat export (date | from | to | message):\n2026-10-17 | Ravi | Mo | Lovely, I'll tidy the boot room by 23 Oct 2026 for sure.\n2026-10-17 | Ravi | Mo | Promise to defrost the old fridge by 22 Oct 2026 if the heritage fete goes ahead.\n2026-10-18 | Ravi | Mo | I will wash the sash windows by 22 Oct 2026 only if the loft clearance day happens.\n2026-10-19 | Ravi | Mo | Will attempt to find the loft ladder by 29 Oct 2026, can't promise.\n2026-10-21 | Ravi | Mo | Absolutely, I will find the loft ladder by 27 Oct 2026.\n2026-10-28 | Ravi | Mo | Log entry: find the loft ladder, carried out",
  "question": "Applying the rules on the card, did Ravi break the promise to find the loft ladder at the end of 30 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q960b62fd5f",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the summer visits\nFrom Priya, the thread below is shared as it stands.\n\nMembers: Arlo, Lee, Priya, Femi\nChat log (oldest first):\n[6 Jul 2026] Femi: Hoping to pack the picnic basket by 17 July 2026, but can't promise.\n[7 Jul 2026] Femi: @Lee I own this, I'll pack the picnic basket by 13 July 2026.\n[10 Jul 2026] Femi: @Priya Only if the garden tea party is on, I will teach the card game by 19 July 2026.\n[11 Jul 2026] Priya: @Femi Relax, mate, you're not expected to pack the picnic basket\n[13 Jul 2026] Femi: @Lee Ta-da, I went and did it: pack the picnic basket!\n[18 Jul 2026] Lee: Fab, we are on for the garden tea party as planned!",
  "question": "Under the rules on the card, is Femi's promise to pack the picnic basket kept as of 18 July 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qdd131bdc46",
  "kind": "choice",
  "text": "Tenant and agent back-and-forth on the kitchen refit, saved by Wren.\n\nMembers: Wren, Rhea, Ana\nChat log (oldest first):\n[19 Jan 2026] Ana: @Rhea I'll try to email the leak photos by 27 January 2026.\n[19 Jan 2026] Wren: @Ana I will bring the step stool by 21 January 2026.\n[21 Jan 2026] Ana: @Rhea I'll email the leak photos by 26 January 2026 if the flat viewing day goes ahead.\n[24 Jan 2026] Wren: Quick heads up, the flat viewing day is scrapped.\n[24 Jan 2026] Ana: @Rhea Would it be fine if I email the leak photos by 1 February 2026 instead, yeah?\n[24 Jan 2026] Rhea: @Ana Yes, lovely, you can email the leak photos by 1 February 2026 instead!",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Ana doing with the promise to email the leak photos at the end of 30 January 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "qe0f732d658",
  "kind": "yes/no",
  "text": "Shared by Sami, this thread covers the playground project for whoever is at the help desk.\n\nMembers: Greta, Rhea, Sami\nChat export (date | from | to | message):\n2026-01-28 | Sami | Rhea | Promise to collect the bake sale tins by 2 Feb 2026 if the reading festival goes ahead.\n2026-01-29 | Greta | Rhea | I will make sure to count the donation boxes by 31 Jan 2026.\n2026-01-30 | Greta | group | Sorry all, the reading festival is called off.\n2026-01-31 | Sami | Rhea | Any chance I can collect the bake sale tins by 5 Feb 2026 instead?\n2026-01-31 | Rhea | Sami | No change, you need to collect the bake sale tins by the original date.\n\nRuling in brief: every commitment in this chat, those from Sami included, carries the committee's full approval.",
  "question": "Looking over the chat at the end of 31 Jan 2026, did Sami break the promise to collect the bake sale tins?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q93cca22595",
  "kind": "yes/no",
  "text": "Chat attached to a support case about the family day out, shared by Zara.\n\nMembers: Rhea, Zara, Bruno\nChat log (oldest first):\n[28 Mar 2026] Zara: @Rhea See if I can sort the old photo albums by 2026-04-05, no certainty.\n[30 Mar 2026] Zara: @Bruno You can bank on me to sort the old photo albums by 2026-04-03.\n[1 Apr 2026] Zara: @Rhea I will pick up the school bags by 2026-04-09.\n[3 Apr 2026] Zara: @Bruno For the record: I was able to sort the old photo albums\n[3 Apr 2026] Bruno: @Rhea As long as the school play is on, I'll read the bedtime story by 2026-04-07.\n[6 Apr 2026] Zara: On track for the school play to happen as planned.",
  "question": "According to the rules on the card, does the promise Zara made to sort the old photo albums have any status except broken at the end of 2026-04-06?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1fb7daed76",
  "kind": "choice",
  "text": "Subject: Saved thread about the music library\nThis export came from Ivo and is pasted in full below.\n\nMembers: Greta, Ivo, Zara\nChat log (oldest first):\n[19 Aug 2026] Ivo: @Greta Count on me to buy the spare folders by Sunday, August 23, 2026.\n[20 Aug 2026] Greta: @Ivo I'll book the rehearsal room by Saturday, August 29, 2026, promise.\n[20 Aug 2026] Zara: @Ivo I will fetch the choir robes by Monday, August 24, 2026 only if the sing along happens.\n[22 Aug 2026] Ivo: @Greta I'll send the audition reminders by Saturday, August 29, 2026, provided the carol concert happens.\n[23 Aug 2026] Greta: @Ivo You don't have to buy the spare folders at all\n[26 Aug 2026] Greta: @Ivo I regret to say that I shall not book the rehearsal room.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Ivo's promise to buy the spare folders at the end of Thursday, August 27, 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q06500d2d2f",
  "kind": "yes/no",
  "text": "Hana forwarded this exchange with the landlord on the tenancy renewal talks.\n\nMembers: Tomas, Hana, Kofi\nChat log (oldest first):\n[13 Oct 2026] Hana: @Tomas Guaranteed I'll remove the bathroom shelf by 20 October 2026.\n[15 Oct 2026] Hana: @Tomas Promise to forward the gas bill by 17 October 2026 if the flat viewing day goes ahead.\n[16 Oct 2026] Hana: @Tomas I own this, I'll wipe the cooker hood by 24 October 2026.\n[18 Oct 2026] Kofi: @Tomas Count on me to ring the flat repair line by 27 October 2026, if the lease renewal call happens.\n[22 Oct 2026] Tomas: Sorry all, the lease renewal call is not happening.\n[24 Oct 2026] Hana: @Tomas Guess who managed to wipe the cooker hood, go team!",
  "question": "Applying the card's rules, does Hana's promise to wipe the cooker hood count as kept, rather than broken, waived, not triggered or not yet due, as of 24 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8d28a1bc8a",
  "kind": "yes/no",
  "text": "Greta shared this back and forth with the client about the guest list.\n\nMembers: Jonas, Greta, Elif\nChat log (oldest first):\n[8 Sep 2026] Jonas: @Greta Count on me, I'll set up the backdrop frame by 14 Sep 2026.\n[9 Sep 2026] Jonas: @Greta Ticked off: set up the backdrop frame, feels so good\n[11 Sep 2026] Elif: @Greta I assure you I'll send the sneak peek gallery by 16 Sep 2026 if the ceremony walkthrough is on.\n[11 Sep 2026] Elif: @Greta Got it, I'll charge the flash batteries by 13 Sep 2026 for sure.\n[13 Sep 2026] Greta: Brilliant news everyone, the ceremony walkthrough is a go!\n[13 Sep 2026] Greta: Any news on plans to set up the backdrop frame?",
  "question": "Going by the card's rules, does Jonas not keep the promise to set up the backdrop frame at the end of 15 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5fc2e38c2e",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the travel plans\nThis export from Rhea is pasted in full for readers who want it.\n\nMembers: Rhea, Lee, Priya\nChat export (date | from | to | message):\n2026-05-19 | Priya | Lee | Relax, I'll return the rental car keys by May 25, 2026 for sure.\n2026-05-20 | Priya | Rhea | Count on me, I'll send the packing list by May 24, 2026.\n2026-05-23 | Lee | Rhea | As long as the ferry crossing is on, I'll print the boarding passes by May 29, 2026.\n2026-05-23 | Lee | group | Sorry, the ferry crossing is off.\n2026-05-24 | Priya | Rhea | Got myself to send the packing list lol.",
  "question": "Under the rules on the card, is Priya's promise to send the packing list broken, waived, not triggered or not yet due, rather than kept, as of May 30, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q79b6474923",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the speed bump plan\nHere is a full export from Arlo, ready to read.\n\nMembers: Kofi, Arlo, Mo\nChat log (oldest first):\n[25 Mar 2026] Arlo: @Kofi You can bet I'll walk the old spaniel by Friday, 3 April 2026.\n[28 Mar 2026] Kofi: @Mo Count on me to feed the cat across the road by Saturday, 4 April 2026.\n[28 Mar 2026] Kofi: @Arlo I'll lock the side gate by Monday, 30 March 2026, providing the hedge trimming day goes ahead.\n[30 Mar 2026] Kofi: @Arlo I'll take in the post by Monday, 6 April 2026 if the speed camera survey goes ahead.\n[5 Apr 2026] Kofi: @Mo Ticked off my list: feed the cat across the road, yay.",
  "question": "According to the rules on the card, has Kofi broken the promise to feed the cat across the road at the end of Wednesday, 8 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qeeb0728e00",
  "kind": "choice",
  "text": "Tomas shared this support thread, which is about the reunion planning.\n\nMembers: Tomas, Malik, Kofi, Zara\nChat log (oldest first):\n[18 Jul 2026] Kofi: @Malik I'll try to order the cousin t-shirts by 2026-07-28, can't promise!\n[19 Jul 2026] Kofi: @Tomas I'll order the cousin t-shirts by 2026-07-25, promise.\n[21 Jul 2026] Kofi: @Tomas Would it be fine if I order the cousin t-shirts by 2026-07-28 instead, yeah?\n[22 Jul 2026] Tomas: @Kofi I'll print the family tree chart by 2026-07-30 if the reunion lunch goes ahead.\n[25 Jul 2026] Tomas: @Kofi Go ahead and order the cousin t-shirts by 2026-07-28, that is fine.\n[26 Jul 2026] Malik: @Kofi Relax, mate, you're not expected to order the cousin t-shirts\n[27 Jul 2026] Tomas: @Malik I promise to buy the name tags by 2026-07-29 if the grandparents visit is on.\n[30 Jul 2026] Kofi: @Tomas Log entry: order the cousin t-shirts, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Kofi due to order the cousin t-shirts at the end of 2026-07-27, after any agreed rescheduling?",
  "options": [
   "2026-07-28",
   "2026-07-30",
   "2026-07-25"
  ]
 },
 {
  "qid": "q059f143dce",
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
  "qid": "q84f5c78d53",
  "kind": "choice",
  "text": "Subject: Saved thread about the winter concert\nHere is a full export from Ines, ready to read.\n\nMembers: Tomas, Malik, Ivo, Ines\nChat log (oldest first):\n[27 Oct 2026] Tomas: Hoping to fix the stand microphones by 30 October 2026, but can't promise.\n[28 Oct 2026] Tomas: @Ines I will fix the stand microphones by 4 November 2026 only if the choir festival happens.\n[29 Oct 2026] Ivo: Lovely, the choir festival is definitely happening!\n[31 Oct 2026] Malik: @Ines You can bank on me to return the library scores by 2 November 2026.\n[1 Nov 2026] Malik: @Ines To my relief, I managed to return the library scores.\n[4 Nov 2026] Ivo: @Tomas Forget it, you won't need to fix the stand microphones",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Tomas gave to fix the stand microphones have at the end of 9 November 2026?",
  "options": [
   "Waived",
   "Broken",
   "Not yet due",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "q0d356fd539",
  "kind": "yes/no",
  "text": "We have been planning the kitchen garden project here, shared by Bruno.\n\nMembers: Hana, Kai, Bruno, Ravi\nChat log (oldest first):\n[8 Jun 2026] Bruno: @Hana If the plot inspection goes ahead, I'll gladly fix the shed door by 14 Jun 2026.\n[12 Jun 2026] Hana: @Kai Provided the harvest supper happens, I will stake the tomato canes by 20 Jun 2026.\n[13 Jun 2026] Hana: @Ravi It's on me to build the compost bay by 16 Jun 2026.\n[15 Jun 2026] Ravi: @Hana Forget it, you won't need to build the compost bay\n[15 Jun 2026] Bruno: @Kai Got it, I'll sow the broad beans by 22 Jun 2026 for sure.\n[18 Jun 2026] Bruno: @Kai Ta-da, I went and did it: sow the broad beans!",
  "question": "Applying the rules on the card, can Hana's promise to build the compost bay be said to have not been broken at the end of 15 Jun 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb13a7334fb",
  "kind": "choice",
  "text": "Volunteers, here is the junior section thread that Lena forwarded for us.\n\nMembers: Ivo, Omar, Zara, Lena\nChat log (oldest first):\n[16 Feb 2026] Ivo: @Zara I'll wash the away kit by Monday, 23 February 2026 if the presentation evening goes ahead.\n[21 Feb 2026] Ivo: @Zara Count on me to pump the match balls by Sunday, 1 March 2026.\n[21 Feb 2026] Ivo: @Zara Sorry, I won't pump the match balls after all\n[21 Feb 2026] Ivo: Please note the presentation evening will proceed.\n[23 Feb 2026] Ivo: @Zara Is Wednesday, 25 February 2026 alright for me to wash the away kit?\n[23 Feb 2026] Lena: @Ivo Yes, you can wash the away kit by Wednesday, 25 February 2026 if that suits you.\n[28 Feb 2026] Ivo: @Zara Got myself to wash the away kit lol.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Ivo supposed to wash the away kit by, going by the chat at the end of Thursday, 26 February 2026 and any agreed changes?",
  "options": [
   "Sunday, 1 March 2026",
   "Wednesday, 25 February 2026",
   "Monday, 23 February 2026"
  ]
 },
 {
  "qid": "q84cdbaf884",
  "kind": "choice",
  "text": "Sami shared this family chat about the trip itinerary for the relatives.\n\nMembers: Ivo, Rhea, Sami\nChat export (date | from | to | message):\n2026-02-07 | Sami | Ivo | You can bet I'll buy the packing cubes by 14 February 2026.\n2026-02-08 | Sami | Ivo | I committed to buy the packing cubes, can I do that by 17 February 2026 instead?\n2026-02-11 | Rhea | Ivo | Provided the family cookout happens, I'll book the airport parking by 13 February 2026.\n2026-02-12 | Ivo | group | Update: the family cookout is going ahead as planned.\n2026-02-14 | Ivo | Sami | Forget it, you won't need to buy the packing cubes",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 14 February 2026, what status has Sami's promise to buy the packing cubes got?",
  "options": [
   "Kept",
   "Broken",
   "Not yet due",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "qa5eb0f5367",
  "kind": "choice",
  "text": "Parents and cousins, this is where we sort out the vegetable plot plan. Saved by Arlo.\n\nMembers: Tess, Rhea, Arlo, Dara\nChat log (oldest first):\n[19 Jan 2026] Rhea: @Dara I'll stake the tomato canes by 21 Jan 2026 if the plot inspection goes ahead.\n[20 Jan 2026] Dara: @Rhea Guaranteed I'll sharpen the hand hoe by 24 Jan 2026.\n[20 Jan 2026] Dara: @Rhea Gutted to say I won't sharpen the hand hoe, sorry team\n[20 Jan 2026] Tess: @Dara Ah, no stress, no need for you to sharpen the hand hoe\n[21 Jan 2026] Rhea: @Tess Promise to deliver the surplus runner beans by 28 Jan 2026 if the allotment site visit goes ahead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Dara made to sharpen the hand hoe at the end of 21 Jan 2026?",
  "options": [
   "Kept",
   "Waived",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qff63bf3623",
  "kind": "choice",
  "text": "Our flat chat about the old house restoration, shared by Kofi for whoever lives here.\n\nMembers: Ivo, Kofi, Arlo\nChat log (oldest first):\n[15 Aug 2026] Kofi: @Arlo I own this, I'll oil the back door hinges by August 18, 2026.\n[15 Aug 2026] Ivo: @Kofi Nobody needs you to oil the back door hinges, that's that\n[16 Aug 2026] Ivo: @Kofi Provided the heritage fete happens, I will clear the kitchen sink by August 21, 2026.\n[18 Aug 2026] Ivo: @Kofi Committing to mend the garden gate by August 23, 2026.\n[18 Aug 2026] Arlo: @Ivo If the loft clearance day goes ahead, I'll find the loft ladder by August 21, 2026.\n[21 Aug 2026] Kofi: @Arlo Quick report: I've managed to oil the back door hinges",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Kofi made to oil the back door hinges at the end of August 22, 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q857f42b067",
  "kind": "choice",
  "text": "Our flat chat about the summer lets season, saved by Mo for whoever lives here.\n\nMembers: Leila, Mo, Greta, Yuki\nChat log (oldest first):\n[22 Mar 2026] Yuki: @Mo Committing to wheel the bins out by 28 March 2026.\n[24 Mar 2026] Yuki: @Mo Mind giving me until 2 April 2026 to wheel the bins out?\n[28 Mar 2026] Leila: @Yuki Yes, you're welcome to wheel the bins out by 2 April 2026 instead.\n[28 Mar 2026] Leila: @Yuki If the owner handover visit is on, I'll definitely scrub the hot tub by 5 April 2026.\n[29 Mar 2026] Yuki: @Mo Quick report: I've managed to wheel the bins out\n[29 Mar 2026] Leila: @Greta I will wash the beach towels by 4 April 2026.\n[31 Mar 2026] Leila: @Greta I'll restock the guest toiletries by 3 April 2026, providing the summer season launch goes ahead.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of 31 March 2026, what is the date by which Yuki has to wheel the bins out, counting any agreed change?",
  "options": [
   "2 April 2026",
   "5 April 2026",
   "28 March 2026"
  ]
 },
 {
  "qid": "q6b6275b845",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the online store move\nFrom Yuki, the thread below is shared as it stands.\n\nMembers: Yuki, Ivo, Greta, Nadia\nChat log (oldest first):\n[20 Apr 2026] Yuki: @Greta Count on me to restore the old theme by April 27, 2026, if the courier pickup happens.\n[23 Apr 2026] Ivo: @Yuki Count on me, I'll send the stock spreadsheet by April 28, 2026.\n[25 Apr 2026] Ivo: Update: the courier pickup is going ahead as planned.\n[26 Apr 2026] Greta: @Ivo Quick update: you do not need to send the stock spreadsheet at all.\n[27 Apr 2026] Nadia: @Yuki Don't sweat it, there's no need to restore the old theme",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Yuki's undertaking to restore the old theme hold at the end of May 1, 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Broken",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qf7a22bb546",
  "kind": "choice",
  "text": "Attached chat: the onboarding flow\nShared by: Hana\n\nMembers: Ana, Kai, Hana\nChat export (date | from | to | message):\n2026-01-07 | Hana | Ana | Relax, I'll merge the login branch by 14 January 2026, promise.\n2026-01-08 | Hana | Kai | Count on me to deploy the staging build by 13 January 2026.\n2026-01-11 | Ana | Hana | I assure you I'll restart the build server by 16 January 2026 if the planning session is on.\n2026-01-12 | Ana | Kai | Count on me to run the security scan by 19 January 2026.\n2026-01-12 | Hana | group | Team, the planning session is not happening.\n2026-01-16 | Hana | Ana | Got myself to merge the login branch lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Hana made to merge the login branch at the end of 19 January 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Kept",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q8e0a3a0d5c",
  "kind": "choice",
  "text": "Team channel export, shared by Kai, which is about the visitor policy.\n\nMembers: Hana, Kai, Mo\nChat log (oldest first):\n[24 Feb 2026] Hana: @Mo I'll renew the fire extinguisher service by 3 March 2026, providing the building survey goes ahead.\n[28 Feb 2026] Mo: Yep, the building survey is on as planned.\n[1 Mar 2026] Hana: @Mo Is it all right if I renew the fire extinguisher service by 5 March 2026 instead?\n[1 Mar 2026] Mo: @Hana Yes, you can renew the fire extinguisher service by 5 March 2026 instead.\n[2 Mar 2026] Kai: @Hana Don't sweat it, there's no need to renew the fire extinguisher service\n[3 Mar 2026] Kai: @Mo I promise to collect the visitor badges by 6 March 2026.\n[5 Mar 2026] Hana: @Mo Guess what, I managed to renew the fire extinguisher service!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nFollowing the rules set out on the card, what date governs Hana's commitment to renew the fire extinguisher service at the end of 9 March 2026, once any agreed shift in the date is factored in?",
  "options": [
   "5 March 2026",
   "6 March 2026",
   "3 March 2026"
  ]
 },
 {
  "qid": "qdc0da5e04b",
  "kind": "yes/no",
  "text": "Forwarded by Tess, this thread on the attic conversion idea stays attached to the ticket.\n\nMembers: Jonas, Tess, Sami, Tomas\nChat export (date | from | to | message):\n2026-10-01 | Sami | Jonas | I will make sure to sort the recycling bags by Thursday, October 8, 2026.\n2026-10-04 | Sami | Tess | Relax, I'll defrost the top freezer by Friday, October 9, 2026 for sure.\n2026-10-06 | Sami | Tess | Quick report: I've managed to defrost the top freezer\n2026-10-07 | Jonas | Tess | Count on me to drop the parcel upstairs by Sunday, October 11, 2026, if the landlord inspection walk happens.\n2026-10-08 | Sami | group | Great news, the landlord inspection walk is on!",
  "question": "Has Sami kept the promise to defrost the top freezer at the end of Sunday, October 11, 2026, instead of broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2b7696a35b",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the big day\nHere is a full export from Omar, ready to read.\n\nMembers: Femi, Lena, Sami, Omar\nChat log (oldest first):\n[21 Jul 2026] Femi: @Lena Provided the ceremony walkthrough happens, I will print the seating cards by 27 July 2026.\n[22 Jul 2026] Lena: @Sami I'll try to collect the venue floor plan by 24 July 2026.\n[23 Jul 2026] Lena: @Femi Count on me, I'll collect the venue floor plan by 29 July 2026.\n[24 Jul 2026] Lena: @Omar Lovely, I'll send the sneak peek gallery by 27 July 2026 if the rehearsal dinner is on.\n[24 Jul 2026] Omar: @Lena You are released, no requirement to collect the venue floor plan.\n[29 Jul 2026] Lena: @Femi Guess who managed to collect the venue floor plan, go team!",
  "question": "Per the card's rules, on 29 July 2026, has Lena's promise to collect the venue floor plan been broken, waived, not triggered or not yet due, rather than kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q98ec0d6c08",
  "kind": "yes/no",
  "text": "Client thread on the documentary cut, saved by Ravi for the project log.\n\nMembers: Ravi, Mo, Priya\nChat export (date | from | to | message):\n2026-02-05 | Ravi | Priya | You can bet I'll export the subtitle files by 7 February 2026.\n2026-02-07 | Mo | Ravi | Count on me to fetch the raw footage by 14 February 2026 if the grading session is on.\n2026-02-07 | Ravi | Priya | Would it be fine if I export the subtitle files by 12 February 2026 instead, yeah?\n2026-02-07 | Priya | Ravi | No new date, so please export the subtitle files by the date given.\n2026-02-09 | Ravi | group | Lovely, the grading session is definitely happening!\n2026-02-14 | Mo | Ravi | Ticked off: fetch the raw footage, feels so good",
  "question": "Does Mo's promise to fetch the raw footage hold up as kept at the end of 15 February 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q78a8bcc526",
  "kind": "choice",
  "text": "Hana shared this channel export, covering the onboarding flow for the team.\n\nMembers: Hana, Wren, Ivo\nChat log (oldest first):\n[3 Oct 2026] Wren: @Ivo I'll see if I can review the pull request by Tuesday, October 6, 2026.\n[4 Oct 2026] Wren: @Ivo Provided the penetration test happens, I'll review the pull request by Thursday, October 8, 2026.\n[4 Oct 2026] Hana: Please note the penetration test will proceed.\n[9 Oct 2026] Hana: @Wren Got it, I'll rotate the test keys by Thursday, October 15, 2026 for sure.\n[13 Oct 2026] Hana: @Wren I committed to rotate the test keys, can I do that by Monday, October 19, 2026 instead?\n[13 Oct 2026] Wren: @Hana Nah, the date's staying put, so you can rotate the test keys.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Wren's promise to review the pull request at the end of Tuesday, October 6, 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Kept",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "qfe5dd17eae",
  "kind": "choice",
  "text": "Volunteers, here is the junior section thread that Lena forwarded for us.\n\nMembers: Ivo, Omar, Zara, Lena\nChat log (oldest first):\n[16 Feb 2026] Ivo: @Zara I'll wash the away kit by Monday, 23 February 2026 if the presentation evening goes ahead.\n[21 Feb 2026] Ivo: @Zara Count on me to pump the match balls by Sunday, 1 March 2026.\n[21 Feb 2026] Ivo: @Zara Sorry, I won't pump the match balls after all\n[21 Feb 2026] Ivo: Please note the presentation evening will proceed.\n[23 Feb 2026] Ivo: @Zara Is Wednesday, 25 February 2026 alright for me to wash the away kit?\n[23 Feb 2026] Omar: @Ivo Yes, you can wash the away kit by Wednesday, 25 February 2026 if that suits you.\n[28 Feb 2026] Ivo: @Zara Got myself to wash the away kit lol.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Ivo supposed to wash the away kit by, going by the chat at the end of Thursday, 26 February 2026 and any agreed changes?",
  "options": [
   "Monday, 23 February 2026",
   "Sunday, 1 March 2026",
   "Wednesday, 25 February 2026"
  ]
 },
 {
  "qid": "q68982a9a89",
  "kind": "choice",
  "text": "Forwarded by Ines: a help-desk thread covering the loft conversion.\n\nMembers: Priya, Tomas, Malik, Ines\nChat export (date | from | to | message):\n2026-01-27 | Priya | Tomas | I'll scrape the old wallpaper by 3 Feb 2026 if the mortgage valuation visit goes ahead.\n2026-02-01 | Ines | Malik | Guaranteed I'll pay the plumbing invoice by 5 Feb 2026.\n2026-02-01 | Ines | Malik | I'll sweep the dust from stairs by 6 Feb 2026 as long as the removal van arrival is on.\n2026-02-02 | Priya | Ines | No need to pay the plumbing invoice, I'm letting you off\n2026-02-02 | Ines | Malik | Ticked off my list: pay the plumbing invoice, yay.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Ines's promise to pay the plumbing invoice at the end of 8 Feb 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not triggered",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q2b87af1871",
  "kind": "yes/no",
  "text": "Forwarded by Tess, this thread on the attic conversion idea stays attached to the ticket.\n\nMembers: Jonas, Tess, Sami, Tomas\nChat export (date | from | to | message):\n2026-10-01 | Sami | Jonas | I will make sure to sort the recycling bags by Thursday, October 8, 2026.\n2026-10-04 | Sami | Tess | Relax, I'll defrost the top freezer by Friday, October 9, 2026 for sure.\n2026-10-06 | Sami | Tess | Quick report: I've managed to defrost the top freezer\n2026-10-07 | Jonas | Tess | Count on me to drop the parcel upstairs by Sunday, October 11, 2026, if the landlord inspection walk happens.\n2026-10-08 | Sami | group | Great news, the landlord inspection walk is on!",
  "question": "Is Sami's promise to defrost the top freezer broken, waived, not triggered or not yet due as of Sunday, October 11, 2026, instead of kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2aed4c86ce",
  "kind": "yes/no",
  "text": "Yo flatmates, Rhea shared this chat about the loft conversion, so chip in.\n\nMembers: Wren, Femi, Yuki, Rhea\nChat export (date | from | to | message):\n2026-03-11 | Wren | Femi | Guaranteed I'll collect the sanding pads by 15 Mar 2026.\n2026-03-11 | Rhea | Wren | Ah, no stress, no need for you to collect the sanding pads\n2026-03-12 | Wren | Femi | Got myself to collect the sanding pads lol.\n2026-03-14 | Rhea | Wren | Lovely, I'll return the tile cutter by 16 Mar 2026 if the removal van arrival is on.\n2026-03-17 | Yuki | Femi | I'll sweep the dust from stairs by 20 Mar 2026, providing the damp survey inspection goes ahead.",
  "question": "On the card, was Wren's promise to collect the sanding pads kept, rather than broken, waived, not triggered or not yet due, at the end of 14 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q007956c953",
  "kind": "choice",
  "text": "Here is the guest travel plans, posted by Rhea for the family to read.\n\nMembers: Omar, Rhea, Malik\nChat log (oldest first):\n[31 May 2026] Omar: @Malik It's on me to buy the name tags by Thursday, June 4, 2026.\n[31 May 2026] Omar: @Rhea Count on me, I'll order the cousin t-shirts by Friday, June 5, 2026.\n[4 Jun 2026] Omar: @Malik Ta-da, I went and did it: buy the name tags!\n[5 Jun 2026] Rhea: @Malik If the family quiz goes ahead, I'll set up the slideshow laptop by Thursday, June 11, 2026.\n[5 Jun 2026] Omar: @Malik Provided the grandparents visit happens, I'll send the group invitations by Sunday, June 14, 2026.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Omar's promise to buy the name tags at the end of Tuesday, June 9, 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Kept",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q3fcb13099e",
  "kind": "choice",
  "text": "Wren forwarded this for the committee as we dig in on the volunteer roster.\n\nMembers: Wren, Tess, Arlo\nChat export (date | from | to | message):\n2026-09-16 | Arlo | Tess | Only if the governors meeting is on, I will set up the book stall by 18 September 2026.\n2026-09-16 | Tess | group | Yay, the governors meeting is all set to go!\n2026-09-20 | Wren | Tess | See if I can count the donation boxes by 1 October 2026, no certainty.\n2026-09-21 | Wren | Arlo | I'll count the donation boxes by 29 September 2026, promise.\n2026-09-21 | Wren | Tess | Lovely, I'll label the raffle prizes by 25 September 2026 for sure.\n2026-09-27 | Wren | Arlo | To my relief, I managed to count the donation boxes.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Wren gave to count the donation boxes have at the end of 3 October 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qb85f8f0d49",
  "kind": "choice",
  "text": "Leila saved this exchange with the client about the sound mix.\n\nMembers: Malik, Jonas, Leila, Ravi\nChat export (date | from | to | message):\n2026-10-21 | Ravi | Jonas | Count on me to send the timeline export by 28 October 2026 if the voiceover session is on.\n2026-10-23 | Ravi | Malik | Aiming to order the stock music licence by 3 November 2026, we'll see.\n2026-10-25 | Ravi | Leila | Guaranteed I'll order the stock music licence by 1 November 2026.\n2026-10-25 | Jonas | group | Afraid the voiceover session is called off.\n2026-10-26 | Jonas | Ravi | Got it, I'll label the clip folders by 31 October 2026 for sure.\n2026-10-29 | Ravi | Leila | I committed to order the stock music licence, can I do that by 5 November 2026 instead?\n2026-10-29 | Malik | Ravi | Yes, all good for you to order the stock music licence by 5 November 2026 instead.\n2026-11-01 | Ravi | Leila | I'm withdrawing my promise to order the stock music licence",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Ravi to order the stock music licence at the end of 2 November 2026, counting any agreed change of date?",
  "options": [
   "1 November 2026",
   "31 October 2026",
   "5 November 2026"
  ]
 },
 {
  "qid": "q7bad185f8e",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the bathroom refit\nThis export from Omar is pasted in full for readers who want it.\n\nMembers: Ivo, Omar, Bruno\nChat export (date | from | to | message):\n2026-07-09 | Ivo | Bruno | Count on me to hang the new curtain rail by 16 July 2026.\n2026-07-11 | Bruno | Ivo | As long as the mortgage valuation visit is on, I'll fetch the paint samples by 19 July 2026.\n2026-07-12 | Omar | Bruno | It's on me to scrape the old wallpaper by 21 July 2026.\n2026-07-15 | Ivo | Bruno | To note: I have managed to hang the new curtain rail\n2026-07-15 | Omar | group | Fab, we are on for the mortgage valuation visit as planned!\n2026-07-19 | Bruno | Ivo | Ticked off my list: fetch the paint samples, yay.",
  "question": "Under the rules on the card, is Bruno's promise to fetch the paint samples kept as of 19 July 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2f42670c11",
  "kind": "yes/no",
  "text": "Messages with the letting agent about the shared kitchen scheme, forwarded by Malik for the rental file.\n\nMembers: Rhea, Malik, Elif\nChat export (date | from | to | message):\n2026-01-14 | Elif | group | Wish me luck, hoping to turn the heating timer by 24 January 2026.\n2026-01-16 | Elif | Malik | Lovely, I'll turn the heating timer by 20 January 2026 if the lodger farewell supper is on.\n2026-01-17 | Elif | group | Fab, we are on for the lodger farewell supper as planned!\n2026-01-17 | Rhea | Elif | Nobody needs you to turn the heating timer, that's that\n2026-01-20 | Malik | Rhea | I own this, I'll cut a spare door key by 22 January 2026.\n2026-01-21 | Malik | Rhea | To note: I have managed to cut a spare door key",
  "question": "Did Elif keep the promise to turn the heating timer as of 17 January 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
