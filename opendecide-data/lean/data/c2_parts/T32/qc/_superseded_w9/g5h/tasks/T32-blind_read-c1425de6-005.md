# G5-H blind read T32-blind_read-c1425de6-005 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T32/qc/g5h/answers/T32-blind_read-c1425de6-005.json

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
  "qid": "qe909506d50",
  "kind": "choice",
  "text": "Freelancer and client exchange about the documentary cut, saved by Hana.\n\nMembers: Jonas, Hana, Kai, Oskar\nChat export (date | from | to | message):\n2026-05-13 | Oskar | Kai | You can bet I'll send the colour notes by 2026-05-20.\n2026-05-13 | Oskar | Kai | Is it all right if I send the colour notes by 2026-05-25 instead?\n2026-05-14 | Kai | Oskar | Yes, you're welcome to send the colour notes by 2026-05-25 instead.\n2026-05-15 | Oskar | Kai | As long as the voiceover session is on, I will back up the project drives by 2026-05-22.\n2026-05-21 | Kai | group | Quick heads up, the voiceover session is scrapped.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Oskar made to back up the project drives at the end of 2026-05-26?",
  "options": [
   "Not triggered",
   "Broken",
   "Not yet due",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qc04c14213d",
  "kind": "yes/no",
  "text": "Thread filed under support\nAbout the garden makeover, saved by Yuki.\n\nMembers: Mo, Yuki, Tess, Kai\nChat export (date | from | to | message):\n2026-03-24 | Tess | Kai | Relax, I'll hang the new curtain rail by 29 March 2026 for sure.\n2026-03-27 | Mo | Tess | Good news, you're let off having to hang the new curtain rail\n2026-03-28 | Tess | Kai | To note: I have managed to hang the new curtain rail\n2026-03-29 | Kai | Yuki | If the mortgage valuation visit goes ahead, I'll return the tile cutter by 6 April 2026.\n2026-04-02 | Yuki | group | Afraid the mortgage valuation visit is called off.",
  "question": "By the end of 31 March 2026, has Tess kept the promise to hang the new curtain rail?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q72a2bd5b40",
  "kind": "yes/no",
  "text": "Freelance chat about the gallery show\nThe client side, saved by Jonas.\n\nMembers: Bruno, Malik, Jonas, Ivo\nChat log (oldest first):\n[19 Feb 2026] Bruno: @Jonas I will check the poster proofs by 23 February 2026 only if the brand review call happens.\n[21 Feb 2026] Ivo: @Bruno Committing to mail the business cards by 28 February 2026.\n[22 Feb 2026] Jonas: @Bruno Promise to export the logo files by 2 March 2026 if the sign reveal goes ahead.\n[24 Feb 2026] Ivo: @Bruno Any chance I can mail the business cards by 3 March 2026 instead?\n[25 Feb 2026] Malik: @Ivo I'll collect the photo credits by 2 March 2026 as long as the print run is on.\n[28 Feb 2026] Malik: @Ivo No worries, you don't need to mail the business cards",
  "question": "Is the promise to mail the business cards kept by Ivo as of 1 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q913dd34fec",
  "kind": "choice",
  "text": "Here we plan the reunion planning together, and Oskar saved this for the family.\n\nMembers: Priya, Oskar\nChat log (oldest first):\n[3 Sep 2026] Oskar: @Priya I will collect the old photo prints by 11 September 2026.\n[5 Sep 2026] Oskar: @Priya Only if the grandparents visit is on, I will fetch the speaker system by 12 September 2026.\n[7 Sep 2026] Oskar: @Priya Is it all right if I collect the old photo prints by 16 September 2026 instead?\n[9 Sep 2026] Oskar: We are dropping the grandparents visit from the list.\n[9 Sep 2026] Priya: @Oskar No change, you need to collect the old photo prints by the original date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Oskar's commitment to collect the old photo prints at the end of 15 September 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q15c1c2254b",
  "kind": "yes/no",
  "text": "Work conversation on the website relaunch, saved as a file by Rhea.\n\nMembers: Priya, Rhea, Arlo\nChat export (date | from | to | message):\n2026-06-20 | Rhea | Arlo | If the webinar rehearsal is on, I'll definitely book the photo studio by 23 June 2026.\n2026-06-20 | Priya | Arlo | Ticket's mine, I'll print the event banners by 24 June 2026.\n2026-06-21 | Arlo | Rhea | Relax, I'll fix the landing page headline by 25 June 2026, promise.\n2026-06-21 | Arlo | Rhea | Scratch what I said, I won't fix the landing page headline.\n2026-06-22 | Priya | group | Really pleased to say the webinar rehearsal will go ahead!\n2026-06-25 | Rhea | Arlo | To note: I have managed to book the photo studio",
  "question": "Under the rules on the card, is the promise Rhea made to book the photo studio in a status other than broken at the end of 23 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q35a5be5bbe",
  "kind": "yes/no",
  "text": "Written exchange with the letting agent, covering the tenancy renewal talks, which Zara copied into the file.\n\nMembers: Zara, Oskar, Priya\nChat log (oldest first):\n[26 Mar 2026] Zara: @Oskar I promise to wipe the cooker hood by 4 April 2026.\n[27 Mar 2026] Zara: @Oskar Provided the boiler annual check happens, I'll bring the step stool by 30 March 2026.\n[28 Mar 2026] Priya: On track for the boiler annual check to happen as planned.\n[29 Mar 2026] Zara: @Oskar Lovely, I'll remove the bathroom shelf by 5 April 2026 for sure.\n[30 Mar 2026] Zara: @Oskar To my relief, I managed to remove the bathroom shelf.\n[31 Mar 2026] Priya: Any news on whether you can remove the bathroom shelf, lovely?",
  "question": "On the card, was Zara's promise to remove the bathroom shelf kept, rather than broken, waived, not triggered or not yet due, at the end of 2 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q74246de7c8",
  "kind": "yes/no",
  "text": "Saved by Jonas: a freelancer's exchange with a client over the campaign edit.\n\nMembers: Greta, Jonas, Bruno, Kai\nChat export (date | from | to | message):\n2026-04-07 | Greta | Jonas | Got it, I'll export the subtitle files by 10 April 2026 for sure.\n2026-04-08 | Jonas | Greta | It's on me to record the voice over by 15 April 2026.\n2026-04-09 | Kai | Bruno | I'll back up the project drives by 11 April 2026, providing the shoot day goes ahead.\n2026-04-09 | Bruno | group | We are dropping the shoot day from the list.\n2026-04-10 | Kai | Greta | Provided the grading session happens, I'll order the stock music licence by 13 April 2026.\n2026-04-12 | Jonas | Greta | Ticked off: record the voice over, feels so good",
  "question": "According to the rules on the card, has Jonas broken the promise to record the voice over at the end of 12 April 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q40e9976a9e",
  "kind": "yes/no",
  "text": "Rhea shared this channel export covering the data cleanup for the team.\n\nMembers: Nadia, Tess, Hana, Rhea\nChat log (oldest first):\n[4 Mar 2026] Tess: @Nadia I will make sure to restart the build server by March 13, 2026.\n[7 Mar 2026] Hana: @Nadia I'll try to merge the login branch by March 14, 2026, no guarantee.\n[8 Mar 2026] Hana: @Tess You can bet I'll merge the login branch by March 12, 2026.\n[8 Mar 2026] Rhea: @Tess I'll label the bug reports by March 17, 2026, providing the hackathon goes ahead.\n[10 Mar 2026] Hana: @Tess Forget what I said, I won't merge the login branch\n[10 Mar 2026] Hana: @Rhea Count on me to write the release notes by March 13, 2026, if the code freeze happens.",
  "question": "Is the promise to merge the login branch that Hana made broken at the end of March 14, 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q10e986e0ba",
  "kind": "yes/no",
  "text": "Ravi shared this to pin down the garden makeover, housemates.\n\nMembers: Tomas, Tess, Ravi, Rhea\nChat export (date | from | to | message):\n2026-09-16 | Ravi | Tomas | I'll try to print the floor plan by 22 Sep 2026, no guarantee.\n2026-09-18 | Ravi | Rhea | Provided the boiler install visit happens, I will print the floor plan by 24 Sep 2026.\n2026-09-20 | Ravi | Tomas | I will scrape the old wallpaper by 27 Sep 2026.\n2026-09-23 | Tomas | group | On track for the boiler install visit to happen as planned.\n2026-09-24 | Rhea | Ravi | Quick update: you do not need to print the floor plan at all.\n2026-09-25 | Tomas | Ravi | No worries, you don't need to scrape the old wallpaper",
  "question": "Under the rules on the card, is Ravi's promise to print the floor plan broken, waived, not triggered or not yet due, rather than kept, as of 23 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q44d17bd773",
  "kind": "choice",
  "text": "{\"item\": \"chat export\", \"matter\": \"the student house hunt\", \"saved_by\": \"Tomas\", \"layout\": \"plain\"}\n\nMembers: Malik, Dara, Tomas, Priya\nChat log (oldest first):\n[9 Jul 2026] Malik: @Priya I'll photograph the bathroom mould by 15 July 2026, providing the freshers welcome night goes ahead.\n[9 Jul 2026] Malik: Lovely, the freshers welcome night is definitely happening!\n[12 Jul 2026] Dara: @Malik Lovely, I'll ring the letting agent by 16 July 2026 if the agent inventory walk is on.\n[12 Jul 2026] Priya: @Tomas Got it, I'll store the spare bike by 20 July 2026 for sure.\n[12 Jul 2026] Tomas: @Priya Relax, mate, you're not expected to store the spare bike\n[12 Jul 2026] Tomas: @Malik You are released, no requirement to photograph the bathroom mould.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status does the chat show for the promise Malik made to photograph the bathroom mould at the end of 15 July 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Kept",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "qa89bcc3216",
  "kind": "yes/no",
  "text": "Omar shared this so the front garden scheme is easy to find, flatmates.\n\nMembers: Omar, Dara, Lena\nChat log (oldest first):\n[13 Jul 2026] Lena: @Dara I promise to return the ladders by 16 Jul 2026.\n[13 Jul 2026] Omar: @Lena No need to return the ladders, I'm letting you off\n[15 Jul 2026] Omar: @Dara As long as the speed camera survey is on, I will share the garden hose by 23 Jul 2026.\n[17 Jul 2026] Omar: @Lena If the road works meeting goes ahead, I'll feed the cat across the road by 21 Jul 2026.\n[17 Jul 2026] Lena: @Dara Log entry: return the ladders, carried out",
  "question": "Would Lena be counted as having broken the promise to return the ladders at the end of 18 Jul 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q55ab9e98e5",
  "kind": "choice",
  "text": "Chat attached to a support case about the spring campaign, shared by Lee.\n\nMembers: Tomas, Lee, Zara\nChat log (oldest first):\n[18 Jul 2026] Lee: @Zara If the annual review goes ahead, I'll gladly send the newsletter copy by 26 Jul 2026.\n[20 Jul 2026] Lee: Sadly, the annual review won't go ahead.\n[20 Jul 2026] Tomas: @Zara Relax, I'll book the photo studio by 23 Jul 2026 for sure.\n[20 Jul 2026] Zara: Oh cheers, that helps.\n[21 Jul 2026] Lee: @Tomas Nobody needs you to book the photo studio, that's that\n[26 Jul 2026] Tomas: @Zara Quick report: I've managed to book the photo studio",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Tomas's pledge to book the photo studio sit at the end of 28 Jul 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q84cba7be49",
  "kind": "yes/no",
  "text": "Attached chat: the onboarding flow\nShared by: Nadia\n\nMembers: Nadia, Kai, Lee\nChat log (oldest first):\n[14 Aug 2026] Kai: @Lee You can bet I'll label the bug reports by 16 August 2026.\n[14 Aug 2026] Kai: @Lee Scratch that, I'm not going to label the bug reports\n[14 Aug 2026] Nadia: @Kai As long as the hackathon is on, I'll update the dependency list by 16 August 2026.\n[19 Aug 2026] Kai: @Lee I'll restart the build server by 26 August 2026 if the server migration goes ahead.\n[24 Aug 2026] Kai: Lovely, the server migration is definitely happening!\n[26 Aug 2026] Kai: @Lee Quick report: I've managed to restart the build server",
  "question": "Applying the card's rules, can it be said that Kai has not kept the promise to restart the build server at the end of 26 August 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9126cbf033",
  "kind": "yes/no",
  "text": "Yo flatmates, Arlo shared this chat about the house rules debate, so chip in.\n\nMembers: Arlo, Femi, Ivo\nChat log (oldest first):\n[19 Apr 2026] Arlo: @Ivo Aiming to find the loft ladder by 30 Apr 2026, we'll see.\n[19 Apr 2026] Femi: @Arlo Got it, I'll clear the kitchen sink by 22 Apr 2026 for sure.\n[20 Apr 2026] Arlo: @Femi Lovely, I'll find the loft ladder by 28 Apr 2026 if the heritage fete is on.\n[22 Apr 2026] Femi: @Arlo Think 26 Apr 2026 would work if I clear the kitchen sink instead?\n[22 Apr 2026] Arlo: @Femi Go ahead and clear the kitchen sink by 26 Apr 2026, that is fine.\n[23 Apr 2026] Arlo: Just so you know, the heritage fete is on as scheduled.",
  "question": "Would you say Arlo didn't keep the promise to find the loft ladder by the end of 25 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd02ffa5fab",
  "kind": "yes/no",
  "text": "Our flat chat about the street watch scheme, saved by Wren for whoever lives here.\n\nMembers: Tomas, Wren, Leila, Lee\nChat log (oldest first):\n[15 Sep 2026] Lee: @Leila If the hedge trimming day is on, I'll definitely feed the cat across the road by 20 September 2026.\n[20 Sep 2026] Lee: @Leila Got it, I'll take in the post by 27 September 2026 for sure.\n[22 Sep 2026] Lee: @Leila Correction, I will not be able to take in the post.\n[23 Sep 2026] Wren: @Lee As long as the bonfire night is on, I will clear the hedge trimmings by 28 September 2026.\n[23 Sep 2026] Leila: Scrapping the bonfire night, apologies to all.\n[25 Sep 2026] Wren: @Lee Don't sweat it, there's no need to take in the post",
  "question": "Applying the rules on the card, can Lee's promise to take in the post be said to have not been broken at the end of 27 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe9ab99fd92",
  "kind": "choice",
  "text": "Work chat channel about the social media plan, exported and saved by Omar.\n\nMembers: Omar, Ravi, Hana\nChat export (date | from | to | message):\n2026-09-30 | Ravi | Omar | I assure you I'll fix the landing page headline by 8 Oct 2026 if the brand photo shoot is on.\n2026-10-02 | Hana | Omar | I'll collect the survey answers by 10 Oct 2026, promise.\n2026-10-03 | Ravi | Omar | You can bet I'll set up the analytics dashboard by 5 Oct 2026.\n2026-10-05 | Ravi | group | Brilliant news everyone, the brand photo shoot is a go!\n2026-10-05 | Ravi | Hana | No worries, you don't need to collect the survey answers\n2026-10-06 | Hana | Omar | To my relief, I managed to collect the survey answers.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Hana's promise to collect the survey answers at the end of 12 Oct 2026?",
  "options": [
   "Kept",
   "Waived",
   "Broken",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q965f839457",
  "kind": "choice",
  "text": "Flatmate thread, saved by Mo, the topic being the vegetable plot plan.\n\nMembers: Kofi, Tess, Zara, Mo\nChat log (oldest first):\n[22 Apr 2026] Mo: @Tess I'll build the compost bay by 29 April 2026, provided the water tank delivery happens.\n[22 Apr 2026] Tess: Thanks lovely, got it!\n[24 Apr 2026] Zara: @Kofi I'll be sure to stake the tomato canes by 30 April 2026.\n[25 Apr 2026] Zara: Please note the water tank delivery will proceed.\n[25 Apr 2026] Zara: @Mo Don't sweat it, there's no need to build the compost bay\n[27 Apr 2026] Mo: @Tess Got myself to build the compost bay lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Mo's promise to build the compost bay at the end of 26 April 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Kept",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q7460f68061",
  "kind": "choice",
  "text": "{\"saved_copy\": \"the guest welcome plan\", \"keeper\": \"Ravi\", \"medium\": \"chat transcript\"}\n\nMembers: Malik, Ravi, Elif\nChat log (oldest first):\n[6 Apr 2026] Malik: @Ravi You can bet I'll restock the guest toiletries by 13 Apr 2026.\n[6 Apr 2026] Malik: @Elif I assure you I'll wash the beach towels by 10 Apr 2026 if the owner handover visit is on.\n[7 Apr 2026] Ravi: @Elif If the pool safety inspection goes ahead, I'll collect the bed linen by 11 Apr 2026.\n[7 Apr 2026] Malik: On track for the owner handover visit to happen as planned.\n[8 Apr 2026] Malik: @Elif Guess what, I managed to wash the beach towels!\n[9 Apr 2026] Malik: @Ravi For the record: I was able to restock the guest toiletries",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Malik's commitment to wash the beach towels at the end of 10 Apr 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "qa7b6d99d66",
  "kind": "yes/no",
  "text": "{\"thread_kind\": \"exported conversation\", \"about\": \"the store makeover\", \"exported_by\": \"Nadia\"}\n\nMembers: Femi, Zara, Nadia, Arlo\nChat log (oldest first):\n[25 Aug 2026] Zara: @Nadia I'll send the moodboard files by 31 August 2026 if the gallery install goes ahead.\n[25 Aug 2026] Femi: Lovely, the gallery install is definitely happening!\n[26 Aug 2026] Zara: @Nadia Guess what, I managed to send the moodboard files!\n[27 Aug 2026] Femi: Quick check, any update on plans to send the moodboard files?\n[28 Aug 2026] Arlo: @Zara I will collect the photo credits by 6 September 2026.\n[6 Sep 2026] Arlo: @Zara Log entry: collect the photo credits, carried out",
  "question": "Applying the card's rules, does Zara's promise to send the moodboard files count as broken, waived, not triggered or not yet due, rather than kept, as of 31 August 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2fbe569b8c",
  "kind": "yes/no",
  "text": "Neighbours and renters, the flat chat, exported by Ravi, covering the loft conversion.\n\nMembers: Greta, Arlo, Ravi, Femi\nChat export (date | from | to | message):\n2026-06-26 | Ravi | Arlo | If the removal van arrival goes ahead, I'll gladly pick up the grout bag by 4 Jul 2026.\n2026-06-26 | Ravi | Femi | Lovely, I'll fetch the paint samples by 2 Jul 2026 for sure.\n2026-06-28 | Ravi | Greta | Absolutely, I will sweep the dust from stairs by 1 Jul 2026.\n2026-06-29 | Arlo | Ravi | Forget it, you won't need to sweep the dust from stairs\n2026-07-01 | Ravi | group | Just so you know, the removal van arrival is on as scheduled.\n2026-07-03 | Ravi | Greta | Ticked off my list: sweep the dust from stairs, yay.",
  "question": "Going by the card's rules, does Ravi keep the promise to sweep the dust from stairs at the end of 30 Jun 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4da9c843c2",
  "kind": "yes/no",
  "text": "Subject: chat export on the house refit\nThe full chat follows, saved by Rhea, for you to read.\n\nMembers: Leila, Rhea, Malik\nChat export (date | from | to | message):\n2026-07-31 | Rhea | Malik | Got it, I'll fetch the paint samples by 9 Aug 2026 for sure.\n2026-08-03 | Leila | Rhea | As long as the kitchen fitting day is on, I will hang the new curtain rail by 8 Aug 2026.\n2026-08-04 | Rhea | Malik | Guess what, I managed to fetch the paint samples!\n2026-08-04 | Malik | group | On track for the kitchen fitting day to happen as planned.\n2026-08-08 | Leila | Rhea | Got myself to hang the new curtain rail lol.",
  "question": "Going by the card's rules, does Leila not keep the promise to hang the new curtain rail at the end of 9 Aug 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8fa4157195",
  "kind": "choice",
  "text": "This export holds the messages about the allotment expansion, which Kofi saved.\n\nMembers: Mo, Kai, Kofi, Ana\nChat log (oldest first):\n[11 Mar 2026] Mo: @Ana I'll weed the carrot row by 15 March 2026, provided the village flower show happens.\n[13 Mar 2026] Kofi: @Ana Absolutely, I will fix the shed door by 16 March 2026.\n[13 Mar 2026] Kofi: @Ana Scratch that, I'm not going to fix the shed door\n[16 Mar 2026] Ana: @Mo Count on me to stake the tomato canes by 25 March 2026 if the plot inspection is on.\n[16 Mar 2026] Mo: @Kofi No worries, you don't need to fix the shed door",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Kofi made to fix the shed door at the end of 20 March 2026?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "qd7823dfd85",
  "kind": "yes/no",
  "text": "Committee thread about the new repertoire, passed on to the group by Rhea.\n\nMembers: Kai, Rhea, Hana, Femi\nChat log (oldest first):\n[19 May 2026] Femi: @Kai I promise to set up the sound desk by 23 May 2026.\n[20 May 2026] Femi: @Hana If the choir festival is on, I'll definitely send the audition reminders by 25 May 2026.\n[24 May 2026] Rhea: Just so you know, the choir festival is on as scheduled.\n[24 May 2026] Femi: @Hana Mate, I promised, may I send the audition reminders by 30 May 2026 instead?\n[25 May 2026] Hana: @Femi Yes, you can send the audition reminders by 30 May 2026 instead.",
  "question": "Would you say the promise Femi made to send the audition reminders is not broken at the end of 30 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5fe95f3808",
  "kind": "yes/no",
  "text": "Shared by Greta, a help-desk thread covering the guest travel plans.\n\nMembers: Greta, Ana\nChat log (oldest first):\n[19 Feb 2026] Ana: @Greta If the reunion lunch goes ahead, I'll label the memory box by 23 Feb 2026.\n[19 Feb 2026] Ana: Brilliant news everyone, the reunion lunch is a go!\n[23 Feb 2026] Ana: @Greta Might I ask whether I could label the memory box by 28 Feb 2026 instead?\n[23 Feb 2026] Ana: @Greta My sincere apologies, I am unable to label the memory box.\n[23 Feb 2026] Ana: @Greta I'll be sure to set up the slideshow laptop by 26 Feb 2026.",
  "question": "Applying the rules on the card, has Ana kept the promise to label the memory box as of 26 Feb 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4e4e262a1b",
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
  "qid": "qa9da0946fe",
  "kind": "yes/no",
  "text": "An exported family chat on the garden makeover, saved by Malik, left unchanged.\n\nMembers: Zara, Malik, Hana, Nadia\nChat export (date | from | to | message):\n2026-06-29 | Hana | Malik | I promise to pick up the grout bag by Friday, July 3, 2026 if the mortgage valuation visit is on.\n2026-06-30 | Malik | Zara | I'll sweep the dust from stairs by Thursday, July 2, 2026, promise.\n2026-06-30 | Malik | Zara | I committed to sweep the dust from stairs, can I do that by Saturday, July 4, 2026 instead?\n2026-06-30 | Malik | group | Great news, the mortgage valuation visit is on!\n2026-07-02 | Zara | Malik | Aw no, you need to sweep the dust from stairs by the original date!\n2026-07-02 | Zara | group | Did you manage to pick up the grout bag?",
  "question": "Has Hana's promise to pick up the grout bag ended up broken, waived, not triggered or not yet due, instead of kept, as of Wednesday, July 1, 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe43aa682d4",
  "kind": "yes/no",
  "text": "Work chat channel about the trade show push, exported and saved by Ravi.\n\nMembers: Ravi, Kofi, Ana\nChat export (date | from | to | message):\n2026-10-29 | Ravi | Ana | Absolutely, I will collect the survey answers by 2026-11-01.\n2026-10-30 | Ana | Ravi | As long as the trade fair stand is on, I'll book the photo studio by 2026-11-02.\n2026-10-31 | Ravi | Ana | Got myself to collect the survey answers lol.\n2026-11-01 | Ana | group | Great news, the trade fair stand is on!\n2026-11-02 | Ana | Ravi | Log entry: book the photo studio, carried out",
  "question": "Is the promise to book the photo studio kept by Ana as of 2026-11-06?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1051e48508",
  "kind": "choice",
  "text": "Copy of a household chat shared by Mo, where neighbours discuss the care plan.\n\nMembers: Yuki, Dara, Mo, Jonas\nChat log (oldest first):\n[9 Apr 2026] Dara: Hoping to set up the medicine dispenser by 16 Apr 2026, can't promise.\n[10 Apr 2026] Dara: @Yuki Count on me, I'll set up the medicine dispenser by 15 Apr 2026.\n[10 Apr 2026] Dara: @Yuki Scratch what I said, I won't set up the medicine dispenser.\n[10 Apr 2026] Yuki: @Dara No worries, you don't need to set up the medicine dispenser\n[11 Apr 2026] Jonas: @Mo I'll fetch the mobility aids by 14 Apr 2026 as long as the eye test is on.\n[13 Apr 2026] Mo: Lovely, the eye test is definitely happening!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Dara's promise to set up the medicine dispenser receive at the end of 15 Apr 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not triggered",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q3078d6abac",
  "kind": "yes/no",
  "text": "{\"kind\": \"exported group chat\", \"about_topic\": \"the staff handbook\", \"sent_by\": \"Omar\"}\n\nMembers: Omar, Zara, Yuki\nChat log (oldest first):\n[26 Jun 2026] Yuki: @Omar I own this, I'll book the boardroom by July 4, 2026.\n[27 Jun 2026] Zara: @Omar If the coffee morning goes ahead, I'll gladly replace the kitchen filters by June 29, 2026.\n[28 Jun 2026] Zara: @Omar Committing to order the office stationery by July 3, 2026.\n[28 Jun 2026] Zara: @Yuki I'll renew the fire extinguisher service by June 30, 2026 if the staff picnic goes ahead.\n[29 Jun 2026] Yuki: @Zara You don't have to order the office stationery at all",
  "question": "Is Zara's promise to order the office stationery kept on July 3, 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q255bb61375",
  "kind": "choice",
  "text": "Subject: Saved thread about the garden makeover\nHere is a full export from Rhea, ready to read.\n\nMembers: Leila, Rhea, Sami\nChat export (date | from | to | message):\n2026-10-22 | Rhea | Sami | It's on me to sweep the dust from stairs by 26 October 2026.\n2026-10-22 | Sami | group | Ah right, thanks for that.\n2026-10-22 | Rhea | Leila | I'll collect the sanding pads by 29 October 2026 if the mortgage valuation visit goes ahead.\n2026-10-25 | Rhea | Sami | Mate, I promised, may I sweep the dust from stairs by 1 November 2026 instead?\n2026-10-26 | Sami | Rhea | Oh hun, I can't budge, so sweep the dust from stairs by the old date!\n2026-10-26 | Leila | Rhea | Don't sweat it, there's no need to sweep the dust from stairs\n2026-10-26 | Rhea | Sami | Mum, I did sweep the dust from stairs, haha.\n2026-10-29 | Rhea | Sami | Provided the kitchen fitting day happens, I will print the floor plan by 31 October 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIf the chat is checked at the end of 8 November 2026, which date marks the deadline for Rhea to sweep the dust from stairs, with agreed date changes included?",
  "options": [
   "29 October 2026",
   "1 November 2026",
   "26 October 2026"
  ]
 },
 {
  "qid": "q57233ce956",
  "kind": "choice",
  "text": "Our flat chat about the house rules debate, shared by Mo for whoever lives here.\n\nMembers: Mo, Lena, Hana\nChat log (oldest first):\n[19 May 2026] Lena: @Mo Only if the house viewing is on, I will tidy the boot room by Thursday, 28 May 2026.\n[19 May 2026] Mo: @Hana I'll try to defrost the old fridge by Saturday, 30 May 2026, can't promise!\n[21 May 2026] Mo: @Hana It's on me to defrost the old fridge by Wednesday, 27 May 2026.\n[23 May 2026] Hana: @Mo Lovely, I'll wash the sash windows by Tuesday, 26 May 2026 for sure.\n[23 May 2026] Mo: @Hana Update on my side: I will not defrost the old fridge, sorry.\n[27 May 2026] Hana: Really pleased to say the house viewing will go ahead!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Mo's promise to defrost the old fridge at the end of Saturday, 23 May 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q7bb90a699d",
  "kind": "choice",
  "text": "Saved by Kofi from the shared house thread on the autumn term budget.\n\nMembers: Greta, Elif, Kofi, Hana\nChat log (oldest first):\n[18 Oct 2026] Hana: @Kofi Relax, I'll store the spare bike by 23 Oct 2026, promise.\n[20 Oct 2026] Elif: @Greta I promise to ring the letting agent by 28 Oct 2026 if the agent inventory walk is on.\n[20 Oct 2026] Elif: @Hana Relax, mate, you're not expected to store the spare bike\n[23 Oct 2026] Greta: Update: the agent inventory walk is going ahead as planned.\n[24 Oct 2026] Kofi: @Elif Ah, no stress, no need for you to ring the letting agent",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Elif made to ring the letting agent at the end of 28 Oct 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q92fa8995af",
  "kind": "choice",
  "text": "Our flat chat about the house refit, saved by Tess for whoever lives here.\n\nMembers: Nadia, Oskar, Tess\nChat export (date | from | to | message):\n2026-08-23 | Nadia | Tess | I'll collect the sanding pads by 31 August 2026 as long as the damp survey inspection is on.\n2026-08-24 | Nadia | Tess | You can bank on me to scrape the old wallpaper by 2 September 2026.\n2026-08-28 | Oskar | group | Really pleased to say the damp survey inspection will go ahead!\n2026-08-28 | Nadia | Tess | Is 6 September 2026 alright for me to collect the sanding pads?\n2026-08-29 | Tess | Nadia | Revised deadline is 6 September 2026, so you can collect the sanding pads.\n2026-09-04 | Nadia | Tess | For the record: I was able to collect the sanding pads",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn the chat, what's the status of Nadia's promise to collect the sanding pads at the end of 27 August 2026?",
  "options": [
   "Kept",
   "Broken",
   "Waived",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q7525e95ba9",
  "kind": "choice",
  "text": "Subject: the garden makeover\nBelow is the group chat that Arlo saved, unedited.\n\nMembers: Greta, Wren, Mo, Arlo\nChat export (date | from | to | message):\n2026-09-07 | Greta | Arlo | I'll be sure to measure the hallway for shelves by 2026-09-12.\n2026-09-10 | Greta | Arlo | Promise to scrape the old wallpaper by 2026-09-14 if the builder quote meeting goes ahead.\n2026-09-11 | Wren | Greta | I'll return the tile cutter by 2026-09-16, promise.\n2026-09-12 | Mo | group | Lovely, the builder quote meeting is definitely happening!\n2026-09-12 | Mo | Greta | Forget it, you won't need to scrape the old wallpaper\n2026-09-14 | Greta | Wren | Relax, mate, you're not expected to return the tile cutter",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Greta's promise to scrape the old wallpaper turn out at the end of 2026-09-17?",
  "options": [
   "Not triggered",
   "Waived",
   "Kept",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q60f27db695",
  "kind": "choice",
  "text": "Sami shared this back and forth with the client about the wedding weekend.\n\nMembers: Sami, Tess, Ines\nChat log (oldest first):\n[2 Apr 2026] Ines: @Sami I'll be sure to set up the backdrop frame by 9 Apr 2026.\n[4 Apr 2026] Tess: @Ines Quick update: you do not need to set up the backdrop frame at all.\n[6 Apr 2026] Ines: @Sami I will return the lighting stands by 14 Apr 2026 only if the engagement shoot happens.\n[7 Apr 2026] Tess: How's the plan to set up the backdrop frame?\n[7 Apr 2026] Ines: @Tess Ticket's mine, I'll buy the candle props by 10 Apr 2026.\n[7 Apr 2026] Ines: @Tess I'll charge the flash batteries by 16 Apr 2026, providing the venue visit goes ahead.\n\nSummary: Dates mentioned in the chat may be moved freely by Sami, so the schedule shown here is provisional.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 5 Apr 2026, what status has Ines's promise to set up the backdrop frame got?",
  "options": [
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q47622ebaed",
  "kind": "choice",
  "text": "Club chat, saved by Zara\nTopic: the choir tour, for the volunteer committee.\n\nMembers: Ivo, Greta, Zara\nChat export (date | from | to | message):\n2026-05-02 | Zara | Greta | Count on me to return the library scores by 2026-05-04 if the choir festival is on.\n2026-05-04 | Greta | Ivo | Count on me to fetch the choir robes by 2026-05-08 if the sing along is on.\n2026-05-04 | Zara | group | Afraid the sing along is called off.\n2026-05-05 | Ivo | Zara | Absolutely, I will send the audition reminders by 2026-05-09.\n2026-05-05 | Ivo | Zara | Ticked off: send the audition reminders, feels so good\n2026-05-06 | Greta | Ivo | Can I fetch the choir robes by 2026-05-13 instead? I did promise, sorry.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Greta made to fetch the choir robes at the end of 2026-05-12?",
  "options": [
   "Kept",
   "Broken",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q929dcfed49",
  "kind": "yes/no",
  "text": "Household group messages for the travel plans were passed along by Bruno.\n\nMembers: Tess, Mo, Bruno, Yuki\nChat log (oldest first):\n[17 May 2026] Yuki: @Tess Count on me to fetch the sunscreen by 20 May 2026.\n[17 May 2026] Bruno: @Yuki Count on me to send the packing list by 22 May 2026, if the beach picnic happens.\n[18 May 2026] Tess: @Yuki Forget it, you won't need to fetch the sunscreen\n[19 May 2026] Mo: @Tess I will book the airport parking by 28 May 2026.\n[20 May 2026] Yuki: Yep, the beach picnic is on as planned.\n[21 May 2026] Mo: @Tess Count on me to print the boarding passes by 24 May 2026, if the family cookout happens.",
  "question": "Did Bruno break the promise to send the packing list at the end of 26 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf9f8144128",
  "kind": "yes/no",
  "text": "Hana shared this channel export, covering the mobile release for the team.\n\nMembers: Hana, Rhea, Kai\nChat log (oldest first):\n[27 Jan 2026] Rhea: @Hana You can bet I'll fix the test runner by Thursday, February 5, 2026.\n[28 Jan 2026] Hana: @Kai Lovely, I'll rotate the test keys by Monday, February 2, 2026 for sure.\n[1 Feb 2026] Hana: @Kai I'll label the bug reports by Saturday, February 7, 2026, providing the sprint demo goes ahead.\n[2 Feb 2026] Kai: @Hana Quick update: you do not need to rotate the test keys at all.\n[6 Feb 2026] Kai: Yep, the sprint demo is on as planned.\n[9 Feb 2026] Rhea: Where are you up to with plans to rotate the test keys?",
  "question": "At the end of Saturday, February 7, 2026, does the promise Hana made to rotate the test keys have any status except broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe5cfc7ef92",
  "kind": "yes/no",
  "text": "Thread filed under support\nAbout the store makeover, saved by Hana.\n\nMembers: Hana, Nadia, Elif\nChat log (oldest first):\n[11 Mar 2026] Nadia: @Elif Relax, I'll pick the colour swatches by 14 March 2026, promise.\n[14 Mar 2026] Hana: @Nadia You are released, no requirement to pick the colour swatches.\n[15 Mar 2026] Elif: @Nadia Count on me to upload the sticker artwork by 19 March 2026, if the brand review call happens.\n[17 Mar 2026] Nadia: Quick heads up, the brand review call is scrapped.\n[17 Mar 2026] Nadia: @Elif I'll be sure to fetch the brand fonts by 20 March 2026.",
  "question": "Has Elif kept the promise to upload the sticker artwork at the end of 21 March 2026, instead of broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2de504ed89",
  "kind": "yes/no",
  "text": "Ivo saved this so we stay on the same page about the garden shed build, mates.\n\nMembers: Ivo, Oskar, Bruno\nChat log (oldest first):\n[2 Aug 2026] Bruno: Will attempt to stake the tomato canes by August 9, 2026, can't promise.\n[2 Aug 2026] Ivo: @Oskar Count on me to weed the carrot row by August 9, 2026, if the village flower show happens.\n[3 Aug 2026] Bruno: @Ivo Relax, I'll stake the tomato canes by August 11, 2026 for sure.\n[3 Aug 2026] Oskar: Fab, we are on for the village flower show as planned!\n[4 Aug 2026] Ivo: @Bruno You are released, no requirement to stake the tomato canes.\n[7 Aug 2026] Oskar: @Ivo You can bet I'll build the compost bay by August 13, 2026.",
  "question": "Has Bruno not kept the promise to stake the tomato canes at the end of August 7, 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q926ac30083",
  "kind": "yes/no",
  "text": "Tess forwarded this for the committee, covering the choir tour.\n\nMembers: Nadia, Tess, Oskar\nChat log (oldest first):\n[5 Jul 2026] Oskar: @Tess Relax, I'll send the audition reminders by 11 Jul 2026, promise.\n[5 Jul 2026] Nadia: @Oskar No worries, you don't need to send the audition reminders\n[7 Jul 2026] Oskar: @Nadia Committing to buy the spare folders by 12 Jul 2026.\n[7 Jul 2026] Oskar: @Nadia I assure you I'll fix the stand microphones by 12 Jul 2026 if the choir festival is on.\n[7 Jul 2026] Oskar: @Nadia Relax, I'll collect the sheet music by 15 Jul 2026, promise.\n[11 Jul 2026] Tess: Yep, the choir festival is on as planned.",
  "question": "Did Oskar break the promise to send the audition reminders at the end of 11 Jul 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbaf50b40e7",
  "kind": "yes/no",
  "text": "Work chat channel about the grant renewal, exported and saved by Nadia.\n\nMembers: Femi, Kofi, Nadia, Ravi\nChat log (oldest first):\n[2 Aug 2026] Femi: @Nadia It's on me to fetch the grant forms by 11 August 2026.\n[3 Aug 2026] Femi: @Nadia For the record: I was able to fetch the grant forms\n[6 Aug 2026] Femi: @Ravi Count on me, I'll return the library books by 9 August 2026.\n[9 Aug 2026] Nadia: @Femi I assure you I'll collect the lab samples by 11 August 2026 if the journal club is on.\n[9 Aug 2026] Nadia: Sorry all, the journal club is called off.\n[10 Aug 2026] Femi: @Ravi Ta-da, I went and did it: return the library books!",
  "question": "Under the rules on the card, is Femi's promise to return the library books kept as of 12 August 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q777d479bed",
  "kind": "choice",
  "text": "Flatmate thread, saved by Omar, the topic being the kitchen garden project.\n\nMembers: Omar, Ines, Tess\nChat log (oldest first):\n[7 Mar 2026] Tess: @Omar Only if the village flower show is on, I will fix the shed door by 15 Mar 2026.\n[8 Mar 2026] Omar: Aiming to dig the potato patch by 12 Mar 2026, we'll see.\n[9 Mar 2026] Tess: @Ines If the water tank delivery goes ahead, I'll water the allotment beds by 16 Mar 2026.\n[10 Mar 2026] Omar: @Tess I will make sure to dig the potato patch by 18 Mar 2026.\n[12 Mar 2026] Omar: @Tess Is it all right if I dig the potato patch by 21 Mar 2026 instead?\n[12 Mar 2026] Omar: @Ines Got it, I'll weed the carrot row by 15 Mar 2026 for sure.\n[14 Mar 2026] Ines: @Omar Go ahead and dig the potato patch by 21 Mar 2026, that is fine.\n[15 Mar 2026] Tess: @Omar You are released, no requirement to weed the carrot row.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat's the day Omar needs to dig the potato patch by at the end of 22 Mar 2026, after any new date the group agreed on?",
  "options": [
   "21 Mar 2026",
   "16 Mar 2026",
   "18 Mar 2026"
  ]
 },
 {
  "qid": "q8530c86b13",
  "kind": "choice",
  "text": "Subject: Chat about the documentary cut\nThe copy from Leila follows below as a plain record.\n\nMembers: Yuki, Leila, Rhea, Hana\nChat export (date | from | to | message):\n2026-01-08 | Hana | Rhea | If the shoot day goes ahead, I'll upload the render files by Thursday, 15 January 2026.\n2026-01-08 | Rhea | group | Really pleased to say the shoot day will go ahead!\n2026-01-11 | Hana | Rhea | Committing to ship the hard drive by Tuesday, 20 January 2026.\n2026-01-13 | Rhea | Hana | Good news, you're let off having to upload the render files\n2026-01-16 | Hana | Rhea | Guess who managed to upload the render files, go team!",
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
  "qid": "qd9696d3f05",
  "kind": "yes/no",
  "text": "A family chat export on the caring rota, shared out by Lena.\n\nMembers: Sami, Lena, Jonas\nChat log (oldest first):\n[28 Oct 2026] Jonas: @Lena Guaranteed I'll drop off the hot meals by 3 November 2026.\n[31 Oct 2026] Jonas: @Lena Is 6 November 2026 alright for me to drop off the hot meals?\n[31 Oct 2026] Jonas: @Lena Ticked off: drop off the hot meals, feels so good\n[2 Nov 2026] Jonas: @Lena I'll collect the post by 11 November 2026, providing the carer handover goes ahead.\n[3 Nov 2026] Sami: @Lena Provided the eye test happens, I'll book the clinic transport by 12 November 2026.\n[11 Nov 2026] Lena: Just so you know, the eye test is on as scheduled.",
  "question": "Is the promise to drop off the hot meals kept by Jonas as of 30 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8d874c2adc",
  "kind": "choice",
  "text": "Channel title: work team chat\nDescription: about the social media plan, exported by Ivo.\n\nMembers: Kai, Ivo, Priya\nChat export (date | from | to | message):\n2026-04-26 | Kai | Priya | Provided the product launch happens, I will fix the landing page headline by 30 April 2026.\n2026-04-26 | Priya | group | Thanks lovely, got it!\n2026-04-26 | Priya | Kai | Got it, I'll return the rented camera gear by 1 May 2026 for sure.\n2026-04-28 | Kai | Priya | You are released, no requirement to return the rented camera gear.\n2026-04-29 | Kai | group | Sadly, the product launch won't go ahead.\n2026-05-01 | Priya | Ivo | I will book the photo studio by 7 May 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Kai's pledge to fix the landing page headline at the end of 4 May 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Not triggered",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "qe1231f4f28",
  "kind": "yes/no",
  "text": "Pasted from our flat chat by Dara, the bit about the guest welcome plan.\n\nMembers: Omar, Dara, Ravi\nChat log (oldest first):\n[16 Sep 2026] Dara: @Omar Relax, I'll leave the welcome basket by 19 Sep 2026 for sure.\n[17 Sep 2026] Omar: @Ravi Ticket's mine, I'll air the spare room by 21 Sep 2026.\n[19 Sep 2026] Ravi: @Omar I'll vacuum the holiday cottage by 24 Sep 2026 as long as the check out clean is on.\n[21 Sep 2026] Omar: @Ravi For the record: I was able to air the spare room\n[21 Sep 2026] Dara: Quick heads up, the check out clean is scrapped.",
  "question": "Checking the chat at the end of 26 Sep 2026, has Omar broken the promise to air the spare room?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qda1e10a3e5",
  "kind": "yes/no",
  "text": "{\"source\": \"saved thread\", \"about\": \"the family day out\", \"owner\": \"Lena\", \"kind\": \"chat export\"}\n\nMembers: Jonas, Nadia, Lena, Sami\nChat log (oldest first):\n[21 Apr 2026] Lena: @Nadia As long as the garden tea party is on, I will walk the dog by 2026-04-30.\n[22 Apr 2026] Sami: Hoping to sort the old photo albums by 2026-04-30, but can't promise.\n[24 Apr 2026] Sami: @Lena I promise to sort the old photo albums by 2026-04-27.\n[24 Apr 2026] Nadia: Sad to report that the garden tea party is off.\n[27 Apr 2026] Jonas: @Sami Relax, I'll fetch the craft box by 2026-05-01, promise.\n[27 Apr 2026] Sami: @Lena To my relief, I managed to sort the old photo albums.",
  "question": "Going by the card's rules, does Sami not keep the promise to sort the old photo albums at the end of 2026-04-27?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0f7593574d",
  "kind": "choice",
  "text": "Team thread shared by Femi, covering the visitor policy in the channel.\n\nMembers: Kai, Nadia, Femi\nChat log (oldest first):\n[17 May 2026] Nadia: @Femi You can bet I'll print the staff rota by 24 May 2026.\n[20 May 2026] Nadia: @Femi Lovely, I'll order the office stationery by 28 May 2026 for sure.\n[20 May 2026] Nadia: @Femi Any chance I can print the staff rota by 27 May 2026 instead?\n[21 May 2026] Kai: @Nadia Yes, you can print the staff rota by 27 May 2026 if that suits you.\n[24 May 2026] Nadia: @Femi Forget what I said, I won't order the office stationery\n[24 May 2026] Nadia: @Kai I'll collect the visitor badges by 30 May 2026 as long as the annual audit is on.\n[25 May 2026] Kai: @Femi I'll send the expense receipts by 28 May 2026, provided the staff picnic happens.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIf the chat is checked at the end of 25 May 2026, which date marks the deadline for Nadia to print the staff rota, with agreed date changes included?",
  "options": [
   "24 May 2026",
   "27 May 2026",
   "28 May 2026"
  ]
 },
 {
  "qid": "q2a05abad54",
  "kind": "choice",
  "text": "Yuki saved this exchange with the client about the online store move.\n\nMembers: Zara, Elif, Yuki, Ines\nChat log (oldest first):\n[31 May 2026] Zara: @Yuki Relax, I'll restore the old theme by 9 June 2026, promise.\n[3 Jun 2026] Zara: @Elif As long as the stock count is on, I will fix the checkout button by 9 June 2026.\n[4 Jun 2026] Yuki: @Elif If the market day is on, I'll definitely set up the email forwarding by 9 June 2026.\n[5 Jun 2026] Elif: @Yuki I'll add the size chart by 8 June 2026, promise.\n[6 Jun 2026] Elif: @Yuki Is it all right if I add the size chart by 10 June 2026 instead?\n[7 Jun 2026] Ines: @Zara Nobody needs you to restore the old theme, that's that\n[8 Jun 2026] Ines: @Elif Yes, all good for you to add the size chart by 10 June 2026 instead.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, what is the deadline for Elif to add the size chart at the end of 21 June 2026, with any agreed change of date counted?",
  "options": [
   "10 June 2026",
   "8 June 2026",
   "9 June 2026"
  ]
 }
]
