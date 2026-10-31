# G5-H blind read (all free-form rows) T32-blind_read-c97f52fe-003 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root/T32/qc/g5h/answers/T32-blind_read-c97f52fe-003.json

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
  "qid": "q3e4647389a",
  "kind": "yes/no",
  "text": "Volunteers, Bruno shared this with you about the winter concert.\n\nMembers: Ines, Femi, Bruno\nChat log (oldest first):\n[10 Aug 2026] Ines: See if I can buy the spare folders by 20 August 2026.\n[11 Aug 2026] Femi: @Bruno If the sing along goes ahead, I'll gladly print the song sheets by 17 August 2026.\n[12 Aug 2026] Femi: @Ines If the carol concert is on, I'll definitely move the piano by 20 August 2026.\n[12 Aug 2026] Ines: @Bruno Relax, I'll buy the spare folders by 16 August 2026 for sure.\n[15 Aug 2026] Bruno: @Femi Lovely, I'll fix the stand microphones by 23 August 2026 for sure.\n[17 Aug 2026] Ines: @Bruno For the record: I was able to buy the spare folders",
  "question": "According to the rules on the card, does the promise Ines made to buy the spare folders have any status except broken at the end of 20 August 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q024fef6ed0",
  "kind": "choice",
  "text": "Subject: Saved thread about the music library\nThis export came from Priya and is pasted in full below.\n\nMembers: Priya, Ana, Jonas, Arlo\nChat log (oldest first):\n[23 Apr 2026] Jonas: @Priya Aiming to send the audition reminders by 30 April 2026, we'll see.\n[25 Apr 2026] Ana: @Jonas I will make sure to fetch the choir robes by 3 May 2026.\n[25 Apr 2026] Jonas: @Ana I'll send the audition reminders by 29 April 2026 as long as the sing along is on.\n[26 Apr 2026] Priya: Sorry, the sing along is off.\n[28 Apr 2026] Jonas: @Ana Might I ask whether I could send the audition reminders by 2 May 2026 instead?\n[29 Apr 2026] Ana: @Jonas Yes, you can send the audition reminders by 2 May 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Jonas made to send the audition reminders is in which status at the end of 29 April 2026?",
  "options": [
   "Waived",
   "Kept",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "qbd211ab298",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the caring rota\nThis export came from Tomas and is pasted in full below.\n\nMembers: Tomas, Dara, Wren, Lee\nChat log (oldest first):\n[3 Oct 2026] Dara: @Lee It's on me to fetch the mobility aids by Sunday, October 11, 2026.\n[5 Oct 2026] Wren: @Tomas Promise to call the home nurse by Monday, October 12, 2026 if the carer handover goes ahead.\n[5 Oct 2026] Tomas: @Dara Good news, you're let off having to fetch the mobility aids\n[6 Oct 2026] Tomas: @Lee I will book the clinic transport by Monday, October 12, 2026 only if the eye test happens.\n[6 Oct 2026] Dara: @Lee Got myself to fetch the mobility aids lol.\n[8 Oct 2026] Wren: @Lee I'll collect the post by Thursday, October 15, 2026 as long as the physio session is on.",
  "question": "Is Dara's promise to fetch the mobility aids kept at the end of Sunday, October 11, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6141dfb231",
  "kind": "choice",
  "text": "Yo flatmates, Sami shared this chat about the guest welcome plan, so chip in.\n\nMembers: Mo, Kai, Sami, Ana\nChat log (oldest first):\n[8 Feb 2026] Mo: @Sami I'll wash the beach towels by Thursday, 12 February 2026, provided the owner handover visit happens.\n[9 Feb 2026] Sami: @Kai Relax, I'll restock the guest toiletries by Saturday, 14 February 2026 for sure.\n[10 Feb 2026] Mo: Fab, we are on for the owner handover visit as planned!\n[10 Feb 2026] Sami: @Kai Ticked off: restock the guest toiletries, feels so good\n[12 Feb 2026] Mo: @Sami Is Wednesday, 18 February 2026 alright for me to wash the beach towels?\n[12 Feb 2026] Sami: @Mo We are holding the date on record, so wash the beach towels by it.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Mo's promise to wash the beach towels have at the end of Wednesday, 11 February 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q79b66c5c52",
  "kind": "choice",
  "text": "Our flat chat about the summer lets season, saved by Mo for whoever lives here.\n\nMembers: Leila, Mo, Greta, Yuki\nChat log (oldest first):\n[22 Mar 2026] Yuki: @Mo Committing to wheel the bins out by 28 March 2026.\n[24 Mar 2026] Yuki: @Mo Mind giving me until 2 April 2026 to wheel the bins out?\n[28 Mar 2026] Mo: @Yuki Yes, you're welcome to wheel the bins out by 2 April 2026 instead.\n[28 Mar 2026] Leila: @Yuki If the owner handover visit is on, I'll definitely scrub the hot tub by 5 April 2026.\n[29 Mar 2026] Yuki: @Mo Quick report: I've managed to wheel the bins out\n[29 Mar 2026] Leila: @Greta I will wash the beach towels by 4 April 2026.\n[31 Mar 2026] Leila: @Greta I'll restock the guest toiletries by 3 April 2026, providing the summer season launch goes ahead.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of 31 March 2026, what is the date by which Yuki has to wheel the bins out, counting any agreed change?",
  "options": [
   "5 April 2026",
   "2 April 2026",
   "28 March 2026"
  ]
 },
 {
  "qid": "qfee47212c3",
  "kind": "yes/no",
  "text": "Posted by Ivo from the work channel, the field survey thread.\n\nMembers: Zara, Omar, Ivo\nChat log (oldest first):\n[10 Apr 2026] Ivo: @Zara If the safety inspection goes ahead, I'll gladly submit the ethics application by Wednesday, April 15, 2026.\n[12 Apr 2026] Zara: @Ivo Relax, I'll print the poster abstracts by Tuesday, April 14, 2026 for sure.\n[13 Apr 2026] Omar: Team, the safety inspection stays on as booked.\n[14 Apr 2026] Omar: @Zara Forget it, you won't need to print the poster abstracts\n[16 Apr 2026] Ivo: @Zara Guess who managed to submit the ethics application, go team!",
  "question": "Is the promise Ivo made to submit the ethics application something that has not been broken at the end of Sunday, April 19, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qde99938489",
  "kind": "choice",
  "text": "Omar forwarded this for the committee as we dig in on the volunteer roster.\n\nMembers: Omar, Greta, Hana, Bruno\nChat export (date | from | to | message):\n2026-03-01 | Greta | Hana | Got it, I'll return the borrowed trestle tables by 7 Mar 2026 for sure.\n2026-03-03 | Bruno | Greta | Ah, no stress, no need for you to return the borrowed trestle tables\n2026-03-04 | Omar | Greta | Provided the governors meeting happens, I'll send the newsletter drafts by 6 Mar 2026.\n2026-03-04 | Greta | Hana | Guess who managed to return the borrowed trestle tables, go team!\n2026-03-05 | Hana | group | Just so you know, the governors meeting is on as scheduled.",
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
  "qid": "q4af81c9458",
  "kind": "yes/no",
  "text": "Hana shared this exchange with the client about the showreel refresh.\n\nMembers: Tomas, Sami, Hana\nChat export (date | from | to | message):\n2026-06-05 | Sami | Hana | Provided the client screening happens, I'll send the colour notes by 8 June 2026.\n2026-06-07 | Sami | group | Quick heads up, the client screening is scrapped.\n2026-06-09 | Hana | Sami | I own this, I'll fetch the raw footage by 16 June 2026.\n2026-06-10 | Tomas | Hana | Nobody needs you to fetch the raw footage, that's that\n2026-06-11 | Hana | Sami | Guess what, I managed to fetch the raw footage!\n2026-06-17 | Tomas | group | Anything new on your way to fetch the raw footage?",
  "question": "On the card, was Hana's promise to fetch the raw footage broken, waived, not triggered or not yet due, rather than kept, at the end of 17 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qba2a481912",
  "kind": "choice",
  "text": "Team channel export, shared by Kai, which is about the visitor policy.\n\nMembers: Hana, Kai, Mo\nChat log (oldest first):\n[24 Feb 2026] Hana: @Mo I'll renew the fire extinguisher service by 3 March 2026, providing the building survey goes ahead.\n[28 Feb 2026] Mo: Yep, the building survey is on as planned.\n[1 Mar 2026] Hana: @Mo Is it all right if I renew the fire extinguisher service by 5 March 2026 instead?\n[1 Mar 2026] Kai: @Hana Yes, you can renew the fire extinguisher service by 5 March 2026 instead.\n[2 Mar 2026] Kai: @Hana Don't sweat it, there's no need to renew the fire extinguisher service\n[3 Mar 2026] Kai: @Mo I promise to collect the visitor badges by 6 March 2026.\n[5 Mar 2026] Hana: @Mo Guess what, I managed to renew the fire extinguisher service!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nFollowing the rules set out on the card, what date governs Hana's commitment to renew the fire extinguisher service at the end of 9 March 2026, once any agreed shift in the date is factored in?",
  "options": [
   "6 March 2026",
   "3 March 2026",
   "5 March 2026"
  ]
 },
 {
  "qid": "qe84a62626e",
  "kind": "yes/no",
  "text": "Greta shared this exchange with the client about the wedding weekend.\n\nMembers: Oskar, Kai, Greta\nChat log (oldest first):\n[20 Jan 2026] Oskar: @Greta You can bank on me to print the seating cards by 24 Jan 2026.\n[20 Jan 2026] Greta: Cheers, noted.\n[22 Jan 2026] Kai: @Oskar Ah, no stress, no need for you to print the seating cards\n[24 Jan 2026] Oskar: @Greta To my relief, I managed to print the seating cards.\n[25 Jan 2026] Greta: @Kai As long as the bridal shower is on, I'll book the assistant photographer by 31 Jan 2026.\n[25 Jan 2026] Greta: Just so you know, the bridal shower is on as scheduled.",
  "question": "Under the rules on the card, is the promise Oskar made to print the seating cards kept as of 24 Jan 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc5988262c4",
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
  "qid": "qf6e09e8041",
  "kind": "yes/no",
  "text": "Ana shared this channel export covering the data cleanup for the team.\n\nMembers: Zara, Ana\nChat log (oldest first):\n[9 Jan 2026] Ana: @Zara I assure you I'll restart the build server by 12 Jan 2026 if the penetration test is on.\n[13 Jan 2026] Zara: @Ana If the hackathon goes ahead, I'll rotate the test keys by 19 Jan 2026.\n[16 Jan 2026] Zara: @Ana I'll merge the login branch by 24 Jan 2026, promise.\n[17 Jan 2026] Ana: Sad to report that the hackathon is off.\n[18 Jan 2026] Zara: @Ana Think 22 Jan 2026 would work if I rotate the test keys instead?\n[19 Jan 2026] Ana: @Zara Yes, lovely, you can rotate the test keys by 22 Jan 2026 instead!",
  "question": "Applying the card's rules, does Zara's promise to rotate the test keys count as broken, waived, not triggered or not yet due, rather than kept, as of 20 Jan 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qcc9c93de63",
  "kind": "choice",
  "text": "Parents and cousins, this is where we sort out the family history. Saved by Lena.\n\nMembers: Lena, Greta, Mo\nChat log (oldest first):\n[1 Apr 2026] Greta: @Lena I'll fetch the speaker system by 7 April 2026 if the garden picnic goes ahead.\n[2 Apr 2026] Greta: Quick heads up, the garden picnic is scrapped.\n[3 Apr 2026] Greta: @Lena I'll print the family tree chart by 10 April 2026, promise.\n[4 Apr 2026] Greta: @Mo Committing to collect the old photo prints by 9 April 2026.\n[6 Apr 2026] Greta: @Mo On my action item, may I collect the old photo prints by 12 April 2026 instead?\n[9 Apr 2026] Mo: @Greta The original date stands, so you need to collect the old photo prints.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Greta's promise to fetch the speaker system at the end of 5 April 2026?",
  "options": [
   "Kept",
   "Broken",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "qc3dee5f04a",
  "kind": "yes/no",
  "text": "Tenant and landlord back-and-forth on the lodger house rules, saved by Kofi.\n\nMembers: Ana, Oskar, Wren, Kofi\nChat export (date | from | to | message):\n2026-07-15 | Kofi | Wren | Provided the fuse box inspection happens, I will buy the washing powder by 19 July 2026.\n2026-07-15 | Kofi | Ana | Relax, I'll replace the loo roll by 20 July 2026 for sure.\n2026-07-17 | Kofi | Ana | On my action item, may I replace the loo roll by 24 July 2026 instead?\n2026-07-17 | Oskar | Kofi | Fine by me, you can replace the loo roll by 24 July 2026.\n2026-07-18 | Ana | group | Update, the fuse box inspection will not take place.",
  "question": "Has Kofi kept the promise to replace the loo roll at the end of 20 July 2026, instead of broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb5128edeef",
  "kind": "choice",
  "text": "Committee chat on the winter concert, shared by Tess with the volunteers.\n\nMembers: Tomas, Dara, Zara, Tess\nChat log (oldest first):\n[20 Aug 2026] Tess: @Tomas I'll collect the sheet music by Thursday, August 27, 2026 if the joint concert goes ahead.\n[25 Aug 2026] Tess: Update: the joint concert is going ahead as planned.\n[25 Aug 2026] Zara: @Dara Guaranteed I'll fetch the choir robes by Tuesday, September 1, 2026.\n[27 Aug 2026] Tess: @Tomas Would it be fine if I collect the sheet music by Monday, August 31, 2026 instead, yeah?\n[27 Aug 2026] Zara: @Tess Works for me, fine for you to collect the sheet music by Monday, August 31, 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Tess's promise to collect the sheet music stand at the end of Wednesday, August 26, 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Not yet due",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q22dfcec806",
  "kind": "choice",
  "text": "Here is the plan for the loft conversion, saved by Tess for the group.\n\nMembers: Tess, Priya, Lena\nChat export (date | from | to | message):\n2026-03-12 | Priya | Tess | I'll try to measure the hallway for shelves by 19 Mar 2026, can't promise!\n2026-03-14 | Lena | Tess | Absolutely, I will fetch the paint samples by 19 Mar 2026.\n2026-03-14 | Priya | Tess | I'll measure the hallway for shelves by 17 Mar 2026 if the boiler install visit goes ahead.\n2026-03-15 | Lena | group | We are dropping the boiler install visit from the list.\n2026-03-20 | Lena | Tess | Count on me, I'll collect the sanding pads by 25 Mar 2026.\n2026-03-20 | Tess | Lena | Relax, mate, you're not expected to collect the sanding pads",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Priya made to measure the hallway for shelves, what state is it in at the end of 16 Mar 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q5665447862",
  "kind": "choice",
  "text": "Forwarded by Kofi: a help-desk thread covering the reunion planning.\n\nMembers: Kofi, Lee\nChat log (oldest first):\n[27 Jun 2026] Kofi: @Lee If the karaoke night goes ahead, I'll pay the catering company by 30 June 2026.\n[27 Jun 2026] Lee: @Kofi Relax, I'll buy the name tags by 6 July 2026, promise.\n[29 Jun 2026] Kofi: We are dropping the karaoke night from the list.\n[2 Jul 2026] Kofi: @Lee Guaranteed I'll send the group invitations by 4 July 2026.\n[4 Jul 2026] Kofi: @Lee Mum, I did send the group invitations, haha.\n[7 Jul 2026] Lee: @Kofi Quick report: I've managed to buy the name tags",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Kofi's promise to pay the catering company at the end of 30 June 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q213b78ae22",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the lab move\nThe chat below comes from Lena, copied as is for reference.\n\nMembers: Priya, Lena, Yuki\nChat log (oldest first):\n[20 Mar 2026] Yuki: @Lena Provided the thesis defence happens, I'll submit the ethics application by Thursday, March 26, 2026.\n[20 Mar 2026] Lena: Update, the thesis defence will not take place.\n[22 Mar 2026] Yuki: @Priya Guaranteed I'll return the library books by Wednesday, March 25, 2026.\n[22 Mar 2026] Priya: @Lena Lovely, I'll book the microscope slot by Saturday, March 28, 2026 if the journal club is on.\n[24 Mar 2026] Lena: @Priya Ticket's mine, I'll clean the glassware set by Monday, March 30, 2026.\n[26 Mar 2026] Yuki: @Priya Got myself to return the library books lol.",
  "question": "According to the card's rules, is the promise Yuki made to return the library books not kept as of Saturday, March 28, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6ae69dc1c7",
  "kind": "choice",
  "text": "Subject: Chat about the trip itinerary\nBelow is a copy that came from Yuki, pasted as found.\n\nMembers: Zara, Rhea, Yuki\nChat export (date | from | to | message):\n2026-05-15 | Rhea | Zara | I own this, I'll buy the packing cubes by 20 May 2026.\n2026-05-16 | Zara | Rhea | If the ferry crossing goes ahead, I'll check the passport copies by 21 May 2026.\n2026-05-16 | Zara | group | On track for the ferry crossing to happen as planned.\n2026-05-17 | Rhea | Zara | Please don't feel you have to check the passport copies\n2026-05-20 | Rhea | Zara | Correction, I will not be able to buy the packing cubes.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Zara's promise to check the passport copies at the end of 16 May 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q6fe3c4d4c6",
  "kind": "choice",
  "text": "Our flat chat about the old house restoration, shared by Kofi for whoever lives here.\n\nMembers: Ivo, Kofi, Arlo\nChat log (oldest first):\n[15 Aug 2026] Kofi: @Arlo I own this, I'll oil the back door hinges by August 18, 2026.\n[15 Aug 2026] Ivo: @Kofi Nobody needs you to oil the back door hinges, that's that\n[16 Aug 2026] Ivo: @Kofi Provided the heritage fete happens, I will clear the kitchen sink by August 21, 2026.\n[18 Aug 2026] Ivo: @Kofi Committing to mend the garden gate by August 23, 2026.\n[18 Aug 2026] Arlo: @Ivo If the loft clearance day goes ahead, I'll find the loft ladder by August 21, 2026.\n[21 Aug 2026] Kofi: @Arlo Quick report: I've managed to oil the back door hinges",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Kofi made to oil the back door hinges at the end of August 22, 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q7605e6b76b",
  "kind": "yes/no",
  "text": "Yo flatmates, Rhea shared this chat about the loft conversion, so chip in.\n\nMembers: Wren, Femi, Yuki, Rhea\nChat export (date | from | to | message):\n2026-03-11 | Wren | Femi | Guaranteed I'll collect the sanding pads by 15 Mar 2026.\n2026-03-11 | Rhea | Wren | Ah, no stress, no need for you to collect the sanding pads\n2026-03-12 | Wren | Femi | Got myself to collect the sanding pads lol.\n2026-03-14 | Rhea | Wren | Lovely, I'll return the tile cutter by 16 Mar 2026 if the removal van arrival is on.\n2026-03-17 | Yuki | Femi | I'll sweep the dust from stairs by 20 Mar 2026, providing the damp survey inspection goes ahead.",
  "question": "Does the card classify Wren's promise to collect the sanding pads as broken, waived, not triggered or not yet due, rather than kept, on 14 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb31b3dbfff",
  "kind": "yes/no",
  "text": "Chat attached to a support case about the wedding weekend, shared by Ines.\n\nMembers: Ines, Leila, Hana\nChat export (date | from | to | message):\n2026-07-01 | Leila | Ines | Committing to buy the candle props by 4 July 2026.\n2026-07-02 | Leila | Ines | Log entry: buy the candle props, carried out\n2026-07-03 | Ines | Hana | I assure you I'll pick up the album prints by 7 July 2026 if the engagement shoot is on.\n2026-07-04 | Hana | group | Team, the engagement shoot stays on as booked.\n2026-07-06 | Hana | group | Any idea how close you are to pick up the album prints?\n2026-07-07 | Ines | Hana | Mum, I did pick up the album prints, haha.",
  "question": "Applying the rules on the card, has Ines kept the promise to pick up the album prints as of 11 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q59aedb3aa3",
  "kind": "yes/no",
  "text": "Hana shared this to pin down the quiet street fund, housemates.\n\nMembers: Ivo, Jonas, Tomas, Hana\nChat log (oldest first):\n[9 Feb 2026] Tomas: @Jonas I will share the garden hose by February 13, 2026 only if the street litter clean happens.\n[11 Feb 2026] Jonas: @Ivo I will lock the side gate by February 17, 2026.\n[12 Feb 2026] Ivo: @Jonas I'll bring the bins in by February 18, 2026, provided the bonfire night happens.\n[13 Feb 2026] Tomas: @Hana Guaranteed I'll feed the cat across the road by February 20, 2026.\n[18 Feb 2026] Jonas: @Ivo Ticked off: lock the side gate, feels so good",
  "question": "At the end of February 19, 2026, does the promise Jonas made to lock the side gate have any status except broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3e18888ff7",
  "kind": "yes/no",
  "text": "Subject: Chat about the school fundraiser\nBelow, with Jonas named as the source, is the chat as exported.\n\nMembers: Jonas, Elif, Sami, Kai\nChat export (date | from | to | message):\n2026-06-16 | Elif | Sami | Absolutely, I will book the school hall by 22 Jun 2026.\n2026-06-21 | Kai | Elif | I will count the donation boxes by 25 Jun 2026 only if the governors meeting happens.\n2026-06-21 | Sami | group | Fab, we are on for the governors meeting as planned!\n2026-06-21 | Elif | Kai | Provided the summer fete happens, I'll return the borrowed trestle tables by 23 Jun 2026.\n2026-06-25 | Jonas | Kai | Quick update: you do not need to count the donation boxes at all.\n2026-06-28 | Kai | Elif | Guess what, I managed to count the donation boxes!",
  "question": "Is it true under the card's rules that Kai has kept the promise to count the donation boxes at the end of 26 Jun 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb819f2ff8f",
  "kind": "choice",
  "text": "Volunteers, here is the junior section thread that Lena forwarded for us.\n\nMembers: Ivo, Omar, Zara, Lena\nChat log (oldest first):\n[16 Feb 2026] Ivo: @Zara I'll wash the away kit by Monday, 23 February 2026 if the presentation evening goes ahead.\n[21 Feb 2026] Ivo: @Zara Count on me to pump the match balls by Sunday, 1 March 2026.\n[21 Feb 2026] Ivo: @Zara Sorry, I won't pump the match balls after all\n[21 Feb 2026] Ivo: Please note the presentation evening will proceed.\n[23 Feb 2026] Ivo: @Zara Is Wednesday, 25 February 2026 alright for me to wash the away kit?\n[23 Feb 2026] Zara: @Ivo Yes, you can wash the away kit by Wednesday, 25 February 2026 if that suits you.\n[28 Feb 2026] Ivo: @Zara Got myself to wash the away kit lol.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Ivo supposed to wash the away kit by, going by the chat at the end of Thursday, 26 February 2026 and any agreed changes?",
  "options": [
   "Monday, 23 February 2026",
   "Sunday, 1 March 2026",
   "Wednesday, 25 February 2026"
  ]
 },
 {
  "qid": "qedcd725bba",
  "kind": "yes/no",
  "text": "Exported by Tess, this is the full back and forth on the honeymoon album.\n\nMembers: Tess, Kai, Jonas\nChat log (oldest first):\n[11 Mar 2026] Kai: @Jonas You can bank on me to pick up the album prints by 17 March 2026.\n[15 Mar 2026] Kai: @Jonas Mate, I promised, may I pick up the album prints by 23 March 2026 instead?\n[15 Mar 2026] Kai: @Jonas If the rehearsal dinner is on, I'll definitely book the assistant photographer by 24 March 2026.\n[16 Mar 2026] Tess: @Kai Yes, happy for you to pick up the album prints by 23 March 2026 instead.\n[21 Mar 2026] Jonas: Sadly, the rehearsal dinner is not going ahead.",
  "question": "Is the promise Kai made to pick up the album prints in a status other than broken at the end of 22 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8a6aeb2856",
  "kind": "choice",
  "text": "Team channel: the platform rewrite\nShared by Lee.\n\nMembers: Lee, Leila, Kofi, Zara\nChat log (oldest first):\n[4 Mar 2026] Kofi: @Zara Count on me, I'll deploy the staging build by 8 Mar 2026.\n[4 Mar 2026] Kofi: @Zara Got it, I'll restart the build server by 10 Mar 2026 for sure.\n[5 Mar 2026] Lee: @Kofi No worries, you don't need to restart the build server\n[6 Mar 2026] Lee: @Kofi Quick update: you do not need to deploy the staging build at all.\n[7 Mar 2026] Kofi: @Zara Provided the code freeze happens, I will review the pull request by 11 Mar 2026.\n[9 Mar 2026] Zara: Just so you know, the code freeze is on as scheduled.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Kofi made to review the pull request is in which status at the end of 15 Mar 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Broken",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "qa312ee2777",
  "kind": "yes/no",
  "text": "Bruno forwarded this support chat about the new kit design.\n\nMembers: Bruno, Oskar, Kai\nChat log (oldest first):\n[24 Feb 2026] Bruno: @Oskar I promise to service the tandem bike by March 5, 2026.\n[24 Feb 2026] Kai: @Bruno Lovely, I'll return the loaned helmets by March 2, 2026 if the bike check is on.\n[27 Feb 2026] Kai: @Bruno Quick update: you do not need to service the tandem bike at all.\n[27 Feb 2026] Kai: Great news, the bike check is on!\n[1 Mar 2026] Oskar: @Kai Relax, mate, you're not expected to return the loaned helmets",
  "question": "Has Kai not kept the promise to return the loaned helmets at the end of March 3, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4b2d0cabaa",
  "kind": "choice",
  "text": "Parents and cousins, this is where we sort out the trip itinerary. Saved by Omar.\n\nMembers: Elif, Omar, Dara\nChat export (date | from | to | message):\n2026-09-13 | Dara | Elif | Relax, I'll buy the packing cubes by 22 September 2026, promise.\n2026-09-15 | Dara | Omar | I'll fetch the sunscreen by 18 September 2026 if the guided tour goes ahead.\n2026-09-16 | Elif | group | Really pleased to say the guided tour will go ahead!\n2026-09-17 | Omar | Dara | Forget it, you won't need to buy the packing cubes\n2026-09-19 | Omar | Dara | You can bet I'll check the passport copies by 28 September 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Dara's commitment to fetch the sunscreen at the end of 17 September 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "qe0787d2783",
  "kind": "yes/no",
  "text": "Attached chat: the annual tour\nForwarded by: Elif\n\nMembers: Greta, Elif, Leila\nChat log (oldest first):\n[19 Feb 2026] Greta: @Leila Promise to wash the club jerseys by 2026-02-27 if the hill climb goes ahead.\n[19 Feb 2026] Elif: @Greta I assure you I'll stock the energy gels by 2026-02-27 if the club sportive is on.\n[22 Feb 2026] Greta: @Elif I promise to fetch the bike stand by 2026-02-26.\n[26 Feb 2026] Greta: @Elif Scratch that, I'm not going to fetch the bike stand\n[26 Feb 2026] Greta: @Leila Count on me, I'll service the tandem bike by 2026-03-05.",
  "question": "Does the card's rule set show that Greta has not kept the promise to fetch the bike stand at the end of 2026-03-02?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe20613e517",
  "kind": "yes/no",
  "text": "Exported by Jonas, this is the full back and forth on the sound mix.\n\nMembers: Jonas, Tomas, Kofi\nChat export (date | from | to | message):\n2026-05-03 | Kofi | group | Hoping to fetch the raw footage by May 14, 2026, no promises.\n2026-05-05 | Kofi | Jonas | It's on me to fetch the raw footage by May 11, 2026.\n2026-05-05 | Tomas | Kofi | Quick update: you do not need to fetch the raw footage at all.\n2026-05-06 | Tomas | Kofi | Count on me, I'll export the subtitle files by May 9, 2026.\n2026-05-09 | Jonas | Tomas | I promise to upload the render files by May 17, 2026 if the client screening is on.\n2026-05-14 | Jonas | group | Please note the client screening will proceed.",
  "question": "At the end of May 13, 2026, does the promise Kofi made to fetch the raw footage have any status except broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q97e60e2664",
  "kind": "choice",
  "text": "Committee chat on the new kit design, forwarded by Greta to the volunteers.\n\nMembers: Dara, Greta, Yuki\nChat log (oldest first):\n[5 Feb 2026] Greta: @Yuki Count on me to tune the gear cables by 13 February 2026 if the mechanics clinic is on.\n[11 Feb 2026] Yuki: Update: the mechanics clinic is going ahead as planned.\n[11 Feb 2026] Greta: @Yuki Would it be fine if I tune the gear cables by 16 February 2026 instead, yeah?\n[11 Feb 2026] Yuki: @Greta I will make sure to pump the spare tyres by 17 February 2026.\n[12 Feb 2026] Yuki: @Greta Go ahead and tune the gear cables by 16 February 2026, that is fine.\n[13 Feb 2026] Dara: @Greta No worries, you don't need to tune the gear cables\n[16 Feb 2026] Greta: @Yuki Guess what, I managed to tune the gear cables!",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Greta to tune the gear cables at the end of 15 February 2026, counting any agreed change of date?",
  "options": [
   "16 February 2026",
   "13 February 2026",
   "17 February 2026"
  ]
 },
 {
  "qid": "q223c472c14",
  "kind": "choice",
  "text": "Chat attached to a support case about the spring campaign, shared by Elif.\n\nMembers: Elif, Tess, Ana, Leila\nChat export (date | from | to | message):\n2026-05-09 | Ana | Leila | Committing to print the event banners by 18 May 2026.\n2026-05-11 | Leila | Tess | I'll fix the landing page headline by 20 May 2026 if the brand photo shoot goes ahead.\n2026-05-12 | Ana | Leila | Got myself to print the event banners lol.\n2026-05-13 | Tess | group | Afraid the brand photo shoot is called off.\n2026-05-14 | Tess | group | I'll try to collect the survey answers by 24 May 2026.\n2026-05-15 | Tess | Elif | Guaranteed I'll collect the survey answers by 23 May 2026.\n2026-05-15 | Tess | Elif | Is 29 May 2026 alright for me to collect the survey answers?\n2026-05-26 | Tess | Elif | To note: I have managed to collect the survey answers",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of 22 May 2026, what is the date by which Tess has to collect the survey answers, counting any agreed change?",
  "options": [
   "29 May 2026",
   "20 May 2026",
   "23 May 2026"
  ]
 },
 {
  "qid": "q34da38326f",
  "kind": "choice",
  "text": "Client thread on the rebrand package, saved by Lena for the project log.\n\nMembers: Malik, Lena, Rhea, Yuki\nChat log (oldest first):\n[3 Nov 2026] Rhea: @Yuki Ticket's mine, I'll mail the business cards by 9 Nov 2026.\n[5 Nov 2026] Malik: @Rhea Count on me to collect the photo credits by 11 Nov 2026, if the print run happens.\n[8 Nov 2026] Malik: Really pleased to say the print run will go ahead!\n[9 Nov 2026] Lena: @Rhea Good news, you're let off having to mail the business cards\n[9 Nov 2026] Rhea: @Yuki Guess what, I managed to mail the business cards!",
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
  "qid": "q3bfa7036bb",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the garden makeover\nFrom Dara, the thread below is shared as it stands.\n\nMembers: Bruno, Dara, Mo, Tomas\nChat export (date | from | to | message):\n2026-07-03 | Bruno | Dara | Count on me to hang the new curtain rail by 10 Jul 2026, if the builder quote meeting happens.\n2026-07-07 | Mo | Tomas | Committing to pick up the grout bag by 11 Jul 2026.\n2026-07-08 | Mo | group | Brilliant news everyone, the builder quote meeting is a go!\n2026-07-08 | Bruno | Dara | Would it be fine if I hang the new curtain rail by 16 Jul 2026 instead, yeah?\n2026-07-08 | Dara | Bruno | Not moving it, hang the new curtain rail by the existing date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Bruno's promise to hang the new curtain rail stand at the end of 10 Jul 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not triggered",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q70699c6c01",
  "kind": "choice",
  "text": "Forwarded by Kofi, these tenant replies are about the guest review drive for the file.\n\nMembers: Nadia, Ana, Ivo, Kofi\nChat log (oldest first):\n[3 Mar 2026] Ana: @Ivo Provided the lettings photo shoot happens, I'll vacuum the holiday cottage by Saturday, March 7, 2026.\n[4 Mar 2026] Ivo: Yay, the lettings photo shoot is all set to go!\n[5 Mar 2026] Ana: @Kofi Committing to air the spare room by Sunday, March 8, 2026.\n[7 Mar 2026] Ana: Not promising, but I'll try to change the lounge bulb by Wednesday, March 11, 2026.\n[9 Mar 2026] Ana: @Ivo You can bet I'll change the lounge bulb by Thursday, March 12, 2026.\n[11 Mar 2026] Ana: @Ivo Mind giving me until Saturday, March 14, 2026 to change the lounge bulb?\n[11 Mar 2026] Nadia: @Ana Yes, you're welcome to change the lounge bulb by Saturday, March 14, 2026 instead.\n[15 Mar 2026] Ana: @Ivo To note: I have managed to change the lounge bulb",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen does Ana have to change the lounge bulb by, at the end of Tuesday, March 24, 2026, once any agreed date change is included?",
  "options": [
   "Thursday, March 12, 2026",
   "Saturday, March 14, 2026",
   "Sunday, March 8, 2026"
  ]
 },
 {
  "qid": "q79ca87286a",
  "kind": "choice",
  "text": "Mo saved this exchange with the client about the big day.\n\nMembers: Hana, Omar, Mo, Tess\nChat log (oldest first):\n[30 Sep 2026] Mo: @Tess I'll try to charge the flash batteries by 3 Oct 2026.\n[1 Oct 2026] Mo: @Hana Committing to charge the flash batteries by 7 Oct 2026.\n[2 Oct 2026] Mo: @Hana Mind giving me until 11 Oct 2026 to charge the flash batteries?\n[4 Oct 2026] Tess: @Mo Yes, happy for you to charge the flash batteries by 11 Oct 2026 instead.\n[5 Oct 2026] Mo: @Omar If the ceremony walkthrough goes ahead, I'll gladly send the sneak peek gallery by 9 Oct 2026.\n[6 Oct 2026] Omar: @Mo Quick update: you do not need to charge the flash batteries at all.\n[8 Oct 2026] Mo: Sadly, the ceremony walkthrough won't go ahead.\n[10 Oct 2026] Mo: @Hana Got myself to charge the flash batteries lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Mo supposed to charge the flash batteries by, going by the chat at the end of 6 Oct 2026 and any agreed changes?",
  "options": [
   "11 Oct 2026",
   "7 Oct 2026",
   "9 Oct 2026"
  ]
 },
 {
  "qid": "qd8052ed3a3",
  "kind": "choice",
  "text": "Omar forwarded these replies from the agent on the attic conversion idea for the file.\n\nMembers: Leila, Ivo, Omar\nChat export (date | from | to | message):\n2026-04-02 | Ivo | Omar | I assure you I'll buy the washing powder by 10 April 2026 if the house insurance review is on.\n2026-04-04 | Ivo | Omar | Quick question, could I buy the washing powder by 13 April 2026 instead?\n2026-04-04 | Omar | Ivo | We are holding the date on record, so buy the washing powder by it.\n2026-04-05 | Omar | Leila | Ticket's mine, I'll sort the recycling bags by 11 April 2026.\n2026-04-07 | Leila | Ivo | I assure you I'll feed the house plants by 11 April 2026 if the lodger house supper is on.\n2026-04-09 | Ivo | group | Brilliant news everyone, the house insurance review is a go!",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Ivo gave to buy the washing powder have at the end of 5 April 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Waived",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "qb46af51a47",
  "kind": "yes/no",
  "text": "Shared by Mo, this back and forth with the client covers the online store move.\n\nMembers: Ivo, Nadia, Mo, Bruno\nChat log (oldest first):\n[24 Jul 2026] Mo: @Ivo If the pop up stall is on, I'll definitely add the size chart by Sunday, July 26, 2026.\n[25 Jul 2026] Ivo: Afraid the pop up stall is called off.\n[27 Jul 2026] Bruno: @Ivo You can bank on me to send the stock spreadsheet by Sunday, August 2, 2026.\n[31 Jul 2026] Bruno: @Ivo Might I ask whether I could send the stock spreadsheet by Wednesday, August 5, 2026 instead?\n[1 Aug 2026] Ivo: Quick check, any update on plans to send the stock spreadsheet?\n[2 Aug 2026] Bruno: @Ivo Ticked off my list: send the stock spreadsheet, yay.",
  "question": "Going by the card's rules, does Bruno not keep the promise to send the stock spreadsheet at the end of Thursday, August 6, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qcd09e0c6d3",
  "kind": "choice",
  "text": "Forwarded by Omar, these tenant replies are about the cottage refresh for the file.\n\nMembers: Femi, Greta, Lena, Omar\nChat log (oldest first):\n[6 Apr 2026] Omar: @Greta Promise to vacuum the holiday cottage by 14 Apr 2026 if the lettings photo shoot goes ahead.\n[7 Apr 2026] Greta: @Omar You can bet I'll leave the welcome basket by 13 Apr 2026.\n[7 Apr 2026] Femi: @Greta Good news, you're let off having to leave the welcome basket\n[8 Apr 2026] Greta: @Omar Ticked off: leave the welcome basket, feels so good\n[13 Apr 2026] Lena: Sad to report that the lettings photo shoot is off.",
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
  "qid": "q02881f3539",
  "kind": "yes/no",
  "text": "Kofi forwarded this for the committee as we dig in on the volunteer roster.\n\nMembers: Leila, Jonas, Bruno, Kofi\nChat export (date | from | to | message):\n2026-02-18 | Jonas | Bruno | Provided the clothes swap happens, I'll wrap the prize hampers by 21 February 2026.\n2026-02-19 | Jonas | group | On track for the clothes swap to happen as planned.\n2026-02-20 | Jonas | Kofi | I will print the raffle tickets by 27 February 2026.\n2026-02-21 | Jonas | Bruno | Got myself to wrap the prize hampers lol.\n2026-02-23 | Bruno | Jonas | Please don't feel you have to print the raffle tickets",
  "question": "Would you say Jonas didn't keep the promise to wrap the prize hampers by the end of 21 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q91aa929f98",
  "kind": "choice",
  "text": "Oskar saved this so we stay on the same page about the student house hunt, mates.\n\nMembers: Nadia, Oskar, Yuki\nChat log (oldest first):\n[25 Sep 2026] Nadia: @Yuki Guaranteed I'll forward the inventory photos by Tuesday, 29 September 2026.\n[25 Sep 2026] Yuki: Cheers, noted.\n[25 Sep 2026] Nadia: @Oskar Count on me to store the spare bike by Friday, 2 October 2026, if the house hunting viewing happens.\n[27 Sep 2026] Nadia: @Yuki Is it all right if I forward the inventory photos by Saturday, 3 October 2026 instead?\n[27 Sep 2026] Oskar: @Nadia I'll photograph the bathroom mould by Thursday, 1 October 2026, promise.\n[28 Sep 2026] Oskar: @Nadia Of course, it is fine for you to forward the inventory photos by Saturday, 3 October 2026.\n[28 Sep 2026] Nadia: @Yuki I will print the tenancy agreement by Thursday, 1 October 2026 only if the gas safety inspection happens.\n[3 Oct 2026] Nadia: @Yuki To my relief, I managed to forward the inventory photos.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat's the day Nadia needs to forward the inventory photos by at the end of Sunday, 11 October 2026, after any new date the group agreed on?",
  "options": [
   "Saturday, 3 October 2026",
   "Tuesday, 29 September 2026",
   "Friday, 2 October 2026"
  ]
 },
 {
  "qid": "q3862418e34",
  "kind": "choice",
  "text": "Shared by Kai, this is where the loft conversion gets planned.\n\nMembers: Ana, Kai, Bruno, Tess\nChat export (date | from | to | message):\n2026-01-13 | Bruno | Tess | Count on me, I'll measure the hallway for shelves by 19 Jan 2026.\n2026-01-17 | Bruno | Tess | Is 25 Jan 2026 alright for me to measure the hallway for shelves?\n2026-01-18 | Tess | Bruno | Go ahead and measure the hallway for shelves by 25 Jan 2026, that is fine.\n2026-01-18 | Kai | Bruno | Quick update: you do not need to measure the hallway for shelves at all.\n2026-01-19 | Ana | Tess | Provided the kitchen fitting day happens, I'll pick up the grout bag by 27 Jan 2026.\n2026-01-23 | Tess | group | Update: the kitchen fitting day is going ahead as planned.\n2026-01-24 | Ana | Bruno | I'll hang the new curtain rail by 27 Jan 2026, promise.\n2026-01-24 | Kai | Ana | Forget it, you won't need to hang the new curtain rail",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 31 Jan 2026, by what date does Bruno have to measure the hallway for shelves, counting any agreed change of date?",
  "options": [
   "27 Jan 2026",
   "25 Jan 2026",
   "19 Jan 2026"
  ]
 },
 {
  "qid": "qbb6d959729",
  "kind": "choice",
  "text": "Team channel: the spring campaign\nShared by: Kofi.\n\nMembers: Kofi, Kai, Lee\nChat export (date | from | to | message):\n2026-08-09 | Lee | Kofi | Provided the annual review happens, I'll draft the press release by August 14, 2026.\n2026-08-09 | Kai | Kofi | You can bank on me to collect the survey answers by August 16, 2026.\n2026-08-12 | Lee | Kai | Count on me to fix the landing page headline by August 17, 2026 if the webinar rehearsal is on.\n2026-08-13 | Kai | group | Afraid the webinar rehearsal is called off.\n2026-08-14 | Kai | Kofi | Is it all right if I collect the survey answers by August 18, 2026 instead?\n2026-08-14 | Kofi | Kai | Not moving it, collect the survey answers by the existing date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Lee made to fix the landing page headline at the end of August 16, 2026?",
  "options": [
   "Waived",
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q97c3a21033",
  "kind": "choice",
  "text": "Casual chat for the flat, saved by Dara, and it covers the cellar project.\n\nMembers: Dara, Tomas\nChat log (oldest first):\n[26 May 2026] Dara: @Tomas Provided the ghost tour happens, I will clear the kitchen sink by 28 May 2026.\n[26 May 2026] Dara: @Tomas Guaranteed I'll tidy the boot room by 30 May 2026.\n[27 May 2026] Dara: Afraid the ghost tour is called off.\n[27 May 2026] Dara: @Tomas Is it all right if I tidy the boot room by 4 Jun 2026 instead?\n[30 May 2026] Dara: @Tomas For the record: I was able to tidy the boot room",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Dara's promise to tidy the boot room at the end of 30 May 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Broken",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q562695afdf",
  "kind": "yes/no",
  "text": "Messages with the letting agent about the guest welcome plan, saved by Lena for the rental file.\n\nMembers: Zara, Jonas, Tess, Lena\nChat log (oldest first):\n[19 Apr 2026] Lena: @Tess Relax, I'll leave the welcome basket by Tuesday, 21 April 2026 for sure.\n[19 Apr 2026] Zara: @Lena Lovely, I'll collect the bed linen by Tuesday, 21 April 2026 if the owner handover visit is on.\n[22 Apr 2026] Lena: @Zara Provided the guest arrival evening happens, I will vacuum the holiday cottage by Tuesday, 28 April 2026.\n[24 Apr 2026] Jonas: @Lena Guaranteed I'll air the spare room by Saturday, 2 May 2026.\n[25 Apr 2026] Jonas: @Lena Ticked off: air the spare room, feels so good\n[25 Apr 2026] Zara: Any idea how close you are to air the spare room?",
  "question": "Does the card classify Jonas's promise to air the spare room as broken, waived, not triggered or not yet due, rather than kept, on Saturday, 25 April 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q640979b0d3",
  "kind": "choice",
  "text": "Lee forwarded this for the committee, covering the sponsor search.\n\nMembers: Mo, Malik, Bruno, Lee\nChat log (oldest first):\n[26 Jan 2026] Lee: @Bruno I'll collect the timing tags by 4 Feb 2026 as long as the club sportive is on.\n[27 Jan 2026] Malik: @Lee Ticket's mine, I'll tune the gear cables by 30 Jan 2026.\n[29 Jan 2026] Mo: @Bruno You can bank on me to wash the club jerseys by 5 Feb 2026.\n[1 Feb 2026] Mo: @Bruno Mum, I did wash the club jerseys, haha.\n[1 Feb 2026] Lee: Update, the club sportive will not take place.\n[2 Feb 2026] Bruno: How's the plan to wash the club jerseys?",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Mo's undertaking to wash the club jerseys hold at the end of 2 Feb 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Not yet due",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q7941e2f40f",
  "kind": "choice",
  "text": "Leila forwarded this for the committee as we dig in on the choir tour.\n\nMembers: Leila, Mo, Malik, Omar\nChat log (oldest first):\n[15 Apr 2026] Omar: @Malik See if I can set up the sound desk by 25 April 2026, no certainty.\n[16 Apr 2026] Omar: @Leila I will set up the sound desk by 22 April 2026.\n[22 Apr 2026] Omar: @Leila Mind giving me until 25 April 2026 to set up the sound desk?\n[22 Apr 2026] Leila: @Omar Revised deadline is 25 April 2026, so you can set up the sound desk.\n[24 Apr 2026] Mo: @Malik As long as the summer recital is on, I will move the piano by 26 April 2026.\n[25 Apr 2026] Malik: @Omar No need to set up the sound desk, I'm letting you off\n[25 Apr 2026] Mo: Sorry, the summer recital is off.\n[28 Apr 2026] Omar: @Leila For the record: I was able to set up the sound desk",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Omar supposed to set up the sound desk by, going by the chat at the end of 24 April 2026 and any agreed changes?",
  "options": [
   "25 April 2026",
   "26 April 2026",
   "22 April 2026"
  ]
 },
 {
  "qid": "q4635b61ae2",
  "kind": "choice",
  "text": "Kai shared this channel export, covering the staff handbook for the team.\n\nMembers: Ines, Kai, Oskar\nChat log (oldest first):\n[8 Jul 2026] Ines: @Oskar As long as the coffee morning is on, I will fetch the parking permits by Thursday, July 16, 2026.\n[12 Jul 2026] Oskar: @Kai I will make sure to print the staff rota by Saturday, July 18, 2026.\n[12 Jul 2026] Kai: Cheers, noted.\n[13 Jul 2026] Ines: @Kai I will make sure to return the printer toner by Wednesday, July 15, 2026.\n[13 Jul 2026] Oskar: Sorry, the coffee morning is off.\n[19 Jul 2026] Oskar: @Kai Quick report: I've managed to print the staff rota",
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
  "qid": "q93865372a4",
  "kind": "yes/no",
  "text": "Here is the thread on the garden shed build, posted by Kofi for the house.\n\nMembers: Kofi, Kai, Jonas, Sami\nChat log (oldest first):\n[6 Mar 2026] Kofi: @Jonas Promise to dig the potato patch by 10 March 2026 if the water tank delivery goes ahead.\n[7 Mar 2026] Kofi: @Jonas I promise to weed the carrot row by 12 March 2026.\n[7 Mar 2026] Kofi: @Jonas Log entry: weed the carrot row, carried out\n[8 Mar 2026] Jonas: Team, the water tank delivery stays on as booked.\n[9 Mar 2026] Kofi: @Jonas Any chance I can dig the potato patch by 13 March 2026 instead?",
  "question": "Applying the card's rules, can it be said that Kofi has not kept the promise to dig the potato patch at the end of 10 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
