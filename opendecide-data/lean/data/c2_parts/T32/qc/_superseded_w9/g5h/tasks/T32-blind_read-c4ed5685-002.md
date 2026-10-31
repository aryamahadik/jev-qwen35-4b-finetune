# G5-H blind read (all free-form rows) T32-blind_read-c4ed5685-002 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T32/qc/g5h/answers/T32-blind_read-c4ed5685-002.json

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
  "qid": "qfd23b74270",
  "kind": "yes/no",
  "text": "Team channel: the office refit\nShared by: Zara.\n\nMembers: Leila, Ines, Omar, Zara\nChat log (oldest first):\n[9 Mar 2026] Leila: @Zara I will make sure to replace the kitchen filters by Wednesday, March 18, 2026.\n[12 Mar 2026] Omar: @Leila If the annual audit is on, I'll definitely fetch the parking permits by Tuesday, March 17, 2026.\n[13 Mar 2026] Omar: @Leila Nobody needs you to replace the kitchen filters, that's that\n[15 Mar 2026] Leila: Brilliant news everyone, the annual audit is a go!\n[20 Mar 2026] Omar: @Leila Got myself to fetch the parking permits lol.",
  "question": "As the rules on the card set out, is it the case that Omar has broken the promise to fetch the parking permits at the end of Wednesday, March 18, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q33288794f7",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the volunteer roster\nThis export from Mo is pasted in full for readers who want it.\n\nMembers: Kai, Oskar, Mo, Ines\nChat export (date | from | to | message):\n2026-04-05 | Oskar | Mo | You can bank on me to book the school hall by 12 April 2026.\n2026-04-05 | Mo | Ines | You can bet I'll label the raffle prizes by 9 April 2026.\n2026-04-07 | Kai | Oskar | Forget it, you won't need to book the school hall\n2026-04-10 | Mo | Ines | To my relief, I managed to label the raffle prizes.\n2026-04-10 | Mo | Kai | If the governors meeting is on, I'll definitely print the raffle tickets by 13 April 2026.\n2026-04-11 | Oskar | Ines | As long as the field day is on, I will set up the book stall by 14 April 2026.",
  "question": "Has Mo kept the promise to label the raffle prizes at the end of 12 April 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q672f94270f",
  "kind": "choice",
  "text": "Femi shared this back and forth with the client about the honeymoon album.\n\nMembers: Tomas, Priya, Femi\nChat log (oldest first):\n[17 Mar 2026] Femi: @Priya If the cake tasting goes ahead, I'll set up the backdrop frame by 25 Mar 2026.\n[17 Mar 2026] Femi: Team, the cake tasting is not happening.\n[21 Mar 2026] Femi: @Priya Relax, I'll pick up the album prints by 30 Mar 2026, promise.\n[23 Mar 2026] Femi: @Priya I'll be sure to print the seating cards by 26 Mar 2026.\n[26 Mar 2026] Priya: @Femi Don't sweat it, there's no need to print the seating cards",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Femi made to set up the backdrop frame at the end of 27 Mar 2026?",
  "options": [
   "Waived",
   "Broken",
   "Not yet due",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "q07660cf47c",
  "kind": "yes/no",
  "text": "Forwarded by Femi, this thread on the lodger house rules stays attached to the ticket.\n\nMembers: Malik, Femi, Tomas, Omar\nChat export (date | from | to | message):\n2026-04-02 | Omar | Tomas | Count on me to buy the washing powder by 5 April 2026.\n2026-04-04 | Omar | Tomas | On my action item, may I buy the washing powder by 7 April 2026 instead?\n2026-04-04 | Malik | Omar | I'll defrost the top freezer by 10 April 2026 as long as the lodger house supper is on.\n2026-04-05 | Tomas | Omar | Revised deadline is 7 April 2026, so you can buy the washing powder.\n2026-04-07 | Tomas | Omar | I will sort the recycling bags by 16 April 2026 only if the house insurance review happens.\n2026-04-09 | Tomas | group | Team, the lodger house supper stays on as booked.",
  "question": "At the end of 10 April 2026, does the promise Malik made to defrost the top freezer have any status except broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q13c5d728d5",
  "kind": "choice",
  "text": "Mo saved these replies from the agent on the flatmate contract terms.\n\nMembers: Kofi, Mo, Ravi, Rhea\nChat log (oldest first):\n[16 Mar 2026] Rhea: @Kofi I will send the deposit receipt by 22 Mar 2026.\n[16 Mar 2026] Rhea: @Kofi I'm withdrawing my promise to send the deposit receipt\n[16 Mar 2026] Mo: @Rhea Provided the gas safety inspection happens, I will ring the letting agent by 18 Mar 2026.\n[19 Mar 2026] Mo: @Ravi As long as the move in day is on, I'll scan the council tax letter by 21 Mar 2026.\n[19 Mar 2026] Mo: Yep, the move in day is on as planned.\n[22 Mar 2026] Kofi: @Rhea No worries, you don't need to send the deposit receipt",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Rhea's commitment to send the deposit receipt at the end of 25 Mar 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "qcd49d83d9a",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the garden shed build\nThis export from Kofi is pasted in full for readers who want it.\n\nMembers: Kofi, Tess, Zara, Hana\nChat log (oldest first):\n[5 Sep 2026] Kofi: @Zara Provided the village flower show happens, I will deliver the surplus runner beans by 8 Sep 2026.\n[6 Sep 2026] Zara: @Kofi Relax, I'll stake the tomato canes by 11 Sep 2026 for sure.\n[6 Sep 2026] Tess: @Hana Count on me to collect the seed potatoes by 9 Sep 2026.\n[6 Sep 2026] Tess: On track for the village flower show to happen as planned.\n[6 Sep 2026] Tess: @Kofi You are released, no requirement to deliver the surplus runner beans.\n[12 Sep 2026] Zara: @Kofi To note: I have managed to stake the tomato canes\n\nNote: Dates set anywhere in this chat can be shifted by Kofi at will, since they are only suggestions.",
  "question": "By the close of 6 Sep 2026, is the promise Kofi made to deliver the surplus runner beans kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q090385c8cd",
  "kind": "yes/no",
  "text": "Attached chat: the platform rewrite\nForwarded by: Arlo\n\nMembers: Ines, Arlo, Jonas\nChat log (oldest first):\n[21 Feb 2026] Arlo: @Jonas I promise to rotate the test keys by Sunday, March 1, 2026.\n[21 Feb 2026] Arlo: @Jonas Ta-da, I went and did it: rotate the test keys!\n[21 Feb 2026] Jonas: @Ines I will deploy the staging build by Monday, February 23, 2026.\n[22 Feb 2026] Jonas: @Ines Ta-da, I went and did it: deploy the staging build!\n[23 Feb 2026] Jonas: @Ines Count on me to update the dependency list by Wednesday, February 25, 2026, if the planning session happens.\n[24 Feb 2026] Arlo: @Jonas Count on me to fix the test runner by Thursday, March 5, 2026, if the penetration test happens.",
  "question": "According to the card's rules, is the promise Arlo made to rotate the test keys not kept as of Thursday, February 26, 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3a9e581c32",
  "kind": "choice",
  "text": "Read up on the speed bump plan, flatmates, as Lee exported it.\n\nMembers: Zara, Lee, Sami\nChat log (oldest first):\n[24 Sep 2026] Lee: Wish me luck, hoping to walk the old spaniel by 4 Oct 2026.\n[25 Sep 2026] Sami: @Lee If the speed camera survey is on, I'll definitely lock the side gate by 27 Sep 2026.\n[26 Sep 2026] Lee: @Zara I promise to walk the old spaniel by 3 Oct 2026.\n[26 Sep 2026] Lee: @Zara I'll feed the cat across the road by 5 Oct 2026 if the bonfire night goes ahead.\n[28 Sep 2026] Sami: @Lee Don't sweat it, there's no need to walk the old spaniel\n[4 Oct 2026] Lee: @Zara Guess what, I managed to walk the old spaniel!\n\nAdded by Lee: The chat export is an outdated snapshot, so whatever it lists may already have changed elsewhere.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Lee's promise to walk the old spaniel at the end of 3 Oct 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q93d7278346",
  "kind": "yes/no",
  "text": "Attached chat: the new term plans\nShared by: Omar\n\nMembers: Omar, Ines, Tess\nChat export (date | from | to | message):\n2026-01-15 | Tess | group | No promises, but I'll aim to book the school hall by 23 Jan 2026.\n2026-01-15 | Tess | Ines | I will wrap the prize hampers by 18 Jan 2026.\n2026-01-16 | Tess | Ines | Count on me to book the school hall by 24 Jan 2026, if the quiz night happens.\n2026-01-16 | Tess | Ines | Is it all right if I wrap the prize hampers by 20 Jan 2026 instead?\n2026-01-16 | Ines | Tess | Yes, lovely, you can wrap the prize hampers by 20 Jan 2026 instead!\n2026-01-19 | Tess | group | Sorry all, the quiz night is not happening.",
  "question": "Does the card classify Tess's promise to book the school hall as kept, instead of broken, waived, not triggered or not yet due, on 28 Jan 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7da031157c",
  "kind": "yes/no",
  "text": "Leila shared this channel export covering the onboarding flow for the team.\n\nMembers: Zara, Leila\nChat log (oldest first):\n[25 Jan 2026] Leila: @Zara Absolutely, I will rotate the test keys by 3 February 2026.\n[27 Jan 2026] Zara: @Leila Only if the server migration is on, I will restart the build server by 1 February 2026.\n[30 Jan 2026] Zara: Great news, the server migration is on!\n[31 Jan 2026] Zara: @Leila Any chance I can restart the build server by 7 February 2026 instead?\n[1 Feb 2026] Leila: @Zara You are released, no requirement to restart the build server.\n[1 Feb 2026] Zara: @Leila Forget it, you won't need to rotate the test keys",
  "question": "Was the promise to restart the build server from Zara kept on 31 January 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q45dff1d2ba",
  "kind": "yes/no",
  "text": "Messages with the letting agent about the attic conversion idea, saved by Hana for the rental file.\n\nMembers: Kofi, Femi, Hana, Nadia\nChat export (date | from | to | message):\n2026-07-30 | Nadia | Kofi | Lovely, I'll stock the spice rack by 4 August 2026 if the lodger house supper is on.\n2026-07-31 | Femi | Hana | You can bank on me to wipe the shared kitchen counter by 6 August 2026.\n2026-08-01 | Femi | Hana | I have to take back my promise to wipe the shared kitchen counter.\n2026-08-02 | Nadia | Kofi | I assure you I'll drop the parcel upstairs by 7 August 2026 if the house insurance review is on.\n2026-08-06 | Hana | group | Great news, the house insurance review is on!\n2026-08-07 | Kofi | Nadia | Ah, no stress, no need for you to drop the parcel upstairs",
  "question": "Is the promise to drop the parcel upstairs that Nadia made broken at the end of 6 August 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qce13594ee0",
  "kind": "choice",
  "text": "Subject: Chat about the trade show push\nBelow, with Nadia named as the source, is the chat as exported.\n\nMembers: Nadia, Mo, Priya\nChat export (date | from | to | message):\n2026-01-07 | Mo | Nadia | Promise to set up the analytics dashboard by 10 January 2026 if the trade fair stand goes ahead.\n2026-01-07 | Priya | group | Fab, we are on for the trade fair stand as planned!\n2026-01-08 | Nadia | Priya | Guaranteed I'll send the newsletter copy by 14 January 2026.\n2026-01-10 | Nadia | group | Update on your plan to set up the analytics dashboard?\n2026-01-10 | Priya | Nadia | I will make sure to collect the survey answers by 12 January 2026.\n2026-01-10 | Mo | Nadia | Quick report: I've managed to set up the analytics dashboard",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Mo made to set up the analytics dashboard at the end of 10 January 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not yet due",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "qb27051d463",
  "kind": "yes/no",
  "text": "Forwarded by Kofi, these tenant replies are about the student house hunt for the file.\n\nMembers: Kofi, Jonas, Mo, Wren\nChat log (oldest first):\n[24 May 2026] Kofi: @Mo I will make sure to ring the letting agent by 27 May 2026.\n[26 May 2026] Mo: @Kofi Provided the move in day happens, I'll return the bin rota by 29 May 2026.\n[26 May 2026] Wren: Yay, the move in day is all set to go!\n[28 May 2026] Kofi: @Wren I will make sure to forward the inventory photos by 5 Jun 2026.\n[1 Jun 2026] Mo: @Kofi Ticked off: return the bin rota, feels so good",
  "question": "Has Mo's promise to return the bin rota ended up broken, waived, not triggered or not yet due, instead of kept, as of 31 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q796598ca17",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the garden shed build\nThis export from Kofi is pasted in full for readers who want it.\n\nMembers: Kofi, Tess, Zara, Hana\nChat log (oldest first):\n[5 Sep 2026] Kofi: @Zara Provided the village flower show happens, I will deliver the surplus runner beans by 8 Sep 2026.\n[6 Sep 2026] Zara: @Kofi Relax, I'll stake the tomato canes by 11 Sep 2026 for sure.\n[6 Sep 2026] Tess: @Hana Count on me to collect the seed potatoes by 9 Sep 2026.\n[6 Sep 2026] Tess: On track for the village flower show to happen as planned.\n[6 Sep 2026] Tess: @Kofi You are released, no requirement to deliver the surplus runner beans.\n[12 Sep 2026] Zara: @Kofi To note: I have managed to stake the tomato canes",
  "question": "Applying the card's rules, does Kofi's promise to deliver the surplus runner beans count as broken, waived, not triggered or not yet due, rather than kept, as of 6 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7592aeab5d",
  "kind": "yes/no",
  "text": "Priya shared this family chat about the packing plan for the relatives.\n\nMembers: Priya, Ines, Kai, Malik\nChat export (date | from | to | message):\n2026-07-30 | Malik | Kai | I'll return the rental car keys by 6 Aug 2026, promise.\n2026-08-01 | Ines | Malik | You can bet I'll print the boarding passes by 4 Aug 2026.\n2026-08-01 | Malik | group | Got it, cheers!\n2026-08-03 | Malik | Ines | No need to print the boarding passes, I'm letting you off\n2026-08-05 | Ines | Kai | If the family cookout goes ahead, I'll send the packing list by 10 Aug 2026.\n2026-08-06 | Kai | group | Scrapping the family cookout, apologies to all.",
  "question": "Is the promise Ines made to print the boarding passes not kept by 3 Aug 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q256b3c447d",
  "kind": "choice",
  "text": "Subject: Chat about the documentary cut\nThe copy from Leila follows below as a plain record.\n\nMembers: Yuki, Leila, Rhea, Hana\nChat export (date | from | to | message):\n2026-01-08 | Hana | Rhea | If the shoot day goes ahead, I'll upload the render files by Thursday, 15 January 2026.\n2026-01-08 | Rhea | group | Really pleased to say the shoot day will go ahead!\n2026-01-11 | Hana | Rhea | Committing to ship the hard drive by Tuesday, 20 January 2026.\n2026-01-13 | Yuki | Hana | Good news, you're let off having to upload the render files\n2026-01-16 | Hana | Rhea | Guess who managed to upload the render files, go team!",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Hana's promise to upload the render files have at the end of Thursday, 15 January 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not triggered",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q0749cfe2c6",
  "kind": "yes/no",
  "text": "Arlo forwarded this support chat, which is about the spring campaign.\n\nMembers: Leila, Lee, Arlo\nChat export (date | from | to | message):\n2026-02-08 | Arlo | Lee | I'll be sure to return the rented camera gear by February 16, 2026.\n2026-02-10 | Arlo | Lee | If the influencer call is on, I'll definitely draft the press release by February 15, 2026.\n2026-02-12 | Lee | Arlo | No need to return the rented camera gear, I'm letting you off\n2026-02-13 | Lee | group | On track for the influencer call to happen as planned.\n2026-02-13 | Lee | Arlo | You are released, no requirement to draft the press release.",
  "question": "Applying the card's rules, does Arlo's promise to draft the press release count as kept, rather than broken, waived, not triggered or not yet due, as of February 18, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q40c807e53a",
  "kind": "choice",
  "text": "Parents and cousins, this is where we sort out the garden shed build. Saved by Dara.\n\nMembers: Greta, Dara, Yuki\nChat log (oldest first):\n[3 Jun 2026] Yuki: @Greta Count on me to stake the tomato canes by June 8, 2026 if the seed swap day is on.\n[6 Jun 2026] Greta: @Dara Count on me, I'll dig the potato patch by June 15, 2026.\n[6 Jun 2026] Yuki: Please note the seed swap day will proceed.\n[8 Jun 2026] Yuki: @Greta Quick question, could I stake the tomato canes by June 13, 2026 instead?\n[8 Jun 2026] Dara: @Yuki You are released, no requirement to stake the tomato canes.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Yuki's promise to stake the tomato canes at the end of June 8, 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qd62ecfcf65",
  "kind": "choice",
  "text": "Yo flatmates, Greta shared this chat about the guest welcome plan, so chip in.\n\nMembers: Jonas, Leila, Omar, Greta\nChat log (oldest first):\n[4 Sep 2026] Jonas: @Leila Only if the summer season launch is on, I will wash the beach towels by 7 September 2026.\n[7 Sep 2026] Omar: @Greta Count on me to vacuum the holiday cottage by 11 September 2026, if the check out clean happens.\n[8 Sep 2026] Leila: @Jonas Relax, I'll collect the bed linen by 12 September 2026, promise.\n[8 Sep 2026] Leila: @Jonas Is 15 September 2026 alright for me to collect the bed linen?\n[11 Sep 2026] Greta: @Leila Nobody needs you to collect the bed linen, that's that",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Leila made to collect the bed linen at the end of 12 September 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Broken",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "qc25d9016d3",
  "kind": "choice",
  "text": "Shared by Leila, this is where the speed bump plan gets planned.\n\nMembers: Lena, Leila, Greta, Hana\nChat log (oldest first):\n[26 Aug 2026] Hana: @Lena I'll be sure to take in the post by 30 Aug 2026.\n[26 Aug 2026] Lena: Hoping to bring the bins in by 30 Aug 2026, no promises.\n[28 Aug 2026] Lena: @Hana Absolutely, I will bring the bins in by 31 Aug 2026.\n[31 Aug 2026] Lena: @Hana For the record: I was able to bring the bins in\n[31 Aug 2026] Leila: @Greta As long as the street litter clean is on, I'll clear the hedge trimmings by 8 Sep 2026.\n[7 Sep 2026] Lena: Sorry, the street litter clean is off.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Lena's commitment to bring the bins in is in what status at the end of 30 Aug 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Waived",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q61ea60fcf0",
  "kind": "choice",
  "text": "Committee chat on the volunteer roster, shared by Kofi with the volunteers.\n\nMembers: Arlo, Kofi, Malik, Rhea\nChat export (date | from | to | message):\n2026-02-19 | Malik | Kofi | I'll return the borrowed trestle tables by Thursday, 26 February 2026, providing the reading festival goes ahead.\n2026-02-23 | Malik | Arlo | I'm aiming to label the raffle prizes by Monday, 2 March 2026, might manage it.\n2026-02-25 | Malik | Rhea | Ticket's mine, I'll label the raffle prizes by Tuesday, 3 March 2026.\n2026-02-27 | Malik | Arlo | You can bank on me to collect the bake sale tins by Sunday, 1 March 2026.\n2026-02-27 | Malik | Rhea | Promise to wrap the prize hampers by Sunday, 1 March 2026 if the quiz night goes ahead.\n2026-02-28 | Malik | Rhea | Is it all right if I label the raffle prizes by Saturday, 7 March 2026 instead?\n2026-03-02 | Rhea | Malik | Yes, you're welcome to label the raffle prizes by Saturday, 7 March 2026 instead.\n2026-03-06 | Malik | Rhea | Mum, I did label the raffle prizes, haha.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Malik to label the raffle prizes at the end of Monday, 2 March 2026, counting any agreed change of date?",
  "options": [
   "Saturday, 7 March 2026",
   "Sunday, 1 March 2026",
   "Tuesday, 3 March 2026"
  ]
 },
 {
  "qid": "qf8bc95b84f",
  "kind": "choice",
  "text": "Subject: Chat about the documentary cut\nBelow, with Malik named as the source, is the chat as exported.\n\nMembers: Malik, Arlo, Jonas, Rhea\nChat log (oldest first):\n[22 Jul 2026] Malik: @Rhea I promise to send the colour notes by 25 Jul 2026 if the client screening is on.\n[22 Jul 2026] Malik: @Jonas I own this, I'll ship the hard drive by 26 Jul 2026.\n[24 Jul 2026] Jonas: @Malik Count on me to back up the project drives by 31 Jul 2026 if the shoot day is on.\n[25 Jul 2026] Malik: @Rhea On my action item, may I send the colour notes by 27 Jul 2026 instead?\n[25 Jul 2026] Jonas: @Malik Yes, you're welcome to send the colour notes by 27 Jul 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Malik's pledge to send the colour notes sit at the end of 26 Jul 2026?",
  "options": [
   "Kept",
   "Broken",
   "Waived",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "qa2373d5f74",
  "kind": "yes/no",
  "text": "Forwarded by Femi, this thread on the lodger house rules stays attached to the ticket.\n\nMembers: Malik, Femi, Tomas, Omar\nChat export (date | from | to | message):\n2026-04-02 | Omar | Tomas | Count on me to buy the washing powder by 5 April 2026.\n2026-04-04 | Omar | Tomas | On my action item, may I buy the washing powder by 7 April 2026 instead?\n2026-04-04 | Malik | Omar | I'll defrost the top freezer by 10 April 2026 as long as the lodger house supper is on.\n2026-04-05 | Tomas | Omar | Revised deadline is 7 April 2026, so you can buy the washing powder.\n2026-04-07 | Tomas | Omar | I will sort the recycling bags by 16 April 2026 only if the house insurance review happens.\n2026-04-09 | Tomas | group | Team, the lodger house supper stays on as booked.",
  "question": "Is it right to say that Malik has broken the promise to defrost the top freezer at the end of 10 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb9c1def058",
  "kind": "choice",
  "text": "Subject: Saved thread about the online store move\nThis export came from Ana and is pasted in full below.\n\nMembers: Rhea, Ana, Ivo, Lee\nChat log (oldest first):\n[18 Aug 2026] Rhea: @Ana As long as the site handover is on, I'll update the product photos by 23 August 2026.\n[20 Aug 2026] Rhea: Team, the site handover stays on as booked.\n[23 Aug 2026] Rhea: @Lee Ticket's mine, I'll add the size chart by 31 August 2026.\n[25 Aug 2026] Rhea: @Lee Gutted to say I won't add the size chart, sorry team\n[25 Aug 2026] Ivo: @Rhea Nobody needs you to add the size chart, that's that",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Rhea's commitment to add the size chart have at the end of 24 August 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Waived",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q267db88a50",
  "kind": "choice",
  "text": "Subject: Saved thread about the online store move\nThis export came from Ana and is pasted in full below.\n\nMembers: Rhea, Ana, Ivo, Lee\nChat log (oldest first):\n[18 Aug 2026] Rhea: @Ana As long as the site handover is on, I'll update the product photos by 23 August 2026.\n[20 Aug 2026] Rhea: Team, the site handover stays on as booked.\n[23 Aug 2026] Rhea: @Lee Ticket's mine, I'll add the size chart by 31 August 2026.\n[25 Aug 2026] Rhea: @Lee Gutted to say I won't add the size chart, sorry team\n[25 Aug 2026] Ivo: @Rhea Nobody needs you to add the size chart, that's that",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Rhea's commitment to add the size chart have at the end of 25 August 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Waived",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q1d3faaaa22",
  "kind": "yes/no",
  "text": "Attached chat: the shop rebuild\nShared by: Lena\n\nMembers: Lena, Sami, Femi, Tomas\nChat log (oldest first):\n[9 Sep 2026] Lena: @Tomas Committing to add the size chart by 16 September 2026.\n[14 Sep 2026] Tomas: @Sami If the site handover goes ahead, I'll gladly fix the checkout button by 21 September 2026.\n[15 Sep 2026] Lena: @Tomas Mate, I promised, may I add the size chart by 19 September 2026 instead?\n[16 Sep 2026] Tomas: @Lena Yes, you can add the size chart by 19 September 2026 if that suits you.\n[19 Sep 2026] Lena: Update, the site handover will not take place.",
  "question": "According to the rules on the card, does the promise Lena made to add the size chart have any status except broken at the end of 18 September 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qee58de1693",
  "kind": "choice",
  "text": "Here is the plan for the loft conversion, saved by Lena for the group.\n\nMembers: Ivo, Greta, Oskar, Lena\nChat export (date | from | to | message):\n2026-01-26 | Oskar | group | Will attempt to collect the sanding pads by Saturday, 31 January 2026, can't promise.\n2026-01-28 | Oskar | Lena | I promise to collect the sanding pads by Tuesday, 3 February 2026.\n2026-02-01 | Oskar | Lena | Think Thursday, 5 February 2026 would work if I collect the sanding pads instead?\n2026-02-01 | Greta | Oskar | Ticket's mine, I'll sweep the dust from stairs by Sunday, 8 February 2026.\n2026-02-02 | Lena | Oskar | I will pay the plumbing invoice by Monday, 9 February 2026 only if the builder quote meeting happens.\n2026-02-02 | Greta | Oskar | Yes, you can collect the sanding pads by Thursday, 5 February 2026 if that suits you.\n2026-02-02 | Ivo | Oskar | Relax, mate, you're not expected to collect the sanding pads\n2026-02-02 | Oskar | Ivo | I'll fetch the paint samples by Monday, 9 February 2026 as long as the kitchen fitting day is on.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen does Oskar have to collect the sanding pads by, at the end of Monday, 2 February 2026, once any agreed date change is included?",
  "options": [
   "Tuesday, 3 February 2026",
   "Thursday, 5 February 2026",
   "Sunday, 8 February 2026"
  ]
 },
 {
  "qid": "q0ee941acdc",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the cellar project\nThis export from Ana is pasted in full for readers who want it.\n\nMembers: Lena, Jonas, Ana\nChat log (oldest first):\n[12 Sep 2026] Lena: @Ana Count on me to wash the sash windows by 18 Sep 2026 if the loft clearance day is on.\n[15 Sep 2026] Ana: @Jonas I will make sure to mend the garden gate by 17 Sep 2026.\n[16 Sep 2026] Ana: @Jonas Ticked off: mend the garden gate, feels so good\n[17 Sep 2026] Lena: @Jonas If the heritage fete goes ahead, I'll clear the kitchen sink by 21 Sep 2026.\n[19 Sep 2026] Lena: Great news, the heritage fete is on!\n[20 Sep 2026] Lena: @Jonas To my relief, I managed to clear the kitchen sink.",
  "question": "Under the rules on the card, is it true that Lena has not kept the promise to clear the kitchen sink as of 23 Sep 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa36b7b5d42",
  "kind": "choice",
  "text": "Our flat chat about the vegetable plot plan, saved by Mo for whoever lives here.\n\nMembers: Ines, Malik, Mo, Ana\nChat log (oldest first):\n[23 Mar 2026] Mo: @Ana Count on me to water the allotment beds by 28 Mar 2026 if the allotment site visit is on.\n[23 Mar 2026] Ines: Lovely, the allotment site visit is definitely happening!\n[23 Mar 2026] Mo: @Ana Can I water the allotment beds by 30 Mar 2026 instead? I did promise, sorry.\n[23 Mar 2026] Ana: @Mo Nah, that deadline counts, mate, so please water the allotment beds!\n[24 Mar 2026] Mo: @Ines You can bank on me to weed the carrot row by 1 Apr 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 23 Mar 2026, what status has Mo's promise to water the allotment beds got?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q2f3ba94995",
  "kind": "choice",
  "text": "Greta saved this so we stay on the same page about the quiet street fund, mates.\n\nMembers: Ines, Greta, Arlo, Zara\nChat log (oldest first):\n[31 Oct 2026] Arlo: I'll try to take in the post by 9 Nov 2026, no promises.\n[2 Nov 2026] Arlo: @Ines Count on me, I'll take in the post by 8 Nov 2026.\n[2 Nov 2026] Greta: @Ines I will clear the hedge trimmings by 6 Nov 2026.\n[5 Nov 2026] Arlo: @Greta If the hedge trimming day goes ahead, I'll return the ladders by 12 Nov 2026.\n[7 Nov 2026] Zara: @Arlo Provided the speed camera survey happens, I'll feed the cat across the road by 12 Nov 2026.\n[8 Nov 2026] Arlo: @Ines Ticked off: take in the post, feels so good",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Arlo made to take in the post at the end of 13 Nov 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Broken",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "qc067a4c1d7",
  "kind": "choice",
  "text": "Yo flatmates, Rhea shared this chat about the flatmate contract terms, so chip in.\n\nMembers: Kai, Priya, Elif, Rhea\nChat log (oldest first):\n[23 Sep 2026] Elif: @Rhea Might manage to print the tenancy agreement by 26 Sep 2026, who knows.\n[24 Sep 2026] Elif: @Priya You can bank on me to print the tenancy agreement by 1 Oct 2026.\n[27 Sep 2026] Priya: @Kai Ticket's mine, I'll copy the house keys by 5 Oct 2026.\n[27 Sep 2026] Elif: @Priya Is it all right if I print the tenancy agreement by 6 Oct 2026 instead?\n[27 Sep 2026] Kai: @Elif Of course, it is fine for you to print the tenancy agreement by 6 Oct 2026.\n[29 Sep 2026] Rhea: @Elif I'll collect the parcel from porch by 4 Oct 2026, providing the check in visit goes ahead.\n[1 Oct 2026] Elif: @Priya Ta-da, I went and did it: print the tenancy agreement!\n[2 Oct 2026] Priya: Great news, the check in visit is on!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo what's the latest day Elif has to print the tenancy agreement by at the end of 4 Oct 2026, given any new date people agreed to?",
  "options": [
   "6 Oct 2026",
   "1 Oct 2026",
   "5 Oct 2026"
  ]
 },
 {
  "qid": "q7a3707aa90",
  "kind": "yes/no",
  "text": "Committee chat on the new term plans, shared by Lee with the volunteers.\n\nMembers: Kofi, Lee, Wren\nChat export (date | from | to | message):\n2026-03-23 | Lee | Kofi | Relax, I'll count the donation boxes by 29 Mar 2026, promise.\n2026-03-26 | Wren | Lee | Count on me to fetch the tea urn by 30 Mar 2026 if the quiz night is on.\n2026-03-27 | Lee | Kofi | My sincere apologies, I am unable to count the donation boxes.\n2026-03-28 | Kofi | Lee | Quick update: you do not need to count the donation boxes at all.\n2026-03-29 | Kofi | group | Scrapping the quiz night, apologies to all.",
  "question": "Has Lee kept the promise to count the donation boxes at the end of 31 Mar 2026, instead of broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qdd305c464c",
  "kind": "yes/no",
  "text": "Team channel: the social media plan\nShared by Tomas.\n\nMembers: Arlo, Greta, Tomas\nChat export (date | from | to | message):\n2026-10-13 | Greta | Tomas | I'll book the photo studio by 21 Oct 2026, promise.\n2026-10-15 | Greta | Tomas | Committing to set up the analytics dashboard by 19 Oct 2026.\n2026-10-15 | Greta | Tomas | I promise to collect the survey answers by 24 Oct 2026 if the annual review is on.\n2026-10-16 | Greta | Tomas | Mum, I did book the photo studio, haha.\n2026-10-20 | Greta | Tomas | Ticked off: set up the analytics dashboard, feels so good\n2026-10-20 | Arlo | group | Fab, we are on for the annual review as planned!",
  "question": "Did Greta keep the promise to book the photo studio as of 21 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4c82b6bf94",
  "kind": "yes/no",
  "text": "Lena shared this so the family follows the family photo book.\n\nMembers: Lena, Leila, Rhea\nChat log (oldest first):\n[28 May 2026] Lena: @Leila I promise to pick up the school bags by Tuesday, 2 June 2026.\n[29 May 2026] Leila: @Rhea Absolutely, I will walk the dog by Thursday, 4 June 2026.\n[30 May 2026] Lena: @Rhea I'll be sure to mend the kite string by Monday, 8 June 2026.\n[31 May 2026] Rhea: @Lena Lovely, I'll pack the picnic basket by Saturday, 6 June 2026 if the sleepover weekend is on.\n[3 Jun 2026] Lena: Update: the sleepover weekend is going ahead as planned.",
  "question": "Does Rhea's promise to pack the picnic basket hold up as kept at the end of Sunday, 7 June 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1aabc57526",
  "kind": "yes/no",
  "text": "Ravi shared this to pin down the garden makeover, housemates.\n\nMembers: Tomas, Tess, Ravi, Rhea\nChat export (date | from | to | message):\n2026-09-16 | Ravi | Tomas | I'll try to print the floor plan by 22 Sep 2026, no guarantee.\n2026-09-18 | Ravi | Rhea | Provided the boiler install visit happens, I will print the floor plan by 24 Sep 2026.\n2026-09-20 | Ravi | Tomas | I will scrape the old wallpaper by 27 Sep 2026.\n2026-09-23 | Tomas | group | On track for the boiler install visit to happen as planned.\n2026-09-24 | Rhea | Ravi | Quick update: you do not need to print the floor plan at all.\n2026-09-25 | Tomas | Ravi | No worries, you don't need to scrape the old wallpaper",
  "question": "Does Ravi's promise to print the floor plan hold up as kept at the end of 23 Sep 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qdbf9492b73",
  "kind": "choice",
  "text": "Team channel export, shared by Bruno, which is about the social media plan.\n\nMembers: Bruno, Femi, Ines\nChat export (date | from | to | message):\n2026-08-03 | Bruno | Ines | Only if the trade fair stand is on, I will fetch the campaign budget sheet by 2026-08-06.\n2026-08-04 | Ines | Bruno | It's on me to set up the analytics dashboard by 2026-08-13.\n2026-08-04 | Femi | group | Update: the trade fair stand is going ahead as planned.\n2026-08-05 | Bruno | Ines | Quick report: I've managed to fetch the campaign budget sheet\n2026-08-10 | Femi | Ines | No worries, you don't need to set up the analytics dashboard",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Bruno's promise to fetch the campaign budget sheet receive at the end of 2026-08-11?",
  "options": [
   "Waived",
   "Not triggered",
   "Not yet due",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q681971fdb9",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the rebrand package\nFrom Mo, the thread below is passed on in its original form.\n\nMembers: Tess, Mo\nChat export (date | from | to | message):\n2026-05-12 | Tess | Mo | I'll collect the photo credits by Wednesday, 20 May 2026, providing the gallery install goes ahead.\n2026-05-12 | Mo | Tess | Count on me to send the moodboard files by Friday, 22 May 2026.\n2026-05-16 | Mo | Tess | If the shop fitting is on, I'll definitely sketch the packaging mockup by Thursday, 21 May 2026.\n2026-05-17 | Mo | group | Quick heads up, the shop fitting is scrapped.\n2026-05-17 | Mo | Tess | Quick question, could I sketch the packaging mockup by Monday, 25 May 2026 instead?\n2026-05-18 | Tess | Mo | Fine by me, you can sketch the packaging mockup by Monday, 25 May 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Mo's undertaking to sketch the packaging mockup hold at the end of Wednesday, 20 May 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q81770d624c",
  "kind": "yes/no",
  "text": "Shared by Nadia, this back and forth with the client covers the sound mix.\n\nMembers: Femi, Greta, Nadia, Ravi\nChat export (date | from | to | message):\n2026-08-26 | Ravi | Femi | Only if the shoot day is on, I will label the clip folders by Tuesday, September 1, 2026.\n2026-08-28 | Femi | group | I'll try to ship the hard drive by Tuesday, September 1, 2026, can't promise!\n2026-08-28 | Femi | Ravi | I'll upload the render files by Tuesday, September 1, 2026 as long as the grading session is on.\n2026-08-29 | Femi | Greta | You can bank on me to ship the hard drive by Wednesday, September 2, 2026.\n2026-09-01 | Femi | Greta | Count on me to send the timeline export by Thursday, September 3, 2026.\n2026-09-02 | Femi | Greta | For the record: I was able to ship the hard drive",
  "question": "Was Femi's promise to ship the hard drive not kept as of Friday, September 4, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q32cb3d8ac2",
  "kind": "yes/no",
  "text": "Shared by Nadia, this back and forth with the client covers the sound mix.\n\nMembers: Femi, Greta, Nadia, Ravi\nChat export (date | from | to | message):\n2026-08-26 | Ravi | Femi | Only if the shoot day is on, I will label the clip folders by Tuesday, September 1, 2026.\n2026-08-28 | Femi | group | I'll try to ship the hard drive by Tuesday, September 1, 2026, can't promise!\n2026-08-28 | Femi | Ravi | I'll upload the render files by Tuesday, September 1, 2026 as long as the grading session is on.\n2026-08-29 | Femi | Greta | You can bank on me to ship the hard drive by Wednesday, September 2, 2026.\n2026-09-01 | Femi | Greta | Count on me to send the timeline export by Thursday, September 3, 2026.\n2026-09-02 | Femi | Greta | For the record: I was able to ship the hard drive",
  "question": "Is it true under the card's rules that Femi has kept the promise to ship the hard drive at the end of Friday, September 4, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5220664ed3",
  "kind": "yes/no",
  "text": "Chat attached to a support case about the holiday catalogue, shared by Ivo.\n\nMembers: Ivo, Kofi, Malik\nChat log (oldest first):\n[7 Aug 2026] Malik: @Ivo I assure you I'll add the size chart by 15 August 2026 if the stock count is on.\n[9 Aug 2026] Kofi: @Malik If the market day goes ahead, I'll gladly print the packing slips by 16 August 2026.\n[11 Aug 2026] Kofi: @Malik Ticket's mine, I'll set up the email forwarding by 18 August 2026.\n[16 Aug 2026] Kofi: @Malik I need to take back my commitment to set up the email forwarding.\n[16 Aug 2026] Ivo: @Kofi Please don't feel you have to set up the email forwarding\n[21 Aug 2026] Malik: Anything new on your way to set up the email forwarding?",
  "question": "Would you say the promise Kofi made to set up the email forwarding is not broken at the end of 20 August 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9a70075129",
  "kind": "choice",
  "text": "Kai saved this exchange with the client about the showreel refresh.\n\nMembers: Kai, Greta, Lena\nChat export (date | from | to | message):\n2026-08-22 | Lena | Kai | I own this, I'll label the clip folders by 31 August 2026.\n2026-08-26 | Greta | Lena | If the shoot day is on, I'll definitely fetch the raw footage by 31 August 2026.\n2026-08-27 | Greta | Lena | Got it, I'll send the timeline export by 4 September 2026 for sure.\n2026-08-28 | Lena | Greta | As long as the festival premiere is on, I will order the stock music licence by 1 September 2026.\n2026-08-30 | Kai | group | Lovely, the shoot day is definitely happening!\n2026-09-04 | Kai | Greta | Quick update: you do not need to send the timeline export at all.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Greta's promise to send the timeline export at the end of 9 September 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Not yet due",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q8f6601b5a1",
  "kind": "choice",
  "text": "Here is the quiet street fund, posted by Malik for the family to read.\n\nMembers: Malik, Wren, Bruno\nChat log (oldest first):\n[27 Oct 2026] Malik: @Bruno I will return the ladders by 1 November 2026 only if the speed camera survey happens.\n[30 Oct 2026] Wren: @Malik Count on me to bring the bins in by 2 November 2026.\n[31 Oct 2026] Bruno: Quick heads up, the speed camera survey is scrapped.\n[1 Nov 2026] Malik: @Wren Quick update: you do not need to bring the bins in at all.\n[1 Nov 2026] Malik: @Bruno Is 5 November 2026 alright for me to return the ladders?\n[1 Nov 2026] Bruno: @Malik Oh hun, I can't budge, so return the ladders by the old date!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Malik made to return the ladders at the end of 2 November 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Waived",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q02e622c9cb",
  "kind": "yes/no",
  "text": "Tomas shared this channel export covering the visitor policy for the team.\n\nMembers: Kai, Femi, Tomas\nChat log (oldest first):\n[28 Jun 2026] Kai: @Femi I assure you I'll fetch the parking permits by 7 Jul 2026 if the lease viewing is on.\n[1 Jul 2026] Tomas: Really pleased to say the lease viewing will go ahead!\n[1 Jul 2026] Tomas: @Kai I'll be sure to collect the visitor badges by 4 Jul 2026.\n[2 Jul 2026] Kai: @Tomas Count on me, I'll return the printer toner by 5 Jul 2026.\n[4 Jul 2026] Tomas: @Kai Ta-da, I went and did it: collect the visitor badges!",
  "question": "Under the rules on the card, is it true that Tomas has not kept the promise to collect the visitor badges as of 4 Jul 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q74eace323e",
  "kind": "yes/no",
  "text": "Our flat chat about the summer lets season, saved by Lee for whoever lives here.\n\nMembers: Lee, Ravi, Leila, Femi\nChat log (oldest first):\n[18 Mar 2026] Lee: @Leila If the check out clean goes ahead, I'll gladly vacuum the holiday cottage by 24 March 2026.\n[22 Mar 2026] Femi: On track for the check out clean to happen as planned.\n[22 Mar 2026] Femi: Hey, any luck with trying to vacuum the holiday cottage?\n[23 Mar 2026] Leila: @Lee I will collect the bed linen by 29 March 2026.\n[24 Mar 2026] Ravi: @Lee Don't sweat it, there's no need to vacuum the holiday cottage\n[29 Mar 2026] Ravi: @Leila Forget it, you won't need to collect the bed linen",
  "question": "According to the rules on the card, has Lee broken the promise to vacuum the holiday cottage at the end of 24 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc1c0abe7e2",
  "kind": "yes/no",
  "text": "Saved by Oskar, this talk about the garden shed build is just for family.\n\nMembers: Bruno, Oskar, Ines\nChat log (oldest first):\n[3 Feb 2026] Bruno: @Ines Count on me to stake the tomato canes by 7 February 2026, if the harvest supper happens.\n[3 Feb 2026] Ines: Thanks mate, noted.\n[3 Feb 2026] Bruno: On track for the harvest supper to happen as planned.\n[5 Feb 2026] Bruno: @Ines I will weed the carrot row by 9 February 2026.\n[9 Feb 2026] Bruno: @Ines Update on my side: I will not weed the carrot row, sorry.\n[10 Feb 2026] Bruno: @Ines Ticked off: stake the tomato canes, feels so good",
  "question": "Did Bruno keep the promise to stake the tomato canes as of 7 February 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4dda2dfcbb",
  "kind": "yes/no",
  "text": "Attached chat: the new term plans\nShared by: Omar\n\nMembers: Omar, Ines, Tess\nChat export (date | from | to | message):\n2026-01-15 | Tess | group | No promises, but I'll aim to book the school hall by 23 Jan 2026.\n2026-01-15 | Tess | Ines | I will wrap the prize hampers by 18 Jan 2026.\n2026-01-16 | Tess | Ines | Count on me to book the school hall by 24 Jan 2026, if the quiz night happens.\n2026-01-16 | Tess | Ines | Is it all right if I wrap the prize hampers by 20 Jan 2026 instead?\n2026-01-16 | Ines | Tess | Yes, lovely, you can wrap the prize hampers by 20 Jan 2026 instead!\n2026-01-19 | Tess | group | Sorry all, the quiz night is not happening.",
  "question": "At the end of 28 Jan 2026, is Tess's promise to book the school hall broken, waived, not triggered or not yet due, rather than kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3a8895dd9c",
  "kind": "yes/no",
  "text": "Leila shared this family chat about the allotment expansion for the relatives.\n\nMembers: Leila, Malik, Femi\nChat log (oldest first):\n[3 Feb 2026] Leila: @Femi Lovely, I'll sow the broad beans by 11 February 2026 for sure.\n[4 Feb 2026] Femi: @Leila As long as the village flower show is on, I'll water the allotment beds by 12 February 2026.\n[4 Feb 2026] Leila: Sorry all, the village flower show is called off.\n[7 Feb 2026] Leila: @Femi Is 14 February 2026 alright for me to sow the broad beans?\n[10 Feb 2026] Femi: @Leila Nah, the date's staying put, so you can sow the broad beans.\n[10 Feb 2026] Leila: @Femi Mum, I did sow the broad beans, haha.",
  "question": "Is the promise Leila made to sow the broad beans in a status other than broken at the end of 13 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q19e5c7ee73",
  "kind": "choice",
  "text": "Zara shared this exchange with the client about the guest list.\n\nMembers: Femi, Zara, Tomas\nChat log (oldest first):\n[8 Jan 2026] Zara: @Femi Fingers crossed I can send the sneak peek gallery by 2026-01-19.\n[10 Jan 2026] Zara: @Femi Got it, I'll send the sneak peek gallery by 2026-01-18 for sure.\n[15 Jan 2026] Zara: @Femi Count on me to pick up the album prints by 2026-01-20.\n[15 Jan 2026] Tomas: @Zara I'll book the assistant photographer by 2026-01-22 if the venue visit goes ahead.\n[18 Jan 2026] Tomas: @Zara Relax, mate, you're not expected to send the sneak peek gallery\n[21 Jan 2026] Zara: Really pleased to say the venue visit will go ahead!",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Zara's promise to send the sneak peek gallery have at the end of 2026-01-23?",
  "options": [
   "Kept",
   "Waived",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qa821f563f6",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the store makeover\nFrom Nadia, the thread below is passed on in its original form.\n\nMembers: Nadia, Leila\nChat log (oldest first):\n[5 Jul 2026] Nadia: @Leila I assure you I'll send the moodboard files by 11 Jul 2026 if the sign reveal is on.\n[5 Jul 2026] Leila: Thanks mate, noted.\n[6 Jul 2026] Leila: Sad to report that the sign reveal is off.\n[7 Jul 2026] Nadia: @Leila Any chance I can send the moodboard files by 17 Jul 2026 instead?\n[7 Jul 2026] Leila: @Nadia No new date, so please send the moodboard files by the date given.\n[8 Jul 2026] Leila: @Nadia I promise to pick the colour swatches by 18 Jul 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Nadia's commitment to send the moodboard files have at the end of 10 Jul 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Kept",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "qbf6f35cc13",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the quiet street fund\nThe chat below comes from Bruno, copied as is for reference.\n\nMembers: Ivo, Kofi, Bruno, Hana\nChat log (oldest first):\n[4 Aug 2026] Hana: @Ivo As long as the street litter clean is on, I'll clear the hedge trimmings by 7 Aug 2026.\n[4 Aug 2026] Ivo: Sadly, the street litter clean won't go ahead.\n[7 Aug 2026] Hana: @Bruno Lovely, I'll walk the old spaniel by 13 Aug 2026 if the parking permit visit is on.\n[7 Aug 2026] Hana: @Ivo I'll be sure to lend the stepladder by 13 Aug 2026.\n[7 Aug 2026] Hana: @Ivo Mate, I promised, may I clear the hedge trimmings by 12 Aug 2026 instead?\n[7 Aug 2026] Ivo: @Hana Nah, that deadline counts, mate, so please clear the hedge trimmings!",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Hana's promise to clear the hedge trimmings sit at the end of 10 Aug 2026, exactly?",
  "options": [
   "Broken",
   "Waived",
   "Kept",
   "Not yet due",
   "Not triggered"
  ]
 }
]
