# G5-H blind read (all free-form rows) T32-blind_read-0ca8b554-008 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root9/T32/qc/g5h/answers/T32-blind_read-0ca8b554-008.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 26. Answers expected: 26 (one per item, each with that item's qid).

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
  "qid": "qdffb156697",
  "kind": "yes/no",
  "text": "Tomas forwarded this support chat, which is about the school fundraiser.\n\nMembers: Tomas, Malik, Jonas, Lee\nChat export (date | from | to | message):\n2026-10-11 | Lee | Malik | I assure you I'll wrap the prize hampers by October 13, 2026 if the quiz night is on.\n2026-10-11 | Tomas | group | Sorry all, the quiz night is not happening.\n2026-10-12 | Malik | Lee | I will set up the book stall by October 22, 2026 only if the summer fete happens.\n2026-10-13 | Lee | Tomas | It's on me to count the donation boxes by October 21, 2026.\n2026-10-16 | Lee | Tomas | I need to take back my commitment to count the donation boxes.\n2026-10-16 | Tomas | Lee | Forget it, you won't need to count the donation boxes",
  "question": "Would a check of the chat at the end of October 19, 2026 show the promise Lee made to count the donation boxes as broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe7f5eb92a8",
  "kind": "yes/no",
  "text": "Team channel export, shared by Femi, which is about the social media plan.\n\nMembers: Greta, Tomas, Femi\nChat export (date | from | to | message):\n2026-04-12 | Tomas | Femi | I will draft the press release by 18 Apr 2026 only if the influencer call happens.\n2026-04-13 | Greta | group | Might be able to set up the analytics dashboard by 21 Apr 2026, who knows!\n2026-04-14 | Greta | Tomas | Got it, I'll set up the analytics dashboard by 22 Apr 2026 for sure.\n2026-04-16 | Greta | Tomas | I'll fetch the campaign budget sheet by 25 Apr 2026 as long as the annual review is on.\n2026-04-20 | Femi | Greta | Quick update: you do not need to set up the analytics dashboard at all.\n2026-04-22 | Greta | Tomas | Mum, I did set up the analytics dashboard, haha.",
  "question": "Is Greta's promise to set up the analytics dashboard kept on 22 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q788bc3ceff",
  "kind": "yes/no",
  "text": "Forwarded by Priya: a help-desk thread covering the choir tour.\n\nMembers: Priya, Mo, Malik, Kofi\nChat log (oldest first):\n[10 Mar 2026] Kofi: I'll see if I can fix the stand microphones by 19 Mar 2026.\n[10 Mar 2026] Priya: @Malik Relax, I'll collect the sheet music by 14 Mar 2026 for sure.\n[12 Mar 2026] Kofi: @Mo Only if the choir festival is on, I will fix the stand microphones by 20 Mar 2026.\n[17 Mar 2026] Kofi: Brilliant news everyone, the choir festival is a go!\n[20 Mar 2026] Kofi: @Mo Might I ask whether I could fix the stand microphones by 22 Mar 2026 instead?\n[20 Mar 2026] Mo: @Kofi Nah, that deadline counts, mate, so please fix the stand microphones!",
  "question": "Is the promise to fix the stand microphones kept by Kofi as of 20 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5297cad350",
  "kind": "yes/no",
  "text": "Rhea shared this support thread, which is about the holiday catalogue.\n\nMembers: Zara, Wren, Rhea\nChat log (oldest first):\n[27 Jun 2026] Wren: @Rhea You can bet I'll fetch the domain login by 1 July 2026.\n[30 Jun 2026] Rhea: @Zara I will renew the hosting plan by 6 July 2026 only if the pop up stall happens.\n[30 Jun 2026] Zara: @Wren Hoping to restore the old theme by 4 July 2026, can't promise.\n[1 Jul 2026] Zara: @Wren I will make sure to restore the old theme by 8 July 2026.\n[1 Jul 2026] Zara: @Wren Got myself to restore the old theme lol.\n[4 Jul 2026] Rhea: @Zara I'll send the stock spreadsheet by 10 July 2026 as long as the market day is on.",
  "question": "Was Zara's promise to restore the old theme not kept as of 1 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2317246abe",
  "kind": "yes/no",
  "text": "Posted by Nadia from the work channel: the platform rewrite.\n\nMembers: Arlo, Nadia\nChat log (oldest first):\n[16 Jan 2026] Arlo: @Nadia Provided the planning session happens, I will review the pull request by 21 January 2026.\n[19 Jan 2026] Nadia: @Arlo Lovely, I'll merge the login branch by 26 January 2026 for sure.\n[19 Jan 2026] Arlo: @Nadia Ticket's mine, I'll rotate the test keys by 28 January 2026.\n[19 Jan 2026] Arlo: Lovely, the planning session is definitely happening!\n[26 Jan 2026] Nadia: @Arlo Log entry: merge the login branch, carried out\n[28 Jan 2026] Arlo: @Nadia Gutted to say I won't rotate the test keys, sorry team",
  "question": "Is Nadia's promise to merge the login branch broken, waived, not triggered or not yet due as of 31 January 2026, instead of kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb1a4427ca1",
  "kind": "choice",
  "text": "Yuki saved these exchanges with the agent about the shared kitchen scheme.\n\nMembers: Arlo, Yuki, Ravi\nChat export (date | from | to | message):\n2026-06-08 | Yuki | Arlo | You can bet I'll wipe the shared kitchen counter by 10 June 2026.\n2026-06-09 | Arlo | Yuki | I own this, I'll buy the washing powder by 11 June 2026.\n2026-06-11 | Arlo | Ravi | Ticket's mine, I'll turn the heating timer by 18 June 2026.\n2026-06-12 | Arlo | Ravi | Lovely, I'll defrost the top freezer by 20 June 2026 if the landlord inspection walk is on.\n2026-06-12 | Arlo | group | Great news, the landlord inspection walk is on!\n2026-06-15 | Ravi | group | Quick check, any update on plans to defrost the top freezer?",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Arlo doing with the promise to defrost the top freezer at the end of 16 June 2026?",
  "options": [
   "Kept",
   "Waived",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qed5a68bbfd",
  "kind": "choice",
  "text": "Here is the thread on the big house plan, posted by Kai for the house.\n\nMembers: Mo, Kai, Oskar, Arlo\nChat log (oldest first):\n[7 Sep 2026] Kai: @Arlo Provided the ghost tour happens, I'll bleed the attic radiators by 15 Sep 2026.\n[10 Sep 2026] Arlo: @Kai Guaranteed I'll mend the garden gate by 18 Sep 2026.\n[10 Sep 2026] Arlo: @Kai I'll be sure to find the loft ladder by 16 Sep 2026.\n[11 Sep 2026] Arlo: We are dropping the ghost tour from the list.\n[18 Sep 2026] Arlo: @Kai On my action item, may I mend the garden gate by 20 Sep 2026 instead?\n[18 Sep 2026] Oskar: @Arlo Yes, all good for you to mend the garden gate by 20 Sep 2026 instead.\n[20 Sep 2026] Arlo: @Kai To my relief, I managed to mend the garden gate.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Arlo supposed to mend the garden gate by, going by the chat at the end of 2 Oct 2026 and any agreed changes?",
  "options": [
   "18 Sep 2026",
   "16 Sep 2026",
   "20 Sep 2026"
  ]
 },
 {
  "qid": "qa892d5309d",
  "kind": "choice",
  "text": "Lena shared this channel export covering the data cleanup for the team.\n\nMembers: Lena, Kai\nChat log (oldest first):\n[28 Sep 2026] Kai: @Lena Provided the penetration test happens, I'll rotate the test keys by 3 Oct 2026.\n[29 Sep 2026] Lena: Update: the penetration test is going ahead as planned.\n[30 Sep 2026] Lena: @Kai Guaranteed I'll merge the login branch by 5 Oct 2026.\n[30 Sep 2026] Lena: @Kai I committed to merge the login branch, can I do that by 8 Oct 2026 instead?\n[30 Sep 2026] Kai: @Lena Fine by me, you can merge the login branch by 8 Oct 2026.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Kai made to rotate the test keys at the end of 4 Oct 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Waived",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q8131192436",
  "kind": "yes/no",
  "text": "Here is the plan for the home adaptations, saved by Sami for the group.\n\nMembers: Jonas, Bruno, Sami\nChat log (oldest first):\n[27 Jul 2026] Jonas: @Bruno It's on me to book the clinic transport by August 3, 2026.\n[29 Jul 2026] Bruno: @Jonas You can bank on me to pick up the repeat prescription by August 6, 2026.\n[31 Jul 2026] Bruno: @Sami I'll collect the post by August 4, 2026, providing the hospital appointment goes ahead.\n[1 Aug 2026] Bruno: @Sami If the home assessment is on, I'll definitely print the care schedule by August 9, 2026.\n[3 Aug 2026] Bruno: Update, the hospital appointment will not take place.\n[6 Aug 2026] Bruno: @Jonas For the record: I was able to pick up the repeat prescription",
  "question": "Applying the card's rules, can it be said that Bruno has not kept the promise to pick up the repeat prescription at the end of August 7, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4bc2fa08cf",
  "kind": "choice",
  "text": "Here is the thread on the vegetable plot plan, posted by Ivo for the house.\n\nMembers: Ivo, Kai, Ravi, Ana\nChat log (oldest first):\n[26 May 2026] Kai: @Ana Only if the allotment site visit is on, I will sow the broad beans by 2026-06-03.\n[28 May 2026] Ivo: @Ravi Absolutely, I will dig the potato patch by 2026-06-05.\n[29 May 2026] Ivo: @Kai Provided the harvest supper happens, I'll water the allotment beds by 2026-06-07.\n[5 Jun 2026] Ivo: @Ravi Scratch that, I'm not going to dig the potato patch\n[5 Jun 2026] Ana: @Ivo Don't sweat it, there's no need to dig the potato patch",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Ivo made to dig the potato patch have at the end of 2026-06-10?",
  "options": [
   "Kept",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q4f3209178b",
  "kind": "choice",
  "text": "Sami saved this so we stay on the same page about the guest review drive, mates.\n\nMembers: Oskar, Kai, Sami\nChat log (oldest first):\n[29 Aug 2026] Oskar: @Sami I'll vacuum the holiday cottage by 5 Sep 2026 if the owner handover visit goes ahead.\n[29 Aug 2026] Oskar: Sorry all, the owner handover visit is not happening.\n[31 Aug 2026] Oskar: @Sami Might I ask whether I could vacuum the holiday cottage by 9 Sep 2026 instead?\n[31 Aug 2026] Oskar: @Sami Got it, I'll wheel the bins out by 10 Sep 2026 for sure.\n[31 Aug 2026] Sami: Anything new on your way to vacuum the holiday cottage?\n[1 Sep 2026] Sami: @Oskar We are holding the date on record, so vacuum the holiday cottage by it.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Oskar made to vacuum the holiday cottage, what state is it in at the end of 5 Sep 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q8a3ad811e4",
  "kind": "choice",
  "text": "Forwarded by Bruno: a help-desk thread covering the desk plan.\n\nMembers: Bruno, Lee, Jonas\nChat log (oldest first):\n[13 Apr 2026] Lee: @Bruno I promise to send the expense receipts by 19 Apr 2026 if the annual audit is on.\n[14 Apr 2026] Jonas: @Bruno I'll be sure to return the printer toner by 22 Apr 2026.\n[14 Apr 2026] Jonas: @Bruno Change of plans: I will not return the printer toner\n[14 Apr 2026] Bruno: @Jonas No worries, you don't need to return the printer toner\n[16 Apr 2026] Lee: @Bruno I'll collect the visitor badges by 18 Apr 2026 if the staff picnic goes ahead.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Jonas's promise to return the printer toner at the end of 15 Apr 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q4c15565b62",
  "kind": "yes/no",
  "text": "Here is the plan for the front garden scheme, saved by Leila for the group.\n\nMembers: Jonas, Malik, Leila\nChat log (oldest first):\n[24 Oct 2026] Jonas: @Leila Provided the bonfire night happens, I will lock the side gate by 28 October 2026.\n[25 Oct 2026] Jonas: Lovely, the bonfire night is definitely happening!\n[26 Oct 2026] Leila: @Jonas You can bank on me to return the ladders by 2 November 2026.\n[28 Oct 2026] Jonas: @Leila Got myself to lock the side gate lol.\n[31 Oct 2026] Leila: @Jonas Sorry, I won't return the ladders after all",
  "question": "Was the promise to lock the side gate from Jonas kept on 28 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd496248b3a",
  "kind": "choice",
  "text": "Casual chat for the flat, saved by Wren, and it covers the bathroom refit.\n\nMembers: Nadia, Sami, Wren\nChat export (date | from | to | message):\n2026-03-24 | Wren | Nadia | Count on me, I'll pay the plumbing invoice by 28 March 2026.\n2026-03-24 | Nadia | Wren | I promise to scrape the old wallpaper by 1 April 2026 if the damp survey inspection is on.\n2026-03-25 | Sami | Nadia | As long as the removal van arrival is on, I'll print the floor plan by 31 March 2026.\n2026-03-26 | Nadia | group | Update: the damp survey inspection is going ahead as planned.\n2026-03-27 | Wren | Sami | I'll return the tile cutter by 30 March 2026, promise.\n2026-03-27 | Sami | Wren | You are released, no requirement to return the tile cutter.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Nadia's commitment to scrape the old wallpaper have at the end of 28 March 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "qe3c2aa6ca6",
  "kind": "yes/no",
  "text": "Subject: Chat about the new repertoire\nBelow is a copy that came from Kofi, pasted as found.\n\nMembers: Elif, Kofi, Oskar, Ivo\nChat log (oldest first):\n[9 Sep 2026] Oskar: @Elif Count on me to print the song sheets by 16 Sep 2026 if the voice test is on.\n[9 Sep 2026] Oskar: Fab, we are on for the voice test as planned!\n[10 Sep 2026] Kofi: @Elif Guaranteed I'll buy the spare folders by 12 Sep 2026.\n[12 Sep 2026] Ivo: @Kofi Got it, I'll move the piano by 20 Sep 2026 for sure.\n[15 Sep 2026] Ivo: @Kofi I regret to say that I shall not move the piano.\n[18 Sep 2026] Kofi: Hey, did you get a chance to move the piano?",
  "question": "Does the card's rule set show that Ivo has not kept the promise to move the piano at the end of 16 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qafc2b51993",
  "kind": "yes/no",
  "text": "Team channel: the peer review\nShared by Sami.\n\nMembers: Omar, Sami, Ivo, Greta\nChat log (oldest first):\n[2 May 2026] Greta: @Ivo You can bank on me to order the reagent kit by 6 May 2026.\n[2 May 2026] Omar: @Greta You are released, no requirement to order the reagent kit.\n[2 May 2026] Greta: @Ivo To my relief, I managed to order the reagent kit.\n[4 May 2026] Omar: @Ivo As long as the safety inspection is on, I will book the microscope slot by 12 May 2026.\n[7 May 2026] Omar: Lovely, the safety inspection is definitely happening!",
  "question": "Does the card classify Greta's promise to order the reagent kit as kept, instead of broken, waived, not triggered or not yet due, on 8 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q79bf660b94",
  "kind": "choice",
  "text": "Ana shared this family chat about the reunion weekend for the relatives.\n\nMembers: Wren, Femi, Ana\nChat log (oldest first):\n[10 Jan 2026] Femi: @Ana If the garden picnic goes ahead, I'll buy the name tags by 18 January 2026.\n[14 Jan 2026] Ana: @Femi I'll print the family tree chart by 18 January 2026, provided the grandparents visit happens.\n[14 Jan 2026] Ana: @Wren Guaranteed I'll label the memory box by 20 January 2026.\n[19 Jan 2026] Ana: @Wren I committed to label the memory box, can I do that by 24 January 2026 instead?\n[20 Jan 2026] Wren: @Ana Yes, all good for you to label the memory box by 24 January 2026 instead.\n[21 Jan 2026] Femi: @Ana Ah, no stress, no need for you to label the memory box\n[23 Jan 2026] Ana: @Wren Got myself to label the memory box lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIf the chat is checked at the end of 26 January 2026, which date marks the deadline for Ana to label the memory box, with agreed date changes included?",
  "options": [
   "18 January 2026",
   "24 January 2026",
   "20 January 2026"
  ]
 },
 {
  "qid": "qabdd081731",
  "kind": "yes/no",
  "text": "Team channel export, shared by Priya, which is about the grant renewal.\n\nMembers: Nadia, Greta, Ravi, Priya\nChat log (oldest first):\n[20 Jan 2026] Priya: @Nadia Committing to order the reagent kit by Sunday, January 25, 2026.\n[20 Jan 2026] Nadia: Thanks, got it.\n[20 Jan 2026] Ravi: @Greta As long as the thesis defence is on, I will send the ethics form by Tuesday, January 27, 2026.\n[21 Jan 2026] Priya: @Nadia I assure you I'll return the library books by Saturday, January 24, 2026 if the seminar series is on.\n[22 Jan 2026] Greta: @Priya You don't have to order the reagent kit at all\n[23 Jan 2026] Ravi: @Priya I own this, I'll fetch the grant forms by Friday, January 30, 2026.",
  "question": "Going by the card's rules, does Priya keep the promise to order the reagent kit at the end of Friday, January 23, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qadd0b02bd9",
  "kind": "choice",
  "text": "Subject: Saved thread about the gallery show\nThis export from Lena is pasted in full for readers who want it.\n\nMembers: Lena, Nadia, Femi, Ivo\nChat log (oldest first):\n[31 Mar 2026] Ivo: @Nadia I own this, I'll export the logo files by 3 Apr 2026.\n[1 Apr 2026] Ivo: @Nadia Quick question, could I export the logo files by 7 Apr 2026 instead?\n[2 Apr 2026] Nadia: @Ivo No new date, so please export the logo files by the date given.\n[3 Apr 2026] Femi: @Nadia If the packaging launch goes ahead, I'll send the moodboard files by 10 Apr 2026.\n[4 Apr 2026] Femi: @Nadia If the brand review call goes ahead, I'll upload the sticker artwork by 8 Apr 2026.\n[7 Apr 2026] Nadia: Quick heads up, the packaging launch is scrapped.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Femi's commitment to send the moodboard files is in what status at the end of 7 Apr 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Not yet due",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "qf126da4304",
  "kind": "yes/no",
  "text": "Our flat chat about the student house hunt, shared by Ivo for whoever lives here.\n\nMembers: Lena, Priya, Ivo, Sami\nChat log (oldest first):\n[26 Aug 2026] Sami: @Lena Count on me to forward the inventory photos by 4 Sep 2026 if the freshers welcome night is on.\n[30 Aug 2026] Priya: @Lena Ticket's mine, I'll photograph the bathroom mould by 2 Sep 2026.\n[31 Aug 2026] Ivo: @Priya Quick update: you do not need to photograph the bathroom mould at all.\n[1 Sep 2026] Sami: @Ivo I promise to copy the house keys by 6 Sep 2026 if the move in day is on.\n[4 Sep 2026] Priya: @Lena Ticked off: photograph the bathroom mould, feels so good",
  "question": "Does the chat, checked at the end of 3 Sep 2026, show that Priya has broken the promise to photograph the bathroom mould?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qce0821de3b",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the bathroom refit\nFrom Femi, the thread below is shared as it stands.\n\nMembers: Rhea, Malik, Mo, Femi\nChat log (oldest first):\n[3 Feb 2026] Mo: @Rhea Promise to hang the new curtain rail by 9 Feb 2026 if the kitchen fitting day goes ahead.\n[4 Feb 2026] Mo: Afraid the kitchen fitting day is called off.\n[6 Feb 2026] Mo: @Rhea Committing to pay the plumbing invoice by 10 Feb 2026.\n[7 Feb 2026] Femi: Did you manage to hang the new curtain rail?\n[9 Feb 2026] Mo: @Rhea Think 14 Feb 2026 would work if I hang the new curtain rail instead?\n[9 Feb 2026] Rhea: @Mo Yes, you're welcome to hang the new curtain rail by 14 Feb 2026 instead.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Mo's commitment to hang the new curtain rail is in what status at the end of 13 Feb 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Not triggered",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q0989e98302",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the quiet street fund\nThis export came from Sami and is pasted in full below.\n\nMembers: Sami, Ana, Lena\nChat log (oldest first):\n[3 Oct 2026] Lena: @Sami Provided the parking permit visit happens, I will return the ladders by Wednesday, 7 October 2026.\n[3 Oct 2026] Sami: Brilliant news everyone, the parking permit visit is a go!\n[3 Oct 2026] Ana: @Lena Ah, no stress, no need for you to return the ladders\n[7 Oct 2026] Lena: @Ana You can bet I'll lend the stepladder by Friday, 16 October 2026.\n[11 Oct 2026] Sami: @Lena Ah, no stress, no need for you to lend the stepladder",
  "question": "Going by the card's rules, does Lena not keep the promise to return the ladders at the end of Sunday, 4 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8f5570f819",
  "kind": "yes/no",
  "text": "Rhea shared this support thread, which is about the holiday catalogue.\n\nMembers: Zara, Wren, Rhea\nChat log (oldest first):\n[27 Jun 2026] Wren: @Rhea You can bet I'll fetch the domain login by 1 July 2026.\n[30 Jun 2026] Rhea: @Zara I will renew the hosting plan by 6 July 2026 only if the pop up stall happens.\n[30 Jun 2026] Zara: @Wren Hoping to restore the old theme by 4 July 2026, can't promise.\n[1 Jul 2026] Zara: @Wren I will make sure to restore the old theme by 8 July 2026.\n[1 Jul 2026] Zara: @Wren Got myself to restore the old theme lol.\n[4 Jul 2026] Rhea: @Zara I'll send the stock spreadsheet by 10 July 2026 as long as the market day is on.",
  "question": "Is it true under the card's rules that Zara has kept the promise to restore the old theme at the end of 1 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q89271f4bf7",
  "kind": "yes/no",
  "text": "Attached chat: the ground upgrade\nShared by: Ivo\n\nMembers: Ivo, Tess, Priya, Tomas\nChat log (oldest first):\n[4 Feb 2026] Ivo: @Priya As long as the youth trial is on, I'll collect the referee whistles by 10 Feb 2026.\n[4 Feb 2026] Priya: Thanks lovely, got it!\n[5 Feb 2026] Ivo: Yay, the youth trial is all set to go!\n[6 Feb 2026] Tess: @Ivo Nobody needs you to collect the referee whistles, that's that\n[10 Feb 2026] Priya: @Tess I'll be sure to print the team sheets by 19 Feb 2026.\n[11 Feb 2026] Ivo: @Priya For the record: I was able to collect the referee whistles",
  "question": "Does the chat, checked at the end of 8 Feb 2026, show that Ivo has broken the promise to collect the referee whistles?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9762e20ea5",
  "kind": "choice",
  "text": "Ivo shared this so the family follows the summer visits.\n\nMembers: Lee, Tomas, Ivo\nChat log (oldest first):\n[1 Jun 2026] Lee: @Tomas Count on me to walk the dog by 4 Jun 2026 if the sleepover weekend is on.\n[3 Jun 2026] Ivo: Team, the sleepover weekend is not happening.\n[4 Jun 2026] Lee: @Tomas On my action item, may I walk the dog by 6 Jun 2026 instead?\n[4 Jun 2026] Tomas: @Lee Not moving it, walk the dog by the existing date.\n[6 Jun 2026] Lee: @Ivo I promise to read the bedtime story by 14 Jun 2026.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 8 Jun 2026, what status has Lee's promise to walk the dog got?",
  "options": [
   "Kept",
   "Not triggered",
   "Broken",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "q47fc46f349",
  "kind": "choice",
  "text": "Our flat chat about the allotment expansion, saved by Kai for whoever lives here.\n\nMembers: Malik, Kai, Wren\nChat log (oldest first):\n[19 Oct 2026] Kai: @Wren As long as the village flower show is on, I will build the compost bay by 26 Oct 2026.\n[21 Oct 2026] Wren: @Malik Lovely, I'll fix the shed door by 30 Oct 2026 for sure.\n[24 Oct 2026] Wren: Update, the village flower show will not take place.\n[24 Oct 2026] Kai: @Wren Is 29 Oct 2026 alright for me to build the compost bay?\n[26 Oct 2026] Wren: @Kai Oh hun, I can't budge, so build the compost bay by the old date!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Kai gave to build the compost bay have at the end of 29 Oct 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not triggered",
   "Not yet due",
   "Kept"
  ]
 }
]
