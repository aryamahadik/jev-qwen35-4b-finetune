# G5-H blind read T32-blind_read-3c0db155-000 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root/T32/qc/g5h/answers/T32-blind_read-3c0db155-000.json

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
  "qid": "q2940d69144",
  "kind": "choice",
  "text": "Kai forwarded this support chat, which is about the documentary cut.\n\nMembers: Arlo, Ines, Kai\nChat export (date | from | to | message):\n2026-09-16 | Kai | Ines | Lovely, I'll upload the render files by 21 Sep 2026 if the festival premiere is on.\n2026-09-17 | Arlo | Ines | Absolutely, I will label the clip folders by 22 Sep 2026.\n2026-09-17 | Arlo | Ines | Can I label the clip folders by 28 Sep 2026 instead? I did promise, sorry.\n2026-09-20 | Ines | Arlo | Fine by me, you can label the clip folders by 28 Sep 2026.\n2026-09-20 | Ines | group | Just so you know, the festival premiere is on as scheduled.\n2026-09-21 | Kai | Arlo | Relax, mate, you're not expected to label the clip folders",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Arlo's commitment to label the clip folders have at the end of 26 Sep 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q188bd67ad4",
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
  "qid": "qc3506afa16",
  "kind": "yes/no",
  "text": "Shared by Rhea, this work thread covers the platform rewrite.\n\nMembers: Rhea, Kofi\nChat log (oldest first):\n[13 Jul 2026] Kofi: @Rhea Provided the sprint demo happens, I will update the dependency list by Thursday, July 16, 2026.\n[14 Jul 2026] Rhea: @Kofi I'll restart the build server by Thursday, July 23, 2026 as long as the planning session is on.\n[14 Jul 2026] Kofi: @Rhea Got it, I'll fix the test runner by Friday, July 17, 2026 for sure.\n[15 Jul 2026] Rhea: @Kofi Committing to run the security scan by Sunday, July 19, 2026.\n[15 Jul 2026] Kofi: Please note the sprint demo will proceed.\n[16 Jul 2026] Rhea: @Kofi Guess what, I managed to run the security scan!",
  "question": "Under the rules on the card, is Rhea's promise to run the security scan broken, waived, not triggered or not yet due, rather than kept, as of Tuesday, July 21, 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3d54831e69",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the lab move\nThe chat below comes from Lena, copied as is for reference.\n\nMembers: Priya, Lena, Yuki\nChat log (oldest first):\n[20 Mar 2026] Yuki: @Lena Provided the thesis defence happens, I'll submit the ethics application by Thursday, March 26, 2026.\n[20 Mar 2026] Lena: Update, the thesis defence will not take place.\n[22 Mar 2026] Yuki: @Priya Guaranteed I'll return the library books by Wednesday, March 25, 2026.\n[22 Mar 2026] Priya: @Lena Lovely, I'll book the microscope slot by Saturday, March 28, 2026 if the journal club is on.\n[24 Mar 2026] Lena: @Priya Ticket's mine, I'll clean the glassware set by Monday, March 30, 2026.\n[26 Mar 2026] Yuki: @Priya Got myself to return the library books lol.",
  "question": "According to the card's rules, is the promise Yuki made to return the library books not kept as of Saturday, March 28, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4c49d3b075",
  "kind": "choice",
  "text": "Work channel export: the field survey, shared by Greta.\n\nMembers: Greta, Hana, Dara, Arlo\nChat log (oldest first):\n[23 Mar 2026] Hana: @Greta I promise to submit the ethics application by 26 Mar 2026.\n[25 Mar 2026] Hana: @Greta Think 29 Mar 2026 would work if I submit the ethics application instead?\n[25 Mar 2026] Dara: @Hana Revised deadline is 29 Mar 2026, so you can submit the ethics application.\n[26 Mar 2026] Arlo: @Hana I'll clean the glassware set by 1 Apr 2026 if the thesis defence goes ahead.\n[27 Mar 2026] Dara: Sorry, the thesis defence is off.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Hana's promise to submit the ethics application turn out at the end of 29 Mar 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Not yet due",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q3ec483d980",
  "kind": "choice",
  "text": "Group thread for the work team about the website relaunch, passed on by Ravi.\n\nMembers: Lena, Malik, Ravi, Nadia\nChat export (date | from | to | message):\n2026-10-12 | Malik | Nadia | I'll try to pay the printing invoice by 14 Oct 2026, no guarantee.\n2026-10-13 | Malik | Lena | If the brand photo shoot goes ahead, I'll gladly pay the printing invoice by 16 Oct 2026.\n2026-10-14 | Malik | Ravi | Count on me to draft the press release by 17 Oct 2026.\n2026-10-14 | Malik | Ravi | Sorry, I won't draft the press release after all\n2026-10-14 | Nadia | group | Great news, the brand photo shoot is on!\n2026-10-15 | Malik | Lena | Think 18 Oct 2026 would work if I pay the printing invoice instead?\n2026-10-16 | Ravi | Malik | Yes, you can pay the printing invoice by 18 Oct 2026 if that suits you.\n2026-10-16 | Malik | Lena | Log entry: pay the printing invoice, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhen does Malik have to pay the printing invoice by, at the end of 15 Oct 2026, once any agreed date change is included?",
  "options": [
   "18 Oct 2026",
   "16 Oct 2026",
   "17 Oct 2026"
  ]
 },
 {
  "qid": "q69cbcac305",
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
  "qid": "qc3c2d6e3f4",
  "kind": "choice",
  "text": "Volunteers, here is the new term plans thread that Bruno forwarded for us.\n\nMembers: Yuki, Wren, Leila, Bruno\nChat export (date | from | to | message):\n2026-05-20 | Leila | Bruno | I assure you I'll set up the book stall by 25 May 2026 if the quiz night is on.\n2026-05-21 | Wren | Bruno | I will make sure to wrap the prize hampers by 29 May 2026.\n2026-05-22 | Leila | Wren | Absolutely, I will print the raffle tickets by 30 May 2026.\n2026-05-24 | Bruno | group | Sadly, the quiz night won't go ahead.\n2026-05-24 | Wren | Bruno | Guess who managed to wrap the prize hampers, go team!\n2026-05-28 | Leila | Wren | I need to take back my commitment to print the raffle tickets.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of 26 May 2026, which status does Wren have for the promise to wrap the prize hampers?",
  "options": [
   "Not triggered",
   "Broken",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qbeeadb177a",
  "kind": "yes/no",
  "text": "Saved by Elif, this copy of the support chat concerns the street watch scheme.\n\nMembers: Jonas, Ana, Oskar, Elif\nChat log (oldest first):\n[28 Oct 2026] Oskar: @Ana You can bank on me to lend the stepladder by 1 November 2026.\n[30 Oct 2026] Jonas: @Ana Relax, I'll share the garden hose by 5 November 2026, promise.\n[2 Nov 2026] Jonas: @Ana Count on me to sweep the pavement outside by 4 November 2026, if the parking permit visit happens.\n[3 Nov 2026] Elif: Brilliant news everyone, the parking permit visit is a go!\n[3 Nov 2026] Jonas: @Ana Can I share the garden hose by 7 November 2026 instead? I did promise, sorry.\n[6 Nov 2026] Jonas: @Ana To my relief, I managed to share the garden hose.\n\nGroup admin reminder: the chat's changes need no further checks, since Elif is covered by the admin sign-off.",
  "question": "Does the chat, checked at the end of 6 November 2026, show that Jonas has broken the promise to share the garden hose?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qde8b6f69aa",
  "kind": "choice",
  "text": "Work conversation on the spring campaign, saved as a file by Ines.\n\nMembers: Hana, Sami, Ines\nChat export (date | from | to | message):\n2026-09-09 | Sami | Ines | Relax, I'll book the photo studio by 11 September 2026, promise.\n2026-09-09 | Ines | Sami | I'll return the rented camera gear by 11 September 2026 as long as the influencer call is on.\n2026-09-10 | Sami | group | Team, the influencer call is not happening.\n2026-09-11 | Hana | Ines | I will fix the landing page headline by 17 September 2026 only if the trade fair stand happens.\n2026-09-12 | Hana | Sami | I will make sure to print the event banners by 15 September 2026.\n2026-09-13 | Ines | Hana | Please don't feel you have to print the event banners",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Hana made to print the event banners have at the end of 18 September 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Waived",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q66b2c98e25",
  "kind": "choice",
  "text": "Subject: copy of a chat on the vegetable plot plan\nPassing this along, with the chat text under it, from Lena.\n\nMembers: Lena, Femi, Ravi\nChat log (oldest first):\n[23 May 2026] Femi: @Ravi Ticket's mine, I'll stake the tomato canes by 1 Jun 2026.\n[23 May 2026] Lena: @Femi I'm aiming to sharpen the hand hoe by 2 Jun 2026, might manage it.\n[24 May 2026] Ravi: @Femi I'll fix the shed door by 29 May 2026, promise.\n[25 May 2026] Lena: @Femi As long as the village flower show is on, I will sharpen the hand hoe by 31 May 2026.\n[25 May 2026] Ravi: Sorry, the village flower show is off.\n[31 May 2026] Femi: @Ravi Guess what, I managed to stake the tomato canes!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status does the chat show for the promise Lena made to sharpen the hand hoe at the end of 3 Jun 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Waived",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "q9ee122544b",
  "kind": "yes/no",
  "text": "Subject: saved chat, the old house restoration\nBelow is the chat that Mo saved for reference.\n\nMembers: Ravi, Mo\nChat log (oldest first):\n[17 Oct 2026] Ravi: @Mo Lovely, I'll tidy the boot room by 23 Oct 2026 for sure.\n[17 Oct 2026] Ravi: @Mo Promise to defrost the old fridge by 22 Oct 2026 if the heritage fete goes ahead.\n[18 Oct 2026] Ravi: @Mo I will wash the sash windows by 22 Oct 2026 only if the loft clearance day happens.\n[19 Oct 2026] Ravi: @Mo Will attempt to find the loft ladder by 29 Oct 2026, can't promise.\n[21 Oct 2026] Ravi: @Mo Absolutely, I will find the loft ladder by 27 Oct 2026.\n[28 Oct 2026] Ravi: @Mo Log entry: find the loft ladder, carried out",
  "question": "Applying the rules on the card, did Ravi break the promise to find the loft ladder at the end of 30 Oct 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q24a45e7634",
  "kind": "choice",
  "text": "{\"source\": \"saved thread\", \"about\": \"the new kit design\", \"owner\": \"Ravi\", \"kind\": \"chat export\"}\n\nMembers: Wren, Lena, Ravi\nChat log (oldest first):\n[24 Mar 2026] Ravi: @Wren Promise to tune the gear cables by 31 March 2026 if the hill climb goes ahead.\n[26 Mar 2026] Wren: @Ravi Guaranteed I'll return the loaned helmets by 28 March 2026.\n[26 Mar 2026] Ravi: @Wren No need to return the loaned helmets, I'm letting you off\n[28 Mar 2026] Ravi: Brilliant news everyone, the hill climb is a go!\n[31 Mar 2026] Ravi: @Wren For the record: I was able to tune the gear cables",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Ravi's promise to tune the gear cables at the end of 5 April 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Broken",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q4d0427b578",
  "kind": "choice",
  "text": "Shared by Arlo, this record holds tenant and landlord messages on the rent split plan.\n\nMembers: Lena, Femi, Arlo, Dara\nChat log (oldest first):\n[18 Jun 2026] Arlo: @Lena You can bank on me to return the bin rota by 28 June 2026.\n[19 Jun 2026] Femi: @Dara If the gas safety inspection goes ahead, I'll print the tenancy agreement by 27 June 2026.\n[20 Jun 2026] Lena: Sad to report that the gas safety inspection is off.\n[20 Jun 2026] Arlo: @Dara I will make sure to copy the house keys by 22 June 2026.\n[20 Jun 2026] Dara: @Arlo Nobody needs you to copy the house keys, that's that\n[21 Jun 2026] Lena: @Femi I promise to photograph the bathroom mould by 29 June 2026 if the house hunting viewing is on.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Femi's pledge to print the tenancy agreement at the end of 27 June 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Waived",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "qba803a46be",
  "kind": "choice",
  "text": "Forwarded by Mo, these tenant replies are about the balcony garden project for the file.\n\nMembers: Nadia, Hana, Mo, Yuki\nChat log (oldest first):\n[16 Jun 2026] Nadia: @Mo If the lease renewal call goes ahead, I'll gladly drop the bin bags off by 2026-06-21.\n[21 Jun 2026] Hana: @Yuki Relax, I'll remove the bathroom shelf by 2026-06-26 for sure.\n[22 Jun 2026] Hana: @Yuki Might I ask whether I could remove the bathroom shelf by 2026-06-30 instead?\n[24 Jun 2026] Hana: @Nadia Promise to email the leak photos by 2026-07-01 if the rent review meeting goes ahead.\n[25 Jun 2026] Nadia: @Hana Good news, you're let off having to remove the bathroom shelf",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Hana's pledge to remove the bathroom shelf at the end of 2026-06-30?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q5bb25853e9",
  "kind": "yes/no",
  "text": "Here is the thread on the garden shed build, posted by Kofi for the house.\n\nMembers: Kofi, Kai, Jonas, Sami\nChat log (oldest first):\n[6 Mar 2026] Kofi: @Jonas Promise to dig the potato patch by 10 March 2026 if the water tank delivery goes ahead.\n[7 Mar 2026] Kofi: @Jonas I promise to weed the carrot row by 12 March 2026.\n[7 Mar 2026] Kofi: @Jonas Log entry: weed the carrot row, carried out\n[8 Mar 2026] Jonas: Team, the water tank delivery stays on as booked.\n[9 Mar 2026] Kofi: @Jonas Any chance I can dig the potato patch by 13 March 2026 instead?",
  "question": "Did Kofi keep the promise to dig the potato patch as of 10 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb6713a5408",
  "kind": "yes/no",
  "text": "Posted by Wren from the work channel: the grant renewal.\n\nMembers: Zara, Wren, Yuki\nChat log (oldest first):\n[28 Jul 2026] Wren: @Yuki If the grant panel goes ahead, I'll gladly return the library books by 1 August 2026.\n[30 Jul 2026] Zara: @Yuki I will make sure to print the poster abstracts by 3 August 2026.\n[30 Jul 2026] Wren: @Zara Good news, you're let off having to print the poster abstracts\n[31 Jul 2026] Zara: @Yuki As long as the thesis defence is on, I will collect the lab samples by 6 August 2026.\n[3 Aug 2026] Wren: Lovely, the thesis defence is definitely happening!\n[6 Aug 2026] Zara: @Yuki Quick report: I've managed to collect the lab samples",
  "question": "By the end of 10 August 2026, has Zara kept the promise to collect the lab samples?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc8748a4569",
  "kind": "yes/no",
  "text": "Local volunteer export\nSaved by Ines, covering the topic of the league run.\n\nMembers: Ana, Ines\nChat log (oldest first):\n[22 May 2026] Ines: I'll try to book the changing room by 30 May 2026, no promises.\n[23 May 2026] Ines: @Ana Provided the pre-season friendly happens, I'll book the changing room by 27 May 2026.\n[24 May 2026] Ana: Yay, the pre-season friendly is all set to go!\n[25 May 2026] Ines: @Ana Relax, I'll set up the corner flags by 28 May 2026 for sure.\n[25 May 2026] Ines: @Ana I'm withdrawing my promise to set up the corner flags\n[3 Jun 2026] Ines: @Ana Log entry: book the changing room, carried out",
  "question": "According to the rules on the card, is it true that the promise Ines made to book the changing room has not been broken at the end of 31 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7c8491cf46",
  "kind": "choice",
  "text": "Subject: saved chat, the platform rewrite\nBelow is the chat that Jonas saved for reference.\n\nMembers: Jonas, Oskar, Kai\nChat log (oldest first):\n[5 Aug 2026] Oskar: @Kai I'll run the security scan by Sunday, 9 August 2026, promise.\n[7 Aug 2026] Kai: @Oskar Don't sweat it, there's no need to run the security scan\n[10 Aug 2026] Jonas: @Kai If the penetration test is on, I'll definitely merge the login branch by Monday, 17 August 2026.\n[10 Aug 2026] Oskar: Lovely, the penetration test is definitely happening!\n[17 Aug 2026] Kai: @Jonas Good news, you're let off having to merge the login branch",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Jonas's pledge to merge the login branch sit at the end of Wednesday, 19 August 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not yet due",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "qc9de5e62ae",
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
  "qid": "q8fd387dabc",
  "kind": "choice",
  "text": "{\"source\": \"saved thread\", \"about\": \"the showreel refresh\", \"owner\": \"Priya\", \"kind\": \"chat export\"}\n\nMembers: Priya, Malik, Rhea\nChat export (date | from | to | message):\n2026-10-01 | Rhea | Malik | I'll record the voice over by Wednesday, October 7, 2026, provided the festival premiere happens.\n2026-10-01 | Priya | Rhea | Got it, I'll send the colour notes by Friday, October 9, 2026 for sure.\n2026-10-02 | Priya | Rhea | I'll be sure to fetch the raw footage by Thursday, October 8, 2026.\n2026-10-02 | Priya | Malik | You can bank on me to label the clip folders by Saturday, October 10, 2026.\n2026-10-04 | Malik | group | Yay, the festival premiere is all set to go!\n2026-10-07 | Rhea | Malik | For the record: I was able to record the voice over",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Rhea's promise to record the voice over at the end of Tuesday, October 6, 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Kept",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q2ad37a38cd",
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
  "qid": "qe90c0ecc0f",
  "kind": "yes/no",
  "text": "Hana shared this so the speed bump plan is easy to find, flatmates.\n\nMembers: Greta, Malik, Hana\nChat log (oldest first):\n[10 Aug 2026] Hana: @Greta I'll try to feed the cat across the road by 12 August 2026, can't promise!\n[11 Aug 2026] Hana: @Greta Committing to feed the cat across the road by 14 August 2026.\n[12 Aug 2026] Greta: @Hana If the road works meeting goes ahead, I'll share the garden hose by 17 August 2026.\n[15 Aug 2026] Hana: @Greta To my relief, I managed to feed the cat across the road.\n[15 Aug 2026] Greta: @Malik I'll sweep the pavement outside by 22 August 2026, promise.\n[16 Aug 2026] Hana: @Greta I'll lock the side gate by 23 August 2026, providing the parking permit visit goes ahead.",
  "question": "Is Hana's promise to feed the cat across the road kept as of 15 August 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q90494942de",
  "kind": "choice",
  "text": "Subject: the menu redesign\nBelow is the group chat that Leila saved, unedited.\n\nMembers: Sami, Rhea, Leila, Femi\nChat log (oldest first):\n[11 Aug 2026] Rhea: @Femi I promise to export the logo files by Sunday, 16 August 2026.\n[14 Aug 2026] Rhea: @Sami Count on me to update the icon set by Saturday, 22 August 2026 if the brand review call is on.\n[14 Aug 2026] Leila: Sadly, the brand review call won't go ahead.\n[18 Aug 2026] Rhea: @Sami Can I update the icon set by Monday, 24 August 2026 instead? I did promise, sorry.\n[20 Aug 2026] Femi: @Rhea Yes, fine to update the icon set by Monday, 24 August 2026 instead.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Rhea's promise to update the icon set receive at the end of Sunday, 23 August 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Waived",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q61bf492a76",
  "kind": "choice",
  "text": "Note on the support case\nWhat it covers: the sponsor search\nPulled by: Leila\n\nMembers: Leila, Dara, Lee, Rhea\nChat log (oldest first):\n[2 Oct 2026] Lee: @Rhea I'll tune the gear cables by October 9, 2026, provided the swap meet happens.\n[4 Oct 2026] Leila: Sorry all, the swap meet is not happening.\n[6 Oct 2026] Dara: @Lee You can bank on me to return the loaned helmets by October 11, 2026.\n[6 Oct 2026] Leila: @Rhea Got it, I'll print the route cards by October 9, 2026 for sure.\n[11 Oct 2026] Dara: @Lee Is it all right if I return the loaned helmets by October 13, 2026 instead?\n[11 Oct 2026] Rhea: @Dara Yes, you have the green light to return the loaned helmets by October 13, 2026.\n[16 Oct 2026] Dara: @Lee Quick report: I've managed to return the loaned helmets",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIf the chat is checked at the end of October 19, 2026, which date marks the deadline for Dara to return the loaned helmets, with agreed date changes included?",
  "options": [
   "October 9, 2026",
   "October 13, 2026",
   "October 11, 2026"
  ]
 },
 {
  "qid": "qa4e2464600",
  "kind": "choice",
  "text": "Chat attached to a support case about the travel plans, shared by Hana.\n\nMembers: Hana, Tomas, Malik\nChat export (date | from | to | message):\n2026-07-04 | Malik | Tomas | Provided the guided tour happens, I will return the rental car keys by 7 Jul 2026.\n2026-07-06 | Malik | group | Yep, the guided tour is on as planned.\n2026-07-10 | Hana | Tomas | Relax, I'll fill the car boot by 16 Jul 2026 for sure.\n2026-07-16 | Hana | Tomas | Think 19 Jul 2026 would work if I fill the car boot instead?\n2026-07-16 | Tomas | Hana | Not moving it, fill the car boot by the existing date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Malik's promise to return the rental car keys at the end of 10 Jul 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "qba43d0857d",
  "kind": "yes/no",
  "text": "Greta forwarded this support chat, which is about the rent split plan.\n\nMembers: Priya, Sami, Greta\nChat export (date | from | to | message):\n2026-06-09 | Sami | Greta | I'll scan the council tax letter by 2026-06-11, provided the house hunting viewing happens.\n2026-06-09 | Sami | Priya | I'll be sure to copy the house keys by 2026-06-14.\n2026-06-10 | Greta | group | Update, the house hunting viewing will not take place.\n2026-06-11 | Sami | Priya | I will make sure to print the tenancy agreement by 2026-06-16.\n2026-06-12 | Sami | Priya | Mum, I did print the tenancy agreement, haha.",
  "question": "Was the promise to print the tenancy agreement from Sami kept on 2026-06-17?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc729ad9128",
  "kind": "choice",
  "text": "Pasted into the project log by Zara, the thread with a client about the big day.\n\nMembers: Femi, Lee, Ivo, Zara\nChat log (oldest first):\n[16 Jan 2026] Femi: Aiming to return the lighting stands by 29 January 2026, we'll see.\n[18 Jan 2026] Femi: @Zara Provided the bridal shower happens, I will return the lighting stands by 25 January 2026.\n[20 Jan 2026] Zara: Yep, the bridal shower is on as planned.\n[25 Jan 2026] Femi: @Zara Would it be fine if I return the lighting stands by 30 January 2026 instead, yeah?\n[25 Jan 2026] Lee: @Femi Go ahead and return the lighting stands by 30 January 2026, that is fine.\n[29 Jan 2026] Lee: @Ivo Count on me to print the seating cards by 31 January 2026.\n[31 Jan 2026] Lee: @Ivo Is it all right if I print the seating cards by 2 February 2026 instead?\n[31 Jan 2026] Ivo: @Lee Go ahead and print the seating cards by 2 February 2026, that is fine.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Femi to return the lighting stands at the end of 6 February 2026, counting any agreed change of date?",
  "options": [
   "25 January 2026",
   "30 January 2026",
   "31 January 2026"
  ]
 },
 {
  "qid": "qb60fe5a604",
  "kind": "yes/no",
  "text": "Client messages for a freelancer about the campaign edit, saved by Ravi.\n\nMembers: Hana, Ravi, Bruno\nChat export (date | from | to | message):\n2026-02-05 | Bruno | Hana | No promises, but I'll aim to back up the project drives by 14 February 2026.\n2026-02-07 | Bruno | Ravi | I will make sure to back up the project drives by 13 February 2026.\n2026-02-07 | Ravi | Hana | I'll order the stock music licence by 16 February 2026 as long as the agency review call is on.\n2026-02-10 | Ravi | Bruno | Got it, I'll ship the hard drive by 14 February 2026 for sure.\n2026-02-13 | Bruno | Ravi | Guess what, I managed to back up the project drives!\n2026-02-13 | Hana | group | Great news, the agency review call is on!",
  "question": "Did Bruno keep the promise to back up the project drives on 14 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q46de2c3128",
  "kind": "yes/no",
  "text": "Thread filed under support\nAbout the new term plans, saved by Elif.\n\nMembers: Oskar, Sami, Elif, Mo\nChat export (date | from | to | message):\n2026-07-09 | Oskar | Elif | See if I can fetch the tea urn by 13 July 2026.\n2026-07-11 | Oskar | Mo | Ticket's mine, I'll fetch the tea urn by 17 July 2026.\n2026-07-14 | Elif | Oskar | Nobody needs you to fetch the tea urn, that's that\n2026-07-16 | Mo | Elif | Provided the reading festival happens, I'll wrap the prize hampers by 24 July 2026.\n2026-07-18 | Oskar | Mo | Quick report: I've managed to fetch the tea urn\n2026-07-21 | Mo | group | Scrapping the reading festival, apologies to all.",
  "question": "As the rules on the card set out, is it the case that Oskar has broken the promise to fetch the tea urn at the end of 16 July 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q15db858679",
  "kind": "yes/no",
  "text": "Family group chat with housemates, covering the reunion planning, exported by Ivo.\n\nMembers: Oskar, Ivo\nChat log (oldest first):\n[20 Mar 2026] Ivo: @Oskar Absolutely, I will fetch the speaker system by 23 Mar 2026.\n[23 Mar 2026] Ivo: @Oskar Lovely, I'll buy the name tags by 29 Mar 2026 if the cousin brunch is on.\n[25 Mar 2026] Ivo: @Oskar To note: I have managed to fetch the speaker system\n[26 Mar 2026] Oskar: Yep, the cousin brunch is on as planned.\n[29 Mar 2026] Ivo: @Oskar Mate, I promised, may I buy the name tags by 4 Apr 2026 instead?\n[29 Mar 2026] Ivo: @Oskar To my relief, I managed to buy the name tags.",
  "question": "Under the rules on the card, is the promise Ivo made to buy the name tags broken at the end of 1 Apr 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q33dd94ffa1",
  "kind": "yes/no",
  "text": "The family thread was saved by Kofi, and its subject is the street watch scheme.\n\nMembers: Hana, Kofi, Dara\nChat log (oldest first):\n[23 Apr 2026] Dara: @Hana I own this, I'll feed the cat across the road by 2 May 2026.\n[26 Apr 2026] Dara: @Hana You can bet I'll return the ladders by 3 May 2026.\n[27 Apr 2026] Dara: @Kofi Count on me to take in the post by 30 Apr 2026, if the road works meeting happens.\n[27 Apr 2026] Dara: Really pleased to say the road works meeting will go ahead!\n[28 Apr 2026] Dara: @Kofi Scratch what I said, I won't take in the post.",
  "question": "Did Dara keep the promise to take in the post as of 28 Apr 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qeac833a2ea",
  "kind": "yes/no",
  "text": "Neighbour and flatmate talk, copied out by Nadia: the old house restoration.\n\nMembers: Hana, Nadia, Sami\nChat log (oldest first):\n[19 Mar 2026] Nadia: @Hana Provided the roof survey visit happens, I'll defrost the old fridge by 23 March 2026.\n[22 Mar 2026] Sami: Quick heads up, the roof survey visit is scrapped.\n[23 Mar 2026] Hana: @Nadia Lovely, I'll tidy the boot room by 30 March 2026 for sure.\n[24 Mar 2026] Sami: @Hana You are released, no requirement to tidy the boot room.\n[24 Mar 2026] Hana: @Nadia Ticked off my list: tidy the boot room, yay.",
  "question": "Is the promise Hana made to tidy the boot room not kept by 28 March 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbdd333332e",
  "kind": "choice",
  "text": "Club and committee chat, saved by Arlo, with the choir tour in the middle.\n\nMembers: Hana, Arlo, Dara\nChat log (oldest first):\n[26 Jan 2026] Dara: @Arlo I'll try to fetch the choir robes by 2026-01-29, no guarantee.\n[28 Jan 2026] Dara: @Arlo I'll fetch the choir robes by 2026-02-01 as long as the voice test is on.\n[28 Jan 2026] Hana: Yay, the voice test is all set to go!\n[29 Jan 2026] Hana: @Dara Nobody needs you to fetch the choir robes, that's that\n[1 Feb 2026] Dara: @Hana I'll be sure to fix the stand microphones by 2026-02-10.\n[8 Feb 2026] Dara: @Hana Scratch that, I'm not going to fix the stand microphones",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Dara made to fetch the choir robes is in which status at the end of 2026-02-01?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "q74a790947c",
  "kind": "choice",
  "text": "This export holds the messages about the guest travel plans, which Tess saved.\n\nMembers: Mo, Ana, Leila, Tess\nChat log (oldest first):\n[31 Oct 2026] Tess: @Leila I'll collect the old photo prints by 9 November 2026 if the reunion lunch goes ahead.\n[2 Nov 2026] Leila: @Mo I'll send the group invitations by 9 November 2026 as long as the garden picnic is on.\n[3 Nov 2026] Leila: @Ana I will buy the name tags by 10 November 2026.\n[5 Nov 2026] Leila: @Ana Sorry, I won't buy the name tags after all\n[7 Nov 2026] Ana: @Leila No need to buy the name tags, I'm letting you off",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Leila made to buy the name tags have at the end of 12 November 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q00b1033b55",
  "kind": "yes/no",
  "text": "This export holds the messages about the care plan, which Zara saved.\n\nMembers: Mo, Zara, Lena\nChat log (oldest first):\n[8 Jul 2026] Zara: Might manage to drop off the hot meals by 20 July 2026, who knows.\n[10 Jul 2026] Zara: @Lena Provided the home assessment happens, I will drop off the hot meals by 17 July 2026.\n[13 Jul 2026] Zara: @Lena Count on me, I'll set up the medicine dispenser by 19 July 2026.\n[15 Jul 2026] Mo: Lovely, the home assessment is definitely happening!\n[17 Jul 2026] Zara: @Lena Is 20 July 2026 alright for me to drop off the hot meals?\n[17 Jul 2026] Zara: @Lena Gutted to say I won't drop off the hot meals, sorry team",
  "question": "Applying the rules on the card, has Zara kept the promise to drop off the hot meals as of 20 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q31fd174cfa",
  "kind": "choice",
  "text": "Work conversation on the website relaunch, saved as a file by Priya.\n\nMembers: Kai, Priya, Wren\nChat export (date | from | to | message):\n2026-10-07 | Priya | Wren | I'll see if I can fix the landing page headline by 11 October 2026.\n2026-10-09 | Kai | Wren | Count on me to fetch the campaign budget sheet by 15 October 2026, if the influencer call happens.\n2026-10-09 | Priya | Wren | I will make sure to fix the landing page headline by 14 October 2026.\n2026-10-10 | Priya | group | Sadly, the influencer call won't go ahead.\n2026-10-10 | Wren | Priya | Forget it, you won't need to fix the landing page headline\n2026-10-14 | Priya | Wren | Log entry: fix the landing page headline, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Priya's promise to fix the landing page headline receive at the end of 19 October 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Not yet due",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q02394bf351",
  "kind": "yes/no",
  "text": "Subject: Chat about the winter concert\nBelow is a copy that came from Hana, pasted as found.\n\nMembers: Hana, Wren, Ines, Kai\nChat log (oldest first):\n[24 Jul 2026] Hana: @Kai Only if the joint concert is on, I will return the library scores by 31 July 2026.\n[24 Jul 2026] Hana: Quick heads up, the joint concert is scrapped.\n[25 Jul 2026] Kai: @Hana You can bank on me to buy the spare folders by 1 August 2026.\n[27 Jul 2026] Ines: @Kai I'll be sure to move the piano by 30 July 2026.\n[30 Jul 2026] Ines: @Kai To my relief, I managed to move the piano.\n[4 Aug 2026] Wren: Anything new on your way to move the piano?",
  "question": "According to the rules on the card, does the promise Ines made to move the piano have any status except broken at the end of 5 August 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5fb62602aa",
  "kind": "choice",
  "text": "Support thread for a help desk case, covering the league run, saved by Lena.\n\nMembers: Femi, Omar, Lena, Sami\nChat log (oldest first):\n[6 Sep 2026] Femi: @Omar Relax, I'll fetch the medical bag by 14 September 2026 for sure.\n[6 Sep 2026] Lena: @Femi I promise to set up the corner flags by 11 September 2026.\n[10 Sep 2026] Sami: @Omar As long as the cup tie is on, I will collect the referee whistles by 15 September 2026.\n[11 Sep 2026] Omar: Update: the cup tie is going ahead as planned.\n[12 Sep 2026] Sami: @Omar I committed to collect the referee whistles, can I do that by 18 September 2026 instead?\n[13 Sep 2026] Femi: @Sami Yes, you're welcome to collect the referee whistles by 18 September 2026 instead.\n[18 Sep 2026] Sami: @Omar Log entry: collect the referee whistles, carried out",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nFollowing the rules set out on the card, what date governs Sami's commitment to collect the referee whistles at the end of 23 September 2026, once any agreed shift in the date is factored in?",
  "options": [
   "18 September 2026",
   "15 September 2026",
   "11 September 2026"
  ]
 },
 {
  "qid": "q0f32a269b5",
  "kind": "yes/no",
  "text": "Subject: Chat about the winter concert\nBelow is a copy that came from Hana, pasted as found.\n\nMembers: Hana, Wren, Ines, Kai\nChat log (oldest first):\n[24 Jul 2026] Hana: @Kai Only if the joint concert is on, I will return the library scores by 31 July 2026.\n[24 Jul 2026] Hana: Quick heads up, the joint concert is scrapped.\n[25 Jul 2026] Kai: @Hana You can bank on me to buy the spare folders by 1 August 2026.\n[27 Jul 2026] Ines: @Kai I'll be sure to move the piano by 30 July 2026.\n[30 Jul 2026] Ines: @Kai To my relief, I managed to move the piano.\n[4 Aug 2026] Wren: Anything new on your way to move the piano?",
  "question": "Checking the chat at the end of 5 August 2026, has Ines broken the promise to move the piano?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7615c745da",
  "kind": "yes/no",
  "text": "Help desk export\nAbout: the school fundraiser\nCopied by: Omar\n\nMembers: Tess, Omar, Malik, Sami\nChat export (date | from | to | message):\n2026-06-23 | Sami | Tess | Count on me to count the donation boxes by 28 June 2026.\n2026-06-26 | Malik | Tess | Count on me to book the school hall by 4 July 2026 if the clothes swap is on.\n2026-06-28 | Omar | Sami | Committing to fetch the tea urn by 5 July 2026.\n2026-06-29 | Tess | group | Yay, the clothes swap is all set to go!\n2026-07-01 | Sami | Omar | No need to fetch the tea urn, I'm letting you off\n2026-07-07 | Malik | Tess | Mum, I did book the school hall, haha.",
  "question": "Under the rules on the card, is the promise Malik made to book the school hall in a status other than broken at the end of 4 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf108e79732",
  "kind": "yes/no",
  "text": "Parents and cousins, this is where we sort out the loft conversion. Saved by Sami.\n\nMembers: Nadia, Sami, Lena\nChat export (date | from | to | message):\n2026-10-08 | Nadia | Sami | If the boiler install visit goes ahead, I'll pay the plumbing invoice by 15 October 2026.\n2026-10-08 | Nadia | Lena | As long as the damp survey inspection is on, I will return the tile cutter by 13 October 2026.\n2026-10-11 | Lena | Sami | Count on me to hang the new curtain rail by 19 October 2026.\n2026-10-13 | Lena | group | Scrapping the boiler install visit, apologies to all.\n2026-10-19 | Lena | Sami | Mate, I promised, may I hang the new curtain rail by 23 October 2026 instead?\n2026-10-19 | Sami | Lena | No, you need to hang the new curtain rail by the original date.",
  "question": "Applying the card's rules, can it be said that Nadia has not kept the promise to pay the plumbing invoice at the end of 18 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q34f3e84fb7",
  "kind": "yes/no",
  "text": "Export from a freelance project log, covering the shop rebuild, saved by Kai.\n\nMembers: Leila, Ines, Ravi, Kai\nChat export (date | from | to | message):\n2026-08-26 | Ravi | Leila | You can bank on me to set up the email forwarding by 29 Aug 2026.\n2026-08-27 | Leila | Ines | I promise to update the product photos by 3 Sep 2026.\n2026-08-29 | Ravi | Leila | Mum, I did set up the email forwarding, haha.\n2026-08-31 | Kai | Leila | I assure you I'll restore the old theme by 2 Sep 2026 if the site handover is on.\n2026-09-01 | Kai | group | Brilliant news everyone, the site handover is a go!",
  "question": "Going by the card's rules, does Ravi keep the promise to set up the email forwarding at the end of 29 Aug 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q652df6ca0a",
  "kind": "choice",
  "text": "Subject: Chat about the trip itinerary\nBelow is a copy that came from Yuki, pasted as found.\n\nMembers: Zara, Rhea, Yuki\nChat export (date | from | to | message):\n2026-05-15 | Rhea | Zara | I own this, I'll buy the packing cubes by 20 May 2026.\n2026-05-16 | Zara | Rhea | If the ferry crossing goes ahead, I'll check the passport copies by 21 May 2026.\n2026-05-16 | Zara | group | On track for the ferry crossing to happen as planned.\n2026-05-17 | Rhea | Zara | Please don't feel you have to check the passport copies\n2026-05-20 | Rhea | Zara | Correction, I will not be able to buy the packing cubes.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Zara's promise to check the passport copies at the end of 16 May 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q19cc976546",
  "kind": "yes/no",
  "text": "Sami saved this so we stay on the same page about the cellar project, mates.\n\nMembers: Ana, Tess, Sami, Leila\nChat log (oldest first):\n[25 Jul 2026] Sami: @Leila Lovely, I'll wash the sash windows by Monday, July 27, 2026 for sure.\n[25 Jul 2026] Leila: @Sami Quick update: you do not need to wash the sash windows at all.\n[27 Jul 2026] Tess: @Sami Committing to oil the back door hinges by Thursday, July 30, 2026.\n[30 Jul 2026] Sami: @Ana As long as the loft clearance day is on, I'll defrost the old fridge by Friday, August 7, 2026.\n[2 Aug 2026] Tess: @Sami Guess who managed to oil the back door hinges, go team!\n[3 Aug 2026] Ana: Afraid the loft clearance day is called off.",
  "question": "On the card, was Tess's promise to oil the back door hinges broken, waived, not triggered or not yet due, rather than kept, at the end of Tuesday, August 4, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3749920790",
  "kind": "yes/no",
  "text": "Work channel holding the platform rewrite, export saved by Sami.\n\nMembers: Sami, Greta\nChat log (oldest first):\n[23 Jun 2026] Sami: @Greta I will make sure to label the bug reports by 26 June 2026.\n[24 Jun 2026] Sami: @Greta Update on my side: I will not label the bug reports, sorry.\n[26 Jun 2026] Greta: @Sami Count on me to rotate the test keys by 5 July 2026, if the penetration test happens.\n[26 Jun 2026] Sami: @Greta You can bank on me to deploy the staging build by 1 July 2026.\n[26 Jun 2026] Sami: @Greta I'll review the pull request by 4 July 2026 if the planning session goes ahead.\n[3 Jul 2026] Sami: Really pleased to say the planning session will go ahead!",
  "question": "Under the rules on the card, is Sami's promise to review the pull request broken, waived, not triggered or not yet due, rather than kept, as of 3 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qa6e07a45cb",
  "kind": "yes/no",
  "text": "Subject: saved chat, the school fundraiser\nBelow is the chat that Malik saved for reference.\n\nMembers: Kofi, Sami, Bruno, Malik\nChat export (date | from | to | message):\n2026-07-28 | Sami | Kofi | Lovely, I'll return the borrowed trestle tables by Friday, July 31, 2026 for sure.\n2026-07-30 | Bruno | Malik | As long as the field day is on, I will print the raffle tickets by Sunday, August 2, 2026.\n2026-07-31 | Sami | Kofi | Got myself to return the borrowed trestle tables lol.\n2026-08-02 | Malik | Sami | Committing to book the school hall by Monday, August 10, 2026.\n2026-08-02 | Kofi | Malik | Lovely, I'll collect the bake sale tins by Saturday, August 8, 2026 if the summer fete is on.\n2026-08-12 | Malik | Sami | For the record: I was able to book the school hall",
  "question": "Would you call Sami's promise to return the borrowed trestle tables broken, waived, not triggered or not yet due, instead of kept, at the end of Monday, August 3, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8c29421e61",
  "kind": "choice",
  "text": "Help desk export\nAbout: the new kit design\nCopied by: Bruno\n\nMembers: Dara, Bruno, Nadia, Priya\nChat log (oldest first):\n[23 Apr 2026] Priya: @Dara I'll wash the club jerseys by 1 May 2026, promise.\n[25 Apr 2026] Dara: @Bruno If the group ride goes ahead, I'll print the route cards by 28 April 2026.\n[25 Apr 2026] Nadia: Update: the group ride is going ahead as planned.\n[26 Apr 2026] Priya: @Dara No need to print the route cards, I'm letting you off\n[30 Apr 2026] Priya: @Dara Scratch what I said, I won't wash the club jerseys.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Dara made to print the route cards have at the end of 26 April 2026?",
  "options": [
   "Not triggered",
   "Waived",
   "Broken",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "qbf046c1259",
  "kind": "choice",
  "text": "Pasted from our flat chat by Elif, the bit about the kitchen garden project.\n\nMembers: Omar, Elif, Kai, Mo\nChat log (oldest first):\n[21 Jun 2026] Elif: @Omar Committing to fix the shed door by Wednesday, June 24, 2026.\n[21 Jun 2026] Elif: @Omar Sorry, I won't fix the shed door after all\n[22 Jun 2026] Omar: @Elif I'll deliver the surplus runner beans by Sunday, June 28, 2026, providing the seed swap day goes ahead.\n[23 Jun 2026] Kai: On track for the seed swap day to happen as planned.\n[26 Jun 2026] Elif: @Mo Count on me to weed the carrot row by Friday, July 3, 2026 if the allotment site visit is on.\n[29 Jun 2026] Omar: @Elif To my relief, I managed to deliver the surplus runner beans.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Omar made to deliver the surplus runner beans at the end of Sunday, June 28, 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Kept",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q9797e63131",
  "kind": "choice",
  "text": "Here's the club committee's chat, saved by Lena, about the annual tour.\n\nMembers: Bruno, Lena, Oskar, Dara\nChat log (oldest first):\n[16 Jul 2026] Lena: @Dara Relax, I'll service the tandem bike by 21 Jul 2026 for sure.\n[20 Jul 2026] Lena: @Dara Can I service the tandem bike by 25 Jul 2026 instead? I did promise, sorry.\n[21 Jul 2026] Oskar: @Dara It's on me to set up the feed stop by 24 Jul 2026.\n[21 Jul 2026] Dara: @Lena Yes, you have the green light to service the tandem bike by 25 Jul 2026.\n[22 Jul 2026] Oskar: @Dara To note: I have managed to set up the feed stop\n[22 Jul 2026] Lena: @Dara I assure you I'll tune the gear cables by 24 Jul 2026 if the club sportive is on.\n[23 Jul 2026] Lena: @Dara Guess who managed to service the tandem bike, go team!\n[23 Jul 2026] Lena: Yay, the club sportive is all set to go!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nFollowing the rules set out on the card, what date governs Lena's commitment to service the tandem bike at the end of 27 Jul 2026, once any agreed shift in the date is factored in?",
  "options": [
   "21 Jul 2026",
   "25 Jul 2026",
   "24 Jul 2026"
  ]
 }
]
