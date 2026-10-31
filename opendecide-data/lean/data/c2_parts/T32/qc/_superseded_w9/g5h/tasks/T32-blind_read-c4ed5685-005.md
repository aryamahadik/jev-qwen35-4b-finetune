# G5-H blind read (all free-form rows) T32-blind_read-c4ed5685-005 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T32/qc/g5h/answers/T32-blind_read-c4ed5685-005.json

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
  "qid": "q9ef6d92327",
  "kind": "choice",
  "text": "Parents and cousins, this is where we sort out the garden shed build. Saved by Dara.\n\nMembers: Greta, Dara, Yuki\nChat log (oldest first):\n[3 Jun 2026] Yuki: @Greta Count on me to stake the tomato canes by June 8, 2026 if the seed swap day is on.\n[6 Jun 2026] Greta: @Dara Count on me, I'll dig the potato patch by June 15, 2026.\n[6 Jun 2026] Yuki: Please note the seed swap day will proceed.\n[8 Jun 2026] Yuki: @Greta Quick question, could I stake the tomato canes by June 13, 2026 instead?\n[8 Jun 2026] Dara: @Yuki You are released, no requirement to stake the tomato canes.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Yuki's promise to stake the tomato canes at the end of June 8, 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q83023946fb",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the new kit design\nThe thread below comes from Zara and is passed on as it is.\n\nMembers: Ivo, Tess, Zara\nChat log (oldest first):\n[20 Jan 2026] Ivo: @Zara Maybe I can wash the club jerseys by 24 Jan 2026.\n[21 Jan 2026] Ivo: @Zara Relax, I'll wash the club jerseys by 26 Jan 2026, promise.\n[21 Jan 2026] Tess: @Ivo Ah, no stress, no need for you to wash the club jerseys\n[22 Jan 2026] Ivo: @Tess If the bike check goes ahead, I'll print the route cards by 28 Jan 2026.\n[22 Jan 2026] Ivo: @Zara For the record: I was able to wash the club jerseys\n[25 Jan 2026] Tess: On track for the bike check to happen as planned.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Ivo's pledge to wash the club jerseys sit at the end of 25 Jan 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Waived",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "qed39d562b2",
  "kind": "choice",
  "text": "Mo saved these replies from the agent on the flatmate contract terms.\n\nMembers: Kofi, Mo, Ravi, Rhea\nChat log (oldest first):\n[16 Mar 2026] Rhea: @Kofi I will send the deposit receipt by 22 Mar 2026.\n[16 Mar 2026] Rhea: @Kofi I'm withdrawing my promise to send the deposit receipt\n[16 Mar 2026] Mo: @Rhea Provided the gas safety inspection happens, I will ring the letting agent by 18 Mar 2026.\n[19 Mar 2026] Mo: @Ravi As long as the move in day is on, I'll scan the council tax letter by 21 Mar 2026.\n[19 Mar 2026] Mo: Yep, the move in day is on as planned.\n[22 Mar 2026] Mo: @Rhea No worries, you don't need to send the deposit receipt",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWith reference to the card's definitions, in what status is Rhea's commitment to send the deposit receipt at the end of 25 Mar 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "qf873872f2e",
  "kind": "choice",
  "text": "Jonas saved this so we stay on the same page about the bathroom refit, mates.\n\nMembers: Dara, Jonas, Tess, Ravi\nChat export (date | from | to | message):\n2026-06-22 | Jonas | Ravi | If the removal van arrival goes ahead, I'll collect the sanding pads by 1 Jul 2026.\n2026-06-25 | Ravi | Dara | I'll sweep the dust from stairs by 30 Jun 2026 if the kitchen fitting day goes ahead.\n2026-06-27 | Ravi | Dara | Relax, I'll fetch the paint samples by 29 Jun 2026, promise.\n2026-06-28 | Ravi | Dara | To note: I have managed to fetch the paint samples\n2026-06-29 | Jonas | group | Lovely, the kitchen fitting day is definitely happening!\n2026-06-29 | Ravi | Dara | Got myself to sweep the dust from stairs lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Ravi made to sweep the dust from stairs at the end of 28 Jun 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q8f5d35d89d",
  "kind": "yes/no",
  "text": "We have been planning the family history here, shared by Mo.\n\nMembers: Mo, Femi, Leila, Arlo\nChat log (oldest first):\n[30 Jan 2026] Leila: @Femi I promise to set up the slideshow laptop by 2026-02-04.\n[1 Feb 2026] Leila: @Arlo Count on me, I'll buy the name tags by 2026-02-09.\n[3 Feb 2026] Arlo: @Mo I promise to send the group invitations by 2026-02-11 if the reunion lunch is on.\n[7 Feb 2026] Mo: How's the plan to buy the name tags?\n[8 Feb 2026] Leila: Fab, we are on for the reunion lunch as planned!\n[8 Feb 2026] Leila: @Arlo Quick report: I've managed to buy the name tags",
  "question": "According to the rules on the card, does the promise Leila made to buy the name tags have any status except broken at the end of 2026-02-08?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf0415b89e8",
  "kind": "yes/no",
  "text": "Mo shared this so the family follows the street watch scheme.\n\nMembers: Omar, Ravi, Mo, Yuki\nChat log (oldest first):\n[22 Jun 2026] Ravi: @Yuki I will lock the side gate by 29 June 2026 only if the parking permit visit happens.\n[26 Jun 2026] Yuki: Really pleased to say the parking permit visit will go ahead!\n[27 Jun 2026] Ravi: @Mo Ticket's mine, I'll clear the hedge trimmings by 5 July 2026.\n[2 Jul 2026] Ravi: @Mo I regret to say that I shall not clear the hedge trimmings.\n[4 Jul 2026] Yuki: @Ravi You don't have to clear the hedge trimmings at all",
  "question": "Would Ravi be counted as having broken the promise to clear the hedge trimmings at the end of 4 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5bfb4f8d2a",
  "kind": "yes/no",
  "text": "Ivo saved this so we stay on the same page about the garden shed build, mates.\n\nMembers: Ivo, Oskar, Bruno\nChat log (oldest first):\n[2 Aug 2026] Bruno: Will attempt to stake the tomato canes by August 9, 2026, can't promise.\n[2 Aug 2026] Ivo: @Oskar Count on me to weed the carrot row by August 9, 2026, if the village flower show happens.\n[3 Aug 2026] Bruno: @Ivo Relax, I'll stake the tomato canes by August 11, 2026 for sure.\n[3 Aug 2026] Oskar: Fab, we are on for the village flower show as planned!\n[4 Aug 2026] Ivo: @Bruno You are released, no requirement to stake the tomato canes.\n[7 Aug 2026] Oskar: @Ivo You can bet I'll build the compost bay by August 13, 2026.",
  "question": "Has Bruno not kept the promise to stake the tomato canes at the end of August 7, 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9344a82d73",
  "kind": "choice",
  "text": "Posted by Priya from the work channel: the office refit.\n\nMembers: Priya, Kai, Ravi\nChat log (oldest first):\n[7 Feb 2026] Priya: @Ravi Got it, I'll fetch the parking permits by 13 Feb 2026 for sure.\n[8 Feb 2026] Kai: @Priya Guaranteed I'll book the boardroom by 17 Feb 2026.\n[12 Feb 2026] Priya: @Ravi Mind giving me until 15 Feb 2026 to fetch the parking permits?\n[12 Feb 2026] Kai: @Priya Of course, it is fine for you to fetch the parking permits by 15 Feb 2026.\n[13 Feb 2026] Kai: @Priya Nobody needs you to fetch the parking permits, that's that\n[13 Feb 2026] Kai: @Priya As long as the team lunch is on, I'll order the office stationery by 18 Feb 2026.\n[15 Feb 2026] Kai: Fab, we are on for the team lunch as planned!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, what is the deadline for Priya to fetch the parking permits at the end of 12 Feb 2026, with any agreed change of date counted?",
  "options": [
   "17 Feb 2026",
   "13 Feb 2026",
   "15 Feb 2026"
  ]
 },
 {
  "qid": "q9e7a878ca7",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the flat upgrade list\nThe thread below comes from Sami and is passed on as it is.\n\nMembers: Hana, Sami\nChat log (oldest first):\n[25 Feb 2026] Hana: @Sami I'll bring the step stool by 5 Mar 2026, providing the electrics safety check goes ahead.\n[25 Feb 2026] Hana: Sad to report that the electrics safety check is off.\n[27 Feb 2026] Sami: @Hana I own this, I'll wipe the cooker hood by 5 Mar 2026.\n[2 Mar 2026] Hana: @Sami You can bet I'll collect the spare flat keys by 7 Mar 2026.\n[2 Mar 2026] Sami: Oh cheers, that helps.\n[2 Mar 2026] Hana: @Sami Is 12 Mar 2026 alright for me to collect the spare flat keys?\n[5 Mar 2026] Sami: @Hana Fine by me, you can collect the spare flat keys by 12 Mar 2026.\n[10 Mar 2026] Hana: @Sami Log entry: collect the spare flat keys, carried out",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs things stand at the end of 16 Mar 2026, which date is the deadline for Hana to collect the spare flat keys, with any agreed change applied?",
  "options": [
   "5 Mar 2026",
   "7 Mar 2026",
   "12 Mar 2026"
  ]
 },
 {
  "qid": "q97f321db88",
  "kind": "choice",
  "text": "Oskar forwarded this support chat about the playground project.\n\nMembers: Leila, Zara, Oskar\nChat export (date | from | to | message):\n2026-03-24 | Oskar | Zara | Guaranteed I'll send the newsletter drafts by 29 Mar 2026.\n2026-03-24 | Zara | group | Thanks mate, noted.\n2026-03-26 | Zara | Leila | I'll set up the book stall by 31 Mar 2026, providing the summer fete goes ahead.\n2026-03-27 | Leila | Zara | I assure you I'll label the raffle prizes by 31 Mar 2026 if the quiz night is on.\n2026-03-28 | Zara | Oskar | Got it, I'll count the donation boxes by 31 Mar 2026 for sure.\n2026-03-28 | Oskar | Zara | No worries, you don't need to count the donation boxes\n2026-03-29 | Oskar | Zara | Is 2 Apr 2026 alright for me to send the newsletter drafts?\n2026-03-29 | Zara | Oskar | Yes, lovely, you can send the newsletter drafts by 2 Apr 2026 instead!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules, when is the date by which Oskar has to send the newsletter drafts at the end of 3 Apr 2026, allowing for any agreed change?",
  "options": [
   "2 Apr 2026",
   "29 Mar 2026",
   "31 Mar 2026"
  ]
 },
 {
  "qid": "q9bdbcda17f",
  "kind": "yes/no",
  "text": "Shared by Yuki, this back and forth with the client covers the campaign edit.\n\nMembers: Ravi, Lee, Yuki\nChat export (date | from | to | message):\n2026-04-14 | Lee | Yuki | Lovely, I'll upload the render files by 23 April 2026 if the festival premiere is on.\n2026-04-16 | Ravi | group | I'm aiming to fetch the raw footage by 25 April 2026, might manage it.\n2026-04-18 | Yuki | group | Sad to report that the festival premiere is off.\n2026-04-18 | Ravi | Yuki | I will fetch the raw footage by 22 April 2026.\n2026-04-19 | Ravi | Yuki | Relax, I'll send the colour notes by 26 April 2026, promise.\n2026-04-25 | Ravi | Yuki | Mum, I did fetch the raw footage, haha.",
  "question": "Is it true under the card's rules that Ravi has kept the promise to fetch the raw footage at the end of 27 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qdfce4c6427",
  "kind": "yes/no",
  "text": "Hana shared this channel export, covering the mobile release for the team.\n\nMembers: Hana, Rhea, Kai\nChat log (oldest first):\n[27 Jan 2026] Rhea: @Hana You can bet I'll fix the test runner by Thursday, February 5, 2026.\n[28 Jan 2026] Hana: @Kai Lovely, I'll rotate the test keys by Monday, February 2, 2026 for sure.\n[1 Feb 2026] Hana: @Kai I'll label the bug reports by Saturday, February 7, 2026, providing the sprint demo goes ahead.\n[2 Feb 2026] Kai: @Hana Quick update: you do not need to rotate the test keys at all.\n[6 Feb 2026] Kai: Yep, the sprint demo is on as planned.\n[9 Feb 2026] Rhea: Where are you up to with plans to rotate the test keys?",
  "question": "At the end of Saturday, February 7, 2026, does the promise Hana made to rotate the test keys have any status except broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd9f7467cfd",
  "kind": "choice",
  "text": "Here is the plan for the reunion weekend, saved by Leila for the group.\n\nMembers: Malik, Leila\nChat log (oldest first):\n[31 Jan 2026] Leila: @Malik Committing to buy the name tags by 8 February 2026.\n[31 Jan 2026] Leila: @Malik Lovely, I'll label the memory box by 8 February 2026 if the reunion lunch is on.\n[2 Feb 2026] Leila: @Malik Ticket's mine, I'll send the group invitations by 5 February 2026.\n[5 Feb 2026] Leila: @Malik Got myself to send the group invitations lol.\n[6 Feb 2026] Malik: @Leila Lovely, I'll print the family tree chart by 13 February 2026 if the garden picnic is on.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Leila made to send the group invitations at the end of 10 February 2026?",
  "options": [
   "Kept",
   "Waived",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q9be9e68a34",
  "kind": "yes/no",
  "text": "Ivo shared this channel export, covering the platform rewrite for the team.\n\nMembers: Ivo, Lee, Mo\nChat log (oldest first):\n[29 Sep 2026] Ivo: @Mo Lovely, I'll merge the login branch by 1 October 2026 if the code freeze is on.\n[29 Sep 2026] Lee: @Mo Committing to update the dependency list by 4 October 2026.\n[29 Sep 2026] Mo: @Lee You are released, no requirement to update the dependency list.\n[30 Sep 2026] Ivo: Just so you know, the code freeze is on as scheduled.\n[2 Oct 2026] Ivo: @Mo Absolutely, I will deploy the staging build by 6 October 2026.",
  "question": "Would a check of the chat at the end of 2 October 2026 show the promise Lee made to update the dependency list as broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q47aac668f2",
  "kind": "yes/no",
  "text": "Forwarded by Omar: a help-desk thread covering the league run.\n\nMembers: Dara, Omar\nChat log (oldest first):\n[7 Oct 2026] Omar: @Dara Only if the presentation evening is on, I will book the changing room by 10 Oct 2026.\n[7 Oct 2026] Omar: @Dara I'll be sure to fetch the medical bag by 14 Oct 2026.\n[7 Oct 2026] Omar: @Dara Might I ask whether I could fetch the medical bag by 20 Oct 2026 instead?\n[8 Oct 2026] Omar: Update, the presentation evening will not take place.\n[12 Oct 2026] Omar: @Dara I have to take back my promise to fetch the medical bag.",
  "question": "At the end of 14 Oct 2026, has the promise Omar made to fetch the medical bag been broken?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q89938d9327",
  "kind": "choice",
  "text": "Our flat chat about the loft conversion, saved by Ines for whoever lives here.\n\nMembers: Ines, Elif, Priya\nChat export (date | from | to | message):\n2026-05-12 | Elif | group | See if I can print the floor plan by 21 May 2026.\n2026-05-14 | Elif | Priya | Provided the builder quote meeting happens, I'll print the floor plan by 19 May 2026.\n2026-05-16 | Ines | group | We are dropping the builder quote meeting from the list.\n2026-05-16 | Priya | Ines | I will make sure to measure the hallway for shelves by 24 May 2026.\n2026-05-16 | Ines | Priya | You don't have to measure the hallway for shelves at all\n2026-05-18 | Priya | Ines | It's on me to return the tile cutter by 22 May 2026.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Elif's promise to print the floor plan at the end of 18 May 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "qb6369ab5b4",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the volunteer roster\nThis export from Mo is pasted in full for readers who want it.\n\nMembers: Kai, Oskar, Mo, Ines\nChat export (date | from | to | message):\n2026-04-05 | Oskar | Mo | You can bank on me to book the school hall by 12 April 2026.\n2026-04-05 | Mo | Ines | You can bet I'll label the raffle prizes by 9 April 2026.\n2026-04-07 | Kai | Oskar | Forget it, you won't need to book the school hall\n2026-04-08 | Mo | Ines | To my relief, I managed to label the raffle prizes.\n2026-04-10 | Mo | Kai | If the governors meeting is on, I'll definitely print the raffle tickets by 13 April 2026.\n2026-04-11 | Oskar | Ines | As long as the field day is on, I will set up the book stall by 14 April 2026.",
  "question": "Has Mo kept the promise to label the raffle prizes at the end of 12 April 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q01ae56b774",
  "kind": "yes/no",
  "text": "Committee chat on the sponsor search, shared by Wren with the volunteers.\n\nMembers: Rhea, Wren, Leila\nChat export (date | from | to | message):\n2026-04-24 | Leila | Wren | Only if the bike check is on, I will collect the timing tags by 1 May 2026.\n2026-04-25 | Leila | Rhea | I'll print the route cards by 29 Apr 2026 as long as the hill climb is on.\n2026-04-25 | Wren | Leila | Relax, I'll pump the spare tyres by 2 May 2026, promise.\n2026-04-26 | Rhea | Leila | I own this, I'll wash the club jerseys by 29 Apr 2026.\n2026-04-28 | Rhea | group | We are dropping the hill climb from the list.\n2026-05-02 | Leila | Wren | No worries, you don't need to pump the spare tyres",
  "question": "Applying the rules on the card, has Wren kept the promise to pump the spare tyres as of 7 May 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8922f30f8c",
  "kind": "choice",
  "text": "Subject: Saved thread about the online store move\nThis export came from Ana and is pasted in full below.\n\nMembers: Rhea, Ana, Ivo, Lee\nChat log (oldest first):\n[18 Aug 2026] Rhea: @Ana As long as the site handover is on, I'll update the product photos by 23 August 2026.\n[20 Aug 2026] Rhea: Team, the site handover stays on as booked.\n[23 Aug 2026] Rhea: @Lee Ticket's mine, I'll add the size chart by 31 August 2026.\n[25 Aug 2026] Rhea: @Lee Gutted to say I won't add the size chart, sorry team\n[25 Aug 2026] Ivo: @Rhea Nobody needs you to add the size chart, that's that",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Rhea's commitment to add the size chart have at the end of 25 August 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Waived",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "q0d0124db4d",
  "kind": "yes/no",
  "text": "Yo flatmates, Arlo shared this chat about the house rules debate, so chip in.\n\nMembers: Arlo, Femi, Ivo\nChat log (oldest first):\n[19 Apr 2026] Arlo: @Ivo Aiming to find the loft ladder by 30 Apr 2026, we'll see.\n[19 Apr 2026] Femi: @Arlo Got it, I'll clear the kitchen sink by 22 Apr 2026 for sure.\n[20 Apr 2026] Arlo: @Femi Lovely, I'll find the loft ladder by 28 Apr 2026 if the heritage fete is on.\n[22 Apr 2026] Femi: @Arlo Think 26 Apr 2026 would work if I clear the kitchen sink instead?\n[22 Apr 2026] Arlo: @Femi Go ahead and clear the kitchen sink by 26 Apr 2026, that is fine.\n[23 Apr 2026] Arlo: Just so you know, the heritage fete is on as scheduled.",
  "question": "Would you say Arlo didn't keep the promise to find the loft ladder by the end of 25 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q08d7ea0f0c",
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
  "qid": "qdfd32a8dc6",
  "kind": "choice",
  "text": "Yo flatmates, Lee shared this chat about the house rules debate, so chip in.\n\nMembers: Lee, Malik, Femi, Greta\nChat log (oldest first):\n[11 Oct 2026] Lee: @Greta Only if the heritage fete is on, I will find the loft ladder by 18 Oct 2026.\n[12 Oct 2026] Greta: Team, the heritage fete is not happening.\n[14 Oct 2026] Greta: @Femi Got it, I'll oil the back door hinges by 19 Oct 2026 for sure.\n[14 Oct 2026] Malik: @Greta Forget it, you won't need to oil the back door hinges\n[17 Oct 2026] Lee: @Greta Quick question, could I find the loft ladder by 23 Oct 2026 instead?\n[17 Oct 2026] Femi: @Lee Go ahead and find the loft ladder by 23 Oct 2026, that is fine.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Lee's promise to find the loft ladder at the end of 19 Oct 2026?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q96a6d6cfc5",
  "kind": "yes/no",
  "text": "Tomas shared this exchange with the client about the honeymoon album.\n\nMembers: Kofi, Tomas, Ivo, Mo\nChat log (oldest first):\n[24 Oct 2026] Kofi: @Ivo Count on me to buy the candle props by Thursday, October 29, 2026, if the bridal shower happens.\n[24 Oct 2026] Tomas: Team, the bridal shower stays on as booked.\n[28 Oct 2026] Mo: @Tomas I will return the lighting stands by Saturday, October 31, 2026.\n[31 Oct 2026] Mo: @Tomas Ticked off my list: return the lighting stands, yay.\n[1 Nov 2026] Kofi: @Mo I will charge the flash batteries by Saturday, November 7, 2026.\n[2 Nov 2026] Ivo: Update on your plan to return the lighting stands?",
  "question": "Under the rules on the card, is the promise Mo made to return the lighting stands in a status other than broken at the end of Saturday, October 31, 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q38e8c6bb0a",
  "kind": "yes/no",
  "text": "Tomas shared this channel export covering the visitor policy for the team.\n\nMembers: Kai, Femi, Tomas\nChat log (oldest first):\n[28 Jun 2026] Kai: @Femi I assure you I'll fetch the parking permits by 7 Jul 2026 if the lease viewing is on.\n[1 Jul 2026] Tomas: Really pleased to say the lease viewing will go ahead!\n[1 Jul 2026] Tomas: @Kai I'll be sure to collect the visitor badges by 4 Jul 2026.\n[2 Jul 2026] Kai: @Tomas Count on me, I'll return the printer toner by 5 Jul 2026.\n[4 Jul 2026] Tomas: @Kai Ta-da, I went and did it: collect the visitor badges!",
  "question": "Is Tomas's promise to collect the visitor badges kept on 4 Jul 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5902da14ac",
  "kind": "yes/no",
  "text": "Tess forwarded this for the committee, covering the choir tour.\n\nMembers: Nadia, Tess, Oskar\nChat log (oldest first):\n[5 Jul 2026] Oskar: @Tess Relax, I'll send the audition reminders by 11 Jul 2026, promise.\n[5 Jul 2026] Nadia: @Oskar No worries, you don't need to send the audition reminders\n[7 Jul 2026] Oskar: @Nadia Committing to buy the spare folders by 12 Jul 2026.\n[7 Jul 2026] Oskar: @Nadia I assure you I'll fix the stand microphones by 12 Jul 2026 if the choir festival is on.\n[7 Jul 2026] Oskar: @Nadia Relax, I'll collect the sheet music by 15 Jul 2026, promise.\n[11 Jul 2026] Tess: Yep, the choir festival is on as planned.",
  "question": "At the end of 11 Jul 2026, does the promise Oskar made to send the audition reminders have any status except broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa1d5721a45",
  "kind": "choice",
  "text": "Our flat chat about the house refit, shared by Ana for whoever lives here.\n\nMembers: Arlo, Ana, Elif\nChat export (date | from | to | message):\n2026-03-10 | Arlo | Ana | I will pick up the grout bag by 17 March 2026.\n2026-03-13 | Arlo | Ana | Think 20 March 2026 would work if I pick up the grout bag instead?\n2026-03-13 | Ana | Arlo | Yes, you have the green light to pick up the grout bag by 20 March 2026.\n2026-03-15 | Arlo | Ana | Mum, I did pick up the grout bag, haha.\n2026-03-20 | Ana | Elif | As long as the kitchen fitting day is on, I'll hang the new curtain rail by 25 March 2026.\n2026-03-21 | Elif | Arlo | You can bet I'll scrape the old wallpaper by 24 March 2026.\n2026-03-24 | Elif | group | Fab, we are on for the kitchen fitting day as planned!",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules, when is the date by which Arlo has to pick up the grout bag at the end of 14 March 2026, allowing for any agreed change?",
  "options": [
   "25 March 2026",
   "20 March 2026",
   "17 March 2026"
  ]
 },
 {
  "qid": "q6fbe55260c",
  "kind": "choice",
  "text": "Rhea shared this family chat about the summer getaway for the relatives.\n\nMembers: Tomas, Lee, Ravi, Rhea\nChat log (oldest first):\n[26 Mar 2026] Tomas: @Rhea I will fill the car boot by 3 April 2026.\n[30 Mar 2026] Lee: @Tomas Lovely, I'll fetch the sunscreen by 5 April 2026 for sure.\n[30 Mar 2026] Rhea: @Tomas Ah, no stress, no need for you to fill the car boot\n[31 Mar 2026] Tomas: @Ravi Provided the beach picnic happens, I will buy the packing cubes by 9 April 2026.\n[31 Mar 2026] Rhea: @Ravi If the flight check-in is on, I'll definitely check the passport copies by 5 April 2026.\n[3 Apr 2026] Tomas: Sad to report that the flight check-in is off.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Tomas's promise to fill the car boot at the end of 30 March 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q7f154a8175",
  "kind": "yes/no",
  "text": "Attached chat: the visitor policy\nShared by: Wren\n\nMembers: Kofi, Wren, Ivo\nChat log (oldest first):\n[30 Mar 2026] Kofi: @Ivo You can bank on me to print the staff rota by 5 April 2026.\n[1 Apr 2026] Kofi: @Wren I'll order the office stationery by 5 April 2026, provided the annual audit happens.\n[1 Apr 2026] Kofi: @Wren I assure you I'll return the printer toner by 6 April 2026 if the coffee morning is on.\n[2 Apr 2026] Kofi: @Ivo You can bet I'll replace the kitchen filters by 10 April 2026.\n[10 Apr 2026] Kofi: @Ivo Got myself to replace the kitchen filters lol.",
  "question": "According to the rules on the card, does the promise Kofi made to replace the kitchen filters have any status except broken at the end of 13 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q246f020078",
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
  "qid": "q8e70f6006b",
  "kind": "yes/no",
  "text": "Rhea shared this channel export covering the data cleanup for the team.\n\nMembers: Nadia, Tess, Hana, Rhea\nChat log (oldest first):\n[4 Mar 2026] Tess: @Nadia I will make sure to restart the build server by March 13, 2026.\n[7 Mar 2026] Hana: @Nadia I'll try to merge the login branch by March 14, 2026, no guarantee.\n[8 Mar 2026] Hana: @Tess You can bet I'll merge the login branch by March 12, 2026.\n[8 Mar 2026] Rhea: @Tess I'll label the bug reports by March 17, 2026, providing the hackathon goes ahead.\n[10 Mar 2026] Hana: @Tess Forget what I said, I won't merge the login branch\n[10 Mar 2026] Hana: @Rhea Count on me to write the release notes by March 13, 2026, if the code freeze happens.",
  "question": "At the end of March 14, 2026, does the promise Hana made to merge the login branch have any status except broken?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q245de27d8e",
  "kind": "yes/no",
  "text": "Ines shared this to pin down the summer lets season, housemates.\n\nMembers: Mo, Lena, Hana, Ines\nChat log (oldest first):\n[19 May 2026] Mo: @Ines Promise to air the spare room by 27 May 2026 if the check out clean goes ahead.\n[22 May 2026] Hana: @Ines Count on me, I'll collect the bed linen by 29 May 2026.\n[22 May 2026] Mo: @Hana Don't sweat it, there's no need to collect the bed linen\n[22 May 2026] Lena: Just so you know, the check out clean is on as scheduled.\n[31 May 2026] Hana: @Ines For the record: I was able to collect the bed linen",
  "question": "On the card, was Hana's promise to collect the bed linen broken, waived, not triggered or not yet due, rather than kept, at the end of 2 Jun 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1c932d4298",
  "kind": "choice",
  "text": "Team channel: the peer review\nExported by Femi.\n\nMembers: Leila, Femi, Zara, Dara\nChat log (oldest first):\n[3 Jun 2026] Femi: @Dara Maybe I can clean the glassware set by 11 June 2026.\n[4 Jun 2026] Leila: @Zara It's on me to collect the lab samples by 13 June 2026.\n[4 Jun 2026] Leila: @Zara Correction, I will not be able to collect the lab samples.\n[5 Jun 2026] Femi: @Dara If the safety inspection goes ahead, I'll clean the glassware set by 12 June 2026.\n[9 Jun 2026] Leila: Yep, the safety inspection is on as planned.\n[12 Jun 2026] Femi: @Dara Ticked off: clean the glassware set, feels so good",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Femi doing with the promise to clean the glassware set at the end of 17 June 2026?",
  "options": [
   "Broken",
   "Waived",
   "Kept",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q453c57f58b",
  "kind": "yes/no",
  "text": "Client thread on the shop rebuild, shared by Leila for the project log.\n\nMembers: Leila, Lena, Bruno\nChat log (oldest first):\n[22 Jun 2026] Leila: @Lena I'll fix the checkout button by 28 June 2026, provided the product photo day happens.\n[24 Jun 2026] Leila: Fab, we are on for the product photo day as planned!\n[25 Jun 2026] Leila: @Lena Mind giving me until 4 July 2026 to fix the checkout button?\n[25 Jun 2026] Leila: @Lena I'll print the packing slips by 29 June 2026, promise.\n[29 Jun 2026] Leila: @Lena Ticked off: fix the checkout button, feels so good",
  "question": "Under the rules on the card, is the promise Leila made to fix the checkout button in a status other than broken at the end of 28 June 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qca570b9717",
  "kind": "yes/no",
  "text": "Here is the summer getaway, posted by Zara for the family to read.\n\nMembers: Ana, Priya, Zara\nChat export (date | from | to | message):\n2026-01-15 | Ana | Zara | I own this, I'll buy the packing cubes by January 19, 2026.\n2026-01-17 | Ana | Zara | Lovely, I'll print the boarding passes by January 20, 2026 if the family cookout is on.\n2026-01-18 | Zara | group | We are dropping the family cookout from the list.\n2026-01-19 | Ana | Zara | Mate, I promised, may I print the boarding passes by January 24, 2026 instead?\n2026-01-19 | Priya | Ana | That suits me, so please print the boarding passes by January 24, 2026 instead.\n2026-01-20 | Ana | Priya | If the ferry crossing goes ahead, I'll gladly book the airport parking by January 23, 2026.",
  "question": "Under the rules on the card, is the promise Ana made to print the boarding passes in a status other than broken at the end of January 18, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q489e011689",
  "kind": "yes/no",
  "text": "Leila forwarded this exchange with the landlord on the guest welcome plan.\n\nMembers: Kai, Sami, Leila\nChat log (oldest first):\n[8 Feb 2026] Sami: @Leila Lovely, I'll air the spare room by 15 Feb 2026 if the guest arrival evening is on.\n[10 Feb 2026] Kai: @Leila Aiming to change the lounge bulb by 15 Feb 2026, we'll see.\n[11 Feb 2026] Leila: Yep, the guest arrival evening is on as planned.\n[12 Feb 2026] Kai: @Sami It's on me to change the lounge bulb by 17 Feb 2026.\n[15 Feb 2026] Sami: @Leila I promise to fill the cleaning cupboard by 22 Feb 2026.\n[17 Feb 2026] Sami: @Kai Nobody needs you to change the lounge bulb, that's that",
  "question": "Under the rules on the card, is the promise Kai made to change the lounge bulb kept as of 17 Feb 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb435d2894d",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the junior section\nThe thread below comes from Zara and is passed on as it is.\n\nMembers: Zara, Kofi\nChat log (oldest first):\n[30 Jun 2026] Kofi: @Zara As long as the cup tie is on, I'll fetch the medical bag by Monday, July 6, 2026.\n[1 Jul 2026] Zara: Sorry all, the cup tie is called off.\n[2 Jul 2026] Zara: @Kofi I'll repair the goal nets by Wednesday, July 8, 2026, promise.\n[6 Jul 2026] Zara: @Kofi Quick question, could I repair the goal nets by Friday, July 10, 2026 instead?\n[6 Jul 2026] Kofi: @Zara Go ahead and repair the goal nets by Friday, July 10, 2026, that is fine.\n[10 Jul 2026] Zara: @Kofi Got myself to repair the goal nets lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Zara's promise to repair the goal nets at the end of Saturday, July 11, 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "qdd7adb8076",
  "kind": "yes/no",
  "text": "Attached chat: the onboarding flow\nShared by: Nadia\n\nMembers: Nadia, Kai, Lee\nChat log (oldest first):\n[14 Aug 2026] Kai: @Lee You can bet I'll label the bug reports by 16 August 2026.\n[14 Aug 2026] Kai: @Lee Scratch that, I'm not going to label the bug reports\n[14 Aug 2026] Nadia: @Kai As long as the hackathon is on, I'll update the dependency list by 16 August 2026.\n[19 Aug 2026] Kai: @Lee I'll restart the build server by 26 August 2026 if the server migration goes ahead.\n[24 Aug 2026] Kai: Lovely, the server migration is definitely happening!\n[26 Aug 2026] Kai: @Lee Quick report: I've managed to restart the build server",
  "question": "Applying the card's rules, can it be said that Kai has not kept the promise to restart the build server at the end of 26 August 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7577078a0d",
  "kind": "yes/no",
  "text": "Attached chat: the shop rebuild\nShared by: Lena\n\nMembers: Lena, Sami, Femi, Tomas\nChat log (oldest first):\n[9 Sep 2026] Lena: @Tomas Committing to add the size chart by 16 September 2026.\n[14 Sep 2026] Tomas: @Sami If the site handover goes ahead, I'll gladly fix the checkout button by 21 September 2026.\n[15 Sep 2026] Lena: @Tomas Mate, I promised, may I add the size chart by 19 September 2026 instead?\n[16 Sep 2026] Tomas: @Lena Yes, you can add the size chart by 19 September 2026 if that suits you.\n[19 Sep 2026] Lena: Update, the site handover will not take place.",
  "question": "Would Lena be counted as having broken the promise to add the size chart at the end of 18 September 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q32b96778b3",
  "kind": "yes/no",
  "text": "Forwarded by Kofi, these tenant replies are about the student house hunt for the file.\n\nMembers: Kofi, Jonas, Mo, Wren\nChat log (oldest first):\n[24 May 2026] Kofi: @Mo I will make sure to ring the letting agent by 27 May 2026.\n[26 May 2026] Mo: @Kofi Provided the move in day happens, I'll return the bin rota by 29 May 2026.\n[26 May 2026] Wren: Yay, the move in day is all set to go!\n[28 May 2026] Kofi: @Wren I will make sure to forward the inventory photos by 5 Jun 2026.\n[1 Jun 2026] Mo: @Kofi Ticked off: return the bin rota, feels so good",
  "question": "Under the rules on the card, is Mo's promise to return the bin rota kept as of 31 May 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q01d0508723",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the volunteer roster\nThis export from Mo is pasted in full for readers who want it.\n\nMembers: Kai, Oskar, Mo, Ines\nChat export (date | from | to | message):\n2026-04-05 | Oskar | Mo | You can bank on me to book the school hall by 12 April 2026.\n2026-04-05 | Mo | Ines | You can bet I'll label the raffle prizes by 9 April 2026.\n2026-04-07 | Kai | Oskar | Forget it, you won't need to book the school hall\n2026-04-08 | Mo | Ines | To my relief, I managed to label the raffle prizes.\n2026-04-10 | Mo | Kai | If the governors meeting is on, I'll definitely print the raffle tickets by 13 April 2026.\n2026-04-11 | Oskar | Ines | As long as the field day is on, I will set up the book stall by 14 April 2026.\n\nModerator ruling: promises in this group count as fine for the record, and the copy shared by Mo confirms it.",
  "question": "Has Mo kept the promise to label the raffle prizes at the end of 12 April 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5592c594b1",
  "kind": "choice",
  "text": "Yuki saved this exchange with the client about the online store move.\n\nMembers: Zara, Elif, Yuki, Ines\nChat log (oldest first):\n[31 May 2026] Zara: @Yuki Relax, I'll restore the old theme by 9 June 2026, promise.\n[3 Jun 2026] Zara: @Elif As long as the stock count is on, I will fix the checkout button by 9 June 2026.\n[4 Jun 2026] Yuki: @Elif If the market day is on, I'll definitely set up the email forwarding by 9 June 2026.\n[5 Jun 2026] Elif: @Yuki I'll add the size chart by 8 June 2026, promise.\n[6 Jun 2026] Elif: @Yuki Is it all right if I add the size chart by 10 June 2026 instead?\n[7 Jun 2026] Ines: @Zara Nobody needs you to restore the old theme, that's that\n[8 Jun 2026] Zara: @Elif Yes, all good for you to add the size chart by 10 June 2026 instead.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, what is the deadline for Elif to add the size chart at the end of 21 June 2026, with any agreed change of date counted?",
  "options": [
   "9 June 2026",
   "8 June 2026",
   "10 June 2026"
  ]
 },
 {
  "qid": "qfe3feb4004",
  "kind": "yes/no",
  "text": "Exported by Mo, this is the full back and forth on the wedding weekend.\n\nMembers: Mo, Arlo, Leila\nChat log (oldest first):\n[10 Apr 2026] Mo: @Leila Relax, I'll set up the backdrop frame by Friday, April 17, 2026 for sure.\n[10 Apr 2026] Mo: @Arlo If the cake tasting goes ahead, I'll gladly collect the venue floor plan by Friday, April 17, 2026.\n[13 Apr 2026] Arlo: @Leila I will print the seating cards by Thursday, April 16, 2026.\n[16 Apr 2026] Arlo: @Leila Forget what I said, I won't print the seating cards\n[18 Apr 2026] Arlo: @Mo Only if the ceremony walkthrough is on, I will fetch the spare memory cards by Thursday, April 23, 2026.",
  "question": "Is Arlo's promise to print the seating cards broken at the end of Friday, April 17, 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q30a6dd4f45",
  "kind": "yes/no",
  "text": "Committee chat on the new term plans, shared by Lee with the volunteers.\n\nMembers: Kofi, Lee, Wren\nChat export (date | from | to | message):\n2026-03-23 | Lee | Kofi | Relax, I'll count the donation boxes by 29 Mar 2026, promise.\n2026-03-26 | Wren | Lee | Count on me to fetch the tea urn by 30 Mar 2026 if the quiz night is on.\n2026-03-27 | Lee | Kofi | My sincere apologies, I am unable to count the donation boxes.\n2026-03-28 | Kofi | Lee | Quick update: you do not need to count the donation boxes at all.\n2026-03-29 | Kofi | group | Scrapping the quiz night, apologies to all.",
  "question": "Does the card classify Lee's promise to count the donation boxes as broken, waived, not triggered or not yet due, rather than kept, on 31 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3065fed357",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the loft conversion\nFrom Ravi, the thread below is shared as it stands.\n\nMembers: Oskar, Ravi, Ana, Malik\nChat export (date | from | to | message):\n2026-07-30 | Ana | Oskar | I'll hang the new curtain rail by Friday, August 7, 2026, providing the kitchen fitting day goes ahead.\n2026-08-02 | Malik | Ana | As long as the boiler install visit is on, I will pick up the grout bag by Tuesday, August 11, 2026.\n2026-08-03 | Ana | Ravi | You can bank on me to return the tile cutter by Monday, August 10, 2026.\n2026-08-06 | Oskar | group | Great news, the kitchen fitting day is on!\n2026-08-06 | Malik | Ana | You don't have to return the tile cutter at all\n2026-08-11 | Ana | Ravi | Got myself to return the tile cutter lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Ana's promise to return the tile cutter at the end of Saturday, August 15, 2026?",
  "options": [
   "Kept",
   "Broken",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "qa577d1692c",
  "kind": "choice",
  "text": "Forwarded by Dara: a help-desk thread covering the field survey.\n\nMembers: Jonas, Sami, Dara\nChat log (oldest first):\n[11 Mar 2026] Jonas: I'll try to scan the field notes by 21 Mar 2026, no guarantee.\n[13 Mar 2026] Jonas: @Dara I'll be sure to scan the field notes by 20 Mar 2026.\n[15 Mar 2026] Dara: @Sami As long as the thesis defence is on, I will print the poster abstracts by 21 Mar 2026.\n[16 Mar 2026] Sami: Please note the thesis defence will proceed.\n[17 Mar 2026] Jonas: @Dara My sincere apologies, I am unable to scan the field notes.\n[19 Mar 2026] Dara: @Jonas Ah, no stress, no need for you to scan the field notes",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Jonas's promise to scan the field notes at the end of 20 Mar 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q7c48b9a61f",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the attic conversion idea\nFrom Nadia, the thread below is shared as it stands.\n\nMembers: Nadia, Ana, Lena\nChat export (date | from | to | message):\n2026-09-30 | Lena | Ana | Lovely, I'll turn the heating timer by 7 October 2026 for sure.\n2026-10-02 | Lena | Ana | I'll sort the recycling bags by 8 October 2026 as long as the lodger house supper is on.\n2026-10-05 | Nadia | group | Please note the lodger house supper will proceed.\n2026-10-05 | Nadia | Lena | Quick update: you do not need to sort the recycling bags at all.\n2026-10-07 | Lena | Ana | For the record: I was able to sort the recycling bags",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Lena's promise to sort the recycling bags sit at the end of 5 October 2026, exactly?",
  "options": [
   "Kept",
   "Waived",
   "Not yet due",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q2eaef84de0",
  "kind": "yes/no",
  "text": "Shared by Yuki, this back and forth with the client covers the campaign edit.\n\nMembers: Ravi, Lee, Yuki\nChat export (date | from | to | message):\n2026-04-14 | Lee | Yuki | Lovely, I'll upload the render files by 23 April 2026 if the festival premiere is on.\n2026-04-16 | Ravi | group | I'm aiming to fetch the raw footage by 25 April 2026, might manage it.\n2026-04-18 | Yuki | group | Sad to report that the festival premiere is off.\n2026-04-18 | Ravi | Yuki | I will fetch the raw footage by 22 April 2026.\n2026-04-19 | Ravi | Yuki | Relax, I'll send the colour notes by 26 April 2026, promise.\n2026-04-25 | Ravi | Yuki | Mum, I did fetch the raw footage, haha.",
  "question": "Was Ravi's promise to fetch the raw footage not kept as of 27 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe3956b54b3",
  "kind": "yes/no",
  "text": "Here is the thread on the flatmate contract terms, posted by Rhea for the house.\n\nMembers: Oskar, Zara, Hana, Rhea\nChat log (oldest first):\n[20 Feb 2026] Hana: @Rhea I'll scan the council tax letter by 2026-02-26 if the move in day goes ahead.\n[22 Feb 2026] Hana: @Oskar Count on me to store the spare bike by 2026-03-01, if the freshers welcome night happens.\n[22 Feb 2026] Oskar: @Rhea Ticket's mine, I'll photograph the bathroom mould by 2026-03-02.\n[24 Feb 2026] Oskar: @Rhea I committed to photograph the bathroom mould, can I do that by 2026-03-06 instead?\n[26 Feb 2026] Oskar: @Rhea Change of plans: I will not photograph the bathroom mould\n[28 Feb 2026] Zara: Sadly, the freshers welcome night is not going ahead.",
  "question": "On 2026-02-26, would you say Oskar kept the promise to photograph the bathroom mould, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa5c1ca054e",
  "kind": "yes/no",
  "text": "Forwarded by Zara: a help-desk thread covering the summer getaway.\n\nMembers: Ana, Priya, Zara\nChat log (oldest first):\n[15 Jan 2026] Ana: @Zara I own this, I'll buy the packing cubes by January 19, 2026.\n[17 Jan 2026] Ana: @Zara Lovely, I'll print the boarding passes by January 20, 2026 if the family cookout is on.\n[18 Jan 2026] Zara: We are dropping the family cookout from the list.\n[19 Jan 2026] Ana: @Zara Mate, I promised, may I print the boarding passes by January 24, 2026 instead?\n[19 Jan 2026] Priya: @Ana That suits me, so please print the boarding passes by January 24, 2026 instead.\n[20 Jan 2026] Ana: @Priya If the ferry crossing goes ahead, I'll gladly book the airport parking by January 23, 2026.",
  "question": "Did Ana break the promise to print the boarding passes at the end of January 18, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6ffb6ade32",
  "kind": "yes/no",
  "text": "Bruno shared this channel export, covering the onboarding flow for the team.\n\nMembers: Bruno, Arlo\nChat export (date | from | to | message):\n2026-01-15 | Arlo | Bruno | It's on me to run the security scan by 20 Jan 2026.\n2026-01-17 | Bruno | Arlo | I'll update the dependency list by 23 Jan 2026 if the planning session goes ahead.\n2026-01-19 | Bruno | Arlo | Guaranteed I'll review the pull request by 27 Jan 2026.\n2026-01-19 | Bruno | Arlo | Scratch that, I'm not going to review the pull request\n2026-01-20 | Bruno | Arlo | I assure you I'll deploy the staging build by 24 Jan 2026 if the code freeze is on.",
  "question": "Would a check of the chat at the end of 19 Jan 2026 show the promise Bruno made to review the pull request as broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
