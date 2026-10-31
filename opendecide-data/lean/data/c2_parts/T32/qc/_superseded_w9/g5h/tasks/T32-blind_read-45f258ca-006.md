# G5-H blind read T32-blind_read-45f258ca-006 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T32/qc/g5h/answers/T32-blind_read-45f258ca-006.json

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
  "qid": "qcf6816d741",
  "kind": "choice",
  "text": "Freelance chat about the payment setup\nThe client side, saved by Wren.\n\nMembers: Zara, Omar, Wren\nChat log (oldest first):\n[27 May 2026] Omar: @Zara I promise to set up the email forwarding by 2026-06-03 if the courier pickup is on.\n[28 May 2026] Omar: @Wren It's on me to fix the checkout button by 2026-05-30.\n[28 May 2026] Zara: Sad to report that the courier pickup is off.\n[28 May 2026] Omar: @Zara Might I ask whether I could set up the email forwarding by 2026-06-09 instead?\n[31 May 2026] Wren: @Omar Yes, all good for you to set up the email forwarding by 2026-06-09 instead.\n[1 Jun 2026] Zara: @Wren Only if the site handover is on, I will add the size chart by 2026-06-10.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Omar made to set up the email forwarding is in which status at the end of 2026-06-02?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q36940ea522",
  "kind": "yes/no",
  "text": "Wren forwarded this for the committee, covering the volunteer roster.\n\nMembers: Nadia, Ines, Wren, Priya\nChat export (date | from | to | message):\n2026-05-15 | Nadia | Priya | As long as the field day is on, I will return the borrowed trestle tables by 19 May 2026.\n2026-05-17 | Wren | group | Maybe I can send the newsletter drafts by 21 May 2026.\n2026-05-17 | Nadia | Priya | It's on me to fetch the tea urn by 20 May 2026.\n2026-05-18 | Ines | group | Sadly, the field day is not going ahead.\n2026-05-19 | Wren | Priya | Relax, I'll send the newsletter drafts by 25 May 2026 for sure.\n2026-05-25 | Wren | Priya | To my relief, I managed to send the newsletter drafts.",
  "question": "Does the card's rule set show that Wren has not kept the promise to send the newsletter drafts at the end of 26 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9a3d0b859f",
  "kind": "yes/no",
  "text": "Subject: Chat about the family day out\nBelow is a copy that came from Omar, pasted as found.\n\nMembers: Omar, Malik, Greta, Priya\nChat log (oldest first):\n[23 Oct 2026] Malik: @Greta Hoping to fetch the craft box by 30 Oct 2026, but can't promise.\n[23 Oct 2026] Omar: @Priya I'll pick up the school bags by 31 Oct 2026 if the puppet show goes ahead.\n[24 Oct 2026] Malik: @Omar Guaranteed I'll fetch the craft box by 28 Oct 2026.\n[24 Oct 2026] Greta: @Malik Got it, I'll teach the card game by 27 Oct 2026 for sure.\n[26 Oct 2026] Omar: Yep, the puppet show is on as planned.\n[28 Oct 2026] Omar: @Malik You are released, no requirement to fetch the craft box.",
  "question": "Going by the card's rules, does Malik not keep the promise to fetch the craft box at the end of 2 Nov 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf88246f160",
  "kind": "yes/no",
  "text": "{\"record\": \"shared group chat\", \"subject\": \"the payment setup\", \"shared_by\": \"Lee\", \"stored\": \"as text\"}\n\nMembers: Oskar, Kai, Hana, Lee\nChat log (oldest first):\n[31 Jan 2026] Oskar: @Hana I promise to restore the old theme by 9 Feb 2026 if the market day is on.\n[3 Feb 2026] Lee: @Oskar Provided the courier pickup happens, I will send the stock spreadsheet by 11 Feb 2026.\n[5 Feb 2026] Oskar: Yep, the courier pickup is on as planned.\n[5 Feb 2026] Lee: @Oskar I committed to send the stock spreadsheet, can I do that by 14 Feb 2026 instead?\n[6 Feb 2026] Hana: @Lee You can bank on me to print the packing slips by 12 Feb 2026.\n[8 Feb 2026] Oskar: @Lee Not moving it, send the stock spreadsheet by the existing date.",
  "question": "According to the rules on the card, is it true that the promise Lee made to send the stock spreadsheet has not been broken at the end of 16 Feb 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6238c02682",
  "kind": "yes/no",
  "text": "Ravi shared this to pin down the garden makeover, housemates.\n\nMembers: Tomas, Tess, Ravi, Rhea\nChat export (date | from | to | message):\n2026-09-16 | Ravi | Tomas | I'll try to print the floor plan by 22 Sep 2026, no guarantee.\n2026-09-18 | Ravi | Rhea | Provided the boiler install visit happens, I will print the floor plan by 24 Sep 2026.\n2026-09-20 | Ravi | Tomas | I will scrape the old wallpaper by 27 Sep 2026.\n2026-09-23 | Tomas | group | On track for the boiler install visit to happen as planned.\n2026-09-24 | Rhea | Ravi | Quick update: you do not need to print the floor plan at all.\n2026-09-25 | Tomas | Ravi | No worries, you don't need to scrape the old wallpaper",
  "question": "Under the rules on the card, is Ravi's promise to print the floor plan broken, waived, not triggered or not yet due, rather than kept, as of 23 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q24fc9a8709",
  "kind": "yes/no",
  "text": "Support note: attached to a help desk case\nTopic: the reunion planning\nShared by: Hana\n\nMembers: Femi, Hana, Kai\nChat log (oldest first):\n[23 Jul 2026] Femi: @Hana If the cousin brunch goes ahead, I'll gladly pay the catering company by 25 Jul 2026.\n[26 Jul 2026] Kai: @Femi Ticket's mine, I'll order the cousin t-shirts by 29 Jul 2026.\n[26 Jul 2026] Kai: @Femi Change of plans: I will not order the cousin t-shirts\n[28 Jul 2026] Femi: @Hana I'll buy the name tags by 4 Aug 2026 if the grandparents visit goes ahead.\n[28 Jul 2026] Hana: @Kai Good news, you're let off having to order the cousin t-shirts",
  "question": "According to the rules on the card, does the promise Kai made to order the cousin t-shirts have any status except broken at the end of 2 Aug 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q351adc3ed0",
  "kind": "yes/no",
  "text": "Yo flatmates, Sami shared this chat about the autumn term budget, so chip in.\n\nMembers: Sami, Tess, Rhea, Kofi\nChat log (oldest first):\n[12 Apr 2026] Kofi: @Rhea You can bank on me to collect the parcel from porch by 2026-04-18.\n[12 Apr 2026] Rhea: Ah right, thanks for that.\n[12 Apr 2026] Sami: @Kofi You are released, no requirement to collect the parcel from porch.\n[16 Apr 2026] Tess: @Kofi As long as the move in day is on, I will ring the letting agent by 2026-04-23.\n[17 Apr 2026] Sami: @Kofi Count on me to print the tenancy agreement by 2026-04-25, if the agent inventory walk happens.\n[18 Apr 2026] Kofi: @Rhea Ta-da, I went and did it: collect the parcel from porch!",
  "question": "Would you say Kofi kept the promise to collect the parcel from porch at the end of 2026-04-22?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8781574d07",
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
  "qid": "qa598009344",
  "kind": "choice",
  "text": "Case note: chat about the music library\nExported by: Rhea\n\nMembers: Rhea, Femi, Yuki\nChat log (oldest first):\n[20 May 2026] Rhea: @Yuki Provided the choir festival happens, I will fetch the choir robes by 24 May 2026.\n[21 May 2026] Femi: @Rhea I'll fix the stand microphones by 27 May 2026, promise.\n[22 May 2026] Yuki: Not promising, but I'll try to return the library scores by 29 May 2026.\n[23 May 2026] Yuki: @Femi I will set up the sound desk by 27 May 2026 only if the joint concert happens.\n[23 May 2026] Yuki: @Femi Absolutely, I will return the library scores by 26 May 2026.\n[25 May 2026] Femi: @Yuki You are released, no requirement to return the library scores.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Yuki's pledge to return the library scores sit at the end of 24 May 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Waived",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qd2a1bc35bb",
  "kind": "choice",
  "text": "Shared by Ravi, this freelance thread with a client is about the menu redesign.\n\nMembers: Omar, Oskar, Dara, Ravi\nChat log (oldest first):\n[28 May 2026] Oskar: @Omar Relax, I'll export the logo files by 2 Jun 2026 for sure.\n[31 May 2026] Ravi: @Omar I'll fetch the brand fonts by 4 Jun 2026, provided the print run happens.\n[31 May 2026] Oskar: Sadly, the print run is not going ahead.\n[31 May 2026] Oskar: @Omar Might manage to mail the business cards by 10 Jun 2026, who knows.\n[2 Jun 2026] Oskar: @Omar You can bet I'll mail the business cards by 7 Jun 2026.\n[2 Jun 2026] Oskar: @Omar Would it be fine if I mail the business cards by 11 Jun 2026 instead, yeah?\n[4 Jun 2026] Oskar: @Omar Got myself to export the logo files lol.\n[7 Jun 2026] Ravi: @Oskar Works for me, fine for you to mail the business cards by 11 Jun 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nFollowing the rules set out on the card, what date governs Oskar's commitment to mail the business cards at the end of 12 Jun 2026, once any agreed shift in the date is factored in?",
  "options": [
   "4 Jun 2026",
   "11 Jun 2026",
   "7 Jun 2026"
  ]
 },
 {
  "qid": "qb7d343f8a4",
  "kind": "choice",
  "text": "Project thread between a freelancer and a client on the rebrand package, saved by Mo.\n\nMembers: Tess, Mo\nChat log (oldest first):\n[12 May 2026] Tess: @Mo I'll collect the photo credits by Wednesday, 20 May 2026, providing the gallery install goes ahead.\n[12 May 2026] Mo: @Tess Count on me to send the moodboard files by Friday, 22 May 2026.\n[16 May 2026] Mo: @Tess If the shop fitting is on, I'll definitely sketch the packaging mockup by Thursday, 21 May 2026.\n[17 May 2026] Mo: Quick heads up, the shop fitting is scrapped.\n[17 May 2026] Mo: @Tess Quick question, could I sketch the packaging mockup by Monday, 25 May 2026 instead?\n[18 May 2026] Tess: @Mo Fine by me, you can sketch the packaging mockup by Monday, 25 May 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Mo's undertaking to sketch the packaging mockup hold at the end of Wednesday, 20 May 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q0cddf0cc4b",
  "kind": "yes/no",
  "text": "This shared chat of a family on the garden makeover was saved by Lena for the record.\n\nMembers: Oskar, Lena, Lee\nChat export (date | from | to | message):\n2026-06-29 | Oskar | Lena | I will pick up the grout bag by 3 Jul 2026.\n2026-06-30 | Lena | Lee | Hoping to measure the hallway for shelves by 5 Jul 2026, can't promise.\n2026-07-01 | Lena | Oskar | You can bank on me to measure the hallway for shelves by 4 Jul 2026.\n2026-07-01 | Lena | Oskar | To note: I have managed to measure the hallway for shelves\n2026-07-02 | Lena | Lee | As long as the damp survey inspection is on, I will pay the plumbing invoice by 6 Jul 2026.\n2026-07-04 | Lee | group | Sad to report that the damp survey inspection is off.",
  "question": "Does Lena's promise to measure the hallway for shelves hold up as kept at the end of 1 Jul 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q18a91cf566",
  "kind": "choice",
  "text": "Client thread on the online store move, saved by Sami for the project log.\n\nMembers: Sami, Rhea, Lena\nChat log (oldest first):\n[4 Jun 2026] Lena: @Rhea Guaranteed I'll fix the checkout button by 6 June 2026.\n[4 Jun 2026] Lena: @Rhea Ticked off: fix the checkout button, feels so good\n[6 Jun 2026] Sami: @Rhea As long as the pop up stall is on, I'll set up the email forwarding by 13 June 2026.\n[6 Jun 2026] Sami: Please note the pop up stall will proceed.\n[10 Jun 2026] Lena: @Rhea As long as the stock count is on, I'll update the product photos by 17 June 2026.\n[12 Jun 2026] Sami: @Rhea I regret to say that I shall not set up the email forwarding.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Sami gave to set up the email forwarding have at the end of 13 June 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Not yet due",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q94fe577475",
  "kind": "yes/no",
  "text": "{\"thread_kind\": \"exported conversation\", \"about\": \"the data cleanup\", \"exported_by\": \"Wren\"}\n\nMembers: Wren, Zara, Oskar, Omar\nChat log (oldest first):\n[6 Sep 2026] Wren: @Oskar As long as the penetration test is on, I'll restart the build server by 15 Sep 2026.\n[6 Sep 2026] Omar: @Oskar Ticket's mine, I'll run the security scan by 12 Sep 2026.\n[9 Sep 2026] Zara: @Omar If the code freeze goes ahead, I'll deploy the staging build by 17 Sep 2026.\n[9 Sep 2026] Wren: @Omar Committing to write the release notes by 14 Sep 2026.\n[13 Sep 2026] Omar: @Oskar To note: I have managed to run the security scan\n[15 Sep 2026] Omar: Lovely, the code freeze is definitely happening!",
  "question": "Applying the rules on the card, can Omar's promise to run the security scan be said to have not been broken at the end of 17 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q365a047ae2",
  "kind": "choice",
  "text": "Our flat chat about the old house restoration, shared by Lee for whoever lives here.\n\nMembers: Arlo, Malik, Lee, Ivo\nChat export (date | from | to | message):\n2026-02-05 | Ivo | Lee | Absolutely, I will mend the garden gate by February 12, 2026.\n2026-02-09 | Lee | Malik | Count on me, I'll bleed the attic radiators by February 12, 2026.\n2026-02-10 | Arlo | Lee | I will wash the sash windows by February 13, 2026 only if the roof survey visit happens.\n2026-02-11 | Lee | Malik | Got myself to bleed the attic radiators lol.\n2026-02-11 | Ivo | group | Fab, we are on for the roof survey visit as planned!\n2026-02-13 | Malik | Arlo | Good news, you're let off having to wash the sash windows",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Arlo's pledge to wash the sash windows at the end of February 14, 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q7019210c9c",
  "kind": "choice",
  "text": "Rented flat, shared group chat, copied by Nadia, filed under the garden makeover.\n\nMembers: Omar, Bruno, Nadia\nChat export (date | from | to | message):\n2026-10-23 | Nadia | group | Might be able to pay the plumbing invoice by 1 November 2026, who knows!\n2026-10-25 | Nadia | Omar | Committing to pay the plumbing invoice by 31 October 2026.\n2026-10-26 | Nadia | Omar | I committed to pay the plumbing invoice, can I do that by 6 November 2026 instead?\n2026-10-31 | Omar | Nadia | That suits me, so please pay the plumbing invoice by 6 November 2026 instead.\n2026-11-03 | Bruno | Omar | Count on me to pick up the grout bag by 8 November 2026.\n2026-11-06 | Omar | Bruno | I promise to sweep the dust from stairs by 9 November 2026 if the mortgage valuation visit is on.\n2026-11-08 | Nadia | group | Really pleased to say the mortgage valuation visit will go ahead!\n2026-11-08 | Bruno | Omar | Ta-da, I went and did it: pick up the grout bag!",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIf the chat is checked at the end of 1 November 2026, which date marks the deadline for Nadia to pay the plumbing invoice, with agreed date changes included?",
  "options": [
   "31 October 2026",
   "6 November 2026",
   "8 November 2026"
  ]
 },
 {
  "qid": "qcf5edc9975",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the menu redesign\nFrom Malik, the thread below is passed on in its original form.\n\nMembers: Malik, Jonas\nChat log (oldest first):\n[26 Aug 2026] Jonas: I'll try to collect the photo credits by 2 September 2026, can't promise!\n[27 Aug 2026] Malik: @Jonas You can bank on me to check the poster proofs by 2 September 2026.\n[28 Aug 2026] Jonas: @Malik As long as the gallery install is on, I will collect the photo credits by 1 September 2026.\n[30 Aug 2026] Malik: Great news, the gallery install is on!\n[30 Aug 2026] Jonas: @Malik Forget it, you won't need to check the poster proofs\n[1 Sep 2026] Malik: @Jonas No need to collect the photo credits, I'm letting you off",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Jonas's undertaking to collect the photo credits hold at the end of 3 September 2026?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q2465d3fb0f",
  "kind": "yes/no",
  "text": "Wren forwarded this support chat about the sponsor search.\n\nMembers: Rhea, Wren, Leila\nChat log (oldest first):\n[24 Apr 2026] Leila: @Wren Only if the bike check is on, I will collect the timing tags by 1 May 2026.\n[25 Apr 2026] Leila: @Rhea I'll print the route cards by 29 Apr 2026 as long as the hill climb is on.\n[25 Apr 2026] Wren: @Leila Relax, I'll pump the spare tyres by 2 May 2026, promise.\n[26 Apr 2026] Rhea: @Leila I own this, I'll wash the club jerseys by 29 Apr 2026.\n[28 Apr 2026] Rhea: We are dropping the hill climb from the list.\n[2 May 2026] Leila: @Wren No worries, you don't need to pump the spare tyres",
  "question": "Applying the rules on the card, has Wren kept the promise to pump the spare tyres as of 7 May 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qee519d827b",
  "kind": "yes/no",
  "text": "{\"chat\": \"exported\", \"about\": \"the peer review\", \"saved_by\": \"Sami\", \"medium\": \"text\"}\n\nMembers: Sami, Lena, Ines\nChat log (oldest first):\n[5 Oct 2026] Lena: @Sami Got it, I'll return the library books by Friday, October 9, 2026 for sure.\n[6 Oct 2026] Lena: @Ines Count on me to submit the ethics application by Wednesday, October 14, 2026 if the conference trip is on.\n[7 Oct 2026] Sami: @Lena I will order the reagent kit by Tuesday, October 13, 2026 only if the grant panel happens.\n[9 Oct 2026] Lena: Quick heads up, the grant panel is scrapped.\n[13 Oct 2026] Sami: @Lena Quick question, could I order the reagent kit by Saturday, October 17, 2026 instead?\n[13 Oct 2026] Lena: @Sami No new date, so please order the reagent kit by the date given.",
  "question": "Going by the card's rules, does Sami keep the promise to order the reagent kit at the end of Saturday, October 17, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9feeb104e5",
  "kind": "yes/no",
  "text": "Casual chat for the flat, saved by Leila, and it covers the big house plan.\n\nMembers: Leila, Ana\nChat log (oldest first):\n[27 Jun 2026] Leila: @Ana Only if the ghost tour is on, I will replace the hallway bulbs by 6 July 2026.\n[27 Jun 2026] Leila: @Ana Provided the roof survey visit happens, I'll bleed the attic radiators by 6 July 2026.\n[27 Jun 2026] Ana: @Leila You can bank on me to defrost the old fridge by 1 July 2026.\n[30 Jun 2026] Ana: @Leila Is it all right if I defrost the old fridge by 4 July 2026 instead?\n[30 Jun 2026] Ana: @Leila Mum, I did defrost the old fridge, haha.",
  "question": "Does the card's rule set show that Ana has not kept the promise to defrost the old fridge at the end of 30 June 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q106cb96735",
  "kind": "choice",
  "text": "{\"thread\": \"the website relaunch\", \"exported_by\": \"Ines\", \"shape\": \"group chat\"}\n\nMembers: Ines, Kofi, Greta, Elif\nChat log (oldest first):\n[16 Sep 2026] Kofi: @Ines As long as the influencer call is on, I will book the photo studio by 22 Sep 2026.\n[17 Sep 2026] Elif: @Kofi I'll set up the analytics dashboard by 22 Sep 2026, provided the product launch happens.\n[17 Sep 2026] Elif: Fab, we are on for the product launch as planned!\n[19 Sep 2026] Greta: @Ines I will print the event banners by 24 Sep 2026.\n[21 Sep 2026] Elif: @Greta Ah, no stress, no need for you to print the event banners\n[23 Sep 2026] Kofi: @Elif Relax, I'll fetch the campaign budget sheet by 1 Oct 2026, promise.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Greta made to print the event banners, what state is it in at the end of 21 Sep 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Broken",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q60a50a3b66",
  "kind": "choice",
  "text": "Shared with the committee, this export of the music library came from Leila.\n\nMembers: Sami, Leila, Wren\nChat log (oldest first):\n[29 Jul 2026] Wren: @Sami Ticket's mine, I'll book the rehearsal room by 2026-08-01.\n[29 Jul 2026] Wren: @Sami Change of plans: I will not book the rehearsal room\n[29 Jul 2026] Sami: @Wren No worries, you don't need to book the rehearsal room\n[29 Jul 2026] Sami: @Wren I'll set up the sound desk by 2026-08-07, providing the joint concert goes ahead.\n[31 Jul 2026] Wren: Sorry, the joint concert is off.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Wren made to book the rehearsal room at the end of 2026-08-02?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q3b0d2f67b8",
  "kind": "yes/no",
  "text": "Here is the thread on the flatmate contract terms, posted by Rhea for the house.\n\nMembers: Oskar, Zara, Hana, Rhea\nChat log (oldest first):\n[20 Feb 2026] Hana: @Rhea I'll scan the council tax letter by 2026-02-26 if the move in day goes ahead.\n[22 Feb 2026] Hana: @Oskar Count on me to store the spare bike by 2026-03-01, if the freshers welcome night happens.\n[22 Feb 2026] Oskar: @Rhea Ticket's mine, I'll photograph the bathroom mould by 2026-03-02.\n[24 Feb 2026] Oskar: @Rhea I committed to photograph the bathroom mould, can I do that by 2026-03-06 instead?\n[26 Feb 2026] Oskar: @Rhea Change of plans: I will not photograph the bathroom mould\n[28 Feb 2026] Zara: Sadly, the freshers welcome night is not going ahead.",
  "question": "Under the rules on the card, is Oskar's promise to photograph the bathroom mould broken, waived, not triggered or not yet due, rather than kept, as of 2026-02-26?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3cbb8e2db0",
  "kind": "yes/no",
  "text": "Shared by Kai, this freelance thread with a client is about the campaign edit.\n\nMembers: Kai, Bruno, Omar, Malik\nChat export (date | from | to | message):\n2026-03-20 | Omar | Bruno | I promise to export the subtitle files by 24 March 2026.\n2026-03-20 | Malik | Kai | If the client screening goes ahead, I'll send the colour notes by 26 March 2026.\n2026-03-21 | Omar | group | Brilliant news everyone, the client screening is a go!\n2026-03-23 | Bruno | Omar | As long as the festival premiere is on, I will send the timeline export by 25 March 2026.\n2026-03-23 | Omar | Malik | Got it, I'll label the clip folders by 31 March 2026 for sure.\n2026-03-25 | Omar | Malik | I'm withdrawing my promise to label the clip folders",
  "question": "According to the rules on the card, has Omar broken the promise to label the clip folders at the end of 26 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q09a1305e47",
  "kind": "choice",
  "text": "Team channel: the website relaunch\nShared by Ana.\n\nMembers: Ana, Femi, Mo, Tess\nChat export (date | from | to | message):\n2026-03-07 | Ana | Tess | It's on me to book the photo studio by 13 March 2026.\n2026-03-08 | Mo | Tess | As long as the brand photo shoot is on, I will set up the analytics dashboard by 15 March 2026.\n2026-03-09 | Tess | Femi | Got it, I'll draft the press release by 14 March 2026 for sure.\n2026-03-12 | Ana | Femi | Provided the product launch happens, I'll print the event banners by 18 March 2026.\n2026-03-14 | Tess | Femi | To my relief, I managed to draft the press release.\n2026-03-17 | Ana | group | Sorry, the product launch is off.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status does the chat show for the promise Tess made to draft the press release at the end of 14 March 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Kept",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "q531540c066",
  "kind": "yes/no",
  "text": "Volunteers, Leila shared this with you about the playground project.\n\nMembers: Bruno, Leila, Hana\nChat export (date | from | to | message):\n2026-05-26 | Bruno | Hana | I will make sure to fetch the tea urn by 5 June 2026.\n2026-05-27 | Leila | group | Fingers crossed I can wrap the prize hampers by 7 June 2026.\n2026-05-28 | Leila | Hana | Relax, I'll wrap the prize hampers by 4 June 2026, promise.\n2026-05-30 | Leila | Hana | Only if the governors meeting is on, I will count the donation boxes by 3 June 2026.\n2026-05-30 | Leila | group | Sadly, the governors meeting is not going ahead.\n2026-06-04 | Leila | Hana | For the record: I was able to wrap the prize hampers",
  "question": "Does the card classify Leila's promise to wrap the prize hampers as kept, instead of broken, waived, not triggered or not yet due, on 5 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1a35e888d8",
  "kind": "choice",
  "text": "Read up on the speed bump plan, flatmates, as Lee exported it.\n\nMembers: Zara, Lee, Sami\nChat log (oldest first):\n[24 Sep 2026] Lee: Wish me luck, hoping to walk the old spaniel by 4 Oct 2026.\n[25 Sep 2026] Sami: @Lee If the speed camera survey is on, I'll definitely lock the side gate by 27 Sep 2026.\n[26 Sep 2026] Lee: @Zara I promise to walk the old spaniel by 3 Oct 2026.\n[26 Sep 2026] Lee: @Zara I'll feed the cat across the road by 5 Oct 2026 if the bonfire night goes ahead.\n[28 Sep 2026] Sami: @Lee Don't sweat it, there's no need to walk the old spaniel\n[3 Oct 2026] Lee: @Zara Guess what, I managed to walk the old spaniel!",
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
  "qid": "q0e468ad872",
  "kind": "choice",
  "text": "Ana shared this so the family follows the home adaptations.\n\nMembers: Lee, Ana, Femi\nChat log (oldest first):\n[6 Aug 2026] Ana: @Femi If the carer handover is on, I'll definitely wash the bed linen by 9 August 2026.\n[7 Aug 2026] Lee: On track for the carer handover to happen as planned.\n[7 Aug 2026] Ana: @Femi Mate, I promised, may I wash the bed linen by 12 August 2026 instead?\n[7 Aug 2026] Femi: @Ana Nah, that deadline counts, mate, so please wash the bed linen!\n[7 Aug 2026] Lee: @Ana I will make sure to book the clinic transport by 15 August 2026.\n[8 Aug 2026] Ana: @Femi Update on my side: I will not wash the bed linen, sorry.\n[12 Aug 2026] Lee: @Ana Mind giving me until 18 August 2026 to book the clinic transport?\n[13 Aug 2026] Ana: @Lee We are holding the date on record, so book the clinic transport by it.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules, when is the date by which Ana has to wash the bed linen at the end of 24 August 2026, allowing for any agreed change?",
  "options": [
   "15 August 2026",
   "9 August 2026",
   "12 August 2026"
  ]
 },
 {
  "qid": "q3a48aed375",
  "kind": "choice",
  "text": "Channel: work team chat\nTopic: the website relaunch\nExported by Ines.\n\nMembers: Ines, Kofi, Greta, Elif\nChat export (date | from | to | message):\n2026-09-16 | Kofi | Ines | As long as the influencer call is on, I will book the photo studio by 22 Sep 2026.\n2026-09-17 | Elif | Kofi | I'll set up the analytics dashboard by 22 Sep 2026, provided the product launch happens.\n2026-09-17 | Elif | group | Fab, we are on for the product launch as planned!\n2026-09-19 | Greta | Ines | I will print the event banners by 24 Sep 2026.\n2026-09-21 | Elif | Greta | Ah, no stress, no need for you to print the event banners\n2026-09-23 | Kofi | Elif | Relax, I'll fetch the campaign budget sheet by 1 Oct 2026, promise.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Greta made to print the event banners, what state is it in at the end of 21 Sep 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Broken",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q8339b984bd",
  "kind": "yes/no",
  "text": "Ravi shared this so the music library is easy to follow for the volunteers.\n\nMembers: Elif, Ravi, Kai\nChat log (oldest first):\n[13 Apr 2026] Kai: Might be able to return the library scores by 22 April 2026, who knows!\n[15 Apr 2026] Kai: @Ravi I promise to return the library scores by 20 April 2026.\n[18 Apr 2026] Kai: @Ravi I will fix the stand microphones by 26 April 2026 only if the choir festival happens.\n[19 Apr 2026] Ravi: @Kai Count on me, I'll fetch the choir robes by 27 April 2026.\n[20 Apr 2026] Kai: @Ravi Gutted to say I won't return the library scores, sorry team\n[21 Apr 2026] Ravi: Brilliant news everyone, the choir festival is a go!",
  "question": "Does the card classify Kai's promise to return the library scores as kept, instead of broken, waived, not triggered or not yet due, on 24 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5a2839f418",
  "kind": "yes/no",
  "text": "{\"source\": \"saved thread\", \"about\": \"the new term plans\", \"owner\": \"Ines\", \"kind\": \"chat export\"}\n\nMembers: Mo, Leila, Bruno, Ines\nChat export (date | from | to | message):\n2026-10-07 | Mo | Ines | Committing to print the raffle tickets by 15 Oct 2026.\n2026-10-08 | Bruno | Mo | Please don't feel you have to print the raffle tickets\n2026-10-08 | Mo | Ines | Guess who managed to print the raffle tickets, go team!\n2026-10-11 | Ines | Bruno | Only if the reading festival is on, I will book the school hall by 17 Oct 2026.\n2026-10-13 | Mo | group | Team, the reading festival is not happening.",
  "question": "Does the card classify Mo's promise to print the raffle tickets as broken, waived, not triggered or not yet due, rather than kept, on 11 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q706907e278",
  "kind": "yes/no",
  "text": "Volunteer chat export. Saved by Priya, it covers the new term plans.\n\nMembers: Omar, Priya, Ivo\nChat export (date | from | to | message):\n2026-04-06 | Priya | Ivo | Relax, I'll collect the bake sale tins by 15 Apr 2026, promise.\n2026-04-08 | Ivo | Omar | Relax, I'll count the donation boxes by 13 Apr 2026 for sure.\n2026-04-09 | Priya | Ivo | If the reading festival goes ahead, I'll return the borrowed trestle tables by 16 Apr 2026.\n2026-04-12 | Ivo | Omar | I have to take back my promise to count the donation boxes.\n2026-04-14 | Priya | group | Update: the reading festival is going ahead as planned.\n2026-04-18 | Ivo | group | Hey, any luck with trying to return the borrowed trestle tables?",
  "question": "At the end of 18 Apr 2026, has Priya broken its promise to return the borrowed trestle tables?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q538dc68689",
  "kind": "yes/no",
  "text": "Case note: chat about the allotment expansion\nExported by: Lena\n\nMembers: Elif, Sami, Lena, Priya\nChat log (oldest first):\n[3 Jul 2026] Elif: @Sami See if I can water the allotment beds by Tuesday, July 7, 2026.\n[5 Jul 2026] Elif: @Priya You can bet I'll water the allotment beds by Friday, July 10, 2026.\n[6 Jul 2026] Sami: @Elif I will make sure to deliver the surplus runner beans by Wednesday, July 8, 2026.\n[8 Jul 2026] Sami: @Elif If the allotment site visit is on, I'll definitely dig the potato patch by Sunday, July 12, 2026.\n[8 Jul 2026] Sami: Sad to report that the allotment site visit is off.\n[9 Jul 2026] Lena: @Elif Good news, you're let off having to water the allotment beds",
  "question": "Is Elif's promise to water the allotment beds kept on Friday, July 10, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qce4059d8d1",
  "kind": "choice",
  "text": "Freelance project export\nFrom Lee, covering the campaign edit with the client.\n\nMembers: Ravi, Lee, Greta, Rhea\nChat export (date | from | to | message):\n2026-04-08 | Lee | Ravi | Ticket's mine, I'll send the timeline export by April 16, 2026.\n2026-04-10 | Rhea | Lee | Promise to send the colour notes by April 14, 2026 if the client screening goes ahead.\n2026-04-11 | Lee | group | Quick heads up, the client screening is scrapped.\n2026-04-14 | Lee | Ravi | I have to take back my promise to send the timeline export.\n2026-04-16 | Rhea | Lee | Don't sweat it, there's no need to send the timeline export",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Lee's commitment to send the timeline export is in what status at the end of April 20, 2026?",
  "options": [
   "Waived",
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "qb502fc5aa5",
  "kind": "yes/no",
  "text": "Thread filed under support\nAbout the garden makeover, saved by Yuki.\n\nMembers: Mo, Yuki, Tess, Kai\nChat export (date | from | to | message):\n2026-03-24 | Tess | Kai | Relax, I'll hang the new curtain rail by 29 March 2026 for sure.\n2026-03-27 | Mo | Tess | Good news, you're let off having to hang the new curtain rail\n2026-03-28 | Tess | Kai | To note: I have managed to hang the new curtain rail\n2026-03-29 | Kai | Yuki | If the mortgage valuation visit goes ahead, I'll return the tile cutter by 6 April 2026.\n2026-04-02 | Yuki | group | Afraid the mortgage valuation visit is called off.",
  "question": "On 31 March 2026 itself, has Tess not kept the promise to hang the new curtain rail?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q080d617a92",
  "kind": "choice",
  "text": "{\"thread_kind\": \"exported conversation\", \"about\": \"the travel plans\", \"exported_by\": \"Ines\"}\n\nMembers: Kai, Ines, Jonas\nChat export (date | from | to | message):\n2026-10-03 | Jonas | Kai | I will make sure to return the rental car keys by Friday, October 9, 2026.\n2026-10-04 | Jonas | Ines | Provided the ferry crossing happens, I'll print the boarding passes by Wednesday, October 7, 2026.\n2026-10-04 | Ines | group | Lovely, the ferry crossing is definitely happening!\n2026-10-05 | Jonas | Ines | Any chance I can print the boarding passes by Monday, October 12, 2026 instead?\n2026-10-05 | Kai | group | Update on your plan to print the boarding passes?\n2026-10-06 | Kai | Jonas | You don't have to return the rental car keys at all",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Jonas's promise to print the boarding passes at the end of Thursday, October 8, 2026?",
  "options": [
   "Kept",
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "q850754215b",
  "kind": "choice",
  "text": "Saved by Tomas, this is the household group chat about the street watch scheme, copied in full.\n\nMembers: Tomas, Nadia, Kai\nChat log (oldest first):\n[3 Jun 2026] Kai: @Tomas I'll share the garden hose by 9 June 2026, provided the bonfire night happens.\n[4 Jun 2026] Nadia: I'll see if I can feed the cat across the road by 12 June 2026.\n[5 Jun 2026] Nadia: @Kai I own this, I'll feed the cat across the road by 10 June 2026.\n[6 Jun 2026] Nadia: @Kai On my action item, may I feed the cat across the road by 15 June 2026 instead?\n[8 Jun 2026] Tomas: @Kai Count on me to sweep the pavement outside by 14 June 2026 if the parking permit visit is on.\n[10 Jun 2026] Nadia: @Kai To note: I have managed to feed the cat across the road",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Nadia's undertaking to feed the cat across the road hold at the end of 9 June 2026?",
  "options": [
   "Waived",
   "Broken",
   "Not yet due",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "qa5083e00fe",
  "kind": "choice",
  "text": "Bruno forwarded this for the committee as we dig in on the training plan.\n\nMembers: Yuki, Bruno, Ana\nChat log (oldest first):\n[21 Jun 2026] Bruno: @Ana If the club sportive is on, I'll definitely set up the feed stop by 29 June 2026.\n[22 Jun 2026] Ana: @Bruno I'll collect the timing tags by 29 June 2026, provided the swap meet happens.\n[22 Jun 2026] Bruno: @Yuki I'll fetch the bike stand by 28 June 2026, promise.\n[22 Jun 2026] Yuki: @Bruno Relax, I'll service the tandem bike by 29 June 2026, promise.\n[24 Jun 2026] Bruno: @Yuki Might I ask whether I could fetch the bike stand by 30 June 2026 instead?\n[25 Jun 2026] Yuki: @Bruno To note: I have managed to service the tandem bike\n[26 Jun 2026] Ana: @Bruno Yes, you have the green light to fetch the bike stand by 30 June 2026.\n[2 Jul 2026] Bruno: @Yuki Quick report: I've managed to fetch the bike stand",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIf the chat is checked at the end of 6 July 2026, which date marks the deadline for Bruno to fetch the bike stand, with agreed date changes included?",
  "options": [
   "28 June 2026",
   "30 June 2026",
   "29 June 2026"
  ]
 },
 {
  "qid": "q635c8ed158",
  "kind": "choice",
  "text": "Flat chat, exported by Priya for the household.\nSubject: the balcony garden project\n\nMembers: Oskar, Nadia, Yuki, Priya\nChat log (oldest first):\n[7 Aug 2026] Nadia: I'll try to email the leak photos by 12 August 2026, can't promise!\n[7 Aug 2026] Priya: @Oskar Count on me to read the meter readings by 12 August 2026.\n[7 Aug 2026] Priya: @Oskar Can I read the meter readings by 17 August 2026 instead? I did promise, sorry.\n[8 Aug 2026] Nadia: @Yuki As long as the flat viewing day is on, I'll email the leak photos by 13 August 2026.\n[10 Aug 2026] Priya: Lovely, the flat viewing day is definitely happening!\n[10 Aug 2026] Oskar: @Priya Of course, it is fine for you to read the meter readings by 17 August 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status is Nadia's promise to email the leak photos at the end of 10 August 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "qfcd8bcc32b",
  "kind": "yes/no",
  "text": "We are getting ready for the family photo book, and Lena shared this chat with us.\n\nMembers: Lena, Leila, Rhea\nChat export (date | from | to | message):\n2026-05-28 | Lena | Leila | I promise to pick up the school bags by Tuesday, 2 June 2026.\n2026-05-29 | Leila | Rhea | Absolutely, I will walk the dog by Thursday, 4 June 2026.\n2026-05-30 | Lena | Rhea | I'll be sure to mend the kite string by Monday, 8 June 2026.\n2026-05-31 | Rhea | Lena | Lovely, I'll pack the picnic basket by Saturday, 6 June 2026 if the sleepover weekend is on.\n2026-06-03 | Lena | group | Update: the sleepover weekend is going ahead as planned.",
  "question": "Does Rhea's promise to pack the picnic basket hold up as kept at the end of Sunday, 7 June 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd03ae74aba",
  "kind": "yes/no",
  "text": "Household group messages for the summer visits were passed along by Ines.\n\nMembers: Arlo, Ines, Malik, Kai\nChat log (oldest first):\n[20 Jan 2026] Ines: @Malik Count on me to pack the picnic basket by 23 January 2026.\n[23 Jan 2026] Arlo: @Kai I assure you I'll fetch the craft box by 30 January 2026 if the storytime session is on.\n[24 Jan 2026] Ines: Update on your plan to fetch the craft box?\n[28 Jan 2026] Ines: Great news, the storytime session is on!\n[29 Jan 2026] Arlo: @Kai I committed to fetch the craft box, can I do that by 3 February 2026 instead?\n[29 Jan 2026] Ines: @Arlo No worries, you don't need to fetch the craft box",
  "question": "Applying the card's rules, does Arlo's promise to fetch the craft box count as kept, rather than broken, waived, not triggered or not yet due, as of 29 January 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe587338470",
  "kind": "yes/no",
  "text": "A family chat export on the house rules debate, shared out by Tess.\n\nMembers: Elif, Tess\nChat log (oldest first):\n[30 Jun 2026] Elif: @Tess Count on me, I'll clear the kitchen sink by 2026-07-03.\n[30 Jun 2026] Tess: @Elif Hoping to find the loft ladder by 2026-07-09, can't promise.\n[1 Jul 2026] Tess: @Elif I'll find the loft ladder by 2026-07-08, provided the house viewing happens.\n[4 Jul 2026] Elif: @Tess Relax, I'll tidy the boot room by 2026-07-06 for sure.\n[7 Jul 2026] Elif: Please note the house viewing will proceed.\n[11 Jul 2026] Tess: @Elif To note: I have managed to find the loft ladder",
  "question": "On 2026-07-12 itself, has Tess not kept the promise to find the loft ladder?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q95ce4eaaa2",
  "kind": "choice",
  "text": "Posted by Priya from the work channel: the office refit.\n\nMembers: Priya, Kai, Ravi\nChat log (oldest first):\n[7 Feb 2026] Priya: @Ravi Got it, I'll fetch the parking permits by 13 Feb 2026 for sure.\n[8 Feb 2026] Kai: @Priya Guaranteed I'll book the boardroom by 17 Feb 2026.\n[12 Feb 2026] Priya: @Ravi Mind giving me until 15 Feb 2026 to fetch the parking permits?\n[12 Feb 2026] Ravi: @Priya Of course, it is fine for you to fetch the parking permits by 15 Feb 2026.\n[13 Feb 2026] Kai: @Priya Nobody needs you to fetch the parking permits, that's that\n[13 Feb 2026] Kai: @Priya As long as the team lunch is on, I'll order the office stationery by 18 Feb 2026.\n[15 Feb 2026] Kai: Fab, we are on for the team lunch as planned!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, what is the deadline for Priya to fetch the parking permits at the end of 12 Feb 2026, with any agreed change of date counted?",
  "options": [
   "13 Feb 2026",
   "17 Feb 2026",
   "15 Feb 2026"
  ]
 },
 {
  "qid": "qf166a98d6d",
  "kind": "choice",
  "text": "Subject: export of the group chat on the online store move\nHere is the chat as saved by Kai, pasted below.\n\nMembers: Lena, Jonas, Kai, Femi\nChat log (oldest first):\n[25 Jun 2026] Lena: @Jonas Lovely, I'll print the packing slips by 3 Jul 2026 if the stock count is on.\n[25 Jun 2026] Jonas: Got it, cheers!\n[25 Jun 2026] Lena: Team, the stock count stays on as booked.\n[27 Jun 2026] Kai: @Lena Ah, no stress, no need for you to print the packing slips\n[30 Jun 2026] Kai: @Jonas Lovely, I'll set up the email forwarding by 2 Jul 2026 for sure.\n[8 Jul 2026] Lena: @Jonas Guess who managed to print the packing slips, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Lena made to print the packing slips at the end of 6 Jul 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Broken",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qa21b9b7e2c",
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
  "qid": "q69b1eaaecd",
  "kind": "yes/no",
  "text": "Subject: copy of a chat on the holiday catalogue\nPassing this along, with the chat text under it, from Ines.\n\nMembers: Sami, Ana, Ines, Rhea\nChat log (oldest first):\n[9 Jan 2026] Ines: @Rhea As long as the stock count is on, I'll set up the email forwarding by 12 Jan 2026.\n[9 Jan 2026] Ines: @Rhea Ticket's mine, I'll renew the hosting plan by 14 Jan 2026.\n[10 Jan 2026] Ana: On track for the stock count to happen as planned.\n[11 Jan 2026] Rhea: @Ines Count on me to fetch the domain login by 20 Jan 2026 if the courier pickup is on.\n[13 Jan 2026] Ana: @Ines Please don't feel you have to renew the hosting plan\n[14 Jan 2026] Ines: @Rhea Mum, I did renew the hosting plan, haha.",
  "question": "Would you say Ines kept the promise to renew the hosting plan at the end of 15 Jan 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf1fc55def0",
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
  "qid": "q7dd0d94d75",
  "kind": "yes/no",
  "text": "Case note: chat about the online store move\nExported by: Lena\n\nMembers: Lena, Omar, Dara\nChat export (date | from | to | message):\n2026-10-28 | Lena | Omar | Promise to send the stock spreadsheet by 5 November 2026 if the stock count goes ahead.\n2026-10-28 | Omar | Dara | It's on me to set up the email forwarding by 4 November 2026.\n2026-10-28 | Omar | Dara | I have to take back my promise to set up the email forwarding.\n2026-10-30 | Omar | Dara | Relax, I'll fetch the domain login by 5 November 2026, promise.\n2026-10-31 | Omar | group | On track for the stock count to happen as planned.",
  "question": "Per the rules on the card, at the end of 29 October 2026, has the promise Omar made to set up the email forwarding been broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9970a35b9f",
  "kind": "choice",
  "text": "Volunteers, here is the ground upgrade chat that Arlo forwarded to us.\n\nMembers: Arlo, Lena, Greta\nChat log (oldest first):\n[25 Jul 2026] Greta: @Lena Relax, I'll fetch the medical bag by August 4, 2026, promise.\n[26 Jul 2026] Lena: @Greta As long as the pre-season friendly is on, I'll set up the corner flags by August 3, 2026.\n[28 Jul 2026] Greta: Team, the pre-season friendly is not happening.\n[28 Jul 2026] Lena: @Greta I committed to set up the corner flags, can I do that by August 9, 2026 instead?\n[3 Aug 2026] Greta: @Lena Yes, happy for you to set up the corner flags by August 9, 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhere does Lena stand on the promise to set up the corner flags at the end of August 2, 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Waived",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "q20182f9694",
  "kind": "yes/no",
  "text": "Saved by Jonas: a freelancer's exchange with a client over the campaign edit.\n\nMembers: Greta, Jonas, Bruno, Kai\nChat export (date | from | to | message):\n2026-04-07 | Greta | Jonas | Got it, I'll export the subtitle files by 10 April 2026 for sure.\n2026-04-08 | Jonas | Greta | It's on me to record the voice over by 15 April 2026.\n2026-04-09 | Kai | Bruno | I'll back up the project drives by 11 April 2026, providing the shoot day goes ahead.\n2026-04-09 | Bruno | group | We are dropping the shoot day from the list.\n2026-04-10 | Kai | Greta | Provided the grading session happens, I'll order the stock music licence by 13 April 2026.\n2026-04-12 | Jonas | Greta | Ticked off: record the voice over, feels so good",
  "question": "According to the rules on the card, has Jonas broken the promise to record the voice over at the end of 12 April 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
