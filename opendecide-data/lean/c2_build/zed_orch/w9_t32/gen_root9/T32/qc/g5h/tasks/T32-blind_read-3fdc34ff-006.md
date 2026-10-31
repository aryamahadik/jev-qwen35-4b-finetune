# G5-H blind read T32-blind_read-3fdc34ff-006 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root9/T32/qc/g5h/answers/T32-blind_read-3fdc34ff-006.json

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
  "qid": "q434e05f706",
  "kind": "choice",
  "text": "{\"source\": \"saved thread\", \"about\": \"the care plan\", \"owner\": \"Priya\", \"kind\": \"chat export\"}\n\nMembers: Priya, Malik, Rhea, Leila\nChat log (oldest first):\n[20 Jan 2026] Malik: @Rhea Count on me, I'll pick up the repeat prescription by 26 Jan 2026.\n[22 Jan 2026] Malik: @Rhea Might I ask whether I could pick up the repeat prescription by 30 Jan 2026 instead?\n[25 Jan 2026] Leila: @Priya If the carer handover goes ahead, I'll gladly collect the post by 31 Jan 2026.\n[25 Jan 2026] Priya: @Malik Yes, all good for you to pick up the repeat prescription by 30 Jan 2026 instead.\n[26 Jan 2026] Priya: @Rhea I'll be sure to print the care schedule by 1 Feb 2026.\n[26 Jan 2026] Priya: Just so you know, the carer handover is on as scheduled.\n[26 Jan 2026] Leila: @Malik No need to pick up the repeat prescription, I'm letting you off\n[30 Jan 2026] Leila: Any news on whether you can pick up the repeat prescription, lovely?",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 29 Jan 2026, by what date does Malik have to pick up the repeat prescription, counting any agreed change of date?",
  "options": [
   "31 Jan 2026",
   "26 Jan 2026",
   "30 Jan 2026"
  ]
 },
 {
  "qid": "q436a779686",
  "kind": "yes/no",
  "text": "{\"source\": \"saved thread\", \"about\": \"the mobile release\", \"owner\": \"Ana\", \"kind\": \"chat export\"}\n\nMembers: Arlo, Ana, Hana, Bruno\nChat log (oldest first):\n[16 Aug 2026] Arlo: @Hana As long as the server migration is on, I'll write the release notes by 23 Aug 2026.\n[19 Aug 2026] Bruno: @Ana It's on me to rotate the test keys by 25 Aug 2026.\n[23 Aug 2026] Hana: @Bruno No need to rotate the test keys, I'm letting you off\n[24 Aug 2026] Bruno: @Arlo I'll label the bug reports by 2 Sep 2026 as long as the code freeze is on.\n[26 Aug 2026] Bruno: @Ana Ticked off my list: rotate the test keys, yay.",
  "question": "Did Bruno break the promise to rotate the test keys at the end of 29 Aug 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q26fc2abe59",
  "kind": "choice",
  "text": "Bruno shared this channel export, covering the mobile release for the team.\n\nMembers: Kofi, Malik, Bruno\nChat log (oldest first):\n[21 Oct 2026] Kofi: @Malik Relax, I'll fix the test runner by 2026-10-24 for sure.\n[24 Oct 2026] Bruno: @Kofi Absolutely, I will update the dependency list by 2026-10-31.\n[28 Oct 2026] Kofi: @Malik Provided the hackathon happens, I will run the security scan by 2026-11-06.\n[31 Oct 2026] Bruno: @Kofi Log entry: update the dependency list, carried out\n[2 Nov 2026] Bruno: We are dropping the hackathon from the list.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Bruno's promise to update the dependency list at the end of 2026-10-31?",
  "options": [
   "Not triggered",
   "Waived",
   "Kept",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qe476a80ec1",
  "kind": "choice",
  "text": "Chat channel log:\nWork messages about the trade show push, exported by Bruno.\n\nMembers: Tomas, Greta, Dara, Bruno\nChat export (date | from | to | message):\n2026-04-18 | Tomas | Dara | I'll set up the analytics dashboard by Tuesday, April 21, 2026, provided the trade fair stand happens.\n2026-04-18 | Greta | group | Update: the trade fair stand is going ahead as planned.\n2026-04-20 | Bruno | Dara | Ticket's mine, I'll collect the survey answers by Sunday, April 26, 2026.\n2026-04-25 | Greta | Bruno | Count on me to return the rented camera gear by Wednesday, April 29, 2026.\n2026-04-26 | Dara | Bruno | Good news, you're let off having to collect the survey answers",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status does the chat show for the promise Bruno made to collect the survey answers at the end of Sunday, April 26, 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "qed5fc8c0ca",
  "kind": "yes/no",
  "text": "Volunteers, here is the choir tour chat that Wren forwarded to us.\n\nMembers: Sami, Hana, Wren, Tess\nChat log (oldest first):\n[24 Sep 2026] Wren: @Sami Committing to print the song sheets by 1 October 2026.\n[24 Sep 2026] Sami: Cheers, noted.\n[26 Sep 2026] Sami: @Hana Provided the carol concert happens, I'll buy the spare folders by 29 September 2026.\n[26 Sep 2026] Hana: Great news, the carol concert is on!\n[26 Sep 2026] Hana: @Wren Forget it, you won't need to print the song sheets\n[1 Oct 2026] Wren: @Sami Got myself to print the song sheets lol.",
  "question": "Is Wren's promise to print the song sheets kept as of 7 October 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7dbc11683c",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the garden shed build\nThe chat below comes from Tomas, copied as is for reference.\n\nMembers: Lena, Mo, Hana, Tomas\nChat log (oldest first):\n[24 Apr 2026] Hana: @Lena It's on me to stake the tomato canes by 1 May 2026.\n[25 Apr 2026] Lena: How's the plan to stake the tomato canes?\n[30 Apr 2026] Hana: @Lena On my action item, may I stake the tomato canes by 4 May 2026 instead?\n[30 Apr 2026] Tomas: @Hana Yes, lovely, you can stake the tomato canes by 4 May 2026 instead!\n[30 Apr 2026] Hana: @Lena For the record: I was able to stake the tomato canes\n[4 May 2026] Mo: @Hana I will dig the potato patch by 6 May 2026 only if the plot inspection happens.\n[4 May 2026] Tomas: Scrapping the plot inspection, apologies to all.\n[5 May 2026] Mo: @Tomas Count on me, I'll collect the seed potatoes by 9 May 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules, when is the date by which Hana has to stake the tomato canes at the end of 2 May 2026, allowing for any agreed change?",
  "options": [
   "4 May 2026",
   "6 May 2026",
   "1 May 2026"
  ]
 },
 {
  "qid": "q46aa2eeae2",
  "kind": "choice",
  "text": "Here's the club committee's chat, saved by Wren, about the playground project.\n\nMembers: Ines, Elif, Wren\nChat export (date | from | to | message):\n2026-10-26 | Ines | Elif | Provided the field day happens, I'll wrap the prize hampers by 28 October 2026.\n2026-10-28 | Elif | Ines | Guaranteed I'll print the raffle tickets by 4 November 2026.\n2026-10-28 | Ines | group | Appreciate you telling me.\n2026-10-31 | Elif | Ines | Is it all right if I print the raffle tickets by 7 November 2026 instead?\n2026-10-31 | Wren | Ines | If the quiz night is on, I'll definitely label the raffle prizes by 5 November 2026.\n2026-11-01 | Ines | Elif | Yes, you're welcome to print the raffle tickets by 7 November 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJust to be sure, what status does the promise Elif made to print the raffle tickets have at the end of 6 November 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not yet due",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "qbf45fd515a",
  "kind": "choice",
  "text": "Volunteer chat export. Saved by Ivo, it covers the new term plans.\n\nMembers: Sami, Ivo, Zara, Ana\nChat export (date | from | to | message):\n2026-09-08 | Ivo | Ana | You can bank on me to label the raffle prizes by 14 September 2026.\n2026-09-13 | Ana | Zara | Count on me, I'll return the borrowed trestle tables by 19 September 2026.\n2026-09-13 | Sami | Zara | I'll send the newsletter drafts by 17 September 2026, providing the governors meeting goes ahead.\n2026-09-13 | Sami | group | Team, the governors meeting is not happening.\n2026-09-14 | Zara | Ana | Relax, I'll collect the bake sale tins by 21 September 2026 for sure.\n2026-09-16 | Zara | Ana | Change of plans: I will not collect the bake sale tins",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Sami's promise to send the newsletter drafts at the end of 21 September 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q319bba3342",
  "kind": "yes/no",
  "text": "Work conversation on the social media plan, saved as a file by Zara.\n\nMembers: Lena, Zara, Arlo\nChat export (date | from | to | message):\n2026-03-29 | Arlo | Lena | I will send the newsletter copy by 6 Apr 2026.\n2026-04-02 | Arlo | Lena | I'll book the photo studio by 6 Apr 2026 if the trade fair stand goes ahead.\n2026-04-02 | Zara | Arlo | Count on me, I'll pay the printing invoice by 5 Apr 2026.\n2026-04-02 | Arlo | group | Cheers, noted.\n2026-04-04 | Arlo | group | Lovely, the trade fair stand is definitely happening!\n2026-04-08 | Zara | Arlo | For the record: I was able to pay the printing invoice",
  "question": "Is Zara's promise to pay the printing invoice broken, waived, not triggered or not yet due as of 10 Apr 2026, instead of kept?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb1d5a6a4b8",
  "kind": "choice",
  "text": "Parents and cousins, this is where we sort out the summer visits. Saved by Zara.\n\nMembers: Tomas, Zara, Rhea\nChat log (oldest first):\n[5 Feb 2026] Rhea: @Zara You can bet I'll read the bedtime story by 12 Feb 2026.\n[6 Feb 2026] Rhea: @Tomas Only if the garden tea party is on, I will walk the dog by 13 Feb 2026.\n[8 Feb 2026] Tomas: @Rhea As long as the school play is on, I'll bake the oat biscuits by 17 Feb 2026.\n[10 Feb 2026] Rhea: @Zara I promise to sort the old photo albums by 19 Feb 2026.\n[12 Feb 2026] Rhea: @Zara To note: I have managed to read the bedtime story\n[15 Feb 2026] Zara: @Rhea Don't sweat it, there's no need to sort the old photo albums",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Rhea's promise to read the bedtime story turn out at the end of 12 Feb 2026?",
  "options": [
   "Broken",
   "Waived",
   "Kept",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q4355bde4ae",
  "kind": "choice",
  "text": "Help desk export\nAbout: the big house plan\nCopied by: Rhea\n\nMembers: Bruno, Rhea\nChat export (date | from | to | message):\n2026-10-11 | Rhea | Bruno | Relax, I'll tidy the boot room by 13 October 2026, promise.\n2026-10-13 | Rhea | Bruno | Mate, I promised, may I tidy the boot room by 17 October 2026 instead?\n2026-10-13 | Bruno | Rhea | Yes, you have the green light to tidy the boot room by 17 October 2026.\n2026-10-14 | Rhea | Bruno | If the heritage fete goes ahead, I'll gladly replace the hallway bulbs by 17 October 2026.\n2026-10-14 | Rhea | group | Brilliant news everyone, the heritage fete is a go!\n2026-10-17 | Bruno | Rhea | Relax, mate, you're not expected to replace the hallway bulbs",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Rhea's promise to replace the hallway bulbs at the end of 20 October 2026?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q545af2bf39",
  "kind": "yes/no",
  "text": "Chat about the home adaptations, from the support queue, gathered by Dara.\n\nMembers: Nadia, Lee, Dara\nChat log (oldest first):\n[24 Jun 2026] Dara: @Lee Guaranteed I'll fetch the mobility aids by 3 Jul 2026.\n[28 Jun 2026] Nadia: @Lee I will collect the post by 2 Jul 2026.\n[29 Jun 2026] Dara: @Nadia Good news, you're let off having to collect the post\n[2 Jul 2026] Lee: @Nadia I'll return the hospital bed by 11 Jul 2026, provided the family care meeting happens.\n[4 Jul 2026] Lee: Sad to report that the family care meeting is off.",
  "question": "Does the card's rule set confirm that Nadia has kept the promise to collect the post on 6 Jul 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb21b6229a0",
  "kind": "yes/no",
  "text": "Flat chat export, saved by Kai\nCovers the autumn term budget, shared among the housemates.\n\nMembers: Wren, Ravi, Kai\nChat log (oldest first):\n[16 Jul 2026] Wren: @Ravi I'll try to print the tenancy agreement by 27 July 2026, no promises.\n[17 Jul 2026] Wren: @Kai Only if the gas safety inspection is on, I will print the tenancy agreement by 24 July 2026.\n[18 Jul 2026] Ravi: Update: the gas safety inspection is going ahead as planned.\n[20 Jul 2026] Ravi: @Wren Got it, I'll send the deposit receipt by 29 July 2026 for sure.\n[21 Jul 2026] Wren: @Kai Mind giving me until 27 July 2026 to print the tenancy agreement?\n[23 Jul 2026] Kai: @Wren That suits me, so please print the tenancy agreement by 27 July 2026 instead.",
  "question": "On 27 July 2026 itself, has Wren not kept the promise to print the tenancy agreement?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Wren (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5e1ce04f95",
  "kind": "yes/no",
  "text": "{\"archive\": \"group chat\", \"subject\": \"the kit sponsorship\", \"sent_by\": \"Arlo\"}\n\nMembers: Arlo, Elif\nChat log (oldest first):\n[24 Jun 2026] Elif: @Arlo I will make sure to mark the pitch lines by 29 June 2026.\n[25 Jun 2026] Elif: @Arlo Lovely, I'll book the changing room by 3 July 2026 if the youth trial is on.\n[26 Jun 2026] Elif: @Arlo Ticket's mine, I'll print the team sheets by 3 July 2026.\n[27 Jun 2026] Elif: Yay, the youth trial is all set to go!\n[30 Jun 2026] Elif: @Arlo Log entry: mark the pitch lines, carried out",
  "question": "Is the promise Elif made to mark the pitch lines not kept by 3 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qcc2da90b00",
  "kind": "choice",
  "text": "Client messages for a freelancer about the gallery show, saved by Lena.\n\nMembers: Priya, Kofi, Zara, Lena\nChat log (oldest first):\n[8 Mar 2026] Kofi: @Priya If the sign reveal goes ahead, I'll gladly send the moodboard files by March 11, 2026.\n[8 Mar 2026] Priya: Scrapping the sign reveal, apologies to all.\n[9 Mar 2026] Kofi: @Priya Mind giving me until March 16, 2026 to send the moodboard files?\n[10 Mar 2026] Lena: @Priya You can bet I'll check the poster proofs by March 15, 2026.\n[11 Mar 2026] Kofi: @Priya I'll update the icon set by March 17, 2026 if the brand review call goes ahead.\n[11 Mar 2026] Priya: @Kofi Yes, you can send the moodboard files by March 16, 2026 if that suits you.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Kofi's promise to send the moodboard files at the end of March 12, 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "qe09b7c76b8",
  "kind": "yes/no",
  "text": "Plain text of a family chat with the caring rota included, saved by Jonas.\n\nMembers: Ravi, Leila, Jonas, Wren\nChat log (oldest first):\n[17 Jan 2026] Jonas: @Ravi Hoping to set up the medicine dispenser by 24 Jan 2026, no promises.\n[18 Jan 2026] Jonas: @Leila I'll be sure to collect the post by 20 Jan 2026.\n[18 Jan 2026] Jonas: @Ravi As long as the eye test is on, I'll set up the medicine dispenser by 21 Jan 2026.\n[18 Jan 2026] Ravi: Lovely, the eye test is definitely happening!\n[21 Jan 2026] Ravi: @Jonas It's on me to print the care schedule by 26 Jan 2026.\n[24 Jan 2026] Jonas: @Ravi To my relief, I managed to set up the medicine dispenser.",
  "question": "Has Jonas broken the promise to set up the medicine dispenser at the end of 21 Jan 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2ebbb0e49c",
  "kind": "choice",
  "text": "Subject: chat about the care plan, forwarded\nThe chat follows below.\nRegards, Lena\n\nMembers: Lena, Priya, Zara\nChat export (date | from | to | message):\n2026-10-07 | Priya | Zara | Relax, I'll call the home nurse by 15 October 2026 for sure.\n2026-10-09 | Priya | Zara | Log entry: call the home nurse, carried out\n2026-10-09 | Zara | Priya | I'll wash the bed linen by 18 October 2026, providing the eye test goes ahead.\n2026-10-11 | Zara | Lena | Ticket's mine, I'll collect the post by 17 October 2026.\n2026-10-11 | Zara | Priya | I will drop off the hot meals by 19 October 2026 only if the family care meeting happens.\n2026-10-18 | Lena | group | Sorry all, the family care meeting is called off.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Zara's pledge to drop off the hot meals at the end of 23 October 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qafb8f71e2c",
  "kind": "choice",
  "text": "{\"export_type\": \"group chat export\", \"chat_topic\": \"the caring rota\", \"saved_by\": \"Greta\"}\n\nMembers: Greta, Malik, Ines\nChat log (oldest first):\n[29 May 2026] Ines: @Malik Lovely, I'll wash the bed linen by 5 June 2026 for sure.\n[30 May 2026] Malik: @Greta Provided the family care meeting happens, I'll collect the post by 4 June 2026.\n[1 Jun 2026] Greta: Scrapping the family care meeting, apologies to all.\n[3 Jun 2026] Malik: @Greta Any chance I can collect the post by 9 June 2026 instead?\n[3 Jun 2026] Ines: @Malik Yes, you're welcome to collect the post by 9 June 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Malik's promise to collect the post at the end of 4 June 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qe28770a706",
  "kind": "yes/no",
  "text": "Subject: exported chat about the big day\nHere it is for you, from Femi, exactly as saved.\n\nMembers: Femi, Ivo, Yuki\nChat log (oldest first):\n[16 Jun 2026] Femi: @Ivo As long as the rehearsal dinner is on, I'll book the assistant photographer by 23 Jun 2026.\n[19 Jun 2026] Femi: @Yuki Ticket's mine, I'll return the lighting stands by 26 Jun 2026.\n[22 Jun 2026] Femi: Lovely, the rehearsal dinner is definitely happening!\n[22 Jun 2026] Yuki: @Femi Relax, mate, you're not expected to book the assistant photographer\n[23 Jun 2026] Femi: @Ivo To my relief, I managed to book the assistant photographer.",
  "question": "Has Femi kept the promise to book the assistant photographer at the end of 24 Jun 2026, instead of broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qfe03271571",
  "kind": "choice",
  "text": "Shared by Tomas, this thread covers the honeymoon album as pasted from email.\n\nMembers: Femi, Tomas, Kai, Dara\nChat log (oldest first):\n[30 Mar 2026] Tomas: @Femi You can bet I'll print the seating cards by 2026-04-01.\n[31 Mar 2026] Tomas: @Femi Ta-da, I went and did it: print the seating cards!\n[1 Apr 2026] Tomas: @Kai Provided the ceremony walkthrough happens, I'll charge the flash batteries by 2026-04-09.\n[2 Apr 2026] Kai: Really pleased to say the ceremony walkthrough will go ahead!\n[9 Apr 2026] Femi: @Tomas Forget it, you won't need to charge the flash batteries",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 2026-04-13, what status has Tomas's promise to charge the flash batteries got?",
  "options": [
   "Waived",
   "Not yet due",
   "Kept",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "qc9f8a1b2bb",
  "kind": "choice",
  "text": "{\"item\": \"chat export\", \"matter\": \"the cottage refresh\", \"saved_by\": \"Arlo\", \"layout\": \"plain\"}\n\nMembers: Mo, Arlo, Omar, Ana\nChat log (oldest first):\n[14 Jan 2026] Mo: @Arlo See if I can vacuum the holiday cottage by 17 Jan 2026, no certainty.\n[16 Jan 2026] Mo: @Arlo You can bet I'll vacuum the holiday cottage by 22 Jan 2026.\n[20 Jan 2026] Omar: @Arlo I assure you I'll air the spare room by 29 Jan 2026 if the summer season launch is on.\n[21 Jan 2026] Mo: @Ana If the check out clean goes ahead, I'll gladly wheel the bins out by 28 Jan 2026.\n[22 Jan 2026] Arlo: @Mo Please don't feel you have to vacuum the holiday cottage\n[22 Jan 2026] Mo: @Arlo Log entry: vacuum the holiday cottage, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Mo's promise to vacuum the holiday cottage stand at the end of 27 Jan 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Broken",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qdb855fe290",
  "kind": "yes/no",
  "text": "Subject: copy of the chat about the speed bump plan\nFor your records, the saved chat is below, from Hana.\n\nMembers: Ivo, Priya, Hana, Bruno\nChat log (oldest first):\n[16 Mar 2026] Hana: @Ivo You can bank on me to sweep the pavement outside by 23 March 2026.\n[16 Mar 2026] Ivo: Got it, thanks a lot.\n[17 Mar 2026] Priya: @Hana I assure you I'll feed the cat across the road by 19 March 2026 if the speed camera survey is on.\n[17 Mar 2026] Hana: Sad to report that the speed camera survey is off.\n[23 Mar 2026] Priya: @Hana No need to sweep the pavement outside, I'm letting you off\n[24 Mar 2026] Hana: @Ivo Guess what, I managed to sweep the pavement outside!",
  "question": "Applying the rules on the card, can Hana's promise to sweep the pavement outside be said to have not been broken at the end of 26 March 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qfccb974d7f",
  "kind": "choice",
  "text": "{\"source\": \"saved thread\", \"about\": \"the autumn term budget\", \"owner\": \"Nadia\", \"kind\": \"chat export\"}\n\nMembers: Priya, Omar, Malik, Nadia\nChat log (oldest first):\n[20 May 2026] Omar: @Malik I'll return the bin rota by 28 May 2026 as long as the gas safety inspection is on.\n[22 May 2026] Malik: Yay, the gas safety inspection is all set to go!\n[27 May 2026] Nadia: @Priya I own this, I'll scan the council tax letter by 3 June 2026.\n[28 May 2026] Omar: @Malik Can I return the bin rota by 1 June 2026 instead? I did promise, sorry.\n[28 May 2026] Nadia: @Omar Yes, you're welcome to return the bin rota by 1 June 2026 instead.\n[28 May 2026] Omar: @Malik Lovely, I'll forward the inventory photos by 4 June 2026 if the agent inventory walk is on.\n[29 May 2026] Nadia: @Priya I committed to scan the council tax letter, can I do that by 7 June 2026 instead?\n[2 Jun 2026] Priya: @Nadia Yes, happy for you to scan the council tax letter by 7 June 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Omar to return the bin rota at the end of 9 June 2026, counting any agreed change of date?",
  "options": [
   "3 June 2026",
   "1 June 2026",
   "28 May 2026"
  ]
 },
 {
  "qid": "qcb96526d1b",
  "kind": "choice",
  "text": "{\"source\": \"saved thread\", \"about\": \"the autumn term budget\", \"owner\": \"Nadia\", \"kind\": \"chat export\"}\n\nMembers: Priya, Omar, Malik, Nadia\nChat log (oldest first):\n[20 May 2026] Omar: @Malik I'll return the bin rota by 28 May 2026 as long as the gas safety inspection is on.\n[22 May 2026] Malik: Yay, the gas safety inspection is all set to go!\n[27 May 2026] Nadia: @Priya I own this, I'll scan the council tax letter by 3 June 2026.\n[28 May 2026] Omar: @Malik Can I return the bin rota by 1 June 2026 instead? I did promise, sorry.\n[28 May 2026] Nadia: @Omar Yes, you're welcome to return the bin rota by 1 June 2026 instead.\n[28 May 2026] Omar: @Malik Lovely, I'll forward the inventory photos by 4 June 2026 if the agent inventory walk is on.\n[29 May 2026] Nadia: @Priya I committed to scan the council tax letter, can I do that by 7 June 2026 instead?\n[2 Jun 2026] Priya: @Nadia Yes, happy for you to scan the council tax letter by 7 June 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Omar to return the bin rota at the end of 9 June 2026, counting any agreed change of date?",
  "options": [
   "28 May 2026",
   "3 June 2026",
   "1 June 2026"
  ]
 },
 {
  "qid": "qfd44b2d3ea",
  "kind": "choice",
  "text": "Attached chat: the house rules debate\nShared by: Mo.\n\nMembers: Tomas, Mo\nChat log (oldest first):\n[20 May 2026] Tomas: @Mo Provided the ghost tour happens, I will tidy the boot room by 28 May 2026.\n[20 May 2026] Tomas: Sorry, the ghost tour is off.\n[23 May 2026] Tomas: @Mo You can bet I'll oil the back door hinges by 1 Jun 2026.\n[26 May 2026] Mo: @Tomas Relax, I'll replace the hallway bulbs by 29 May 2026, promise.\n[27 May 2026] Tomas: @Mo Log entry: oil the back door hinges, carried out\n[28 May 2026] Mo: @Tomas I have to take back my promise to replace the hallway bulbs.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs a check of the chat, what status does Tomas's commitment to tidy the boot room have at the end of 28 May 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Broken",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q11374cc215",
  "kind": "choice",
  "text": "Thread between a landlord and tenants on the attic conversion idea left as it was and shared by Omar.\n\nMembers: Bruno, Arlo, Omar\nChat export (date | from | to | message):\n2026-05-31 | Bruno | Arlo | Hoping to turn the heating timer by 9 June 2026, but can't promise.\n2026-06-02 | Arlo | Omar | You can bank on me to replace the loo roll by 6 June 2026.\n2026-06-02 | Bruno | Omar | I'll turn the heating timer by 10 June 2026 as long as the lodger farewell supper is on.\n2026-06-04 | Omar | group | Sadly, the lodger farewell supper won't go ahead.\n2026-06-05 | Arlo | Omar | On my action item, may I replace the loo roll by 9 June 2026 instead?\n2026-06-06 | Omar | Arlo | No new date, so please replace the loo roll by the date given.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Bruno made to turn the heating timer is in which status at the end of 13 June 2026?",
  "options": [
   "Waived",
   "Broken",
   "Not triggered",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q5d007296f6",
  "kind": "choice",
  "text": "Pasted into the project log by Ivo, the thread with a client about the holiday catalogue.\n\nMembers: Ivo, Ana, Sami\nChat log (oldest first):\n[7 Mar 2026] Ana: @Sami If the pop up stall goes ahead, I'll restore the old theme by Thursday, March 12, 2026.\n[9 Mar 2026] Ana: @Sami I'll set up the email forwarding by Friday, March 13, 2026 if the courier pickup goes ahead.\n[10 Mar 2026] Ana: @Sami Hoping to test the mobile layout by Friday, March 20, 2026, can't promise.\n[11 Mar 2026] Ana: @Ivo Count on me, I'll test the mobile layout by Wednesday, March 18, 2026.\n[11 Mar 2026] Sami: @Ana You don't have to test the mobile layout at all\n[14 Mar 2026] Ana: @Sami I will print the packing slips by Tuesday, March 17, 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Ana made to test the mobile layout at the end of Saturday, March 14, 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Broken",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "qab620e1821",
  "kind": "yes/no",
  "text": "Ana saved these replies from the agent on the kitchen refit.\n\nMembers: Yuki, Ana, Lee, Kofi\nChat log (oldest first):\n[14 Sep 2026] Yuki: @Ana Count on me, I'll measure the kitchen for fridge by 19 Sep 2026.\n[15 Sep 2026] Yuki: @Lee As long as the electrics safety check is on, I'll drop the bin bags off by 18 Sep 2026.\n[17 Sep 2026] Yuki: @Ana I committed to measure the kitchen for fridge, can I do that by 23 Sep 2026 instead?\n[17 Sep 2026] Yuki: @Ana Guess what, I managed to measure the kitchen for fridge!\n[18 Sep 2026] Kofi: Where are you up to with plans to measure the kitchen for fridge?\n[19 Sep 2026] Ana: @Kofi I'll ring the flat repair line by 24 Sep 2026 as long as the flat viewing day is on.",
  "question": "Has Yuki not kept the promise to measure the kitchen for fridge at the end of 22 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9ec06970c6",
  "kind": "yes/no",
  "text": "Subject: saved chat on the winter concert\nGathered by Tomas for you, full text below.\n\nMembers: Tomas, Ana, Arlo, Ravi\nChat log (oldest first):\n[17 May 2026] Ana: @Tomas Got it, I'll buy the spare folders by Wednesday, May 20, 2026 for sure.\n[17 May 2026] Tomas: Thanks lovely, got it!\n[19 May 2026] Ravi: @Arlo Ticket's mine, I'll send the audition reminders by Friday, May 22, 2026.\n[20 May 2026] Ana: @Arlo I promise to print the song sheets by Saturday, May 23, 2026 if the carol concert is on.\n[20 May 2026] Arlo: Really pleased to say the carol concert will go ahead!\n[21 May 2026] Ana: @Tomas To note: I have managed to buy the spare folders",
  "question": "Going by the card's rules, does Ana not keep the promise to buy the spare folders at the end of Monday, May 25, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb95f683120",
  "kind": "yes/no",
  "text": "Shared by Arlo, this back and forth with the client covers the guest list.\n\nMembers: Priya, Yuki, Arlo\nChat log (oldest first):\n[1 Jun 2026] Priya: I'll try to set up the backdrop frame by 5 June 2026, no guarantee.\n[3 Jun 2026] Priya: @Yuki Relax, I'll set up the backdrop frame by 7 June 2026, promise.\n[5 Jun 2026] Arlo: @Yuki Provided the rehearsal dinner happens, I will collect the venue floor plan by 14 June 2026.\n[7 Jun 2026] Yuki: Sadly, the rehearsal dinner won't go ahead.\n[8 Jun 2026] Priya: @Yuki Guess who managed to set up the backdrop frame, go team!\n[9 Jun 2026] Priya: @Arlo You can bet I'll pick up the album prints by 18 June 2026.",
  "question": "Is Priya's promise to set up the backdrop frame kept at the end of 11 June 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q52f61a77a4",
  "kind": "yes/no",
  "text": "Our house group, sorted by Wren, with the rent split plan up front.\n\nMembers: Kai, Malik, Wren, Hana\nChat log (oldest first):\n[20 Feb 2026] Kai: @Hana Guaranteed I'll print the tenancy agreement by 27 Feb 2026.\n[21 Feb 2026] Wren: @Kai As long as the gas safety inspection is on, I will return the bin rota by 25 Feb 2026.\n[22 Feb 2026] Wren: @Kai No need to print the tenancy agreement, I'm letting you off\n[23 Feb 2026] Hana: We are dropping the gas safety inspection from the list.\n[28 Feb 2026] Kai: @Hana Quick report: I've managed to print the tenancy agreement",
  "question": "Is the promise Kai made to print the tenancy agreement not kept by 4 Mar 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q6e400ff6b8",
  "kind": "choice",
  "text": "Shared by Kofi, an export of a household chat about the caring rota, as saved.\n\nMembers: Kofi, Elif, Greta\nChat log (oldest first):\n[16 Sep 2026] Greta: @Elif Count on me to wash the bed linen by 21 Sep 2026 if the home assessment is on.\n[19 Sep 2026] Kofi: Really pleased to say the home assessment will go ahead!\n[19 Sep 2026] Greta: @Elif Mate, I promised, may I wash the bed linen by 23 Sep 2026 instead?\n[19 Sep 2026] Kofi: @Greta Revised deadline is 23 Sep 2026, so you can wash the bed linen.\n[21 Sep 2026] Elif: Hey, any luck with trying to wash the bed linen?\n[22 Sep 2026] Greta: @Kofi It's on me to drop off the hot meals by 24 Sep 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Greta's promise to wash the bed linen stand at the end of 21 Sep 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not yet due",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q3555bc71ab",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the garden shed build\nThe chat below comes from Tomas, copied as is for reference.\n\nMembers: Lena, Mo, Hana, Tomas\nChat log (oldest first):\n[24 Apr 2026] Hana: @Lena It's on me to stake the tomato canes by 1 May 2026.\n[25 Apr 2026] Lena: How's the plan to stake the tomato canes?\n[30 Apr 2026] Hana: @Lena On my action item, may I stake the tomato canes by 4 May 2026 instead?\n[30 Apr 2026] Lena: @Hana Yes, lovely, you can stake the tomato canes by 4 May 2026 instead!\n[30 Apr 2026] Hana: @Lena For the record: I was able to stake the tomato canes\n[4 May 2026] Mo: @Hana I will dig the potato patch by 6 May 2026 only if the plot inspection happens.\n[4 May 2026] Tomas: Scrapping the plot inspection, apologies to all.\n[5 May 2026] Mo: @Tomas Count on me, I'll collect the seed potatoes by 9 May 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules, when is the date by which Hana has to stake the tomato canes at the end of 2 May 2026, allowing for any agreed change?",
  "options": [
   "1 May 2026",
   "6 May 2026",
   "4 May 2026"
  ]
 },
 {
  "qid": "q1431c1128c",
  "kind": "yes/no",
  "text": "Chat about the choir tour, from the support queue, gathered by Oskar.\n\nMembers: Tess, Oskar, Zara\nChat log (oldest first):\n[22 Aug 2026] Zara: Hoping to fix the stand microphones by 31 Aug 2026, no promises.\n[24 Aug 2026] Zara: @Tess I own this, I'll fix the stand microphones by 1 Sep 2026.\n[26 Aug 2026] Zara: @Tess Count on me to set up the sound desk by 28 Aug 2026, if the voice test happens.\n[26 Aug 2026] Zara: Sad to report that the voice test is off.\n[29 Aug 2026] Zara: @Tess I own this, I'll buy the spare folders by 4 Sep 2026.\n[1 Sep 2026] Zara: @Tess Quick report: I've managed to fix the stand microphones",
  "question": "Does the card's rule set show that Zara has not kept the promise to fix the stand microphones at the end of 1 Sep 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0c063c0847",
  "kind": "choice",
  "text": "This export holds the messages about the caring rota, which Femi saved.\n\nMembers: Ravi, Femi, Mo, Zara\nChat log (oldest first):\n[20 Sep 2026] Zara: @Ravi Count on me to call the home nurse by 28 September 2026.\n[26 Sep 2026] Zara: @Ravi I committed to call the home nurse, can I do that by 4 October 2026 instead?\n[27 Sep 2026] Femi: @Zara That suits me, so please call the home nurse by 4 October 2026 instead.\n[30 Sep 2026] Femi: @Zara I'll pick up the repeat prescription by 6 October 2026, provided the family care meeting happens.\n[30 Sep 2026] Mo: Just so you know, the family care meeting is on as scheduled.\n[1 Oct 2026] Ravi: @Femi Count on me, I'll set up the medicine dispenser by 6 October 2026.\n[1 Oct 2026] Ravi: @Zara I promise to collect the post by 8 October 2026 if the eye test is on.\n[4 Oct 2026] Femi: @Ravi No need to set up the medicine dispenser, I'm letting you off",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs things stand at the end of 3 October 2026, which date is the deadline for Zara to call the home nurse, with any agreed change applied?",
  "options": [
   "4 October 2026",
   "28 September 2026",
   "6 October 2026"
  ]
 },
 {
  "qid": "qb897808987",
  "kind": "choice",
  "text": "This short note between tenants and a landlord covers the balcony garden project. Saved by Rhea for the record.\n\nMembers: Priya, Zara, Kai, Rhea\nChat log (oldest first):\n[1 Sep 2026] Kai: @Zara I'll ring the flat repair line by 9 Sep 2026, provided the window cleaner visit happens.\n[6 Sep 2026] Rhea: @Zara Count on me to remove the bathroom shelf by 15 Sep 2026.\n[7 Sep 2026] Zara: @Rhea Lovely, I'll email the leak photos by 13 Sep 2026 for sure.\n[8 Sep 2026] Kai: On track for the window cleaner visit to happen as planned.\n[8 Sep 2026] Zara: @Rhea Any chance I can email the leak photos by 15 Sep 2026 instead?\n[13 Sep 2026] Rhea: @Zara We are holding the date on record, so email the leak photos by it.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 9 Sep 2026, what status has Kai's promise to ring the flat repair line got?",
  "options": [
   "Not yet due",
   "Waived",
   "Kept",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "qe6bb583480",
  "kind": "yes/no",
  "text": "Subject: Chat about the family history\nBelow, with Elif named as the source, is the chat as exported.\n\nMembers: Tess, Mo, Ines, Elif\nChat log (oldest first):\n[16 Apr 2026] Ines: @Mo I'll pay the catering company by 20 April 2026, provided the family quiz happens.\n[17 Apr 2026] Tess: Just so you know, the family quiz is on as scheduled.\n[18 Apr 2026] Ines: @Tess Absolutely, I will label the memory box by 25 April 2026.\n[18 Apr 2026] Ines: @Tess I regret to say that I shall not label the memory box.\n[21 Apr 2026] Ines: @Mo Guess who managed to pay the catering company, go team!",
  "question": "Would you say Ines kept the promise to pay the catering company at the end of 23 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3e6281e01b",
  "kind": "choice",
  "text": "Subject: exported chat about the choir tour\nHere it is for you, from Leila, exactly as saved.\n\nMembers: Leila, Tomas, Yuki, Ines\nChat log (oldest first):\n[3 May 2026] Tomas: @Ines I own this, I'll book the rehearsal room by 8 May 2026.\n[6 May 2026] Ines: @Yuki I'll send the audition reminders by 12 May 2026, providing the sing along goes ahead.\n[6 May 2026] Tomas: Quick heads up, the sing along is scrapped.\n[7 May 2026] Leila: @Ines I promise to fix the stand microphones by 9 May 2026.\n[9 May 2026] Ines: @Tomas I'll be sure to move the piano by 11 May 2026.\n[10 May 2026] Tomas: @Ines Guess what, I managed to book the rehearsal room!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, what's the situation with Ines's promise to send the audition reminders at the end of 9 May 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "qbe1b1fedf9",
  "kind": "choice",
  "text": "Here is the trip itinerary, posted by Omar for the family to read.\n\nMembers: Omar, Priya, Elif\nChat export (date | from | to | message):\n2026-04-24 | Elif | Omar | I'll book the airport parking by 29 Apr 2026, promise.\n2026-04-28 | Priya | Omar | Absolutely, I will send the packing list by 6 May 2026.\n2026-04-30 | Elif | Priya | Provided the hotel arrival happens, I'll return the rental car keys by 2 May 2026.\n2026-04-30 | Elif | group | Sorry all, the hotel arrival is not happening.\n2026-05-04 | Priya | Omar | Any chance I can send the packing list by 11 May 2026 instead?\n2026-05-05 | Omar | Priya | Nah, the date's staying put, so you can send the packing list.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Priya made to send the packing list is in which status at the end of 5 May 2026?",
  "options": [
   "Broken",
   "Waived",
   "Not yet due",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "qc5aa976792",
  "kind": "yes/no",
  "text": "Landlord and renters' group talk on the street watch scheme, from Priya's export.\n\nMembers: Hana, Nadia, Priya\nChat log (oldest first):\n[8 Jul 2026] Hana: @Nadia I will return the ladders by 16 Jul 2026 only if the road works meeting happens.\n[8 Jul 2026] Nadia: @Hana Lovely, I'll walk the old spaniel by 12 Jul 2026 for sure.\n[9 Jul 2026] Priya: @Nadia Count on me to take in the post by 13 Jul 2026, if the speed camera survey happens.\n[11 Jul 2026] Nadia: @Hana I regret to say that I shall not walk the old spaniel.\n[12 Jul 2026] Priya: @Nadia Forget it, you won't need to walk the old spaniel",
  "question": "Would you call Nadia's promise to walk the old spaniel broken, waived, not triggered or not yet due, instead of kept, at the end of 17 Jul 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q08094eeb48",
  "kind": "choice",
  "text": "Support: help desk chat\nSubject: the family day out\nSaved by: Nadia\n\nMembers: Sami, Greta, Nadia, Omar\nChat log (oldest first):\n[17 Feb 2026] Sami: @Nadia Lovely, I'll fetch the craft box by 21 February 2026 for sure.\n[18 Feb 2026] Sami: @Nadia Can I fetch the craft box by 26 February 2026 instead? I did promise, sorry.\n[21 Feb 2026] Omar: @Greta It's on me to mend the kite string by 1 March 2026.\n[21 Feb 2026] Nadia: @Sami No, you need to fetch the craft box by the original date.\n[21 Feb 2026] Sami: @Nadia Update on my side: I will not fetch the craft box, sorry.\n[21 Feb 2026] Omar: @Sami Please don't feel you have to fetch the craft box\n[24 Feb 2026] Sami: @Greta I'll bake the oat biscuits by 27 February 2026 if the seaside outing goes ahead.\n[26 Feb 2026] Sami: Update: the seaside outing is going ahead as planned.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, what is the deadline for Sami to fetch the craft box at the end of 24 February 2026, with any agreed change of date counted?",
  "options": [
   "1 March 2026",
   "21 February 2026",
   "26 February 2026"
  ]
 },
 {
  "qid": "qec4068c271",
  "kind": "choice",
  "text": "Here is the thread on the big house plan, posted by Kai for the house.\n\nMembers: Mo, Kai, Oskar, Arlo\nChat log (oldest first):\n[7 Sep 2026] Kai: @Arlo Provided the ghost tour happens, I'll bleed the attic radiators by 15 Sep 2026.\n[10 Sep 2026] Arlo: @Kai Guaranteed I'll mend the garden gate by 18 Sep 2026.\n[10 Sep 2026] Arlo: @Kai I'll be sure to find the loft ladder by 16 Sep 2026.\n[11 Sep 2026] Arlo: We are dropping the ghost tour from the list.\n[18 Sep 2026] Arlo: @Kai On my action item, may I mend the garden gate by 20 Sep 2026 instead?\n[18 Sep 2026] Kai: @Arlo Yes, all good for you to mend the garden gate by 20 Sep 2026 instead.\n[20 Sep 2026] Arlo: @Kai To my relief, I managed to mend the garden gate.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Arlo supposed to mend the garden gate by, going by the chat at the end of 2 Oct 2026 and any agreed changes?",
  "options": [
   "18 Sep 2026",
   "20 Sep 2026",
   "16 Sep 2026"
  ]
 },
 {
  "qid": "q8dee090269",
  "kind": "choice",
  "text": "{\"saved_copy\": \"the music library\", \"keeper\": \"Nadia\", \"medium\": \"chat transcript\"}\n\nMembers: Tess, Tomas, Ana, Nadia\nChat log (oldest first):\n[21 Jan 2026] Nadia: @Tess If the joint concert goes ahead, I'll gladly collect the sheet music by 28 January 2026.\n[23 Jan 2026] Nadia: @Tess Count on me, I'll book the rehearsal room by 30 January 2026.\n[25 Jan 2026] Tomas: Update on your plan to book the rehearsal room?\n[25 Jan 2026] Tess: Sorry all, the joint concert is not happening.\n[29 Jan 2026] Nadia: @Tess Is 5 February 2026 alright for me to book the rehearsal room?\n[29 Jan 2026] Tess: @Nadia Nobody needs you to book the rehearsal room, that's that",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Nadia's promise to book the rehearsal room at the end of 31 January 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Waived",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q40e61009b1",
  "kind": "yes/no",
  "text": "Team chat export\nAbout the mobile release, saved by Elif from the channel.\n\nMembers: Mo, Elif\nChat log (oldest first):\n[17 May 2026] Mo: @Elif I promise to write the release notes by 20 May 2026 if the server migration is on.\n[17 May 2026] Mo: Team, the server migration stays on as booked.\n[19 May 2026] Mo: @Elif You can bank on me to update the dependency list by 27 May 2026.\n[20 May 2026] Mo: @Elif Guess what, I managed to write the release notes!\n[22 May 2026] Elif: @Mo I will fix the test runner by 26 May 2026.",
  "question": "Is the promise to write the release notes that Mo made broken at the end of 24 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q7657a49f9d",
  "kind": "choice",
  "text": "Freelance thread record, the payment setup, shared by Zara.\n\nMembers: Lena, Kai, Zara\nChat log (oldest first):\n[20 Apr 2026] Kai: @Zara If the pop up stall goes ahead, I'll send the stock spreadsheet by 25 April 2026.\n[20 Apr 2026] Lena: @Zara Relax, I'll set up the email forwarding by 24 April 2026 for sure.\n[24 Apr 2026] Lena: Sorry, the pop up stall is off.\n[24 Apr 2026] Lena: @Zara Mind giving me until 28 April 2026 to set up the email forwarding?\n[24 Apr 2026] Zara: @Lena Nah, that deadline counts, mate, so please set up the email forwarding!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nPer the card's rules for reading the chat, which status belongs to the promise Kai made to send the stock spreadsheet at the end of 27 April 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q21074b7a12",
  "kind": "yes/no",
  "text": "Team channel: the peer review\nExported by Bruno.\n\nMembers: Bruno, Lee, Malik\nChat log (oldest first):\n[19 Feb 2026] Lee: @Malik Lovely, I'll order the reagent kit by 26 Feb 2026 if the safety inspection is on.\n[20 Feb 2026] Malik: @Lee Provided the conference trip happens, I will return the library books by 28 Feb 2026.\n[22 Feb 2026] Malik: Team, the conference trip is not happening.\n[23 Feb 2026] Malik: @Bruno You can bet I'll print the poster abstracts by 3 Mar 2026.\n[25 Feb 2026] Malik: @Lee Is 6 Mar 2026 alright for me to return the library books?\n[28 Feb 2026] Bruno: @Malik Fine by me, you can return the library books by 6 Mar 2026.",
  "question": "Did Malik keep the promise to return the library books as of 3 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qaf9ab3ea1e",
  "kind": "yes/no",
  "text": "{\"thread_kind\": \"exported conversation\", \"about\": \"the guest welcome plan\", \"exported_by\": \"Rhea\"}\n\nMembers: Lena, Kai, Rhea\nChat log (oldest first):\n[3 Oct 2026] Rhea: @Kai I'll collect the bed linen by Monday, October 12, 2026 if the guest arrival evening goes ahead.\n[4 Oct 2026] Kai: @Lena Committing to scrub the hot tub by Sunday, October 11, 2026.\n[5 Oct 2026] Kai: @Lena Ticked off my list: scrub the hot tub, yay.\n[6 Oct 2026] Kai: Update, the guest arrival evening will not take place.\n[8 Oct 2026] Lena: @Rhea I own this, I'll wheel the bins out by Saturday, October 17, 2026.\n[9 Oct 2026] Rhea: Hey, did you get a chance to scrub the hot tub?",
  "question": "Would Kai be counted as having broken the promise to scrub the hot tub at the end of Wednesday, October 7, 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q5a6f73f517",
  "kind": "choice",
  "text": "Channel: work team chat\nTopic: the data cleanup\nExported by Oskar.\n\nMembers: Hana, Wren, Oskar\nChat log (oldest first):\n[4 May 2026] Oskar: @Hana If the code freeze goes ahead, I'll merge the login branch by 12 May 2026.\n[6 May 2026] Hana: @Wren I promise to rotate the test keys by 11 May 2026.\n[6 May 2026] Hana: @Wren Relax, I'll fix the test runner by 10 May 2026, promise.\n[10 May 2026] Oskar: @Hana I assure you I'll restart the build server by 13 May 2026 if the planning session is on.\n[10 May 2026] Oskar: Brilliant news everyone, the planning session is a go!\n[11 May 2026] Oskar: @Hana Can I restart the build server by 17 May 2026 instead? I did promise, sorry.\n[11 May 2026] Hana: @Oskar Yes, all good for you to restart the build server by 17 May 2026 instead.\n[20 May 2026] Oskar: @Hana Guess who managed to restart the build server, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Hana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Oskar supposed to restart the build server by, going by the chat at the end of 19 May 2026 and any agreed changes?",
  "options": [
   "17 May 2026",
   "10 May 2026",
   "13 May 2026"
  ]
 },
 {
  "qid": "q356b60d6b5",
  "kind": "choice",
  "text": "Club chat exported by Greta, the local thread about the music library.\n\nMembers: Greta, Ravi, Bruno\nChat log (oldest first):\n[7 Jan 2026] Bruno: @Greta If the voice test is on, I'll definitely book the rehearsal room by 16 Jan 2026.\n[8 Jan 2026] Ravi: @Greta Lovely, I'll buy the spare folders by 15 Jan 2026 if the joint concert is on.\n[13 Jan 2026] Ravi: Yep, the joint concert is on as planned.\n[13 Jan 2026] Ravi: @Greta Mind giving me until 19 Jan 2026 to buy the spare folders?\n[13 Jan 2026] Bruno: @Ravi Yes, you have the green light to buy the spare folders by 19 Jan 2026.\n[15 Jan 2026] Bruno: @Ravi Guaranteed I'll fix the stand microphones by 18 Jan 2026.\n[19 Jan 2026] Ravi: @Greta For the record: I was able to buy the spare folders\n[20 Jan 2026] Bruno: @Ravi To note: I have managed to fix the stand microphones",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Ravi supposed to buy the spare folders by, going by the chat at the end of 13 Jan 2026 and any agreed changes?",
  "options": [
   "19 Jan 2026",
   "15 Jan 2026",
   "16 Jan 2026"
  ]
 },
 {
  "qid": "qe277135c9e",
  "kind": "yes/no",
  "text": "Saved by Arlo, this copy of the support chat concerns the guest list.\n\nMembers: Arlo, Rhea, Wren, Priya\nChat log (oldest first):\n[19 Jul 2026] Rhea: @Arlo It's on me to pick up the album prints by 2026-07-24.\n[19 Jul 2026] Arlo: @Wren I promise to book the assistant photographer by 2026-07-28.\n[20 Jul 2026] Arlo: @Wren I promise to print the seating cards by 2026-07-27 if the ceremony walkthrough is on.\n[21 Jul 2026] Wren: @Rhea I promise to fetch the spare memory cards by 2026-07-27 if the venue visit is on.\n[24 Jul 2026] Rhea: @Arlo To note: I have managed to pick up the album prints\n[26 Jul 2026] Wren: Sorry all, the venue visit is called off.",
  "question": "Under the rules on the card, is the promise Rhea made to pick up the album prints kept as of 2026-07-24?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
