# G5-H blind read T32-blind_read-82a505c2-006 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root/T32/qc/g5h/answers/T32-blind_read-82a505c2-006.json

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
  "qid": "q165517ebd8",
  "kind": "choice",
  "text": "Team export header with the peer review, saved by Greta.\n\nMembers: Oskar, Kai, Greta, Yuki\nChat log (oldest first):\n[13 Sep 2026] Greta: @Yuki I assure you I'll submit the ethics application by 20 Sep 2026 if the seminar series is on.\n[16 Sep 2026] Yuki: Please note the seminar series will proceed.\n[16 Sep 2026] Yuki: @Oskar Got it, I'll order the reagent kit by 21 Sep 2026 for sure.\n[18 Sep 2026] Yuki: @Oskar Mum, I did order the reagent kit, haha.\n[21 Sep 2026] Greta: @Yuki Ticked off my list: submit the ethics application, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Greta's promise to submit the ethics application at the end of 21 Sep 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q9cca8f5e40",
  "kind": "yes/no",
  "text": "Read up on the house rules debate, flatmates, as Rhea exported it.\n\nMembers: Ines, Rhea, Arlo\nChat log (oldest first):\n[8 Mar 2026] Ines: @Arlo I'll defrost the old fridge by 15 Mar 2026 as long as the chimney sweep visit is on.\n[8 Mar 2026] Arlo: Hoping to oil the back door hinges by 17 Mar 2026, can't promise.\n[9 Mar 2026] Arlo: @Ines Count on me to oil the back door hinges by 14 Mar 2026.\n[10 Mar 2026] Rhea: @Arlo Quick update: you do not need to oil the back door hinges at all.\n[14 Mar 2026] Arlo: @Ines Quick report: I've managed to oil the back door hinges\n[15 Mar 2026] Rhea: @Arlo Count on me to bleed the attic radiators by 22 Mar 2026, if the house viewing happens.",
  "question": "Was the promise to oil the back door hinges from Arlo kept on 15 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q24a54f6825",
  "kind": "choice",
  "text": "{\"export_type\": \"group chat export\", \"chat_topic\": \"the shop rebuild\", \"saved_by\": \"Ravi\"}\n\nMembers: Rhea, Ravi, Hana, Ana\nChat log (oldest first):\n[20 Sep 2026] Rhea: @Ana Will attempt to update the product photos by 30 September 2026, can't promise.\n[21 Sep 2026] Rhea: @Ana If the product photo day is on, I'll definitely update the product photos by 27 September 2026.\n[22 Sep 2026] Rhea: Lovely, the product photo day is definitely happening!\n[26 Sep 2026] Hana: @Rhea It's on me to send the stock spreadsheet by 2 October 2026.\n[26 Sep 2026] Hana: @Rhea Think 6 October 2026 would work if I send the stock spreadsheet instead?\n[26 Sep 2026] Rhea: @Hana No new date, so please send the stock spreadsheet by the date given.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Rhea's pledge to update the product photos at the end of 27 September 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Kept",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q616f640f86",
  "kind": "choice",
  "text": "Attached chat: the caring rota\nShared by: Greta\n\nMembers: Greta, Rhea, Yuki\nChat log (oldest first):\n[24 Mar 2026] Yuki: @Rhea Wish me luck, hoping to print the care schedule by Friday, March 27, 2026.\n[26 Mar 2026] Yuki: @Rhea Got it, I'll print the care schedule by Friday, April 3, 2026 for sure.\n[29 Mar 2026] Rhea: @Yuki No need to print the care schedule, I'm letting you off\n[29 Mar 2026] Rhea: @Greta Provided the family care meeting happens, I'll book the clinic transport by Wednesday, April 1, 2026.\n[30 Mar 2026] Greta: Team, the family care meeting is not happening.\n[1 Apr 2026] Yuki: @Rhea Guess who managed to print the care schedule, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Yuki's promise to print the care schedule at the end of Friday, April 3, 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qe9803268c0",
  "kind": "yes/no",
  "text": "Subject: export of the group chat on the spring campaign\nHere is the chat as saved by Dara, pasted below.\n\nMembers: Femi, Dara, Lee, Zara\nChat export (date | from | to | message):\n2026-06-27 | Zara | Dara | I own this, I'll pay the printing invoice by 1 Jul 2026.\n2026-06-27 | Dara | group | Thanks lovely, got it!\n2026-06-29 | Femi | Lee | Ticket's mine, I'll set up the analytics dashboard by 3 Jul 2026.\n2026-06-29 | Femi | Lee | As long as the annual review is on, I'll fix the landing page headline by 2 Jul 2026.\n2026-06-30 | Dara | group | Yep, the annual review is on as planned.\n2026-07-01 | Zara | Dara | To note: I have managed to pay the printing invoice",
  "question": "Has Zara kept the promise to pay the printing invoice as of 6 Jul 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q91fa501e96",
  "kind": "yes/no",
  "text": "Project thread between a freelancer and a client on the shop rebuild, saved by Arlo.\n\nMembers: Lee, Hana, Arlo, Ravi\nChat log (oldest first):\n[9 Aug 2026] Ravi: @Arlo Count on me to renew the hosting plan by Sunday, August 16, 2026 if the market day is on.\n[9 Aug 2026] Arlo: Thanks lovely, got it!\n[10 Aug 2026] Arlo: @Ravi Count on me to fetch the domain login by Wednesday, August 19, 2026.\n[11 Aug 2026] Ravi: Really pleased to say the market day will go ahead!\n[15 Aug 2026] Hana: @Arlo Forget it, you won't need to fetch the domain login\n[16 Aug 2026] Ravi: @Arlo To note: I have managed to renew the hosting plan",
  "question": "On the card, was Ravi's promise to renew the hosting plan kept, rather than broken, waived, not triggered or not yet due, at the end of Wednesday, August 19, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q40dc397340",
  "kind": "yes/no",
  "text": "Subject: chat about the music library, forwarded\nThe chat follows below.\nRegards, Rhea\n\nMembers: Kai, Rhea, Greta, Tomas\nChat log (oldest first):\n[27 Oct 2026] Greta: @Kai I promise to book the rehearsal room by 4 Nov 2026 if the choir festival is on.\n[28 Oct 2026] Greta: @Tomas Lovely, I'll move the piano by 1 Nov 2026 if the summer recital is on.\n[28 Oct 2026] Kai: @Greta Absolutely, I will collect the sheet music by 2 Nov 2026.\n[29 Oct 2026] Kai: @Tomas I promise to fetch the choir robes by 31 Oct 2026.\n[29 Oct 2026] Kai: @Tomas Update on my side: I will not fetch the choir robes, sorry.\n[2 Nov 2026] Greta: @Kai Ah, no stress, no need for you to collect the sheet music",
  "question": "Under the rules on the card, is Kai's promise to collect the sheet music broken, waived, not triggered or not yet due, rather than kept, as of 3 Nov 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qea4f09baf0",
  "kind": "choice",
  "text": "Client chat in a freelance log: the honeymoon album, passed on by Ivo.\n\nMembers: Elif, Ivo, Hana\nChat log (oldest first):\n[2 Aug 2026] Elif: @Ivo I'll try to book the assistant photographer by Wednesday, 12 August 2026.\n[3 Aug 2026] Elif: @Ivo I'll pick up the album prints by Monday, 10 August 2026 if the venue visit goes ahead.\n[4 Aug 2026] Elif: @Ivo I will make sure to book the assistant photographer by Saturday, 8 August 2026.\n[8 Aug 2026] Elif: @Ivo Apologies, I'll not be able to book the assistant photographer\n[8 Aug 2026] Ivo: @Elif Forget it, you won't need to book the assistant photographer\n[9 Aug 2026] Elif: @Ivo I'll send the sneak peek gallery by Sunday, 16 August 2026, providing the rehearsal dinner goes ahead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of Tuesday, 11 August 2026, which status does Elif have for the promise to book the assistant photographer?",
  "options": [
   "Waived",
   "Not triggered",
   "Broken",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "qa30e5a06d4",
  "kind": "choice",
  "text": "{\"export_type\": \"group chat export\", \"chat_topic\": \"the showreel refresh\", \"saved_by\": \"Greta\"}\n\nMembers: Greta, Femi, Dara\nChat export (date | from | to | message):\n2026-08-03 | Femi | Dara | Lovely, I'll export the subtitle files by 12 August 2026 if the grading session is on.\n2026-08-04 | Dara | Greta | Count on me, I'll record the voice over by 9 August 2026.\n2026-08-08 | Dara | group | Sorry all, the grading session is not happening.\n2026-08-09 | Dara | Femi | Got it, I'll send the timeline export by 14 August 2026 for sure.\n2026-08-09 | Dara | Femi | Is 20 August 2026 alright for me to send the timeline export?\n2026-08-11 | Femi | Greta | Lovely, I'll back up the project drives by 13 August 2026 for sure.\n2026-08-12 | Greta | Dara | Yes, you're welcome to send the timeline export by 20 August 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 16 August 2026, by what date does Dara have to send the timeline export, counting any agreed change of date?",
  "options": [
   "20 August 2026",
   "13 August 2026",
   "14 August 2026"
  ]
 },
 {
  "qid": "q98f9161ca5",
  "kind": "yes/no",
  "text": "Flat chat export, saved by Ana\nCovers the balcony garden project, shared among the housemates.\n\nMembers: Oskar, Ana\nChat log (oldest first):\n[24 Jun 2026] Ana: @Oskar I'll ring the flat repair line by Friday, 26 June 2026 if the boiler annual check goes ahead.\n[24 Jun 2026] Oskar: Team, the boiler annual check is not happening.\n[25 Jun 2026] Ana: @Oskar Count on me to collect the spare flat keys by Sunday, 28 June 2026.\n[25 Jun 2026] Ana: @Oskar Quick question, could I collect the spare flat keys by Saturday, 4 July 2026 instead?\n[26 Jun 2026] Ana: @Oskar Guess what, I managed to collect the spare flat keys!\n[27 Jun 2026] Oskar: @Ana I promise to measure the kitchen for fridge by Wednesday, 1 July 2026.",
  "question": "Does the card's rule set show that Ana has not kept the promise to collect the spare flat keys at the end of Sunday, 28 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8249e2fd91",
  "kind": "choice",
  "text": "Written exchange with the letting agent, covering the student house hunt, which Jonas copied into the file.\n\nMembers: Ivo, Priya, Jonas\nChat log (oldest first):\n[20 Feb 2026] Ivo: @Jonas Lovely, I'll copy the house keys by 26 February 2026 if the move in day is on.\n[20 Feb 2026] Ivo: @Jonas I will make sure to ring the letting agent by 24 February 2026.\n[22 Feb 2026] Ivo: @Priya You can bet I'll scan the council tax letter by 1 March 2026.\n[23 Feb 2026] Ivo: Scrapping the move in day, apologies to all.\n[1 Mar 2026] Jonas: @Ivo You don't have to scan the council tax letter at all",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Ivo's commitment to scan the council tax letter have at the end of 1 March 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Broken",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "q2a013d5a16",
  "kind": "choice",
  "text": "Chat from the support case covering the front garden scheme, exported by Rhea.\n\nMembers: Rhea, Arlo, Omar\nChat export (date | from | to | message):\n2026-04-16 | Rhea | Omar | Relax, I'll take in the post by Thursday, April 23, 2026, promise.\n2026-04-17 | Arlo | Omar | As long as the parking permit visit is on, I'll sweep the pavement outside by Wednesday, April 22, 2026.\n2026-04-17 | Rhea | group | Afraid the parking permit visit is called off.\n2026-04-17 | Rhea | Arlo | Relax, I'll walk the old spaniel by Saturday, April 25, 2026 for sure.\n2026-04-19 | Rhea | Arlo | Is it all right if I walk the old spaniel by Wednesday, April 29, 2026 instead?\n2026-04-25 | Arlo | Rhea | Fine by me, you can walk the old spaniel by Wednesday, April 29, 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Arlo's pledge to sweep the pavement outside at the end of Sunday, April 19, 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qbfec8abdd6",
  "kind": "choice",
  "text": "Yo flatmates, Tess shared this chat about the spare room plan, so chip in.\n\nMembers: Tess, Nadia, Wren\nChat export (date | from | to | message):\n2026-05-27 | Nadia | Wren | Count on me to sort the recycling bags by 1 June 2026 if the water tank check is on.\n2026-05-28 | Wren | Nadia | Guaranteed I'll buy the washing powder by 2 June 2026.\n2026-05-30 | Nadia | group | Yay, the water tank check is all set to go!\n2026-06-01 | Wren | Nadia | Sorry, I won't buy the washing powder after all\n2026-06-03 | Nadia | Wren | To note: I have managed to sort the recycling bags",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Nadia's promise to sort the recycling bags at the end of 5 June 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Kept",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "qcbbb094651",
  "kind": "choice",
  "text": "Saved by Kofi, this copy of the support chat concerns the wedding weekend.\n\nMembers: Sami, Lena, Kofi\nChat export (date | from | to | message):\n2026-05-09 | Sami | Lena | Promise to fetch the spare memory cards by 18 May 2026 if the bridal shower goes ahead.\n2026-05-11 | Sami | group | Just so you know, the bridal shower is on as scheduled.\n2026-05-12 | Lena | Sami | Aiming to pick up the album prints by 16 May 2026, we'll see.\n2026-05-13 | Lena | Sami | Lovely, I'll pick up the album prints by 17 May 2026 for sure.\n2026-05-16 | Kofi | Lena | Forget it, you won't need to pick up the album prints\n2026-05-16 | Lena | Sami | Log entry: pick up the album prints, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Lena's commitment to pick up the album prints is in what status at the end of 17 May 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qf23e04203e",
  "kind": "yes/no",
  "text": "Subject: Chat about the grant renewal\nA plain copy from Priya follows, exactly as exported.\n\nMembers: Zara, Kai, Priya\nChat log (oldest first):\n[28 May 2026] Priya: @Zara Lovely, I'll return the library books by 5 Jun 2026 for sure.\n[29 May 2026] Kai: @Priya No need to return the library books, I'm letting you off\n[29 May 2026] Priya: @Zara To my relief, I managed to return the library books.\n[31 May 2026] Priya: @Zara I'll scan the field notes by 6 Jun 2026, providing the thesis defence goes ahead.\n[4 Jun 2026] Priya: Afraid the thesis defence is called off.",
  "question": "Under the rules on the card, is Priya's promise to return the library books broken, waived, not triggered or not yet due, rather than kept, as of 1 Jun 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9f62d31014",
  "kind": "yes/no",
  "text": "Above the messages with the letting agent, a note from Bruno, filed under the guest welcome plan.\n\nMembers: Ines, Lena, Bruno\nChat log (oldest first):\n[23 Apr 2026] Ines: @Bruno Wish me luck, hoping to leave the welcome basket by May 3, 2026.\n[24 Apr 2026] Ines: @Lena Promise to wash the beach towels by May 1, 2026 if the guest arrival evening goes ahead.\n[25 Apr 2026] Ines: @Bruno I'll leave the welcome basket by April 30, 2026, promise.\n[26 Apr 2026] Ines: @Bruno Got myself to leave the welcome basket lol.\n[28 Apr 2026] Lena: @Ines Lovely, I'll wheel the bins out by May 1, 2026 for sure.\n[29 Apr 2026] Ines: @Lena If the pool safety inspection goes ahead, I'll gladly vacuum the holiday cottage by May 4, 2026.",
  "question": "Would you say Ines kept the promise to leave the welcome basket at the end of April 28, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe1b963ec2f",
  "kind": "yes/no",
  "text": "Support thread for a help desk case, covering the rebrand package, saved by Leila.\n\nMembers: Leila, Wren, Kofi\nChat log (oldest first):\n[3 Aug 2026] Kofi: @Leila I will make sure to check the poster proofs by 6 August 2026.\n[4 Aug 2026] Wren: @Kofi Got it, I'll sketch the packaging mockup by 7 August 2026 for sure.\n[7 Aug 2026] Kofi: Hey, any luck with trying to sketch the packaging mockup?\n[7 Aug 2026] Leila: @Wren Provided the brand review call happens, I'll fetch the brand fonts by 12 August 2026.\n[7 Aug 2026] Wren: @Kofi Ticked off my list: sketch the packaging mockup, yay.\n[8 Aug 2026] Wren: Great news, the brand review call is on!",
  "question": "Would you say Wren kept the promise to sketch the packaging mockup at the end of 8 August 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5bdafde974",
  "kind": "choice",
  "text": "Subject: chat export, the caring rota\nHere is the full text.\nWarmly, Ines\n\nMembers: Ines, Tomas, Greta\nChat log (oldest first):\n[11 Aug 2026] Tomas: @Greta I will pick up the repeat prescription by 18 Aug 2026.\n[15 Aug 2026] Tomas: @Greta Count on me to print the care schedule by 20 Aug 2026, if the carer handover happens.\n[18 Aug 2026] Ines: On track for the carer handover to happen as planned.\n[18 Aug 2026] Greta: @Tomas Guaranteed I'll set up the medicine dispenser by 23 Aug 2026.\n[23 Aug 2026] Greta: @Tomas Mate, I promised, may I set up the medicine dispenser by 29 Aug 2026 instead?\n[23 Aug 2026] Tomas: @Greta Yes, you have the green light to set up the medicine dispenser by 29 Aug 2026.\n[27 Aug 2026] Greta: @Tomas Ticked off my list: set up the medicine dispenser, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Greta supposed to set up the medicine dispenser by, going by the chat at the end of 4 Sep 2026 and any agreed changes?",
  "options": [
   "29 Aug 2026",
   "23 Aug 2026",
   "20 Aug 2026"
  ]
 },
 {
  "qid": "q6edd59d781",
  "kind": "yes/no",
  "text": "Flatmates' thread\nExport of the balcony garden project, passed on by Bruno.\n\nMembers: Bruno, Ivo\nChat export (date | from | to | message):\n2026-04-07 | Bruno | Ivo | Count on me, I'll remove the bathroom shelf by 15 Apr 2026.\n2026-04-09 | Bruno | Ivo | I promise to ring the flat repair line by 17 Apr 2026.\n2026-04-12 | Bruno | Ivo | As long as the lease renewal call is on, I'll bring the step stool by 18 Apr 2026.\n2026-04-15 | Bruno | group | Lovely, the lease renewal call is definitely happening!\n2026-04-18 | Bruno | Ivo | Mum, I did ring the flat repair line, haha.",
  "question": "Has Bruno broken the promise to ring the flat repair line at the end of 22 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa197897170",
  "kind": "yes/no",
  "text": "Family group chat with housemates, covering the garden makeover, exported by Oskar.\n\nMembers: Sami, Rhea, Oskar\nChat export (date | from | to | message):\n2026-04-13 | Rhea | Oskar | I will measure the hallway for shelves by 18 April 2026 only if the damp survey inspection happens.\n2026-04-13 | Rhea | group | Really pleased to say the damp survey inspection will go ahead!\n2026-04-18 | Rhea | Oskar | Quick report: I've managed to measure the hallway for shelves\n2026-04-18 | Oskar | Rhea | Ticket's mine, I'll hang the new curtain rail by 23 April 2026.\n2026-04-20 | Oskar | Rhea | Forget what I said, I won't hang the new curtain rail",
  "question": "On 24 April 2026 itself, has Rhea not kept the promise to measure the hallway for shelves?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8bd87adbfc",
  "kind": "yes/no",
  "text": "{\"chat_export\": \"the cottage refresh\", \"saved_by\": \"Mo\", \"scope\": \"group chat\"}\n\nMembers: Mo, Kai, Arlo\nChat log (oldest first):\n[16 Oct 2026] Mo: @Kai Count on me to vacuum the holiday cottage by 19 Oct 2026 if the guest arrival evening is on.\n[16 Oct 2026] Arlo: Really pleased to say the guest arrival evening will go ahead!\n[20 Oct 2026] Arlo: @Mo I promise to fill the cleaning cupboard by 29 Oct 2026.\n[20 Oct 2026] Mo: @Kai It's on me to change the lounge bulb by 24 Oct 2026.\n[21 Oct 2026] Mo: @Kai Log entry: change the lounge bulb, carried out",
  "question": "Applying the card's rules, can it be said that Mo has not kept the promise to change the lounge bulb at the end of 24 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc21a05c06e",
  "kind": "yes/no",
  "text": "Subject: Saved chat on the online store move\nHere is the export from Mo, for the record.\n\nMembers: Mo, Kofi, Omar\nChat log (oldest first):\n[29 Jan 2026] Kofi: @Mo Lovely, I'll send the stock spreadsheet by 6 Feb 2026 for sure.\n[30 Jan 2026] Kofi: @Mo If the product photo day goes ahead, I'll gladly fetch the domain login by 3 Feb 2026.\n[31 Jan 2026] Kofi: @Mo Lovely, I'll update the product photos by 5 Feb 2026 if the stock count is on.\n[2 Feb 2026] Omar: Yep, the stock count is on as planned.\n[2 Feb 2026] Kofi: @Mo Would it be fine if I update the product photos by 9 Feb 2026 instead, yeah?\n[5 Feb 2026] Omar: @Kofi Go ahead and update the product photos by 9 Feb 2026, that is fine.",
  "question": "Is Kofi's promise to update the product photos broken at the end of 5 Feb 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q79bfa6348f",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the spare room plan\nThe thread below comes from Mo and is passed on as it is.\n\nMembers: Arlo, Mo, Ivo, Hana\nChat export (date | from | to | message):\n2026-01-17 | Mo | Arlo | I will sort the recycling bags by 22 Jan 2026 only if the lodger house supper happens.\n2026-01-19 | Arlo | group | Yay, the lodger house supper is all set to go!\n2026-01-19 | Arlo | Hana | I promise to defrost the top freezer by 24 Jan 2026.\n2026-01-22 | Mo | Arlo | Mate, I promised, may I sort the recycling bags by 28 Jan 2026 instead?\n2026-01-22 | Arlo | Mo | Aw no, you need to sort the recycling bags by the original date!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Mo's promise to sort the recycling bags turn out at the end of 22 Jan 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Broken",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q593fa6da45",
  "kind": "choice",
  "text": "Leila shared this support thread, which is about the tenancy renewal talks.\n\nMembers: Leila, Kai\nChat export (date | from | to | message):\n2026-06-23 | Leila | Kai | I'll ring the flat repair line by 28 June 2026, promise.\n2026-06-26 | Leila | Kai | If the flat viewing day goes ahead, I'll drop the bin bags off by 4 July 2026.\n2026-06-28 | Leila | Kai | Is 1 July 2026 alright for me to ring the flat repair line?\n2026-06-28 | Kai | Leila | Yes, you can ring the flat repair line by 1 July 2026 instead.\n2026-06-28 | Kai | group | Yep, the flat viewing day is on as planned.\n2026-07-01 | Leila | Kai | I committed to drop the bin bags off, can I do that by 8 July 2026 instead?",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Leila's promise to drop the bin bags off turn out at the end of 6 July 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "qe57aa7cdc4",
  "kind": "yes/no",
  "text": "Attached chat: the attic conversion idea\nForwarded by: Sami\n\nMembers: Nadia, Lena, Sami\nChat export (date | from | to | message):\n2026-02-26 | Lena | Sami | If the house insurance review is on, I'll definitely feed the house plants by 2026-03-06.\n2026-02-26 | Nadia | Sami | Lovely, I'll drop the parcel upstairs by 2026-03-02 for sure.\n2026-03-01 | Sami | Nadia | No need to drop the parcel upstairs, I'm letting you off\n2026-03-04 | Lena | group | Great news, the house insurance review is on!\n2026-03-05 | Lena | Sami | Guess what, I managed to feed the house plants!",
  "question": "Is Lena's promise to feed the house plants kept as of 2026-03-06, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9920cac171",
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
  "qid": "q56cb649ba3",
  "kind": "choice",
  "text": "Subject: exported chat about the league run\nHere it is for you, from Priya, exactly as saved.\n\nMembers: Greta, Malik, Rhea, Priya\nChat log (oldest first):\n[5 Jan 2026] Priya: @Rhea Ticket's mine, I'll return the bib sets by 2026-01-07.\n[8 Jan 2026] Malik: @Greta Only if the training camp is on, I will print the team sheets by 2026-01-12.\n[9 Jan 2026] Malik: Sorry, the training camp is off.\n[10 Jan 2026] Malik: @Greta I committed to print the team sheets, can I do that by 2026-01-17 instead?\n[12 Jan 2026] Greta: @Malik No change, you need to print the team sheets by the original date.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Malik's promise to print the team sheets at the end of 2026-01-13?",
  "options": [
   "Waived",
   "Not triggered",
   "Not yet due",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "q4bed3b5266",
  "kind": "choice",
  "text": "A written chat between housemates about the reunion weekend. Exported from the device by Dara.\n\nMembers: Greta, Dara, Tomas\nChat log (oldest first):\n[27 Oct 2026] Dara: @Tomas If the family quiz is on, I'll definitely print the family tree chart by 30 October 2026.\n[28 Oct 2026] Greta: @Dara Lovely, I'll buy the name tags by 1 November 2026 for sure.\n[29 Oct 2026] Dara: Scrapping the family quiz, apologies to all.\n[1 Nov 2026] Greta: @Dara I committed to buy the name tags, can I do that by 4 November 2026 instead?\n[1 Nov 2026] Dara: @Greta Works for me, fine for you to buy the name tags by 4 November 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Dara's promise to print the family tree chart stand at the end of 31 October 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Broken",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q69ff2e875c",
  "kind": "yes/no",
  "text": "Ivo shared this so the allotment expansion is easy to find, flatmates.\n\nMembers: Ivo, Ines, Jonas\nChat log (oldest first):\n[4 Jul 2026] Ines: @Jonas You can bank on me to build the compost bay by Monday, 6 July 2026.\n[5 Jul 2026] Ines: @Ivo I promise to weed the carrot row by Thursday, 9 July 2026.\n[6 Jul 2026] Ivo: Where are you up to with plans to weed the carrot row?\n[7 Jul 2026] Jonas: @Ivo Lovely, I'll sow the broad beans by Saturday, 11 July 2026 if the harvest supper is on.\n[8 Jul 2026] Ines: @Jonas Provided the allotment site visit happens, I will sharpen the hand hoe by Wednesday, 15 July 2026.\n[9 Jul 2026] Ines: @Ivo For the record: I was able to weed the carrot row",
  "question": "Going by the card's rules, does Ines not keep the promise to weed the carrot row at the end of Friday, 10 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa0baede3e5",
  "kind": "choice",
  "text": "Case note: chat about the campaign edit\nExported by: Leila\n\nMembers: Leila, Zara, Hana, Lee\nChat export (date | from | to | message):\n2026-02-21 | Leila | Zara | Maybe I can order the stock music licence by 6 Mar 2026.\n2026-02-22 | Leila | Zara | I'll order the stock music licence by 2 Mar 2026, providing the client screening goes ahead.\n2026-02-23 | Lee | Hana | I will make sure to record the voice over by 3 Mar 2026.\n2026-02-23 | Lee | Hana | Scratch what I said, I won't record the voice over.\n2026-02-24 | Hana | group | Team, the client screening stays on as booked.\n2026-03-02 | Leila | Zara | For the record: I was able to order the stock music licence",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 28 Feb 2026, what status has Leila's promise to order the stock music licence got?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q4a16bd1eb5",
  "kind": "yes/no",
  "text": "Support: help desk chat\nSubject: the training plan\nSaved by: Kofi\n\nMembers: Femi, Kofi, Yuki\nChat log (oldest first):\n[27 Apr 2026] Femi: @Yuki Count on me to return the loaned helmets by 5 May 2026.\n[1 May 2026] Femi: @Yuki I will fetch the bike stand by 8 May 2026 only if the hill climb happens.\n[4 May 2026] Kofi: @Femi Good news, you're let off having to return the loaned helmets\n[7 May 2026] Yuki: Sad to report that the hill climb is off.\n[10 May 2026] Femi: @Yuki Mum, I did return the loaned helmets, haha.",
  "question": "According to the rules on the card, does the promise Femi made to return the loaned helmets have any status except broken at the end of 9 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc8532c99e2",
  "kind": "choice",
  "text": "Read up on the loft conversion, flatmates, as Nadia exported it.\n\nMembers: Dara, Malik, Nadia\nChat export (date | from | to | message):\n2026-03-11 | Malik | Nadia | Only if the kitchen fitting day is on, I will pick up the grout bag by Tuesday, March 17, 2026.\n2026-03-15 | Nadia | Dara | Relax, I'll pay the plumbing invoice by Sunday, March 22, 2026 for sure.\n2026-03-15 | Malik | Nadia | Good news, you're let off having to pay the plumbing invoice\n2026-03-16 | Malik | Nadia | I'll sweep the dust from stairs by Wednesday, March 25, 2026 as long as the boiler install visit is on.\n2026-03-22 | Nadia | Dara | To my relief, I managed to pay the plumbing invoice.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Nadia made to pay the plumbing invoice, what state is it in at the end of Wednesday, March 25, 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Waived",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "qafc02df4af",
  "kind": "yes/no",
  "text": "Subject: Chat about the showreel refresh\nBelow is a copy that came from Leila, pasted as found.\n\nMembers: Leila, Omar, Wren, Bruno\nChat export (date | from | to | message):\n2026-05-21 | Omar | Bruno | I'll send the timeline export by 26 May 2026, providing the client screening goes ahead.\n2026-05-23 | Leila | Bruno | I assure you I'll back up the project drives by 27 May 2026 if the shoot day is on.\n2026-05-24 | Omar | group | Sorry all, the shoot day is not happening.\n2026-05-25 | Wren | Omar | I own this, I'll upload the render files by 31 May 2026.\n2026-05-27 | Bruno | Wren | Quick update: you do not need to upload the render files at all.\n2026-05-31 | Wren | Omar | Got myself to upload the render files lol.",
  "question": "Is the promise to upload the render files that Wren made broken at the end of 31 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb00792efe5",
  "kind": "choice",
  "text": "Shared by Femi, an export of a household chat about the allotment expansion, as saved.\n\nMembers: Kai, Sami, Femi, Jonas\nChat log (oldest first):\n[13 Feb 2026] Jonas: @Kai Relax, I'll deliver the surplus runner beans by 20 Feb 2026, promise.\n[14 Feb 2026] Kai: @Sami Provided the allotment site visit happens, I'll stake the tomato canes by 18 Feb 2026.\n[15 Feb 2026] Femi: Just so you know, the allotment site visit is on as scheduled.\n[16 Feb 2026] Kai: @Jonas Count on me to collect the seed potatoes by 25 Feb 2026.\n[17 Feb 2026] Jonas: @Kai Nobody needs you to stake the tomato canes, that's that\n[20 Feb 2026] Jonas: @Kai Correction, I will not be able to deliver the surplus runner beans.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Kai's promise to stake the tomato canes at the end of 19 Feb 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "qdca6c534fa",
  "kind": "choice",
  "text": "{\"thread\": \"the trade show push\", \"exported_by\": \"Greta\", \"shape\": \"group chat\"}\n\nMembers: Yuki, Greta, Lee\nChat export (date | from | to | message):\n2026-04-21 | Yuki | Greta | As long as the trade fair stand is on, I will print the event banners by 26 Apr 2026.\n2026-04-21 | Lee | Yuki | I will fetch the campaign budget sheet by 27 Apr 2026.\n2026-04-21 | Lee | Yuki | To note: I have managed to fetch the campaign budget sheet\n2026-04-22 | Lee | Greta | I will set up the analytics dashboard by 1 May 2026.\n2026-04-25 | Yuki | group | Sorry, the trade fair stand is off.\n2026-04-30 | Greta | Lee | Don't sweat it, there's no need to set up the analytics dashboard",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of 28 Apr 2026, which status does Yuki have for the promise to print the event banners?",
  "options": [
   "Broken",
   "Kept",
   "Waived",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "qbd5636917a",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the allotment expansion\nThis export from Malik is pasted in full for readers who want it.\n\nMembers: Greta, Leila, Malik\nChat export (date | from | to | message):\n2026-09-11 | Greta | Malik | Count on me, I'll dig the potato patch by 14 September 2026.\n2026-09-13 | Malik | Greta | Count on me to weed the carrot row by 18 September 2026, if the water tank delivery happens.\n2026-09-14 | Leila | group | Great news, the water tank delivery is on!\n2026-09-16 | Leila | Greta | Relax, I'll sow the broad beans by 22 September 2026, promise.\n2026-09-19 | Leila | Greta | Ticked off: sow the broad beans, feels so good",
  "question": "At the end of 20 September 2026, has the promise Leila made to sow the broad beans been broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q035eeea4b0",
  "kind": "yes/no",
  "text": "Work team channel\nSaved by Tomas, which talks about the staff handbook.\n\nMembers: Oskar, Tomas, Tess\nChat log (oldest first):\n[19 Jul 2026] Tomas: @Oskar Guaranteed I'll send the expense receipts by 21 Jul 2026.\n[19 Jul 2026] Tomas: @Oskar Mum, I did send the expense receipts, haha.\n[20 Jul 2026] Oskar: @Tomas Count on me, I'll replace the kitchen filters by 28 Jul 2026.\n[24 Jul 2026] Tomas: @Oskar I promise to print the staff rota by 27 Jul 2026 if the coffee morning is on.\n[24 Jul 2026] Tomas: Sorry, the coffee morning is off.\n[26 Jul 2026] Tess: @Oskar I'll book the boardroom by 1 Aug 2026 as long as the lease viewing is on.",
  "question": "Under the rules on the card, is it true that Tomas has not kept the promise to print the staff rota as of 27 Jul 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qab9e1ea8a8",
  "kind": "yes/no",
  "text": "Subject: export of the group chat on the spring campaign\nHere is the chat as saved by Dara, pasted below.\n\nMembers: Femi, Dara, Lee, Zara\nChat export (date | from | to | message):\n2026-06-27 | Zara | Dara | I own this, I'll pay the printing invoice by 1 Jul 2026.\n2026-06-27 | Dara | group | Thanks lovely, got it!\n2026-06-29 | Femi | Lee | Ticket's mine, I'll set up the analytics dashboard by 3 Jul 2026.\n2026-06-29 | Femi | Lee | As long as the annual review is on, I'll fix the landing page headline by 2 Jul 2026.\n2026-06-30 | Dara | group | Yep, the annual review is on as planned.\n2026-07-01 | Zara | Dara | To note: I have managed to pay the printing invoice",
  "question": "Would you say Zara didn't keep the promise to pay the printing invoice by the end of 6 Jul 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q26c43e7641",
  "kind": "yes/no",
  "text": "Subject: chat about the sponsor search, forwarded\nThe chat follows below.\nRegards, Bruno\n\nMembers: Tess, Bruno, Ravi\nChat log (oldest first):\n[16 Jan 2026] Bruno: @Ravi Relax, I'll pump the spare tyres by 18 Jan 2026 for sure.\n[16 Jan 2026] Ravi: @Tess I own this, I'll fetch the bike stand by 22 Jan 2026.\n[21 Jan 2026] Ravi: @Tess Lovely, I'll service the tandem bike by 28 Jan 2026 if the group ride is on.\n[22 Jan 2026] Bruno: Fab, we are on for the group ride as planned!\n[22 Jan 2026] Ravi: @Tess Ticked off: fetch the bike stand, feels so good",
  "question": "At the end of 28 Jan 2026, is Ravi's promise to fetch the bike stand broken, waived, not triggered or not yet due, rather than kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb034cd606d",
  "kind": "choice",
  "text": "Support case copy, filed for the lab move\nSaved on record by Femi\n\nMembers: Mo, Elif, Hana, Femi\nChat log (oldest first):\n[27 Jul 2026] Mo: @Hana I promise to return the library books by 3 Aug 2026.\n[28 Jul 2026] Hana: @Mo I'll try to print the poster abstracts by 2 Aug 2026, no guarantee.\n[29 Jul 2026] Mo: @Elif I will book the microscope slot by 3 Aug 2026.\n[29 Jul 2026] Hana: @Femi Only if the grant panel is on, I will print the poster abstracts by 6 Aug 2026.\n[4 Aug 2026] Mo: Really pleased to say the grant panel will go ahead!\n[6 Aug 2026] Femi: @Hana Nobody needs you to print the poster abstracts, that's that",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Hana's commitment to print the poster abstracts at the end of 7 Aug 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Broken",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "q3a790cd1f5",
  "kind": "yes/no",
  "text": "Volunteers, here is the league run thread that Kofi forwarded for us.\n\nMembers: Kofi, Mo, Tomas, Zara\nChat log (oldest first):\n[21 May 2026] Zara: @Tomas I'll collect the referee whistles by 29 May 2026, provided the youth trial happens.\n[21 May 2026] Zara: @Mo If the training camp goes ahead, I'll gladly mark the pitch lines by 26 May 2026.\n[23 May 2026] Zara: @Tomas I will book the changing room by 31 May 2026.\n[25 May 2026] Zara: @Tomas Scratch that, I'm not going to book the changing room\n[28 May 2026] Mo: Just so you know, the youth trial is on as scheduled.\n[29 May 2026] Zara: @Tomas To my relief, I managed to collect the referee whistles.",
  "question": "Was Zara's promise to collect the referee whistles not kept as of 2 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9e7f386643",
  "kind": "choice",
  "text": "Saved by Nadia, this copy of the support chat concerns the family photo book.\n\nMembers: Ivo, Malik, Nadia\nChat log (oldest first):\n[25 Aug 2026] Malik: @Ivo No promises, but I'll aim to pick up the school bags by 4 Sep 2026.\n[27 Aug 2026] Malik: @Ivo Provided the seaside outing happens, I will pick up the school bags by 3 Sep 2026.\n[27 Aug 2026] Ivo: Just so you know, the seaside outing is on as scheduled.\n[1 Sep 2026] Nadia: @Ivo Guaranteed I'll fetch the craft box by 10 Sep 2026.\n[9 Sep 2026] Nadia: @Ivo Mate, I promised, may I fetch the craft box by 14 Sep 2026 instead?\n[9 Sep 2026] Ivo: @Nadia Revised deadline is 14 Sep 2026, so you can fetch the craft box.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Malik's commitment to pick up the school bags have at the end of 29 Aug 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Broken",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qff2bbf1a80",
  "kind": "choice",
  "text": "Shared by Omar for the committee, this is the group chat on the ground upgrade.\n\nMembers: Lee, Nadia, Lena, Omar\nChat log (oldest first):\n[1 May 2026] Lena: @Lee I promise to collect the referee whistles by 8 May 2026.\n[2 May 2026] Lena: @Lee Quick question, could I collect the referee whistles by 13 May 2026 instead?\n[2 May 2026] Omar: @Lena Yes, fine to collect the referee whistles by 13 May 2026 instead.\n[11 May 2026] Lee: @Nadia If the training camp goes ahead, I'll mark the pitch lines by 17 May 2026.\n[11 May 2026] Omar: @Lena Lovely, I'll book the changing room by 17 May 2026 for sure.\n[13 May 2026] Lee: Sadly, the training camp is not going ahead.\n[17 May 2026] Omar: @Lena Update on my side: I will not book the changing room, sorry.\n[18 May 2026] Lena: @Lee Guess who managed to collect the referee whistles, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Lena due to collect the referee whistles at the end of 12 May 2026, after any agreed rescheduling?",
  "options": [
   "17 May 2026",
   "8 May 2026",
   "13 May 2026"
  ]
 },
 {
  "qid": "q4d1fb81f00",
  "kind": "choice",
  "text": "Tenant and agent back-and-forth on the autumn term budget, forwarded by Ravi.\n\nMembers: Tomas, Jonas, Ravi, Lena\nChat log (oldest first):\n[18 Oct 2026] Tomas: @Lena I assure you I'll return the bin rota by 26 Oct 2026 if the freshers welcome night is on.\n[19 Oct 2026] Jonas: Update, the freshers welcome night will not take place.\n[21 Oct 2026] Tomas: @Jonas Relax, I'll store the spare bike by 23 Oct 2026 for sure.\n[22 Oct 2026] Tomas: @Jonas Scratch that, I'm not going to store the spare bike\n[24 Oct 2026] Tomas: @Lena Any chance I can return the bin rota by 31 Oct 2026 instead?\n[26 Oct 2026] Jonas: @Tomas Yes, all good for you to return the bin rota by 31 Oct 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Tomas made to return the bin rota have at the end of 22 Oct 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "qba6715094d",
  "kind": "choice",
  "text": "Case note: chat about the guest travel plans\nExported by: Femi\n\nMembers: Femi, Leila\nChat log (oldest first):\n[9 Mar 2026] Femi: @Leila I'll be sure to buy the name tags by Wednesday, 18 March 2026.\n[13 Mar 2026] Leila: @Femi I will pay the catering company by Thursday, 19 March 2026.\n[14 Mar 2026] Femi: @Leila Lovely, I'll order the cousin t-shirts by Tuesday, 17 March 2026 if the garden picnic is on.\n[15 Mar 2026] Leila: Sorry all, the garden picnic is called off.\n[16 Mar 2026] Leila: @Femi To note: I have managed to pay the catering company",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Leila's promise to pay the catering company at the end of Monday, 16 March 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Not yet due",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q12f6b744c0",
  "kind": "yes/no",
  "text": "We have been planning the speed bump plan here, shared by Ivo.\n\nMembers: Bruno, Ivo, Ines\nChat log (oldest first):\n[17 Oct 2026] Bruno: @Ines It's on me to sweep the pavement outside by 24 Oct 2026.\n[17 Oct 2026] Bruno: @Ines Ticket's mine, I'll return the ladders by 23 Oct 2026.\n[17 Oct 2026] Ines: Oh cheers, that helps.\n[18 Oct 2026] Ivo: @Bruno Only if the hedge trimming day is on, I will bring the bins in by 27 Oct 2026.\n[19 Oct 2026] Bruno: @Ivo I promise to share the garden hose by 26 Oct 2026 if the bonfire night is on.\n[23 Oct 2026] Bruno: @Ines Mum, I did return the ladders, haha.",
  "question": "Applying the card's rules, can it be said that Bruno has not kept the promise to return the ladders at the end of 24 Oct 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q85a9458519",
  "kind": "yes/no",
  "text": "Flat chat, exported by Elif for the household.\nSubject: the rent split plan\n\nMembers: Elif, Oskar, Zara, Kofi\nChat log (oldest first):\n[28 Apr 2026] Kofi: @Elif If the move in day is on, I'll definitely photograph the bathroom mould by 30 Apr 2026.\n[30 Apr 2026] Elif: @Kofi I own this, I'll forward the inventory photos by 5 May 2026.\n[2 May 2026] Kofi: @Elif I own this, I'll scan the council tax letter by 11 May 2026.\n[2 May 2026] Zara: @Elif Nobody needs you to forward the inventory photos, that's that\n[3 May 2026] Kofi: @Zara I assure you I'll ring the letting agent by 6 May 2026 if the house hunting viewing is on.\n[5 May 2026] Kofi: Yep, the house hunting viewing is on as planned.",
  "question": "Is it true under the card's rules that Elif has kept the promise to forward the inventory photos at the end of 7 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8be03c2dcb",
  "kind": "choice",
  "text": "{\"chat\": \"exported\", \"about\": \"the lab move\", \"saved_by\": \"Dara\", \"medium\": \"text\"}\n\nMembers: Sami, Mo, Dara, Jonas\nChat log (oldest first):\n[14 Apr 2026] Jonas: @Sami Count on me, I'll clean the glassware set by Friday, 24 April 2026.\n[16 Apr 2026] Sami: @Dara I'll print the poster abstracts by Thursday, 23 April 2026 if the safety inspection goes ahead.\n[18 Apr 2026] Mo: @Jonas Forget it, you won't need to clean the glassware set\n[21 Apr 2026] Mo: @Jonas Got it, I'll send the ethics form by Monday, 27 April 2026 for sure.\n[22 Apr 2026] Jonas: Sorry all, the safety inspection is called off.\n[25 Apr 2026] Mo: @Jonas I need to take back my commitment to send the ethics form.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Sami's promise to print the poster abstracts at the end of Monday, 27 April 2026?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q3f8c2a1405",
  "kind": "choice",
  "text": "{\"saved_copy\": \"the spring campaign\", \"keeper\": \"Tomas\", \"medium\": \"chat transcript\"}\n\nMembers: Tomas, Arlo, Yuki, Lee\nChat export (date | from | to | message):\n2026-04-15 | Arlo | Yuki | Provided the annual review happens, I will fetch the campaign budget sheet by 18 Apr 2026.\n2026-04-16 | Lee | Yuki | I promise to draft the press release by 19 Apr 2026.\n2026-04-17 | Tomas | group | We are dropping the annual review from the list.\n2026-04-17 | Lee | Arlo | I will collect the survey answers by 22 Apr 2026.\n2026-04-18 | Lee | Arlo | Think 26 Apr 2026 would work if I collect the survey answers instead?\n2026-04-19 | Arlo | Lee | Aw no, you need to collect the survey answers by the original date!\n\nExport tool: this copy, shared by Tomas, may be out of date, so later edits might not appear here.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Arlo's promise to fetch the campaign budget sheet have at the end of 22 Apr 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Not triggered",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "qa8a5e0cfe2",
  "kind": "choice",
  "text": "{\"record_type\": \"saved chat\", \"matter\": \"the playground project\", \"by\": \"Oskar\", \"stored\": \"as text\"}\n\nMembers: Priya, Ines, Oskar\nChat export (date | from | to | message):\n2026-05-19 | Priya | Ines | I'll be sure to send the newsletter drafts by 2026-05-21.\n2026-05-20 | Ines | Priya | Quick update: you do not need to send the newsletter drafts at all.\n2026-05-20 | Oskar | Priya | Count on me to collect the bake sale tins by 2026-05-24 if the clothes swap is on.\n2026-05-23 | Priya | group | Sad to report that the clothes swap is off.\n2026-05-23 | Oskar | Priya | Mind giving me until 2026-05-29 to collect the bake sale tins?\n2026-05-23 | Priya | Oskar | Works for me, fine for you to collect the bake sale tins by 2026-05-29.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Oskar made to collect the bake sale tins at the end of 2026-05-23?",
  "options": [
   "Broken",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Waived"
  ]
 }
]
