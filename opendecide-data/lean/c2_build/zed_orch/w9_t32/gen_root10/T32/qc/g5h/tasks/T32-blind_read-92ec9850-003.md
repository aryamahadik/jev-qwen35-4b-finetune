# G5-H blind read (all free-form rows) T32-blind_read-92ec9850-003 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root10/T32/qc/g5h/answers/T32-blind_read-92ec9850-003.json

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
  "qid": "q52f3484389",
  "kind": "choice",
  "text": "Dara shared this back and forth with the client about the menu redesign.\n\nMembers: Hana, Dara\nChat log (oldest first):\n[6 Oct 2026] Dara: @Hana I'll be sure to sketch the packaging mockup by 11 Oct 2026.\n[9 Oct 2026] Dara: @Hana I'll upload the sticker artwork by 13 Oct 2026 if the packaging launch goes ahead.\n[9 Oct 2026] Hana: Sorry all, the packaging launch is called off.\n[9 Oct 2026] Dara: @Hana Can I upload the sticker artwork by 19 Oct 2026 instead? I did promise, sorry.\n[9 Oct 2026] Dara: @Hana Count on me to update the icon set by 15 Oct 2026, if the gallery install happens.\n[12 Oct 2026] Hana: @Dara No new date, so please upload the sticker artwork by the date given.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Dara's promise to upload the sticker artwork have at the end of 13 Oct 2026?",
  "options": [
   "Waived",
   "Broken",
   "Not triggered",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q3dc64c275c",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the visitor policy\nThe chat below comes from Jonas, copied as is for reference.\n\nMembers: Tomas, Ines, Priya, Jonas\nChat log (oldest first):\n[17 Oct 2026] Priya: @Ines I assure you I'll replace the kitchen filters by 24 Oct 2026 if the annual audit is on.\n[17 Oct 2026] Tomas: @Priya Count on me to collect the visitor badges by 23 Oct 2026.\n[17 Oct 2026] Priya: Ah right, thanks for that.\n[19 Oct 2026] Priya: Team, the annual audit stays on as booked.\n[20 Oct 2026] Tomas: @Priya Can I collect the visitor badges by 25 Oct 2026 instead? I did promise, sorry.\n[20 Oct 2026] Priya: @Tomas No, I'd like you to collect the visitor badges by the original date.",
  "question": "On 23 Oct 2026 itself, has Tomas not kept the promise to collect the visitor badges?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Tomas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1256c0281d",
  "kind": "choice",
  "text": "Greta shared this back and forth with the client about the campaign edit.\n\nMembers: Greta, Ines, Leila, Ravi\nChat export (date | from | to | message):\n2026-06-15 | Greta | Ravi | Lovely, I'll upload the render files by Monday, 22 June 2026 for sure.\n2026-06-16 | Ravi | Ines | As long as the shoot day is on, I'll order the stock music licence by Thursday, 25 June 2026.\n2026-06-19 | Greta | Ravi | Might I ask whether I could upload the render files by Saturday, 27 June 2026 instead?\n2026-06-20 | Ravi | Greta | Works for me, fine for you to upload the render files by Saturday, 27 June 2026.\n2026-06-21 | Greta | Ravi | You can bet I'll record the voice over by Wednesday, 24 June 2026.\n2026-06-24 | Greta | group | Quick heads up, the shoot day is scrapped.\n2026-06-26 | Greta | Ravi | My sincere apologies, I am unable to upload the render files.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhich day is Greta supposed to upload the render files by, going by the chat at the end of Wednesday, 24 June 2026 and any agreed changes?",
  "options": [
   "Monday, 22 June 2026",
   "Thursday, 25 June 2026",
   "Saturday, 27 June 2026"
  ]
 },
 {
  "qid": "q7c6f5a1930",
  "kind": "choice",
  "text": "Here we plan the care plan together, and Ravi saved this for the family.\n\nMembers: Leila, Ivo, Ravi, Tomas\nChat log (oldest first):\n[11 Jul 2026] Ravi: @Tomas Fingers crossed I can drop off the hot meals by Tuesday, 21 July 2026.\n[12 Jul 2026] Ravi: @Leila Relax, I'll drop off the hot meals by Monday, 20 July 2026 for sure.\n[14 Jul 2026] Ravi: @Leila Think Sunday, 26 July 2026 would work if I drop off the hot meals instead?\n[19 Jul 2026] Tomas: @Ravi Yes, you can drop off the hot meals by Sunday, 26 July 2026 if that suits you.\n[25 Jul 2026] Leila: @Ravi Relax, I'll set up the medicine dispenser by Tuesday, 28 July 2026, promise.\n[27 Jul 2026] Tomas: @Ravi I assure you I'll return the hospital bed by Thursday, 30 July 2026 if the eye test is on.\n[29 Jul 2026] Ravi: Quick heads up, the eye test is scrapped.\n[30 Jul 2026] Ravi: @Leila Quick report: I've managed to drop off the hot meals",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo what's the latest day Ravi has to drop off the hot meals by at the end of Saturday, 25 July 2026, given any new date people agreed to?",
  "options": [
   "Tuesday, 28 July 2026",
   "Monday, 20 July 2026",
   "Sunday, 26 July 2026"
  ]
 },
 {
  "qid": "q3652741460",
  "kind": "choice",
  "text": "Here we plan the garden makeover together, and Rhea saved this for the family.\n\nMembers: Lee, Dara, Rhea\nChat export (date | from | to | message):\n2026-07-07 | Lee | Dara | You can bet I'll pick up the grout bag by 10 July 2026.\n2026-07-07 | Lee | Rhea | I own this, I'll pay the plumbing invoice by 15 July 2026.\n2026-07-09 | Lee | Dara | My sincere apologies, I am unable to pick up the grout bag.\n2026-07-11 | Dara | Lee | Good news, you're let off having to pay the plumbing invoice\n2026-07-12 | Rhea | Dara | If the removal van arrival goes ahead, I'll collect the sanding pads by 16 July 2026.\n2026-07-13 | Rhea | group | Team, the removal van arrival is not happening.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Rhea (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Rhea's undertaking to collect the sanding pads hold at the end of 16 July 2026?",
  "options": [
   "Broken",
   "Kept",
   "Waived",
   "Not yet due",
   "Not triggered"
  ]
 },
 {
  "qid": "q0571dc142c",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the family photo book\nThe thread below comes from Priya and is passed on as it is.\n\nMembers: Priya, Tess, Oskar\nChat log (oldest first):\n[5 Sep 2026] Priya: @Oskar Only if the seaside outing is on, I will read the bedtime story by 8 September 2026.\n[6 Sep 2026] Tess: @Oskar Not promising, but I'll try to pack the picnic basket by 13 September 2026.\n[8 Sep 2026] Tess: @Priya Guaranteed I'll pack the picnic basket by 15 September 2026.\n[10 Sep 2026] Priya: @Tess I promise to bake the oat biscuits by 14 September 2026 if the storytime session is on.\n[13 Sep 2026] Oskar: @Priya Committing to teach the card game by 17 September 2026.\n[15 Sep 2026] Tess: @Priya Guess who managed to pack the picnic basket, go team!",
  "question": "Is the promise Tess made to pack the picnic basket in a status other than broken at the end of 19 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qf99607053a",
  "kind": "choice",
  "text": "Team channel export, shared by Kofi, which is about the mobile release.\n\nMembers: Lena, Kofi, Mo\nChat log (oldest first):\n[28 May 2026] Lena: @Mo As long as the sprint demo is on, I'll review the pull request by 3 June 2026.\n[29 May 2026] Lena: @Kofi I'll rotate the test keys by 31 May 2026 as long as the planning session is on.\n[30 May 2026] Mo: @Kofi It's on me to deploy the staging build by 6 June 2026.\n[30 May 2026] Lena: Brilliant news everyone, the planning session is a go!\n[4 Jun 2026] Mo: @Kofi Forget what I said, I won't deploy the staging build\n[6 Jun 2026] Kofi: @Mo No worries, you don't need to deploy the staging build",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Mo's pledge to deploy the staging build sit at the end of 9 June 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Not yet due",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "q8f7d4e0833",
  "kind": "choice",
  "text": "Omar shared this support thread, which is about the caring rota.\n\nMembers: Ivo, Nadia, Mo, Omar\nChat log (oldest first):\n[19 May 2026] Omar: @Nadia As long as the home assessment is on, I will return the hospital bed by 2026-05-22.\n[19 May 2026] Ivo: Sadly, the home assessment is not going ahead.\n[20 May 2026] Mo: @Nadia I own this, I'll pick up the repeat prescription by 2026-05-27.\n[21 May 2026] Omar: @Nadia Mate, I promised, may I return the hospital bed by 2026-05-25 instead?\n[22 May 2026] Nadia: @Omar No, I'd like you to return the hospital bed by the original date.\n[23 May 2026] Omar: @Nadia Absolutely, I will collect the post by 2026-05-28.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Omar gave to return the hospital bed have at the end of 2026-05-22?",
  "options": [
   "Kept",
   "Not yet due",
   "Waived",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q2f781c5a41",
  "kind": "yes/no",
  "text": "Jonas shared this so the junior section is easy to follow for the volunteers.\n\nMembers: Dara, Nadia, Jonas, Sami\nChat log (oldest first):\n[19 Jan 2026] Jonas: @Nadia Relax, I'll set up the corner flags by 22 January 2026 for sure.\n[19 Jan 2026] Nadia: @Sami Count on me, I'll wash the away kit by 21 January 2026.\n[22 Jan 2026] Nadia: @Sami If the cup tie goes ahead, I'll repair the goal nets by 28 January 2026.\n[23 Jan 2026] Jonas: @Nadia Guess who managed to set up the corner flags, go team!\n[24 Jan 2026] Nadia: Update: the cup tie is going ahead as planned.",
  "question": "On the card, was Jonas's promise to set up the corner flags kept, rather than broken, waived, not triggered or not yet due, at the end of 26 January 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q60fac1ed63",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the junior section\nThe thread below comes from Lee and is passed on as it is.\n\nMembers: Lee, Mo\nChat log (oldest first):\n[28 May 2026] Lee: @Mo If the presentation evening goes ahead, I'll mark the pitch lines by 31 May 2026.\n[28 May 2026] Lee: Scrapping the presentation evening, apologies to all.\n[28 May 2026] Mo: @Lee Ticket's mine, I'll fetch the medical bag by 4 June 2026.\n[29 May 2026] Lee: @Mo If the cup tie goes ahead, I'll gladly wash the away kit by 5 June 2026.\n[2 Jun 2026] Mo: @Lee Mind giving me until 7 June 2026 to fetch the medical bag?\n[3 Jun 2026] Mo: @Lee Change of plans: I will not fetch the medical bag",
  "question": "Does the chat, checked at the end of 7 June 2026, show that Mo has broken the promise to fetch the medical bag?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qbec59db48a",
  "kind": "yes/no",
  "text": "We are getting ready for the caring rota, and Lena shared this chat with us.\n\nMembers: Femi, Wren, Sami, Lena\nChat log (oldest first):\n[26 Feb 2026] Sami: @Wren Count on me to pick up the repeat prescription by 3 Mar 2026 if the carer handover is on.\n[28 Feb 2026] Wren: @Lena See if I can return the hospital bed by 8 Mar 2026.\n[1 Mar 2026] Wren: @Femi I will return the hospital bed by 7 Mar 2026.\n[2 Mar 2026] Wren: Brilliant news everyone, the carer handover is a go!\n[5 Mar 2026] Sami: @Femi I will fetch the mobility aids by 12 Mar 2026.\n[8 Mar 2026] Wren: @Femi Quick report: I've managed to return the hospital bed",
  "question": "Per the rules on the card, does the promise Wren made to return the hospital bed count as not broken at the end of 9 Mar 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qde943b0074",
  "kind": "choice",
  "text": "Arlo forwarded this exchange with the landlord on the balcony garden project.\n\nMembers: Nadia, Arlo\nChat log (oldest first):\n[21 Aug 2026] Nadia: @Arlo It's on me to measure the kitchen for fridge by Saturday, August 29, 2026.\n[23 Aug 2026] Arlo: @Nadia You can bet I'll read the meter readings by Saturday, August 29, 2026.\n[23 Aug 2026] Arlo: @Nadia If the lease renewal call goes ahead, I'll collect the spare flat keys by Friday, August 28, 2026.\n[23 Aug 2026] Nadia: Thanks lovely, got it!\n[26 Aug 2026] Arlo: On track for the lease renewal call to happen as planned.\n[27 Aug 2026] Nadia: @Arlo Guaranteed I'll remove the bathroom shelf by Thursday, September 3, 2026.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nMind telling me the status of Arlo's promise to collect the spare flat keys at the end of Friday, August 28, 2026?",
  "options": [
   "Not yet due",
   "Not triggered",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "qf8750eb4ca",
  "kind": "choice",
  "text": "Lena shared this to pin down the kitchen garden project, housemates.\n\nMembers: Femi, Elif, Lena\nChat log (oldest first):\n[29 Jan 2026] Lena: @Femi I promise to sharpen the hand hoe by Saturday, January 31, 2026 if the village flower show is on.\n[31 Jan 2026] Elif: @Lena It's on me to dig the potato patch by Sunday, February 8, 2026.\n[31 Jan 2026] Lena: @Elif Nobody needs you to dig the potato patch, that's that\n[1 Feb 2026] Elif: @Lena Ta-da, I went and did it: dig the potato patch!\n[2 Feb 2026] Femi: @Lena I will build the compost bay by Wednesday, February 4, 2026 only if the allotment site visit happens.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status does the chat show for the promise Elif made to dig the potato patch at the end of Saturday, February 7, 2026?",
  "options": [
   "Not yet due",
   "Waived",
   "Kept",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q9a1fb012f8",
  "kind": "choice",
  "text": "Shared by Leila for the committee, this is the group chat on the training plan.\n\nMembers: Leila, Ana, Malik\nChat log (oldest first):\n[17 Aug 2026] Malik: @Leila Lovely, I'll pump the spare tyres by 20 Aug 2026 for sure.\n[21 Aug 2026] Leila: @Ana Promise to service the tandem bike by 24 Aug 2026 if the bike check goes ahead.\n[23 Aug 2026] Leila: Yep, the bike check is on as planned.\n[24 Aug 2026] Leila: @Ana Committing to fetch the bike stand by 1 Sep 2026.\n[24 Aug 2026] Leila: @Ana Guess who managed to service the tandem bike, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Leila's promise to service the tandem bike at the end of 24 Aug 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q015c23d65b",
  "kind": "yes/no",
  "text": "Team channel export, shared by Malik, which is about the trade show push.\n\nMembers: Omar, Tess, Malik, Femi\nChat export (date | from | to | message):\n2026-08-14 | Femi | Malik | Fingers crossed I can collect the survey answers by 19 Aug 2026.\n2026-08-16 | Femi | Tess | I will make sure to collect the survey answers by 20 Aug 2026.\n2026-08-16 | Malik | Femi | Relax, mate, you're not expected to collect the survey answers\n2026-08-16 | Femi | Tess | Guess who managed to collect the survey answers, go team!\n2026-08-22 | Malik | Femi | If the product launch goes ahead, I'll pay the printing invoice by 30 Aug 2026.\n2026-08-26 | Malik | group | Fab, we are on for the product launch as planned!",
  "question": "According to the rules on the card, does the promise Femi made to collect the survey answers have any status except broken at the end of 16 Aug 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qfd78915844",
  "kind": "choice",
  "text": "Volunteers, this is the music library thread that Leila shared with the committee.\n\nMembers: Lena, Nadia, Leila\nChat log (oldest first):\n[27 Sep 2026] Leila: @Lena I'll print the song sheets by 4 Oct 2026 as long as the joint concert is on.\n[27 Sep 2026] Lena: @Leila Lovely, I'll fetch the choir robes by 4 Oct 2026 for sure.\n[29 Sep 2026] Nadia: @Lena As long as the summer recital is on, I'll return the library scores by 3 Oct 2026.\n[2 Oct 2026] Leila: Great news, the summer recital is on!\n[2 Oct 2026] Nadia: @Lena Might I ask whether I could return the library scores by 6 Oct 2026 instead?\n[2 Oct 2026] Lena: @Nadia Not moving it, return the library scores by the existing date.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nInsofar as the rules on the card apply, what status governs Nadia's promise to return the library scores at the end of 3 Oct 2026?",
  "options": [
   "Waived",
   "Broken",
   "Not triggered",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qe5e3b6f6b7",
  "kind": "choice",
  "text": "Ines saved these exchanges with the agent about the attic conversion idea.\n\nMembers: Ines, Omar, Rhea\nChat export (date | from | to | message):\n2026-02-01 | Ines | group | I'll try to replace the loo roll by 10 February 2026.\n2026-02-02 | Ines | Omar | Count on me to replace the loo roll by 7 February 2026 if the house insurance review is on.\n2026-02-02 | Ines | Omar | Relax, I'll stock the spice rack by 10 February 2026, promise.\n2026-02-03 | Ines | Rhea | I own this, I'll feed the house plants by 10 February 2026.\n2026-02-04 | Rhea | group | Sorry all, the house insurance review is not happening.\n2026-02-04 | Ines | Rhea | I'm withdrawing my promise to feed the house plants",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ines (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Ines's promise to replace the loo roll stand at the end of 7 February 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q348e8f194e",
  "kind": "choice",
  "text": "Subject: Saved thread about the showreel refresh\nThis export came from Kofi and is pasted in full below.\n\nMembers: Kofi, Ivo, Lena\nChat log (oldest first):\n[5 Apr 2026] Ivo: @Kofi I'll export the subtitle files by 10 April 2026 as long as the voiceover session is on.\n[6 Apr 2026] Ivo: Brilliant news everyone, the voiceover session is a go!\n[8 Apr 2026] Ivo: @Kofi Gutted to say I won't export the subtitle files, sorry team\n[10 Apr 2026] Lena: @Kofi I'll be sure to label the clip folders by 18 April 2026.\n[10 Apr 2026] Lena: @Kofi Change of plans: I will not label the clip folders",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIn plain terms, how did Ivo's promise to export the subtitle files turn out at the end of 13 April 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Waived",
   "Not yet due",
   "Broken"
  ]
 },
 {
  "qid": "qd92649aa9f",
  "kind": "yes/no",
  "text": "Subject: Forwarded chat on the rebrand package\nThe chat below comes from Mo, copied as is for reference.\n\nMembers: Mo, Leila, Ana\nChat log (oldest first):\n[13 Jul 2026] Mo: @Leila It's on me to export the logo files by Saturday, July 18, 2026.\n[15 Jul 2026] Ana: @Leila I'll fetch the brand fonts by Thursday, July 23, 2026, provided the gallery install happens.\n[16 Jul 2026] Leila: @Mo Count on me to pick the colour swatches by Friday, July 24, 2026.\n[17 Jul 2026] Leila: @Mo Quick report: I've managed to pick the colour swatches\n[17 Jul 2026] Mo: Fab, we are on for the gallery install as planned!\n[26 Jul 2026] Ana: @Leila Ta-da, I went and did it: fetch the brand fonts!",
  "question": "On Friday, July 24, 2026 itself, has Ana not kept the promise to fetch the brand fonts?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Mo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q322d6afbca",
  "kind": "yes/no",
  "text": "Team channel export, shared by Malik, which is about the trade show push.\n\nMembers: Omar, Tess, Malik, Femi\nChat export (date | from | to | message):\n2026-08-14 | Femi | Malik | Fingers crossed I can collect the survey answers by 19 Aug 2026.\n2026-08-16 | Femi | Tess | I will make sure to collect the survey answers by 20 Aug 2026.\n2026-08-16 | Malik | Femi | Relax, mate, you're not expected to collect the survey answers\n2026-08-16 | Femi | Tess | Guess who managed to collect the survey answers, go team!\n2026-08-22 | Malik | Femi | If the product launch goes ahead, I'll pay the printing invoice by 30 Aug 2026.\n2026-08-26 | Malik | group | Fab, we are on for the product launch as planned!",
  "question": "When you check the chat at the end of 16 Aug 2026, is the promise Femi made to collect the survey answers broken?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q2db39bed5d",
  "kind": "yes/no",
  "text": "Yo flatmates, Kofi shared this chat about the house refit, so chip in.\n\nMembers: Ana, Leila, Kofi\nChat log (oldest first):\n[17 Sep 2026] Ana: @Kofi Relax, I'll scrape the old wallpaper by 23 September 2026, promise.\n[18 Sep 2026] Ana: @Kofi Count on me, I'll pay the plumbing invoice by 27 September 2026.\n[19 Sep 2026] Leila: @Ana I'll fetch the paint samples by 26 September 2026, provided the boiler install visit happens.\n[21 Sep 2026] Ana: @Kofi Guess what, I managed to scrape the old wallpaper!\n[22 Sep 2026] Kofi: @Ana I assure you I'll return the tile cutter by 29 September 2026 if the mortgage valuation visit is on.\n[28 Sep 2026] Ana: Quick heads up, the mortgage valuation visit is scrapped.",
  "question": "Has Ana kept the promise to scrape the old wallpaper at the end of 26 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q4f9b36f5d8",
  "kind": "yes/no",
  "text": "Leila shared this channel export covering the visitor policy for the team.\n\nMembers: Ivo, Nadia, Omar, Leila\nChat log (oldest first):\n[9 Jul 2026] Nadia: @Ivo If the coffee morning goes ahead, I'll gladly book the boardroom by 11 July 2026.\n[10 Jul 2026] Nadia: Lovely, the coffee morning is definitely happening!\n[11 Jul 2026] Leila: @Nadia Guaranteed I'll send the expense receipts by 14 July 2026.\n[13 Jul 2026] Ivo: @Leila Good news, you're let off having to send the expense receipts\n[16 Jul 2026] Leila: @Nadia Mum, I did send the expense receipts, haha.\n[17 Jul 2026] Nadia: Checking you mean to send the expense receipts?",
  "question": "Going by the card's rules, does Leila not keep the promise to send the expense receipts at the end of 15 July 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Omar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qd8073b7810",
  "kind": "choice",
  "text": "Here is the summer getaway, posted by Zara for the family to read.\n\nMembers: Zara, Kofi, Ravi\nChat export (date | from | to | message):\n2026-04-27 | Kofi | Ravi | Will attempt to buy the packing cubes by May 5, 2026, can't promise.\n2026-04-28 | Kofi | Ravi | Got it, I'll buy the packing cubes by May 4, 2026 for sure.\n2026-05-01 | Kofi | Ravi | Quick question, could I buy the packing cubes by May 10, 2026 instead?\n2026-05-02 | Ravi | Kofi | Yes, lovely, you can buy the packing cubes by May 10, 2026 instead!\n2026-05-02 | Kofi | Zara | I'll collect the insurance papers by May 11, 2026, promise.\n2026-05-06 | Zara | Kofi | I'll book the airport parking by May 12, 2026 as long as the guided tour is on.\n2026-05-06 | Kofi | group | Sorry all, the guided tour is called off.\n2026-05-15 | Kofi | Ravi | For the record: I was able to buy the packing cubes",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, what is the deadline for Kofi to buy the packing cubes at the end of May 9, 2026, with any agreed change of date counted?",
  "options": [
   "May 10, 2026",
   "May 4, 2026",
   "May 11, 2026"
  ]
 },
 {
  "qid": "q87d7bc47b5",
  "kind": "yes/no",
  "text": "Jonas forwarded this exchange with the landlord on the student house hunt.\n\nMembers: Leila, Jonas, Dara\nChat log (oldest first):\n[31 Jan 2026] Leila: @Dara I'll try to print the tenancy agreement by 6 Feb 2026, can't promise!\n[2 Feb 2026] Leila: @Dara Got it, I'll print the tenancy agreement by 9 Feb 2026 for sure.\n[2 Feb 2026] Leila: @Dara Count on me to return the bin rota by 6 Feb 2026, if the move in day happens.\n[2 Feb 2026] Leila: @Jonas I promise to scan the council tax letter by 7 Feb 2026.\n[4 Feb 2026] Dara: Really pleased to say the move in day will go ahead!\n[9 Feb 2026] Leila: @Dara Ta-da, I went and did it: print the tenancy agreement!",
  "question": "Does Leila's promise to print the tenancy agreement hold up as kept at the end of 15 Feb 2026, rather than broken, waived, not triggered or not yet due?",
  "definitions": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qb69e855f5e",
  "kind": "choice",
  "text": "Yo flatmates, Mo shared this chat about the kitchen refit, so chip in.\n\nMembers: Kofi, Mo\nChat export (date | from | to | message):\n2026-06-13 | Kofi | Mo | Lovely, I'll ring the flat repair line by Tuesday, 16 June 2026 if the electrics safety check is on.\n2026-06-13 | Mo | group | Brilliant news everyone, the electrics safety check is a go!\n2026-06-14 | Kofi | Mo | I'll be sure to wipe the cooker hood by Wednesday, 17 June 2026.\n2026-06-15 | Mo | Kofi | Good news, you're let off having to wipe the cooker hood\n2026-06-16 | Mo | Kofi | Ah, no stress, no need for you to ring the flat repair line",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Kofi's promise to ring the flat repair line at the end of Sunday, 21 June 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered",
   "Broken"
  ]
 },
 {
  "qid": "q4626faa38f",
  "kind": "choice",
  "text": "Forwarded by Nadia, these tenant replies are about the guest welcome plan for the file.\n\nMembers: Ana, Kai, Nadia\nChat log (oldest first):\n[3 May 2026] Kai: @Nadia Count on me to wheel the bins out by 10 May 2026 if the guest arrival evening is on.\n[9 May 2026] Ana: @Kai If the summer season launch is on, I'll definitely scrub the hot tub by 14 May 2026.\n[10 May 2026] Nadia: Yep, the summer season launch is on as planned.\n[11 May 2026] Nadia: @Kai Ticket's mine, I'll fill the cleaning cupboard by 13 May 2026.\n[13 May 2026] Ana: @Nadia Forget it, you won't need to fill the cleaning cupboard\n[13 May 2026] Ana: @Kai Can I scrub the hot tub by 20 May 2026 instead? I did promise, sorry.\n[13 May 2026] Kai: @Ana Yes, happy for you to scrub the hot tub by 20 May 2026 instead.\n[14 May 2026] Nadia: @Ana Nobody needs you to scrub the hot tub, that's that",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kai (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Ana to scrub the hot tub at the end of 18 May 2026, counting any agreed change of date?",
  "options": [
   "10 May 2026",
   "14 May 2026",
   "20 May 2026"
  ]
 },
 {
  "qid": "q91488f20a5",
  "kind": "choice",
  "text": "Yuki shared this exchange with the client about the guest list.\n\nMembers: Oskar, Greta, Yuki\nChat export (date | from | to | message):\n2026-04-27 | Greta | Oskar | Absolutely, I will print the seating cards by 5 May 2026.\n2026-04-27 | Oskar | group | Got it, cheers!\n2026-04-27 | Greta | Oskar | If the venue visit goes ahead, I'll gladly send the sneak peek gallery by 29 April 2026.\n2026-04-29 | Greta | Oskar | As long as the cake tasting is on, I'll buy the candle props by 7 May 2026.\n2026-04-30 | Yuki | Greta | Relax, mate, you're not expected to print the seating cards\n2026-05-06 | Greta | Oskar | Got myself to print the seating cards lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Oskar (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat status does the chat show for the promise Greta made to print the seating cards at the end of 4 May 2026?",
  "options": [
   "Waived",
   "Broken",
   "Not triggered",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qa4cd93eccb",
  "kind": "yes/no",
  "text": "Sami forwarded this support chat, which is about the menu redesign.\n\nMembers: Ivo, Sami, Tomas\nChat log (oldest first):\n[13 Sep 2026] Ivo: @Sami Committing to mail the business cards by Wednesday, 16 September 2026.\n[15 Sep 2026] Tomas: @Ivo If the brand review call goes ahead, I'll gladly collect the photo credits by Friday, 25 September 2026.\n[16 Sep 2026] Tomas: @Ivo Got it, I'll export the logo files by Thursday, 24 September 2026 for sure.\n[16 Sep 2026] Tomas: Sadly, the brand review call is not going ahead.\n[18 Sep 2026] Sami: @Tomas Ah, no stress, no need for you to export the logo files",
  "question": "Is the promise Tomas made to export the logo files not kept by Friday, 18 September 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ivo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc2745023a3",
  "kind": "choice",
  "text": "Here is the reunion planning, posted by Greta for the family to read.\n\nMembers: Greta, Oskar\nChat log (oldest first):\n[25 Oct 2026] Oskar: @Greta I promise to order the cousin t-shirts by Monday, November 2, 2026 if the family quiz is on.\n[25 Oct 2026] Oskar: Team, the family quiz stays on as booked.\n[29 Oct 2026] Greta: @Oskar Committing to set up the slideshow laptop by Thursday, November 5, 2026.\n[29 Oct 2026] Greta: @Oskar I promise to reserve the reunion hall by Wednesday, November 4, 2026.\n[31 Oct 2026] Greta: @Oskar Would it be fine if I set up the slideshow laptop by Tuesday, November 10, 2026 instead, yeah?\n[2 Nov 2026] Greta: @Oskar Update on my side: I will not reserve the reunion hall, sorry.\n[5 Nov 2026] Greta: @Oskar Ta-da, I went and did it: set up the slideshow laptop!",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nIf the chat is checked at the end of Saturday, November 7, 2026, which date marks the deadline for Greta to set up the slideshow laptop, with agreed date changes included?",
  "options": [
   "Thursday, November 5, 2026",
   "Tuesday, November 10, 2026",
   "Wednesday, November 4, 2026"
  ]
 },
 {
  "qid": "qc00297c56f",
  "kind": "yes/no",
  "text": "Team channel export, shared by Kofi, which is about the visitor policy.\n\nMembers: Femi, Ines, Tess, Kofi\nChat log (oldest first):\n[9 Oct 2026] Kofi: @Femi Lovely, I'll book the boardroom by Thursday, 15 October 2026 if the lease viewing is on.\n[11 Oct 2026] Kofi: @Tess Count on me to return the printer toner by Monday, 19 October 2026.\n[15 Oct 2026] Kofi: @Tess I'll replace the kitchen filters by Thursday, 22 October 2026, providing the coffee morning goes ahead.\n[15 Oct 2026] Femi: @Kofi Don't sweat it, there's no need to return the printer toner\n[20 Oct 2026] Kofi: @Tess Ta-da, I went and did it: return the printer toner!",
  "question": "Is the promise to return the printer toner kept by Kofi as of Saturday, 24 October 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qc0d8dc915c",
  "kind": "choice",
  "text": "Shared by Yuki, this back and forth with the client covers the menu redesign.\n\nMembers: Yuki, Jonas\nChat log (oldest first):\n[5 Aug 2026] Yuki: @Jonas Count on me, I'll export the logo files by 13 Aug 2026.\n[5 Aug 2026] Jonas: @Yuki I own this, I'll update the icon set by 13 Aug 2026.\n[7 Aug 2026] Jonas: @Yuki Absolutely, I will mail the business cards by 10 Aug 2026.\n[7 Aug 2026] Yuki: @Jonas You are released, no requirement to mail the business cards.\n[11 Aug 2026] Yuki: @Jonas Count on me to check the poster proofs by 15 Aug 2026, if the shop fitting happens.\n[13 Aug 2026] Jonas: Yay, the shop fitting is all set to go!\n[15 Aug 2026] Yuki: @Jonas Is 20 Aug 2026 alright for me to check the poster proofs?\n[15 Aug 2026] Yuki: @Jonas Ticked off my list: check the poster proofs, yay.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Jonas (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nReading the chat as a full check at the end of 17 Aug 2026, by what date does Yuki have to check the poster proofs, counting any agreed change of date?",
  "options": [
   "15 Aug 2026",
   "20 Aug 2026",
   "10 Aug 2026"
  ]
 },
 {
  "qid": "q8e8573f5d1",
  "kind": "choice",
  "text": "We are getting ready for the garden shed build, and Arlo shared this chat with us.\n\nMembers: Kofi, Arlo, Omar, Elif\nChat log (oldest first):\n[22 Sep 2026] Kofi: @Elif It's on me to build the compost bay by 1 October 2026.\n[24 Sep 2026] Omar: @Arlo Count on me to weed the carrot row by 28 September 2026 if the water tank delivery is on.\n[24 Sep 2026] Arlo: Got it, thanks a lot.\n[24 Sep 2026] Kofi: Please note the water tank delivery will proceed.\n[26 Sep 2026] Kofi: @Omar Guaranteed I'll dig the potato patch by 4 October 2026.\n[28 Sep 2026] Kofi: @Elif Mum, I did build the compost bay, haha.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Arlo (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Omar doing with the promise to weed the carrot row at the end of 1 October 2026?",
  "options": [
   "Broken",
   "Kept",
   "Not triggered",
   "Waived",
   "Not yet due"
  ]
 },
 {
  "qid": "qf23434f15b",
  "kind": "choice",
  "text": "Kofi shared this support thread, which is about the showreel refresh.\n\nMembers: Dara, Kofi, Ivo, Priya\nChat export (date | from | to | message):\n2026-06-30 | Priya | Kofi | If the agency review call is on, I'll definitely ship the hard drive by 9 July 2026.\n2026-07-01 | Ivo | Kofi | Guaranteed I'll label the clip folders by 8 July 2026.\n2026-07-06 | Ivo | Kofi | Might I ask whether I could label the clip folders by 10 July 2026 instead?\n2026-07-06 | Dara | Ivo | Yes, you have the green light to label the clip folders by 10 July 2026.\n2026-07-06 | Priya | Ivo | No worries, you don't need to label the clip folders\n2026-07-07 | Dara | Ivo | Count on me to back up the project drives by 9 July 2026, if the grading session happens.\n2026-07-07 | Dara | Ivo | As long as the voiceover session is on, I'll send the colour notes by 9 July 2026.\n2026-07-16 | Ivo | Kofi | Log entry: label the clip folders, carried out",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat's the day Ivo needs to label the clip folders by at the end of 7 July 2026, after any new date the group agreed on?",
  "options": [
   "10 July 2026",
   "8 July 2026",
   "9 July 2026"
  ]
 },
 {
  "qid": "qcc376fc27a",
  "kind": "choice",
  "text": "Yuki exported this channel chat about the desk plan for the team.\n\nMembers: Yuki, Elif, Oskar, Hana\nChat log (oldest first):\n[10 May 2026] Oskar: @Elif Only if the coffee morning is on, I will book the boardroom by 18 May 2026.\n[13 May 2026] Hana: @Elif Lovely, I'll order the office stationery by 17 May 2026 for sure.\n[15 May 2026] Oskar: Team, the coffee morning stays on as booked.\n[15 May 2026] Elif: @Hana Got it, I'll replace the kitchen filters by 19 May 2026 for sure.\n[17 May 2026] Elif: @Hana Don't sweat it, there's no need to order the office stationery",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, which status applies to the promise Hana made to order the office stationery at the end of 22 May 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Waived",
   "Kept",
   "Broken"
  ]
 },
 {
  "qid": "q02201cb593",
  "kind": "yes/no",
  "text": "Subject: Saved chat on the office refit\nHere is the export from Omar, for the record.\n\nMembers: Omar, Rhea, Elif\nChat log (oldest first):\n[2 Feb 2026] Elif: Fingers crossed I can replace the kitchen filters by Monday, 9 February 2026.\n[3 Feb 2026] Elif: @Omar As long as the coffee morning is on, I will renew the fire extinguisher service by Thursday, 5 February 2026.\n[3 Feb 2026] Elif: @Omar Guaranteed I'll replace the kitchen filters by Friday, 6 February 2026.\n[4 Feb 2026] Omar: Really pleased to say the coffee morning will go ahead!\n[4 Feb 2026] Elif: @Omar Would it be fine if I replace the kitchen filters by Tuesday, 10 February 2026 instead, yeah?\n[5 Feb 2026] Elif: @Omar Guess who managed to replace the kitchen filters, go team!",
  "question": "Is it true under the card's rules that Elif has kept the promise to replace the kitchen filters at the end of Friday, 6 February 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q1b24ea1973",
  "kind": "yes/no",
  "text": "Shared by Femi, this is where the reunion weekend gets planned.\n\nMembers: Femi, Greta, Ana\nChat log (oldest first):\n[2 Mar 2026] Greta: @Femi Ticket's mine, I'll set up the slideshow laptop by 9 Mar 2026.\n[4 Mar 2026] Femi: @Ana Promise to order the cousin t-shirts by 13 Mar 2026 if the reunion lunch goes ahead.\n[6 Mar 2026] Greta: @Ana Count on me to reserve the reunion hall by 11 Mar 2026 if the family quiz is on.\n[7 Mar 2026] Ana: @Greta Committing to collect the old photo prints by 12 Mar 2026.\n[7 Mar 2026] Greta: Thanks, got it.\n[12 Mar 2026] Ana: @Greta Ticked off my list: collect the old photo prints, yay.",
  "question": "Is the promise to collect the old photo prints kept by Ana as of 14 Mar 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q47951e70dc",
  "kind": "choice",
  "text": "Omar shared this support thread, which is about the caring rota.\n\nMembers: Ivo, Nadia, Mo, Omar\nChat log (oldest first):\n[19 May 2026] Omar: @Nadia As long as the home assessment is on, I will return the hospital bed by 2026-05-22.\n[19 May 2026] Ivo: Brilliant news everyone, the home assessment is a go!\n[20 May 2026] Mo: @Nadia I own this, I'll pick up the repeat prescription by 2026-05-27.\n[21 May 2026] Omar: @Nadia Mate, I promised, may I return the hospital bed by 2026-05-25 instead?\n[22 May 2026] Nadia: @Omar No, I'd like you to return the hospital bed by the original date.\n[23 May 2026] Omar: @Nadia Absolutely, I will collect the post by 2026-05-28.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAccording to the card's rules, what status does the commitment Omar gave to return the hospital bed have at the end of 2026-05-22?",
  "options": [
   "Kept",
   "Not yet due",
   "Waived",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q061c63e14e",
  "kind": "choice",
  "text": "Shared by Lena from the work chat, with the lab move at its heart.\n\nMembers: Nadia, Lena, Omar\nChat log (oldest first):\n[12 Sep 2026] Omar: @Nadia I own this, I'll return the library books by September 14, 2026.\n[13 Sep 2026] Omar: @Nadia Provided the thesis defence happens, I'll submit the ethics application by September 21, 2026.\n[14 Sep 2026] Omar: @Nadia Ta-da, I went and did it: return the library books!\n[15 Sep 2026] Nadia: @Omar Got it, I'll fetch the grant forms by September 19, 2026 for sure.\n[16 Sep 2026] Omar: On track for the thesis defence to happen as planned.\n[17 Sep 2026] Nadia: @Omar I'm withdrawing my promise to fetch the grant forms",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nAs set out by the rules on the card, what status is attached to Omar's pledge to submit the ethics application at the end of September 22, 2026?",
  "options": [
   "Waived",
   "Not triggered",
   "Broken",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "q31019ab568",
  "kind": "choice",
  "text": "Hana saved this so we stay on the same page about the garden makeover, mates.\n\nMembers: Zara, Kofi, Hana\nChat export (date | from | to | message):\n2026-08-25 | Zara | Kofi | Count on me to collect the sanding pads by 28 August 2026 if the kitchen fitting day is on.\n2026-08-26 | Kofi | Zara | I assure you I'll sweep the dust from stairs by 30 August 2026 if the mortgage valuation visit is on.\n2026-08-26 | Zara | group | Sorry all, the mortgage valuation visit is called off.\n2026-08-26 | Kofi | Hana | You can bet I'll pick up the grout bag by 4 September 2026.\n2026-08-30 | Kofi | Hana | You can bet I'll print the floor plan by 2 September 2026.\n2026-09-02 | Hana | Kofi | Relax, mate, you're not expected to print the floor plan",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person in its to column; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Kofi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Kofi's promise to print the floor plan at the end of 3 September 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Kept",
   "Not yet due",
   "Waived"
  ]
 },
 {
  "qid": "q72ff978249",
  "kind": "choice",
  "text": "Tenant and agent back-and-forth on the attic conversion idea, saved by Leila.\n\nMembers: Elif, Leila, Tess\nChat export (date | from | to | message):\n2026-07-01 | Leila | Tess | I assure you I'll stock the spice rack by 7 Jul 2026 if the fuse box inspection is on.\n2026-07-01 | Leila | Tess | Ticket's mine, I'll wipe the shared kitchen counter by 4 Jul 2026.\n2026-07-01 | Tess | Leila | Nobody needs you to wipe the shared kitchen counter, that's that\n2026-07-02 | Tess | group | Team, the fuse box inspection is not happening.\n2026-07-02 | Elif | group | Quick check, any update on plans to wipe the shared kitchen counter?\n2026-07-05 | Tess | Leila | Relax, I'll replace the loo roll by 7 Jul 2026 for sure.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Leila made to wipe the shared kitchen counter is in which status at the end of 1 Jul 2026?",
  "options": [
   "Kept",
   "Broken",
   "Not yet due",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "qd984442f54",
  "kind": "choice",
  "text": "Attached chat: the home adaptations\nForwarded by: Yuki\n\nMembers: Oskar, Yuki, Wren, Lee\nChat log (oldest first):\n[11 Jan 2026] Lee: @Wren I promise to book the clinic transport by 19 January 2026 if the home assessment is on.\n[11 Jan 2026] Yuki: Really pleased to say the home assessment will go ahead!\n[11 Jan 2026] Lee: @Wren Would it be fine if I book the clinic transport by 22 January 2026 instead, yeah?\n[16 Jan 2026] Lee: @Yuki Count on me to return the hospital bed by 24 January 2026, if the hospital appointment happens.\n[18 Jan 2026] Wren: @Lee Of course, it is fine for you to book the clinic transport by 22 January 2026.\n[24 Jan 2026] Lee: @Wren Got myself to book the clinic transport lol.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Lee's promise to book the clinic transport at the end of 22 January 2026?",
  "options": [
   "Not yet due",
   "Kept",
   "Waived",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q00906f8d68",
  "kind": "choice",
  "text": "Tenant and agent back-and-forth on the attic conversion idea, saved by Leila.\n\nMembers: Elif, Leila, Tess\nChat export (date | from | to | message):\n2026-07-01 | Leila | Tess | I assure you I'll stock the spice rack by 7 Jul 2026 if the fuse box inspection is on.\n2026-07-01 | Leila | Tess | Ticket's mine, I'll wipe the shared kitchen counter by 4 Jul 2026.\n2026-07-01 | Elif | Leila | Nobody needs you to wipe the shared kitchen counter, that's that\n2026-07-02 | Tess | group | Team, the fuse box inspection is not happening.\n2026-07-02 | Elif | group | Quick check, any update on plans to wipe the shared kitchen counter?\n2026-07-05 | Tess | Leila | Relax, I'll replace the loo roll by 7 Jul 2026 for sure.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person in its to column; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Tess (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nChecking the group chat, the promise Leila made to wipe the shared kitchen counter is in which status at the end of 1 Jul 2026?",
  "options": [
   "Kept",
   "Broken",
   "Not yet due",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "qd4d7df20df",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the staff handbook\nFrom Femi, the thread below is shared as it stands.\n\nMembers: Ravi, Oskar, Femi\nChat log (oldest first):\n[26 Mar 2026] Ravi: @Oskar I'm aiming to order the office stationery by Tuesday, 31 March 2026, might manage it.\n[27 Mar 2026] Ravi: @Oskar I will order the office stationery by Friday, 3 April 2026 only if the building survey happens.\n[30 Mar 2026] Femi: @Ravi Count on me, I'll book the boardroom by Monday, 6 April 2026.\n[2 Apr 2026] Ravi: Sadly, the building survey is not going ahead.\n[3 Apr 2026] Ravi: @Oskar Quick question, could I order the office stationery by Tuesday, 7 April 2026 instead?\n[3 Apr 2026] Oskar: @Ravi No new date, so please order the office stationery by the date given.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ravi (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nHow is Ravi doing with the promise to order the office stationery at the end of Friday, 3 April 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "qccb4885e34",
  "kind": "choice",
  "text": "Volunteers, here is the training plan chat that Jonas forwarded to us.\n\nMembers: Dara, Greta, Jonas\nChat log (oldest first):\n[14 Jul 2026] Greta: @Dara Got it, I'll set up the feed stop by 21 July 2026 for sure.\n[14 Jul 2026] Dara: Ah right, thanks for that.\n[14 Jul 2026] Dara: @Greta You are released, no requirement to set up the feed stop.\n[15 Jul 2026] Greta: @Dara Log entry: set up the feed stop, carried out\n[17 Jul 2026] Jonas: @Greta Lovely, I'll service the tandem bike by 19 July 2026 if the hill climb is on.\n[18 Jul 2026] Greta: Yep, the hill climb is on as planned.",
  "question": "Count only lines on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes or let off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Greta's promise to set up the feed stop receive at the end of 16 July 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Kept",
   "Not yet due"
  ]
 },
 {
  "qid": "q4eb1d897e3",
  "kind": "choice",
  "text": "Here we plan the allotment expansion together, and Nadia saved this for the family.\n\nMembers: Femi, Priya, Bruno, Nadia\nChat log (oldest first):\n[11 May 2026] Femi: @Priya Absolutely, I will collect the seed potatoes by 18 May 2026.\n[12 May 2026] Nadia: @Femi As long as the seed swap day is on, I'll weed the carrot row by 17 May 2026.\n[16 May 2026] Nadia: Sorry all, the seed swap day is called off.\n[17 May 2026] Nadia: @Femi Mind giving me until 20 May 2026 to weed the carrot row?\n[17 May 2026] Bruno: @Nadia Yes, lovely, you can weed the carrot row by 20 May 2026 instead!\n\nNotice from the chat app: the copy Nadia shared is an older export, and newer messages are not included.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Nadia's promise to weed the carrot row stand at the end of 17 May 2026?",
  "options": [
   "Broken",
   "Not yet due",
   "Kept",
   "Waived",
   "Not triggered"
  ]
 },
 {
  "qid": "q26b71cafff",
  "kind": "yes/no",
  "text": "Messages with the letting agent about the summer lets season, forwarded by Nadia for the rental file.\n\nMembers: Mo, Nadia, Lena\nChat log (oldest first):\n[23 Sep 2026] Nadia: @Lena Promise to air the spare room by 27 Sep 2026 if the lettings photo shoot goes ahead.\n[23 Sep 2026] Mo: @Nadia Count on me, I'll wheel the bins out by 30 Sep 2026.\n[25 Sep 2026] Nadia: @Mo I promise to restock the guest toiletries by 1 Oct 2026 if the summer season launch is on.\n[28 Sep 2026] Lena: @Mo You can bet I'll vacuum the holiday cottage by 1 Oct 2026.\n[29 Sep 2026] Mo: @Nadia Ticked off: wheel the bins out, feels so good",
  "question": "Does the card classify Mo's promise to wheel the bins out as kept, instead of broken, waived, not triggered or not yet due, on 29 Sep 2026?",
  "definitions": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qce1bcbfef6",
  "kind": "choice",
  "text": "Forwarded by Nadia, these tenant replies are about the guest welcome plan for the file.\n\nMembers: Ana, Kai, Nadia\nChat log (oldest first):\n[3 May 2026] Kai: @Nadia Count on me to wheel the bins out by 10 May 2026 if the guest arrival evening is on.\n[9 May 2026] Ana: @Kai If the summer season launch is on, I'll definitely scrub the hot tub by 14 May 2026.\n[10 May 2026] Nadia: Yep, the summer season launch is on as planned.\n[11 May 2026] Nadia: @Kai Ticket's mine, I'll fill the cleaning cupboard by 13 May 2026.\n[13 May 2026] Ana: @Nadia Forget it, you won't need to fill the cleaning cupboard\n[13 May 2026] Ana: @Kai Can I scrub the hot tub by 20 May 2026 instead? I did promise, sorry.\n[13 May 2026] Nadia: @Ana Yes, happy for you to scrub the hot tub by 20 May 2026 instead.\n[14 May 2026] Nadia: @Ana Nobody needs you to scrub the hot tub, that's that",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Nadia (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nWhat is the deadline for Ana to scrub the hot tub at the end of 18 May 2026, counting any agreed change of date?",
  "options": [
   "20 May 2026",
   "10 May 2026",
   "14 May 2026"
  ]
 },
 {
  "qid": "qc3cc4cbf95",
  "kind": "yes/no",
  "text": "Here is the thread on the cottage refresh, posted by Dara for the house.\n\nMembers: Nadia, Ana, Dara\nChat log (oldest first):\n[27 Apr 2026] Ana: @Nadia Count on me, I'll vacuum the holiday cottage by May 4, 2026.\n[29 Apr 2026] Dara: @Nadia If the owner handover visit is on, I'll definitely scrub the hot tub by May 2, 2026.\n[29 Apr 2026] Nadia: Yep, the owner handover visit is on as planned.\n[1 May 2026] Nadia: @Ana No worries, you don't need to vacuum the holiday cottage\n[3 May 2026] Dara: @Nadia Guess what, I managed to scrub the hot tub!",
  "question": "Does the card's rule set show that Dara has not kept the promise to scrub the hot tub at the end of May 5, 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Dara (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "qfdd28eff45",
  "kind": "yes/no",
  "text": "We are getting ready for the caring rota, and Lena shared this chat with us.\n\nMembers: Femi, Wren, Sami, Lena\nChat log (oldest first):\n[26 Feb 2026] Sami: @Wren Count on me to pick up the repeat prescription by 3 Mar 2026 if the carer handover is on.\n[28 Feb 2026] Wren: @Lena See if I can return the hospital bed by 8 Mar 2026.\n[1 Mar 2026] Wren: @Femi I will return the hospital bed by 7 Mar 2026.\n[2 Mar 2026] Wren: Brilliant news everyone, the carer handover is a go!\n[5 Mar 2026] Sami: @Femi I will fetch the mobility aids by 12 Mar 2026.\n[8 Mar 2026] Wren: @Femi Quick report: I've managed to return the hospital bed",
  "question": "Applying the rules on the card, did Wren break the promise to return the hospital bed at the end of 9 Mar 2026?",
  "definitions": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists."
 },
 {
  "qid": "q42643cb0b2",
  "kind": "choice",
  "text": "Subject: Forwarded chat on the data cleanup\nFrom Rhea, the thread below is shared as it stands.\n\nMembers: Rhea, Oskar, Ana, Ravi\nChat log (oldest first):\n[10 Mar 2026] Ravi: @Oskar Provided the penetration test happens, I will restart the build server by March 13, 2026.\n[11 Mar 2026] Ana: Really pleased to say the penetration test will go ahead!\n[13 Mar 2026] Ana: @Oskar I will label the bug reports by March 17, 2026.\n[15 Mar 2026] Rhea: @Oskar Lovely, I'll merge the login branch by March 18, 2026 for sure.\n[16 Mar 2026] Ana: @Oskar To note: I have managed to label the bug reports\n[18 Mar 2026] Rhea: @Oskar Is it all right if I merge the login branch by March 23, 2026 instead?\n[18 Mar 2026] Ravi: @Rhea Yes, you're welcome to merge the login branch by March 23, 2026 instead.\n[24 Mar 2026] Rhea: @Oskar To my relief, I managed to merge the login branch.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Ana (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nOn a check of the chat at the end of March 26, 2026, what is the date by which Rhea has to merge the login branch, counting any agreed change?",
  "options": [
   "March 23, 2026",
   "March 18, 2026",
   "March 17, 2026"
  ]
 }
]
