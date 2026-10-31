# G5-H blind read T32-blind_read-204fa153-006 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root8/T32/qc/g5h/answers/T32-blind_read-204fa153-006.json

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
  "qid": "qbe0b432b4a",
  "kind": "choice",
  "text": "Volunteers, this is the annual tour thread that Hana shared with the committee.\n\nMembers: Nadia, Leila, Hana, Sami\nChat log (oldest first):\n[8 Sep 2026] Sami: @Leila Provided the mechanics clinic happens, I will tune the gear cables by 13 September 2026.\n[8 Sep 2026] Hana: Scrapping the mechanics clinic, apologies to all.\n[8 Sep 2026] Nadia: @Sami I will make sure to collect the timing tags by 12 September 2026.\n[14 Sep 2026] Nadia: @Sami Relax, I'll print the route cards by 20 September 2026 for sure.\n[16 Sep 2026] Leila: @Nadia Good news, you're let off having to print the route cards",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Sami's commitment to tune the gear cables have at the end of 15 September 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "qc11f2aa9dc",
  "kind": "yes/no",
  "text": "This short note between tenants and a landlord covers the guest review drive. Saved by Nadia for the record.\n\nMembers: Rhea, Oskar, Nadia, Ivo\nChat log (oldest first):\n[10 Aug 2026] Oskar: @Ivo Might be able to vacuum the holiday cottage by 18 August 2026, who knows!\n[11 Aug 2026] Ivo: @Oskar Relax, I'll fill the cleaning cupboard by 14 August 2026, promise.\n[12 Aug 2026] Oskar: @Nadia I'll vacuum the holiday cottage by 17 August 2026 as long as the lettings photo shoot is on.\n[16 Aug 2026] Nadia: Yay, the lettings photo shoot is all set to go!\n[17 Aug 2026] Rhea: @Oskar Forget it, you won't need to vacuum the holiday cottage\n[18 Aug 2026] Oskar: @Nadia Ticked off my list: vacuum the holiday cottage, yay.",
  "question": "Looking over the chat at the end of 18 August 2026, did Oskar break the promise to vacuum the holiday cottage?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q554e2f4b07",
  "kind": "choice",
  "text": "Saved by Ana, this is the household group chat about the garden makeover, copied in full.\n\nMembers: Ana, Malik, Dara\nChat export (date | from | to | message):\n2026-05-07 | Ana | Malik | I will fetch the paint samples by 14 May 2026.\n2026-05-11 | Dara | Ana | Got it, I'll hang the new curtain rail by 18 May 2026 for sure.\n2026-05-12 | Ana | Dara | If the kitchen fitting day goes ahead, I'll gladly scrape the old wallpaper by 21 May 2026.\n2026-05-16 | Malik | group | Fab, we are on for the kitchen fitting day as planned!\n2026-05-19 | Dara | Ana | To note: I have managed to hang the new curtain rail",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Dara made to hang the new curtain rail have at the end of 22 May 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q9792a453cd",
  "kind": "choice",
  "text": "Subject: the kit sponsorship\nBelow is the group chat that Leila saved, unedited.\n\nMembers: Lena, Rhea, Leila, Greta\nChat log (oldest first):\n[25 Apr 2026] Lena: @Leila Count on me, I'll repair the goal nets by 28 Apr 2026.\n[26 Apr 2026] Greta: @Rhea Ticket's mine, I'll wash the away kit by 29 Apr 2026.\n[28 Apr 2026] Greta: @Rhea Ta-da, I went and did it: wash the away kit!\n[28 Apr 2026] Lena: @Leila Quick report: I've managed to repair the goal nets\n[28 Apr 2026] Greta: @Leila Only if the presentation evening is on, I will return the bib sets by 7 May 2026.\n[28 Apr 2026] Lena: Lovely, the presentation evening is definitely happening!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of 1 May 2026, which status does Greta have for the promise to wash the away kit?",
  "options": [
   "Waived",
   "Not triggered",
   "Broken",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "qe2db8b3a8e",
  "kind": "choice",
  "text": "Volunteers, this is the league run thread that Tess shared with the committee.\n\nMembers: Greta, Femi, Ana, Tess\nChat log (oldest first):\n[18 Jul 2026] Ana: @Tess Lovely, I'll set up the corner flags by 27 Jul 2026 for sure.\n[18 Jul 2026] Ana: @Tess Ta-da, I went and did it: set up the corner flags!\n[22 Jul 2026] Ana: @Femi I'll mark the pitch lines by 28 Jul 2026 as long as the training camp is on.\n[22 Jul 2026] Ana: Sadly, the training camp won't go ahead.\n[24 Jul 2026] Femi: @Greta I will return the bib sets by 27 Jul 2026.\n[26 Jul 2026] Femi: @Greta For the record: I was able to return the bib sets",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Ana's pledge to mark the pitch lines sit at the end of 28 Jul 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "qbe723720cd",
  "kind": "yes/no",
  "text": "{\"chat\": \"exported\", \"about\": \"the spare room plan\", \"saved_by\": \"Priya\", \"medium\": \"text\"}\n\nMembers: Priya, Hana, Mo, Sami\nChat export (date | from | to | message):\n2026-10-11 | Sami | Mo | I'll try to drop the parcel upstairs by 18 October 2026, no promises.\n2026-10-13 | Sami | Mo | Guaranteed I'll drop the parcel upstairs by 21 October 2026.\n2026-10-17 | Priya | Mo | Provided the lodger farewell supper happens, I'll replace the loo roll by 24 October 2026.\n2026-10-18 | Sami | Mo | Mind giving me until 26 October 2026 to drop the parcel upstairs?\n2026-10-19 | Mo | Sami | We are holding the date on record, so drop the parcel upstairs by it.\n2026-10-20 | Hana | group | On track for the lodger farewell supper to happen as planned.",
  "question": "At the end of 20 October 2026, would it be right to say Sami has not broken the promise to drop the parcel upstairs?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q35ed9bdfdc",
  "kind": "choice",
  "text": "Subject: Saved thread about the family photo book\nThis export came from Sami and is pasted in full below.\n\nMembers: Priya, Sami, Tess, Arlo\nChat log (oldest first):\n[18 Jan 2026] Arlo: @Priya I will make sure to pick up the school bags by Saturday, 24 January 2026.\n[18 Jan 2026] Sami: @Arlo I own this, I'll sort the old photo albums by Sunday, 25 January 2026.\n[19 Jan 2026] Tess: @Sami Count on me to pack the picnic basket by Wednesday, 21 January 2026, if the sleepover weekend happens.\n[19 Jan 2026] Tess: @Sami I'll read the bedtime story by Sunday, 25 January 2026 as long as the seaside outing is on.\n[24 Jan 2026] Tess: Anything new on your way to pick up the school bags?\n[24 Jan 2026] Priya: @Arlo Good news, you're let off having to pick up the school bags",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Arlo's undertaking to pick up the school bags hold at the end of Monday, 26 January 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "qc0b3d72094",
  "kind": "yes/no",
  "text": "A short note above messages between tenants and the landlord about the rent split plan, saved by Lee.\n\nMembers: Kofi, Lee, Ines, Femi\nChat log (oldest first):\n[15 Oct 2026] Kofi: @Lee Fingers crossed I can copy the house keys by October 27, 2026.\n[16 Oct 2026] Kofi: @Femi I'll copy the house keys by October 23, 2026 if the move in day goes ahead.\n[16 Oct 2026] Ines: Yay, the move in day is all set to go!\n[18 Oct 2026] Lee: @Kofi Relax, I'll ring the letting agent by October 21, 2026 for sure.\n[22 Oct 2026] Lee: @Kofi Please don't feel you have to copy the house keys\n[26 Oct 2026] Kofi: @Femi For the record: I was able to copy the house keys",
  "question": "According to the rules on the card, is it true that the promise Kofi made to copy the house keys has not been broken at the end of October 24, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbf94521fef",
  "kind": "yes/no",
  "text": "{\"record_type\": \"saved chat\", \"matter\": \"the holiday memories\", \"by\": \"Bruno\", \"stored\": \"as text\"}\n\nMembers: Ivo, Bruno, Elif, Hana\nChat log (oldest first):\n[28 Mar 2026] Bruno: @Hana Provided the seaside outing happens, I will mend the kite string by 6 Apr 2026.\n[28 Mar 2026] Elif: @Ivo I will make sure to read the bedtime story by 4 Apr 2026.\n[30 Mar 2026] Hana: @Ivo Relax, I'll pack the picnic basket by 5 Apr 2026, promise.\n[30 Mar 2026] Bruno: @Hana I'll fetch the craft box by 6 Apr 2026 if the school play goes ahead.\n[5 Apr 2026] Hana: @Ivo Ta-da, I went and did it: pack the picnic basket!",
  "question": "Is Hana's promise to pack the picnic basket broken, waived, not triggered or not yet due as of 7 Apr 2026, instead of kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q440aa0be27",
  "kind": "choice",
  "text": "Forwarded by Sami, this thread on the holiday memories stays attached to the ticket.\n\nMembers: Malik, Sami, Zara, Mo\nChat log (oldest first):\n[29 Jan 2026] Mo: @Zara It's on me to fetch the craft box by Saturday, 7 February 2026.\n[2 Feb 2026] Mo: @Sami I'll try to pick up the school bags by Wednesday, 4 February 2026, no promises.\n[3 Feb 2026] Mo: @Zara Promise to pick up the school bags by Tuesday, 10 February 2026 if the sleepover weekend goes ahead.\n[5 Feb 2026] Mo: @Zara On my action item, may I pick up the school bags by Sunday, 15 February 2026 instead?\n[6 Feb 2026] Sami: @Mo Yes, you can pick up the school bags by Sunday, 15 February 2026 if that suits you.\n[9 Feb 2026] Zara: Just so you know, the sleepover weekend is on as scheduled.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of Friday, 6 February 2026, which status does Mo have for the promise to pick up the school bags?",
  "options": [
   "Not triggered",
   "Waived",
   "Not yet due",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "q0674e9713a",
  "kind": "yes/no",
  "text": "Subject: the summer visits, from the group chat\nSharing it here as Bruno saved it.\n\nMembers: Bruno, Ivo, Ravi, Nadia\nChat log (oldest first):\n[28 May 2026] Nadia: @Bruno I promise to pick up the school bags by 31 May 2026 if the sleepover weekend is on.\n[28 May 2026] Ivo: Update, the sleepover weekend will not take place.\n[31 May 2026] Ivo: @Nadia Got it, I'll sort the old photo albums by 6 Jun 2026 for sure.\n[1 Jun 2026] Ivo: @Nadia Lovely, I'll bake the oat biscuits by 9 Jun 2026 if the garden tea party is on.\n[1 Jun 2026] Ravi: @Nadia Got it, I'll teach the card game by 8 Jun 2026 for sure.\n[8 Jun 2026] Nadia: @Ravi Don't sweat it, there's no need to teach the card game",
  "question": "Per the card's rules, on 11 Jun 2026, has Ravi's promise to teach the card game been broken, waived, not triggered or not yet due, rather than kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2961150945",
  "kind": "choice",
  "text": "Our flat chat about the attic conversion idea, shared by Hana for whoever lives here.\n\nMembers: Yuki, Hana, Tess, Malik\nChat export (date | from | to | message):\n2026-02-10 | Hana | Malik | Count on me, I'll wipe the shared kitchen counter by 16 Feb 2026.\n2026-02-14 | Malik | Hana | If the house insurance review is on, I'll definitely turn the heating timer by 22 Feb 2026.\n2026-02-15 | Hana | Tess | I'll stock the spice rack by 21 Feb 2026, provided the water tank check happens.\n2026-02-20 | Tess | group | Please note the water tank check will proceed.\n2026-02-20 | Hana | Tess | Mate, I promised, may I stock the spice rack by 25 Feb 2026 instead?\n2026-02-20 | Yuki | Hana | Yes, all good for you to stock the spice rack by 25 Feb 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Hana made to stock the spice rack is in which status at the end of 24 Feb 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Not triggered",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "qf026091abf",
  "kind": "choice",
  "text": "Exported by Priya, this is the full back and forth on the documentary cut.\n\nMembers: Priya, Ravi, Jonas\nChat export (date | from | to | message):\n2026-05-07 | Priya | group | No promises, but I'll aim to order the stock music licence by 2026-05-13.\n2026-05-08 | Priya | Ravi | Lovely, I'll order the stock music licence by 2026-05-12 for sure.\n2026-05-09 | Priya | Ravi | For the record: I was able to order the stock music licence\n2026-05-10 | Priya | Jonas | If the client screening goes ahead, I'll gladly export the subtitle files by 2026-05-17.\n2026-05-11 | Priya | Ravi | You can bet I'll send the timeline export by 2026-05-17.\n2026-05-15 | Ravi | group | Update: the client screening is going ahead as planned.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Priya's promise to order the stock music licence at the end of 2026-05-11?",
  "options": [
   "Not triggered",
   "Broken",
   "Kept",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "qd9c7190870",
  "kind": "choice",
  "text": "Shared by Jonas, a help-desk thread covering the big day.\n\nMembers: Jonas, Mo, Nadia, Leila\nChat log (oldest first):\n[16 May 2026] Jonas: @Leila I'll send the sneak peek gallery by 24 May 2026, providing the engagement shoot goes ahead.\n[17 May 2026] Leila: Afraid the engagement shoot is called off.\n[20 May 2026] Nadia: @Leila Not promising, but I'll try to return the lighting stands by 27 May 2026.\n[22 May 2026] Nadia: @Jonas You can bet I'll return the lighting stands by 28 May 2026.\n[27 May 2026] Nadia: @Jonas I committed to return the lighting stands, can I do that by 31 May 2026 instead?\n[27 May 2026] Mo: @Nadia Revised deadline is 31 May 2026, so you can return the lighting stands.\n[27 May 2026] Leila: @Nadia Forget it, you won't need to return the lighting stands\n[1 Jun 2026] Nadia: @Jonas To my relief, I managed to return the lighting stands.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs things stand at the end of 29 May 2026, which date is the deadline for Nadia to return the lighting stands, with any agreed change applied?",
  "options": [
   "24 May 2026",
   "31 May 2026",
   "28 May 2026"
  ]
 },
 {
  "qid": "qe15756904e",
  "kind": "choice",
  "text": "Greta forwarded this support chat, which is about the payment setup.\n\nMembers: Sami, Hana, Greta\nChat log (oldest first):\n[21 Oct 2026] Hana: @Sami Promise to print the packing slips by 2026-10-23 if the courier pickup goes ahead.\n[21 Oct 2026] Sami: Fab, we are on for the courier pickup as planned!\n[24 Oct 2026] Sami: @Hana I promise to add the size chart by 2026-11-01 if the stock count is on.\n[25 Oct 2026] Hana: @Greta Absolutely, I will fetch the domain login by 2026-10-31.\n[25 Oct 2026] Greta: @Hana Good news, you're let off having to fetch the domain login\n[25 Oct 2026] Sami: @Hana I promise to test the mobile layout by 2026-11-01.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Hana made to fetch the domain login at the end of 2026-10-27?",
  "options": [
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q8df9fe682b",
  "kind": "yes/no",
  "text": "Shared by Ana from the work chat, with the onboarding flow at its heart.\n\nMembers: Ana, Tess, Leila\nChat log (oldest first):\n[13 Oct 2026] Ana: @Tess I'll fix the test runner by 16 Oct 2026 if the hackathon goes ahead.\n[14 Oct 2026] Tess: Team, the hackathon stays on as booked.\n[15 Oct 2026] Tess: @Ana Relax, I'll run the security scan by 21 Oct 2026 for sure.\n[16 Oct 2026] Ana: @Tess Think 20 Oct 2026 would work if I fix the test runner instead?\n[16 Oct 2026] Ana: @Tess Guess what, I managed to fix the test runner!",
  "question": "On the card, was Ana's promise to fix the test runner broken, waived, not triggered or not yet due, rather than kept, at the end of 19 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb2e5ca3ed8",
  "kind": "choice",
  "text": "Freelancer to client messages, the menu redesign, passed on by Elif.\n\nMembers: Elif, Priya, Oskar, Leila\nChat log (oldest first):\n[15 Jun 2026] Elif: @Leila I will pick the colour swatches by 23 Jun 2026.\n[16 Jun 2026] Leila: @Priya I promise to export the logo files by 24 Jun 2026 if the print run is on.\n[16 Jun 2026] Leila: @Priya If the packaging launch is on, I'll definitely check the poster proofs by 25 Jun 2026.\n[20 Jun 2026] Priya: @Oskar Fingers crossed I can mail the business cards by 23 Jun 2026.\n[22 Jun 2026] Priya: @Elif Got it, I'll mail the business cards by 28 Jun 2026 for sure.\n[28 Jun 2026] Priya: @Elif Think 3 Jul 2026 would work if I mail the business cards instead?\n[28 Jun 2026] Leila: @Priya Revised deadline is 3 Jul 2026, so you can mail the business cards.\n[2 Jul 2026] Priya: @Elif To note: I have managed to mail the business cards",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs things stand at the end of 30 Jun 2026, which date is the deadline for Priya to mail the business cards, with any agreed change applied?",
  "options": [
   "25 Jun 2026",
   "3 Jul 2026",
   "28 Jun 2026"
  ]
 },
 {
  "qid": "q41324bafec",
  "kind": "yes/no",
  "text": "Freelance project export\nFrom Arlo, covering the rebrand package with the client.\n\nMembers: Rhea, Arlo, Wren\nChat log (oldest first):\n[21 Oct 2026] Arlo: @Wren If the brand review call goes ahead, I'll gladly send the moodboard files by 28 October 2026.\n[21 Oct 2026] Wren: @Arlo I'll mail the business cards by 25 October 2026, provided the gallery install happens.\n[23 Oct 2026] Rhea: @Arlo Relax, I'll sketch the packaging mockup by 29 October 2026 for sure.\n[24 Oct 2026] Rhea: @Arlo I have to take back my promise to sketch the packaging mockup.\n[25 Oct 2026] Arlo: Just so you know, the brand review call is on as scheduled.\n[30 Oct 2026] Arlo: @Wren Guess what, I managed to send the moodboard files!",
  "question": "Has Arlo kept the promise to send the moodboard files as of 27 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd9184607ad",
  "kind": "choice",
  "text": "Read up on the flat upgrade list, flatmates, as Zara exported it.\n\nMembers: Oskar, Mo, Zara\nChat log (oldest first):\n[25 Jan 2026] Oskar: I'll see if I can email the leak photos by 2 Feb 2026.\n[27 Jan 2026] Oskar: @Zara You can bank on me to email the leak photos by 4 Feb 2026.\n[30 Jan 2026] Mo: @Oskar Forget it, you won't need to email the leak photos\n[1 Feb 2026] Zara: @Mo Count on me to collect the spare flat keys by 6 Feb 2026, if the lease renewal call happens.\n[4 Feb 2026] Oskar: @Zara Got myself to email the leak photos lol.\n[4 Feb 2026] Zara: Great news, the lease renewal call is on!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Oskar's promise to email the leak photos at the end of 10 Feb 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q4e3814ac7e",
  "kind": "yes/no",
  "text": "Our flat chat about the house refit, shared by Nadia for whoever lives here.\n\nMembers: Nadia, Elif, Hana\nChat export (date | from | to | message):\n2026-08-25 | Elif | Nadia | Relax, I'll print the floor plan by 31 August 2026, promise.\n2026-08-25 | Hana | Elif | No worries, you don't need to print the floor plan\n2026-08-25 | Elif | Nadia | Mum, I did print the floor plan, haha.\n2026-08-27 | Hana | Elif | If the builder quote meeting goes ahead, I'll pick up the grout bag by 30 August 2026.\n2026-08-28 | Hana | group | Sadly, the builder quote meeting is not going ahead.\n2026-08-31 | Elif | Hana | If the removal van arrival goes ahead, I'll collect the sanding pads by 9 September 2026.",
  "question": "On the card, was Elif's promise to print the floor plan broken, waived, not triggered or not yet due, rather than kept, at the end of 31 August 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe1bcc7c8a2",
  "kind": "choice",
  "text": "Team chat header\nSubject line: the visitor policy, exported by Sami.\n\nMembers: Lee, Sami, Femi\nChat log (oldest first):\n[10 Apr 2026] Sami: @Lee Count on me to return the printer toner by 2026-04-17 if the staff picnic is on.\n[13 Apr 2026] Sami: @Lee Relax, I'll renew the fire extinguisher service by 2026-04-18 for sure.\n[14 Apr 2026] Lee: Sorry, the staff picnic is off.\n[18 Apr 2026] Femi: @Sami Ah, no stress, no need for you to renew the fire extinguisher service\n[18 Apr 2026] Sami: @Lee Quick report: I've managed to renew the fire extinguisher service",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Sami's promise to renew the fire extinguisher service at the end of 2026-04-19?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "qa8f3da3baf",
  "kind": "choice",
  "text": "Note above a chat from the support case, covering the shared kitchen scheme, shared by Priya.\n\nMembers: Sami, Mo, Priya, Kai\nChat log (oldest first):\n[15 Sep 2026] Kai: @Sami I assure you I'll feed the house plants by 19 September 2026 if the house insurance review is on.\n[17 Sep 2026] Priya: Sorry all, the house insurance review is not happening.\n[19 Sep 2026] Kai: @Priya I will make sure to replace the loo roll by 25 September 2026.\n[22 Sep 2026] Sami: @Kai No worries, you don't need to replace the loo roll\n[30 Sep 2026] Kai: @Priya Ticked off: replace the loo roll, feels so good",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 27 September 2026, what status has Kai's promise to replace the loo roll got?",
  "options": [
   "Not yet due",
   "Broken",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "qe0c5385775",
  "kind": "choice",
  "text": "Subject: chat about the visitor policy, forwarded\nThe chat follows below.\nRegards, Tess\n\nMembers: Tess, Rhea, Elif\nChat log (oldest first):\n[10 May 2026] Elif: @Rhea Count on me to book the boardroom by Monday, May 18, 2026, if the team lunch happens.\n[11 May 2026] Elif: @Rhea I will renew the fire extinguisher service by Sunday, May 17, 2026 only if the staff picnic happens.\n[11 May 2026] Elif: Quick heads up, the team lunch is scrapped.\n[14 May 2026] Elif: @Rhea You can bet I'll send the expense receipts by Friday, May 22, 2026.\n[16 May 2026] Elif: @Rhea Mind giving me until Wednesday, May 20, 2026 to book the boardroom?\n[18 May 2026] Rhea: @Elif Fine by me, you can book the boardroom by Wednesday, May 20, 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Elif's promise to book the boardroom at the end of Monday, May 25, 2026?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q511a3eb373",
  "kind": "choice",
  "text": "Attached chat: the visitor policy\nForwarded by: Omar\n\nMembers: Lee, Wren, Omar, Kai\nChat log (oldest first):\n[18 Apr 2026] Kai: @Lee Provided the team lunch happens, I'll book the boardroom by 26 April 2026.\n[22 Apr 2026] Kai: @Lee You can bank on me to return the printer toner by 27 April 2026.\n[23 Apr 2026] Wren: @Omar It's on me to renew the fire extinguisher service by 29 April 2026.\n[23 Apr 2026] Kai: @Wren I promise to replace the kitchen filters by 28 April 2026 if the annual audit is on.\n[27 Apr 2026] Kai: @Wren Nobody needs you to renew the fire extinguisher service, that's that\n[29 Apr 2026] Wren: @Omar To my relief, I managed to renew the fire extinguisher service.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Wren doing with the promise to renew the fire extinguisher service at the end of 2 May 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q2b63fc4682",
  "kind": "choice",
  "text": "Work team channel\nSaved by Sami, which talks about the desk plan.\n\nMembers: Sami, Wren, Ana\nChat log (oldest first):\n[16 May 2026] Sami: @Ana As long as the team lunch is on, I will order the office stationery by 21 May 2026.\n[17 May 2026] Wren: Sorry all, the team lunch is not happening.\n[18 May 2026] Ana: @Wren I'll try to return the printer toner by 26 May 2026.\n[19 May 2026] Sami: @Wren Count on me, I'll send the expense receipts by 24 May 2026.\n[19 May 2026] Sami: @Wren Log entry: send the expense receipts, carried out\n[19 May 2026] Ana: @Sami You can bank on me to return the printer toner by 25 May 2026.\n[20 May 2026] Ana: @Sami Would it be fine if I return the printer toner by 31 May 2026 instead, yeah?\n[20 May 2026] Wren: @Ana Yes, lovely, you can return the printer toner by 31 May 2026 instead!",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 30 May 2026, by what date does Ana have to return the printer toner, counting any agreed change of date?",
  "options": [
   "31 May 2026",
   "25 May 2026",
   "24 May 2026"
  ]
 },
 {
  "qid": "qe78d173777",
  "kind": "yes/no",
  "text": "Subject: chat about the family photo book, forwarded\nThe chat follows below.\nRegards, Kofi\n\nMembers: Sami, Ivo, Kofi, Mo\nChat log (oldest first):\n[19 May 2026] Kofi: @Ivo I'll be sure to sort the old photo albums by 27 May 2026.\n[19 May 2026] Ivo: Thanks mate, noted.\n[19 May 2026] Ivo: @Mo You can bank on me to read the bedtime story by 25 May 2026.\n[19 May 2026] Kofi: @Mo If the seaside outing goes ahead, I'll gladly bake the oat biscuits by 23 May 2026.\n[24 May 2026] Kofi: @Sami Provided the storytime session happens, I'll fetch the craft box by 30 May 2026.\n[26 May 2026] Kofi: @Ivo To note: I have managed to sort the old photo albums",
  "question": "Is the promise Kofi made to sort the old photo albums in a status other than broken at the end of 26 May 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q58610ec099",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the sound mix\nThe thread below comes from Omar and is passed on as it is.\n\nMembers: Priya, Kofi, Omar, Kai\nChat export (date | from | to | message):\n2026-05-14 | Omar | Kofi | You can bet I'll record the voice over by 18 May 2026.\n2026-05-16 | Omar | group | Might manage to send the timeline export by 27 May 2026, who knows.\n2026-05-16 | Omar | Kofi | Guess who managed to record the voice over, go team!\n2026-05-18 | Omar | Kofi | I promise to send the timeline export by 26 May 2026 if the client screening is on.\n2026-05-19 | Kofi | Kai | Count on me, I'll order the stock music licence by 25 May 2026.\n2026-05-24 | Kofi | group | Just so you know, the client screening is on as scheduled.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Omar's promise to send the timeline export sit at the end of 28 May 2026, exactly?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Broken",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qdfb7de1816",
  "kind": "choice",
  "text": "{\"saved_copy_of\": \"group chat\", \"subject\": \"the quiet street fund\", \"saver\": \"Leila\", \"format\": \"plain text\"}\n\nMembers: Wren, Zara, Lena, Leila\nChat export (date | from | to | message):\n2026-07-17 | Wren | Lena | Committing to bring the bins in by 19 July 2026.\n2026-07-21 | Lena | Wren | Provided the parking permit visit happens, I will return the ladders by 29 July 2026.\n2026-07-23 | Lena | Zara | If the speed camera survey goes ahead, I'll gladly lock the side gate by 30 July 2026.\n2026-07-26 | Leila | group | Sorry, the parking permit visit is off.\n2026-07-29 | Lena | Wren | Mate, I promised, may I return the ladders by 3 August 2026 instead?\n2026-07-29 | Wren | Lena | Nah, the date's staying put, so you can return the ladders.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Lena made to return the ladders at the end of 29 July 2026?",
  "options": [
   "Waived",
   "Broken",
   "Not yet due",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qb7bf69d189",
  "kind": "yes/no",
  "text": "Ana forwarded this support chat about the spare room plan.\n\nMembers: Ana, Omar, Kai\nChat export (date | from | to | message):\n2026-08-05 | Omar | Ana | I promise to stock the spice rack by August 13, 2026 if the lodger farewell supper is on.\n2026-08-07 | Ana | Kai | Promise to defrost the top freezer by August 14, 2026 if the lodger house supper goes ahead.\n2026-08-08 | Omar | Ana | Relax, I'll feed the house plants by August 12, 2026 for sure.\n2026-08-08 | Omar | Ana | Scratch what I said, I won't feed the house plants.\n2026-08-09 | Kai | group | Yep, the lodger house supper is on as planned.\n2026-08-14 | Kai | Ana | Ah, no stress, no need for you to defrost the top freezer",
  "question": "By the end of August 17, 2026, has Ana kept the promise to defrost the top freezer?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe359144924",
  "kind": "choice",
  "text": "Export from the support queue, covering the desk plan; passed on by Femi.\n\nMembers: Hana, Femi, Ines, Ana\nChat export (date | from | to | message):\n2026-10-27 | Hana | Femi | I will replace the kitchen filters by 3 November 2026.\n2026-10-27 | Femi | Ana | Relax, I'll send the expense receipts by 29 October 2026 for sure.\n2026-10-29 | Hana | Ines | Only if the lease viewing is on, I will order the office stationery by 2 November 2026.\n2026-10-30 | Ines | group | Sadly, the lease viewing won't go ahead.\n2026-11-02 | Femi | Hana | No worries, you don't need to replace the kitchen filters",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Hana's promise to replace the kitchen filters at the end of 7 November 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Not yet due",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "qb479f537d6",
  "kind": "yes/no",
  "text": "Tess saved this so we stay on the same page about the lodger house rules, mates.\n\nMembers: Elif, Tess, Hana\nChat export (date | from | to | message):\n2026-02-06 | Tess | Hana | Committing to replace the loo roll by Thursday, 12 February 2026.\n2026-02-10 | Hana | Tess | Absolutely, I will cut a spare door key by Sunday, 15 February 2026.\n2026-02-13 | Hana | Tess | Promise to wipe the shared kitchen counter by Saturday, 21 February 2026 if the lodger farewell supper goes ahead.\n2026-02-14 | Tess | Hana | Ah, no stress, no need for you to cut a spare door key\n2026-02-19 | Hana | group | Team, the lodger farewell supper is not happening.",
  "question": "Was Hana's promise to cut a spare door key not kept as of Tuesday, 17 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q818c241218",
  "kind": "choice",
  "text": "Subject: Saved thread about the guest welcome plan\nThis export came from Leila and is pasted in full below.\n\nMembers: Jonas, Leila, Elif\nChat log (oldest first):\n[4 Mar 2026] Jonas: @Elif Ticket's mine, I'll fill the cleaning cupboard by 10 March 2026.\n[8 Mar 2026] Elif: @Jonas As long as the check out clean is on, I will restock the guest toiletries by 14 March 2026.\n[10 Mar 2026] Leila: Brilliant news everyone, the check out clean is a go!\n[11 Mar 2026] Jonas: @Leila I'll wheel the bins out by 19 March 2026, promise.\n[12 Mar 2026] Jonas: Any news on plans to restock the guest toiletries?\n[14 Mar 2026] Elif: @Jonas Guess what, I managed to restock the guest toiletries!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Elif's promise to restock the guest toiletries at the end of 14 March 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "qdbf26c48f8",
  "kind": "yes/no",
  "text": "Volunteer chat export. Saved by Sami, it covers the school fundraiser.\n\nMembers: Kofi, Sami, Lena\nChat export (date | from | to | message):\n2026-05-23 | Kofi | Sami | As long as the summer fete is on, I will wrap the prize hampers by 28 May 2026.\n2026-05-25 | Kofi | Lena | As long as the field day is on, I'll return the borrowed trestle tables by 28 May 2026.\n2026-05-26 | Sami | Kofi | Guaranteed I'll print the raffle tickets by 30 May 2026.\n2026-05-27 | Sami | Kofi | I assure you I'll send the newsletter drafts by 3 Jun 2026 if the reading festival is on.\n2026-05-28 | Lena | Sami | Quick update: you do not need to print the raffle tickets at all.\n2026-05-28 | Sami | Kofi | Ticked off: print the raffle tickets, feels so good",
  "question": "Is the promise to print the raffle tickets kept by Sami as of 29 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb5599d8263",
  "kind": "choice",
  "text": "Pasted from our flat chat by Lee, the bit about the guest welcome plan.\n\nMembers: Lee, Tess, Femi\nChat log (oldest first):\n[10 Oct 2026] Tess: @Lee I promise to wheel the bins out by 12 Oct 2026 if the check out clean is on.\n[14 Oct 2026] Tess: @Femi Relax, I'll leave the welcome basket by 17 Oct 2026, promise.\n[14 Oct 2026] Tess: @Femi My sincere apologies, I am unable to leave the welcome basket.\n[15 Oct 2026] Lee: @Tess I promise to scrub the hot tub by 22 Oct 2026 if the guest arrival evening is on.\n[17 Oct 2026] Femi: @Tess You don't have to leave the welcome basket at all",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Tess's promise to leave the welcome basket at the end of 19 Oct 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Not yet due",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q146e9e1313",
  "kind": "choice",
  "text": "{\"saved_copy\": \"the data cleanup\", \"keeper\": \"Sami\", \"medium\": \"chat transcript\"}\n\nMembers: Mo, Kofi, Sami\nChat log (oldest first):\n[27 Apr 2026] Mo: @Kofi Count on me to rotate the test keys by 3 May 2026.\n[2 May 2026] Mo: @Kofi Mate, I promised, may I rotate the test keys by 6 May 2026 instead?\n[2 May 2026] Kofi: @Mo Got it, I'll deploy the staging build by 10 May 2026 for sure.\n[3 May 2026] Mo: @Kofi Change of plans: I will not rotate the test keys\n[4 May 2026] Mo: @Sami Provided the hackathon happens, I will run the security scan by 7 May 2026.\n[6 May 2026] Sami: Yay, the hackathon is all set to go!\n[7 May 2026] Sami: @Kofi Relax, mate, you're not expected to deploy the staging build",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Mo due to rotate the test keys at the end of 5 May 2026, after any agreed rescheduling?",
  "options": [
   "6 May 2026",
   "10 May 2026",
   "3 May 2026"
  ]
 },
 {
  "qid": "q08164cad5f",
  "kind": "choice",
  "text": "{\"chat_export\": \"the bathroom refit\", \"saved_by\": \"Kai\", \"scope\": \"group chat\"}\n\nMembers: Kai, Zara, Jonas, Rhea\nChat export (date | from | to | message):\n2026-02-23 | Kai | Zara | I'll fetch the paint samples by March 4, 2026 if the mortgage valuation visit goes ahead.\n2026-02-26 | Jonas | group | Update: the mortgage valuation visit is going ahead as planned.\n2026-02-27 | Jonas | Kai | Count on me to pick up the grout bag by March 7, 2026.\n2026-02-28 | Zara | Kai | I'll be sure to print the floor plan by March 5, 2026.\n2026-02-28 | Rhea | Jonas | I'll sweep the dust from stairs by March 2, 2026, promise.\n2026-02-28 | Jonas | Kai | Is it all right if I pick up the grout bag by March 11, 2026 instead?\n2026-03-04 | Rhea | Jonas | Go ahead and pick up the grout bag by March 11, 2026, that is fine.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Jonas due to pick up the grout bag at the end of March 12, 2026, after any agreed rescheduling?",
  "options": [
   "March 5, 2026",
   "March 7, 2026",
   "March 11, 2026"
  ]
 },
 {
  "qid": "qc73a645c22",
  "kind": "yes/no",
  "text": "{\"item\": \"chat export\", \"matter\": \"the winter concert\", \"saved_by\": \"Oskar\", \"layout\": \"plain\"}\n\nMembers: Femi, Sami, Elif, Oskar\nChat log (oldest first):\n[14 Jul 2026] Femi: @Sami You can bet I'll print the song sheets by 19 July 2026.\n[15 Jul 2026] Femi: Might manage to set up the sound desk by 21 July 2026, who knows.\n[16 Jul 2026] Femi: @Elif I own this, I'll set up the sound desk by 23 July 2026.\n[20 Jul 2026] Sami: @Elif Promise to return the library scores by 26 July 2026 if the choir festival goes ahead.\n[23 Jul 2026] Femi: @Elif Log entry: set up the sound desk, carried out\n[24 Jul 2026] Elif: Yep, the choir festival is on as planned.",
  "question": "Under the rules on the card, is the promise Femi made to set up the sound desk kept as of 29 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf1698bca5e",
  "kind": "choice",
  "text": "Yo flatmates, Femi shared this chat about the street watch scheme, so chip in.\n\nMembers: Femi, Hana, Kofi, Omar\nChat log (oldest first):\n[28 Sep 2026] Kofi: @Hana Count on me to lock the side gate by 2026-10-03 if the speed camera survey is on.\n[30 Sep 2026] Kofi: @Femi Relax, I'll clear the hedge trimmings by 2026-10-05, promise.\n[4 Oct 2026] Femi: @Hana I'll return the ladders by 2026-10-13 as long as the bonfire night is on.\n[5 Oct 2026] Hana: @Kofi No worries, you don't need to clear the hedge trimmings\n[5 Oct 2026] Kofi: @Femi To note: I have managed to clear the hedge trimmings",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Kofi's promise to clear the hedge trimmings sit at the end of 2026-10-11, exactly?",
  "options": [
   "Broken",
   "Waived",
   "Not triggered",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q5a32017172",
  "kind": "choice",
  "text": "Subject: Saved thread about the mobile release\nThis export came from Mo and is pasted in full below.\n\nMembers: Yuki, Bruno, Mo, Arlo\nChat log (oldest first):\n[6 Apr 2026] Arlo: @Yuki I'm aiming to deploy the staging build by 11 Apr 2026, might manage it.\n[8 Apr 2026] Arlo: @Yuki Guaranteed I'll deploy the staging build by 12 Apr 2026.\n[8 Apr 2026] Yuki: @Arlo As long as the sprint demo is on, I will restart the build server by 11 Apr 2026.\n[9 Apr 2026] Yuki: Yep, the sprint demo is on as planned.\n[11 Apr 2026] Arlo: @Yuki On my action item, may I deploy the staging build by 15 Apr 2026 instead?\n[11 Apr 2026] Bruno: @Arlo Fine by me, you can deploy the staging build by 15 Apr 2026.\n[11 Apr 2026] Bruno: @Arlo Good news, you're let off having to deploy the staging build\n[11 Apr 2026] Arlo: @Yuki Ticked off: deploy the staging build, feels so good",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo what's the latest day Arlo has to deploy the staging build by at the end of 18 Apr 2026, given any new date people agreed to?",
  "options": [
   "15 Apr 2026",
   "12 Apr 2026",
   "11 Apr 2026"
  ]
 },
 {
  "qid": "qacab60ca6f",
  "kind": "choice",
  "text": "Pasted into the project log by Greta, the thread with a client about the showreel refresh.\n\nMembers: Mo, Rhea, Nadia, Greta\nChat export (date | from | to | message):\n2026-03-19 | Mo | Nadia | Absolutely, I will record the voice over by 2026-03-23.\n2026-03-22 | Mo | Nadia | Mate, I promised, may I record the voice over by 2026-03-28 instead?\n2026-03-22 | Rhea | Mo | Works for me, fine for you to record the voice over by 2026-03-28.\n2026-03-24 | Mo | Nadia | I regret to say that I shall not record the voice over.\n2026-03-25 | Rhea | Mo | Got it, I'll send the colour notes by 2026-04-01 for sure.\n2026-03-29 | Nadia | Rhea | Only if the shoot day is on, I will upload the render files by 2026-04-02.\n2026-03-29 | Rhea | Mo | I'll export the subtitle files by 2026-04-01 as long as the festival premiere is on.\n2026-03-29 | Nadia | group | Yep, the festival premiere is on as planned.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, what is the deadline for Mo to record the voice over at the end of 2026-03-27, with any agreed change of date counted?",
  "options": [
   "2026-03-28",
   "2026-03-23",
   "2026-04-01"
  ]
 },
 {
  "qid": "qce4dd9c17d",
  "kind": "choice",
  "text": "Subject: the data cleanup\nBelow is the group chat that Ivo saved, unedited.\n\nMembers: Malik, Ivo, Lee, Ravi\nChat log (oldest first):\n[17 Apr 2026] Ravi: @Malik I'll be sure to run the security scan by 24 Apr 2026.\n[20 Apr 2026] Ravi: @Ivo I'll try to rotate the test keys by 26 Apr 2026, no guarantee.\n[20 Apr 2026] Malik: @Ravi Count on me to label the bug reports by 27 Apr 2026 if the sprint demo is on.\n[21 Apr 2026] Ravi: @Ivo Count on me, I'll rotate the test keys by 28 Apr 2026.\n[25 Apr 2026] Ravi: @Ivo Ta-da, I went and did it: rotate the test keys!\n[25 Apr 2026] Ivo: Yay, the sprint demo is all set to go!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Ravi's promise to rotate the test keys have at the end of 27 Apr 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Kept",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q3695e032d9",
  "kind": "yes/no",
  "text": "Subject: copy of the chat about the online store move\nFor your records, the saved chat is below, from Jonas.\n\nMembers: Ana, Jonas, Dara\nChat log (oldest first):\n[14 Jan 2026] Ana: @Jonas I assure you I'll restore the old theme by 21 Jan 2026 if the site handover is on.\n[16 Jan 2026] Jonas: @Ana Absolutely, I will send the stock spreadsheet by 23 Jan 2026.\n[16 Jan 2026] Jonas: @Ana I need to take back my commitment to send the stock spreadsheet.\n[18 Jan 2026] Ana: @Dara Promise to print the packing slips by 27 Jan 2026 if the pop up stall goes ahead.\n[23 Jan 2026] Dara: @Jonas Please don't feel you have to send the stock spreadsheet\n[30 Jan 2026] Ana: How's the plan to send the stock spreadsheet?",
  "question": "At the end of 28 Jan 2026, has the promise Jonas made to send the stock spreadsheet been broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbce9f57758",
  "kind": "choice",
  "text": "Leila shared this family chat about the reunion weekend for the relatives.\n\nMembers: Ana, Ravi, Dara, Leila\nChat log (oldest first):\n[12 May 2026] Ravi: @Leila It's on me to print the family tree chart by 20 May 2026.\n[13 May 2026] Ana: @Ravi As long as the karaoke night is on, I will send the group invitations by 21 May 2026.\n[15 May 2026] Ana: On track for the karaoke night to happen as planned.\n[18 May 2026] Ana: @Ravi Mind giving me until 27 May 2026 to send the group invitations?\n[21 May 2026] Leila: @Ana Of course, it is fine for you to send the group invitations by 27 May 2026.\n[21 May 2026] Leila: @Ana Please don't feel you have to send the group invitations\n[22 May 2026] Ana: @Ravi Ta-da, I went and did it: send the group invitations!",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Ana to send the group invitations at the end of 26 May 2026, counting any agreed change of date?",
  "options": [
   "21 May 2026",
   "27 May 2026",
   "20 May 2026"
  ]
 },
 {
  "qid": "qcbad1cec0c",
  "kind": "choice",
  "text": "A written chat between housemates about the care plan. Exported from the device by Nadia.\n\nMembers: Nadia, Ines, Lee\nChat log (oldest first):\n[3 Feb 2026] Ines: @Lee Wish me luck, hoping to collect the post by 11 February 2026.\n[5 Feb 2026] Ines: @Lee I'll collect the post by 8 February 2026 as long as the carer handover is on.\n[5 Feb 2026] Ines: On track for the carer handover to happen as planned.\n[7 Feb 2026] Ines: @Lee Lovely, I'll wash the bed linen by 12 February 2026 for sure.\n[9 Feb 2026] Ines: @Lee Ticked off my list: collect the post, yay.\n[14 Feb 2026] Ines: @Lee Ticked off: wash the bed linen, feels so good\n\nGenerated automatically: the chat as exported for Nadia predates recent messages, so its dates are not reliable.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Ines's promise to collect the post receive at the end of 8 February 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Waived",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "qaf004cb0d1",
  "kind": "yes/no",
  "text": "Flat chat, exported by Sami for the household.\nSubject: the student house hunt\n\nMembers: Dara, Lee, Kai, Sami\nChat log (oldest first):\n[30 Aug 2026] Dara: @Sami Ticket's mine, I'll store the spare bike by Saturday, 5 September 2026.\n[30 Aug 2026] Kai: @Dara Ah, no stress, no need for you to store the spare bike\n[31 Aug 2026] Dara: @Lee Only if the agent inventory walk is on, I will forward the inventory photos by Monday, 7 September 2026.\n[1 Sep 2026] Kai: @Sami As long as the gas safety inspection is on, I'll photograph the bathroom mould by Tuesday, 8 September 2026.\n[8 Sep 2026] Dara: @Sami Ticked off: store the spare bike, feels so good",
  "question": "Under the rules on the card, is it true that Dara has not kept the promise to store the spare bike as of Saturday, 5 September 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qae70422e9e",
  "kind": "choice",
  "text": "Subject: Saved thread about the autumn term budget\nThis export came from Jonas and is pasted in full below.\n\nMembers: Ivo, Sami, Jonas, Malik\nChat log (oldest first):\n[3 Mar 2026] Jonas: @Sami Provided the check in visit happens, I'll forward the inventory photos by 7 March 2026.\n[5 Mar 2026] Sami: @Jonas Committing to collect the parcel from porch by 13 March 2026.\n[5 Mar 2026] Ivo: Sorry all, the check in visit is called off.\n[7 Mar 2026] Sami: @Jonas Absolutely, I will copy the house keys by 15 March 2026.\n[13 Mar 2026] Jonas: @Sami Ah, no stress, no need for you to collect the parcel from porch",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Sami made to collect the parcel from porch at the end of 16 March 2026?",
  "options": [
   "Kept",
   "Waived",
   "Broken",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q44d2e46684",
  "kind": "yes/no",
  "text": "Attached chat: the documentary cut\nForwarded by: Tess\n\nMembers: Femi, Tess, Ines, Bruno\nChat export (date | from | to | message):\n2026-01-29 | Femi | Bruno | Count on me, I'll record the voice over by 3 Feb 2026.\n2026-01-29 | Bruno | Tess | Only if the agency review call is on, I will ship the hard drive by 1 Feb 2026.\n2026-01-30 | Ines | Femi | Quick update: you do not need to record the voice over at all.\n2026-01-31 | Bruno | group | Sorry, the agency review call is off.\n2026-02-01 | Femi | Bruno | To my relief, I managed to record the voice over.",
  "question": "Applying the card's rules, can it be said that Femi has not kept the promise to record the voice over at the end of 6 Feb 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q61016b6570",
  "kind": "choice",
  "text": "{\"thread_kind\": \"exported conversation\", \"about\": \"the family day out\", \"exported_by\": \"Yuki\"}\n\nMembers: Ivo, Malik, Yuki, Nadia\nChat log (oldest first):\n[26 Sep 2026] Nadia: Wish me luck, hoping to mend the kite string by 8 October 2026.\n[28 Sep 2026] Nadia: @Malik Count on me to mend the kite string by 5 October 2026, if the sleepover weekend happens.\n[2 Oct 2026] Yuki: @Malik I'll tidy the playroom by 9 October 2026, promise.\n[4 Oct 2026] Nadia: Please note the sleepover weekend will proceed.\n[6 Oct 2026] Nadia: @Malik Got myself to mend the kite string lol.\n[11 Oct 2026] Yuki: @Malik Ticked off my list: tidy the playroom, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Nadia's promise to mend the kite string turn out at the end of 10 October 2026?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q07855f73ec",
  "kind": "choice",
  "text": "Client thread on the holiday catalogue, saved by Mo for the project log.\n\nMembers: Mo, Hana, Kofi\nChat log (oldest first):\n[12 Jul 2026] Hana: @Kofi Count on me to fetch the domain login by 20 July 2026 if the courier pickup is on.\n[14 Jul 2026] Kofi: @Hana As long as the product photo day is on, I'll fix the checkout button by 17 July 2026.\n[14 Jul 2026] Kofi: @Mo I own this, I'll print the packing slips by 19 July 2026.\n[18 Jul 2026] Kofi: @Hana I'll be sure to set up the email forwarding by 25 July 2026.\n[18 Jul 2026] Kofi: @Mo Scratch what I said, I won't print the packing slips.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Kofi's promise to print the packing slips at the end of 18 July 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q202cf13355",
  "kind": "choice",
  "text": "Malik exported this channel chat about the data cleanup for the team.\n\nMembers: Femi, Malik, Tomas, Arlo\nChat log (oldest first):\n[17 May 2026] Malik: @Tomas Relax, I'll run the security scan by 20 May 2026, promise.\n[18 May 2026] Malik: @Femi Promise to update the dependency list by 22 May 2026 if the hackathon goes ahead.\n[18 May 2026] Femi: Oh cheers, that helps.\n[18 May 2026] Tomas: Yep, the hackathon is on as planned.\n[19 May 2026] Malik: @Femi Mate, I promised, may I update the dependency list by 28 May 2026 instead?\n[21 May 2026] Femi: @Malik No, you need to update the dependency list by the original date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 23 May 2026, what status has Malik's promise to update the dependency list got?",
  "options": [
   "Not yet due",
   "Broken",
   "Waived",
   "Not triggered",
   "Kept"
  ]
 }
]
