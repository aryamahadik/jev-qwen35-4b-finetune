# G5-H blind read T25-blind_read-e79f4456-001 (family T25)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T25/qc/g5h/answers/T25-blind_read-e79f4456-001.json

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
  "qid": "qd8bab3b953",
  "kind": "choice",
  "text": "Dear colleague,\nMy name is Lucia Carvalho and I am writing to look into the entry price at Cresswell Rail Company. I have pasted what was found below for your reference. Thank you for your help on this matter.\nKind regards,\n\nSources on the entry price:\n- Source A: guide booklet; tier cedar; dated Saturday, 29 November 2025; independent. It states the entry price is $35.00.\n- Source B: ledger entry; tier maple; dated Friday, 28 November 2025; independent. It states the entry price is $45.00.\n- Source C: receipt slip; tier birch; dated Thursday, 27 November 2025; copied from Source E. It states the entry price is $28.00.\n- Source D: site banner; tier cedar; dated Saturday, 29 November 2025; independent. It states the entry price is $35.00.\n- Source E: loudspeaker message; tier maple; dated Thursday, 27 November 2025; independent. It states the entry price is $28.00.",
  "question": "How to settle the entry price from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the entry price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value do the listed sources settle on for the fact, according to the stated rules?",
  "options": [
   "Not determinable from reliable sources",
   "$45.00",
   "$28.00"
  ]
 },
 {
  "qid": "qbc907566f5",
  "kind": "yes/no",
  "text": "Subject: Notes below\nHello desk,\nCamila Restrepo here, in a bit of a rush but keen to get the express surcharge at Harrowden Upholstery Services clear. Pasted below is the material gathered so far.\nBest,\n\nSource table for the express surcharge:\nsource | name | tier | dated | origin | stated value\nA | price list | sparrow | 27 November 2025 | independent | $9.00\nB | questions page | finch | 25 September 2025 | independent | $7.50\nC | letter | finch | 29 November 2025 | independent | $10.00\nD | hold message | sparrow | 5 December 2025 | copied from E | $12.00\nE | inbox note | sparrow | 28 November 2025 | independent | $12.00\n\nClaim to check: the express surcharge is $10.00.",
  "question": "Going by the listed sources, is the value the stated rules settle on other than the value in the claim to check?",
  "definitions": "How to settle the express surcharge from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the express surcharge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qd7790f3344",
  "kind": "choice",
  "text": "Title: Looking into the season registration fee at Haverley Lending Circle\nRequester: Hana Watanabe\nTeam: front desk\nThe notes gathered for it are below.\n\nSource table for the season registration fee:\nsource | name | tier | dated | origin | stated value\nA | text message | rhine | January 20, 2026 | independent | $50.00\nB | register extract | rhine | January 21, 2026 | independent | $80.00\nC | fee schedule | rhine | January 20, 2026 | independent | $80.00\nD | wall sign | rhine | January 22, 2026 | copied from A | $50.00",
  "question": "How to settle the season registration fee from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the season registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, what settled value for the season registration fee comes out of the listed sources?",
  "options": [
   "Not determinable from reliable sources",
   "$80.00",
   "$50.00"
  ]
 },
 {
  "qid": "qf2e5f4d0ca",
  "kind": "choice",
  "text": "Help centre entry: Giulia Ferraro came to the front desk and looked into the guided tour charge at Meadowbank Dental Practice with care. The material pasted below is set out neatly.\n\nSource table for the guided tour charge:\nsource | name | tier | dated | origin | stated value\nA | video caption | clove | April 6, 2026 | independent | 25.00 USD\nB | queue sign | clove | April 13, 2026 | independent | 10.00 USD\nC | guide booklet | clove | April 13, 2026 | copied from D | 12.00 USD\nD | application form | clove | December 30, 2025 | independent | 12.00 USD",
  "question": "How to settle the guided tour charge from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the guided tour charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value do they settle on for the fact?",
  "options": [
   "10.00 USD",
   "Not determinable from reliable sources",
   "25.00 USD"
  ]
 },
 {
  "qid": "q9ddf89c3b1",
  "kind": "choice",
  "text": "requested_by: Maja Lindqvist\nasked_via: member form\norganisation: Wickerwood Theatre\ntopic: the express surcharge\nnote: pasted material below\n\nSource table for the express surcharge:\nsource | name | tier | dated | origin | stated value\nA | station announcement | finch | 28 April 2025 | independent | $12.00\nB | envelope insert | sparrow | 29 April 2025 | independent | $12.00\nC | postal notice | sparrow | 14 January 2025 | independent | $15.00\nD | bulletin | finch | 30 April 2025 | independent | $9.00",
  "question": "How to settle the express surcharge from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the express surcharge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, what value of the fact is fixed by the stated rules?",
  "options": [
   "$12.00",
   "$15.00",
   "$9.00"
  ]
 },
 {
  "qid": "q004ae92c23",
  "kind": "choice",
  "text": "teammate: still on the electronics drop-off deadline at Hartwell Locksmiths, so tidy the rest.\nRhys Gwilym: got it, the material is gathered and pasted in.\ndesk: fine, filing it with the rest.\n\nExcerpts on the electronics drop-off deadline:\n[A] printed notice, tier autumn, dated 2026-04-24, independent: \"The electronics drop-off deadline is 2026-07-05.\"\n[B] call centre script, tier spring, dated 2026-04-23, independent: \"The electronics drop-off deadline is 2026-01-05.\"\n[C] social post, tier autumn, dated 2026-05-20, copied from B: \"The electronics drop-off deadline is 2026-01-05.\"\n[D] bulletin, tier winter, dated 2026-04-16, independent: \"The electronics drop-off deadline is 2027-05-08.\"",
  "question": "How to settle the electronics drop-off deadline from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the electronics drop-off deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which value for the electronics drop-off deadline is settled from the listed sources?",
  "options": [
   "2026-01-05",
   "2027-05-08",
   "2026-07-05"
  ]
 },
 {
  "qid": "qef01ef7ed4",
  "kind": "choice",
  "text": "Sofia Benitez: Bit of a hurry at the front desk about the consultation fee at Meadowbank Dental Practice.\ndesk: Pulling the pasted material up for you.\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-83 | hold message | pluto | 4 Jul 2025 | independent | $75.00\nS-99 | annual report | jupiter | 18 Jun 2025 | independent | $60.00\nS-56 | recorded message | uranus | 24 Apr 2025 | independent | $85.00\nS-68 | record card | uranus | 24 Apr 2025 | independent | $85.00",
  "question": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value do they settle on for the fact?",
  "options": [
   "$85.00",
   "$75.00",
   "$60.00"
  ]
 },
 {
  "qid": "q1f6c55b10f",
  "kind": "choice",
  "text": "Title: Lookup on the guided tour charge at Haldane Travel Express\nRequester: Jiho Kang\nTeam: staff support\nPasted material follows this ticket.\n\nSource table for the guided tour charge:\nsource | name | tier | dated | origin | stated value\nA | news article | cumin | Monday, 17 March 2025 | copied from C | 15.00 USD\nB | forum reply | cumin | Monday, 17 March 2025 | independent | 8.00 USD\nC | hanging banner | sumac | Thursday, 6 February 2025 | independent | 15.00 USD\nD | email message | cumin | Sunday, 16 March 2025 | independent | 15.00 USD",
  "question": "How to settle the guided tour charge from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the guided tour charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which of the listed sources sets the guided tour charge value?",
  "options": [
   "Source B",
   "Source C",
   "No source: not determinable from reliable sources",
   "Source A"
  ]
 },
 {
  "qid": "qa7ce6adb34",
  "kind": "yes/no",
  "text": "Title | Reply prep for the young driver fee at Larchwood Park\nRequester | Dina Saleh\nTeam | customer care\nMaterial for the reply is pasted below.\n\nSources on the young driver fee:\n- Source S-36: summary sheet; tier fog; dated Thursday, April 3, 2025; independent. It states the young driver fee is $50.00.\n- Source S-23: information sheet; tier sleet; dated Thursday, April 3, 2025; independent. It states the young driver fee is $25.00.\n- Source S-27: telephone menu; tier fog; dated Wednesday, April 2, 2025; independent. It states the young driver fee is $25.00.\n- Source S-48: flyer; tier fog; dated Wednesday, April 2, 2025; independent. It states the young driver fee is $25.00.\n- Source S-29: ledger entry; tier fog; dated Sunday, April 6, 2025; copied from Source S-36. It states the young driver fee is $50.00.\n\nClaim to check: the young driver fee is $50.00.",
  "question": "Going by the listed sources, does the claim to check give the same value the stated rules settle on?",
  "definitions": "How to settle the young driver fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the young driver fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q02cc44475c",
  "kind": "choice",
  "text": "Giulia Ferraro: Hurrying here, just grabbing the race entry fee at Marrowdown Arts Festival before leaving.\ndesk: Got it, the gathered lines are pasted below.\nsupport: Have a look at those when you get a moment.\n\nSource table for the race entry fee:\nsource | name | tier | dated | origin | stated value\nS-15 | feed item | winter | November 13, 2025 | independent | 20.00 USD\nS-85 | footer text | autumn | August 26, 2025 | independent | 50.00 USD\nS-58 | spoken reminder | autumn | November 12, 2025 | independent | 40.00 USD\nS-69 | brochure | winter | January 14, 2026 | independent | 20.00 USD",
  "question": "How to settle the race entry fee from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the race entry fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value for the fact do the rules settle on?",
  "options": [
   "20.00 USD",
   "40.00 USD",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "qeb65a16f90",
  "kind": "yes/no",
  "text": "Staff memo: Yasmin Khoury is helping out and has looked into the account opening fee at Quayside Lettings Office. The material pasted below has been gathered for the file, arranged neatly for people reviewing the matter.\n\nExcerpts on the account opening fee:\n[S-48] poster, tier fog, dated 2025-10-31, independent: \"The account opening fee is 20.00 USD.\"\n[S-19] forum reply, tier fog, dated 2025-10-31, independent: \"The account opening fee is 20.00 USD.\"\n[S-54] video caption, tier hail, dated 2025-12-21, independent: \"The account opening fee is 30.00 USD.\"\n[S-62] inbox note, tier fog, dated 2025-10-31, independent: \"The account opening fee is 20.00 USD.\"\n\nClaim to check: the account opening fee is 20.00 USD.",
  "question": "Does the claim to check name the same value the stated rules settle on from the listed sources?",
  "definitions": "How to settle the account opening fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the account opening fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q2de0b8b2ee",
  "kind": "choice",
  "text": "Help centre entry: Eleanor Farrant has been digging into the registration fee at Hollinwood Tennis Centre, and the notes are gathered together below. Happy reading, and thanks for stopping by.\n\nSources on the registration fee:\n- Source A: bulletin; tier fog; dated Saturday, 26 July 2025; copied from Source C. It states the registration fee is 225.00 USD.\n- Source B: register extract; tier sleet; dated Sunday, 27 July 2025; independent. It states the registration fee is 350.00 USD.\n- Source C: forum thread; tier sleet; dated Saturday, 26 July 2025; independent. It states the registration fee is 225.00 USD.",
  "question": "How to settle the registration fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, what settled value for the registration fee comes out of the listed sources?",
  "options": [
   "350.00 USD",
   "225.00 USD",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "qdbeef53328",
  "kind": "choice",
  "text": "Subject: Ahead of a visit\nDear desk,\nThis is Declan Murphy, planning ahead for Meadowbank Dental Practice and keen to pin down the electronics drop-off deadline. The material below is what has been put together for reference.\nYours sincerely,\n\nExcerpts on the electronics drop-off deadline:\n[A] photo caption, tier winter, dated Friday, 24 October 2025, independent: \"The electronics drop-off deadline is Tuesday, 8 September 2026.\"\n[B] printed notice, tier winter, dated Saturday, 25 October 2025, independent: \"The electronics drop-off deadline is Friday, 30 October 2026.\"\n[C] spoken reminder, tier winter, dated Wednesday, 1 October 2025, independent: \"The electronics drop-off deadline is Saturday, 29 May 2027.\"",
  "question": "How to settle the electronics drop-off deadline from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the electronics drop-off deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value does the fact end up with?",
  "options": [
   "Friday, 30 October 2026",
   "Saturday, 29 May 2027",
   "Tuesday, 8 September 2026"
  ]
 },
 {
  "qid": "q83cb0632d6",
  "kind": "choice",
  "text": "Front desk memo: Abena Boateng is planning a visit and wants the season registration fee at Thistledown Gallery pinned down. The gathered material sits pasted below for reference.\n\nSource table for the season registration fee:\nsource | name | tier | dated | origin | stated value\nA | conference call | tigris | Monday, June 1, 2026 | independent | $40.00\nB | info pack | rhine | Tuesday, June 1, 2027 | copied from A | $40.00\nC | poster | tigris | Sunday, June 1, 2025 | independent | $75.00\nD | photo caption | rhine | Sunday, June 1, 2025 | independent | $40.00\nE | comment thread | rhine | Monday, June 1, 2026 | independent | $30.00",
  "question": "How to settle the season registration fee from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the season registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value of the fact do the listed sources settle on under the stated rules?",
  "options": [
   "$75.00",
   "$40.00",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q84d1444bbb",
  "kind": "yes/no",
  "text": "Joaquin Lozano: Bit of a hurry at the front desk about the document request deadline at Meadowbank Dental Practice.\ndesk: Pulling the pasted material up for you.\n\nExcerpts on the document request deadline:\n[S-73] spoken reminder, tier cumin, dated 13 Dec 2025, independent: \"The document request deadline is 14 Mar 2027.\"\n[S-60] car park sign, tier cumin, dated 12 Dec 2025, independent: \"The document request deadline is 2 Jun 2026.\"\n[S-23] poster, tier sumac, dated 20 Dec 2025, independent: \"The document request deadline is 20 Jan 2027.\"\n\nClaim to check: the document request deadline is 14 Mar 2027.",
  "question": "Going by the listed sources, does the claim to check state the same value the stated rules settle on?",
  "definitions": "How to settle the document request deadline from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the document request deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q1316dcd14d",
  "kind": "yes/no",
  "text": "{\"organisation\": \"Marrowdown Arts Festival\", \"requested_by\": \"Lucia Carvalho\", \"topic\": \"the fitness orientation start date\", \"asked_via\": \"phone\", \"note\": \"pasted material follows\"}\n\nExcerpts on the fitness orientation start date:\n[A] hanging banner, tier denim, dated Friday, 14 February 2025, independent: \"The fitness orientation start date is Monday, 14 September 2026.\"\n[B] forum reply, tier wool, dated Friday, 14 February 2025, copied from A: \"The fitness orientation start date is Monday, 14 September 2026.\"\n[C] envelope insert, tier wool, dated Thursday, 13 February 2025, independent: \"The fitness orientation start date is Saturday, 25 April 2026.\"\n\nClaim to check: the fitness orientation start date is Monday, 14 September 2026.",
  "question": "Does the claim to check name the very value that the stated rules settle on from the listed sources?",
  "definitions": "How to settle the fitness orientation start date from the listed sources:\n- Tiers, most reliable first: wool; then linen; then denim.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the fitness orientation start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qf031093b75",
  "kind": "yes/no",
  "text": "Subject: Lookup at Linnet Savings Club\nDear front desk,\nSofia Benitez is planning a visit and wants a clear picture of the parking charge. Material gathered for this is pasted below, and thank you for reading it.\nKind regards,\n\nSources on the parking charge:\n- Source S-42: photo caption; tier rhine; dated 2 May 2025; independent. It states the parking charge is $12.00.\n- Source S-57: letter; tier rhine; dated 4 May 2025; independent. It states the parking charge is $6.00.\n- Source S-60: spoken bulletin; tier rhine; dated 5 May 2025; independent. It states the parking charge is $8.00.\n- Source S-43: bulletin; tier rhine; dated 4 May 2025; independent. It states the parking charge is $6.00.\n- Source S-69: pamphlet; tier rhine; dated 4 May 2025; independent. It states the parking charge is $8.00.\n\nClaim to check: the parking charge is $8.00.",
  "question": "Is the value in the claim to check for the parking charge the same as the listed sources settle on under the stated rules?",
  "definitions": "How to settle the parking charge from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the parking charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qe0a1d8861d",
  "kind": "yes/no",
  "text": "Subject: Enquiry for the front desk file\nDear desk team,\nMirek Hruska is writing about the camera hire price at Corrie Hall Institute, and the notes gathered below are set out in full. Thank you for your time.\nKind regards,\n\nSources on the camera hire price:\n- Source S-87: landing page; tier opal; dated 2026-06-18; independent. It states the camera hire price is 50.00 USD.\n- Source S-80: desk diary; tier garnet; dated 2026-06-25; copied from Source S-87. It states the camera hire price is 50.00 USD.\n- Source S-20: envelope insert; tier opal; dated 2026-06-19; independent. It states the camera hire price is 25.00 USD.\n- Source S-67: megaphone call; tier opal; dated 2026-06-19; copied from Source S-87. It states the camera hire price is 50.00 USD.\n\nClaim to check: the camera hire price is 25.00 USD.",
  "question": "Going by the listed sources, does the claim to check give the same value the stated rules settle on?",
  "definitions": "How to settle the camera hire price from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the camera hire price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qb90e6e3d14",
  "kind": "yes/no",
  "text": "Tariq Mansour: Tidying records at a steady pace, and the rural route price at Starling Cinema is the tricky bit.\nteammate: The gathered material is pasted below, so get it sorted.\ndesk: Give a shout when you want a hand.\n\nSources on the rural route price:\n- Source A: telephone menu; tier wynn; dated 2025-02-10; independent. It states the rural route price is $3.00.\n- Source B: station announcement; tier wynn; dated 2025-02-11; independent. It states the rural route price is $5.00.\n- Source C: flyer; tier wynn; dated 2025-02-12; independent. It states the rural route price is $3.00.\n- Source D: social post; tier yogh; dated 2025-02-11; copied from Source A. It states the rural route price is $3.00.\n\nClaim to check: the rural route price is $5.00.",
  "question": "According to the rules given, does the claim to check give the same value for the rural route price as the listed sources settle?",
  "definitions": "How to settle the rural route price from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the rural route price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q0fe817f075",
  "kind": "choice",
  "text": "Visit query | the custom cake deposit at Garrow Cab Company\nAsked by | Idris Varga\nDesk | front desk\nGathered material is pasted below.\n\nSources on the custom cake deposit:\n- Source A: postcard; tier winter; dated 17 June 2026; independent. It states the custom cake deposit is $20.00.\n- Source B: annual report; tier winter; dated 16 June 2026; independent. It states the custom cake deposit is $50.00.\n- Source C: news article; tier winter; dated 17 June 2026; independent. It states the custom cake deposit is $10.00.\n- Source D: text message; tier winter; dated 16 June 2026; independent. It states the custom cake deposit is $10.00.\n- Source E: activity log; tier spring; dated 17 June 2026; copied from Source D. It states the custom cake deposit is $10.00.",
  "question": "How to settle the custom cake deposit from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the custom cake deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which listed source should the custom cake deposit value be taken from?",
  "options": [
   "No source: not determinable from reliable sources",
   "Source E",
   "Source A"
  ]
 },
 {
  "qid": "q23d42d860a",
  "kind": "yes/no",
  "text": "Minjun Park: Quick ask at the front desk about the desk rental fee at Lindenfield Music Hall, with the gathered material pasted below.\nsupport: Got it, stand by.\ndesk: Happy to help.\n\nSources on the desk rental fee:\n- Source A: info pack; tier garnet; dated Saturday, 12 April 2025; independent. It states the desk rental fee is $220.00.\n- Source B: database printout; tier garnet; dated Monday, 3 March 2025; independent. It states the desk rental fee is $300.00.\n- Source C: conference call; tier garnet; dated Saturday, 12 April 2025; independent. It states the desk rental fee is $220.00.\n- Source D: voice message; tier garnet; dated Saturday, 12 April 2025; independent. It states the desk rental fee is $220.00.\n\nClaim to check: the desk rental fee is $300.00.",
  "question": "Going by the listed sources, does the claim to check agree with the value the stated rules settle on?",
  "definitions": "How to settle the desk rental fee from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the desk rental fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q2ffe809987",
  "kind": "yes/no",
  "text": "Subject: Lookup at Starling Cinema\nDear front desk,\nArjun Sethi is planning a visit and wants a clear picture of the registration fee. Material gathered for this is pasted below, and thank you for reading it.\nKind regards,\n\nSources on the registration fee:\n- Source A: conference call; tier sleet; dated Sunday, 12 October 2025; independent. It states the registration fee is $225.00.\n- Source B: queue sign; tier sleet; dated Sunday, 12 October 2025; independent. It states the registration fee is $225.00.\n- Source C: wall calendar; tier sleet; dated Sunday, 5 October 2025; independent. It states the registration fee is $300.00.\n\nClaim to check: the registration fee is $300.00.",
  "question": "Does the claim to check agree with the registration fee value that the listed sources yield under the stated rules?",
  "definitions": "How to settle the registration fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q7356f53099",
  "kind": "yes/no",
  "text": "Ananya Iyer, writing in as a member, looked into the account opening fee at Linnet Savings Club. The extract is pasted in with this write-up and the wording has been kept intact. The approach is recorded here so that colleagues can repeat it. Thank you for reading.\n\nExcerpts on the account opening fee:\n[S-99] questions page, tier hail, dated Monday, 19 January 2026, copied from S-20: \"The account opening fee is 20.00 USD.\"\n[S-37] ledger entry, tier fog, dated Monday, 26 January 2026, independent: \"The account opening fee is 35.00 USD.\"\n[S-20] catalogue, tier fog, dated Monday, 12 January 2026, independent: \"The account opening fee is 20.00 USD.\"\n\nClaim to check: the account opening fee is 35.00 USD.",
  "question": "Is the value in the claim to check for the account opening fee the same as the listed sources settle on under the stated rules?",
  "definitions": "How to settle the account opening fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the account opening fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qcb3af997de",
  "kind": "choice",
  "text": "{\"organisation\": \"Millrace Credit Union\", \"requested_by\": \"Farid Azizi\", \"topic\": \"the bicycle carriage charge\", \"asked_via\": \"phone\", \"note\": \"pasted material follows\"}\n\nSources on the bicycle carriage charge:\n- Source A: letter; tier ochre; dated Friday, February 21, 2025; independent. It states the bicycle carriage charge is $15.00.\n- Source B: voice message; tier teal; dated Saturday, May 10, 2025; independent. It states the bicycle carriage charge is $12.00.\n- Source C: programme; tier ochre; dated Thursday, February 27, 2025; copied from Source E. It states the bicycle carriage charge is $25.00.\n- Source D: social post; tier scarlet; dated Friday, November 29, 2024; independent. It states the bicycle carriage charge is $25.00.\n- Source E: ledger entry; tier scarlet; dated Thursday, February 20, 2025; independent. It states the bicycle carriage charge is $25.00.",
  "question": "How to settle the bicycle carriage charge from the listed sources:\n- Tiers, most reliable first: scarlet; then teal; then ochre.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the bicycle carriage charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which value for the bicycle carriage charge is settled from the listed sources?",
  "options": [
   "$15.00",
   "$12.00",
   "$25.00"
  ]
 },
 {
  "qid": "q9a41a8c375",
  "kind": "choice",
  "text": "Help centre entry: Ilinca Dobre dug into the league start date at Larkfield Coach Tours for a class project, sorting through the pasted material below. It was a bit of a puzzle and great fun to tackle.\n\nExcerpts on the league start date:\n[A] case file, tier uranus, dated 7 Sep 2025, independent: \"The league start date is 19 Nov 2026.\"\n[B] hold message, tier uranus, dated 14 Sep 2025, copied from D: \"The league start date is 31 May 2027.\"\n[C] flyer, tier uranus, dated 7 Sep 2025, independent: \"The league start date is 19 Nov 2026.\"\n[D] application form, tier pluto, dated 14 Sep 2025, independent: \"The league start date is 31 May 2027.\"",
  "question": "How to settle the league start date from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the league start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, what value do the stated rules settle on for the fact?",
  "options": [
   "Not determinable from reliable sources",
   "31 May 2027",
   "19 Nov 2026"
  ]
 },
 {
  "qid": "q7567557f99",
  "kind": "choice",
  "text": "Help centre entry: here is how Camila Restrepo looked into the fitness orientation start date at Quayside Lettings Office. The pasted material below was gathered in a calm, steady way.\n\nExcerpts on the fitness orientation start date:\n[A] account page, tier wool, dated 22 Jan 2026, independent: \"The fitness orientation start date is 18 Mar 2027.\"\n[B] car park sign, tier wool, dated 14 May 2026, independent: \"The fitness orientation start date is 11 Dec 2026.\"\n[C] postcard, tier denim, dated 21 May 2026, independent: \"The fitness orientation start date is 10 Sep 2026.\"\n[D] news article, tier wool, dated 7 May 2026, independent: \"The fitness orientation start date is 11 Dec 2026.\"",
  "question": "How to settle the fitness orientation start date from the listed sources:\n- Tiers, most reliable first: wool; then linen; then denim.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the fitness orientation start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nLooking at the listed sources, which value does the fact settle on under the stated rules?",
  "options": [
   "11 Dec 2026",
   "Not determinable from reliable sources",
   "18 Mar 2027"
  ]
 },
 {
  "qid": "qa597598862",
  "kind": "yes/no",
  "text": "{\"requested_by\": \"Jiho Kang\", \"team\": \"onboarding\", \"organisation\": \"Thimble Lane Evening Classes\", \"topic\": \"the consultation fee\", \"note\": \"notes gathered below\"}\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-36 | summary sheet | pluto | Wednesday, 18 June 2025 | independent | $75.00\nS-34 | brochure | jupiter | Thursday, 18 June 2026 | independent | $85.00\nS-51 | pop up message | jupiter | Tuesday, 17 June 2025 | independent | $85.00\nS-23 | system log | pluto | Tuesday, 17 June 2025 | independent | $75.00\nS-69 | handbook | pluto | Wednesday, 18 June 2025 | copied from S-51 | $85.00\n\nClaim to check: the consultation fee is $75.00.",
  "question": "According to the rules given, does the claim to check for the consultation fee match the value the listed sources settle on?",
  "definitions": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qd3ef0b5b8e",
  "kind": "yes/no",
  "text": "Tunde Adeyemi: Working on the reply about the custom cake deposit at Hartwell Locksmiths, which is routine stuff.\nteammate: Fine, carry on as usual.\ndesk: The notes sit just below.\n\nSources on the custom cake deposit:\n- Source A: record card; tier winter; dated 11 July 2025; independent. It states the custom cake deposit is $50.00.\n- Source B: blog entry; tier spring; dated 13 July 2025; copied from Source D. It states the custom cake deposit is $40.00.\n- Source C: feed item; tier winter; dated 9 July 2025; independent. It states the custom cake deposit is $75.00.\n- Source D: feed headline; tier winter; dated 12 July 2025; independent. It states the custom cake deposit is $40.00.\n\nClaim to check: the custom cake deposit is $50.00.",
  "question": "Does the claim to check for the custom cake deposit give the same value that the listed sources yield under the stated rules?",
  "definitions": "How to settle the custom cake deposit from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the custom cake deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q993a52d9bf",
  "kind": "choice",
  "text": "requested_by: Dina Saleh\norganisation: Stonechat Park\nteam: records\ntopic: the membership fee\n\nSource table for the membership fee:\nsource | name | tier | dated | origin | stated value\nS-52 | voice message | wynn | March 18, 2026 | independent | $75.00\nS-85 | spoken reminder | thorn | April 26, 2026 | independent | $75.00\nS-43 | instant message | thorn | April 24, 2026 | independent | $50.00\nS-11 | forum thread | thorn | April 25, 2026 | independent | $30.00\nS-23 | call centre script | thorn | July 22, 2026 | copied from S-11 | $30.00",
  "question": "How to settle the membership fee from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the membership fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which listed source supplies the value for the membership fee?",
  "options": [
   "Source S-43",
   "No source: not determinable from reliable sources",
   "Source S-85",
   "Source S-52"
  ]
 },
 {
  "qid": "q5a443b7c8c",
  "kind": "yes/no",
  "text": "requested_by: Oksana Bondar\norganisation: Meadowbank Dental Practice\ntopic: the camera hire price\nnote: details pasted below\n\nSources on the camera hire price:\n- Source S-88: poster; tier garnet; dated 1 Oct 2025; independent. It states the camera hire price is $40.00.\n- Source S-14: megaphone call; tier opal; dated 29 Sep 2025; independent. It states the camera hire price is $50.00.\n- Source S-19: board notice; tier opal; dated 30 Sep 2025; independent. It states the camera hire price is $50.00.\n- Source S-48: questions page; tier topaz; dated 29 Sep 2025; independent. It states the camera hire price is $40.00.\n\nClaim to check: the camera hire price is $40.00.",
  "question": "According to the rules given, does the camera hire price value in the claim to check equal what the stated rules settle on from the listed sources?",
  "definitions": "How to settle the camera hire price from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the camera hire price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q6acfce7764",
  "kind": "yes/no",
  "text": "Freja Nyberg: Need a hand with the padlock price at Garrow Cab Company, I am on it but flat out.\ncoordinator: Fine, paste the extract over and I will help you read it.\ncoordinator: Stay with it, we are close to finishing.\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | social post | hail | Tuesday, 13 May 2025 | independent | $18.00\nB | pamphlet | hail | Friday, 21 March 2025 | independent | $18.00\nC | rate card | fog | Wednesday, 25 June 2025 | copied from B | $18.00\nD | record card | fog | Thursday, 20 March 2025 | independent | $20.00\nE | database printout | fog | Friday, 21 March 2025 | copied from B | $18.00\n\nClaim to check: the padlock price is $20.00.",
  "question": "Does the claim to check line up with the value the listed sources settle on under the stated rules?",
  "definitions": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q8071ab8b69",
  "kind": "yes/no",
  "text": "Subject: Quick note about the consultation fee at Tinkerwell Repairs\nHi there,\nRadu Calin is helping out at speed and has the notes below ready to pass along. Sorry for the rush.\nThanks again,\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-66 | rate card | uranus | 9 October 2025 | independent | $50.00\nS-80 | receipt slip | jupiter | 10 October 2025 | copied from S-66 | $50.00\nS-81 | video caption | uranus | 9 October 2025 | independent | $50.00\nS-47 | email message | pluto | 24 November 2025 | independent | $85.00\nS-78 | feed headline | jupiter | 10 October 2025 | independent | $85.00\n\nClaim to check: the consultation fee is $50.00.",
  "question": "Applying the stated rules to these sources, is the settled value of the fact other than the value in the claim to check?",
  "definitions": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q74ad48d1df",
  "kind": "choice",
  "text": "Help centre entry: Ananya Iyer looked into the plant sale date at Carrickmoor Sketch Club while standing at the front desk, and gathered the pasted material below. The desk takes it from here.\n\nExcerpts on the plant sale date:\n[S-91] flyer, tier rhine, dated 5 Jul 2024, independent: \"The plant sale date is 19 Nov 2026.\"\n[S-17] receipt slip, tier tigris, dated 5 Jul 2025, independent: \"The plant sale date is 5 Jan 2026.\"\n[S-57] envelope insert, tier tigris, dated 5 Jul 2025, copied from S-91: \"The plant sale date is 19 Nov 2026.\"",
  "question": "How to settle the plant sale date from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the plant sale date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhat value of the fact do the stated rules settle on from the listed sources?",
  "options": [
   "Not determinable from reliable sources",
   "5 Jan 2026",
   "19 Nov 2026"
  ]
 },
 {
  "qid": "qdb3dd1715c",
  "kind": "choice",
  "text": "Help centre entry: Giulia Ferraro is looking into the plant sale date at Lowmoor Heath Gardens for a school project. The material pasted below was pulled together in a friendly, chatty way.\n\nExcerpts on the plant sale date:\n[S-84] photo caption, tier ganges, dated 6 Jan 2026, copied from S-99: \"The plant sale date is 21 Aug 2026.\"\n[S-99] handbook, tier ganges, dated 18 Aug 2025, independent: \"The plant sale date is 21 Aug 2026.\"\n[S-70] feed item, tier ganges, dated 24 Sep 2025, independent: \"The plant sale date is 1 Jul 2026.\"\n[S-72] letter, tier ganges, dated 24 Sep 2025, copied from S-99: \"The plant sale date is 21 Aug 2026.\"",
  "question": "How to settle the plant sale date from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the plant sale date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which value of the fact do the stated rules settle on?",
  "options": [
   "1 Jul 2026",
   "21 Aug 2026",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "qd1c076db53",
  "kind": "choice",
  "text": "Title | Request about the custom cake deposit at Brightwater Physio Clinic\nRequester | Sunil Dhawan\nTeam | support\nGathered material is pasted underneath.\n\nSources on the custom cake deposit:\n- Source A: poster; tier spring; dated 3 Mar 2025; independent. It states the custom cake deposit is $40.00.\n- Source B: pricing page; tier autumn; dated 4 Mar 2025; independent. It states the custom cake deposit is $30.00.\n- Source C: loudspeaker message; tier spring; dated 4 Mar 2025; copied from Source D. It states the custom cake deposit is $60.00.\n- Source D: wall calendar; tier spring; dated 26 Feb 2025; independent. It states the custom cake deposit is $60.00.\n- Source E: station announcement; tier winter; dated 4 Mar 2025; independent. It states the custom cake deposit is $60.00.",
  "question": "How to settle the custom cake deposit from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the custom cake deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich of the listed sources do the stated rules rely on for the value of this fact?",
  "options": [
   "Source A",
   "Source C",
   "No source: not determinable from reliable sources"
  ]
 },
 {
  "qid": "qf41a25cd88",
  "kind": "choice",
  "text": "Title: Booking query on the plant sale date at Lindenfield Music Hall\nRequester: Nikos Papadakis\nTeam: bookings\nThe pasted list below was gathered for this.\n\nExcerpts on the plant sale date:\n[S-55] inbox note, tier rhine, dated 24 May 2026, independent: \"The plant sale date is 9 June 2027.\"\n[S-46] wall calendar, tier ganges, dated 24 May 2026, independent: \"The plant sale date is 4 August 2026.\"\n[S-96] cover note, tier tigris, dated 24 May 2026, copied from S-55: \"The plant sale date is 9 June 2027.\"\n[S-49] letter, tier ganges, dated 24 May 2026, independent: \"The plant sale date is 4 August 2026.\"",
  "question": "How to settle the plant sale date from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the plant sale date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value do the listed sources settle on for the fact, according to the stated rules?",
  "options": [
   "9 June 2027",
   "4 August 2026",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "qd2e31e6514",
  "kind": "yes/no",
  "text": "requested_by: Lakshmi Nair\nasked_via: member form\norganisation: Hallam Chess Club\ntopic: the season registration fee\nnote: pasted material below\n\nSource table for the season registration fee:\nsource | name | tier | dated | origin | stated value\nA | footer text | rhine | 31 Oct 2025 | independent | $30.00\nB | pricing page | rhine | 24 Oct 2025 | independent | $40.00\nC | shop window card | rhine | 30 Oct 2025 | independent | $30.00\nD | mobile screen | rhine | 6 Jul 2025 | independent | $40.00\nE | sandwich board | rhine | 30 Oct 2025 | independent | $30.00\n\nClaim to check: the season registration fee is $30.00.",
  "question": "Does the claim to check match the value that the stated rules settle on from the listed sources?",
  "definitions": "How to settle the season registration fee from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the season registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qc633aea094",
  "kind": "yes/no",
  "text": "Andreas Kallas: Hello, I have been reading up on the account opening fee at Corrie Hall Institute and the notes are in hand.\nsupport: That is fine, take it steady.\ndesk: The material below is set out for you.\n\nExcerpts on the account opening fee:\n[S-77] comment thread, tier hail, dated Sunday, 4 January 2026, copied from S-76: \"The account opening fee is $30.00.\"\n[S-91] answerphone greeting, tier sleet, dated Thursday, 25 September 2025, independent: \"The account opening fee is $25.00.\"\n[S-76] record card, tier sleet, dated Wednesday, 24 September 2025, independent: \"The account opening fee is $30.00.\"\n\nClaim to check: the account opening fee is $25.00.",
  "question": "Under the stated rules, is the claim to check for the account opening fee equal in value to what the rules settle on from the listed sources?",
  "definitions": "How to settle the account opening fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the account opening fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qe39b2fb589",
  "kind": "choice",
  "text": "Memo for the team from Farhan Qureshi, a parent sorting out arrangements and stretched thin. The writer wants the shoe hire charge at Bramwell Market and the extract is pasted in for reference. Please pass this on with the usual papers. Thanks for picking it up.\n\nSources on the shoe hire charge:\n- Source S-15: instant message; tier cedar; dated April 30, 2025; independent. It states the shoe hire charge is 4.00 USD.\n- Source S-72: car park sign; tier birch; dated April 30, 2026; independent. It states the shoe hire charge is 8.00 USD.\n- Source S-44: call centre script; tier cedar; dated May 1, 2026; independent. It states the shoe hire charge is 5.00 USD.\n- Source S-96: news article; tier cedar; dated April 30, 2026; independent. It states the shoe hire charge is 4.00 USD.",
  "question": "How to settle the shoe hire charge from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the shoe hire charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nLooking at the listed sources, which value does the fact settle on under the stated rules?",
  "options": [
   "5.00 USD",
   "8.00 USD",
   "4.00 USD"
  ]
 },
 {
  "qid": "qb43edefd2c",
  "kind": "choice",
  "text": "Title: Booking query on the electronics drop-off deadline at Rookery Commons\nRequester: Dina Saleh\nTeam: bookings\nPasted material is set out below.\n\nExcerpts on the electronics drop-off deadline:\n[A] hanging banner, tier spring, dated 28 Aug 2025, independent: \"The electronics drop-off deadline is 10 Sep 2026.\"\n[B] loudspeaker message, tier spring, dated 28 Aug 2024, independent: \"The electronics drop-off deadline is 23 Dec 2026.\"\n[C] database printout, tier spring, dated 16 Sep 2025, copied from D: \"The electronics drop-off deadline is 15 May 2027.\"\n[D] megaphone call, tier autumn, dated 28 Aug 2024, independent: \"The electronics drop-off deadline is 15 May 2027.\"",
  "question": "How to settle the electronics drop-off deadline from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the electronics drop-off deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, what value of the fact comes out as the settled answer?",
  "options": [
   "23 Dec 2026",
   "15 May 2027",
   "10 Sep 2026"
  ]
 },
 {
  "qid": "qdda788ac55",
  "kind": "choice",
  "text": "title: query on the term start date at Meadowbank Dental Practice\nrequester: Thandiwe Morrow\nteam: support\nPasted notes sit underneath this line.\n\nExcerpts on the term start date:\n[S-72] comment thread, tier harp, dated 2025-06-19, independent: \"The term start date is 2026-11-08.\"\n[S-89] spoken reminder, tier harp, dated 2025-06-19, independent: \"The term start date is 2026-12-26.\"\n[S-12] activity log, tier harp, dated 2025-06-20, copied from S-89: \"The term start date is 2026-12-26.\"",
  "question": "How to settle the term start date from the listed sources:\n- Tiers, most reliable first: harp; then lute; then viola.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the term start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value of the term start date is settled by the listed sources under the stated rules?",
  "options": [
   "2026-12-26",
   "2026-11-08",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q9111ca9462",
  "kind": "choice",
  "text": "Requester: Omar Nasser\nTopic: the document request deadline at Hawthorne Walk-In Clinic\nContext: sorting out a booking\nI have pasted what was found below so the team can see it.\n\nSources on the document request deadline:\n- Source S-40: programme; tier clove; dated 7 Sep 2025; independent. It states the document request deadline is 4 Feb 2027.\n- Source S-28: on-hold recording; tier clove; dated 8 Sep 2025; independent. It states the document request deadline is 26 Sep 2026.\n- Source S-85: flyer; tier clove; dated 7 Sep 2025; independent. It states the document request deadline is 26 Sep 2026.",
  "question": "How to settle the document request deadline from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the document request deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which value of the fact is settled under the stated rules?",
  "options": [
   "26 Sep 2026",
   "Not determinable from reliable sources",
   "4 Feb 2027"
  ]
 },
 {
  "qid": "q169af6804e",
  "kind": "yes/no",
  "text": "Front desk memo: Minjun Park is putting together a reply on the account opening fee at Quayside Lettings Office, and the gathered material is pasted below. Give it a quick read, it is laid out clearly.\n\nExcerpts on the account opening fee:\n[S-41] instruction card, tier sleet, dated Tuesday, 22 April 2025, independent: \"The account opening fee is 15.00 USD.\"\n[S-58] voice message, tier fog, dated Monday, 14 July 2025, copied from S-24: \"The account opening fee is 25.00 USD.\"\n[S-24] annual report, tier hail, dated Monday, 14 July 2025, independent: \"The account opening fee is 25.00 USD.\"\n[S-38] price list, tier sleet, dated Tuesday, 22 April 2025, independent: \"The account opening fee is 15.00 USD.\"\n\nClaim to check: the account opening fee is 25.00 USD.",
  "question": "Under the stated rules, is the claim to check for the account opening fee in agreement with the value the listed sources settle on?",
  "definitions": "How to settle the account opening fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the account opening fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q901df45847",
  "kind": "yes/no",
  "text": "Help centre entry: Andreas Kallas is in a bit of a hurry over the league start date at Cresswell Rail Company, so the notes gathered below are on hand. Quick reference, plain and simple.\n\nExcerpts on the league start date:\n[A] information sheet, tier jupiter, dated 2025-12-29, independent: \"The league start date is 2026-09-14.\"\n[B] brochure, tier jupiter, dated 2025-09-07, independent: \"The league start date is 2026-12-15.\"\n[C] recorded message, tier jupiter, dated 2025-12-29, copied from B: \"The league start date is 2026-12-15.\"\n\nClaim to check: the league start date is 2026-12-15.",
  "question": "Is the value given in the claim to check the same as the stated rules settle on from the listed sources?",
  "definitions": "How to settle the league start date from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the league start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qb9de0145ca",
  "kind": "yes/no",
  "text": "requested_by: Camila Restrepo\norganisation: Saltmarsh Exchange\ntopic: the late return fee\nteam: support\nnote: reply in progress, material pasted below\n\nSource table for the late return fee:\nsource | name | tier | dated | origin | stated value\nS-49 | feed item | robin | Wednesday, December 3, 2025 | independent | 25.00 USD\nS-99 | forum reply | finch | Wednesday, December 3, 2025 | independent | 25.00 USD\nS-87 | feed headline | finch | Thursday, December 4, 2025 | independent | 8.00 USD\nS-57 | door sign | finch | Thursday, December 4, 2025 | independent | 8.00 USD\n\nClaim to check: the late return fee is 8.00 USD.",
  "question": "According to the rules given, does the claim to check give the same value for the late return fee as the listed sources settle?",
  "definitions": "How to settle the late return fee from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the late return fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qf2d47f988d",
  "kind": "yes/no",
  "text": "Requester: Andreas Kallas\nTopic: the padlock price at Crestline Climbing Gym\nStage: preparing a reply\nI have pasted what was found below for the team to read.\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | flyer | hail | 25 May 2026 | independent | 25.00 USD\nB | desk diary | sleet | 25 May 2026 | independent | 10.00 USD\nC | fee schedule | sleet | 24 May 2026 | independent | 10.00 USD\nD | postcard | sleet | 18 May 2026 | independent | 10.00 USD\nE | telephone menu | hail | 25 May 2026 | independent | 25.00 USD\n\nClaim to check: the padlock price is 10.00 USD.",
  "question": "Does the claim to check line up with the value the listed sources settle on under the stated rules?",
  "definitions": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q1666ff9ddf",
  "kind": "choice",
  "text": "Arjun Sethi: Hiya, I'm tidying the records and looking into the shoe hire charge at Stonechat Park. I've pasted what was found below, nice and neat.\nteammate: Brilliant, thanks for tidying that up.\nteammate: Let's get it all filed.\n\nSources on the shoe hire charge:\n- Source S-47: forum thread; tier birch; dated Friday, August 29, 2025; copied from Source S-85. It states the shoe hire charge is 3.50 USD.\n- Source S-90: door sign; tier birch; dated Thursday, August 28, 2025; independent. It states the shoe hire charge is 5.00 USD.\n- Source S-33: filing cabinet folder; tier birch; dated Wednesday, August 27, 2025; independent. It states the shoe hire charge is 5.00 USD.\n- Source S-12: news article; tier cedar; dated Friday, September 12, 2025; independent. It states the shoe hire charge is 5.00 USD.\n- Source S-85: postcard; tier cedar; dated Thursday, August 28, 2025; independent. It states the shoe hire charge is 3.50 USD.",
  "question": "How to settle the shoe hire charge from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the shoe hire charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which source do the stated rules draw the value from?",
  "options": [
   "Source S-33",
   "Source S-47",
   "Source S-90"
  ]
 },
 {
  "qid": "q3a00ae463e",
  "kind": "choice",
  "text": "Front desk memo: Arjun Sethi is putting a reply together, and it has been a fun bit of digging into the rural route price at Marrowdown Arts Festival. The pasted material below sits in a tidy pile.\n\nSources on the rural route price:\n- Source A: filing cabinet folder; tier wynn; dated 4 November 2025; copied from Source E. It states the rural route price is $5.00.\n- Source B: appointment card; tier thorn; dated 5 November 2025; copied from Source E. It states the rural route price is $5.00.\n- Source C: poster; tier wynn; dated 1 November 2025; independent. It states the rural route price is $2.00.\n- Source D: text message; tier wynn; dated 1 November 2025; independent. It states the rural route price is $2.00.\n- Source E: system log; tier yogh; dated 4 November 2025; independent. It states the rural route price is $5.00.",
  "question": "How to settle the rural route price from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the rural route price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, what value for the rural route price is settled by the listed sources?",
  "options": [
   "Not determinable from reliable sources",
   "$2.00",
   "$5.00"
  ]
 },
 {
  "qid": "qe7f98d4fd9",
  "kind": "yes/no",
  "text": "title: enquiry about the membership fee at Ridgeway Swim Club\nrequester: Andreas Kallas\nteam: front desk\nNotes gathered for this enquiry are pasted below.\n\nSource table for the membership fee:\nsource | name | tier | dated | origin | stated value\nS-71 | cover note | yogh | Sunday, 5 April 2026 | independent | $25.00\nS-32 | tooltip | yogh | Sunday, 14 June 2026 | copied from S-81 | $75.00\nS-83 | portal page | thorn | Sunday, 12 April 2026 | copied from S-71 | $25.00\nS-81 | appointment card | yogh | Thursday, 19 March 2026 | independent | $75.00\n\nClaim to check: the membership fee is $25.00.",
  "question": "Under the stated rules, does the claim to check give the same value for the membership fee that the listed sources settle on?",
  "definitions": "How to settle the membership fee from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the membership fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q746ecec5be",
  "kind": "choice",
  "text": "Valentina Ochoa: Need to check the registration fee at Millrace Credit Union, I am juggling a busy list at the moment.\ncolleague: Send the extract over and I will look at it with you.\ncolleague: Happy to help you work through it.\n\nSources on the registration fee:\n- Source A: voice message; tier fog; dated April 26, 2026; independent. It states the registration fee is 350.00 USD.\n- Source B: letter; tier sleet; dated June 7, 2026; copied from Source C. It states the registration fee is 180.00 USD.\n- Source C: spoken bulletin; tier fog; dated June 7, 2026; independent. It states the registration fee is 180.00 USD.\n- Source D: megaphone call; tier sleet; dated June 8, 2026; independent. It states the registration fee is 180.00 USD.",
  "question": "How to settle the registration fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich listed source do the stated rules take the value of this fact from?",
  "options": [
   "Source A",
   "Source C",
   "No source: not determinable from reliable sources",
   "Source D"
  ]
 }
]
