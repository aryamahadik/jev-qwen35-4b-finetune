# G5-H blind read T32-blind_read-5df20cb2-000 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T32/qc/g5h/answers/T32-blind_read-5df20cb2-000.json

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
  "qid": "qe4bdba6be9",
  "kind": "yes/no",
  "text": "Chat from the support case covering the league run, exported by Kai.\n\nMembers: Kai, Elif, Leila\nChat log (oldest first):\n[21 Mar 2026] Kai: @Leila I'll try to set up the corner flags by 2 Apr 2026, can't promise!\n[23 Mar 2026] Kai: @Leila It's on me to set up the corner flags by 30 Mar 2026.\n[23 Mar 2026] Kai: @Elif Count on me to mark the pitch lines by 25 Mar 2026 if the presentation evening is on.\n[23 Mar 2026] Kai: Lovely, the presentation evening is definitely happening!\n[27 Mar 2026] Elif: @Kai Relax, mate, you're not expected to set up the corner flags\n[27 Mar 2026] Kai: @Leila Ta-da, I went and did it: set up the corner flags!",
  "question": "Does the card's rule set show that Kai has not kept the promise to set up the corner flags at the end of 30 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4e4e87629b",
  "kind": "choice",
  "text": "Freelance chat about the big day\nThe client side, saved by Priya.\n\nMembers: Kai, Mo, Hana, Priya\nChat log (oldest first):\n[29 Jun 2026] Kai: @Mo Count on me to book the assistant photographer by 8 July 2026.\n[1 Jul 2026] Priya: @Kai You can bet I'll fetch the spare memory cards by 7 July 2026.\n[1 Jul 2026] Priya: @Mo Provided the rehearsal dinner happens, I will pick up the album prints by 6 July 2026.\n[1 Jul 2026] Kai: Please note the rehearsal dinner will proceed.\n[5 Jul 2026] Mo: Checking you mean to fetch the spare memory cards?\n[7 Jul 2026] Hana: @Priya No need to fetch the spare memory cards, I'm letting you off",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Priya's commitment to fetch the spare memory cards is in what status at the end of 8 July 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Waived",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "qb734c352d6",
  "kind": "yes/no",
  "text": "Leila shared this channel export covering the visitor policy for the team.\n\nMembers: Ivo, Nadia, Omar, Leila\nChat log (oldest first):\n[9 Jul 2026] Nadia: @Ivo If the coffee morning goes ahead, I'll gladly book the boardroom by 11 July 2026.\n[10 Jul 2026] Nadia: Lovely, the coffee morning is definitely happening!\n[11 Jul 2026] Leila: @Nadia Guaranteed I'll send the expense receipts by 14 July 2026.\n[13 Jul 2026] Ivo: @Leila Good news, you're let off having to send the expense receipts\n[16 Jul 2026] Leila: @Nadia Mum, I did send the expense receipts, haha.\n[17 Jul 2026] Nadia: Checking you mean to send the expense receipts?",
  "question": "Did Leila keep the promise to send the expense receipts as of 15 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa5803ed861",
  "kind": "yes/no",
  "text": "Letting agent thread with tenants on the attic conversion idea, copied out by Malik.\n\nMembers: Malik, Rhea, Yuki, Femi\nChat export (date | from | to | message):\n2026-07-11 | Malik | Yuki | Count on me to sort the recycling bags by Sunday, 19 July 2026.\n2026-07-13 | Yuki | Femi | It's on me to buy the washing powder by Friday, 17 July 2026.\n2026-07-13 | Femi | group | Thanks, got it.\n2026-07-15 | Yuki | Femi | For the record: I was able to buy the washing powder\n2026-07-17 | Femi | Rhea | I promise to turn the heating timer by Monday, 20 July 2026 if the fuse box inspection is on.\n2026-07-18 | Rhea | Femi | I'll feed the house plants by Friday, 24 July 2026 as long as the water tank check is on.",
  "question": "Applying the card's rules, can it be said that Yuki has not kept the promise to buy the washing powder at the end of Saturday, 18 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9d5a8de9e4",
  "kind": "choice",
  "text": "Parents and cousins, this is where we sort out the speed bump plan. Saved by Mo.\n\nMembers: Mo, Greta, Kai\nChat log (oldest first):\n[30 Jun 2026] Mo: @Greta I'll be sure to lock the side gate by 4 Jul 2026.\n[1 Jul 2026] Mo: @Greta As long as the bonfire night is on, I'll feed the cat across the road by 7 Jul 2026.\n[2 Jul 2026] Mo: @Greta Mind giving me until 9 Jul 2026 to lock the side gate?\n[2 Jul 2026] Mo: @Kai Count on me to take in the post by 8 Jul 2026, if the street litter clean happens.\n[4 Jul 2026] Kai: @Mo I'll share the garden hose by 7 Jul 2026, promise.\n[4 Jul 2026] Kai: @Mo That suits me, so please lock the side gate by 9 Jul 2026 instead.\n[12 Jul 2026] Mo: @Greta To note: I have managed to lock the side gate",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 10 Jul 2026, by what date does Mo have to lock the side gate, counting any agreed change of date?",
  "options": [
   "9 Jul 2026",
   "4 Jul 2026",
   "7 Jul 2026"
  ]
 },
 {
  "qid": "qd3e2af80ac",
  "kind": "choice",
  "text": "A short note above messages between tenants and the landlord about the kitchen refit, saved by Jonas.\n\nMembers: Nadia, Oskar, Jonas, Rhea\nChat log (oldest first):\n[16 Aug 2026] Oskar: @Jonas Count on me to drop the bin bags off by 24 Aug 2026, if the electrics safety check happens.\n[17 Aug 2026] Nadia: @Rhea I'll be sure to collect the spare flat keys by 19 Aug 2026.\n[17 Aug 2026] Rhea: @Nadia Quick update: you do not need to collect the spare flat keys at all.\n[23 Aug 2026] Jonas: Fab, we are on for the electrics safety check as planned!\n[23 Aug 2026] Oskar: @Jonas Can I drop the bin bags off by 30 Aug 2026 instead? I did promise, sorry.\n[23 Aug 2026] Jonas: @Oskar The original date stands, so you need to drop the bin bags off.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Oskar's commitment to drop the bin bags off have at the end of 24 Aug 2026?",
  "options": [
   "Waived",
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q05e46a8f41",
  "kind": "yes/no",
  "text": "Client messages for a freelancer about the sound mix, saved by Priya.\n\nMembers: Bruno, Tess, Priya, Kofi\nChat export (date | from | to | message):\n2026-09-18 | Priya | Bruno | Relax, I'll send the colour notes by 23 Sep 2026 for sure.\n2026-09-23 | Bruno | Tess | I promise to ship the hard drive by 26 Sep 2026.\n2026-09-23 | Tess | Priya | Provided the client screening happens, I will label the clip folders by 29 Sep 2026.\n2026-09-25 | Kofi | Bruno | I'll upload the render files by 27 Sep 2026, provided the grading session happens.\n2026-09-26 | Tess | Bruno | Forget it, you won't need to ship the hard drive\n2026-09-28 | Tess | group | Brilliant news everyone, the client screening is a go!",
  "question": "By the end of 29 Sep 2026, has Bruno kept the promise to ship the hard drive?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qaa5440b1e2",
  "kind": "choice",
  "text": "Freelancer and client exchange about the guest list, saved by Omar.\n\nMembers: Omar, Dara, Nadia\nChat log (oldest first):\n[10 Oct 2026] Omar: @Dara Promise to fetch the spare memory cards by 18 October 2026 if the venue visit goes ahead.\n[14 Oct 2026] Nadia: @Omar I'll return the lighting stands by 18 October 2026, providing the engagement shoot goes ahead.\n[14 Oct 2026] Omar: @Dara Lovely, I'll pick up the album prints by 17 October 2026 for sure.\n[14 Oct 2026] Dara: Appreciate you telling me.\n[14 Oct 2026] Omar: @Dara Mind giving me until 20 October 2026 to pick up the album prints?\n[15 Oct 2026] Nadia: @Omar Yes, you're welcome to pick up the album prints by 20 October 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Omar made to pick up the album prints have at the end of 18 October 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q7a21745a2a",
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
  "qid": "q671a2cf18b",
  "kind": "choice",
  "text": "Written exchange with the letting agent, covering the guest review drive, which Zara copied into the file.\n\nMembers: Yuki, Dara, Zara\nChat log (oldest first):\n[13 Mar 2026] Zara: @Yuki I own this, I'll collect the bed linen by 22 Mar 2026.\n[14 Mar 2026] Yuki: @Zara I'll wash the beach towels by 18 Mar 2026 if the check out clean goes ahead.\n[15 Mar 2026] Dara: @Zara I'll fill the cleaning cupboard by 22 Mar 2026, promise.\n[15 Mar 2026] Zara: Please note the check out clean will proceed.\n[15 Mar 2026] Yuki: @Zara I committed to wash the beach towels, can I do that by 24 Mar 2026 instead?\n[17 Mar 2026] Yuki: @Dara Committing to restock the guest toiletries by 19 Mar 2026.\n[17 Mar 2026] Zara: @Yuki No, you need to wash the beach towels by the original date.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo what's the latest day Yuki has to wash the beach towels by at the end of 30 Mar 2026, given any new date people agreed to?",
  "options": [
   "22 Mar 2026",
   "18 Mar 2026",
   "24 Mar 2026"
  ]
 },
 {
  "qid": "q17f08616d6",
  "kind": "choice",
  "text": "Subject: the summer getaway, chat copy\nPassed along by Dara, with the full chat below.\n\nMembers: Dara, Zara, Tess, Femi\nChat export (date | from | to | message):\n2026-01-06 | Femi | Tess | I will pack the travel adaptors by 11 Jan 2026 only if the guided tour happens.\n2026-01-08 | Dara | Femi | Guaranteed I'll print the boarding passes by 13 Jan 2026.\n2026-01-09 | Dara | Zara | If the ferry crossing goes ahead, I'll check the passport copies by 15 Jan 2026.\n2026-01-13 | Dara | Femi | Scratch what I said, I won't print the boarding passes.\n2026-01-13 | Tess | Dara | No need to print the boarding passes, I'm letting you off",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhere does Dara stand on the promise to print the boarding passes at the end of 17 Jan 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Broken",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "qddb213d04e",
  "kind": "yes/no",
  "text": "Our flat chat about the house refit, saved by Kofi for whoever lives here.\n\nMembers: Ana, Leila, Kofi\nChat export (date | from | to | message):\n2026-09-17 | Ana | Kofi | Relax, I'll scrape the old wallpaper by 23 September 2026, promise.\n2026-09-18 | Ana | Kofi | Count on me, I'll pay the plumbing invoice by 27 September 2026.\n2026-09-19 | Leila | Ana | I'll fetch the paint samples by 26 September 2026, provided the boiler install visit happens.\n2026-09-21 | Ana | Kofi | Guess what, I managed to scrape the old wallpaper!\n2026-09-22 | Kofi | Ana | I assure you I'll return the tile cutter by 29 September 2026 if the mortgage valuation visit is on.\n2026-09-28 | Ana | group | Quick heads up, the mortgage valuation visit is scrapped.",
  "question": "Was Ana's promise to scrape the old wallpaper not kept as of 26 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q37eabacaba",
  "kind": "yes/no",
  "text": "Committee thread about the junior section, passed on to the group by Kai.\n\nMembers: Greta, Wren, Ana, Kai\nChat log (oldest first):\n[9 Apr 2026] Greta: No promises, but I'll aim to wash the away kit by 19 Apr 2026.\n[11 Apr 2026] Greta: @Ana I'll wash the away kit by 18 Apr 2026, promise.\n[12 Apr 2026] Greta: @Kai Promise to fetch the medical bag by 19 Apr 2026 if the training camp goes ahead.\n[16 Apr 2026] Wren: @Ana I'll mark the pitch lines by 24 Apr 2026, promise.\n[16 Apr 2026] Kai: Brilliant news everyone, the training camp is a go!\n[19 Apr 2026] Greta: @Ana Ticked off my list: wash the away kit, yay.",
  "question": "According to the rules on the card, has Greta broken the promise to wash the away kit at the end of 22 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0c31cb52bd",
  "kind": "choice",
  "text": "Subject: the family photo book, from the group chat\nSharing it here as Kofi saved it.\n\nMembers: Mo, Zara, Kofi\nChat log (oldest first):\n[1 Jul 2026] Zara: I'm aiming to fetch the craft box by Sunday, July 5, 2026, might manage it.\n[1 Jul 2026] Mo: @Zara Only if the puppet show is on, I will walk the dog by Thursday, July 9, 2026.\n[2 Jul 2026] Zara: @Mo You can bank on me to fetch the craft box by Wednesday, July 8, 2026.\n[3 Jul 2026] Mo: @Kofi Lovely, I'll read the bedtime story by Tuesday, July 7, 2026 if the storytime session is on.\n[7 Jul 2026] Mo: @Zara No need to fetch the craft box, I'm letting you off\n[8 Jul 2026] Zara: @Mo Guess who managed to fetch the craft box, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Zara's promise to fetch the craft box stand at the end of Wednesday, July 8, 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q2a5330491d",
  "kind": "choice",
  "text": "{\"record\": \"shared group chat\", \"subject\": \"the big day\", \"shared_by\": \"Ines\", \"stored\": \"as text\"}\n\nMembers: Greta, Leila, Ines\nChat log (oldest first):\n[6 Jun 2026] Ines: @Leila Count on me, I'll print the seating cards by June 13, 2026.\n[9 Jun 2026] Ines: @Greta I'll fetch the spare memory cards by June 12, 2026, provided the venue visit happens.\n[11 Jun 2026] Ines: Update: the venue visit is going ahead as planned.\n[11 Jun 2026] Ines: @Greta Is June 15, 2026 alright for me to fetch the spare memory cards?\n[13 Jun 2026] Ines: @Greta Ticked off my list: fetch the spare memory cards, yay.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Ines made to fetch the spare memory cards, what state is it in at the end of June 18, 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q9f0a275b43",
  "kind": "choice",
  "text": "Forwarded by Elif, this thread on the documentary cut stays attached to the ticket.\n\nMembers: Lee, Elif, Jonas\nChat log (oldest first):\n[22 Oct 2026] Jonas: @Elif Relax, I'll upload the render files by 2026-10-27, promise.\n[23 Oct 2026] Jonas: @Elif Would it be fine if I upload the render files by 2026-10-29 instead, yeah?\n[24 Oct 2026] Elif: @Jonas Yes, you're welcome to upload the render files by 2026-10-29 instead.\n[26 Oct 2026] Elif: @Jonas As long as the shoot day is on, I'll send the colour notes by 2026-11-02.\n[27 Oct 2026] Jonas: @Lee Count on me to back up the project drives by 2026-11-03.\n[28 Oct 2026] Lee: @Jonas Relax, mate, you're not expected to back up the project drives\n[30 Oct 2026] Lee: @Jonas Provided the client screening happens, I'll record the voice over by 2026-11-03.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Jonas supposed to upload the render files by, going by the chat at the end of 2026-11-03 and any agreed changes?",
  "options": [
   "2026-10-27",
   "2026-11-02",
   "2026-10-29"
  ]
 },
 {
  "qid": "qfd0565049b",
  "kind": "choice",
  "text": "Attached chat: the winter concert\nShared by: Kofi\n\nMembers: Elif, Malik, Kofi, Wren\nChat log (oldest first):\n[3 Sep 2026] Malik: Fingers crossed I can collect the sheet music by Thursday, September 10, 2026.\n[5 Sep 2026] Malik: @Elif Count on me to collect the sheet music by Saturday, September 12, 2026, if the voice test happens.\n[5 Sep 2026] Malik: @Elif I'll be sure to return the library scores by Monday, September 14, 2026.\n[7 Sep 2026] Wren: Afraid the voice test is called off.\n[8 Sep 2026] Malik: @Elif Any chance I can collect the sheet music by Wednesday, September 16, 2026 instead?\n[10 Sep 2026] Kofi: @Malik Yes, you have the green light to collect the sheet music by Wednesday, September 16, 2026.",
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
  "qid": "qf9fc085204",
  "kind": "choice",
  "text": "Freelancer and client exchange about the guest list, saved by Omar.\n\nMembers: Omar, Dara, Nadia\nChat log (oldest first):\n[10 Oct 2026] Omar: @Dara Promise to fetch the spare memory cards by 18 October 2026 if the venue visit goes ahead.\n[14 Oct 2026] Nadia: @Omar I'll return the lighting stands by 18 October 2026, providing the engagement shoot goes ahead.\n[14 Oct 2026] Omar: @Dara Lovely, I'll pick up the album prints by 17 October 2026 for sure.\n[14 Oct 2026] Dara: Appreciate you telling me.\n[14 Oct 2026] Omar: @Dara Mind giving me until 20 October 2026 to pick up the album prints?\n[15 Oct 2026] Nadia: @Omar Yes, you're welcome to pick up the album prints by 20 October 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Omar made to pick up the album prints have at the end of 18 October 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q1badafccce",
  "kind": "choice",
  "text": "Freelance thread record, the shop rebuild, shared by Hana.\n\nMembers: Kai, Wren, Hana\nChat log (oldest first):\n[27 Aug 2026] Wren: @Hana Got it, I'll fix the checkout button by 1 Sep 2026 for sure.\n[31 Aug 2026] Kai: @Hana I'll set up the email forwarding by 5 Sep 2026, provided the pop up stall happens.\n[31 Aug 2026] Wren: Fab, we are on for the pop up stall as planned!\n[2 Sep 2026] Wren: @Kai Please don't feel you have to set up the email forwarding\n[7 Sep 2026] Kai: @Hana Mum, I did set up the email forwarding, haha.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Kai's pledge to set up the email forwarding at the end of 5 Sep 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q6ca90311fb",
  "kind": "choice",
  "text": "Volunteers' thread on the new term plans, exported by Mo for the committee.\n\nMembers: Ana, Tess, Mo, Oskar\nChat export (date | from | to | message):\n2026-09-13 | Ana | Mo | Only if the governors meeting is on, I will return the borrowed trestle tables by 17 Sep 2026.\n2026-09-13 | Ana | Oskar | I will count the donation boxes by 22 Sep 2026 only if the clothes swap happens.\n2026-09-15 | Tess | group | We are dropping the governors meeting from the list.\n2026-09-15 | Oskar | Ana | It's on me to send the newsletter drafts by 21 Sep 2026.\n2026-09-18 | Tess | Oskar | No worries, you don't need to send the newsletter drafts\n2026-09-20 | Mo | Ana | I will book the school hall by 29 Sep 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Oskar's promise to send the newsletter drafts receive at the end of 19 Sep 2026?",
  "options": [
   "Waived",
   "Broken",
   "Not triggered",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "qa68ce8b2cc",
  "kind": "yes/no",
  "text": "Work conversation on the trade show push, saved as a file by Lena.\n\nMembers: Bruno, Greta, Jonas, Lena\nChat export (date | from | to | message):\n2026-03-08 | Lena | Bruno | Count on me to pay the printing invoice by 14 Mar 2026 if the product launch is on.\n2026-03-08 | Bruno | group | Ah right, thanks for that.\n2026-03-10 | Bruno | group | Sadly, the product launch won't go ahead.\n2026-03-10 | Greta | Jonas | Got it, I'll return the rented camera gear by 15 Mar 2026 for sure.\n2026-03-12 | Lena | Bruno | On my action item, may I pay the printing invoice by 19 Mar 2026 instead?\n2026-03-12 | Bruno | Lena | We are holding the date on record, so pay the printing invoice by it.",
  "question": "Has Lena broken the promise to pay the printing invoice at the end of 18 Mar 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf42a2d2ab0",
  "kind": "choice",
  "text": "Volunteers, here is the training plan chat that Jonas forwarded to us.\n\nMembers: Dara, Greta, Jonas\nChat log (oldest first):\n[14 Jul 2026] Greta: @Dara Got it, I'll set up the feed stop by 21 July 2026 for sure.\n[14 Jul 2026] Dara: Ah right, thanks for that.\n[14 Jul 2026] Jonas: @Greta You are released, no requirement to set up the feed stop.\n[15 Jul 2026] Greta: @Dara Log entry: set up the feed stop, carried out\n[17 Jul 2026] Jonas: @Greta Lovely, I'll service the tandem bike by 19 July 2026 if the hill climb is on.\n[18 Jul 2026] Greta: Yep, the hill climb is on as planned.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Greta's promise to set up the feed stop receive at the end of 16 July 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q86f9da12e7",
  "kind": "yes/no",
  "text": "Ivo saved this so we stay on the same page about the cellar project, mates.\n\nMembers: Rhea, Ivo, Jonas\nChat log (oldest first):\n[16 May 2026] Rhea: @Jonas I'll mend the garden gate by 22 May 2026, provided the loft clearance day happens.\n[18 May 2026] Jonas: Update: the loft clearance day is going ahead as planned.\n[20 May 2026] Jonas: Update on your plan to mend the garden gate?\n[20 May 2026] Jonas: @Rhea Forget it, you won't need to mend the garden gate\n[20 May 2026] Rhea: @Ivo Got it, I'll scrub the cellar steps by 23 May 2026 for sure.\n[22 May 2026] Rhea: @Ivo Sorry, I won't scrub the cellar steps after all",
  "question": "Would a check of the chat at the end of 21 May 2026 show the promise Rhea made to mend the garden gate as broken?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8776e612bf",
  "kind": "yes/no",
  "text": "Written between tenants and a landlord, this copy concerns the spare room plan. It was saved by Kofi.\n\nMembers: Ivo, Kofi, Tomas, Jonas\nChat export (date | from | to | message):\n2026-01-16 | Jonas | Tomas | I promise to drop the parcel upstairs by 23 Jan 2026.\n2026-01-16 | Jonas | Tomas | Ticked off: drop the parcel upstairs, feels so good\n2026-01-16 | Tomas | Jonas | Lovely, I'll cut a spare door key by 22 Jan 2026 if the house insurance review is on.\n2026-01-16 | Jonas | group | Sorry all, the house insurance review is not happening.\n2026-01-22 | Ivo | Jonas | It's on me to turn the heating timer by 26 Jan 2026.",
  "question": "Per the card's rules, on 21 Jan 2026, has Jonas's promise to drop the parcel upstairs been kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9ddbe9a50b",
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
  "qid": "q2a2082ea10",
  "kind": "choice",
  "text": "{\"archive\": \"group chat\", \"subject\": \"the family photo book\", \"sent_by\": \"Priya\"}\n\nMembers: Wren, Rhea, Priya\nChat log (oldest first):\n[20 Jul 2026] Wren: @Rhea I'll be sure to sort the old photo albums by Monday, July 27, 2026.\n[20 Jul 2026] Wren: @Rhea Quick question, could I sort the old photo albums by Friday, July 31, 2026 instead?\n[25 Jul 2026] Rhea: @Wren That suits me, so please sort the old photo albums by Friday, July 31, 2026 instead.\n[27 Jul 2026] Rhea: @Priya I promise to bake the oat biscuits by Saturday, August 1, 2026 if the garden tea party is on.\n[28 Jul 2026] Wren: Sadly, the garden tea party is not going ahead.\n[29 Jul 2026] Priya: @Rhea Count on me to walk the dog by Saturday, August 1, 2026.\n[30 Jul 2026] Rhea: @Priya I'll be sure to pick up the school bags by Monday, August 3, 2026.\n[31 Jul 2026] Wren: @Rhea To my relief, I managed to sort the old photo albums.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of Thursday, July 30, 2026, what is the date by which Wren has to sort the old photo albums, counting any agreed change?",
  "options": [
   "Saturday, August 1, 2026",
   "Monday, July 27, 2026",
   "Friday, July 31, 2026"
  ]
 },
 {
  "qid": "qba80bea336",
  "kind": "yes/no",
  "text": "Read up on the allotment expansion, flatmates, as Tomas exported it.\n\nMembers: Zara, Tomas, Mo\nChat log (oldest first):\n[24 Feb 2026] Tomas: Hoping to stake the tomato canes by 1 March 2026, can't promise.\n[25 Feb 2026] Tomas: @Zara Guaranteed I'll stake the tomato canes by 5 March 2026.\n[27 Feb 2026] Tomas: @Zara To note: I have managed to stake the tomato canes\n[27 Feb 2026] Mo: @Zara As long as the allotment site visit is on, I'll fix the shed door by 6 March 2026.\n[27 Feb 2026] Tomas: @Zara I will make sure to water the allotment beds by 2 March 2026.\n[4 Mar 2026] Mo: Really pleased to say the allotment site visit will go ahead!",
  "question": "Under the rules on the card, is Tomas's promise to stake the tomato canes broken, waived, not triggered or not yet due, rather than kept, as of 27 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7c52bb72d0",
  "kind": "yes/no",
  "text": "Note on the support case\nWhat it covers: the training plan\nPulled by: Yuki\n\nMembers: Oskar, Bruno, Yuki, Tess\nChat log (oldest first):\n[10 Oct 2026] Yuki: @Bruno Might manage to set up the feed stop by 12 October 2026, who knows.\n[11 Oct 2026] Yuki: @Bruno If the mechanics clinic goes ahead, I'll set up the feed stop by 17 October 2026.\n[12 Oct 2026] Bruno: Sad to report that the mechanics clinic is off.\n[12 Oct 2026] Oskar: @Bruno I promise to tune the gear cables by 21 October 2026.\n[13 Oct 2026] Oskar: @Bruno Mate, I promised, may I tune the gear cables by 25 October 2026 instead?\n[19 Oct 2026] Bruno: @Oskar Yes, you have the green light to tune the gear cables by 25 October 2026.",
  "question": "Applying the rules on the card, has Yuki kept the promise to set up the feed stop as of 13 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc0f22d8ca6",
  "kind": "yes/no",
  "text": "Team channel export, shared by Kofi, which is about the visitor policy.\n\nMembers: Femi, Ines, Tess, Kofi\nChat log (oldest first):\n[9 Oct 2026] Kofi: @Femi Lovely, I'll book the boardroom by Thursday, 15 October 2026 if the lease viewing is on.\n[11 Oct 2026] Kofi: @Tess Count on me to return the printer toner by Monday, 19 October 2026.\n[15 Oct 2026] Kofi: @Tess I'll replace the kitchen filters by Thursday, 22 October 2026, providing the coffee morning goes ahead.\n[15 Oct 2026] Femi: @Kofi Don't sweat it, there's no need to return the printer toner\n[19 Oct 2026] Kofi: @Tess Ta-da, I went and did it: return the printer toner!",
  "question": "Is the promise to return the printer toner kept by Kofi as of Saturday, 24 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9edde8aeb5",
  "kind": "choice",
  "text": "Team channel export, shared by Tomas, which is about the peer review.\n\nMembers: Mo, Tomas, Bruno\nChat log (oldest first):\n[30 Jan 2026] Tomas: @Mo Count on me to send the ethics form by 3 Feb 2026 if the safety inspection is on.\n[31 Jan 2026] Mo: Great news, the safety inspection is on!\n[2 Feb 2026] Mo: @Bruno Count on me, I'll order the reagent kit by 6 Feb 2026.\n[2 Feb 2026] Tomas: @Mo Ta-da, I went and did it: send the ethics form!\n[3 Feb 2026] Mo: How's the plan to send the ethics form?\n[4 Feb 2026] Mo: @Bruno Log entry: order the reagent kit, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Tomas's promise to send the ethics form at the end of 3 Feb 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q7ba39505e1",
  "kind": "choice",
  "text": "{\"source\": \"saved thread\", \"about\": \"the reunion planning\", \"owner\": \"Mo\", \"kind\": \"chat export\"}\n\nMembers: Leila, Hana, Mo, Oskar\nChat log (oldest first):\n[22 Sep 2026] Leila: @Oskar I promise to print the family tree chart by 2026-09-28 if the garden picnic is on.\n[22 Sep 2026] Oskar: @Mo I'll try to reserve the reunion hall by 2026-09-30.\n[23 Sep 2026] Leila: Update, the garden picnic will not take place.\n[24 Sep 2026] Oskar: @Hana You can bank on me to reserve the reunion hall by 2026-09-29.\n[28 Sep 2026] Mo: @Oskar No worries, you don't need to reserve the reunion hall\n[29 Sep 2026] Oskar: @Hana Got myself to reserve the reunion hall lol.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Oskar's promise to reserve the reunion hall at the end of 2026-10-04?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q3d8441fff1",
  "kind": "choice",
  "text": "Arlo forwarded this exchange with the landlord on the balcony garden project.\n\nMembers: Nadia, Arlo\nChat log (oldest first):\n[21 Aug 2026] Nadia: @Arlo It's on me to measure the kitchen for fridge by Saturday, August 29, 2026.\n[23 Aug 2026] Arlo: @Nadia You can bet I'll read the meter readings by Saturday, August 29, 2026.\n[23 Aug 2026] Arlo: @Nadia If the lease renewal call goes ahead, I'll collect the spare flat keys by Friday, August 28, 2026.\n[23 Aug 2026] Nadia: Thanks lovely, got it!\n[26 Aug 2026] Arlo: Sad to report that the lease renewal call is off.\n[27 Aug 2026] Nadia: @Arlo Guaranteed I'll remove the bathroom shelf by Thursday, September 3, 2026.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Arlo's promise to collect the spare flat keys at the end of Friday, August 28, 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "qf81bd1d55f",
  "kind": "yes/no",
  "text": "Shared by Tomas for the committee, this is the group chat on the new term plans.\n\nMembers: Tomas, Hana, Kofi\nChat export (date | from | to | message):\n2026-04-28 | Tomas | Kofi | Provided the reading festival happens, I'll count the donation boxes by 2 May 2026.\n2026-04-30 | Kofi | Hana | I will make sure to send the newsletter drafts by 6 May 2026.\n2026-05-01 | Kofi | group | Scrapping the reading festival, apologies to all.\n2026-05-04 | Tomas | Hana | Guaranteed I'll fetch the tea urn by 8 May 2026.\n2026-05-06 | Kofi | Hana | My sincere apologies, I am unable to send the newsletter drafts.\n2026-05-08 | Hana | Tomas | You are released, no requirement to fetch the tea urn.",
  "question": "Has Kofi kept the promise to send the newsletter drafts at the end of 10 May 2026, instead of broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qac9998133e",
  "kind": "yes/no",
  "text": "A written chat between housemates about the family photo book. Exported from the device by Kofi.\n\nMembers: Oskar, Kofi, Hana\nChat log (oldest first):\n[5 May 2026] Kofi: @Hana Might manage to walk the dog by 11 May 2026, who knows.\n[7 May 2026] Kofi: @Hana Provided the seaside outing happens, I'll walk the dog by 15 May 2026.\n[9 May 2026] Hana: @Oskar I will tidy the playroom by 11 May 2026.\n[10 May 2026] Oskar: Scrapping the seaside outing, apologies to all.\n[13 May 2026] Kofi: @Hana Is 21 May 2026 alright for me to walk the dog?\n[13 May 2026] Hana: @Kofi No, I'd like you to walk the dog by the original date.",
  "question": "Did Kofi break the promise to walk the dog at the end of 18 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7c74cd95bf",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the family photo book\nThe thread below comes from Priya and is passed on as it is.\n\nMembers: Priya, Tess, Oskar\nChat log (oldest first):\n[5 Sep 2026] Priya: @Oskar Only if the seaside outing is on, I will read the bedtime story by 8 September 2026.\n[6 Sep 2026] Tess: @Oskar Not promising, but I'll try to pack the picnic basket by 13 September 2026.\n[8 Sep 2026] Tess: @Priya Guaranteed I'll pack the picnic basket by 15 September 2026.\n[10 Sep 2026] Priya: @Tess I promise to bake the oat biscuits by 14 September 2026 if the storytime session is on.\n[13 Sep 2026] Oskar: @Priya Committing to teach the card game by 17 September 2026.\n[15 Sep 2026] Tess: @Priya Guess who managed to pack the picnic basket, go team!",
  "question": "Looking over the chat at the end of 19 September 2026, did Tess break the promise to pack the picnic basket?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q759a3e6100",
  "kind": "choice",
  "text": "Freelance project export\nFrom Malik, covering the honeymoon album with the client.\n\nMembers: Oskar, Malik, Arlo, Rhea\nChat log (oldest first):\n[15 Jul 2026] Rhea: @Malik I'll be sure to print the seating cards by 23 Jul 2026.\n[17 Jul 2026] Arlo: @Malik I'll collect the venue floor plan by 24 Jul 2026, providing the cake tasting goes ahead.\n[18 Jul 2026] Malik: @Rhea Count on me to pick up the album prints by 25 Jul 2026.\n[19 Jul 2026] Oskar: Really pleased to say the cake tasting will go ahead!\n[25 Jul 2026] Rhea: @Malik Ticked off: print the seating cards, feels so good",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Arlo's commitment to collect the venue floor plan is in what status at the end of 24 Jul 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "qf15d406330",
  "kind": "yes/no",
  "text": "Our house group, sorted by Kofi, with the flatmate contract terms up front.\n\nMembers: Kofi, Lee, Nadia\nChat log (oldest first):\n[7 Aug 2026] Kofi: @Nadia Lovely, I'll scan the council tax letter by 10 August 2026 if the freshers welcome night is on.\n[8 Aug 2026] Nadia: @Kofi Absolutely, I will copy the house keys by 11 August 2026.\n[9 Aug 2026] Kofi: Scrapping the freshers welcome night, apologies to all.\n[9 Aug 2026] Kofi: @Nadia On my action item, may I scan the council tax letter by 12 August 2026 instead?\n[9 Aug 2026] Nadia: @Kofi Of course, it is fine for you to scan the council tax letter by 12 August 2026.\n[10 Aug 2026] Kofi: @Nadia You are released, no requirement to copy the house keys.",
  "question": "Under the rules on the card, is the promise Kofi made to scan the council tax letter in a status other than broken at the end of 11 August 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc8a2e3de03",
  "kind": "choice",
  "text": "Volunteers, here is the training plan chat that Jonas forwarded to us.\n\nMembers: Dara, Greta, Jonas\nChat log (oldest first):\n[14 Jul 2026] Greta: @Dara Got it, I'll set up the feed stop by 21 July 2026 for sure.\n[14 Jul 2026] Dara: Ah right, thanks for that.\n[14 Jul 2026] Dara: @Greta You are released, no requirement to set up the feed stop.\n[15 Jul 2026] Greta: @Dara Log entry: set up the feed stop, carried out\n[17 Jul 2026] Jonas: @Greta Lovely, I'll service the tandem bike by 19 July 2026 if the hill climb is on.\n[18 Jul 2026] Greta: Yep, the hill climb is on as planned.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Greta's promise to set up the feed stop receive at the end of 16 July 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q5162104952",
  "kind": "choice",
  "text": "Saved by Mo, this copy of the support chat concerns the family photo book.\n\nMembers: Mo, Bruno, Ana\nChat log (oldest first):\n[25 Oct 2026] Ana: @Bruno Lovely, I'll walk the dog by 29 Oct 2026 if the school play is on.\n[25 Oct 2026] Ana: Sadly, the school play won't go ahead.\n[25 Oct 2026] Ana: @Bruno Think 4 Nov 2026 would work if I walk the dog instead?\n[27 Oct 2026] Bruno: @Ana Aw no, you need to walk the dog by the original date!\n[31 Oct 2026] Bruno: @Ana Ticket's mine, I'll fetch the craft box by 9 Nov 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Ana's promise to walk the dog at the end of 28 Oct 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q3019fd2130",
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
  "qid": "q752ac18b76",
  "kind": "yes/no",
  "text": "Shared by Arlo, an export of a household chat about the home adaptations, as saved.\n\nMembers: Jonas, Arlo, Hana, Ana\nChat log (oldest first):\n[21 Jun 2026] Jonas: @Ana Provided the carer handover happens, I'll drop off the hot meals by Monday, June 29, 2026.\n[23 Jun 2026] Ana: @Arlo You can bet I'll wash the bed linen by Sunday, June 28, 2026.\n[24 Jun 2026] Jonas: @Hana Committing to collect the post by Wednesday, July 1, 2026.\n[25 Jun 2026] Hana: Just so you know, the carer handover is on as scheduled.\n[28 Jun 2026] Jonas: @Hana For the record: I was able to collect the post",
  "question": "Does Jonas's promise to collect the post hold up as kept at the end of Friday, July 3, 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf27f93cf46",
  "kind": "yes/no",
  "text": "Leila shared this channel export covering the visitor policy for the team.\n\nMembers: Ivo, Nadia, Omar, Leila\nChat log (oldest first):\n[9 Jul 2026] Nadia: @Ivo If the coffee morning goes ahead, I'll gladly book the boardroom by 11 July 2026.\n[10 Jul 2026] Nadia: Lovely, the coffee morning is definitely happening!\n[11 Jul 2026] Leila: @Nadia Guaranteed I'll send the expense receipts by 14 July 2026.\n[13 Jul 2026] Ivo: @Leila Good news, you're let off having to send the expense receipts\n[16 Jul 2026] Leila: @Nadia Mum, I did send the expense receipts, haha.\n[17 Jul 2026] Nadia: Checking you mean to send the expense receipts?",
  "question": "Going by the card's rules, does Leila not keep the promise to send the expense receipts at the end of 15 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q447ea9a48a",
  "kind": "choice",
  "text": "Freelance project export\nFrom Bruno, covering the wedding weekend with the client.\n\nMembers: Bruno, Oskar, Tomas\nChat export (date | from | to | message):\n2026-09-01 | Tomas | Oskar | As long as the bridal shower is on, I'll fetch the spare memory cards by 9 September 2026.\n2026-09-03 | Bruno | Tomas | I will make sure to set up the backdrop frame by 10 September 2026.\n2026-09-04 | Bruno | group | We are dropping the bridal shower from the list.\n2026-09-07 | Tomas | Oskar | Can I fetch the spare memory cards by 12 September 2026 instead? I did promise, sorry.\n2026-09-08 | Bruno | Tomas | I'm withdrawing my promise to set up the backdrop frame",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Tomas's promise to fetch the spare memory cards at the end of 6 September 2026?",
  "options": [
   "Waived",
   "Kept",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q7dd1731987",
  "kind": "yes/no",
  "text": "Casual chat for the flat, saved by Wren, and it covers the front garden scheme.\n\nMembers: Wren, Ravi, Arlo\nChat log (oldest first):\n[10 Jun 2026] Arlo: Hoping to clear the hedge trimmings by Friday, June 19, 2026, but can't promise.\n[12 Jun 2026] Arlo: @Wren I will clear the hedge trimmings by Monday, June 15, 2026.\n[13 Jun 2026] Ravi: @Arlo I'll lock the side gate by Tuesday, June 16, 2026 as long as the parking permit visit is on.\n[13 Jun 2026] Wren: Brilliant news everyone, the parking permit visit is a go!\n[14 Jun 2026] Ravi: @Arlo Ah, no stress, no need for you to clear the hedge trimmings\n[15 Jun 2026] Arlo: @Wren To my relief, I managed to clear the hedge trimmings.",
  "question": "By the end of Monday, June 15, 2026, has Arlo kept the promise to clear the hedge trimmings?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3eaf81889d",
  "kind": "yes/no",
  "text": "Attached chat: the store makeover\nShared by: Mo\n\nMembers: Femi, Mo, Oskar, Jonas\nChat log (oldest first):\n[26 Jan 2026] Femi: @Oskar I will check the poster proofs by 2026-01-29 only if the sign reveal happens.\n[27 Jan 2026] Oskar: Sad to report that the sign reveal is off.\n[27 Jan 2026] Mo: @Oskar I'll fetch the brand fonts by 2026-02-05, providing the packaging launch goes ahead.\n[30 Jan 2026] Jonas: @Femi You can bank on me to sketch the packaging mockup by 2026-02-07.\n[31 Jan 2026] Jonas: @Femi For the record: I was able to sketch the packaging mockup\n[2 Feb 2026] Oskar: @Jonas Ticket's mine, I'll mail the business cards by 2026-02-10.",
  "question": "By the end of 2026-02-06, has Jonas kept the promise to sketch the packaging mockup?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q22ee5849b6",
  "kind": "yes/no",
  "text": "Subject: Saved chat on the store makeover\nHere is the export from Ivo, for the record.\n\nMembers: Ivo, Leila\nChat log (oldest first):\n[30 Sep 2026] Leila: @Ivo Relax, I'll collect the photo credits by 5 Oct 2026 for sure.\n[2 Oct 2026] Leila: @Ivo If the gallery install goes ahead, I'll update the icon set by 9 Oct 2026.\n[4 Oct 2026] Leila: @Ivo For the record: I was able to collect the photo credits\n[6 Oct 2026] Leila: Lovely, the gallery install is definitely happening!\n[6 Oct 2026] Leila: @Ivo Ta-da, I went and did it: update the icon set!",
  "question": "When you check the chat at the end of 9 Oct 2026, is the promise Leila made to update the icon set broken?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbdfaf89c52",
  "kind": "choice",
  "text": "{\"kind\": \"exported group chat\", \"about_topic\": \"the music library\", \"sent_by\": \"Wren\"}\n\nMembers: Zara, Arlo, Wren\nChat log (oldest first):\n[12 Aug 2026] Arlo: @Wren If the sing along goes ahead, I'll gladly buy the spare folders by 16 August 2026.\n[14 Aug 2026] Arlo: Lovely, the sing along is definitely happening!\n[15 Aug 2026] Wren: @Zara Absolutely, I will fix the stand microphones by 23 August 2026.\n[15 Aug 2026] Arlo: @Wren It's on me to collect the sheet music by 21 August 2026.\n[17 Aug 2026] Arlo: @Wren Gutted to say I won't collect the sheet music, sorry team\n[18 Aug 2026] Wren: @Zara I regret to say that I shall not fix the stand microphones.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Arlo made to buy the spare folders at the end of 19 August 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not triggered",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qcc8d83065e",
  "kind": "choice",
  "text": "Subject: saved chat, the loft conversion\nBelow is the chat that Arlo saved for reference.\n\nMembers: Ana, Arlo, Femi\nChat export (date | from | to | message):\n2026-09-11 | Ana | Femi | I'll fetch the paint samples by 16 September 2026, promise.\n2026-09-12 | Arlo | Femi | Relax, I'll hang the new curtain rail by 18 September 2026, promise.\n2026-09-13 | Arlo | Femi | If the removal van arrival goes ahead, I'll gladly pick up the grout bag by 17 September 2026.\n2026-09-14 | Femi | group | Brilliant news everyone, the removal van arrival is a go!\n2026-09-14 | Arlo | Femi | Quick report: I've managed to pick up the grout bag",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Arlo's pledge to pick up the grout bag at the end of 14 September 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q835cdf8a71",
  "kind": "choice",
  "text": "Club volunteers' chat\nSent to the committee by Tess, about the choir tour.\n\nMembers: Tomas, Arlo, Mo, Tess\nChat log (oldest first):\n[10 Mar 2026] Tess: @Tomas I'll collect the sheet music by 13 March 2026, promise.\n[10 Mar 2026] Arlo: @Tess Please don't feel you have to collect the sheet music\n[10 Mar 2026] Arlo: @Mo Lovely, I'll move the piano by 19 March 2026 for sure.\n[14 Mar 2026] Mo: @Arlo If the carol concert goes ahead, I'll set up the sound desk by 23 March 2026.\n[14 Mar 2026] Mo: @Tess Lovely, I'll buy the spare folders by 17 March 2026 if the joint concert is on.\n[18 Mar 2026] Arlo: @Mo Change of plans: I will not move the piano",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Tess made to collect the sheet music at the end of 10 March 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q7ac0393156",
  "kind": "yes/no",
  "text": "{\"archive\": \"group chat\", \"subject\": \"the quiet street fund\", \"sent_by\": \"Oskar\"}\n\nMembers: Oskar, Mo, Kai\nChat log (oldest first):\n[14 May 2026] Kai: @Oskar Relax, I'll lend the stepladder by 23 May 2026 for sure.\n[15 May 2026] Kai: @Oskar I'll lock the side gate by 22 May 2026, providing the hedge trimming day goes ahead.\n[17 May 2026] Mo: @Kai Got it, I'll clear the hedge trimmings by 25 May 2026 for sure.\n[17 May 2026] Oskar: Just so you know, the hedge trimming day is on as scheduled.\n[22 May 2026] Kai: @Oskar Ticked off: lock the side gate, feels so good",
  "question": "Under the rules on the card, is it true that Kai has not kept the promise to lock the side gate as of 22 May 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
