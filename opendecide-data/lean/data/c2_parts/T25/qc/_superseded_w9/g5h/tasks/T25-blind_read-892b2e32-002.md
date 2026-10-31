# G5-H blind read T25-blind_read-892b2e32-002 (family T25)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T25/qc/g5h/answers/T25-blind_read-892b2e32-002.json

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
  "qid": "q65ac553ba0",
  "kind": "choice",
  "text": "Help centre entry: Elena Marchetti went through the young driver fee at Garrow Cab Company in a calm, routine way, using the material gathered below. The steps are set out in order, and the pasted details follow straight after.\n\nSources on the young driver fee:\n- Source S-35: programme; tier sleet; dated 2025-12-30; independent. It states the young driver fee is 35.00 USD.\n- Source S-62: social post; tier fog; dated 2025-12-31; independent. It states the young driver fee is 20.00 USD.\n- Source S-27: station announcement; tier fog; dated 2025-12-31; independent. It states the young driver fee is 15.00 USD.\n- Source S-34: spoken reminder; tier fog; dated 2026-01-01; copied from Source S-35. It states the young driver fee is 35.00 USD.",
  "question": "How to settle the young driver fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the young driver fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value do the listed sources settle on for the fact, according to the stated rules?",
  "options": [
   "15.00 USD",
   "20.00 USD",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q92d056552b",
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
  "qid": "q99a32c9c51",
  "kind": "choice",
  "text": "teammate: Tidy up the damage deposit at Corrie Hall Institute before the desk starts, please.\nWei Zhang: Got it. Pulling the material below together, quick as possible.\nsupport: Thanks. Drop it in the thread.\n\nSources on the damage deposit:\n- Source A: questions page; tier finch; dated May 17, 2025; copied from Source E. It states the damage deposit is $200.00.\n- Source B: loudspeaker message; tier finch; dated May 18, 2025; independent. It states the damage deposit is $400.00.\n- Source C: receipt slip; tier finch; dated May 17, 2025; independent. It states the damage deposit is $200.00.\n- Source D: photo caption; tier finch; dated May 18, 2025; independent. It states the damage deposit is $250.00.\n- Source E: station announcement; tier finch; dated May 17, 2025; independent. It states the damage deposit is $200.00.",
  "question": "How to settle the damage deposit from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the damage deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, at which value do the listed sources settle the damage deposit?",
  "options": [
   "$400.00",
   "$250.00",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q714caaac2b",
  "kind": "yes/no",
  "text": "Subject: quick check for the reply\nHi,\nArjun Sethi wants to know the electronics drop-off deadline at Fennel Hollow Gardens and has the notes ready. The material pasted below is what came in. Let me know once you have read it.\nThanks,\n\nExcerpts on the electronics drop-off deadline:\n[A] station announcement, tier winter, dated 5 Mar 2026, independent: \"The electronics drop-off deadline is 15 Jan 2027.\"\n[B] shop window card, tier winter, dated 10 May 2026, copied from C: \"The electronics drop-off deadline is 26 Oct 2026.\"\n[C] conference call, tier spring, dated 10 May 2026, independent: \"The electronics drop-off deadline is 26 Oct 2026.\"\n[D] tooltip, tier spring, dated 11 May 2026, copied from A: \"The electronics drop-off deadline is 15 Jan 2027.\"\n\nClaim to check: the electronics drop-off deadline is 15 Jan 2027.",
  "question": "Does the claim to check for the electronics drop-off deadline give the same value that the listed sources yield under the stated rules?",
  "definitions": "How to settle the electronics drop-off deadline from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the electronics drop-off deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qba02c1b3f2",
  "kind": "yes/no",
  "text": "title | support look at the late return fee at Brightmoor College of Crafts\nrequester | Tomasz Kowalczyk\nteam | help-desk\nNotes for the handover are gathered below.\n\nSources on the late return fee:\n- Source S-81: photo caption; tier robin; dated Friday, 20 March 2026; independent. It states the late return fee is $30.00.\n- Source S-13: appointment card; tier sparrow; dated Saturday, 21 March 2026; independent. It states the late return fee is $25.00.\n- Source S-46: spoken bulletin; tier robin; dated Friday, 20 March 2026; independent. It states the late return fee is $30.00.\n- Source S-92: price list; tier finch; dated Saturday, 21 March 2026; independent. It states the late return fee is $30.00.\n\nClaim to check: the late return fee is $25.00.",
  "question": "Applying the stated rules to these sources, does the claim to check match the figure they settle on?",
  "definitions": "How to settle the late return fee from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the late return fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qcee705cbc1",
  "kind": "choice",
  "text": "Help centre entry: Mateo Quiroga looked into the late return fee at Harrowden Upholstery Services at speed, reading through the pasted material below. The desk team picks up from there.\n\nSources on the late return fee:\n- Source S-66: on-hold recording; tier sparrow; dated 19 March 2026; independent. It states the late return fee is $12.00.\n- Source S-89: database printout; tier sparrow; dated 20 March 2026; independent. It states the late return fee is $5.00.\n- Source S-13: social post; tier robin; dated 20 March 2026; copied from Source S-98. It states the late return fee is $30.00.\n- Source S-98: email message; tier finch; dated 20 March 2026; independent. It states the late return fee is $30.00.",
  "question": "How to settle the late return fee from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the late return fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich of the listed sources do the stated rules rely on for the value of this fact?",
  "options": [
   "No source: not determinable from reliable sources",
   "Source S-98",
   "Source S-89",
   "Source S-13"
  ]
 },
 {
  "qid": "qc76f7f9fa2",
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
  "qid": "q195aeceee5",
  "kind": "yes/no",
  "text": "Title | Reply prep for the document request deadline at Hadley Bike Works\nRequester | Mei Huang\nTeam | customer care\nMaterial for the reply is pasted below.\n\nExcerpts on the document request deadline:\n[S-14] telephone menu, tier sumac, dated 12 Mar 2025, independent: \"The document request deadline is 26 Apr 2027.\"\n[S-21] voice message, tier sumac, dated 12 Mar 2025, independent: \"The document request deadline is 26 Apr 2027.\"\n[S-22] comment thread, tier clove, dated 15 May 2025, independent: \"The document request deadline is 2 Mar 2026.\"\n\nClaim to check: the document request deadline is 26 Apr 2027.",
  "question": "Is the claim to check wrong if the stated rules are applied to the listed sources?",
  "definitions": "How to settle the document request deadline from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the document request deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q6607ca24e9",
  "kind": "yes/no",
  "text": "title | preparing a reply on the custom cake deposit at Hallam Chess Club\nrequester | Radu Calin\nteam | desk\nThe material gathered below is ready for the reply.\n\nSources on the custom cake deposit:\n- Source A: envelope insert; tier winter; dated 15 May 2025; independent. It states the custom cake deposit is $30.00.\n- Source B: instant message; tier autumn; dated 14 May 2025; independent. It states the custom cake deposit is $75.00.\n- Source C: programme; tier autumn; dated 13 May 2025; independent. It states the custom cake deposit is $30.00.\n- Source D: case file; tier autumn; dated 14 May 2025; independent. It states the custom cake deposit is $75.00.\n- Source E: photo caption; tier autumn; dated 13 May 2025; independent. It states the custom cake deposit is $40.00.\n\nClaim to check: the custom cake deposit is $75.00.",
  "question": "Going by the listed sources, is the claim to check consistent with the value the stated rules settle on?",
  "definitions": "How to settle the custom cake deposit from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the custom cake deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q2a3be47b87",
  "kind": "choice",
  "text": "Help centre entry: Thandiwe Morrow, who leads the team, is tidying records and has looked into the plant sale date at Larchwood Park along the way. Helpful notes sit below, which is a nice bonus for the file.\n\nExcerpts on the plant sale date:\n[S-63] sandwich board, tier ganges, dated 28 February 2025, independent: \"The plant sale date is 27 May 2026.\"\n[S-62] brochure, tier tigris, dated 8 February 2025, independent: \"The plant sale date is 17 May 2027.\"\n[S-70] guide booklet, tier ganges, dated 20 March 2025, copied from S-62: \"The plant sale date is 17 May 2027.\"",
  "question": "How to settle the plant sale date from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the plant sale date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, what value of the fact comes out as the settled answer?",
  "options": [
   "27 May 2026",
   "17 May 2027",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q583bfcfc6f",
  "kind": "yes/no",
  "text": "Front desk memo: Mateo Quiroga is planning a visit and wants the season registration fee at Ormsby Mart pinned down. The gathered material sits pasted below for reference.\n\nSource table for the season registration fee:\nsource | name | tier | dated | origin | stated value\nA | guide booklet | ganges | 14 June 2025 | copied from B | $60.00\nB | blog entry | tigris | 7 June 2025 | independent | $60.00\nC | loudspeaker message | tigris | 8 June 2025 | independent | $80.00\nD | settings screen | rhine | 9 June 2025 | independent | $60.00\nE | spoken reminder | rhine | 15 August 2025 | independent | $75.00\n\nClaim to check: the season registration fee is $75.00.",
  "question": "Under the stated rules, does the claim to check for the season registration fee not give the value the listed sources settle on?",
  "definitions": "How to settle the season registration fee from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the season registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q3475b87efb",
  "kind": "choice",
  "text": "Dear colleague,\nMy name is Elena Marchetti and I am writing to look into the registration fee at Quarry Lane Debating Society. I have pasted what was found below for your reference. Thank you for your help on this matter.\nKind regards,\n\nSources on the registration fee:\n- Source A: appointment card; tier hail; dated 6 Feb 2026; independent. It states the registration fee is 350.00 USD.\n- Source B: guide booklet; tier fog; dated 1 Apr 2026; copied from Source A. It states the registration fee is 350.00 USD.\n- Source C: filing cabinet folder; tier sleet; dated 6 Feb 2026; copied from Source A. It states the registration fee is 350.00 USD.\n- Source D: price list; tier sleet; dated 30 Jan 2025; independent. It states the registration fee is 300.00 USD.\n- Source E: landing page; tier sleet; dated 6 Feb 2025; independent. It states the registration fee is 300.00 USD.",
  "question": "How to settle the registration fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, what value comes out as the settled answer for the fact?",
  "options": [
   "Not determinable from reliable sources",
   "350.00 USD",
   "300.00 USD"
  ]
 },
 {
  "qid": "qc7dace5a83",
  "kind": "yes/no",
  "text": "{\"requested_by\": \"Kofi Mensah\", \"organisation\": \"Brookhollow Folk Club\", \"topic\": \"damage deposit\", \"asked_via\": \"pasted material below\"}\n\nSources on the damage deposit:\n- Source A: video caption; tier finch; dated 28 Oct 2025; independent. It states the damage deposit is $300.00.\n- Source B: guide booklet; tier robin; dated 29 Oct 2025; independent. It states the damage deposit is $250.00.\n- Source C: entrance sign; tier robin; dated 16 Dec 2025; copied from Source A. It states the damage deposit is $300.00.\n\nClaim to check: the damage deposit is $300.00.",
  "question": "According to the rules given, does the claim to check for the damage deposit state the same value the rules settle on from the listed sources?",
  "definitions": "How to settle the damage deposit from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the damage deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qb5feab7e7c",
  "kind": "choice",
  "text": "Team memo: Joaquin Lozano leads the team and is a bit pressed about the document request deadline at Linnet Savings Club. The material gathered below is pasted in, ready to look over.\n\nExcerpts on the document request deadline:\n[S-45] wall calendar, tier sumac, dated 2026-04-22, independent: \"The document request deadline is 2026-01-10.\"\n[S-91] desk handout, tier cumin, dated 2025-04-22, copied from S-33: \"The document request deadline is 2026-09-13.\"\n[S-33] settings screen, tier sumac, dated 2025-04-22, independent: \"The document request deadline is 2026-09-13.\"\n[S-44] catalogue, tier sumac, dated 2026-04-22, independent: \"The document request deadline is 2026-01-10.\"",
  "question": "How to settle the document request deadline from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the document request deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nTaking the stated rules and the listed sources together, what value is the fact settled at?",
  "options": [
   "Not determinable from reliable sources",
   "2026-09-13",
   "2026-01-10"
  ]
 },
 {
  "qid": "qe0ca6591e9",
  "kind": "yes/no",
  "text": "Subject | the damage deposit at Garrow Cab Company\nRaised by | Tariq Mansour\nTeam | member desk\nPasted material sits below.\n\nSources on the damage deposit:\n- Source A: postcard; tier sparrow; dated Friday, May 9, 2025; copied from Source C. It states the damage deposit is $300.00.\n- Source B: inbox note; tier finch; dated Saturday, May 3, 2025; independent. It states the damage deposit is $350.00.\n- Source C: profile post; tier finch; dated Friday, May 9, 2025; independent. It states the damage deposit is $300.00.\n- Source D: filing cabinet folder; tier sparrow; dated Friday, May 9, 2025; copied from Source C. It states the damage deposit is $300.00.\n- Source E: entrance sign; tier sparrow; dated Friday, May 2, 2025; independent. It states the damage deposit is $350.00.\n\nClaim to check: the damage deposit is $300.00.",
  "question": "Applying the stated rules to these sources, does the claim to check hold the same value they settle on?",
  "definitions": "How to settle the damage deposit from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the damage deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qe4711facf0",
  "kind": "yes/no",
  "text": "Help centre entry: Busy desk, so Yuki Hayashi looked into the shoe hire charge at Stonechat Park straight away and pasted the material below. A reply is being put together.\n\nSources on the shoe hire charge:\n- Source S-64: feed headline; tier birch; dated Saturday, 3 January 2026; copied from Source S-28. It states the shoe hire charge is $5.00.\n- Source S-89: settings screen; tier birch; dated Friday, 31 October 2025; independent. It states the shoe hire charge is $4.50.\n- Source S-28: appointment card; tier birch; dated Friday, 7 November 2025; independent. It states the shoe hire charge is $5.00.\n\nClaim to check: the shoe hire charge is $5.00.",
  "question": "Applying the stated rules to these sources, does the claim to check state the same value the rules settle on?",
  "definitions": "How to settle the shoe hire charge from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the shoe hire charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q6b4346ce4f",
  "kind": "yes/no",
  "text": "Tomasz Kowalczyk: Need to check the camera hire price at Linnet Savings Club, I am juggling a busy list at the moment.\ncolleague: Send the extract over and I will look at it with you.\ncolleague: Happy to help you work through it.\n\nSources on the camera hire price:\n- Source S-65: photo caption; tier topaz; dated Sunday, June 1, 2025; copied from Source S-98. It states the camera hire price is $25.00.\n- Source S-98: reference card; tier garnet; dated Sunday, June 1, 2025; independent. It states the camera hire price is $25.00.\n- Source S-66: board notice; tier topaz; dated Friday, May 30, 2025; independent. It states the camera hire price is $25.00.\n- Source S-49: instruction card; tier opal; dated Monday, June 2, 2025; copied from Source S-98. It states the camera hire price is $25.00.\n- Source S-44: system log; tier topaz; dated Saturday, May 31, 2025; independent. It states the camera hire price is $60.00.\n\nClaim to check: the camera hire price is $25.00.",
  "question": "Under the stated rules, does the claim to check for the camera hire price not give the value the listed sources settle on?",
  "definitions": "How to settle the camera hire price from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the camera hire price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q93038cd91d",
  "kind": "choice",
  "text": "{\"requested_by\": \"Declan Murphy\", \"organisation\": \"Starling Cinema\", \"topic\": \"the parking charge\", \"asked_via\": \"front desk\"}\n\nSources on the parking charge:\n- Source S-10: record card; tier ganges; dated 21 February 2025; independent. It states the parking charge is $10.00.\n- Source S-28: printed notice; tier ganges; dated 21 February 2025; independent. It states the parking charge is $10.00.\n- Source S-37: system log; tier ganges; dated 21 February 2025; independent. It states the parking charge is $12.00.\n- Source S-46: settings screen; tier tigris; dated 21 February 2025; independent. It states the parking charge is $12.00.\n- Source S-20: door sign; tier ganges; dated 22 February 2025; independent. It states the parking charge is $6.00.",
  "question": "How to settle the parking charge from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the parking charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which listed source does the settled value come from?",
  "options": [
   "Source S-10",
   "No source: not determinable from reliable sources",
   "Source S-20",
   "Source S-46"
  ]
 },
 {
  "qid": "q882e581f95",
  "kind": "yes/no",
  "text": "{\"requested_by\": \"Mateo Quiroga\", \"organisation\": \"Carrickmoor Sketch Club\", \"topic\": \"padlock price\", \"asked_via\": \"pasted material below\"}\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | comment thread | fog | 12 December 2025 | copied from C | $15.00\nB | footer text | sleet | 10 December 2025 | independent | $10.00\nC | account page | hail | 12 December 2025 | independent | $15.00\nD | door sign | sleet | 11 December 2026 | copied from C | $15.00\nE | car park sign | sleet | 11 December 2025 | independent | $10.00\n\nClaim to check: the padlock price is $10.00.",
  "question": "Under the stated rules, is the claim to check for the padlock price in agreement with the value the listed sources settle on?",
  "definitions": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qb8b8e8a069",
  "kind": "yes/no",
  "text": "Sigrid Lund: Hello there, looking at the electronics drop-off deadline at Harbourside Ferry Lines for a reply.\nclerk: Sounds fine.\nclerk: The pasted material below is ready when you are.\n\nExcerpts on the electronics drop-off deadline:\n[A] forum reply, tier spring, dated 2026-11-10, copied from B: \"The electronics drop-off deadline is 2026-05-11.\"\n[B] annual report, tier autumn, dated 2026-01-13, independent: \"The electronics drop-off deadline is 2026-05-11.\"\n[C] profile post, tier spring, dated 2025-11-10, independent: \"The electronics drop-off deadline is 2026-05-21.\"\n[D] email message, tier spring, dated 2025-11-11, independent: \"The electronics drop-off deadline is 2026-05-11.\"\n\nClaim to check: the electronics drop-off deadline is 2026-05-21.",
  "question": "According to the rules given, does the claim to check for the electronics drop-off deadline state the same value the rules settle on from the listed sources?",
  "definitions": "How to settle the electronics drop-off deadline from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the electronics drop-off deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qaca98e9a6c",
  "kind": "yes/no",
  "text": "Subject: Quick check on the camera hire price at Saltmarsh Exchange\nHi there,\nAbena Boateng is sorting out a booking and is in a bit of a hurry, so the notes below are pulled together for you. Sorry to hurry you on it.\nThanks,\n\nSources on the camera hire price:\n- Source S-98: window notice; tier topaz; dated Wednesday, 16 July 2025; independent. It states the camera hire price is $40.00.\n- Source S-68: station announcement; tier topaz; dated Wednesday, 16 July 2025; independent. It states the camera hire price is $20.00.\n- Source S-48: printed notice; tier garnet; dated Friday, 18 July 2025; independent. It states the camera hire price is $15.00.\n- Source S-18: profile post; tier topaz; dated Thursday, 17 July 2025; independent. It states the camera hire price is $15.00.\n\nClaim to check: the camera hire price is $40.00.",
  "question": "Going by the listed sources, does the claim to check agree with the value the stated rules settle on?",
  "definitions": "How to settle the camera hire price from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the camera hire price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qc33c75e34a",
  "kind": "yes/no",
  "text": "Dina Saleh: Bit of a hurry at the front desk about the document request deadline at Pellham Coding Academy.\ndesk: Pulling the pasted material up for you.\n\nExcerpts on the document request deadline:\n[S-36] record card, tier sumac, dated 21 May 2025, independent: \"The document request deadline is 13 Aug 2026.\"\n[S-85] shop window card, tier cumin, dated 21 May 2025, copied from S-80: \"The document request deadline is 11 Jan 2027.\"\n[S-80] envelope insert, tier clove, dated 21 May 2025, independent: \"The document request deadline is 11 Jan 2027.\"\n\nClaim to check: the document request deadline is 13 Aug 2026.",
  "question": "Under the stated rules, does the claim to check not match the figure for the document request deadline settled by these sources?",
  "definitions": "How to settle the document request deadline from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the document request deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q40a6e97def",
  "kind": "choice",
  "text": "Subject: Gentle follow on about the padlock price at Marrowdown Arts Festival\nHello there,\nAdaeze Nwosu is writing in with a calm, easy request and has the material gathered below. Take your time with it.\nWarm regards,\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | letter | fog | Wednesday, July 23, 2025 | copied from C | $12.00\nB | catalogue | fog | Wednesday, July 23, 2025 | independent | $25.00\nC | footer text | fog | Tuesday, July 22, 2025 | independent | $12.00\nD | door sign | fog | Sunday, June 22, 2025 | independent | $10.00\nE | megaphone call | fog | Wednesday, July 23, 2025 | independent | $10.00",
  "question": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, what value of the padlock price comes out from the listed sources?",
  "options": [
   "$25.00",
   "$10.00",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q7bc65e9633",
  "kind": "choice",
  "text": "Idris Varga: Reaching out about the term start date at Oakhaven Residents Association, with notes sitting below.\nsupport: Thank you for getting in touch, the message is logged.\ndesk: Pasted notes below are ready to be read.\n\nExcerpts on the term start date:\n[S-31] reference card, tier harp, dated Friday, 12 December 2025, copied from S-85: \"The term start date is Saturday, 17 October 2026.\"\n[S-85] shop window card, tier lute, dated Friday, 12 December 2025, independent: \"The term start date is Saturday, 17 October 2026.\"\n[S-82] station announcement, tier lute, dated Saturday, 13 December 2025, independent: \"The term start date is Friday, 24 July 2026.\"",
  "question": "How to settle the term start date from the listed sources:\n- Tiers, most reliable first: harp; then lute; then viola.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the term start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value of the term start date is settled by the listed sources under the stated rules?",
  "options": [
   "Saturday, 17 October 2026",
   "Friday, 24 July 2026",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q711a714c9c",
  "kind": "choice",
  "text": "Rhys Gwilym: Quick ask at the front desk about the desk rental fee at Oakhaven Residents Association, with the gathered material pasted below.\nsupport: Got it, stand by.\ndesk: Happy to help.\n\nSources on the desk rental fee:\n- Source A: desk handout; tier topaz; dated January 29, 2025; independent. It states the desk rental fee is 300.00 USD.\n- Source B: pamphlet; tier topaz; dated February 5, 2026; copied from Source E. It states the desk rental fee is 180.00 USD.\n- Source C: counter sign; tier topaz; dated January 29, 2026; independent. It states the desk rental fee is 350.00 USD.\n- Source D: instruction card; tier garnet; dated January 29, 2026; independent. It states the desk rental fee is 150.00 USD.\n- Source E: entrance sign; tier garnet; dated February 5, 2026; independent. It states the desk rental fee is 180.00 USD.",
  "question": "How to settle the desk rental fee from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the desk rental fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which value of the fact do the stated rules settle on?",
  "options": [
   "Not determinable from reliable sources",
   "350.00 USD",
   "300.00 USD"
  ]
 },
 {
  "qid": "q1a4f7f5fe2",
  "kind": "yes/no",
  "text": "Subject: Lookup on the consultation fee\nHi team,\nYaw Ofori is on the staff and is busy getting to grips with Quarry Lane Debating Society. The pasted material below is there for a quick read.\nThanks,\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-66 | landing page | uranus | 17 April 2026 | independent | $45.00\nS-53 | tooltip | uranus | 17 April 2026 | independent | $45.00\nS-58 | activity log | pluto | 17 April 2027 | independent | $75.00\nS-12 | sandwich board | uranus | 28 March 2026 | independent | $35.00\nS-36 | news article | pluto | 23 February 2026 | independent | $45.00\n\nClaim to check: the consultation fee is $75.00.",
  "question": "Does the claim to check for the consultation fee give the same value that the listed sources yield under the stated rules?",
  "definitions": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q24265f4c15",
  "kind": "yes/no",
  "text": "Routine desk memo: Minjun Park is a customer who came to the front desk and asked about the document request deadline at Hollowcastle Appliance Service. The pasted material is attached for the team to read.\n\nExcerpts on the document request deadline:\n[S-29] receipt slip, tier sumac, dated 28 Nov 2025, independent: \"The document request deadline is 19 Dec 2026.\"\n[S-61] social post, tier clove, dated 29 Nov 2025, independent: \"The document request deadline is 17 Feb 2027.\"\n[S-85] spoken reminder, tier sumac, dated 28 Nov 2025, independent: \"The document request deadline is 19 Dec 2026.\"\n\nClaim to check: the document request deadline is 19 Dec 2026.",
  "question": "According to the rules given, does the claim to check give the same value for the document request deadline as the listed sources settle?",
  "definitions": "How to settle the document request deadline from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the document request deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q498ebe6df0",
  "kind": "choice",
  "text": "Andreas Kallas: hiya team, been chasing the fitness orientation start date at Millrace Credit Union and got a stack pasted in.\ndesk: nice work, thanks for the lot.\nsupport: that helps the rest of us loads.\n\nExcerpts on the fitness orientation start date:\n[A] counter sign, tier wool, dated March 17, 2024, independent: \"The fitness orientation start date is April 28, 2026.\"\n[B] meeting minutes, tier wool, dated March 16, 2025, independent: \"The fitness orientation start date is April 28, 2026.\"\n[C] postal notice, tier wool, dated March 17, 2025, independent: \"The fitness orientation start date is March 21, 2026.\"\n[D] voice message, tier denim, dated May 2, 2025, independent: \"The fitness orientation start date is July 14, 2026.\"",
  "question": "How to settle the fitness orientation start date from the listed sources:\n- Tiers, most reliable first: wool; then linen; then denim.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the fitness orientation start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhat value of the fact do the stated rules settle on from the listed sources?",
  "options": [
   "April 28, 2026",
   "March 21, 2026",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "qe87bc5ad14",
  "kind": "choice",
  "text": "Office memo: Yasmin Khoury is planning ahead and wants the membership fee at Wickerwood Theatre written down. The material pasted below is set out for that.\n\nSource table for the membership fee:\nsource | name | tier | dated | origin | stated value\nS-51 | postcard | thorn | 24 Oct 2025 | copied from S-91 | $60.00\nS-91 | board notice | yogh | 3 Jul 2025 | independent | $60.00\nS-57 | printed notice | thorn | 3 Jul 2026 | copied from S-91 | $60.00\nS-52 | transaction history | wynn | 26 Apr 2025 | independent | $50.00",
  "question": "How to settle the membership fee from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the membership fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which source do the stated rules draw the value from?",
  "options": [
   "Source S-52",
   "Source S-91",
   "Source S-51"
  ]
 },
 {
  "qid": "q8286577e24",
  "kind": "yes/no",
  "text": "Subject: Follow-up note\nHello,\nHana Watanabe is a support agent who has picked up the request about the entry price at Haldane Travel Express. The material that follows was pasted in as gathered, so it is easy to read alongside the request.\nRegards,\n\nSources on the entry price:\n- Source A: summary sheet; tier cedar; dated 2025-09-08; independent. It states the entry price is 32.00 USD.\n- Source B: pricing page; tier birch; dated 2025-09-14; independent. It states the entry price is 32.00 USD.\n- Source C: board notice; tier cedar; dated 2025-09-15; copied from Source B. It states the entry price is 32.00 USD.\n- Source D: blog entry; tier birch; dated 2025-09-13; independent. It states the entry price is 45.00 USD.\n- Source E: door sign; tier cedar; dated 2025-09-14; independent. It states the entry price is 32.00 USD.\n\nClaim to check: the entry price is 32.00 USD.",
  "question": "Is the value in the claim to check for the entry price the same as the listed sources settle on under the stated rules?",
  "definitions": "How to settle the entry price from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the entry price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q5360b1b675",
  "kind": "yes/no",
  "text": "Elena Marchetti: Passing on the request about the electronics drop-off deadline at Wexcombe Hospice, with the material gathered below.\nsupport: Thank you, that is logged.\ndesk: Pasted material is ready to go.\n\nExcerpts on the electronics drop-off deadline:\n[A] information sheet, tier winter, dated August 13, 2025, independent: \"The electronics drop-off deadline is May 18, 2026.\"\n[B] conference call, tier winter, dated October 21, 2025, independent: \"The electronics drop-off deadline is December 17, 2026.\"\n[C] reply letter, tier winter, dated October 14, 2025, independent: \"The electronics drop-off deadline is September 22, 2026.\"\n\nClaim to check: the electronics drop-off deadline is May 18, 2026.",
  "question": "Under the stated rules, is the claim to check for the electronics drop-off deadline equal in value to what the rules settle on from the listed sources?",
  "definitions": "How to settle the electronics drop-off deadline from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the electronics drop-off deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q889a95cbdd",
  "kind": "yes/no",
  "text": "requested_by: Farid Azizi\nchannel: front desk\norganisation: Brightmoor College of Crafts\ntopic: the race entry fee\nnote: gathered below\n\nSource table for the race entry fee:\nsource | name | tier | dated | origin | stated value\nS-86 | annual report | spring | 18 February 2025 | copied from S-15 | $25.00\nS-72 | counter sign | autumn | 9 February 2025 | independent | $25.00\nS-33 | information sheet | winter | 17 February 2025 | independent | $15.00\nS-15 | inbox note | autumn | 17 February 2025 | independent | $25.00\n\nClaim to check: the race entry fee is $15.00.",
  "question": "Under the stated rules, is the value settled for the race entry fee other than the value the claim to check gives?",
  "definitions": "How to settle the race entry fee from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the race entry fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qd1a2cb659f",
  "kind": "yes/no",
  "text": "title | enquiry on the term start date at Lindenfield Music Hall\nrequester | Arjun Sethi\nteam | support\nThe notes are gathered below.\n\nSource table for the term start date:\nsource | name | tier | dated | origin | stated value\nS-18 | shop window card | lute | Saturday, 15 November 2025 | copied from S-56 | Saturday, 13 March 2027\nS-41 | info pack | lute | Friday, 14 November 2025 | independent | Saturday, 4 July 2026\nS-56 | activity log | viola | Thursday, 13 November 2025 | independent | Saturday, 13 March 2027\nS-69 | answerphone greeting | lute | Friday, 14 November 2025 | independent | Saturday, 4 July 2026\n\nClaim to check: the term start date is Saturday, 13 March 2027.",
  "question": "Under the stated rules, does the claim to check agree with the value these sources settle for the term start date?",
  "definitions": "How to settle the term start date from the listed sources:\n- Tiers, most reliable first: harp; then lute; then viola.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the term start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qb8642a8f0e",
  "kind": "choice",
  "text": "agent: hello, the shoe hire charge at Bramwell Market is a fair thing to look into\nLayla Haddad: brilliant, got the material together and pasted it below\nagent: thanks, the pasted material is a head start\n\nSources on the shoe hire charge:\n- Source S-39: guide booklet; tier cedar; dated May 21, 2026; independent. It states the shoe hire charge is 4.50 USD.\n- Source S-28: forum thread; tier maple; dated May 21, 2025; independent. It states the shoe hire charge is 5.00 USD.\n- Source S-50: appointment card; tier cedar; dated July 2, 2025; independent. It states the shoe hire charge is 4.50 USD.\n- Source S-48: settings screen; tier maple; dated July 2, 2025; copied from Source S-50. It states the shoe hire charge is 4.50 USD.",
  "question": "How to settle the shoe hire charge from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the shoe hire charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value of the fact do the listed sources settle on under the stated rules?",
  "options": [
   "4.50 USD",
   "5.00 USD",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q7bef0260fc",
  "kind": "choice",
  "text": "Records memo: Declan Murphy is tidying the files in a hurry and has the registration fee at Quayside Lettings Office in view. The material pasted below is ready for a quick look.\n\nSources on the registration fee:\n- Source A: answerphone greeting; tier fog; dated Thursday, 7 May 2026; copied from Source D. It states the registration fee is $180.00.\n- Source B: voice message; tier fog; dated Wednesday, 17 June 2026; copied from Source C. It states the registration fee is $350.00.\n- Source C: social post; tier fog; dated Saturday, 4 April 2026; independent. It states the registration fee is $350.00.\n- Source D: sign-in sheet; tier hail; dated Saturday, 26 April 2025; independent. It states the registration fee is $180.00.\n- Source E: spoken reminder; tier fog; dated Sunday, 26 April 2026; independent. It states the registration fee is $275.00.",
  "question": "How to settle the registration fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, which value of the registration fee do the listed sources settle on?",
  "options": [
   "$180.00",
   "$350.00",
   "$275.00"
  ]
 },
 {
  "qid": "q6f6b5d611f",
  "kind": "choice",
  "text": "teammate: The request concerns the camera hire price at Larchwood Park.\nOmar Nasser: Thank you. The material pasted below is set out in order.\nsupport: Appreciated, thank you.\n\nSources on the camera hire price:\n- Source S-46: car park sign; tier garnet; dated July 10, 2025; independent. It states the camera hire price is $15.00.\n- Source S-92: price list; tier opal; dated July 12, 2025; copied from Source S-64. It states the camera hire price is $25.00.\n- Source S-64: instant message; tier garnet; dated July 11, 2025; independent. It states the camera hire price is $25.00.\n- Source S-37: forum thread; tier topaz; dated July 10, 2025; independent. It states the camera hire price is $15.00.",
  "question": "How to settle the camera hire price from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the camera hire price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, which value for the camera hire price is settled from the listed sources?",
  "options": [
   "$25.00",
   "$15.00",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "qc08db910e0",
  "kind": "choice",
  "text": "Ticket: look-up of the parking charge at Hawthorne Walk-In Clinic\nrequester | Ilinca Dobre\nteam | records\nPasted material is below.\n\nSources on the parking charge:\n- Source S-38: answerphone greeting; tier ganges; dated Thursday, 28 May 2026; copied from Source S-58. It states the parking charge is $12.00.\n- Source S-11: sandwich board; tier ganges; dated Thursday, 28 May 2026; copied from Source S-58. It states the parking charge is $12.00.\n- Source S-97: call centre script; tier tigris; dated Thursday, 28 May 2026; independent. It states the parking charge is $10.00.\n- Source S-58: reference card; tier tigris; dated Wednesday, 27 May 2026; independent. It states the parking charge is $12.00.",
  "question": "How to settle the parking charge from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the parking charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value of the fact do the listed sources settle on under the stated rules?",
  "options": [
   "Not determinable from reliable sources",
   "$12.00",
   "$10.00"
  ]
 },
 {
  "qid": "q27bc7c157b",
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
  "qid": "q4cfc29de78",
  "kind": "choice",
  "text": "Mei Huang: Greetings to the team. The entry price at Oakhaven Residents Association is the matter at hand, and the material gathered is pasted in for your review.\ndesk: Thank you for the note, the material is received.\nsupport: Set the material aside for the review.\n\nSources on the entry price:\n- Source A: landing page; tier maple; dated 2025-09-03; independent. It states the entry price is $50.00.\n- Source B: spoken bulletin; tier birch; dated 2025-09-02; independent. It states the entry price is $45.00.\n- Source C: car park sign; tier maple; dated 2025-09-03; independent. It states the entry price is $50.00.\n- Source D: video caption; tier birch; dated 2025-09-01; independent. It states the entry price is $28.00.",
  "question": "How to settle the entry price from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the entry price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, what does the fact come to under the stated rules?",
  "options": [
   "$45.00",
   "$50.00",
   "$28.00"
  ]
 },
 {
  "qid": "q4c567af6fc",
  "kind": "yes/no",
  "text": "Title: sorting out a booking, the membership fee at Hollin Corner Bazaar\nRequester: Sunil Dhawan\nTeam: bookings desk\nThe pasted material below is ready to read.\n\nSource table for the membership fee:\nsource | name | tier | dated | origin | stated value\nS-24 | settings screen | thorn | Saturday, October 18, 2025 | independent | 25.00 USD\nS-47 | conference call | wynn | Wednesday, August 13, 2025 | copied from S-97 | 25.00 USD\nS-84 | postcard | wynn | Thursday, July 31, 2025 | independent | 75.00 USD\nS-88 | answerphone greeting | wynn | Sunday, October 26, 2025 | independent | 75.00 USD\nS-97 | feed headline | yogh | Wednesday, August 6, 2025 | independent | 25.00 USD\n\nClaim to check: the membership fee is 25.00 USD.",
  "question": "Applying the stated rules to these sources, does the claim to check state the same value the rules settle on?",
  "definitions": "How to settle the membership fee from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the membership fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q2749519b1b",
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
  "qid": "q230faf893e",
  "kind": "yes/no",
  "text": "Title: tidying the records\nRequester: Maja Lindqvist\nTeam: records desk\nMaterial on the camera hire price at Quarry Lane Debating Society is pasted below.\n\nSources on the camera hire price:\n- Source S-21: system log; tier garnet; dated 7 February 2025; independent. It states the camera hire price is $30.00.\n- Source S-57: inbox note; tier garnet; dated 6 February 2025; independent. It states the camera hire price is $25.00.\n- Source S-94: pricing page; tier garnet; dated 6 February 2025; independent. It states the camera hire price is $50.00.\n- Source S-78: social post; tier garnet; dated 6 February 2025; copied from Source S-94. It states the camera hire price is $50.00.\n\nClaim to check: the camera hire price is $50.00.",
  "question": "Does the settled value for the camera hire price come out other than the value in the claim to check under the stated rules?",
  "definitions": "How to settle the camera hire price from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the camera hire price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q1c3fdf4459",
  "kind": "choice",
  "text": "Declan Murphy: Quick note, planning a visit and want the parking charge at Starling Cinema pinned down before setting off.\nteammate: Go for it.\nsupport: The gathered material is pasted below.\n\nSources on the parking charge:\n- Source S-10: record card; tier ganges; dated 21 February 2025; independent. It states the parking charge is $10.00.\n- Source S-28: printed notice; tier ganges; dated 21 February 2025; independent. It states the parking charge is $10.00.\n- Source S-37: system log; tier ganges; dated 21 February 2025; independent. It states the parking charge is $12.00.\n- Source S-46: settings screen; tier tigris; dated 21 February 2025; independent. It states the parking charge is $12.00.\n- Source S-20: door sign; tier ganges; dated 22 February 2025; independent. It states the parking charge is $6.00.",
  "question": "How to settle the parking charge from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the parking charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which listed source does the settled value come from?",
  "options": [
   "Source S-10",
   "No source: not determinable from reliable sources",
   "Source S-20",
   "Source S-46"
  ]
 },
 {
  "qid": "q1a2af9bd44",
  "kind": "yes/no",
  "text": "requested_by: Declan Murphy\ntopic: the private lesson price\norganisation: Oldbridge Language School\nasked_via: phone\nnote: booking help\n\nSources on the private lesson price:\n- Source S-67: footer text; tier nickel; dated Tuesday, 15 April 2025; independent. It states the private lesson price is 225.00 USD.\n- Source S-55: desk handout; tier nickel; dated Wednesday, 15 April 2026; copied from Source S-77. It states the private lesson price is 180.00 USD.\n- Source S-77: information sheet; tier copper; dated Wednesday, 15 April 2026; independent. It states the private lesson price is 180.00 USD.\n- Source S-53: tooltip; tier nickel; dated Tuesday, 8 April 2025; independent. It states the private lesson price is 180.00 USD.\n- Source S-26: programme; tier copper; dated Wednesday, 16 April 2025; independent. It states the private lesson price is 250.00 USD.\n\nClaim to check: the private lesson price is 225.00 USD.",
  "question": "Applying the stated rules to these sources, does the claim to check state the same value the rules settle on?",
  "definitions": "How to settle the private lesson price from the listed sources:\n- Tiers, most reliable first: cobalt; then nickel; then copper.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the private lesson price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q557c59fde0",
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
  "qid": "q4282f60f07",
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
  "qid": "qc91dee7362",
  "kind": "yes/no",
  "text": "Help centre entry: Ximena Ferreira looked into the account opening fee at Harbourside Ferry Lines by going through the pasted lines below. The work was squeezed in between calls, piece by piece.\n\nExcerpts on the account opening fee:\n[S-19] loudspeaker message, tier hail, dated Tuesday, 25 November 2025, independent: \"The account opening fee is $50.00.\"\n[S-99] poster, tier fog, dated Monday, 5 January 2026, independent: \"The account opening fee is $10.00.\"\n[S-21] reference card, tier fog, dated Monday, 5 January 2026, independent: \"The account opening fee is $10.00.\"\n\nClaim to check: the account opening fee is $10.00.",
  "question": "Applying the stated rules to these sources, does the claim to check report the value they settle on?",
  "definitions": "How to settle the account opening fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the account opening fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qcd8933afd5",
  "kind": "yes/no",
  "text": "requested_by: Adaeze Nwosu\norganisation: Rookery Commons\ntopic: padlock price\nchannel: counter\nasked_via: in person, lines pasted below\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | instant message | sleet | 7 April 2026 | independent | 8.00 USD\nB | reply letter | fog | 20 December 2025 | copied from D | 20.00 USD\nC | recorded message | fog | 20 December 2025 | independent | 10.00 USD\nD | landing page | hail | 20 December 2025 | independent | 20.00 USD\nE | entrance sign | fog | 20 December 2025 | independent | 10.00 USD\n\nClaim to check: the padlock price is 10.00 USD.",
  "question": "Applying the stated rules to these sources, does the claim to check not agree with the value the rules settle on?",
  "definitions": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q59ec9792f5",
  "kind": "yes/no",
  "text": "Felix Okonjo: Hi there. I'd like to look into the bicycle carriage charge at Garrow Cab Company and I've pasted what was found below.\ndesk: Thank you, I'll take it from here.\nsupervisor: Carry on, and send it back when you've finished.\n\nSources on the bicycle carriage charge:\n- Source A: tooltip; tier ochre; dated March 11, 2027; copied from Source B. It states the bicycle carriage charge is $25.00.\n- Source B: shop window card; tier scarlet; dated March 11, 2026; independent. It states the bicycle carriage charge is $25.00.\n- Source C: receipt slip; tier ochre; dated March 10, 2026; independent. It states the bicycle carriage charge is $5.00.\n\nClaim to check: the bicycle carriage charge is $25.00.",
  "question": "Under the stated rules, does the claim to check give the same value for the bicycle carriage charge that the listed sources settle on?",
  "definitions": "How to settle the bicycle carriage charge from the listed sources:\n- Tiers, most reliable first: scarlet; then teal; then ochre.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the bicycle carriage charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q358db33dc6",
  "kind": "choice",
  "text": "Memo: Layla Haddad is sorting out a booking and has put the notes on the registration fee at Thornmere Leisure Centre in good order. Please take a look at the material below.\n\nSources on the registration fee:\n- Source A: reply letter; tier sleet; dated 20 Feb 2026; independent. It states the registration fee is $250.00.\n- Source B: sandwich board; tier hail; dated 26 May 2026; copied from Source C. It states the registration fee is $350.00.\n- Source C: video caption; tier hail; dated 21 Feb 2026; independent. It states the registration fee is $350.00.\n- Source D: board notice; tier sleet; dated 20 Feb 2026; independent. It states the registration fee is $300.00.\n- Source E: poster; tier fog; dated 20 Feb 2026; copied from Source D. It states the registration fee is $300.00.",
  "question": "How to settle the registration fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which listed source should the registration fee value be taken from?",
  "options": [
   "Source A",
   "Source E",
   "No source: not determinable from reliable sources"
  ]
 }
]
