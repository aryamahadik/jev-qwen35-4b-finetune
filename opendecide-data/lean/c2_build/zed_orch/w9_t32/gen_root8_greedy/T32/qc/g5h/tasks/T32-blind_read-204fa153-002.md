# G5-H blind read T32-blind_read-204fa153-002 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root8/T32/qc/g5h/answers/T32-blind_read-204fa153-002.json

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
  "qid": "q737dec3afa",
  "kind": "yes/no",
  "text": "{\"item\": \"chat export\", \"matter\": \"the student house hunt\", \"saved_by\": \"Ivo\", \"layout\": \"plain\"}\n\nMembers: Nadia, Ivo, Leila\nChat log (oldest first):\n[12 May 2026] Nadia: @Leila Relax, I'll print the tenancy agreement by 16 May 2026 for sure.\n[14 May 2026] Ivo: @Nadia I'll copy the house keys by 23 May 2026, providing the check in visit goes ahead.\n[14 May 2026] Nadia: @Leila Think 19 May 2026 would work if I print the tenancy agreement instead?\n[16 May 2026] Ivo: @Nadia You don't have to print the tenancy agreement at all\n[16 May 2026] Nadia: @Leila Log entry: print the tenancy agreement, carried out\n[19 May 2026] Nadia: Team, the check in visit stays on as booked.",
  "question": "On the card, was Nadia's promise to print the tenancy agreement kept, rather than broken, waived, not triggered or not yet due, at the end of 20 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q728c6b29b0",
  "kind": "choice",
  "text": "Pasted into the project log by Nadia, the thread with a client about the guest list.\n\nMembers: Leila, Nadia, Hana\nChat log (oldest first):\n[16 Jul 2026] Leila: @Nadia I assure you I'll return the lighting stands by 2026-07-24 if the venue visit is on.\n[17 Jul 2026] Nadia: @Hana Might be able to print the seating cards by 2026-07-22, who knows!\n[18 Jul 2026] Hana: @Nadia I will fetch the spare memory cards by 2026-07-26 only if the rehearsal dinner happens.\n[18 Jul 2026] Nadia: @Leila Count on me to print the seating cards by 2026-07-21.\n[19 Jul 2026] Leila: @Nadia You don't have to print the seating cards at all\n[22 Jul 2026] Nadia: @Leila Log entry: print the seating cards, carried out",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Nadia's commitment to print the seating cards at the end of 2026-07-26?",
  "options": [
   "Waived",
   "Not triggered",
   "Not yet due",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q4a82c0be67",
  "kind": "yes/no",
  "text": "Team export header with the grant renewal, saved by Ivo.\n\nMembers: Leila, Tess, Ivo\nChat log (oldest first):\n[14 Mar 2026] Leila: @Tess It's on me to book the microscope slot by 18 Mar 2026.\n[14 Mar 2026] Leila: @Ivo Count on me to fetch the grant forms by 19 Mar 2026, if the grant panel happens.\n[15 Mar 2026] Leila: @Ivo I'll return the library books by 23 Mar 2026 if the conference trip goes ahead.\n[15 Mar 2026] Leila: @Tess For the record: I was able to book the microscope slot\n[15 Mar 2026] Ivo: @Tess You can bank on me to print the poster abstracts by 23 Mar 2026.\n[18 Mar 2026] Ivo: @Tess Got myself to print the poster abstracts lol.",
  "question": "Was the promise to book the microscope slot from Leila kept on 18 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb24f3fba5e",
  "kind": "choice",
  "text": "Here is the thread on the attic conversion idea, posted by Zara for the house.\n\nMembers: Bruno, Priya, Zara, Rhea\nChat export (date | from | to | message):\n2026-05-20 | Rhea | group | Aiming to replace the loo roll by 31 May 2026, we'll see.\n2026-05-21 | Rhea | Bruno | I'll be sure to defrost the top freezer by 29 May 2026.\n2026-05-22 | Rhea | Priya | I will replace the loo roll by 30 May 2026.\n2026-05-24 | Rhea | Priya | Quick report: I've managed to replace the loo roll\n2026-05-24 | Bruno | Zara | If the lodger house supper goes ahead, I'll stock the spice rack by 26 May 2026.\n2026-05-25 | Zara | group | Yep, the lodger house supper is on as planned.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Rhea's promise to replace the loo roll have at the end of 27 May 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "qcfd92e655e",
  "kind": "yes/no",
  "text": "Our flat chat about the guest welcome plan, shared by Leila for whoever lives here.\n\nMembers: Leila, Mo, Ana\nChat log (oldest first):\n[14 Oct 2026] Mo: See if I can leave the welcome basket by 16 October 2026.\n[15 Oct 2026] Mo: @Ana Absolutely, I will leave the welcome basket by 23 October 2026.\n[17 Oct 2026] Ana: @Mo You can bet I'll wash the beach towels by 26 October 2026.\n[20 Oct 2026] Leila: @Mo Lovely, I'll vacuum the holiday cottage by 26 October 2026 if the guest arrival evening is on.\n[21 Oct 2026] Mo: @Ana Ta-da, I went and did it: leave the welcome basket!\n[25 Oct 2026] Ana: Great news, the guest arrival evening is on!",
  "question": "Does the card's rule set show that Mo has not kept the promise to leave the welcome basket at the end of 25 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc8e0e274dd",
  "kind": "choice",
  "text": "{\"thread_kind\": \"exported conversation\", \"about\": \"the shared kitchen scheme\", \"exported_by\": \"Priya\"}\n\nMembers: Sami, Mo, Priya, Kai\nChat export (date | from | to | message):\n2026-09-15 | Kai | Sami | I assure you I'll feed the house plants by 19 September 2026 if the house insurance review is on.\n2026-09-17 | Priya | group | Sorry all, the house insurance review is not happening.\n2026-09-19 | Kai | Priya | I will make sure to replace the loo roll by 25 September 2026.\n2026-09-22 | Sami | Kai | No worries, you don't need to replace the loo roll\n2026-09-30 | Kai | Priya | Ticked off: replace the loo roll, feels so good",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 27 September 2026, what status has Kai's promise to replace the loo roll got?",
  "options": [
   "Not yet due",
   "Broken",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q641c23a35e",
  "kind": "yes/no",
  "text": "{\"chat\": \"exported\", \"about\": \"the holiday memories\", \"saved_by\": \"Sami\", \"medium\": \"text\"}\n\nMembers: Rhea, Sami, Yuki\nChat log (oldest first):\n[10 Oct 2026] Rhea: Might manage to bake the oat biscuits by 21 October 2026, who knows.\n[10 Oct 2026] Sami: @Yuki I will pick up the school bags by 18 October 2026 only if the seaside outing happens.\n[10 Oct 2026] Yuki: Brilliant news everyone, the seaside outing is a go!\n[12 Oct 2026] Rhea: @Sami Relax, I'll bake the oat biscuits by 19 October 2026 for sure.\n[14 Oct 2026] Yuki: @Rhea You don't have to bake the oat biscuits at all\n[21 Oct 2026] Rhea: @Sami Guess what, I managed to bake the oat biscuits!",
  "question": "Applying the rules on the card, can Rhea's promise to bake the oat biscuits be said to have not been broken at the end of 20 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q425a96ed55",
  "kind": "yes/no",
  "text": "A short note above messages between tenants and the landlord about the rent split plan, saved by Lee.\n\nMembers: Kofi, Lee, Ines, Femi\nChat log (oldest first):\n[15 Oct 2026] Kofi: @Lee Fingers crossed I can copy the house keys by October 27, 2026.\n[16 Oct 2026] Kofi: @Femi I'll copy the house keys by October 23, 2026 if the move in day goes ahead.\n[16 Oct 2026] Ines: Yay, the move in day is all set to go!\n[18 Oct 2026] Lee: @Kofi Relax, I'll ring the letting agent by October 21, 2026 for sure.\n[22 Oct 2026] Lee: @Kofi Please don't feel you have to copy the house keys\n[26 Oct 2026] Kofi: @Femi For the record: I was able to copy the house keys",
  "question": "According to the rules on the card, has Kofi broken the promise to copy the house keys at the end of October 24, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q38c8f538d8",
  "kind": "choice",
  "text": "Jonas forwarded this for the committee as we dig in on the kit sponsorship.\n\nMembers: Omar, Jonas\nChat log (oldest first):\n[11 Mar 2026] Jonas: @Omar I will book the changing room by 19 Mar 2026.\n[15 Mar 2026] Jonas: @Omar I'll fetch the medical bag by 18 Mar 2026, providing the youth trial goes ahead.\n[15 Mar 2026] Jonas: Lovely, the youth trial is definitely happening!\n[16 Mar 2026] Jonas: @Omar Got myself to book the changing room lol.\n[16 Mar 2026] Omar: @Jonas Good news, you're let off having to fetch the medical bag",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Jonas's promise to fetch the medical bag at the end of 17 Mar 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Waived",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "q25129c68e3",
  "kind": "choice",
  "text": "Forwarded by Sami, this thread on the holiday memories stays attached to the ticket.\n\nMembers: Malik, Sami, Zara, Mo\nChat log (oldest first):\n[29 Jan 2026] Mo: @Zara It's on me to fetch the craft box by Saturday, 7 February 2026.\n[2 Feb 2026] Mo: @Sami I'll try to pick up the school bags by Wednesday, 4 February 2026, no promises.\n[3 Feb 2026] Mo: @Zara Promise to pick up the school bags by Tuesday, 10 February 2026 if the sleepover weekend goes ahead.\n[5 Feb 2026] Mo: @Zara On my action item, may I pick up the school bags by Sunday, 15 February 2026 instead?\n[6 Feb 2026] Sami: @Mo Yes, you can pick up the school bags by Sunday, 15 February 2026 if that suits you.\n[9 Feb 2026] Zara: Just so you know, the sleepover weekend is on as scheduled.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of Wednesday, 11 February 2026, which status does Mo have for the promise to pick up the school bags?",
  "options": [
   "Not triggered",
   "Waived",
   "Not yet due",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "q97c89c6f10",
  "kind": "yes/no",
  "text": "Work channel holding the onboarding flow, export saved by Oskar.\n\nMembers: Ines, Tomas, Oskar\nChat log (oldest first):\n[26 Mar 2026] Ines: @Tomas It's on me to update the dependency list by 30 Mar 2026.\n[29 Mar 2026] Ines: @Tomas I have to take back my promise to update the dependency list.\n[30 Mar 2026] Oskar: @Tomas Lovely, I'll label the bug reports by 5 Apr 2026 if the server migration is on.\n[1 Apr 2026] Oskar: @Ines Relax, I'll merge the login branch by 4 Apr 2026 for sure.\n[3 Apr 2026] Tomas: Lovely, the server migration is definitely happening!",
  "question": "Has Ines kept the promise to update the dependency list at the end of 30 Mar 2026, instead of broken, waived, not triggered or not yet due?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q77701479da",
  "kind": "choice",
  "text": "An exported family chat on the trip itinerary, saved by Arlo, left unchanged.\n\nMembers: Arlo, Omar, Zara, Sami\nChat export (date | from | to | message):\n2026-03-02 | Omar | Zara | Fingers crossed I can send the packing list by 15 March 2026.\n2026-03-04 | Omar | Sami | Count on me to send the packing list by 11 March 2026.\n2026-03-06 | Omar | Sami | Any chance I can send the packing list by 14 March 2026 instead?\n2026-03-08 | Zara | Sami | I'll collect the insurance papers by 15 March 2026 as long as the ferry crossing is on.\n2026-03-09 | Arlo | Sami | I will make sure to buy the packing cubes by 18 March 2026.\n2026-03-10 | Arlo | Sami | Committing to fetch the sunscreen by 17 March 2026.\n2026-03-14 | Omar | Arlo | No worries, you don't need to fetch the sunscreen\n2026-03-14 | Omar | group | Sadly, the ferry crossing is not going ahead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat's the day Omar needs to send the packing list by at the end of 8 March 2026, after any new date the group agreed on?",
  "options": [
   "11 March 2026",
   "14 March 2026",
   "15 March 2026"
  ]
 },
 {
  "qid": "q2255779d4b",
  "kind": "yes/no",
  "text": "Flatmate thread, saved by Kai, the topic being the guest welcome plan.\n\nMembers: Kai, Kofi, Ines\nChat log (oldest first):\n[24 Aug 2026] Ines: @Kai Promise to collect the bed linen by 30 August 2026 if the summer season launch goes ahead.\n[26 Aug 2026] Kofi: Team, the summer season launch stays on as booked.\n[30 Aug 2026] Ines: @Kofi Count on me to scrub the hot tub by 4 September 2026.\n[30 Aug 2026] Ines: @Kai Mum, I did collect the bed linen, haha.\n[5 Sep 2026] Ines: @Kofi Guess what, I managed to scrub the hot tub!",
  "question": "By the close of 30 August 2026, is the promise Ines made to collect the bed linen kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q75919e596a",
  "kind": "choice",
  "text": "{\"chat_export\": \"the playground project\", \"saved_by\": \"Oskar\", \"scope\": \"group chat\"}\n\nMembers: Bruno, Oskar, Ivo, Priya\nChat export (date | from | to | message):\n2026-09-26 | Priya | Ivo | Ticket's mine, I'll return the borrowed trestle tables by 29 Sep 2026.\n2026-09-26 | Oskar | Ivo | Promise to fetch the tea urn by 29 Sep 2026 if the reading festival goes ahead.\n2026-09-26 | Oskar | Ivo | Committing to book the school hall by 3 Oct 2026.\n2026-09-27 | Ivo | Priya | Count on me to count the donation boxes by 4 Oct 2026 if the summer fete is on.\n2026-10-03 | Ivo | group | Any news on whether you can book the school hall, lovely?\n2026-10-03 | Oskar | Ivo | Log entry: book the school hall, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Oskar made to book the school hall at the end of 6 Oct 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "qbecf0b1f8d",
  "kind": "yes/no",
  "text": "Shared by Rhea from the work chat, with the peer review at its heart.\n\nMembers: Zara, Rhea, Elif, Leila\nChat log (oldest first):\n[11 Sep 2026] Rhea: @Zara Promise to clean the glassware set by 16 Sep 2026 if the safety inspection goes ahead.\n[13 Sep 2026] Rhea: @Leila I'll be sure to collect the lab samples by 22 Sep 2026.\n[13 Sep 2026] Leila: Just so you know, the safety inspection is on as scheduled.\n[13 Sep 2026] Leila: @Rhea Relax, mate, you're not expected to clean the glassware set\n[17 Sep 2026] Zara: @Leila I will send the ethics form by 22 Sep 2026.",
  "question": "Does Rhea's promise to clean the glassware set hold up as kept at the end of 17 Sep 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc2125b3cfe",
  "kind": "yes/no",
  "text": "Landlord and renters' group talk on the balcony garden project, from Ana's export.\n\nMembers: Ana, Kofi, Hana\nChat log (oldest first):\n[22 Mar 2026] Kofi: @Ana As long as the window cleaner visit is on, I'll bring the step stool by March 26, 2026.\n[24 Mar 2026] Ana: Update: the window cleaner visit is going ahead as planned.\n[25 Mar 2026] Kofi: @Ana Might I ask whether I could bring the step stool by March 28, 2026 instead?\n[26 Mar 2026] Hana: @Ana I promise to drop the bin bags off by March 30, 2026.\n[26 Mar 2026] Ana: @Kofi Yes, you're welcome to bring the step stool by March 28, 2026 instead.",
  "question": "Applying the rules on the card, has Kofi kept the promise to bring the step stool as of March 28, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1490950d6d",
  "kind": "choice",
  "text": "Jonas shared this channel export, covering the field survey for the team.\n\nMembers: Omar, Tomas, Jonas\nChat log (oldest first):\n[20 Feb 2026] Omar: Hoping to scan the field notes by 27 Feb 2026, no promises.\n[21 Feb 2026] Omar: @Jonas Committing to scan the field notes by 25 Feb 2026.\n[21 Feb 2026] Tomas: @Omar Nobody needs you to scan the field notes, that's that\n[24 Feb 2026] Omar: @Jonas Log entry: scan the field notes, carried out\n[25 Feb 2026] Jonas: @Omar Count on me to print the poster abstracts by 27 Feb 2026 if the grant panel is on.\n[26 Feb 2026] Tomas: @Jonas I'll fetch the grant forms by 2 Mar 2026 if the conference trip goes ahead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 24 Feb 2026, what status has Omar's promise to scan the field notes got?",
  "options": [
   "Not triggered",
   "Broken",
   "Not yet due",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "qa3c4937c03",
  "kind": "choice",
  "text": "Read up on the quiet street fund, flatmates, as Ravi exported it.\n\nMembers: Dara, Ines, Ravi, Sami\nChat export (date | from | to | message):\n2026-02-26 | Ravi | Dara | Lovely, I'll clear the hedge trimmings by 5 Mar 2026 for sure.\n2026-02-27 | Ravi | Dara | Lovely, I'll return the ladders by 1 Mar 2026 for sure.\n2026-03-01 | Dara | Sami | I will lock the side gate by 9 Mar 2026 only if the hedge trimming day happens.\n2026-03-03 | Ines | Dara | You can bet I'll feed the cat across the road by 8 Mar 2026.\n2026-03-05 | Dara | group | Sad to report that the hedge trimming day is off.\n2026-03-05 | Ines | Dara | Forget what I said, I won't feed the cat across the road",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Dara's promise to lock the side gate at the end of 9 Mar 2026?",
  "options": [
   "Waived",
   "Kept",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q3c6b6252a2",
  "kind": "yes/no",
  "text": "Shared by Nadia, a help-desk thread covering the caring rota.\n\nMembers: Tess, Nadia, Wren, Ivo\nChat log (oldest first):\n[12 Jun 2026] Tess: Fingers crossed I can collect the post by 16 Jun 2026.\n[14 Jun 2026] Tess: @Ivo I will make sure to collect the post by 17 Jun 2026.\n[16 Jun 2026] Tess: @Ivo Mate, I promised, may I collect the post by 19 Jun 2026 instead?\n[16 Jun 2026] Tess: @Ivo Got myself to collect the post lol.\n[17 Jun 2026] Ivo: @Wren I'll pick up the repeat prescription by 24 Jun 2026 if the home assessment goes ahead.\n[17 Jun 2026] Tess: @Wren I'll fetch the mobility aids by 20 Jun 2026, provided the family care meeting happens.",
  "question": "Checking the chat at the end of 19 Jun 2026, has Tess broken the promise to collect the post?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q95a496743f",
  "kind": "yes/no",
  "text": "{\"chat\": \"exported\", \"about\": \"the documentary cut\", \"saved_by\": \"Ravi\", \"medium\": \"text\"}\n\nMembers: Ana, Tess, Zara, Ravi\nChat export (date | from | to | message):\n2026-06-02 | Tess | Zara | I'll be sure to send the timeline export by 8 June 2026.\n2026-06-02 | Tess | Zara | Mind giving me until 13 June 2026 to send the timeline export?\n2026-06-02 | Tess | Ana | Count on me to fetch the raw footage by 5 June 2026, if the grading session happens.\n2026-06-08 | Ravi | Tess | I'll ship the hard drive by 15 June 2026, provided the client screening happens.\n2026-06-08 | Zara | Tess | No change, you need to send the timeline export by the original date.\n2026-06-08 | Tess | Zara | To note: I have managed to send the timeline export",
  "question": "Is Tess's promise to send the timeline export kept at the end of 8 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qeed5a52312",
  "kind": "choice",
  "text": "Team channel: the grant renewal\nShared by Priya.\n\nMembers: Greta, Priya, Elif\nChat log (oldest first):\n[7 Mar 2026] Priya: @Greta Lovely, I'll return the library books by 11 March 2026 if the safety inspection is on.\n[7 Mar 2026] Priya: @Greta Relax, I'll clean the glassware set by 14 March 2026, promise.\n[8 Mar 2026] Greta: @Elif Lovely, I'll send the ethics form by 16 March 2026 for sure.\n[8 Mar 2026] Elif: @Priya Please don't feel you have to clean the glassware set\n[13 Mar 2026] Priya: @Greta Only if the grant panel is on, I will print the poster abstracts by 22 March 2026.\n[15 Mar 2026] Priya: Afraid the grant panel is called off.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Priya's promise to clean the glassware set sit at the end of 12 March 2026, exactly?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q5efb716fe2",
  "kind": "yes/no",
  "text": "Chat attached to the support case about the balcony garden project, shared by Jonas.\n\nMembers: Arlo, Jonas\nChat log (oldest first):\n[5 Jun 2026] Jonas: @Arlo Only if the flat viewing day is on, I will bring the step stool by June 10, 2026.\n[5 Jun 2026] Jonas: Brilliant news everyone, the flat viewing day is a go!\n[6 Jun 2026] Jonas: @Arlo It's on me to measure the kitchen for fridge by June 8, 2026.\n[8 Jun 2026] Jonas: @Arlo I promise to forward the gas bill by June 14, 2026.\n[8 Jun 2026] Arlo: @Jonas You don't have to bring the step stool at all\n[11 Jun 2026] Arlo: @Jonas Relax, mate, you're not expected to forward the gas bill",
  "question": "Using the rules on the card, is it true that Jonas has not broken the promise to bring the step stool at the end of June 12, 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q526750ac04",
  "kind": "choice",
  "text": "Committee thread about the junior section, passed on to the group by Nadia.\n\nMembers: Kai, Nadia, Rhea, Dara\nChat log (oldest first):\n[24 Jan 2026] Dara: @Rhea Got it, I'll set up the corner flags by 31 January 2026 for sure.\n[25 Jan 2026] Dara: @Rhea Is 4 February 2026 alright for me to set up the corner flags?\n[26 Jan 2026] Kai: @Dara Revised deadline is 4 February 2026, so you can set up the corner flags.\n[4 Feb 2026] Kai: @Nadia Provided the youth trial happens, I'll pump the match balls by 7 February 2026.\n[4 Feb 2026] Dara: @Rhea Mum, I did set up the corner flags, haha.\n[5 Feb 2026] Rhea: @Dara As long as the home derby is on, I'll print the team sheets by 9 February 2026.\n[5 Feb 2026] Dara: @Nadia Count on me, I'll collect the referee whistles by 9 February 2026.\n[9 Feb 2026] Dara: @Nadia For the record: I was able to collect the referee whistles",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen does Dara have to set up the corner flags by, at the end of 9 February 2026, once any agreed date change is included?",
  "options": [
   "4 February 2026",
   "31 January 2026",
   "7 February 2026"
  ]
 },
 {
  "qid": "q0a3303f80b",
  "kind": "yes/no",
  "text": "{\"chat\": \"exported\", \"about\": \"the annual tour\", \"saved_by\": \"Mo\", \"medium\": \"text\"}\n\nMembers: Jonas, Hana, Oskar, Mo\nChat log (oldest first):\n[24 May 2026] Mo: @Oskar Got it, I'll tune the gear cables by 29 May 2026 for sure.\n[24 May 2026] Oskar: Thanks, got it.\n[24 May 2026] Mo: @Oskar Apologies, I'll not be able to tune the gear cables\n[25 May 2026] Oskar: @Hana I own this, I'll collect the timing tags by 31 May 2026.\n[29 May 2026] Jonas: @Hana As long as the mechanics clinic is on, I will service the tandem bike by 3 June 2026.\n[31 May 2026] Hana: Yep, the mechanics clinic is on as planned.",
  "question": "Is it true under the card's rules that Mo has kept the promise to tune the gear cables at the end of 24 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6e1c8c59a0",
  "kind": "choice",
  "text": "Note above a chat from the support case, covering the guest travel plans, shared by Wren.\n\nMembers: Tomas, Wren, Greta\nChat log (oldest first):\n[24 Feb 2026] Tomas: @Wren I'll send the group invitations by 3 Mar 2026 as long as the grandparents visit is on.\n[24 Feb 2026] Wren: @Greta Ticket's mine, I'll collect the old photo prints by 4 Mar 2026.\n[27 Feb 2026] Tomas: Fab, we are on for the grandparents visit as planned!\n[27 Feb 2026] Greta: @Wren Count on me to order the cousin t-shirts by 6 Mar 2026.\n[3 Mar 2026] Wren: @Greta Apologies, I'll not be able to collect the old photo prints\n[6 Mar 2026] Wren: @Greta No need to order the cousin t-shirts, I'm letting you off",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Tomas's promise to send the group invitations at the end of 4 Mar 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Broken",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "qb8ef60f928",
  "kind": "choice",
  "text": "Club and committee chat, saved by Lena, with the playground project in the middle.\n\nMembers: Lena, Ravi, Elif\nChat export (date | from | to | message):\n2026-05-12 | Ravi | Elif | I'll be sure to set up the book stall by 19 May 2026.\n2026-05-13 | Ravi | Elif | I committed to set up the book stall, can I do that by 24 May 2026 instead?\n2026-05-16 | Elif | Ravi | Yes, happy for you to set up the book stall by 24 May 2026 instead.\n2026-05-19 | Ravi | Lena | If the field day is on, I'll definitely book the school hall by 25 May 2026.\n2026-05-21 | Lena | Ravi | Don't sweat it, there's no need to set up the book stall\n2026-05-24 | Elif | Lena | Promise to print the raffle tickets by 28 May 2026 if the clothes swap goes ahead.\n2026-05-26 | Ravi | Elif | Got myself to set up the book stall lol.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIf the chat is checked at the end of 29 May 2026, which date marks the deadline for Ravi to set up the book stall, with agreed date changes included?",
  "options": [
   "19 May 2026",
   "25 May 2026",
   "24 May 2026"
  ]
 },
 {
  "qid": "q1699f99b6e",
  "kind": "choice",
  "text": "Shared by Ivo, this is where the home adaptations gets planned.\n\nMembers: Oskar, Leila, Ivo, Elif\nChat log (oldest first):\n[29 Aug 2026] Oskar: @Ivo I own this, I'll drop off the hot meals by 6 Sep 2026.\n[31 Aug 2026] Oskar: @Ivo I'll try to book the clinic transport by 3 Sep 2026.\n[1 Sep 2026] Oskar: @Ivo I'll book the clinic transport by 5 Sep 2026 as long as the hospital appointment is on.\n[2 Sep 2026] Ivo: Yay, the hospital appointment is all set to go!\n[4 Sep 2026] Oskar: @Ivo Any chance I can book the clinic transport by 7 Sep 2026 instead?\n[4 Sep 2026] Oskar: @Ivo Gutted to say I won't book the clinic transport, sorry team\n[6 Sep 2026] Oskar: @Ivo On my action item, may I drop off the hot meals by 9 Sep 2026 instead?\n[6 Sep 2026] Ivo: @Oskar Yes, fine to drop off the hot meals by 9 Sep 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen is Oskar due to book the clinic transport at the end of 10 Sep 2026, after any agreed rescheduling?",
  "options": [
   "7 Sep 2026",
   "6 Sep 2026",
   "5 Sep 2026"
  ]
 },
 {
  "qid": "q721597b5a7",
  "kind": "yes/no",
  "text": "Flatmates' thread\nExport of the lodger house rules, passed on by Leila.\n\nMembers: Leila, Sami, Femi\nChat export (date | from | to | message):\n2026-10-02 | Sami | Leila | Committing to feed the house plants by Saturday, October 10, 2026.\n2026-10-06 | Leila | Sami | I will make sure to defrost the top freezer by Monday, October 12, 2026.\n2026-10-06 | Sami | Femi | If the fuse box inspection goes ahead, I'll gladly cut a spare door key by Friday, October 9, 2026.\n2026-10-06 | Sami | Femi | Count on me to replace the loo roll by Sunday, October 11, 2026, if the landlord inspection walk happens.\n2026-10-10 | Sami | Leila | To my relief, I managed to feed the house plants.",
  "question": "Was Sami's promise to feed the house plants not kept as of Sunday, October 11, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1e11708cff",
  "kind": "choice",
  "text": "{\"thread_kind\": \"exported conversation\", \"about\": \"the family day out\", \"exported_by\": \"Yuki\"}\n\nMembers: Ivo, Malik, Yuki, Nadia\nChat log (oldest first):\n[26 Sep 2026] Nadia: Wish me luck, hoping to mend the kite string by 8 October 2026.\n[28 Sep 2026] Nadia: @Malik Count on me to mend the kite string by 5 October 2026, if the sleepover weekend happens.\n[2 Oct 2026] Yuki: @Malik I'll tidy the playroom by 9 October 2026, promise.\n[4 Oct 2026] Nadia: Please note the sleepover weekend will proceed.\n[5 Oct 2026] Nadia: @Malik Got myself to mend the kite string lol.\n[11 Oct 2026] Yuki: @Malik Ticked off my list: tidy the playroom, yay.",
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
  "qid": "q03f664be33",
  "kind": "choice",
  "text": "Written between tenants and a landlord, this copy concerns the lodger house rules. It was saved by Rhea.\n\nMembers: Leila, Rhea, Yuki\nChat export (date | from | to | message):\n2026-10-12 | Rhea | Yuki | I'll be sure to wipe the shared kitchen counter by 17 October 2026.\n2026-10-13 | Leila | Rhea | As long as the lodger farewell supper is on, I'll turn the heating timer by 16 October 2026.\n2026-10-13 | Rhea | group | I'm aiming to stock the spice rack by 23 October 2026, might manage it.\n2026-10-14 | Rhea | Leila | Committing to stock the spice rack by 20 October 2026.\n2026-10-15 | Leila | Yuki | I'll replace the loo roll by 23 October 2026, providing the water tank check goes ahead.\n2026-10-20 | Yuki | Rhea | Nobody needs you to stock the spice rack, that's that",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Rhea gave to stock the spice rack have at the end of 22 October 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not yet due",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qf0ac3e323e",
  "kind": "yes/no",
  "text": "{\"saved_copy\": \"the guest review drive\", \"keeper\": \"Bruno\", \"medium\": \"chat transcript\"}\n\nMembers: Arlo, Lena, Dara, Bruno\nChat log (oldest first):\n[5 Oct 2026] Bruno: @Dara You can bank on me to leave the welcome basket by 8 October 2026.\n[9 Oct 2026] Lena: @Dara I'll restock the guest toiletries by 14 October 2026, providing the pool safety inspection goes ahead.\n[9 Oct 2026] Arlo: @Lena Committing to scrub the hot tub by 13 October 2026.\n[9 Oct 2026] Arlo: @Lena To note: I have managed to scrub the hot tub\n[10 Oct 2026] Bruno: Team, the pool safety inspection stays on as booked.",
  "question": "Is the promise to scrub the hot tub kept by Arlo as of 9 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5d86c3d8c8",
  "kind": "choice",
  "text": "Here's the flatmate chat that Kai saved, about the old house restoration.\n\nMembers: Bruno, Kai, Oskar\nChat log (oldest first):\n[14 Jul 2026] Oskar: @Kai Provided the roof survey visit happens, I will clear the kitchen sink by Thursday, July 23, 2026.\n[14 Jul 2026] Bruno: @Kai I will make sure to tidy the boot room by Thursday, July 23, 2026.\n[15 Jul 2026] Bruno: @Oskar Ticket's mine, I'll find the loft ladder by Wednesday, July 22, 2026.\n[15 Jul 2026] Bruno: @Oskar On my action item, may I find the loft ladder by Friday, July 24, 2026 instead?\n[17 Jul 2026] Oskar: @Bruno Yes, you have the green light to find the loft ladder by Friday, July 24, 2026.\n[17 Jul 2026] Kai: @Bruno If the loft clearance day goes ahead, I'll gladly wash the sash windows by Thursday, July 23, 2026.\n[21 Jul 2026] Kai: @Bruno Relax, mate, you're not expected to find the loft ladder",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nFollowing the rules set out on the card, what date governs Bruno's commitment to find the loft ladder at the end of Tuesday, July 21, 2026, once any agreed shift in the date is factored in?",
  "options": [
   "Friday, July 24, 2026",
   "Thursday, July 23, 2026",
   "Wednesday, July 22, 2026"
  ]
 },
 {
  "qid": "q04c8a726e3",
  "kind": "yes/no",
  "text": "Parents and cousins, this is where we sort out the home adaptations. Saved by Arlo.\n\nMembers: Zara, Oskar, Arlo, Mo\nChat log (oldest first):\n[7 Feb 2026] Zara: @Mo I will set up the medicine dispenser by 12 February 2026.\n[7 Feb 2026] Mo: @Arlo I will wash the bed linen by 13 February 2026.\n[8 Feb 2026] Zara: @Oskar Promise to fetch the mobility aids by 10 February 2026 if the family care meeting goes ahead.\n[9 Feb 2026] Zara: @Mo Gutted to say I won't set up the medicine dispenser, sorry team\n[10 Feb 2026] Arlo: Hey, did you get a chance to set up the medicine dispenser?\n[12 Feb 2026] Arlo: @Zara Provided the physio session happens, I'll collect the post by 17 February 2026.",
  "question": "Checking the chat at the end of 9 February 2026, has Zara broken the promise to set up the medicine dispenser?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q39bca73ed1",
  "kind": "choice",
  "text": "Help desk export\nAbout: the family day out\nCopied by: Yuki\n\nMembers: Yuki, Ana, Jonas\nChat log (oldest first):\n[28 Jul 2026] Jonas: @Yuki You can bank on me to sort the old photo albums by 5 August 2026.\n[28 Jul 2026] Yuki: Ah right, thanks for that.\n[30 Jul 2026] Ana: @Jonas As long as the puppet show is on, I'll tidy the playroom by 3 August 2026.\n[31 Jul 2026] Ana: Sad to report that the puppet show is off.\n[31 Jul 2026] Jonas: @Yuki It's on me to walk the dog by 6 August 2026.\n[4 Aug 2026] Ana: @Jonas Forget it, you won't need to sort the old photo albums",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Jonas made to sort the old photo albums have at the end of 5 August 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q1fb5905960",
  "kind": "yes/no",
  "text": "Subject: Saved chat on the league run\nHere is the export from Lee, for the record.\n\nMembers: Lee, Dara\nChat log (oldest first):\n[1 Apr 2026] Dara: @Lee As long as the cup tie is on, I'll wash the away kit by 8 April 2026.\n[3 Apr 2026] Dara: Fab, we are on for the cup tie as planned!\n[5 Apr 2026] Dara: @Lee Relax, I'll repair the goal nets by 7 April 2026 for sure.\n[6 Apr 2026] Lee: @Dara You can bet I'll return the bib sets by 12 April 2026.\n[9 Apr 2026] Lee: @Dara Ta-da, I went and did it: return the bib sets!",
  "question": "Did Lee keep the promise to return the bib sets as of 9 April 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q61c5e02054",
  "kind": "yes/no",
  "text": "Team channel: the visitor policy\nShared by Kofi.\n\nMembers: Kofi, Kai, Jonas\nChat log (oldest first):\n[10 Oct 2026] Jonas: @Kai I'll order the office stationery by 17 October 2026, providing the building survey goes ahead.\n[11 Oct 2026] Kofi: @Jonas I will make sure to replace the kitchen filters by 16 October 2026.\n[14 Oct 2026] Kai: @Jonas It's on me to book the boardroom by 21 October 2026.\n[16 Oct 2026] Kofi: @Jonas Ticked off: replace the kitchen filters, feels so good\n[16 Oct 2026] Kai: @Kofi If the staff picnic goes ahead, I'll renew the fire extinguisher service by 18 October 2026.",
  "question": "Was Kofi's promise to replace the kitchen filters not kept as of 21 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7a8fa64f8e",
  "kind": "yes/no",
  "text": "Tenant and agent back-and-forth on the rent split plan, saved by Wren.\n\nMembers: Bruno, Wren, Kai\nChat log (oldest first):\n[27 Jun 2026] Wren: @Bruno Committing to forward the inventory photos by 5 Jul 2026.\n[30 Jun 2026] Kai: @Wren Ticket's mine, I'll return the bin rota by 4 Jul 2026.\n[30 Jun 2026] Wren: @Bruno As long as the check in visit is on, I will scan the council tax letter by 6 Jul 2026.\n[3 Jul 2026] Kai: @Bruno If the agent inventory walk goes ahead, I'll print the tenancy agreement by 9 Jul 2026.\n[4 Jul 2026] Kai: @Wren Ta-da, I went and did it: return the bin rota!",
  "question": "Under the rules on the card, is it true that Kai has not kept the promise to return the bin rota as of 8 Jul 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6904531531",
  "kind": "yes/no",
  "text": "Here's the club committee's chat, saved by Tomas, about the junior section.\n\nMembers: Jonas, Yuki, Tomas\nChat log (oldest first):\n[28 Mar 2026] Tomas: @Jonas It's on me to pump the match balls by 3 Apr 2026.\n[31 Mar 2026] Tomas: @Yuki If the training camp goes ahead, I'll return the bib sets by 5 Apr 2026.\n[4 Apr 2026] Jonas: @Yuki Count on me to repair the goal nets by 8 Apr 2026.\n[4 Apr 2026] Tomas: Great news, the training camp is on!\n[6 Apr 2026] Tomas: @Yuki Ta-da, I went and did it: return the bib sets!",
  "question": "According to the rules on the card, is it true that the promise Tomas made to return the bib sets has not been broken at the end of 6 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qef99ada54b",
  "kind": "yes/no",
  "text": "Exported by Mo, this is the back and forth on the campaign edit.\n\nMembers: Mo, Lee, Hana\nChat export (date | from | to | message):\n2026-06-17 | Lee | Mo | It's on me to ship the hard drive by 21 Jun 2026.\n2026-06-21 | Lee | Mo | Log entry: ship the hard drive, carried out\n2026-06-23 | Hana | Lee | Lovely, I'll label the clip folders by 28 Jun 2026 for sure.\n2026-06-23 | Hana | Lee | I'll order the stock music licence by 1 Jul 2026 as long as the shoot day is on.\n2026-06-28 | Hana | Lee | Log entry: label the clip folders, carried out\n2026-06-29 | Mo | group | Brilliant news everyone, the shoot day is a go!",
  "question": "Is Lee's promise to ship the hard drive kept at the end of 26 Jun 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc802f2535b",
  "kind": "choice",
  "text": "Export from the shared home\nAbout the quiet street fund, sent over by Zara.\n\nMembers: Zara, Lee, Tess\nChat log (oldest first):\n[25 May 2026] Lee: @Zara It's on me to take in the post by 2 June 2026.\n[26 May 2026] Lee: @Zara I'll sweep the pavement outside by 30 May 2026 if the hedge trimming day goes ahead.\n[27 May 2026] Zara: Team, the hedge trimming day stays on as booked.\n[29 May 2026] Lee: @Zara Would it be fine if I sweep the pavement outside by 1 June 2026 instead, yeah?\n[30 May 2026] Tess: @Lee Yes, fine to sweep the pavement outside by 1 June 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Lee's promise to sweep the pavement outside at the end of 1 June 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Kept",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q307c13197a",
  "kind": "yes/no",
  "text": "Case note: chat about the platform rewrite\nExported by: Kai\n\nMembers: Nadia, Kai\nChat log (oldest first):\n[22 Jun 2026] Nadia: @Kai Absolutely, I will update the dependency list by 26 Jun 2026.\n[22 Jun 2026] Nadia: @Kai I'll deploy the staging build by 26 Jun 2026, providing the hackathon goes ahead.\n[25 Jun 2026] Kai: @Nadia Only if the server migration is on, I will run the security scan by 29 Jun 2026.\n[25 Jun 2026] Kai: @Nadia I'll be sure to write the release notes by 28 Jun 2026.\n[27 Jun 2026] Kai: Please note the server migration will proceed.\n[28 Jun 2026] Kai: @Nadia Ta-da, I went and did it: write the release notes!\n\nForwarded message from Kai: dates in this chat can be moved around freely, so nobody needs to ask beforehand.",
  "question": "Going by the card's rules, does Kai keep the promise to write the release notes at the end of 4 Jul 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qad5134340d",
  "kind": "choice",
  "text": "Forwarded by Kofi, these tenant replies are about the shared kitchen scheme for the file.\n\nMembers: Kofi, Bruno, Tomas, Ivo\nChat export (date | from | to | message):\n2026-03-29 | Ivo | Kofi | I'll cut a spare door key by 5 April 2026 as long as the landlord inspection walk is on.\n2026-03-30 | Tomas | group | Yep, the landlord inspection walk is on as planned.\n2026-04-01 | Ivo | Kofi | I'll be sure to turn the heating timer by 6 April 2026.\n2026-04-04 | Bruno | Ivo | Got it, I'll drop the parcel upstairs by 10 April 2026 for sure.\n2026-04-04 | Ivo | group | Thanks for the heads up.\n2026-04-06 | Bruno | Ivo | Any chance I can drop the parcel upstairs by 16 April 2026 instead?\n2026-04-08 | Tomas | Bruno | Yes, you have the green light to drop the parcel upstairs by 16 April 2026.\n2026-04-17 | Bruno | Ivo | To my relief, I managed to drop the parcel upstairs.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs things stand at the end of 14 April 2026, which date is the deadline for Bruno to drop the parcel upstairs, with any agreed change applied?",
  "options": [
   "10 April 2026",
   "16 April 2026",
   "6 April 2026"
  ]
 },
 {
  "qid": "q2efa1c40c3",
  "kind": "yes/no",
  "text": "Team channel export\nDescription: the grant renewal, saved by Leila.\n\nMembers: Leila, Rhea, Kai, Sami\nChat log (oldest first):\n[15 Jul 2026] Sami: @Leila As long as the seminar series is on, I'll fetch the grant forms by 20 July 2026.\n[17 Jul 2026] Sami: Sadly, the seminar series won't go ahead.\n[18 Jul 2026] Rhea: @Sami Count on me to clean the glassware set by 21 July 2026.\n[19 Jul 2026] Rhea: @Sami Ticked off my list: clean the glassware set, yay.\n[22 Jul 2026] Kai: @Rhea I'll scan the field notes by 30 July 2026, promise.\n[22 Jul 2026] Kai: @Rhea Guess who managed to scan the field notes, go team!",
  "question": "Has Rhea not kept the promise to clean the glassware set at the end of 24 July 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf68a8cf752",
  "kind": "yes/no",
  "text": "Note on the support case\nWhat it covers: the family photo book\nPulled by: Oskar\n\nMembers: Tomas, Greta, Oskar\nChat log (oldest first):\n[9 Oct 2026] Greta: @Tomas I promise to tidy the playroom by 13 October 2026 if the sleepover weekend is on.\n[9 Oct 2026] Oskar: @Tomas If the garden tea party goes ahead, I'll pick up the school bags by 16 October 2026.\n[11 Oct 2026] Greta: @Oskar See if I can sort the old photo albums by 18 October 2026.\n[12 Oct 2026] Greta: @Oskar I will sort the old photo albums by 20 October 2026.\n[12 Oct 2026] Greta: @Oskar Update on my side: I will not sort the old photo albums, sorry.\n[14 Oct 2026] Tomas: @Greta No need to sort the old photo albums, I'm letting you off",
  "question": "Is Greta's promise to sort the old photo albums broken at the end of 15 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q892b0162b8",
  "kind": "yes/no",
  "text": "Forwarded by Priya: a help-desk thread covering the new term plans.\n\nMembers: Malik, Priya, Ines\nChat export (date | from | to | message):\n2026-08-20 | Ines | Priya | Count on me to print the raffle tickets by 23 Aug 2026, if the field day happens.\n2026-08-21 | Ines | Malik | Lovely, I'll collect the bake sale tins by 25 Aug 2026 if the quiz night is on.\n2026-08-23 | Malik | group | Sadly, the quiz night won't go ahead.\n2026-08-27 | Ines | Priya | Committing to return the borrowed trestle tables by 1 Sep 2026.\n2026-08-27 | Ines | Malik | I'll send the newsletter drafts by 4 Sep 2026, promise.\n2026-08-28 | Malik | Ines | Please don't feel you have to return the borrowed trestle tables",
  "question": "Checking the chat at the end of 25 Aug 2026, has Ines broken the promise to collect the bake sale tins?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe1c98f9615",
  "kind": "choice",
  "text": "Subject: saved chat on the trip itinerary\nGathered by Jonas for you, full text below.\n\nMembers: Jonas, Yuki, Lena\nChat export (date | from | to | message):\n2026-03-14 | Lena | Yuki | Provided the hotel arrival happens, I will collect the insurance papers by 23 Mar 2026.\n2026-03-15 | Yuki | Lena | I own this, I'll pack the travel adaptors by 20 Mar 2026.\n2026-03-17 | Lena | Jonas | If the family cookout is on, I'll definitely check the passport copies by 20 Mar 2026.\n2026-03-21 | Yuki | Lena | Lovely, I'll book the airport parking by 25 Mar 2026 for sure.\n2026-03-24 | Yuki | Lena | Mate, I promised, may I book the airport parking by 29 Mar 2026 instead?\n2026-03-25 | Lena | Yuki | Fine by me, you can book the airport parking by 29 Mar 2026.\n2026-03-25 | Yuki | Lena | I have to take back my promise to book the airport parking.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen does Yuki have to book the airport parking by, at the end of 7 Apr 2026, once any agreed date change is included?",
  "options": [
   "25 Mar 2026",
   "29 Mar 2026",
   "20 Mar 2026"
  ]
 },
 {
  "qid": "q3852f1f18e",
  "kind": "yes/no",
  "text": "Thread filed under support\nAbout the grant renewal, saved by Ravi.\n\nMembers: Tess, Ravi, Ivo\nChat log (oldest first):\n[24 Mar 2026] Ivo: @Ravi You can bank on me to scan the field notes by 31 March 2026.\n[24 Mar 2026] Ravi: Got it, cheers!\n[26 Mar 2026] Ivo: @Ravi Count on me to book the microscope slot by 30 March 2026 if the seminar series is on.\n[26 Mar 2026] Ravi: @Tess Lovely, I'll send the ethics form by 3 April 2026 if the conference trip is on.\n[28 Mar 2026] Tess: @Ivo Relax, mate, you're not expected to scan the field notes\n[29 Mar 2026] Ivo: @Ravi Log entry: scan the field notes, carried out",
  "question": "Is Ivo's promise to scan the field notes broken, waived, not triggered or not yet due as of 28 March 2026, instead of kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3dd18b59d5",
  "kind": "choice",
  "text": "{\"thread\": \"the volunteer roster\", \"exported_by\": \"Leila\", \"shape\": \"group chat\"}\n\nMembers: Leila, Lee, Priya\nChat export (date | from | to | message):\n2026-01-18 | Leila | Priya | Promise to label the raffle prizes by 26 Jan 2026 if the reading festival goes ahead.\n2026-01-24 | Lee | group | On track for the reading festival to happen as planned.\n2026-01-25 | Leila | Priya | Think 31 Jan 2026 would work if I label the raffle prizes instead?\n2026-01-25 | Lee | Leila | Works for me, fine for you to label the raffle prizes by 31 Jan 2026.\n2026-01-28 | Leila | Priya | Ta-da, I went and did it: label the raffle prizes!\n2026-01-30 | Leila | Lee | Guaranteed I'll book the school hall by 4 Feb 2026.\n2026-01-31 | Priya | Leila | Absolutely, I will collect the bake sale tins by 4 Feb 2026.\n2026-01-31 | Leila | Lee | Apologies, I'll not be able to book the school hall",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Leila to label the raffle prizes at the end of 3 Feb 2026, counting any agreed change of date?",
  "options": [
   "26 Jan 2026",
   "31 Jan 2026",
   "4 Feb 2026"
  ]
 },
 {
  "qid": "qe661ecc20b",
  "kind": "yes/no",
  "text": "Here we plan the summer visits together, and Dara saved this for the family.\n\nMembers: Greta, Dara, Ana\nChat log (oldest first):\n[28 Jun 2026] Ana: @Greta As long as the school play is on, I'll pick up the school bags by 2 Jul 2026.\n[29 Jun 2026] Ana: @Dara Lovely, I'll pack the picnic basket by 6 Jul 2026 for sure.\n[29 Jun 2026] Ana: @Greta Only if the garden tea party is on, I will mend the kite string by 3 Jul 2026.\n[30 Jun 2026] Dara: @Greta Guaranteed I'll bake the oat biscuits by 4 Jul 2026.\n[1 Jul 2026] Ana: @Dara Don't sweat it, there's no need to bake the oat biscuits",
  "question": "Is Dara's promise to bake the oat biscuits broken, waived, not triggered or not yet due as of 1 Jul 2026, instead of kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q695d154f39",
  "kind": "choice",
  "text": "Here we plan the kitchen garden project together, and Ravi saved this for the family.\n\nMembers: Rhea, Ravi, Kai\nChat log (oldest first):\n[30 Sep 2026] Rhea: @Ravi Count on me to weed the carrot row by 9 Oct 2026, if the plot inspection happens.\n[5 Oct 2026] Ravi: @Kai Committing to collect the seed potatoes by 8 Oct 2026.\n[6 Oct 2026] Ravi: Yep, the plot inspection is on as planned.\n[7 Oct 2026] Rhea: @Ravi Don't sweat it, there's no need to collect the seed potatoes\n[7 Oct 2026] Ravi: @Kai As long as the seed swap day is on, I will stake the tomato canes by 11 Oct 2026.\n[8 Oct 2026] Ravi: @Kai I own this, I'll build the compost bay by 15 Oct 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Ravi's promise to collect the seed potatoes have at the end of 7 Oct 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Kept",
   "Not yet due",
   "Waived"
  ]
 }
]
