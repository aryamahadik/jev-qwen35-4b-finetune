# G5-H blind read (all free-form rows) T32-blind_read-c97f52fe-008 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root/T32/qc/g5h/answers/T32-blind_read-c97f52fe-008.json

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
  "qid": "qf6031cdccb",
  "kind": "choice",
  "text": "Dara shared this so the student house hunt is easy to find, flatmates.\n\nMembers: Priya, Tomas, Omar, Dara\nChat log (oldest first):\n[28 May 2026] Omar: @Priya I'll collect the parcel from porch by Friday, 5 June 2026, providing the check in visit goes ahead.\n[29 May 2026] Omar: @Priya Absolutely, I will send the deposit receipt by Saturday, 6 June 2026.\n[29 May 2026] Omar: @Priya To note: I have managed to send the deposit receipt\n[1 Jun 2026] Dara: Quick heads up, the check in visit is scrapped.\n[1 Jun 2026] Omar: @Priya Can I collect the parcel from porch by Sunday, 7 June 2026 instead? I did promise, sorry.\n[1 Jun 2026] Priya: @Omar The original date stands, so you need to collect the parcel from porch.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Omar's promise to collect the parcel from porch at the end of Monday, 1 June 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qd497b0e544",
  "kind": "yes/no",
  "text": "Bruno forwarded this support chat about the new kit design.\n\nMembers: Bruno, Oskar, Kai\nChat log (oldest first):\n[24 Feb 2026] Bruno: @Oskar I promise to service the tandem bike by March 5, 2026.\n[24 Feb 2026] Kai: @Bruno Lovely, I'll return the loaned helmets by March 2, 2026 if the bike check is on.\n[27 Feb 2026] Kai: @Bruno Quick update: you do not need to service the tandem bike at all.\n[27 Feb 2026] Kai: Great news, the bike check is on!\n[1 Mar 2026] Oskar: @Kai Relax, mate, you're not expected to return the loaned helmets",
  "question": "Was the promise to return the loaned helmets from Kai kept on March 3, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q829e232c53",
  "kind": "choice",
  "text": "Our flat chat about the attic conversion idea, shared by Yuki for whoever lives here.\n\nMembers: Zara, Yuki, Arlo, Kai\nChat export (date | from | to | message):\n2026-09-29 | Zara | Kai | Guaranteed I'll stock the spice rack by 6 Oct 2026.\n2026-10-01 | Arlo | Kai | If the fuse box inspection is on, I'll definitely drop the parcel upstairs by 5 Oct 2026.\n2026-10-02 | Zara | Kai | Provided the water tank check happens, I will feed the house plants by 9 Oct 2026.\n2026-10-03 | Arlo | Kai | Got it, I'll cut a spare door key by 8 Oct 2026 for sure.\n2026-10-05 | Zara | Kai | Ticked off my list: stock the spice rack, yay.\n2026-10-08 | Arlo | group | Quick check, any update on plans to stock the spice rack?",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Zara's promise to stock the spice rack at the end of 6 Oct 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Not yet due",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q289028ba5f",
  "kind": "yes/no",
  "text": "Attached chat: the documentary cut\nShared by: Bruno.\n\nMembers: Ivo, Bruno, Ravi, Nadia\nChat export (date | from | to | message):\n2026-07-24 | Ivo | Ravi | If the shoot day goes ahead, I'll gladly send the timeline export by 29 July 2026.\n2026-07-24 | Ravi | Nadia | You can bet I'll upload the render files by 2 August 2026.\n2026-07-27 | Bruno | Nadia | Lovely, I'll label the clip folders by 2 August 2026 if the agency review call is on.\n2026-07-27 | Ivo | Nadia | Committing to export the subtitle files by 1 August 2026.\n2026-08-01 | Bruno | group | Update: the agency review call is going ahead as planned.\n2026-08-04 | Ivo | Nadia | Log entry: export the subtitle files, carried out",
  "question": "Using the rules on the card, is it true that Ivo has not broken the promise to export the subtitle files at the end of 4 August 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q382e53a935",
  "kind": "choice",
  "text": "Here is the plan for the loft conversion, saved by Tess for the group.\n\nMembers: Tess, Priya, Lena\nChat export (date | from | to | message):\n2026-03-12 | Priya | Tess | I'll try to measure the hallway for shelves by 19 Mar 2026, can't promise!\n2026-03-14 | Lena | Tess | Absolutely, I will fetch the paint samples by 19 Mar 2026.\n2026-03-14 | Priya | Tess | I'll measure the hallway for shelves by 17 Mar 2026 if the boiler install visit goes ahead.\n2026-03-15 | Lena | group | Great news, the boiler install visit is on!\n2026-03-20 | Lena | Tess | Count on me, I'll collect the sanding pads by 25 Mar 2026.\n2026-03-20 | Tess | Lena | Relax, mate, you're not expected to collect the sanding pads",
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
  "qid": "q18f3d46ea9",
  "kind": "choice",
  "text": "Tenant and landlord back-and-forth on the spare room plan, saved by Zara.\n\nMembers: Rhea, Priya, Zara, Elif\nChat export (date | from | to | message):\n2026-01-20 | Priya | Zara | Only if the lodger house supper is on, I will wipe the shared kitchen counter by 28 January 2026.\n2026-01-23 | Elif | group | Update, the lodger house supper will not take place.\n2026-01-23 | Zara | Priya | As long as the fuse box inspection is on, I will buy the washing powder by 25 January 2026.\n2026-01-25 | Rhea | Priya | Count on me, I'll drop the parcel upstairs by 30 January 2026.\n2026-01-29 | Rhea | Priya | I committed to drop the parcel upstairs, can I do that by 4 February 2026 instead?\n2026-01-30 | Priya | Rhea | Works for me, fine for you to drop the parcel upstairs by 4 February 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Priya's pledge to wipe the shared kitchen counter sit at the end of 31 January 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Waived",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "q8a777fb4c4",
  "kind": "choice",
  "text": "Parents and cousins, this is where we sort out the vegetable plot plan. Saved by Arlo.\n\nMembers: Tess, Rhea, Arlo, Dara\nChat log (oldest first):\n[19 Jan 2026] Rhea: @Dara I'll stake the tomato canes by 21 Jan 2026 if the plot inspection goes ahead.\n[20 Jan 2026] Dara: @Rhea Guaranteed I'll sharpen the hand hoe by 24 Jan 2026.\n[20 Jan 2026] Dara: @Rhea Gutted to say I won't sharpen the hand hoe, sorry team\n[20 Jan 2026] Tess: @Dara Ah, no stress, no need for you to sharpen the hand hoe\n[21 Jan 2026] Rhea: @Tess Promise to deliver the surplus runner beans by 28 Jan 2026 if the allotment site visit goes ahead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Dara made to sharpen the hand hoe at the end of 21 Jan 2026?",
  "options": [
   "Kept",
   "Waived",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q1082185ad1",
  "kind": "choice",
  "text": "Subject: Saved thread about the ground upgrade\nHere is a full export from Mo, ready to read.\n\nMembers: Zara, Kofi, Mo\nChat log (oldest first):\n[9 Jul 2026] Zara: @Mo Might be able to book the changing room by July 11, 2026, who knows!\n[10 Jul 2026] Zara: @Kofi It's on me to book the changing room by July 17, 2026.\n[11 Jul 2026] Zara: @Kofi I committed to book the changing room, can I do that by July 23, 2026 instead?\n[12 Jul 2026] Kofi: @Zara I'll repair the goal nets by July 18, 2026, providing the training camp goes ahead.\n[16 Jul 2026] Kofi: @Zara Oh hun, I can't budge, so book the changing room by the old date!\n[17 Jul 2026] Zara: Sadly, the training camp is not going ahead.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Zara's undertaking to book the changing room hold at the end of July 17, 2026?",
  "options": [
   "Broken",
   "Waived",
   "Kept",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q2fd80aa23e",
  "kind": "yes/no",
  "text": "Committee chat on the winter concert, shared by Femi with the volunteers.\n\nMembers: Femi, Tess, Malik, Mo\nChat log (oldest first):\n[19 Jul 2026] Mo: @Femi Provided the summer recital happens, I will print the song sheets by 21 July 2026.\n[19 Jul 2026] Femi: Lovely, the summer recital is definitely happening!\n[19 Jul 2026] Malik: @Femi Relax, I'll book the rehearsal room by 27 July 2026 for sure.\n[25 Jul 2026] Mo: @Femi It's on me to buy the spare folders by 1 August 2026.\n[27 Jul 2026] Malik: @Femi Quick report: I've managed to book the rehearsal room",
  "question": "Is it true under the card's rules that Malik has kept the promise to book the rehearsal room at the end of 30 July 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q205582cdae",
  "kind": "choice",
  "text": "Forwarded by Arlo: a help-desk thread covering the lodger house rules.\n\nMembers: Malik, Oskar, Arlo\nChat export (date | from | to | message):\n2026-07-23 | Arlo | Oskar | If the lodger farewell supper goes ahead, I'll stock the spice rack by 25 July 2026.\n2026-07-24 | Malik | Arlo | Count on me to feed the house plants by 31 July 2026.\n2026-07-25 | Malik | Arlo | I'll replace the loo roll by 1 August 2026, providing the lodger house supper goes ahead.\n2026-07-27 | Malik | group | Update, the lodger house supper will not take place.\n2026-08-01 | Malik | Arlo | Would it be fine if I replace the loo roll by 4 August 2026 instead, yeah?\n2026-08-01 | Oskar | Malik | Yes, fine to replace the loo roll by 4 August 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Malik's pledge to replace the loo roll at the end of 31 July 2026?",
  "options": [
   "Waived",
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "qfe348cb695",
  "kind": "yes/no",
  "text": "Parents and cousins, this is where we sort out the loft conversion. Saved by Sami.\n\nMembers: Nadia, Sami, Lena\nChat export (date | from | to | message):\n2026-10-08 | Nadia | Sami | If the boiler install visit goes ahead, I'll pay the plumbing invoice by 15 October 2026.\n2026-10-08 | Nadia | Lena | As long as the damp survey inspection is on, I will return the tile cutter by 13 October 2026.\n2026-10-11 | Lena | Sami | Count on me to hang the new curtain rail by 19 October 2026.\n2026-10-13 | Lena | group | Scrapping the boiler install visit, apologies to all.\n2026-10-19 | Lena | Sami | Mate, I promised, may I hang the new curtain rail by 23 October 2026 instead?\n2026-10-19 | Sami | Lena | No, you need to hang the new curtain rail by the original date.",
  "question": "Under the rules on the card, is the promise Nadia made to pay the plumbing invoice kept as of 18 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q37e5f36579",
  "kind": "yes/no",
  "text": "Hana shared this exchange with the client about the guest list.\n\nMembers: Omar, Ivo, Hana\nChat log (oldest first):\n[28 Oct 2026] Ivo: @Hana Wish me luck, hoping to fetch the spare memory cards by 3 Nov 2026.\n[30 Oct 2026] Ivo: @Omar You can bank on me to fetch the spare memory cards by 2 Nov 2026.\n[31 Oct 2026] Ivo: @Hana If the engagement shoot is on, I'll definitely charge the flash batteries by 8 Nov 2026.\n[1 Nov 2026] Ivo: @Omar Gutted to say I won't fetch the spare memory cards, sorry team\n[1 Nov 2026] Omar: @Ivo Good news, you're let off having to fetch the spare memory cards\n[5 Nov 2026] Ivo: On track for the engagement shoot to happen as planned.",
  "question": "Applying the rules on the card, has Ivo kept the promise to fetch the spare memory cards as of 2 Nov 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa22734d240",
  "kind": "yes/no",
  "text": "Subject: Chat about the house refit\nBelow is a copy that came from Jonas, pasted as found.\n\nMembers: Lena, Jonas, Ravi\nChat export (date | from | to | message):\n2026-07-20 | Lena | Ravi | Might manage to hang the new curtain rail by 27 July 2026, who knows.\n2026-07-21 | Lena | Jonas | Count on me to hang the new curtain rail by 26 July 2026, if the mortgage valuation visit happens.\n2026-07-23 | Jonas | Ravi | It's on me to scrape the old wallpaper by 27 July 2026.\n2026-07-24 | Jonas | group | Brilliant news everyone, the mortgage valuation visit is a go!\n2026-07-26 | Lena | Jonas | My sincere apologies, I am unable to hang the new curtain rail.\n2026-07-27 | Jonas | Ravi | Guess what, I managed to scrape the old wallpaper!",
  "question": "Under the rules on the card, is the promise Lena made to hang the new curtain rail in a status other than broken at the end of 30 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb726329e1e",
  "kind": "yes/no",
  "text": "Volunteers, here is the league run chat that Jonas forwarded to us.\n\nMembers: Tess, Rhea, Jonas\nChat log (oldest first):\n[22 Oct 2026] Jonas: @Rhea Might be able to print the team sheets by 24 October 2026, who knows!\n[23 Oct 2026] Jonas: @Rhea I promise to print the team sheets by 28 October 2026 if the home derby is on.\n[23 Oct 2026] Jonas: @Tess I'll repair the goal nets by 29 October 2026, promise.\n[24 Oct 2026] Tess: Great news, the home derby is on!\n[24 Oct 2026] Jonas: @Rhea Can I print the team sheets by 2 November 2026 instead? I did promise, sorry.\n[24 Oct 2026] Tess: @Jonas Go ahead and print the team sheets by 2 November 2026, that is fine.",
  "question": "Is the promise Jonas made to print the team sheets in a status other than broken at the end of 26 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q665d7bce57",
  "kind": "yes/no",
  "text": "Forwarded by Elif, this thread on the home adaptations stays attached to the ticket.\n\nMembers: Elif, Ana, Rhea\nChat log (oldest first):\n[29 May 2026] Ana: @Elif Got it, I'll print the care schedule by 2 June 2026 for sure.\n[30 May 2026] Ana: @Rhea Count on me to set up the medicine dispenser by 3 June 2026, if the home assessment happens.\n[30 May 2026] Elif: @Ana Don't sweat it, there's no need to print the care schedule\n[31 May 2026] Rhea: @Ana I will call the home nurse by 4 June 2026 only if the carer handover happens.\n[1 Jun 2026] Elif: Yay, the home assessment is all set to go!\n[3 Jun 2026] Ana: @Rhea I regret to say that I shall not set up the medicine dispenser.",
  "question": "Is the promise Ana made to set up the medicine dispenser not kept by 5 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe50e131c34",
  "kind": "choice",
  "text": "Tenant and agent back-and-forth on the attic conversion idea, forwarded by Lee.\n\nMembers: Ines, Lee, Malik, Mo\nChat export (date | from | to | message):\n2026-08-19 | Lee | Ines | Absolutely, I will replace the loo roll by 25 August 2026.\n2026-08-21 | Mo | Malik | Count on me to turn the heating timer by 25 August 2026, if the house insurance review happens.\n2026-08-23 | Mo | group | Just so you know, the house insurance review is on as scheduled.\n2026-08-23 | Ines | Malik | It's on me to defrost the top freezer by 30 August 2026.\n2026-08-24 | Ines | Mo | As long as the water tank check is on, I'll drop the parcel upstairs by 1 September 2026.\n2026-08-26 | Mo | Ines | Don't sweat it, there's no need to defrost the top freezer",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Ines's promise to defrost the top freezer at the end of 29 August 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "qca420024c0",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the trade show push\nFrom Jonas, the thread below is shared as it stands.\n\nMembers: Lena, Jonas, Omar\nChat export (date | from | to | message):\n2026-03-28 | Omar | Lena | I'll be sure to return the rented camera gear by 31 March 2026.\n2026-03-29 | Omar | Lena | I'll set up the analytics dashboard by 2 April 2026 if the webinar rehearsal goes ahead.\n2026-03-29 | Omar | Lena | Ticked off my list: return the rented camera gear, yay.\n2026-03-30 | Jonas | Omar | I will make sure to draft the press release by 3 April 2026.\n2026-04-01 | Lena | Omar | Count on me to collect the survey answers by 8 April 2026, if the influencer call happens.",
  "question": "Under the rules on the card, is it true that Omar has not kept the promise to return the rented camera gear as of 31 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc790148701",
  "kind": "yes/no",
  "text": "Forwarded by Elif, this thread on the home adaptations stays attached to the ticket.\n\nMembers: Elif, Ana, Rhea\nChat log (oldest first):\n[29 May 2026] Ana: @Elif Got it, I'll print the care schedule by 2 June 2026 for sure.\n[30 May 2026] Ana: @Rhea Count on me to set up the medicine dispenser by 3 June 2026, if the home assessment happens.\n[30 May 2026] Elif: @Ana Don't sweat it, there's no need to print the care schedule\n[31 May 2026] Rhea: @Ana I will call the home nurse by 4 June 2026 only if the carer handover happens.\n[1 Jun 2026] Elif: Yay, the home assessment is all set to go!\n[3 Jun 2026] Ana: @Rhea I regret to say that I shall not set up the medicine dispenser.",
  "question": "Is Ana's promise to set up the medicine dispenser kept at the end of 5 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q85bc53208a",
  "kind": "yes/no",
  "text": "Attached chat: the loft conversion\nShared by: Ravi.\n\nMembers: Femi, Ravi, Zara, Hana\nChat export (date | from | to | message):\n2026-08-31 | Ravi | Femi | You can bank on me to pay the plumbing invoice by 3 September 2026.\n2026-09-04 | Hana | Femi | Count on me, I'll scrape the old wallpaper by 11 September 2026.\n2026-09-05 | Zara | Hana | I will pick up the grout bag by 13 September 2026 only if the boiler install visit happens.\n2026-09-11 | Hana | Femi | I have to take back my promise to scrape the old wallpaper.\n2026-09-11 | Femi | Hana | Nobody needs you to scrape the old wallpaper, that's that\n2026-09-12 | Ravi | group | Sorry, the boiler install visit is off.",
  "question": "Does the card's rule set confirm that Hana has kept the promise to scrape the old wallpaper on 16 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3ae028a523",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the trade show push\nFrom Jonas, the thread below is shared as it stands.\n\nMembers: Lena, Jonas, Omar\nChat export (date | from | to | message):\n2026-03-28 | Omar | Lena | I'll be sure to return the rented camera gear by 31 March 2026.\n2026-03-29 | Omar | Lena | I'll set up the analytics dashboard by 2 April 2026 if the webinar rehearsal goes ahead.\n2026-03-29 | Omar | Lena | Ticked off my list: return the rented camera gear, yay.\n2026-03-30 | Jonas | Omar | I will make sure to draft the press release by 3 April 2026.\n2026-04-01 | Lena | Omar | Count on me to collect the survey answers by 8 April 2026, if the influencer call happens.",
  "question": "Has Omar kept the promise to return the rented camera gear at the end of 31 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc8cbdaef12",
  "kind": "choice",
  "text": "Tenant and agent back-and-forth on the cottage refresh, forwarded by Kofi.\n\nMembers: Bruno, Kofi, Priya, Ivo\nChat log (oldest first):\n[18 May 2026] Kofi: @Ivo I will make sure to scrub the hot tub by 26 May 2026.\n[26 May 2026] Ivo: @Priya I'll wash the beach towels by 30 May 2026, providing the check out clean goes ahead.\n[26 May 2026] Ivo: @Bruno Count on me to air the spare room by 29 May 2026 if the summer season launch is on.\n[26 May 2026] Priya: @Bruno I will make sure to vacuum the holiday cottage by 31 May 2026.\n[31 May 2026] Priya: @Bruno Is it all right if I vacuum the holiday cottage by 3 Jun 2026 instead?\n[31 May 2026] Ivo: @Priya Yes, happy for you to vacuum the holiday cottage by 3 Jun 2026 instead.\n[1 Jun 2026] Priya: @Bruno Log entry: vacuum the holiday cottage, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen does Priya have to vacuum the holiday cottage by, at the end of 5 Jun 2026, once any agreed date change is included?",
  "options": [
   "3 Jun 2026",
   "29 May 2026",
   "31 May 2026"
  ]
 },
 {
  "qid": "qcf8108616d",
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
  "qid": "q4ce5115dc8",
  "kind": "choice",
  "text": "Sami shared this so the family follows the travel plans.\n\nMembers: Sami, Yuki, Zara, Elif\nChat export (date | from | to | message):\n2026-04-30 | Yuki | Sami | I'll print the boarding passes by 8 May 2026, provided the beach picnic happens.\n2026-05-04 | Sami | Zara | As long as the ferry crossing is on, I will pack the travel adaptors by 12 May 2026.\n2026-05-04 | Elif | Zara | Absolutely, I will collect the insurance papers by 11 May 2026.\n2026-05-06 | Elif | Yuki | Relax, I'll buy the packing cubes by 13 May 2026, promise.\n2026-05-11 | Elif | Zara | Got myself to collect the insurance papers lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Elif made to collect the insurance papers at the end of 16 May 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q425d305aab",
  "kind": "choice",
  "text": "Tenant and agent back-and-forth on the attic conversion idea, forwarded by Lee.\n\nMembers: Ines, Lee, Malik, Mo\nChat export (date | from | to | message):\n2026-08-19 | Lee | Ines | Absolutely, I will replace the loo roll by 25 August 2026.\n2026-08-21 | Mo | Malik | Count on me to turn the heating timer by 25 August 2026, if the house insurance review happens.\n2026-08-23 | Mo | group | Just so you know, the house insurance review is on as scheduled.\n2026-08-23 | Ines | Malik | It's on me to defrost the top freezer by 30 August 2026.\n2026-08-24 | Ines | Mo | As long as the water tank check is on, I'll drop the parcel upstairs by 1 September 2026.\n2026-08-26 | Lee | Ines | Don't sweat it, there's no need to defrost the top freezer",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Ines's promise to defrost the top freezer at the end of 29 August 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "qc48c6ecd15",
  "kind": "choice",
  "text": "Jonas shared this family chat about the home adaptations for the relatives.\n\nMembers: Kofi, Jonas, Ana\nChat log (oldest first):\n[2 Nov 2026] Jonas: @Kofi I'll print the care schedule by Friday, 6 November 2026, promise.\n[2 Nov 2026] Ana: @Jonas Forget it, you won't need to print the care schedule\n[6 Nov 2026] Kofi: @Jonas You can bet I'll call the home nurse by Sunday, 15 November 2026.\n[7 Nov 2026] Ana: @Kofi I will book the clinic transport by Tuesday, 10 November 2026 only if the physio session happens.\n[7 Nov 2026] Kofi: We are dropping the physio session from the list.\n[7 Nov 2026] Jonas: @Ana I will set up the medicine dispenser by Wednesday, 11 November 2026 only if the carer handover happens.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Jonas made to print the care schedule, what state is it in at the end of Friday, 6 November 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q585b369430",
  "kind": "yes/no",
  "text": "Subject: Chat about the school fundraiser\nBelow, with Jonas named as the source, is the chat as exported.\n\nMembers: Jonas, Elif, Sami, Kai\nChat export (date | from | to | message):\n2026-06-16 | Elif | Sami | Absolutely, I will book the school hall by 22 Jun 2026.\n2026-06-21 | Kai | Elif | I will count the donation boxes by 25 Jun 2026 only if the governors meeting happens.\n2026-06-21 | Sami | group | Fab, we are on for the governors meeting as planned!\n2026-06-21 | Elif | Kai | Provided the summer fete happens, I'll return the borrowed trestle tables by 23 Jun 2026.\n2026-06-25 | Jonas | Kai | Quick update: you do not need to count the donation boxes at all.\n2026-06-28 | Kai | Elif | Guess what, I managed to count the donation boxes!",
  "question": "According to the card's rules, is the promise Kai made to count the donation boxes not kept as of 26 Jun 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1e19723b35",
  "kind": "yes/no",
  "text": "Shared by Sami, this thread covers the playground project for whoever is at the help desk.\n\nMembers: Greta, Rhea, Sami\nChat export (date | from | to | message):\n2026-01-28 | Sami | Rhea | Promise to collect the bake sale tins by 2 Feb 2026 if the reading festival goes ahead.\n2026-01-29 | Greta | Rhea | I will make sure to count the donation boxes by 31 Jan 2026.\n2026-01-30 | Greta | group | Sorry all, the reading festival is called off.\n2026-01-31 | Sami | Rhea | Any chance I can collect the bake sale tins by 5 Feb 2026 instead?\n2026-01-31 | Rhea | Sami | No change, you need to collect the bake sale tins by the original date.",
  "question": "Looking over the chat at the end of 31 Jan 2026, did Sami break the promise to collect the bake sale tins?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qfca608ae26",
  "kind": "yes/no",
  "text": "Attached chat: the spring campaign\nShared by: Sami\n\nMembers: Hana, Tomas, Sami\nChat export (date | from | to | message):\n2026-10-09 | Sami | Hana | Count on me, I'll fetch the campaign budget sheet by 12 Oct 2026.\n2026-10-10 | Sami | Hana | Guaranteed I'll send the newsletter copy by 13 Oct 2026.\n2026-10-11 | Tomas | Hana | As long as the brand photo shoot is on, I will draft the press release by 14 Oct 2026.\n2026-10-12 | Tomas | group | Sad to report that the brand photo shoot is off.\n2026-10-14 | Sami | Hana | For the record: I was able to send the newsletter copy",
  "question": "Has Sami kept the promise to send the newsletter copy as of 14 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q207edd6815",
  "kind": "yes/no",
  "text": "Sami saved this so we stay on the same page about the cellar project, mates.\n\nMembers: Ana, Tess, Sami, Leila\nChat log (oldest first):\n[25 Jul 2026] Sami: @Leila Lovely, I'll wash the sash windows by Monday, July 27, 2026 for sure.\n[25 Jul 2026] Leila: @Sami Quick update: you do not need to wash the sash windows at all.\n[27 Jul 2026] Tess: @Sami Committing to oil the back door hinges by Thursday, July 30, 2026.\n[30 Jul 2026] Sami: @Ana As long as the loft clearance day is on, I'll defrost the old fridge by Friday, August 7, 2026.\n[2 Aug 2026] Tess: @Sami Guess who managed to oil the back door hinges, go team!\n[3 Aug 2026] Ana: Afraid the loft clearance day is called off.",
  "question": "By the close of Tuesday, August 4, 2026, is the promise Tess made to oil the back door hinges kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q551c8960ab",
  "kind": "choice",
  "text": "Ines shared this so the guest welcome plan is easy to find, flatmates.\n\nMembers: Femi, Lee, Ines\nChat log (oldest first):\n[5 Jun 2026] Lee: @Femi I'll wash the beach towels by 9 Jun 2026, promise.\n[5 Jun 2026] Lee: @Ines Lovely, I'll wheel the bins out by 12 Jun 2026 for sure.\n[7 Jun 2026] Femi: @Ines I'll collect the bed linen by 14 Jun 2026, provided the lettings photo shoot happens.\n[7 Jun 2026] Lee: @Ines I will vacuum the holiday cottage by 13 Jun 2026 only if the summer season launch happens.\n[11 Jun 2026] Lee: @Ines For the record: I was able to wheel the bins out\n[12 Jun 2026] Lee: Team, the lettings photo shoot stays on as booked.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Lee's promise to wheel the bins out stand at the end of 17 Jun 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q5055fed99b",
  "kind": "yes/no",
  "text": "Chat attached to a support case about the platform rewrite, shared by Sami.\n\nMembers: Sami, Greta\nChat log (oldest first):\n[14 Mar 2026] Sami: @Greta As long as the server migration is on, I will write the release notes by 21 Mar 2026.\n[15 Mar 2026] Sami: @Greta I promise to run the security scan by 24 Mar 2026.\n[19 Mar 2026] Greta: @Sami I'll review the pull request by 27 Mar 2026, provided the sprint demo happens.\n[20 Mar 2026] Sami: @Greta You can bank on me to update the dependency list by 23 Mar 2026.\n[22 Mar 2026] Sami: Really pleased to say the sprint demo will go ahead!\n[26 Mar 2026] Greta: @Sami Mate, I promised, may I review the pull request by 29 Mar 2026 instead?",
  "question": "Going by the card's rules, does Greta keep the promise to review the pull request at the end of 26 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2e5d9f50db",
  "kind": "choice",
  "text": "Jonas shared this family chat about the home adaptations for the relatives.\n\nMembers: Kofi, Jonas, Ana\nChat log (oldest first):\n[2 Nov 2026] Jonas: @Kofi I'll print the care schedule by Friday, 6 November 2026, promise.\n[2 Nov 2026] Kofi: @Jonas Forget it, you won't need to print the care schedule\n[6 Nov 2026] Kofi: @Jonas You can bet I'll call the home nurse by Sunday, 15 November 2026.\n[7 Nov 2026] Ana: @Kofi I will book the clinic transport by Tuesday, 10 November 2026 only if the physio session happens.\n[7 Nov 2026] Kofi: We are dropping the physio session from the list.\n[7 Nov 2026] Jonas: @Ana I will set up the medicine dispenser by Wednesday, 11 November 2026 only if the carer handover happens.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Jonas made to print the care schedule, what state is it in at the end of Friday, 6 November 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "qefa9c62eb0",
  "kind": "choice",
  "text": "Tess shared this channel export covering the spring campaign for the team.\n\nMembers: Yuki, Wren, Femi, Tess\nChat export (date | from | to | message):\n2026-04-05 | Yuki | Tess | It's on me to pay the printing invoice by 13 Apr 2026.\n2026-04-08 | Yuki | Wren | I'll draft the press release by 11 Apr 2026 if the annual review goes ahead.\n2026-04-10 | Yuki | group | Fab, we are on for the annual review as planned!\n2026-04-11 | Yuki | Tess | Update on my side: I will not pay the printing invoice, sorry.\n2026-04-11 | Yuki | Wren | Is 16 Apr 2026 alright for me to draft the press release?\n2026-04-11 | Wren | Yuki | Revised deadline is 16 Apr 2026, so you can draft the press release.\n2026-04-12 | Tess | Yuki | Nobody needs you to draft the press release, that's that",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Yuki due to draft the press release at the end of 12 Apr 2026, after any agreed rescheduling?",
  "options": [
   "16 Apr 2026",
   "11 Apr 2026",
   "13 Apr 2026"
  ]
 },
 {
  "qid": "qdfb5aa402b",
  "kind": "choice",
  "text": "Subject: Saved thread about the travel plans\nThis export from Ivo is pasted in full for readers who want it.\n\nMembers: Ivo, Malik, Yuki\nChat export (date | from | to | message):\n2026-05-30 | Ivo | Yuki | If the flight check-in goes ahead, I'll fill the car boot by 7 June 2026.\n2026-06-02 | Yuki | Malik | Lovely, I'll return the rental car keys by 5 June 2026 for sure.\n2026-06-02 | Malik | Yuki | You don't have to return the rental car keys at all\n2026-06-05 | Malik | group | Team, the flight check-in is not happening.\n2026-06-06 | Ivo | Yuki | On my action item, may I fill the car boot by 11 June 2026 instead?\n2026-06-07 | Malik | Ivo | Yes, you can fill the car boot by 11 June 2026 if that suits you.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Ivo's commitment to fill the car boot is in what status at the end of 11 June 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Waived",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "qaff6cbf2f8",
  "kind": "yes/no",
  "text": "We are getting ready for the street watch scheme, and Bruno shared this chat with us.\n\nMembers: Elif, Dara, Jonas, Bruno\nChat log (oldest first):\n[22 Jul 2026] Dara: @Bruno Absolutely, I will walk the old spaniel by 26 July 2026.\n[22 Jul 2026] Dara: @Bruno Scratch that, I'm not going to walk the old spaniel\n[23 Jul 2026] Elif: @Jonas If the hedge trimming day goes ahead, I'll feed the cat across the road by 28 July 2026.\n[25 Jul 2026] Jonas: @Elif I'll clear the hedge trimmings by 2 August 2026 if the parking permit visit goes ahead.\n[26 Jul 2026] Bruno: Yep, the hedge trimming day is on as planned.\n[28 Jul 2026] Elif: @Jonas Got myself to feed the cat across the road lol.",
  "question": "Is the promise Elif made to feed the cat across the road in a status other than broken at the end of 30 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q12341eb769",
  "kind": "yes/no",
  "text": "Here is the thread on the guest review drive, posted by Sami for the house.\n\nMembers: Ana, Yuki, Sami\nChat log (oldest first):\n[16 Aug 2026] Sami: @Yuki Relax, I'll change the lounge bulb by 19 August 2026, promise.\n[16 Aug 2026] Ana: @Yuki Only if the lettings photo shoot is on, I will scrub the hot tub by 23 August 2026.\n[17 Aug 2026] Sami: @Yuki Sorry, I won't change the lounge bulb after all\n[18 Aug 2026] Ana: @Sami You don't have to change the lounge bulb at all\n[21 Aug 2026] Ana: Sorry all, the lettings photo shoot is called off.",
  "question": "By the close of 18 August 2026, is the promise Sami made to change the lounge bulb kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q85b8fae676",
  "kind": "choice",
  "text": "Tomas shared this so the training plan is easy to follow for the volunteers.\n\nMembers: Femi, Wren, Tomas\nChat log (oldest first):\n[24 Sep 2026] Femi: @Wren If the group ride goes ahead, I'll pump the spare tyres by Thursday, October 1, 2026.\n[25 Sep 2026] Tomas: Sadly, the group ride won't go ahead.\n[26 Sep 2026] Femi: @Wren Committing to fetch the bike stand by Monday, September 28, 2026.\n[1 Oct 2026] Femi: @Wren Would it be fine if I pump the spare tyres by Sunday, October 4, 2026 instead, yeah?\n[1 Oct 2026] Wren: @Femi Nah, that deadline counts, mate, so please pump the spare tyres!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Femi's promise to pump the spare tyres sit at the end of Saturday, October 3, 2026, exactly?",
  "options": [
   "Broken",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q7145ae240f",
  "kind": "yes/no",
  "text": "Shared by Dara for the committee, this is the group chat on the volunteer roster.\n\nMembers: Tomas, Dara, Ana\nChat export (date | from | to | message):\n2026-06-02 | Dara | Tomas | Promise to count the donation boxes by 9 June 2026 if the clothes swap goes ahead.\n2026-06-04 | Tomas | Dara | Relax, I'll wrap the prize hampers by 8 June 2026 for sure.\n2026-06-04 | Ana | Tomas | Ah, no stress, no need for you to wrap the prize hampers\n2026-06-07 | Tomas | group | Yep, the clothes swap is on as planned.\n2026-06-08 | Ana | Dara | Don't sweat it, there's no need to count the donation boxes",
  "question": "Going by the card's rules, does Dara keep the promise to count the donation boxes at the end of 10 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6d9e00da60",
  "kind": "choice",
  "text": "Shared by Kai, this thread covers the rebrand package as pasted from email.\n\nMembers: Kai, Elif, Bruno\nChat log (oldest first):\n[13 Feb 2026] Bruno: @Kai I own this, I'll send the moodboard files by 22 February 2026.\n[14 Feb 2026] Bruno: @Kai I assure you I'll update the icon set by 20 February 2026 if the sign reveal is on.\n[14 Feb 2026] Elif: @Kai I will upload the sticker artwork by 21 February 2026.\n[16 Feb 2026] Bruno: @Elif Lovely, I'll check the poster proofs by 24 February 2026 if the print run is on.\n[22 Feb 2026] Elif: Brilliant news everyone, the print run is a go!\n[23 Feb 2026] Kai: @Bruno Don't sweat it, there's no need to check the poster proofs",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Bruno's promise to check the poster proofs at the end of 27 February 2026?",
  "options": [
   "Broken",
   "Waived",
   "Kept",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qa487902b9a",
  "kind": "choice",
  "text": "Mo saved this so we stay on the same page about the house refit, mates.\n\nMembers: Wren, Malik, Mo\nChat export (date | from | to | message):\n2026-06-25 | Wren | Mo | I assure you I'll measure the hallway for shelves by Wednesday, July 1, 2026 if the removal van arrival is on.\n2026-06-27 | Malik | group | Quick heads up, the removal van arrival is scrapped.\n2026-06-30 | Wren | Malik | I own this, I'll sweep the dust from stairs by Sunday, July 5, 2026.\n2026-07-01 | Wren | Mo | You can bank on me to pick up the grout bag by Friday, July 3, 2026.\n2026-07-01 | Malik | group | Update on your plan to sweep the dust from stairs?\n2026-07-04 | Wren | Malik | Is Thursday, July 9, 2026 alright for me to sweep the dust from stairs?\n2026-07-05 | Mo | Wren | Yes, you're welcome to sweep the dust from stairs by Thursday, July 9, 2026 instead.\n2026-07-06 | Wren | Malik | To my relief, I managed to sweep the dust from stairs.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Wren supposed to sweep the dust from stairs by, going by the chat at the end of Sunday, July 12, 2026 and any agreed changes?",
  "options": [
   "Thursday, July 9, 2026",
   "Sunday, July 5, 2026",
   "Friday, July 3, 2026"
  ]
 },
 {
  "qid": "qef58df571c",
  "kind": "yes/no",
  "text": "Shared by Priya, a help-desk thread covering the flat upgrade list.\n\nMembers: Priya, Greta\nChat log (oldest first):\n[24 Apr 2026] Priya: @Greta Only if the boiler annual check is on, I will measure the kitchen for fridge by April 30, 2026.\n[26 Apr 2026] Priya: @Greta Relax, I'll wipe the cooker hood by May 3, 2026, promise.\n[27 Apr 2026] Greta: @Priya Lovely, I'll ring the flat repair line by May 6, 2026 for sure.\n[28 Apr 2026] Priya: @Greta Ticked off: wipe the cooker hood, feels so good\n[29 Apr 2026] Priya: @Greta Provided the rent review meeting happens, I will email the leak photos by May 2, 2026.",
  "question": "Would you say Priya didn't keep the promise to wipe the cooker hood by the end of April 28, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7ab3d208aa",
  "kind": "yes/no",
  "text": "Dara shared this so the playground project is easy to follow for the volunteers.\n\nMembers: Ravi, Rhea, Bruno, Dara\nChat export (date | from | to | message):\n2026-06-29 | Dara | Ravi | If the reading festival is on, I'll definitely set up the book stall by 5 July 2026.\n2026-06-30 | Dara | Ravi | I'll see if I can label the raffle prizes by 8 July 2026.\n2026-07-01 | Dara | Rhea | Got it, I'll label the raffle prizes by 7 July 2026 for sure.\n2026-07-04 | Dara | Rhea | Scratch that, I'm not going to label the raffle prizes\n2026-07-04 | Ravi | group | Sorry all, the reading festival is not happening.\n2026-07-05 | Bruno | Dara | Committing to wrap the prize hampers by 12 July 2026.",
  "question": "Applying the rules on the card, can Dara's promise to label the raffle prizes be said to have not been broken at the end of 6 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbbbc299847",
  "kind": "yes/no",
  "text": "Here is the thread on the garden shed build, posted by Kofi for the house.\n\nMembers: Kofi, Kai, Jonas, Sami\nChat log (oldest first):\n[6 Mar 2026] Kofi: @Jonas Promise to dig the potato patch by 10 March 2026 if the water tank delivery goes ahead.\n[7 Mar 2026] Kofi: @Jonas I promise to weed the carrot row by 12 March 2026.\n[7 Mar 2026] Kofi: @Jonas Log entry: weed the carrot row, carried out\n[8 Mar 2026] Jonas: Team, the water tank delivery stays on as booked.\n[9 Mar 2026] Kofi: @Jonas Any chance I can dig the potato patch by 13 March 2026 instead?",
  "question": "Did Kofi keep the promise to dig the potato patch as of 10 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qde1a509dc3",
  "kind": "choice",
  "text": "Committee chat on the new kit design, forwarded by Greta to the volunteers.\n\nMembers: Dara, Greta, Yuki\nChat log (oldest first):\n[5 Feb 2026] Greta: @Yuki Count on me to tune the gear cables by 13 February 2026 if the mechanics clinic is on.\n[11 Feb 2026] Yuki: Update: the mechanics clinic is going ahead as planned.\n[11 Feb 2026] Greta: @Yuki Would it be fine if I tune the gear cables by 16 February 2026 instead, yeah?\n[11 Feb 2026] Yuki: @Greta I will make sure to pump the spare tyres by 17 February 2026.\n[12 Feb 2026] Dara: @Greta Go ahead and tune the gear cables by 16 February 2026, that is fine.\n[13 Feb 2026] Dara: @Greta No worries, you don't need to tune the gear cables\n[16 Feb 2026] Greta: @Yuki Guess what, I managed to tune the gear cables!",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Greta to tune the gear cables at the end of 15 February 2026, counting any agreed change of date?",
  "options": [
   "17 February 2026",
   "13 February 2026",
   "16 February 2026"
  ]
 },
 {
  "qid": "qb37b7cda92",
  "kind": "yes/no",
  "text": "Parents and cousins, this is where we sort out the loft conversion. Saved by Sami.\n\nMembers: Nadia, Sami, Lena\nChat export (date | from | to | message):\n2026-10-08 | Nadia | Sami | If the boiler install visit goes ahead, I'll pay the plumbing invoice by 15 October 2026.\n2026-10-08 | Nadia | Lena | As long as the damp survey inspection is on, I will return the tile cutter by 13 October 2026.\n2026-10-11 | Lena | Sami | Count on me to hang the new curtain rail by 19 October 2026.\n2026-10-13 | Lena | group | Scrapping the boiler install visit, apologies to all.\n2026-10-19 | Lena | Sami | Mate, I promised, may I hang the new curtain rail by 23 October 2026 instead?\n2026-10-19 | Sami | Lena | No, you need to hang the new curtain rail by the original date.",
  "question": "Applying the card's rules, can it be said that Nadia has not kept the promise to pay the plumbing invoice at the end of 18 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2b27fb8662",
  "kind": "yes/no",
  "text": "Client thread on the online store move, saved by Leila for the project log.\n\nMembers: Ana, Leila, Malik\nChat log (oldest first):\n[14 Jun 2026] Ana: @Malik I will make sure to restore the old theme by 21 Jun 2026.\n[15 Jun 2026] Malik: @Ana No worries, you don't need to restore the old theme\n[16 Jun 2026] Ana: @Leila Count on me to update the product photos by 23 Jun 2026 if the stock count is on.\n[17 Jun 2026] Malik: @Ana I'll be sure to set up the email forwarding by 24 Jun 2026.\n[17 Jun 2026] Malik: Yay, the stock count is all set to go!",
  "question": "Would you say Ana didn't keep the promise to update the product photos by the end of 24 Jun 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q356d4340d7",
  "kind": "yes/no",
  "text": "Malik shared this support thread, which is about the kitchen refit.\n\nMembers: Elif, Lee, Malik\nChat log (oldest first):\n[11 May 2026] Malik: @Lee As long as the lease renewal call is on, I'll collect the spare flat keys by 16 May 2026.\n[12 May 2026] Lee: Sadly, the lease renewal call is not going ahead.\n[12 May 2026] Malik: @Lee You can bank on me to bring the step stool by 17 May 2026.\n[16 May 2026] Malik: @Lee Think 22 May 2026 would work if I collect the spare flat keys instead?\n[16 May 2026] Elif: @Malik Yes, you have the green light to collect the spare flat keys by 22 May 2026.",
  "question": "Under the rules on the card, is the promise Malik made to collect the spare flat keys kept as of 20 May 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qcde759634c",
  "kind": "yes/no",
  "text": "Rhea forwarded this for the committee as we dig in on the school fundraiser.\n\nMembers: Rhea, Yuki, Femi, Omar\nChat export (date | from | to | message):\n2026-09-20 | Omar | Femi | I own this, I'll label the raffle prizes by 28 September 2026.\n2026-09-21 | Yuki | group | Not promising, but I'll try to wrap the prize hampers by 2 October 2026.\n2026-09-22 | Omar | Femi | If the summer fete goes ahead, I'll book the school hall by 1 October 2026.\n2026-09-22 | Yuki | Rhea | I'll be sure to wrap the prize hampers by 30 September 2026.\n2026-09-28 | Omar | Femi | As long as the field day is on, I'll return the borrowed trestle tables by 4 October 2026.\n2026-09-30 | Rhea | Yuki | You don't have to wrap the prize hampers at all",
  "question": "Applying the rules on the card, can Yuki's promise to wrap the prize hampers be said to have not been broken at the end of 1 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc37e8fe055",
  "kind": "yes/no",
  "text": "Shared by Hana, a help-desk thread covering the choir tour.\n\nMembers: Hana, Lena, Greta\nChat log (oldest first):\n[18 Jun 2026] Greta: @Lena Ticket's mine, I'll print the song sheets by 20 Jun 2026.\n[20 Jun 2026] Hana: @Lena If the carol concert is on, I'll definitely buy the spare folders by 25 Jun 2026.\n[20 Jun 2026] Lena: Really pleased to say the carol concert will go ahead!\n[23 Jun 2026] Hana: @Lena Mind giving me until 1 Jul 2026 to buy the spare folders?\n[25 Jun 2026] Hana: @Lena For the record: I was able to buy the spare folders",
  "question": "By the close of 1 Jul 2026, is the promise Hana made to buy the spare folders kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2680a90417",
  "kind": "yes/no",
  "text": "Tenant and landlord back-and-forth on the lodger house rules, saved by Kofi.\n\nMembers: Ana, Oskar, Wren, Kofi\nChat export (date | from | to | message):\n2026-07-15 | Kofi | Wren | Provided the fuse box inspection happens, I will buy the washing powder by 19 July 2026.\n2026-07-15 | Kofi | Ana | Relax, I'll replace the loo roll by 20 July 2026 for sure.\n2026-07-17 | Kofi | Ana | On my action item, may I replace the loo roll by 24 July 2026 instead?\n2026-07-17 | Oskar | Kofi | Fine by me, you can replace the loo roll by 24 July 2026.\n2026-07-18 | Ana | group | Update, the fuse box inspection will not take place.",
  "question": "Is Kofi's promise to replace the loo roll broken, waived, not triggered or not yet due as of 20 July 2026, instead of kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
