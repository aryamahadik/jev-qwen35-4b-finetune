# G5-H blind read T32-blind_read-4c0dc177-006 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root9/T32/qc/g5h/answers/T32-blind_read-4c0dc177-006.json

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
  "qid": "qdb6f057faa",
  "kind": "choice",
  "text": "{\"export_type\": \"group chat export\", \"chat_topic\": \"the shared kitchen scheme\", \"saved_by\": \"Lena\"}\n\nMembers: Tomas, Femi, Lena\nChat export (date | from | to | message):\n2026-04-16 | Tomas | Lena | If the house insurance review goes ahead, I'll gladly wipe the shared kitchen counter by 19 April 2026.\n2026-04-18 | Lena | group | Sorry, the house insurance review is off.\n2026-04-19 | Femi | Tomas | I will defrost the top freezer by 22 April 2026.\n2026-04-22 | Femi | Tomas | Mind giving me until 26 April 2026 to defrost the top freezer?\n2026-04-22 | Tomas | Femi | No, you need to defrost the top freezer by the original date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Tomas's promise to wipe the shared kitchen counter sit at the end of 21 April 2026, exactly?",
  "options": [
   "Kept",
   "Not triggered",
   "Not yet due",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q2a3d3da6b8",
  "kind": "yes/no",
  "text": "Shared by Lee, this work thread covers the platform rewrite.\n\nMembers: Lee, Rhea, Ines, Nadia\nChat log (oldest first):\n[9 Jan 2026] Ines: @Nadia No promises, but I'll aim to deploy the staging build by 17 Jan 2026.\n[9 Jan 2026] Rhea: @Ines If the sprint demo goes ahead, I'll write the release notes by 18 Jan 2026.\n[11 Jan 2026] Ines: @Nadia Ticket's mine, I'll deploy the staging build by 14 Jan 2026.\n[14 Jan 2026] Ines: @Nadia Change of plans: I will not deploy the staging build\n[15 Jan 2026] Nadia: @Ines I'll be sure to run the security scan by 22 Jan 2026.\n[16 Jan 2026] Rhea: Team, the sprint demo is not happening.",
  "question": "At the end of 15 Jan 2026, has the promise Ines made to deploy the staging build been broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4999db10b8",
  "kind": "yes/no",
  "text": "Thread filed under support\nAbout the caring rota, saved by Nadia.\n\nMembers: Nadia, Elif, Tomas\nChat log (oldest first):\n[14 Sep 2026] Tomas: @Nadia It's on me to collect the post by 19 September 2026.\n[15 Sep 2026] Nadia: @Elif Relax, I'll wash the bed linen by 18 September 2026 for sure.\n[15 Sep 2026] Tomas: @Nadia Quick update: you do not need to wash the bed linen at all.\n[17 Sep 2026] Nadia: @Elif To note: I have managed to wash the bed linen\n[18 Sep 2026] Nadia: @Elif I'll fetch the mobility aids by 24 September 2026, provided the physio session happens.\n[20 Sep 2026] Tomas: Sad to report that the physio session is off.",
  "question": "Has Nadia kept the promise to wash the bed linen at the end of 22 September 2026, instead of broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q06aecc1156",
  "kind": "choice",
  "text": "Local volunteer export\nSaved by Rhea, covering the topic of the school fundraiser.\n\nMembers: Leila, Omar, Ana, Rhea\nChat export (date | from | to | message):\n2026-01-15 | Ana | Rhea | Committing to print the raffle tickets by 19 January 2026.\n2026-01-18 | Ana | Omar | Count on me to send the newsletter drafts by 26 January 2026.\n2026-01-18 | Omar | Ana | Forget it, you won't need to send the newsletter drafts\n2026-01-18 | Ana | Rhea | Update on my side: I will not print the raffle tickets, sorry.\n2026-01-19 | Rhea | Ana | Provided the summer fete happens, I'll fetch the tea urn by 21 January 2026.\n2026-01-20 | Leila | group | Really pleased to say the summer fete will go ahead!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhere does Ana stand on the promise to send the newsletter drafts at the end of 22 January 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Broken",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qe70fe70ae3",
  "kind": "yes/no",
  "text": "Here is the plan for the travel plans, saved by Kai for the group.\n\nMembers: Ana, Kai, Kofi\nChat export (date | from | to | message):\n2026-09-22 | Kai | group | Will attempt to send the packing list by 2026-10-02, can't promise.\n2026-09-23 | Kai | Kofi | If the ferry crossing goes ahead, I'll print the boarding passes by 2026-10-02.\n2026-09-24 | Kai | Ana | I will make sure to send the packing list by 2026-10-01.\n2026-09-24 | Ana | group | Please note the ferry crossing will proceed.\n2026-09-26 | Kai | Ana | I need to take back my commitment to send the packing list.\n2026-10-01 | Kofi | Kai | Please don't feel you have to send the packing list",
  "question": "At the end of 2026-10-06, would it be right to say Kai has not broken the promise to send the packing list?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa20504e1c6",
  "kind": "yes/no",
  "text": "Exported by Oskar, this is the back and forth on the shop rebuild.\n\nMembers: Bruno, Greta, Oskar, Leila\nChat log (oldest first):\n[7 Feb 2026] Bruno: @Oskar I'll restore the old theme by 13 February 2026, provided the courier pickup happens.\n[8 Feb 2026] Oskar: Great news, the courier pickup is on!\n[11 Feb 2026] Greta: @Bruno Got it, I'll update the product photos by 16 February 2026 for sure.\n[15 Feb 2026] Greta: @Bruno I committed to update the product photos, can I do that by 18 February 2026 instead?\n[16 Feb 2026] Leila: @Greta Yes, fine to update the product photos by 18 February 2026 instead.\n[16 Feb 2026] Greta: @Bruno Got myself to update the product photos lol.",
  "question": "Has Greta not kept the promise to update the product photos at the end of 20 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q572d380602",
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
  "qid": "qedc8af1ac1",
  "kind": "choice",
  "text": "Freelance thread record, the payment setup, shared by Zara.\n\nMembers: Lena, Kai, Zara\nChat log (oldest first):\n[20 Apr 2026] Kai: @Zara If the pop up stall goes ahead, I'll send the stock spreadsheet by 25 April 2026.\n[20 Apr 2026] Lena: @Zara Relax, I'll set up the email forwarding by 24 April 2026 for sure.\n[24 Apr 2026] Lena: Sorry, the pop up stall is off.\n[24 Apr 2026] Lena: @Zara Mind giving me until 28 April 2026 to set up the email forwarding?\n[24 Apr 2026] Zara: @Lena Nah, that deadline counts, mate, so please set up the email forwarding!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Kai made to send the stock spreadsheet at the end of 27 April 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q36ee22abe7",
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
  "qid": "q211f393105",
  "kind": "yes/no",
  "text": "Landlord and renters' group talk on the street watch scheme, from Priya's export.\n\nMembers: Hana, Nadia, Priya\nChat log (oldest first):\n[8 Jul 2026] Hana: @Nadia I will return the ladders by 16 Jul 2026 only if the road works meeting happens.\n[8 Jul 2026] Nadia: @Hana Lovely, I'll walk the old spaniel by 12 Jul 2026 for sure.\n[9 Jul 2026] Priya: @Nadia Count on me to take in the post by 13 Jul 2026, if the speed camera survey happens.\n[11 Jul 2026] Nadia: @Hana I regret to say that I shall not walk the old spaniel.\n[12 Jul 2026] Priya: @Nadia Forget it, you won't need to walk the old spaniel",
  "question": "Would you call Nadia's promise to walk the old spaniel broken, waived, not triggered or not yet due, instead of kept, at the end of 17 Jul 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q502eab383a",
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
  "qid": "qbe37bb7bf8",
  "kind": "yes/no",
  "text": "Landlord and renters' group talk on the big house plan, from Zara's export.\n\nMembers: Ravi, Wren, Zara\nChat log (oldest first):\n[1 Mar 2026] Zara: @Ravi I'll oil the back door hinges by 9 Mar 2026, provided the heritage fete happens.\n[4 Mar 2026] Zara: @Ravi Relax, I'll scrub the cellar steps by 8 Mar 2026 for sure.\n[4 Mar 2026] Wren: @Zara I will wash the sash windows by 10 Mar 2026 only if the loft clearance day happens.\n[7 Mar 2026] Zara: @Ravi I own this, I'll find the loft ladder by 9 Mar 2026.\n[8 Mar 2026] Zara: @Ravi Got myself to scrub the cellar steps lol.",
  "question": "Applying the card's rules, does Zara's promise to scrub the cellar steps count as broken, waived, not triggered or not yet due, rather than kept, as of 8 Mar 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q57f0effa98",
  "kind": "yes/no",
  "text": "Forwarded by Malik, these tenant replies are about the guest welcome plan for the file.\n\nMembers: Malik, Lee, Oskar, Bruno\nChat log (oldest first):\n[7 Sep 2026] Lee: @Oskar Only if the summer season launch is on, I will air the spare room by 13 Sep 2026.\n[8 Sep 2026] Lee: Brilliant news everyone, the summer season launch is a go!\n[10 Sep 2026] Oskar: @Malik You can bet I'll vacuum the holiday cottage by 12 Sep 2026.\n[10 Sep 2026] Oskar: @Malik Would it be fine if I vacuum the holiday cottage by 15 Sep 2026 instead, yeah?\n[10 Sep 2026] Malik: @Oskar That suits me, so please vacuum the holiday cottage by 15 Sep 2026 instead.\n[13 Sep 2026] Oskar: @Lee Don't sweat it, there's no need to air the spare room",
  "question": "Under the rules on the card, is Lee's promise to air the spare room kept as of 12 Sep 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0cb6daac09",
  "kind": "yes/no",
  "text": "Tomas shared this so the family follows the allotment expansion.\n\nMembers: Tomas, Bruno, Dara, Yuki\nChat log (oldest first):\n[17 Apr 2026] Yuki: @Dara Lovely, I'll deliver the surplus runner beans by 21 Apr 2026 if the water tank delivery is on.\n[17 Apr 2026] Bruno: @Yuki Guaranteed I'll sow the broad beans by 25 Apr 2026.\n[17 Apr 2026] Yuki: Got it, thanks a lot.\n[18 Apr 2026] Tomas: Yay, the water tank delivery is all set to go!\n[18 Apr 2026] Bruno: @Yuki I have to take back my promise to sow the broad beans.\n[25 Apr 2026] Yuki: @Bruno Don't sweat it, there's no need to sow the broad beans",
  "question": "Under the rules on the card, is the promise Bruno made to sow the broad beans kept as of 26 Apr 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc2884365d1",
  "kind": "choice",
  "text": "Subject: Chat about the data cleanup\nBelow, with Jonas named as the source, is the chat as exported.\n\nMembers: Ana, Jonas\nChat log (oldest first):\n[17 Jun 2026] Ana: @Jonas Only if the penetration test is on, I will restart the build server by 23 June 2026.\n[19 Jun 2026] Jonas: @Ana I own this, I'll merge the login branch by 24 June 2026.\n[19 Jun 2026] Ana: Fab, we are on for the penetration test as planned!\n[23 Jun 2026] Ana: @Jonas Log entry: restart the build server, carried out\n[24 Jun 2026] Jonas: @Ana Update on my side: I will not merge the login branch, sorry.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Ana's commitment to restart the build server at the end of 22 June 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Broken",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q2275e0455b",
  "kind": "yes/no",
  "text": "An exported family chat on the house rules debate, saved by Dara, left unchanged.\n\nMembers: Dara, Femi\nChat log (oldest first):\n[25 Jun 2026] Dara: @Femi As long as the house viewing is on, I will oil the back door hinges by 27 June 2026.\n[25 Jun 2026] Femi: @Dara Absolutely, I will scrub the cellar steps by 30 June 2026.\n[28 Jun 2026] Dara: @Femi I assure you I'll clear the kitchen sink by 4 July 2026 if the ghost tour is on.\n[3 Jul 2026] Femi: Quick heads up, the ghost tour is scrapped.\n[4 Jul 2026] Dara: @Femi Mind giving me until 7 July 2026 to clear the kitchen sink?\n[4 Jul 2026] Femi: @Dara Fine by me, you can clear the kitchen sink by 7 July 2026.",
  "question": "Under the rules on the card, is it true that Dara has not kept the promise to clear the kitchen sink as of 4 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5d720a178e",
  "kind": "yes/no",
  "text": "Subject: exported chat about the big day\nHere it is for you, from Femi, exactly as saved.\n\nMembers: Femi, Ivo, Yuki\nChat log (oldest first):\n[16 Jun 2026] Femi: @Ivo As long as the rehearsal dinner is on, I'll book the assistant photographer by 23 Jun 2026.\n[19 Jun 2026] Femi: @Yuki Ticket's mine, I'll return the lighting stands by 26 Jun 2026.\n[22 Jun 2026] Femi: Lovely, the rehearsal dinner is definitely happening!\n[22 Jun 2026] Yuki: @Femi Relax, mate, you're not expected to book the assistant photographer\n[23 Jun 2026] Femi: @Ivo To my relief, I managed to book the assistant photographer.",
  "question": "Has Femi kept the promise to book the assistant photographer at the end of 24 Jun 2026, instead of broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbb20632144",
  "kind": "choice",
  "text": "Our house group, sorted by Tess, with the cottage refresh up front.\n\nMembers: Jonas, Leila, Sami, Tess\nChat log (oldest first):\n[22 Jan 2026] Sami: @Jonas I'll leave the welcome basket by 29 January 2026 as long as the check out clean is on.\n[22 Jan 2026] Jonas: @Sami I will make sure to scrub the hot tub by 31 January 2026.\n[24 Jan 2026] Jonas: How's the plan to leave the welcome basket?\n[24 Jan 2026] Sami: @Jonas Nobody needs you to scrub the hot tub, that's that\n[28 Jan 2026] Leila: Just so you know, the check out clean is on as scheduled.\n[30 Jan 2026] Sami: @Jonas For the record: I was able to leave the welcome basket",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of 2 February 2026, which status does Sami have for the promise to leave the welcome basket?",
  "options": [
   "Waived",
   "Broken",
   "Kept",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qea21e0c31f",
  "kind": "choice",
  "text": "Here's the club committee's chat, saved by Wren, about the playground project.\n\nMembers: Ines, Elif, Wren\nChat export (date | from | to | message):\n2026-10-26 | Ines | Elif | Provided the field day happens, I'll wrap the prize hampers by 28 October 2026.\n2026-10-28 | Elif | Ines | Guaranteed I'll print the raffle tickets by 4 November 2026.\n2026-10-28 | Ines | group | Appreciate you telling me.\n2026-10-31 | Elif | Ines | Is it all right if I print the raffle tickets by 7 November 2026 instead?\n2026-10-31 | Wren | Ines | If the quiz night is on, I'll definitely label the raffle prizes by 5 November 2026.\n2026-11-01 | Ines | Elif | Yes, you're welcome to print the raffle tickets by 7 November 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Elif made to print the raffle tickets have at the end of 6 November 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not yet due",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q8f2dbb6c79",
  "kind": "choice",
  "text": "Here is the quiet street fund, posted by Nadia for the family to read.\n\nMembers: Bruno, Oskar, Nadia\nChat log (oldest first):\n[15 May 2026] Oskar: @Nadia Ticket's mine, I'll lend the stepladder by 19 May 2026.\n[15 May 2026] Oskar: @Nadia Can I lend the stepladder by 21 May 2026 instead? I did promise, sorry.\n[15 May 2026] Oskar: @Nadia Count on me to return the ladders by 20 May 2026.\n[15 May 2026] Oskar: @Nadia I will take in the post by 20 May 2026.\n[16 May 2026] Nadia: @Bruno I assure you I'll feed the cat across the road by 20 May 2026 if the street litter clean is on.\n[19 May 2026] Oskar: Please note the street litter clean will proceed.\n[19 May 2026] Oskar: @Nadia To note: I have managed to lend the stepladder\n[20 May 2026] Bruno: @Oskar Don't sweat it, there's no need to take in the post",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of 31 May 2026, what is the date by which Oskar has to lend the stepladder, counting any agreed change?",
  "options": [
   "19 May 2026",
   "20 May 2026",
   "21 May 2026"
  ]
 },
 {
  "qid": "q41332b0b43",
  "kind": "choice",
  "text": "Subject: chat export on the school fundraiser\nThe full chat follows, saved by Jonas, for you to read.\n\nMembers: Wren, Jonas, Ivo, Femi\nChat export (date | from | to | message):\n2026-06-26 | Femi | Ivo | Provided the quiz night happens, I will return the borrowed trestle tables by 3 Jul 2026.\n2026-06-29 | Jonas | Ivo | Relax, I'll collect the bake sale tins by 5 Jul 2026 for sure.\n2026-06-30 | Jonas | Ivo | Count on me to fetch the tea urn by 6 Jul 2026.\n2026-06-30 | Jonas | Ivo | Scratch that, I'm not going to collect the bake sale tins\n2026-07-02 | Ivo | group | Update: the quiz night is going ahead as planned.\n2026-07-03 | Jonas | Ivo | Mate, I promised, may I fetch the tea urn by 11 Jul 2026 instead?\n2026-07-05 | Ivo | Jonas | That suits me, so please fetch the tea urn by 11 Jul 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 12 Jul 2026, by what date does Jonas have to fetch the tea urn, counting any agreed change of date?",
  "options": [
   "11 Jul 2026",
   "6 Jul 2026",
   "5 Jul 2026"
  ]
 },
 {
  "qid": "q1a3d1b22a8",
  "kind": "yes/no",
  "text": "A short note above messages between tenants and the landlord about the guest welcome plan, saved by Greta.\n\nMembers: Femi, Leila, Kai, Greta\nChat log (oldest first):\n[2 Mar 2026] Kai: @Leila I assure you I'll vacuum the holiday cottage by 5 March 2026 if the pool safety inspection is on.\n[2 Mar 2026] Femi: We are dropping the pool safety inspection from the list.\n[4 Mar 2026] Kai: @Leila Any chance I can vacuum the holiday cottage by 9 March 2026 instead?\n[5 Mar 2026] Femi: @Kai Go ahead and vacuum the holiday cottage by 9 March 2026, that is fine.\n[7 Mar 2026] Leila: @Femi Ticket's mine, I'll wheel the bins out by 16 March 2026.",
  "question": "Has Kai's promise to vacuum the holiday cottage ended up broken, waived, not triggered or not yet due, instead of kept, as of 8 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6b19692591",
  "kind": "yes/no",
  "text": "Our flat chat about the student house hunt, shared by Ivo for whoever lives here.\n\nMembers: Lena, Priya, Ivo, Sami\nChat log (oldest first):\n[26 Aug 2026] Sami: @Lena Count on me to forward the inventory photos by 4 Sep 2026 if the freshers welcome night is on.\n[30 Aug 2026] Priya: @Lena Ticket's mine, I'll photograph the bathroom mould by 2 Sep 2026.\n[31 Aug 2026] Ivo: @Priya Quick update: you do not need to photograph the bathroom mould at all.\n[1 Sep 2026] Sami: @Ivo I promise to copy the house keys by 6 Sep 2026 if the move in day is on.\n[4 Sep 2026] Priya: @Lena Ticked off: photograph the bathroom mould, feels so good\n\nAdmin sign-off: plans changed in this chat carry the admins' blessing, so Ivo can move on.",
  "question": "Does the chat, checked at the end of 3 Sep 2026, show that Priya has broken the promise to photograph the bathroom mould?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6dfe3b7546",
  "kind": "choice",
  "text": "{\"record\": \"shared group chat\", \"subject\": \"the travel plans\", \"shared_by\": \"Tess\", \"stored\": \"as text\"}\n\nMembers: Malik, Tess, Nadia, Rhea\nChat export (date | from | to | message):\n2026-02-27 | Malik | Rhea | I will make sure to send the packing list by Friday, 6 March 2026.\n2026-02-27 | Tess | Malik | I'll book the airport parking by Sunday, 1 March 2026, provided the flight check-in happens.\n2026-03-03 | Tess | Malik | I'll check the passport copies by Saturday, 7 March 2026, provided the beach picnic happens.\n2026-03-04 | Tess | Rhea | I'll be sure to pack the travel adaptors by Tuesday, 10 March 2026.\n2026-03-06 | Malik | Rhea | Quick report: I've managed to send the packing list",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Malik's promise to send the packing list have at the end of Tuesday, 10 March 2026?",
  "options": [
   "Waived",
   "Kept",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "qc03af9c72a",
  "kind": "choice",
  "text": "Kofi shared this so the family follows the summer getaway.\n\nMembers: Tess, Kofi, Leila\nChat export (date | from | to | message):\n2026-03-24 | Kofi | Tess | Hoping to book the airport parking by 30 Mar 2026, no promises.\n2026-03-26 | Kofi | Tess | Promise to book the airport parking by 31 Mar 2026 if the hotel arrival goes ahead.\n2026-03-29 | Kofi | group | Yep, the hotel arrival is on as planned.\n2026-03-30 | Leila | Tess | Count on me to fetch the sunscreen by 4 Apr 2026.\n2026-04-01 | Kofi | Tess | Got myself to book the airport parking lol.\n2026-04-02 | Kofi | Leila | You are released, no requirement to fetch the sunscreen.",
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
  "qid": "q2214d14542",
  "kind": "yes/no",
  "text": "Here's the club committee's chat, saved by Kofi, about the sponsor search.\n\nMembers: Kofi, Oskar, Bruno, Kai\nChat export (date | from | to | message):\n2026-03-08 | Kofi | Kai | I'll set up the feed stop by 15 Mar 2026, promise.\n2026-03-09 | Kai | Kofi | Provided the mechanics clinic happens, I'll wash the club jerseys by 16 Mar 2026.\n2026-03-11 | Oskar | Kofi | Forget it, you won't need to set up the feed stop\n2026-03-13 | Bruno | group | Please note the mechanics clinic will proceed.\n2026-03-14 | Kofi | Kai | Ah, no stress, no need for you to wash the club jerseys",
  "question": "Is Kai's promise to wash the club jerseys kept as of 18 Mar 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa12c3dce04",
  "kind": "yes/no",
  "text": "{\"thread_kind\": \"exported conversation\", \"about\": \"the guest welcome plan\", \"exported_by\": \"Rhea\"}\n\nMembers: Lena, Kai, Rhea\nChat log (oldest first):\n[3 Oct 2026] Rhea: @Kai I'll collect the bed linen by Monday, October 12, 2026 if the guest arrival evening goes ahead.\n[4 Oct 2026] Kai: @Lena Committing to scrub the hot tub by Sunday, October 11, 2026.\n[5 Oct 2026] Kai: @Lena Ticked off my list: scrub the hot tub, yay.\n[6 Oct 2026] Kai: Update, the guest arrival evening will not take place.\n[8 Oct 2026] Lena: @Rhea I own this, I'll wheel the bins out by Saturday, October 17, 2026.\n[9 Oct 2026] Rhea: Hey, did you get a chance to scrub the hot tub?",
  "question": "Is the promise Kai made to scrub the hot tub in a status other than broken at the end of Wednesday, October 7, 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qce73daa9b1",
  "kind": "choice",
  "text": "{\"archive\": \"group chat\", \"subject\": \"the menu redesign\", \"sent_by\": \"Sami\"}\n\nMembers: Priya, Sami, Tess\nChat log (oldest first):\n[27 Jul 2026] Sami: @Priya I'll collect the photo credits by 4 August 2026, provided the print run happens.\n[28 Jul 2026] Sami: See if I can send the moodboard files by 2 August 2026.\n[29 Jul 2026] Sami: @Priya Count on me, I'll send the moodboard files by 3 August 2026.\n[31 Jul 2026] Sami: @Priya I'll export the logo files by 8 August 2026, promise.\n[1 Aug 2026] Tess: @Priya As long as the brand review call is on, I will fetch the brand fonts by 5 August 2026.\n[3 Aug 2026] Sami: @Priya Ticked off my list: send the moodboard files, yay.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Sami made to send the moodboard files, what state is it in at the end of 7 August 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Kept",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "qca88939cc1",
  "kind": "choice",
  "text": "Volunteers, here is the new term plans thread that Ivo forwarded for us.\n\nMembers: Sami, Ivo, Zara, Ana\nChat log (oldest first):\n[8 Sep 2026] Ivo: @Ana You can bank on me to label the raffle prizes by 14 September 2026.\n[13 Sep 2026] Ana: @Zara Count on me, I'll return the borrowed trestle tables by 19 September 2026.\n[13 Sep 2026] Sami: @Zara I'll send the newsletter drafts by 17 September 2026, providing the governors meeting goes ahead.\n[13 Sep 2026] Sami: Team, the governors meeting is not happening.\n[14 Sep 2026] Zara: @Ana Relax, I'll collect the bake sale tins by 21 September 2026 for sure.\n[16 Sep 2026] Zara: @Ana Change of plans: I will not collect the bake sale tins",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Sami's promise to send the newsletter drafts at the end of 21 September 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q7366daecb4",
  "kind": "yes/no",
  "text": "Oskar shared this support thread, which is about the website relaunch.\n\nMembers: Dara, Femi, Oskar\nChat export (date | from | to | message):\n2026-08-11 | Femi | Oskar | I assure you I'll print the event banners by 18 Aug 2026 if the annual review is on.\n2026-08-14 | Dara | Oskar | If the influencer call is on, I'll definitely fetch the campaign budget sheet by 21 Aug 2026.\n2026-08-15 | Dara | Oskar | Count on me to draft the press release by 23 Aug 2026.\n2026-08-16 | Dara | Oskar | To my relief, I managed to draft the press release.\n2026-08-16 | Oskar | Dara | Absolutely, I will pay the printing invoice by 18 Aug 2026.\n2026-08-20 | Dara | group | Yep, the influencer call is on as planned.",
  "question": "On the card, was Dara's promise to draft the press release broken, waived, not triggered or not yet due, rather than kept, at the end of 21 Aug 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1f5a9f9110",
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
  "qid": "q0e2eaef665",
  "kind": "choice",
  "text": "Chat channel log:\nWork messages about the trade show push, exported by Bruno.\n\nMembers: Tomas, Greta, Dara, Bruno\nChat export (date | from | to | message):\n2026-04-18 | Tomas | Dara | I'll set up the analytics dashboard by Tuesday, April 21, 2026, provided the trade fair stand happens.\n2026-04-18 | Greta | group | Update: the trade fair stand is going ahead as planned.\n2026-04-20 | Bruno | Dara | Ticket's mine, I'll collect the survey answers by Sunday, April 26, 2026.\n2026-04-25 | Greta | Bruno | Count on me to return the rented camera gear by Wednesday, April 29, 2026.\n2026-04-26 | Dara | Bruno | Good news, you're let off having to collect the survey answers",
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
  "qid": "q72a6d8a0e8",
  "kind": "choice",
  "text": "Shared by Lena, this work thread covers the staff handbook.\n\nMembers: Lena, Elif, Greta\nChat log (oldest first):\n[16 Jun 2026] Lena: @Greta I promise to renew the fire extinguisher service by 21 Jun 2026 if the staff picnic is on.\n[19 Jun 2026] Elif: Update: the staff picnic is going ahead as planned.\n[19 Jun 2026] Greta: @Lena I'll collect the visitor badges by 28 Jun 2026, promise.\n[21 Jun 2026] Elif: @Lena Ah, no stress, no need for you to renew the fire extinguisher service\n[28 Jun 2026] Greta: @Lena Quick question, could I collect the visitor badges by 1 Jul 2026 instead?\n[28 Jun 2026] Lena: @Greta Aw no, you need to collect the visitor badges by the original date!",
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
  "qid": "qdc076bedfa",
  "kind": "choice",
  "text": "Notes saved by Tess from messages between tenants and a landlord about the cottage refresh.\n\nMembers: Lena, Tess, Rhea, Leila\nChat log (oldest first):\n[8 Jul 2026] Tess: @Lena Guaranteed I'll fill the cleaning cupboard by 12 Jul 2026.\n[12 Jul 2026] Tess: @Lena Can I fill the cleaning cupboard by 18 Jul 2026 instead? I did promise, sorry.\n[12 Jul 2026] Tess: @Lena Got myself to fill the cleaning cupboard lol.\n[14 Jul 2026] Rhea: @Tess You can bank on me to leave the welcome basket by 23 Jul 2026.\n[20 Jul 2026] Rhea: @Tess Sorry, I won't leave the welcome basket after all\n[21 Jul 2026] Lena: @Tess Provided the summer season launch happens, I will wheel the bins out by 23 Jul 2026.\n[22 Jul 2026] Leila: Sorry all, the summer season launch is called off.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo what's the latest day Tess has to fill the cleaning cupboard by at the end of 16 Jul 2026, given any new date people agreed to?",
  "options": [
   "23 Jul 2026",
   "12 Jul 2026",
   "18 Jul 2026"
  ]
 },
 {
  "qid": "q95a62a7491",
  "kind": "choice",
  "text": "Help desk export\nAbout: the big house plan\nCopied by: Rhea\n\nMembers: Bruno, Rhea\nChat export (date | from | to | message):\n2026-10-11 | Rhea | Bruno | Relax, I'll tidy the boot room by 13 October 2026, promise.\n2026-10-13 | Rhea | Bruno | Mate, I promised, may I tidy the boot room by 17 October 2026 instead?\n2026-10-13 | Bruno | Rhea | Yes, you have the green light to tidy the boot room by 17 October 2026.\n2026-10-14 | Rhea | Bruno | If the heritage fete goes ahead, I'll gladly replace the hallway bulbs by 17 October 2026.\n2026-10-14 | Rhea | group | Brilliant news everyone, the heritage fete is a go!\n2026-10-17 | Bruno | Rhea | Relax, mate, you're not expected to replace the hallway bulbs",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Rhea's promise to replace the hallway bulbs at the end of 20 October 2026?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q7c9b99bf9e",
  "kind": "choice",
  "text": "Zara shared this support thread, which is about the gallery show.\n\nMembers: Femi, Zara, Wren, Tess\nChat log (oldest first):\n[14 Jul 2026] Wren: @Femi Absolutely, I will mail the business cards by Thursday, July 23, 2026.\n[16 Jul 2026] Tess: @Femi I'll check the poster proofs by Sunday, July 19, 2026 if the packaging launch goes ahead.\n[17 Jul 2026] Zara: Team, the packaging launch stays on as booked.\n[17 Jul 2026] Tess: @Femi Quick report: I've managed to check the poster proofs\n[19 Jul 2026] Wren: @Tess Committing to sketch the packaging mockup by Tuesday, July 28, 2026.\n[19 Jul 2026] Tess: @Zara As long as the brand review call is on, I'll fetch the brand fonts by Thursday, July 23, 2026.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Tess's promise to check the poster proofs receive at the end of Wednesday, July 22, 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q11fe4348c1",
  "kind": "yes/no",
  "text": "Plain copy of a family thread on the home adaptations, passed on by Bruno.\n\nMembers: Ravi, Jonas, Bruno, Mo\nChat log (oldest first):\n[14 Mar 2026] Jonas: @Ravi Might be able to print the care schedule by 2026-03-19, who knows!\n[16 Mar 2026] Jonas: @Bruno Provided the home assessment happens, I will print the care schedule by 2026-03-22.\n[17 Mar 2026] Ravi: Please note the home assessment will proceed.\n[20 Mar 2026] Jonas: @Bruno Mate, I promised, may I print the care schedule by 2026-03-27 instead?\n[21 Mar 2026] Bruno: @Jonas No change, you need to print the care schedule by the original date.\n[22 Mar 2026] Ravi: @Mo It's on me to collect the post by 2026-03-26.",
  "question": "Is the promise Jonas made to print the care schedule not kept by 2026-03-22?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe83281998e",
  "kind": "yes/no",
  "text": "Our house group, sorted by Wren, with the rent split plan up front.\n\nMembers: Kai, Malik, Wren, Hana\nChat log (oldest first):\n[20 Feb 2026] Kai: @Hana Guaranteed I'll print the tenancy agreement by 27 Feb 2026.\n[21 Feb 2026] Wren: @Kai As long as the gas safety inspection is on, I will return the bin rota by 25 Feb 2026.\n[22 Feb 2026] Wren: @Kai No need to print the tenancy agreement, I'm letting you off\n[23 Feb 2026] Hana: We are dropping the gas safety inspection from the list.\n[28 Feb 2026] Kai: @Hana Quick report: I've managed to print the tenancy agreement",
  "question": "Is the promise Kai made to print the tenancy agreement not kept by 4 Mar 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3d3d18edfb",
  "kind": "yes/no",
  "text": "Client chat in a freelance log: the documentary cut, passed on by Leila.\n\nMembers: Lena, Kai, Leila, Rhea\nChat export (date | from | to | message):\n2026-05-14 | Leila | Lena | Relax, I'll record the voice over by 18 May 2026 for sure.\n2026-05-14 | Rhea | Leila | I assure you I'll export the subtitle files by 22 May 2026 if the festival premiere is on.\n2026-05-15 | Leila | Lena | On my action item, may I record the voice over by 23 May 2026 instead?\n2026-05-17 | Lena | Leila | Nah, the date's staying put, so you can record the voice over.\n2026-05-17 | Leila | Lena | Quick report: I've managed to record the voice over\n2026-05-17 | Lena | Leila | If the shoot day goes ahead, I'll gladly ship the hard drive by 24 May 2026.",
  "question": "Does the card classify Leila's promise to record the voice over as broken, waived, not triggered or not yet due, rather than kept, on 18 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc32ef12251",
  "kind": "choice",
  "text": "Freelance thread record, the payment setup, shared by Zara.\n\nMembers: Lena, Kai, Zara\nChat log (oldest first):\n[20 Apr 2026] Kai: @Zara If the pop up stall goes ahead, I'll send the stock spreadsheet by 25 April 2026.\n[20 Apr 2026] Lena: @Zara Relax, I'll set up the email forwarding by 24 April 2026 for sure.\n[24 Apr 2026] Lena: Yep, the pop up stall is on as planned.\n[24 Apr 2026] Lena: @Zara Mind giving me until 28 April 2026 to set up the email forwarding?\n[24 Apr 2026] Zara: @Lena Nah, that deadline counts, mate, so please set up the email forwarding!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Kai made to send the stock spreadsheet at the end of 27 April 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q079b504829",
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
  "qid": "q52d6932b11",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the social media plan\nThis export came from Bruno and is pasted in full below.\n\nMembers: Bruno, Priya, Hana\nChat export (date | from | to | message):\n2026-02-06 | Bruno | Priya | As long as the webinar rehearsal is on, I'll fetch the campaign budget sheet by Monday, 9 February 2026.\n2026-02-10 | Bruno | Hana | Relax, I'll set up the analytics dashboard by Tuesday, 17 February 2026 for sure.\n2026-02-10 | Bruno | Hana | Mate, I promised, may I set up the analytics dashboard by Sunday, 22 February 2026 instead?\n2026-02-10 | Hana | Priya | Promise to fix the landing page headline by Wednesday, 18 February 2026 if the annual review goes ahead.\n2026-02-15 | Hana | Bruno | No, I'd like you to set up the analytics dashboard by the original date.\n2026-02-15 | Priya | group | Fab, we are on for the annual review as planned!",
  "question": "On the card, was Hana's promise to fix the landing page headline broken, waived, not triggered or not yet due, rather than kept, at the end of Monday, 16 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3e55d317b4",
  "kind": "yes/no",
  "text": "Saved by Omar, this talk about the trip itinerary is just for family.\n\nMembers: Ana, Omar, Malik, Nadia\nChat export (date | from | to | message):\n2026-08-04 | Nadia | Ana | Ticket's mine, I'll collect the insurance papers by 12 August 2026.\n2026-08-06 | Malik | Nadia | Don't sweat it, there's no need to collect the insurance papers\n2026-08-07 | Malik | Ana | I'll return the rental car keys by 14 August 2026 as long as the flight check-in is on.\n2026-08-07 | Malik | Ana | If the beach picnic goes ahead, I'll buy the packing cubes by 16 August 2026.\n2026-08-09 | Malik | group | Really pleased to say the flight check-in will go ahead!\n2026-08-12 | Nadia | Ana | Mum, I did collect the insurance papers, haha.",
  "question": "Is Nadia's promise to collect the insurance papers broken at the end of 16 August 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0c1ba3bd73",
  "kind": "yes/no",
  "text": "Flat chat export, saved by Kai\nCovers the autumn term budget, shared among the housemates.\n\nMembers: Wren, Ravi, Kai\nChat log (oldest first):\n[16 Jul 2026] Wren: @Ravi I'll try to print the tenancy agreement by 27 July 2026, no promises.\n[17 Jul 2026] Wren: @Kai Only if the gas safety inspection is on, I will print the tenancy agreement by 24 July 2026.\n[18 Jul 2026] Ravi: Update: the gas safety inspection is going ahead as planned.\n[20 Jul 2026] Ravi: @Wren Got it, I'll send the deposit receipt by 29 July 2026 for sure.\n[21 Jul 2026] Wren: @Kai Mind giving me until 27 July 2026 to print the tenancy agreement?\n[23 Jul 2026] Kai: @Wren That suits me, so please print the tenancy agreement by 27 July 2026 instead.",
  "question": "On 27 July 2026 itself, has Wren not kept the promise to print the tenancy agreement?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbbd9393e5d",
  "kind": "yes/no",
  "text": "Here is the plan for the travel plans, saved by Kai for the group.\n\nMembers: Ana, Kai, Kofi\nChat export (date | from | to | message):\n2026-09-22 | Kai | group | Will attempt to send the packing list by 2026-10-02, can't promise.\n2026-09-23 | Kai | Kofi | If the ferry crossing goes ahead, I'll print the boarding passes by 2026-10-02.\n2026-09-24 | Kai | Ana | I will make sure to send the packing list by 2026-10-01.\n2026-09-24 | Ana | group | Please note the ferry crossing will proceed.\n2026-09-26 | Kai | Ana | I need to take back my commitment to send the packing list.\n2026-10-01 | Kofi | Kai | Please don't feel you have to send the packing list",
  "question": "Does the chat, checked at the end of 2026-10-06, show that Kai has broken the promise to send the packing list?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd14323c1d5",
  "kind": "choice",
  "text": "Attached chat: the league run\nForwarded by: Wren\n\nMembers: Dara, Tomas, Wren, Ana\nChat log (oldest first):\n[4 Apr 2026] Wren: @Ana If the presentation evening goes ahead, I'll book the changing room by 8 April 2026.\n[8 Apr 2026] Tomas: I'll try to print the team sheets by 15 April 2026, no promises.\n[9 Apr 2026] Tomas: @Ana Lovely, I'll print the team sheets by 14 April 2026 for sure.\n[11 Apr 2026] Ana: @Wren Lovely, I'll return the bib sets by 20 April 2026 if the pre-season friendly is on.\n[11 Apr 2026] Dara: @Tomas No worries, you don't need to print the team sheets\n[15 Apr 2026] Tomas: @Ana Log entry: print the team sheets, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Tomas gave to print the team sheets have at the end of 15 April 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not triggered",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "qa192753a81",
  "kind": "choice",
  "text": "Copy of a household chat shared by Zara, where neighbours discuss the packing plan.\n\nMembers: Greta, Zara, Ines, Dara\nChat export (date | from | to | message):\n2026-06-09 | Ines | Zara | Committing to book the airport parking by 18 June 2026.\n2026-06-11 | Greta | Zara | Count on me to fetch the sunscreen by 16 June 2026 if the guided tour is on.\n2026-06-14 | Greta | Zara | Guaranteed I'll collect the insurance papers by 21 June 2026.\n2026-06-14 | Greta | group | Fab, we are on for the guided tour as planned!\n2026-06-17 | Greta | Zara | Guess what, I managed to fetch the sunscreen!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 18 June 2026, what status has Greta's promise to fetch the sunscreen got?",
  "options": [
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qf91f5d7560",
  "kind": "yes/no",
  "text": "Work team channel\nSaved by Rhea, which talks about the platform rewrite.\n\nMembers: Elif, Rhea, Bruno, Zara\nChat log (oldest first):\n[22 Mar 2026] Elif: @Bruno I own this, I'll deploy the staging build by 24 March 2026.\n[22 Mar 2026] Zara: @Bruno I promise to run the security scan by 28 March 2026.\n[25 Mar 2026] Bruno: @Zara I promise to review the pull request by 30 March 2026 if the server migration is on.\n[26 Mar 2026] Zara: Just so you know, the server migration is on as scheduled.\n[31 Mar 2026] Bruno: @Zara To note: I have managed to review the pull request",
  "question": "Is the promise Bruno made to review the pull request in a status other than broken at the end of 4 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qcfc4adbd98",
  "kind": "choice",
  "text": "Pasted into a record by Bruno: the messages sent between a tenant and an agent about the guest welcome plan.\n\nMembers: Oskar, Ravi, Ana, Bruno\nChat log (oldest first):\n[15 Aug 2026] Ana: @Bruno I will make sure to air the spare room by 20 August 2026.\n[15 Aug 2026] Bruno: @Ana I will wash the beach towels by 23 August 2026 only if the owner handover visit happens.\n[16 Aug 2026] Oskar: Update on your plan to air the spare room?\n[18 Aug 2026] Ravi: @Ana Nobody needs you to air the spare room, that's that\n[21 Aug 2026] Bruno: Update, the owner handover visit will not take place.\n[23 Aug 2026] Ana: @Bruno To my relief, I managed to air the spare room.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Ana's pledge to air the spare room sit at the end of 20 August 2026?",
  "options": [
   "Waived",
   "Broken",
   "Not yet due",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "q910cfcf872",
  "kind": "yes/no",
  "text": "Shared with the committee, this export of the sponsor search came from Ana.\n\nMembers: Ana, Lena, Bruno\nChat log (oldest first):\n[15 Feb 2026] Ana: @Lena Count on me to set up the feed stop by 22 February 2026.\n[15 Feb 2026] Lena: Cheers, noted.\n[19 Feb 2026] Ana: @Lena You can bank on me to wash the club jerseys by 23 February 2026.\n[20 Feb 2026] Lena: @Ana Provided the hill climb happens, I'll fetch the bike stand by 23 February 2026.\n[21 Feb 2026] Bruno: Brilliant news everyone, the hill climb is a go!\n[25 Feb 2026] Ana: @Lena For the record: I was able to set up the feed stop",
  "question": "Would you say Ana kept the promise to set up the feed stop at the end of 1 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
