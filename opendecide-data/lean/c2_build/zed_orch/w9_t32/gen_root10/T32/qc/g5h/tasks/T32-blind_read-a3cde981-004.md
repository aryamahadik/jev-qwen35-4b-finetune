# G5-H blind read T32-blind_read-a3cde981-004 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root10/T32/qc/g5h/answers/T32-blind_read-a3cde981-004.json

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
  "qid": "qfb8b6d6edd",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the visitor policy\nThe chat below comes from Jonas, copied as is for reference.\n\nMembers: Tomas, Ines, Priya, Jonas\nChat log (oldest first):\n[17 Oct 2026] Priya: @Ines I assure you I'll replace the kitchen filters by 24 Oct 2026 if the annual audit is on.\n[17 Oct 2026] Tomas: @Priya Count on me to collect the visitor badges by 23 Oct 2026.\n[17 Oct 2026] Priya: Ah right, thanks for that.\n[19 Oct 2026] Priya: Team, the annual audit stays on as booked.\n[20 Oct 2026] Tomas: @Priya Can I collect the visitor badges by 25 Oct 2026 instead? I did promise, sorry.\n[20 Oct 2026] Priya: @Tomas No, I'd like you to collect the visitor badges by the original date.",
  "question": "On 23 Oct 2026 itself, has Tomas not kept the promise to collect the visitor badges?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1d09b6af51",
  "kind": "choice",
  "text": "Leila forwarded these replies from the agent on the tenancy renewal talks for the file.\n\nMembers: Ivo, Leila, Elif\nChat log (oldest first):\n[12 Mar 2026] Elif: @Ivo I'll forward the gas bill by Monday, March 16, 2026, promise.\n[12 Mar 2026] Leila: @Elif Forget it, you won't need to forward the gas bill\n[12 Mar 2026] Elif: @Ivo Ticked off my list: forward the gas bill, yay.\n[14 Mar 2026] Ivo: @Leila If the flat viewing day is on, I'll definitely bring the step stool by Tuesday, March 17, 2026.\n[16 Mar 2026] Leila: Quick heads up, the flat viewing day is scrapped.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Elif's promise to forward the gas bill stand at the end of Friday, March 13, 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qeab2121a49",
  "kind": "yes/no",
  "text": "{\"chat\": \"exported\", \"about\": \"the garden makeover\", \"saved_by\": \"Jonas\", \"medium\": \"text\"}\n\nMembers: Wren, Nadia, Jonas\nChat export (date | from | to | message):\n2026-09-24 | Wren | Nadia | I will make sure to return the tile cutter by 28 September 2026.\n2026-09-24 | Wren | Nadia | Mind giving me until 1 October 2026 to return the tile cutter?\n2026-09-25 | Jonas | Wren | Provided the builder quote meeting happens, I will pick up the grout bag by 4 October 2026.\n2026-09-28 | Jonas | group | Team, the builder quote meeting is not happening.\n2026-09-28 | Wren | Nadia | Mum, I did return the tile cutter, haha.",
  "question": "Was Wren's promise to return the tile cutter not kept as of 30 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9c2971351e",
  "kind": "choice",
  "text": "Note above exported messages from a tenant to the letting agent, covering the summer lets season, saved by Bruno.\n\nMembers: Yuki, Ines, Tess, Bruno\nChat log (oldest first):\n[28 Jul 2026] Ines: @Tess I own this, I'll restock the guest toiletries by 3 August 2026.\n[29 Jul 2026] Yuki: @Bruno As long as the guest arrival evening is on, I will air the spare room by 6 August 2026.\n[30 Jul 2026] Tess: We are dropping the guest arrival evening from the list.\n[1 Aug 2026] Ines: @Tess Any chance I can restock the guest toiletries by 8 August 2026 instead?\n[1 Aug 2026] Bruno: @Ines I will make sure to wash the beach towels by 7 August 2026.\n[7 Aug 2026] Bruno: @Ines Is it all right if I wash the beach towels by 11 August 2026 instead?\n[7 Aug 2026] Ines: @Bruno Yes, lovely, you can wash the beach towels by 11 August 2026 instead!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo what's the latest day Ines has to restock the guest toiletries by at the end of 2 August 2026, given any new date people agreed to?",
  "options": [
   "3 August 2026",
   "8 August 2026",
   "6 August 2026"
  ]
 },
 {
  "qid": "q1f2f4b1d8b",
  "kind": "choice",
  "text": "Yo flatmates, Mo shared this chat about the kitchen refit, so chip in.\n\nMembers: Kofi, Mo\nChat export (date | from | to | message):\n2026-06-13 | Kofi | Mo | Lovely, I'll ring the flat repair line by Tuesday, 16 June 2026 if the electrics safety check is on.\n2026-06-13 | Mo | group | Brilliant news everyone, the electrics safety check is a go!\n2026-06-14 | Kofi | Mo | I'll be sure to wipe the cooker hood by Wednesday, 17 June 2026.\n2026-06-15 | Mo | Kofi | Good news, you're let off having to wipe the cooker hood\n2026-06-16 | Mo | Kofi | Ah, no stress, no need for you to ring the flat repair line",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Kofi's promise to ring the flat repair line at the end of Sunday, 21 June 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q2875a4eaf7",
  "kind": "choice",
  "text": "We are getting ready for the family day out, and Tomas shared this chat with us.\n\nMembers: Kai, Tomas, Tess, Rhea\nChat log (oldest first):\n[24 Sep 2026] Rhea: @Kai You can bank on me to pick up the school bags by 30 Sep 2026.\n[24 Sep 2026] Kai: @Rhea Relax, mate, you're not expected to pick up the school bags\n[27 Sep 2026] Tomas: @Tess Count on me to teach the card game by 4 Oct 2026, if the puppet show happens.\n[28 Sep 2026] Tomas: @Tess Provided the school play happens, I will tidy the playroom by 2 Oct 2026.\n[29 Sep 2026] Kai: @Tomas Guaranteed I'll fetch the craft box by 6 Oct 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 1 Oct 2026, what status has Rhea's promise to pick up the school bags got?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q0bc0e9a2d6",
  "kind": "yes/no",
  "text": "Ana forwarded this for the committee as we dig in on the junior section.\n\nMembers: Ana, Nadia, Mo\nChat log (oldest first):\n[3 Feb 2026] Nadia: @Ana Only if the pre-season friendly is on, I will pump the match balls by February 11, 2026.\n[4 Feb 2026] Ana: @Nadia I promise to collect the referee whistles by February 7, 2026.\n[6 Feb 2026] Mo: @Nadia I'll wash the away kit by February 12, 2026, promise.\n[6 Feb 2026] Ana: @Nadia I promise to mark the pitch lines by February 13, 2026.\n[8 Feb 2026] Mo: Lovely, the pre-season friendly is definitely happening!\n[13 Feb 2026] Nadia: @Ana Don't sweat it, there's no need to mark the pitch lines",
  "question": "Checking the chat at the end of February 17, 2026, has Ana broken the promise to mark the pitch lines?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q98c861dc04",
  "kind": "choice",
  "text": "Attached chat: the winter concert\nShared by: Kofi\n\nMembers: Elif, Malik, Kofi, Wren\nChat log (oldest first):\n[3 Sep 2026] Malik: Fingers crossed I can collect the sheet music by Thursday, September 10, 2026.\n[5 Sep 2026] Malik: @Elif Count on me to collect the sheet music by Saturday, September 12, 2026, if the voice test happens.\n[5 Sep 2026] Malik: @Elif I'll be sure to return the library scores by Monday, September 14, 2026.\n[7 Sep 2026] Wren: Update: the voice test is going ahead as planned.\n[8 Sep 2026] Malik: @Elif Any chance I can collect the sheet music by Wednesday, September 16, 2026 instead?\n[10 Sep 2026] Kofi: @Malik Yes, you have the green light to collect the sheet music by Wednesday, September 16, 2026.",
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
  "qid": "q9136c7330f",
  "kind": "choice",
  "text": "{\"item\": \"chat export\", \"matter\": \"the travel plans\", \"saved_by\": \"Sami\", \"layout\": \"plain\"}\n\nMembers: Sami, Rhea, Zara\nChat export (date | from | to | message):\n2026-02-15 | Rhea | Sami | Committing to fill the car boot by 22 Feb 2026.\n2026-02-15 | Sami | group | Thanks mate, noted.\n2026-02-18 | Sami | Zara | Guaranteed I'll check the passport copies by 25 Feb 2026.\n2026-02-20 | Sami | Rhea | Provided the ferry crossing happens, I will buy the packing cubes by 26 Feb 2026.\n2026-02-21 | Sami | Zara | I'll fetch the sunscreen by 2 Mar 2026 if the flight check-in goes ahead.\n2026-02-23 | Rhea | Sami | Mum, I did fill the car boot, haha.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Rhea's commitment to fill the car boot at the end of 26 Feb 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q4c25340c31",
  "kind": "choice",
  "text": "{\"record\": \"shared group chat\", \"subject\": \"the caring rota\", \"shared_by\": \"Ravi\", \"stored\": \"as text\"}\n\nMembers: Ivo, Priya, Tomas, Ravi\nChat log (oldest first):\n[7 Jan 2026] Ivo: @Priya Got it, I'll fetch the mobility aids by 16 Jan 2026 for sure.\n[9 Jan 2026] Ravi: I'll try to print the care schedule by 14 Jan 2026, no guarantee.\n[10 Jan 2026] Ravi: @Ivo I promise to print the care schedule by 15 Jan 2026.\n[13 Jan 2026] Tomas: @Ivo Provided the hospital appointment happens, I'll set up the medicine dispenser by 17 Jan 2026.\n[13 Jan 2026] Ravi: @Ivo Is it all right if I print the care schedule by 18 Jan 2026 instead?\n[14 Jan 2026] Priya: @Ravi I'll pick up the repeat prescription by 16 Jan 2026, providing the carer handover goes ahead.\n[15 Jan 2026] Tomas: @Ravi Relax, mate, you're not expected to print the care schedule\n[15 Jan 2026] Ravi: @Ivo Ticked off: print the care schedule, feels so good",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of 13 Jan 2026, what is the date by which Ravi has to print the care schedule, counting any agreed change?",
  "options": [
   "15 Jan 2026",
   "17 Jan 2026",
   "18 Jan 2026"
  ]
 },
 {
  "qid": "qb063064b6d",
  "kind": "choice",
  "text": "Plain copy of a family thread on the street watch scheme, passed on by Priya.\n\nMembers: Priya, Malik, Sami, Ana\nChat log (oldest first):\n[5 Apr 2026] Ana: @Malik It's on me to lend the stepladder by 8 Apr 2026.\n[7 Apr 2026] Ana: @Malik Quick question, could I lend the stepladder by 13 Apr 2026 instead?\n[8 Apr 2026] Sami: @Ana Revised deadline is 13 Apr 2026, so you can lend the stepladder.\n[8 Apr 2026] Sami: @Ana You don't have to lend the stepladder at all\n[12 Apr 2026] Malik: @Ana I promise to walk the old spaniel by 17 Apr 2026.\n[14 Apr 2026] Malik: @Sami As long as the parking permit visit is on, I will sweep the pavement outside by 18 Apr 2026.\n[14 Apr 2026] Sami: Lovely, the parking permit visit is definitely happening!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules, when is the date by which Ana has to lend the stepladder at the end of 21 Apr 2026, allowing for any agreed change?",
  "options": [
   "8 Apr 2026",
   "17 Apr 2026",
   "13 Apr 2026"
  ]
 },
 {
  "qid": "qf5a7030c18",
  "kind": "yes/no",
  "text": "Work conversation on the trade show push, saved as a file by Lena.\n\nMembers: Bruno, Greta, Jonas, Lena\nChat export (date | from | to | message):\n2026-03-08 | Lena | Bruno | Count on me to pay the printing invoice by 14 Mar 2026 if the product launch is on.\n2026-03-08 | Bruno | group | Ah right, thanks for that.\n2026-03-10 | Bruno | group | Sadly, the product launch won't go ahead.\n2026-03-10 | Greta | Jonas | Got it, I'll return the rented camera gear by 15 Mar 2026 for sure.\n2026-03-12 | Lena | Bruno | On my action item, may I pay the printing invoice by 19 Mar 2026 instead?\n2026-03-12 | Bruno | Lena | We are holding the date on record, so pay the printing invoice by it.",
  "question": "Under the rules on the card, is the promise Lena made to pay the printing invoice not broken at the end of 18 Mar 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q49d41dba8d",
  "kind": "choice",
  "text": "Subject: the guest review drive\nBelow is the group chat that Priya saved, unedited.\n\nMembers: Priya, Mo, Yuki\nChat export (date | from | to | message):\n2026-04-20 | Yuki | Mo | I'll wash the beach towels by 27 April 2026, providing the lettings photo shoot goes ahead.\n2026-04-20 | Yuki | Priya | If the guest arrival evening is on, I'll definitely fill the cleaning cupboard by 27 April 2026.\n2026-04-23 | Yuki | Mo | Absolutely, I will vacuum the holiday cottage by 25 April 2026.\n2026-04-24 | Priya | Mo | Lovely, I'll air the spare room by 28 April 2026 for sure.\n2026-04-24 | Priya | Mo | Quick question, could I air the spare room by 4 May 2026 instead?\n2026-04-26 | Mo | Priya | Of course, it is fine for you to air the spare room by 4 May 2026.\n2026-05-07 | Priya | Mo | Guess what, I managed to air the spare room!",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Priya to air the spare room at the end of 5 May 2026, counting any agreed change of date?",
  "options": [
   "25 April 2026",
   "4 May 2026",
   "28 April 2026"
  ]
 },
 {
  "qid": "q554955e31b",
  "kind": "choice",
  "text": "{\"source\": \"saved thread\", \"about\": \"the cellar project\", \"owner\": \"Leila\", \"kind\": \"chat export\"}\n\nMembers: Leila, Tess\nChat log (oldest first):\n[30 Apr 2026] Leila: @Tess Committing to replace the hallway bulbs by 2 May 2026.\n[3 May 2026] Tess: Not promising, but I'll try to tidy the boot room by 5 May 2026.\n[4 May 2026] Tess: @Leila Provided the heritage fete happens, I'll tidy the boot room by 7 May 2026.\n[4 May 2026] Tess: Brilliant news everyone, the heritage fete is a go!\n[4 May 2026] Tess: @Leila Might I ask whether I could tidy the boot room by 12 May 2026 instead?\n[12 May 2026] Tess: @Leila Ticked off: tidy the boot room, feels so good",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Tess made to tidy the boot room at the end of 7 May 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q56afbd126d",
  "kind": "choice",
  "text": "Subject: the family photo book, from the group chat\nSharing it here as Kofi saved it.\n\nMembers: Mo, Zara, Kofi\nChat log (oldest first):\n[1 Jul 2026] Zara: I'm aiming to fetch the craft box by Sunday, July 5, 2026, might manage it.\n[1 Jul 2026] Mo: @Zara Only if the puppet show is on, I will walk the dog by Thursday, July 9, 2026.\n[2 Jul 2026] Zara: @Mo You can bank on me to fetch the craft box by Wednesday, July 8, 2026.\n[3 Jul 2026] Mo: @Kofi Lovely, I'll read the bedtime story by Tuesday, July 7, 2026 if the storytime session is on.\n[7 Jul 2026] Kofi: @Zara No need to fetch the craft box, I'm letting you off\n[8 Jul 2026] Zara: @Mo Guess who managed to fetch the craft box, go team!",
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
  "qid": "q411668ea99",
  "kind": "choice",
  "text": "Chat from the support case covering the sponsor search, exported by Arlo.\n\nMembers: Elif, Kofi, Arlo\nChat export (date | from | to | message):\n2026-10-12 | Elif | Arlo | Count on me to set up the feed stop by 15 October 2026, if the hill climb happens.\n2026-10-12 | Elif | group | Scrapping the hill climb, apologies to all.\n2026-10-12 | Elif | Arlo | Can I set up the feed stop by 18 October 2026 instead? I did promise, sorry.\n2026-10-13 | Arlo | Elif | We are holding the date on record, so set up the feed stop by it.\n2026-10-13 | Elif | Arlo | I promise to service the tandem bike by 19 October 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Elif gave to set up the feed stop have at the end of 14 October 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not yet due",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qa9d35fff9d",
  "kind": "choice",
  "text": "Freelancer and client exchange about the documentary cut, saved by Hana.\n\nMembers: Sami, Hana, Mo\nChat log (oldest first):\n[28 Aug 2026] Mo: @Hana I will order the stock music licence by 1 Sep 2026.\n[29 Aug 2026] Sami: @Mo I will ship the hard drive by 3 Sep 2026 only if the agency review call happens.\n[30 Aug 2026] Mo: @Sami I promise to send the timeline export by 2 Sep 2026.\n[30 Aug 2026] Hana: @Mo Lovely, I'll upload the render files by 3 Sep 2026 if the festival premiere is on.\n[30 Aug 2026] Sami: We are dropping the festival premiere from the list.\n[1 Sep 2026] Sami: @Mo Forget it, you won't need to send the timeline export",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Mo made to send the timeline export, what state is it in at the end of 2 Sep 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Not triggered",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "qb2871091c3",
  "kind": "choice",
  "text": "Volunteers, Tomas shared this with you about the ground upgrade.\n\nMembers: Tomas, Oskar\nChat log (oldest first):\n[27 May 2026] Oskar: @Tomas Promise to fetch the medical bag by 3 June 2026 if the presentation evening goes ahead.\n[30 May 2026] Oskar: Sadly, the presentation evening won't go ahead.\n[1 Jun 2026] Oskar: @Tomas Would it be fine if I fetch the medical bag by 6 June 2026 instead, yeah?\n[2 Jun 2026] Oskar: @Tomas I promise to set up the corner flags by 7 June 2026 if the home derby is on.\n[2 Jun 2026] Tomas: @Oskar No, I'd like you to fetch the medical bag by the original date.\n[2 Jun 2026] Tomas: @Oskar Absolutely, I will wash the away kit by 7 June 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Oskar gave to fetch the medical bag have at the end of 3 June 2026?",
  "options": [
   "Waived",
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "qa4ce0a31cc",
  "kind": "choice",
  "text": "Neighbours and renters, the flat chat, exported by Priya, covering the summer lets season.\n\nMembers: Priya, Kai, Elif\nChat log (oldest first):\n[18 Jun 2026] Kai: @Priya I promise to wash the beach towels by Thursday, June 25, 2026.\n[20 Jun 2026] Kai: @Priya Would it be fine if I wash the beach towels by Tuesday, June 30, 2026 instead, yeah?\n[23 Jun 2026] Elif: @Kai Works for me, fine for you to wash the beach towels by Tuesday, June 30, 2026.\n[25 Jun 2026] Elif: @Priya If the owner handover visit is on, I'll definitely collect the bed linen by Saturday, July 4, 2026.\n[27 Jun 2026] Priya: @Kai Promise to fill the cleaning cupboard by Wednesday, July 1, 2026 if the lettings photo shoot goes ahead.\n[28 Jun 2026] Kai: @Priya Ticked off my list: wash the beach towels, yay.\n[30 Jun 2026] Kai: @Elif I'll be sure to restock the guest toiletries by Sunday, July 5, 2026.\n[3 Jul 2026] Priya: Sorry all, the owner handover visit is called off.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs things stand at the end of Sunday, June 28, 2026, which date is the deadline for Kai to wash the beach towels, with any agreed change applied?",
  "options": [
   "Saturday, July 4, 2026",
   "Tuesday, June 30, 2026",
   "Thursday, June 25, 2026"
  ]
 },
 {
  "qid": "qb69f67a12f",
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
  "qid": "qdf645242dc",
  "kind": "choice",
  "text": "Landlord and renters' group talk on the vegetable plot plan, from Kofi's export.\n\nMembers: Omar, Ivo, Kofi\nChat log (oldest first):\n[7 Mar 2026] Kofi: @Omar Provided the water tank delivery happens, I will fix the shed door by 15 Mar 2026.\n[8 Mar 2026] Omar: Great news, the water tank delivery is on!\n[9 Mar 2026] Ivo: @Omar Guaranteed I'll weed the carrot row by 18 Mar 2026.\n[9 Mar 2026] Ivo: @Omar To my relief, I managed to weed the carrot row.\n[15 Mar 2026] Kofi: @Omar Ta-da, I went and did it: fix the shed door!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Kofi's promise to fix the shed door at the end of 19 Mar 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q65fc66b8b8",
  "kind": "choice",
  "text": "Our flat chat about the allotment expansion, saved by Wren for whoever lives here.\n\nMembers: Ines, Mo, Wren\nChat log (oldest first):\n[18 Aug 2026] Ines: I'll see if I can stake the tomato canes by 24 August 2026.\n[19 Aug 2026] Wren: @Ines Count on me, I'll fix the shed door by 27 August 2026.\n[20 Aug 2026] Ines: @Wren Count on me to stake the tomato canes by 28 August 2026, if the plot inspection happens.\n[24 Aug 2026] Mo: @Wren Ah, no stress, no need for you to fix the shed door\n[24 Aug 2026] Ines: Team, the plot inspection stays on as booked.\n[28 Aug 2026] Ines: @Wren Is it all right if I stake the tomato canes by 2 September 2026 instead?\n[28 Aug 2026] Wren: @Ines Yes, you're welcome to stake the tomato canes by 2 September 2026 instead.\n[2 Sep 2026] Ines: @Wren Ticked off my list: stake the tomato canes, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat's the day Ines needs to stake the tomato canes by at the end of 8 September 2026, after any new date the group agreed on?",
  "options": [
   "27 August 2026",
   "28 August 2026",
   "2 September 2026"
  ]
 },
 {
  "qid": "q569fb5c345",
  "kind": "yes/no",
  "text": "Saved by Ana, this copy of the support chat concerns the league run.\n\nMembers: Ana, Lena, Tess\nChat log (oldest first):\n[29 May 2026] Lena: @Ana Only if the training camp is on, I will book the changing room by 1 June 2026.\n[30 May 2026] Tess: Great news, the training camp is on!\n[30 May 2026] Lena: @Ana I need to take back my commitment to book the changing room.\n[3 Jun 2026] Ana: @Lena Count on me, I'll print the team sheets by 10 June 2026.\n[6 Jun 2026] Lena: @Ana Forget it, you won't need to print the team sheets",
  "question": "By the close of 3 June 2026, is the promise Lena made to book the changing room kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc2c906d9b4",
  "kind": "yes/no",
  "text": "{\"record_type\": \"saved chat\", \"matter\": \"the caring rota\", \"by\": \"Femi\", \"stored\": \"as text\"}\n\nMembers: Femi, Hana, Zara\nChat log (oldest first):\n[23 Jun 2026] Zara: @Hana I'll fetch the mobility aids by 27 June 2026, provided the home assessment happens.\n[26 Jun 2026] Zara: Quick heads up, the home assessment is scrapped.\n[27 Jun 2026] Femi: @Hana I own this, I'll book the clinic transport by 4 July 2026.\n[27 Jun 2026] Hana: @Zara If the eye test is on, I'll definitely collect the post by 29 June 2026.\n[30 Jun 2026] Zara: @Femi No need to book the clinic transport, I'm letting you off\n[4 Jul 2026] Femi: @Hana Quick report: I've managed to book the clinic transport",
  "question": "Did Femi break the promise to book the clinic transport at the end of 5 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qcd7f123c42",
  "kind": "choice",
  "text": "Chat from the support case covering the mobile release, exported by Oskar.\n\nMembers: Oskar, Jonas, Tomas\nChat log (oldest first):\n[30 Sep 2026] Jonas: @Oskar Relax, I'll rotate the test keys by 7 Oct 2026 for sure.\n[1 Oct 2026] Jonas: @Oskar Provided the sprint demo happens, I'll fix the test runner by 5 Oct 2026.\n[2 Oct 2026] Tomas: @Oskar Hoping to label the bug reports by 5 Oct 2026, can't promise.\n[3 Oct 2026] Tomas: @Oskar I'll label the bug reports by 6 Oct 2026, promise.\n[4 Oct 2026] Tomas: Quick heads up, the sprint demo is scrapped.\n[6 Oct 2026] Jonas: @Tomas No worries, you don't need to label the bug reports",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Tomas made to label the bug reports, what state is it in at the end of 8 Oct 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "qbf58602402",
  "kind": "yes/no",
  "text": "Attached chat: the volunteer roster\nShared by: Dara\n\nMembers: Dara, Ravi, Hana\nChat export (date | from | to | message):\n2026-02-20 | Ravi | Dara | You can bet I'll wrap the prize hampers by Saturday, 28 February 2026.\n2026-02-22 | Dara | Hana | If the clothes swap goes ahead, I'll gladly label the raffle prizes by Friday, 27 February 2026.\n2026-02-22 | Hana | group | Ta, I saw this.\n2026-02-24 | Dara | group | Brilliant news everyone, the clothes swap is a go!\n2026-02-24 | Ravi | Dara | No worries, you don't need to label the raffle prizes\n2026-02-26 | Hana | Ravi | You are released, no requirement to wrap the prize hampers.",
  "question": "Per the rules on the card, at the end of Friday, 27 February 2026, has the promise Dara made to label the raffle prizes been broken?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5c6a4f5c25",
  "kind": "choice",
  "text": "Written between tenants and a landlord, this copy concerns the rent split plan. It was saved by Mo.\n\nMembers: Ines, Lee, Mo, Oskar\nChat log (oldest first):\n[13 Jun 2026] Mo: @Ines I promise to collect the parcel from porch by 17 June 2026.\n[13 Jun 2026] Lee: @Ines I promise to send the deposit receipt by 18 June 2026 if the house hunting viewing is on.\n[15 Jun 2026] Lee: @Mo Relax, mate, you're not expected to collect the parcel from porch\n[16 Jun 2026] Mo: Team, the house hunting viewing is not happening.\n[18 Jun 2026] Mo: @Ines Mum, I did collect the parcel from porch, haha.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Mo's promise to collect the parcel from porch sit at the end of 22 June 2026, exactly?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Kept",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "qb95f779eb1",
  "kind": "yes/no",
  "text": "Client thread on the holiday catalogue, shared by Wren for the project log.\n\nMembers: Wren, Lena, Hana, Oskar\nChat log (oldest first):\n[21 Jul 2026] Hana: @Wren Only if the site handover is on, I will fix the checkout button by Tuesday, 28 July 2026.\n[24 Jul 2026] Lena: @Wren Count on me, I'll update the product photos by Thursday, 30 July 2026.\n[24 Jul 2026] Lena: @Hana It's on me to test the mobile layout by Monday, 27 July 2026.\n[27 Jul 2026] Lena: Afraid the site handover is called off.\n[27 Jul 2026] Wren: @Lena Quick update: you do not need to test the mobile layout at all.\n[27 Jul 2026] Lena: @Hana Log entry: test the mobile layout, carried out",
  "question": "Is the promise to test the mobile layout kept by Lena as of Wednesday, 29 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q38401203c5",
  "kind": "yes/no",
  "text": "Work team channel\nSaved by Elif, which talks about the lab move.\n\nMembers: Dara, Elif, Ravi\nChat log (oldest first):\n[14 Jan 2026] Elif: Might be able to collect the lab samples by 23 Jan 2026, who knows!\n[16 Jan 2026] Elif: @Dara Promise to collect the lab samples by 22 Jan 2026 if the grant panel goes ahead.\n[17 Jan 2026] Elif: Really pleased to say the grant panel will go ahead!\n[19 Jan 2026] Ravi: @Elif Absolutely, I will order the reagent kit by 24 Jan 2026.\n[22 Jan 2026] Elif: @Dara Is it all right if I collect the lab samples by 25 Jan 2026 instead?\n[22 Jan 2026] Elif: @Dara Scratch what I said, I won't collect the lab samples.",
  "question": "Under the rules on the card, is the promise Elif made to collect the lab samples not broken at the end of 22 Jan 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe0a9cb524b",
  "kind": "yes/no",
  "text": "A written chat between housemates about the family photo book. Exported from the device by Kofi.\n\nMembers: Oskar, Kofi, Hana\nChat log (oldest first):\n[5 May 2026] Kofi: @Hana Might manage to walk the dog by 11 May 2026, who knows.\n[7 May 2026] Kofi: @Hana Provided the seaside outing happens, I'll walk the dog by 15 May 2026.\n[9 May 2026] Hana: @Oskar I will tidy the playroom by 11 May 2026.\n[10 May 2026] Oskar: Scrapping the seaside outing, apologies to all.\n[13 May 2026] Kofi: @Hana Is 21 May 2026 alright for me to walk the dog?\n[13 May 2026] Hana: @Kofi No, I'd like you to walk the dog by the original date.",
  "question": "Did Kofi break the promise to walk the dog at the end of 18 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd6ee126fea",
  "kind": "choice",
  "text": "Subject: the ground upgrade, chat copy\nPassed along by Arlo, with the full chat below.\n\nMembers: Tomas, Lena, Nadia, Arlo\nChat log (oldest first):\n[20 Jan 2026] Arlo: @Nadia You can bank on me to wash the away kit by 29 January 2026.\n[20 Jan 2026] Arlo: @Nadia Correction, I will not be able to wash the away kit.\n[21 Jan 2026] Tomas: @Arlo As long as the cup tie is on, I will set up the corner flags by 30 January 2026.\n[21 Jan 2026] Nadia: @Arlo Count on me to return the bib sets by 27 January 2026, if the training camp happens.\n[26 Jan 2026] Nadia: @Arlo Any chance I can return the bib sets by 2 February 2026 instead?\n[26 Jan 2026] Lena: @Nadia Yes, you can return the bib sets by 2 February 2026 if that suits you.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 31 January 2026, what status has Nadia's promise to return the bib sets got?",
  "options": [
   "Waived",
   "Not triggered",
   "Not yet due",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q0ce78b2cba",
  "kind": "yes/no",
  "text": "Saved by Zara: a freelancer's exchange with a client over the rebrand package.\n\nMembers: Zara, Sami, Femi\nChat log (oldest first):\n[14 Jun 2026] Zara: @Sami I'll export the logo files by June 16, 2026 as long as the gallery install is on.\n[14 Jun 2026] Femi: @Zara Guaranteed I'll upload the sticker artwork by June 17, 2026.\n[17 Jun 2026] Femi: @Zara Count on me to sketch the packaging mockup by June 21, 2026.\n[17 Jun 2026] Sami: @Femi You don't have to upload the sticker artwork at all\n[21 Jun 2026] Femi: @Zara Ticked off: sketch the packaging mockup, feels so good\n[21 Jun 2026] Femi: @Sami If the shop fitting goes ahead, I'll mail the business cards by June 26, 2026.",
  "question": "Going by the card's rules, does Femi keep the promise to sketch the packaging mockup at the end of June 21, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q20fe5859dd",
  "kind": "yes/no",
  "text": "Subject: the garden shed build, chat copy\nPassed along by Ines, with the full chat below.\n\nMembers: Tess, Lee, Ines\nChat log (oldest first):\n[25 Jan 2026] Lee: @Tess If the plot inspection goes ahead, I'll weed the carrot row by 30 January 2026.\n[28 Jan 2026] Tess: @Lee I'll sow the broad beans by 1 February 2026 if the harvest supper goes ahead.\n[28 Jan 2026] Ines: Fab, we are on for the plot inspection as planned!\n[29 Jan 2026] Ines: @Lee It's on me to stake the tomato canes by 7 February 2026.\n[30 Jan 2026] Tess: @Lee Got it, I'll water the allotment beds by 5 February 2026 for sure.\n[30 Jan 2026] Lee: @Tess Sorry, I won't weed the carrot row after all",
  "question": "Under the rules on the card, is it true that Lee has not kept the promise to weed the carrot row as of 4 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q64e9aa005d",
  "kind": "choice",
  "text": "Omar shared this support thread, which is about the guest list.\n\nMembers: Omar, Dara, Nadia\nChat export (date | from | to | message):\n2026-10-10 | Omar | Dara | Promise to fetch the spare memory cards by 18 October 2026 if the venue visit goes ahead.\n2026-10-14 | Nadia | Omar | I'll return the lighting stands by 18 October 2026, providing the engagement shoot goes ahead.\n2026-10-14 | Omar | Dara | Lovely, I'll pick up the album prints by 17 October 2026 for sure.\n2026-10-14 | Dara | group | Appreciate you telling me.\n2026-10-14 | Omar | Dara | Mind giving me until 20 October 2026 to pick up the album prints?\n2026-10-15 | Nadia | Omar | Yes, you're welcome to pick up the album prints by 20 October 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Omar made to pick up the album prints have at the end of 18 October 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qb6c7e74f5a",
  "kind": "choice",
  "text": "Shared by Leila for the committee, this is the group chat on the training plan.\n\nMembers: Leila, Ana, Malik\nChat log (oldest first):\n[17 Aug 2026] Malik: @Leila Lovely, I'll pump the spare tyres by 20 Aug 2026 for sure.\n[21 Aug 2026] Leila: @Ana Promise to service the tandem bike by 24 Aug 2026 if the bike check goes ahead.\n[23 Aug 2026] Leila: Yep, the bike check is on as planned.\n[24 Aug 2026] Leila: @Ana Committing to fetch the bike stand by 1 Sep 2026.\n[24 Aug 2026] Leila: @Ana Guess who managed to service the tandem bike, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Leila's promise to service the tandem bike at the end of 24 Aug 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qcd9729c0aa",
  "kind": "yes/no",
  "text": "{\"chat\": \"exported\", \"about\": \"the field survey\", \"saved_by\": \"Ines\", \"medium\": \"text\"}\n\nMembers: Dara, Ines, Zara, Kofi\nChat export (date | from | to | message):\n2026-09-20 | Zara | Dara | Hoping to book the microscope slot by 30 Sep 2026, no promises.\n2026-09-22 | Zara | Ines | If the conference trip is on, I'll definitely book the microscope slot by 29 Sep 2026.\n2026-09-22 | Zara | Ines | Got it, I'll collect the lab samples by 30 Sep 2026 for sure.\n2026-09-23 | Kofi | Zara | Guaranteed I'll fetch the grant forms by 25 Sep 2026.\n2026-09-23 | Kofi | group | We are dropping the conference trip from the list.\n2026-09-24 | Dara | Ines | I will order the reagent kit by 27 Sep 2026.",
  "question": "Per the card's rules, on 2 Oct 2026, has Zara's promise to book the microscope slot been kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9eb6c9a741",
  "kind": "choice",
  "text": "Work team channel\nSaved by Tess, which talks about the platform rewrite.\n\nMembers: Lena, Greta, Tess\nChat log (oldest first):\n[25 Jun 2026] Lena: @Tess Count on me to merge the login branch by 1 Jul 2026.\n[29 Jun 2026] Lena: @Tess Lovely, I'll run the security scan by 6 Jul 2026 for sure.\n[1 Jul 2026] Greta: @Tess I assure you I'll write the release notes by 7 Jul 2026 if the sprint demo is on.\n[4 Jul 2026] Lena: @Tess For the record: I was able to run the security scan\n[6 Jul 2026] Tess: Update, the sprint demo will not take place.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Lena's promise to run the security scan have at the end of 9 Jul 2026?",
  "options": [
   "Kept",
   "Broken",
   "Waived",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qf811fd2912",
  "kind": "choice",
  "text": "Support case copy, filed for the street watch scheme\nSaved on record by Wren\n\nMembers: Hana, Zara, Tess, Wren\nChat log (oldest first):\n[23 Jun 2026] Zara: @Tess Lovely, I'll sweep the pavement outside by 29 Jun 2026 if the hedge trimming day is on.\n[25 Jun 2026] Zara: @Tess Relax, I'll take in the post by 28 Jun 2026, promise.\n[25 Jun 2026] Hana: @Tess Count on me to share the garden hose by 1 Jul 2026, if the bonfire night happens.\n[26 Jun 2026] Hana: @Zara I assure you I'll lend the stepladder by 2 Jul 2026 if the street litter clean is on.\n[27 Jun 2026] Zara: @Tess Forget what I said, I won't take in the post\n[28 Jun 2026] Wren: @Zara No worries, you don't need to take in the post",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of 29 Jun 2026, which status does Zara have for the promise to take in the post?",
  "options": [
   "Broken",
   "Kept",
   "Waived",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q44cbb44fa0",
  "kind": "yes/no",
  "text": "Here we plan the family day out together, and Greta saved this for the family.\n\nMembers: Malik, Oskar, Leila, Greta\nChat log (oldest first):\n[16 Jul 2026] Oskar: @Greta Relax, I'll sort the old photo albums by 2026-07-24 for sure.\n[17 Jul 2026] Leila: @Oskar Provided the storytime session happens, I will tidy the playroom by 2026-07-20.\n[19 Jul 2026] Greta: Update: the storytime session is going ahead as planned.\n[19 Jul 2026] Malik: @Greta Count on me to pack the picnic basket by 2026-07-23.\n[20 Jul 2026] Oskar: @Leila Relax, mate, you're not expected to tidy the playroom\n[21 Jul 2026] Leila: @Malik Ah, no stress, no need for you to pack the picnic basket",
  "question": "According to the rules on the card, does the promise Leila made to tidy the playroom have any status except broken at the end of 2026-07-25?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9bf6a3741f",
  "kind": "yes/no",
  "text": "Volunteers, here is the playground project thread that Tomas forwarded for us.\n\nMembers: Kofi, Tomas, Ana\nChat export (date | from | to | message):\n2026-02-01 | Tomas | group | See if I can collect the bake sale tins by 7 Feb 2026.\n2026-02-02 | Tomas | Kofi | Got it, I'll collect the bake sale tins by 10 Feb 2026 for sure.\n2026-02-04 | Ana | Kofi | I assure you I'll label the raffle prizes by 7 Feb 2026 if the governors meeting is on.\n2026-02-06 | Ana | group | Great news, the governors meeting is on!\n2026-02-06 | Ana | Tomas | Forget it, you won't need to collect the bake sale tins\n2026-02-11 | Tomas | Kofi | Log entry: collect the bake sale tins, carried out",
  "question": "Under the rules on the card, is the promise Tomas made to collect the bake sale tins in a status other than broken at the end of 12 Feb 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qdd04e27d49",
  "kind": "choice",
  "text": "Here's the flatmate chat that Femi saved, about the old house restoration.\n\nMembers: Kofi, Lena, Elif, Femi\nChat log (oldest first):\n[28 Mar 2026] Femi: @Kofi Count on me to mend the garden gate by 31 March 2026.\n[29 Mar 2026] Lena: @Elif I promise to bleed the attic radiators by 4 April 2026 if the heritage fete is on.\n[29 Mar 2026] Lena: Yep, the heritage fete is on as planned.\n[30 Mar 2026] Femi: @Kofi Would it be fine if I mend the garden gate by 4 April 2026 instead, yeah?\n[31 Mar 2026] Kofi: @Femi Not moving it, mend the garden gate by the existing date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhere does Lena stand on the promise to bleed the attic radiators at the end of 1 April 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Broken",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q2167fc3a98",
  "kind": "yes/no",
  "text": "Support thread for a help desk case, covering the family photo book, saved by Arlo.\n\nMembers: Rhea, Arlo, Hana\nChat log (oldest first):\n[20 Apr 2026] Rhea: @Arlo Provided the seaside outing happens, I'll read the bedtime story by 24 April 2026.\n[22 Apr 2026] Arlo: Sadly, the seaside outing won't go ahead.\n[23 Apr 2026] Rhea: Might be able to fetch the craft box by 28 April 2026, who knows!\n[24 Apr 2026] Rhea: @Hana Guaranteed I'll fetch the craft box by 29 April 2026.\n[29 Apr 2026] Arlo: @Rhea Ah, no stress, no need for you to fetch the craft box\n[3 May 2026] Rhea: @Hana Mum, I did fetch the craft box, haha.",
  "question": "On 30 April 2026, would you say Rhea kept the promise to fetch the craft box, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5bb00e5d55",
  "kind": "yes/no",
  "text": "Note on the support case\nWhat it covers: the training plan\nPulled by: Yuki\n\nMembers: Oskar, Bruno, Yuki, Tess\nChat log (oldest first):\n[10 Oct 2026] Yuki: @Bruno Might manage to set up the feed stop by 12 October 2026, who knows.\n[11 Oct 2026] Yuki: @Bruno If the mechanics clinic goes ahead, I'll set up the feed stop by 17 October 2026.\n[12 Oct 2026] Bruno: Sad to report that the mechanics clinic is off.\n[12 Oct 2026] Oskar: @Bruno I promise to tune the gear cables by 21 October 2026.\n[13 Oct 2026] Oskar: @Bruno Mate, I promised, may I tune the gear cables by 25 October 2026 instead?\n[19 Oct 2026] Bruno: @Oskar Yes, you have the green light to tune the gear cables by 25 October 2026.",
  "question": "Applying the rules on the card, has Yuki kept the promise to set up the feed stop as of 13 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qac4d2d2c29",
  "kind": "yes/no",
  "text": "Subject: Saved chat on the home adaptations\nHere is the export from Femi, for the record.\n\nMembers: Tomas, Hana, Femi\nChat log (oldest first):\n[18 Jul 2026] Femi: @Hana You can bet I'll drop off the hot meals by 21 July 2026.\n[19 Jul 2026] Femi: @Hana I regret to say that I shall not drop off the hot meals.\n[20 Jul 2026] Femi: @Tomas I'll print the care schedule by 26 July 2026, provided the home assessment happens.\n[25 Jul 2026] Hana: Afraid the home assessment is called off.\n[26 Jul 2026] Femi: @Tomas Is it all right if I print the care schedule by 1 August 2026 instead?\n[26 Jul 2026] Hana: @Femi Revised deadline is 1 August 2026, so you can print the care schedule.",
  "question": "Going by the card's rules, does Femi keep the promise to print the care schedule at the end of 27 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qfaf2c130ca",
  "kind": "yes/no",
  "text": "Volunteer chat export. Saved by Ivo, it covers the new repertoire.\n\nMembers: Femi, Hana, Ivo\nChat log (oldest first):\n[21 Apr 2026] Hana: @Femi I'll book the rehearsal room by 27 April 2026 if the joint concert goes ahead.\n[21 Apr 2026] Ivo: Yep, the joint concert is on as planned.\n[23 Apr 2026] Ivo: @Hana Got it, I'll fix the stand microphones by 28 April 2026 for sure.\n[24 Apr 2026] Hana: @Femi Any chance I can book the rehearsal room by 1 May 2026 instead?\n[27 Apr 2026] Ivo: @Hana No worries, you don't need to book the rehearsal room\n[30 Apr 2026] Hana: @Femi Ta-da, I went and did it: book the rehearsal room!",
  "question": "At the end of 29 April 2026, is Hana's promise to book the rehearsal room broken, waived, not triggered or not yet due, rather than kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q86343404ad",
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
  "qid": "q170caa4cee",
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
  "qid": "qa980b15a1e",
  "kind": "yes/no",
  "text": "Help desk export\nAbout: the reunion weekend\nCopied by: Arlo\n\nMembers: Jonas, Ana, Lena, Arlo\nChat log (oldest first):\n[4 Jul 2026] Arlo: @Lena No promises, but I'll aim to label the memory box by 17 Jul 2026.\n[6 Jul 2026] Lena: @Jonas I will make sure to order the cousin t-shirts by 11 Jul 2026.\n[6 Jul 2026] Arlo: @Ana Count on me to label the memory box by 14 Jul 2026 if the cousin brunch is on.\n[8 Jul 2026] Ana: @Lena Absolutely, I will print the family tree chart by 17 Jul 2026.\n[12 Jul 2026] Ana: Just so you know, the cousin brunch is on as scheduled.\n[12 Jul 2026] Arlo: @Ana Quick report: I've managed to label the memory box",
  "question": "Has Arlo kept the promise to label the memory box at the end of 13 Jul 2026, instead of broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf7350d8a51",
  "kind": "choice",
  "text": "Household group messages for the garden shed build were passed along by Malik.\n\nMembers: Omar, Malik, Tess\nChat log (oldest first):\n[27 Mar 2026] Omar: @Tess Count on me to water the allotment beds by 1 Apr 2026, if the harvest supper happens.\n[29 Mar 2026] Omar: @Malik Count on me, I'll build the compost bay by 2 Apr 2026.\n[29 Mar 2026] Tess: @Omar Only if the village flower show is on, I will stake the tomato canes by 4 Apr 2026.\n[31 Mar 2026] Tess: @Omar Don't sweat it, there's no need to build the compost bay\n[1 Apr 2026] Omar: @Malik To my relief, I managed to build the compost bay.\n[1 Apr 2026] Tess: We are dropping the village flower show from the list.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Omar's promise to build the compost bay at the end of 4 Apr 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "qef8bcaaff8",
  "kind": "choice",
  "text": "Plain copy of a family thread on the street watch scheme, passed on by Priya.\n\nMembers: Priya, Malik, Sami, Ana\nChat log (oldest first):\n[5 Apr 2026] Ana: @Malik It's on me to lend the stepladder by 8 Apr 2026.\n[7 Apr 2026] Ana: @Malik Quick question, could I lend the stepladder by 13 Apr 2026 instead?\n[8 Apr 2026] Priya: @Ana Revised deadline is 13 Apr 2026, so you can lend the stepladder.\n[8 Apr 2026] Sami: @Ana You don't have to lend the stepladder at all\n[12 Apr 2026] Malik: @Ana I promise to walk the old spaniel by 17 Apr 2026.\n[14 Apr 2026] Malik: @Sami As long as the parking permit visit is on, I will sweep the pavement outside by 18 Apr 2026.\n[14 Apr 2026] Sami: Lovely, the parking permit visit is definitely happening!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules, when is the date by which Ana has to lend the stepladder at the end of 21 Apr 2026, allowing for any agreed change?",
  "options": [
   "8 Apr 2026",
   "17 Apr 2026",
   "13 Apr 2026"
  ]
 }
]
