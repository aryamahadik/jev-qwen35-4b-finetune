# G5-H blind read T32-blind_read-a3cde981-007 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T32/qc/g5h/answers/T32-blind_read-a3cde981-007.json

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
  "qid": "q97f59811de",
  "kind": "yes/no",
  "text": "Here is the plan for the care plan, saved by Ivo for the group.\n\nMembers: Kofi, Nadia, Ana, Ivo\nChat log (oldest first):\n[11 Jul 2026] Ivo: @Ana I assure you I'll call the home nurse by 14 July 2026 if the carer handover is on.\n[13 Jul 2026] Ivo: Really pleased to say the carer handover will go ahead!\n[14 Jul 2026] Kofi: @Ivo You can bank on me to collect the post by 22 July 2026.\n[14 Jul 2026] Ivo: @Ana I need to take back my commitment to call the home nurse.\n[16 Jul 2026] Nadia: @Ivo If the physio session goes ahead, I'll gladly pick up the repeat prescription by 19 July 2026.\n[20 Jul 2026] Kofi: @Ivo Guess what, I managed to collect the post!",
  "question": "Applying the rules on the card, can Ivo's promise to call the home nurse be said to have not been broken at the end of 15 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7c8b288e20",
  "kind": "choice",
  "text": "Ravi shared this support thread, which is about the family history.\n\nMembers: Ravi, Bruno, Wren, Ivo\nChat log (oldest first):\n[18 Mar 2026] Wren: Hoping to collect the old photo prints by 2026-03-22, but can't promise.\n[18 Mar 2026] Wren: @Bruno I will make sure to set up the slideshow laptop by 2026-03-26.\n[20 Mar 2026] Wren: @Bruno I'll collect the old photo prints by 2026-03-28, providing the garden picnic goes ahead.\n[22 Mar 2026] Ravi: @Wren Relax, mate, you're not expected to set up the slideshow laptop\n[26 Mar 2026] Wren: Yay, the garden picnic is all set to go!\n[28 Mar 2026] Bruno: @Wren No need to collect the old photo prints, I'm letting you off",
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
  "qid": "q52398ac3c2",
  "kind": "choice",
  "text": "Shared by Arlo, an export of a household chat about the cellar project, as saved.\n\nMembers: Arlo, Yuki, Tess\nChat log (oldest first):\n[16 Apr 2026] Arlo: I'll try to wash the sash windows by 20 April 2026, no guarantee.\n[18 Apr 2026] Arlo: @Yuki Relax, I'll wash the sash windows by 23 April 2026 for sure.\n[21 Apr 2026] Arlo: @Yuki I committed to wash the sash windows, can I do that by 25 April 2026 instead?\n[22 Apr 2026] Tess: @Arlo Fine by me, you can wash the sash windows by 25 April 2026.\n[23 Apr 2026] Arlo: @Yuki Got myself to wash the sash windows lol.\n[24 Apr 2026] Arlo: @Tess As long as the heritage fete is on, I will tidy the boot room by 27 April 2026.\n[24 Apr 2026] Yuki: @Tess I will scrub the cellar steps by 27 April 2026.\n[25 Apr 2026] Yuki: Just so you know, the heritage fete is on as scheduled.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Arlo due to wash the sash windows at the end of 26 April 2026, after any agreed rescheduling?",
  "options": [
   "27 April 2026",
   "23 April 2026",
   "25 April 2026"
  ]
 },
 {
  "qid": "q522e25c4c5",
  "kind": "choice",
  "text": "Shared by Priya, a help-desk thread covering the summer lets season.\n\nMembers: Priya, Kai, Elif\nChat export (date | from | to | message):\n2026-06-18 | Kai | Priya | I promise to wash the beach towels by Thursday, June 25, 2026.\n2026-06-20 | Kai | Priya | Would it be fine if I wash the beach towels by Tuesday, June 30, 2026 instead, yeah?\n2026-06-23 | Priya | Kai | Works for me, fine for you to wash the beach towels by Tuesday, June 30, 2026.\n2026-06-25 | Elif | Priya | If the owner handover visit is on, I'll definitely collect the bed linen by Saturday, July 4, 2026.\n2026-06-27 | Priya | Kai | Promise to fill the cleaning cupboard by Wednesday, July 1, 2026 if the lettings photo shoot goes ahead.\n2026-06-28 | Kai | Priya | Ticked off my list: wash the beach towels, yay.\n2026-06-30 | Kai | Elif | I'll be sure to restock the guest toiletries by Sunday, July 5, 2026.\n2026-07-03 | Priya | group | Sorry all, the owner handover visit is called off.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs things stand at the end of Sunday, June 28, 2026, which date is the deadline for Kai to wash the beach towels, with any agreed change applied?",
  "options": [
   "Thursday, June 25, 2026",
   "Tuesday, June 30, 2026",
   "Saturday, July 4, 2026"
  ]
 },
 {
  "qid": "qb89e5b9347",
  "kind": "yes/no",
  "text": "Yo flatmates, Kofi shared this chat about the house refit, so chip in.\n\nMembers: Ana, Leila, Kofi\nChat log (oldest first):\n[17 Sep 2026] Ana: @Kofi Relax, I'll scrape the old wallpaper by 23 September 2026, promise.\n[18 Sep 2026] Ana: @Kofi Count on me, I'll pay the plumbing invoice by 27 September 2026.\n[19 Sep 2026] Leila: @Ana I'll fetch the paint samples by 26 September 2026, provided the boiler install visit happens.\n[21 Sep 2026] Ana: @Kofi Guess what, I managed to scrape the old wallpaper!\n[22 Sep 2026] Kofi: @Ana I assure you I'll return the tile cutter by 29 September 2026 if the mortgage valuation visit is on.\n[28 Sep 2026] Ana: Quick heads up, the mortgage valuation visit is scrapped.",
  "question": "Has Ana kept the promise to scrape the old wallpaper at the end of 26 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q39e62b6a6b",
  "kind": "choice",
  "text": "Committee chat on the music library, shared by Lee with the volunteers.\n\nMembers: Lee, Mo, Malik\nChat log (oldest first):\n[17 Jan 2026] Mo: @Malik Count on me, I'll set up the sound desk by 25 Jan 2026.\n[18 Jan 2026] Lee: @Mo I'll collect the sheet music by 24 Jan 2026, promise.\n[18 Jan 2026] Lee: @Malik I'll buy the spare folders by 27 Jan 2026 as long as the joint concert is on.\n[23 Jan 2026] Malik: @Lee You are released, no requirement to collect the sheet music.\n[23 Jan 2026] Mo: Really pleased to say the joint concert will go ahead!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Lee made to collect the sheet music have at the end of 25 Jan 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Broken",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "qdb904b9373",
  "kind": "choice",
  "text": "Here we plan the care plan together, and Ravi saved this for the family.\n\nMembers: Leila, Ivo, Ravi, Tomas\nChat log (oldest first):\n[11 Jul 2026] Ravi: @Tomas Fingers crossed I can drop off the hot meals by Tuesday, 21 July 2026.\n[12 Jul 2026] Ravi: @Leila Relax, I'll drop off the hot meals by Monday, 20 July 2026 for sure.\n[14 Jul 2026] Ravi: @Leila Think Sunday, 26 July 2026 would work if I drop off the hot meals instead?\n[19 Jul 2026] Tomas: @Ravi Yes, you can drop off the hot meals by Sunday, 26 July 2026 if that suits you.\n[25 Jul 2026] Leila: @Ravi Relax, I'll set up the medicine dispenser by Tuesday, 28 July 2026, promise.\n[27 Jul 2026] Tomas: @Ravi I assure you I'll return the hospital bed by Thursday, 30 July 2026 if the eye test is on.\n[29 Jul 2026] Ravi: Quick heads up, the eye test is scrapped.\n[30 Jul 2026] Ravi: @Leila Quick report: I've managed to drop off the hot meals",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo what's the latest day Ravi has to drop off the hot meals by at the end of Saturday, 25 July 2026, given any new date people agreed to?",
  "options": [
   "Tuesday, 28 July 2026",
   "Monday, 20 July 2026",
   "Sunday, 26 July 2026"
  ]
 },
 {
  "qid": "qa0445ee18f",
  "kind": "yes/no",
  "text": "Subject: the menu redesign\nBelow is the group chat that Rhea saved, unedited.\n\nMembers: Wren, Ines, Rhea\nChat log (oldest first):\n[2 Apr 2026] Wren: @Rhea Lovely, I'll sketch the packaging mockup by 2026-04-08 if the sign reveal is on.\n[4 Apr 2026] Ines: @Rhea I'm aiming to export the logo files by 2026-04-14, might manage it.\n[4 Apr 2026] Wren: @Rhea Absolutely, I will upload the sticker artwork by 2026-04-12.\n[5 Apr 2026] Ines: @Rhea I promise to export the logo files by 2026-04-10.\n[8 Apr 2026] Ines: @Rhea Provided the print run happens, I'll fetch the brand fonts by 2026-04-12.\n[9 Apr 2026] Wren: @Ines You don't have to export the logo files at all",
  "question": "Has Ines kept the promise to export the logo files at the end of 2026-04-10?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1f27ad7f22",
  "kind": "yes/no",
  "text": "Note above a chat from the support case, covering the sound mix, shared by Hana.\n\nMembers: Elif, Tess, Hana\nChat export (date | from | to | message):\n2026-01-22 | Tess | Hana | I will ship the hard drive by 24 January 2026.\n2026-01-25 | Tess | Elif | As long as the shoot day is on, I will record the voice over by 28 January 2026.\n2026-01-25 | Elif | group | Thanks for the heads up.\n2026-01-25 | Tess | group | Team, the shoot day stays on as booked.\n2026-01-26 | Tess | Hana | Count on me to fetch the raw footage by 1 February 2026.\n2026-01-29 | Tess | Hana | Change of plans: I will not fetch the raw footage",
  "question": "Has Tess not kept the promise to record the voice over at the end of 26 January 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2d4406b060",
  "kind": "choice",
  "text": "Extract of the club chat on the new kit design, copied by Jonas for the group.\n\nMembers: Yuki, Kai, Hana, Jonas\nChat log (oldest first):\n[1 Jun 2026] Hana: @Yuki I'll print the route cards by 5 Jun 2026, provided the club sportive happens.\n[3 Jun 2026] Yuki: @Hana Got it, I'll pump the spare tyres by 8 Jun 2026 for sure.\n[4 Jun 2026] Jonas: @Kai Provided the hill climb happens, I'll service the tandem bike by 9 Jun 2026.\n[5 Jun 2026] Jonas: @Kai Relax, I'll return the loaned helmets by 11 Jun 2026 for sure.\n[6 Jun 2026] Kai: Fab, we are on for the hill climb as planned!\n[7 Jun 2026] Hana: @Yuki You are released, no requirement to pump the spare tyres.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Yuki's promise to pump the spare tyres at the end of 12 Jun 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q45bd45ceb5",
  "kind": "choice",
  "text": "Zara saved these exchanges with the agent about the summer lets season.\n\nMembers: Mo, Zara, Omar, Lena\nChat log (oldest first):\n[1 Jul 2026] Omar: @Lena Provided the guest arrival evening happens, I will collect the bed linen by 2026-07-04.\n[3 Jul 2026] Zara: @Lena I'll be sure to wash the beach towels by 2026-07-07.\n[5 Jul 2026] Zara: @Omar Only if the summer season launch is on, I will leave the welcome basket by 2026-07-08.\n[6 Jul 2026] Zara: @Lena I'll be sure to wheel the bins out by 2026-07-12.\n[11 Jul 2026] Zara: @Lena I regret to say that I shall not wheel the bins out.\n[12 Jul 2026] Omar: @Zara Good news, you're let off having to wheel the bins out",
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
  "qid": "q49533b8176",
  "kind": "choice",
  "text": "Channel title: work team chat\nDescription: about the website relaunch, exported by Kofi.\n\nMembers: Rhea, Kofi, Jonas, Kai\nChat export (date | from | to | message):\n2026-02-16 | Kai | Jonas | You can bank on me to book the photo studio by 22 Feb 2026.\n2026-02-18 | Rhea | Kofi | Count on me to fetch the campaign budget sheet by 23 Feb 2026 if the annual review is on.\n2026-02-22 | Kai | Jonas | Mind giving me until 28 Feb 2026 to book the photo studio?\n2026-02-22 | Rhea | Kai | Yes, fine to book the photo studio by 28 Feb 2026 instead.\n2026-02-23 | Kai | Rhea | I assure you I'll fix the landing page headline by 26 Feb 2026 if the product launch is on.\n2026-02-24 | Kofi | Kai | Good news, you're let off having to book the photo studio\n2026-02-27 | Kai | Jonas | To my relief, I managed to book the photo studio.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 24 Feb 2026, by what date does Kai have to book the photo studio, counting any agreed change of date?",
  "options": [
   "23 Feb 2026",
   "22 Feb 2026",
   "28 Feb 2026"
  ]
 },
 {
  "qid": "q5dd0d30939",
  "kind": "yes/no",
  "text": "Client messages for a freelancer about the sound mix, saved by Priya.\n\nMembers: Bruno, Tess, Priya, Kofi\nChat export (date | from | to | message):\n2026-09-18 | Priya | Bruno | Relax, I'll send the colour notes by 23 Sep 2026 for sure.\n2026-09-23 | Bruno | Tess | I promise to ship the hard drive by 26 Sep 2026.\n2026-09-23 | Tess | Priya | Provided the client screening happens, I will label the clip folders by 29 Sep 2026.\n2026-09-25 | Kofi | Bruno | I'll upload the render files by 27 Sep 2026, provided the grading session happens.\n2026-09-26 | Tess | Bruno | Forget it, you won't need to ship the hard drive\n2026-09-28 | Tess | group | Brilliant news everyone, the client screening is a go!",
  "question": "By the end of 29 Sep 2026, has Bruno kept the promise to ship the hard drive?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7a4e9fda11",
  "kind": "choice",
  "text": "Subject: the office refit\nForwarding a saved copy of the conversation from Femi.\n\nMembers: Greta, Femi, Malik, Sami\nChat log (oldest first):\n[29 Jan 2026] Malik: @Femi Wish me luck, hoping to renew the fire extinguisher service by 1 Feb 2026.\n[30 Jan 2026] Sami: @Femi Got it, I'll order the office stationery by 8 Feb 2026 for sure.\n[31 Jan 2026] Malik: @Sami I'll renew the fire extinguisher service by 7 Feb 2026, providing the annual audit goes ahead.\n[3 Feb 2026] Greta: Yay, the annual audit is all set to go!\n[6 Feb 2026] Malik: @Sami Any chance I can renew the fire extinguisher service by 11 Feb 2026 instead?\n[6 Feb 2026] Sami: @Malik Oh hun, I can't budge, so renew the fire extinguisher service by the old date!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Malik made to renew the fire extinguisher service at the end of 8 Feb 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q0b1be143cd",
  "kind": "yes/no",
  "text": "Our house group, sorted by Kofi, with the flatmate contract terms up front.\n\nMembers: Kofi, Lee, Nadia\nChat log (oldest first):\n[7 Aug 2026] Kofi: @Nadia Lovely, I'll scan the council tax letter by 10 August 2026 if the freshers welcome night is on.\n[8 Aug 2026] Nadia: @Kofi Absolutely, I will copy the house keys by 11 August 2026.\n[9 Aug 2026] Kofi: Scrapping the freshers welcome night, apologies to all.\n[9 Aug 2026] Kofi: @Nadia On my action item, may I scan the council tax letter by 12 August 2026 instead?\n[9 Aug 2026] Nadia: @Kofi Of course, it is fine for you to scan the council tax letter by 12 August 2026.\n[10 Aug 2026] Kofi: @Nadia You are released, no requirement to copy the house keys.",
  "question": "Under the rules on the card, is the promise Kofi made to scan the council tax letter in a status other than broken at the end of 11 August 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q16b01a3918",
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
  "qid": "q680d792297",
  "kind": "yes/no",
  "text": "Shared by Kai, this record holds tenant and landlord messages on the flatmate contract terms.\n\nMembers: Kai, Oskar, Arlo\nChat export (date | from | to | message):\n2026-05-19 | Oskar | Arlo | Absolutely, I will photograph the bathroom mould by 23 May 2026.\n2026-05-20 | Oskar | Kai | I assure you I'll return the bin rota by 22 May 2026 if the check in visit is on.\n2026-05-21 | Oskar | Kai | Count on me to forward the inventory photos by 27 May 2026, if the agent inventory walk happens.\n2026-05-23 | Kai | Oskar | Relax, mate, you're not expected to photograph the bathroom mould\n2026-05-23 | Oskar | Arlo | Quick report: I've managed to photograph the bathroom mould",
  "question": "Applying the rules on the card, has Oskar kept the promise to photograph the bathroom mould as of 27 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0fba695374",
  "kind": "choice",
  "text": "Freelancer to client messages, the menu redesign, passed on by Elif.\n\nMembers: Mo, Lee, Elif\nChat log (oldest first):\n[23 Jun 2026] Mo: @Lee If the gallery install goes ahead, I'll gladly export the logo files by Thursday, July 2, 2026.\n[25 Jun 2026] Lee: @Mo I promise to check the poster proofs by Monday, June 29, 2026.\n[25 Jun 2026] Lee: @Elif Relax, I'll sketch the packaging mockup by Wednesday, July 1, 2026, promise.\n[27 Jun 2026] Mo: @Lee Nobody needs you to sketch the packaging mockup, that's that\n[28 Jun 2026] Mo: @Lee I'll send the moodboard files by Thursday, July 2, 2026, provided the sign reveal happens.\n[1 Jul 2026] Elif: Sadly, the gallery install won't go ahead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Lee's promise to sketch the packaging mockup at the end of Monday, June 29, 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qc5c4577c86",
  "kind": "yes/no",
  "text": "Chat from the support case covering the league run, exported by Kai.\n\nMembers: Kai, Elif, Leila\nChat log (oldest first):\n[21 Mar 2026] Kai: @Leila I'll try to set up the corner flags by 2 Apr 2026, can't promise!\n[23 Mar 2026] Kai: @Leila It's on me to set up the corner flags by 30 Mar 2026.\n[23 Mar 2026] Kai: @Elif Count on me to mark the pitch lines by 25 Mar 2026 if the presentation evening is on.\n[23 Mar 2026] Kai: Lovely, the presentation evening is definitely happening!\n[27 Mar 2026] Elif: @Kai Relax, mate, you're not expected to set up the corner flags\n[27 Mar 2026] Kai: @Leila Ta-da, I went and did it: set up the corner flags!",
  "question": "Does the card's rule set show that Kai has not kept the promise to set up the corner flags at the end of 30 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0c24983270",
  "kind": "choice",
  "text": "Zara saved these exchanges with the agent about the summer lets season.\n\nMembers: Mo, Zara, Omar, Lena\nChat log (oldest first):\n[1 Jul 2026] Omar: @Lena Provided the guest arrival evening happens, I will collect the bed linen by 2026-07-04.\n[3 Jul 2026] Zara: @Lena I'll be sure to wash the beach towels by 2026-07-07.\n[5 Jul 2026] Zara: @Omar Only if the summer season launch is on, I will leave the welcome basket by 2026-07-08.\n[6 Jul 2026] Zara: @Lena I'll be sure to wheel the bins out by 2026-07-12.\n[11 Jul 2026] Zara: @Lena I regret to say that I shall not wheel the bins out.\n[12 Jul 2026] Lena: @Zara Good news, you're let off having to wheel the bins out",
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
  "qid": "qe7e1adad48",
  "kind": "yes/no",
  "text": "Saved by Jonas, this talk about the summer visits is just for family.\n\nMembers: Sami, Jonas, Bruno\nChat log (oldest first):\n[18 Jun 2026] Jonas: @Sami As long as the storytime session is on, I'll teach the card game by 25 June 2026.\n[19 Jun 2026] Bruno: @Jonas Count on me to tidy the playroom by 23 June 2026 if the seaside outing is on.\n[19 Jun 2026] Jonas: @Sami As long as the garden tea party is on, I will read the bedtime story by 26 June 2026.\n[21 Jun 2026] Sami: @Bruno Relax, I'll bake the oat biscuits by 29 June 2026, promise.\n[25 Jun 2026] Sami: @Bruno Can I bake the oat biscuits by 3 July 2026 instead? I did promise, sorry.\n[29 Jun 2026] Sami: @Bruno To my relief, I managed to bake the oat biscuits.",
  "question": "By the close of 29 June 2026, is the promise Sami made to bake the oat biscuits kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd351278ff3",
  "kind": "yes/no",
  "text": "Club chat exported by Greta, the local thread about the winter concert.\n\nMembers: Ana, Greta, Kofi\nChat log (oldest first):\n[2 Feb 2026] Ana: @Kofi I'll set up the sound desk by February 4, 2026, providing the voice test goes ahead.\n[2 Feb 2026] Greta: Please note the voice test will proceed.\n[4 Feb 2026] Ana: @Kofi Got it, I'll collect the sheet music by February 10, 2026 for sure.\n[5 Feb 2026] Ana: @Kofi I'm withdrawing my promise to collect the sheet music\n[5 Feb 2026] Kofi: @Ana Ah, no stress, no need for you to collect the sheet music",
  "question": "At the end of February 6, 2026, does the promise Ana made to collect the sheet music have any status except broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc2e5068267",
  "kind": "yes/no",
  "text": "Attached chat: the store makeover\nShared by: Mo\n\nMembers: Femi, Mo, Oskar, Jonas\nChat log (oldest first):\n[26 Jan 2026] Femi: @Oskar I will check the poster proofs by 2026-01-29 only if the sign reveal happens.\n[27 Jan 2026] Oskar: Sad to report that the sign reveal is off.\n[27 Jan 2026] Mo: @Oskar I'll fetch the brand fonts by 2026-02-05, providing the packaging launch goes ahead.\n[30 Jan 2026] Jonas: @Femi You can bank on me to sketch the packaging mockup by 2026-02-07.\n[31 Jan 2026] Jonas: @Femi For the record: I was able to sketch the packaging mockup\n[2 Feb 2026] Oskar: @Jonas Ticket's mine, I'll mail the business cards by 2026-02-10.",
  "question": "Was Jonas's promise to sketch the packaging mockup not kept as of 2026-02-06?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q30b2ad4c97",
  "kind": "choice",
  "text": "Team channel: the mobile release\nShared by Wren.\n\nMembers: Rhea, Wren\nChat log (oldest first):\n[1 Sep 2026] Rhea: @Wren I'll rotate the test keys by 4 September 2026, provided the server migration happens.\n[4 Sep 2026] Rhea: @Wren I'll be sure to run the security scan by 12 September 2026.\n[6 Sep 2026] Wren: @Rhea You can bank on me to write the release notes by 9 September 2026.\n[7 Sep 2026] Wren: @Rhea As long as the code freeze is on, I'll review the pull request by 11 September 2026.\n[8 Sep 2026] Wren: @Rhea I'm withdrawing my promise to write the release notes\n[12 Sep 2026] Wren: @Rhea You are released, no requirement to run the security scan.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Rhea's undertaking to run the security scan hold at the end of 17 September 2026?",
  "options": [
   "Waived",
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q49631f2e88",
  "kind": "choice",
  "text": "Here is the summer getaway, posted by Zara for the family to read.\n\nMembers: Zara, Kofi, Ravi\nChat export (date | from | to | message):\n2026-04-27 | Kofi | Ravi | Will attempt to buy the packing cubes by May 5, 2026, can't promise.\n2026-04-28 | Kofi | Ravi | Got it, I'll buy the packing cubes by May 4, 2026 for sure.\n2026-05-01 | Kofi | Ravi | Quick question, could I buy the packing cubes by May 10, 2026 instead?\n2026-05-02 | Zara | Kofi | Yes, lovely, you can buy the packing cubes by May 10, 2026 instead!\n2026-05-02 | Kofi | Zara | I'll collect the insurance papers by May 11, 2026, promise.\n2026-05-06 | Zara | Kofi | I'll book the airport parking by May 12, 2026 as long as the guided tour is on.\n2026-05-06 | Kofi | group | Sorry all, the guided tour is called off.\n2026-05-15 | Kofi | Ravi | For the record: I was able to buy the packing cubes",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, what is the deadline for Kofi to buy the packing cubes at the end of May 9, 2026, with any agreed change of date counted?",
  "options": [
   "May 4, 2026",
   "May 11, 2026",
   "May 10, 2026"
  ]
 },
 {
  "qid": "q2382fb16ab",
  "kind": "choice",
  "text": "Work channel export: the platform rewrite, shared by Malik.\n\nMembers: Hana, Leila, Malik\nChat log (oldest first):\n[19 Jul 2026] Leila: @Hana I promise to restart the build server by 26 July 2026 if the sprint demo is on.\n[19 Jul 2026] Malik: @Hana Committing to rotate the test keys by 23 July 2026.\n[23 Jul 2026] Malik: Yep, the sprint demo is on as planned.\n[24 Jul 2026] Malik: @Hana For the record: I was able to rotate the test keys\n[26 Jul 2026] Malik: @Leila You are released, no requirement to restart the build server.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Leila's promise to restart the build server at the end of 26 July 2026?",
  "options": [
   "Waived",
   "Kept",
   "Not yet due",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q7895142d55",
  "kind": "yes/no",
  "text": "Club and committee chat, saved by Ravi, with the sponsor search in the middle.\n\nMembers: Ivo, Ravi, Zara, Sami\nChat log (oldest first):\n[22 Oct 2026] Zara: @Ravi I promise to collect the timing tags by 27 October 2026 if the club sportive is on.\n[22 Oct 2026] Ravi: @Ivo Lovely, I'll print the route cards by 31 October 2026 for sure.\n[25 Oct 2026] Ravi: @Ivo I regret to say that I shall not print the route cards.\n[26 Oct 2026] Ivo: Just so you know, the club sportive is on as scheduled.\n[26 Oct 2026] Ivo: @Sami Ticket's mine, I'll fetch the bike stand by 30 October 2026.\n[27 Oct 2026] Zara: @Ravi Quick report: I've managed to collect the timing tags",
  "question": "At the end of 31 October 2026, is Zara's promise to collect the timing tags broken, waived, not triggered or not yet due, rather than kept?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0cead0c99c",
  "kind": "yes/no",
  "text": "Local volunteer export\nSaved by Ana, covering the topic of the training plan.\n\nMembers: Tess, Ana, Wren, Lena\nChat log (oldest first):\n[17 Feb 2026] Wren: @Ana Promise to pump the spare tyres by 26 Feb 2026 if the swap meet goes ahead.\n[18 Feb 2026] Lena: @Wren I'll print the route cards by 23 Feb 2026, promise.\n[18 Feb 2026] Wren: Thanks, got it.\n[19 Feb 2026] Wren: @Lena I'll tune the gear cables by 26 Feb 2026, promise.\n[20 Feb 2026] Lena: Please note the swap meet will proceed.\n[21 Feb 2026] Lena: @Wren For the record: I was able to print the route cards",
  "question": "Was Lena's promise to print the route cards not kept as of 24 Feb 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc1f5572e6d",
  "kind": "choice",
  "text": "Saved by Malik, this is the household group chat about the home adaptations, copied in full.\n\nMembers: Malik, Ravi, Yuki\nChat log (oldest first):\n[27 Feb 2026] Malik: @Yuki I'll try to wash the bed linen by 12 March 2026, can't promise!\n[28 Feb 2026] Malik: @Yuki I will wash the bed linen by 8 March 2026.\n[3 Mar 2026] Malik: @Yuki Quick question, could I wash the bed linen by 14 March 2026 instead?\n[6 Mar 2026] Ravi: @Malik I'll pick up the repeat prescription by 10 March 2026, provided the eye test happens.\n[6 Mar 2026] Malik: Update: the eye test is going ahead as planned.\n[6 Mar 2026] Yuki: @Malik Yes, lovely, you can wash the bed linen by 14 March 2026 instead!\n[7 Mar 2026] Ravi: @Malik Good news, you're let off having to wash the bed linen\n[8 Mar 2026] Malik: @Yuki To note: I have managed to wash the bed linen",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen does Malik have to wash the bed linen by, at the end of 19 March 2026, once any agreed date change is included?",
  "options": [
   "8 March 2026",
   "14 March 2026",
   "10 March 2026"
  ]
 },
 {
  "qid": "q4eaa4bac95",
  "kind": "choice",
  "text": "Subject: the kitchen refit\nBelow is the group chat that Mo saved, unedited.\n\nMembers: Kofi, Mo\nChat log (oldest first):\n[13 Jun 2026] Kofi: @Mo Lovely, I'll ring the flat repair line by Tuesday, 16 June 2026 if the electrics safety check is on.\n[13 Jun 2026] Mo: Brilliant news everyone, the electrics safety check is a go!\n[14 Jun 2026] Kofi: @Mo I'll be sure to wipe the cooker hood by Wednesday, 17 June 2026.\n[15 Jun 2026] Mo: @Kofi Good news, you're let off having to wipe the cooker hood\n[16 Jun 2026] Mo: @Kofi Ah, no stress, no need for you to ring the flat repair line",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Kofi's promise to ring the flat repair line at the end of Sunday, 21 June 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q840e2dae34",
  "kind": "choice",
  "text": "Saved chat on the care plan. Exported by Kai, unedited, from a household group.\n\nMembers: Kai, Tess, Omar\nChat export (date | from | to | message):\n2026-02-14 | Omar | Tess | Ticket's mine, I'll call the home nurse by 2026-02-19.\n2026-02-14 | Omar | Tess | Would it be fine if I call the home nurse by 2026-02-21 instead, yeah?\n2026-02-14 | Kai | Omar | Yes, fine to call the home nurse by 2026-02-21 instead.\n2026-02-16 | Kai | group | Checking you mean to call the home nurse?\n2026-02-16 | Kai | Omar | If the carer handover goes ahead, I'll book the clinic transport by 2026-02-23.\n2026-02-16 | Omar | Tess | Got myself to call the home nurse lol.\n2026-02-18 | Tess | Kai | Absolutely, I will print the care schedule by 2026-02-25.\n2026-02-20 | Omar | Kai | As long as the home assessment is on, I'll drop off the hot meals by 2026-02-23.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Omar to call the home nurse at the end of 2026-02-22, counting any agreed change of date?",
  "options": [
   "2026-02-19",
   "2026-02-21",
   "2026-02-23"
  ]
 },
 {
  "qid": "qff3ff497b1",
  "kind": "yes/no",
  "text": "Team thread shared by Tomas, covering the visitor policy in the channel.\n\nMembers: Femi, Tomas, Oskar, Tess\nChat log (oldest first):\n[11 Oct 2026] Tomas: @Tess If the team lunch goes ahead, I'll print the staff rota by 13 Oct 2026.\n[11 Oct 2026] Oskar: Update, the team lunch will not take place.\n[11 Oct 2026] Oskar: @Tess I will make sure to collect the visitor badges by 18 Oct 2026.\n[11 Oct 2026] Oskar: @Tess Can I collect the visitor badges by 21 Oct 2026 instead? I did promise, sorry.\n[12 Oct 2026] Oskar: @Tess To my relief, I managed to collect the visitor badges.\n[14 Oct 2026] Tess: Any news on plans to collect the visitor badges?",
  "question": "Did Oskar keep the promise to collect the visitor badges as of 16 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf0d98a395b",
  "kind": "yes/no",
  "text": "Copied into a record, this is the letting agent thread on the guest welcome plan, shared by Mo.\n\nMembers: Mo, Priya, Oskar, Bruno\nChat log (oldest first):\n[22 Jul 2026] Mo: @Bruno You can bank on me to wheel the bins out by 26 July 2026.\n[22 Jul 2026] Bruno: Thanks for the heads up.\n[25 Jul 2026] Mo: @Bruno Got myself to wheel the bins out lol.\n[26 Jul 2026] Priya: @Bruno If the owner handover visit is on, I'll definitely restock the guest toiletries by 28 July 2026.\n[26 Jul 2026] Bruno: Update, the owner handover visit will not take place.\n[28 Jul 2026] Bruno: @Mo Count on me, I'll change the lounge bulb by 5 August 2026.",
  "question": "By the end of 29 July 2026, has Mo kept the promise to wheel the bins out?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb07c163713",
  "kind": "choice",
  "text": "Letting agent thread with tenants on the guest welcome plan, copied out by Tess.\n\nMembers: Ravi, Yuki, Sami, Tess\nChat log (oldest first):\n[23 Sep 2026] Yuki: @Ravi I will change the lounge bulb by 28 Sep 2026.\n[24 Sep 2026] Tess: @Yuki I promise to leave the welcome basket by 30 Sep 2026.\n[25 Sep 2026] Yuki: @Tess As long as the check out clean is on, I will wash the beach towels by 29 Sep 2026.\n[26 Sep 2026] Ravi: On track for the check out clean to happen as planned.\n[27 Sep 2026] Ravi: @Yuki Ah, no stress, no need for you to change the lounge bulb",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Yuki's promise to change the lounge bulb at the end of 29 Sep 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q500eb30ccf",
  "kind": "yes/no",
  "text": "{\"archive\": \"group chat\", \"subject\": \"the quiet street fund\", \"sent_by\": \"Oskar\"}\n\nMembers: Oskar, Mo, Kai\nChat log (oldest first):\n[14 May 2026] Kai: @Oskar Relax, I'll lend the stepladder by 23 May 2026 for sure.\n[15 May 2026] Kai: @Oskar I'll lock the side gate by 22 May 2026, providing the hedge trimming day goes ahead.\n[17 May 2026] Mo: @Kai Got it, I'll clear the hedge trimmings by 25 May 2026 for sure.\n[17 May 2026] Oskar: Just so you know, the hedge trimming day is on as scheduled.\n[22 May 2026] Kai: @Oskar Ticked off: lock the side gate, feels so good",
  "question": "Under the rules on the card, is it true that Kai has not kept the promise to lock the side gate as of 22 May 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2fc0d6d5b2",
  "kind": "choice",
  "text": "Forwarded from the volunteer committee's group, with the choir tour at the centre, by Wren.\n\nMembers: Ines, Wren, Rhea\nChat log (oldest first):\n[12 Jun 2026] Rhea: Might be able to fetch the choir robes by Friday, 19 June 2026, who knows!\n[14 Jun 2026] Rhea: @Ines I'll fetch the choir robes by Saturday, 20 June 2026 as long as the joint concert is on.\n[16 Jun 2026] Rhea: @Wren Committing to return the library scores by Monday, 22 June 2026.\n[16 Jun 2026] Wren: Afraid the joint concert is called off.\n[19 Jun 2026] Rhea: @Ines Is it all right if I fetch the choir robes by Wednesday, 24 June 2026 instead?\n[19 Jun 2026] Ines: @Rhea The original date stands, so you need to fetch the choir robes.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Rhea's commitment to fetch the choir robes is in what status at the end of Sunday, 21 June 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "qf6b4539e9a",
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
  "qid": "qbb132603bb",
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
  "qid": "q21aa365e61",
  "kind": "yes/no",
  "text": "Support case copy, filed for the quiet street fund\nSaved on record by Rhea\n\nMembers: Tess, Bruno, Rhea, Nadia\nChat export (date | from | to | message):\n2026-05-31 | Nadia | group | Hoping to lend the stepladder by 3 Jun 2026, can't promise.\n2026-06-01 | Nadia | Rhea | I'll be sure to lend the stepladder by 4 Jun 2026.\n2026-06-02 | Bruno | Nadia | Quick update: you do not need to lend the stepladder at all.\n2026-06-04 | Nadia | Rhea | Ta-da, I went and did it: lend the stepladder!\n2026-06-06 | Rhea | Tess | If the street litter clean is on, I'll definitely bring the bins in by 11 Jun 2026.\n2026-06-10 | Tess | group | Afraid the street litter clean is called off.",
  "question": "Going by the card's rules, does Nadia keep the promise to lend the stepladder at the end of 5 Jun 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qac6027d029",
  "kind": "yes/no",
  "text": "Our flat chat about the house refit, saved by Kofi for whoever lives here.\n\nMembers: Ana, Leila, Kofi\nChat export (date | from | to | message):\n2026-09-17 | Ana | Kofi | Relax, I'll scrape the old wallpaper by 23 September 2026, promise.\n2026-09-18 | Ana | Kofi | Count on me, I'll pay the plumbing invoice by 27 September 2026.\n2026-09-19 | Leila | Ana | I'll fetch the paint samples by 26 September 2026, provided the boiler install visit happens.\n2026-09-21 | Ana | Kofi | Guess what, I managed to scrape the old wallpaper!\n2026-09-22 | Kofi | Ana | I assure you I'll return the tile cutter by 29 September 2026 if the mortgage valuation visit is on.\n2026-09-28 | Ana | group | Quick heads up, the mortgage valuation visit is scrapped.",
  "question": "Was Ana's promise to scrape the old wallpaper not kept as of 26 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q989abc4384",
  "kind": "choice",
  "text": "Neighbour and flatmate talk, copied out by Rhea: the vegetable plot plan.\n\nMembers: Rhea, Tomas, Priya, Arlo\nChat log (oldest first):\n[25 Jun 2026] Rhea: @Tomas I'll sharpen the hand hoe by 2 Jul 2026, promise.\n[27 Jun 2026] Rhea: @Tomas Quick report: I've managed to sharpen the hand hoe\n[28 Jun 2026] Tomas: @Priya As long as the village flower show is on, I'll build the compost bay by 6 Jul 2026.\n[30 Jun 2026] Rhea: @Priya Relax, I'll water the allotment beds by 8 Jul 2026, promise.\n[3 Jul 2026] Rhea: Yay, the village flower show is all set to go!\n[6 Jul 2026] Rhea: @Priya Change of plans: I will not water the allotment beds",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Tomas's promise to build the compost bay at the end of 6 Jul 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "qacaa7fba25",
  "kind": "choice",
  "text": "Subject: chat about the sponsor search, forwarded\nThe chat follows below.\nRegards, Ana\n\nMembers: Yuki, Ana, Nadia, Mo\nChat log (oldest first):\n[22 Sep 2026] Nadia: @Mo Count on me to return the loaned helmets by 29 Sep 2026 if the hill climb is on.\n[22 Sep 2026] Nadia: @Yuki Relax, I'll print the route cards by 25 Sep 2026 for sure.\n[23 Sep 2026] Yuki: @Ana I assure you I'll pump the spare tyres by 1 Oct 2026 if the group ride is on.\n[24 Sep 2026] Nadia: @Ana Committing to fetch the bike stand by 3 Oct 2026.\n[25 Sep 2026] Yuki: @Nadia Nobody needs you to print the route cards, that's that",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Nadia's promise to print the route cards turn out at the end of 26 Sep 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qf4c871a2e4",
  "kind": "yes/no",
  "text": "Jonas shared this so the junior section is easy to follow for the volunteers.\n\nMembers: Dara, Nadia, Jonas, Sami\nChat log (oldest first):\n[19 Jan 2026] Jonas: @Nadia Relax, I'll set up the corner flags by 22 January 2026 for sure.\n[19 Jan 2026] Nadia: @Sami Count on me, I'll wash the away kit by 21 January 2026.\n[22 Jan 2026] Nadia: @Sami If the cup tie goes ahead, I'll repair the goal nets by 28 January 2026.\n[23 Jan 2026] Jonas: @Nadia Guess who managed to set up the corner flags, go team!\n[24 Jan 2026] Nadia: Update: the cup tie is going ahead as planned.",
  "question": "On the card, was Jonas's promise to set up the corner flags kept, rather than broken, waived, not triggered or not yet due, at the end of 26 January 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q947139796b",
  "kind": "yes/no",
  "text": "Support case copy, filed for the house refit\nSaved on record by Greta\n\nMembers: Malik, Tomas, Zara, Greta\nChat export (date | from | to | message):\n2026-09-17 | Tomas | Greta | If the mortgage valuation visit goes ahead, I'll gladly print the floor plan by Friday, 25 September 2026.\n2026-09-18 | Malik | Tomas | Absolutely, I will scrape the old wallpaper by Wednesday, 23 September 2026.\n2026-09-19 | Tomas | group | Really pleased to say the mortgage valuation visit will go ahead!\n2026-09-20 | Zara | Greta | Provided the damp survey inspection happens, I'll fetch the paint samples by Wednesday, 23 September 2026.\n2026-09-22 | Malik | Tomas | To my relief, I managed to scrape the old wallpaper.\n2026-09-24 | Tomas | Greta | Forget what I said, I won't print the floor plan",
  "question": "Going by the card's rules, does Tomas not keep the promise to print the floor plan at the end of Friday, 25 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qeeb4e1d679",
  "kind": "choice",
  "text": "Subject: exported chat about the music library\nHere it is for you, from Tomas, exactly as saved.\n\nMembers: Wren, Tomas, Omar, Priya\nChat log (oldest first):\n[22 Sep 2026] Omar: @Wren Count on me, I'll send the audition reminders by 28 September 2026.\n[23 Sep 2026] Tomas: @Wren As long as the voice test is on, I will collect the sheet music by 26 September 2026.\n[25 Sep 2026] Tomas: Sorry, the voice test is off.\n[26 Sep 2026] Priya: Aiming to move the piano by 3 October 2026, we'll see.\n[27 Sep 2026] Priya: @Tomas Ticket's mine, I'll move the piano by 1 October 2026.\n[27 Sep 2026] Priya: @Tomas Would it be fine if I move the piano by 4 October 2026 instead, yeah?\n[30 Sep 2026] Wren: @Priya Yes, you can move the piano by 4 October 2026 if that suits you.\n[5 Oct 2026] Priya: @Tomas Guess what, I managed to move the piano!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs things stand at the end of 2 October 2026, which date is the deadline for Priya to move the piano, with any agreed change applied?",
  "options": [
   "26 September 2026",
   "4 October 2026",
   "1 October 2026"
  ]
 },
 {
  "qid": "q8956dba114",
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
  "qid": "q61c993e1e3",
  "kind": "yes/no",
  "text": "Here we plan the family day out together, and Greta saved this for the family.\n\nMembers: Malik, Oskar, Leila, Greta\nChat log (oldest first):\n[16 Jul 2026] Oskar: @Greta Relax, I'll sort the old photo albums by 2026-07-24 for sure.\n[17 Jul 2026] Leila: @Oskar Provided the storytime session happens, I will tidy the playroom by 2026-07-20.\n[19 Jul 2026] Greta: Update: the storytime session is going ahead as planned.\n[19 Jul 2026] Malik: @Greta Count on me to pack the picnic basket by 2026-07-23.\n[20 Jul 2026] Oskar: @Leila Relax, mate, you're not expected to tidy the playroom\n[21 Jul 2026] Leila: @Malik Ah, no stress, no need for you to pack the picnic basket",
  "question": "Per the rules on the card, at the end of 2026-07-25, has the promise Leila made to tidy the playroom been broken?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9a0b087707",
  "kind": "yes/no",
  "text": "Neighbours and renters, the flat chat, exported by Tess, covering the garden makeover.\n\nMembers: Greta, Lee, Tess, Yuki\nChat export (date | from | to | message):\n2026-01-06 | Lee | Tess | You can bank on me to sweep the dust from stairs by 14 January 2026.\n2026-01-10 | Lee | Tess | Gutted to say I won't sweep the dust from stairs, sorry team\n2026-01-10 | Yuki | Greta | Only if the boiler install visit is on, I will scrape the old wallpaper by 17 January 2026.\n2026-01-12 | Yuki | group | Yep, the boiler install visit is on as planned.\n2026-01-16 | Lee | Yuki | Forget it, you won't need to scrape the old wallpaper",
  "question": "Did the promise that Yuki made to scrape the old wallpaper turn out broken, waived, not triggered or not yet due, rather than kept, on 17 January 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4574726358",
  "kind": "yes/no",
  "text": "Club and committee chat, saved by Nadia, with the league run in the middle.\n\nMembers: Omar, Nadia, Ines\nChat log (oldest first):\n[29 Jan 2026] Nadia: @Omar As long as the cup tie is on, I'll repair the goal nets by 6 February 2026.\n[30 Jan 2026] Ines: @Nadia You can bank on me to fetch the medical bag by 2 February 2026.\n[1 Feb 2026] Ines: @Nadia Mind giving me until 5 February 2026 to fetch the medical bag?\n[1 Feb 2026] Omar: @Ines Ah, no stress, no need for you to fetch the medical bag\n[3 Feb 2026] Ines: Sorry all, the cup tie is not happening.",
  "question": "At the end of 2 February 2026, has the promise Ines made to fetch the medical bag been broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3c08662221",
  "kind": "choice",
  "text": "Shared by Tomas, this thread covers the honeymoon album as pasted from email.\n\nMembers: Rhea, Lena, Tomas, Wren\nChat log (oldest first):\n[6 May 2026] Lena: @Tomas You can bank on me to pick up the album prints by 14 May 2026.\n[9 May 2026] Lena: @Rhea Lovely, I'll return the lighting stands by 13 May 2026 for sure.\n[10 May 2026] Wren: @Lena Promise to buy the candle props by 15 May 2026 if the rehearsal dinner goes ahead.\n[10 May 2026] Tomas: @Lena Quick update: you do not need to return the lighting stands at all.\n[12 May 2026] Rhea: Team, the rehearsal dinner stays on as booked.\n[13 May 2026] Tomas: @Lena Forget it, you won't need to pick up the album prints",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Lena's pledge to return the lighting stands sit at the end of 17 May 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Kept",
   "Waived",
   "Not triggered"
  ]
 }
]
