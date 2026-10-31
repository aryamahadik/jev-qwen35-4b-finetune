# G5-H blind read T32-blind_read-aa45a0db-000 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T32/pilot_i2/g5h/answers/T32-blind_read-aa45a0db-000.json

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
  "qid": "qa6c5a654ff",
  "kind": "choice",
  "text": "Help desk export\nAbout: the spring campaign\nCopied by: Leila\n\nMembers: Kai, Malik, Yuki, Leila\nChat export (date | from | to | message):\n2026-02-25 | Kai | Yuki | I will pay the printing invoice by 4 Mar 2026.\n2026-02-28 | Kai | Malik | Provided the influencer call happens, I'll fix the landing page headline by 6 Mar 2026.\n2026-03-01 | Kai | group | Team, the influencer call stays on as booked.\n2026-03-05 | Kai | Malik | Quick question, could I fix the landing page headline by 8 Mar 2026 instead?\n2026-03-05 | Malik | Kai | No new date, so please fix the landing page headline by the date given.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Kai doing with the promise to fix the landing page headline at the end of 6 Mar 2026?",
  "options": [
   "Broken",
   "Waived",
   "Kept",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q2188405f31",
  "kind": "yes/no",
  "text": "Volunteer chat export. Saved by Greta, it covers the junior section.\n\nMembers: Kofi, Greta\nChat log (oldest first):\n[18 Oct 2026] Greta: @Kofi I own this, I'll print the team sheets by 25 October 2026.\n[19 Oct 2026] Kofi: @Greta Lovely, I'll repair the goal nets by 22 October 2026 if the cup tie is on.\n[20 Oct 2026] Greta: @Kofi Count on me, I'll return the bib sets by 27 October 2026.\n[21 Oct 2026] Kofi: @Greta As long as the youth trial is on, I'll mark the pitch lines by 28 October 2026.\n[27 Oct 2026] Greta: @Kofi Ticked off: return the bib sets, feels so good",
  "question": "By the end of 27 October 2026, has Greta kept the promise to return the bib sets?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd1c9f1ab1e",
  "kind": "yes/no",
  "text": "Freelancer to client messages, the rebrand package, passed on by Lee.\n\nMembers: Lee, Greta\nChat log (oldest first):\n[9 Jul 2026] Greta: @Lee Lovely, I'll sketch the packaging mockup by July 15, 2026 for sure.\n[12 Jul 2026] Lee: @Greta You can bet I'll update the icon set by July 19, 2026.\n[13 Jul 2026] Greta: @Lee Got myself to sketch the packaging mockup lol.\n[14 Jul 2026] Greta: @Lee If the packaging launch goes ahead, I'll gladly check the poster proofs by July 22, 2026.\n[15 Jul 2026] Lee: Sadly, the packaging launch won't go ahead.\n[16 Jul 2026] Lee: @Greta Guess what, I managed to update the icon set!",
  "question": "Does the card classify Greta's promise to check the poster proofs as broken, waived, not triggered or not yet due, rather than kept, on July 21, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q769a8922c4",
  "kind": "yes/no",
  "text": "Household group messages for the reunion weekend were passed along by Yuki.\n\nMembers: Yuki, Kofi, Elif, Ines\nChat log (oldest first):\n[12 May 2026] Kofi: @Elif You can bet I'll buy the name tags by 19 May 2026.\n[13 May 2026] Kofi: @Ines If the grandparents visit goes ahead, I'll send the group invitations by 15 May 2026.\n[13 May 2026] Yuki: Afraid the grandparents visit is called off.\n[14 May 2026] Kofi: @Elif Gutted to say I won't buy the name tags, sorry team\n[14 May 2026] Yuki: @Elif Relax, I'll pay the catering company by 18 May 2026 for sure.\n[19 May 2026] Yuki: @Elif Mum, I did pay the catering company, haha.",
  "question": "Did Yuki keep the promise to pay the catering company as of 19 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4c7410ece2",
  "kind": "yes/no",
  "text": "Attached chat: the junior section\nShared by: Tomas.\n\nMembers: Greta, Yuki, Tomas, Kai\nChat log (oldest first):\n[7 Aug 2026] Tomas: @Kai I promise to wash the away kit by 9 August 2026.\n[9 Aug 2026] Tomas: @Kai Got myself to wash the away kit lol.\n[11 Aug 2026] Greta: @Kai If the home derby goes ahead, I'll mark the pitch lines by 18 August 2026.\n[11 Aug 2026] Yuki: @Tomas Got it, I'll print the team sheets by 16 August 2026 for sure.\n[12 Aug 2026] Kai: @Tomas Lovely, I'll fetch the medical bag by 21 August 2026 if the youth trial is on.\n[12 Aug 2026] Yuki: @Tomas Got myself to print the team sheets lol.",
  "question": "By the close of 13 August 2026, is the promise Yuki made to print the team sheets kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9549fb1b3b",
  "kind": "yes/no",
  "text": "Our house group, sorted by Ravi, with the bathroom refit up front.\n\nMembers: Elif, Ravi, Priya, Yuki\nChat export (date | from | to | message):\n2026-01-12 | Ravi | Priya | It's on me to return the tile cutter by 15 January 2026.\n2026-01-14 | Priya | Elif | Guaranteed I'll fetch the paint samples by 20 January 2026.\n2026-01-14 | Ravi | Priya | Update on my side: I will not return the tile cutter, sorry.\n2026-01-15 | Ravi | Priya | Good news, you're let off having to fetch the paint samples\n2026-01-16 | Yuki | Ravi | Promise to print the floor plan by 18 January 2026 if the removal van arrival goes ahead.\n2026-01-17 | Priya | group | Update: the removal van arrival is going ahead as planned.",
  "question": "Applying the card's rules, does Priya's promise to fetch the paint samples count as broken, waived, not triggered or not yet due, rather than kept, as of 18 January 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q376c99f4ab",
  "kind": "yes/no",
  "text": "Shared with the club committee by Kai, the chat about the new kit design.\n\nMembers: Femi, Ana, Kai\nChat log (oldest first):\n[28 Jun 2026] Femi: @Kai I promise to return the loaned helmets by July 2, 2026.\n[1 Jul 2026] Femi: @Ana Count on me to service the tandem bike by July 6, 2026 if the swap meet is on.\n[3 Jul 2026] Femi: Just so you know, the swap meet is on as scheduled.\n[4 Jul 2026] Kai: @Femi I'll be sure to tune the gear cables by July 10, 2026.\n[5 Jul 2026] Kai: @Femi Ah, no stress, no need for you to service the tandem bike\n[9 Jul 2026] Femi: @Ana Ticked off my list: service the tandem bike, yay.",
  "question": "On the card, was Femi's promise to service the tandem bike kept, rather than broken, waived, not triggered or not yet due, at the end of July 6, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa097c18e67",
  "kind": "yes/no",
  "text": "{\"subject\": \"the lodger house rules\", \"source\": \"group chat export\", \"shared_by\": \"Jonas\"}\n\nMembers: Jonas, Wren, Elif, Femi\nChat log (oldest first):\n[27 Oct 2026] Elif: Will attempt to cut a spare door key by 30 October 2026, can't promise.\n[29 Oct 2026] Elif: @Wren Ticket's mine, I'll cut a spare door key by 6 November 2026.\n[29 Oct 2026] Elif: @Wren Is 9 November 2026 alright for me to cut a spare door key?\n[31 Oct 2026] Femi: @Elif Provided the lodger farewell supper happens, I'll feed the house plants by 7 November 2026.\n[2 Nov 2026] Jonas: @Elif Yes, you can cut a spare door key by 9 November 2026 if that suits you.\n[5 Nov 2026] Wren: Really pleased to say the lodger farewell supper will go ahead!",
  "question": "As the rules on the card set out, is it the case that Elif has broken the promise to cut a spare door key at the end of 12 November 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q80eb27c97c",
  "kind": "choice",
  "text": "{\"source\": \"saved thread\", \"about\": \"the old house restoration\", \"owner\": \"Sami\", \"kind\": \"chat export\"}\n\nMembers: Mo, Lee, Oskar, Sami\nChat log (oldest first):\n[23 Jul 2026] Sami: @Mo I promise to bleed the attic radiators by 25 July 2026.\n[23 Jul 2026] Sami: @Mo Scratch what I said, I won't bleed the attic radiators.\n[24 Jul 2026] Oskar: @Lee Guaranteed I'll oil the back door hinges by 31 July 2026.\n[27 Jul 2026] Sami: @Oskar Promise to replace the hallway bulbs by 5 August 2026 if the loft clearance day goes ahead.\n[28 Jul 2026] Sami: @Oskar Don't sweat it, there's no need to oil the back door hinges\n[4 Aug 2026] Mo: Yay, the loft clearance day is all set to go!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Oskar's pledge to oil the back door hinges sit at the end of 28 July 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "qa57df24429",
  "kind": "yes/no",
  "text": "We are getting ready for the street watch scheme, and Kai shared this chat with us.\n\nMembers: Lee, Kofi, Dara, Kai\nChat log (oldest first):\n[30 Apr 2026] Kofi: @Kai I'll bring the bins in by 5 May 2026, provided the road works meeting happens.\n[30 Apr 2026] Dara: @Kai It's on me to lock the side gate by 6 May 2026.\n[1 May 2026] Kai: @Dara Forget it, you won't need to lock the side gate\n[2 May 2026] Lee: Team, the road works meeting stays on as booked.\n[2 May 2026] Dara: @Kofi You are released, no requirement to bring the bins in.\n[5 May 2026] Kai: Any idea how close you are to bring the bins in?",
  "question": "Per the card's rules, on 5 May 2026, has Kofi's promise to bring the bins in been kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q82b6e8f74f",
  "kind": "choice",
  "text": "Messages with the letting agent about the kitchen refit, forwarded by Ivo for the rental file.\n\nMembers: Nadia, Elif, Ivo\nChat log (oldest first):\n[21 May 2026] Elif: @Nadia Ticket's mine, I'll forward the gas bill by 29 May 2026.\n[22 May 2026] Nadia: I'll try to collect the spare flat keys by 25 May 2026.\n[22 May 2026] Nadia: @Ivo Relax, I'll wipe the cooker hood by 27 May 2026, promise.\n[23 May 2026] Nadia: @Ivo I assure you I'll collect the spare flat keys by 30 May 2026 if the window cleaner visit is on.\n[24 May 2026] Nadia: @Elif Good news, you're let off having to forward the gas bill\n[29 May 2026] Nadia: Fab, we are on for the window cleaner visit as planned!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Nadia made to collect the spare flat keys is in which status at the end of 30 May 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "qde35cd9737",
  "kind": "choice",
  "text": "{\"saved_copy_of\": \"group chat\", \"subject\": \"the training plan\", \"saver\": \"Oskar\", \"format\": \"plain text\"}\n\nMembers: Kofi, Oskar, Rhea\nChat log (oldest first):\n[1 Feb 2026] Kofi: Aiming to service the tandem bike by 12 Feb 2026, we'll see.\n[3 Feb 2026] Kofi: @Oskar Only if the hill climb is on, I will service the tandem bike by 10 Feb 2026.\n[5 Feb 2026] Oskar: @Kofi I'll be sure to wash the club jerseys by 9 Feb 2026.\n[6 Feb 2026] Oskar: @Kofi Can I wash the club jerseys by 14 Feb 2026 instead? I did promise, sorry.\n[8 Feb 2026] Kofi: @Oskar Of course, it is fine for you to wash the club jerseys by 14 Feb 2026.\n[8 Feb 2026] Oskar: Fab, we are on for the hill climb as planned!\n[9 Feb 2026] Kofi: @Oskar Is 12 Feb 2026 alright for me to service the tandem bike?\n[9 Feb 2026] Rhea: @Kofi Relax, mate, you're not expected to service the tandem bike",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nFollowing the rules set out on the card, what date governs Kofi's commitment to service the tandem bike at the end of 13 Feb 2026, once any agreed shift in the date is factored in?",
  "options": [
   "12 Feb 2026",
   "9 Feb 2026",
   "10 Feb 2026"
  ]
 },
 {
  "qid": "q1906f1a393",
  "kind": "choice",
  "text": "{\"record_type\": \"saved chat\", \"matter\": \"the desk plan\", \"by\": \"Tomas\", \"stored\": \"as text\"}\n\nMembers: Omar, Femi, Tomas, Dara\nChat log (oldest first):\n[3 May 2026] Omar: @Femi I'll collect the visitor badges by 11 May 2026, providing the building survey goes ahead.\n[3 May 2026] Femi: Appreciate you telling me.\n[8 May 2026] Omar: Update: the building survey is going ahead as planned.\n[9 May 2026] Omar: @Tomas I own this, I'll order the office stationery by 17 May 2026.\n[11 May 2026] Omar: @Femi Any chance I can collect the visitor badges by 16 May 2026 instead?\n[11 May 2026] Tomas: @Omar Of course, it is fine for you to collect the visitor badges by 16 May 2026.\n[12 May 2026] Omar: @Tomas Committing to print the staff rota by 21 May 2026.\n[15 May 2026] Tomas: @Dara I'll renew the fire extinguisher service by 21 May 2026, promise.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 14 May 2026, by what date does Omar have to collect the visitor badges, counting any agreed change of date?",
  "options": [
   "11 May 2026",
   "17 May 2026",
   "16 May 2026"
  ]
 },
 {
  "qid": "q7d8778d44b",
  "kind": "yes/no",
  "text": "Shared by Tomas, an export of a household chat about the family photo book, as saved.\n\nMembers: Femi, Sami, Tomas, Kai\nChat log (oldest first):\n[16 Feb 2026] Femi: @Kai I'll pack the picnic basket by 20 February 2026, promise.\n[17 Feb 2026] Femi: @Tomas I'll mend the kite string by 19 February 2026, providing the sleepover weekend goes ahead.\n[17 Feb 2026] Sami: Just so you know, the sleepover weekend is on as scheduled.\n[19 Feb 2026] Femi: @Kai Can I pack the picnic basket by 26 February 2026 instead? I did promise, sorry.\n[20 Feb 2026] Femi: @Kai Ticked off: pack the picnic basket, feels so good\n[20 Feb 2026] Kai: Any news on plans to pack the picnic basket?",
  "question": "Going by the card's rules, does Femi not keep the promise to pack the picnic basket at the end of 20 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q453b7afd74",
  "kind": "yes/no",
  "text": "Arlo saved this so we stay on the same page about the kitchen garden project, mates.\n\nMembers: Arlo, Dara, Tess\nChat log (oldest first):\n[28 Oct 2026] Dara: @Tess Count on me to collect the seed potatoes by 2 Nov 2026.\n[28 Oct 2026] Tess: @Dara Provided the water tank delivery happens, I'll stake the tomato canes by 30 Oct 2026.\n[29 Oct 2026] Arlo: @Tess I will sow the broad beans by 5 Nov 2026 only if the seed swap day happens.\n[31 Oct 2026] Dara: @Tess Scratch that, I'm not going to collect the seed potatoes\n[1 Nov 2026] Tess: Scrapping the seed swap day, apologies to all.\n[2 Nov 2026] Dara: @Tess Lovely, I'll deliver the surplus runner beans by 11 Nov 2026 for sure.",
  "question": "By the close of 4 Nov 2026, is the promise Arlo made to sow the broad beans kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q261d4f69a5",
  "kind": "yes/no",
  "text": "Yo flatmates, Ana shared this chat about the flatmate contract terms, so chip in.\n\nMembers: Ines, Ana, Jonas\nChat log (oldest first):\n[4 Sep 2026] Jonas: @Ines No promises, but I'll aim to scan the council tax letter by 10 Sep 2026.\n[5 Sep 2026] Ana: @Ines I will copy the house keys by 14 Sep 2026 only if the agent inventory walk happens.\n[6 Sep 2026] Jonas: @Ana Count on me to scan the council tax letter by 9 Sep 2026.\n[8 Sep 2026] Jonas: @Ana I have to take back my promise to scan the council tax letter.\n[8 Sep 2026] Jonas: Please note the agent inventory walk will proceed.\n[9 Sep 2026] Ana: @Jonas Count on me, I'll ring the letting agent by 17 Sep 2026.",
  "question": "Is Jonas's promise to scan the council tax letter broken at the end of 8 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd983126ac5",
  "kind": "choice",
  "text": "Shared by Kai, this freelance thread with a client is about the rebrand package.\n\nMembers: Jonas, Kai\nChat log (oldest first):\n[22 Feb 2026] Jonas: @Kai I own this, I'll pick the colour swatches by 26 Feb 2026.\n[23 Feb 2026] Jonas: @Kai It's on me to mail the business cards by 26 Feb 2026.\n[25 Feb 2026] Jonas: @Kai Scratch what I said, I won't mail the business cards.\n[27 Feb 2026] Jonas: @Kai I will check the poster proofs by 2 Mar 2026 only if the packaging launch happens.\n[1 Mar 2026] Kai: On track for the packaging launch to happen as planned.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Jonas made to check the poster proofs, what state is it in at the end of 1 Mar 2026?",
  "options": [
   "Broken",
   "Waived",
   "Kept",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qaf85be95e2",
  "kind": "choice",
  "text": "Omar shared this to pin down the speed bump plan, housemates.\n\nMembers: Dara, Rhea, Omar\nChat log (oldest first):\n[20 Oct 2026] Omar: @Rhea I'll lock the side gate by 2026-10-29 if the speed camera survey goes ahead.\n[21 Oct 2026] Omar: @Dara It's on me to walk the old spaniel by 2026-10-25.\n[24 Oct 2026] Rhea: @Dara Count on me to sweep the pavement outside by 2026-10-28.\n[24 Oct 2026] Dara: Cheers, noted.\n[24 Oct 2026] Rhea: @Dara Count on me to lend the stepladder by 2026-10-30 if the bonfire night is on.\n[28 Oct 2026] Dara: @Rhea Forget it, you won't need to sweep the pavement outside",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Rhea's promise to sweep the pavement outside at the end of 2026-10-29?",
  "options": [
   "Kept",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "qfe6536f4c7",
  "kind": "yes/no",
  "text": "The family thread was saved by Ana, and its subject is the garden shed build.\n\nMembers: Ana, Greta, Ivo\nChat log (oldest first):\n[10 Jul 2026] Ana: @Ivo Promise to build the compost bay by 19 July 2026 if the village flower show goes ahead.\n[10 Jul 2026] Greta: @Ivo Absolutely, I will sow the broad beans by 12 July 2026.\n[11 Jul 2026] Greta: @Ana Relax, I'll weed the carrot row by 14 July 2026, promise.\n[13 Jul 2026] Ivo: @Ana I assure you I'll fix the shed door by 20 July 2026 if the water tank delivery is on.\n[13 Jul 2026] Greta: @Ana Log entry: weed the carrot row, carried out",
  "question": "According to the card's rules, is the promise Greta made to weed the carrot row not kept as of 15 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc4b0445e1b",
  "kind": "choice",
  "text": "{\"subject\": \"the platform rewrite\", \"source\": \"group chat export\", \"shared_by\": \"Lee\"}\n\nMembers: Lee, Tess\nChat log (oldest first):\n[14 May 2026] Lee: @Tess Lovely, I'll merge the login branch by 18 May 2026 if the code freeze is on.\n[17 May 2026] Lee: @Tess Count on me to review the pull request by 25 May 2026.\n[17 May 2026] Tess: @Lee You don't have to review the pull request at all\n[17 May 2026] Tess: Please note the code freeze will proceed.\n[17 May 2026] Lee: @Tess Is it all right if I merge the login branch by 24 May 2026 instead?\n[19 May 2026] Lee: @Tess Got myself to merge the login branch lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich status ends up on the promise Lee made to merge the login branch at the end of 16 May 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Not yet due",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "qfa0aaa7489",
  "kind": "choice",
  "text": "Shared by Malik, a help-desk thread covering the spring campaign.\n\nMembers: Malik, Wren, Ivo\nChat export (date | from | to | message):\n2026-07-09 | Malik | Wren | Guaranteed I'll fix the landing page headline by 17 July 2026.\n2026-07-11 | Ivo | Wren | Promise to collect the survey answers by 16 July 2026 if the brand photo shoot goes ahead.\n2026-07-13 | Ivo | Malik | Ah, no stress, no need for you to fix the landing page headline\n2026-07-14 | Ivo | Malik | If the webinar rehearsal is on, I'll definitely set up the analytics dashboard by 19 July 2026.\n2026-07-17 | Ivo | group | Sorry, the webinar rehearsal is off.\n2026-07-17 | Malik | Wren | Ta-da, I went and did it: fix the landing page headline!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat would you say the situation is with Malik and their promise to fix the landing page headline at the end of 16 July 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Not yet due",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q55a1090799",
  "kind": "yes/no",
  "text": "Help desk export\nAbout: the caring rota\nCopied by: Leila\n\nMembers: Ines, Tess, Oskar, Leila\nChat log (oldest first):\n[24 Jan 2026] Oskar: @Tess Relax, I'll fetch the mobility aids by 26 January 2026 for sure.\n[26 Jan 2026] Oskar: Hoping to book the clinic transport by 28 January 2026, but can't promise.\n[27 Jan 2026] Oskar: @Tess Promise to book the clinic transport by 2 February 2026 if the carer handover goes ahead.\n[1 Feb 2026] Ines: Sadly, the carer handover is not going ahead.\n[2 Feb 2026] Oskar: @Tess Any chance I can book the clinic transport by 4 February 2026 instead?\n[2 Feb 2026] Tess: @Oskar Revised deadline is 4 February 2026, so you can book the clinic transport.",
  "question": "When you check the chat at the end of 5 February 2026, is the promise Oskar made to book the clinic transport broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q50b0dbb3bf",
  "kind": "choice",
  "text": "Subject: Saved thread about the store makeover\nThis export from Wren is pasted in full for readers who want it.\n\nMembers: Wren, Ivo\nChat log (oldest first):\n[3 Jul 2026] Ivo: @Wren I assure you I'll mail the business cards by Thursday, 9 July 2026 if the sign reveal is on.\n[3 Jul 2026] Ivo: Please note the sign reveal will proceed.\n[4 Jul 2026] Ivo: @Wren Might I ask whether I could mail the business cards by Saturday, 11 July 2026 instead?\n[9 Jul 2026] Ivo: @Wren Ticked off my list: mail the business cards, yay.\n[9 Jul 2026] Wren: @Ivo You can bet I'll send the moodboard files by Tuesday, 14 July 2026.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Ivo's promise to mail the business cards at the end of Wednesday, 8 July 2026?",
  "options": [
   "Broken",
   "Waived",
   "Kept",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qc1028192c8",
  "kind": "choice",
  "text": "Client thread on the shop rebuild, shared by Yuki for the project log.\n\nMembers: Lee, Tomas, Nadia, Yuki\nChat log (oldest first):\n[18 Feb 2026] Lee: @Yuki Ticket's mine, I'll restore the old theme by 27 February 2026.\n[20 Feb 2026] Tomas: @Lee Lovely, I'll test the mobile layout by 27 February 2026 for sure.\n[22 Feb 2026] Lee: @Yuki Promise to print the packing slips by 28 February 2026 if the site handover goes ahead.\n[23 Feb 2026] Tomas: Fab, we are on for the site handover as planned!\n[27 Feb 2026] Nadia: @Lee No worries, you don't need to print the packing slips",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status does the chat show for the promise Lee made to print the packing slips at the end of 2 March 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "q438df88980",
  "kind": "choice",
  "text": "Note: help desk thread about the campaign edit\nSaved by: Ravi\n\nMembers: Ravi, Tomas, Elif\nChat log (oldest first):\n[5 Jul 2026] Ravi: @Tomas I will make sure to back up the project drives by 12 July 2026.\n[9 Jul 2026] Ravi: @Tomas I promise to record the voice over by 15 July 2026 if the agency review call is on.\n[12 Jul 2026] Ravi: Please note the agency review call will proceed.\n[12 Jul 2026] Ravi: @Tomas Got myself to back up the project drives lol.\n[13 Jul 2026] Ravi: @Tomas Quick question, could I record the voice over by 19 July 2026 instead?\n[15 Jul 2026] Tomas: @Ravi Yes, you have the green light to record the voice over by 19 July 2026.\n[19 Jul 2026] Ravi: @Tomas Quick report: I've managed to record the voice over",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules, when is the date by which Ravi has to record the voice over at the end of 16 July 2026, allowing for any agreed change?",
  "options": [
   "12 July 2026",
   "15 July 2026",
   "19 July 2026"
  ]
 },
 {
  "qid": "q74942f997e",
  "kind": "yes/no",
  "text": "Attached chat: the music library\nShared by: Oskar\n\nMembers: Oskar, Femi, Rhea, Malik\nChat log (oldest first):\n[21 Feb 2026] Femi: Will attempt to move the piano by 6 March 2026, can't promise.\n[22 Feb 2026] Malik: @Femi Provided the summer recital happens, I'll set up the sound desk by 3 March 2026.\n[23 Feb 2026] Femi: @Rhea Got it, I'll move the piano by 2 March 2026 for sure.\n[25 Feb 2026] Femi: @Rhea Only if the sing along is on, I will collect the sheet music by 3 March 2026.\n[26 Feb 2026] Malik: @Femi Please don't feel you have to move the piano\n[2 Mar 2026] Femi: @Rhea To note: I have managed to move the piano",
  "question": "Applying the card's rules, can it be said that Femi has not kept the promise to move the piano at the end of 8 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf07a29b78b",
  "kind": "yes/no",
  "text": "Chat attached to the support case about the winter concert, shared by Femi.\n\nMembers: Ivo, Femi, Sami, Arlo\nChat log (oldest first):\n[24 Jul 2026] Ivo: @Sami I'll move the piano by 27 Jul 2026, providing the choir festival goes ahead.\n[24 Jul 2026] Ivo: @Femi I will make sure to set up the sound desk by 29 Jul 2026.\n[26 Jul 2026] Sami: Lovely, the choir festival is definitely happening!\n[27 Jul 2026] Ivo: @Arlo I'll be sure to send the audition reminders by 1 Aug 2026.\n[1 Aug 2026] Arlo: @Ivo No worries, you don't need to send the audition reminders",
  "question": "Under the rules on the card, is it true that Ivo has not kept the promise to send the audition reminders as of 6 Aug 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9c27b3c10a",
  "kind": "choice",
  "text": "Subject: chat export on the grant renewal\nThe full chat follows, saved by Tomas, for you to read.\n\nMembers: Malik, Tomas, Ivo\nChat export (date | from | to | message):\n2026-09-09 | Tomas | Ivo | You can bank on me to return the library books by 13 Sep 2026.\n2026-09-10 | Ivo | Tomas | Promise to book the microscope slot by 19 Sep 2026 if the conference trip goes ahead.\n2026-09-12 | Tomas | Ivo | Quick question, could I return the library books by 17 Sep 2026 instead?\n2026-09-12 | Ivo | Tomas | Fine by me, you can return the library books by 17 Sep 2026.\n2026-09-17 | Tomas | Ivo | Forget what I said, I won't return the library books\n2026-09-17 | Malik | Tomas | Forget it, you won't need to return the library books\n2026-09-18 | Ivo | group | Sorry all, the conference trip is called off.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIf the chat is checked at the end of 16 Sep 2026, which date marks the deadline for Tomas to return the library books, with agreed date changes included?",
  "options": [
   "19 Sep 2026",
   "17 Sep 2026",
   "13 Sep 2026"
  ]
 },
 {
  "qid": "q0df8581e14",
  "kind": "choice",
  "text": "Shared by Malik, a help-desk thread covering the spring campaign.\n\nMembers: Malik, Wren, Ivo\nChat export (date | from | to | message):\n2026-07-09 | Malik | Wren | Guaranteed I'll fix the landing page headline by 17 July 2026.\n2026-07-11 | Ivo | Wren | Promise to collect the survey answers by 16 July 2026 if the brand photo shoot goes ahead.\n2026-07-13 | Wren | Malik | Ah, no stress, no need for you to fix the landing page headline\n2026-07-14 | Ivo | Malik | If the webinar rehearsal is on, I'll definitely set up the analytics dashboard by 19 July 2026.\n2026-07-17 | Ivo | group | Sorry, the webinar rehearsal is off.\n2026-07-17 | Malik | Wren | Ta-da, I went and did it: fix the landing page headline!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat would you say the situation is with Malik and their promise to fix the landing page headline at the end of 16 July 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Not yet due",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q2c4d55a08e",
  "kind": "yes/no",
  "text": "Channel title: work team chat\nDescription: about the social media plan, exported by Malik.\n\nMembers: Elif, Zara, Malik\nChat export (date | from | to | message):\n2026-02-21 | Zara | Malik | I promise to return the rented camera gear by 1 March 2026.\n2026-02-25 | Elif | Malik | Lovely, I'll fetch the campaign budget sheet by 2 March 2026 if the annual review is on.\n2026-02-26 | Zara | Malik | Sorry, I won't return the rented camera gear after all\n2026-02-26 | Elif | Zara | Good news, you're let off having to return the rented camera gear\n2026-03-01 | Zara | group | We are dropping the annual review from the list.",
  "question": "Has Zara broken the promise to return the rented camera gear at the end of 27 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf27a86e4be",
  "kind": "yes/no",
  "text": "Here's the flatmate chat that Jonas saved, about the house refit.\n\nMembers: Jonas, Rhea, Mo\nChat export (date | from | to | message):\n2026-05-03 | Mo | Jonas | Relax, I'll scrape the old wallpaper by 7 May 2026 for sure.\n2026-05-03 | Jonas | Mo | Don't sweat it, there's no need to scrape the old wallpaper\n2026-05-05 | Jonas | Mo | As long as the kitchen fitting day is on, I will pay the plumbing invoice by 13 May 2026.\n2026-05-10 | Rhea | group | Yay, the kitchen fitting day is all set to go!\n2026-05-13 | Jonas | Mo | Mum, I did pay the plumbing invoice, haha.",
  "question": "According to the rules on the card, has Jonas broken the promise to pay the plumbing invoice at the end of 14 May 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q79d0f3f8f1",
  "kind": "yes/no",
  "text": "Volunteers, this is the winter concert thread that Leila shared with the committee.\n\nMembers: Omar, Leila, Wren\nChat log (oldest first):\n[21 May 2026] Leila: @Omar Count on me to move the piano by 27 May 2026.\n[23 May 2026] Wren: @Omar I'll buy the spare folders by 28 May 2026 as long as the sing along is on.\n[26 May 2026] Leila: @Omar Would it be fine if I move the piano by 1 Jun 2026 instead, yeah?\n[26 May 2026] Leila: @Omar Provided the carol concert happens, I will send the audition reminders by 31 May 2026.\n[30 May 2026] Leila: Update: the carol concert is going ahead as planned.\n[31 May 2026] Leila: @Omar Guess what, I managed to move the piano!",
  "question": "Is the promise to move the piano that Leila made broken at the end of 31 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5c062dcf99",
  "kind": "yes/no",
  "text": "Client thread on the online store move, saved by Bruno for the project log.\n\nMembers: Bruno, Ana, Lee\nChat log (oldest first):\n[18 May 2026] Lee: @Bruno As long as the site handover is on, I'll fetch the domain login by 22 May 2026.\n[19 May 2026] Lee: @Ana I'll set up the email forwarding by 25 May 2026, providing the stock count goes ahead.\n[20 May 2026] Lee: @Bruno Relax, I'll renew the hosting plan by 24 May 2026, promise.\n[23 May 2026] Ana: @Lee Nobody needs you to renew the hosting plan, that's that\n[25 May 2026] Lee: @Bruno Got myself to renew the hosting plan lol.",
  "question": "According to the rules on the card, is it true that the promise Lee made to renew the hosting plan has not been broken at the end of 26 May 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe28a2a7fbb",
  "kind": "choice",
  "text": "{\"saved_copy\": \"the big day\", \"keeper\": \"Ivo\", \"medium\": \"chat transcript\"}\n\nMembers: Femi, Yuki, Ivo\nChat log (oldest first):\n[29 Apr 2026] Yuki: @Femi Relax, I'll collect the venue floor plan by Monday, May 4, 2026, promise.\n[29 Apr 2026] Femi: Oh cheers, that helps.\n[3 May 2026] Yuki: @Ivo If the cake tasting is on, I'll definitely print the seating cards by Friday, May 8, 2026.\n[3 May 2026] Yuki: Sorry all, the cake tasting is called off.\n[4 May 2026] Ivo: @Yuki Don't sweat it, there's no need to collect the venue floor plan\n[5 May 2026] Yuki: @Femi Log entry: collect the venue floor plan, carried out",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Yuki's commitment to collect the venue floor plan have at the end of Monday, May 4, 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Not yet due",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q9cf332d029",
  "kind": "choice",
  "text": "We are getting ready for the bathroom refit, and Malik shared this chat with us.\n\nMembers: Malik, Priya, Bruno, Wren\nChat export (date | from | to | message):\n2026-03-03 | Priya | Bruno | If the mortgage valuation visit goes ahead, I'll gladly collect the sanding pads by 6 March 2026.\n2026-03-03 | Bruno | Malik | Only if the removal van arrival is on, I will fetch the paint samples by 7 March 2026.\n2026-03-03 | Wren | group | On track for the removal van arrival to happen as planned.\n2026-03-03 | Priya | Bruno | Guaranteed I'll sweep the dust from stairs by 6 March 2026.\n2026-03-04 | Bruno | Malik | Log entry: fetch the paint samples, carried out\n2026-03-04 | Malik | Priya | No worries, you don't need to sweep the dust from stairs",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Bruno's promise to fetch the paint samples at the end of 3 March 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Not yet due",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "q4aa5039f4a",
  "kind": "yes/no",
  "text": "Shared by Priya, a help-desk thread covering the new kit design.\n\nMembers: Tomas, Priya, Sami\nChat log (oldest first):\n[27 Jan 2026] Priya: @Tomas Only if the group ride is on, I will wash the club jerseys by 3 Feb 2026.\n[28 Jan 2026] Priya: @Sami Got it, I'll set up the feed stop by 5 Feb 2026 for sure.\n[28 Jan 2026] Tomas: @Sami Count on me to tune the gear cables by 6 Feb 2026, if the mechanics clinic happens.\n[1 Feb 2026] Priya: @Sami Apologies, I'll not be able to set up the feed stop\n[1 Feb 2026] Sami: @Priya No worries, you don't need to set up the feed stop",
  "question": "Under the rules on the card, is Priya's promise to set up the feed stop kept as of 2 Feb 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7a5f52630f",
  "kind": "yes/no",
  "text": "{\"thread_kind\": \"exported conversation\", \"about\": \"the trade show push\", \"exported_by\": \"Zara\"}\n\nMembers: Rhea, Zara, Lena, Wren\nChat export (date | from | to | message):\n2026-07-03 | Lena | Rhea | Might be able to pay the printing invoice by 8 July 2026, who knows!\n2026-07-04 | Zara | Lena | I'll fetch the campaign budget sheet by 8 July 2026, promise.\n2026-07-04 | Wren | Rhea | It's on me to fix the landing page headline by 7 July 2026.\n2026-07-04 | Lena | Wren | If the trade fair stand goes ahead, I'll pay the printing invoice by 9 July 2026.\n2026-07-06 | Wren | group | Sorry all, the trade fair stand is called off.\n2026-07-09 | Zara | Lena | Got myself to fetch the campaign budget sheet lol.",
  "question": "Per the card's rules, on 7 July 2026, has Lena's promise to pay the printing invoice been kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4c00f8aa07",
  "kind": "yes/no",
  "text": "Subject: Chat about the school fundraiser\nBelow, with Sami named as the source, is the chat as exported.\n\nMembers: Sami, Wren, Bruno\nChat export (date | from | to | message):\n2026-04-26 | Wren | Sami | Provided the clothes swap happens, I'll fetch the tea urn by 1 May 2026.\n2026-04-27 | Sami | Bruno | You can bet I'll book the school hall by 29 April 2026.\n2026-05-01 | Wren | Bruno | Absolutely, I will label the raffle prizes by 6 May 2026.\n2026-05-01 | Sami | Bruno | Guess who managed to book the school hall, go team!\n2026-05-03 | Bruno | Sami | If the summer fete goes ahead, I'll gladly count the donation boxes by 11 May 2026.\n2026-05-05 | Wren | Bruno | For the record: I was able to label the raffle prizes",
  "question": "Under the rules on the card, is the promise Wren made to label the raffle prizes kept as of 10 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd00c83ceac",
  "kind": "yes/no",
  "text": "Neighbour and flatmate talk, copied out by Arlo: the student house hunt.\n\nMembers: Ana, Tomas, Arlo\nChat log (oldest first):\n[11 Apr 2026] Tomas: @Arlo I'll scan the council tax letter by 13 April 2026, providing the check in visit goes ahead.\n[12 Apr 2026] Ana: Sorry all, the check in visit is called off.\n[12 Apr 2026] Tomas: @Ana Relax, I'll copy the house keys by 16 April 2026 for sure.\n[12 Apr 2026] Tomas: @Ana Is 19 April 2026 alright for me to copy the house keys?\n[13 Apr 2026] Ana: @Tomas Don't sweat it, there's no need to copy the house keys\n[14 Apr 2026] Ana: @Arlo If the agent inventory walk goes ahead, I'll forward the inventory photos by 17 April 2026.",
  "question": "Going by the card's rules, does Tomas keep the promise to copy the house keys at the end of 18 April 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3035da144c",
  "kind": "choice",
  "text": "{\"subject\": \"the platform rewrite\", \"source\": \"group chat export\", \"shared_by\": \"Lee\"}\n\nMembers: Lee, Tess\nChat log (oldest first):\n[14 May 2026] Lee: @Tess Lovely, I'll merge the login branch by 18 May 2026 if the code freeze is on.\n[17 May 2026] Lee: @Tess Count on me to review the pull request by 25 May 2026.\n[17 May 2026] Tess: @Lee You don't have to review the pull request at all\n[17 May 2026] Tess: Please note the code freeze will proceed.\n[17 May 2026] Lee: @Tess Is it all right if I merge the login branch by 24 May 2026 instead?\n[19 May 2026] Lee: @Tess Got myself to merge the login branch lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich status ends up on the promise Lee made to merge the login branch at the end of 17 May 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Not yet due",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q9c03b99dad",
  "kind": "yes/no",
  "text": "Ravi saved this so we stay on the same page about the cellar project, mates.\n\nMembers: Ravi, Arlo, Sami, Yuki\nChat log (oldest first):\n[28 Sep 2026] Sami: @Arlo I'll wash the sash windows by 7 October 2026, promise.\n[29 Sep 2026] Arlo: @Ravi I'll mend the garden gate by 4 October 2026 if the loft clearance day goes ahead.\n[1 Oct 2026] Yuki: @Sami I own this, I'll find the loft ladder by 6 October 2026.\n[1 Oct 2026] Yuki: @Sami Please don't feel you have to wash the sash windows\n[3 Oct 2026] Yuki: Quick heads up, the loft clearance day is scrapped.",
  "question": "Under the rules on the card, is the promise Arlo made to mend the garden gate in a status other than broken at the end of 8 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q37d8863772",
  "kind": "choice",
  "text": "Shared by Lee for the committee, this is the group chat on the new repertoire.\n\nMembers: Ines, Kai, Lee\nChat log (oldest first):\n[8 Oct 2026] Kai: @Ines As long as the summer recital is on, I'll fetch the choir robes by 15 Oct 2026.\n[11 Oct 2026] Ines: @Kai I promise to buy the spare folders by 15 Oct 2026 if the joint concert is on.\n[11 Oct 2026] Ines: @Lee I'll send the audition reminders by 16 Oct 2026, promise.\n[11 Oct 2026] Ines: @Lee I'm withdrawing my promise to send the audition reminders\n[14 Oct 2026] Ines: Fab, we are on for the summer recital as planned!\n[15 Oct 2026] Kai: @Ines You are released, no requirement to send the audition reminders.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Ines made to send the audition reminders is in which status at the end of 17 Oct 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Not yet due",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "q083324b175",
  "kind": "yes/no",
  "text": "Team thread shared by Oskar, covering the trade show push in the channel.\n\nMembers: Priya, Arlo, Elif, Oskar\nChat export (date | from | to | message):\n2026-06-09 | Oskar | Priya | You can bet I'll pay the printing invoice by 17 June 2026.\n2026-06-10 | Arlo | Elif | As long as the influencer call is on, I will return the rented camera gear by 18 June 2026.\n2026-06-13 | Oskar | Priya | Update on my side: I will not pay the printing invoice, sorry.\n2026-06-14 | Priya | Elif | As long as the webinar rehearsal is on, I will draft the press release by 19 June 2026.\n2026-06-17 | Priya | Oskar | No worries, you don't need to pay the printing invoice",
  "question": "Has Oskar's promise to pay the printing invoice ended up broken, waived, not triggered or not yet due, instead of kept, as of 19 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qde3bc7f40b",
  "kind": "yes/no",
  "text": "Lena shared this so the family follows the quiet street fund.\n\nMembers: Greta, Lena, Dara\nChat log (oldest first):\n[30 Aug 2026] Dara: @Greta Provided the speed camera survey happens, I'll bring the bins in by 4 September 2026.\n[30 Aug 2026] Greta: Sadly, the speed camera survey is not going ahead.\n[2 Sep 2026] Dara: @Greta It's on me to clear the hedge trimmings by 10 September 2026.\n[4 Sep 2026] Dara: @Greta Quick question, could I bring the bins in by 7 September 2026 instead?\n[4 Sep 2026] Greta: @Dara Yes, you have the green light to bring the bins in by 7 September 2026.",
  "question": "By the close of 6 September 2026, is the promise Dara made to bring the bins in kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6dadfdacf4",
  "kind": "choice",
  "text": "Help desk export\nAbout: the online store move\nCopied by: Bruno\n\nMembers: Oskar, Nadia, Bruno, Femi\nChat log (oldest first):\n[3 Sep 2026] Nadia: @Femi I'll try to renew the hosting plan by Monday, 14 September 2026, can't promise!\n[5 Sep 2026] Nadia: @Bruno Promise to renew the hosting plan by Saturday, 12 September 2026 if the product photo day goes ahead.\n[6 Sep 2026] Nadia: Sorry all, the product photo day is not happening.\n[7 Sep 2026] Oskar: @Nadia Relax, I'll fix the checkout button by Tuesday, 15 September 2026, promise.\n[9 Sep 2026] Oskar: @Nadia On my action item, may I fix the checkout button by Thursday, 17 September 2026 instead?\n[11 Sep 2026] Nadia: @Oskar Go ahead and fix the checkout button by Thursday, 17 September 2026, that is fine.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Nadia's pledge to renew the hosting plan sit at the end of Thursday, 10 September 2026?",
  "options": [
   "Kept",
   "Broken",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "qde10a0f0d5",
  "kind": "yes/no",
  "text": "Subject: Chat about the school fundraiser\nBelow, with Sami named as the source, is the chat as exported.\n\nMembers: Sami, Wren, Bruno\nChat export (date | from | to | message):\n2026-04-26 | Wren | Sami | Provided the clothes swap happens, I'll fetch the tea urn by 1 May 2026.\n2026-04-27 | Sami | Bruno | You can bet I'll book the school hall by 29 April 2026.\n2026-05-01 | Wren | Bruno | Absolutely, I will label the raffle prizes by 6 May 2026.\n2026-05-01 | Sami | Bruno | Guess who managed to book the school hall, go team!\n2026-05-03 | Bruno | Sami | If the summer fete goes ahead, I'll gladly count the donation boxes by 11 May 2026.\n2026-05-05 | Wren | Bruno | For the record: I was able to label the raffle prizes",
  "question": "Would you say Wren didn't keep the promise to label the raffle prizes by the end of 10 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q09cef5ccb9",
  "kind": "choice",
  "text": "A family chat export on the quiet street fund, shared out by Lena.\n\nMembers: Lena, Malik, Sami\nChat log (oldest first):\n[14 Feb 2026] Lena: @Malik Guaranteed I'll lend the stepladder by 22 February 2026.\n[15 Feb 2026] Sami: @Lena I'll take in the post by 21 February 2026 if the parking permit visit goes ahead.\n[16 Feb 2026] Malik: @Lena I'm aiming to sweep the pavement outside by 24 February 2026, might manage it.\n[16 Feb 2026] Sami: We are dropping the parking permit visit from the list.\n[17 Feb 2026] Malik: @Sami Absolutely, I will sweep the pavement outside by 20 February 2026.\n[20 Feb 2026] Malik: @Sami For the record: I was able to sweep the pavement outside",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Malik's promise to sweep the pavement outside at the end of 20 February 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not triggered",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qe867b73ebf",
  "kind": "yes/no",
  "text": "{\"export_type\": \"group chat export\", \"chat_topic\": \"the guest welcome plan\", \"saved_by\": \"Malik\"}\n\nMembers: Malik, Zara, Lena, Rhea\nChat log (oldest first):\n[9 Apr 2026] Rhea: @Lena Might be able to leave the welcome basket by 12 April 2026, who knows!\n[11 Apr 2026] Rhea: @Malik I promise to leave the welcome basket by 18 April 2026 if the lettings photo shoot is on.\n[14 Apr 2026] Rhea: @Lena I will make sure to wheel the bins out by 19 April 2026.\n[17 Apr 2026] Rhea: Sorry all, the lettings photo shoot is called off.\n[18 Apr 2026] Rhea: @Malik Think 22 April 2026 would work if I leave the welcome basket instead?\n[18 Apr 2026] Malik: @Rhea Revised deadline is 22 April 2026, so you can leave the welcome basket.",
  "question": "According to the card's rules, is the promise Rhea made to leave the welcome basket not kept as of 21 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q40eca47fdd",
  "kind": "yes/no",
  "text": "Subject: export of the group chat on the guest list\nHere is the chat as saved by Zara, pasted below.\n\nMembers: Ravi, Zara, Femi, Malik\nChat log (oldest first):\n[26 Apr 2026] Ravi: @Femi I'll fetch the spare memory cards by 30 Apr 2026, provided the bridal shower happens.\n[27 Apr 2026] Zara: @Malik Relax, I'll set up the backdrop frame by 3 May 2026, promise.\n[29 Apr 2026] Femi: Quick heads up, the bridal shower is scrapped.\n[29 Apr 2026] Ravi: @Femi Can I fetch the spare memory cards by 4 May 2026 instead? I did promise, sorry.\n[30 Apr 2026] Femi: @Ravi Yes, you have the green light to fetch the spare memory cards by 4 May 2026.",
  "question": "Under the rules on the card, is the promise Ravi made to fetch the spare memory cards in a status other than broken at the end of 1 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd38cdda24b",
  "kind": "yes/no",
  "text": "{\"archive\": \"group chat\", \"subject\": \"the trade show push\", \"sent_by\": \"Tess\"}\n\nMembers: Kai, Tess, Nadia, Rhea\nChat export (date | from | to | message):\n2026-10-16 | Kai | Tess | Count on me, I'll draft the press release by October 25, 2026.\n2026-10-16 | Rhea | Tess | Relax, I'll return the rented camera gear by October 24, 2026 for sure.\n2026-10-16 | Tess | Nadia | If the trade fair stand goes ahead, I'll collect the survey answers by October 23, 2026.\n2026-10-19 | Kai | Tess | Update on my side: I will not draft the press release, sorry.\n2026-10-22 | Rhea | group | Please note the trade fair stand will proceed.\n2026-10-24 | Rhea | Tess | Got myself to return the rented camera gear lol.",
  "question": "At the end of October 30, 2026, does the promise Rhea made to return the rented camera gear have any status except broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
