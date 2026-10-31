# G5-H blind read T32-blind_read-3fdc34ff-000 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root9/T32/qc/g5h/answers/T32-blind_read-3fdc34ff-000.json

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
  "qid": "q7fdd39c580",
  "kind": "yes/no",
  "text": "{\"saved_copy_of\": \"group chat\", \"subject\": \"the peer review\", \"saver\": \"Ana\", \"format\": \"plain text\"}\n\nMembers: Arlo, Ana, Yuki, Lena\nChat log (oldest first):\n[1 Jul 2026] Arlo: @Lena Count on me to print the poster abstracts by 8 July 2026 if the safety inspection is on.\n[2 Jul 2026] Ana: Update: the safety inspection is going ahead as planned.\n[6 Jul 2026] Yuki: @Arlo Count on me, I'll book the microscope slot by 11 July 2026.\n[6 Jul 2026] Lena: @Yuki I will fetch the grant forms by 8 July 2026 only if the journal club happens.\n[6 Jul 2026] Lena: @Yuki Guaranteed I'll send the ethics form by 9 July 2026.\n[11 Jul 2026] Yuki: @Arlo Guess who managed to book the microscope slot, go team!",
  "question": "Applying the card's rules, can it be said that Yuki has not kept the promise to book the microscope slot at the end of 13 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q57425a7933",
  "kind": "yes/no",
  "text": "Sami forwarded this for the committee as we dig in on the school fundraiser.\n\nMembers: Bruno, Hana, Sami, Rhea\nChat export (date | from | to | message):\n2026-07-14 | Sami | Bruno | Count on me to print the raffle tickets by 2026-07-21.\n2026-07-15 | Sami | Bruno | Might I ask whether I could print the raffle tickets by 2026-07-24 instead?\n2026-07-16 | Bruno | Hana | I'll set up the book stall by 2026-07-18 as long as the governors meeting is on.\n2026-07-19 | Sami | Bruno | As long as the summer fete is on, I will count the donation boxes by 2026-07-25.\n2026-07-21 | Sami | Bruno | Log entry: print the raffle tickets, carried out",
  "question": "Per the card's rules, on 2026-07-21, has Sami's promise to print the raffle tickets been kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q16d6a2f7ac",
  "kind": "choice",
  "text": "Attached chat: the honeymoon album\nForwarded by: Oskar\n\nMembers: Tess, Dara, Oskar\nChat log (oldest first):\n[28 Jul 2026] Tess: @Dara Count on me to fetch the spare memory cards by 6 Aug 2026.\n[29 Jul 2026] Tess: Aiming to return the lighting stands by 4 Aug 2026, we'll see.\n[31 Jul 2026] Tess: @Oskar As long as the venue visit is on, I'll return the lighting stands by 5 Aug 2026.\n[31 Jul 2026] Dara: Update: the venue visit is going ahead as planned.\n[31 Jul 2026] Tess: @Dara Quick report: I've managed to fetch the spare memory cards\n[2 Aug 2026] Tess: @Oskar Ta-da, I went and did it: return the lighting stands!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Tess's promise to return the lighting stands at the end of 3 Aug 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Kept",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "qc1adf24b6b",
  "kind": "yes/no",
  "text": "Shared with the club committee by Priya, the chat about the kit sponsorship.\n\nMembers: Bruno, Priya\nChat log (oldest first):\n[10 Mar 2026] Priya: @Bruno Count on me to return the bib sets by 13 March 2026.\n[11 Mar 2026] Priya: @Bruno I'll set up the corner flags by 18 March 2026 if the youth trial goes ahead.\n[12 Mar 2026] Priya: @Bruno Absolutely, I will mark the pitch lines by 15 March 2026.\n[15 Mar 2026] Priya: @Bruno I'll print the team sheets by 23 March 2026 as long as the training camp is on.\n[15 Mar 2026] Priya: @Bruno Got myself to mark the pitch lines lol.",
  "question": "Is the promise Priya made to mark the pitch lines not kept by 19 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd2751b84c9",
  "kind": "choice",
  "text": "Forwarded by Ravi: a help-desk thread covering the home adaptations.\n\nMembers: Ivo, Arlo, Kai, Ravi\nChat log (oldest first):\n[14 Feb 2026] Ravi: @Ivo Committing to set up the medicine dispenser by 21 Feb 2026.\n[16 Feb 2026] Kai: @Arlo I'll be sure to drop off the hot meals by 20 Feb 2026.\n[19 Feb 2026] Arlo: @Ivo I will collect the post by 22 Feb 2026 only if the physio session happens.\n[19 Feb 2026] Kai: On track for the physio session to happen as planned.\n[20 Feb 2026] Kai: @Arlo Gutted to say I won't drop off the hot meals, sorry team",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Kai's commitment to drop off the hot meals have at the end of 22 Feb 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qca4f0edc95",
  "kind": "yes/no",
  "text": "{\"archive\": \"group chat\", \"subject\": \"the kit sponsorship\", \"sent_by\": \"Arlo\"}\n\nMembers: Arlo, Elif\nChat log (oldest first):\n[24 Jun 2026] Elif: @Arlo I will make sure to mark the pitch lines by 29 June 2026.\n[25 Jun 2026] Elif: @Arlo Lovely, I'll book the changing room by 3 July 2026 if the youth trial is on.\n[26 Jun 2026] Elif: @Arlo Ticket's mine, I'll print the team sheets by 3 July 2026.\n[27 Jun 2026] Elif: Yay, the youth trial is all set to go!\n[30 Jun 2026] Elif: @Arlo Log entry: mark the pitch lines, carried out",
  "question": "Was the promise to mark the pitch lines from Elif kept on 3 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q53b1b4e5c0",
  "kind": "yes/no",
  "text": "Plain copy of a family thread on the home adaptations, passed on by Bruno.\n\nMembers: Ravi, Jonas, Bruno, Mo\nChat log (oldest first):\n[14 Mar 2026] Jonas: @Ravi Might be able to print the care schedule by 2026-03-19, who knows!\n[16 Mar 2026] Jonas: @Bruno Provided the home assessment happens, I will print the care schedule by 2026-03-22.\n[17 Mar 2026] Ravi: Please note the home assessment will proceed.\n[20 Mar 2026] Jonas: @Bruno Mate, I promised, may I print the care schedule by 2026-03-27 instead?\n[21 Mar 2026] Bruno: @Jonas No change, you need to print the care schedule by the original date.\n[22 Mar 2026] Ravi: @Mo It's on me to collect the post by 2026-03-26.",
  "question": "Is the promise Jonas made to print the care schedule not kept by 2026-03-22?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1f032dabbe",
  "kind": "yes/no",
  "text": "Exported by Sami, this is the back and forth on the wedding weekend.\n\nMembers: Elif, Mo, Sami\nChat log (oldest first):\n[13 Jul 2026] Mo: @Elif Relax, I'll collect the venue floor plan by July 17, 2026, promise.\n[15 Jul 2026] Sami: @Elif I'll set up the backdrop frame by July 21, 2026, providing the engagement shoot goes ahead.\n[15 Jul 2026] Mo: @Sami Relax, I'll print the seating cards by July 19, 2026, promise.\n[19 Jul 2026] Mo: Team, the engagement shoot stays on as booked.\n[22 Jul 2026] Sami: @Elif Mum, I did set up the backdrop frame, haha.",
  "question": "Has Sami kept the promise to set up the backdrop frame at the end of July 21, 2026, instead of broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q29788e35be",
  "kind": "choice",
  "text": "Subject: chat export on the school fundraiser\nThe full chat follows, saved by Jonas, for you to read.\n\nMembers: Wren, Jonas, Ivo, Femi\nChat export (date | from | to | message):\n2026-06-26 | Femi | Ivo | Provided the quiz night happens, I will return the borrowed trestle tables by 3 Jul 2026.\n2026-06-29 | Jonas | Ivo | Relax, I'll collect the bake sale tins by 5 Jul 2026 for sure.\n2026-06-30 | Jonas | Ivo | Count on me to fetch the tea urn by 6 Jul 2026.\n2026-06-30 | Jonas | Ivo | Scratch that, I'm not going to collect the bake sale tins\n2026-07-02 | Ivo | group | Update: the quiz night is going ahead as planned.\n2026-07-03 | Jonas | Ivo | Mate, I promised, may I fetch the tea urn by 11 Jul 2026 instead?\n2026-07-05 | Ivo | Jonas | That suits me, so please fetch the tea urn by 11 Jul 2026 instead.\n\nSummary feature: Generated automatically from this chat, every promise in it counts as fine for Jonas.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 12 Jul 2026, by what date does Jonas have to fetch the tea urn, counting any agreed change of date?",
  "options": [
   "11 Jul 2026",
   "6 Jul 2026",
   "5 Jul 2026"
  ]
 },
 {
  "qid": "q46101d1655",
  "kind": "choice",
  "text": "Rhea shared this back and forth with the client about the payment setup.\n\nMembers: Ravi, Rhea, Bruno, Nadia\nChat log (oldest first):\n[7 Apr 2026] Nadia: @Rhea Provided the stock count happens, I will test the mobile layout by 13 Apr 2026.\n[8 Apr 2026] Nadia: @Ravi Ticket's mine, I'll update the product photos by 15 Apr 2026.\n[9 Apr 2026] Rhea: @Nadia I'll set up the email forwarding by 14 Apr 2026 as long as the market day is on.\n[10 Apr 2026] Rhea: @Nadia Ah, no stress, no need for you to update the product photos\n[12 Apr 2026] Nadia: @Ravi Mum, I did update the product photos, haha.\n[12 Apr 2026] Bruno: @Nadia As long as the product photo day is on, I'll print the packing slips by 14 Apr 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Nadia's promise to update the product photos at the end of 14 Apr 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "qe2f940ce38",
  "kind": "yes/no",
  "text": "Client chat in a freelance log: the documentary cut, passed on by Leila.\n\nMembers: Lena, Kai, Leila, Rhea\nChat export (date | from | to | message):\n2026-05-14 | Leila | Lena | Relax, I'll record the voice over by 18 May 2026 for sure.\n2026-05-14 | Rhea | Leila | I assure you I'll export the subtitle files by 22 May 2026 if the festival premiere is on.\n2026-05-15 | Leila | Lena | On my action item, may I record the voice over by 23 May 2026 instead?\n2026-05-17 | Lena | Leila | Nah, the date's staying put, so you can record the voice over.\n2026-05-17 | Leila | Lena | Quick report: I've managed to record the voice over\n2026-05-17 | Lena | Leila | If the shoot day goes ahead, I'll gladly ship the hard drive by 24 May 2026.",
  "question": "Does the card classify Leila's promise to record the voice over as broken, waived, not triggered or not yet due, rather than kept, on 18 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q06341aaa89",
  "kind": "yes/no",
  "text": "Saved by Kofi, this copy of the support chat concerns the big house plan.\n\nMembers: Kofi, Femi\nChat log (oldest first):\n[18 Feb 2026] Kofi: @Femi I'll bleed the attic radiators by 22 Feb 2026 as long as the loft clearance day is on.\n[18 Feb 2026] Femi: We are dropping the loft clearance day from the list.\n[19 Feb 2026] Kofi: @Femi Think 24 Feb 2026 would work if I bleed the attic radiators instead?\n[21 Feb 2026] Femi: @Kofi Lovely, I'll defrost the old fridge by 25 Feb 2026 for sure.\n[22 Feb 2026] Femi: @Kofi The original date stands, so you need to bleed the attic radiators.",
  "question": "Going by the card's rules, does Kofi not keep the promise to bleed the attic radiators at the end of 24 Feb 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbb32f4214e",
  "kind": "yes/no",
  "text": "Neighbour and flatmate talk, copied out by Ravi: the balcony garden project.\n\nMembers: Tomas, Arlo, Ravi, Sami\nChat log (oldest first):\n[12 Jan 2026] Arlo: See if I can email the leak photos by 24 Jan 2026, no certainty.\n[13 Jan 2026] Arlo: @Ravi Count on me to email the leak photos by 21 Jan 2026, if the flat viewing day happens.\n[18 Jan 2026] Tomas: @Arlo I will make sure to measure the kitchen for fridge by 22 Jan 2026.\n[20 Jan 2026] Tomas: Brilliant news everyone, the flat viewing day is a go!\n[21 Jan 2026] Arlo: @Ravi Mate, I promised, may I email the leak photos by 23 Jan 2026 instead?\n[21 Jan 2026] Ravi: @Arlo No new date, so please email the leak photos by the date given.",
  "question": "When you check the chat at the end of 21 Jan 2026, is the promise Arlo made to email the leak photos broken?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qabe3563ffe",
  "kind": "yes/no",
  "text": "{\"chat_export\": \"the gallery show\", \"saved_by\": \"Yuki\", \"scope\": \"group chat\"}\n\nMembers: Wren, Yuki\nChat log (oldest first):\n[27 Jun 2026] Wren: @Yuki Relax, I'll send the moodboard files by July 3, 2026, promise.\n[29 Jun 2026] Yuki: @Wren I'll pick the colour swatches by July 6, 2026 as long as the brand review call is on.\n[30 Jun 2026] Wren: Checking you mean to pick the colour swatches?\n[2 Jul 2026] Yuki: @Wren I will check the poster proofs by July 7, 2026.\n[2 Jul 2026] Wren: Please note the brand review call will proceed.\n[7 Jul 2026] Yuki: @Wren Change of plans: I will not check the poster proofs",
  "question": "Is the promise Yuki made to pick the colour swatches not kept by July 4, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qdf9c861751",
  "kind": "yes/no",
  "text": "{\"thread_kind\": \"exported conversation\", \"about\": \"the guest welcome plan\", \"exported_by\": \"Rhea\"}\n\nMembers: Lena, Kai, Rhea\nChat log (oldest first):\n[3 Oct 2026] Rhea: @Kai I'll collect the bed linen by Monday, October 12, 2026 if the guest arrival evening goes ahead.\n[4 Oct 2026] Kai: @Lena Committing to scrub the hot tub by Sunday, October 11, 2026.\n[5 Oct 2026] Kai: @Lena Ticked off my list: scrub the hot tub, yay.\n[6 Oct 2026] Kai: Update, the guest arrival evening will not take place.\n[8 Oct 2026] Lena: @Rhea I own this, I'll wheel the bins out by Saturday, October 17, 2026.\n[9 Oct 2026] Rhea: Hey, did you get a chance to scrub the hot tub?",
  "question": "Is the promise Kai made to scrub the hot tub in a status other than broken at the end of Wednesday, October 7, 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2d7dc6fbb2",
  "kind": "yes/no",
  "text": "Subject: chat export on the cellar project\nThe full chat follows, saved by Femi, for you to read.\n\nMembers: Ines, Femi, Jonas, Greta\nChat log (oldest first):\n[17 Oct 2026] Jonas: @Ines Hoping to replace the hallway bulbs by 29 Oct 2026, can't promise.\n[19 Oct 2026] Jonas: @Greta Got it, I'll replace the hallway bulbs by 25 Oct 2026 for sure.\n[21 Oct 2026] Jonas: @Ines Lovely, I'll oil the back door hinges by 26 Oct 2026 if the chimney sweep visit is on.\n[21 Oct 2026] Jonas: @Femi Count on me to clear the kitchen sink by 31 Oct 2026 if the roof survey visit is on.\n[25 Oct 2026] Jonas: @Greta Think 30 Oct 2026 would work if I replace the hallway bulbs instead?\n[26 Oct 2026] Jonas: @Greta Ticked off my list: replace the hallway bulbs, yay.",
  "question": "Is Jonas's promise to replace the hallway bulbs kept on 25 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb03d89982e",
  "kind": "choice",
  "text": "Freelance log for the store makeover\nSaved by Hana from the client thread.\n\nMembers: Hana, Wren\nChat log (oldest first):\n[18 May 2026] Wren: @Hana I will sketch the packaging mockup by Monday, May 25, 2026 only if the packaging launch happens.\n[18 May 2026] Hana: Fab, we are on for the packaging launch as planned!\n[18 May 2026] Hana: @Wren Provided the sign reveal happens, I will send the moodboard files by Wednesday, May 27, 2026.\n[19 May 2026] Hana: @Wren Got it, I'll pick the colour swatches by Monday, May 25, 2026 for sure.\n[19 May 2026] Hana: @Wren Absolutely, I will update the icon set by Tuesday, May 26, 2026.\n[25 May 2026] Wren: @Hana Good news, you're let off having to update the icon set",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Hana made to update the icon set at the end of Monday, May 25, 2026?",
  "options": [
   "Kept",
   "Broken",
   "Waived",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q27bf65c13e",
  "kind": "choice",
  "text": "Shared by Lena, this work thread covers the staff handbook.\n\nMembers: Lena, Elif, Greta\nChat log (oldest first):\n[16 Jun 2026] Lena: @Greta I promise to renew the fire extinguisher service by 21 Jun 2026 if the staff picnic is on.\n[19 Jun 2026] Elif: Update: the staff picnic is going ahead as planned.\n[19 Jun 2026] Greta: @Lena I'll collect the visitor badges by 28 Jun 2026, promise.\n[21 Jun 2026] Greta: @Lena Ah, no stress, no need for you to renew the fire extinguisher service\n[28 Jun 2026] Greta: @Lena Quick question, could I collect the visitor badges by 1 Jul 2026 instead?\n[28 Jun 2026] Lena: @Greta Aw no, you need to collect the visitor badges by the original date!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Lena made to renew the fire extinguisher service is in which status at the end of 21 Jun 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "qf0f30e6b5b",
  "kind": "yes/no",
  "text": "Household group messages for the trip itinerary were passed along by Greta.\n\nMembers: Wren, Arlo, Ivo, Greta\nChat export (date | from | to | message):\n2026-02-28 | Arlo | Wren | I'll check the passport copies by 4 March 2026, providing the ferry crossing goes ahead.\n2026-03-02 | Arlo | Greta | If the hotel arrival is on, I'll definitely buy the packing cubes by 5 March 2026.\n2026-03-02 | Wren | Greta | Committing to pack the travel adaptors by 6 March 2026.\n2026-03-04 | Arlo | group | Yep, the hotel arrival is on as planned.\n2026-03-04 | Wren | Arlo | Good news, you're let off having to buy the packing cubes\n2026-03-06 | Arlo | Wren | Nobody needs you to pack the travel adaptors, that's that",
  "question": "Is Arlo's promise to buy the packing cubes broken at the end of 5 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4180b861c4",
  "kind": "yes/no",
  "text": "Team channel export, shared by Priya, which is about the grant renewal.\n\nMembers: Nadia, Greta, Ravi, Priya\nChat log (oldest first):\n[20 Jan 2026] Priya: @Nadia Committing to order the reagent kit by Sunday, January 25, 2026.\n[20 Jan 2026] Nadia: Thanks, got it.\n[20 Jan 2026] Ravi: @Greta As long as the thesis defence is on, I will send the ethics form by Tuesday, January 27, 2026.\n[21 Jan 2026] Priya: @Nadia I assure you I'll return the library books by Saturday, January 24, 2026 if the seminar series is on.\n[22 Jan 2026] Greta: @Priya You don't have to order the reagent kit at all\n[23 Jan 2026] Ravi: @Priya I own this, I'll fetch the grant forms by Friday, January 30, 2026.",
  "question": "Going by the card's rules, does Priya keep the promise to order the reagent kit at the end of Friday, January 23, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd24f2e27fa",
  "kind": "choice",
  "text": "Saved by Ana, this copy of the support chat concerns the onboarding flow.\n\nMembers: Zara, Ana, Nadia, Priya\nChat log (oldest first):\n[15 Jul 2026] Priya: @Ana You can bet I'll label the bug reports by 22 July 2026.\n[18 Jul 2026] Nadia: @Priya Quick update: you do not need to label the bug reports at all.\n[18 Jul 2026] Priya: @Nadia Provided the sprint demo happens, I'll deploy the staging build by 24 July 2026.\n[20 Jul 2026] Nadia: @Ana I'll fix the test runner by 27 July 2026 as long as the hackathon is on.\n[20 Jul 2026] Nadia: Sadly, the sprint demo is not going ahead.\n[21 Jul 2026] Priya: @Ana To note: I have managed to label the bug reports",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Priya doing with the promise to label the bug reports at the end of 25 July 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q12f1ee69ab",
  "kind": "choice",
  "text": "Rhea shared this back and forth with the client about the payment setup.\n\nMembers: Ravi, Rhea, Bruno, Nadia\nChat log (oldest first):\n[7 Apr 2026] Nadia: @Rhea Provided the stock count happens, I will test the mobile layout by 13 Apr 2026.\n[8 Apr 2026] Nadia: @Ravi Ticket's mine, I'll update the product photos by 15 Apr 2026.\n[9 Apr 2026] Rhea: @Nadia I'll set up the email forwarding by 14 Apr 2026 as long as the market day is on.\n[10 Apr 2026] Rhea: @Nadia Ah, no stress, no need for you to update the product photos\n[12 Apr 2026] Nadia: @Ravi Mum, I did update the product photos, haha.\n[12 Apr 2026] Bruno: @Nadia As long as the product photo day is on, I'll print the packing slips by 14 Apr 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Nadia's promise to update the product photos at the end of 14 Apr 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "qd752298032",
  "kind": "yes/no",
  "text": "Committee chat on the volunteer roster, forwarded by Jonas to the volunteers.\n\nMembers: Oskar, Greta, Lena, Jonas\nChat export (date | from | to | message):\n2026-07-15 | Greta | Lena | Not promising, but I'll try to collect the bake sale tins by 21 July 2026.\n2026-07-16 | Greta | Jonas | Count on me, I'll collect the bake sale tins by 22 July 2026.\n2026-07-19 | Oskar | Lena | If the quiz night goes ahead, I'll set up the book stall by 26 July 2026.\n2026-07-20 | Lena | Greta | Nobody needs you to collect the bake sale tins, that's that\n2026-07-21 | Jonas | group | Fab, we are on for the quiz night as planned!\n2026-07-22 | Greta | Jonas | Got myself to collect the bake sale tins lol.",
  "question": "Was the promise to collect the bake sale tins from Greta kept on 22 July 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q10fde35f8b",
  "kind": "yes/no",
  "text": "Work team channel\nSaved by Wren, which talks about the field survey.\n\nMembers: Wren, Jonas, Elif, Femi\nChat log (oldest first):\n[21 Jul 2026] Femi: @Elif If the safety inspection goes ahead, I'll gladly book the microscope slot by 24 Jul 2026.\n[23 Jul 2026] Femi: Sadly, the safety inspection is not going ahead.\n[24 Jul 2026] Elif: @Jonas I'll be sure to scan the field notes by 1 Aug 2026.\n[25 Jul 2026] Elif: @Femi Guaranteed I'll return the library books by 2 Aug 2026.\n[28 Jul 2026] Elif: @Jonas Only if the journal club is on, I will print the poster abstracts by 6 Aug 2026.\n[31 Jul 2026] Wren: @Elif Relax, mate, you're not expected to scan the field notes",
  "question": "Applying the card's rules, can it be said that Elif has not kept the promise to scan the field notes at the end of 2 Aug 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9ba5ee855e",
  "kind": "choice",
  "text": "Subject: Chat about the packing plan\nA plain copy from Zara follows, exactly as exported.\n\nMembers: Greta, Zara, Ines, Dara\nChat log (oldest first):\n[9 Jun 2026] Ines: @Zara Committing to book the airport parking by 18 June 2026.\n[11 Jun 2026] Greta: @Zara Count on me to fetch the sunscreen by 16 June 2026 if the guided tour is on.\n[14 Jun 2026] Greta: @Zara Guaranteed I'll collect the insurance papers by 21 June 2026.\n[14 Jun 2026] Greta: Fab, we are on for the guided tour as planned!\n[16 Jun 2026] Greta: @Zara Guess what, I managed to fetch the sunscreen!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 18 June 2026, what status has Greta's promise to fetch the sunscreen got?",
  "options": [
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qd13bf58036",
  "kind": "yes/no",
  "text": "Our flat chat about the tenancy renewal talks, saved by Dara for whoever lives here.\n\nMembers: Dara, Malik\nChat log (oldest first):\n[1 Mar 2026] Malik: No promises, but I'll aim to remove the bathroom shelf by 3 Mar 2026.\n[2 Mar 2026] Malik: @Dara As long as the electrics safety check is on, I'll remove the bathroom shelf by 9 Mar 2026.\n[3 Mar 2026] Malik: @Dara Relax, I'll read the meter readings by 6 Mar 2026, promise.\n[5 Mar 2026] Dara: @Malik Forget it, you won't need to read the meter readings\n[8 Mar 2026] Malik: On track for the electrics safety check to happen as planned.\n[12 Mar 2026] Malik: @Dara Ta-da, I went and did it: remove the bathroom shelf!",
  "question": "At the end of 11 Mar 2026, has Malik broken its promise to remove the bathroom shelf?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q96f817df03",
  "kind": "choice",
  "text": "Kai shared this channel export covering the social media plan for the team.\n\nMembers: Elif, Kai, Ravi\nChat export (date | from | to | message):\n2026-07-31 | Kai | Ravi | If the webinar rehearsal goes ahead, I'll draft the press release by 9 Aug 2026.\n2026-08-01 | Elif | Ravi | I will make sure to collect the survey answers by 4 Aug 2026.\n2026-08-01 | Ravi | group | Appreciate you telling me.\n2026-08-01 | Ravi | Elif | Don't sweat it, there's no need to collect the survey answers\n2026-08-02 | Kai | group | Yep, the webinar rehearsal is on as planned.\n2026-08-06 | Kai | Ravi | It's on me to set up the analytics dashboard by 13 Aug 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Elif's commitment to collect the survey answers at the end of 1 Aug 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Kept",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "qc27f65813f",
  "kind": "choice",
  "text": "Saved by Sami, this is the household group chat about the trip itinerary, copied in full.\n\nMembers: Bruno, Kofi, Sami, Lee\nChat export (date | from | to | message):\n2026-02-10 | Bruno | Lee | Lovely, I'll fetch the sunscreen by 17 February 2026 if the beach picnic is on.\n2026-02-10 | Lee | group | Fab, we are on for the beach picnic as planned!\n2026-02-13 | Kofi | Sami | You can bet I'll check the passport copies by 18 February 2026.\n2026-02-17 | Kofi | Sami | Got myself to check the passport copies lol.\n2026-02-18 | Bruno | Lee | Guess what, I managed to fetch the sunscreen!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Bruno's promise to fetch the sunscreen at the end of 17 February 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Not yet due",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "qbc9f5e4f55",
  "kind": "yes/no",
  "text": "Subject: copy of a chat on the lab move\nPassing this along, with the chat text under it, from Nadia.\n\nMembers: Dara, Nadia, Leila\nChat log (oldest first):\n[1 Nov 2026] Leila: Hoping to order the reagent kit by 6 November 2026, but can't promise.\n[1 Nov 2026] Nadia: @Dara Got it, I'll book the microscope slot by 8 November 2026 for sure.\n[3 Nov 2026] Leila: @Nadia If the journal club goes ahead, I'll order the reagent kit by 9 November 2026.\n[3 Nov 2026] Nadia: @Dara Change of plans: I will not book the microscope slot\n[5 Nov 2026] Leila: Fab, we are on for the journal club as planned!\n[5 Nov 2026] Leila: @Nadia Update on my side: I will not order the reagent kit, sorry.",
  "question": "According to the rules on the card, does the promise Leila made to order the reagent kit have any status except broken at the end of 7 November 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q85599997bb",
  "kind": "yes/no",
  "text": "Shared by Leila, a help-desk thread covering the new term plans.\n\nMembers: Leila, Lee, Tomas\nChat export (date | from | to | message):\n2026-01-24 | Leila | Tomas | Promise to collect the bake sale tins by 29 January 2026 if the reading festival goes ahead.\n2026-01-24 | Lee | Tomas | I'll try to count the donation boxes by 28 January 2026, can't promise!\n2026-01-25 | Lee | Tomas | It's on me to count the donation boxes by 30 January 2026.\n2026-01-26 | Tomas | group | Sadly, the reading festival won't go ahead.\n2026-01-30 | Lee | Tomas | I'll be sure to set up the book stall by 6 February 2026.\n2026-01-31 | Lee | Tomas | Ticked off my list: count the donation boxes, yay.",
  "question": "On 1 February 2026 itself, has Lee not kept the promise to count the donation boxes?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1a1359ece6",
  "kind": "choice",
  "text": "Chat channel log:\nWork messages about the trade show push, exported by Bruno.\n\nMembers: Tomas, Greta, Dara, Bruno\nChat export (date | from | to | message):\n2026-04-18 | Tomas | Dara | I'll set up the analytics dashboard by Tuesday, April 21, 2026, provided the trade fair stand happens.\n2026-04-18 | Greta | group | Update: the trade fair stand is going ahead as planned.\n2026-04-20 | Bruno | Dara | Ticket's mine, I'll collect the survey answers by Sunday, April 26, 2026.\n2026-04-25 | Greta | Bruno | Count on me to return the rented camera gear by Wednesday, April 29, 2026.\n2026-04-26 | Tomas | Bruno | Good news, you're let off having to collect the survey answers",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status does the chat show for the promise Bruno made to collect the survey answers at the end of Sunday, April 26, 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "qa88f168cf2",
  "kind": "yes/no",
  "text": "Here's the club committee's chat, saved by Kofi, about the sponsor search.\n\nMembers: Kofi, Oskar, Bruno, Kai\nChat export (date | from | to | message):\n2026-03-08 | Kofi | Kai | I'll set up the feed stop by 15 Mar 2026, promise.\n2026-03-09 | Kai | Kofi | Provided the mechanics clinic happens, I'll wash the club jerseys by 16 Mar 2026.\n2026-03-11 | Oskar | Kofi | Forget it, you won't need to set up the feed stop\n2026-03-13 | Bruno | group | Please note the mechanics clinic will proceed.\n2026-03-14 | Kofi | Kai | Ah, no stress, no need for you to wash the club jerseys",
  "question": "Is Kai's promise to wash the club jerseys kept as of 18 Mar 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q588081d4a9",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the social media plan\nThis export came from Bruno and is pasted in full below.\n\nMembers: Bruno, Priya, Hana\nChat export (date | from | to | message):\n2026-02-06 | Bruno | Priya | As long as the webinar rehearsal is on, I'll fetch the campaign budget sheet by Monday, 9 February 2026.\n2026-02-10 | Bruno | Hana | Relax, I'll set up the analytics dashboard by Tuesday, 17 February 2026 for sure.\n2026-02-10 | Bruno | Hana | Mate, I promised, may I set up the analytics dashboard by Sunday, 22 February 2026 instead?\n2026-02-10 | Hana | Priya | Promise to fix the landing page headline by Wednesday, 18 February 2026 if the annual review goes ahead.\n2026-02-15 | Hana | Bruno | No, I'd like you to set up the analytics dashboard by the original date.\n2026-02-15 | Priya | group | Fab, we are on for the annual review as planned!",
  "question": "Has Hana kept the promise to fix the landing page headline at the end of Monday, 16 February 2026, instead of broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbd44c791af",
  "kind": "yes/no",
  "text": "Shared with the club committee by Mo, the chat about the school fundraiser.\n\nMembers: Sami, Arlo, Mo\nChat export (date | from | to | message):\n2026-08-09 | Sami | Arlo | I'll collect the bake sale tins by 11 August 2026 if the summer fete goes ahead.\n2026-08-12 | Sami | Mo | Guaranteed I'll set up the book stall by 18 August 2026.\n2026-08-12 | Arlo | Sami | No worries, you don't need to set up the book stall\n2026-08-12 | Sami | Mo | For the record: I was able to set up the book stall\n2026-08-17 | Arlo | Mo | Lovely, I'll count the donation boxes by 24 August 2026 if the quiz night is on.\n2026-08-17 | Arlo | Sami | Lovely, I'll wrap the prize hampers by 20 August 2026 for sure.",
  "question": "At the end of 12 August 2026, is Sami's promise to set up the book stall broken, waived, not triggered or not yet due, rather than kept?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q554724d311",
  "kind": "choice",
  "text": "{\"thread\": \"the new kit design\", \"exported_by\": \"Lee\", \"shape\": \"group chat\"}\n\nMembers: Lee, Leila, Ravi, Kofi\nChat log (oldest first):\n[30 Aug 2026] Ravi: @Leila You can bet I'll tune the gear cables by 6 September 2026.\n[3 Sep 2026] Lee: @Leila I assure you I'll set up the feed stop by 10 September 2026 if the club sportive is on.\n[5 Sep 2026] Ravi: @Kofi I own this, I'll service the tandem bike by 8 September 2026.\n[5 Sep 2026] Ravi: Lovely, the club sportive is definitely happening!\n[6 Sep 2026] Lee: @Leila Might I ask whether I could set up the feed stop by 13 September 2026 instead?\n[7 Sep 2026] Ravi: @Kofi I'll return the loaned helmets by 9 September 2026, promise.\n[9 Sep 2026] Kofi: @Lee Yes, you can set up the feed stop by 13 September 2026 if that suits you.\n[12 Sep 2026] Lee: @Leila I'm withdrawing my promise to set up the feed stop",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules, when is the date by which Lee has to set up the feed stop at the end of 11 September 2026, allowing for any agreed change?",
  "options": [
   "13 September 2026",
   "10 September 2026",
   "8 September 2026"
  ]
 },
 {
  "qid": "q0fde3c3c1b",
  "kind": "yes/no",
  "text": "Ana forwarded this for the committee, covering the playground project.\n\nMembers: Elif, Omar, Ana, Ravi\nChat export (date | from | to | message):\n2026-08-18 | Ravi | Omar | I will count the donation boxes by Saturday, August 22, 2026 only if the field day happens.\n2026-08-19 | Elif | Ravi | I own this, I'll print the raffle tickets by Friday, August 28, 2026.\n2026-08-20 | Elif | Omar | Got it, I'll set up the book stall by Wednesday, August 26, 2026 for sure.\n2026-08-21 | Omar | Ana | Lovely, I'll fetch the tea urn by Saturday, August 29, 2026 if the quiz night is on.\n2026-08-21 | Omar | group | Just so you know, the field day is on as scheduled.\n2026-08-27 | Elif | Omar | Ticked off: set up the book stall, feels so good",
  "question": "Did Elif keep the promise to set up the book stall on Wednesday, August 26, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5a682a9bc0",
  "kind": "choice",
  "text": "Attached chat: the league run\nForwarded by: Wren\n\nMembers: Dara, Tomas, Wren, Ana\nChat log (oldest first):\n[4 Apr 2026] Wren: @Ana If the presentation evening goes ahead, I'll book the changing room by 8 April 2026.\n[8 Apr 2026] Tomas: I'll try to print the team sheets by 15 April 2026, no promises.\n[9 Apr 2026] Tomas: @Ana Lovely, I'll print the team sheets by 14 April 2026 for sure.\n[11 Apr 2026] Ana: @Wren Lovely, I'll return the bib sets by 20 April 2026 if the pre-season friendly is on.\n[11 Apr 2026] Ana: @Tomas No worries, you don't need to print the team sheets\n[15 Apr 2026] Tomas: @Ana Log entry: print the team sheets, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Tomas gave to print the team sheets have at the end of 12 April 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not triggered",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "qd1466371a3",
  "kind": "choice",
  "text": "Saved chat on the house refit. Exported by Lena, unedited, from a household group.\n\nMembers: Leila, Malik, Lena, Ivo\nChat export (date | from | to | message):\n2026-09-21 | Leila | Lena | I'll measure the hallway for shelves by 26 Sep 2026, provided the builder quote meeting happens.\n2026-09-22 | Leila | Ivo | I'll be sure to collect the sanding pads by 27 Sep 2026.\n2026-09-23 | Lena | Leila | No need to collect the sanding pads, I'm letting you off\n2026-09-23 | Leila | Ivo | As long as the kitchen fitting day is on, I will sweep the dust from stairs by 30 Sep 2026.\n2026-09-29 | Leila | Ivo | Ticked off my list: collect the sanding pads, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 27 Sep 2026, what status has Leila's promise to collect the sanding pads got?",
  "options": [
   "Not triggered",
   "Kept",
   "Not yet due",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q663dff185d",
  "kind": "choice",
  "text": "{\"kind\": \"exported group chat\", \"about_topic\": \"the documentary cut\", \"sent_by\": \"Zara\"}\n\nMembers: Zara, Wren, Omar\nChat export (date | from | to | message):\n2026-03-31 | Wren | Zara | Fingers crossed I can fetch the raw footage by 12 Apr 2026.\n2026-04-02 | Wren | Zara | If the shoot day goes ahead, I'll fetch the raw footage by 10 Apr 2026.\n2026-04-02 | Wren | group | Yep, the shoot day is on as planned.\n2026-04-04 | Zara | Omar | You can bank on me to record the voice over by 8 Apr 2026.\n2026-04-04 | Wren | Zara | Think 12 Apr 2026 would work if I fetch the raw footage instead?\n2026-04-11 | Wren | Zara | To note: I have managed to fetch the raw footage",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Wren made to fetch the raw footage at the end of 14 Apr 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "qf207c266ba",
  "kind": "yes/no",
  "text": "Here is the plan for the travel plans, saved by Kai for the group.\n\nMembers: Ana, Kai, Kofi\nChat export (date | from | to | message):\n2026-09-22 | Kai | group | Will attempt to send the packing list by 2026-10-02, can't promise.\n2026-09-23 | Kai | Kofi | If the ferry crossing goes ahead, I'll print the boarding passes by 2026-10-02.\n2026-09-24 | Kai | Ana | I will make sure to send the packing list by 2026-10-01.\n2026-09-24 | Ana | group | Please note the ferry crossing will proceed.\n2026-09-26 | Kai | Ana | I need to take back my commitment to send the packing list.\n2026-10-01 | Ana | Kai | Please don't feel you have to send the packing list",
  "question": "Does the chat, checked at the end of 2026-10-06, show that Kai has broken the promise to send the packing list?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q448f20ccbe",
  "kind": "yes/no",
  "text": "An exported family chat on the house rules debate, saved by Dara, left unchanged.\n\nMembers: Dara, Femi\nChat log (oldest first):\n[25 Jun 2026] Dara: @Femi As long as the house viewing is on, I will oil the back door hinges by 27 June 2026.\n[25 Jun 2026] Femi: @Dara Absolutely, I will scrub the cellar steps by 30 June 2026.\n[28 Jun 2026] Dara: @Femi I assure you I'll clear the kitchen sink by 4 July 2026 if the ghost tour is on.\n[3 Jul 2026] Femi: Quick heads up, the ghost tour is scrapped.\n[4 Jul 2026] Dara: @Femi Mind giving me until 7 July 2026 to clear the kitchen sink?\n[4 Jul 2026] Femi: @Dara Fine by me, you can clear the kitchen sink by 7 July 2026.",
  "question": "Under the rules on the card, is it true that Dara has not kept the promise to clear the kitchen sink as of 4 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe82b3001b4",
  "kind": "choice",
  "text": "Team export header with the social media plan, saved by Lena.\n\nMembers: Kofi, Lee, Lena, Bruno\nChat export (date | from | to | message):\n2026-06-14 | Lee | Bruno | I will make sure to fetch the campaign budget sheet by Tuesday, 23 June 2026.\n2026-06-14 | Lena | Lee | Lovely, I'll set up the analytics dashboard by Monday, 22 June 2026 for sure.\n2026-06-16 | Lena | Lee | Mind giving me until Thursday, 25 June 2026 to set up the analytics dashboard?\n2026-06-21 | Kofi | Lena | Provided the influencer call happens, I will pay the printing invoice by Tuesday, 23 June 2026.\n2026-06-21 | Kofi | Lee | Count on me to book the photo studio by Wednesday, 24 June 2026 if the product launch is on.\n2026-06-21 | Lee | Lena | Aw no, you need to set up the analytics dashboard by the original date!\n2026-06-25 | Lena | Lee | To my relief, I managed to set up the analytics dashboard.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs things stand at the end of Saturday, 20 June 2026, which date is the deadline for Lena to set up the analytics dashboard, with any agreed change applied?",
  "options": [
   "Monday, 22 June 2026",
   "Tuesday, 23 June 2026",
   "Thursday, 25 June 2026"
  ]
 },
 {
  "qid": "qa3a5d612c0",
  "kind": "choice",
  "text": "Kofi shared this so the family follows the summer getaway.\n\nMembers: Tess, Kofi, Leila\nChat export (date | from | to | message):\n2026-03-24 | Kofi | Tess | Hoping to book the airport parking by 30 Mar 2026, no promises.\n2026-03-26 | Kofi | Tess | Promise to book the airport parking by 31 Mar 2026 if the hotel arrival goes ahead.\n2026-03-29 | Kofi | group | Yep, the hotel arrival is on as planned.\n2026-03-30 | Leila | Tess | Count on me to fetch the sunscreen by 4 Apr 2026.\n2026-03-31 | Kofi | Tess | Got myself to book the airport parking lol.\n2026-04-02 | Kofi | Leila | You are released, no requirement to fetch the sunscreen.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Kofi's promise to book the airport parking at the end of 6 Apr 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q976d71a1ae",
  "kind": "choice",
  "text": "{\"record\": \"shared group chat\", \"subject\": \"the front garden scheme\", \"shared_by\": \"Ravi\", \"stored\": \"as text\"}\n\nMembers: Zara, Ravi, Hana\nChat log (oldest first):\n[16 Jun 2026] Ravi: @Hana Lovely, I'll clear the hedge trimmings by 21 Jun 2026 if the speed camera survey is on.\n[20 Jun 2026] Ravi: @Hana You can bank on me to bring the bins in by 23 Jun 2026.\n[20 Jun 2026] Hana: @Zara Provided the road works meeting happens, I will feed the cat across the road by 25 Jun 2026.\n[23 Jun 2026] Ravi: @Hana Update on my side: I will not bring the bins in, sorry.\n[23 Jun 2026] Hana: @Ravi Forget it, you won't need to bring the bins in",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Ravi doing with the promise to bring the bins in at the end of 23 Jun 2026?",
  "options": [
   "Kept",
   "Broken",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q8bf384e4db",
  "kind": "choice",
  "text": "Work team channel\nSaved by Ines, which talks about the social media plan.\n\nMembers: Ravi, Ines, Malik\nChat export (date | from | to | message):\n2026-08-21 | Ines | Ravi | I'll be sure to set up the analytics dashboard by 27 August 2026.\n2026-08-26 | Ines | Ravi | Fingers crossed I can send the newsletter copy by 3 September 2026.\n2026-08-28 | Ines | Malik | I will send the newsletter copy by 31 August 2026 only if the influencer call happens.\n2026-08-30 | Ines | group | Yay, the influencer call is all set to go!\n2026-08-31 | Ines | Malik | Mind giving me until 2 September 2026 to send the newsletter copy?\n2026-08-31 | Ravi | Ines | Yes, you can send the newsletter copy by 2 September 2026 instead.\n2026-08-31 | Ravi | Ines | Please don't feel you have to send the newsletter copy\n2026-09-02 | Ines | Malik | For the record: I was able to send the newsletter copy",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo what's the latest day Ines has to send the newsletter copy by at the end of 16 September 2026, given any new date people agreed to?",
  "options": [
   "31 August 2026",
   "2 September 2026",
   "27 August 2026"
  ]
 },
 {
  "qid": "q53feec10c5",
  "kind": "yes/no",
  "text": "Attached chat: the student house hunt\nForwarded by: Femi\n\nMembers: Ivo, Femi, Ines, Zara\nChat log (oldest first):\n[28 Oct 2026] Zara: @Ines I will scan the council tax letter by 30 Oct 2026.\n[29 Oct 2026] Zara: @Ines If the agent inventory walk goes ahead, I'll return the bin rota by 6 Nov 2026.\n[29 Oct 2026] Ines: Cheers, noted.\n[29 Oct 2026] Ivo: @Femi Lovely, I'll print the tenancy agreement by 2 Nov 2026 for sure.\n[5 Nov 2026] Ivo: Brilliant news everyone, the agent inventory walk is a go!\n[6 Nov 2026] Zara: @Ines Log entry: return the bin rota, carried out",
  "question": "On 6 Nov 2026 itself, has Zara not kept the promise to return the bin rota?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q88b94c6896",
  "kind": "choice",
  "text": "Written between tenants and a landlord, this copy concerns the summer lets season. It was saved by Kai.\n\nMembers: Leila, Kai, Lena\nChat log (oldest first):\n[14 Jan 2026] Kai: @Lena I'll scrub the hot tub by 17 Jan 2026 as long as the lettings photo shoot is on.\n[14 Jan 2026] Kai: Please note the lettings photo shoot will proceed.\n[14 Jan 2026] Kai: @Lena Would it be fine if I scrub the hot tub by 23 Jan 2026 instead, yeah?\n[16 Jan 2026] Leila: @Lena Relax, I'll change the lounge bulb by 22 Jan 2026 for sure.\n[16 Jan 2026] Leila: @Kai Yes, fine to scrub the hot tub by 23 Jan 2026 instead.\n[22 Jan 2026] Leila: @Lena I'm withdrawing my promise to change the lounge bulb\n[23 Jan 2026] Kai: @Lena Guess what, I managed to scrub the hot tub!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs things stand at the end of 16 Jan 2026, which date is the deadline for Kai to scrub the hot tub, with any agreed change applied?",
  "options": [
   "17 Jan 2026",
   "23 Jan 2026",
   "22 Jan 2026"
  ]
 },
 {
  "qid": "q5687cbe731",
  "kind": "choice",
  "text": "Posted by Zara from the work channel: the desk plan.\n\nMembers: Zara, Arlo, Lee\nChat export (date | from | to | message):\n2026-08-01 | Zara | Arlo | Provided the building survey happens, I will return the printer toner by 2026-08-07.\n2026-08-03 | Lee | Arlo | I'll be sure to order the office stationery by 2026-08-05.\n2026-08-05 | Zara | group | Quick heads up, the building survey is scrapped.\n2026-08-06 | Zara | Arlo | Might I ask whether I could return the printer toner by 2026-08-11 instead?\n2026-08-06 | Lee | Zara | Yes, all good for you to return the printer toner by 2026-08-11 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Zara made to return the printer toner, what state is it in at the end of 2026-08-09?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Broken",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q480cf4fdb5",
  "kind": "yes/no",
  "text": "Saved by Kofi, this copy of the support chat concerns the big house plan.\n\nMembers: Kofi, Femi\nChat log (oldest first):\n[18 Feb 2026] Kofi: @Femi I'll bleed the attic radiators by 22 Feb 2026 as long as the loft clearance day is on.\n[18 Feb 2026] Femi: We are dropping the loft clearance day from the list.\n[19 Feb 2026] Kofi: @Femi Think 24 Feb 2026 would work if I bleed the attic radiators instead?\n[21 Feb 2026] Femi: @Kofi Lovely, I'll defrost the old fridge by 25 Feb 2026 for sure.\n[22 Feb 2026] Femi: @Kofi The original date stands, so you need to bleed the attic radiators.",
  "question": "Going by the card's rules, does Kofi keep the promise to bleed the attic radiators at the end of 24 Feb 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q629cc72f2e",
  "kind": "choice",
  "text": "Export from the support queue, covering the new term plans; passed on by Greta.\n\nMembers: Mo, Ravi, Zara, Greta\nChat export (date | from | to | message):\n2026-01-11 | Mo | Greta | Absolutely, I will set up the book stall by 14 January 2026.\n2026-01-14 | Mo | Ravi | Only if the reading festival is on, I will wrap the prize hampers by 21 January 2026.\n2026-01-17 | Zara | group | Yay, the reading festival is all set to go!\n2026-01-21 | Mo | Ravi | On my action item, may I wrap the prize hampers by 27 January 2026 instead?\n2026-01-21 | Ravi | Mo | Yes, happy for you to wrap the prize hampers by 27 January 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Mo's commitment to wrap the prize hampers at the end of 24 January 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken",
   "Kept"
  ]
 }
]
