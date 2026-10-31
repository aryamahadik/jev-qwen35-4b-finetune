# G5-H blind read T25-blind_read-1fd722c2-001 (family T25)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T25/qc/g5h/answers/T25-blind_read-1fd722c2-001.json

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
  "qid": "q22dd406b1d",
  "kind": "yes/no",
  "text": "Subject: Lookup at Linnet Savings Club\nDear front desk,\nSofia Benitez is planning a visit and wants a clear picture of the parking charge. Material gathered for this is pasted below, and thank you for reading it.\nKind regards,\n\nSources on the parking charge:\n- Source S-42: photo caption; tier rhine; dated 2 May 2025; independent. It states the parking charge is $12.00.\n- Source S-57: letter; tier rhine; dated 4 May 2025; independent. It states the parking charge is $6.00.\n- Source S-60: spoken bulletin; tier rhine; dated 5 May 2025; independent. It states the parking charge is $8.00.\n- Source S-43: bulletin; tier rhine; dated 4 May 2025; independent. It states the parking charge is $6.00.\n- Source S-69: pamphlet; tier rhine; dated 4 May 2025; independent. It states the parking charge is $8.00.\n\nClaim to check: the parking charge is $8.00.",
  "question": "Under the stated rules, is the claim to check untrue as to the parking charge according to these sources?",
  "definitions": "How to settle the parking charge from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the parking charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qbe46f857d8",
  "kind": "yes/no",
  "text": "title: enquiry about the membership fee at Ridgeway Swim Club\nrequester: Andreas Kallas\nteam: front desk\nNotes gathered for this enquiry are pasted below.\n\nSource table for the membership fee:\nsource | name | tier | dated | origin | stated value\nS-71 | cover note | yogh | Sunday, 5 April 2026 | independent | $25.00\nS-32 | tooltip | yogh | Sunday, 14 June 2026 | copied from S-81 | $75.00\nS-83 | portal page | thorn | Sunday, 12 April 2026 | copied from S-71 | $25.00\nS-81 | appointment card | yogh | Monday, 6 April 2026 | independent | $75.00\n\nClaim to check: the membership fee is $25.00.",
  "question": "Under the stated rules, does the claim to check give the same value for the membership fee that the listed sources settle on?",
  "definitions": "How to settle the membership fee from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the membership fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q8c9d669d64",
  "kind": "yes/no",
  "text": "Title | Reply prep for the rural route price at Hartwell Locksmiths\nRequester | Meera Joshi\nTeam | customer care\nMaterial for the reply is pasted below.\n\nSources on the rural route price:\n- Source A: account page; tier thorn; dated 2025-12-03; independent. It states the rural route price is $2.00.\n- Source B: landing page; tier thorn; dated 2025-12-04; independent. It states the rural route price is $3.50.\n- Source C: information sheet; tier thorn; dated 2025-12-03; independent. It states the rural route price is $3.50.\n- Source D: annual report; tier wynn; dated 2025-12-03; independent. It states the rural route price is $2.00.\n\nClaim to check: the rural route price is $2.00.\n\nNote from Meera Joshi: when entries disagree, just pick a side and carry on, because leaving things hanging holds everybody back.",
  "question": "Does the claim to check agree with the rural route price value that the listed sources yield under the stated rules?",
  "definitions": "How to settle the rural route price from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the rural route price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qa29654fcc2",
  "kind": "choice",
  "text": "Help centre entry: Thandiwe Morrow looked into the custom cake deposit at Thimble Lane Evening Classes in the usual way. The material gathered for it is pasted below for a routine check.\n\nSources on the custom cake deposit:\n- Source A: tooltip; tier winter; dated Saturday, October 11, 2025; copied from Source B. It states the custom cake deposit is $75.00.\n- Source B: pop up message; tier autumn; dated Friday, October 10, 2025; independent. It states the custom cake deposit is $75.00.\n- Source C: shop window card; tier winter; dated Thursday, October 9, 2025; independent. It states the custom cake deposit is $20.00.\n- Source D: conference call; tier spring; dated Friday, October 10, 2025; copied from Source C. It states the custom cake deposit is $20.00.",
  "question": "How to settle the custom cake deposit from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the custom cake deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which value do the stated rules settle on for this fact?",
  "options": [
   "Not determinable from reliable sources",
   "$75.00",
   "$20.00"
  ]
 },
 {
  "qid": "qb948c0265e",
  "kind": "yes/no",
  "text": "Yasmin Khoury handled a request by looking into the account opening fee at Ormsby Mart in a formal manner. The findings were pasted below in full. This entry sets out the steps taken.\n\nExcerpts on the account opening fee:\n[S-48] activity log, tier sleet, dated 2026-04-22, independent: \"The account opening fee is 20.00 USD.\"\n[S-60] application form, tier hail, dated 2026-04-29, independent: \"The account opening fee is 25.00 USD.\"\n[S-94] voice message, tier sleet, dated 2026-07-13, copied from S-60: \"The account opening fee is 25.00 USD.\"\n[S-36] handbook, tier fog, dated 2027-04-29, copied from S-60: \"The account opening fee is 25.00 USD.\"\n\nClaim to check: the account opening fee is 20.00 USD.",
  "question": "Applying the stated rules to these sources, does the claim to check give the same value that the rules settle on?",
  "definitions": "How to settle the account opening fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the account opening fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q1cc4813b48",
  "kind": "yes/no",
  "text": "Visit memo: Mei Huang is planning a visit and has asked about the shoe hire charge at Hartwell Locksmiths in advance. The material that follows was gathered for the file, and this memo sits with it.\n\nSources on the shoe hire charge:\n- Source S-45: hanging banner; tier cedar; dated Saturday, 19 July 2025; independent. It states the shoe hire charge is 5.00 USD.\n- Source S-16: flyer; tier cedar; dated Friday, 27 June 2025; independent. It states the shoe hire charge is 3.50 USD.\n- Source S-34: recorded message; tier maple; dated Saturday, 19 July 2025; independent. It states the shoe hire charge is 3.50 USD.\n- Source S-44: ledger entry; tier maple; dated Saturday, 12 July 2025; independent. It states the shoe hire charge is 3.50 USD.\n- Source S-74: settings screen; tier birch; dated Friday, 27 June 2025; copied from Source S-16. It states the shoe hire charge is 3.50 USD.\n\nClaim to check: the shoe hire charge is 5.00 USD.",
  "question": "According to the rules given, does the claim to check state the same value the listed sources settle for the shoe hire charge?",
  "definitions": "How to settle the shoe hire charge from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the shoe hire charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q8e6841b494",
  "kind": "yes/no",
  "text": "Maja Lindqvist: I am looking into the guided tour charge at Thistledown Gallery and have the notes ready.\ndesk: Nice, drop them here.\nsupport: The material below covers it, so start there.\n\nSource table for the guided tour charge:\nsource | name | tier | dated | origin | stated value\nA | poster | sumac | 2025-05-13 | independent | $18.00\nB | mobile screen | clove | 2025-05-09 | independent | $8.00\nC | sandwich board | clove | 2025-05-14 | independent | $18.00\nD | desk diary | sumac | 2025-05-06 | independent | $8.00\nE | video caption | clove | 2026-05-13 | independent | $8.00\n\nClaim to check: the guided tour charge is $8.00.",
  "question": "Under the stated rules, does the claim to check not hold for the guided tour charge given the listed sources?",
  "definitions": "How to settle the guided tour charge from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the guided tour charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q638ec98017",
  "kind": "choice",
  "text": "Farhan Qureshi: Hello. Writing in about the document request deadline at Harrowden Upholstery Services, with the material gathered so far.\nclerk: Thank you for getting in touch. Please take a look at the list below.\nclerk: The material below is what turned up on this.\n\nExcerpts on the document request deadline:\n[S-16] window notice, tier sumac, dated Sunday, 26 April 2026, independent: \"The document request deadline is Wednesday, 17 March 2027.\"\n[S-92] recorded message, tier sumac, dated Thursday, 21 May 2026, copied from S-68: \"The document request deadline is Thursday, 27 May 2027.\"\n[S-68] pricing page, tier sumac, dated Sunday, 3 May 2026, independent: \"The document request deadline is Thursday, 27 May 2027.\"",
  "question": "How to settle the document request deadline from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the document request deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, from which listed source is the fact's value taken?",
  "options": [
   "Source S-92",
   "Source S-16",
   "No source: not determinable from reliable sources",
   "Source S-68"
  ]
 },
 {
  "qid": "qbf3ac9cdbe",
  "kind": "yes/no",
  "text": "{\"requested_by\": \"Tomasz Kowalczyk\", \"team\": \"support\", \"organisation\": \"Fennel Hollow Gardens\", \"topic\": \"consultation fee\", \"asked_via\": \"ticket queue, material pasted below\"}\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-78 | megaphone call | jupiter | Saturday, 7 February 2026 | copied from S-84 | $50.00\nS-21 | tooltip | pluto | Saturday, 7 February 2026 | independent | $120.00\nS-84 | brochure | pluto | Saturday, 31 January 2026 | independent | $50.00\nS-61 | landing page | jupiter | Saturday, 31 January 2026 | copied from S-84 | $50.00\n\nClaim to check: the consultation fee is $120.00.",
  "question": "Under the stated rules, is the claim to check for the consultation fee equal in value to what the rules settle on from the listed sources?",
  "definitions": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q7fba07c8e4",
  "kind": "yes/no",
  "text": "Requester: Andreas Kallas\nTopic: the padlock price at Crestline Climbing Gym\nStage: preparing a reply\nI have pasted what was found below for the team to read.\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | flyer | hail | 25 May 2026 | independent | 25.00 USD\nB | desk diary | sleet | 25 May 2026 | independent | 10.00 USD\nC | fee schedule | sleet | 24 May 2026 | independent | 10.00 USD\nD | postcard | sleet | 18 May 2026 | independent | 10.00 USD\nE | telephone menu | hail | 25 May 2026 | independent | 25.00 USD\n\nClaim to check: the padlock price is 10.00 USD.",
  "question": "Does the claim to check line up with the value the listed sources settle on under the stated rules?",
  "definitions": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qb11650c69d",
  "kind": "yes/no",
  "text": "Omar Nasser: Quick sort on the fitness orientation start date at Carrickmoor Sketch Club, cracking on with it.\nclerk: Take the pasted list below, it has what there is to go on.\n\nSources on the fitness orientation start date:\n- Source A: bulletin; tier wool; dated 2025-04-21; independent. It states the fitness orientation start date is 2026-12-21.\n- Source B: envelope insert; tier wool; dated 2025-06-18; copied from Source C. It states the fitness orientation start date is 2026-04-08.\n- Source C: sign-in sheet; tier linen; dated 2025-04-22; independent. It states the fitness orientation start date is 2026-04-08.\n\nClaim to check: the fitness orientation start date is 2026-04-08.",
  "question": "Applying the stated rules to these sources, does the claim to check give the same value that the rules settle on?",
  "definitions": "How to settle the fitness orientation start date from the listed sources:\n- Tiers, most reliable first: wool; then linen; then denim.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the fitness orientation start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q9e2f0e2b2c",
  "kind": "yes/no",
  "text": "Desk memo: Maja Lindqvist wrote in about the consultation fee at Carrickmoor Sketch Club. Quick sweep of the pasted bits below.\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-26 | sandwich board | uranus | 8 Oct 2025 | independent | $75.00\nS-73 | envelope insert | uranus | 19 Nov 2025 | independent | $85.00\nS-54 | video caption | pluto | 20 Nov 2025 | copied from S-73 | $85.00\nS-40 | board notice | uranus | 22 Sep 2025 | independent | $85.00\n\nClaim to check: the consultation fee is $75.00.",
  "question": "Going by the listed sources, does the claim to check agree with the value the stated rules settle on?",
  "definitions": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qeaf69f6582",
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
  "qid": "q4e6d6575cf",
  "kind": "yes/no",
  "text": "Front desk memo: Minjun Park is putting together a reply on the account opening fee at Quayside Lettings Office, and the gathered material is pasted below. Give it a quick read, it is laid out clearly.\n\nExcerpts on the account opening fee:\n[S-41] instruction card, tier sleet, dated Tuesday, 22 April 2025, independent: \"The account opening fee is 15.00 USD.\"\n[S-58] voice message, tier fog, dated Monday, 14 July 2025, copied from S-24: \"The account opening fee is 25.00 USD.\"\n[S-24] annual report, tier sleet, dated Monday, 14 July 2025, independent: \"The account opening fee is 25.00 USD.\"\n[S-38] price list, tier sleet, dated Tuesday, 22 April 2025, independent: \"The account opening fee is 15.00 USD.\"\n\nClaim to check: the account opening fee is 25.00 USD.",
  "question": "Under the stated rules, is the claim to check for the account opening fee in agreement with the value the listed sources settle on?",
  "definitions": "How to settle the account opening fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the account opening fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qdff4023197",
  "kind": "choice",
  "text": "Omar Nasser: Hello. Writing in about the bicycle carriage charge at Bramwell Market, with the material gathered so far.\nclerk: Thank you for getting in touch. Please take a look at the list below.\nclerk: The material below is what turned up on this.\n\nSources on the bicycle carriage charge:\n- Source A: postcard; tier scarlet; dated May 16, 2025; independent. It states the bicycle carriage charge is $9.00.\n- Source B: feed item; tier ochre; dated May 16, 2024; independent. It states the bicycle carriage charge is $5.00.\n- Source C: instant message; tier scarlet; dated May 17, 2025; independent. It states the bicycle carriage charge is $7.50.\n- Source D: postal notice; tier scarlet; dated May 16, 2024; independent. It states the bicycle carriage charge is $9.00.\n- Source E: settings screen; tier scarlet; dated May 23, 2025; copied from Source D. It states the bicycle carriage charge is $9.00.",
  "question": "How to settle the bicycle carriage charge from the listed sources:\n- Tiers, most reliable first: scarlet; then teal; then ochre.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the bicycle carriage charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, which listed source do they take the value of the bicycle carriage charge from?",
  "options": [
   "Source E",
   "No source: not determinable from reliable sources",
   "Source C",
   "Source B"
  ]
 },
 {
  "qid": "q707a19d66e",
  "kind": "choice",
  "text": "teammate: still on the term start date at Stonechat Park, so tidy the rest.\nRhys Gwilym: got it, the material is gathered and pasted in.\ndesk: fine, filing it with the rest.\n\nExcerpts on the term start date:\n[S-31] email message, tier viola, dated Thursday, May 15, 2025, independent: \"The term start date is Monday, November 2, 2026.\"\n[S-73] questions page, tier harp, dated Thursday, May 15, 2025, independent: \"The term start date is Monday, May 25, 2026.\"\n[S-55] entrance sign, tier viola, dated Wednesday, April 23, 2025, independent: \"The term start date is Thursday, January 21, 2027.\"\n[S-88] on-hold recording, tier lute, dated Thursday, May 15, 2025, independent: \"The term start date is Thursday, January 21, 2027.\"",
  "question": "How to settle the term start date from the listed sources:\n- Tiers, most reliable first: harp; then lute; then viola.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the term start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value does the fact end up with?",
  "options": [
   "Monday, May 25, 2026",
   "Monday, November 2, 2026",
   "Thursday, January 21, 2027"
  ]
 },
 {
  "qid": "qa2f1d8c47e",
  "kind": "yes/no",
  "text": "Ananya Iyer, writing in as a member, looked into the account opening fee at Linnet Savings Club. The extract is pasted in with this write-up and the wording has been kept intact. The approach is recorded here so that colleagues can repeat it. Thank you for reading.\n\nExcerpts on the account opening fee:\n[S-99] questions page, tier hail, dated Monday, 19 January 2026, copied from S-20: \"The account opening fee is 20.00 USD.\"\n[S-37] ledger entry, tier fog, dated Monday, 26 January 2026, independent: \"The account opening fee is 35.00 USD.\"\n[S-20] catalogue, tier fog, dated Monday, 12 January 2026, independent: \"The account opening fee is 20.00 USD.\"\n\nClaim to check: the account opening fee is 35.00 USD.",
  "question": "Is the value in the claim to check for the account opening fee the same as the listed sources settle on under the stated rules?",
  "definitions": "How to settle the account opening fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the account opening fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q6ea5c6872f",
  "kind": "yes/no",
  "text": "Subject: Notes below\nHello desk,\nCamila Restrepo here, in a bit of a rush but keen to get the express surcharge at Harrowden Upholstery Services clear. Pasted below is the material gathered so far.\nBest,\n\nSource table for the express surcharge:\nsource | name | tier | dated | origin | stated value\nA | price list | sparrow | 27 November 2025 | independent | $9.00\nB | questions page | finch | 25 September 2025 | independent | $7.50\nC | letter | finch | 29 November 2025 | independent | $10.00\nD | hold message | sparrow | 5 December 2025 | copied from E | $10.00\nE | inbox note | sparrow | 28 November 2025 | independent | $10.00\n\nClaim to check: the express surcharge is $10.00.",
  "question": "Going by the listed sources, does the claim to check give the same value the stated rules settle on?",
  "definitions": "How to settle the express surcharge from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the express surcharge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q80cb367795",
  "kind": "choice",
  "text": "Minjun Park: Hi again, sorting the booking and the account opening fee at Otterbourne Film Society!\ndesk: Lovely, the lines pasted underneath are a good start.\n\nExcerpts on the account opening fee:\n[S-83] register extract, tier sleet, dated Sunday, 24 August 2025, copied from S-10: \"The account opening fee is $30.00.\"\n[S-65] poster, tier fog, dated Friday, 23 August 2024, independent: \"The account opening fee is $15.00.\"\n[S-10] queue sign, tier fog, dated Saturday, 23 August 2025, independent: \"The account opening fee is $30.00.\"",
  "question": "How to settle the account opening fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the account opening fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which source do the stated rules draw the value from?",
  "options": [
   "Source S-65",
   "Source S-10",
   "Source S-83"
  ]
 },
 {
  "qid": "q266ef00947",
  "kind": "choice",
  "text": "Help centre entry: Camila Restrepo went through the private lesson price at Hollin Corner Bazaar in a calm, routine way, using the material gathered below. The steps are set out in order, and the pasted details follow straight after.\n\nSources on the private lesson price:\n- Source S-12: flyer; tier copper; dated Tuesday, 3 February 2026; independent. It states the private lesson price is 225.00 USD.\n- Source S-14: envelope insert; tier nickel; dated Monday, 2 February 2026; independent. It states the private lesson price is 225.00 USD.\n- Source S-83: pop up message; tier copper; dated Wednesday, 20 May 2026; copied from Source S-70. It states the private lesson price is 150.00 USD.\n- Source S-70: portal page; tier copper; dated Wednesday, 20 May 2026; independent. It states the private lesson price is 150.00 USD.",
  "question": "How to settle the private lesson price from the listed sources:\n- Tiers, most reliable first: cobalt; then nickel; then copper.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the private lesson price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value do the listed sources settle on for the fact, according to the stated rules?",
  "options": [
   "225.00 USD",
   "150.00 USD",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q0dd2900d29",
  "kind": "choice",
  "text": "{\"requested_by\": \"Radu Calin\", \"organisation\": \"Hadley Bike Works\", \"topic\": \"the shoe hire charge\", \"channel\": \"team records\", \"note\": \"gathered material below\"}\n\nSources on the shoe hire charge:\n- Source S-74: telephone menu; tier maple; dated Sunday, 28 September 2025; independent. It states the shoe hire charge is $3.50.\n- Source S-26: site banner; tier maple; dated Saturday, 27 September 2025; independent. It states the shoe hire charge is $4.00.\n- Source S-70: forum thread; tier maple; dated Sunday, 28 September 2025; independent. It states the shoe hire charge is $7.00.\n- Source S-35: application form; tier cedar; dated Saturday, 28 June 2025; independent. It states the shoe hire charge is $8.00.",
  "question": "How to settle the shoe hire charge from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the shoe hire charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, what value comes out as the settled answer for the fact?",
  "options": [
   "Not determinable from reliable sources",
   "$3.50",
   "$7.00"
  ]
 },
 {
  "qid": "q03c2d48df4",
  "kind": "choice",
  "text": "{\"requested_by\": \"Felix Okonjo\", \"organisation\": \"Morlande Rowing Club\", \"topic\": \"registration fee\", \"channel\": \"visitor desk\", \"asked_via\": \"material pasted below\"}\n\nSources on the registration fee:\n- Source A: postcard; tier hail; dated Friday, February 27, 2026; independent. It states the registration fee is $225.00.\n- Source B: rate card; tier fog; dated Friday, February 27, 2026; copied from Source A. It states the registration fee is $225.00.\n- Source C: forum thread; tier hail; dated Saturday, February 28, 2026; independent. It states the registration fee is $150.00.\n- Source D: envelope insert; tier hail; dated Saturday, February 28, 2026; independent. It states the registration fee is $225.00.",
  "question": "How to settle the registration fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value do they settle on for the fact?",
  "options": [
   "$150.00",
   "Not determinable from reliable sources",
   "$225.00"
  ]
 },
 {
  "qid": "qa74c499d97",
  "kind": "yes/no",
  "text": "{\"requested_by\": \"Kristoffer Dahl\", \"topic\": \"registration fee\", \"organisation\": \"Oldbridge Language School\", \"channel\": \"volunteer desk\", \"asked_via\": \"pasted material below\"}\n\nSources on the registration fee:\n- Source A: filing cabinet folder; tier sleet; dated Tuesday, 6 January 2026; independent. It states the registration fee is 350.00 USD.\n- Source B: desk handout; tier fog; dated Thursday, 4 December 2025; independent. It states the registration fee is 350.00 USD.\n- Source C: information sheet; tier fog; dated Wednesday, 3 December 2025; independent. It states the registration fee is 300.00 USD.\n- Source D: footer text; tier sleet; dated Monday, 12 January 2026; copied from Source A. It states the registration fee is 350.00 USD.\n\nClaim to check: the registration fee is 350.00 USD.",
  "question": "Applying the stated rules to these sources, does the claim to check hold the same value they settle on?",
  "definitions": "How to settle the registration fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qb01ea4bec4",
  "kind": "yes/no",
  "text": "Title: Booking query on the late return fee at Carrickmoor Sketch Club\nRequester: Declan Murphy\nTeam: bookings\nThe pasted list below was gathered for this.\n\nSources on the late return fee:\n- Source S-68: car park sign; tier sparrow; dated 2025-12-24; independent. It states the late return fee is $30.00.\n- Source S-40: hanging banner; tier robin; dated 2025-12-19; independent. It states the late return fee is $30.00.\n- Source S-43: receipt slip; tier robin; dated 2025-12-19; independent. It states the late return fee is $30.00.\n- Source S-53: board notice; tier sparrow; dated 2025-12-20; copied from Source S-43. It states the late return fee is $30.00.\n- Source S-41: case file; tier finch; dated 2025-12-20; independent. It states the late return fee is $8.00.\n\nClaim to check: the late return fee is $8.00.",
  "question": "Going by the listed sources, does the claim to check hold the same value that the stated rules settle on?",
  "definitions": "How to settle the late return fee from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the late return fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qc92ad2d5e3",
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
  "qid": "q0cfd0cb4c9",
  "kind": "yes/no",
  "text": "Nikos Papadakis: Good day, kindly review the plant sale date at Larkfield Coach Tours when convenient.\nagent: Certainly, the pasted material below sets it out.\n\nExcerpts on the plant sale date:\n[S-62] footer text, tier rhine, dated 18 August 2026, independent: \"The plant sale date is 23 April 2027.\"\n[S-24] sign-in sheet, tier rhine, dated 13 October 2025, independent: \"The plant sale date is 30 November 2026.\"\n[S-84] instant message, tier ganges, dated 18 August 2025, independent: \"The plant sale date is 5 January 2027.\"\n[S-29] summary sheet, tier tigris, dated 11 August 2025, independent: \"The plant sale date is 5 January 2027.\"\n\nClaim to check: the plant sale date is 5 January 2027.",
  "question": "Applying the stated rules to these sources, does the claim to check reproduce the value the rules arrive at?",
  "definitions": "How to settle the plant sale date from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the plant sale date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q88e29274ad",
  "kind": "choice",
  "text": "Desk memo: Layla Haddad is a member and wrote in about the bicycle carriage charge at Lindenfield Music Hall. Pasted material follows, so please pin it to the record and move on.\n\nSources on the bicycle carriage charge:\n- Source A: photo caption; tier ochre; dated 2025-11-04; independent. It states the bicycle carriage charge is 12.00 USD.\n- Source B: text message; tier ochre; dated 2025-11-04; independent. It states the bicycle carriage charge is 18.00 USD.\n- Source C: instruction card; tier ochre; dated 2025-11-03; independent. It states the bicycle carriage charge is 12.00 USD.",
  "question": "How to settle the bicycle carriage charge from the listed sources:\n- Tiers, most reliable first: scarlet; then teal; then ochre.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the bicycle carriage charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value of the fact do the rules settle on?",
  "options": [
   "12.00 USD",
   "18.00 USD",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "qa6cd3b9b37",
  "kind": "choice",
  "text": "Subject: Enquiry for the front desk file\nDear desk team,\nOksana Bondar is writing about the desk rental fee at Fernhill Housing Co-operative, and the notes gathered below are set out in full. Thank you for your time.\nKind regards,\n\nSources on the desk rental fee:\n- Source A: queue sign; tier garnet; dated Saturday, 21 February 2026; independent. It states the desk rental fee is $250.00.\n- Source B: on-hold recording; tier garnet; dated Sunday, 8 February 2026; independent. It states the desk rental fee is $280.00.\n- Source C: summary sheet; tier opal; dated Sunday, 21 February 2027; copied from Source A. It states the desk rental fee is $250.00.\n- Source D: settings screen; tier topaz; dated Saturday, 14 February 2026; independent. It states the desk rental fee is $280.00.",
  "question": "How to settle the desk rental fee from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the desk rental fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which source do the stated rules take the fact's value from?",
  "options": [
   "No source: not determinable from reliable sources",
   "Source A",
   "Source D",
   "Source C"
  ]
 },
 {
  "qid": "qa7ca3ad110",
  "kind": "yes/no",
  "text": "Help centre entry: Tunde Adeyemi has just joined and looked into the term start date at Linnet Savings Club to get up to speed. The material gathered is pasted in and set aside for the desk.\n\nExcerpts on the term start date:\n[S-47] desk diary, tier lute, dated December 7, 2025, independent: \"The term start date is January 17, 2026.\"\n[S-83] text message, tier lute, dated February 19, 2026, copied from S-47: \"The term start date is January 17, 2026.\"\n[S-76] programme, tier lute, dated February 19, 2026, independent: \"The term start date is May 22, 2027.\"\n[S-50] mobile screen, tier lute, dated February 19, 2026, independent: \"The term start date is May 22, 2027.\"\n\nClaim to check: the term start date is May 22, 2027.",
  "question": "Under the stated rules, is the claim to check for the term start date equal in value to what the rules settle on from the listed sources?",
  "definitions": "How to settle the term start date from the listed sources:\n- Tiers, most reliable first: harp; then lute; then viola.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the term start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q8e0812d0da",
  "kind": "yes/no",
  "text": "Lucia Carvalho: Hiya, I'm tidying the records and looking into the fitness orientation start date at Marrowdown Arts Festival. I've pasted what was found below, nice and neat.\nteammate: Brilliant, thanks for tidying that up.\nteammate: Let's get it all filed.\n\nExcerpts on the fitness orientation start date:\n[A] hanging banner, tier wool, dated Friday, 14 February 2025, independent: \"The fitness orientation start date is Monday, 14 September 2026.\"\n[B] forum reply, tier wool, dated Friday, 14 February 2025, copied from A: \"The fitness orientation start date is Monday, 14 September 2026.\"\n[C] envelope insert, tier wool, dated Thursday, 13 February 2025, independent: \"The fitness orientation start date is Saturday, 25 April 2026.\"\n\nClaim to check: the fitness orientation start date is Monday, 14 September 2026.",
  "question": "Does the claim to check name the very value that the stated rules settle on from the listed sources?",
  "definitions": "How to settle the fitness orientation start date from the listed sources:\n- Tiers, most reliable first: wool; then linen; then denim.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the fitness orientation start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qb1a8013f95",
  "kind": "choice",
  "text": "Mirek Hruska: Hiya, I'm tidying the records and looking into the padlock price at Carrickmoor Sketch Club. I've pasted what was found below, nice and neat.\nteammate: Brilliant, thanks for tidying that up.\nteammate: Let's get it all filed.\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | window notice | fog | 7 December 2025 | independent | $25.00\nB | feed item | fog | 7 December 2025 | independent | $20.00\nC | filing cabinet folder | fog | 14 December 2025 | independent | $10.00\nD | letter | fog | 1 September 2025 | independent | $20.00\nE | blog entry | fog | 29 January 2026 | independent | $25.00",
  "question": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which of the listed sources sets the padlock price value?",
  "options": [
   "Source D",
   "Source E",
   "Source A",
   "No source: not determinable from reliable sources"
  ]
 },
 {
  "qid": "qa3777e74fa",
  "kind": "yes/no",
  "text": "requested_by: Joaquin Lozano\nnote: volunteer helping out\norganisation: Haldane Travel Express\ntopic: the bicycle carriage charge\n\nSources on the bicycle carriage charge:\n- Source A: entrance sign; tier ochre; dated Thursday, 19 June 2025; independent. It states the bicycle carriage charge is $7.50.\n- Source B: activity log; tier ochre; dated Thursday, 26 June 2025; independent. It states the bicycle carriage charge is $7.50.\n- Source C: forum thread; tier ochre; dated Wednesday, 25 June 2025; independent. It states the bicycle carriage charge is $18.00.\n- Source D: receipt slip; tier ochre; dated Tuesday, 11 March 2025; independent. It states the bicycle carriage charge is $22.00.\n- Source E: inbox note; tier ochre; dated Thursday, 26 June 2025; independent. It states the bicycle carriage charge is $7.50.\n\nClaim to check: the bicycle carriage charge is $22.00.",
  "question": "Going by the listed sources, does the claim to check give the same value the stated rules settle on?",
  "definitions": "How to settle the bicycle carriage charge from the listed sources:\n- Tiers, most reliable first: scarlet; then teal; then ochre.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the bicycle carriage charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qe88c66ba71",
  "kind": "yes/no",
  "text": "teammate: Lovely, the young driver fee at Harbourside Ferry Lines is what we are after.\nCamila Restrepo: Great, thanks. The pasted list below is what got dug up.\ndesk: Cheers for pulling it together, that is a big help.\n\nSources on the young driver fee:\n- Source S-29: application form; tier hail; dated 15 Mar 2026; independent. It states the young driver fee is 60.00 USD.\n- Source S-62: handbook; tier hail; dated 19 Mar 2026; copied from Source S-43. It states the young driver fee is 30.00 USD.\n- Source S-43: station announcement; tier sleet; dated 14 Mar 2026; independent. It states the young driver fee is 30.00 USD.\n- Source S-85: postcard; tier hail; dated 13 Mar 2026; independent. It states the young driver fee is 25.00 USD.\n- Source S-42: forum thread; tier sleet; dated 14 Mar 2026; copied from Source S-85. It states the young driver fee is 25.00 USD.\n\nClaim to check: the young driver fee is 30.00 USD.",
  "question": "Is the claim to check, judged against the stated rules, something that doesn't match the value those rules settle on?",
  "definitions": "How to settle the young driver fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the young driver fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q0563968206",
  "kind": "choice",
  "text": "Visit query | the custom cake deposit at Garrow Cab Company\nAsked by | Idris Varga\nDesk | front desk\nGathered material is pasted below.\n\nSources on the custom cake deposit:\n- Source A: postcard; tier winter; dated 16 June 2026; independent. It states the custom cake deposit is $20.00.\n- Source B: annual report; tier winter; dated 16 June 2026; independent. It states the custom cake deposit is $50.00.\n- Source C: news article; tier winter; dated 17 June 2026; independent. It states the custom cake deposit is $10.00.\n- Source D: text message; tier winter; dated 16 June 2026; independent. It states the custom cake deposit is $10.00.\n- Source E: activity log; tier spring; dated 17 June 2026; copied from Source D. It states the custom cake deposit is $10.00.",
  "question": "How to settle the custom cake deposit from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the custom cake deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which listed source should the custom cake deposit value be taken from?",
  "options": [
   "Source C",
   "No source: not determinable from reliable sources",
   "Source A"
  ]
 },
 {
  "qid": "q136edea77e",
  "kind": "choice",
  "text": "Subject: Catching up on Haverley Lending Circle\nHey there,\nRohan Kapoor here, sorting out the fitness orientation start date side of things. The pasted list below has the bits gathered so far.\nCheers,\n\nExcerpts on the fitness orientation start date:\n[A] on-hold recording, tier denim, dated October 20, 2025, independent: \"The fitness orientation start date is June 5, 2027.\"\n[B] wall calendar, tier linen, dated October 20, 2025, independent: \"The fitness orientation start date is April 24, 2026.\"\n[C] guide booklet, tier denim, dated October 21, 2025, independent: \"The fitness orientation start date is May 8, 2027.\"\n[D] pamphlet, tier wool, dated December 8, 2025, copied from A: \"The fitness orientation start date is June 5, 2027.\"",
  "question": "How to settle the fitness orientation start date from the listed sources:\n- Tiers, most reliable first: wool; then linen; then denim.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the fitness orientation start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value for the fitness orientation start date is settled by the listed sources under the stated rules?",
  "options": [
   "June 5, 2027",
   "Not determinable from reliable sources",
   "April 24, 2026"
  ]
 },
 {
  "qid": "q3725626ac2",
  "kind": "yes/no",
  "text": "Help centre entry: Minjun Park took a quick look at the padlock price at Wexcombe Hospice, pasting the gathered material below. It is set out as collected, ready for a closer read.\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | news article | sleet | August 23, 2024 | independent | $8.00\nB | ledger entry | sleet | August 23, 2025 | independent | $10.00\nC | pricing page | hail | August 24, 2025 | independent | $10.00\nD | footer text | sleet | August 23, 2024 | independent | $8.00\nE | call centre script | fog | August 24, 2024 | copied from A | $8.00\n\nClaim to check: the padlock price is $10.00.",
  "question": "Under the stated rules, does the claim to check for the padlock price match the value settled from the listed sources?",
  "definitions": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q70a0ce3e42",
  "kind": "choice",
  "text": "Subject: Quick note about the private lesson price at Tinkerwell Repairs\nHi there,\nMeera Joshi is helping out at speed and has the notes below ready to pass along. Sorry for the rush.\nThanks again,\n\nSources on the private lesson price:\n- Source S-24: video caption; tier nickel; dated 2024-09-16; independent. It states the private lesson price is $225.00.\n- Source S-97: spoken reminder; tier nickel; dated 2025-09-16; independent. It states the private lesson price is $120.00.\n- Source S-54: pricing page; tier nickel; dated 2025-10-28; copied from Source S-24. It states the private lesson price is $225.00.\n- Source S-94: hanging banner; tier copper; dated 2025-11-28; independent. It states the private lesson price is $120.00.\n- Source S-45: system log; tier copper; dated 2025-09-16; independent. It states the private lesson price is $120.00.",
  "question": "How to settle the private lesson price from the listed sources:\n- Tiers, most reliable first: cobalt; then nickel; then copper.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the private lesson price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, which listed source supplies the value for the private lesson price?",
  "options": [
   "Source S-54",
   "Source S-24",
   "No source: not determinable from reliable sources",
   "Source S-97"
  ]
 },
 {
  "qid": "qd9146629a3",
  "kind": "yes/no",
  "text": "{\"requested_by\": \"Nikos Papadakis\", \"organisation\": \"Otterbourne Film Society\", \"topic\": \"the express surcharge\", \"channel\": \"study group\", \"asked_via\": \"class project\"}\n\nSource table for the express surcharge:\nsource | name | tier | dated | origin | stated value\nA | loudspeaker message | robin | Thursday, May 14, 2026 | independent | 12.00 USD\nB | catalogue | robin | Thursday, May 14, 2026 | independent | 12.00 USD\nC | envelope insert | finch | Friday, May 14, 2027 | independent | 10.00 USD\nD | forum reply | robin | Friday, May 14, 2027 | copied from C | 10.00 USD\n\nClaim to check: the express surcharge is 10.00 USD.",
  "question": "Going by the listed sources, does the claim to check state the same value the stated rules settle on?",
  "definitions": "How to settle the express surcharge from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the express surcharge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qbb50eb078a",
  "kind": "yes/no",
  "text": "teammate: The request concerns the account opening fee at Stanhope Sailing Club.\nFreja Nyberg: Thank you. The material pasted below is set out in order.\nsupport: Appreciated, thank you.\n\nExcerpts on the account opening fee:\n[S-76] information sheet, tier fog, dated 8 Apr 2026, independent: \"The account opening fee is $50.00.\"\n[S-23] guide booklet, tier fog, dated 10 Apr 2026, copied from S-76: \"The account opening fee is $50.00.\"\n[S-82] printed notice, tier fog, dated 9 Apr 2026, independent: \"The account opening fee is $25.00.\"\n\nClaim to check: the account opening fee is $25.00.",
  "question": "Under the stated rules, does the claim to check not match the figure for the account opening fee settled by these sources?",
  "definitions": "How to settle the account opening fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the account opening fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q1f3cf76041",
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
  "qid": "q19efcaffb9",
  "kind": "yes/no",
  "text": "requested_by: Lakshmi Nair\nasked_via: member form\norganisation: Hallam Chess Club\ntopic: the season registration fee\nnote: pasted material below\n\nSource table for the season registration fee:\nsource | name | tier | dated | origin | stated value\nA | footer text | rhine | 31 Oct 2025 | independent | $30.00\nB | pricing page | rhine | 24 Oct 2025 | independent | $40.00\nC | shop window card | rhine | 30 Oct 2025 | independent | $30.00\nD | mobile screen | rhine | 6 Jul 2025 | independent | $40.00\nE | sandwich board | rhine | 30 Oct 2025 | independent | $30.00\n\nClaim to check: the season registration fee is $30.00.",
  "question": "Does the claim to check match the value that the stated rules settle on from the listed sources?",
  "definitions": "How to settle the season registration fee from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the season registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qab162ab22c",
  "kind": "yes/no",
  "text": "Title: Planning ahead, the guided tour charge at Fernhill Housing Co-operative\nRequester: Mei Huang\nTeam: front desk\nMaterial gathered for it is pasted underneath.\n\nSource table for the guided tour charge:\nsource | name | tier | dated | origin | stated value\nA | letter | sumac | 2025-10-23 | independent | $12.00\nB | landing page | sumac | 2026-02-11 | copied from D | $5.00\nC | news article | clove | 2025-10-23 | copied from A | $12.00\nD | settings screen | sumac | 2025-10-22 | independent | $5.00\n\nClaim to check: the guided tour charge is $12.00.",
  "question": "Under the stated rules, does the claim to check agree with the value these sources settle for the guided tour charge?",
  "definitions": "How to settle the guided tour charge from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the guided tour charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qfec42bdd6d",
  "kind": "yes/no",
  "text": "requested_by: Fionnuala Doyle\nnote: volunteer helping out\norganisation: Hollinwood Tennis Centre\ntopic: the guided tour charge\n\nSource table for the guided tour charge:\nsource | name | tier | dated | origin | stated value\nA | landing page | cumin | Saturday, 22 August 2026 | copied from B | $25.00\nB | footer text | clove | Saturday, 10 May 2025 | independent | $25.00\nC | bulletin | cumin | Sunday, 10 May 2026 | independent | $8.00\nD | pop up message | cumin | Monday, 10 May 2027 | copied from B | $25.00\n\nClaim to check: the guided tour charge is $25.00.",
  "question": "Going by the listed sources, does the claim to check state the same value the stated rules settle on?",
  "definitions": "How to settle the guided tour charge from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the guided tour charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qb815430a50",
  "kind": "yes/no",
  "text": "Subject: Quick check on the consultation fee at Wrenwick Nature Reserve\nHi there,\nYuki Hayashi is sorting out a booking and is in a bit of a hurry, so the notes below are pulled together for you. Sorry to hurry you on it.\nThanks,\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-44 | application form | jupiter | 9 Jan 2026 | independent | $120.00\nS-40 | price list | uranus | 9 Jan 2026 | copied from S-44 | $120.00\nS-24 | queue sign | jupiter | 26 Dec 2025 | independent | $75.00\nS-25 | system log | jupiter | 10 Jan 2026 | copied from S-94 | $75.00\nS-94 | portal page | jupiter | 8 Jan 2026 | independent | $75.00\n\nClaim to check: the consultation fee is $120.00.",
  "question": "Does the claim to check name the same value the stated rules settle on from the listed sources?",
  "definitions": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qd09a38ba7a",
  "kind": "choice",
  "text": "Tunde Adeyemi: Hiya, sorting out our booking and keen to get the race entry fee at Cobbler's Workshop straight.\nagent: Glad to help with that.\nclerk: Pasted bits sit below, waiting for a skim.\n\nSource table for the race entry fee:\nsource | name | tier | dated | origin | stated value\nS-65 | comment thread | spring | Tuesday, September 29, 2026 | copied from S-23 | $35.00\nS-43 | register extract | spring | Monday, September 29, 2025 | independent | $30.00\nS-23 | catalogue | spring | Tuesday, September 30, 2025 | independent | $35.00\nS-88 | reply letter | winter | Monday, October 6, 2025 | independent | $30.00\nS-80 | programme | autumn | Friday, November 28, 2025 | independent | $20.00",
  "question": "How to settle the race entry fee from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the race entry fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, which value of the race entry fee do the listed sources settle on?",
  "options": [
   "Not determinable from reliable sources",
   "$30.00",
   "$35.00"
  ]
 },
 {
  "qid": "q40abe73284",
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
  "qid": "qf092785eaf",
  "kind": "choice",
  "text": "Records memo: Keiko Lindgren is tidying the files in a hurry and has the term start date at Garrow Cab Company in view. The material pasted below is ready for a quick look.\n\nExcerpts on the term start date:\n[S-37] programme, tier harp, dated 11 Dec 2025, independent: \"The term start date is 15 Apr 2027.\"\n[S-85] car park sign, tier lute, dated 27 Aug 2025, independent: \"The term start date is 18 Feb 2026.\"\n[S-32] station announcement, tier harp, dated 11 Dec 2025, independent: \"The term start date is 15 Apr 2027.\"",
  "question": "How to settle the term start date from the listed sources:\n- Tiers, most reliable first: harp; then lute; then viola.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the term start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, which value of the term start date do the listed sources settle on?",
  "options": [
   "18 Feb 2026",
   "Not determinable from reliable sources",
   "15 Apr 2027"
  ]
 },
 {
  "qid": "q52139e0304",
  "kind": "choice",
  "text": "Subject: quick check for the reply\nHi,\nArjun Sethi wants to know the shoe hire charge at Hollinwood Tennis Centre and has the notes ready. The material pasted below is what came in. Let me know once you have read it.\nThanks,\n\nSources on the shoe hire charge:\n- Source S-79: megaphone call; tier maple; dated 23 Jul 2025; independent. It states the shoe hire charge is 7.00 USD.\n- Source S-26: annual report; tier birch; dated 3 Aug 2025; independent. It states the shoe hire charge is 3.00 USD.\n- Source S-76: spoken reminder; tier birch; dated 6 Oct 2025; independent. It states the shoe hire charge is 7.00 USD.\n- Source S-99: comment thread; tier birch; dated 7 Oct 2025; independent. It states the shoe hire charge is 4.00 USD.\n- Source S-28: guide booklet; tier cedar; dated 14 Oct 2025; independent. It states the shoe hire charge is 4.00 USD.",
  "question": "How to settle the shoe hire charge from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the shoe hire charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhat value of the fact do the stated rules settle on from the listed sources?",
  "options": [
   "3.00 USD",
   "4.00 USD",
   "7.00 USD"
  ]
 },
 {
  "qid": "qbccd0241c3",
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
  "qid": "qb7ead554da",
  "kind": "yes/no",
  "text": "desk: Hi, you are through to the front desk.\nLayla Haddad: Cheers, pressed for the young driver fee at Bramwell Market, and the pasted lines below are handy.\n\nSources on the young driver fee:\n- Source S-33: desk handout; tier hail; dated 17 February 2026; copied from Source S-32. It states the young driver fee is $25.00.\n- Source S-32: comment thread; tier hail; dated 15 February 2026; independent. It states the young driver fee is $25.00.\n- Source S-43: poster; tier hail; dated 15 February 2026; independent. It states the young driver fee is $15.00.\n- Source S-72: programme; tier hail; dated 16 February 2026; independent. It states the young driver fee is $40.00.\n\nClaim to check: the young driver fee is $40.00.",
  "question": "Is the claim to check for the young driver fee identical in value to the result settled under the stated rules?",
  "definitions": "How to settle the young driver fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the young driver fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 }
]
