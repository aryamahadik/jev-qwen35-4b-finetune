# G5-H blind read T25-blind_read-61aa53ae-000 (family T25)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T25/qc/g5h/answers/T25-blind_read-61aa53ae-000.json

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
  "qid": "q4e2499efdb",
  "kind": "choice",
  "text": "Help centre entry: Adaeze Nwosu has just joined and looked into the consultation fee at Hallam Chess Club to get up to speed. The material gathered is pasted in and set aside for the desk.\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-46 | board notice | pluto | 2 November 2025 | independent | 75.00 USD\nS-16 | station announcement | jupiter | 1 November 2025 | independent | 120.00 USD\nS-82 | bulletin | uranus | 26 October 2025 | independent | 75.00 USD\nS-19 | case file | uranus | 2 November 2025 | independent | 85.00 USD",
  "question": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value for the consultation fee do the listed sources settle on under the stated rules?",
  "options": [
   "Not determinable from reliable sources",
   "75.00 USD",
   "85.00 USD"
  ]
 },
 {
  "qid": "q022b799947",
  "kind": "yes/no",
  "text": "Help centre entry: Thandiwe Morrow is a parent who looked into the desk rental fee at Brightwater Physio Clinic in a bit of a rush. What came up is pasted below for the file.\n\nSources on the desk rental fee:\n- Source A: desk handout; tier opal; dated Tuesday, 12 May 2026; independent. It states the desk rental fee is 250.00 USD.\n- Source B: record card; tier topaz; dated Tuesday, 19 May 2026; independent. It states the desk rental fee is 150.00 USD.\n- Source C: social post; tier opal; dated Wednesday, 12 May 2027; copied from Source B. It states the desk rental fee is 150.00 USD.\n- Source D: inbox note; tier topaz; dated Wednesday, 19 May 2027; copied from Source B. It states the desk rental fee is 150.00 USD.\n\nClaim to check: the desk rental fee is 250.00 USD.",
  "question": "According to the rules given, does the claim to check give the same value for the desk rental fee as the listed sources settle?",
  "definitions": "How to settle the desk rental fee from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the desk rental fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q0348c4f7c1",
  "kind": "yes/no",
  "text": "Subject: Lookup on the season registration fee at Stanhope Sailing Club\nHello there,\nThis is Yasmin Khoury, a parent in a bit of a hurry. What was gathered is pasted below, so the lookup is well on its way.\nThanks,\n\nSource table for the season registration fee:\nsource | name | tier | dated | origin | stated value\nA | brochure | tigris | 21 August 2025 | independent | 100.00 USD\nB | poster | rhine | 11 June 2025 | independent | 30.00 USD\nC | system log | tigris | 22 August 2025 | independent | 60.00 USD\nD | instant message | tigris | 23 August 2025 | copied from B | 30.00 USD\nE | counter sign | rhine | 9 October 2025 | independent | 60.00 USD\n\nClaim to check: the season registration fee is 100.00 USD.",
  "question": "Going by the listed sources, does the claim to check not match the value the stated rules settle on?",
  "definitions": "How to settle the season registration fee from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the season registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q4b1634d583",
  "kind": "choice",
  "text": "Title: looking into the parking charge at Lowmoor Heath Gardens\nRequester: Amir Castellano\nTeam: student services\nPasted material is attached.\n\nSources on the parking charge:\n- Source S-43: bulletin; tier rhine; dated 5 February 2025; independent. It states the parking charge is 8.00 USD.\n- Source S-99: inbox note; tier rhine; dated 4 February 2025; independent. It states the parking charge is 8.00 USD.\n- Source S-17: brochure; tier rhine; dated 6 February 2025; independent. It states the parking charge is 15.00 USD.\n- Source S-94: system log; tier tigris; dated 4 February 2025; copied from Source S-99. It states the parking charge is 8.00 USD.",
  "question": "How to settle the parking charge from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the parking charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which value for the parking charge is settled from the listed sources?",
  "options": [
   "Not determinable from reliable sources",
   "8.00 USD",
   "15.00 USD"
  ]
 },
 {
  "qid": "qd67f7358b7",
  "kind": "yes/no",
  "text": "{\"requested_by\": \"Nikos Papadakis\", \"organisation\": \"Larchwood Park\", \"topic\": \"the desk rental fee\", \"note\": \"tidying records\"}\n\nSources on the desk rental fee:\n- Source A: spoken bulletin; tier garnet; dated 24 July 2025; independent. It states the desk rental fee is $350.00.\n- Source B: envelope insert; tier garnet; dated 31 July 2025; independent. It states the desk rental fee is $150.00.\n- Source C: receipt slip; tier garnet; dated 20 June 2025; independent. It states the desk rental fee is $350.00.\n- Source D: catalogue; tier garnet; dated 8 May 2025; independent. It states the desk rental fee is $250.00.\n\nClaim to check: the desk rental fee is $250.00.",
  "question": "Is the claim to check not correct for the desk rental fee under the stated rules?",
  "definitions": "How to settle the desk rental fee from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the desk rental fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q77455eee7d",
  "kind": "yes/no",
  "text": "Title: Booking query on the express surcharge at Larchwood Park\nRequester: Declan Murphy\nTeam: bookings\nThe pasted list below was gathered for this.\n\nSource table for the express surcharge:\nsource | name | tier | dated | origin | stated value\nA | news article | finch | Thursday, 6 February 2025 | independent | 10.00 USD\nB | door sign | finch | Saturday, 1 February 2025 | independent | 7.50 USD\nC | spoken bulletin | finch | Thursday, 6 February 2025 | independent | 10.00 USD\nD | handbook | finch | Thursday, 6 February 2025 | independent | 15.00 USD\nE | filing cabinet folder | finch | Friday, 7 February 2025 | independent | 3.00 USD\n\nClaim to check: the express surcharge is 10.00 USD.",
  "question": "Under the stated rules, does the claim to check give the same value for the express surcharge that the listed sources settle on?",
  "definitions": "How to settle the express surcharge from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the express surcharge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q65ab52d17f",
  "kind": "yes/no",
  "text": "Subject: Enquiry for the records team\nDear desk,\nCamila Restrepo is writing about the race entry fee at Larchwood Park. The material pasted below has been lined up for your reference.\nKind regards,\n\nSource table for the race entry fee:\nsource | name | tier | dated | origin | stated value\nS-74 | bulletin | autumn | Thursday, June 12, 2025 | independent | $40.00\nS-34 | board notice | winter | Wednesday, July 16, 2025 | independent | $50.00\nS-67 | photo caption | winter | Wednesday, June 11, 2025 | independent | $35.00\nS-56 | pricing page | winter | Wednesday, June 12, 2024 | independent | $50.00\nS-68 | envelope insert | autumn | Wednesday, June 11, 2025 | independent | $40.00\n\nClaim to check: the race entry fee is $50.00.",
  "question": "Applying the stated rules to these sources, does the claim to check state the same value the rules settle on?",
  "definitions": "How to settle the race entry fee from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the race entry fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qe846be6dc5",
  "kind": "yes/no",
  "text": "Subject: planning a visit\nGood day,\nArjun Sethi is planning a visit and wants to be clear on the term start date at Lindenfield Music Hall before arriving. The gathered material is pasted below for reference.\nYours sincerely,\n\nExcerpts on the term start date:\n[S-18] shop window card, tier lute, dated Saturday, 15 November 2025, copied from S-56: \"The term start date is Saturday, 13 March 2027.\"\n[S-41] info pack, tier lute, dated Friday, 14 November 2025, independent: \"The term start date is Saturday, 4 July 2026.\"\n[S-56] activity log, tier viola, dated Thursday, 13 November 2025, independent: \"The term start date is Saturday, 13 March 2027.\"\n[S-69] answerphone greeting, tier lute, dated Friday, 14 November 2025, independent: \"The term start date is Saturday, 4 July 2026.\"\n\nClaim to check: the term start date is Saturday, 13 March 2027.",
  "question": "Under the stated rules, does the claim to check agree with the value these sources settle for the term start date?",
  "definitions": "How to settle the term start date from the listed sources:\n- Tiers, most reliable first: harp; then lute; then viola.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the term start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qca1940bcda",
  "kind": "yes/no",
  "text": "Subject: Quick word on Larkfield Coach Tours\nHello there,\nFarhan Qureshi is a volunteer in a rush to get the race entry fee sorted. The pasted material below is ready to read, and thanks for taking a look.\nBest,\n\nSource table for the race entry fee:\nsource | name | tier | dated | origin | stated value\nS-18 | wall sign | autumn | 10 October 2025 | independent | $40.00\nS-84 | pamphlet | spring | 10 October 2026 | copied from S-89 | $30.00\nS-89 | ledger entry | winter | 10 October 2026 | independent | $30.00\nS-60 | email message | winter | 17 October 2025 | independent | $30.00\n\nClaim to check: the race entry fee is $40.00.",
  "question": "Is the claim to check not correct for the race entry fee under the stated rules?",
  "definitions": "How to settle the race entry fee from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the race entry fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q091d7203ff",
  "kind": "yes/no",
  "text": "This internal memo records that Lucia Carvalho, a support agent, is handling a request about the late return fee at Hawthorne Walk-In Clinic. The extract supplied for that request has been pasted in for reference. The matter is being dealt with in a formal and orderly manner. Please keep this with the usual support papers.\n\nSources on the late return fee:\n- Source S-81: news article; tier finch; dated 12 Jun 2026; independent. It states the late return fee is 12.00 USD.\n- Source S-49: tooltip; tier robin; dated 14 Jun 2026; copied from Source S-81. It states the late return fee is 12.00 USD.\n- Source S-34: system log; tier sparrow; dated 13 Jun 2026; independent. It states the late return fee is 25.00 USD.\n- Source S-32: filing cabinet folder; tier sparrow; dated 12 Jun 2026; independent. It states the late return fee is 12.00 USD.\n\nClaim to check: the late return fee is 12.00 USD.",
  "question": "Under the stated rules, is the value settled for the late return fee other than the value in the claim to check?",
  "definitions": "How to settle the late return fee from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the late return fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q101481f124",
  "kind": "choice",
  "text": "requested_by: Felix Okonjo\ntopic: desk rental fee\norganisation: Quarry Lane Debating Society\nchannel: booking desk\nasked_via: pasted material below\n\nSources on the desk rental fee:\n- Source A: meeting minutes; tier opal; dated 17 July 2025; independent. It states the desk rental fee is $350.00.\n- Source B: recorded message; tier topaz; dated 17 July 2024; independent. It states the desk rental fee is $250.00.\n- Source C: envelope insert; tier topaz; dated 18 July 2025; independent. It states the desk rental fee is $250.00.\n- Source D: cover note; tier opal; dated 17 July 2024; independent. It states the desk rental fee is $300.00.",
  "question": "How to settle the desk rental fee from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the desk rental fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, what value comes out as the settled answer for the fact?",
  "options": [
   "$250.00",
   "$300.00",
   "$350.00"
  ]
 },
 {
  "qid": "qf0c54dd9b8",
  "kind": "choice",
  "text": "Team memo:\nMatteo Bruno leads a team tidying records and has the league start date at Lantern Hill Rowing Club on the list. The pasted material below is pulled together for a quick read.\n\nExcerpts on the league start date:\n[A] information sheet, tier jupiter, dated Friday, 15 May 2026, copied from C: \"The league start date is Saturday, 31 January 2026.\"\n[B] brochure, tier jupiter, dated Friday, 15 May 2026, independent: \"The league start date is Thursday, 23 April 2026.\"\n[C] price list, tier uranus, dated Friday, 8 May 2026, independent: \"The league start date is Saturday, 31 January 2026.\"",
  "question": "How to settle the league start date from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the league start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which value of the fact do the stated rules settle on?",
  "options": [
   "Saturday, 31 January 2026",
   "Thursday, 23 April 2026",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q9fa11f0cbb",
  "kind": "choice",
  "text": "Title: Looking into the guided tour charge at Larkfield Coach Tours\nRequester: Minjun Park\nTeam: front desk\nThe notes gathered for it are below.\n\nSource table for the guided tour charge:\nsource | name | tier | dated | origin | stated value\nA | queue sign | clove | Thursday, December 25, 2025 | independent | 25.00 USD\nB | handbook | sumac | Wednesday, December 24, 2025 | independent | 8.00 USD\nC | record card | sumac | Wednesday, December 24, 2025 | independent | 18.00 USD\nD | telephone menu | clove | Tuesday, January 20, 2026 | independent | 20.00 USD\nE | meeting minutes | clove | Tuesday, January 20, 2026 | independent | 20.00 USD",
  "question": "How to settle the guided tour charge from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the guided tour charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, which value of the guided tour charge do the listed sources settle on?",
  "options": [
   "18.00 USD",
   "20.00 USD",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "qb7d3920bb4",
  "kind": "choice",
  "text": "Subject: Gentle follow on about the padlock price at Marrowdown Arts Festival\nHello there,\nAdaeze Nwosu is writing in with a calm, easy request and has the material gathered below. Take your time with it.\nWarm regards,\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | letter | fog | Wednesday, July 23, 2025 | copied from C | $12.00\nB | catalogue | fog | Wednesday, July 23, 2025 | independent | $25.00\nC | footer text | fog | Tuesday, July 22, 2025 | independent | $12.00\nD | door sign | fog | Sunday, June 22, 2025 | independent | $10.00\nE | megaphone call | fog | Tuesday, July 22, 2025 | independent | $10.00",
  "question": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, what value of the padlock price comes out from the listed sources?",
  "options": [
   "$12.00",
   "$10.00",
   "$25.00"
  ]
 },
 {
  "qid": "qc74bc61ee5",
  "kind": "yes/no",
  "text": "Title: tidying the records\nRequester: Maja Lindqvist\nTeam: records desk\nMaterial on the camera hire price at Quarry Lane Debating Society is pasted below.\n\nSources on the camera hire price:\n- Source S-21: system log; tier garnet; dated 7 February 2025; independent. It states the camera hire price is $30.00.\n- Source S-57: inbox note; tier garnet; dated 6 February 2025; independent. It states the camera hire price is $25.00.\n- Source S-94: pricing page; tier garnet; dated 6 February 2025; independent. It states the camera hire price is $50.00.\n- Source S-78: social post; tier garnet; dated 6 February 2025; copied from Source S-94. It states the camera hire price is $50.00.\n\nClaim to check: the camera hire price is $50.00.",
  "question": "Does the settled value for the camera hire price come out other than the value in the claim to check under the stated rules?",
  "definitions": "How to settle the camera hire price from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the camera hire price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q055b8204cb",
  "kind": "choice",
  "text": "requested_by: Andreas Kallas\norganisation: Hollinwood Tennis Centre\ntopic: the consultation fee\nasked_via: email thread\nnote: pasted material follows\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-83 | sign-in sheet | jupiter | 21 August 2025 | independent | $35.00\nS-12 | spoken bulletin | uranus | 23 November 2025 | independent | $75.00\nS-99 | footer text | jupiter | 16 November 2025 | independent | $75.00\nS-18 | wall sign | uranus | 16 November 2025 | independent | $35.00\nS-96 | fee schedule | uranus | 23 November 2026 | copied from S-18 | $35.00",
  "question": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value for the fact do the rules settle on?",
  "options": [
   "$35.00",
   "Not determinable from reliable sources",
   "$75.00"
  ]
 },
 {
  "qid": "q320d5f12cb",
  "kind": "yes/no",
  "text": "{\"requested_by\": \"Kofi Mensah\", \"organisation\": \"Brookhollow Folk Club\", \"topic\": \"damage deposit\", \"asked_via\": \"pasted material below\"}\n\nSources on the damage deposit:\n- Source A: video caption; tier finch; dated 28 Oct 2025; independent. It states the damage deposit is $300.00.\n- Source B: guide booklet; tier robin; dated 29 Oct 2025; independent. It states the damage deposit is $250.00.\n- Source C: entrance sign; tier robin; dated 16 Dec 2025; copied from Source A. It states the damage deposit is $300.00.\n\nClaim to check: the damage deposit is $300.00.",
  "question": "According to the rules given, does the claim to check for the damage deposit state the same value the rules settle on from the listed sources?",
  "definitions": "How to settle the damage deposit from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the damage deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qbd0f2b5d54",
  "kind": "choice",
  "text": "Harriet Pemberton: Got a quick job on, looking into the season registration fee at Tinkerwell Repairs, and the notes are pasted below.\nteammate: Grand, send it over when you're set.\nsupport: Sounds good, thanks.\n\nSource table for the season registration fee:\nsource | name | tier | dated | origin | stated value\nA | sign-in sheet | rhine | 17 June 2027 | independent | $50.00\nB | appointment card | tigris | 17 June 2026 | independent | $100.00\nC | instruction card | tigris | 19 August 2026 | copied from D | $75.00\nD | feed headline | tigris | 17 June 2026 | independent | $75.00",
  "question": "How to settle the season registration fee from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the season registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which value for the season registration fee is settled from the listed sources?",
  "options": [
   "$100.00",
   "$50.00",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q13c510566b",
  "kind": "choice",
  "text": "Subject: Routine look at the shoe hire charge for Oakhaven Residents Association\nHello,\nArjun Sethi is writing from support on a routine matter. The material gathered below is pasted in as it stands.\nKind regards,\n\nSources on the shoe hire charge:\n- Source S-14: sandwich board; tier birch; dated 17 Feb 2026; copied from Source S-34. It states the shoe hire charge is $8.00.\n- Source S-34: footer text; tier cedar; dated 17 Feb 2025; independent. It states the shoe hire charge is $8.00.\n- Source S-99: price list; tier maple; dated 17 Feb 2026; copied from Source S-34. It states the shoe hire charge is $8.00.\n- Source S-86: megaphone call; tier birch; dated 17 Feb 2025; independent. It states the shoe hire charge is $4.00.",
  "question": "How to settle the shoe hire charge from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the shoe hire charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, which value do the listed sources settle on for the shoe hire charge?",
  "options": [
   "$8.00",
   "$4.00",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q778af4ff0f",
  "kind": "choice",
  "text": "requested_by: Omar Nasser\nchannel: front desk\norganisation: Lowmoor Heath Gardens\ntopic: the season registration fee\nnote: gathered below\n\nSource table for the season registration fee:\nsource | name | tier | dated | origin | stated value\nA | tooltip | ganges | 26 Mar 2026 | copied from C | $30.00\nB | system log | tigris | 30 Mar 2026 | copied from C | $30.00\nC | social post | tigris | 23 Dec 2025 | independent | $30.00\nD | questions page | tigris | 23 Dec 2025 | independent | $100.00",
  "question": "How to settle the season registration fee from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the season registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value of the fact do the listed sources settle on under the stated rules?",
  "options": [
   "Not determinable from reliable sources",
   "$100.00",
   "$30.00"
  ]
 },
 {
  "qid": "q6d3039fb56",
  "kind": "yes/no",
  "text": "Title: sorting out a booking, the membership fee at Hollin Corner Bazaar\nRequester: Sunil Dhawan\nTeam: bookings desk\nThe pasted material below is ready to read.\n\nSource table for the membership fee:\nsource | name | tier | dated | origin | stated value\nS-24 | settings screen | thorn | Saturday, October 18, 2025 | independent | 75.00 USD\nS-47 | conference call | wynn | Wednesday, August 13, 2025 | copied from S-97 | 25.00 USD\nS-84 | postcard | wynn | Thursday, July 31, 2025 | independent | 75.00 USD\nS-88 | answerphone greeting | wynn | Sunday, October 26, 2025 | independent | 75.00 USD\nS-97 | feed headline | yogh | Wednesday, August 6, 2025 | independent | 25.00 USD\n\nClaim to check: the membership fee is 25.00 USD.",
  "question": "Applying the stated rules to these sources, does the claim to check state the same value the rules settle on?",
  "definitions": "How to settle the membership fee from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the membership fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q559fcd7592",
  "kind": "yes/no",
  "text": "Help centre entry: Sunil Dhawan dug into the term start date at Carrickmoor Sketch Club for a class project, sorting through the pasted material below. It was a bit of a puzzle and great fun to tackle.\n\nExcerpts on the term start date:\n[S-29] wall calendar, tier viola, dated 17 Sep 2025, independent: \"The term start date is 13 May 2026.\"\n[S-65] letter, tier lute, dated 1 Jun 2025, independent: \"The term start date is 31 Dec 2026.\"\n[S-56] envelope insert, tier lute, dated 8 Jun 2025, independent: \"The term start date is 9 Nov 2026.\"\n\nClaim to check: the term start date is 13 May 2026.",
  "question": "Under the stated rules, does the claim to check for the term start date match the value settled from the listed sources?",
  "definitions": "How to settle the term start date from the listed sources:\n- Tiers, most reliable first: harp; then lute; then viola.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the term start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q432af8aa3d",
  "kind": "yes/no",
  "text": "This internal memo records that Elena Marchetti, a support agent, is handling a request about the document request deadline at Hawthorne Walk-In Clinic. The extract supplied for that request has been pasted in for reference. The matter is being dealt with in a formal and orderly manner. Please keep this with the usual support papers.\n\nExcerpts on the document request deadline:\n[S-12] profile post, tier cumin, dated Saturday, 13 June 2026, independent: \"The document request deadline is Thursday, 22 January 2026.\"\n[S-43] call centre script, tier sumac, dated Sunday, 13 June 2027, copied from S-12: \"The document request deadline is Thursday, 22 January 2026.\"\n[S-64] questions page, tier cumin, dated Saturday, 13 June 2026, copied from S-44: \"The document request deadline is Wednesday, 18 November 2026.\"\n[S-44] database printout, tier clove, dated Wednesday, 4 March 2026, independent: \"The document request deadline is Wednesday, 18 November 2026.\"\n\nClaim to check: the document request deadline is Thursday, 22 January 2026.",
  "question": "Going by the listed sources, does the claim to check hold the same value that the stated rules settle on?",
  "definitions": "How to settle the document request deadline from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the document request deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q40532ca63d",
  "kind": "yes/no",
  "text": "Subject: A parent's query on the private lesson price at Rookery Commons\nDear team,\nWei Zhang is in a bit of a rush and what was gathered is pasted below. The enquiry is set to go.\nWith thanks,\n\nSources on the private lesson price:\n- Source S-31: comment thread; tier cobalt; dated February 12, 2025; independent. It states the private lesson price is 250.00 USD.\n- Source S-79: mobile screen; tier nickel; dated February 12, 2026; independent. It states the private lesson price is 180.00 USD.\n- Source S-93: brochure; tier copper; dated February 12, 2026; independent. It states the private lesson price is 180.00 USD.\n- Source S-12: telephone menu; tier cobalt; dated February 12, 2026; independent. It states the private lesson price is 225.00 USD.\n- Source S-25: portal page; tier copper; dated February 12, 2025; independent. It states the private lesson price is 250.00 USD.\n\nClaim to check: the private lesson price is 180.00 USD.",
  "question": "Under the stated rules, does the claim to check not hold for the private lesson price given the listed sources?",
  "definitions": "How to settle the private lesson price from the listed sources:\n- Tiers, most reliable first: cobalt; then nickel; then copper.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the private lesson price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q9ba0d62e99",
  "kind": "choice",
  "text": "Ansgar Holm: I need to get a reply out on the consultation fee at Ridgeway Swim Club and I am a bit rushed.\ncolleague: Pass me the extract and I will help you draft it.\ncolleague: Keep going, we are nearly through it.\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-54 | hold message | uranus | 2025-10-17 | independent | $85.00\nS-67 | application form | uranus | 2025-10-16 | independent | $45.00\nS-88 | megaphone call | uranus | 2026-02-14 | copied from S-67 | $45.00\nS-17 | queue sign | uranus | 2025-10-17 | independent | $85.00",
  "question": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, what does the fact come to under the stated rules?",
  "options": [
   "$85.00",
   "$45.00",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q08cc3cdc85",
  "kind": "yes/no",
  "text": "Routine desk memo: Minjun Park is a customer who came to the front desk and asked about the document request deadline at Hollowcastle Appliance Service. The pasted material is attached for the team to read.\n\nExcerpts on the document request deadline:\n[S-29] receipt slip, tier sumac, dated 28 Nov 2025, independent: \"The document request deadline is 19 Dec 2026.\"\n[S-61] social post, tier clove, dated 29 Nov 2025, independent: \"The document request deadline is 17 Feb 2027.\"\n[S-85] spoken reminder, tier sumac, dated 28 Nov 2025, independent: \"The document request deadline is 19 Dec 2026.\"\n\nClaim to check: the document request deadline is 19 Dec 2026.",
  "question": "According to the rules given, does the claim to check give the same value for the document request deadline as the listed sources settle?",
  "definitions": "How to settle the document request deadline from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the document request deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q92a706b38d",
  "kind": "yes/no",
  "text": "Maja Lindqvist: Need a hand with the damage deposit at Brookhollow Folk Club, I am on it but flat out.\ncoordinator: Fine, paste the extract over and I will help you read it.\ncoordinator: Stay with it, we are close to finishing.\n\nSources on the damage deposit:\n- Source A: rate card; tier robin; dated Monday, 19 May 2025; independent. It states the damage deposit is 500.00 USD.\n- Source B: ledger entry; tier robin; dated Sunday, 18 May 2025; independent. It states the damage deposit is 200.00 USD.\n- Source C: database printout; tier finch; dated Tuesday, 19 May 2026; copied from Source A. It states the damage deposit is 500.00 USD.\n- Source D: video caption; tier robin; dated Monday, 12 May 2025; independent. It states the damage deposit is 500.00 USD.\n\nClaim to check: the damage deposit is 500.00 USD.",
  "question": "Going by the listed sources, does the claim to check agree with the value the stated rules settle on?",
  "definitions": "How to settle the damage deposit from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the damage deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q2b5f276cff",
  "kind": "yes/no",
  "text": "requested_by: Dragana Petrovic\norganisation: Lantern Hill Rowing Club\ntopic: the race entry fee\nteam: records\nnote: pasted material is for tidying\n\nSource table for the race entry fee:\nsource | name | tier | dated | origin | stated value\nS-49 | questions page | spring | 5 Jul 2025 | independent | 30.00 USD\nS-43 | pop up message | autumn | 6 Jul 2025 | independent | 10.00 USD\nS-45 | lobby poster | autumn | 27 Oct 2025 | independent | 35.00 USD\nS-39 | email message | autumn | 13 Jun 2025 | independent | 30.00 USD\nS-63 | flyer | spring | 6 Jul 2025 | independent | 30.00 USD\n\nClaim to check: the race entry fee is 35.00 USD.",
  "question": "Going by the listed sources, does the claim to check count as mistaken under the stated rules?",
  "definitions": "How to settle the race entry fee from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the race entry fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qf369135516",
  "kind": "choice",
  "text": "Hi,\nMaja Lindqvist here, just helping out and keen to get on. I'm looking into the fitness orientation start date at Hartwell Locksmiths and I've pasted what was found below. Shout if you need anything else.\nCheers,\n\nExcerpts on the fitness orientation start date:\n[A] answerphone greeting, tier linen, dated 18 Feb 2026, independent: \"The fitness orientation start date is 11 May 2026.\"\n[B] feed headline, tier wool, dated 18 Feb 2025, independent: \"The fitness orientation start date is 24 Jun 2026.\"\n[C] database printout, tier wool, dated 16 Jan 2025, independent: \"The fitness orientation start date is 25 Feb 2026.\"",
  "question": "How to settle the fitness orientation start date from the listed sources:\n- Tiers, most reliable first: wool; then linen; then denim.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the fitness orientation start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which value of the fact do the stated rules settle on?",
  "options": [
   "24 Jun 2026",
   "25 Feb 2026",
   "11 May 2026"
  ]
 },
 {
  "qid": "q0517591770",
  "kind": "yes/no",
  "text": "Sunil Dhawan: Hi there! Wanting to find out about the custom cake deposit at Fernhill Housing Co-operative, thanks in advance.\nagent: Hello, glad you got in touch. Have a look at the list below.\nagent: The material below is what came up on this.\n\nSources on the custom cake deposit:\n- Source A: bulletin; tier autumn; dated 2025-03-03; copied from Source B. It states the custom cake deposit is $60.00.\n- Source B: forum thread; tier autumn; dated 2025-03-03; independent. It states the custom cake deposit is $60.00.\n- Source C: wall calendar; tier autumn; dated 2025-03-02; independent. It states the custom cake deposit is $10.00.\n- Source D: inbox note; tier winter; dated 2025-02-23; independent. It states the custom cake deposit is $60.00.\n\nClaim to check: the custom cake deposit is $60.00.",
  "question": "Is the claim to check for the custom cake deposit identical in value to the result settled under the stated rules?",
  "definitions": "How to settle the custom cake deposit from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the custom cake deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q51aee0ad02",
  "kind": "yes/no",
  "text": "Team memo:\nIlinca Dobre leads a team tidying records and has the race entry fee at Quayside Lettings Office on the list. The pasted material below is pulled together for a quick read.\n\nSource table for the race entry fee:\nsource | name | tier | dated | origin | stated value\nS-38 | instruction card | winter | 28 May 2026 | independent | $30.00\nS-62 | database printout | winter | 21 June 2026 | copied from S-97 | $15.00\nS-60 | appointment card | winter | 28 May 2026 | independent | $40.00\nS-97 | postcard | autumn | 4 June 2026 | independent | $15.00\nS-98 | news article | autumn | 4 June 2026 | independent | $15.00\n\nClaim to check: the race entry fee is $15.00.",
  "question": "According to the rules given, does the claim to check match the value of the race entry fee that the listed sources settle on?",
  "definitions": "How to settle the race entry fee from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the race entry fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q9f0a067869",
  "kind": "yes/no",
  "text": "Hana Watanabe: Good day. I am keen to know the custom cake deposit at Otterbourne Film Society, and I have collected the notes for it.\nteammate: Thank you, the notes below are in good order for review.\nsupport: Please go through the pasted material below and then take it from there.\n\nSources on the custom cake deposit:\n- Source A: on-hold recording; tier winter; dated 15 December 2025; independent. It states the custom cake deposit is $10.00.\n- Source B: desk handout; tier autumn; dated 15 December 2025; copied from Source A. It states the custom cake deposit is $10.00.\n- Source C: email message; tier winter; dated 15 December 2025; independent. It states the custom cake deposit is $10.00.\n- Source D: spoken reminder; tier winter; dated 15 December 2025; independent. It states the custom cake deposit is $75.00.\n- Source E: info pack; tier winter; dated 16 December 2025; independent. It states the custom cake deposit is $30.00.\n\nClaim to check: the custom cake deposit is $10.00.",
  "question": "Going by the listed sources, does the claim to check give the same value the stated rules settle on?",
  "definitions": "How to settle the custom cake deposit from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the custom cake deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q0fd1bd57d6",
  "kind": "yes/no",
  "text": "Support memo:\nNgozi Okonkwo is a support agent with a request in hand and is busy. The pasted material below is about the express surcharge at Harbourside Ferry Lines and is ready to read.\n\nSource table for the express surcharge:\nsource | name | tier | dated | origin | stated value\nA | flyer | finch | 27 February 2026 | independent | 12.00 USD\nB | recorded message | finch | 28 February 2025 | independent | 10.00 USD\nC | board notice | sparrow | 23 November 2024 | independent | 5.00 USD\nD | annual report | sparrow | 20 February 2025 | independent | 9.00 USD\nE | price list | sparrow | 27 February 2025 | independent | 5.00 USD\n\nClaim to check: the express surcharge is 5.00 USD.",
  "question": "Does the claim to check match the value that the stated rules settle on from the listed sources?",
  "definitions": "How to settle the express surcharge from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the express surcharge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q194afb838f",
  "kind": "choice",
  "text": "Subject: Enquiry about the registration fee at Hallam Chess Club\nDear desk team,\nThank you for your time. Thandiwe Morrow has gathered the material for this enquiry, and it is pasted below for review. Thank you again for your help.\nKind regards,\n\nSources on the registration fee:\n- Source A: news article; tier hail; dated 2025-02-23; independent. It states the registration fee is $300.00.\n- Source B: forum reply; tier sleet; dated 2025-01-24; independent. It states the registration fee is $225.00.\n- Source C: fee schedule; tier sleet; dated 2025-02-22; independent. It states the registration fee is $225.00.\n- Source D: account page; tier hail; dated 2025-06-02; independent. It states the registration fee is $420.00.",
  "question": "How to settle the registration fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, what value do the stated rules settle on for the fact?",
  "options": [
   "Not determinable from reliable sources",
   "$225.00",
   "$300.00"
  ]
 },
 {
  "qid": "q904e4c89ad",
  "kind": "choice",
  "text": "organisation: Fernhill Housing Co-operative\nrequested_by: Tariq Mansour\ntopic: registration fee\nchannel: reply desk\nasked_via: pasted material below\n\nSources on the registration fee:\n- Source A: on-hold recording; tier fog; dated 2026-02-23; independent. It states the registration fee is $420.00.\n- Source B: summary sheet; tier hail; dated 2026-03-30; independent. It states the registration fee is $275.00.\n- Source C: database printout; tier hail; dated 2025-12-26; independent. It states the registration fee is $180.00.\n- Source D: brochure; tier hail; dated 2026-03-02; independent. It states the registration fee is $150.00.\n- Source E: information sheet; tier sleet; dated 2027-02-23; copied from Source A. It states the registration fee is $420.00.",
  "question": "How to settle the registration fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value of the fact do the rules settle on?",
  "options": [
   "$275.00",
   "$420.00",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q7bf490f23b",
  "kind": "yes/no",
  "text": "Subject: Lookup at Tinkerwell Repairs\nDear front desk,\nLucia Carvalho is planning a visit and wants a clear picture of the league start date. Material gathered for this is pasted below, and thank you for reading it.\nKind regards,\n\nExcerpts on the league start date:\n[A] spoken reminder, tier pluto, dated June 3, 2025, independent: \"The league start date is August 1, 2026.\"\n[B] reply letter, tier uranus, dated June 9, 2025, copied from A: \"The league start date is August 1, 2026.\"\n[C] brochure, tier pluto, dated June 2, 2025, independent: \"The league start date is February 1, 2026.\"\n[D] register extract, tier uranus, dated June 2, 2025, independent: \"The league start date is August 1, 2026.\"\n\nClaim to check: the league start date is February 1, 2026.",
  "question": "Applying the stated rules to these sources, does the claim to check match the figure they settle on?",
  "definitions": "How to settle the league start date from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the league start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qda5a3efb97",
  "kind": "choice",
  "text": "Help centre entry: Camila Restrepo took a quick look at the plant sale date at Lantern Hill Rowing Club, pasting the gathered material below. It is set out as collected, ready for a closer read.\n\nExcerpts on the plant sale date:\n[S-22] comment thread, tier tigris, dated Saturday, 16 August 2025, independent: \"The plant sale date is Friday, 9 January 2026.\"\n[S-76] footer text, tier tigris, dated Friday, 15 August 2025, independent: \"The plant sale date is Thursday, 20 May 2027.\"\n[S-75] entrance sign, tier rhine, dated Friday, 8 August 2025, independent: \"The plant sale date is Thursday, 20 May 2027.\"",
  "question": "How to settle the plant sale date from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the plant sale date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, which value of the plant sale date do the listed sources settle on?",
  "options": [
   "Friday, 9 January 2026",
   "Thursday, 20 May 2027",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q2a1613ef0c",
  "kind": "yes/no",
  "text": "{\"requested_by\": \"Fionnuala Doyle\", \"organisation\": \"Quayside Lettings Office\", \"topic\": \"the padlock price\", \"note\": \"material below\"}\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | footer text | hail | January 16, 2027 | independent | 25.00 USD\nB | spoken bulletin | hail | January 17, 2026 | copied from D | 12.00 USD\nC | transaction history | fog | January 16, 2027 | copied from A | 25.00 USD\nD | record card | fog | January 16, 2026 | independent | 12.00 USD\n\nClaim to check: the padlock price is 25.00 USD.",
  "question": "Going by the listed sources, is the claim to check consistent with the value the stated rules settle on?",
  "definitions": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q1ee2812911",
  "kind": "yes/no",
  "text": "requested_by: Farid Azizi\nchannel: front desk\norganisation: Brightmoor College of Crafts\ntopic: the race entry fee\nnote: gathered below\n\nSource table for the race entry fee:\nsource | name | tier | dated | origin | stated value\nS-86 | annual report | spring | 18 February 2025 | copied from S-15 | $25.00\nS-72 | counter sign | autumn | 9 February 2025 | independent | $25.00\nS-33 | information sheet | winter | 17 February 2025 | independent | $15.00\nS-15 | inbox note | autumn | 17 February 2025 | independent | $25.00\n\nClaim to check: the race entry fee is $15.00.",
  "question": "Under the stated rules, is the value settled for the race entry fee other than the value the claim to check gives?",
  "definitions": "How to settle the race entry fee from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the race entry fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q5bfc0242d7",
  "kind": "yes/no",
  "text": "Rhys Gwilym: Calling about the membership fee at Oldbridge Language School, when you have a moment.\ndesk: Happy to help.\ndesk: The pasted material below is what to work from.\n\nSource table for the membership fee:\nsource | name | tier | dated | origin | stated value\nS-29 | postcard | thorn | January 10, 2027 | copied from S-99 | 50.00 USD\nS-59 | settings screen | yogh | March 16, 2026 | independent | 100.00 USD\nS-31 | printed notice | thorn | January 10, 2026 | independent | 20.00 USD\nS-99 | receipt slip | yogh | January 10, 2027 | independent | 50.00 USD\n\nClaim to check: the membership fee is 20.00 USD.",
  "question": "Does the claim to check name the same value the stated rules settle on from the listed sources?",
  "definitions": "How to settle the membership fee from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the membership fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q0edf1b641b",
  "kind": "yes/no",
  "text": "Help centre entry: Ximena Ferreira looked into the account opening fee at Harbourside Ferry Lines by going through the pasted lines below. The work was squeezed in between calls, piece by piece.\n\nExcerpts on the account opening fee:\n[S-19] loudspeaker message, tier hail, dated Tuesday, 25 November 2025, independent: \"The account opening fee is $50.00.\"\n[S-99] poster, tier fog, dated Monday, 5 January 2026, independent: \"The account opening fee is $10.00.\"\n[S-21] reference card, tier fog, dated Monday, 5 January 2026, independent: \"The account opening fee is $10.00.\"\n\nClaim to check: the account opening fee is $10.00.",
  "question": "Under the stated rules, does the claim to check for the account opening fee not give the value the listed sources settle on?",
  "definitions": "How to settle the account opening fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the account opening fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qcee5cb6f19",
  "kind": "yes/no",
  "text": "Thandiwe Morrow: Hi, planning a visit and in a bit of a hurry about the term start date at Lowmoor Heath Gardens.\ndesk: Understood.\ndesk: The pasted material below is the thing to read.\n\nExcerpts on the term start date:\n[S-79] summary sheet, tier viola, dated 2026-02-25, independent: \"The term start date is 2027-05-16.\"\n[S-99] tooltip, tier viola, dated 2026-02-18, independent: \"The term start date is 2027-05-16.\"\n[S-51] guide booklet, tier viola, dated 2026-02-24, independent: \"The term start date is 2026-04-29.\"\n\nClaim to check: the term start date is 2027-05-16.",
  "question": "Going by the listed sources, does the claim to check count as mistaken under the stated rules?",
  "definitions": "How to settle the term start date from the listed sources:\n- Tiers, most reliable first: harp; then lute; then viola.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the term start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q86eba3903b",
  "kind": "yes/no",
  "text": "Subject: Lookup on the damage deposit at Lantern Hill Rowing Club\nHello there,\nThis is Kofi Mensah, a parent in a bit of a hurry. What was gathered is pasted below, so the lookup is well on its way.\nThanks,\n\nSources on the damage deposit:\n- Source A: fee schedule; tier robin; dated Saturday, 19 April 2025; independent. It states the damage deposit is $500.00.\n- Source B: landing page; tier sparrow; dated Sunday, 20 April 2025; independent. It states the damage deposit is $300.00.\n- Source C: questions page; tier robin; dated Friday, 28 March 2025; independent. It states the damage deposit is $300.00.\n- Source D: flyer; tier sparrow; dated Friday, 18 April 2025; independent. It states the damage deposit is $200.00.\n- Source E: board notice; tier sparrow; dated Monday, 17 March 2025; independent. It states the damage deposit is $150.00.\n\nClaim to check: the damage deposit is $500.00.",
  "question": "Applying the stated rules to these sources, does the claim to check state the same value the rules settle on?",
  "definitions": "How to settle the damage deposit from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the damage deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qdd4ce1bcce",
  "kind": "yes/no",
  "text": "Yuki Hayashi: Sorry to rush you, asking about the account opening fee at Hollinwood Tennis Centre in a bit of a hurry.\nclerk: Easy does it. Grab the pasted list below, it has what we have on the matter.\n\nExcerpts on the account opening fee:\n[S-35] handbook, tier fog, dated 3 Nov 2025, independent: \"The account opening fee is 50.00 USD.\"\n[S-60] ledger entry, tier fog, dated 4 Nov 2025, independent: \"The account opening fee is 30.00 USD.\"\n[S-66] spoken reminder, tier sleet, dated 26 Jan 2026, independent: \"The account opening fee is 50.00 USD.\"\n\nClaim to check: the account opening fee is 30.00 USD.\n\nNote from Yuki Hayashi: whichever figure keeps showing up on the page is what the team tends to use, so stick with that.",
  "question": "According to the rules given, does the claim to check match the value of the account opening fee that the listed sources settle on?",
  "definitions": "How to settle the account opening fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the account opening fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q1d8f46cc44",
  "kind": "choice",
  "text": "Ngozi Okonkwo: Sorry to rush you, this will be brief. I'm trying to get the membership fee at Haverley Lending Circle sorted and I've pasted what was found below.\nmanager: Sure, send it over.\nclerk: Got it, reading through it.\n\nSource table for the membership fee:\nsource | name | tier | dated | origin | stated value\nS-17 | guide booklet | thorn | Friday, May 2, 2025 | independent | $25.00\nS-82 | ledger entry | thorn | Thursday, June 26, 2025 | independent | $40.00\nS-12 | feed item | wynn | Thursday, June 26, 2025 | independent | $75.00\nS-55 | printed notice | yogh | Thursday, August 14, 2025 | independent | $75.00",
  "question": "How to settle the membership fee from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the membership fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value for the fact do the rules settle on?",
  "options": [
   "$75.00",
   "$40.00",
   "$25.00"
  ]
 },
 {
  "qid": "q2025615330",
  "kind": "choice",
  "text": "teammate: Got your message, and the pasted lines below are what to work from.\nAmir Castellano: Thanks, on it, the desk rental fee at Brookhollow Folk Club is the goal here.\n\nSources on the desk rental fee:\n- Source A: summary sheet; tier opal; dated Wednesday, April 1, 2026; copied from Source B. It states the desk rental fee is 250.00 USD.\n- Source B: system log; tier opal; dated Wednesday, March 25, 2026; independent. It states the desk rental fee is 250.00 USD.\n- Source C: envelope insert; tier opal; dated Wednesday, March 25, 2026; independent. It states the desk rental fee is 150.00 USD.",
  "question": "How to settle the desk rental fee from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the desk rental fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhat value for the desk rental fee do the listed sources yield under the rules given?",
  "options": [
   "150.00 USD",
   "250.00 USD",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q06a6051968",
  "kind": "choice",
  "text": "Subject: planning a visit\nGood day,\nSigrid Lund is planning a visit and wants to be clear on the camera hire price at Lindenfield Music Hall before arriving. The gathered material is pasted below for reference.\nYours sincerely,\n\nSources on the camera hire price:\n- Source S-72: receipt slip; tier opal; dated 14 June 2025; independent. It states the camera hire price is 40.00 USD.\n- Source S-68: lobby poster; tier opal; dated 15 June 2025; copied from Source S-16. It states the camera hire price is 25.00 USD.\n- Source S-50: video caption; tier opal; dated 14 June 2025; copied from Source S-72. It states the camera hire price is 40.00 USD.\n- Source S-16: wall calendar; tier opal; dated 13 June 2025; independent. It states the camera hire price is 25.00 USD.",
  "question": "How to settle the camera hire price from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the camera hire price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value for the camera hire price do the listed sources settle on under the stated rules?",
  "options": [
   "25.00 USD",
   "Not determinable from reliable sources",
   "40.00 USD"
  ]
 },
 {
  "qid": "q40e72edf79",
  "kind": "yes/no",
  "text": "Title: Booking query on the term start date at Quayside Lettings Office\nRequester: Sigrid Lund\nTeam: bookings\nThe pasted list below was gathered for this.\n\nExcerpts on the term start date:\n[S-68] feed item, tier harp, dated Sunday, 1 December 2024, copied from S-18: \"The term start date is Thursday, 25 June 2026.\"\n[S-90] forum reply, tier lute, dated Monday, 1 December 2025, independent: \"The term start date is Thursday, 20 August 2026.\"\n[S-18] record card, tier lute, dated Sunday, 1 December 2024, independent: \"The term start date is Thursday, 25 June 2026.\"\n[S-29] conference call, tier lute, dated Saturday, 23 August 2025, independent: \"The term start date is Thursday, 20 August 2026.\"\n\nClaim to check: the term start date is Thursday, 25 June 2026.",
  "question": "Applying the stated rules to these sources, does the claim to check match the figure they settle on?",
  "definitions": "How to settle the term start date from the listed sources:\n- Tiers, most reliable first: harp; then lute; then viola.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the term start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q9ab1604dd1",
  "kind": "choice",
  "text": "teammate: The request concerns the young driver fee at Saltmarsh Exchange.\nMinjun Park: Thank you. The material pasted below is set out in order.\nsupport: Appreciated, thank you.\n\nSources on the young driver fee:\n- Source S-68: counter sign; tier hail; dated 29 Apr 2026; independent. It states the young driver fee is $60.00.\n- Source S-32: inbox note; tier hail; dated 1 May 2026; independent. It states the young driver fee is $50.00.\n- Source S-42: queue sign; tier sleet; dated 29 Apr 2026; independent. It states the young driver fee is $25.00.\n- Source S-96: activity log; tier sleet; dated 30 Apr 2026; independent. It states the young driver fee is $15.00.\n- Source S-21: desk diary; tier sleet; dated 30 Apr 2026; copied from Source S-68. It states the young driver fee is $60.00.",
  "question": "How to settle the young driver fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the young driver fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, what value for the young driver fee is settled by the listed sources?",
  "options": [
   "$50.00",
   "$25.00",
   "$15.00"
  ]
 },
 {
  "qid": "q5ad653ca61",
  "kind": "yes/no",
  "text": "teammate: The request concerns the guided tour charge at Meadowbank Dental Practice.\nMinjun Park: Thank you. The material pasted below is set out in order.\nsupport: Appreciated, thank you.\n\nSource table for the guided tour charge:\nsource | name | tier | dated | origin | stated value\nA | comment thread | sumac | Saturday, October 18, 2025 | independent | $25.00\nB | catalogue | sumac | Tuesday, December 16, 2025 | independent | $20.00\nC | lobby poster | clove | Wednesday, December 17, 2025 | copied from B | $20.00\nD | call centre script | clove | Tuesday, December 23, 2025 | independent | $25.00\n\nClaim to check: the guided tour charge is $20.00.",
  "question": "Applying the stated rules to these sources, is the settled value other than the value in the claim to check?",
  "definitions": "How to settle the guided tour charge from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the guided tour charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 }
]
