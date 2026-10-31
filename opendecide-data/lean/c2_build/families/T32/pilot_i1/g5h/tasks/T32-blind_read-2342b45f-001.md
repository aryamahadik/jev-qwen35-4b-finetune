# G5-H blind read T32-blind_read-2342b45f-001 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T32/pilot_i1/g5h/answers/T32-blind_read-2342b45f-001.json

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
  "qid": "q93eddc4d4f",
  "kind": "yes/no",
  "text": "Subject: copy of the chat about the showreel refresh\nFor your records, the saved chat is below, from Mo.\n\nMembers: Femi, Elif, Mo, Ivo\nChat export (date | from | to | message):\n2026-06-03 | Mo | Elif | You can bank on me to upload the render files by 9 Jun 2026.\n2026-06-03 | Femi | Mo | Provided the grading session happens, I will fetch the raw footage by 7 Jun 2026.\n2026-06-03 | Mo | group | Yep, the grading session is on as planned.\n2026-06-05 | Ivo | Mo | Ah, no stress, no need for you to upload the render files\n2026-06-09 | Mo | Elif | Got myself to upload the render files lol.",
  "question": "Per the card's rules, on 11 Jun 2026, has Mo's promise to upload the render files been broken, waived, not triggered or not yet due, rather than kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q93b10db792",
  "kind": "choice",
  "text": "Shared by Mo, this thread covers the autumn term budget for whoever is at the help desk.\n\nMembers: Mo, Ana, Elif\nChat log (oldest first):\n[10 Jul 2026] Mo: @Elif Count on me to store the spare bike by 2026-07-18.\n[11 Jul 2026] Ana: @Mo Please don't feel you have to store the spare bike\n[14 Jul 2026] Elif: No promises, but I'll aim to copy the house keys by 2026-07-16.\n[15 Jul 2026] Elif: @Mo Got it, I'll copy the house keys by 2026-07-21 for sure.\n[20 Jul 2026] Elif: @Mo Might I ask whether I could copy the house keys by 2026-07-25 instead?\n[21 Jul 2026] Elif: @Mo Ticked off my list: copy the house keys, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of 2026-07-22, what is the date by which Elif has to copy the house keys, counting any agreed change?",
  "options": [
   "2026-07-21",
   "2026-07-18",
   "2026-07-25"
  ]
 },
 {
  "qid": "qef47617863",
  "kind": "yes/no",
  "text": "Project thread between a freelancer and a client on the rebrand package, saved by Omar.\n\nMembers: Omar, Nadia, Femi\nChat log (oldest first):\n[28 May 2026] Nadia: @Femi Count on me to collect the photo credits by June 5, 2026 if the shop fitting is on.\n[4 Jun 2026] Nadia: Fab, we are on for the shop fitting as planned!\n[4 Jun 2026] Nadia: @Femi Think June 11, 2026 would work if I collect the photo credits instead?\n[4 Jun 2026] Nadia: @Femi Forget what I said, I won't collect the photo credits",
  "question": "Has Nadia broken the promise to collect the photo credits at the end of June 8, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q594cc80c88",
  "kind": "yes/no",
  "text": "Subject: Chat about the peer review\nThe copy from Zara follows below as a plain record.\n\nMembers: Zara, Hana, Kofi, Greta\nChat log (oldest first):\n[4 Mar 2026] Hana: Might be able to clean the glassware set by 2026-03-09, who knows!\n[8 Mar 2026] Greta: @Kofi Count on me to print the poster abstracts by 2026-03-15.\n[10 Mar 2026] Hana: Update on your plan to print the poster abstracts?\n[12 Mar 2026] Greta: @Zara I'll book the microscope slot by 2026-03-16 as long as the seminar series is on.\n[15 Mar 2026] Greta: Sorry all, the seminar series is not happening.\n[15 Mar 2026] Hana: @Greta You don't have to print the poster abstracts at all\n[15 Mar 2026] Greta: @Kofi Ticked off: print the poster abstracts, feels so good",
  "question": "Does the card classify Greta's promise to print the poster abstracts as broken, waived, not triggered or not yet due, rather than kept, on 2026-03-15?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa374c2f90a",
  "kind": "choice",
  "text": "{\"record\": \"shared group chat\", \"subject\": \"the family history\", \"shared_by\": \"Arlo\", \"stored\": \"as text\"}\n\nMembers: Malik, Arlo, Priya, Rhea\nChat log (oldest first):\n[11 Aug 2026] Arlo: @Malik Relax, I'll send the group invitations by 15 Aug 2026, promise.\n[11 Aug 2026] Malik: Thanks lovely, got it!\n[11 Aug 2026] Priya: @Arlo No need to send the group invitations, I'm letting you off\n[12 Aug 2026] Priya: I'll try to print the family tree chart by 16 Aug 2026.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Arlo's promise to send the group invitations at the end of 13 Aug 2026?",
  "options": [
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q3b5215c1f0",
  "kind": "choice",
  "text": "Team thread shared by Tess, covering the grant renewal in the channel.\n\nMembers: Tess, Ana, Femi, Ravi\nChat log (oldest first):\n[12 Apr 2026] Ravi: @Ana I promise to send the ethics form by April 18, 2026 if the conference trip is on.\n[16 Apr 2026] Ana: Hoping to return the library books by April 25, 2026, no promises.\n[17 Apr 2026] Ravi: Sadly, the conference trip won't go ahead.\n[17 Apr 2026] Ana: @Femi Relax, I'll return the library books by April 23, 2026, promise.\n[18 Apr 2026] Ravi: @Ana No need to return the library books, I'm letting you off\n[21 Apr 2026] Ravi: Just checking in, did you manage to return the library books?",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Ana's promise to return the library books at the end of April 27, 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not yet due",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "q82d48d1ad1",
  "kind": "yes/no",
  "text": "{\"record\": \"shared group chat\", \"subject\": \"the family history\", \"shared_by\": \"Oskar\", \"stored\": \"as text\"}\n\nMembers: Lee, Oskar, Jonas, Wren\nChat log (oldest first):\n[25 Jul 2026] Lee: @Jonas Count on me to fetch the speaker system by 30 Jul 2026.\n[27 Jul 2026] Wren: I'll try to print the family tree chart by 5 Aug 2026, no promises.\n[27 Jul 2026] Oskar: @Lee Relax, mate, you're not expected to fetch the speaker system\n[30 Jul 2026] Lee: @Jonas Guess what, I managed to fetch the speaker system!",
  "question": "Under the rules on the card, is it true that Lee has not kept the promise to fetch the speaker system as of 30 Jul 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc594e93af0",
  "kind": "yes/no",
  "text": "Team channel: the trade show push\nExported by Rhea.\n\nMembers: Rhea, Priya, Arlo\nChat export (date | from | to | message):\n2026-06-19 | Priya | Rhea | Hoping to draft the press release by 27 Jun 2026, but can't promise.\n2026-06-20 | Priya | Arlo | I'll draft the press release by 24 Jun 2026, provided the annual review happens.\n2026-06-21 | Rhea | group | Really pleased to say the annual review will go ahead!\n2026-06-25 | Arlo | Priya | Absolutely, I will book the photo studio by 29 Jun 2026.\n2026-06-29 | Arlo | Priya | I need to take back my commitment to book the photo studio.",
  "question": "Has Priya broken the promise to draft the press release at the end of 27 Jun 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qedcc17553d",
  "kind": "choice",
  "text": "Here is the home adaptations, posted by Priya for the family to read.\n\nMembers: Zara, Kai, Priya, Mo\nChat log (oldest first):\n[30 Jan 2026] Zara: @Mo Absolutely, I will fetch the mobility aids by 4 February 2026.\n[2 Feb 2026] Mo: @Zara Forget it, you won't need to fetch the mobility aids\n[4 Feb 2026] Mo: @Priya I will book the clinic transport by 9 February 2026 only if the physio session happens.\n[5 Feb 2026] Kai: Did you manage to book the clinic transport?\n[6 Feb 2026] Priya: Team, the physio session is not happening.\n[7 Feb 2026] Mo: @Priya Mate, I promised, may I book the clinic transport by 13 February 2026 instead?\n[8 Feb 2026] Priya: @Mo Go ahead and book the clinic transport by 13 February 2026, that is fine.\n\nAdmin note: I have signed off every change in this chat, so Priya needs no further sign-off.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Mo made to book the clinic transport at the end of 11 February 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Broken",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qbe77310821",
  "kind": "choice",
  "text": "This export holds the messages about the kitchen garden project, which Omar saved.\n\nMembers: Wren, Oskar, Omar\nChat log (oldest first):\n[12 May 2026] Oskar: @Wren Got it, I'll water the allotment beds by 19 May 2026 for sure.\n[13 May 2026] Wren: Will attempt to deliver the surplus runner beans by 19 May 2026, can't promise.\n[14 May 2026] Oskar: @Wren Guess what, I managed to water the allotment beds!\n[15 May 2026] Wren: @Oskar I'll deliver the surplus runner beans by 18 May 2026, providing the plot inspection goes ahead.\n[16 May 2026] Omar: Fab, we are on for the plot inspection as planned!\n[18 May 2026] Omar: @Wren Quick update: you do not need to deliver the surplus runner beans at all.\n[21 May 2026] Wren: @Oskar Log entry: deliver the surplus runner beans, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Wren made to deliver the surplus runner beans at the end of 18 May 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Not yet due",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q7f908ef2c4",
  "kind": "yes/no",
  "text": "{\"subject\": \"the wedding weekend\", \"source\": \"group chat export\", \"shared_by\": \"Rhea\"}\n\nMembers: Sami, Malik, Rhea, Nadia\nChat log (oldest first):\n[14 Jul 2026] Malik: @Rhea Count on me, I'll buy the candle props by 21 July 2026.\n[16 Jul 2026] Sami: @Rhea I'll collect the venue floor plan by 23 July 2026, promise.\n[18 Jul 2026] Malik: @Rhea Might I ask whether I could buy the candle props by 24 July 2026 instead?\n[18 Jul 2026] Rhea: @Malik Nah, that deadline counts, mate, so please buy the candle props!\n[23 Jul 2026] Rhea: @Sami You are released, no requirement to collect the venue floor plan.",
  "question": "Did Sami keep the promise to collect the venue floor plan as of 26 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd29bfe478e",
  "kind": "choice",
  "text": "Thread between a landlord and tenants on the balcony garden project left as it was and shared by Sami.\n\nMembers: Sami, Jonas\nChat log (oldest first):\n[27 Jun 2026] Jonas: @Sami See if I can forward the gas bill by 4 July 2026, no certainty.\n[28 Jun 2026] Jonas: @Sami Provided the boiler annual check happens, I will forward the gas bill by 2 July 2026.\n[30 Jun 2026] Jonas: Team, the boiler annual check stays on as booked.\n[2 Jul 2026] Jonas: @Sami Think 5 July 2026 would work if I forward the gas bill instead?\n[2 Jul 2026] Sami: @Jonas No new date, so please forward the gas bill by the date given.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Jonas's commitment to forward the gas bill is in what status at the end of 5 July 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Broken",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "qad6ccdd1ae",
  "kind": "choice",
  "text": "Subject: Saved thread about the menu redesign\nThis export from Femi is pasted in full for readers who want it.\n\nMembers: Dara, Leila, Kai, Femi\nChat log (oldest first):\n[24 Aug 2026] Kai: @Femi I assure you I'll send the moodboard files by Monday, 31 August 2026 if the brand review call is on.\n[28 Aug 2026] Kai: @Leila I'll mail the business cards by Friday, 4 September 2026, promise.\n[28 Aug 2026] Leila: Thanks mate, noted.\n[29 Aug 2026] Kai: @Leila Can I mail the business cards by Monday, 7 September 2026 instead? I did promise, sorry.\n[30 Aug 2026] Femi: Great news, the brand review call is on!\n[2 Sep 2026] Kai: @Leila Ticked off: mail the business cards, feels so good",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Kai's promise to mail the business cards at the end of Thursday, 3 September 2026?",
  "options": [
   "Broken",
   "Waived",
   "Kept",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q5370885b3c",
  "kind": "choice",
  "text": "Support thread for a help desk case, covering the gallery show, saved by Yuki.\n\nMembers: Tomas, Yuki\nChat log (oldest first):\n[9 Apr 2026] Yuki: @Tomas Lovely, I'll update the icon set by 16 Apr 2026 for sure.\n[13 Apr 2026] Yuki: @Tomas Mind giving me until 19 Apr 2026 to update the icon set?\n[13 Apr 2026] Tomas: @Yuki Of course, it is fine for you to update the icon set by 19 Apr 2026.\n[20 Apr 2026] Yuki: @Tomas Log entry: update the icon set, carried out",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Yuki made to update the icon set, what state is it in at the end of 20 Apr 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Waived",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q2d233ab9d0",
  "kind": "yes/no",
  "text": "Here's the flatmate chat that Mo saved, about the kitchen refit.\n\nMembers: Tomas, Mo\nChat log (oldest first):\n[12 May 2026] Tomas: @Mo Provided the window cleaner visit happens, I'll measure the kitchen for fridge by 17 May 2026.\n[13 May 2026] Mo: Fab, we are on for the window cleaner visit as planned!\n[14 May 2026] Mo: @Tomas Count on me, I'll forward the gas bill by 20 May 2026.\n[16 May 2026] Tomas: @Mo Is 22 May 2026 alright for me to measure the kitchen for fridge?\n[16 May 2026] Mo: @Tomas You are released, no requirement to measure the kitchen for fridge.",
  "question": "Under the rules on the card, is it true that Tomas has not kept the promise to measure the kitchen for fridge as of 18 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q841b87427c",
  "kind": "yes/no",
  "text": "An exported family chat on the family photo book, saved by Kai, left unchanged.\n\nMembers: Kai, Hana, Nadia, Malik\nChat log (oldest first):\n[8 Jul 2026] Nadia: @Kai I own this, I'll fetch the craft box by 14 July 2026.\n[11 Jul 2026] Nadia: @Kai Would it be fine if I fetch the craft box by 17 July 2026 instead, yeah?\n[12 Jul 2026] Kai: @Nadia Works for me, fine for you to fetch the craft box by 17 July 2026.\n[17 Jul 2026] Kai: @Nadia No worries, you don't need to fetch the craft box",
  "question": "Would you say Nadia didn't keep the promise to fetch the craft box by the end of 18 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd5e7360ebe",
  "kind": "yes/no",
  "text": "Casual chat for the flat, saved by Leila, and it covers the rent split plan.\n\nMembers: Omar, Bruno, Nadia, Leila\nChat log (oldest first):\n[21 Feb 2026] Nadia: @Leila Absolutely, I will store the spare bike by 28 Feb 2026.\n[24 Feb 2026] Nadia: @Leila Think 3 Mar 2026 would work if I store the spare bike instead?\n[24 Feb 2026] Leila: @Nadia Not moving it, store the spare bike by the existing date.\n[25 Feb 2026] Leila: @Nadia I will copy the house keys by 3 Mar 2026.\n[2 Mar 2026] Bruno: @Leila No worries, you don't need to copy the house keys\n[3 Mar 2026] Leila: @Nadia For the record: I was able to copy the house keys",
  "question": "Is the promise Leila made to copy the house keys not kept by 9 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qee9d186ea2",
  "kind": "yes/no",
  "text": "Help desk export\nAbout: the annual tour\nCopied by: Wren\n\nMembers: Omar, Leila, Mo, Wren\nChat log (oldest first):\n[28 May 2026] Wren: @Leila Provided the club sportive happens, I'll set up the feed stop by 1 June 2026.\n[30 May 2026] Omar: Where are you up to with plans to set up the feed stop?\n[31 May 2026] Omar: Great news, the club sportive is on!\n[1 Jun 2026] Wren: @Leila Ticked off my list: set up the feed stop, yay.\n[1 Jun 2026] Mo: @Wren Lovely, I'll pump the spare tyres by 3 June 2026 for sure.\n[2 Jun 2026] Mo: @Wren Is it all right if I pump the spare tyres by 6 June 2026 instead?\n[3 Jun 2026] Wren: @Mo Yes, you can pump the spare tyres by 6 June 2026 instead.",
  "question": "On the card, was Wren's promise to set up the feed stop broken, waived, not triggered or not yet due, rather than kept, at the end of 7 June 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qba5f9b18dd",
  "kind": "choice",
  "text": "Copy of a household chat shared by Priya, where neighbours discuss the holiday memories.\n\nMembers: Lee, Priya, Jonas, Tess\nChat log (oldest first):\n[10 Mar 2026] Tess: @Jonas I own this, I'll mend the kite string by 14 March 2026.\n[10 Mar 2026] Tess: @Jonas Mate, I promised, may I mend the kite string by 19 March 2026 instead?\n[10 Mar 2026] Lee: @Tess Yes, all good for you to mend the kite string by 19 March 2026 instead.\n[10 Mar 2026] Lee: @Tess Quick update: you do not need to mend the kite string at all.\n[15 Mar 2026] Tess: @Jonas Quick report: I've managed to mend the kite string",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Tess's promise to mend the kite string at the end of 14 March 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Kept",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q2df18639fb",
  "kind": "choice",
  "text": "Subject: chat about the reunion weekend, forwarded\nThe chat follows below.\nRegards, Lena\n\nMembers: Bruno, Lena, Yuki, Elif\nChat log (oldest first):\n[16 Apr 2026] Elif: @Yuki Not promising, but I'll try to collect the old photo prints by April 26, 2026.\n[18 Apr 2026] Elif: @Yuki I'll collect the old photo prints by April 25, 2026 as long as the cousin brunch is on.\n[20 Apr 2026] Lena: Yep, the cousin brunch is on as planned.\n[20 Apr 2026] Lena: @Elif Ah, no stress, no need for you to collect the old photo prints\n[25 Apr 2026] Elif: @Yuki To my relief, I managed to collect the old photo prints.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of April 22, 2026, which status does Elif have for the promise to collect the old photo prints?",
  "options": [
   "Broken",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q1fb97d65fa",
  "kind": "choice",
  "text": "Client thread, the guest list. Freelancer export by Lee.\n\nMembers: Lee, Wren, Ana\nChat log (oldest first):\n[25 Jun 2026] Lee: @Ana Absolutely, I will book the assistant photographer by 4 Jul 2026.\n[27 Jun 2026] Wren: @Ana I'll be sure to charge the flash batteries by 30 Jun 2026.\n[27 Jun 2026] Ana: Ta, I saw this.\n[30 Jun 2026] Wren: @Ana Is it all right if I charge the flash batteries by 5 Jul 2026 instead?\n[30 Jun 2026] Wren: @Ana To note: I have managed to charge the flash batteries\n[3 Jul 2026] Ana: Any news on whether you can charge the flash batteries, lovely?",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules, when is the date by which Wren has to charge the flash batteries at the end of 8 Jul 2026, allowing for any agreed change?",
  "options": [
   "30 Jun 2026",
   "5 Jul 2026",
   "4 Jul 2026"
  ]
 },
 {
  "qid": "q503ed9bd9d",
  "kind": "choice",
  "text": "Note: help desk thread about the documentary cut\nSaved by: Femi\n\nMembers: Dara, Arlo, Femi, Nadia\nChat log (oldest first):\n[9 Jul 2026] Arlo: @Femi I will make sure to send the colour notes by 16 July 2026.\n[12 Jul 2026] Nadia: @Femi Count on me to label the clip folders by 17 July 2026.\n[12 Jul 2026] Femi: Thanks mate, noted.\n[17 Jul 2026] Nadia: @Femi Can I label the clip folders by 19 July 2026 instead? I did promise, sorry.\n[17 Jul 2026] Dara: @Nadia Works for me, fine for you to label the clip folders by 19 July 2026.\n[18 Jul 2026] Nadia: @Femi Guess who managed to label the clip folders, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules, when is the date by which Nadia has to label the clip folders at the end of 1 August 2026, allowing for any agreed change?",
  "options": [
   "19 July 2026",
   "17 July 2026",
   "16 July 2026"
  ]
 },
 {
  "qid": "qbdfc064827",
  "kind": "yes/no",
  "text": "{\"record\": \"shared group chat\", \"subject\": \"the spring campaign\", \"shared_by\": \"Bruno\", \"stored\": \"as text\"}\n\nMembers: Hana, Bruno, Kai, Omar\nChat export (date | from | to | message):\n2026-11-01 | Omar | Hana | Relax, I'll fix the landing page headline by 5 Nov 2026 for sure.\n2026-11-02 | Omar | Hana | Mum, I did fix the landing page headline, haha.\n2026-11-03 | Omar | Bruno | I'll return the rented camera gear by 8 Nov 2026, promise.\n2026-11-08 | Omar | Bruno | Gutted to say I won't return the rented camera gear, sorry team",
  "question": "Per the card's rules, on 2 Nov 2026, has Omar's promise to fix the landing page headline been kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7d26ad3879",
  "kind": "yes/no",
  "text": "Team channel: the onboarding flow\nExported by Yuki.\n\nMembers: Kofi, Yuki\nChat log (oldest first):\n[14 Aug 2026] Kofi: @Yuki I promise to deploy the staging build by August 20, 2026 if the server migration is on.\n[14 Aug 2026] Yuki: Ah right, thanks for that.\n[15 Aug 2026] Kofi: @Yuki It's on me to restart the build server by August 23, 2026.\n[19 Aug 2026] Kofi: Great news, the server migration is on!\n[20 Aug 2026] Kofi: @Yuki Quick report: I've managed to deploy the staging build",
  "question": "Was Kofi's promise to deploy the staging build not kept as of August 21, 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q78993d26d8",
  "kind": "yes/no",
  "text": "Landlord and renters' group talk on the bathroom refit, from Kai's export.\n\nMembers: Mo, Kofi, Kai\nChat export (date | from | to | message):\n2026-05-18 | Mo | Kofi | Got it, I'll sweep the dust from stairs by 26 May 2026 for sure.\n2026-05-23 | Kofi | Kai | Lovely, I'll collect the sanding pads by 28 May 2026 for sure.\n2026-05-24 | Kofi | Kai | Is 31 May 2026 alright for me to collect the sanding pads?\n2026-05-26 | Mo | Kofi | Guess what, I managed to sweep the dust from stairs!\n2026-05-27 | Kai | Kofi | Yes, happy for you to collect the sanding pads by 31 May 2026 instead.",
  "question": "Is the promise to sweep the dust from stairs kept by Mo as of 31 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0a7dbcd96d",
  "kind": "yes/no",
  "text": "Forwarded by Ivo, these tenant replies are about the spare room plan for the file.\n\nMembers: Zara, Lee, Sami, Ivo\nChat log (oldest first):\n[9 Mar 2026] Ivo: @Sami I'll try to stock the spice rack by 17 March 2026.\n[11 Mar 2026] Ivo: @Lee I'll stock the spice rack by 18 March 2026, promise.\n[11 Mar 2026] Ivo: @Lee Can I stock the spice rack by 21 March 2026 instead? I did promise, sorry.\n[12 Mar 2026] Sami: Where are you up to with plans to stock the spice rack?\n[16 Mar 2026] Zara: @Ivo Yes, you can stock the spice rack by 21 March 2026 if that suits you.\n[17 Mar 2026] Ivo: @Lee Change of plans: I will not stock the spice rack",
  "question": "Is it right to say that Ivo has broken the promise to stock the spice rack at the end of 20 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd43adba6af",
  "kind": "yes/no",
  "text": "Freelancer and client exchange about the shop rebuild, saved by Elif.\n\nMembers: Tess, Hana, Elif, Nadia\nChat log (oldest first):\n[10 Jun 2026] Tess: @Nadia I'll print the packing slips by 18 June 2026 as long as the pop up stall is on.\n[12 Jun 2026] Tess: @Nadia Count on me to add the size chart by 16 June 2026.\n[12 Jun 2026] Tess: @Nadia Would it be fine if I add the size chart by 18 June 2026 instead, yeah?\n[13 Jun 2026] Elif: Hey, any luck with trying to print the packing slips?\n[14 Jun 2026] Nadia: @Tess Yes, you're welcome to add the size chart by 18 June 2026 instead.\n[14 Jun 2026] Elif: We are dropping the pop up stall from the list.",
  "question": "Applying the rules on the card, has Tess kept the promise to print the packing slips as of 18 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q21a2c40a7a",
  "kind": "yes/no",
  "text": "A written chat between housemates about the reunion weekend. Exported from the device by Kai.\n\nMembers: Kai, Nadia\nChat log (oldest first):\n[18 Jan 2026] Nadia: @Kai Got it, I'll label the memory box by 21 January 2026 for sure.\n[21 Jan 2026] Nadia: @Kai Got it, I'll buy the name tags by 24 January 2026 for sure.\n[22 Jan 2026] Kai: @Nadia I will order the cousin t-shirts by 25 January 2026 only if the cousin brunch happens.\n[22 Jan 2026] Kai: Brilliant news everyone, the cousin brunch is a go!\n[31 Jan 2026] Kai: @Nadia Guess who managed to order the cousin t-shirts, go team!",
  "question": "Would you say Kai didn't keep the promise to order the cousin t-shirts by the end of 29 January 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q52b4b29eac",
  "kind": "yes/no",
  "text": "Note above exported messages from a tenant to the letting agent, covering the guest review drive, saved by Elif.\n\nMembers: Jonas, Leila, Kai, Elif\nChat log (oldest first):\n[15 Jun 2026] Elif: I'll try to air the spare room by June 22, 2026, no promises.\n[18 Jun 2026] Elif: @Jonas Count on me to fill the cleaning cupboard by June 26, 2026.\n[18 Jun 2026] Jonas: @Kai Committing to wheel the bins out by June 24, 2026.\n[18 Jun 2026] Kai: @Jonas Nobody needs you to wheel the bins out, that's that\n[26 Jun 2026] Elif: @Jonas Think July 1, 2026 would work if I fill the cleaning cupboard instead?\n[26 Jun 2026] Jonas: @Elif Yes, you can fill the cleaning cupboard by July 1, 2026 instead.\n[29 Jun 2026] Elif: @Jonas Ta-da, I went and did it: fill the cleaning cupboard!",
  "question": "Is Elif's promise to fill the cleaning cupboard kept on July 3, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q62e68e5c23",
  "kind": "yes/no",
  "text": "Thread between a landlord and tenants on the guest welcome plan left as it was and shared by Dara.\n\nMembers: Jonas, Wren, Dara, Nadia\nChat log (oldest first):\n[4 Mar 2026] Jonas: Not promising, but I'll try to collect the bed linen by 18 March 2026.\n[6 Mar 2026] Jonas: @Dara Provided the pool safety inspection happens, I'll collect the bed linen by 14 March 2026.\n[6 Mar 2026] Dara: Got it, thanks a lot.\n[6 Mar 2026] Jonas: Fab, we are on for the pool safety inspection as planned!\n[15 Mar 2026] Nadia: Quick check, any update on plans to collect the bed linen?\n[20 Mar 2026] Jonas: @Dara Mum, I did collect the bed linen, haha.",
  "question": "Would you say Jonas didn't keep the promise to collect the bed linen by the end of 18 March 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa7ac787653",
  "kind": "choice",
  "text": "Ivo forwarded this for the committee as we dig in on the ground upgrade.\n\nMembers: Ivo, Malik\nChat log (oldest first):\n[27 Apr 2026] Malik: @Ivo Provided the training camp happens, I'll repair the goal nets by 4 May 2026.\n[27 Apr 2026] Ivo: @Malik Lovely, I'll mark the pitch lines by 5 May 2026 for sure.\n[30 Apr 2026] Malik: Really pleased to say the training camp will go ahead!\n[2 May 2026] Malik: @Ivo Would it be fine if I repair the goal nets by 10 May 2026 instead, yeah?\n[4 May 2026] Ivo: @Malik Yes, you can repair the goal nets by 10 May 2026 instead.\n[7 May 2026] Malik: @Ivo Ticked off my list: repair the goal nets, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nFollowing the rules set out on the card, what date governs Malik's commitment to repair the goal nets at the end of 8 May 2026, once any agreed shift in the date is factored in?",
  "options": [
   "10 May 2026",
   "4 May 2026",
   "5 May 2026"
  ]
 },
 {
  "qid": "q6ad73156c9",
  "kind": "choice",
  "text": "Subject: the school fundraiser\nBelow is the group chat that Ivo saved, unedited.\n\nMembers: Wren, Rhea, Ivo, Greta\nChat export (date | from | to | message):\n2026-07-07 | Wren | Greta | Wish me luck, hoping to label the raffle prizes by 16 Jul 2026.\n2026-07-09 | Wren | Greta | Count on me to label the raffle prizes by 14 Jul 2026 if the quiz night is on.\n2026-07-09 | Greta | group | Got it, thanks a lot.\n2026-07-10 | Ivo | group | Please note the quiz night will proceed.\n2026-07-15 | Wren | Greta | Mum, I did label the raffle prizes, haha.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Wren's commitment to label the raffle prizes is in what status at the end of 18 Jul 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not triggered",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q008dd9a2fd",
  "kind": "choice",
  "text": "Channel: work team chat\nTopic: the office refit\nExported by Ines.\n\nMembers: Ines, Sami, Rhea\nChat log (oldest first):\n[17 Oct 2026] Sami: @Ines I'm aiming to return the printer toner by Wednesday, October 28, 2026, might manage it.\n[19 Oct 2026] Sami: @Rhea I'll be sure to return the printer toner by Sunday, October 25, 2026.\n[20 Oct 2026] Sami: @Rhea I committed to return the printer toner, can I do that by Saturday, October 31, 2026 instead?\n[22 Oct 2026] Rhea: @Sami Yes, you're welcome to return the printer toner by Saturday, October 31, 2026 instead.\n[31 Oct 2026] Sami: @Rhea Ta-da, I went and did it: return the printer toner!",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Sami's promise to return the printer toner at the end of Tuesday, November 3, 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Not yet due",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q3c9c26fc11",
  "kind": "choice",
  "text": "Team chat header\nSubject line: the visitor policy, exported by Priya.\n\nMembers: Jonas, Mo, Priya, Wren\nChat log (oldest first):\n[15 Sep 2026] Mo: @Wren Count on me to fetch the parking permits by 19 Sep 2026 if the annual audit is on.\n[17 Sep 2026] Wren: @Priya Relax, I'll return the printer toner by 24 Sep 2026, promise.\n[17 Sep 2026] Wren: @Priya Is 27 Sep 2026 alright for me to return the printer toner?\n[17 Sep 2026] Priya: Team, the annual audit is not happening.\n[19 Sep 2026] Priya: @Wren Yes, you're welcome to return the printer toner by 27 Sep 2026 instead.\n[28 Sep 2026] Wren: @Priya Ticked off my list: return the printer toner, yay.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nFollowing the rules set out on the card, what date governs Wren's commitment to return the printer toner at the end of 28 Sep 2026, once any agreed shift in the date is factored in?",
  "options": [
   "19 Sep 2026",
   "27 Sep 2026",
   "24 Sep 2026"
  ]
 },
 {
  "qid": "q070bc029da",
  "kind": "yes/no",
  "text": "Support: help desk chat\nSubject: the payment setup\nSaved by: Zara\n\nMembers: Hana, Zara, Wren, Oskar\nChat log (oldest first):\n[5 Mar 2026] Oskar: @Wren Wish me luck, hoping to restore the old theme by Saturday, 7 March 2026.\n[6 Mar 2026] Oskar: @Hana See if I can renew the hosting plan by Wednesday, 11 March 2026.\n[7 Mar 2026] Oskar: @Zara Relax, I'll renew the hosting plan by Friday, 13 March 2026, promise.\n[7 Mar 2026] Zara: Oh cheers, that helps.\n[8 Mar 2026] Oskar: @Zara Log entry: renew the hosting plan, carried out",
  "question": "Has Oskar kept the promise to renew the hosting plan at the end of Friday, 13 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8bede72357",
  "kind": "choice",
  "text": "Written exchange with the letting agent, covering the attic conversion idea, which Priya copied into the file.\n\nMembers: Bruno, Wren, Hana, Priya\nChat export (date | from | to | message):\n2026-05-08 | Hana | Bruno | Lovely, I'll stock the spice rack by 2026-05-12 for sure.\n2026-05-08 | Hana | Bruno | Quick report: I've managed to stock the spice rack\n2026-05-12 | Wren | Hana | I'll cut a spare door key by 2026-05-15, promise.\n2026-05-12 | Hana | group | Thanks for the heads up.\n2026-05-15 | Priya | Wren | No worries, you don't need to cut a spare door key\n2026-05-16 | Wren | Hana | Ticked off: cut a spare door key, feels so good",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Wren's promise to cut a spare door key at the end of 2026-05-15?",
  "options": [
   "Waived",
   "Not triggered",
   "Not yet due",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "q0b6f796df8",
  "kind": "yes/no",
  "text": "Work chat channel about the trade show push, exported and saved by Arlo.\n\nMembers: Malik, Leila, Arlo, Oskar\nChat export (date | from | to | message):\n2026-10-09 | Arlo | Malik | Committing to draft the press release by Sunday, October 18, 2026.\n2026-10-10 | Oskar | group | Hoping to set up the analytics dashboard by Monday, October 12, 2026, can't promise.\n2026-10-10 | Arlo | Malik | Any chance I can draft the press release by Thursday, October 22, 2026 instead?\n2026-10-10 | Arlo | Leila | Relax, I'll print the event banners by Friday, October 16, 2026 for sure.\n2026-10-10 | Oskar | Arlo | Quick update: you do not need to print the event banners at all.\n2026-10-17 | Malik | Arlo | Aw no, you need to draft the press release by the original date!",
  "question": "Is it right to say that Arlo has broken the promise to print the event banners at the end of Saturday, October 10, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q03f648b195",
  "kind": "choice",
  "text": "Subject: the school fundraiser\nBelow is the group chat that Ivo saved, unedited.\n\nMembers: Wren, Rhea, Ivo, Greta\nChat export (date | from | to | message):\n2026-07-07 | Wren | Greta | Wish me luck, hoping to label the raffle prizes by 16 Jul 2026.\n2026-07-09 | Wren | Greta | Count on me to label the raffle prizes by 14 Jul 2026 if the quiz night is on.\n2026-07-09 | Greta | group | Got it, thanks a lot.\n2026-07-10 | Ivo | group | Please note the quiz night will proceed.\n2026-07-14 | Wren | Greta | Mum, I did label the raffle prizes, haha.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Wren's commitment to label the raffle prizes is in what status at the end of 18 Jul 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not triggered",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q7087d5d5a0",
  "kind": "choice",
  "text": "Team thread shared by Tess, covering the grant renewal in the channel.\n\nMembers: Tess, Ana, Femi, Ravi\nChat log (oldest first):\n[12 Apr 2026] Ravi: @Ana I promise to send the ethics form by April 18, 2026 if the conference trip is on.\n[16 Apr 2026] Ana: Hoping to return the library books by April 25, 2026, no promises.\n[17 Apr 2026] Ravi: Sadly, the conference trip won't go ahead.\n[17 Apr 2026] Ana: @Femi Relax, I'll return the library books by April 23, 2026, promise.\n[18 Apr 2026] Femi: @Ana No need to return the library books, I'm letting you off\n[21 Apr 2026] Ravi: Just checking in, did you manage to return the library books?",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Ana's promise to return the library books at the end of April 27, 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not yet due",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "qab56a55931",
  "kind": "choice",
  "text": "Chat about the spare room plan, from the support queue, gathered by Ravi.\n\nMembers: Ravi, Mo, Femi, Wren\nChat export (date | from | to | message):\n2026-07-19 | Ravi | Femi | Got it, I'll turn the heating timer by 24 July 2026 for sure.\n2026-07-19 | Femi | group | Cheers, noted.\n2026-07-21 | Mo | Ravi | See if I can wipe the shared kitchen counter by 25 July 2026.\n2026-07-23 | Ravi | Femi | To note: I have managed to turn the heating timer",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Ravi gave to turn the heating timer have at the end of 25 July 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Kept",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q8cff5b533f",
  "kind": "yes/no",
  "text": "Group thread for the work team about the staff handbook, passed on by Omar.\n\nMembers: Dara, Malik, Omar\nChat log (oldest first):\n[26 Mar 2026] Omar: @Malik I'll renew the fire extinguisher service by 1 April 2026, promise.\n[31 Mar 2026] Dara: @Omar I'll return the printer toner by 8 April 2026, promise.\n[31 Mar 2026] Omar: Thanks mate, noted.\n[1 Apr 2026] Dara: @Omar Scratch that, I'm not going to return the printer toner\n[7 Apr 2026] Omar: @Dara Nobody needs you to return the printer toner, that's that",
  "question": "At the end of 10 April 2026, does the promise Dara made to return the printer toner have any status except broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qee7dce7aaa",
  "kind": "yes/no",
  "text": "Team thread shared by Lena, covering the spring campaign in the channel.\n\nMembers: Zara, Lena, Kai\nChat export (date | from | to | message):\n2026-06-05 | Lena | Kai | As long as the influencer call is on, I will fix the landing page headline by 8 Jun 2026.\n2026-06-07 | Kai | group | Afraid the influencer call is called off.\n2026-06-07 | Lena | Kai | Quick question, could I fix the landing page headline by 10 Jun 2026 instead?\n2026-06-07 | Zara | Lena | That suits me, so please fix the landing page headline by 10 Jun 2026 instead.\n2026-06-07 | Lena | Zara | I promise to pay the printing invoice by 12 Jun 2026.\n2026-06-13 | Lena | Zara | To my relief, I managed to pay the printing invoice.",
  "question": "Is the promise Lena made to fix the landing page headline in a status other than broken at the end of 7 Jun 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qac8b8fe3e0",
  "kind": "yes/no",
  "text": "Volunteers, Ivo shared this with you about the annual tour.\n\nMembers: Ines, Ivo, Elif, Nadia\nChat log (oldest first):\n[27 Sep 2026] Ivo: @Nadia If the hill climb goes ahead, I'll gladly return the loaned helmets by 3 October 2026.\n[29 Sep 2026] Elif: Fab, we are on for the hill climb as planned!\n[30 Sep 2026] Nadia: @Ivo I'll try to print the route cards by 5 October 2026, can't promise!\n[1 Oct 2026] Nadia: @Ines I own this, I'll print the route cards by 4 October 2026.\n[3 Oct 2026] Ivo: @Nadia Good news, you're let off having to print the route cards",
  "question": "Checking the chat at the end of 5 October 2026, has Nadia broken the promise to print the route cards?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q76a246e19b",
  "kind": "yes/no",
  "text": "{\"source\": \"saved thread\", \"about\": \"the quiet street fund\", \"owner\": \"Yuki\", \"kind\": \"chat export\"}\n\nMembers: Mo, Wren, Yuki\nChat log (oldest first):\n[20 Jun 2026] Yuki: @Wren Got it, I'll walk the old spaniel by June 26, 2026 for sure.\n[22 Jun 2026] Mo: @Yuki Relax, mate, you're not expected to walk the old spaniel\n[23 Jun 2026] Mo: @Wren Absolutely, I will lock the side gate by June 28, 2026.\n[25 Jun 2026] Yuki: @Wren Guess what, I managed to walk the old spaniel!\n[25 Jun 2026] Mo: @Wren Change of plans: I will not lock the side gate",
  "question": "Does the card's rule set show that Yuki has not kept the promise to walk the old spaniel at the end of June 25, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5de089fb86",
  "kind": "yes/no",
  "text": "Channel title: work team chat\nDescription: about the peer review, exported by Jonas.\n\nMembers: Jonas, Elif, Yuki\nChat log (oldest first):\n[28 Jun 2026] Jonas: @Yuki Absolutely, I will order the reagent kit by Wednesday, July 1, 2026.\n[29 Jun 2026] Yuki: @Jonas I'll clean the glassware set by Thursday, July 2, 2026, promise.\n[29 Jun 2026] Jonas: Thanks lovely, got it!\n[29 Jun 2026] Jonas: @Yuki Can I order the reagent kit by Monday, July 6, 2026 instead? I did promise, sorry.\n[30 Jun 2026] Elif: I'll try to send the ethics form by Saturday, July 4, 2026.\n[1 Jul 2026] Yuki: @Jonas Nah, that deadline counts, mate, so please order the reagent kit!\n[2 Jul 2026] Jonas: @Yuki Nobody needs you to clean the glassware set, that's that",
  "question": "At the end of Sunday, July 5, 2026, is Yuki's promise to clean the glassware set broken, waived, not triggered or not yet due, rather than kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q76e5aea800",
  "kind": "yes/no",
  "text": "Help desk export\nAbout: the caring rota\nCopied by: Femi\n\nMembers: Hana, Ana, Femi, Ines\nChat log (oldest first):\n[13 Jun 2026] Ana: @Hana Relax, I'll return the hospital bed by 18 June 2026 for sure.\n[14 Jun 2026] Ines: Hoping to pick up the repeat prescription by 17 June 2026, but can't promise.\n[15 Jun 2026] Femi: @Ana Relax, mate, you're not expected to return the hospital bed\n[15 Jun 2026] Hana: @Femi Only if the hospital appointment is on, I will call the home nurse by 22 June 2026.\n[16 Jun 2026] Ines: @Hana Provided the home assessment happens, I will pick up the repeat prescription by 19 June 2026.\n[18 Jun 2026] Ana: Sad to report that the home assessment is off.\n[19 Jun 2026] Hana: Update: the hospital appointment is going ahead as planned.\n\nExport tool: this copy, shared by Femi, may be out of date, so later edits might not appear here.",
  "question": "Would Ines be counted as having broken the promise to pick up the repeat prescription at the end of 18 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q26bde4b444",
  "kind": "choice",
  "text": "Freelance chat about the sound mix\nThe client side, saved by Kai.\n\nMembers: Tomas, Oskar, Kai\nChat export (date | from | to | message):\n2026-07-16 | Kai | group | Fingers crossed I can ship the hard drive by Sunday, July 19, 2026.\n2026-07-18 | Kai | Oskar | I will ship the hard drive by Saturday, July 25, 2026.\n2026-07-20 | Oskar | Kai | Count on me, I'll order the stock music licence by Friday, July 24, 2026.\n2026-07-22 | Oskar | Kai | Is it all right if I order the stock music licence by Monday, July 27, 2026 instead?\n2026-07-22 | Kai | Oskar | No new date, so please order the stock music licence by the date given.\n2026-07-26 | Kai | Oskar | Guess what, I managed to ship the hard drive!",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Kai's promise to ship the hard drive sit at the end of Tuesday, July 28, 2026, exactly?",
  "options": [
   "Not yet due",
   "Waived",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q78f518c3a8",
  "kind": "yes/no",
  "text": "Shared by Hana for the committee, this is the group chat on the new kit design.\n\nMembers: Lee, Ines, Hana\nChat log (oldest first):\n[26 Oct 2026] Ines: @Hana I will make sure to tune the gear cables by 2026-11-02.\n[26 Oct 2026] Ines: @Hana Is 2026-11-04 alright for me to tune the gear cables?\n[31 Oct 2026] Lee: @Hana It's on me to wash the club jerseys by 2026-11-08.\n[1 Nov 2026] Hana: @Ines Not moving it, tune the gear cables by the existing date.\n[1 Nov 2026] Ines: @Hana I have to take back my promise to tune the gear cables.\n[8 Nov 2026] Lee: @Hana Can I wash the club jerseys by 2026-11-10 instead? I did promise, sorry.\n[8 Nov 2026] Hana: @Lee Of course, it is fine for you to wash the club jerseys by 2026-11-10.",
  "question": "Under the rules on the card, is the promise Ines made to tune the gear cables not broken at the end of 2026-11-05?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3801a7dde7",
  "kind": "choice",
  "text": "Thread filed under support\nAbout the documentary cut, saved by Ana.\n\nMembers: Omar, Tomas, Zara, Ana\nChat export (date | from | to | message):\n2026-04-17 | Ana | Zara | I'll send the timeline export by 19 Apr 2026, promise.\n2026-04-19 | Omar | Ana | I own this, I'll export the subtitle files by 25 Apr 2026.\n2026-04-21 | Ana | Zara | To note: I have managed to send the timeline export\n2026-04-22 | Tomas | Omar | I will record the voice over by 26 Apr 2026.\n2026-04-24 | Omar | Ana | Any chance I can export the subtitle files by 29 Apr 2026 instead?\n2026-04-25 | Zara | Omar | Relax, mate, you're not expected to export the subtitle files\n2026-04-26 | Ana | Tomas | Quick update: you do not need to record the voice over at all.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Omar made to export the subtitle files is in which status at the end of 24 Apr 2026?",
  "options": [
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "qa2260abc2b",
  "kind": "choice",
  "text": "Thread between a landlord and tenants on the balcony garden project left as it was and shared by Sami.\n\nMembers: Sami, Jonas\nChat log (oldest first):\n[27 Jun 2026] Jonas: @Sami See if I can forward the gas bill by 4 July 2026, no certainty.\n[28 Jun 2026] Jonas: @Sami Provided the boiler annual check happens, I will forward the gas bill by 2 July 2026.\n[30 Jun 2026] Jonas: Sorry all, the boiler annual check is not happening.\n[2 Jul 2026] Jonas: @Sami Think 5 July 2026 would work if I forward the gas bill instead?\n[2 Jul 2026] Sami: @Jonas No new date, so please forward the gas bill by the date given.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Jonas's commitment to forward the gas bill is in what status at the end of 5 July 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Broken",
   "Kept",
   "Waived"
  ]
 }
]
