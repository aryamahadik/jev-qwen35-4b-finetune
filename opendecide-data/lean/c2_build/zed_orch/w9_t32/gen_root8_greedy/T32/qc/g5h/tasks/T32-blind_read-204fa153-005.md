# G5-H blind read T32-blind_read-204fa153-005 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root8/T32/qc/g5h/answers/T32-blind_read-204fa153-005.json

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
  "qid": "q12faecc289",
  "kind": "choice",
  "text": "A written chat between housemates about the reunion weekend. Exported from the device by Nadia.\n\nMembers: Leila, Nadia, Rhea\nChat log (oldest first):\n[6 Aug 2026] Nadia: @Leila I'll collect the old photo prints by Saturday, 8 August 2026 as long as the grandparents visit is on.\n[7 Aug 2026] Nadia: Sorry, the grandparents visit is off.\n[7 Aug 2026] Rhea: @Nadia No promises, but I'll aim to send the group invitations by Tuesday, 11 August 2026.\n[8 Aug 2026] Rhea: @Leila Absolutely, I will send the group invitations by Wednesday, 12 August 2026.\n[9 Aug 2026] Nadia: @Rhea Don't sweat it, there's no need to send the group invitations\n[9 Aug 2026] Rhea: @Leila To my relief, I managed to send the group invitations.\n\nSummary note: Every promise listed here is covered by the group's blanket permission, which extends to Nadia.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing through the chat for that day, which status goes with the promise Rhea made to send the group invitations at the end of Wednesday, 12 August 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q708bfb7a8d",
  "kind": "choice",
  "text": "Work team channel\nSaved by Zara, which talks about the onboarding flow.\n\nMembers: Sami, Zara\nChat log (oldest first):\n[3 May 2026] Sami: Wish me luck, hoping to review the pull request by 14 May 2026.\n[5 May 2026] Sami: @Zara I'll be sure to review the pull request by 10 May 2026.\n[8 May 2026] Sami: @Zara I assure you I'll merge the login branch by 16 May 2026 if the code freeze is on.\n[9 May 2026] Zara: @Sami Provided the hackathon happens, I will label the bug reports by 18 May 2026.\n[10 May 2026] Zara: @Sami I own this, I'll rotate the test keys by 17 May 2026.\n[12 May 2026] Sami: @Zara Log entry: review the pull request, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Sami's promise to review the pull request have at the end of 12 May 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Broken",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q1a7abcf75d",
  "kind": "yes/no",
  "text": "{\"chat_export\": \"the annual tour\", \"saved_by\": \"Ivo\", \"scope\": \"group chat\"}\n\nMembers: Elif, Ivo, Omar\nChat log (oldest first):\n[8 May 2026] Ivo: @Elif Count on me to tune the gear cables by May 16, 2026 if the group ride is on.\n[8 May 2026] Omar: @Elif Got it, I'll service the tandem bike by May 13, 2026 for sure.\n[9 May 2026] Ivo: @Omar Aiming to fetch the bike stand by May 21, 2026, we'll see.\n[11 May 2026] Ivo: @Elif Ticket's mine, I'll fetch the bike stand by May 17, 2026.\n[12 May 2026] Elif: @Ivo Count on me to wash the club jerseys by May 20, 2026, if the club sportive happens.\n[17 May 2026] Ivo: @Elif Ticked off my list: fetch the bike stand, yay.\n\nAdmin sign-off: plans changed in this chat carry the admins' blessing, so Ivo can move on.",
  "question": "Is it true under the card's rules that Ivo has kept the promise to fetch the bike stand at the end of May 21, 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0d4564451c",
  "kind": "choice",
  "text": "Subject: chat about the visitor policy, forwarded\nThe chat follows below.\nRegards, Tess\n\nMembers: Tess, Rhea, Elif\nChat log (oldest first):\n[10 May 2026] Elif: @Rhea Count on me to book the boardroom by Monday, May 18, 2026, if the team lunch happens.\n[11 May 2026] Elif: @Rhea I will renew the fire extinguisher service by Sunday, May 17, 2026 only if the staff picnic happens.\n[11 May 2026] Elif: Yep, the team lunch is on as planned.\n[14 May 2026] Elif: @Rhea You can bet I'll send the expense receipts by Friday, May 22, 2026.\n[16 May 2026] Elif: @Rhea Mind giving me until Wednesday, May 20, 2026 to book the boardroom?\n[18 May 2026] Rhea: @Elif Fine by me, you can book the boardroom by Wednesday, May 20, 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Elif's promise to book the boardroom at the end of Monday, May 25, 2026?",
  "options": [
   "Waived",
   "Kept",
   "Broken",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "qbcc82c50f6",
  "kind": "yes/no",
  "text": "Note above a chat from the support case, covering the new repertoire, shared by Priya.\n\nMembers: Rhea, Priya, Malik\nChat log (oldest first):\n[2 Mar 2026] Malik: @Rhea You can bet I'll send the audition reminders by 10 Mar 2026.\n[3 Mar 2026] Malik: @Rhea I'll try to fetch the choir robes by 9 Mar 2026, no guarantee.\n[4 Mar 2026] Malik: @Rhea If the summer recital goes ahead, I'll fetch the choir robes by 7 Mar 2026.\n[6 Mar 2026] Malik: Afraid the summer recital is called off.\n[7 Mar 2026] Priya: @Rhea I will print the song sheets by 11 Mar 2026.\n[11 Mar 2026] Rhea: @Priya Don't sweat it, there's no need to print the song sheets",
  "question": "Is it true that the promise Malik made to fetch the choir robes has not been broken at the end of 9 Mar 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd138b943bf",
  "kind": "yes/no",
  "text": "Thread filed under support\nAbout the annual tour, saved by Leila.\n\nMembers: Ana, Leila, Greta, Malik\nChat log (oldest first):\n[29 Jan 2026] Leila: @Malik Hoping to print the route cards by 5 Feb 2026, can't promise.\n[29 Jan 2026] Malik: @Greta I'll return the loaned helmets by 2 Feb 2026 if the mechanics clinic goes ahead.\n[29 Jan 2026] Ana: On track for the mechanics clinic to happen as planned.\n[31 Jan 2026] Leila: @Ana Relax, I'll print the route cards by 4 Feb 2026, promise.\n[2 Feb 2026] Malik: @Leila Ah, no stress, no need for you to print the route cards\n[4 Feb 2026] Leila: @Ana Ticked off my list: print the route cards, yay.",
  "question": "Is Leila's promise to print the route cards kept on 9 Feb 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q3de45c459e",
  "kind": "yes/no",
  "text": "Committee chat on the kit sponsorship, forwarded by Yuki to the volunteers.\n\nMembers: Yuki, Ivo\nChat log (oldest first):\n[31 Jul 2026] Yuki: @Ivo You can bank on me to set up the corner flags by 4 Aug 2026.\n[31 Jul 2026] Yuki: @Ivo I own this, I'll mark the pitch lines by 4 Aug 2026.\n[3 Aug 2026] Yuki: @Ivo I own this, I'll return the bib sets by 11 Aug 2026.\n[3 Aug 2026] Ivo: @Yuki Only if the presentation evening is on, I will print the team sheets by 9 Aug 2026.\n[8 Aug 2026] Ivo: Lovely, the presentation evening is definitely happening!",
  "question": "Does the card classify Ivo's promise to print the team sheets as kept, instead of broken, waived, not triggered or not yet due, on 8 Aug 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q970c7890ef",
  "kind": "yes/no",
  "text": "Work channel holding the field survey, export saved by Wren.\n\nMembers: Mo, Oskar, Wren, Ana\nChat log (oldest first):\n[19 Aug 2026] Oskar: @Mo Count on me to book the microscope slot by 27 August 2026 if the thesis defence is on.\n[21 Aug 2026] Mo: Brilliant news everyone, the thesis defence is a go!\n[23 Aug 2026] Mo: @Wren Count on me to return the library books by 26 August 2026.\n[24 Aug 2026] Mo: @Ana Count on me to collect the lab samples by 28 August 2026.\n[26 Aug 2026] Mo: @Wren To my relief, I managed to return the library books.",
  "question": "Under the rules on the card, is the promise Mo made to return the library books kept as of 29 August 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q59e7b3a8a3",
  "kind": "yes/no",
  "text": "{\"archive\": \"group chat\", \"subject\": \"the mobile release\", \"sent_by\": \"Ravi\"}\n\nMembers: Bruno, Malik, Ravi\nChat log (oldest first):\n[21 Mar 2026] Malik: @Ravi It's on me to label the bug reports by 26 Mar 2026.\n[25 Mar 2026] Bruno: @Ravi Count on me to review the pull request by 29 Mar 2026, if the planning session happens.\n[26 Mar 2026] Bruno: @Ravi I assure you I'll fix the test runner by 31 Mar 2026 if the hackathon is on.\n[27 Mar 2026] Ravi: Please note the hackathon will proceed.\n[27 Mar 2026] Malik: @Ravi Committing to merge the login branch by 4 Apr 2026.\n[1 Apr 2026] Bruno: @Ravi Mum, I did fix the test runner, haha.",
  "question": "At the end of 3 Apr 2026, has the promise Bruno made to fix the test runner been broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q86a3528671",
  "kind": "yes/no",
  "text": "Subject: copy of the chat about the cottage refresh\nFor your records, the saved chat is below, from Bruno.\n\nMembers: Bruno, Sami, Lee\nChat log (oldest first):\n[10 Aug 2026] Sami: I'll try to collect the bed linen by Wednesday, 19 August 2026, no guarantee.\n[12 Aug 2026] Sami: @Lee Provided the summer season launch happens, I'll collect the bed linen by Saturday, 15 August 2026.\n[14 Aug 2026] Bruno: Update: the summer season launch is going ahead as planned.\n[14 Aug 2026] Sami: @Lee I regret to say that I shall not collect the bed linen.\n[14 Aug 2026] Lee: @Bruno I will make sure to scrub the hot tub by Tuesday, 18 August 2026.\n[16 Aug 2026] Lee: @Bruno Sorry, I won't scrub the hot tub after all",
  "question": "Looking over the chat at the end of Monday, 17 August 2026, did Sami break the promise to collect the bed linen?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q093caac1c4",
  "kind": "choice",
  "text": "Shared by Lena, this is where the street watch scheme gets planned.\n\nMembers: Sami, Malik, Lena, Femi\nChat log (oldest first):\n[17 Mar 2026] Femi: @Lena You can bet I'll feed the cat across the road by 20 March 2026.\n[17 Mar 2026] Sami: @Lena Count on me to share the garden hose by 23 March 2026.\n[20 Mar 2026] Malik: @Femi No need to feed the cat across the road, I'm letting you off\n[21 Mar 2026] Femi: @Sami I will walk the old spaniel by 28 March 2026 only if the road works meeting happens.\n[23 Mar 2026] Lena: @Sami Please don't feel you have to share the garden hose\n[26 Mar 2026] Femi: Please note the road works meeting will proceed.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 26 March 2026, what status has Sami's promise to share the garden hose got?",
  "options": [
   "Not triggered",
   "Waived",
   "Not yet due",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "qbd42e4c85d",
  "kind": "yes/no",
  "text": "Committee chat on the music library, shared by Tomas with the volunteers.\n\nMembers: Sami, Mo, Tomas, Greta\nChat log (oldest first):\n[28 Aug 2026] Sami: @Mo I promise to move the piano by 2 Sep 2026 if the choir festival is on.\n[30 Aug 2026] Tomas: Great news, the choir festival is on!\n[2 Sep 2026] Greta: @Sami Forget it, you won't need to move the piano\n[3 Sep 2026] Greta: @Tomas Count on me to return the library scores by 12 Sep 2026.\n[3 Sep 2026] Mo: @Greta Count on me, I'll fetch the choir robes by 5 Sep 2026.\n[5 Sep 2026] Greta: @Tomas Ticked off my list: return the library scores, yay.",
  "question": "Under the rules on the card, is the promise Sami made to move the piano in a status other than broken at the end of 2 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qe7b4fc9352",
  "kind": "yes/no",
  "text": "Thread filed under support\nAbout the shop rebuild, saved by Kai.\n\nMembers: Wren, Bruno, Mo, Kai\nChat log (oldest first):\n[17 Feb 2026] Wren: @Mo I'll restore the old theme by Saturday, 21 February 2026, providing the site handover goes ahead.\n[19 Feb 2026] Bruno: @Mo I will add the size chart by Wednesday, 25 February 2026.\n[20 Feb 2026] Mo: On track for the site handover to happen as planned.\n[21 Feb 2026] Wren: @Mo Log entry: restore the old theme, carried out\n[25 Feb 2026] Bruno: @Mo My sincere apologies, I am unable to add the size chart.",
  "question": "Is Wren's promise to restore the old theme kept at the end of Saturday, 21 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q8d2fa4b1b2",
  "kind": "choice",
  "text": "Subject: forwarded chat, the training plan\nWord for word, the text below came from the saved copy.\nBest, Oskar\n\nMembers: Oskar, Nadia, Ravi\nChat log (oldest first):\n[22 Feb 2026] Ravi: @Oskar Promise to tune the gear cables by February 26, 2026 if the swap meet goes ahead.\n[25 Feb 2026] Nadia: @Ravi As long as the mechanics clinic is on, I will service the tandem bike by March 1, 2026.\n[25 Feb 2026] Nadia: @Oskar You can bet I'll print the route cards by March 1, 2026.\n[25 Feb 2026] Nadia: Sorry all, the swap meet is not happening.\n[26 Feb 2026] Ravi: @Oskar Relax, I'll pump the spare tyres by March 2, 2026 for sure.\n[26 Feb 2026] Ravi: @Oskar Log entry: pump the spare tyres, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhere does Ravi stand on the promise to pump the spare tyres at the end of March 4, 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q890f55970a",
  "kind": "yes/no",
  "text": "{\"source\": \"saved thread\", \"about\": \"the kit sponsorship\", \"owner\": \"Ravi\", \"kind\": \"chat export\"}\n\nMembers: Elif, Oskar, Ravi, Rhea\nChat log (oldest first):\n[20 Mar 2026] Elif: @Rhea I promise to set up the corner flags by 24 Mar 2026 if the training camp is on.\n[20 Mar 2026] Ravi: On track for the training camp to happen as planned.\n[24 Mar 2026] Ravi: @Rhea I will make sure to pump the match balls by 27 Mar 2026.\n[24 Mar 2026] Rhea: @Elif Quick update: you do not need to set up the corner flags at all.\n[25 Mar 2026] Ravi: @Rhea I'm withdrawing my promise to pump the match balls\n[27 Mar 2026] Oskar: How's the plan to set up the corner flags?",
  "question": "Has Elif kept the promise to set up the corner flags at the end of 25 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q561535441b",
  "kind": "choice",
  "text": "Subject: group chat about the autumn term budget, exported by Femi\nForwarding the chat below for your reference.\n\nMembers: Tomas, Priya, Malik, Femi\nChat log (oldest first):\n[7 May 2026] Tomas: @Malik I'll photograph the bathroom mould by 10 May 2026, providing the house hunting viewing goes ahead.\n[9 May 2026] Tomas: Quick heads up, the house hunting viewing is scrapped.\n[9 May 2026] Tomas: @Malik Think 15 May 2026 would work if I photograph the bathroom mould instead?\n[9 May 2026] Malik: @Tomas No, I'd like you to photograph the bathroom mould by the original date.\n[10 May 2026] Femi: @Tomas Lovely, I'll copy the house keys by 13 May 2026 for sure.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Femi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 12 May 2026, what status has Tomas's promise to photograph the bathroom mould got?",
  "options": [
   "Waived",
   "Kept",
   "Not yet due",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q7372145dc5",
  "kind": "choice",
  "text": "Shared by Priya, a help-desk thread covering the grant renewal.\n\nMembers: Jonas, Priya, Elif, Ana\nChat export (date | from | to | message):\n2026-01-12 | Jonas | Ana | I assure you I'll submit the ethics application by 14 January 2026 if the safety inspection is on.\n2026-01-12 | Ana | Elif | I'll collect the lab samples by 14 January 2026, providing the journal club goes ahead.\n2026-01-13 | Priya | group | Fab, we are on for the safety inspection as planned!\n2026-01-14 | Ana | Priya | Guaranteed I'll book the microscope slot by 19 January 2026.\n2026-01-14 | Ana | Priya | Would it be fine if I book the microscope slot by 22 January 2026 instead, yeah?\n2026-01-14 | Priya | Ana | We are holding the date on record, so book the microscope slot by it.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Ana made to book the microscope slot is in which status at the end of 19 January 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Kept",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "qfa132b427e",
  "kind": "choice",
  "text": "Committee chat on the ground upgrade, shared by Oskar with the volunteers.\n\nMembers: Ana, Hana, Priya, Oskar\nChat log (oldest first):\n[31 May 2026] Hana: @Oskar Will attempt to repair the goal nets by 7 June 2026, can't promise.\n[2 Jun 2026] Hana: @Ana You can bank on me to repair the goal nets by 10 June 2026.\n[6 Jun 2026] Hana: @Ana I committed to repair the goal nets, can I do that by 13 June 2026 instead?\n[9 Jun 2026] Oskar: @Hana Yes, you have the green light to repair the goal nets by 13 June 2026.\n[9 Jun 2026] Oskar: @Ana Count on me to return the bib sets by 12 June 2026.\n[10 Jun 2026] Hana: @Priya I'll fetch the medical bag by 12 June 2026, provided the cup tie happens.\n[10 Jun 2026] Hana: Yay, the cup tie is all set to go!\n[12 Jun 2026] Hana: @Ana Sorry, I won't repair the goal nets after all",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat's the day Hana needs to repair the goal nets by at the end of 9 June 2026, after any new date the group agreed on?",
  "options": [
   "10 June 2026",
   "12 June 2026",
   "13 June 2026"
  ]
 },
 {
  "qid": "qad95351897",
  "kind": "choice",
  "text": "Here we plan the care plan together, and Zara saved this for the family.\n\nMembers: Greta, Ines, Kai, Zara\nChat log (oldest first):\n[6 Sep 2026] Greta: @Ines I'm aiming to pick up the repeat prescription by September 18, 2026, might manage it.\n[8 Sep 2026] Kai: @Ines As long as the hospital appointment is on, I will drop off the hot meals by September 11, 2026.\n[8 Sep 2026] Greta: @Zara I will make sure to pick up the repeat prescription by September 16, 2026.\n[8 Sep 2026] Kai: @Greta No need to pick up the repeat prescription, I'm letting you off\n[9 Sep 2026] Zara: Sorry all, the hospital appointment is called off.\n[9 Sep 2026] Greta: @Zara Mum, I did pick up the repeat prescription, haha.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Greta made to pick up the repeat prescription, what state is it in at the end of September 12, 2026?",
  "options": [
   "Kept",
   "Broken",
   "Waived",
   "Not triggered",
   "Not yet due"
  ]
 },
 {
  "qid": "q6f5a5b2cb6",
  "kind": "yes/no",
  "text": "Team chat header\nSubject line: the grant renewal, exported by Ana.\n\nMembers: Bruno, Arlo, Ana\nChat log (oldest first):\n[3 May 2026] Arlo: @Ana As long as the conference trip is on, I will submit the ethics application by 6 May 2026.\n[5 May 2026] Bruno: @Arlo If the seminar series goes ahead, I'll return the library books by 9 May 2026.\n[6 May 2026] Bruno: Please note the seminar series will proceed.\n[6 May 2026] Ana: @Arlo It's on me to scan the field notes by 10 May 2026.\n[8 May 2026] Bruno: @Arlo Guess who managed to return the library books, go team!\n[9 May 2026] Arlo: @Ana Forget it, you won't need to scan the field notes",
  "question": "By the end of 11 May 2026, has Bruno kept the promise to return the library books?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q0d7779c845",
  "kind": "choice",
  "text": "Subject: Chat about the spare room plan\nThe copy from Yuki follows below as a plain record.\n\nMembers: Lena, Lee, Yuki, Sami\nChat log (oldest first):\n[11 Jan 2026] Sami: @Lee Count on me, I'll replace the loo roll by 2026-01-18.\n[14 Jan 2026] Sami: @Yuki If the water tank check goes ahead, I'll gladly turn the heating timer by 2026-01-19.\n[15 Jan 2026] Yuki: Hey, did you get a chance to turn the heating timer?\n[18 Jan 2026] Yuki: Team, the water tank check stays on as booked.\n[18 Jan 2026] Sami: @Yuki Think 2026-01-24 would work if I turn the heating timer instead?\n[19 Jan 2026] Sami: @Yuki Quick report: I've managed to turn the heating timer",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Sami doing with the promise to turn the heating timer at the end of 2026-01-25?",
  "options": [
   "Waived",
   "Kept",
   "Not yet due",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q6cbbfd4b22",
  "kind": "choice",
  "text": "Freelance log for the sound mix\nSaved by Arlo from the client thread.\n\nMembers: Nadia, Arlo, Ravi, Oskar\nChat export (date | from | to | message):\n2026-09-11 | Oskar | Ravi | Guaranteed I'll upload the render files by 17 September 2026.\n2026-09-14 | Oskar | Ravi | On my action item, may I upload the render files by 21 September 2026 instead?\n2026-09-14 | Ravi | Oskar | That suits me, so please upload the render files by 21 September 2026 instead.\n2026-09-15 | Arlo | Oskar | Not promising, but I'll try to record the voice over by 24 September 2026.\n2026-09-16 | Arlo | Nadia | I'll record the voice over by 23 September 2026 as long as the agency review call is on.\n2026-09-22 | Nadia | group | Fab, we are on for the agency review call as planned!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of 25 September 2026, which status does Arlo have for the promise to record the voice over?",
  "options": [
   "Not triggered",
   "Waived",
   "Broken",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q0d4fe33a54",
  "kind": "yes/no",
  "text": "Forwarded from the volunteer committee's group, with the training plan at the centre, by Kai.\n\nMembers: Kai, Priya, Lena, Leila\nChat log (oldest first):\n[29 Apr 2026] Kai: @Lena Relax, I'll stock the energy gels by 8 May 2026 for sure.\n[29 Apr 2026] Leila: @Kai I own this, I'll service the tandem bike by 4 May 2026.\n[2 May 2026] Kai: @Lena I assure you I'll fetch the bike stand by 5 May 2026 if the swap meet is on.\n[3 May 2026] Lena: @Leila Relax, I'll wash the club jerseys by 6 May 2026 for sure.\n[3 May 2026] Leila: Scrapping the swap meet, apologies to all.",
  "question": "Did Kai keep the promise to fetch the bike stand as of 3 May 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q55ccecd345",
  "kind": "yes/no",
  "text": "Support case copy, filed for the house refit\nSaved on record by Kofi\n\nMembers: Dara, Kofi, Ravi, Tomas\nChat export (date | from | to | message):\n2026-06-26 | Ravi | Dara | If the mortgage valuation visit goes ahead, I'll gladly pick up the grout bag by June 30, 2026.\n2026-06-29 | Tomas | Dara | Got it, I'll measure the hallway for shelves by July 5, 2026 for sure.\n2026-06-29 | Dara | group | Lovely, the mortgage valuation visit is definitely happening!\n2026-07-02 | Ravi | Dara | To note: I have managed to pick up the grout bag\n2026-07-04 | Ravi | Tomas | Please don't feel you have to measure the hallway for shelves",
  "question": "Did Ravi keep the promise to pick up the grout bag on July 1, 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q34e23cb02e",
  "kind": "choice",
  "text": "Saved chat on the loft conversion. Exported by Tess, unedited, from a household group.\n\nMembers: Sami, Tess, Jonas\nChat log (oldest first):\n[30 Apr 2026] Tess: @Sami I assure you I'll hang the new curtain rail by 4 May 2026 if the mortgage valuation visit is on.\n[1 May 2026] Jonas: @Tess I'll be sure to collect the sanding pads by 6 May 2026.\n[4 May 2026] Jonas: @Tess If the damp survey inspection goes ahead, I'll pay the plumbing invoice by 12 May 2026.\n[6 May 2026] Jonas: @Tess Mind giving me until 11 May 2026 to collect the sanding pads?\n[6 May 2026] Sami: @Jonas Revised deadline is 11 May 2026, so you can collect the sanding pads.\n[11 May 2026] Jonas: @Tess Quick report: I've managed to collect the sanding pads",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Jonas's promise to collect the sanding pads at the end of 11 May 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Not triggered",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "qe632d3e857",
  "kind": "choice",
  "text": "Our flat chat about the attic conversion idea, shared by Hana for whoever lives here.\n\nMembers: Yuki, Hana, Tess, Malik\nChat export (date | from | to | message):\n2026-02-10 | Hana | Malik | Count on me, I'll wipe the shared kitchen counter by 16 Feb 2026.\n2026-02-14 | Malik | Hana | If the house insurance review is on, I'll definitely turn the heating timer by 22 Feb 2026.\n2026-02-15 | Hana | Tess | I'll stock the spice rack by 21 Feb 2026, provided the water tank check happens.\n2026-02-20 | Tess | group | We are dropping the water tank check from the list.\n2026-02-20 | Hana | Tess | Mate, I promised, may I stock the spice rack by 25 Feb 2026 instead?\n2026-02-20 | Yuki | Hana | Yes, all good for you to stock the spice rack by 25 Feb 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Hana made to stock the spice rack is in which status at the end of 24 Feb 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Not triggered",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "qf4c99355c3",
  "kind": "yes/no",
  "text": "Team channel export\nDescription: the social media plan, saved by Wren.\n\nMembers: Wren, Ravi, Mo, Elif\nChat export (date | from | to | message):\n2026-03-12 | Elif | Wren | Provided the webinar rehearsal happens, I'll return the rented camera gear by 20 Mar 2026.\n2026-03-13 | Ravi | Mo | Absolutely, I will fetch the campaign budget sheet by 19 Mar 2026.\n2026-03-13 | Elif | group | Sad to report that the webinar rehearsal is off.\n2026-03-14 | Ravi | Wren | I will pay the printing invoice by 23 Mar 2026.\n2026-03-19 | Ravi | Mo | To note: I have managed to fetch the campaign budget sheet",
  "question": "Was Ravi's promise to fetch the campaign budget sheet not kept as of 19 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q9a16ba5056",
  "kind": "yes/no",
  "text": "Chat attached to the support case about the balcony garden project, shared by Jonas.\n\nMembers: Arlo, Jonas\nChat log (oldest first):\n[5 Jun 2026] Jonas: @Arlo Only if the flat viewing day is on, I will bring the step stool by June 10, 2026.\n[5 Jun 2026] Jonas: Brilliant news everyone, the flat viewing day is a go!\n[6 Jun 2026] Jonas: @Arlo It's on me to measure the kitchen for fridge by June 8, 2026.\n[8 Jun 2026] Jonas: @Arlo I promise to forward the gas bill by June 14, 2026.\n[8 Jun 2026] Arlo: @Jonas You don't have to bring the step stool at all\n[11 Jun 2026] Arlo: @Jonas Relax, mate, you're not expected to forward the gas bill",
  "question": "Is it right to say that Jonas has broken the promise to bring the step stool at the end of June 12, 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q424f746175",
  "kind": "yes/no",
  "text": "Jonas saved these replies from the agent on the cottage refresh.\n\nMembers: Dara, Arlo, Jonas\nChat log (oldest first):\n[5 Jun 2026] Jonas: @Dara I'll leave the welcome basket by 13 June 2026 as long as the summer season launch is on.\n[6 Jun 2026] Dara: @Arlo It's on me to restock the guest toiletries by 14 June 2026.\n[8 Jun 2026] Jonas: @Dara You can bank on me to collect the bed linen by 10 June 2026.\n[9 Jun 2026] Dara: Really pleased to say the summer season launch will go ahead!\n[9 Jun 2026] Jonas: @Dara Gutted to say I won't leave the welcome basket, sorry team",
  "question": "By the close of 10 June 2026, is the promise Jonas made to leave the welcome basket kept, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb2c38f64eb",
  "kind": "choice",
  "text": "Subject: chat export, the house refit\nHere is the full text.\nWarmly, Bruno\n\nMembers: Yuki, Bruno, Ivo, Priya\nChat export (date | from | to | message):\n2026-04-08 | Bruno | Ivo | It's on me to pick up the grout bag by 14 Apr 2026.\n2026-04-08 | Priya | Yuki | I'll fetch the paint samples by 13 Apr 2026 if the removal van arrival goes ahead.\n2026-04-08 | Priya | group | Yay, the removal van arrival is all set to go!\n2026-04-12 | Bruno | Ivo | Quick question, could I pick up the grout bag by 16 Apr 2026 instead?\n2026-04-13 | Ivo | Bruno | Yes, you have the green light to pick up the grout bag by 16 Apr 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Priya's promise to fetch the paint samples at the end of 13 Apr 2026?",
  "options": [
   "Kept",
   "Not triggered",
   "Waived",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q9145eb22a2",
  "kind": "choice",
  "text": "Thread between a landlord and tenants on the kitchen refit left as it was and shared by Ines.\n\nMembers: Ines, Arlo\nChat export (date | from | to | message):\n2026-05-24 | Arlo | Ines | Count on me to bring the step stool by 2 June 2026, if the electrics safety check happens.\n2026-05-25 | Arlo | Ines | Count on me to email the leak photos by 2 June 2026, if the flat viewing day happens.\n2026-05-26 | Arlo | Ines | I will make sure to read the meter readings by 1 June 2026.\n2026-05-26 | Arlo | Ines | Is 3 June 2026 alright for me to read the meter readings?\n2026-05-26 | Ines | Arlo | You can bank on me to wipe the cooker hood by 2 June 2026.\n2026-05-29 | Arlo | Ines | Got myself to read the meter readings lol.\n2026-05-29 | Ines | Arlo | Correction, I will not be able to wipe the cooker hood.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, what is the deadline for Arlo to read the meter readings at the end of 30 May 2026, with any agreed change of date counted?",
  "options": [
   "3 June 2026",
   "1 June 2026",
   "2 June 2026"
  ]
 },
 {
  "qid": "q524adbcfc6",
  "kind": "yes/no",
  "text": "Flatmates' thread\nExport of the guest review drive, passed on by Greta.\n\nMembers: Lena, Zara, Greta, Elif\nChat log (oldest first):\n[5 May 2026] Greta: @Lena I'll be sure to collect the bed linen by 10 May 2026.\n[6 May 2026] Elif: @Zara I'll be sure to change the lounge bulb by 8 May 2026.\n[8 May 2026] Elif: @Lena As long as the check out clean is on, I'll wash the beach towels by 13 May 2026.\n[9 May 2026] Lena: @Greta Please don't feel you have to collect the bed linen\n[11 May 2026] Greta: On track for the check out clean to happen as planned.",
  "question": "Under the rules on the card, is it true that Greta has not kept the promise to collect the bed linen as of 10 May 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Greta (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q73de984409",
  "kind": "choice",
  "text": "Subject: Chat about the guest list\nBelow is a copy that came from Yuki, pasted as found.\n\nMembers: Yuki, Dara, Oskar\nChat log (oldest first):\n[2 Apr 2026] Oskar: @Yuki I assure you I'll fetch the spare memory cards by 5 Apr 2026 if the engagement shoot is on.\n[4 Apr 2026] Yuki: @Dara As long as the bridal shower is on, I'll pick up the album prints by 9 Apr 2026.\n[6 Apr 2026] Oskar: Fab, we are on for the bridal shower as planned!\n[7 Apr 2026] Yuki: @Oskar I promise to book the assistant photographer by 15 Apr 2026.\n[14 Apr 2026] Yuki: @Oskar Can I book the assistant photographer by 17 Apr 2026 instead? I did promise, sorry.\n[15 Apr 2026] Oskar: @Yuki Nah, that deadline counts, mate, so please book the assistant photographer!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Yuki (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Yuki's pledge to pick up the album prints sit at the end of 13 Apr 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not yet due",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q22e6b367e2",
  "kind": "yes/no",
  "text": "Volunteers, here is the league run chat that Lena forwarded to us.\n\nMembers: Nadia, Lena, Bruno\nChat log (oldest first):\n[28 Jun 2026] Bruno: @Nadia Relax, I'll fetch the medical bag by July 6, 2026 for sure.\n[2 Jul 2026] Bruno: @Nadia I promise to collect the referee whistles by July 8, 2026 if the cup tie is on.\n[4 Jul 2026] Bruno: @Lena Lovely, I'll set up the corner flags by July 10, 2026 for sure.\n[6 Jul 2026] Nadia: Brilliant news everyone, the cup tie is a go!\n[8 Jul 2026] Bruno: @Nadia Got myself to collect the referee whistles lol.",
  "question": "Does the card's rule set show that Bruno has not kept the promise to collect the referee whistles at the end of July 7, 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q06d1e14cac",
  "kind": "choice",
  "text": "Thread filed under support\nAbout the staff handbook, saved by Dara.\n\nMembers: Arlo, Zara, Dara, Kai\nChat log (oldest first):\n[16 Aug 2026] Kai: @Zara You can bank on me to send the expense receipts by 20 Aug 2026.\n[18 Aug 2026] Kai: @Zara I regret to say that I shall not send the expense receipts.\n[20 Aug 2026] Dara: @Zara I will collect the visitor badges by 25 Aug 2026 only if the staff picnic happens.\n[24 Aug 2026] Kai: On track for the staff picnic to happen as planned.\n[24 Aug 2026] Dara: @Zara Quick question, could I collect the visitor badges by 27 Aug 2026 instead?\n[24 Aug 2026] Kai: @Dara Yes, you can collect the visitor badges by 27 Aug 2026 instead.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Dara's promise to collect the visitor badges at the end of 24 Aug 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Broken",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q72e361243f",
  "kind": "choice",
  "text": "Shared by Lena, this is where the street watch scheme gets planned.\n\nMembers: Sami, Malik, Lena, Femi\nChat log (oldest first):\n[17 Mar 2026] Femi: @Lena You can bet I'll feed the cat across the road by 20 March 2026.\n[17 Mar 2026] Sami: @Lena Count on me to share the garden hose by 23 March 2026.\n[20 Mar 2026] Malik: @Femi No need to feed the cat across the road, I'm letting you off\n[21 Mar 2026] Femi: @Sami I will walk the old spaniel by 28 March 2026 only if the road works meeting happens.\n[23 Mar 2026] Malik: @Sami Please don't feel you have to share the garden hose\n[26 Mar 2026] Femi: Please note the road works meeting will proceed.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lena (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nQuick question, at the end of 26 March 2026, what status has Sami's promise to share the garden hose got?",
  "options": [
   "Not triggered",
   "Waived",
   "Not yet due",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "q7124ecda2b",
  "kind": "choice",
  "text": "Shared by Malik, this record holds tenant and landlord messages on the autumn term budget.\n\nMembers: Ivo, Malik, Mo\nChat log (oldest first):\n[26 Apr 2026] Malik: @Ivo I will scan the council tax letter by 29 Apr 2026 only if the house hunting viewing happens.\n[26 Apr 2026] Mo: @Malik I will print the tenancy agreement by 4 May 2026 only if the check in visit happens.\n[28 Apr 2026] Malik: Lovely, the house hunting viewing is definitely happening!\n[28 Apr 2026] Malik: @Ivo Might I ask whether I could scan the council tax letter by 2 May 2026 instead?\n[28 Apr 2026] Malik: @Ivo I own this, I'll collect the parcel from porch by 3 May 2026.\n[30 Apr 2026] Ivo: @Malik Ticket's mine, I'll store the spare bike by 3 May 2026.\n[3 May 2026] Malik: @Ivo To my relief, I managed to scan the council tax letter.\n[3 May 2026] Malik: @Ivo Apologies, I'll not be able to collect the parcel from porch",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of 1 May 2026, what is the date by which Malik has to scan the council tax letter, counting any agreed change?",
  "options": [
   "4 May 2026",
   "2 May 2026",
   "29 Apr 2026"
  ]
 },
 {
  "qid": "q6ea2445f38",
  "kind": "choice",
  "text": "Shared by Tomas, this back and forth with the client covers the campaign edit.\n\nMembers: Ana, Tomas, Leila\nChat export (date | from | to | message):\n2026-08-12 | Leila | Tomas | I'll be sure to label the clip folders by August 16, 2026.\n2026-08-15 | Ana | Tomas | If the client screening goes ahead, I'll gladly export the subtitle files by August 20, 2026.\n2026-08-16 | Leila | Tomas | Any chance I can label the clip folders by August 18, 2026 instead?\n2026-08-16 | Ana | Leila | Yes, happy for you to label the clip folders by August 18, 2026 instead.\n2026-08-18 | Leila | Tomas | I promise to send the timeline export by August 22, 2026 if the agency review call is on.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Leila's promise to label the clip folders at the end of August 18, 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Kept",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "q226cf8abc5",
  "kind": "yes/no",
  "text": "Messages with the letting agent about the flatmate contract terms, forwarded by Zara for the rental file.\n\nMembers: Zara, Omar, Lena\nChat log (oldest first):\n[15 Oct 2026] Omar: @Lena Count on me to photograph the bathroom mould by 21 Oct 2026.\n[18 Oct 2026] Omar: @Lena Any chance I can photograph the bathroom mould by 24 Oct 2026 instead?\n[18 Oct 2026] Lena: @Omar Nah, the date's staying put, so you can photograph the bathroom mould.\n[19 Oct 2026] Zara: @Omar Only if the house hunting viewing is on, I will scan the council tax letter by 25 Oct 2026.\n[21 Oct 2026] Zara: @Omar You are released, no requirement to photograph the bathroom mould.\n[24 Oct 2026] Omar: Brilliant news everyone, the house hunting viewing is a go!",
  "question": "Would you call Omar's promise to photograph the bathroom mould broken, waived, not triggered or not yet due, instead of kept, at the end of 22 Oct 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Zara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd89b25c870",
  "kind": "choice",
  "text": "Saved by Ivo, this is the household group chat about the family photo book, copied in full.\n\nMembers: Ivo, Malik, Oskar, Kofi\nChat log (oldest first):\n[20 Feb 2026] Oskar: Wish me luck, hoping to walk the dog by February 27, 2026.\n[21 Feb 2026] Oskar: @Malik If the puppet show is on, I'll definitely walk the dog by February 26, 2026.\n[23 Feb 2026] Kofi: Scrapping the puppet show, apologies to all.\n[27 Feb 2026] Ivo: @Malik Count on me to bake the oat biscuits by March 7, 2026.\n[27 Feb 2026] Ivo: @Oskar I own this, I'll fetch the craft box by March 8, 2026.\n[7 Mar 2026] Ivo: @Oskar Guess what, I managed to fetch the craft box!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Oskar's promise to walk the dog receive at the end of February 26, 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Kept",
   "Broken",
   "Not yet due"
  ]
 },
 {
  "qid": "q94afb10e01",
  "kind": "yes/no",
  "text": "Yuki shared this family chat about the holiday memories for the relatives.\n\nMembers: Yuki, Malik, Arlo, Sami\nChat log (oldest first):\n[19 Feb 2026] Yuki: @Malik If the sleepover weekend is on, I'll definitely mend the kite string by 25 Feb 2026.\n[23 Feb 2026] Malik: @Yuki I'll be sure to teach the card game by 2 Mar 2026.\n[25 Feb 2026] Yuki: @Sami Count on me to pack the picnic basket by 6 Mar 2026 if the school play is on.\n[28 Feb 2026] Yuki: Really pleased to say the school play will go ahead!\n[28 Feb 2026] Sami: @Malik Quick update: you do not need to teach the card game at all.\n[2 Mar 2026] Malik: @Yuki Mum, I did teach the card game, haha.",
  "question": "Does the card's rule set confirm that Malik has kept the promise to teach the card game on 8 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qefa224e030",
  "kind": "choice",
  "text": "Arlo shared this channel export covering the lab move for the team.\n\nMembers: Malik, Hana, Arlo\nChat export (date | from | to | message):\n2026-08-29 | Malik | Hana | I promise to return the library books by 1 Sep 2026 if the seminar series is on.\n2026-08-29 | Arlo | group | Really pleased to say the seminar series will go ahead!\n2026-08-29 | Malik | Hana | Quick report: I've managed to return the library books\n2026-09-01 | Hana | Malik | I'll scan the field notes by 9 Sep 2026, provided the thesis defence happens.\n2026-09-02 | Arlo | Hana | You can bank on me to submit the ethics application by 5 Sep 2026.\n2026-09-04 | Arlo | Hana | Mum, I did submit the ethics application, haha.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Malik (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Malik's commitment to return the library books is in what status at the end of 29 Aug 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Kept",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "qa048632420",
  "kind": "choice",
  "text": "Help desk export\nAbout: the family day out\nCopied by: Yuki\n\nMembers: Yuki, Ana, Jonas\nChat log (oldest first):\n[28 Jul 2026] Jonas: @Yuki You can bank on me to sort the old photo albums by 5 August 2026.\n[28 Jul 2026] Yuki: Ah right, thanks for that.\n[30 Jul 2026] Ana: @Jonas As long as the puppet show is on, I'll tidy the playroom by 3 August 2026.\n[31 Jul 2026] Ana: Sad to report that the puppet show is off.\n[31 Jul 2026] Jonas: @Yuki It's on me to walk the dog by 6 August 2026.\n[4 Aug 2026] Yuki: @Jonas Forget it, you won't need to sort the old photo albums",
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
  "qid": "qc2ced2594a",
  "kind": "yes/no",
  "text": "Support: help desk chat\nSubject: the new kit design\nSaved by: Femi\n\nMembers: Elif, Greta, Femi\nChat log (oldest first):\n[24 Jan 2026] Femi: @Greta Lovely, I'll set up the feed stop by 31 Jan 2026 for sure.\n[26 Jan 2026] Elif: @Greta Count on me to service the tandem bike by 28 Jan 2026, if the mechanics clinic happens.\n[27 Jan 2026] Femi: @Elif I will return the loaned helmets by 3 Feb 2026.\n[27 Jan 2026] Elif: Team, the mechanics clinic stays on as booked.\n[2 Feb 2026] Femi: @Elif Change of plans: I will not return the loaned helmets",
  "question": "Under the rules on the card, is the promise Femi made to return the loaned helmets in a status other than broken at the end of 4 Feb 2026?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q359768c063",
  "kind": "choice",
  "text": "{\"thread\": \"the volunteer roster\", \"exported_by\": \"Leila\", \"shape\": \"group chat\"}\n\nMembers: Leila, Lee, Priya\nChat export (date | from | to | message):\n2026-01-18 | Leila | Priya | Promise to label the raffle prizes by 26 Jan 2026 if the reading festival goes ahead.\n2026-01-24 | Lee | group | On track for the reading festival to happen as planned.\n2026-01-25 | Leila | Priya | Think 31 Jan 2026 would work if I label the raffle prizes instead?\n2026-01-25 | Priya | Leila | Works for me, fine for you to label the raffle prizes by 31 Jan 2026.\n2026-01-28 | Leila | Priya | Ta-da, I went and did it: label the raffle prizes!\n2026-01-30 | Leila | Lee | Guaranteed I'll book the school hall by 4 Feb 2026.\n2026-01-31 | Priya | Leila | Absolutely, I will collect the bake sale tins by 4 Feb 2026.\n2026-01-31 | Leila | Lee | Apologies, I'll not be able to book the school hall",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Leila to label the raffle prizes at the end of 3 Feb 2026, counting any agreed change of date?",
  "options": [
   "4 Feb 2026",
   "31 Jan 2026",
   "26 Jan 2026"
  ]
 },
 {
  "qid": "q7363c1ee41",
  "kind": "yes/no",
  "text": "Saved by Sami: a freelancer's exchange with a client over the payment setup.\n\nMembers: Kofi, Leila, Sami\nChat log (oldest first):\n[20 Oct 2026] Leila: I'm aiming to print the packing slips by 26 October 2026, might manage it.\n[20 Oct 2026] Leila: @Kofi Only if the market day is on, I will restore the old theme by 26 October 2026.\n[21 Oct 2026] Leila: @Kofi Got it, I'll print the packing slips by 24 October 2026 for sure.\n[22 Oct 2026] Leila: @Kofi Scratch that, I'm not going to print the packing slips\n[22 Oct 2026] Kofi: @Leila Ah, no stress, no need for you to print the packing slips\n[22 Oct 2026] Leila: Yay, the market day is all set to go!",
  "question": "At the end of 22 October 2026, has the promise Leila made to print the packing slips been broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc08a90b7b5",
  "kind": "yes/no",
  "text": "Subject: Saved thread about the kit sponsorship\nThis export from Ivo is pasted in full for readers who want it.\n\nMembers: Ivo, Tomas\nChat export (date | from | to | message):\n2026-01-17 | Ivo | Tomas | Ticket's mine, I'll wash the away kit by 23 January 2026.\n2026-01-20 | Tomas | Ivo | I promise to print the team sheets by 28 January 2026.\n2026-01-20 | Ivo | group | Appreciate you telling me.\n2026-01-23 | Ivo | Tomas | Count on me to book the changing room by 27 January 2026 if the youth trial is on.\n2026-01-23 | Ivo | group | Sad to report that the youth trial is off.\n2026-01-28 | Tomas | Ivo | Guess what, I managed to print the team sheets!",
  "question": "Is Tomas's promise to print the team sheets kept at the end of 30 January 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q35ba8a6048",
  "kind": "choice",
  "text": "Shared by Tess, this freelance thread with a client is about the guest list.\n\nMembers: Hana, Omar, Ana, Tess\nChat log (oldest first):\n[23 Sep 2026] Hana: @Omar I'll be sure to collect the venue floor plan by 30 September 2026.\n[25 Sep 2026] Ana: @Hana I'll send the sneak peek gallery by 2 October 2026 as long as the cake tasting is on.\n[27 Sep 2026] Ana: @Omar Lovely, I'll return the lighting stands by 2 October 2026 for sure.\n[28 Sep 2026] Hana: Fab, we are on for the cake tasting as planned!\n[30 Sep 2026] Hana: @Omar Guess what, I managed to collect the venue floor plan!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAt the end of 30 September 2026, which status does Hana have for the promise to collect the venue floor plan?",
  "options": [
   "Waived",
   "Not yet due",
   "Not triggered",
   "Broken",
   "Kept"
  ]
 },
 {
  "qid": "qb7866d6375",
  "kind": "choice",
  "text": "Committee chat on the ground upgrade, shared by Oskar with the volunteers.\n\nMembers: Ana, Hana, Priya, Oskar\nChat log (oldest first):\n[31 May 2026] Hana: @Oskar Will attempt to repair the goal nets by 7 June 2026, can't promise.\n[2 Jun 2026] Hana: @Ana You can bank on me to repair the goal nets by 10 June 2026.\n[6 Jun 2026] Hana: @Ana I committed to repair the goal nets, can I do that by 13 June 2026 instead?\n[9 Jun 2026] Priya: @Hana Yes, you have the green light to repair the goal nets by 13 June 2026.\n[9 Jun 2026] Oskar: @Ana Count on me to return the bib sets by 12 June 2026.\n[10 Jun 2026] Hana: @Priya I'll fetch the medical bag by 12 June 2026, provided the cup tie happens.\n[10 Jun 2026] Hana: Yay, the cup tie is all set to go!\n[12 Jun 2026] Hana: @Ana Sorry, I won't repair the goal nets after all",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat's the day Hana needs to repair the goal nets by at the end of 9 June 2026, after any new date the group agreed on?",
  "options": [
   "13 June 2026",
   "12 June 2026",
   "10 June 2026"
  ]
 },
 {
  "qid": "q2b66541b42",
  "kind": "yes/no",
  "text": "Subject: Chat about the peer review\nA plain copy from Tess follows, exactly as exported.\n\nMembers: Oskar, Ivo, Tess\nChat log (oldest first):\n[1 Apr 2026] Tess: @Oskar I'll be sure to book the microscope slot by 4 April 2026.\n[1 Apr 2026] Ivo: @Tess Please don't feel you have to book the microscope slot\n[6 Apr 2026] Oskar: @Ivo I will clean the glassware set by 13 April 2026 only if the safety inspection happens.\n[6 Apr 2026] Oskar: Brilliant news everyone, the safety inspection is a go!\n[12 Apr 2026] Tess: @Oskar Quick report: I've managed to book the microscope slot",
  "question": "Using the rules on the card, is it true that Tess has not broken the promise to book the microscope slot at the end of 9 April 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 }
]
