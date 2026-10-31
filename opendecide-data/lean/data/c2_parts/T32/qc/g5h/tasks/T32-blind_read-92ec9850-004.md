# G5-H blind read (all free-form rows) T32-blind_read-92ec9850-004 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T32/qc/g5h/answers/T32-blind_read-92ec9850-004.json

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
  "qid": "q330328ec25",
  "kind": "yes/no",
  "text": "Kai shared this support thread, which is about the new term plans.\n\nMembers: Arlo, Kai, Zara\nChat export (date | from | to | message):\n2026-05-04 | Arlo | Kai | If the clothes swap is on, I'll definitely set up the book stall by 12 May 2026.\n2026-05-04 | Zara | Arlo | Relax, I'll label the raffle prizes by 11 May 2026 for sure.\n2026-05-06 | Zara | Kai | It's on me to print the raffle tickets by 15 May 2026.\n2026-05-09 | Zara | Arlo | I'll wrap the prize hampers by 18 May 2026 as long as the governors meeting is on.\n2026-05-10 | Zara | Arlo | Sorry, I won't label the raffle prizes after all",
  "question": "Did Zara keep the promise to label the raffle prizes on 12 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qad395e5142",
  "kind": "choice",
  "text": "Client thread on the showreel refresh, saved by Ana for the project log.\n\nMembers: Greta, Ravi, Ana\nChat export (date | from | to | message):\n2026-01-21 | Greta | Ana | Relax, I'll order the stock music licence by Friday, 23 January 2026, promise.\n2026-01-22 | Greta | Ana | If the festival premiere is on, I'll definitely label the clip folders by Thursday, 29 January 2026.\n2026-01-24 | Greta | Ana | To my relief, I managed to order the stock music licence.\n2026-01-25 | Greta | Ana | I'll upload the render files by Saturday, 31 January 2026, promise.\n2026-01-27 | Ana | group | Brilliant news everyone, the festival premiere is a go!\n2026-01-27 | Ana | Ravi | Guaranteed I'll record the voice over by Monday, 2 February 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Greta's promise to label the clip folders at the end of Saturday, 31 January 2026?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "qbf95509a8a",
  "kind": "choice",
  "text": "Team channel: the trade show push\nExported by Dara.\n\nMembers: Kofi, Greta, Mo, Dara\nChat export (date | from | to | message):\n2026-04-16 | Dara | Greta | You can bet I'll fetch the campaign budget sheet by Thursday, April 23, 2026.\n2026-04-17 | Greta | Dara | Got it, I'll draft the press release by Wednesday, April 22, 2026 for sure.\n2026-04-18 | Mo | Kofi | I will return the rented camera gear by Saturday, April 25, 2026 only if the annual review happens.\n2026-04-19 | Greta | Dara | Correction, I will not be able to draft the press release.\n2026-04-21 | Kofi | group | Afraid the annual review is called off.\n2026-04-22 | Kofi | Dara | Forget it, you won't need to fetch the campaign budget sheet",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Dara's commitment to fetch the campaign budget sheet at the end of Thursday, April 23, 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q46b6c7141b",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the care plan\nThis export from Ivo is pasted in full for readers who want it.\n\nMembers: Kofi, Nadia, Ana, Ivo\nChat export (date | from | to | message):\n2026-07-11 | Ivo | Ana | I assure you I'll call the home nurse by 14 July 2026 if the carer handover is on.\n2026-07-13 | Ivo | group | Really pleased to say the carer handover will go ahead!\n2026-07-14 | Kofi | Ivo | You can bank on me to collect the post by 22 July 2026.\n2026-07-14 | Ivo | Ana | I need to take back my commitment to call the home nurse.\n2026-07-16 | Nadia | Ivo | If the physio session goes ahead, I'll gladly pick up the repeat prescription by 19 July 2026.\n2026-07-20 | Kofi | Ivo | Guess what, I managed to collect the post!",
  "question": "Did Ivo break the promise to call the home nurse at the end of 15 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q47a27d90b3",
  "kind": "yes/no",
  "text": "We have been planning the old house restoration here, shared by Kofi.\n\nMembers: Dara, Kofi, Tess, Bruno\nChat log (oldest first):\n[1 May 2026] Dara: @Tess I promise to tidy the boot room by 5 May 2026 if the ghost tour is on.\n[2 May 2026] Tess: Really pleased to say the ghost tour will go ahead!\n[3 May 2026] Tess: @Dara Got it, I'll bleed the attic radiators by 8 May 2026 for sure.\n[3 May 2026] Kofi: @Dara Quick update: you do not need to tidy the boot room at all.\n[8 May 2026] Tess: Did you manage to tidy the boot room?\n[8 May 2026] Dara: @Tess Guess what, I managed to tidy the boot room!",
  "question": "Applying the card's rules, does Dara's promise to tidy the boot room count as broken, waived, not triggered or not yet due, rather than kept, as of 7 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf63ca69863",
  "kind": "choice",
  "text": "Volunteers, here is the choir tour chat that Rhea forwarded to us.\n\nMembers: Zara, Oskar, Omar, Rhea\nChat log (oldest first):\n[5 Sep 2026] Omar: Fingers crossed I can collect the sheet music by 15 Sep 2026.\n[7 Sep 2026] Omar: @Zara I'll collect the sheet music by 14 Sep 2026 as long as the carol concert is on.\n[8 Sep 2026] Zara: Please note the carol concert will proceed.\n[13 Sep 2026] Omar: @Zara Might I ask whether I could collect the sheet music by 20 Sep 2026 instead?\n[14 Sep 2026] Zara: @Omar Yes, you're welcome to collect the sheet music by 20 Sep 2026 instead.\n[16 Sep 2026] Rhea: @Omar Ah, no stress, no need for you to collect the sheet music\n[19 Sep 2026] Zara: @Rhea Committing to send the audition reminders by 23 Sep 2026.\n[22 Sep 2026] Rhea: @Oskar I promise to buy the spare folders by 25 Sep 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Omar to collect the sheet music at the end of 30 Sep 2026, counting any agreed change of date?",
  "options": [
   "23 Sep 2026",
   "20 Sep 2026",
   "14 Sep 2026"
  ]
 },
 {
  "qid": "qebc069763c",
  "kind": "choice",
  "text": "Zara saved these exchanges with the agent about the summer lets season.\n\nMembers: Mo, Zara, Omar, Lena\nChat log (oldest first):\n[1 Jul 2026] Omar: @Lena Provided the guest arrival evening happens, I will collect the bed linen by 2026-07-04.\n[3 Jul 2026] Zara: @Lena I'll be sure to wash the beach towels by 2026-07-07.\n[5 Jul 2026] Zara: @Omar Only if the summer season launch is on, I will leave the welcome basket by 2026-07-08.\n[6 Jul 2026] Zara: @Lena I'll be sure to wheel the bins out by 2026-07-12.\n[11 Jul 2026] Zara: @Lena I regret to say that I shall not wheel the bins out.\n[12 Jul 2026] Mo: @Zara Good news, you're let off having to wheel the bins out",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Zara's promise to wheel the bins out have at the end of 2026-07-13?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q5a4e476fa7",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the platform rewrite\nThe chat below comes from Arlo, copied as is for reference.\n\nMembers: Arlo, Ines, Omar, Rhea\nChat log (oldest first):\n[26 Mar 2026] Rhea: @Arlo Count on me, I'll label the bug reports by 29 Mar 2026.\n[28 Mar 2026] Arlo: @Ines Got it, I'll deploy the staging build by 31 Mar 2026 for sure.\n[29 Mar 2026] Omar: @Rhea If the sprint demo goes ahead, I'll gladly rotate the test keys by 4 Apr 2026.\n[29 Mar 2026] Rhea: @Arlo Guess who managed to label the bug reports, go team!\n[1 Apr 2026] Arlo: @Ines For the record: I was able to deploy the staging build\n[3 Apr 2026] Ines: Scrapping the sprint demo, apologies to all.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Rhea's promise to label the bug reports at the end of 1 Apr 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q50db4d0d8d",
  "kind": "yes/no",
  "text": "Oskar forwarded this exchange with the landlord on the spare room plan.\n\nMembers: Femi, Arlo, Oskar\nChat export (date | from | to | message):\n2026-04-15 | Femi | Arlo | Provided the landlord inspection walk happens, I will turn the heating timer by 2026-04-20.\n2026-04-17 | Oskar | Femi | If the fuse box inspection goes ahead, I'll gladly feed the house plants by 2026-04-23.\n2026-04-17 | Arlo | group | Really pleased to say the fuse box inspection will go ahead!\n2026-04-18 | Oskar | Femi | Quick report: I've managed to feed the house plants\n2026-04-20 | Oskar | Arlo | I'll be sure to sort the recycling bags by 2026-04-25.\n2026-04-25 | Arlo | Oskar | Don't sweat it, there's no need to sort the recycling bags",
  "question": "Does Oskar's promise to feed the house plants hold up as kept at the end of 2026-04-18, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qba9168339d",
  "kind": "yes/no",
  "text": "Volunteers, here is the choir tour thread that Lena forwarded for us.\n\nMembers: Malik, Rhea, Dara, Lena\nChat log (oldest first):\n[21 May 2026] Rhea: @Dara If the sing along is on, I'll definitely book the rehearsal room by 23 May 2026.\n[21 May 2026] Rhea: @Dara You can bet I'll set up the sound desk by 26 May 2026.\n[22 May 2026] Malik: Sorry all, the sing along is called off.\n[23 May 2026] Rhea: @Dara Quick question, could I set up the sound desk by 31 May 2026 instead?\n[26 May 2026] Dara: @Rhea Of course, it is fine for you to set up the sound desk by 31 May 2026.\n[31 May 2026] Rhea: @Dara To my relief, I managed to set up the sound desk.",
  "question": "At the end of 5 June 2026, is Rhea's promise to set up the sound desk broken, waived, not triggered or not yet due, rather than kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb5375aad2e",
  "kind": "choice",
  "text": "Shared by Zara, a help-desk thread covering the family day out.\n\nMembers: Yuki, Oskar, Zara\nChat log (oldest first):\n[17 Sep 2026] Zara: @Oskar Count on me to tidy the playroom by 20 Sep 2026.\n[18 Sep 2026] Oskar: @Yuki Count on me to fetch the craft box by 24 Sep 2026, if the storytime session happens.\n[22 Sep 2026] Zara: Really pleased to say the storytime session will go ahead!\n[24 Sep 2026] Oskar: @Yuki Might I ask whether I could fetch the craft box by 29 Sep 2026 instead?\n[24 Sep 2026] Oskar: @Yuki Mum, I did fetch the craft box, haha.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Oskar made to fetch the craft box at the end of 26 Sep 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Waived",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q233281bb90",
  "kind": "yes/no",
  "text": "Client thread on the sound mix, shared by Nadia for the project log.\n\nMembers: Nadia, Lee, Rhea\nChat export (date | from | to | message):\n2026-09-01 | Lee | Rhea | Guaranteed I'll ship the hard drive by 4 September 2026.\n2026-09-03 | Nadia | Rhea | As long as the agency review call is on, I'll label the clip folders by 11 September 2026.\n2026-09-04 | Rhea | Nadia | Lovely, I'll record the voice over by 9 September 2026 for sure.\n2026-09-04 | Nadia | Rhea | Good news, you're let off having to record the voice over\n2026-09-07 | Nadia | group | Great news, the agency review call is on!\n2026-09-09 | Lee | Nadia | Count on me, I'll order the stock music licence by 12 September 2026.",
  "question": "Applying the card's rules, does Rhea's promise to record the voice over count as kept, rather than broken, waived, not triggered or not yet due, as of 8 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q15ff6094f8",
  "kind": "yes/no",
  "text": "Here is the thread on the cellar project, posted by Greta for the house.\n\nMembers: Nadia, Greta\nChat log (oldest first):\n[22 Mar 2026] Nadia: @Greta Relax, I'll scrub the cellar steps by 24 March 2026, promise.\n[22 Mar 2026] Nadia: @Greta Scratch what I said, I won't scrub the cellar steps.\n[25 Mar 2026] Greta: @Nadia I'll be sure to find the loft ladder by 1 April 2026.\n[25 Mar 2026] Greta: @Nadia I regret to say that I shall not find the loft ladder.\n[28 Mar 2026] Greta: @Nadia I assure you I'll oil the back door hinges by 31 March 2026 if the house viewing is on.\n[29 Mar 2026] Greta: Yep, the house viewing is on as planned.",
  "question": "Under the rules on the card, is the promise Greta made to find the loft ladder broken at the end of 26 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbfaa053175",
  "kind": "yes/no",
  "text": "Hana forwarded this for the committee as we dig in on the choir tour.\n\nMembers: Bruno, Hana, Jonas\nChat log (oldest first):\n[29 May 2026] Bruno: Might be able to fetch the choir robes by 10 June 2026, who knows!\n[31 May 2026] Bruno: @Hana You can bank on me to fetch the choir robes by 7 June 2026.\n[2 Jun 2026] Bruno: @Hana I own this, I'll fix the stand microphones by 8 June 2026.\n[3 Jun 2026] Bruno: @Hana Count on me to collect the sheet music by 11 June 2026, if the sing along happens.\n[6 Jun 2026] Bruno: @Hana Guess who managed to fetch the choir robes, go team!\n[10 Jun 2026] Jonas: Sadly, the sing along won't go ahead.",
  "question": "Would you say Bruno didn't keep the promise to fetch the choir robes by the end of 6 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe54b1fa828",
  "kind": "choice",
  "text": "Shared by Leila for the committee, this is the group chat on the training plan.\n\nMembers: Leila, Ana, Malik\nChat log (oldest first):\n[17 Aug 2026] Malik: @Leila Lovely, I'll pump the spare tyres by 20 Aug 2026 for sure.\n[21 Aug 2026] Leila: @Ana Promise to service the tandem bike by 24 Aug 2026 if the bike check goes ahead.\n[23 Aug 2026] Leila: Yep, the bike check is on as planned.\n[24 Aug 2026] Leila: @Ana Committing to fetch the bike stand by 1 Sep 2026.\n[25 Aug 2026] Leila: @Ana Guess who managed to service the tandem bike, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Leila's promise to service the tandem bike at the end of 24 Aug 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qdff4fab980",
  "kind": "yes/no",
  "text": "Shared by Leila for the committee, this is the group chat on the junior section.\n\nMembers: Ivo, Ana, Leila\nChat log (oldest first):\n[6 Jul 2026] Ana: @Leila Count on me to set up the corner flags by 15 Jul 2026.\n[9 Jul 2026] Ana: @Ivo Count on me to return the bib sets by 14 Jul 2026.\n[14 Jul 2026] Leila: @Ana As long as the cup tie is on, I will pump the match balls by 21 Jul 2026.\n[16 Jul 2026] Ana: @Ivo Mum, I did return the bib sets, haha.\n[17 Jul 2026] Ivo: Team, the cup tie is not happening.",
  "question": "At the end of 19 Jul 2026, has the promise Ana made to return the bib sets been broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5eaa864d77",
  "kind": "choice",
  "text": "Tenant and agent back-and-forth on the cottage refresh, forwarded by Mo.\n\nMembers: Mo, Ines, Greta, Kai\nChat log (oldest first):\n[19 Jan 2026] Ines: @Mo Promise to scrub the hot tub by 22 January 2026 if the lettings photo shoot goes ahead.\n[19 Jan 2026] Ines: @Greta I promise to wash the beach towels by 23 January 2026 if the guest arrival evening is on.\n[20 Jan 2026] Kai: Yep, the guest arrival evening is on as planned.\n[22 Jan 2026] Mo: @Greta Count on me to vacuum the holiday cottage by 31 January 2026.\n[23 Jan 2026] Greta: @Mo Committing to air the spare room by 27 January 2026.\n[23 Jan 2026] Greta: @Ines Relax, mate, you're not expected to wash the beach towels",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Ines's promise to wash the beach towels at the end of 23 January 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "qc7359db0a0",
  "kind": "choice",
  "text": "Kofi shared this support thread, which is about the showreel refresh.\n\nMembers: Dara, Kofi, Ivo, Priya\nChat export (date | from | to | message):\n2026-06-30 | Priya | Kofi | If the agency review call is on, I'll definitely ship the hard drive by 9 July 2026.\n2026-07-01 | Ivo | Kofi | Guaranteed I'll label the clip folders by 8 July 2026.\n2026-07-06 | Ivo | Kofi | Might I ask whether I could label the clip folders by 10 July 2026 instead?\n2026-07-06 | Priya | Ivo | Yes, you have the green light to label the clip folders by 10 July 2026.\n2026-07-06 | Priya | Ivo | No worries, you don't need to label the clip folders\n2026-07-07 | Dara | Ivo | Count on me to back up the project drives by 9 July 2026, if the grading session happens.\n2026-07-07 | Dara | Ivo | As long as the voiceover session is on, I'll send the colour notes by 9 July 2026.\n2026-07-16 | Ivo | Kofi | Log entry: label the clip folders, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat's the day Ivo needs to label the clip folders by at the end of 7 July 2026, after any new date the group agreed on?",
  "options": [
   "8 July 2026",
   "9 July 2026",
   "10 July 2026"
  ]
 },
 {
  "qid": "qfcf3b224c1",
  "kind": "choice",
  "text": "Volunteers, this is the junior section thread that Bruno shared with the committee.\n\nMembers: Bruno, Lee\nChat log (oldest first):\n[16 Jun 2026] Bruno: @Lee I'll wash the away kit by 23 Jun 2026, promise.\n[18 Jun 2026] Lee: @Bruno I'll mark the pitch lines by 21 Jun 2026 as long as the cup tie is on.\n[20 Jun 2026] Bruno: @Lee I promise to print the team sheets by 27 Jun 2026 if the training camp is on.\n[26 Jun 2026] Bruno: Sad to report that the training camp is off.\n[27 Jun 2026] Bruno: @Lee Would it be fine if I print the team sheets by 2 Jul 2026 instead, yeah?\n[27 Jun 2026] Lee: @Bruno No, you need to print the team sheets by the original date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 30 Jun 2026, what status has Bruno's promise to print the team sheets got?",
  "options": [
   "Not yet due",
   "Kept",
   "Not triggered",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q3be834d50d",
  "kind": "yes/no",
  "text": "Parents and cousins, this is where we sort out the allotment expansion. Saved by Dara.\n\nMembers: Hana, Yuki, Dara\nChat log (oldest first):\n[22 Oct 2026] Dara: @Yuki I'll be sure to collect the seed potatoes by Thursday, October 29, 2026.\n[23 Oct 2026] Dara: @Yuki Think Sunday, November 1, 2026 would work if I collect the seed potatoes instead?\n[24 Oct 2026] Hana: @Dara I will deliver the surplus runner beans by Saturday, October 31, 2026 only if the plot inspection happens.\n[25 Oct 2026] Dara: Sorry, the plot inspection is off.\n[25 Oct 2026] Yuki: @Hana Promise to stake the tomato canes by Tuesday, October 27, 2026 if the harvest supper goes ahead.\n[26 Oct 2026] Dara: @Yuki Quick report: I've managed to collect the seed potatoes",
  "question": "Would you say Dara didn't keep the promise to collect the seed potatoes by the end of Wednesday, October 28, 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd6e5b8a7a7",
  "kind": "yes/no",
  "text": "We have been planning the caring rota here, shared by Femi.\n\nMembers: Femi, Hana, Zara\nChat export (date | from | to | message):\n2026-06-23 | Zara | Hana | I'll fetch the mobility aids by 27 June 2026, provided the home assessment happens.\n2026-06-26 | Zara | group | Quick heads up, the home assessment is scrapped.\n2026-06-27 | Femi | Hana | I own this, I'll book the clinic transport by 4 July 2026.\n2026-06-27 | Hana | Zara | If the eye test is on, I'll definitely collect the post by 29 June 2026.\n2026-06-30 | Zara | Femi | No need to book the clinic transport, I'm letting you off\n2026-07-04 | Femi | Hana | Quick report: I've managed to book the clinic transport",
  "question": "Did Femi break the promise to book the clinic transport at the end of 5 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q59999ea81e",
  "kind": "yes/no",
  "text": "Subject: Chat about the choir tour\nThe copy from Femi follows below as a plain record.\n\nMembers: Mo, Rhea, Femi\nChat log (oldest first):\n[9 Sep 2026] Mo: I'll see if I can book the rehearsal room by 14 Sep 2026.\n[11 Sep 2026] Rhea: @Femi Lovely, I'll fetch the choir robes by 16 Sep 2026 if the sing along is on.\n[11 Sep 2026] Mo: @Rhea It's on me to book the rehearsal room by 15 Sep 2026.\n[12 Sep 2026] Mo: Fab, we are on for the sing along as planned!\n[15 Sep 2026] Femi: @Mo Ah, no stress, no need for you to book the rehearsal room\n[15 Sep 2026] Mo: @Rhea To note: I have managed to book the rehearsal room",
  "question": "Would you say Mo didn't keep the promise to book the rehearsal room by the end of 16 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q61952ceafa",
  "kind": "yes/no",
  "text": "Rhea forwarded this support chat, which is about the sponsor search.\n\nMembers: Greta, Elif, Rhea, Wren\nChat log (oldest first):\n[1 Apr 2026] Rhea: @Elif I'll collect the timing tags by 2026-04-09, promise.\n[1 Apr 2026] Rhea: @Elif I'm withdrawing my promise to collect the timing tags\n[2 Apr 2026] Elif: @Wren I promise to tune the gear cables by 2026-04-11 if the hill climb is on.\n[3 Apr 2026] Greta: Sad to report that the hill climb is off.\n[4 Apr 2026] Wren: @Rhea I'll pump the spare tyres by 2026-04-10, promise.\n[7 Apr 2026] Wren: @Rhea Guess what, I managed to pump the spare tyres!",
  "question": "Did Wren keep the promise to pump the spare tyres on 2026-04-11?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qfbbc303eb7",
  "kind": "yes/no",
  "text": "Nadia forwarded this support chat, which is about the new repertoire.\n\nMembers: Lee, Zara, Wren, Nadia\nChat log (oldest first):\n[15 Jan 2026] Wren: @Zara I will set up the sound desk by 20 Jan 2026 only if the summer recital happens.\n[18 Jan 2026] Zara: @Wren You can bank on me to buy the spare folders by 21 Jan 2026.\n[19 Jan 2026] Nadia: @Wren Count on me to print the song sheets by 28 Jan 2026, if the sing along happens.\n[20 Jan 2026] Zara: @Lee I will make sure to fetch the choir robes by 28 Jan 2026.\n[22 Jan 2026] Zara: @Wren Got myself to buy the spare folders lol.",
  "question": "Checking the chat at the end of 26 Jan 2026, has Zara broken the promise to buy the spare folders?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q69b15e36c8",
  "kind": "choice",
  "text": "Committee chat on the new kit design, forwarded by Jonas to the volunteers.\n\nMembers: Yuki, Kai, Hana, Jonas\nChat export (date | from | to | message):\n2026-06-01 | Hana | Yuki | I'll print the route cards by 5 Jun 2026, provided the club sportive happens.\n2026-06-03 | Yuki | Hana | Got it, I'll pump the spare tyres by 8 Jun 2026 for sure.\n2026-06-04 | Jonas | Kai | Provided the hill climb happens, I'll service the tandem bike by 9 Jun 2026.\n2026-06-05 | Jonas | Kai | Relax, I'll return the loaned helmets by 11 Jun 2026 for sure.\n2026-06-06 | Kai | group | Fab, we are on for the hill climb as planned!\n2026-06-07 | Hana | Yuki | You are released, no requirement to pump the spare tyres.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Yuki's promise to pump the spare tyres at the end of 12 Jun 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q1f562ea8ff",
  "kind": "choice",
  "text": "Attached chat: the winter concert\nShared by: Kofi\n\nMembers: Elif, Malik, Kofi, Wren\nChat log (oldest first):\n[3 Sep 2026] Malik: Fingers crossed I can collect the sheet music by Thursday, September 10, 2026.\n[5 Sep 2026] Malik: @Elif Count on me to collect the sheet music by Saturday, September 12, 2026, if the voice test happens.\n[5 Sep 2026] Malik: @Elif I'll be sure to return the library scores by Monday, September 14, 2026.\n[7 Sep 2026] Wren: Update: the voice test is going ahead as planned.\n[8 Sep 2026] Malik: @Elif Any chance I can collect the sheet music by Wednesday, September 16, 2026 instead?\n[10 Sep 2026] Kofi: @Malik Yes, you have the green light to collect the sheet music by Wednesday, September 16, 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Malik's pledge to collect the sheet music sit at the end of Saturday, September 12, 2026?",
  "options": [
   "Waived",
   "Kept",
   "Not yet due",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q1b4418c0f4",
  "kind": "yes/no",
  "text": "Client thread on the menu redesign, saved by Kai for the project log.\n\nMembers: Kai, Tess, Lee\nChat log (oldest first):\n[5 Apr 2026] Tess: @Kai Lovely, I'll collect the photo credits by 10 April 2026 for sure.\n[7 Apr 2026] Tess: @Lee Provided the packaging launch happens, I'll export the logo files by 14 April 2026.\n[9 Apr 2026] Lee: Fab, we are on for the packaging launch as planned!\n[10 Apr 2026] Tess: @Kai Apologies, I'll not be able to collect the photo credits\n[12 Apr 2026] Kai: @Tess You don't have to export the logo files at all",
  "question": "When you check the chat at the end of 18 April 2026, is the promise Tess made to export the logo files broken?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qce05f352a8",
  "kind": "yes/no",
  "text": "Ravi saved this so we stay on the same page about the summer lets season, mates.\n\nMembers: Ravi, Femi, Sami, Ines\nChat log (oldest first):\n[22 Jul 2026] Ines: @Sami You can bank on me to leave the welcome basket by August 1, 2026.\n[23 Jul 2026] Sami: @Femi If the guest arrival evening is on, I'll definitely collect the bed linen by July 31, 2026.\n[25 Jul 2026] Sami: Yep, the guest arrival evening is on as planned.\n[26 Jul 2026] Sami: @Femi Log entry: collect the bed linen, carried out\n[26 Jul 2026] Ines: @Ravi It's on me to air the spare room by August 3, 2026.",
  "question": "Does the card's rule set show that Sami has not kept the promise to collect the bed linen at the end of July 31, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q26b9c2c666",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the reunion planning\nFrom Leila, the thread below is shared as it stands.\n\nMembers: Leila, Priya, Elif, Ivo\nChat export (date | from | to | message):\n2026-07-20 | Elif | Leila | I'll set up the slideshow laptop by 29 Jul 2026 if the cousin brunch goes ahead.\n2026-07-21 | Priya | group | Yay, the cousin brunch is all set to go!\n2026-07-21 | Ivo | Elif | I'll be sure to send the group invitations by 26 Jul 2026.\n2026-07-25 | Priya | Leila | It's on me to collect the old photo prints by 28 Jul 2026.\n2026-07-26 | Ivo | Elif | Log entry: send the group invitations, carried out",
  "question": "Does the card classify Ivo's promise to send the group invitations as kept, instead of broken, waived, not triggered or not yet due, on 1 Aug 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd69aa544ab",
  "kind": "choice",
  "text": "Team channel export, shared by Kofi, which is about the mobile release.\n\nMembers: Lena, Kofi, Mo\nChat log (oldest first):\n[28 May 2026] Lena: @Mo As long as the sprint demo is on, I'll review the pull request by 3 June 2026.\n[29 May 2026] Lena: @Kofi I'll rotate the test keys by 31 May 2026 as long as the planning session is on.\n[30 May 2026] Mo: @Kofi It's on me to deploy the staging build by 6 June 2026.\n[30 May 2026] Lena: Brilliant news everyone, the planning session is a go!\n[4 Jun 2026] Mo: @Kofi Forget what I said, I won't deploy the staging build\n[6 Jun 2026] Lena: @Mo No worries, you don't need to deploy the staging build",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Mo's pledge to deploy the staging build sit at the end of 9 June 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Not yet due",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "qcb2819e0b9",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the trade show push\nThe chat below comes from Nadia, copied as is for reference.\n\nMembers: Priya, Jonas, Nadia\nChat export (date | from | to | message):\n2026-04-15 | Jonas | group | Aiming to return the rented camera gear by 22 April 2026, we'll see.\n2026-04-16 | Jonas | Priya | Relax, I'll return the rented camera gear by 24 April 2026 for sure.\n2026-04-19 | Priya | Jonas | I assure you I'll collect the survey answers by 28 April 2026 if the webinar rehearsal is on.\n2026-04-19 | Jonas | Nadia | I own this, I'll pay the printing invoice by 25 April 2026.\n2026-04-20 | Jonas | Priya | Log entry: return the rented camera gear, carried out\n2026-04-27 | Nadia | group | Brilliant news everyone, the webinar rehearsal is a go!",
  "question": "Would you say Jonas kept the promise to return the rented camera gear at the end of 20 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9a50ad45f3",
  "kind": "choice",
  "text": "Shared by Arlo, this is where the street watch scheme gets planned.\n\nMembers: Ravi, Tomas, Arlo\nChat log (oldest first):\n[4 Jun 2026] Tomas: @Ravi Count on me to return the ladders by 12 Jun 2026 if the parking permit visit is on.\n[5 Jun 2026] Ravi: @Arlo Count on me to lock the side gate by 13 Jun 2026.\n[6 Jun 2026] Tomas: @Arlo Count on me, I'll sweep the pavement outside by 14 Jun 2026.\n[8 Jun 2026] Ravi: Lovely, the parking permit visit is definitely happening!\n[9 Jun 2026] Ravi: @Arlo It's on me to take in the post by 13 Jun 2026.\n[12 Jun 2026] Tomas: @Ravi On my action item, may I return the ladders by 15 Jun 2026 instead?\n[12 Jun 2026] Arlo: @Tomas Yes, fine to return the ladders by 15 Jun 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, what is the deadline for Tomas to return the ladders at the end of 21 Jun 2026, with any agreed change of date counted?",
  "options": [
   "13 Jun 2026",
   "15 Jun 2026",
   "12 Jun 2026"
  ]
 },
 {
  "qid": "q2aff8a5698",
  "kind": "yes/no",
  "text": "Subject: Saved chat on the home adaptations\nHere is the export from Femi, for the record.\n\nMembers: Tomas, Hana, Femi\nChat log (oldest first):\n[18 Jul 2026] Femi: @Hana You can bet I'll drop off the hot meals by 21 July 2026.\n[19 Jul 2026] Femi: @Hana I regret to say that I shall not drop off the hot meals.\n[20 Jul 2026] Femi: @Tomas I'll print the care schedule by 26 July 2026, provided the home assessment happens.\n[25 Jul 2026] Hana: Afraid the home assessment is called off.\n[26 Jul 2026] Femi: @Tomas Is it all right if I print the care schedule by 1 August 2026 instead?\n[26 Jul 2026] Hana: @Femi Revised deadline is 1 August 2026, so you can print the care schedule.",
  "question": "Going by the card's rules, does Femi not keep the promise to print the care schedule at the end of 27 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qaca16e05b3",
  "kind": "choice",
  "text": "Messages with the letting agent about the student house hunt, forwarded by Yuki for the rental file.\n\nMembers: Ivo, Bruno, Yuki\nChat log (oldest first):\n[7 Feb 2026] Bruno: @Ivo Count on me to send the deposit receipt by Saturday, 14 February 2026, if the agent inventory walk happens.\n[7 Feb 2026] Bruno: Please note the agent inventory walk will proceed.\n[11 Feb 2026] Yuki: @Bruno It's on me to return the bin rota by Sunday, 15 February 2026.\n[11 Feb 2026] Yuki: @Bruno Count on me to copy the house keys by Monday, 16 February 2026.\n[14 Feb 2026] Bruno: @Ivo Ta-da, I went and did it: send the deposit receipt!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Bruno made to send the deposit receipt is in which status at the end of Saturday, 14 February 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q873ac10847",
  "kind": "yes/no",
  "text": "Shared by Wren, this is where the caring rota gets planned.\n\nMembers: Sami, Dara, Greta, Wren\nChat log (oldest first):\n[15 May 2026] Sami: @Dara I promise to book the clinic transport by 23 May 2026.\n[16 May 2026] Sami: @Dara I will call the home nurse by 19 May 2026.\n[19 May 2026] Dara: @Sami I promise to fetch the mobility aids by 26 May 2026 if the eye test is on.\n[19 May 2026] Dara: @Greta Guaranteed I'll return the hospital bed by 27 May 2026.\n[25 May 2026] Wren: Really pleased to say the eye test will go ahead!\n[25 May 2026] Dara: @Sami Mum, I did fetch the mobility aids, haha.",
  "question": "Going by the card's rules, does Dara keep the promise to fetch the mobility aids at the end of 31 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q601d73eb2b",
  "kind": "yes/no",
  "text": "Yo flatmates, Priya shared this chat about the garden makeover, so chip in.\n\nMembers: Priya, Tess, Lena\nChat export (date | from | to | message):\n2026-05-29 | Priya | Tess | I'll measure the hallway for shelves by 5 Jun 2026, providing the kitchen fitting day goes ahead.\n2026-05-30 | Tess | group | Fab, we are on for the kitchen fitting day as planned!\n2026-05-30 | Tess | Lena | Relax, I'll fetch the paint samples by 7 Jun 2026, promise.\n2026-05-31 | Tess | Lena | Count on me, I'll print the floor plan by 7 Jun 2026.\n2026-05-31 | Tess | Lena | Apologies, I'll not be able to print the floor plan\n2026-06-08 | Priya | Tess | Log entry: measure the hallway for shelves, carried out",
  "question": "Is the promise Priya made to measure the hallway for shelves in a status other than broken at the end of 9 Jun 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q564f1883ee",
  "kind": "yes/no",
  "text": "Ravi saved this so we stay on the same page about the summer lets season, mates.\n\nMembers: Ravi, Femi, Sami, Ines\nChat log (oldest first):\n[22 Jul 2026] Ines: @Sami You can bank on me to leave the welcome basket by August 1, 2026.\n[23 Jul 2026] Sami: @Femi If the guest arrival evening is on, I'll definitely collect the bed linen by July 31, 2026.\n[25 Jul 2026] Sami: Yep, the guest arrival evening is on as planned.\n[26 Jul 2026] Sami: @Femi Log entry: collect the bed linen, carried out\n[26 Jul 2026] Ines: @Ravi It's on me to air the spare room by August 3, 2026.",
  "question": "Is Sami's promise to collect the bed linen kept at the end of July 31, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9c13a94f1a",
  "kind": "choice",
  "text": "Attached chat: the new repertoire\nShared by: Lena.\n\nMembers: Ines, Lena, Oskar\nChat log (oldest first):\n[5 Aug 2026] Ines: @Oskar I will make sure to move the piano by 9 August 2026.\n[7 Aug 2026] Oskar: @Ines I assure you I'll return the library scores by 12 August 2026 if the sing along is on.\n[10 Aug 2026] Lena: Sorry all, the sing along is called off.\n[11 Aug 2026] Oskar: @Ines Would it be fine if I return the library scores by 14 August 2026 instead, yeah?\n[11 Aug 2026] Ines: @Oskar Of course, it is fine for you to return the library scores by 14 August 2026.",
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
  "qid": "q212a4d78bb",
  "kind": "choice",
  "text": "Ines shared this to pin down the attic conversion idea, housemates.\n\nMembers: Oskar, Bruno, Ines, Zara\nChat export (date | from | to | message):\n2026-07-15 | Oskar | Ines | No promises, but I'll aim to sort the recycling bags by 21 July 2026.\n2026-07-17 | Oskar | Ines | Got it, I'll sort the recycling bags by 20 July 2026 for sure.\n2026-07-17 | Zara | Oskar | Nobody needs you to sort the recycling bags, that's that\n2026-07-17 | Oskar | Ines | To my relief, I managed to sort the recycling bags.\n2026-07-21 | Oskar | Bruno | As long as the lodger house supper is on, I'll cut a spare door key by 27 July 2026.\n2026-07-21 | Zara | Ines | I will defrost the top freezer by 24 July 2026 only if the lodger farewell supper happens.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Oskar's commitment to sort the recycling bags have at the end of 17 July 2026?",
  "options": [
   "Broken",
   "Kept",
   "Waived",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qc5054ad214",
  "kind": "choice",
  "text": "Malik shared this so the new repertoire is easy to follow for the volunteers.\n\nMembers: Nadia, Malik, Zara, Sami\nChat export (date | from | to | message):\n2026-04-13 | Zara | Malik | I will make sure to move the piano by 22 Apr 2026.\n2026-04-13 | Sami | Zara | Forget it, you won't need to move the piano\n2026-04-15 | Nadia | Malik | As long as the carol concert is on, I will send the audition reminders by 18 Apr 2026.\n2026-04-17 | Malik | group | Afraid the carol concert is called off.\n2026-04-17 | Nadia | Malik | Is 23 Apr 2026 alright for me to send the audition reminders?\n2026-04-17 | Malik | Nadia | Yes, you're welcome to send the audition reminders by 23 Apr 2026 instead.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Nadia's promise to send the audition reminders turn out at the end of 22 Apr 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not triggered",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q3930d9bef0",
  "kind": "yes/no",
  "text": "Ana shared this exchange with the client about the rebrand package.\n\nMembers: Ana, Lena, Kai\nChat log (oldest first):\n[3 Jun 2026] Ana: @Lena As long as the brand review call is on, I will mail the business cards by 9 June 2026.\n[5 Jun 2026] Kai: @Lena I'll collect the photo credits by 8 June 2026 as long as the packaging launch is on.\n[6 Jun 2026] Lena: @Ana I will pick the colour swatches by 12 June 2026.\n[6 Jun 2026] Ana: Yep, the brand review call is on as planned.\n[9 Jun 2026] Ana: @Lena Mate, I promised, may I mail the business cards by 15 June 2026 instead?\n[9 Jun 2026] Kai: @Ana Yes, happy for you to mail the business cards by 15 June 2026 instead.",
  "question": "Did the promise that Ana made to mail the business cards turn out broken, waived, not triggered or not yet due, rather than kept, on 13 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd4cb24dc4f",
  "kind": "yes/no",
  "text": "Attached chat: the social media plan\nShared by: Femi.\n\nMembers: Zara, Hana, Femi, Elif\nChat export (date | from | to | message):\n2026-03-16 | Elif | Hana | Count on me to draft the press release by 18 Mar 2026.\n2026-03-17 | Zara | Femi | Count on me to book the photo studio by 19 Mar 2026 if the annual review is on.\n2026-03-21 | Femi | Zara | You can bet I'll fetch the campaign budget sheet by 27 Mar 2026.\n2026-03-21 | Zara | group | Ah right, thanks for that.\n2026-03-21 | Elif | Femi | If the brand photo shoot goes ahead, I'll pay the printing invoice by 28 Mar 2026.\n2026-03-23 | Hana | Femi | Relax, mate, you're not expected to fetch the campaign budget sheet",
  "question": "Would you say Femi kept the promise to fetch the campaign budget sheet at the end of 28 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q21948beb6d",
  "kind": "choice",
  "text": "Lee exported this channel chat about the social media plan for the team.\n\nMembers: Priya, Ravi, Lee, Arlo\nChat export (date | from | to | message):\n2026-04-25 | Arlo | Priya | I'll print the event banners by 1 May 2026, promise.\n2026-04-27 | Arlo | Priya | I promise to fix the landing page headline by 4 May 2026 if the annual review is on.\n2026-04-27 | Priya | group | Brilliant news everyone, the annual review is a go!\n2026-04-27 | Ravi | Arlo | Forget it, you won't need to fix the landing page headline\n2026-05-02 | Priya | Ravi | Count on me to book the photo studio by 6 May 2026.\n2026-05-03 | Lee | Priya | Don't sweat it, there's no need to book the photo studio",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of 27 Apr 2026, which status does Arlo have for the promise to fix the landing page headline?",
  "options": [
   "Not triggered",
   "Broken",
   "Waived",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q3e0e722e77",
  "kind": "choice",
  "text": "Subject: Chat about the kitchen garden project\nThe copy from Malik follows below as a plain record.\n\nMembers: Femi, Wren, Malik, Sami\nChat log (oldest first):\n[14 Jan 2026] Malik: @Wren I'll water the allotment beds by 16 January 2026, promise.\n[15 Jan 2026] Wren: @Femi I will deliver the surplus runner beans by 18 January 2026 only if the plot inspection happens.\n[16 Jan 2026] Wren: Just so you know, the plot inspection is on as scheduled.\n[16 Jan 2026] Femi: @Wren Don't sweat it, there's no need to deliver the surplus runner beans\n[18 Jan 2026] Wren: @Femi For the record: I was able to deliver the surplus runner beans",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Wren's promise to deliver the surplus runner beans at the end of 17 January 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "qf3824361ce",
  "kind": "yes/no",
  "text": "Here is the plan for the travel plans, saved by Yuki for the group.\n\nMembers: Lena, Ravi, Yuki, Ivo\nChat export (date | from | to | message):\n2026-07-16 | Yuki | Ivo | Provided the family cookout happens, I will buy the packing cubes by 25 July 2026.\n2026-07-17 | Yuki | group | Please note the family cookout will proceed.\n2026-07-17 | Yuki | Lena | Count on me to return the rental car keys by 20 July 2026.\n2026-07-20 | Lena | Ravi | If the beach picnic goes ahead, I'll book the airport parking by 24 July 2026.\n2026-07-20 | Ivo | Yuki | No worries, you don't need to return the rental car keys\n2026-07-23 | Yuki | Lena | Quick report: I've managed to return the rental car keys",
  "question": "Does the card classify Yuki's promise to return the rental car keys as kept, instead of broken, waived, not triggered or not yet due, on 21 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe0d7e7b86e",
  "kind": "choice",
  "text": "Kofi shared this support thread, which is about the showreel refresh.\n\nMembers: Dara, Kofi, Ivo, Priya\nChat export (date | from | to | message):\n2026-06-30 | Priya | Kofi | If the agency review call is on, I'll definitely ship the hard drive by 9 July 2026.\n2026-07-01 | Ivo | Kofi | Guaranteed I'll label the clip folders by 8 July 2026.\n2026-07-06 | Ivo | Kofi | Might I ask whether I could label the clip folders by 10 July 2026 instead?\n2026-07-06 | Kofi | Ivo | Yes, you have the green light to label the clip folders by 10 July 2026.\n2026-07-06 | Priya | Ivo | No worries, you don't need to label the clip folders\n2026-07-07 | Dara | Ivo | Count on me to back up the project drives by 9 July 2026, if the grading session happens.\n2026-07-07 | Dara | Ivo | As long as the voiceover session is on, I'll send the colour notes by 9 July 2026.\n2026-07-16 | Ivo | Kofi | Log entry: label the clip folders, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat's the day Ivo needs to label the clip folders by at the end of 7 July 2026, after any new date the group agreed on?",
  "options": [
   "8 July 2026",
   "10 July 2026",
   "9 July 2026"
  ]
 },
 {
  "qid": "q94dec530e8",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the data cleanup\nFrom Rhea, the thread below is shared as it stands.\n\nMembers: Rhea, Oskar, Ana, Ravi\nChat log (oldest first):\n[10 Mar 2026] Ravi: @Oskar Provided the penetration test happens, I will restart the build server by March 13, 2026.\n[11 Mar 2026] Ana: Really pleased to say the penetration test will go ahead!\n[13 Mar 2026] Ana: @Oskar I will label the bug reports by March 17, 2026.\n[15 Mar 2026] Rhea: @Oskar Lovely, I'll merge the login branch by March 18, 2026 for sure.\n[16 Mar 2026] Ana: @Oskar To note: I have managed to label the bug reports\n[18 Mar 2026] Rhea: @Oskar Is it all right if I merge the login branch by March 23, 2026 instead?\n[18 Mar 2026] Oskar: @Rhea Yes, you're welcome to merge the login branch by March 23, 2026 instead.\n[24 Mar 2026] Rhea: @Oskar To my relief, I managed to merge the login branch.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of March 26, 2026, what is the date by which Rhea has to merge the login branch, counting any agreed change?",
  "options": [
   "March 23, 2026",
   "March 18, 2026",
   "March 17, 2026"
  ]
 },
 {
  "qid": "q47cb230c5a",
  "kind": "choice",
  "text": "Shared by Tomas, this thread covers the honeymoon album as pasted from email.\n\nMembers: Rhea, Lena, Tomas, Wren\nChat log (oldest first):\n[6 May 2026] Lena: @Tomas You can bank on me to pick up the album prints by 14 May 2026.\n[9 May 2026] Lena: @Rhea Lovely, I'll return the lighting stands by 13 May 2026 for sure.\n[10 May 2026] Wren: @Lena Promise to buy the candle props by 15 May 2026 if the rehearsal dinner goes ahead.\n[10 May 2026] Wren: @Lena Quick update: you do not need to return the lighting stands at all.\n[12 May 2026] Rhea: Team, the rehearsal dinner stays on as booked.\n[13 May 2026] Tomas: @Lena Forget it, you won't need to pick up the album prints",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Lena's pledge to return the lighting stands sit at the end of 17 May 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Kept",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q4dfd7c1997",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the summer getaway\nThis export came from Yuki and is pasted in full below.\n\nMembers: Ravi, Greta, Yuki\nChat export (date | from | to | message):\n2026-06-02 | Greta | Yuki | I will fetch the sunscreen by Monday, 8 June 2026 only if the ferry crossing happens.\n2026-06-02 | Yuki | group | Sorry, the ferry crossing is off.\n2026-06-04 | Yuki | Ravi | You can bet I'll collect the insurance papers by Thursday, 11 June 2026.\n2026-06-05 | Greta | Yuki | Any chance I can fetch the sunscreen by Saturday, 13 June 2026 instead?\n2026-06-07 | Yuki | Greta | Yes, you're welcome to fetch the sunscreen by Saturday, 13 June 2026 instead.",
  "question": "At the end of Sunday, 7 June 2026, has Greta broken its promise to fetch the sunscreen?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa688879278",
  "kind": "choice",
  "text": "Team channel: the trade show push\nExported by Dara.\n\nMembers: Kofi, Greta, Mo, Dara\nChat export (date | from | to | message):\n2026-04-16 | Dara | Greta | You can bet I'll fetch the campaign budget sheet by Thursday, April 23, 2026.\n2026-04-17 | Greta | Dara | Got it, I'll draft the press release by Wednesday, April 22, 2026 for sure.\n2026-04-18 | Mo | Kofi | I will return the rented camera gear by Saturday, April 25, 2026 only if the annual review happens.\n2026-04-19 | Greta | Dara | Correction, I will not be able to draft the press release.\n2026-04-21 | Kofi | group | Afraid the annual review is called off.\n2026-04-22 | Kofi | Dara | Forget it, you won't need to fetch the campaign budget sheet",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Dara's commitment to fetch the campaign budget sheet at the end of Thursday, April 23, 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Waived",
   "Broken"
  ]
 }
]
