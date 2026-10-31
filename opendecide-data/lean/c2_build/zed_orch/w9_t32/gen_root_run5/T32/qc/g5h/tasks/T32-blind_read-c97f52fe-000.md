# G5-H blind read (all free-form rows) T32-blind_read-c97f52fe-000 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root/T32/qc/g5h/answers/T32-blind_read-c97f52fe-000.json

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
  "qid": "qaca5c8041f",
  "kind": "choice",
  "text": "We have been planning the guest travel plans here, shared by Dara.\n\nMembers: Dara, Priya, Lee, Jonas\nChat log (oldest first):\n[15 Apr 2026] Lee: @Priya Only if the garden picnic is on, I will pay the catering company by 23 April 2026.\n[18 Apr 2026] Lee: Brilliant news everyone, the garden picnic is a go!\n[20 Apr 2026] Lee: @Priya Any chance I can pay the catering company by 28 April 2026 instead?\n[21 Apr 2026] Priya: @Lee That suits me, so please pay the catering company by 28 April 2026 instead.\n[21 Apr 2026] Dara: @Jonas I will make sure to send the group invitations by 26 April 2026.\n[27 Apr 2026] Jonas: @Lee Forget it, you won't need to pay the catering company\n[1 May 2026] Lee: @Priya Guess what, I managed to pay the catering company!",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Lee supposed to pay the catering company by, going by the chat at the end of 4 May 2026 and any agreed changes?",
  "options": [
   "28 April 2026",
   "23 April 2026",
   "26 April 2026"
  ]
 },
 {
  "qid": "q9662f69175",
  "kind": "choice",
  "text": "Volunteers, here is the annual tour thread that Lena forwarded for us.\n\nMembers: Bruno, Lena, Oskar, Dara\nChat export (date | from | to | message):\n2026-07-16 | Lena | Dara | Relax, I'll service the tandem bike by 21 Jul 2026 for sure.\n2026-07-20 | Lena | Dara | Can I service the tandem bike by 25 Jul 2026 instead? I did promise, sorry.\n2026-07-21 | Oskar | Dara | It's on me to set up the feed stop by 24 Jul 2026.\n2026-07-21 | Dara | Lena | Yes, you have the green light to service the tandem bike by 25 Jul 2026.\n2026-07-22 | Oskar | Dara | To note: I have managed to set up the feed stop\n2026-07-22 | Lena | Dara | I assure you I'll tune the gear cables by 24 Jul 2026 if the club sportive is on.\n2026-07-23 | Lena | Dara | Guess who managed to service the tandem bike, go team!\n2026-07-23 | Lena | group | Yay, the club sportive is all set to go!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nFollowing the rules set out on the card, what date governs Lena's commitment to service the tandem bike at the end of 27 Jul 2026, once any agreed shift in the date is factored in?",
  "options": [
   "25 Jul 2026",
   "21 Jul 2026",
   "24 Jul 2026"
  ]
 },
 {
  "qid": "q8f3c6ed3ec",
  "kind": "choice",
  "text": "Sami shared this so the annual tour is easy to follow for the volunteers.\n\nMembers: Omar, Sami, Nadia\nChat log (oldest first):\n[11 Apr 2026] Nadia: @Sami Got it, I'll return the loaned helmets by 13 Apr 2026 for sure.\n[11 Apr 2026] Omar: @Nadia Provided the bike check happens, I'll service the tandem bike by 14 Apr 2026.\n[11 Apr 2026] Nadia: Really pleased to say the bike check will go ahead!\n[13 Apr 2026] Sami: @Nadia You are released, no requirement to return the loaned helmets.\n[13 Apr 2026] Omar: @Nadia Quick question, could I service the tandem bike by 18 Apr 2026 instead?\n[14 Apr 2026] Nadia: @Omar That suits me, so please service the tandem bike by 18 Apr 2026 instead.\n[14 Apr 2026] Omar: @Nadia I regret to say that I shall not service the tandem bike.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo what's the latest day Omar has to service the tandem bike by at the end of 15 Apr 2026, given any new date people agreed to?",
  "options": [
   "14 Apr 2026",
   "13 Apr 2026",
   "18 Apr 2026"
  ]
 },
 {
  "qid": "qebb6eb6bcf",
  "kind": "yes/no",
  "text": "Subject: Saved chat on the guest travel plans\nHere is the export from Leila, for the record.\n\nMembers: Sami, Leila, Rhea\nChat log (oldest first):\n[2 Jul 2026] Sami: @Rhea I own this, I'll print the family tree chart by 9 July 2026.\n[3 Jul 2026] Sami: @Leila Count on me to pay the catering company by 11 July 2026 if the reunion lunch is on.\n[4 Jul 2026] Leila: @Rhea Provided the cousin brunch happens, I'll buy the name tags by 10 July 2026.\n[9 Jul 2026] Leila: @Sami You are released, no requirement to print the family tree chart.\n[9 Jul 2026] Leila: Fab, we are on for the cousin brunch as planned!\n[11 Jul 2026] Leila: @Rhea Mum, I did buy the name tags, haha.",
  "question": "Has Leila kept the promise to buy the name tags as of 10 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2f392973ba",
  "kind": "choice",
  "text": "Chat attached to a support case about the onboarding flow, shared by Elif.\n\nMembers: Hana, Elif, Ravi\nChat log (oldest first):\n[23 Apr 2026] Ravi: @Elif Relax, I'll label the bug reports by 27 Apr 2026, promise.\n[24 Apr 2026] Elif: Not promising, but I'll try to fix the test runner by 3 May 2026.\n[25 Apr 2026] Elif: @Hana If the planning session goes ahead, I'll write the release notes by 28 Apr 2026.\n[25 Apr 2026] Ravi: Sad to report that the planning session is off.\n[25 Apr 2026] Elif: @Hana Got it, I'll fix the test runner by 30 Apr 2026 for sure.\n[29 Apr 2026] Elif: @Hana Any chance I can fix the test runner by 3 May 2026 instead?\n[30 Apr 2026] Ravi: @Elif Go ahead and fix the test runner by 3 May 2026, that is fine.\n[5 May 2026] Elif: @Hana To note: I have managed to fix the test runner",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIf the chat is checked at the end of 2 May 2026, which date marks the deadline for Elif to fix the test runner, with agreed date changes included?",
  "options": [
   "3 May 2026",
   "30 Apr 2026",
   "28 Apr 2026"
  ]
 },
 {
  "qid": "q69e4b4bd52",
  "kind": "yes/no",
  "text": "Mo forwarded this support chat, which is about the honeymoon album.\n\nMembers: Greta, Mo, Yuki\nChat log (oldest first):\n[18 Oct 2026] Mo: @Yuki Count on me to print the seating cards by 23 Oct 2026.\n[18 Oct 2026] Mo: @Yuki Update on my side: I will not print the seating cards, sorry.\n[19 Oct 2026] Yuki: @Greta I promise to pick up the album prints by 28 Oct 2026 if the cake tasting is on.\n[19 Oct 2026] Mo: Brilliant news everyone, the cake tasting is a go!\n[23 Oct 2026] Greta: @Yuki Relax, I'll fetch the spare memory cards by 30 Oct 2026, promise.",
  "question": "Is the promise Mo made to print the seating cards in a status other than broken at the end of 20 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q170aeca70b",
  "kind": "yes/no",
  "text": "Our flat chat about the house rules debate, shared by Kofi for whoever lives here.\n\nMembers: Sami, Kofi, Malik, Elif\nChat log (oldest first):\n[25 Sep 2026] Sami: @Kofi I'll defrost the old fridge by 1 October 2026 as long as the loft clearance day is on.\n[27 Sep 2026] Malik: @Elif I will make sure to bleed the attic radiators by 5 October 2026.\n[27 Sep 2026] Malik: Fab, we are on for the loft clearance day as planned!\n[29 Sep 2026] Sami: @Malik You can bet I'll clear the kitchen sink by 7 October 2026.\n[1 Oct 2026] Malik: @Elif Got myself to bleed the attic radiators lol.",
  "question": "On the card, was Malik's promise to bleed the attic radiators kept, rather than broken, waived, not triggered or not yet due, at the end of 7 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q83d065d9d4",
  "kind": "choice",
  "text": "Our flat chat about the summer lets season, saved by Mo for whoever lives here.\n\nMembers: Leila, Mo, Greta, Yuki\nChat log (oldest first):\n[22 Mar 2026] Yuki: @Mo Committing to wheel the bins out by 28 March 2026.\n[24 Mar 2026] Yuki: @Mo Mind giving me until 2 April 2026 to wheel the bins out?\n[28 Mar 2026] Greta: @Yuki Yes, you're welcome to wheel the bins out by 2 April 2026 instead.\n[28 Mar 2026] Leila: @Yuki If the owner handover visit is on, I'll definitely scrub the hot tub by 5 April 2026.\n[29 Mar 2026] Yuki: @Mo Quick report: I've managed to wheel the bins out\n[29 Mar 2026] Leila: @Greta I will wash the beach towels by 4 April 2026.\n[31 Mar 2026] Leila: @Greta I'll restock the guest toiletries by 3 April 2026, providing the summer season launch goes ahead.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of 31 March 2026, what is the date by which Yuki has to wheel the bins out, counting any agreed change?",
  "options": [
   "2 April 2026",
   "5 April 2026",
   "28 March 2026"
  ]
 },
 {
  "qid": "q85fc1ce1e5",
  "kind": "choice",
  "text": "Leila saved this exchange with the client about the sound mix.\n\nMembers: Malik, Jonas, Leila, Ravi\nChat export (date | from | to | message):\n2026-10-21 | Ravi | Jonas | Count on me to send the timeline export by 28 October 2026 if the voiceover session is on.\n2026-10-23 | Ravi | Malik | Aiming to order the stock music licence by 3 November 2026, we'll see.\n2026-10-25 | Ravi | Leila | Guaranteed I'll order the stock music licence by 1 November 2026.\n2026-10-25 | Jonas | group | Afraid the voiceover session is called off.\n2026-10-26 | Jonas | Ravi | Got it, I'll label the clip folders by 31 October 2026 for sure.\n2026-10-29 | Ravi | Leila | I committed to order the stock music licence, can I do that by 5 November 2026 instead?\n2026-10-29 | Jonas | Ravi | Yes, all good for you to order the stock music licence by 5 November 2026 instead.\n2026-11-01 | Ravi | Leila | I'm withdrawing my promise to order the stock music licence",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Ravi to order the stock music licence at the end of 2 November 2026, counting any agreed change of date?",
  "options": [
   "1 November 2026",
   "31 October 2026",
   "5 November 2026"
  ]
 },
 {
  "qid": "q714e4ea853",
  "kind": "yes/no",
  "text": "Subject: Saved chat on the guest travel plans\nHere is the export from Leila, for the record.\n\nMembers: Sami, Leila, Rhea\nChat log (oldest first):\n[2 Jul 2026] Sami: @Rhea I own this, I'll print the family tree chart by 9 July 2026.\n[3 Jul 2026] Sami: @Leila Count on me to pay the catering company by 11 July 2026 if the reunion lunch is on.\n[4 Jul 2026] Leila: @Rhea Provided the cousin brunch happens, I'll buy the name tags by 10 July 2026.\n[9 Jul 2026] Leila: @Sami You are released, no requirement to print the family tree chart.\n[9 Jul 2026] Leila: Fab, we are on for the cousin brunch as planned!\n[11 Jul 2026] Leila: @Rhea Mum, I did buy the name tags, haha.",
  "question": "According to the card's rules, is the promise Leila made to buy the name tags not kept as of 10 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc7afcfa29e",
  "kind": "yes/no",
  "text": "We have been planning the quiet street fund here, shared by Hana.\n\nMembers: Malik, Hana, Ivo\nChat log (oldest first):\n[12 Apr 2026] Malik: @Ivo Guaranteed I'll take in the post by 17 Apr 2026.\n[14 Apr 2026] Malik: @Ivo Ticked off: take in the post, feels so good\n[14 Apr 2026] Malik: @Ivo You can bet I'll walk the old spaniel by 18 Apr 2026.\n[18 Apr 2026] Hana: @Ivo Lovely, I'll clear the hedge trimmings by 25 Apr 2026 for sure.\n[18 Apr 2026] Ivo: @Malik If the street litter clean goes ahead, I'll gladly lock the side gate by 22 Apr 2026.\n[21 Apr 2026] Malik: Yep, the street litter clean is on as planned.\n\nAdded by Hana: The chat export is an outdated snapshot, so whatever it lists may already have changed elsewhere.",
  "question": "Does the chat, checked at the end of 20 Apr 2026, show that Malik has broken the promise to take in the post?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1badaef775",
  "kind": "yes/no",
  "text": "Hana shared this so the speed bump plan is easy to find, flatmates.\n\nMembers: Greta, Malik, Hana\nChat log (oldest first):\n[10 Aug 2026] Hana: @Greta I'll try to feed the cat across the road by 12 August 2026, can't promise!\n[11 Aug 2026] Hana: @Greta Committing to feed the cat across the road by 14 August 2026.\n[12 Aug 2026] Greta: @Hana If the road works meeting goes ahead, I'll share the garden hose by 17 August 2026.\n[15 Aug 2026] Hana: @Greta To my relief, I managed to feed the cat across the road.\n[15 Aug 2026] Greta: @Malik I'll sweep the pavement outside by 22 August 2026, promise.\n[16 Aug 2026] Hana: @Greta I'll lock the side gate by 23 August 2026, providing the parking permit visit goes ahead.",
  "question": "Would you call Hana's promise to feed the cat across the road broken, waived, not triggered or not yet due, instead of kept, at the end of 15 August 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q434851dc03",
  "kind": "choice",
  "text": "Tenant and landlord back-and-forth on the spare room plan, saved by Zara.\n\nMembers: Rhea, Priya, Zara, Elif\nChat export (date | from | to | message):\n2026-01-20 | Priya | Zara | Only if the lodger house supper is on, I will wipe the shared kitchen counter by 28 January 2026.\n2026-01-23 | Elif | group | Just so you know, the lodger house supper is on as scheduled.\n2026-01-23 | Zara | Priya | As long as the fuse box inspection is on, I will buy the washing powder by 25 January 2026.\n2026-01-25 | Rhea | Priya | Count on me, I'll drop the parcel upstairs by 30 January 2026.\n2026-01-29 | Rhea | Priya | I committed to drop the parcel upstairs, can I do that by 4 February 2026 instead?\n2026-01-30 | Priya | Rhea | Works for me, fine for you to drop the parcel upstairs by 4 February 2026.",
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
  "qid": "q7b08d1dd3b",
  "kind": "choice",
  "text": "Subject: Chat about the honeymoon album\nA plain copy from Tess follows, exactly as exported.\n\nMembers: Malik, Rhea, Tess\nChat export (date | from | to | message):\n2026-06-25 | Rhea | Tess | If the venue visit goes ahead, I'll print the seating cards by Friday, 3 July 2026.\n2026-06-29 | Tess | group | Sad to report that the venue visit is off.\n2026-06-30 | Rhea | Malik | Got it, I'll pick up the album prints by Sunday, 5 July 2026 for sure.\n2026-07-03 | Rhea | Malik | Correction, I will not be able to pick up the album prints.\n2026-07-05 | Malik | Rhea | No need to pick up the album prints, I'm letting you off",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Rhea's promise to pick up the album prints at the end of Friday, 10 July 2026?",
  "options": [
   "Waived",
   "Broken",
   "Not yet due",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "qeb28508bd4",
  "kind": "yes/no",
  "text": "Elif shared this exchange with the client about the documentary cut.\n\nMembers: Greta, Elif, Oskar, Tess\nChat export (date | from | to | message):\n2026-09-08 | Elif | Greta | I'll send the colour notes by Sunday, September 13, 2026 as long as the shoot day is on.\n2026-09-10 | Tess | Oskar | Count on me to order the stock music licence by Friday, September 18, 2026.\n2026-09-11 | Oskar | Greta | Promise to record the voice over by Sunday, September 20, 2026 if the client screening goes ahead.\n2026-09-12 | Tess | Oskar | I will fetch the raw footage by Saturday, September 19, 2026.\n2026-09-14 | Oskar | Tess | Nobody needs you to fetch the raw footage, that's that\n2026-09-17 | Tess | group | Team, the client screening is not happening.",
  "question": "According to the rules on the card, has Tess broken the promise to fetch the raw footage at the end of Saturday, September 19, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3b79903688",
  "kind": "yes/no",
  "text": "Saved by Omar, this talk about the garden shed build is just for family.\n\nMembers: Bruno, Ines, Omar\nChat log (oldest first):\n[7 Feb 2026] Ines: @Omar I'll stake the tomato canes by 14 February 2026, providing the plot inspection goes ahead.\n[9 Feb 2026] Ines: Brilliant news everyone, the plot inspection is a go!\n[10 Feb 2026] Bruno: @Omar Count on me, I'll dig the potato patch by 15 February 2026.\n[12 Feb 2026] Bruno: @Omar Got myself to dig the potato patch lol.\n[19 Feb 2026] Ines: @Omar Ticked off: stake the tomato canes, feels so good",
  "question": "Is it right to say that Ines has broken the promise to stake the tomato canes at the end of 16 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb0cf5e77b2",
  "kind": "choice",
  "text": "Forwarded by Mo, these tenant replies are about the balcony garden project for the file.\n\nMembers: Nadia, Hana, Mo, Yuki\nChat log (oldest first):\n[16 Jun 2026] Nadia: @Mo If the lease renewal call goes ahead, I'll gladly drop the bin bags off by 2026-06-21.\n[21 Jun 2026] Hana: @Yuki Relax, I'll remove the bathroom shelf by 2026-06-26 for sure.\n[22 Jun 2026] Hana: @Yuki Might I ask whether I could remove the bathroom shelf by 2026-06-30 instead?\n[24 Jun 2026] Hana: @Nadia Promise to email the leak photos by 2026-07-01 if the rent review meeting goes ahead.\n[25 Jun 2026] Nadia: @Hana Good news, you're let off having to remove the bathroom shelf",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Hana's pledge to remove the bathroom shelf at the end of 2026-06-30?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q0c661a91da",
  "kind": "yes/no",
  "text": "Attached chat: the annual tour\nForwarded by: Elif\n\nMembers: Greta, Elif, Leila\nChat log (oldest first):\n[19 Feb 2026] Greta: @Leila Promise to wash the club jerseys by 2026-02-27 if the hill climb goes ahead.\n[19 Feb 2026] Elif: @Greta I assure you I'll stock the energy gels by 2026-02-27 if the club sportive is on.\n[22 Feb 2026] Greta: @Elif I promise to fetch the bike stand by 2026-02-26.\n[26 Feb 2026] Greta: @Elif Scratch that, I'm not going to fetch the bike stand\n[26 Feb 2026] Greta: @Leila Count on me, I'll service the tandem bike by 2026-03-05.",
  "question": "Does the card's rule set confirm that Greta has kept the promise to fetch the bike stand on 2026-03-02?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q640e70687d",
  "kind": "choice",
  "text": "Team channel: the spring campaign\nShared by: Kofi.\n\nMembers: Kofi, Kai, Lee\nChat export (date | from | to | message):\n2026-08-09 | Lee | Kofi | Provided the annual review happens, I'll draft the press release by August 14, 2026.\n2026-08-09 | Kai | Kofi | You can bank on me to collect the survey answers by August 16, 2026.\n2026-08-12 | Lee | Kai | Count on me to fix the landing page headline by August 17, 2026 if the webinar rehearsal is on.\n2026-08-13 | Kai | group | On track for the webinar rehearsal to happen as planned.\n2026-08-14 | Kai | Kofi | Is it all right if I collect the survey answers by August 18, 2026 instead?\n2026-08-14 | Kofi | Kai | Not moving it, collect the survey answers by the existing date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Lee made to fix the landing page headline at the end of August 16, 2026?",
  "options": [
   "Waived",
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "qeb1455ab52",
  "kind": "choice",
  "text": "We are getting ready for the family history, and Rhea shared this chat with us.\n\nMembers: Rhea, Yuki\nChat log (oldest first):\n[5 Aug 2026] Rhea: @Yuki Only if the karaoke night is on, I will set up the slideshow laptop by 12 Aug 2026.\n[5 Aug 2026] Yuki: Fab, we are on for the karaoke night as planned!\n[6 Aug 2026] Yuki: @Rhea I will send the group invitations by 8 Aug 2026.\n[6 Aug 2026] Yuki: @Rhea I committed to send the group invitations, can I do that by 11 Aug 2026 instead?\n[7 Aug 2026] Rhea: @Yuki No, you need to send the group invitations by the original date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Rhea made to set up the slideshow laptop have at the end of 9 Aug 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Broken",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q638f4875ce",
  "kind": "yes/no",
  "text": "Yo flatmates, Kai shared this chat about the vegetable plot plan, so chip in.\n\nMembers: Bruno, Ines, Kai, Malik\nChat log (oldest first):\n[26 Jun 2026] Kai: @Malik Promise to water the allotment beds by 28 Jun 2026 if the village flower show goes ahead.\n[28 Jun 2026] Malik: @Kai Provided the seed swap day happens, I'll weed the carrot row by 30 Jun 2026.\n[1 Jul 2026] Bruno: @Ines Count on me, I'll deliver the surplus runner beans by 8 Jul 2026.\n[6 Jul 2026] Malik: @Bruno No worries, you don't need to deliver the surplus runner beans\n[8 Jul 2026] Bruno: @Ines Ta-da, I went and did it: deliver the surplus runner beans!",
  "question": "Would you say Bruno kept the promise to deliver the surplus runner beans at the end of 11 Jul 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3a4eb5407d",
  "kind": "yes/no",
  "text": "Subject: Chat about the winter concert\nBelow is a copy that came from Hana, pasted as found.\n\nMembers: Hana, Wren, Ines, Kai\nChat log (oldest first):\n[24 Jul 2026] Hana: @Kai Only if the joint concert is on, I will return the library scores by 31 July 2026.\n[24 Jul 2026] Hana: Quick heads up, the joint concert is scrapped.\n[25 Jul 2026] Kai: @Hana You can bank on me to buy the spare folders by 1 August 2026.\n[27 Jul 2026] Ines: @Kai I'll be sure to move the piano by 30 July 2026.\n[30 Jul 2026] Ines: @Kai To my relief, I managed to move the piano.\n[4 Aug 2026] Wren: Anything new on your way to move the piano?",
  "question": "Checking the chat at the end of 5 August 2026, has Ines broken the promise to move the piano?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qfeca6af9c0",
  "kind": "choice",
  "text": "Forwarded by Jonas: a help-desk thread covering the kitchen garden project.\n\nMembers: Tomas, Priya, Jonas, Elif\nChat log (oldest first):\n[4 May 2026] Elif: @Tomas You can bet I'll sow the broad beans by 11 May 2026.\n[5 May 2026] Priya: @Elif Relax, I'll dig the potato patch by 8 May 2026, promise.\n[5 May 2026] Tomas: @Priya Provided the harvest supper happens, I will sharpen the hand hoe by 9 May 2026.\n[6 May 2026] Elif: @Priya Good news, you're let off having to dig the potato patch\n[7 May 2026] Jonas: Team, the harvest supper is not happening.\n[11 May 2026] Priya: @Elif Ah, no stress, no need for you to sow the broad beans\n\nAdded by Jonas: The chat export is an outdated snapshot, so whatever it lists may already have changed elsewhere.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Tomas made to sharpen the hand hoe at the end of 13 May 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q5b8728e420",
  "kind": "choice",
  "text": "Volunteers, this is the league run thread that Tomas shared with the committee.\n\nMembers: Rhea, Tomas\nChat log (oldest first):\n[27 Feb 2026] Rhea: @Tomas Absolutely, I will print the team sheets by 5 Mar 2026.\n[2 Mar 2026] Rhea: @Tomas I will wash the away kit by 7 Mar 2026 only if the home derby happens.\n[3 Mar 2026] Rhea: Sorry, the home derby is off.\n[4 Mar 2026] Rhea: @Tomas Quick question, could I print the team sheets by 11 Mar 2026 instead?\n[4 Mar 2026] Rhea: @Tomas To my relief, I managed to print the team sheets.\n[4 Mar 2026] Tomas: @Rhea I'll be sure to mark the pitch lines by 8 Mar 2026.\n[5 Mar 2026] Tomas: @Rhea Ticked off my list: mark the pitch lines, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat's the day Rhea needs to print the team sheets by at the end of 15 Mar 2026, after any new date the group agreed on?",
  "options": [
   "11 Mar 2026",
   "5 Mar 2026",
   "7 Mar 2026"
  ]
 },
 {
  "qid": "q56099838d4",
  "kind": "choice",
  "text": "Subject: Saved thread about the house rules debate\nThis export came from Wren and is pasted in full below.\n\nMembers: Wren, Zara\nChat log (oldest first):\n[21 Jun 2026] Wren: @Zara Lovely, I'll oil the back door hinges by 26 Jun 2026 if the house viewing is on.\n[21 Jun 2026] Wren: @Zara Promise to bleed the attic radiators by 24 Jun 2026 if the heritage fete goes ahead.\n[21 Jun 2026] Zara: Team, the heritage fete is not happening.\n[23 Jun 2026] Wren: @Zara Count on me, I'll scrub the cellar steps by 2 Jul 2026.\n[24 Jun 2026] Wren: @Zara You can bank on me to mend the garden gate by 1 Jul 2026.\n[1 Jul 2026] Wren: @Zara Mum, I did scrub the cellar steps, haha.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Wren made to bleed the attic radiators have at the end of 23 Jun 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q4a333bda3a",
  "kind": "choice",
  "text": "We are getting ready for the travel plans, and Arlo shared this chat with us.\n\nMembers: Ravi, Bruno, Arlo\nChat export (date | from | to | message):\n2026-01-08 | Bruno | Arlo | I promise to print the boarding passes by 15 Jan 2026 if the ferry crossing is on.\n2026-01-09 | Arlo | group | On track for the ferry crossing to happen as planned.\n2026-01-10 | Ravi | Arlo | I own this, I'll return the rental car keys by 13 Jan 2026.\n2026-01-13 | Ravi | Arlo | Any chance I can return the rental car keys by 19 Jan 2026 instead?\n2026-01-13 | Arlo | Ravi | Yes, fine to return the rental car keys by 19 Jan 2026 instead.\n2026-01-14 | Ravi | Arlo | To note: I have managed to return the rental car keys",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Ravi made to return the rental car keys is in which status at the end of 16 Jan 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Kept",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q6c0cda5cab",
  "kind": "choice",
  "text": "Committee chat on the playground project, shared by Sami with the volunteers.\n\nMembers: Oskar, Sami, Ana\nChat export (date | from | to | message):\n2026-03-31 | Sami | Oskar | Might be able to fetch the tea urn by 8 April 2026, who knows!\n2026-04-01 | Ana | Sami | Guaranteed I'll wrap the prize hampers by 6 April 2026.\n2026-04-02 | Sami | Ana | If the quiz night is on, I'll definitely fetch the tea urn by 5 April 2026.\n2026-04-02 | Sami | group | On track for the quiz night to happen as planned.\n2026-04-05 | Sami | Ana | I committed to fetch the tea urn, can I do that by 7 April 2026 instead?\n2026-04-05 | Ana | Sami | No, you need to fetch the tea urn by the original date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Sami's commitment to fetch the tea urn at the end of 5 April 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Broken",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qabcfbc55d4",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the kitchen refit\nThe thread below comes from Greta and is passed on as it is.\n\nMembers: Nadia, Greta, Ines\nChat log (oldest first):\n[1 Jun 2026] Nadia: @Greta Provided the flat viewing day happens, I'll measure the kitchen for fridge by 3 Jun 2026.\n[1 Jun 2026] Nadia: Team, the flat viewing day stays on as booked.\n[3 Jun 2026] Ines: @Nadia Relax, I'll collect the spare flat keys by 6 Jun 2026 for sure.\n[3 Jun 2026] Greta: @Ines Ah, no stress, no need for you to collect the spare flat keys\n[3 Jun 2026] Ines: @Nadia Mum, I did collect the spare flat keys, haha.\n[7 Jun 2026] Greta: @Ines As long as the lease renewal call is on, I'll bring the step stool by 13 Jun 2026.",
  "question": "At the end of 3 Jun 2026, does the promise Ines made to collect the spare flat keys have any status except broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc6eabf4088",
  "kind": "yes/no",
  "text": "Forwarded by Omar, these tenant replies are about the flatmate contract terms for the file.\n\nMembers: Tomas, Lee, Hana, Omar\nChat log (oldest first):\n[6 Apr 2026] Hana: @Tomas I'll return the bin rota by 11 Apr 2026, providing the check in visit goes ahead.\n[8 Apr 2026] Lee: Brilliant news everyone, the check in visit is a go!\n[8 Apr 2026] Omar: @Hana No need to return the bin rota, I'm letting you off\n[12 Apr 2026] Omar: @Tomas Ticket's mine, I'll send the deposit receipt by 18 Apr 2026.\n[12 Apr 2026] Omar: @Tomas Gutted to say I won't send the deposit receipt, sorry team",
  "question": "Is the promise to return the bin rota that Hana made broken at the end of 8 Apr 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa86f279501",
  "kind": "yes/no",
  "text": "Subject: Chat about the bathroom refit\nBelow is a copy that came from Omar, pasted as found.\n\nMembers: Ivo, Omar, Zara\nChat export (date | from | to | message):\n2026-01-24 | Zara | Ivo | You can bet I'll print the floor plan by 1 February 2026.\n2026-01-28 | Zara | Ivo | Guess who managed to print the floor plan, go team!\n2026-01-28 | Zara | Ivo | I'll hang the new curtain rail by 2 February 2026, providing the boiler install visit goes ahead.\n2026-01-28 | Ivo | group | Thanks lovely, got it!\n2026-01-31 | Omar | group | Great news, the boiler install visit is on!\n2026-02-02 | Zara | Ivo | Mum, I did hang the new curtain rail, haha.",
  "question": "Going by the card's rules, does Zara not keep the promise to hang the new curtain rail at the end of 5 February 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q42fcbb3e73",
  "kind": "yes/no",
  "text": "Forwarded by Lee: a help-desk thread covering the guest review drive.\n\nMembers: Priya, Lee, Hana\nChat log (oldest first):\n[7 Oct 2026] Hana: @Lee Promise to change the lounge bulb by 13 October 2026 if the pool safety inspection goes ahead.\n[10 Oct 2026] Hana: Yay, the pool safety inspection is all set to go!\n[11 Oct 2026] Hana: @Lee To my relief, I managed to change the lounge bulb.\n[12 Oct 2026] Priya: @Lee Count on me to fill the cleaning cupboard by 16 October 2026.\n[12 Oct 2026] Hana: @Priya No worries, you don't need to fill the cleaning cupboard",
  "question": "Under the rules on the card, is Hana's promise to change the lounge bulb broken, waived, not triggered or not yet due, rather than kept, as of 14 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q465143b493",
  "kind": "choice",
  "text": "Team channel: the visitor policy\nShared by: Hana.\n\nMembers: Ravi, Hana, Lee\nChat log (oldest first):\n[13 Oct 2026] Lee: @Hana I own this, I'll return the printer toner by 20 October 2026.\n[16 Oct 2026] Hana: @Ravi Provided the building survey happens, I will order the office stationery by 23 October 2026.\n[18 Oct 2026] Hana: Great news, the building survey is on!\n[18 Oct 2026] Lee: Checking you mean to order the office stationery?\n[19 Oct 2026] Hana: @Ravi Guaranteed I'll set up the reception screen by 26 October 2026.\n[24 Oct 2026] Hana: @Ravi I regret to say that I shall not set up the reception screen.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Hana's promise to order the office stationery sit at the end of 23 October 2026, exactly?",
  "options": [
   "Broken",
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q91c141d238",
  "kind": "choice",
  "text": "Attached chat: the documentary cut\nShared by: Elif\n\nMembers: Greta, Elif, Rhea, Bruno\nChat export (date | from | to | message):\n2026-02-17 | Bruno | Greta | It's on me to record the voice over by 22 Feb 2026.\n2026-02-17 | Bruno | Rhea | If the client screening goes ahead, I'll send the timeline export by 20 Feb 2026.\n2026-02-19 | Greta | Elif | Promise to order the stock music licence by 26 Feb 2026 if the festival premiere goes ahead.\n2026-02-23 | Greta | Elif | I will ship the hard drive by 27 Feb 2026.\n2026-02-23 | Bruno | group | We are dropping the festival premiere from the list.\n2026-02-27 | Greta | Elif | To my relief, I managed to ship the hard drive.\n\nNotice from the chat app: the copy Elif shared is an older export, and newer messages are not included.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Greta's promise to order the stock music licence at the end of 26 Feb 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q626cbc7b65",
  "kind": "yes/no",
  "text": "Hana shared this so the speed bump plan is easy to find, flatmates.\n\nMembers: Greta, Malik, Hana\nChat log (oldest first):\n[10 Aug 2026] Hana: @Greta I'll try to feed the cat across the road by 12 August 2026, can't promise!\n[11 Aug 2026] Hana: @Greta Committing to feed the cat across the road by 14 August 2026.\n[12 Aug 2026] Greta: @Hana If the road works meeting goes ahead, I'll share the garden hose by 17 August 2026.\n[15 Aug 2026] Hana: @Greta To my relief, I managed to feed the cat across the road.\n[15 Aug 2026] Greta: @Malik I'll sweep the pavement outside by 22 August 2026, promise.\n[16 Aug 2026] Hana: @Greta I'll lock the side gate by 23 August 2026, providing the parking permit visit goes ahead.",
  "question": "Is Hana's promise to feed the cat across the road kept as of 15 August 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qcc742d638b",
  "kind": "choice",
  "text": "Kai forwarded this support chat, which is about the documentary cut.\n\nMembers: Arlo, Ines, Kai\nChat export (date | from | to | message):\n2026-09-16 | Kai | Ines | Lovely, I'll upload the render files by 21 Sep 2026 if the festival premiere is on.\n2026-09-17 | Arlo | Ines | Absolutely, I will label the clip folders by 22 Sep 2026.\n2026-09-17 | Arlo | Ines | Can I label the clip folders by 28 Sep 2026 instead? I did promise, sorry.\n2026-09-20 | Ines | Arlo | Fine by me, you can label the clip folders by 28 Sep 2026.\n2026-09-20 | Ines | group | Just so you know, the festival premiere is on as scheduled.\n2026-09-21 | Kai | Arlo | Relax, mate, you're not expected to label the clip folders",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Arlo's commitment to label the clip folders have at the end of 26 Sep 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "qcbb6ebaa06",
  "kind": "choice",
  "text": "Our flat chat about the old house restoration, shared by Kofi for whoever lives here.\n\nMembers: Ivo, Kofi, Arlo\nChat log (oldest first):\n[15 Aug 2026] Kofi: @Arlo I own this, I'll oil the back door hinges by August 18, 2026.\n[15 Aug 2026] Ivo: @Kofi Nobody needs you to oil the back door hinges, that's that\n[16 Aug 2026] Ivo: @Kofi Provided the heritage fete happens, I will clear the kitchen sink by August 21, 2026.\n[18 Aug 2026] Ivo: @Kofi Committing to mend the garden gate by August 23, 2026.\n[18 Aug 2026] Arlo: @Ivo If the loft clearance day goes ahead, I'll find the loft ladder by August 21, 2026.\n[18 Aug 2026] Kofi: @Arlo Quick report: I've managed to oil the back door hinges",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Kofi made to oil the back door hinges at the end of August 22, 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q3045d40abd",
  "kind": "choice",
  "text": "Subject: Chat about the trip itinerary\nBelow is a copy that came from Yuki, pasted as found.\n\nMembers: Zara, Rhea, Yuki\nChat export (date | from | to | message):\n2026-05-15 | Rhea | Zara | I own this, I'll buy the packing cubes by 20 May 2026.\n2026-05-16 | Zara | Rhea | If the ferry crossing goes ahead, I'll check the passport copies by 21 May 2026.\n2026-05-16 | Zara | group | On track for the ferry crossing to happen as planned.\n2026-05-17 | Rhea | Zara | Please don't feel you have to check the passport copies\n2026-05-20 | Rhea | Zara | Correction, I will not be able to buy the packing cubes.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Zara's promise to check the passport copies at the end of 20 May 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qa3776ec8af",
  "kind": "yes/no",
  "text": "Posted by Ivo from the work channel, the field survey thread.\n\nMembers: Zara, Omar, Ivo\nChat log (oldest first):\n[10 Apr 2026] Ivo: @Zara If the safety inspection goes ahead, I'll gladly submit the ethics application by Wednesday, April 15, 2026.\n[12 Apr 2026] Zara: @Ivo Relax, I'll print the poster abstracts by Tuesday, April 14, 2026 for sure.\n[13 Apr 2026] Omar: Team, the safety inspection stays on as booked.\n[14 Apr 2026] Omar: @Zara Forget it, you won't need to print the poster abstracts\n[16 Apr 2026] Ivo: @Zara Guess who managed to submit the ethics application, go team!",
  "question": "Would a check of the chat at the end of Sunday, April 19, 2026 show the promise Ivo made to submit the ethics application as broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qfe3347b603",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the guest travel plans\nThis export came from Kai and is pasted in full below.\n\nMembers: Tomas, Kai\nChat log (oldest first):\n[29 Apr 2026] Kai: @Tomas Might be able to print the family tree chart by 2 May 2026, who knows!\n[1 May 2026] Kai: @Tomas I'll print the family tree chart by 7 May 2026 if the grandparents visit goes ahead.\n[4 May 2026] Kai: @Tomas I own this, I'll collect the old photo prints by 12 May 2026.\n[4 May 2026] Tomas: @Kai Forget it, you won't need to collect the old photo prints\n[5 May 2026] Tomas: Team, the grandparents visit stays on as booked.\n[7 May 2026] Kai: @Tomas Guess who managed to print the family tree chart, go team!",
  "question": "Did Kai keep the promise to print the family tree chart on 12 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6a9b18fcbb",
  "kind": "choice",
  "text": "Team channel: the desk plan\nShared by Bruno.\n\nMembers: Yuki, Priya, Bruno\nChat log (oldest first):\n[4 Apr 2026] Yuki: @Bruno I will replace the kitchen filters by 9 April 2026.\n[4 Apr 2026] Priya: I'll try to send the expense receipts by 18 April 2026, no promises.\n[5 Apr 2026] Bruno: @Priya I will book the boardroom by 7 April 2026 only if the team lunch happens.\n[6 Apr 2026] Priya: @Bruno Absolutely, I will send the expense receipts by 14 April 2026.\n[9 Apr 2026] Priya: @Yuki Only if the coffee morning is on, I will collect the visitor badges by 15 April 2026.\n[15 Apr 2026] Priya: @Bruno For the record: I was able to send the expense receipts",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Priya's promise to send the expense receipts at the end of 20 April 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "q5ca0eef1f4",
  "kind": "choice",
  "text": "Tenant and agent back-and-forth on the flat upgrade list, forwarded by Malik.\n\nMembers: Lena, Elif, Malik, Femi\nChat log (oldest first):\n[5 May 2026] Malik: @Elif I own this, I'll measure the kitchen for fridge by Saturday, May 9, 2026.\n[9 May 2026] Femi: @Malik I promise to collect the spare flat keys by Sunday, May 17, 2026 if the rent review meeting is on.\n[9 May 2026] Elif: @Malik Please don't feel you have to measure the kitchen for fridge\n[10 May 2026] Malik: @Lena I'll read the meter readings by Tuesday, May 19, 2026 if the flat viewing day goes ahead.\n[12 May 2026] Malik: @Elif Quick report: I've managed to measure the kitchen for fridge",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Malik's promise to measure the kitchen for fridge turn out at the end of Saturday, May 9, 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "qbe75df1d13",
  "kind": "choice",
  "text": "Subject: Chat about the menu redesign\nThe copy from Ines follows below as a plain record.\n\nMembers: Nadia, Ines\nChat log (oldest first):\n[28 Jan 2026] Ines: @Nadia I promise to mail the business cards by 5 February 2026.\n[28 Jan 2026] Ines: @Nadia Update on my side: I will not mail the business cards, sorry.\n[30 Jan 2026] Nadia: @Ines I will collect the photo credits by 3 February 2026 only if the packaging launch happens.\n[31 Jan 2026] Nadia: @Ines You are released, no requirement to mail the business cards.\n[1 Feb 2026] Ines: Quick heads up, the packaging launch is scrapped.\n[1 Feb 2026] Nadia: @Ines I'll export the logo files by 8 February 2026 as long as the brand review call is on.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Ines doing with the promise to mail the business cards at the end of 5 February 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "qd0efdcf5aa",
  "kind": "choice",
  "text": "Attached chat: the travel plans\nShared by: Wren.\n\nMembers: Hana, Wren, Kai, Tess\nChat log (oldest first):\n[9 May 2026] Tess: @Hana Lovely, I'll return the rental car keys by 19 May 2026 if the family cookout is on.\n[12 May 2026] Hana: @Tess Absolutely, I will fill the car boot by 18 May 2026.\n[13 May 2026] Wren: @Hana No need to fill the car boot, I'm letting you off\n[16 May 2026] Wren: @Kai Count on me to check the passport copies by 19 May 2026 if the guided tour is on.\n[18 May 2026] Hana: @Tess Ticked off: fill the car boot, feels so good",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status does the chat show for the promise Hana made to fill the car boot at the end of 18 May 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "qf61745d522",
  "kind": "choice",
  "text": "Forwarded by Mo, these tenant replies are about the balcony garden project for the file.\n\nMembers: Nadia, Hana, Mo, Yuki\nChat log (oldest first):\n[16 Jun 2026] Nadia: @Mo If the lease renewal call goes ahead, I'll gladly drop the bin bags off by 2026-06-21.\n[21 Jun 2026] Hana: @Yuki Relax, I'll remove the bathroom shelf by 2026-06-26 for sure.\n[22 Jun 2026] Hana: @Yuki Might I ask whether I could remove the bathroom shelf by 2026-06-30 instead?\n[24 Jun 2026] Hana: @Nadia Promise to email the leak photos by 2026-07-01 if the rent review meeting goes ahead.\n[25 Jun 2026] Nadia: @Hana Good news, you're let off having to remove the bathroom shelf",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Hana's pledge to remove the bathroom shelf at the end of 2026-06-30?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "qb0a1587349",
  "kind": "choice",
  "text": "Parents and cousins, this is where we sort out the family history. Saved by Lena.\n\nMembers: Lena, Greta, Mo\nChat log (oldest first):\n[1 Apr 2026] Greta: @Lena I'll fetch the speaker system by 7 April 2026 if the garden picnic goes ahead.\n[2 Apr 2026] Greta: Yep, the garden picnic is on as planned.\n[3 Apr 2026] Greta: @Lena I'll print the family tree chart by 10 April 2026, promise.\n[4 Apr 2026] Greta: @Mo Committing to collect the old photo prints by 9 April 2026.\n[6 Apr 2026] Greta: @Mo On my action item, may I collect the old photo prints by 12 April 2026 instead?\n[9 Apr 2026] Mo: @Greta The original date stands, so you need to collect the old photo prints.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Greta's promise to fetch the speaker system at the end of 5 April 2026?",
  "options": [
   "Kept",
   "Broken",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "qa97e5f6fa8",
  "kind": "yes/no",
  "text": "Client thread on the gallery show, shared by Ivo for the project log.\n\nMembers: Kofi, Ana, Ivo\nChat log (oldest first):\n[3 Oct 2026] Ivo: @Kofi I will make sure to collect the photo credits by 9 Oct 2026.\n[5 Oct 2026] Ivo: @Kofi Count on me to mail the business cards by 10 Oct 2026 if the sign reveal is on.\n[5 Oct 2026] Kofi: Sad to report that the sign reveal is off.\n[7 Oct 2026] Ana: @Ivo Ah, no stress, no need for you to collect the photo credits\n[12 Oct 2026] Ivo: @Kofi Guess who managed to collect the photo credits, go team!",
  "question": "According to the rules on the card, has Ivo broken the promise to collect the photo credits at the end of 13 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4342140786",
  "kind": "choice",
  "text": "Shared by Dara, a help-desk thread covering the guest list.\n\nMembers: Lee, Oskar, Dara, Jonas\nChat export (date | from | to | message):\n2026-02-27 | Jonas | Dara | I will make sure to buy the candle props by 7 March 2026.\n2026-03-05 | Jonas | Dara | On my action item, may I buy the candle props by 9 March 2026 instead?\n2026-03-07 | Dara | Jonas | Yes, you can buy the candle props by 9 March 2026 if that suits you.\n2026-03-08 | Dara | Jonas | Provided the venue visit happens, I'll charge the flash batteries by 13 March 2026.\n2026-03-08 | Dara | group | Please note the venue visit will proceed.\n2026-03-09 | Jonas | Dara | Guess who managed to buy the candle props, go team!\n2026-03-10 | Oskar | Jonas | Relax, I'll pick up the album prints by 13 March 2026, promise.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Jonas due to buy the candle props at the end of 10 March 2026, after any agreed rescheduling?",
  "options": [
   "13 March 2026",
   "9 March 2026",
   "7 March 2026"
  ]
 },
 {
  "qid": "qc4d9b8adde",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the social media plan\nThis export from Kai is pasted in full for readers who want it.\n\nMembers: Ravi, Kai, Greta\nChat export (date | from | to | message):\n2026-10-23 | Kai | Ravi | I will collect the survey answers by 27 October 2026 only if the annual review happens.\n2026-10-28 | Ravi | Greta | I will draft the press release by 5 November 2026.\n2026-10-28 | Kai | Greta | Relax, I'll return the rented camera gear by 1 November 2026, promise.\n2026-10-29 | Greta | Ravi | I'll send the newsletter copy by 4 November 2026, providing the product launch goes ahead.\n2026-10-30 | Ravi | Kai | Forget it, you won't need to return the rented camera gear",
  "question": "Would you say Kai kept the promise to return the rented camera gear at the end of 3 November 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0102bddbed",
  "kind": "choice",
  "text": "Mo saved this so we stay on the same page about the house refit, mates.\n\nMembers: Wren, Malik, Mo\nChat export (date | from | to | message):\n2026-06-25 | Wren | Mo | I assure you I'll measure the hallway for shelves by Wednesday, July 1, 2026 if the removal van arrival is on.\n2026-06-27 | Malik | group | Quick heads up, the removal van arrival is scrapped.\n2026-06-30 | Wren | Malik | I own this, I'll sweep the dust from stairs by Sunday, July 5, 2026.\n2026-07-01 | Wren | Mo | You can bank on me to pick up the grout bag by Friday, July 3, 2026.\n2026-07-01 | Malik | group | Update on your plan to sweep the dust from stairs?\n2026-07-04 | Wren | Malik | Is Thursday, July 9, 2026 alright for me to sweep the dust from stairs?\n2026-07-05 | Malik | Wren | Yes, you're welcome to sweep the dust from stairs by Thursday, July 9, 2026 instead.\n2026-07-06 | Wren | Malik | To my relief, I managed to sweep the dust from stairs.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Wren supposed to sweep the dust from stairs by, going by the chat at the end of Sunday, July 12, 2026 and any agreed changes?",
  "options": [
   "Sunday, July 5, 2026",
   "Friday, July 3, 2026",
   "Thursday, July 9, 2026"
  ]
 },
 {
  "qid": "qbe26430ec2",
  "kind": "choice",
  "text": "Omar forwarded this for the committee as we dig in on the volunteer roster.\n\nMembers: Omar, Greta, Hana, Bruno\nChat export (date | from | to | message):\n2026-03-01 | Greta | Hana | Got it, I'll return the borrowed trestle tables by 7 Mar 2026 for sure.\n2026-03-03 | Hana | Greta | Ah, no stress, no need for you to return the borrowed trestle tables\n2026-03-04 | Omar | Greta | Provided the governors meeting happens, I'll send the newsletter drafts by 6 Mar 2026.\n2026-03-04 | Greta | Hana | Guess who managed to return the borrowed trestle tables, go team!\n2026-03-05 | Hana | group | Just so you know, the governors meeting is on as scheduled.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Greta made to return the borrowed trestle tables at the end of 3 Mar 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 }
]
