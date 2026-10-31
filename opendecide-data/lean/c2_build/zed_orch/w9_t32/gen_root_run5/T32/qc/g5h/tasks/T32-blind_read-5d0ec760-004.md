# G5-H blind read T32-blind_read-5d0ec760-004 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root/T32/qc/g5h/answers/T32-blind_read-5d0ec760-004.json

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
  "qid": "q998840c010",
  "kind": "choice",
  "text": "Subject: Saved thread about the house rules debate\nThis export came from Wren and is pasted in full below.\n\nMembers: Wren, Zara\nChat log (oldest first):\n[21 Jun 2026] Wren: @Zara Lovely, I'll oil the back door hinges by 26 Jun 2026 if the house viewing is on.\n[21 Jun 2026] Wren: @Zara Promise to bleed the attic radiators by 24 Jun 2026 if the heritage fete goes ahead.\n[21 Jun 2026] Zara: Team, the heritage fete stays on as booked.\n[23 Jun 2026] Wren: @Zara Count on me, I'll scrub the cellar steps by 2 Jul 2026.\n[24 Jun 2026] Wren: @Zara You can bank on me to mend the garden gate by 1 Jul 2026.\n[1 Jul 2026] Wren: @Zara Mum, I did scrub the cellar steps, haha.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Wren made to bleed the attic radiators have at the end of 23 Jun 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q7fed8b99e4",
  "kind": "choice",
  "text": "Copied into a record by Ivo: tenants writing to a letting agent about the balcony garden project.\n\nMembers: Sami, Ivo\nChat log (oldest first):\n[4 Feb 2026] Sami: @Ivo Count on me, I'll collect the spare flat keys by 8 February 2026.\n[5 Feb 2026] Sami: @Ivo Change of plans: I will not collect the spare flat keys\n[7 Feb 2026] Ivo: @Sami Lovely, I'll measure the kitchen for fridge by 10 February 2026 if the flat viewing day is on.\n[9 Feb 2026] Sami: Team, the flat viewing day is not happening.\n[9 Feb 2026] Ivo: @Sami I promise to wipe the cooker hood by 14 February 2026 if the window cleaner visit is on.\n[10 Feb 2026] Sami: @Ivo I promise to email the leak photos by 14 February 2026.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Ivo made to measure the kitchen for fridge, what state is it in at the end of 11 February 2026?",
  "options": [
   "Kept",
   "Broken",
   "Waived",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q4bdc1117a3",
  "kind": "yes/no",
  "text": "Saved chat on the reunion planning. Exported by Wren, unedited, from a household group.\n\nMembers: Wren, Malik, Kai\nChat log (oldest first):\n[13 May 2026] Malik: @Kai I'll reserve the reunion hall by 18 May 2026 if the grandparents visit goes ahead.\n[14 May 2026] Wren: No promises, but I'll aim to send the group invitations by 27 May 2026.\n[15 May 2026] Wren: @Malik Absolutely, I will send the group invitations by 23 May 2026.\n[17 May 2026] Kai: @Malik Provided the family quiz happens, I will pay the catering company by 26 May 2026.\n[18 May 2026] Wren: @Malik I need to take back my commitment to send the group invitations.\n[23 May 2026] Malik: @Wren No worries, you don't need to send the group invitations",
  "question": "Would you say Wren kept the promise to send the group invitations at the end of 23 May 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa639c60307",
  "kind": "yes/no",
  "text": "Local volunteer export\nSaved by Ines, covering the topic of the league run.\n\nMembers: Ana, Ines\nChat log (oldest first):\n[22 May 2026] Ines: I'll try to book the changing room by 30 May 2026, no promises.\n[23 May 2026] Ines: @Ana Provided the pre-season friendly happens, I'll book the changing room by 27 May 2026.\n[24 May 2026] Ana: Yay, the pre-season friendly is all set to go!\n[25 May 2026] Ines: @Ana Relax, I'll set up the corner flags by 28 May 2026 for sure.\n[25 May 2026] Ines: @Ana I'm withdrawing my promise to set up the corner flags\n[27 May 2026] Ines: @Ana Log entry: book the changing room, carried out",
  "question": "As the rules on the card set out, is it the case that Ines has broken the promise to book the changing room at the end of 31 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9d8d2c8a8f",
  "kind": "choice",
  "text": "{\"record\": \"shared group chat\", \"subject\": \"the peer review\", \"shared_by\": \"Tess\", \"stored\": \"as text\"}\n\nMembers: Bruno, Leila, Omar, Tess\nChat log (oldest first):\n[16 Aug 2026] Leila: @Bruno I will book the microscope slot by 18 August 2026 only if the seminar series happens.\n[16 Aug 2026] Bruno: Sadly, the seminar series won't go ahead.\n[19 Aug 2026] Omar: @Bruno I promise to submit the ethics application by 27 August 2026.\n[19 Aug 2026] Leila: @Omar Nobody needs you to submit the ethics application, that's that\n[22 Aug 2026] Tess: @Leila I'll return the library books by 24 August 2026, providing the grant panel goes ahead.\n[28 Aug 2026] Omar: @Bruno To my relief, I managed to submit the ethics application.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Omar's pledge to submit the ethics application sit at the end of 29 August 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Not yet due",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "qfbcdef54f5",
  "kind": "yes/no",
  "text": "Neighbour and flatmate talk, copied out by Nadia: the old house restoration.\n\nMembers: Hana, Nadia, Sami\nChat log (oldest first):\n[19 Mar 2026] Nadia: @Hana Provided the roof survey visit happens, I'll defrost the old fridge by 23 March 2026.\n[22 Mar 2026] Sami: Quick heads up, the roof survey visit is scrapped.\n[23 Mar 2026] Hana: @Nadia Lovely, I'll tidy the boot room by 30 March 2026 for sure.\n[24 Mar 2026] Sami: @Hana You are released, no requirement to tidy the boot room.\n[24 Mar 2026] Hana: @Nadia Ticked off my list: tidy the boot room, yay.",
  "question": "Does the card's rule set confirm that Hana has kept the promise to tidy the boot room on 28 March 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q782b7ed3ab",
  "kind": "choice",
  "text": "Kai forwarded this support chat, which is about the documentary cut.\n\nMembers: Arlo, Ines, Kai\nChat export (date | from | to | message):\n2026-09-16 | Kai | Ines | Lovely, I'll upload the render files by 21 Sep 2026 if the festival premiere is on.\n2026-09-17 | Arlo | Ines | Absolutely, I will label the clip folders by 22 Sep 2026.\n2026-09-17 | Arlo | Ines | Can I label the clip folders by 28 Sep 2026 instead? I did promise, sorry.\n2026-09-20 | Ines | Arlo | Fine by me, you can label the clip folders by 28 Sep 2026.\n2026-09-20 | Ines | group | Just so you know, the festival premiere is on as scheduled.\n2026-09-21 | Kai | Arlo | Relax, mate, you're not expected to label the clip folders",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Arlo's commitment to label the clip folders have at the end of 26 Sep 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q026f2cf82c",
  "kind": "yes/no",
  "text": "{\"export_type\": \"group chat export\", \"chat_topic\": \"the campaign edit\", \"saved_by\": \"Ivo\"}\n\nMembers: Arlo, Femi, Priya, Ivo\nChat export (date | from | to | message):\n2026-03-21 | Arlo | Ivo | If the festival premiere is on, I'll definitely export the subtitle files by Monday, 30 March 2026.\n2026-03-22 | Arlo | Femi | Count on me to ship the hard drive by Saturday, 28 March 2026.\n2026-03-27 | Femi | group | Update: the festival premiere is going ahead as planned.\n2026-03-28 | Arlo | Femi | Would it be fine if I ship the hard drive by Wednesday, 1 April 2026 instead, yeah?\n2026-03-28 | Femi | Arlo | Nah, the date's staying put, so you can ship the hard drive.\n2026-03-28 | Arlo | Femi | Update on my side: I will not ship the hard drive, sorry.",
  "question": "Is Arlo's promise to ship the hard drive kept on Saturday, 28 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6416fcdbf6",
  "kind": "choice",
  "text": "Volunteers, here is the new term plans thread that Bruno forwarded for us.\n\nMembers: Yuki, Wren, Leila, Bruno\nChat export (date | from | to | message):\n2026-05-20 | Leila | Bruno | I assure you I'll set up the book stall by 25 May 2026 if the quiz night is on.\n2026-05-21 | Wren | Bruno | I will make sure to wrap the prize hampers by 29 May 2026.\n2026-05-22 | Leila | Wren | Absolutely, I will print the raffle tickets by 30 May 2026.\n2026-05-24 | Bruno | group | Sadly, the quiz night won't go ahead.\n2026-05-24 | Wren | Bruno | Guess who managed to wrap the prize hampers, go team!\n2026-05-28 | Leila | Wren | I need to take back my commitment to print the raffle tickets.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of 26 May 2026, which status does Wren have for the promise to wrap the prize hampers?",
  "options": [
   "Not triggered",
   "Broken",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qe84c0604ed",
  "kind": "yes/no",
  "text": "Neighbour and flatmate talk, copied out by Jonas: the speed bump plan.\n\nMembers: Jonas, Omar, Ana\nChat log (oldest first):\n[8 Jul 2026] Ana: @Jonas Count on me to feed the cat across the road by Friday, July 17, 2026 if the street litter clean is on.\n[10 Jul 2026] Omar: @Ana I assure you I'll take in the post by Sunday, July 19, 2026 if the bonfire night is on.\n[11 Jul 2026] Jonas: @Ana It's on me to lend the stepladder by Saturday, July 18, 2026.\n[12 Jul 2026] Omar: @Jonas Ah, no stress, no need for you to lend the stepladder\n[15 Jul 2026] Ana: On track for the bonfire night to happen as planned.\n[21 Jul 2026] Jonas: @Ana Ticked off: lend the stepladder, feels so good",
  "question": "Applying the rules on the card, did Jonas break the promise to lend the stepladder at the end of Tuesday, July 21, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8168572d31",
  "kind": "yes/no",
  "text": "Elif shared this exchange with the client about the documentary cut.\n\nMembers: Greta, Elif, Oskar, Tess\nChat export (date | from | to | message):\n2026-09-08 | Elif | Greta | I'll send the colour notes by Sunday, September 13, 2026 as long as the shoot day is on.\n2026-09-10 | Tess | Oskar | Count on me to order the stock music licence by Friday, September 18, 2026.\n2026-09-11 | Oskar | Greta | Promise to record the voice over by Sunday, September 20, 2026 if the client screening goes ahead.\n2026-09-12 | Tess | Oskar | I will fetch the raw footage by Saturday, September 19, 2026.\n2026-09-14 | Oskar | Tess | Nobody needs you to fetch the raw footage, that's that\n2026-09-17 | Tess | group | Team, the client screening is not happening.",
  "question": "Using the rules on the card, is it true that Tess has not broken the promise to fetch the raw footage at the end of Saturday, September 19, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf48aa6e3f0",
  "kind": "yes/no",
  "text": "Shared by Rhea, this work thread covers the platform rewrite.\n\nMembers: Rhea, Kofi\nChat log (oldest first):\n[13 Jul 2026] Kofi: @Rhea Provided the sprint demo happens, I will update the dependency list by Thursday, July 16, 2026.\n[14 Jul 2026] Rhea: @Kofi I'll restart the build server by Thursday, July 23, 2026 as long as the planning session is on.\n[14 Jul 2026] Kofi: @Rhea Got it, I'll fix the test runner by Friday, July 17, 2026 for sure.\n[15 Jul 2026] Rhea: @Kofi Committing to run the security scan by Sunday, July 19, 2026.\n[15 Jul 2026] Kofi: Please note the sprint demo will proceed.\n[16 Jul 2026] Rhea: @Kofi Guess what, I managed to run the security scan!",
  "question": "Is Rhea's promise to run the security scan kept as of Tuesday, July 21, 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf2a6863ecd",
  "kind": "choice",
  "text": "Our flat chat about the summer lets season, saved by Mo for whoever lives here.\n\nMembers: Leila, Mo, Greta, Yuki\nChat log (oldest first):\n[22 Mar 2026] Yuki: @Mo Committing to wheel the bins out by 28 March 2026.\n[24 Mar 2026] Yuki: @Mo Mind giving me until 2 April 2026 to wheel the bins out?\n[28 Mar 2026] Greta: @Yuki Yes, you're welcome to wheel the bins out by 2 April 2026 instead.\n[28 Mar 2026] Leila: @Yuki If the owner handover visit is on, I'll definitely scrub the hot tub by 5 April 2026.\n[29 Mar 2026] Yuki: @Mo Quick report: I've managed to wheel the bins out\n[29 Mar 2026] Leila: @Greta I will wash the beach towels by 4 April 2026.\n[31 Mar 2026] Leila: @Greta I'll restock the guest toiletries by 3 April 2026, providing the summer season launch goes ahead.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of 31 March 2026, what is the date by which Yuki has to wheel the bins out, counting any agreed change?",
  "options": [
   "2 April 2026",
   "5 April 2026",
   "28 March 2026"
  ]
 },
 {
  "qid": "q67cbd6180c",
  "kind": "yes/no",
  "text": "The family thread was saved by Kofi, and its subject is the street watch scheme.\n\nMembers: Hana, Kofi, Dara\nChat log (oldest first):\n[23 Apr 2026] Dara: @Hana I own this, I'll feed the cat across the road by 2 May 2026.\n[26 Apr 2026] Dara: @Hana You can bet I'll return the ladders by 3 May 2026.\n[27 Apr 2026] Dara: @Kofi Count on me to take in the post by 30 Apr 2026, if the road works meeting happens.\n[27 Apr 2026] Dara: Really pleased to say the road works meeting will go ahead!\n[28 Apr 2026] Dara: @Kofi Scratch what I said, I won't take in the post.",
  "question": "Did Dara keep the promise to take in the post as of 28 Apr 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q70b93a077c",
  "kind": "choice",
  "text": "Flat chat, exported by Ana for the household.\nSubject: the vegetable plot plan\n\nMembers: Priya, Ana, Ravi\nChat log (oldest first):\n[9 Oct 2026] Priya: @Ravi Absolutely, I will sharpen the hand hoe by 12 October 2026.\n[9 Oct 2026] Priya: @Ana Might manage to deliver the surplus runner beans by 12 October 2026, who knows.\n[11 Oct 2026] Priya: @Ravi Lovely, I'll deliver the surplus runner beans by 14 October 2026 if the allotment site visit is on.\n[11 Oct 2026] Ravi: Update: the allotment site visit is going ahead as planned.\n[12 Oct 2026] Ana: @Priya Relax, mate, you're not expected to sharpen the hand hoe\n[14 Oct 2026] Priya: @Ravi Guess what, I managed to deliver the surplus runner beans!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Priya doing with the promise to deliver the surplus runner beans at the end of 14 October 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q24dcd2f6fd",
  "kind": "choice",
  "text": "Club and committee chat, saved by Arlo, with the choir tour in the middle.\n\nMembers: Hana, Arlo, Dara\nChat log (oldest first):\n[26 Jan 2026] Dara: @Arlo I'll try to fetch the choir robes by 2026-01-29, no guarantee.\n[28 Jan 2026] Dara: @Arlo I'll fetch the choir robes by 2026-02-01 as long as the voice test is on.\n[28 Jan 2026] Hana: Yay, the voice test is all set to go!\n[29 Jan 2026] Hana: @Dara Nobody needs you to fetch the choir robes, that's that\n[1 Feb 2026] Dara: @Hana I'll be sure to fix the stand microphones by 2026-02-10.\n[8 Feb 2026] Dara: @Hana Scratch that, I'm not going to fix the stand microphones",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Dara made to fetch the choir robes is in which status at the end of 2026-02-01?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q656650b219",
  "kind": "choice",
  "text": "{\"chat\": \"exported\", \"about\": \"the choir tour\", \"saved_by\": \"Wren\", \"medium\": \"text\"}\n\nMembers: Omar, Priya, Wren\nChat log (oldest first):\n[14 May 2026] Omar: @Wren Count on me, I'll collect the sheet music by 22 May 2026.\n[17 May 2026] Priya: @Omar Don't sweat it, there's no need to collect the sheet music\n[19 May 2026] Priya: @Omar If the summer recital goes ahead, I'll gladly fetch the choir robes by 27 May 2026.\n[21 May 2026] Omar: Fab, we are on for the summer recital as planned!\n[22 May 2026] Omar: @Wren To my relief, I managed to collect the sheet music.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Omar's promise to collect the sheet music turn out at the end of 23 May 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Not triggered",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q008a76ff7c",
  "kind": "yes/no",
  "text": "Sami saved this so we stay on the same page about the cellar project, mates.\n\nMembers: Ana, Tess, Sami, Leila\nChat log (oldest first):\n[25 Jul 2026] Sami: @Leila Lovely, I'll wash the sash windows by Monday, July 27, 2026 for sure.\n[25 Jul 2026] Leila: @Sami Quick update: you do not need to wash the sash windows at all.\n[27 Jul 2026] Tess: @Sami Committing to oil the back door hinges by Thursday, July 30, 2026.\n[30 Jul 2026] Sami: @Ana As long as the loft clearance day is on, I'll defrost the old fridge by Friday, August 7, 2026.\n[2 Aug 2026] Tess: @Sami Guess who managed to oil the back door hinges, go team!\n[3 Aug 2026] Ana: Afraid the loft clearance day is called off.",
  "question": "By the close of Tuesday, August 4, 2026, is the promise Tess made to oil the back door hinges kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa20d811792",
  "kind": "choice",
  "text": "Plain text of a family chat with the kitchen garden project included, saved by Ravi.\n\nMembers: Leila, Ravi, Ana, Tess\nChat log (oldest first):\n[16 Feb 2026] Ana: @Leila I promise to weed the carrot row by 23 February 2026 if the harvest supper is on.\n[17 Feb 2026] Leila: Great news, the harvest supper is on!\n[17 Feb 2026] Ana: @Leila Can I weed the carrot row by 28 February 2026 instead? I did promise, sorry.\n[20 Feb 2026] Leila: @Tess Relax, I'll sow the broad beans by 24 February 2026, promise.\n[22 Feb 2026] Ana: @Leila Update on my side: I will not weed the carrot row, sorry.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Ana's promise to weed the carrot row at the end of 23 February 2026?",
  "options": [
   "Broken",
   "Waived",
   "Kept",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qeeec770cf5",
  "kind": "choice",
  "text": "Flat chat export, saved by Dara\nCovers the flatmate contract terms, shared among the housemates.\n\nMembers: Priya, Dara, Mo, Arlo\nChat log (oldest first):\n[19 Mar 2026] Dara: @Priya Got it, I'll store the spare bike by March 26, 2026 for sure.\n[22 Mar 2026] Arlo: @Mo Count on me, I'll photograph the bathroom mould by March 28, 2026.\n[23 Mar 2026] Mo: @Priya Count on me to collect the parcel from porch by March 28, 2026, if the gas safety inspection happens.\n[24 Mar 2026] Dara: @Mo I'll return the bin rota by March 27, 2026, providing the agent inventory walk goes ahead.\n[24 Mar 2026] Dara: @Priya Quick question, could I store the spare bike by March 30, 2026 instead?\n[26 Mar 2026] Priya: @Dara Oh hun, I can't budge, so store the spare bike by the old date!\n[29 Mar 2026] Dara: @Priya To my relief, I managed to store the spare bike.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of March 25, 2026, what is the date by which Dara has to store the spare bike, counting any agreed change?",
  "options": [
   "March 30, 2026",
   "March 28, 2026",
   "March 26, 2026"
  ]
 },
 {
  "qid": "qbe68661bde",
  "kind": "yes/no",
  "text": "{\"export_type\": \"group chat export\", \"chat_topic\": \"the campaign edit\", \"saved_by\": \"Ivo\"}\n\nMembers: Arlo, Femi, Priya, Ivo\nChat export (date | from | to | message):\n2026-03-21 | Arlo | Ivo | If the festival premiere is on, I'll definitely export the subtitle files by Monday, 30 March 2026.\n2026-03-22 | Arlo | Femi | Count on me to ship the hard drive by Saturday, 28 March 2026.\n2026-03-27 | Femi | group | Update: the festival premiere is going ahead as planned.\n2026-03-28 | Arlo | Femi | Would it be fine if I ship the hard drive by Wednesday, 1 April 2026 instead, yeah?\n2026-03-28 | Femi | Arlo | Nah, the date's staying put, so you can ship the hard drive.\n2026-03-28 | Arlo | Femi | Update on my side: I will not ship the hard drive, sorry.",
  "question": "Does the card's rule set show that Arlo has not kept the promise to ship the hard drive at the end of Saturday, 28 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7d4cc53fad",
  "kind": "yes/no",
  "text": "Attached chat: the spring campaign\nShared by: Sami\n\nMembers: Hana, Tomas, Sami\nChat export (date | from | to | message):\n2026-10-09 | Sami | Hana | Count on me, I'll fetch the campaign budget sheet by 12 Oct 2026.\n2026-10-10 | Sami | Hana | Guaranteed I'll send the newsletter copy by 13 Oct 2026.\n2026-10-11 | Tomas | Hana | As long as the brand photo shoot is on, I will draft the press release by 14 Oct 2026.\n2026-10-12 | Tomas | group | Sad to report that the brand photo shoot is off.\n2026-10-14 | Sami | Hana | For the record: I was able to send the newsletter copy",
  "question": "Does the card's rule set show that Sami has not kept the promise to send the newsletter copy at the end of 14 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf16f7eb5a8",
  "kind": "choice",
  "text": "This shared chat of a family on the front garden scheme was saved by Sami for the record.\n\nMembers: Tomas, Wren, Sami, Kofi\nChat log (oldest first):\n[21 Jul 2026] Wren: @Tomas I will make sure to return the ladders by Sunday, 26 July 2026.\n[22 Jul 2026] Sami: @Kofi Might manage to lend the stepladder by Sunday, 26 July 2026, who knows.\n[23 Jul 2026] Sami: @Wren Got it, I'll lend the stepladder by Tuesday, 28 July 2026 for sure.\n[23 Jul 2026] Tomas: @Sami Don't sweat it, there's no need to lend the stepladder\n[24 Jul 2026] Wren: @Kofi As long as the parking permit visit is on, I'll share the garden hose by Friday, 31 July 2026.\n[25 Jul 2026] Sami: Team, the parking permit visit stays on as booked.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of Tuesday, 28 July 2026, which status does Sami have for the promise to lend the stepladder?",
  "options": [
   "Broken",
   "Waived",
   "Not yet due",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qf0e382195b",
  "kind": "choice",
  "text": "Forwarded by Mo, these tenant replies are about the balcony garden project for the file.\n\nMembers: Nadia, Hana, Mo, Yuki\nChat log (oldest first):\n[16 Jun 2026] Nadia: @Mo If the lease renewal call goes ahead, I'll gladly drop the bin bags off by 2026-06-21.\n[21 Jun 2026] Hana: @Yuki Relax, I'll remove the bathroom shelf by 2026-06-26 for sure.\n[22 Jun 2026] Hana: @Yuki Might I ask whether I could remove the bathroom shelf by 2026-06-30 instead?\n[24 Jun 2026] Hana: @Nadia Promise to email the leak photos by 2026-07-01 if the rent review meeting goes ahead.\n[25 Jun 2026] Nadia: @Hana Good news, you're let off having to remove the bathroom shelf",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Hana's pledge to remove the bathroom shelf at the end of 2026-06-30?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q0a72086192",
  "kind": "choice",
  "text": "Mo saved this exchange with the client about the big day.\n\nMembers: Hana, Omar, Mo, Tess\nChat log (oldest first):\n[30 Sep 2026] Mo: @Tess I'll try to charge the flash batteries by 3 Oct 2026.\n[1 Oct 2026] Mo: @Hana Committing to charge the flash batteries by 7 Oct 2026.\n[2 Oct 2026] Mo: @Hana Mind giving me until 11 Oct 2026 to charge the flash batteries?\n[4 Oct 2026] Omar: @Mo Yes, happy for you to charge the flash batteries by 11 Oct 2026 instead.\n[5 Oct 2026] Mo: @Omar If the ceremony walkthrough goes ahead, I'll gladly send the sneak peek gallery by 9 Oct 2026.\n[6 Oct 2026] Omar: @Mo Quick update: you do not need to charge the flash batteries at all.\n[8 Oct 2026] Mo: Sadly, the ceremony walkthrough won't go ahead.\n[10 Oct 2026] Mo: @Hana Got myself to charge the flash batteries lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Mo supposed to charge the flash batteries by, going by the chat at the end of 6 Oct 2026 and any agreed changes?",
  "options": [
   "11 Oct 2026",
   "7 Oct 2026",
   "9 Oct 2026"
  ]
 },
 {
  "qid": "qbe1310abca",
  "kind": "yes/no",
  "text": "Shared by Sami, this thread covers the playground project for whoever is at the help desk.\n\nMembers: Greta, Rhea, Sami\nChat export (date | from | to | message):\n2026-01-28 | Sami | Rhea | Promise to collect the bake sale tins by 2 Feb 2026 if the reading festival goes ahead.\n2026-01-29 | Greta | Rhea | I will make sure to count the donation boxes by 31 Jan 2026.\n2026-01-30 | Greta | group | Sorry all, the reading festival is called off.\n2026-01-31 | Sami | Rhea | Any chance I can collect the bake sale tins by 5 Feb 2026 instead?\n2026-01-31 | Rhea | Sami | No change, you need to collect the bake sale tins by the original date.",
  "question": "Is the promise Sami made to collect the bake sale tins in a status other than broken at the end of 31 Jan 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0b117b5c99",
  "kind": "choice",
  "text": "Chat attached to the support case about the bathroom refit, shared by Kai.\n\nMembers: Kai, Hana, Sami, Yuki\nChat export (date | from | to | message):\n2026-01-29 | Yuki | Sami | Count on me, I'll collect the sanding pads by 31 Jan 2026.\n2026-01-30 | Sami | Yuki | Only if the removal van arrival is on, I will print the floor plan by 4 Feb 2026.\n2026-01-30 | Yuki | group | Thanks, got it.\n2026-01-31 | Yuki | Sami | My sincere apologies, I am unable to collect the sanding pads.\n2026-01-31 | Sami | group | Quick heads up, the removal van arrival is scrapped.\n2026-01-31 | Sami | Yuki | Think 10 Feb 2026 would work if I print the floor plan instead?",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Sami's promise to print the floor plan at the end of 3 Feb 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q0910205e12",
  "kind": "choice",
  "text": "Oskar saved this so we stay on the same page about the student house hunt, mates.\n\nMembers: Nadia, Oskar, Yuki\nChat log (oldest first):\n[25 Sep 2026] Nadia: @Yuki Guaranteed I'll forward the inventory photos by Tuesday, 29 September 2026.\n[25 Sep 2026] Yuki: Cheers, noted.\n[25 Sep 2026] Nadia: @Oskar Count on me to store the spare bike by Friday, 2 October 2026, if the house hunting viewing happens.\n[27 Sep 2026] Nadia: @Yuki Is it all right if I forward the inventory photos by Saturday, 3 October 2026 instead?\n[27 Sep 2026] Oskar: @Nadia I'll photograph the bathroom mould by Thursday, 1 October 2026, promise.\n[28 Sep 2026] Yuki: @Nadia Of course, it is fine for you to forward the inventory photos by Saturday, 3 October 2026.\n[28 Sep 2026] Nadia: @Yuki I will print the tenancy agreement by Thursday, 1 October 2026 only if the gas safety inspection happens.\n[3 Oct 2026] Nadia: @Yuki To my relief, I managed to forward the inventory photos.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat's the day Nadia needs to forward the inventory photos by at the end of Sunday, 11 October 2026, after any new date the group agreed on?",
  "options": [
   "Friday, 2 October 2026",
   "Tuesday, 29 September 2026",
   "Saturday, 3 October 2026"
  ]
 },
 {
  "qid": "q3d440ea23c",
  "kind": "yes/no",
  "text": "Client thread on the gallery show, shared by Ivo for the project log.\n\nMembers: Kofi, Ana, Ivo\nChat log (oldest first):\n[3 Oct 2026] Ivo: @Kofi I will make sure to collect the photo credits by 9 Oct 2026.\n[5 Oct 2026] Ivo: @Kofi Count on me to mail the business cards by 10 Oct 2026 if the sign reveal is on.\n[5 Oct 2026] Kofi: Sad to report that the sign reveal is off.\n[7 Oct 2026] Ana: @Ivo Ah, no stress, no need for you to collect the photo credits\n[12 Oct 2026] Ivo: @Kofi Guess who managed to collect the photo credits, go team!",
  "question": "Is it true that the promise Ivo made to collect the photo credits has not been broken at the end of 13 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7d8e2348f0",
  "kind": "choice",
  "text": "Help desk export\nAbout: the new kit design\nCopied by: Bruno\n\nMembers: Dara, Bruno, Nadia, Priya\nChat log (oldest first):\n[23 Apr 2026] Priya: @Dara I'll wash the club jerseys by 1 May 2026, promise.\n[25 Apr 2026] Dara: @Bruno If the group ride goes ahead, I'll print the route cards by 28 April 2026.\n[25 Apr 2026] Nadia: Update: the group ride is going ahead as planned.\n[26 Apr 2026] Priya: @Dara No need to print the route cards, I'm letting you off\n[30 Apr 2026] Priya: @Dara Scratch what I said, I won't wash the club jerseys.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Dara made to print the route cards have at the end of 26 April 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Broken",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q162c66a50d",
  "kind": "choice",
  "text": "Copied out of the local club chat, covering the music library, by Nadia.\n\nMembers: Ivo, Omar, Nadia, Dara\nChat log (oldest first):\n[25 Mar 2026] Ivo: @Dara Provided the joint concert happens, I'll send the audition reminders by 30 March 2026.\n[26 Mar 2026] Nadia: @Ivo I own this, I'll return the library scores by 31 March 2026.\n[26 Mar 2026] Dara: Team, the joint concert is not happening.\n[26 Mar 2026] Dara: @Nadia Ticket's mine, I'll collect the sheet music by 30 March 2026.\n[31 Mar 2026] Ivo: @Nadia You are released, no requirement to return the library scores.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Nadia's promise to return the library scores have at the end of 3 April 2026?",
  "options": [
   "Waived",
   "Broken",
   "Not triggered",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q42757ca496",
  "kind": "yes/no",
  "text": "Hana shared this so the speed bump plan is easy to find, flatmates.\n\nMembers: Greta, Malik, Hana\nChat log (oldest first):\n[10 Aug 2026] Hana: @Greta I'll try to feed the cat across the road by 12 August 2026, can't promise!\n[11 Aug 2026] Hana: @Greta Committing to feed the cat across the road by 14 August 2026.\n[12 Aug 2026] Greta: @Hana If the road works meeting goes ahead, I'll share the garden hose by 17 August 2026.\n[15 Aug 2026] Hana: @Greta To my relief, I managed to feed the cat across the road.\n[15 Aug 2026] Greta: @Malik I'll sweep the pavement outside by 22 August 2026, promise.\n[16 Aug 2026] Hana: @Greta I'll lock the side gate by 23 August 2026, providing the parking permit visit goes ahead.",
  "question": "Is Hana's promise to feed the cat across the road kept as of 15 August 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q87463e7d60",
  "kind": "yes/no",
  "text": "Team channel: the peer review\nExported by Tomas.\n\nMembers: Ines, Tomas, Rhea\nChat log (oldest first):\n[15 May 2026] Tomas: @Rhea I will make sure to scan the field notes by 18 May 2026.\n[18 May 2026] Rhea: @Tomas I'll clean the glassware set by 20 May 2026, promise.\n[19 May 2026] Rhea: @Ines Lovely, I'll collect the lab samples by 26 May 2026 if the conference trip is on.\n[22 May 2026] Ines: Just so you know, the conference trip is on as scheduled.\n[25 May 2026] Rhea: @Ines I regret to say that I shall not collect the lab samples.",
  "question": "At the end of 26 May 2026, has Rhea broken its promise to collect the lab samples?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q629f5e8bbe",
  "kind": "choice",
  "text": "Support case copy, filed for the new repertoire\nSaved on record by Bruno\n\nMembers: Dara, Leila, Bruno\nChat log (oldest first):\n[30 Jun 2026] Bruno: @Leila Promise to buy the spare folders by 5 Jul 2026 if the summer recital goes ahead.\n[1 Jul 2026] Bruno: Sorry, the summer recital is off.\n[3 Jul 2026] Dara: @Leila I will book the rehearsal room by 7 Jul 2026.\n[4 Jul 2026] Bruno: @Leila Lovely, I'll send the audition reminders by 11 Jul 2026 for sure.\n[5 Jul 2026] Dara: @Leila I'll return the library scores by 7 Jul 2026 as long as the carol concert is on.\n[11 Jul 2026] Bruno: @Leila Log entry: send the audition reminders, carried out",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Bruno's commitment to send the audition reminders is in what status at the end of 14 Jul 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Not yet due",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q3d115229ca",
  "kind": "yes/no",
  "text": "Pasted into the project log by Zara, the thread with a client about the showreel refresh.\n\nMembers: Nadia, Bruno, Zara, Elif\nChat export (date | from | to | message):\n2026-05-03 | Elif | Nadia | As long as the agency review call is on, I'll back up the project drives by 9 May 2026.\n2026-05-04 | Elif | Nadia | It's on me to fetch the raw footage by 6 May 2026.\n2026-05-05 | Nadia | Bruno | Guaranteed I'll record the voice over by 8 May 2026.\n2026-05-05 | Elif | Nadia | You are released, no requirement to record the voice over.\n2026-05-05 | Nadia | Bruno | Guess what, I managed to record the voice over!\n2026-05-08 | Nadia | group | Fab, we are on for the agency review call as planned!",
  "question": "Does the card's rule set show that Nadia has not kept the promise to record the voice over at the end of 8 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf4df71df96",
  "kind": "choice",
  "text": "Support thread for a help desk case, covering the league run, saved by Lena.\n\nMembers: Femi, Omar, Lena, Sami\nChat log (oldest first):\n[6 Sep 2026] Femi: @Omar Relax, I'll fetch the medical bag by 14 September 2026 for sure.\n[6 Sep 2026] Lena: @Femi I promise to set up the corner flags by 11 September 2026.\n[10 Sep 2026] Sami: @Omar As long as the cup tie is on, I will collect the referee whistles by 15 September 2026.\n[11 Sep 2026] Omar: Update: the cup tie is going ahead as planned.\n[12 Sep 2026] Sami: @Omar I committed to collect the referee whistles, can I do that by 18 September 2026 instead?\n[13 Sep 2026] Omar: @Sami Yes, you're welcome to collect the referee whistles by 18 September 2026 instead.\n[18 Sep 2026] Sami: @Omar Log entry: collect the referee whistles, carried out",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nFollowing the rules set out on the card, what date governs Sami's commitment to collect the referee whistles at the end of 23 September 2026, once any agreed shift in the date is factored in?",
  "options": [
   "18 September 2026",
   "11 September 2026",
   "15 September 2026"
  ]
 },
 {
  "qid": "qe340b07674",
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
  "qid": "q8eeed7d1ba",
  "kind": "yes/no",
  "text": "{\"source\": \"saved thread\", \"about\": \"the reunion weekend\", \"owner\": \"Lee\", \"kind\": \"chat export\"}\n\nMembers: Lee, Ravi, Nadia\nChat log (oldest first):\n[13 Jan 2026] Nadia: @Ravi I will make sure to fetch the speaker system by Sunday, 18 January 2026.\n[15 Jan 2026] Lee: @Nadia You can bank on me to reserve the reunion hall by Wednesday, 21 January 2026.\n[15 Jan 2026] Lee: @Nadia As long as the reunion lunch is on, I will print the family tree chart by Saturday, 17 January 2026.\n[15 Jan 2026] Nadia: Fab, we are on for the reunion lunch as planned!\n[16 Jan 2026] Nadia: @Ravi I have to take back my promise to fetch the speaker system.\n[16 Jan 2026] Ravi: @Lee You are released, no requirement to reserve the reunion hall.",
  "question": "Under the rules on the card, is it true that Lee has not kept the promise to reserve the reunion hall as of Friday, 16 January 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc88583ad5f",
  "kind": "choice",
  "text": "Client thread on the rebrand package, saved by Lena for the project log.\n\nMembers: Malik, Lena, Rhea, Yuki\nChat log (oldest first):\n[3 Nov 2026] Rhea: @Yuki Ticket's mine, I'll mail the business cards by 9 Nov 2026.\n[5 Nov 2026] Malik: @Rhea Count on me to collect the photo credits by 11 Nov 2026, if the print run happens.\n[8 Nov 2026] Malik: Really pleased to say the print run will go ahead!\n[9 Nov 2026] Yuki: @Rhea Good news, you're let off having to mail the business cards\n[10 Nov 2026] Rhea: @Yuki Guess what, I managed to mail the business cards!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Rhea's promise to mail the business cards receive at the end of 11 Nov 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "q820ff52d96",
  "kind": "choice",
  "text": "Casual chat for the flat, saved by Nadia, and it covers the lodger house rules.\n\nMembers: Ivo, Sami, Nadia, Arlo\nChat export (date | from | to | message):\n2026-10-15 | Ivo | Arlo | Count on me, I'll buy the washing powder by 18 Oct 2026.\n2026-10-15 | Arlo | group | Thanks mate, noted.\n2026-10-15 | Arlo | Ivo | Count on me to defrost the top freezer by 23 Oct 2026 if the water tank check is on.\n2026-10-16 | Ivo | Nadia | I'll cut a spare door key by 19 Oct 2026, promise.\n2026-10-18 | Nadia | Ivo | Quick update: you do not need to buy the washing powder at all.\n2026-10-18 | Ivo | group | Just so you know, the water tank check is on as scheduled.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 22 Oct 2026, what status has Ivo's promise to buy the washing powder got?",
  "options": [
   "Waived",
   "Broken",
   "Not yet due",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q968ca52260",
  "kind": "choice",
  "text": "Here we plan the family day out together, and Elif saved this for the family.\n\nMembers: Arlo, Elif, Lee, Ana\nChat log (oldest first):\n[14 Jun 2026] Elif: @Ana Provided the school play happens, I'll mend the kite string by Thursday, June 18, 2026.\n[16 Jun 2026] Elif: @Ana It's on me to read the bedtime story by Tuesday, June 23, 2026.\n[16 Jun 2026] Elif: @Ana Is Saturday, June 27, 2026 alright for me to read the bedtime story?\n[16 Jun 2026] Arlo: Great news, the school play is on!\n[17 Jun 2026] Lee: How's the plan to read the bedtime story?\n[23 Jun 2026] Lee: @Elif Relax, mate, you're not expected to read the bedtime story",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Elif's undertaking to read the bedtime story hold at the end of Tuesday, June 23, 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Broken",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qb471282836",
  "kind": "yes/no",
  "text": "{\"saved_copy_of\": \"group chat\", \"subject\": \"the lab move\", \"saver\": \"Priya\", \"format\": \"plain text\"}\n\nMembers: Leila, Wren, Priya\nChat log (oldest first):\n[24 Aug 2026] Priya: @Wren I will make sure to fetch the grant forms by 3 Sep 2026.\n[27 Aug 2026] Leila: @Wren I'll collect the lab samples by 2 Sep 2026 if the seminar series goes ahead.\n[28 Aug 2026] Leila: Brilliant news everyone, the seminar series is a go!\n[30 Aug 2026] Wren: @Leila I promise to order the reagent kit by 3 Sep 2026 if the journal club is on.\n[31 Aug 2026] Wren: @Leila Please don't feel you have to collect the lab samples\n[31 Aug 2026] Leila: @Wren I'll send the ethics form by 6 Sep 2026, promise.",
  "question": "By the end of 31 Aug 2026, has Leila kept the promise to collect the lab samples?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q24e98ad0e6",
  "kind": "yes/no",
  "text": "Saved by Kai from the shared house thread on the rent split plan.\n\nMembers: Ines, Bruno, Hana, Kai\nChat log (oldest first):\n[5 May 2026] Bruno: @Hana Got it, I'll photograph the bathroom mould by 13 May 2026 for sure.\n[5 May 2026] Bruno: @Kai Got it, I'll forward the inventory photos by 12 May 2026 for sure.\n[6 May 2026] Bruno: @Hana If the house hunting viewing goes ahead, I'll gladly print the tenancy agreement by 9 May 2026.\n[8 May 2026] Ines: @Bruno I assure you I'll ring the letting agent by 16 May 2026 if the gas safety inspection is on.\n[14 May 2026] Bruno: @Hana To note: I have managed to photograph the bathroom mould",
  "question": "Was the promise to photograph the bathroom mould from Bruno kept on 16 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9d7bce2324",
  "kind": "choice",
  "text": "Saved by Tess, this is the household group chat about the home adaptations, copied in full.\n\nMembers: Ana, Greta, Ravi, Tess\nChat log (oldest first):\n[6 Mar 2026] Tess: @Ravi Relax, I'll pick up the repeat prescription by Saturday, March 14, 2026, promise.\n[9 Mar 2026] Ravi: @Ana If the carer handover goes ahead, I'll gladly collect the post by Friday, March 13, 2026.\n[11 Mar 2026] Greta: Update: the carer handover is going ahead as planned.\n[13 Mar 2026] Greta: @Ravi Relax, mate, you're not expected to collect the post\n[16 Mar 2026] Ravi: @Ana To my relief, I managed to collect the post.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Ravi made to collect the post at the end of Friday, March 13, 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Kept",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "q7d8c14c4b7",
  "kind": "choice",
  "text": "Subject: chat about the lodger house rules, forwarded\nThe chat follows below.\nRegards, Ivo\n\nMembers: Kai, Tess, Ivo, Yuki\nChat export (date | from | to | message):\n2026-03-27 | Tess | Kai | I'll replace the loo roll by 3 April 2026, providing the lodger farewell supper goes ahead.\n2026-03-29 | Kai | Tess | Absolutely, I will feed the house plants by 2 April 2026.\n2026-03-29 | Yuki | Kai | Please don't feel you have to feed the house plants\n2026-03-29 | Kai | Tess | I will defrost the top freezer by 7 April 2026 only if the fuse box inspection happens.\n2026-03-31 | Tess | group | Sorry all, the lodger farewell supper is called off.\n2026-04-03 | Kai | Tess | Got it, I'll drop the parcel upstairs by 9 April 2026 for sure.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Kai's promise to feed the house plants at the end of 29 March 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Broken",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "qe93b9b1461",
  "kind": "choice",
  "text": "Committee chat on the school fundraiser, forwarded by Kai to the volunteers.\n\nMembers: Kai, Ravi, Rhea, Lena\nChat export (date | from | to | message):\n2026-01-23 | Ravi | group | No promises, but I'll aim to send the newsletter drafts by 29 January 2026.\n2026-01-25 | Ravi | Lena | Committing to send the newsletter drafts by 30 January 2026.\n2026-01-26 | Rhea | Ravi | Don't sweat it, there's no need to send the newsletter drafts\n2026-01-26 | Kai | Ravi | I'll collect the bake sale tins by 1 February 2026, provided the quiz night happens.\n2026-01-27 | Ravi | Lena | To note: I have managed to send the newsletter drafts\n2026-01-27 | Lena | Ravi | I'll book the school hall by 2 February 2026, provided the governors meeting happens.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Ravi's pledge to send the newsletter drafts sit at the end of 26 January 2026?",
  "options": [
   "Waived",
   "Kept",
   "Not yet due",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "qbcfd43cf1b",
  "kind": "choice",
  "text": "Exported by Rhea, this is the full back and forth on the payment setup.\n\nMembers: Zara, Rhea, Yuki, Ivo\nChat log (oldest first):\n[25 Feb 2026] Ivo: @Rhea Relax, I'll set up the email forwarding by 4 March 2026, promise.\n[26 Feb 2026] Rhea: @Zara Count on me to renew the hosting plan by 6 March 2026, if the courier pickup happens.\n[27 Feb 2026] Ivo: @Rhea Would it be fine if I set up the email forwarding by 8 March 2026 instead, yeah?\n[27 Feb 2026] Zara: Quick heads up, the courier pickup is scrapped.\n[28 Feb 2026] Rhea: @Ivo Yes, you can set up the email forwarding by 8 March 2026 if that suits you.\n[28 Feb 2026] Zara: @Ivo You don't have to set up the email forwarding at all\n[28 Feb 2026] Yuki: @Rhea If the product photo day is on, I'll definitely test the mobile layout by 7 March 2026.\n[7 Mar 2026] Ivo: @Rhea Ticked off my list: set up the email forwarding, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo what's the latest day Ivo has to set up the email forwarding by at the end of 10 March 2026, given any new date people agreed to?",
  "options": [
   "6 March 2026",
   "8 March 2026",
   "4 March 2026"
  ]
 },
 {
  "qid": "q5d88cf0072",
  "kind": "yes/no",
  "text": "{\"record\": \"shared group chat\", \"subject\": \"the guest list\", \"shared_by\": \"Dara\", \"stored\": \"as text\"}\n\nMembers: Dara, Leila, Kofi, Priya\nChat log (oldest first):\n[28 Jul 2026] Priya: @Leila Guaranteed I'll return the lighting stands by Sunday, August 2, 2026.\n[2 Aug 2026] Priya: @Leila Think Saturday, August 8, 2026 would work if I return the lighting stands instead?\n[2 Aug 2026] Priya: @Leila Change of plans: I will not return the lighting stands\n[2 Aug 2026] Kofi: @Leila Provided the rehearsal dinner happens, I'll collect the venue floor plan by Monday, August 10, 2026.\n[3 Aug 2026] Priya: @Dara Provided the bridal shower happens, I will buy the candle props by Sunday, August 9, 2026.\n[3 Aug 2026] Kofi: Just so you know, the bridal shower is on as scheduled.",
  "question": "Is Priya's promise to return the lighting stands broken at the end of Tuesday, August 4, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0460046fab",
  "kind": "choice",
  "text": "Committee group\nExported by Priya, shared as a thread on the sponsor search.\n\nMembers: Lena, Priya, Ivo, Leila\nChat log (oldest first):\n[5 Feb 2026] Ivo: @Priya Committing to wash the club jerseys by 12 February 2026.\n[8 Feb 2026] Ivo: @Leila Guaranteed I'll set up the feed stop by 12 February 2026.\n[8 Feb 2026] Lena: @Leila You can bet I'll tune the gear cables by 13 February 2026.\n[9 Feb 2026] Ivo: @Priya Provided the swap meet happens, I'll print the route cards by 15 February 2026.\n[11 Feb 2026] Leila: Brilliant news everyone, the swap meet is a go!\n[12 Feb 2026] Ivo: @Leila Guess who managed to set up the feed stop, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Ivo made to print the route cards have at the end of 15 February 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Waived",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "qcbb87c866c",
  "kind": "yes/no",
  "text": "Freelance thread record, the campaign edit, shared by Lee.\n\nMembers: Nadia, Lee, Dara, Leila\nChat export (date | from | to | message):\n2026-06-08 | Nadia | Lee | Relax, I'll upload the render files by Thursday, 11 June 2026 for sure.\n2026-06-09 | Nadia | Lee | Scratch that, I'm not going to upload the render files\n2026-06-10 | Nadia | Leila | As long as the grading session is on, I'll fetch the raw footage by Saturday, 13 June 2026.\n2026-06-12 | Lee | group | Yep, the grading session is on as planned.\n2026-06-12 | Nadia | Leila | My sincere apologies, I am unable to fetch the raw footage.",
  "question": "Is Nadia's promise to fetch the raw footage broken at the end of Tuesday, 16 June 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
