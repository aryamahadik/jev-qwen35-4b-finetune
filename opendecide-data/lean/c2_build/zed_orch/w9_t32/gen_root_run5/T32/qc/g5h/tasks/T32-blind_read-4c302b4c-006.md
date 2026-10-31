# G5-H blind read (all free-form rows) T32-blind_read-4c302b4c-006 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root/T32/qc/g5h/answers/T32-blind_read-4c302b4c-006.json

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
  "qid": "q11d1580379",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the spare room plan\nThe thread below comes from Mo and is passed on as it is.\n\nMembers: Arlo, Mo, Ivo, Hana\nChat export (date | from | to | message):\n2026-01-17 | Mo | Arlo | I will sort the recycling bags by 22 Jan 2026 only if the lodger house supper happens.\n2026-01-19 | Arlo | group | Quick heads up, the lodger house supper is scrapped.\n2026-01-19 | Arlo | Hana | I promise to defrost the top freezer by 24 Jan 2026.\n2026-01-22 | Mo | Arlo | Mate, I promised, may I sort the recycling bags by 28 Jan 2026 instead?\n2026-01-22 | Arlo | Mo | Aw no, you need to sort the recycling bags by the original date!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Mo's promise to sort the recycling bags turn out at the end of 22 Jan 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Broken",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q7f26f98efe",
  "kind": "yes/no",
  "text": "Ivo shared this so the allotment expansion is easy to find, flatmates.\n\nMembers: Ivo, Ines, Jonas\nChat log (oldest first):\n[4 Jul 2026] Ines: @Jonas You can bank on me to build the compost bay by Monday, 6 July 2026.\n[5 Jul 2026] Ines: @Ivo I promise to weed the carrot row by Thursday, 9 July 2026.\n[6 Jul 2026] Ivo: Where are you up to with plans to weed the carrot row?\n[7 Jul 2026] Jonas: @Ivo Lovely, I'll sow the broad beans by Saturday, 11 July 2026 if the harvest supper is on.\n[8 Jul 2026] Ines: @Jonas Provided the allotment site visit happens, I will sharpen the hand hoe by Wednesday, 15 July 2026.\n[9 Jul 2026] Ines: @Ivo For the record: I was able to weed the carrot row",
  "question": "Did Ines keep the promise to weed the carrot row as of Friday, 10 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qcfb7bf65cc",
  "kind": "yes/no",
  "text": "Saved by Omar, this talk about the house refit is just for family.\n\nMembers: Malik, Ivo, Nadia, Omar\nChat export (date | from | to | message):\n2026-05-25 | Malik | Omar | Promise to return the tile cutter by 27 May 2026 if the mortgage valuation visit goes ahead.\n2026-05-26 | Ivo | Malik | You can bank on me to scrape the old wallpaper by 4 Jun 2026.\n2026-05-27 | Malik | Ivo | Promise to sweep the dust from stairs by 2 Jun 2026 if the removal van arrival goes ahead.\n2026-05-27 | Malik | group | Team, the removal van arrival stays on as booked.\n2026-05-30 | Ivo | Nadia | I promise to hang the new curtain rail by 7 Jun 2026.\n2026-06-09 | Ivo | Nadia | Ta-da, I went and did it: hang the new curtain rail!",
  "question": "Would a check of the chat at the end of 11 Jun 2026 show the promise Ivo made to hang the new curtain rail as broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q67c98a2cd5",
  "kind": "yes/no",
  "text": "Posted by Greta from the work channel: the grant renewal.\n\nMembers: Jonas, Lena, Greta\nChat log (oldest first):\n[23 Apr 2026] Greta: @Lena I promise to scan the field notes by 25 Apr 2026 if the grant panel is on.\n[25 Apr 2026] Jonas: @Greta I'll book the microscope slot by 28 Apr 2026, providing the conference trip goes ahead.\n[25 Apr 2026] Greta: On track for the conference trip to happen as planned.\n[27 Apr 2026] Greta: @Jonas Got it, I'll fetch the grant forms by 3 May 2026 for sure.\n[3 May 2026] Greta: @Jonas Is 8 May 2026 alright for me to fetch the grant forms?\n[3 May 2026] Jonas: @Greta The original date stands, so you need to fetch the grant forms.",
  "question": "Did the promise that Jonas made to book the microscope slot turn out broken, waived, not triggered or not yet due, rather than kept, on 29 Apr 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q52bd75da44",
  "kind": "choice",
  "text": "Committee chat on the new term plans, forwarded by Ravi to the volunteers.\n\nMembers: Zara, Ravi, Leila, Ivo\nChat export (date | from | to | message):\n2026-07-23 | Zara | Ivo | I'll book the school hall by 29 July 2026 if the reading festival goes ahead.\n2026-07-25 | Ravi | group | Yay, the reading festival is all set to go!\n2026-07-27 | Leila | Zara | I'll be sure to return the borrowed trestle tables by 3 August 2026.\n2026-07-27 | Leila | Zara | Is it all right if I return the borrowed trestle tables by 6 August 2026 instead?\n2026-07-29 | Zara | Ivo | Ta-da, I went and did it: book the school hall!\n2026-07-30 | Zara | Leila | Oh hun, I can't budge, so return the borrowed trestle tables by the old date!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Zara made to book the school hall at the end of 29 July 2026?",
  "options": [
   "Waived",
   "Broken",
   "Not triggered",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qb1b864723c",
  "kind": "choice",
  "text": "Here is the thread on the vegetable plot plan, posted by Elif for the house.\n\nMembers: Zara, Bruno, Tomas, Elif\nChat log (oldest first):\n[1 Jun 2026] Tomas: @Bruno I'll fix the shed door by 7 Jun 2026, promise.\n[2 Jun 2026] Tomas: @Bruno If the harvest supper is on, I'll definitely dig the potato patch by 6 Jun 2026.\n[4 Jun 2026] Tomas: @Bruno On my action item, may I fix the shed door by 12 Jun 2026 instead?\n[5 Jun 2026] Bruno: @Tomas Of course, it is fine for you to fix the shed door by 12 Jun 2026.\n[6 Jun 2026] Tomas: @Bruno Lovely, I'll build the compost bay by 12 Jun 2026 if the plot inspection is on.\n[8 Jun 2026] Bruno: Sorry all, the plot inspection is not happening.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 10 Jun 2026, what status has Tomas's promise to build the compost bay got?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q069a4eb9db",
  "kind": "yes/no",
  "text": "Saved by Tess, this talk about the reunion planning is just for family.\n\nMembers: Wren, Omar, Hana, Tess\nChat log (oldest first):\n[30 Mar 2026] Hana: @Omar Count on me to pay the catering company by 4 April 2026 if the reunion lunch is on.\n[1 Apr 2026] Tess: @Wren Relax, I'll fetch the speaker system by 8 April 2026, promise.\n[2 Apr 2026] Wren: Really pleased to say the reunion lunch will go ahead!\n[6 Apr 2026] Wren: Quick check, any update on plans to pay the catering company?\n[7 Apr 2026] Tess: @Wren Mate, I promised, may I fetch the speaker system by 11 April 2026 instead?\n[8 Apr 2026] Wren: @Tess Yes, happy for you to fetch the speaker system by 11 April 2026 instead.",
  "question": "Is the promise Hana made to pay the catering company in a status other than broken at the end of 4 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0101e46b6f",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the garden makeover\nThis export from Ravi is pasted in full for readers who want it.\n\nMembers: Ines, Ravi, Kai\nChat export (date | from | to | message):\n2026-09-23 | Kai | Ines | You can bank on me to pay the plumbing invoice by 25 Sep 2026.\n2026-09-23 | Kai | Ines | Scratch what I said, I won't pay the plumbing invoice.\n2026-09-25 | Ravi | Kai | I promise to return the tile cutter by 1 Oct 2026 if the builder quote meeting is on.\n2026-09-26 | Ravi | Kai | I'll be sure to pick up the grout bag by 29 Sep 2026.\n2026-09-27 | Ravi | Kai | As long as the kitchen fitting day is on, I'll measure the hallway for shelves by 5 Oct 2026.\n2026-09-27 | Kai | group | Please note the builder quote meeting will proceed.",
  "question": "Is it true that the promise Ravi made to return the tile cutter has not been broken at the end of 2 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa2041009ee",
  "kind": "choice",
  "text": "Here is the big house plan, posted by Greta for the family to read.\n\nMembers: Zara, Greta, Oskar, Elif\nChat log (oldest first):\n[15 Feb 2026] Elif: Might manage to defrost the old fridge by 20 February 2026, who knows.\n[17 Feb 2026] Elif: @Zara Lovely, I'll defrost the old fridge by 22 February 2026 for sure.\n[21 Feb 2026] Elif: @Zara Think 27 February 2026 would work if I defrost the old fridge instead?\n[21 Feb 2026] Zara: @Elif Yes, you're welcome to defrost the old fridge by 27 February 2026 instead.\n[22 Feb 2026] Zara: @Elif I assure you I'll scrub the cellar steps by 28 February 2026 if the chimney sweep visit is on.\n[22 Feb 2026] Zara: Scrapping the chimney sweep visit, apologies to all.\n[26 Feb 2026] Greta: @Oskar Relax, I'll tidy the boot room by 28 February 2026, promise.\n[26 Feb 2026] Elif: @Zara Log entry: defrost the old fridge, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIf the chat is checked at the end of 5 March 2026, which date marks the deadline for Elif to defrost the old fridge, with agreed date changes included?",
  "options": [
   "27 February 2026",
   "28 February 2026",
   "22 February 2026"
  ]
 },
 {
  "qid": "q4d639cb6ea",
  "kind": "choice",
  "text": "Saved by Femi, this talk about the vegetable plot plan is just for family.\n\nMembers: Sami, Ana, Femi\nChat log (oldest first):\n[1 Aug 2026] Sami: @Femi If the water tank delivery is on, I'll definitely dig the potato patch by 6 Aug 2026.\n[2 Aug 2026] Ana: @Sami Ticket's mine, I'll collect the seed potatoes by 9 Aug 2026.\n[3 Aug 2026] Ana: Sadly, the water tank delivery won't go ahead.\n[6 Aug 2026] Ana: @Sami Apologies, I'll not be able to collect the seed potatoes\n[7 Aug 2026] Sami: @Ana Ah, no stress, no need for you to collect the seed potatoes\n[9 Aug 2026] Sami: Where are you up to with plans to collect the seed potatoes?",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Ana's promise to collect the seed potatoes at the end of 7 Aug 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Kept",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "qdcb72ed155",
  "kind": "choice",
  "text": "Kai shared this so the winter concert is easy to follow for the volunteers.\n\nMembers: Greta, Nadia, Kai\nChat log (oldest first):\n[11 Jul 2026] Kai: @Nadia You can bank on me to set up the sound desk by 13 July 2026.\n[13 Jul 2026] Kai: @Nadia Relax, I'll move the piano by 17 July 2026, promise.\n[13 Jul 2026] Kai: @Greta Provided the sing along happens, I'll fetch the choir robes by 15 July 2026.\n[14 Jul 2026] Nadia: @Kai I promise to print the song sheets by 22 July 2026 if the joint concert is on.\n[17 Jul 2026] Nadia: @Kai No worries, you don't need to move the piano\n[19 Jul 2026] Greta: Really pleased to say the joint concert will go ahead!",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhere does Kai stand on the promise to move the piano at the end of 17 July 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Broken",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "qc663d8eae7",
  "kind": "yes/no",
  "text": "Exported by Tomas, this is the back and forth on the store makeover.\n\nMembers: Tomas, Lee\nChat log (oldest first):\n[15 Aug 2026] Lee: @Tomas I'll upload the sticker artwork by Friday, 21 August 2026, providing the gallery install goes ahead.\n[16 Aug 2026] Tomas: @Lee You can bank on me to pick the colour swatches by Saturday, 22 August 2026.\n[18 Aug 2026] Tomas: @Lee Quick report: I've managed to pick the colour swatches\n[20 Aug 2026] Lee: Yay, the gallery install is all set to go!\n[20 Aug 2026] Lee: @Tomas Correction, I will not be able to upload the sticker artwork.",
  "question": "According to the rules on the card, does the promise Lee made to upload the sticker artwork have any status except broken at the end of Monday, 24 August 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1e608fb227",
  "kind": "yes/no",
  "text": "Rhea saved this so we stay on the same page about the house refit, mates.\n\nMembers: Jonas, Bruno, Malik, Rhea\nChat export (date | from | to | message):\n2026-07-15 | Bruno | Malik | I'll collect the sanding pads by 22 Jul 2026 if the boiler install visit goes ahead.\n2026-07-17 | Jonas | Malik | Count on me to scrape the old wallpaper by 19 Jul 2026, if the damp survey inspection happens.\n2026-07-19 | Jonas | Malik | I will make sure to sweep the dust from stairs by 24 Jul 2026.\n2026-07-23 | Jonas | Malik | Might I ask whether I could sweep the dust from stairs by 28 Jul 2026 instead?\n2026-07-24 | Malik | Jonas | Yes, all good for you to sweep the dust from stairs by 28 Jul 2026 instead.\n2026-07-28 | Jonas | Malik | Ticked off my list: sweep the dust from stairs, yay.",
  "question": "Applying the rules on the card, has Jonas kept the promise to sweep the dust from stairs as of 2 Aug 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9a1ab031cd",
  "kind": "choice",
  "text": "Tenant and agent back-and-forth on the autumn term budget, forwarded by Ravi.\n\nMembers: Tomas, Jonas, Ravi, Lena\nChat log (oldest first):\n[18 Oct 2026] Tomas: @Lena I assure you I'll return the bin rota by 26 Oct 2026 if the freshers welcome night is on.\n[19 Oct 2026] Jonas: Update, the freshers welcome night will not take place.\n[21 Oct 2026] Tomas: @Jonas Relax, I'll store the spare bike by 23 Oct 2026 for sure.\n[22 Oct 2026] Tomas: @Jonas Scratch that, I'm not going to store the spare bike\n[24 Oct 2026] Tomas: @Lena Any chance I can return the bin rota by 31 Oct 2026 instead?\n[26 Oct 2026] Jonas: @Tomas Yes, all good for you to return the bin rota by 31 Oct 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Tomas made to return the bin rota have at the end of 22 Oct 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q5fd4988f92",
  "kind": "choice",
  "text": "Here is the thread on the flat upgrade list, posted by Kofi for the house.\n\nMembers: Kofi, Ivo, Bruno\nChat log (oldest first):\n[5 May 2026] Ivo: @Kofi I will email the leak photos by 8 May 2026 only if the flat viewing day happens.\n[5 May 2026] Bruno: @Ivo Ticket's mine, I'll bring the step stool by 13 May 2026.\n[8 May 2026] Ivo: @Kofi I assure you I'll ring the flat repair line by 17 May 2026 if the rent review meeting is on.\n[8 May 2026] Bruno: Afraid the rent review meeting is called off.\n[11 May 2026] Kofi: @Bruno You don't have to bring the step stool at all\n[13 May 2026] Bruno: @Ivo Mum, I did bring the step stool, haha.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Bruno's promise to bring the step stool at the end of 11 May 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "qde58db84bf",
  "kind": "yes/no",
  "text": "Team channel export, shared by Tomas, which is about the mobile release.\n\nMembers: Tomas, Hana, Greta\nChat export (date | from | to | message):\n2026-03-09 | Tomas | Greta | Provided the hackathon happens, I'll merge the login branch by 12 Mar 2026.\n2026-03-12 | Tomas | Greta | Count on me to restart the build server by 15 Mar 2026 if the server migration is on.\n2026-03-13 | Hana | group | Fab, we are on for the server migration as planned!\n2026-03-15 | Hana | Greta | Committing to run the security scan by 20 Mar 2026.\n2026-03-15 | Hana | Greta | Sorry, I won't run the security scan after all\n2026-03-15 | Hana | Tomas | Please don't feel you have to restart the build server",
  "question": "At the end of 15 Mar 2026, has Tomas broken its promise to restart the build server?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf6b6fb0622",
  "kind": "yes/no",
  "text": "Shared by Sami, this thread covers the showreel refresh as pasted from email.\n\nMembers: Tess, Zara, Dara, Sami\nChat export (date | from | to | message):\n2026-02-15 | Tess | Sami | If the voiceover session goes ahead, I'll gladly back up the project drives by 22 Feb 2026.\n2026-02-16 | Sami | Zara | I will make sure to export the subtitle files by 21 Feb 2026.\n2026-02-16 | Sami | Zara | For the record: I was able to export the subtitle files\n2026-02-18 | Tess | Sami | I will make sure to upload the render files by 26 Feb 2026.\n2026-02-19 | Dara | group | Lovely, the voiceover session is definitely happening!",
  "question": "At the end of 19 Feb 2026, does the promise Sami made to export the subtitle files have any status except broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q75bcf37a83",
  "kind": "choice",
  "text": "Tomas forwarded this for the committee as we dig in on the annual tour.\n\nMembers: Lena, Tomas, Tess\nChat log (oldest first):\n[24 May 2026] Tess: @Tomas I'll collect the timing tags by 31 May 2026, promise.\n[27 May 2026] Tomas: @Tess If the hill climb goes ahead, I'll wash the club jerseys by 2 June 2026.\n[27 May 2026] Lena: @Tomas Provided the group ride happens, I will pump the spare tyres by 1 June 2026.\n[30 May 2026] Tess: @Tomas Quick question, could I collect the timing tags by 5 June 2026 instead?\n[31 May 2026] Tomas: @Tess Yes, all good for you to collect the timing tags by 5 June 2026 instead.\n[5 Jun 2026] Tess: @Tomas For the record: I was able to collect the timing tags",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Tess gave to collect the timing tags have at the end of 9 June 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qe903024209",
  "kind": "choice",
  "text": "Subject: Saved thread about the spare room plan\nHere is a full export from Oskar, ready to read.\n\nMembers: Oskar, Greta, Ines\nChat export (date | from | to | message):\n2026-05-16 | Oskar | Ines | Ticket's mine, I'll sort the recycling bags by May 24, 2026.\n2026-05-19 | Ines | Greta | If the landlord inspection walk goes ahead, I'll gladly drop the parcel upstairs by May 23, 2026.\n2026-05-19 | Oskar | group | Yay, the landlord inspection walk is all set to go!\n2026-05-22 | Oskar | Ines | Scratch what I said, I won't sort the recycling bags.\n2026-05-24 | Ines | Oskar | Good news, you're let off having to sort the recycling bags",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Oskar's promise to sort the recycling bags at the end of May 28, 2026?",
  "options": [
   "Broken",
   "Kept",
   "Waived",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q8fbeb4c601",
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
  "qid": "q1434759844",
  "kind": "yes/no",
  "text": "Subject: Chat about the street watch scheme\nBelow is a copy that came from Wren, pasted as found.\n\nMembers: Ana, Malik, Lena, Wren\nChat log (oldest first):\n[20 Mar 2026] Ana: Maybe I can return the ladders by Monday, 30 March 2026.\n[21 Mar 2026] Ana: @Wren I'll return the ladders by Thursday, 26 March 2026, providing the hedge trimming day goes ahead.\n[22 Mar 2026] Lena: @Wren Relax, I'll feed the cat across the road by Monday, 30 March 2026, promise.\n[23 Mar 2026] Ana: Yay, the hedge trimming day is all set to go!\n[23 Mar 2026] Ana: @Wren Is it all right if I return the ladders by Sunday, 29 March 2026 instead?\n[23 Mar 2026] Wren: @Ana Not moving it, return the ladders by the existing date.",
  "question": "Would Ana be counted as having broken the promise to return the ladders at the end of Thursday, 26 March 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q497a7ada5d",
  "kind": "yes/no",
  "text": "Subject: Chat about the vegetable plot plan\nA plain copy from Sami follows, exactly as exported.\n\nMembers: Sami, Ana, Lena, Omar\nChat export (date | from | to | message):\n2026-10-30 | Lena | Sami | I own this, I'll stake the tomato canes by November 1, 2026.\n2026-10-30 | Lena | Sami | Log entry: stake the tomato canes, carried out\n2026-11-03 | Ana | Sami | If the plot inspection is on, I'll definitely deliver the surplus runner beans by November 7, 2026.\n2026-11-03 | Sami | group | Yay, the plot inspection is all set to go!\n2026-11-10 | Ana | Sami | Ticked off: deliver the surplus runner beans, feels so good",
  "question": "At the end of November 9, 2026, has the promise Ana made to deliver the surplus runner beans been broken?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7d88399f24",
  "kind": "yes/no",
  "text": "Subject: Chat about the grant renewal\nA plain copy from Priya follows, exactly as exported.\n\nMembers: Zara, Kai, Priya\nChat log (oldest first):\n[28 May 2026] Priya: @Zara Lovely, I'll return the library books by 5 Jun 2026 for sure.\n[29 May 2026] Kai: @Priya No need to return the library books, I'm letting you off\n[29 May 2026] Priya: @Zara To my relief, I managed to return the library books.\n[31 May 2026] Priya: @Zara I'll scan the field notes by 6 Jun 2026, providing the thesis defence goes ahead.\n[4 Jun 2026] Priya: Afraid the thesis defence is called off.",
  "question": "Under the rules on the card, is Priya's promise to return the library books broken, waived, not triggered or not yet due, rather than kept, as of 1 Jun 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qdc017f26d7",
  "kind": "yes/no",
  "text": "Casual chat for the flat, saved by Jonas, and it covers the house refit.\n\nMembers: Jonas, Lee, Yuki\nChat export (date | from | to | message):\n2026-03-01 | Jonas | group | Might manage to pay the plumbing invoice by 8 Mar 2026, who knows.\n2026-03-01 | Jonas | Yuki | If the removal van arrival goes ahead, I'll gladly collect the sanding pads by 10 Mar 2026.\n2026-03-02 | Jonas | Yuki | Relax, I'll pay the plumbing invoice by 9 Mar 2026, promise.\n2026-03-02 | Lee | group | Lovely, the removal van arrival is definitely happening!\n2026-03-03 | Yuki | Lee | You can bank on me to measure the hallway for shelves by 10 Mar 2026.\n2026-03-08 | Jonas | Yuki | Scratch that, I'm not going to pay the plumbing invoice",
  "question": "Has Jonas broken the promise to pay the plumbing invoice at the end of 13 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q53b00c66da",
  "kind": "choice",
  "text": "Exported by Priya, this is the back and forth on the showreel refresh.\n\nMembers: Sami, Nadia, Priya\nChat export (date | from | to | message):\n2026-03-20 | Priya | Nadia | Count on me to order the stock music licence by 25 March 2026.\n2026-03-22 | Nadia | group | No promises, but I'll aim to export the subtitle files by 1 April 2026.\n2026-03-23 | Nadia | Priya | I'll export the subtitle files by 31 March 2026 as long as the shoot day is on.\n2026-03-25 | Nadia | Priya | Quick update: you do not need to order the stock music licence at all.\n2026-03-29 | Sami | group | Just so you know, the shoot day is on as scheduled.\n2026-03-29 | Sami | Nadia | Don't sweat it, there's no need to export the subtitle files",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 30 March 2026, what status has Nadia's promise to export the subtitle files got?",
  "options": [
   "Not yet due",
   "Waived",
   "Not triggered",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "qc9494467b7",
  "kind": "choice",
  "text": "Client thread on the campaign edit, shared by Leila for the project log.\n\nMembers: Leila, Zara, Hana, Lee\nChat log (oldest first):\n[21 Feb 2026] Leila: @Zara Maybe I can order the stock music licence by 6 Mar 2026.\n[22 Feb 2026] Leila: @Zara I'll order the stock music licence by 2 Mar 2026, providing the client screening goes ahead.\n[23 Feb 2026] Lee: @Hana I will make sure to record the voice over by 3 Mar 2026.\n[23 Feb 2026] Lee: @Hana Scratch what I said, I won't record the voice over.\n[24 Feb 2026] Hana: Team, the client screening stays on as booked.\n[26 Feb 2026] Leila: @Zara For the record: I was able to order the stock music licence",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 28 Feb 2026, what status has Leila's promise to order the stock music licence got?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q025160a9cd",
  "kind": "yes/no",
  "text": "Volunteers, this is the choir tour thread that Elif shared with the committee.\n\nMembers: Lena, Greta, Elif\nChat log (oldest first):\n[30 Apr 2026] Elif: @Lena You can bank on me to move the piano by 4 May 2026.\n[2 May 2026] Elif: I'll try to send the audition reminders by 7 May 2026, can't promise!\n[3 May 2026] Greta: @Elif Relax, mate, you're not expected to move the piano\n[3 May 2026] Elif: @Greta I promise to send the audition reminders by 10 May 2026 if the joint concert is on.\n[7 May 2026] Elif: Lovely, the joint concert is definitely happening!\n[9 May 2026] Elif: @Greta Ta-da, I went and did it: send the audition reminders!",
  "question": "Does the card's rule set show that Elif has not kept the promise to send the audition reminders at the end of 13 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb08cf4d3c2",
  "kind": "yes/no",
  "text": "Messages with the letting agent about the balcony garden project, saved by Priya for the rental file.\n\nMembers: Tomas, Priya, Greta\nChat log (oldest first):\n[27 Sep 2026] Tomas: @Priya No promises, but I'll aim to remove the bathroom shelf by Tuesday, 29 September 2026.\n[28 Sep 2026] Tomas: @Priya If the flat viewing day is on, I'll definitely remove the bathroom shelf by Sunday, 4 October 2026.\n[3 Oct 2026] Priya: @Greta I own this, I'll collect the spare flat keys by Thursday, 8 October 2026.\n[3 Oct 2026] Priya: @Greta I promise to drop the bin bags off by Thursday, 8 October 2026 if the electrics safety check is on.\n[4 Oct 2026] Tomas: @Priya Might I ask whether I could remove the bathroom shelf by Wednesday, 7 October 2026 instead?\n[4 Oct 2026] Priya: @Tomas Yes, you have the green light to remove the bathroom shelf by Wednesday, 7 October 2026.",
  "question": "By the end of Monday, 5 October 2026, has Tomas kept the promise to remove the bathroom shelf?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qcdd8f3fb6c",
  "kind": "choice",
  "text": "Our flat chat about the house refit, saved by Ivo for whoever lives here.\n\nMembers: Bruno, Tess, Ivo\nChat export (date | from | to | message):\n2026-04-13 | Ivo | Tess | Guaranteed I'll return the tile cutter by 19 April 2026.\n2026-04-14 | Bruno | Tess | I'll be sure to hang the new curtain rail by 18 April 2026.\n2026-04-15 | Tess | Ivo | Nobody needs you to return the tile cutter, that's that\n2026-04-15 | Tess | Bruno | If the kitchen fitting day goes ahead, I'll gladly pick up the grout bag by 22 April 2026.\n2026-04-18 | Ivo | Bruno | As long as the removal van arrival is on, I will collect the sanding pads by 26 April 2026.\n2026-04-21 | Bruno | group | We are dropping the kitchen fitting day from the list.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Ivo's pledge to return the tile cutter at the end of 20 April 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Broken",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q52bf4756ea",
  "kind": "yes/no",
  "text": "Subject: Chat about the grant renewal\nBelow, with Femi named as the source, is the chat as exported.\n\nMembers: Ravi, Femi, Kai\nChat log (oldest first):\n[16 Jun 2026] Ravi: @Femi I'll scan the field notes by 24 June 2026 as long as the safety inspection is on.\n[18 Jun 2026] Kai: @Ravi Absolutely, I will book the microscope slot by 21 June 2026.\n[18 Jun 2026] Kai: @Ravi Count on me, I'll print the poster abstracts by 26 June 2026.\n[19 Jun 2026] Ravi: Sadly, the safety inspection is not going ahead.\n[29 Jun 2026] Kai: @Ravi Guess who managed to print the poster abstracts, go team!",
  "question": "According to the rules on the card, is it true that the promise Kai made to print the poster abstracts has not been broken at the end of 3 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf9a8c66f8e",
  "kind": "yes/no",
  "text": "Volunteers, here is the winter concert thread that Greta forwarded for us.\n\nMembers: Greta, Malik, Lee, Ivo\nChat log (oldest first):\n[21 Jan 2026] Ivo: @Lee If the carol concert goes ahead, I'll gladly fetch the choir robes by 24 January 2026.\n[21 Jan 2026] Malik: @Ivo I'll try to collect the sheet music by 30 January 2026.\n[22 Jan 2026] Malik: @Ivo Guaranteed I'll collect the sheet music by 29 January 2026.\n[23 Jan 2026] Malik: Really pleased to say the carol concert will go ahead!\n[26 Jan 2026] Malik: @Ivo Might I ask whether I could collect the sheet music by 1 February 2026 instead?\n[29 Jan 2026] Ivo: @Malik Please don't feel you have to collect the sheet music",
  "question": "Under the rules on the card, is the promise Malik made to collect the sheet music in a status other than broken at the end of 31 January 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q220dc08b06",
  "kind": "yes/no",
  "text": "Casual chat for the flat, saved by Jonas, and it covers the house refit.\n\nMembers: Jonas, Lee, Yuki\nChat export (date | from | to | message):\n2026-03-01 | Jonas | group | Might manage to pay the plumbing invoice by 8 Mar 2026, who knows.\n2026-03-01 | Jonas | Yuki | If the removal van arrival goes ahead, I'll gladly collect the sanding pads by 10 Mar 2026.\n2026-03-02 | Jonas | Yuki | Relax, I'll pay the plumbing invoice by 9 Mar 2026, promise.\n2026-03-02 | Lee | group | Lovely, the removal van arrival is definitely happening!\n2026-03-03 | Yuki | Lee | You can bank on me to measure the hallway for shelves by 10 Mar 2026.\n2026-03-08 | Jonas | Yuki | Scratch that, I'm not going to pay the plumbing invoice",
  "question": "According to the rules on the card, does the promise Jonas made to pay the plumbing invoice have any status except broken at the end of 13 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q886e22570c",
  "kind": "choice",
  "text": "Subject: Chat about the packing plan\nBelow is a copy that came from Oskar, pasted as found.\n\nMembers: Ines, Oskar, Tomas, Ivo\nChat export (date | from | to | message):\n2026-08-14 | Oskar | Ines | Count on me to send the packing list by 24 Aug 2026 if the guided tour is on.\n2026-08-17 | Ivo | Tomas | Guaranteed I'll check the passport copies by 20 Aug 2026.\n2026-08-18 | Ines | Tomas | Lovely, I'll pack the travel adaptors by 25 Aug 2026 if the beach picnic is on.\n2026-08-20 | Ivo | Tomas | Is it all right if I check the passport copies by 23 Aug 2026 instead?\n2026-08-20 | Ines | Ivo | Revised deadline is 23 Aug 2026, so you can check the passport copies.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Ivo made to check the passport copies at the end of 20 Aug 2026?",
  "options": [
   "Waived",
   "Broken",
   "Kept",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qe94690d7c6",
  "kind": "yes/no",
  "text": "Posted by Jonas from the work channel, the trade show push thread.\n\nMembers: Ines, Jonas, Femi\nChat export (date | from | to | message):\n2026-01-26 | Ines | Jonas | It's on me to pay the printing invoice by 30 January 2026.\n2026-01-30 | Jonas | Ines | I promise to draft the press release by 8 February 2026 if the webinar rehearsal is on.\n2026-01-30 | Jonas | group | Sorry, the webinar rehearsal is off.\n2026-01-31 | Jonas | Femi | I will send the newsletter copy by 7 February 2026.\n2026-02-04 | Jonas | Femi | For the record: I was able to send the newsletter copy\n2026-02-05 | Femi | group | How's the plan to send the newsletter copy?",
  "question": "Does the card's rule set show that Jonas has not kept the promise to send the newsletter copy at the end of 4 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2a49d84e59",
  "kind": "choice",
  "text": "Tomas forwarded this for the committee as we dig in on the annual tour.\n\nMembers: Lena, Tomas, Tess\nChat log (oldest first):\n[24 May 2026] Tess: @Tomas I'll collect the timing tags by 31 May 2026, promise.\n[27 May 2026] Tomas: @Tess If the hill climb goes ahead, I'll wash the club jerseys by 2 June 2026.\n[27 May 2026] Lena: @Tomas Provided the group ride happens, I will pump the spare tyres by 1 June 2026.\n[30 May 2026] Tess: @Tomas Quick question, could I collect the timing tags by 5 June 2026 instead?\n[31 May 2026] Tomas: @Tess Yes, all good for you to collect the timing tags by 5 June 2026 instead.\n[6 Jun 2026] Tess: @Tomas For the record: I was able to collect the timing tags",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Tess gave to collect the timing tags have at the end of 9 June 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qec2aa5c022",
  "kind": "choice",
  "text": "Casual chat for the flat, saved by Sami, and it covers the autumn term budget.\n\nMembers: Tomas, Lena, Elif, Sami\nChat log (oldest first):\n[5 Apr 2026] Sami: @Lena Committing to photograph the bathroom mould by Thursday, 9 April 2026.\n[5 Apr 2026] Sami: @Lena Correction, I will not be able to photograph the bathroom mould.\n[9 Apr 2026] Tomas: @Lena Ticket's mine, I'll store the spare bike by Wednesday, 15 April 2026.\n[10 Apr 2026] Tomas: @Lena I will ring the letting agent by Monday, 13 April 2026 only if the check in visit happens.\n[11 Apr 2026] Tomas: Sorry, the check in visit is off.\n[13 Apr 2026] Tomas: @Lena Ta-da, I went and did it: store the spare bike!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Tomas's promise to store the spare bike at the end of Friday, 17 April 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Not triggered",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q58d2d9a221",
  "kind": "yes/no",
  "text": "Casual chat for the flat, saved by Malik, and it covers the allotment expansion.\n\nMembers: Greta, Leila, Malik\nChat log (oldest first):\n[11 Sep 2026] Greta: @Malik Count on me, I'll dig the potato patch by 14 September 2026.\n[13 Sep 2026] Malik: @Greta Count on me to weed the carrot row by 18 September 2026, if the water tank delivery happens.\n[14 Sep 2026] Leila: Great news, the water tank delivery is on!\n[16 Sep 2026] Leila: @Greta Relax, I'll sow the broad beans by 22 September 2026, promise.\n[19 Sep 2026] Leila: @Greta Ticked off: sow the broad beans, feels so good",
  "question": "At the end of 20 September 2026, has the promise Leila made to sow the broad beans been broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe0e3d1469e",
  "kind": "choice",
  "text": "Subject: Chat about the home adaptations\nThe copy from Lee follows below as a plain record.\n\nMembers: Omar, Oskar, Elif, Lee\nChat log (oldest first):\n[6 Feb 2026] Oskar: @Elif Only if the hospital appointment is on, I will call the home nurse by 14 February 2026.\n[8 Feb 2026] Elif: @Oskar As long as the physio session is on, I will print the care schedule by 14 February 2026.\n[8 Feb 2026] Elif: @Omar It's on me to book the clinic transport by 13 February 2026.\n[10 Feb 2026] Omar: @Elif Good news, you're let off having to book the clinic transport\n[10 Feb 2026] Elif: Yay, the hospital appointment is all set to go!\n[10 Feb 2026] Lee: @Elif I own this, I'll collect the post by 19 February 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Elif made to book the clinic transport at the end of 14 February 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Kept",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q1a7ec81254",
  "kind": "yes/no",
  "text": "Team channel export, shared by Femi, which is about the spring campaign.\n\nMembers: Femi, Kofi, Kai\nChat export (date | from | to | message):\n2026-08-02 | Kofi | group | Fingers crossed I can return the rented camera gear by Tuesday, 4 August 2026.\n2026-08-03 | Kofi | Kai | As long as the influencer call is on, I'll return the rented camera gear by Saturday, 8 August 2026.\n2026-08-06 | Kai | group | Just so you know, the influencer call is on as scheduled.\n2026-08-08 | Femi | Kofi | You can bet I'll draft the press release by Tuesday, 11 August 2026.\n2026-08-08 | Kofi | Femi | Forget it, you won't need to draft the press release\n2026-08-08 | Kofi | Kai | To note: I have managed to return the rented camera gear",
  "question": "By the end of Saturday, 8 August 2026, has Kofi kept the promise to return the rented camera gear?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4da41eded4",
  "kind": "choice",
  "text": "Read up on the loft conversion, flatmates, as Nadia exported it.\n\nMembers: Dara, Malik, Nadia\nChat export (date | from | to | message):\n2026-03-11 | Malik | Nadia | Only if the kitchen fitting day is on, I will pick up the grout bag by Tuesday, March 17, 2026.\n2026-03-15 | Nadia | Dara | Relax, I'll pay the plumbing invoice by Sunday, March 22, 2026 for sure.\n2026-03-15 | Malik | Nadia | Good news, you're let off having to pay the plumbing invoice\n2026-03-16 | Malik | Nadia | I'll sweep the dust from stairs by Wednesday, March 25, 2026 as long as the boiler install visit is on.\n2026-03-23 | Nadia | Dara | To my relief, I managed to pay the plumbing invoice.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Nadia made to pay the plumbing invoice, what state is it in at the end of Wednesday, March 25, 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Waived",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q7ed400f04b",
  "kind": "yes/no",
  "text": "Subject: Saved chat on the annual tour\nHere is the export from Ana, for the record.\n\nMembers: Ana, Nadia, Mo, Bruno\nChat log (oldest first):\n[30 Jul 2026] Nadia: Maybe I can tune the gear cables by Monday, August 3, 2026.\n[1 Aug 2026] Nadia: @Mo I'll tune the gear cables by Tuesday, August 4, 2026 if the mechanics clinic goes ahead.\n[3 Aug 2026] Mo: Sorry all, the mechanics clinic is not happening.\n[4 Aug 2026] Mo: @Bruno You can bet I'll pump the spare tyres by Sunday, August 9, 2026.\n[5 Aug 2026] Ana: @Nadia Ticket's mine, I'll set up the feed stop by Monday, August 10, 2026.\n[5 Aug 2026] Mo: @Bruno Got it, I'll print the route cards by Saturday, August 8, 2026 for sure.",
  "question": "Did Nadia break the promise to tune the gear cables at the end of Wednesday, August 5, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qec6a49df69",
  "kind": "yes/no",
  "text": "Leila shared this channel export covering the staff handbook for the team.\n\nMembers: Arlo, Ravi, Leila\nChat log (oldest first):\n[21 May 2026] Ravi: @Arlo Count on me to return the printer toner by 28 May 2026 if the staff picnic is on.\n[22 May 2026] Leila: @Arlo Guaranteed I'll collect the visitor badges by 31 May 2026.\n[25 May 2026] Ravi: Lovely, the staff picnic is definitely happening!\n[28 May 2026] Ravi: @Arlo Ticked off my list: return the printer toner, yay.\n[29 May 2026] Ravi: @Leila Quick update: you do not need to collect the visitor badges at all.",
  "question": "Would you say Ravi kept the promise to return the printer toner at the end of 28 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb3655a363a",
  "kind": "yes/no",
  "text": "Shared by Zara from the work chat, with the data cleanup at its heart.\n\nMembers: Zara, Ana, Kofi\nChat log (oldest first):\n[20 Jul 2026] Kofi: @Zara As long as the code freeze is on, I will deploy the staging build by 25 July 2026.\n[21 Jul 2026] Kofi: @Zara Provided the sprint demo happens, I'll fix the test runner by 24 July 2026.\n[22 Jul 2026] Ana: @Zara I promise to merge the login branch by 25 July 2026.\n[23 Jul 2026] Kofi: Yay, the sprint demo is all set to go!\n[25 Jul 2026] Zara: @Ana Quick update: you do not need to merge the login branch at all.\n[25 Jul 2026] Kofi: @Zara Got myself to fix the test runner lol.",
  "question": "Under the rules on the card, is the promise Kofi made to fix the test runner in a status other than broken at the end of 28 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q803a329f4d",
  "kind": "yes/no",
  "text": "Posted by Malik from the work channel, the staff handbook thread.\n\nMembers: Elif, Greta, Malik\nChat log (oldest first):\n[2 Jul 2026] Malik: Fingers crossed I can set up the reception screen by 12 July 2026.\n[3 Jul 2026] Malik: @Elif I own this, I'll set up the reception screen by 10 July 2026.\n[8 Jul 2026] Greta: @Malik If the annual audit goes ahead, I'll gladly collect the visitor badges by 11 July 2026.\n[8 Jul 2026] Malik: @Elif Count on me, I'll order the office stationery by 17 July 2026.\n[9 Jul 2026] Greta: Update: the annual audit is going ahead as planned.\n[10 Jul 2026] Malik: @Elif Log entry: set up the reception screen, carried out",
  "question": "Applying the card's rules, does Malik's promise to set up the reception screen count as broken, waived, not triggered or not yet due, rather than kept, as of 10 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe78ed189a6",
  "kind": "yes/no",
  "text": "Committee chat on the ground upgrade, shared by Wren with the volunteers.\n\nMembers: Arlo, Wren, Omar\nChat log (oldest first):\n[17 Jul 2026] Wren: @Arlo Count on me, I'll mark the pitch lines by 20 July 2026.\n[18 Jul 2026] Arlo: @Wren I'll pump the match balls by 20 July 2026 if the training camp goes ahead.\n[19 Jul 2026] Arlo: Sadly, the training camp is not going ahead.\n[19 Jul 2026] Omar: @Wren I will collect the referee whistles by 23 July 2026.\n[19 Jul 2026] Omar: @Wren To note: I have managed to collect the referee whistles\n[25 Jul 2026] Wren: Update on your plan to collect the referee whistles?",
  "question": "On 24 July 2026 itself, has Omar not kept the promise to collect the referee whistles?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc499900a17",
  "kind": "choice",
  "text": "Subject: Chat about the caring rota\nA plain copy from Ana follows, exactly as exported.\n\nMembers: Ana, Yuki, Rhea, Omar\nChat export (date | from | to | message):\n2026-04-19 | Omar | Rhea | Provided the hospital appointment happens, I'll drop off the hot meals by 25 April 2026.\n2026-04-21 | Omar | group | Team, the hospital appointment stays on as booked.\n2026-04-22 | Omar | Rhea | Lovely, I'll book the clinic transport by 30 April 2026 for sure.\n2026-04-25 | Omar | Rhea | Quick report: I've managed to drop off the hot meals\n2026-05-01 | Omar | Rhea | Ticked off: book the clinic transport, feels so good",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Omar's promise to drop off the hot meals turn out at the end of 25 April 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "qa26d8621d5",
  "kind": "yes/no",
  "text": "Team channel export, shared by Femi, which is about the spring campaign.\n\nMembers: Femi, Kofi, Kai\nChat export (date | from | to | message):\n2026-08-02 | Kofi | group | Fingers crossed I can return the rented camera gear by Tuesday, 4 August 2026.\n2026-08-03 | Kofi | Kai | As long as the influencer call is on, I'll return the rented camera gear by Saturday, 8 August 2026.\n2026-08-06 | Kai | group | Just so you know, the influencer call is on as scheduled.\n2026-08-08 | Femi | Kofi | You can bet I'll draft the press release by Tuesday, 11 August 2026.\n2026-08-08 | Kofi | Femi | Forget it, you won't need to draft the press release\n2026-08-08 | Kofi | Kai | To note: I have managed to return the rented camera gear",
  "question": "Was Kofi's promise to return the rented camera gear not kept as of Saturday, 8 August 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc3d2665d9c",
  "kind": "yes/no",
  "text": "We have been planning the garden makeover here, shared by Ana.\n\nMembers: Ana, Malik, Bruno, Hana\nChat export (date | from | to | message):\n2026-07-22 | Hana | Malik | See if I can fetch the paint samples by 28 July 2026.\n2026-07-23 | Hana | Bruno | I'll fetch the paint samples by 31 July 2026 as long as the mortgage valuation visit is on.\n2026-07-25 | Ana | Bruno | Count on me, I'll hang the new curtain rail by 3 August 2026.\n2026-07-26 | Hana | Ana | I will pay the plumbing invoice by 4 August 2026.\n2026-07-28 | Malik | group | Update: the mortgage valuation visit is going ahead as planned.\n2026-08-02 | Hana | Ana | I regret to say that I shall not pay the plumbing invoice.",
  "question": "Has Hana broken the promise to fetch the paint samples at the end of 4 August 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qcef0e8ea81",
  "kind": "yes/no",
  "text": "Committee chat on the ground upgrade, shared by Wren with the volunteers.\n\nMembers: Arlo, Wren, Omar\nChat log (oldest first):\n[17 Jul 2026] Wren: @Arlo Count on me, I'll mark the pitch lines by 20 July 2026.\n[18 Jul 2026] Arlo: @Wren I'll pump the match balls by 20 July 2026 if the training camp goes ahead.\n[19 Jul 2026] Arlo: Sadly, the training camp is not going ahead.\n[19 Jul 2026] Omar: @Wren I will collect the referee whistles by 23 July 2026.\n[19 Jul 2026] Omar: @Wren To note: I have managed to collect the referee whistles\n[25 Jul 2026] Wren: Update on your plan to collect the referee whistles?",
  "question": "Is Omar's promise to collect the referee whistles kept on 24 July 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0650a1aa49",
  "kind": "yes/no",
  "text": "We have been planning the home adaptations here, shared by Zara.\n\nMembers: Ines, Rhea, Zara\nChat log (oldest first):\n[12 Jan 2026] Ines: @Zara I'll print the care schedule by 19 Jan 2026 if the family care meeting goes ahead.\n[12 Jan 2026] Zara: Brilliant news everyone, the family care meeting is a go!\n[12 Jan 2026] Ines: @Rhea I'll fetch the mobility aids by 17 Jan 2026, promise.\n[15 Jan 2026] Ines: @Rhea Mum, I did fetch the mobility aids, haha.\n[17 Jan 2026] Rhea: @Ines Absolutely, I will book the clinic transport by 24 Jan 2026.\n[18 Jan 2026] Zara: @Rhea Lovely, I'll return the hospital bed by 24 Jan 2026 if the physio session is on.",
  "question": "Under the rules on the card, is it true that Ines has not kept the promise to fetch the mobility aids as of 20 Jan 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
