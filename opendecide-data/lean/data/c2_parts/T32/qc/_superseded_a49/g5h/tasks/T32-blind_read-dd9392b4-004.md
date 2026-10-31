# G5-H blind read T32-blind_read-dd9392b4-004 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T32/qc/g5h/answers/T32-blind_read-dd9392b4-004.json

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
  "qid": "q81a6abac4e",
  "kind": "choice",
  "text": "Subject: copy of a chat on the cellar project\nPassing this along, with the chat text under it, from Omar.\n\nMembers: Mo, Tess, Omar\nChat log (oldest first):\n[26 Jan 2026] Mo: @Tess Count on me to clear the kitchen sink by 30 January 2026.\n[28 Jan 2026] Tess: @Omar Only if the chimney sweep visit is on, I will oil the back door hinges by 3 February 2026.\n[30 Jan 2026] Omar: Lovely, the chimney sweep visit is definitely happening!\n[31 Jan 2026] Tess: @Omar It's on me to scrub the cellar steps by 2 February 2026.\n[31 Jan 2026] Mo: @Tess You are released, no requirement to oil the back door hinges.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Tess made to oil the back door hinges at the end of 1 February 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Not yet due",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "qa70a0144ea",
  "kind": "yes/no",
  "text": "Shared by Rhea, this is where the speed bump plan gets planned.\n\nMembers: Ines, Rhea, Leila\nChat log (oldest first):\n[18 Jan 2026] Rhea: @Leila Only if the hedge trimming day is on, I will take in the post by 23 January 2026.\n[21 Jan 2026] Ines: @Rhea You can bank on me to return the ladders by 30 January 2026.\n[22 Jan 2026] Rhea: @Leila Count on me to lend the stepladder by 28 January 2026.\n[22 Jan 2026] Rhea: Scrapping the hedge trimming day, apologies to all.\n[23 Jan 2026] Ines: @Rhea Forget it, you won't need to lend the stepladder\n[28 Jan 2026] Leila: @Ines Don't sweat it, there's no need to return the ladders",
  "question": "At the end of 22 January 2026, does the promise Rhea made to take in the post have any status except broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbfa6a8df60",
  "kind": "choice",
  "text": "Shared by Priya, this freelance thread with a client is about the honeymoon album.\n\nMembers: Sami, Malik, Priya, Ana\nChat log (oldest first):\n[12 Aug 2026] Ana: @Priya As long as the cake tasting is on, I'll pick up the album prints by 20 Aug 2026.\n[13 Aug 2026] Ana: @Priya I'll be sure to print the seating cards by 21 Aug 2026.\n[14 Aug 2026] Malik: @Ana I promise to return the lighting stands by 17 Aug 2026.\n[15 Aug 2026] Priya: Sad to report that the cake tasting is off.\n[17 Aug 2026] Malik: @Ana Gutted to say I won't return the lighting stands, sorry team\n[19 Aug 2026] Malik: @Priya I own this, I'll send the sneak peek gallery by 22 Aug 2026.\n[19 Aug 2026] Malik: @Priya Would it be fine if I send the sneak peek gallery by 24 Aug 2026 instead, yeah?\n[21 Aug 2026] Ana: @Malik Yes, all good for you to send the sneak peek gallery by 24 Aug 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of 21 Aug 2026, what is the date by which Malik has to send the sneak peek gallery, counting any agreed change?",
  "options": [
   "17 Aug 2026",
   "22 Aug 2026",
   "24 Aug 2026"
  ]
 },
 {
  "qid": "q7db3576120",
  "kind": "choice",
  "text": "This shared chat of a family on the allotment expansion was saved by Tess for the record.\n\nMembers: Mo, Yuki, Tess, Kai\nChat log (oldest first):\n[4 Sep 2026] Yuki: @Mo If the allotment site visit goes ahead, I'll fix the shed door by 8 September 2026.\n[5 Sep 2026] Kai: @Yuki Relax, I'll water the allotment beds by 10 September 2026, promise.\n[5 Sep 2026] Yuki: @Kai You are released, no requirement to water the allotment beds.\n[5 Sep 2026] Tess: Great news, the allotment site visit is on!\n[8 Sep 2026] Kai: @Yuki Forget it, you won't need to fix the shed door",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Yuki made to fix the shed door is in which status at the end of 13 September 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Waived",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "qef65edd1fd",
  "kind": "yes/no",
  "text": "Omar shared this so the family follows the old house restoration.\n\nMembers: Omar, Elif, Nadia, Lena\nChat log (oldest first):\n[25 Oct 2026] Lena: @Omar I promise to wash the sash windows by 2 November 2026.\n[27 Oct 2026] Nadia: @Elif Provided the roof survey visit happens, I'll find the loft ladder by 1 November 2026.\n[28 Oct 2026] Lena: @Omar Quick question, could I wash the sash windows by 7 November 2026 instead?\n[28 Oct 2026] Elif: @Lena Quick update: you do not need to wash the sash windows at all.\n[31 Oct 2026] Omar: Sorry all, the roof survey visit is called off.\n[1 Nov 2026] Omar: Where are you up to with plans to wash the sash windows?",
  "question": "When you check the chat at the end of 7 November 2026, is the promise Lena made to wash the sash windows broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0db2216f74",
  "kind": "choice",
  "text": "Shared by Greta, an export of a household chat about the packing plan, as saved.\n\nMembers: Bruno, Oskar, Greta, Ravi\nChat export (date | from | to | message):\n2026-09-16 | Ravi | group | Not promising, but I'll try to collect the insurance papers by Monday, September 21, 2026.\n2026-09-17 | Ravi | Bruno | Provided the ferry crossing happens, I'll collect the insurance papers by Sunday, September 20, 2026.\n2026-09-17 | Ravi | group | Lovely, the ferry crossing is definitely happening!\n2026-09-19 | Ravi | Bruno | Mind giving me until Saturday, September 26, 2026 to collect the insurance papers?\n2026-09-19 | Oskar | Ravi | Yes, all good for you to collect the insurance papers by Saturday, September 26, 2026 instead.\n2026-09-25 | Bruno | Ravi | Ticket's mine, I'll check the passport copies by Wednesday, September 30, 2026.\n2026-09-28 | Bruno | Ravi | Is Friday, October 2, 2026 alright for me to check the passport copies?\n2026-09-28 | Ravi | Bruno | That suits me, so please check the passport copies by Friday, October 2, 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of Thursday, September 24, 2026, by what date does Ravi have to collect the insurance papers, counting any agreed change of date?",
  "options": [
   "Wednesday, September 30, 2026",
   "Saturday, September 26, 2026",
   "Sunday, September 20, 2026"
  ]
 },
 {
  "qid": "q668655dfbf",
  "kind": "choice",
  "text": "Tenant and landlord back-and-forth on the summer lets season, saved by Omar.\n\nMembers: Arlo, Omar, Mo, Hana\nChat log (oldest first):\n[28 Jun 2026] Arlo: Hoping to restock the guest toiletries by 1 July 2026, no promises.\n[29 Jun 2026] Arlo: @Mo Only if the lettings photo shoot is on, I will restock the guest toiletries by 7 July 2026.\n[1 Jul 2026] Mo: Please note the lettings photo shoot will proceed.\n[2 Jul 2026] Arlo: @Mo Is it all right if I restock the guest toiletries by 12 July 2026 instead?\n[2 Jul 2026] Omar: @Arlo Go ahead and restock the guest toiletries by 12 July 2026, that is fine.\n[3 Jul 2026] Hana: @Omar Relax, I'll collect the bed linen by 9 July 2026 for sure.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Arlo doing with the promise to restock the guest toiletries at the end of 10 July 2026?",
  "options": [
   "Kept",
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "qbe2bbccfad",
  "kind": "choice",
  "text": "Leila shared this channel export covering the platform rewrite for the team.\n\nMembers: Ravi, Greta, Leila\nChat log (oldest first):\n[12 Aug 2026] Leila: @Ravi I'll update the dependency list by 17 August 2026 as long as the hackathon is on.\n[12 Aug 2026] Leila: @Ravi If the penetration test is on, I'll definitely fix the test runner by 17 August 2026.\n[12 Aug 2026] Greta: @Ravi Count on me to review the pull request by 16 August 2026.\n[15 Aug 2026] Greta: @Ravi Can I review the pull request by 19 August 2026 instead? I did promise, sorry.\n[15 Aug 2026] Ravi: @Greta Yes, you can review the pull request by 19 August 2026 instead.\n[18 Aug 2026] Greta: @Ravi Apologies, I'll not be able to review the pull request",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Greta's commitment to review the pull request at the end of 14 August 2026?",
  "options": [
   "Waived",
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q4f9a670802",
  "kind": "choice",
  "text": "Here is the care plan, posted by Femi for the family to read.\n\nMembers: Nadia, Oskar, Arlo, Femi\nChat log (oldest first):\n[22 Sep 2026] Oskar: @Arlo Count on me to print the care schedule by 26 Sep 2026 if the eye test is on.\n[23 Sep 2026] Oskar: @Nadia Count on me to drop off the hot meals by 30 Sep 2026 if the home assessment is on.\n[23 Sep 2026] Femi: Please note the home assessment will proceed.\n[24 Sep 2026] Oskar: @Arlo Relax, I'll fetch the mobility aids by 29 Sep 2026, promise.\n[24 Sep 2026] Femi: @Oskar Relax, mate, you're not expected to fetch the mobility aids\n[29 Sep 2026] Oskar: @Nadia Quick question, could I drop off the hot meals by 3 Oct 2026 instead?\n[30 Sep 2026] Nadia: @Oskar Yes, you have the green light to drop off the hot meals by 3 Oct 2026.\n[1 Oct 2026] Oskar: @Nadia Guess who managed to drop off the hot meals, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 1 Oct 2026, by what date does Oskar have to drop off the hot meals, counting any agreed change of date?",
  "options": [
   "3 Oct 2026",
   "30 Sep 2026",
   "26 Sep 2026"
  ]
 },
 {
  "qid": "q9f57d6691a",
  "kind": "yes/no",
  "text": "Flatmates' thread\nExport of the kitchen refit, passed on by Yuki.\n\nMembers: Tess, Yuki, Malik\nChat log (oldest first):\n[29 Mar 2026] Tess: @Yuki Count on me to email the leak photos by 5 April 2026.\n[29 Mar 2026] Tess: @Malik I'll measure the kitchen for fridge by 4 April 2026 as long as the electrics safety check is on.\n[29 Mar 2026] Malik: Lovely, the electrics safety check is definitely happening!\n[31 Mar 2026] Malik: @Yuki If the boiler annual check goes ahead, I'll gladly read the meter readings by 3 April 2026.\n[31 Mar 2026] Yuki: @Tess It's on me to remove the bathroom shelf by 5 April 2026.\n[2 Apr 2026] Yuki: @Tess Gutted to say I won't remove the bathroom shelf, sorry team",
  "question": "Is Tess's promise to measure the kitchen for fridge broken at the end of 6 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q83737ed205",
  "kind": "yes/no",
  "text": "Shared by Mo for the committee, this is the group chat on the kit sponsorship.\n\nMembers: Jonas, Oskar, Femi, Mo\nChat log (oldest first):\n[31 Jul 2026] Femi: @Jonas I assure you I'll book the changing room by 7 August 2026 if the home derby is on.\n[1 Aug 2026] Femi: @Mo See if I can print the team sheets by 9 August 2026.\n[2 Aug 2026] Femi: @Mo Relax, I'll print the team sheets by 6 August 2026 for sure.\n[4 Aug 2026] Jonas: Sorry, the home derby is off.\n[6 Aug 2026] Femi: @Mo Got myself to print the team sheets lol.\n[8 Aug 2026] Mo: @Jonas I'll be sure to wash the away kit by 12 August 2026.",
  "question": "Is it true under the card's rules that Femi has kept the promise to print the team sheets at the end of 6 August 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q81be2f5ecf",
  "kind": "choice",
  "text": "{\"archive\": \"group chat\", \"subject\": \"the website relaunch\", \"sent_by\": \"Hana\"}\n\nMembers: Hana, Leila, Nadia, Greta\nChat export (date | from | to | message):\n2026-02-09 | Nadia | Hana | Lovely, I'll draft the press release by 11 February 2026 for sure.\n2026-02-10 | Hana | Nadia | As long as the trade fair stand is on, I will print the event banners by 15 February 2026.\n2026-02-10 | Greta | group | Sadly, the trade fair stand is not going ahead.\n2026-02-11 | Hana | Nadia | Is it all right if I print the event banners by 17 February 2026 instead?\n2026-02-11 | Greta | Hana | Yes, you can print the event banners by 17 February 2026 if that suits you.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Hana's undertaking to print the event banners hold at the end of 10 February 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "qa917aba08b",
  "kind": "choice",
  "text": "Here we plan the front garden scheme together, and Tess saved this for the family.\n\nMembers: Tomas, Kofi, Kai, Tess\nChat log (oldest first):\n[5 May 2026] Kai: @Tomas Lovely, I'll feed the cat across the road by 10 May 2026 for sure.\n[8 May 2026] Kai: @Tomas You can bet I'll bring the bins in by 15 May 2026.\n[9 May 2026] Tomas: @Kai You don't have to bring the bins in at all\n[9 May 2026] Kai: @Tomas Would it be fine if I feed the cat across the road by 13 May 2026 instead, yeah?\n[9 May 2026] Kofi: @Kai Yes, lovely, you can feed the cat across the road by 13 May 2026 instead!\n[15 May 2026] Tess: @Kofi Provided the speed camera survey happens, I'll share the garden hose by 17 May 2026.\n[15 May 2026] Tomas: Yep, the speed camera survey is on as planned.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of 9 May 2026, what is the date by which Kai has to feed the cat across the road, counting any agreed change?",
  "options": [
   "15 May 2026",
   "13 May 2026",
   "10 May 2026"
  ]
 },
 {
  "qid": "q049f5d26f1",
  "kind": "choice",
  "text": "Thread filed under support\nAbout the guest welcome plan, saved by Bruno.\n\nMembers: Nadia, Kofi, Bruno\nChat export (date | from | to | message):\n2026-02-09 | Bruno | Nadia | Count on me to vacuum the holiday cottage by 12 February 2026 if the owner handover visit is on.\n2026-02-09 | Kofi | Nadia | You can bet I'll collect the bed linen by 12 February 2026.\n2026-02-10 | Nadia | group | Scrapping the owner handover visit, apologies to all.\n2026-02-10 | Bruno | Nadia | Relax, I'll restock the guest toiletries by 15 February 2026, promise.\n2026-02-10 | Nadia | group | Cheers, noted.\n2026-02-10 | Bruno | Nadia | Mate, I promised, may I restock the guest toiletries by 19 February 2026 instead?\n2026-02-11 | Nadia | Kofi | Quick update: you do not need to collect the bed linen at all.\n2026-02-11 | Nadia | Bruno | Yes, you can restock the guest toiletries by 19 February 2026 if that suits you.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 16 February 2026, by what date does Bruno have to restock the guest toiletries, counting any agreed change of date?",
  "options": [
   "15 February 2026",
   "12 February 2026",
   "19 February 2026"
  ]
 },
 {
  "qid": "q12e21db09d",
  "kind": "choice",
  "text": "Jonas saved these replies from the agent on the kitchen refit.\n\nMembers: Sami, Jonas\nChat log (oldest first):\n[8 Oct 2026] Jonas: @Sami Count on me to forward the gas bill by 16 October 2026, if the flat viewing day happens.\n[11 Oct 2026] Jonas: @Sami Lovely, I'll collect the spare flat keys by 18 October 2026 for sure.\n[12 Oct 2026] Sami: Yay, the flat viewing day is all set to go!\n[14 Oct 2026] Jonas: @Sami Count on me to wipe the cooker hood by 18 October 2026 if the window cleaner visit is on.\n[15 Oct 2026] Jonas: @Sami Relax, I'll measure the kitchen for fridge by 19 October 2026 for sure.\n[18 Oct 2026] Jonas: @Sami Think 25 October 2026 would work if I measure the kitchen for fridge instead?\n[18 Oct 2026] Sami: @Jonas Works for me, fine for you to measure the kitchen for fridge by 25 October 2026.\n[23 Oct 2026] Jonas: @Sami Guess what, I managed to measure the kitchen for fridge!",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Jonas due to measure the kitchen for fridge at the end of 23 October 2026, after any agreed rescheduling?",
  "options": [
   "18 October 2026",
   "25 October 2026",
   "19 October 2026"
  ]
 },
 {
  "qid": "qab4339beff",
  "kind": "choice",
  "text": "Team channel export\nDescription: the social media plan, saved by Mo.\n\nMembers: Malik, Mo, Ana, Wren\nChat export (date | from | to | message):\n2026-06-12 | Ana | Mo | I'll fix the landing page headline by 2026-06-20, promise.\n2026-06-14 | Mo | Wren | I'll fetch the campaign budget sheet by 2026-06-17, provided the annual review happens.\n2026-06-16 | Wren | group | We are dropping the annual review from the list.\n2026-06-19 | Mo | Ana | I promise to set up the analytics dashboard by 2026-06-21.\n2026-06-20 | Mo | Ana | To note: I have managed to set up the analytics dashboard",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Mo's promise to fetch the campaign budget sheet at the end of 2026-06-21?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "qb7ca88a0fa",
  "kind": "choice",
  "text": "Exported by Priya, this is the full back and forth on the guest list.\n\nMembers: Kofi, Hana, Priya, Dara\nChat log (oldest first):\n[20 May 2026] Hana: @Kofi I promise to print the seating cards by 27 May 2026 if the venue visit is on.\n[21 May 2026] Kofi: @Hana Promise to send the sneak peek gallery by 30 May 2026 if the ceremony walkthrough goes ahead.\n[23 May 2026] Priya: Sadly, the ceremony walkthrough won't go ahead.\n[23 May 2026] Kofi: @Priya I will pick up the album prints by 31 May 2026.\n[24 May 2026] Kofi: @Priya Quick question, could I pick up the album prints by 4 June 2026 instead?\n[24 May 2026] Dara: @Hana I will make sure to collect the venue floor plan by 28 May 2026.\n[29 May 2026] Priya: @Kofi No change, you need to pick up the album prints by the original date.\n[30 May 2026] Dara: @Hana Mum, I did collect the venue floor plan, haha.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Kofi supposed to pick up the album prints by, going by the chat at the end of 6 June 2026 and any agreed changes?",
  "options": [
   "28 May 2026",
   "4 June 2026",
   "31 May 2026"
  ]
 },
 {
  "qid": "q135f816b26",
  "kind": "choice",
  "text": "Work channel holding the field survey, export saved by Greta.\n\nMembers: Sami, Greta, Ines, Bruno\nChat log (oldest first):\n[7 Sep 2026] Bruno: @Greta I own this, I'll scan the field notes by 15 Sep 2026.\n[9 Sep 2026] Bruno: @Greta Is it all right if I scan the field notes by 19 Sep 2026 instead?\n[10 Sep 2026] Sami: @Bruno Yes, happy for you to scan the field notes by 19 Sep 2026 instead.\n[17 Sep 2026] Ines: @Sami Provided the thesis defence happens, I'll submit the ethics application by 24 Sep 2026.\n[17 Sep 2026] Sami: @Greta Lovely, I'll print the poster abstracts by 21 Sep 2026 for sure.\n[20 Sep 2026] Ines: We are dropping the thesis defence from the list.\n[20 Sep 2026] Bruno: @Greta To my relief, I managed to scan the field notes.\n[20 Sep 2026] Sami: @Greta Change of plans: I will not print the poster abstracts",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen does Bruno have to scan the field notes by, at the end of 1 Oct 2026, once any agreed date change is included?",
  "options": [
   "19 Sep 2026",
   "15 Sep 2026",
   "24 Sep 2026"
  ]
 },
 {
  "qid": "q32d745de2d",
  "kind": "choice",
  "text": "{\"archive\": \"group chat\", \"subject\": \"the annual tour\", \"sent_by\": \"Wren\"}\n\nMembers: Mo, Wren, Lee\nChat export (date | from | to | message):\n2026-07-23 | Lee | Mo | Count on me to pump the spare tyres by 26 July 2026 if the bike check is on.\n2026-07-25 | Lee | Mo | I committed to pump the spare tyres, can I do that by 28 July 2026 instead?\n2026-07-25 | Mo | Lee | Committing to fetch the bike stand by 31 July 2026.\n2026-07-26 | Wren | Lee | Yes, fine to pump the spare tyres by 28 July 2026 instead.\n2026-07-28 | Wren | Lee | I'll wash the club jerseys by 30 July 2026, provided the swap meet happens.\n2026-07-29 | Lee | group | Update, the swap meet will not take place.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of 27 July 2026, which status does Lee have for the promise to pump the spare tyres?",
  "options": [
   "Kept",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q930ed2a8e0",
  "kind": "yes/no",
  "text": "Family group chat with housemates, covering the care plan, exported by Malik.\n\nMembers: Malik, Ana, Oskar\nChat log (oldest first):\n[28 Sep 2026] Ana: @Oskar I own this, I'll pick up the repeat prescription by 7 October 2026.\n[1 Oct 2026] Ana: @Oskar If the eye test goes ahead, I'll fetch the mobility aids by 4 October 2026.\n[3 Oct 2026] Malik: Yep, the eye test is on as planned.\n[4 Oct 2026] Oskar: @Ana Quick update: you do not need to fetch the mobility aids at all.\n[5 Oct 2026] Malik: @Ana Please don't feel you have to pick up the repeat prescription",
  "question": "Would you say Ana didn't keep the promise to fetch the mobility aids by the end of 4 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q606e63ddb8",
  "kind": "yes/no",
  "text": "An exported family chat on the caring rota, saved by Arlo, left unchanged.\n\nMembers: Arlo, Dara, Rhea, Ines\nChat log (oldest first):\n[10 Jun 2026] Rhea: @Arlo I'll call the home nurse by 13 June 2026, providing the family care meeting goes ahead.\n[11 Jun 2026] Rhea: Update, the family care meeting will not take place.\n[11 Jun 2026] Arlo: @Rhea I'll try to book the clinic transport by 14 June 2026.\n[13 Jun 2026] Arlo: @Dara Ticket's mine, I'll book the clinic transport by 16 June 2026.\n[14 Jun 2026] Ines: @Arlo Relax, I'll print the care schedule by 22 June 2026, promise.\n[15 Jun 2026] Arlo: @Dara Guess who managed to book the clinic transport, go team!",
  "question": "Per the rules on the card, does the promise Arlo made to book the clinic transport count as not broken at the end of 16 June 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q87e067de7c",
  "kind": "choice",
  "text": "Support thread for a help desk case, covering the menu redesign, saved by Malik.\n\nMembers: Dara, Malik, Tomas, Lee\nChat log (oldest first):\n[16 Apr 2026] Lee: @Tomas Only if the brand review call is on, I will mail the business cards by 20 April 2026.\n[17 Apr 2026] Dara: Yep, the brand review call is on as planned.\n[19 Apr 2026] Lee: @Tomas Quick report: I've managed to mail the business cards\n[19 Apr 2026] Tomas: @Dara It's on me to check the poster proofs by 22 April 2026.\n[23 Apr 2026] Tomas: @Dara Ticked off: check the poster proofs, feels so good",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status does the chat show for the promise Lee made to mail the business cards at the end of 22 April 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Kept",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qb7d54d7623",
  "kind": "yes/no",
  "text": "Omar forwarded this support chat about the rent split plan.\n\nMembers: Omar, Hana, Nadia\nChat log (oldest first):\n[7 Sep 2026] Nadia: @Hana I will ring the letting agent by 14 Sep 2026.\n[8 Sep 2026] Hana: @Omar I'll store the spare bike by 11 Sep 2026 as long as the agent inventory walk is on.\n[9 Sep 2026] Nadia: Team, the agent inventory walk is not happening.\n[11 Sep 2026] Nadia: @Hana Might I ask whether I could ring the letting agent by 17 Sep 2026 instead?\n[12 Sep 2026] Omar: @Nadia Of course, it is fine for you to ring the letting agent by 17 Sep 2026.\n[14 Sep 2026] Nadia: @Hana Quick report: I've managed to ring the letting agent",
  "question": "Going by the card's rules, does Nadia not keep the promise to ring the letting agent at the end of 18 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3ba1b8cc3d",
  "kind": "choice",
  "text": "Subject: Chat about the spring campaign\nA plain copy from Femi follows, exactly as exported.\n\nMembers: Omar, Mo, Femi\nChat export (date | from | to | message):\n2026-05-01 | Mo | Omar | You can bank on me to draft the press release by 8 May 2026.\n2026-05-02 | Femi | Omar | Count on me to send the newsletter copy by 10 May 2026 if the brand photo shoot is on.\n2026-05-03 | Omar | group | Update: the brand photo shoot is going ahead as planned.\n2026-05-03 | Omar | Femi | Relax, I'll collect the survey answers by 9 May 2026 for sure.\n2026-05-07 | Omar | Mo | I promise to set up the analytics dashboard by 14 May 2026.\n2026-05-11 | Femi | Omar | Guess who managed to send the newsletter copy, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Femi's undertaking to send the newsletter copy hold at the end of 16 May 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Broken",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qb56c1b5530",
  "kind": "yes/no",
  "text": "Shared by Leila from the work chat, with the spring campaign at its heart.\n\nMembers: Ana, Ravi, Leila, Arlo\nChat export (date | from | to | message):\n2026-01-12 | Arlo | Ravi | Absolutely, I will set up the analytics dashboard by 18 January 2026.\n2026-01-15 | Arlo | Ravi | Any chance I can set up the analytics dashboard by 20 January 2026 instead?\n2026-01-15 | Arlo | Ravi | My sincere apologies, I am unable to set up the analytics dashboard.\n2026-01-15 | Ana | Arlo | No need to set up the analytics dashboard, I'm letting you off\n2026-01-15 | Ravi | Arlo | Count on me to draft the press release by 17 January 2026 if the brand photo shoot is on.\n2026-01-16 | Leila | group | Fab, we are on for the brand photo shoot as planned!",
  "question": "Is the promise Arlo made to set up the analytics dashboard in a status other than broken at the end of 20 January 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q24cad4a95c",
  "kind": "yes/no",
  "text": "Volunteer chat export. Saved by Lena, it covers the ground upgrade.\n\nMembers: Lena, Femi\nChat log (oldest first):\n[14 Apr 2026] Femi: @Lena Guaranteed I'll return the bib sets by Friday, April 17, 2026.\n[16 Apr 2026] Lena: @Femi Provided the training camp happens, I will pump the match balls by Saturday, April 25, 2026.\n[17 Apr 2026] Femi: @Lena I own this, I'll collect the referee whistles by Sunday, April 19, 2026.\n[17 Apr 2026] Lena: @Femi No need to return the bib sets, I'm letting you off\n[18 Apr 2026] Femi: @Lena Got myself to collect the referee whistles lol.\n[20 Apr 2026] Femi: On track for the training camp to happen as planned.",
  "question": "By the end of Sunday, April 19, 2026, has Femi kept the promise to return the bib sets?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1c7e7e1fba",
  "kind": "yes/no",
  "text": "Club and committee chat, saved by Ana, with the kit sponsorship in the middle.\n\nMembers: Mo, Ana, Nadia\nChat log (oldest first):\n[14 May 2026] Nadia: @Mo If the pre-season friendly goes ahead, I'll gladly set up the corner flags by 19 May 2026.\n[18 May 2026] Ana: @Nadia It's on me to print the team sheets by 27 May 2026.\n[19 May 2026] Ana: @Mo Guaranteed I'll pump the match balls by 24 May 2026.\n[19 May 2026] Mo: @Nadia I'll collect the referee whistles by 25 May 2026 as long as the youth trial is on.\n[20 May 2026] Ana: @Nadia Guess what, I managed to print the team sheets!\n[24 May 2026] Ana: @Mo Guess who managed to pump the match balls, go team!",
  "question": "Is the promise Ana made to pump the match balls not kept by 24 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qef53c84159",
  "kind": "yes/no",
  "text": "Written between tenants and a landlord, this copy concerns the student house hunt. It was saved by Priya.\n\nMembers: Priya, Tomas, Leila\nChat log (oldest first):\n[29 Aug 2026] Priya: @Leila Guaranteed I'll return the bin rota by 6 Sep 2026.\n[30 Aug 2026] Priya: @Leila On my action item, may I return the bin rota by 9 Sep 2026 instead?\n[31 Aug 2026] Tomas: @Priya Count on me to scan the council tax letter by 7 Sep 2026 if the gas safety inspection is on.\n[3 Sep 2026] Tomas: @Leila If the agent inventory walk is on, I'll definitely forward the inventory photos by 10 Sep 2026.\n[6 Sep 2026] Leila: @Priya No need to return the bin rota, I'm letting you off",
  "question": "Under the rules on the card, is the promise Priya made to return the bin rota in a status other than broken at the end of 10 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q387273902b",
  "kind": "yes/no",
  "text": "A written chat between housemates about the family photo book. Exported from the device by Lena.\n\nMembers: Lena, Femi, Kai\nChat log (oldest first):\n[17 Aug 2026] Femi: @Kai Count on me to read the bedtime story by 24 August 2026 if the seaside outing is on.\n[18 Aug 2026] Femi: On track for the seaside outing to happen as planned.\n[22 Aug 2026] Kai: @Lena If the sleepover weekend is on, I'll definitely pack the picnic basket by 30 August 2026.\n[22 Aug 2026] Kai: @Lena You can bet I'll mend the kite string by 26 August 2026.\n[23 Aug 2026] Lena: @Kai Good news, you're let off having to mend the kite string\n[24 Aug 2026] Femi: @Kai Ticked off my list: read the bedtime story, yay.",
  "question": "Under the rules on the card, is the promise Femi made to read the bedtime story kept as of 27 August 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qae4167c8fe",
  "kind": "yes/no",
  "text": "Freelancer to client messages, the wedding weekend, passed on by Omar.\n\nMembers: Kai, Omar, Arlo\nChat log (oldest first):\n[10 Jul 2026] Arlo: @Omar I promise to set up the backdrop frame by Wednesday, 15 July 2026.\n[11 Jul 2026] Omar: @Arlo Lovely, I'll book the assistant photographer by Saturday, 18 July 2026 for sure.\n[13 Jul 2026] Arlo: @Omar I assure you I'll fetch the spare memory cards by Tuesday, 21 July 2026 if the bridal shower is on.\n[13 Jul 2026] Omar: Yay, the bridal shower is all set to go!\n[14 Jul 2026] Kai: @Arlo I'll return the lighting stands by Monday, 20 July 2026 as long as the engagement shoot is on.\n[15 Jul 2026] Arlo: @Omar Log entry: set up the backdrop frame, carried out",
  "question": "By the close of Friday, 17 July 2026, is the promise Arlo made to set up the backdrop frame kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd5c8ce6cdb",
  "kind": "yes/no",
  "text": "Malik forwarded this support chat about the volunteer roster.\n\nMembers: Malik, Arlo, Mo\nChat export (date | from | to | message):\n2026-02-12 | Malik | Mo | Not promising, but I'll try to book the school hall by 21 February 2026.\n2026-02-12 | Malik | Mo | Promise to set up the book stall by 20 February 2026 if the reading festival goes ahead.\n2026-02-13 | Malik | Arlo | Got it, I'll book the school hall by 19 February 2026 for sure.\n2026-02-14 | Malik | Arlo | Mind giving me until 24 February 2026 to book the school hall?\n2026-02-15 | Mo | Malik | I'll wrap the prize hampers by 18 February 2026 if the field day goes ahead.\n2026-02-16 | Mo | Malik | Go ahead and book the school hall by 24 February 2026, that is fine.",
  "question": "According to the card's rules, is the promise Malik made to book the school hall not kept as of 22 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q639194b32e",
  "kind": "choice",
  "text": "Team channel export, shared by Yuki, which is about the peer review.\n\nMembers: Yuki, Tomas, Tess\nChat log (oldest first):\n[11 Oct 2026] Tomas: @Tess If the seminar series goes ahead, I'll submit the ethics application by 16 Oct 2026.\n[13 Oct 2026] Tess: @Yuki You can bank on me to scan the field notes by 17 Oct 2026.\n[13 Oct 2026] Tomas: Yep, the seminar series is on as planned.\n[17 Oct 2026] Tess: @Yuki To note: I have managed to scan the field notes\n[17 Oct 2026] Yuki: @Tomas Guaranteed I'll order the reagent kit by 24 Oct 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Tess's promise to scan the field notes turn out at the end of 16 Oct 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "qaea54cbf1f",
  "kind": "choice",
  "text": "{\"item\": \"chat export\", \"matter\": \"the choir tour\", \"saved_by\": \"Omar\", \"layout\": \"plain\"}\n\nMembers: Omar, Leila, Priya\nChat log (oldest first):\n[12 May 2026] Leila: @Omar I'll see if I can fetch the choir robes by May 23, 2026.\n[13 May 2026] Leila: @Priya I own this, I'll fetch the choir robes by May 21, 2026.\n[15 May 2026] Leila: @Omar Lovely, I'll print the song sheets by May 17, 2026 if the joint concert is on.\n[15 May 2026] Omar: @Priya If the summer recital goes ahead, I'll gladly book the rehearsal room by May 24, 2026.\n[17 May 2026] Leila: @Priya On my action item, may I fetch the choir robes by May 25, 2026 instead?\n[21 May 2026] Omar: @Leila Nobody needs you to fetch the choir robes, that's that",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Leila's commitment to fetch the choir robes at the end of May 22, 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "qc23cca7329",
  "kind": "choice",
  "text": "{\"chat\": \"exported\", \"about\": \"the visitor policy\", \"saved_by\": \"Bruno\", \"medium\": \"text\"}\n\nMembers: Leila, Priya, Yuki, Bruno\nChat log (oldest first):\n[20 Jun 2026] Leila: Hoping to replace the kitchen filters by June 27, 2026, but can't promise.\n[21 Jun 2026] Leila: @Bruno If the lease viewing is on, I'll definitely replace the kitchen filters by June 29, 2026.\n[22 Jun 2026] Leila: Really pleased to say the lease viewing will go ahead!\n[25 Jun 2026] Yuki: @Priya You can bet I'll send the expense receipts by June 30, 2026.\n[28 Jun 2026] Priya: @Yuki Got it, I'll renew the fire extinguisher service by June 30, 2026 for sure.\n[29 Jun 2026] Leila: @Bruno Is July 2, 2026 alright for me to replace the kitchen filters?\n[29 Jun 2026] Yuki: @Leila Yes, lovely, you can replace the kitchen filters by July 2, 2026 instead!\n[3 Jul 2026] Leila: @Bruno Guess who managed to replace the kitchen filters, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen does Leila have to replace the kitchen filters by, at the end of July 7, 2026, once any agreed date change is included?",
  "options": [
   "June 30, 2026",
   "July 2, 2026",
   "June 29, 2026"
  ]
 },
 {
  "qid": "q1ad4b10979",
  "kind": "yes/no",
  "text": "Subject: the office refit\nBelow is the group chat that Hana saved, unedited.\n\nMembers: Nadia, Hana, Wren, Oskar\nChat log (oldest first):\n[11 Feb 2026] Wren: @Oskar Provided the staff picnic happens, I'll order the office stationery by 19 February 2026.\n[11 Feb 2026] Hana: Really pleased to say the staff picnic will go ahead!\n[11 Feb 2026] Nadia: Hoping to book the boardroom by 14 February 2026, but can't promise.\n[12 Feb 2026] Nadia: @Hana Absolutely, I will book the boardroom by 20 February 2026.\n[16 Feb 2026] Wren: @Nadia You are released, no requirement to book the boardroom.\n[21 Feb 2026] Nadia: @Hana For the record: I was able to book the boardroom",
  "question": "On the card, was Nadia's promise to book the boardroom kept, rather than broken, waived, not triggered or not yet due, at the end of 24 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q55269de34b",
  "kind": "choice",
  "text": "Thread between a landlord and tenants on the flat upgrade list left as it was and shared by Mo.\n\nMembers: Ivo, Omar, Kai, Mo\nChat log (oldest first):\n[4 Oct 2026] Kai: @Ivo Count on me, I'll remove the bathroom shelf by 13 Oct 2026.\n[5 Oct 2026] Mo: @Ivo As long as the lease renewal call is on, I will wipe the cooker hood by 7 Oct 2026.\n[6 Oct 2026] Ivo: We are dropping the lease renewal call from the list.\n[6 Oct 2026] Omar: @Kai Count on me to measure the kitchen for fridge by 12 Oct 2026.\n[11 Oct 2026] Omar: @Kai Log entry: measure the kitchen for fridge, carried out",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Omar's commitment to measure the kitchen for fridge have at the end of 11 Oct 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Broken",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q3b1ff0420f",
  "kind": "choice",
  "text": "Subject: exported chat about the spring campaign\nHere it is for you, from Lena, exactly as saved.\n\nMembers: Ravi, Lena, Lee, Greta\nChat export (date | from | to | message):\n2026-04-30 | Greta | Lena | I'll print the event banners by 8 May 2026 as long as the influencer call is on.\n2026-05-06 | Lena | Ravi | I'll be sure to return the rented camera gear by 13 May 2026.\n2026-05-06 | Lee | group | Quick heads up, the influencer call is scrapped.\n2026-05-08 | Greta | Lena | Forget it, you won't need to return the rented camera gear\n2026-05-08 | Greta | Lena | Mate, I promised, may I print the event banners by 12 May 2026 instead?",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Greta made to print the event banners have at the end of 10 May 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q3f8d957c12",
  "kind": "yes/no",
  "text": "Subject: exported chat about the house refit\nHere it is for you, from Zara, exactly as saved.\n\nMembers: Zara, Tess, Omar\nChat export (date | from | to | message):\n2026-04-10 | Tess | Zara | Ticket's mine, I'll hang the new curtain rail by 17 Apr 2026.\n2026-04-11 | Zara | Omar | Count on me to collect the sanding pads by 20 Apr 2026, if the removal van arrival happens.\n2026-04-12 | Tess | Zara | Count on me to fetch the paint samples by 14 Apr 2026.\n2026-04-15 | Tess | Omar | Lovely, I'll measure the hallway for shelves by 21 Apr 2026 if the kitchen fitting day is on.\n2026-04-17 | Tess | Zara | For the record: I was able to hang the new curtain rail\n2026-04-20 | Omar | group | Sadly, the kitchen fitting day won't go ahead.",
  "question": "Does the card's rule set show that Tess has not kept the promise to hang the new curtain rail at the end of 23 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7f852806f9",
  "kind": "choice",
  "text": "Copy of a household chat shared by Priya, where neighbours discuss the loft conversion.\n\nMembers: Priya, Hana, Sami\nChat export (date | from | to | message):\n2026-08-28 | Priya | Hana | As long as the mortgage valuation visit is on, I will measure the hallway for shelves by Thursday, September 3, 2026.\n2026-08-28 | Hana | group | Just so you know, the mortgage valuation visit is on as scheduled.\n2026-08-29 | Hana | Priya | If the damp survey inspection goes ahead, I'll gladly pay the plumbing invoice by Saturday, September 5, 2026.\n2026-08-30 | Priya | Hana | You can bank on me to pick up the grout bag by Wednesday, September 2, 2026.\n2026-08-31 | Hana | Priya | Quick update: you do not need to pick up the grout bag at all.\n2026-09-02 | Priya | Hana | Got myself to measure the hallway for shelves lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Priya's promise to measure the hallway for shelves at the end of Tuesday, September 1, 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Waived",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "q15428b36e7",
  "kind": "yes/no",
  "text": "Volunteers, Bruno shared this with you about the music library.\n\nMembers: Bruno, Leila, Greta\nChat log (oldest first):\n[6 Mar 2026] Greta: Will attempt to buy the spare folders by 9 Mar 2026, can't promise.\n[8 Mar 2026] Greta: @Bruno Ticket's mine, I'll buy the spare folders by 15 Mar 2026.\n[13 Mar 2026] Greta: @Bruno I regret to say that I shall not buy the spare folders.\n[13 Mar 2026] Leila: @Greta Nobody needs you to buy the spare folders, that's that\n[14 Mar 2026] Bruno: @Leila I'll book the rehearsal room by 21 Mar 2026 if the sing along goes ahead.\n[19 Mar 2026] Greta: We are dropping the sing along from the list.",
  "question": "Does the card classify Greta's promise to buy the spare folders as broken, waived, not triggered or not yet due, rather than kept, on 14 Mar 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6b194b42e5",
  "kind": "choice",
  "text": "Yuki forwarded these replies from the agent on the balcony garden project for the file.\n\nMembers: Zara, Yuki\nChat log (oldest first):\n[5 Jul 2026] Zara: @Yuki Got it, I'll wipe the cooker hood by 13 July 2026 for sure.\n[6 Jul 2026] Zara: @Yuki Relax, I'll drop the bin bags off by 15 July 2026, promise.\n[10 Jul 2026] Yuki: @Zara I'll forward the gas bill by 17 July 2026, promise.\n[14 Jul 2026] Yuki: @Zara I promise to collect the spare flat keys by 18 July 2026 if the window cleaner visit is on.\n[15 Jul 2026] Zara: Yay, the window cleaner visit is all set to go!\n[17 Jul 2026] Yuki: @Zara On my action item, may I collect the spare flat keys by 24 July 2026 instead?\n[23 Jul 2026] Yuki: @Zara To note: I have managed to collect the spare flat keys",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Yuki to collect the spare flat keys at the end of 4 August 2026, counting any agreed change of date?",
  "options": [
   "17 July 2026",
   "18 July 2026",
   "24 July 2026"
  ]
 },
 {
  "qid": "q565bff024a",
  "kind": "choice",
  "text": "Team channel: the lab move\nShared by: Elif.\n\nMembers: Lena, Yuki, Elif\nChat log (oldest first):\n[31 Jan 2026] Yuki: @Lena Count on me to submit the ethics application by 2026-02-08 if the grant panel is on.\n[31 Jan 2026] Lena: Cheers, noted.\n[31 Jan 2026] Lena: @Elif Guaranteed I'll book the microscope slot by 2026-02-05.\n[1 Feb 2026] Lena: Just so you know, the grant panel is on as scheduled.\n[3 Feb 2026] Elif: @Yuki Nobody needs you to submit the ethics application, that's that\n[6 Feb 2026] Yuki: @Lena Ticked off my list: submit the ethics application, yay.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Yuki's promise to submit the ethics application at the end of 2026-02-03?",
  "options": [
   "Not triggered",
   "Kept",
   "Broken",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "qd7a4bd94ff",
  "kind": "yes/no",
  "text": "A short note above messages between tenants and the landlord about the shared kitchen scheme, saved by Lee.\n\nMembers: Kai, Lee, Sami\nChat export (date | from | to | message):\n2026-05-06 | Sami | Kai | I'll sort the recycling bags by 10 May 2026, promise.\n2026-05-07 | Lee | Sami | Lovely, I'll replace the loo roll by 15 May 2026 if the fuse box inspection is on.\n2026-05-08 | Lee | Sami | Absolutely, I will buy the washing powder by 11 May 2026.\n2026-05-09 | Sami | group | Lovely, the fuse box inspection is definitely happening!\n2026-05-11 | Lee | Sami | Apologies, I'll not be able to buy the washing powder",
  "question": "Has Lee not kept the promise to replace the loo roll at the end of 17 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q98ef0c52ee",
  "kind": "choice",
  "text": "We have been planning the old house restoration here, shared by Hana.\n\nMembers: Kofi, Ana, Wren, Hana\nChat log (oldest first):\n[11 Jul 2026] Ana: @Wren I promise to mend the garden gate by 19 Jul 2026.\n[14 Jul 2026] Kofi: @Wren Count on me to oil the back door hinges by 20 Jul 2026, if the heritage fete happens.\n[16 Jul 2026] Kofi: @Ana You are released, no requirement to mend the garden gate.\n[18 Jul 2026] Ana: Sad to report that the heritage fete is off.\n[19 Jul 2026] Ana: @Wren For the record: I was able to mend the garden gate",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Ana's pledge to mend the garden gate at the end of 21 Jul 2026?",
  "options": [
   "Waived",
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "qb40ff0ba92",
  "kind": "yes/no",
  "text": "{\"record_type\": \"saved chat\", \"matter\": \"the documentary cut\", \"by\": \"Jonas\", \"stored\": \"as text\"}\n\nMembers: Arlo, Jonas, Leila\nChat export (date | from | to | message):\n2026-08-31 | Jonas | Leila | Committing to fetch the raw footage by 5 September 2026.\n2026-09-04 | Jonas | Arlo | Count on me to send the colour notes by 12 September 2026 if the client screening is on.\n2026-09-05 | Leila | Jonas | Forget it, you won't need to fetch the raw footage\n2026-09-07 | Arlo | Jonas | I will order the stock music licence by 13 September 2026.\n2026-09-08 | Jonas | group | We are dropping the client screening from the list.\n2026-09-08 | Arlo | Jonas | Ticked off: order the stock music licence, feels so good",
  "question": "On the card, was Jonas's promise to send the colour notes broken, waived, not triggered or not yet due, rather than kept, at the end of 8 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q57376630a5",
  "kind": "choice",
  "text": "Household chat saved by Ivo, with the shared kitchen scheme at its heart.\n\nMembers: Greta, Priya, Ivo\nChat export (date | from | to | message):\n2026-06-11 | Priya | Greta | Committing to replace the loo roll by June 14, 2026.\n2026-06-12 | Ivo | Priya | Ah, no stress, no need for you to replace the loo roll\n2026-06-13 | Greta | group | Maybe I can wipe the shared kitchen counter by June 19, 2026.\n2026-06-14 | Greta | Priya | Provided the lodger farewell supper happens, I'll wipe the shared kitchen counter by June 22, 2026.\n2026-06-18 | Ivo | group | Team, the lodger farewell supper stays on as booked.\n2026-06-22 | Greta | Priya | Got myself to wipe the shared kitchen counter lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Greta made to wipe the shared kitchen counter at the end of June 22, 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Not yet due",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "qdd11ba0ccf",
  "kind": "yes/no",
  "text": "Saved by Dara: a freelancer's exchange with a client over the campaign edit.\n\nMembers: Dara, Oskar, Zara\nChat export (date | from | to | message):\n2026-10-05 | Zara | Dara | If the voiceover session is on, I'll definitely label the clip folders by 11 October 2026.\n2026-10-08 | Zara | Oskar | Count on me, I'll back up the project drives by 12 October 2026.\n2026-10-10 | Oskar | group | Just so you know, the voiceover session is on as scheduled.\n2026-10-11 | Zara | Oskar | Quick report: I've managed to back up the project drives\n2026-10-11 | Dara | Oskar | Got it, I'll fetch the raw footage by 17 October 2026 for sure.",
  "question": "Applying the card's rules, does Zara's promise to back up the project drives count as broken, waived, not triggered or not yet due, rather than kept, as of 16 October 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb937db0a6b",
  "kind": "yes/no",
  "text": "{\"export_type\": \"group chat export\", \"chat_topic\": \"the house rules debate\", \"saved_by\": \"Nadia\"}\n\nMembers: Nadia, Ravi, Yuki\nChat log (oldest first):\n[21 Jun 2026] Yuki: @Nadia As long as the chimney sweep visit is on, I'll tidy the boot room by June 26, 2026.\n[21 Jun 2026] Nadia: Thanks for the heads up.\n[24 Jun 2026] Nadia: @Yuki Count on me, I'll bleed the attic radiators by July 3, 2026.\n[25 Jun 2026] Yuki: Yay, the chimney sweep visit is all set to go!\n[25 Jun 2026] Yuki: @Nadia Think June 29, 2026 would work if I tidy the boot room instead?\n[26 Jun 2026] Nadia: @Yuki Aw no, you need to tidy the boot room by the original date!",
  "question": "Under the rules on the card, is the promise Yuki made to tidy the boot room broken at the end of June 27, 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9f2923ff9b",
  "kind": "yes/no",
  "text": "{\"record_type\": \"saved chat\", \"matter\": \"the desk plan\", \"by\": \"Rhea\", \"stored\": \"as text\"}\n\nMembers: Rhea, Lena, Nadia\nChat log (oldest first):\n[16 Sep 2026] Nadia: @Rhea Might be able to collect the visitor badges by 23 September 2026, who knows!\n[18 Sep 2026] Nadia: @Rhea Relax, I'll collect the visitor badges by 24 September 2026, promise.\n[19 Sep 2026] Lena: @Rhea Ticket's mine, I'll replace the kitchen filters by 27 September 2026.\n[21 Sep 2026] Nadia: @Rhea Ta-da, I went and did it: collect the visitor badges!\n[23 Sep 2026] Lena: @Rhea As long as the building survey is on, I will fetch the parking permits by 1 October 2026.\n[27 Sep 2026] Rhea: Brilliant news everyone, the building survey is a go!",
  "question": "Would you say Nadia didn't keep the promise to collect the visitor badges by the end of 23 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7b6ee1bfcf",
  "kind": "choice",
  "text": "Priya shared this channel export covering the office refit for the team.\n\nMembers: Priya, Dara, Lena, Greta\nChat log (oldest first):\n[1 Jul 2026] Lena: @Greta I'll book the boardroom by 7 July 2026, provided the staff picnic happens.\n[1 Jul 2026] Dara: Sorry, the staff picnic is off.\n[3 Jul 2026] Lena: @Priya It's on me to return the printer toner by 8 July 2026.\n[7 Jul 2026] Lena: @Greta Would it be fine if I book the boardroom by 9 July 2026 instead, yeah?\n[7 Jul 2026] Greta: @Lena Aw no, you need to book the boardroom by the original date!\n\nAdmin: each change here has been signed off by an admin, and Priya asked for that to be recorded.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Lena's promise to book the boardroom turn out at the end of 9 July 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Broken",
   "Kept",
   "Waived"
  ]
 }
]
