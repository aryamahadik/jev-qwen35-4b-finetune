# G5-H blind read T32-blind_read-016d8c93-001 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root/T32/qc/g5h/answers/T32-blind_read-016d8c93-001.json

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
  "qid": "qe3bc33f342",
  "kind": "yes/no",
  "text": "Family group chat with housemates, covering the garden makeover, exported by Oskar.\n\nMembers: Sami, Rhea, Oskar\nChat export (date | from | to | message):\n2026-04-13 | Rhea | Oskar | I will measure the hallway for shelves by 18 April 2026 only if the damp survey inspection happens.\n2026-04-13 | Rhea | group | Really pleased to say the damp survey inspection will go ahead!\n2026-04-18 | Rhea | Oskar | Quick report: I've managed to measure the hallway for shelves\n2026-04-18 | Oskar | Rhea | Ticket's mine, I'll hang the new curtain rail by 23 April 2026.\n2026-04-20 | Oskar | Rhea | Forget what I said, I won't hang the new curtain rail",
  "question": "On 24 April 2026 itself, has Rhea not kept the promise to measure the hallway for shelves?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q45cb1fb186",
  "kind": "choice",
  "text": "Mo shared this channel export covering the mobile release for the team.\n\nMembers: Mo, Hana\nChat log (oldest first):\n[2 Jun 2026] Mo: @Hana Got it, I'll restart the build server by June 5, 2026 for sure.\n[3 Jun 2026] Hana: @Mo I promise to deploy the staging build by June 11, 2026 if the sprint demo is on.\n[3 Jun 2026] Mo: Got it, cheers!\n[4 Jun 2026] Hana: Sorry all, the sprint demo is not happening.\n[4 Jun 2026] Hana: @Mo Is June 15, 2026 alright for me to deploy the staging build?\n[9 Jun 2026] Mo: @Hana The original date stands, so you need to deploy the staging build.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Hana made to deploy the staging build is in which status at the end of June 11, 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q3dd40f4ab9",
  "kind": "choice",
  "text": "Shared by Zara from the work chat, with the social media plan at its heart.\n\nMembers: Zara, Oskar, Wren\nChat export (date | from | to | message):\n2026-08-06 | Wren | Zara | I assure you I'll fetch the campaign budget sheet by 11 Aug 2026 if the brand photo shoot is on.\n2026-08-06 | Zara | group | Got it, thanks a lot.\n2026-08-10 | Oskar | group | Great news, the brand photo shoot is on!\n2026-08-10 | Zara | Oskar | Count on me to pay the printing invoice by 16 Aug 2026.\n2026-08-11 | Wren | Zara | Is it all right if I fetch the campaign budget sheet by 15 Aug 2026 instead?\n2026-08-11 | Oskar | Wren | Ah, no stress, no need for you to fetch the campaign budget sheet\n2026-08-11 | Wren | Zara | To my relief, I managed to fetch the campaign budget sheet.\n2026-08-15 | Wren | Zara | You don't have to pay the printing invoice at all",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Wren supposed to fetch the campaign budget sheet by, going by the chat at the end of 12 Aug 2026 and any agreed changes?",
  "options": [
   "15 Aug 2026",
   "11 Aug 2026",
   "16 Aug 2026"
  ]
 },
 {
  "qid": "q902ef599f0",
  "kind": "yes/no",
  "text": "Here is the thread on the guest welcome plan, posted by Leila for the house.\n\nMembers: Elif, Leila, Nadia, Lee\nChat log (oldest first):\n[8 Feb 2026] Lee: Hoping to fill the cleaning cupboard by 2026-02-11, but can't promise.\n[10 Feb 2026] Lee: @Nadia Ticket's mine, I'll fill the cleaning cupboard by 2026-02-18.\n[15 Feb 2026] Leila: @Elif Provided the owner handover visit happens, I will change the lounge bulb by 2026-02-23.\n[18 Feb 2026] Lee: @Nadia Think 2026-02-22 would work if I fill the cleaning cupboard instead?\n[18 Feb 2026] Nadia: @Lee Nah, that deadline counts, mate, so please fill the cleaning cupboard!\n[20 Feb 2026] Nadia: Sadly, the owner handover visit won't go ahead.",
  "question": "Would you say Lee kept the promise to fill the cleaning cupboard at the end of 2026-02-21?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qed8ca9a457",
  "kind": "choice",
  "text": "Ivo shared this so the house rules debate is easy to find, flatmates.\n\nMembers: Lena, Tess, Ivo\nChat log (oldest first):\n[31 Mar 2026] Ivo: @Lena I will tidy the boot room by 8 April 2026.\n[1 Apr 2026] Ivo: @Lena Only if the chimney sweep visit is on, I will clear the kitchen sink by 8 April 2026.\n[1 Apr 2026] Tess: @Lena I own this, I'll wash the sash windows by 7 April 2026.\n[1 Apr 2026] Lena: Oh cheers, that helps.\n[4 Apr 2026] Ivo: Really pleased to say the chimney sweep visit will go ahead!\n[7 Apr 2026] Tess: @Lena To note: I have managed to wash the sash windows",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Tess's promise to wash the sash windows have at the end of 7 April 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Broken",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q60df4316a0",
  "kind": "choice",
  "text": "Housemates' chat about the speed bump plan, saved on Sami's device.\n\nMembers: Sami, Jonas, Hana\nChat log (oldest first):\n[16 Feb 2026] Sami: @Hana I will take in the post by 18 Feb 2026.\n[16 Feb 2026] Sami: @Hana Ta-da, I went and did it: take in the post!\n[16 Feb 2026] Jonas: @Hana I'll bring the bins in by 20 Feb 2026, provided the bonfire night happens.\n[17 Feb 2026] Jonas: @Hana Might I ask whether I could bring the bins in by 23 Feb 2026 instead?\n[18 Feb 2026] Hana: @Jonas That suits me, so please bring the bins in by 23 Feb 2026 instead.\n[18 Feb 2026] Jonas: @Sami I will walk the old spaniel by 24 Feb 2026 only if the street litter clean happens.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Jonas made to bring the bins in at the end of 21 Feb 2026?",
  "options": [
   "Kept",
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "qa22e3b5472",
  "kind": "choice",
  "text": "Volunteers, Kofi shared this with you about the league run.\n\nMembers: Jonas, Kofi, Ravi, Ivo\nChat log (oldest first):\n[16 Aug 2026] Kofi: @Jonas I will make sure to repair the goal nets by Tuesday, August 18, 2026.\n[18 Aug 2026] Ivo: @Ravi I'll set up the corner flags by Sunday, August 23, 2026, promise.\n[18 Aug 2026] Ivo: @Ravi To my relief, I managed to set up the corner flags.\n[21 Aug 2026] Ivo: @Kofi I'll wash the away kit by Wednesday, August 26, 2026 as long as the youth trial is on.\n[23 Aug 2026] Ravi: Update: the youth trial is going ahead as planned.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Ivo's pledge to set up the corner flags sit at the end of Sunday, August 23, 2026?",
  "options": [
   "Waived",
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "qb85912cb58",
  "kind": "choice",
  "text": "Landlord and renters' group talk on the garden makeover, from Tomas's export.\n\nMembers: Priya, Oskar, Tomas, Yuki\nChat export (date | from | to | message):\n2026-09-29 | Oskar | Yuki | I'll return the tile cutter by 2 Oct 2026, promise.\n2026-09-30 | Priya | Oskar | Forget it, you won't need to return the tile cutter\n2026-09-30 | Oskar | Tomas | As long as the removal van arrival is on, I'll hang the new curtain rail by 6 Oct 2026.\n2026-10-02 | Oskar | group | Sadly, the removal van arrival won't go ahead.\n2026-10-03 | Oskar | Yuki | Quick report: I've managed to return the tile cutter",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Oskar's pledge to return the tile cutter at the end of 7 Oct 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Waived",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "qbb53fe9bcf",
  "kind": "yes/no",
  "text": "Rented flat, shared group chat, copied by Tomas, filed under the front garden scheme.\n\nMembers: Tess, Tomas, Bruno, Kofi\nChat log (oldest first):\n[12 Aug 2026] Tess: I'll try to return the ladders by August 22, 2026.\n[13 Aug 2026] Tess: @Tomas Count on me to return the ladders by August 20, 2026.\n[14 Aug 2026] Bruno: @Tess If the parking permit visit is on, I'll definitely feed the cat across the road by August 16, 2026.\n[15 Aug 2026] Bruno: Great news, the parking permit visit is on!\n[17 Aug 2026] Tess: @Tomas My sincere apologies, I am unable to return the ladders.\n[20 Aug 2026] Bruno: @Tess No worries, you don't need to return the ladders",
  "question": "As the rules on the card set out, is it the case that Tess has broken the promise to return the ladders at the end of August 22, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9631d2610f",
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
  "qid": "q3f123c4f35",
  "kind": "yes/no",
  "text": "Support case copy, filed for the annual tour\nSaved on record by Priya\n\nMembers: Oskar, Tess, Priya\nChat log (oldest first):\n[30 May 2026] Priya: @Oskar I'll stock the energy gels by 3 June 2026 as long as the hill climb is on.\n[30 May 2026] Tess: Maybe I can print the route cards by 2 June 2026.\n[31 May 2026] Priya: Sadly, the hill climb won't go ahead.\n[1 Jun 2026] Tess: @Priya I will make sure to print the route cards by 8 June 2026.\n[5 Jun 2026] Tess: @Priya Is it all right if I print the route cards by 11 June 2026 instead?\n[5 Jun 2026] Oskar: @Tess Yes, you can print the route cards by 11 June 2026 instead.",
  "question": "Per the rules on the card, does the promise Tess made to print the route cards count as not broken at the end of 9 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5566246737",
  "kind": "yes/no",
  "text": "Team chat export\nAbout the lab move, saved by Ines from the channel.\n\nMembers: Ines, Kai, Hana\nChat log (oldest first):\n[3 Aug 2026] Hana: @Kai I'll print the poster abstracts by 6 August 2026, provided the safety inspection happens.\n[3 Aug 2026] Ines: @Hana Got it, I'll submit the ethics application by 7 August 2026 for sure.\n[5 Aug 2026] Hana: @Ines Lovely, I'll order the reagent kit by 8 August 2026 if the seminar series is on.\n[7 Aug 2026] Ines: @Hana I need to take back my commitment to submit the ethics application.\n[7 Aug 2026] Kai: @Ines No worries, you don't need to submit the ethics application",
  "question": "Under the rules on the card, is Ines's promise to submit the ethics application broken, waived, not triggered or not yet due, rather than kept, as of 8 August 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q385d0f66ca",
  "kind": "yes/no",
  "text": "Subject: chat about the music library, forwarded\nThe chat follows below.\nRegards, Rhea\n\nMembers: Kai, Rhea, Greta, Tomas\nChat log (oldest first):\n[27 Oct 2026] Greta: @Kai I promise to book the rehearsal room by 4 Nov 2026 if the choir festival is on.\n[28 Oct 2026] Greta: @Tomas Lovely, I'll move the piano by 1 Nov 2026 if the summer recital is on.\n[28 Oct 2026] Kai: @Greta Absolutely, I will collect the sheet music by 2 Nov 2026.\n[29 Oct 2026] Kai: @Tomas I promise to fetch the choir robes by 31 Oct 2026.\n[29 Oct 2026] Kai: @Tomas Update on my side: I will not fetch the choir robes, sorry.\n[2 Nov 2026] Greta: @Kai Ah, no stress, no need for you to collect the sheet music",
  "question": "Under the rules on the card, is Kai's promise to collect the sheet music broken, waived, not triggered or not yet due, rather than kept, as of 3 Nov 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5ebac42d8a",
  "kind": "choice",
  "text": "Extract of the club chat on the ground upgrade, copied by Lena for the group.\n\nMembers: Femi, Elif, Lena, Ana\nChat log (oldest first):\n[18 May 2026] Ana: @Lena Count on me to mark the pitch lines by 26 May 2026 if the pre-season friendly is on.\n[20 May 2026] Lena: On track for the pre-season friendly to happen as planned.\n[22 May 2026] Elif: @Femi Count on me to book the changing room by 25 May 2026.\n[23 May 2026] Elif: @Femi Gutted to say I won't book the changing room, sorry team\n[24 May 2026] Lena: @Elif Nobody needs you to book the changing room, that's that",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Elif's promise to book the changing room at the end of 24 May 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Broken",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qee75c87e4f",
  "kind": "yes/no",
  "text": "Flatmates' thread\nExport of the kitchen garden project, passed on by Omar.\n\nMembers: Omar, Lee, Yuki, Priya\nChat log (oldest first):\n[3 Oct 2026] Yuki: @Priya As long as the plot inspection is on, I'll dig the potato patch by 9 October 2026.\n[5 Oct 2026] Lee: @Priya Count on me, I'll stake the tomato canes by 13 October 2026.\n[6 Oct 2026] Priya: @Omar Absolutely, I will water the allotment beds by 14 October 2026.\n[6 Oct 2026] Omar: Cheers, noted.\n[8 Oct 2026] Priya: @Lee Count on me to weed the carrot row by 17 October 2026, if the seed swap day happens.\n[10 Oct 2026] Priya: @Omar My sincere apologies, I am unable to water the allotment beds.",
  "question": "Going by the card's rules, does Priya not keep the promise to water the allotment beds at the end of 11 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qdd4f2ba996",
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
  "qid": "q93d3d2a8a5",
  "kind": "yes/no",
  "text": "Oskar shared this channel export, covering the field survey for the team.\n\nMembers: Oskar, Ivo, Hana, Ana\nChat log (oldest first):\n[24 Jan 2026] Ana: @Ivo You can bank on me to send the ethics form by 26 January 2026.\n[24 Jan 2026] Ivo: @Oskar I'll return the library books by 1 February 2026 if the thesis defence goes ahead.\n[26 Jan 2026] Ana: @Ivo Might I ask whether I could send the ethics form by 28 January 2026 instead?\n[26 Jan 2026] Ivo: @Ana Yes, you can send the ethics form by 28 January 2026 instead.\n[27 Jan 2026] Hana: Sorry all, the thesis defence is not happening.\n[30 Jan 2026] Ivo: @Oskar Would it be fine if I return the library books by 3 February 2026 instead, yeah?",
  "question": "Looking over the chat at the end of 4 February 2026, did Ivo break the promise to return the library books?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q24b2bab6be",
  "kind": "yes/no",
  "text": "Plain text of a family chat with the family day out included, saved by Lee.\n\nMembers: Lee, Tomas, Ines\nChat log (oldest first):\n[30 May 2026] Ines: @Tomas Provided the school play happens, I will read the bedtime story by 6 Jun 2026.\n[2 Jun 2026] Ines: @Tomas If the puppet show goes ahead, I'll pick up the school bags by 11 Jun 2026.\n[2 Jun 2026] Tomas: @Ines I'll pack the picnic basket by 6 Jun 2026, providing the garden tea party goes ahead.\n[4 Jun 2026] Ines: @Tomas I'll be sure to teach the card game by 9 Jun 2026.\n[8 Jun 2026] Lee: @Ines Relax, mate, you're not expected to teach the card game\n[10 Jun 2026] Ines: @Tomas To note: I have managed to teach the card game",
  "question": "Would a check of the chat at the end of 10 Jun 2026 show the promise Ines made to teach the card game as broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q58c1c5cfa4",
  "kind": "yes/no",
  "text": "{\"thread\": \"the grant renewal\", \"exported_by\": \"Femi\", \"shape\": \"group chat\"}\n\nMembers: Ravi, Femi, Kai\nChat export (date | from | to | message):\n2026-06-16 | Ravi | Femi | I'll scan the field notes by 24 June 2026 as long as the safety inspection is on.\n2026-06-18 | Kai | Ravi | Absolutely, I will book the microscope slot by 21 June 2026.\n2026-06-18 | Kai | Ravi | Count on me, I'll print the poster abstracts by 26 June 2026.\n2026-06-19 | Ravi | group | Sadly, the safety inspection is not going ahead.\n2026-06-29 | Kai | Ravi | Guess who managed to print the poster abstracts, go team!",
  "question": "Has Kai broken the promise to print the poster abstracts at the end of 3 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qad8340af31",
  "kind": "choice",
  "text": "Subject: forwarded chat, the sponsor search\nWord for word, the text below came from the saved copy.\nBest, Bruno\n\nMembers: Kofi, Oskar, Tomas, Bruno\nChat log (oldest first):\n[10 Jul 2026] Bruno: @Oskar I'll be sure to return the loaned helmets by 18 Jul 2026.\n[15 Jul 2026] Bruno: @Tomas As long as the bike check is on, I'll tune the gear cables by 21 Jul 2026.\n[15 Jul 2026] Bruno: @Oskar I committed to return the loaned helmets, can I do that by 22 Jul 2026 instead?\n[16 Jul 2026] Kofi: @Oskar I will set up the feed stop by 20 Jul 2026 only if the swap meet happens.\n[16 Jul 2026] Oskar: @Bruno I'll be sure to pump the spare tyres by 19 Jul 2026.\n[17 Jul 2026] Oskar: @Bruno No, I'd like you to return the loaned helmets by the original date.\n[17 Jul 2026] Kofi: @Oskar No worries, you don't need to pump the spare tyres",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs things stand at the end of 24 Jul 2026, which date is the deadline for Bruno to return the loaned helmets, with any agreed change applied?",
  "options": [
   "21 Jul 2026",
   "18 Jul 2026",
   "22 Jul 2026"
  ]
 },
 {
  "qid": "q3353cbc097",
  "kind": "yes/no",
  "text": "We have been planning the speed bump plan here, shared by Ivo.\n\nMembers: Bruno, Ivo, Ines\nChat log (oldest first):\n[17 Oct 2026] Bruno: @Ines It's on me to sweep the pavement outside by 24 Oct 2026.\n[17 Oct 2026] Bruno: @Ines Ticket's mine, I'll return the ladders by 23 Oct 2026.\n[17 Oct 2026] Ines: Oh cheers, that helps.\n[18 Oct 2026] Ivo: @Bruno Only if the hedge trimming day is on, I will bring the bins in by 27 Oct 2026.\n[19 Oct 2026] Bruno: @Ivo I promise to share the garden hose by 26 Oct 2026 if the bonfire night is on.\n[23 Oct 2026] Bruno: @Ines Mum, I did return the ladders, haha.",
  "question": "Applying the card's rules, can it be said that Bruno has not kept the promise to return the ladders at the end of 24 Oct 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6c9588575f",
  "kind": "yes/no",
  "text": "Volunteers, here is the league run thread that Kofi forwarded for us.\n\nMembers: Kofi, Mo, Tomas, Zara\nChat log (oldest first):\n[21 May 2026] Zara: @Tomas I'll collect the referee whistles by 29 May 2026, provided the youth trial happens.\n[21 May 2026] Zara: @Mo If the training camp goes ahead, I'll gladly mark the pitch lines by 26 May 2026.\n[23 May 2026] Zara: @Tomas I will book the changing room by 31 May 2026.\n[25 May 2026] Zara: @Tomas Scratch that, I'm not going to book the changing room\n[28 May 2026] Mo: Just so you know, the youth trial is on as scheduled.\n[29 May 2026] Zara: @Tomas To my relief, I managed to collect the referee whistles.",
  "question": "Was Zara's promise to collect the referee whistles not kept as of 2 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q93207e9d43",
  "kind": "choice",
  "text": "Shared by Priya, this freelance thread with a client is about the store makeover.\n\nMembers: Priya, Lee, Kai, Greta\nChat log (oldest first):\n[2 Jul 2026] Kai: @Lee I promise to export the logo files by Tuesday, 7 July 2026.\n[4 Jul 2026] Kai: @Lee Might I ask whether I could export the logo files by Thursday, 9 July 2026 instead?\n[5 Jul 2026] Lee: @Priya Count on me to mail the business cards by Sunday, 12 July 2026 if the sign reveal is on.\n[5 Jul 2026] Priya: @Kai Yes, all good for you to export the logo files by Thursday, 9 July 2026 instead.\n[10 Jul 2026] Kai: Brilliant news everyone, the sign reveal is a go!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Kai's commitment to export the logo files have at the end of Sunday, 12 July 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q5bc757f4c2",
  "kind": "yes/no",
  "text": "Channel: work team chat\nTopic: the office refit\nExported by Elif.\n\nMembers: Ravi, Yuki, Elif\nChat log (oldest first):\n[5 Feb 2026] Yuki: @Elif Provided the coffee morning happens, I'll collect the visitor badges by 2026-02-11.\n[7 Feb 2026] Ravi: @Elif Relax, I'll print the staff rota by 2026-02-10 for sure.\n[10 Feb 2026] Yuki: @Ravi Ah, no stress, no need for you to print the staff rota\n[10 Feb 2026] Ravi: @Elif Got myself to print the staff rota lol.\n[11 Feb 2026] Ravi: @Yuki I assure you I'll renew the fire extinguisher service by 2026-02-13 if the team lunch is on.\n[12 Feb 2026] Ravi: Brilliant news everyone, the team lunch is a go!",
  "question": "Would you call Ravi's promise to print the staff rota broken, waived, not triggered or not yet due, instead of kept, at the end of 2026-02-10?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qca3d66ad3e",
  "kind": "choice",
  "text": "Casual chat for the flat, saved by Rhea, and it covers the front garden scheme.\n\nMembers: Rhea, Lena, Arlo, Ines\nChat log (oldest first):\n[30 Mar 2026] Ines: @Arlo Relax, I'll lend the stepladder by Tuesday, 7 April 2026, promise.\n[3 Apr 2026] Ines: @Arlo If the road works meeting goes ahead, I'll sweep the pavement outside by Monday, 6 April 2026.\n[4 Apr 2026] Ines: @Arlo Ticket's mine, I'll bring the bins in by Wednesday, 8 April 2026.\n[4 Apr 2026] Ines: Brilliant news everyone, the road works meeting is a go!\n[4 Apr 2026] Ines: @Arlo Any chance I can sweep the pavement outside by Sunday, 12 April 2026 instead?\n[4 Apr 2026] Rhea: @Ines That suits me, so please sweep the pavement outside by Sunday, 12 April 2026 instead.\n[5 Apr 2026] Ines: @Arlo Sorry, I won't bring the bins in after all\n[5 Apr 2026] Lena: @Ines Relax, mate, you're not expected to sweep the pavement outside",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of Wednesday, 15 April 2026, what is the date by which Ines has to sweep the pavement outside, counting any agreed change?",
  "options": [
   "Monday, 6 April 2026",
   "Wednesday, 8 April 2026",
   "Sunday, 12 April 2026"
  ]
 },
 {
  "qid": "q343069c1f4",
  "kind": "choice",
  "text": "Shared by Dara, this thread covers the winter concert for whoever is at the help desk.\n\nMembers: Ivo, Dara, Arlo\nChat log (oldest first):\n[16 Mar 2026] Dara: @Arlo Ticket's mine, I'll send the audition reminders by March 20, 2026.\n[17 Mar 2026] Arlo: @Dara As long as the carol concert is on, I will set up the sound desk by March 23, 2026.\n[20 Mar 2026] Ivo: @Dara Relax, mate, you're not expected to send the audition reminders\n[21 Mar 2026] Ivo: Quick heads up, the carol concert is scrapped.\n[21 Mar 2026] Arlo: @Dara Mate, I promised, may I set up the sound desk by March 25, 2026 instead?\n[23 Mar 2026] Dara: @Arlo Yes, you can set up the sound desk by March 25, 2026 if that suits you.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Arlo's promise to set up the sound desk at the end of March 24, 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Not yet due",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "q060e8abfa5",
  "kind": "choice",
  "text": "Read up on the speed bump plan, flatmates, as Ivo exported it.\n\nMembers: Jonas, Omar, Ivo\nChat log (oldest first):\n[8 Sep 2026] Ivo: @Jonas I'll feed the cat across the road by 16 September 2026, providing the road works meeting goes ahead.\n[11 Sep 2026] Ivo: @Jonas I'll be sure to lock the side gate by 15 September 2026.\n[11 Sep 2026] Jonas: Fab, we are on for the road works meeting as planned!\n[13 Sep 2026] Ivo: @Jonas Ticked off: lock the side gate, feels so good\n[16 Sep 2026] Jonas: @Ivo No need to feed the cat across the road, I'm letting you off",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Ivo's promise to feed the cat across the road have at the end of 16 September 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "qa9f6aea9c1",
  "kind": "yes/no",
  "text": "{\"thread\": \"the field survey\", \"exported_by\": \"Oskar\", \"shape\": \"group chat\"}\n\nMembers: Oskar, Ivo, Hana, Ana\nChat export (date | from | to | message):\n2026-01-24 | Ana | Ivo | You can bank on me to send the ethics form by 26 January 2026.\n2026-01-24 | Ivo | Oskar | I'll return the library books by 1 February 2026 if the thesis defence goes ahead.\n2026-01-26 | Ana | Ivo | Might I ask whether I could send the ethics form by 28 January 2026 instead?\n2026-01-26 | Ivo | Ana | Yes, you can send the ethics form by 28 January 2026 instead.\n2026-01-27 | Hana | group | Sorry all, the thesis defence is not happening.\n2026-01-30 | Ivo | Oskar | Would it be fine if I return the library books by 3 February 2026 instead, yeah?",
  "question": "Looking over the chat at the end of 4 February 2026, did Ivo break the promise to return the library books?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0ced6a6dbe",
  "kind": "yes/no",
  "text": "Flat chat, exported by Nadia for the household.\nSubject: the old house restoration\n\nMembers: Oskar, Zara, Nadia, Tess\nChat log (oldest first):\n[12 Sep 2026] Nadia: @Oskar I'll bleed the attic radiators by September 16, 2026 if the loft clearance day goes ahead.\n[12 Sep 2026] Tess: Not promising, but I'll try to oil the back door hinges by September 19, 2026.\n[13 Sep 2026] Tess: @Zara Count on me, I'll oil the back door hinges by September 17, 2026.\n[15 Sep 2026] Nadia: Great news, the loft clearance day is on!\n[15 Sep 2026] Oskar: @Tess Ah, no stress, no need for you to oil the back door hinges\n[18 Sep 2026] Tess: @Zara Ticked off: oil the back door hinges, feels so good",
  "question": "Was the promise to oil the back door hinges from Tess kept on September 22, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9a4a533188",
  "kind": "choice",
  "text": "Local volunteer export\nSaved by Mo, covering the topic of the volunteer roster.\n\nMembers: Lena, Greta, Lee, Mo\nChat export (date | from | to | message):\n2026-09-04 | Mo | Lee | I assure you I'll print the raffle tickets by 12 September 2026 if the governors meeting is on.\n2026-09-05 | Greta | group | Sadly, the governors meeting won't go ahead.\n2026-09-06 | Mo | Lena | Committing to fetch the tea urn by 13 September 2026.\n2026-09-08 | Mo | Lena | I promise to label the raffle prizes by 14 September 2026.\n2026-09-13 | Greta | Mo | Good news, you're let off having to fetch the tea urn",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Mo's promise to fetch the tea urn stand at the end of 16 September 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q60c0b4fdfe",
  "kind": "choice",
  "text": "Flat chat export, saved by Kai\nCovers the bathroom refit, shared among the housemates.\n\nMembers: Yuki, Kai, Lena\nChat export (date | from | to | message):\n2026-07-09 | Kai | Lena | I will make sure to print the floor plan by 17 July 2026.\n2026-07-11 | Yuki | Kai | Quick update: you do not need to print the floor plan at all.\n2026-07-13 | Yuki | Lena | If the removal van arrival goes ahead, I'll scrape the old wallpaper by 16 July 2026.\n2026-07-15 | Lena | group | Great news, the removal van arrival is on!\n2026-07-16 | Lena | Yuki | Forget it, you won't need to scrape the old wallpaper",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Yuki's promise to scrape the old wallpaper have at the end of 21 July 2026?",
  "options": [
   "Kept",
   "Broken",
   "Not yet due",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q8646c30207",
  "kind": "choice",
  "text": "Freelancer and client exchange about the honeymoon album, saved by Yuki.\n\nMembers: Zara, Tomas, Yuki\nChat export (date | from | to | message):\n2026-01-17 | Yuki | Zara | I'll book the assistant photographer by 23 January 2026, provided the venue visit happens.\n2026-01-17 | Zara | group | Great news, the venue visit is on!\n2026-01-23 | Yuki | Zara | Mate, I promised, may I book the assistant photographer by 26 January 2026 instead?\n2026-01-23 | Zara | Yuki | Nah, the date's staying put, so you can book the assistant photographer.\n2026-01-23 | Yuki | Zara | Relax, I'll print the seating cards by 27 January 2026, promise.\n2026-01-25 | Yuki | Zara | Mind giving me until 31 January 2026 to print the seating cards?\n2026-01-25 | Zara | Yuki | No, I'd like you to print the seating cards by the original date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nFollowing the rules set out on the card, what date governs Yuki's commitment to book the assistant photographer at the end of 2 February 2026, once any agreed shift in the date is factored in?",
  "options": [
   "27 January 2026",
   "26 January 2026",
   "23 January 2026"
  ]
 },
 {
  "qid": "q19fc67851a",
  "kind": "choice",
  "text": "Rhea shared this exchange with the client about the campaign edit.\n\nMembers: Oskar, Rhea, Ana, Ines\nChat export (date | from | to | message):\n2026-05-08 | Oskar | Ana | I promise to send the colour notes by 14 May 2026.\n2026-05-09 | Oskar | Ana | I'm withdrawing my promise to send the colour notes\n2026-05-12 | Ana | Rhea | I own this, I'll upload the render files by 19 May 2026.\n2026-05-13 | Rhea | Oskar | Provided the festival premiere happens, I'll send the timeline export by 20 May 2026.\n2026-05-18 | Ana | group | Sorry all, the festival premiere is not happening.\n2026-05-19 | Ines | Ana | Relax, mate, you're not expected to upload the render files",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Ana's promise to upload the render files sit at the end of 19 May 2026, exactly?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Broken",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q098dbcc974",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the family photo book\nFrom Elif, the thread below is passed on in its original form.\n\nMembers: Elif, Rhea, Arlo, Femi\nChat log (oldest first):\n[24 Jun 2026] Femi: @Arlo Absolutely, I will bake the oat biscuits by 3 July 2026.\n[25 Jun 2026] Arlo: @Elif Hoping to tidy the playroom by 4 July 2026, but can't promise.\n[26 Jun 2026] Arlo: @Rhea I'll tidy the playroom by 2 July 2026, provided the sleepover weekend happens.\n[28 Jun 2026] Femi: Yay, the sleepover weekend is all set to go!\n[1 Jul 2026] Arlo: @Rhea Quick question, could I tidy the playroom by 7 July 2026 instead?\n[1 Jul 2026] Rhea: @Arlo That suits me, so please tidy the playroom by 7 July 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Arlo's promise to tidy the playroom at the end of 3 July 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qb516254f18",
  "kind": "yes/no",
  "text": "Subject: Saved chat on the annual tour\nHere is the export from Ana, for the record.\n\nMembers: Ana, Nadia, Mo, Bruno\nChat log (oldest first):\n[30 Jul 2026] Nadia: Maybe I can tune the gear cables by Monday, August 3, 2026.\n[1 Aug 2026] Nadia: @Mo I'll tune the gear cables by Tuesday, August 4, 2026 if the mechanics clinic goes ahead.\n[3 Aug 2026] Mo: Brilliant news everyone, the mechanics clinic is a go!\n[4 Aug 2026] Mo: @Bruno You can bet I'll pump the spare tyres by Sunday, August 9, 2026.\n[5 Aug 2026] Ana: @Nadia Ticket's mine, I'll set up the feed stop by Monday, August 10, 2026.\n[5 Aug 2026] Mo: @Bruno Got it, I'll print the route cards by Saturday, August 8, 2026 for sure.",
  "question": "Did Nadia break the promise to tune the gear cables at the end of Wednesday, August 5, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa48566556c",
  "kind": "choice",
  "text": "Household group messages for the holiday memories were passed along by Dara.\n\nMembers: Ana, Dara, Oskar\nChat log (oldest first):\n[12 May 2026] Oskar: @Ana It's on me to teach the card game by 18 May 2026.\n[13 May 2026] Oskar: @Dara As long as the seaside outing is on, I'll sort the old photo albums by 19 May 2026.\n[16 May 2026] Oskar: @Dara Is 22 May 2026 alright for me to sort the old photo albums?\n[17 May 2026] Dara: @Oskar Yes, happy for you to sort the old photo albums by 22 May 2026 instead.\n[18 May 2026] Dara: Yep, the seaside outing is on as planned.\n[19 May 2026] Oskar: @Dara For the record: I was able to sort the old photo albums",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Oskar's commitment to sort the old photo albums at the end of 18 May 2026?",
  "options": [
   "Waived",
   "Kept",
   "Not triggered",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q974009d366",
  "kind": "yes/no",
  "text": "Chat attached to a support case about the campaign edit, shared by Ivo.\n\nMembers: Oskar, Malik, Greta, Ivo\nChat export (date | from | to | message):\n2026-06-29 | Ivo | Greta | Lovely, I'll send the colour notes by 3 July 2026 for sure.\n2026-06-29 | Ivo | Greta | Scratch that, I'm not going to send the colour notes\n2026-07-02 | Greta | Ivo | If the voiceover session goes ahead, I'll upload the render files by 7 July 2026.\n2026-07-03 | Malik | Ivo | If the agency review call goes ahead, I'll fetch the raw footage by 6 July 2026.\n2026-07-05 | Oskar | group | Team, the agency review call stays on as booked.\n2026-07-07 | Malik | Ivo | For the record: I was able to fetch the raw footage",
  "question": "Per the card's rules, on 9 July 2026, has Malik's promise to fetch the raw footage been broken, waived, not triggered or not yet due, rather than kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3bb8eb7a48",
  "kind": "choice",
  "text": "Saved by Jonas: a freelancer's exchange with a client over the documentary cut.\n\nMembers: Rhea, Jonas, Ines, Kai\nChat export (date | from | to | message):\n2026-07-23 | Jonas | Kai | Count on me to record the voice over by 1 August 2026 if the agency review call is on.\n2026-07-24 | Rhea | Jonas | Count on me to back up the project drives by 29 July 2026.\n2026-07-24 | Rhea | Jonas | Forget what I said, I won't back up the project drives\n2026-07-28 | Jonas | group | Sadly, the agency review call is not going ahead.\n2026-07-29 | Ines | Rhea | Good news, you're let off having to back up the project drives\n2026-07-31 | Ines | group | Hey, any luck with trying to back up the project drives?",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Rhea's promise to back up the project drives receive at the end of 3 August 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q8cd51d2e88",
  "kind": "yes/no",
  "text": "Subject: Chat about the grant renewal\nBelow, with Femi named as the source, is the chat as exported.\n\nMembers: Ravi, Femi, Kai\nChat log (oldest first):\n[16 Jun 2026] Ravi: @Femi I'll scan the field notes by 24 June 2026 as long as the safety inspection is on.\n[18 Jun 2026] Kai: @Ravi Absolutely, I will book the microscope slot by 21 June 2026.\n[18 Jun 2026] Kai: @Ravi Count on me, I'll print the poster abstracts by 26 June 2026.\n[19 Jun 2026] Ravi: Sadly, the safety inspection is not going ahead.\n[29 Jun 2026] Kai: @Ravi Guess who managed to print the poster abstracts, go team!",
  "question": "According to the rules on the card, is it true that the promise Kai made to print the poster abstracts has not been broken at the end of 3 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb08b77e312",
  "kind": "choice",
  "text": "Subject: Chat about the allotment expansion\nA plain copy from Ana follows, exactly as exported.\n\nMembers: Ana, Jonas, Lee\nChat log (oldest first):\n[16 Oct 2026] Ana: @Jonas Lovely, I'll sow the broad beans by October 20, 2026 if the seed swap day is on.\n[16 Oct 2026] Lee: @Jonas I assure you I'll water the allotment beds by October 21, 2026 if the water tank delivery is on.\n[17 Oct 2026] Ana: @Lee You can bet I'll collect the seed potatoes by October 23, 2026.\n[17 Oct 2026] Lee: Thanks, got it.\n[23 Oct 2026] Ana: @Lee Think October 25, 2026 would work if I collect the seed potatoes instead?\n[23 Oct 2026] Jonas: @Ana You don't have to collect the seed potatoes at all",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Ana doing with the promise to collect the seed potatoes at the end of October 23, 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "qb57a2113ad",
  "kind": "yes/no",
  "text": "Neighbours and renters, the flat chat, exported by Elif, covering the garden makeover.\n\nMembers: Femi, Elif, Jonas\nChat export (date | from | to | message):\n2026-09-12 | Elif | Jonas | As long as the mortgage valuation visit is on, I'll fetch the paint samples by 21 September 2026.\n2026-09-12 | Femi | Elif | Committing to pay the plumbing invoice by 20 September 2026.\n2026-09-12 | Elif | group | Cheers, noted.\n2026-09-15 | Femi | Jonas | It's on me to sweep the dust from stairs by 21 September 2026.\n2026-09-15 | Femi | Elif | Count on me to hang the new curtain rail by 17 September 2026, if the damp survey inspection happens.\n2026-09-20 | Femi | Elif | I need to take back my commitment to pay the plumbing invoice.",
  "question": "According to the rules on the card, does the promise Femi made to pay the plumbing invoice have any status except broken at the end of 21 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q54142ac81f",
  "kind": "choice",
  "text": "Subject: Chat about the kit sponsorship\nA plain copy from Lee follows, exactly as exported.\n\nMembers: Lee, Yuki\nChat log (oldest first):\n[12 Jun 2026] Lee: @Yuki If the pre-season friendly goes ahead, I'll set up the corner flags by 18 June 2026.\n[17 Jun 2026] Lee: @Yuki If the youth trial goes ahead, I'll pump the match balls by 21 June 2026.\n[19 Jun 2026] Lee: Fab, we are on for the youth trial as planned!\n[19 Jun 2026] Lee: @Yuki Think 25 June 2026 would work if I pump the match balls instead?\n[21 Jun 2026] Yuki: @Lee Aw no, you need to pump the match balls by the original date!\n[24 Jun 2026] Lee: @Yuki Guess who managed to pump the match balls, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Lee's promise to pump the match balls have at the end of 21 June 2026?",
  "options": [
   "Waived",
   "Kept",
   "Not yet due",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q146f9420a4",
  "kind": "choice",
  "text": "Subject: saved chat, the speed bump plan\nBelow is the chat that Elif saved for reference.\n\nMembers: Rhea, Zara, Elif, Ravi\nChat log (oldest first):\n[16 May 2026] Ravi: @Rhea You can bank on me to sweep the pavement outside by 2026-05-22.\n[16 May 2026] Rhea: Thanks mate, noted.\n[18 May 2026] Ravi: @Zara As long as the street litter clean is on, I will take in the post by 2026-05-26.\n[18 May 2026] Elif: @Ravi You don't have to sweep the pavement outside at all\n[22 May 2026] Ravi: @Rhea Ticked off: sweep the pavement outside, feels so good\n[23 May 2026] Elif: Team, the street litter clean is not happening.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Ravi's promise to sweep the pavement outside sit at the end of 2026-05-21, exactly?",
  "options": [
   "Not triggered",
   "Kept",
   "Not yet due",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q10a78f4e98",
  "kind": "yes/no",
  "text": "Team export header with the spring campaign, saved by Lee.\n\nMembers: Tess, Malik, Lee, Rhea\nChat export (date | from | to | message):\n2026-01-20 | Lee | Tess | It's on me to fix the landing page headline by 28 Jan 2026.\n2026-01-21 | Lee | Malik | Only if the brand photo shoot is on, I will collect the survey answers by 26 Jan 2026.\n2026-01-21 | Lee | Tess | If the influencer call goes ahead, I'll gladly return the rented camera gear by 30 Jan 2026.\n2026-01-22 | Rhea | Malik | Lovely, I'll set up the analytics dashboard by 27 Jan 2026 if the product launch is on.\n2026-01-24 | Lee | Tess | I regret to say that I shall not fix the landing page headline.\n2026-01-27 | Rhea | Lee | You don't have to fix the landing page headline at all",
  "question": "On 27 Jan 2026 itself, has Lee not kept the promise to fix the landing page headline?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6511531727",
  "kind": "choice",
  "text": "Tenant and agent back-and-forth on the guest welcome plan, saved by Tess.\n\nMembers: Tess, Lena, Ines\nChat log (oldest first):\n[16 Jul 2026] Lena: @Ines Absolutely, I will air the spare room by 24 Jul 2026.\n[23 Jul 2026] Tess: @Lena Only if the pool safety inspection is on, I will wash the beach towels by 30 Jul 2026.\n[23 Jul 2026] Lena: @Tess You can bet I'll change the lounge bulb by 28 Jul 2026.\n[24 Jul 2026] Lena: @Ines Mind giving me until 26 Jul 2026 to air the spare room?\n[24 Jul 2026] Tess: @Lena Yes, you can air the spare room by 26 Jul 2026 if that suits you.\n[27 Jul 2026] Ines: Yay, the pool safety inspection is all set to go!\n[27 Jul 2026] Lena: @Ines Ticked off my list: air the spare room, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 27 Jul 2026, by what date does Lena have to air the spare room, counting any agreed change of date?",
  "options": [
   "30 Jul 2026",
   "24 Jul 2026",
   "26 Jul 2026"
  ]
 },
 {
  "qid": "qe6c1ec3aed",
  "kind": "yes/no",
  "text": "{\"thread\": \"the family history\", \"exported_by\": \"Arlo\", \"shape\": \"group chat\"}\n\nMembers: Tomas, Arlo, Nadia, Rhea\nChat log (oldest first):\n[29 Jan 2026] Arlo: Hoping to label the memory box by 1 Feb 2026, but can't promise.\n[31 Jan 2026] Arlo: @Tomas You can bet I'll buy the name tags by 3 Feb 2026.\n[31 Jan 2026] Arlo: @Tomas I need to take back my commitment to buy the name tags.\n[31 Jan 2026] Arlo: @Tomas Promise to label the memory box by 4 Feb 2026 if the karaoke night goes ahead.\n[1 Feb 2026] Tomas: Yay, the karaoke night is all set to go!\n[2 Feb 2026] Arlo: @Tomas Ticked off my list: label the memory box, yay.",
  "question": "Is Arlo's promise to label the memory box kept as of 4 Feb 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2876618ae2",
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
  "qid": "q26295075a5",
  "kind": "choice",
  "text": "Rented flat, shared group chat, copied by Lee, filed under the balcony garden project.\n\nMembers: Jonas, Greta, Lee\nChat log (oldest first):\n[10 Jul 2026] Greta: @Lee Absolutely, I will forward the gas bill by 17 Jul 2026.\n[10 Jul 2026] Greta: @Lee Would it be fine if I forward the gas bill by 20 Jul 2026 instead, yeah?\n[13 Jul 2026] Lee: @Greta Only if the window cleaner visit is on, I will email the leak photos by 17 Jul 2026.\n[14 Jul 2026] Greta: @Jonas I'll measure the kitchen for fridge by 16 Jul 2026 if the flat viewing day goes ahead.\n[14 Jul 2026] Jonas: Afraid the flat viewing day is called off.\n[16 Jul 2026] Lee: @Jonas I own this, I'll bring the step stool by 20 Jul 2026.\n[17 Jul 2026] Lee: @Greta The original date stands, so you need to forward the gas bill.\n[19 Jul 2026] Lee: @Jonas Quick question, could I bring the step stool by 26 Jul 2026 instead?",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Lee to bring the step stool at the end of 19 Jul 2026, counting any agreed change of date?",
  "options": [
   "26 Jul 2026",
   "20 Jul 2026",
   "16 Jul 2026"
  ]
 },
 {
  "qid": "qb1dc36181c",
  "kind": "yes/no",
  "text": "Subject: group chat about the gallery show, exported by Tomas\nForwarding the chat below for your reference.\n\nMembers: Tomas, Yuki, Ravi, Ines\nChat log (oldest first):\n[26 Mar 2026] Yuki: @Ines I'll be sure to mail the business cards by 3 April 2026.\n[28 Mar 2026] Ravi: @Yuki Ticket's mine, I'll check the poster proofs by 2 April 2026.\n[29 Mar 2026] Ines: @Tomas Provided the sign reveal happens, I will pick the colour swatches by 6 April 2026.\n[30 Mar 2026] Ravi: @Yuki Only if the gallery install is on, I will update the icon set by 3 April 2026.\n[31 Mar 2026] Ravi: Sorry, the gallery install is off.\n[2 Apr 2026] Ravi: @Yuki For the record: I was able to check the poster proofs",
  "question": "Under the rules on the card, is it true that Ravi has not kept the promise to check the poster proofs as of 2 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q55765c52d4",
  "kind": "yes/no",
  "text": "Channel: work team chat\nTopic: the trade show push\nExported by Kofi.\n\nMembers: Sami, Kofi, Mo, Malik\nChat log (oldest first):\n[2 May 2026] Sami: @Malik Hoping to set up the analytics dashboard by 5 May 2026, can't promise.\n[4 May 2026] Sami: @Mo Absolutely, I will set up the analytics dashboard by 9 May 2026.\n[6 May 2026] Malik: @Sami Don't sweat it, there's no need to set up the analytics dashboard\n[7 May 2026] Malik: @Mo I'll be sure to draft the press release by 10 May 2026.\n[8 May 2026] Kofi: @Malik I'll fetch the campaign budget sheet by 12 May 2026, provided the webinar rehearsal happens.\n[9 May 2026] Mo: Lovely, the webinar rehearsal is definitely happening!",
  "question": "Was the promise to set up the analytics dashboard from Sami kept on 11 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
