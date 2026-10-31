# G5-H blind read (all free-form rows) T32-blind_read-92ec9850-005 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T32/qc/g5h/answers/T32-blind_read-92ec9850-005.json

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
  "qid": "q25aec8266d",
  "kind": "yes/no",
  "text": "Parents and cousins, this is where we sort out the packing plan. Saved by Ana.\n\nMembers: Zara, Jonas, Ana, Nadia\nChat export (date | from | to | message):\n2026-01-26 | Nadia | Jonas | Count on me, I'll book the airport parking by 2 Feb 2026.\n2026-01-29 | Zara | Nadia | As long as the hotel arrival is on, I'll pack the travel adaptors by 1 Feb 2026.\n2026-01-31 | Nadia | Jonas | Correction, I will not be able to book the airport parking.\n2026-01-31 | Jonas | group | Just so you know, the hotel arrival is on as scheduled.\n2026-02-01 | Ana | group | Any news on plans to pack the travel adaptors?\n2026-02-05 | Zara | Nadia | Guess who managed to pack the travel adaptors, go team!",
  "question": "At the end of 2 Feb 2026, does the promise Zara made to pack the travel adaptors have any status except broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qebc856e7f0",
  "kind": "choice",
  "text": "Here we plan the house rules debate together, and Sami saved this for the family.\n\nMembers: Sami, Leila, Tomas\nChat log (oldest first):\n[16 Sep 2026] Sami: @Leila I will find the loft ladder by 26 September 2026.\n[20 Sep 2026] Leila: @Tomas If the loft clearance day goes ahead, I'll gladly mend the garden gate by 25 September 2026.\n[22 Sep 2026] Sami: @Leila To my relief, I managed to find the loft ladder.\n[22 Sep 2026] Tomas: Fab, we are on for the loft clearance day as planned!\n[25 Sep 2026] Tomas: @Leila Quick update: you do not need to mend the garden gate at all.\n[27 Sep 2026] Tomas: Quick check, any update on plans to mend the garden gate?",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Leila's pledge to mend the garden gate at the end of 30 September 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Broken",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "qfc996b70e1",
  "kind": "choice",
  "text": "Subject: Chat about the trip itinerary\nThe copy from Arlo follows below as a plain record.\n\nMembers: Priya, Yuki, Arlo, Rhea\nChat export (date | from | to | message):\n2026-10-29 | Arlo | Yuki | I assure you I'll fetch the sunscreen by 4 Nov 2026 if the ferry crossing is on.\n2026-10-31 | Rhea | Yuki | I assure you I'll send the packing list by 6 Nov 2026 if the beach picnic is on.\n2026-11-01 | Priya | Yuki | Count on me to return the rental car keys by 5 Nov 2026.\n2026-11-05 | Priya | Yuki | I'm withdrawing my promise to return the rental car keys\n2026-11-05 | Rhea | Priya | Good news, you're let off having to return the rental car keys",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Priya's pledge to return the rental car keys at the end of 6 Nov 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qc0cab8d41a",
  "kind": "choice",
  "text": "Forwarded by Yuki, this thread on the holiday catalogue stays attached to the ticket.\n\nMembers: Yuki, Lena, Rhea, Elif\nChat log (oldest first):\n[21 Jul 2026] Elif: @Yuki As long as the pop up stall is on, I will send the stock spreadsheet by 25 July 2026.\n[24 Jul 2026] Yuki: Afraid the pop up stall is called off.\n[24 Jul 2026] Elif: @Yuki Is it all right if I send the stock spreadsheet by 28 July 2026 instead?\n[24 Jul 2026] Rhea: @Elif Yes, all good for you to send the stock spreadsheet by 28 July 2026 instead.\n[25 Jul 2026] Yuki: @Lena Relax, I'll fix the checkout button by 1 August 2026, promise.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Elif's commitment to send the stock spreadsheet have at the end of 25 July 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Not triggered",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q04c9964818",
  "kind": "choice",
  "text": "Here is the house refit, posted by Arlo for the family to read.\n\nMembers: Ravi, Lee, Ivo, Arlo\nChat export (date | from | to | message):\n2026-07-05 | Lee | Ravi | I'll pick up the grout bag by 8 July 2026, promise.\n2026-07-05 | Lee | Ravi | For the record: I was able to pick up the grout bag\n2026-07-06 | Arlo | Ivo | Lovely, I'll pay the plumbing invoice by 9 July 2026 if the boiler install visit is on.\n2026-07-08 | Lee | group | Fab, we are on for the boiler install visit as planned!\n2026-07-11 | Arlo | Lee | I own this, I'll scrape the old wallpaper by 13 July 2026.\n2026-07-12 | Arlo | Ravi | I'll be sure to return the tile cutter by 17 July 2026.",
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
  "qid": "q76d35b0f89",
  "kind": "yes/no",
  "text": "Shared by Tomas for the committee, this is the group chat on the new term plans.\n\nMembers: Tomas, Hana, Kofi\nChat export (date | from | to | message):\n2026-04-28 | Tomas | Kofi | Provided the reading festival happens, I'll count the donation boxes by 2 May 2026.\n2026-04-30 | Kofi | Hana | I will make sure to send the newsletter drafts by 6 May 2026.\n2026-05-01 | Kofi | group | Scrapping the reading festival, apologies to all.\n2026-05-04 | Tomas | Hana | Guaranteed I'll fetch the tea urn by 8 May 2026.\n2026-05-06 | Kofi | Hana | My sincere apologies, I am unable to send the newsletter drafts.\n2026-05-08 | Hana | Tomas | You are released, no requirement to fetch the tea urn.",
  "question": "Has Kofi kept the promise to send the newsletter drafts at the end of 10 May 2026, instead of broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4b9e9e8e66",
  "kind": "choice",
  "text": "Omar shared this channel export, covering the spring campaign for the team.\n\nMembers: Lena, Omar, Jonas, Rhea\nChat export (date | from | to | message):\n2026-06-04 | Omar | Rhea | I will make sure to pay the printing invoice by June 10, 2026.\n2026-06-05 | Lena | Rhea | I will send the newsletter copy by June 12, 2026 only if the webinar rehearsal happens.\n2026-06-06 | Omar | Rhea | Guess what, I managed to pay the printing invoice!\n2026-06-09 | Jonas | Omar | Lovely, I'll collect the survey answers by June 18, 2026 if the influencer call is on.\n2026-06-10 | Lena | Rhea | I promise to book the photo studio by June 18, 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Omar's promise to pay the printing invoice at the end of June 7, 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q1af06e4b96",
  "kind": "yes/no",
  "text": "Our flat chat about the house refit, saved by Kofi for whoever lives here.\n\nMembers: Ana, Leila, Kofi\nChat export (date | from | to | message):\n2026-09-17 | Ana | Kofi | Relax, I'll scrape the old wallpaper by 23 September 2026, promise.\n2026-09-18 | Ana | Kofi | Count on me, I'll pay the plumbing invoice by 27 September 2026.\n2026-09-19 | Leila | Ana | I'll fetch the paint samples by 26 September 2026, provided the boiler install visit happens.\n2026-09-21 | Ana | Kofi | Guess what, I managed to scrape the old wallpaper!\n2026-09-22 | Kofi | Ana | I assure you I'll return the tile cutter by 29 September 2026 if the mortgage valuation visit is on.\n2026-09-28 | Ana | group | Quick heads up, the mortgage valuation visit is scrapped.",
  "question": "Was Ana's promise to scrape the old wallpaper not kept as of 26 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q14f97b7107",
  "kind": "yes/no",
  "text": "Attached chat: the guest list\nShared by: Lena\n\nMembers: Lena, Ines, Priya, Mo\nChat log (oldest first):\n[11 Sep 2026] Lena: @Mo I own this, I'll fetch the spare memory cards by Wednesday, 16 September 2026.\n[11 Sep 2026] Priya: @Lena Forget it, you won't need to fetch the spare memory cards\n[12 Sep 2026] Lena: @Ines Got it, I'll set up the backdrop frame by Thursday, 17 September 2026 for sure.\n[15 Sep 2026] Mo: @Lena Lovely, I'll send the sneak peek gallery by Saturday, 19 September 2026 if the cake tasting is on.\n[15 Sep 2026] Ines: Afraid the cake tasting is called off.\n[19 Sep 2026] Lena: @Mo Guess who managed to fetch the spare memory cards, go team!",
  "question": "Is Lena's promise to fetch the spare memory cards kept at the end of Wednesday, 16 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa9a38d7a9e",
  "kind": "yes/no",
  "text": "Ivo saved this so we stay on the same page about the cellar project, mates.\n\nMembers: Rhea, Ivo, Jonas\nChat log (oldest first):\n[16 May 2026] Rhea: @Jonas I'll mend the garden gate by 22 May 2026, provided the loft clearance day happens.\n[18 May 2026] Jonas: Update: the loft clearance day is going ahead as planned.\n[20 May 2026] Jonas: Update on your plan to mend the garden gate?\n[20 May 2026] Jonas: @Rhea Forget it, you won't need to mend the garden gate\n[20 May 2026] Rhea: @Ivo Got it, I'll scrub the cellar steps by 23 May 2026 for sure.\n[22 May 2026] Rhea: @Ivo Sorry, I won't scrub the cellar steps after all",
  "question": "Has Rhea not broken the promise to mend the garden gate at the end of 21 May 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4504807564",
  "kind": "yes/no",
  "text": "Nadia shared this family chat about the summer visits for the relatives.\n\nMembers: Nadia, Malik, Tomas\nChat log (oldest first):\n[31 Jul 2026] Nadia: @Tomas Provided the school play happens, I'll bake the oat biscuits by 9 August 2026.\n[2 Aug 2026] Tomas: Team, the school play is not happening.\n[4 Aug 2026] Tomas: @Malik See if I can pack the picnic basket by 10 August 2026.\n[4 Aug 2026] Tomas: @Nadia I promise to tidy the playroom by 9 August 2026.\n[5 Aug 2026] Tomas: @Nadia Count on me, I'll pack the picnic basket by 8 August 2026.\n[5 Aug 2026] Malik: @Tomas Please don't feel you have to pack the picnic basket",
  "question": "Has Tomas kept the promise to pack the picnic basket at the end of 8 August 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb40fdf3480",
  "kind": "yes/no",
  "text": "Attached chat: the online store move\nShared by: Zara\n\nMembers: Zara, Priya, Arlo, Kai\nChat log (oldest first):\n[14 Feb 2026] Kai: @Priya I'll add the size chart by 2026-02-21 if the market day goes ahead.\n[16 Feb 2026] Priya: Brilliant news everyone, the market day is a go!\n[16 Feb 2026] Priya: @Zara Lovely, I'll fix the checkout button by 2026-02-22 for sure.\n[18 Feb 2026] Priya: @Zara I have to take back my promise to fix the checkout button.\n[23 Feb 2026] Kai: @Priya To my relief, I managed to add the size chart.",
  "question": "At the end of 2026-02-25, would it be right to say Kai has not broken the promise to add the size chart?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0daa77a891",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the rebrand package\nThe chat below comes from Mo, copied as is for reference.\n\nMembers: Mo, Leila, Ana\nChat log (oldest first):\n[13 Jul 2026] Mo: @Leila It's on me to export the logo files by Saturday, July 18, 2026.\n[15 Jul 2026] Ana: @Leila I'll fetch the brand fonts by Thursday, July 23, 2026, provided the gallery install happens.\n[16 Jul 2026] Leila: @Mo Count on me to pick the colour swatches by Friday, July 24, 2026.\n[17 Jul 2026] Leila: @Mo Quick report: I've managed to pick the colour swatches\n[17 Jul 2026] Mo: Fab, we are on for the gallery install as planned!\n[26 Jul 2026] Ana: @Leila Ta-da, I went and did it: fetch the brand fonts!",
  "question": "Has Ana kept the promise to fetch the brand fonts as of Friday, July 24, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0b49beba0d",
  "kind": "yes/no",
  "text": "Omar shared this family chat about the garden shed build for the relatives.\n\nMembers: Omar, Malik, Hana\nChat log (oldest first):\n[17 Mar 2026] Hana: @Malik It's on me to stake the tomato canes by 24 March 2026.\n[20 Mar 2026] Malik: @Hana Will attempt to water the allotment beds by 22 March 2026, can't promise.\n[21 Mar 2026] Malik: @Omar Lovely, I'll water the allotment beds by 28 March 2026 if the allotment site visit is on.\n[23 Mar 2026] Omar: @Hana I will collect the seed potatoes by 27 March 2026.\n[26 Mar 2026] Omar: @Hana Quick report: I've managed to collect the seed potatoes\n[27 Mar 2026] Omar: Just so you know, the allotment site visit is on as scheduled.",
  "question": "Applying the card's rules, does Malik's promise to water the allotment beds count as kept, rather than broken, waived, not triggered or not yet due, as of 28 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q201d97a9e9",
  "kind": "yes/no",
  "text": "Sami forwarded this support chat, which is about the menu redesign.\n\nMembers: Ivo, Sami, Tomas\nChat log (oldest first):\n[13 Sep 2026] Ivo: @Sami Committing to mail the business cards by Wednesday, 16 September 2026.\n[15 Sep 2026] Tomas: @Ivo If the brand review call goes ahead, I'll gladly collect the photo credits by Friday, 25 September 2026.\n[16 Sep 2026] Tomas: @Ivo Got it, I'll export the logo files by Thursday, 24 September 2026 for sure.\n[16 Sep 2026] Tomas: Sadly, the brand review call is not going ahead.\n[18 Sep 2026] Sami: @Tomas Ah, no stress, no need for you to export the logo files",
  "question": "Does the card's rule set confirm that Tomas has kept the promise to export the logo files on Friday, 18 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa99c5a8978",
  "kind": "yes/no",
  "text": "Client thread on the menu redesign, saved by Kai for the project log.\n\nMembers: Kai, Tess, Lee\nChat log (oldest first):\n[5 Apr 2026] Tess: @Kai Lovely, I'll collect the photo credits by 10 April 2026 for sure.\n[7 Apr 2026] Tess: @Lee Provided the packaging launch happens, I'll export the logo files by 14 April 2026.\n[9 Apr 2026] Lee: Fab, we are on for the packaging launch as planned!\n[10 Apr 2026] Tess: @Kai Apologies, I'll not be able to collect the photo credits\n[12 Apr 2026] Kai: @Tess You don't have to export the logo files at all",
  "question": "At the end of 18 April 2026, does the promise Tess made to export the logo files have any status except broken?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd319578ebe",
  "kind": "yes/no",
  "text": "Attached chat: the guest welcome plan\nForwarded by: Sami\n\nMembers: Dara, Sami, Ines, Mo\nChat log (oldest first):\n[2 Nov 2026] Dara: @Sami Count on me to wash the beach towels by Friday, 6 November 2026.\n[2 Nov 2026] Mo: @Dara Provided the guest arrival evening happens, I'll scrub the hot tub by Thursday, 5 November 2026.\n[2 Nov 2026] Ines: Yay, the guest arrival evening is all set to go!\n[3 Nov 2026] Mo: @Ines It's on me to change the lounge bulb by Monday, 9 November 2026.\n[5 Nov 2026] Mo: @Dara To my relief, I managed to scrub the hot tub.",
  "question": "Has Mo kept the promise to scrub the hot tub as of Monday, 9 November 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q78e11b8d24",
  "kind": "choice",
  "text": "Ines shared this to pin down the attic conversion idea, housemates.\n\nMembers: Oskar, Bruno, Ines, Zara\nChat export (date | from | to | message):\n2026-07-15 | Oskar | Ines | No promises, but I'll aim to sort the recycling bags by 21 July 2026.\n2026-07-17 | Oskar | Ines | Got it, I'll sort the recycling bags by 20 July 2026 for sure.\n2026-07-17 | Zara | Oskar | Nobody needs you to sort the recycling bags, that's that\n2026-07-21 | Oskar | Ines | To my relief, I managed to sort the recycling bags.\n2026-07-21 | Oskar | Bruno | As long as the lodger house supper is on, I'll cut a spare door key by 27 July 2026.\n2026-07-21 | Zara | Ines | I will defrost the top freezer by 24 July 2026 only if the lodger farewell supper happens.",
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
  "qid": "qd8cbb54d8a",
  "kind": "choice",
  "text": "Subject: Chat about the kitchen garden project\nThe copy from Malik follows below as a plain record.\n\nMembers: Femi, Wren, Malik, Sami\nChat log (oldest first):\n[14 Jan 2026] Malik: @Wren I'll water the allotment beds by 16 January 2026, promise.\n[15 Jan 2026] Wren: @Femi I will deliver the surplus runner beans by 18 January 2026 only if the plot inspection happens.\n[16 Jan 2026] Wren: Just so you know, the plot inspection is on as scheduled.\n[16 Jan 2026] Malik: @Wren Don't sweat it, there's no need to deliver the surplus runner beans\n[18 Jan 2026] Wren: @Femi For the record: I was able to deliver the surplus runner beans",
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
  "qid": "q13ce1baa16",
  "kind": "choice",
  "text": "Greta shared this back and forth with the client about the campaign edit.\n\nMembers: Greta, Ines, Leila, Ravi\nChat export (date | from | to | message):\n2026-06-15 | Greta | Ravi | Lovely, I'll upload the render files by Monday, 22 June 2026 for sure.\n2026-06-16 | Ravi | Ines | As long as the shoot day is on, I'll order the stock music licence by Thursday, 25 June 2026.\n2026-06-19 | Greta | Ravi | Might I ask whether I could upload the render files by Saturday, 27 June 2026 instead?\n2026-06-20 | Leila | Greta | Works for me, fine for you to upload the render files by Saturday, 27 June 2026.\n2026-06-21 | Greta | Ravi | You can bet I'll record the voice over by Wednesday, 24 June 2026.\n2026-06-24 | Greta | group | Quick heads up, the shoot day is scrapped.\n2026-06-26 | Greta | Ravi | My sincere apologies, I am unable to upload the render files.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Greta supposed to upload the render files by, going by the chat at the end of Wednesday, 24 June 2026 and any agreed changes?",
  "options": [
   "Monday, 22 June 2026",
   "Saturday, 27 June 2026",
   "Thursday, 25 June 2026"
  ]
 },
 {
  "qid": "q8013a3a3a9",
  "kind": "choice",
  "text": "Here we plan the allotment expansion together, and Nadia saved this for the family.\n\nMembers: Femi, Priya, Bruno, Nadia\nChat log (oldest first):\n[11 May 2026] Femi: @Priya Absolutely, I will collect the seed potatoes by 18 May 2026.\n[12 May 2026] Nadia: @Femi As long as the seed swap day is on, I'll weed the carrot row by 17 May 2026.\n[16 May 2026] Nadia: On track for the seed swap day to happen as planned.\n[17 May 2026] Nadia: @Femi Mind giving me until 20 May 2026 to weed the carrot row?\n[17 May 2026] Bruno: @Nadia Yes, lovely, you can weed the carrot row by 20 May 2026 instead!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Nadia's promise to weed the carrot row stand at the end of 17 May 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "qf86c15291e",
  "kind": "choice",
  "text": "Here we plan the street watch scheme together, and Kofi saved this for the family.\n\nMembers: Nadia, Lena, Tomas, Kofi\nChat log (oldest first):\n[31 Jan 2026] Tomas: @Lena I will make sure to walk the old spaniel by 8 Feb 2026.\n[3 Feb 2026] Kofi: @Tomas I will return the ladders by 5 Feb 2026.\n[3 Feb 2026] Lena: @Kofi Only if the parking permit visit is on, I will lock the side gate by 7 Feb 2026.\n[6 Feb 2026] Lena: Yep, the parking permit visit is on as planned.\n[6 Feb 2026] Nadia: @Lena Forget it, you won't need to lock the side gate\n[8 Feb 2026] Kofi: Hey, any luck with trying to lock the side gate?",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Lena's promise to lock the side gate turn out at the end of 7 Feb 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qcd0002b292",
  "kind": "choice",
  "text": "Subject: Saved chat on the volunteer roster\nHere is the export from Femi, for the record.\n\nMembers: Femi, Lena, Nadia, Ivo\nChat export (date | from | to | message):\n2026-07-25 | Lena | Nadia | I promise to book the school hall by 2026-07-29 if the summer fete is on.\n2026-07-26 | Nadia | Femi | I'll print the raffle tickets by 2026-07-31, promise.\n2026-07-27 | Ivo | Femi | I'll label the raffle prizes by 2026-07-31, provided the reading festival happens.\n2026-07-27 | Femi | Lena | I will make sure to set up the book stall by 2026-07-30.\n2026-07-27 | Femi | Lena | Can I set up the book stall by 2026-08-05 instead? I did promise, sorry.\n2026-07-30 | Femi | Lena | Quick report: I've managed to set up the book stall",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Femi's promise to set up the book stall turn out at the end of 2026-08-03?",
  "options": [
   "Not triggered",
   "Kept",
   "Waived",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qbfc63172ed",
  "kind": "choice",
  "text": "Subject: Chat about the campaign edit\nBelow is a copy that came from Ana, pasted as found.\n\nMembers: Ana, Jonas, Tess\nChat export (date | from | to | message):\n2026-07-14 | Jonas | Tess | I'll record the voice over by 21 Jul 2026 if the shoot day goes ahead.\n2026-07-15 | Ana | group | Just so you know, the shoot day is on as scheduled.\n2026-07-18 | Tess | Ana | I promise to export the subtitle files by 23 Jul 2026.\n2026-07-18 | Jonas | Tess | Think 26 Jul 2026 would work if I record the voice over instead?\n2026-07-19 | Tess | Ana | Lovely, I'll back up the project drives by 27 Jul 2026 for sure.\n2026-07-21 | Tess | Jonas | Relax, mate, you're not expected to record the voice over",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Jonas's undertaking to record the voice over hold at the end of 20 Jul 2026?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q0838ebfd02",
  "kind": "choice",
  "text": "Subject: Chat about the campaign edit\nBelow is a copy that came from Ana, pasted as found.\n\nMembers: Ana, Jonas, Tess\nChat export (date | from | to | message):\n2026-07-14 | Jonas | Tess | I'll record the voice over by 21 Jul 2026 if the shoot day goes ahead.\n2026-07-15 | Ana | group | Just so you know, the shoot day is on as scheduled.\n2026-07-18 | Tess | Ana | I promise to export the subtitle files by 23 Jul 2026.\n2026-07-18 | Jonas | Tess | Think 26 Jul 2026 would work if I record the voice over instead?\n2026-07-19 | Tess | Ana | Lovely, I'll back up the project drives by 27 Jul 2026 for sure.\n2026-07-21 | Tess | Jonas | Relax, mate, you're not expected to record the voice over",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Jonas's undertaking to record the voice over hold at the end of 21 Jul 2026?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q12365e0c07",
  "kind": "choice",
  "text": "Shared by Bruno, a help-desk thread covering the guest welcome plan.\n\nMembers: Oskar, Femi, Kai, Bruno\nChat log (oldest first):\n[28 May 2026] Oskar: @Femi Promise to scrub the hot tub by 30 May 2026 if the check out clean goes ahead.\n[29 May 2026] Oskar: @Kai You can bet I'll change the lounge bulb by 1 June 2026.\n[31 May 2026] Kai: @Oskar I'll wash the beach towels by 9 June 2026, providing the summer season launch goes ahead.\n[1 Jun 2026] Bruno: Any news on plans to change the lounge bulb?\n[1 Jun 2026] Bruno: @Oskar No need to change the lounge bulb, I'm letting you off\n[1 Jun 2026] Femi: @Bruno I will make sure to wheel the bins out by 8 June 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Oskar's promise to change the lounge bulb at the end of 1 June 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q53be8e66ac",
  "kind": "choice",
  "text": "Ravi shared this support thread, which is about the family history.\n\nMembers: Ravi, Bruno, Wren, Ivo\nChat log (oldest first):\n[18 Mar 2026] Wren: Hoping to collect the old photo prints by 2026-03-22, but can't promise.\n[18 Mar 2026] Wren: @Bruno I will make sure to set up the slideshow laptop by 2026-03-26.\n[20 Mar 2026] Wren: @Bruno I'll collect the old photo prints by 2026-03-28, providing the garden picnic goes ahead.\n[22 Mar 2026] Ravi: @Wren Relax, mate, you're not expected to set up the slideshow laptop\n[26 Mar 2026] Wren: Yay, the garden picnic is all set to go!\n[28 Mar 2026] Ivo: @Wren No need to collect the old photo prints, I'm letting you off",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Wren's promise to collect the old photo prints stand at the end of 2026-03-30?",
  "options": [
   "Not yet due",
   "Broken",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "qed3e70e7aa",
  "kind": "choice",
  "text": "Here is the plan for the family day out, saved by Nadia for the group.\n\nMembers: Nadia, Ivo, Zara\nChat log (oldest first):\n[17 Jul 2026] Zara: @Ivo I'll pack the picnic basket by 20 July 2026 as long as the puppet show is on.\n[18 Jul 2026] Zara: @Ivo I promise to fetch the craft box by 24 July 2026.\n[22 Jul 2026] Zara: @Ivo Provided the sleepover weekend happens, I'll read the bedtime story by 26 July 2026.\n[22 Jul 2026] Ivo: @Nadia I'll be sure to teach the card game by 25 July 2026.\n[24 Jul 2026] Nadia: Lovely, the sleepover weekend is definitely happening!\n[25 Jul 2026] Ivo: @Nadia Got myself to teach the card game lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Ivo's promise to teach the card game at the end of 27 July 2026?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q8bde053f3d",
  "kind": "yes/no",
  "text": "Hana forwarded this for the committee as we dig in on the choir tour.\n\nMembers: Bruno, Hana, Jonas\nChat log (oldest first):\n[29 May 2026] Bruno: Might be able to fetch the choir robes by 10 June 2026, who knows!\n[31 May 2026] Bruno: @Hana You can bank on me to fetch the choir robes by 7 June 2026.\n[2 Jun 2026] Bruno: @Hana I own this, I'll fix the stand microphones by 8 June 2026.\n[3 Jun 2026] Bruno: @Hana Count on me to collect the sheet music by 11 June 2026, if the sing along happens.\n[6 Jun 2026] Bruno: @Hana Guess who managed to fetch the choir robes, go team!\n[10 Jun 2026] Jonas: Sadly, the sing along won't go ahead.",
  "question": "Would you say Bruno kept the promise to fetch the choir robes at the end of 6 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe64b87196c",
  "kind": "yes/no",
  "text": "Messages with the letting agent about the summer lets season, forwarded by Nadia for the rental file.\n\nMembers: Mo, Nadia, Lena\nChat log (oldest first):\n[23 Sep 2026] Nadia: @Lena Promise to air the spare room by 27 Sep 2026 if the lettings photo shoot goes ahead.\n[23 Sep 2026] Mo: @Nadia Count on me, I'll wheel the bins out by 30 Sep 2026.\n[25 Sep 2026] Nadia: @Mo I promise to restock the guest toiletries by 1 Oct 2026 if the summer season launch is on.\n[28 Sep 2026] Lena: @Mo You can bet I'll vacuum the holiday cottage by 1 Oct 2026.\n[1 Oct 2026] Mo: @Nadia Ticked off: wheel the bins out, feels so good",
  "question": "Does the card classify Mo's promise to wheel the bins out as kept, instead of broken, waived, not triggered or not yet due, on 29 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q39254f99b5",
  "kind": "choice",
  "text": "Attached chat: the shared kitchen scheme\nForwarded by: Malik\n\nMembers: Malik, Leila, Oskar, Ana\nChat log (oldest first):\n[7 Oct 2026] Malik: @Leila Lovely, I'll feed the house plants by 15 Oct 2026 for sure.\n[11 Oct 2026] Leila: @Ana Count on me to cut a spare door key by 17 Oct 2026, if the landlord inspection walk happens.\n[14 Oct 2026] Oskar: I'm aiming to replace the loo roll by 19 Oct 2026, might manage it.\n[15 Oct 2026] Malik: @Leila I'll defrost the top freezer by 17 Oct 2026, provided the house insurance review happens.\n[15 Oct 2026] Oskar: @Malik I'll be sure to replace the loo roll by 18 Oct 2026.\n[17 Oct 2026] Oskar: @Malik Would it be fine if I replace the loo roll by 24 Oct 2026 instead, yeah?\n[18 Oct 2026] Malik: @Oskar The original date stands, so you need to replace the loo roll.\n[18 Oct 2026] Leila: @Oskar Forget it, you won't need to replace the loo roll",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs things stand at the end of 31 Oct 2026, which date is the deadline for Oskar to replace the loo roll, with any agreed change applied?",
  "options": [
   "17 Oct 2026",
   "24 Oct 2026",
   "18 Oct 2026"
  ]
 },
 {
  "qid": "qbf2efa7290",
  "kind": "yes/no",
  "text": "Volunteers, here is the playground project thread that Tomas forwarded for us.\n\nMembers: Kofi, Tomas, Ana\nChat export (date | from | to | message):\n2026-02-01 | Tomas | group | See if I can collect the bake sale tins by 7 Feb 2026.\n2026-02-02 | Tomas | Kofi | Got it, I'll collect the bake sale tins by 10 Feb 2026 for sure.\n2026-02-04 | Ana | Kofi | I assure you I'll label the raffle prizes by 7 Feb 2026 if the governors meeting is on.\n2026-02-06 | Ana | group | Great news, the governors meeting is on!\n2026-02-06 | Ana | Tomas | Forget it, you won't need to collect the bake sale tins\n2026-02-11 | Tomas | Kofi | Log entry: collect the bake sale tins, carried out",
  "question": "Per the rules on the card, at the end of 12 Feb 2026, has the promise Tomas made to collect the bake sale tins been broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6fc714a1cc",
  "kind": "choice",
  "text": "Chat attached to a support case about the platform rewrite, shared by Omar.\n\nMembers: Leila, Omar, Jonas\nChat log (oldest first):\n[8 May 2026] Omar: @Jonas Provided the planning session happens, I will label the bug reports by 12 May 2026.\n[9 May 2026] Jonas: @Leila Count on me, I'll restart the build server by 15 May 2026.\n[11 May 2026] Leila: Sadly, the planning session won't go ahead.\n[11 May 2026] Jonas: @Omar Absolutely, I will run the security scan by 19 May 2026.\n[19 May 2026] Jonas: @Omar Guess who managed to run the security scan, go team!\n[20 May 2026] Omar: Any idea how close you are to run the security scan?",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Jonas made to run the security scan at the end of 19 May 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "qfc85f7e4e4",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the big house plan\nFrom Elif, the thread below is shared as it stands.\n\nMembers: Sami, Greta, Elif, Ines\nChat log (oldest first):\n[18 Aug 2026] Sami: @Greta I'll replace the hallway bulbs by 25 August 2026 as long as the house viewing is on.\n[22 Aug 2026] Elif: @Sami Guaranteed I'll clear the kitchen sink by 26 August 2026.\n[23 Aug 2026] Ines: Update: the house viewing is going ahead as planned.\n[28 Aug 2026] Elif: @Sami Ta-da, I went and did it: clear the kitchen sink!\n[28 Aug 2026] Sami: @Greta Ta-da, I went and did it: replace the hallway bulbs!",
  "question": "Is Sami's promise to replace the hallway bulbs kept as of 26 August 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qaf4465df4b",
  "kind": "yes/no",
  "text": "Subject: Saved chat on the home adaptations\nHere is the export from Femi, for the record.\n\nMembers: Tomas, Hana, Femi\nChat log (oldest first):\n[18 Jul 2026] Femi: @Hana You can bet I'll drop off the hot meals by 21 July 2026.\n[19 Jul 2026] Femi: @Hana I regret to say that I shall not drop off the hot meals.\n[20 Jul 2026] Femi: @Tomas I'll print the care schedule by 26 July 2026, provided the home assessment happens.\n[25 Jul 2026] Hana: Afraid the home assessment is called off.\n[26 Jul 2026] Femi: @Tomas Is it all right if I print the care schedule by 1 August 2026 instead?\n[26 Jul 2026] Hana: @Femi Revised deadline is 1 August 2026, so you can print the care schedule.",
  "question": "Going by the card's rules, does Femi keep the promise to print the care schedule at the end of 27 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qda2649c773",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the field survey\nThe thread below comes from Ines and is passed on as it is.\n\nMembers: Dara, Ines, Zara, Kofi\nChat log (oldest first):\n[20 Sep 2026] Zara: @Dara Hoping to book the microscope slot by 30 Sep 2026, no promises.\n[22 Sep 2026] Zara: @Ines If the conference trip is on, I'll definitely book the microscope slot by 29 Sep 2026.\n[22 Sep 2026] Zara: @Ines Got it, I'll collect the lab samples by 30 Sep 2026 for sure.\n[23 Sep 2026] Kofi: @Zara Guaranteed I'll fetch the grant forms by 25 Sep 2026.\n[23 Sep 2026] Kofi: We are dropping the conference trip from the list.\n[24 Sep 2026] Dara: @Ines I will order the reagent kit by 27 Sep 2026.",
  "question": "Has Zara's promise to book the microscope slot ended up broken, waived, not triggered or not yet due, instead of kept, as of 2 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9c406542de",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the garden shed build\nFrom Leila, the thread below is shared as it stands.\n\nMembers: Leila, Femi, Greta\nChat export (date | from | to | message):\n2026-06-02 | Femi | Greta | Lovely, I'll build the compost bay by 10 June 2026 if the village flower show is on.\n2026-06-04 | Leila | group | Sadly, the village flower show won't go ahead.\n2026-06-04 | Leila | Greta | I'll be sure to water the allotment beds by 11 June 2026.\n2026-06-05 | Greta | Leila | Count on me, I'll dig the potato patch by 13 June 2026.\n2026-06-08 | Leila | Greta | Update on my side: I will not water the allotment beds, sorry.\n2026-06-15 | Greta | Leila | To my relief, I managed to dig the potato patch.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status does the chat show for the promise Femi made to build the compost bay at the end of 13 June 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Broken",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "qab8f7b3707",
  "kind": "yes/no",
  "text": "Client thread on the store makeover, shared by Hana for the project log.\n\nMembers: Nadia, Hana\nChat log (oldest first):\n[14 Jan 2026] Hana: @Nadia Lovely, I'll send the moodboard files by Friday, 16 January 2026 if the brand review call is on.\n[18 Jan 2026] Hana: @Nadia You can bet I'll pick the colour swatches by Saturday, 24 January 2026.\n[20 Jan 2026] Hana: @Nadia Lovely, I'll update the icon set by Thursday, 22 January 2026 if the sign reveal is on.\n[20 Jan 2026] Hana: Great news, the sign reveal is on!\n[20 Jan 2026] Nadia: @Hana It's on me to sketch the packaging mockup by Monday, 26 January 2026.\n[26 Jan 2026] Hana: @Nadia Quick report: I've managed to pick the colour swatches",
  "question": "Was Hana's promise to pick the colour swatches not kept as of Wednesday, 28 January 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6e671bf9c6",
  "kind": "choice",
  "text": "Omar shared this so the annual tour is easy to follow for the volunteers.\n\nMembers: Hana, Omar, Bruno\nChat log (oldest first):\n[23 Apr 2026] Hana: @Bruno Ticket's mine, I'll collect the timing tags by 26 April 2026.\n[25 Apr 2026] Hana: @Bruno Scratch that, I'm not going to collect the timing tags\n[26 Apr 2026] Omar: @Hana Promise to tune the gear cables by 3 May 2026 if the group ride goes ahead.\n[28 Apr 2026] Omar: Please note the group ride will proceed.\n[30 Apr 2026] Omar: @Hana Ticked off: tune the gear cables, feels so good",
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
  "qid": "qce75352dac",
  "kind": "choice",
  "text": "Shared by Ravi from the work chat, with the office refit at its heart.\n\nMembers: Priya, Ravi, Ines, Leila\nChat log (oldest first):\n[6 Feb 2026] Ravi: @Leila I own this, I'll return the printer toner by 10 February 2026.\n[7 Feb 2026] Ines: @Priya I will renew the fire extinguisher service by 14 February 2026 only if the team lunch happens.\n[8 Feb 2026] Priya: Yep, the team lunch is on as planned.\n[9 Feb 2026] Ravi: @Leila Ta-da, I went and did it: return the printer toner!\n[10 Feb 2026] Priya: @Ines I own this, I'll collect the visitor badges by 17 February 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Ines's promise to renew the fire extinguisher service receive at the end of 15 February 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not yet due",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qe95d2492a9",
  "kind": "choice",
  "text": "Shared by Bruno, this back and forth with the client covers the wedding weekend.\n\nMembers: Bruno, Oskar, Tomas\nChat log (oldest first):\n[1 Sep 2026] Tomas: @Oskar As long as the bridal shower is on, I'll fetch the spare memory cards by 9 September 2026.\n[3 Sep 2026] Bruno: @Tomas I will make sure to set up the backdrop frame by 10 September 2026.\n[4 Sep 2026] Bruno: Brilliant news everyone, the bridal shower is a go!\n[7 Sep 2026] Tomas: @Oskar Can I fetch the spare memory cards by 12 September 2026 instead? I did promise, sorry.\n[8 Sep 2026] Bruno: @Tomas I'm withdrawing my promise to set up the backdrop frame",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Tomas's promise to fetch the spare memory cards at the end of 6 September 2026?",
  "options": [
   "Waived",
   "Kept",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q23076e8dc2",
  "kind": "yes/no",
  "text": "Shared by Leila for the committee, this is the group chat on the junior section.\n\nMembers: Ivo, Ana, Leila\nChat log (oldest first):\n[6 Jul 2026] Ana: @Leila Count on me to set up the corner flags by 15 Jul 2026.\n[9 Jul 2026] Ana: @Ivo Count on me to return the bib sets by 14 Jul 2026.\n[14 Jul 2026] Leila: @Ana As long as the cup tie is on, I will pump the match balls by 21 Jul 2026.\n[16 Jul 2026] Ana: @Ivo Mum, I did return the bib sets, haha.\n[17 Jul 2026] Ivo: Team, the cup tie is not happening.",
  "question": "At the end of 14 Jul 2026, has the promise Ana made to return the bib sets been broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6d180489ac",
  "kind": "choice",
  "text": "Here we plan the care plan together, and Ravi saved this for the family.\n\nMembers: Leila, Ivo, Ravi, Tomas\nChat log (oldest first):\n[11 Jul 2026] Ravi: @Tomas Fingers crossed I can drop off the hot meals by Tuesday, 21 July 2026.\n[12 Jul 2026] Ravi: @Leila Relax, I'll drop off the hot meals by Monday, 20 July 2026 for sure.\n[14 Jul 2026] Ravi: @Leila Think Sunday, 26 July 2026 would work if I drop off the hot meals instead?\n[19 Jul 2026] Ivo: @Ravi Yes, you can drop off the hot meals by Sunday, 26 July 2026 if that suits you.\n[25 Jul 2026] Leila: @Ravi Relax, I'll set up the medicine dispenser by Tuesday, 28 July 2026, promise.\n[27 Jul 2026] Tomas: @Ravi I assure you I'll return the hospital bed by Thursday, 30 July 2026 if the eye test is on.\n[29 Jul 2026] Ravi: Quick heads up, the eye test is scrapped.\n[30 Jul 2026] Ravi: @Leila Quick report: I've managed to drop off the hot meals",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo what's the latest day Ravi has to drop off the hot meals by at the end of Saturday, 25 July 2026, given any new date people agreed to?",
  "options": [
   "Monday, 20 July 2026",
   "Sunday, 26 July 2026",
   "Tuesday, 28 July 2026"
  ]
 },
 {
  "qid": "q541d2d083a",
  "kind": "choice",
  "text": "Malik saved this so we stay on the same page about the vegetable plot plan, mates.\n\nMembers: Femi, Ines, Malik, Leila\nChat log (oldest first):\n[14 Jan 2026] Ines: @Femi Provided the water tank delivery happens, I will build the compost bay by 21 Jan 2026.\n[15 Jan 2026] Femi: Sadly, the water tank delivery won't go ahead.\n[17 Jan 2026] Ines: @Femi You can bank on me to stake the tomato canes by 23 Jan 2026.\n[17 Jan 2026] Malik: @Ines Please don't feel you have to stake the tomato canes\n[17 Jan 2026] Ines: @Femi For the record: I was able to stake the tomato canes",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Ines made to stake the tomato canes have at the end of 22 Jan 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q06932f1f9f",
  "kind": "yes/no",
  "text": "Subject: Chat about the garden makeover\nBelow, with Priya named as the source, is the chat as exported.\n\nMembers: Priya, Tess, Lena\nChat log (oldest first):\n[29 May 2026] Priya: @Tess I'll measure the hallway for shelves by 5 Jun 2026, providing the kitchen fitting day goes ahead.\n[30 May 2026] Tess: Fab, we are on for the kitchen fitting day as planned!\n[30 May 2026] Tess: @Lena Relax, I'll fetch the paint samples by 7 Jun 2026, promise.\n[31 May 2026] Tess: @Lena Count on me, I'll print the floor plan by 7 Jun 2026.\n[31 May 2026] Tess: @Lena Apologies, I'll not be able to print the floor plan\n[8 Jun 2026] Priya: @Tess Log entry: measure the hallway for shelves, carried out",
  "question": "Is the promise to measure the hallway for shelves that Priya made broken at the end of 9 Jun 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q68f7570184",
  "kind": "yes/no",
  "text": "Committee chat on the training plan, forwarded by Yuki to the volunteers.\n\nMembers: Leila, Arlo, Yuki\nChat log (oldest first):\n[1 May 2026] Leila: @Yuki I will make sure to return the loaned helmets by 8 May 2026.\n[4 May 2026] Arlo: @Leila Provided the group ride happens, I will collect the timing tags by 13 May 2026.\n[4 May 2026] Yuki: @Leila Committing to set up the feed stop by 11 May 2026.\n[8 May 2026] Yuki: @Leila To my relief, I managed to set up the feed stop.\n[10 May 2026] Leila: Sadly, the group ride won't go ahead.",
  "question": "Is Yuki's promise to set up the feed stop broken at the end of 12 May 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4e56c3e335",
  "kind": "yes/no",
  "text": "Forwarded by Mo, these tenant replies are about the kitchen refit for the file.\n\nMembers: Wren, Lee, Mo\nChat log (oldest first):\n[13 Mar 2026] Wren: @Mo As long as the electrics safety check is on, I'll collect the spare flat keys by 15 March 2026.\n[13 Mar 2026] Lee: Sadly, the electrics safety check won't go ahead.\n[18 Mar 2026] Lee: @Mo I will make sure to remove the bathroom shelf by 24 March 2026.\n[21 Mar 2026] Wren: @Lee Count on me, I'll forward the gas bill by 26 March 2026.\n[24 Mar 2026] Lee: @Mo Got myself to remove the bathroom shelf lol.\n[26 Mar 2026] Mo: Checking you mean to remove the bathroom shelf?",
  "question": "Would you say Lee didn't keep the promise to remove the bathroom shelf by the end of 24 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q800c0f2d02",
  "kind": "choice",
  "text": "Forwarded by Ana: a help-desk thread covering the spare room plan.\n\nMembers: Tomas, Bruno, Ana\nChat export (date | from | to | message):\n2026-02-25 | Tomas | Bruno | Got it, I'll defrost the top freezer by 2 March 2026 for sure.\n2026-02-25 | Bruno | group | Thanks mate, noted.\n2026-03-01 | Tomas | Bruno | On my action item, may I defrost the top freezer by 6 March 2026 instead?\n2026-03-01 | Bruno | Tomas | Fine by me, you can defrost the top freezer by 6 March 2026.\n2026-03-04 | Bruno | Ana | Provided the water tank check happens, I'll wipe the shared kitchen counter by 9 March 2026.\n2026-03-05 | Tomas | Bruno | Quick report: I've managed to defrost the top freezer\n2026-03-06 | Ana | Tomas | Provided the house insurance review happens, I'll replace the loo roll by 8 March 2026.\n2026-03-07 | Bruno | Tomas | Ticket's mine, I'll feed the house plants by 11 March 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Tomas due to defrost the top freezer at the end of 7 March 2026, after any agreed rescheduling?",
  "options": [
   "9 March 2026",
   "6 March 2026",
   "2 March 2026"
  ]
 },
 {
  "qid": "qd36c1df4c4",
  "kind": "yes/no",
  "text": "Yo flatmates, Zara shared this chat about the cellar project, so chip in.\n\nMembers: Nadia, Arlo, Zara\nChat log (oldest first):\n[4 May 2026] Zara: @Arlo Count on me, I'll mend the garden gate by 9 May 2026.\n[4 May 2026] Nadia: @Zara I'm aiming to replace the hallway bulbs by 14 May 2026, might manage it.\n[6 May 2026] Nadia: @Arlo If the heritage fete is on, I'll definitely replace the hallway bulbs by 13 May 2026.\n[6 May 2026] Arlo: On track for the heritage fete to happen as planned.\n[10 May 2026] Nadia: @Arlo I promise to wash the sash windows by 19 May 2026.\n[12 May 2026] Nadia: @Arlo Guess who managed to replace the hallway bulbs, go team!",
  "question": "Does Nadia's promise to replace the hallway bulbs hold up as kept at the end of 15 May 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q945ec4fd8e",
  "kind": "choice",
  "text": "Casual chat for the flat, saved by Sami, and it covers the loft conversion.\n\nMembers: Sami, Ravi, Tomas, Oskar\nChat export (date | from | to | message):\n2026-04-05 | Oskar | Ravi | I will scrape the old wallpaper by 9 Apr 2026 only if the kitchen fitting day happens.\n2026-04-05 | Tomas | Sami | Ticket's mine, I'll hang the new curtain rail by 11 Apr 2026.\n2026-04-07 | Tomas | Sami | I'm withdrawing my promise to hang the new curtain rail\n2026-04-08 | Tomas | group | Please note the kitchen fitting day will proceed.\n2026-04-09 | Sami | Oskar | No need to scrape the old wallpaper, I'm letting you off",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Oskar's promise to scrape the old wallpaper at the end of 12 Apr 2026?",
  "options": [
   "Waived",
   "Kept",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 }
]
