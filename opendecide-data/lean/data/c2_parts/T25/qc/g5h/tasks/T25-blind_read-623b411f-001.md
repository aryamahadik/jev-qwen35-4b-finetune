# G5-H blind read T25-blind_read-623b411f-001 (family T25)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T25/qc/g5h/answers/T25-blind_read-623b411f-001.json

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
  "qid": "qcea5df8449",
  "kind": "choice",
  "text": "requested_by: Ansgar Holm\nnote: student looking into it\norganisation: Halsey Study Centre\ntopic: the private lesson price\n\nSources on the private lesson price:\n- Source S-99: pop up message; tier cobalt; dated 2026-05-12; independent. It states the private lesson price is $300.00.\n- Source S-36: queue sign; tier cobalt; dated 2026-06-28; copied from Source S-99. It states the private lesson price is $300.00.\n- Source S-34: photo caption; tier copper; dated 2026-05-13; independent. It states the private lesson price is $250.00.",
  "question": "How to settle the private lesson price from the listed sources:\n- Tiers, most reliable first: cobalt; then nickel; then copper.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the private lesson price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which value for the private lesson price is settled from the listed sources?",
  "options": [
   "$250.00",
   "$300.00",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q68580722fb",
  "kind": "yes/no",
  "text": "Subject: Lookup on the race entry fee\nHi team,\nFreja Nyberg is on the staff and is busy getting to grips with Hawthorne Walk-In Clinic. The pasted material below is there for a quick read.\nThanks,\n\nSource table for the race entry fee:\nsource | name | tier | dated | origin | stated value\nS-54 | mobile screen | autumn | Sunday, 3 May 2026 | copied from S-99 | $15.00\nS-32 | register extract | winter | Monday, 27 April 2026 | independent | $10.00\nS-84 | tooltip | winter | Monday, 27 April 2026 | copied from S-99 | $15.00\nS-99 | answerphone greeting | winter | Sunday, 26 April 2026 | independent | $15.00\nS-79 | handbook | winter | Monday, 20 April 2026 | independent | $10.00\n\nClaim to check: the race entry fee is $10.00.",
  "question": "Does the claim to check line up with the value the listed sources settle on under the stated rules?",
  "definitions": "How to settle the race entry fee from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the race entry fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q9fee432772",
  "kind": "choice",
  "text": "{\"requested_by\": \"Yuki Hayashi\", \"organisation\": \"Corrie Hall Institute\", \"topic\": \"the bicycle carriage charge\", \"note\": \"still finding my feet\"}\n\nSources on the bicycle carriage charge:\n- Source A: feed headline; tier scarlet; dated Wednesday, March 4, 2026; independent. It states the bicycle carriage charge is 15.00 USD.\n- Source B: flyer; tier scarlet; dated Thursday, April 16, 2026; copied from Source D. It states the bicycle carriage charge is 22.00 USD.\n- Source C: hold message; tier scarlet; dated Thursday, March 5, 2026; independent. It states the bicycle carriage charge is 18.00 USD.\n- Source D: poster; tier scarlet; dated Wednesday, March 5, 2025; independent. It states the bicycle carriage charge is 22.00 USD.\n- Source E: telephone menu; tier scarlet; dated Thursday, March 5, 2026; independent. It states the bicycle carriage charge is 18.00 USD.",
  "question": "How to settle the bicycle carriage charge from the listed sources:\n- Tiers, most reliable first: scarlet; then teal; then ochre.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the bicycle carriage charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, which value of the bicycle carriage charge do the listed sources settle on?",
  "options": [
   "18.00 USD",
   "22.00 USD",
   "15.00 USD"
  ]
 },
 {
  "qid": "q4ef21344fd",
  "kind": "choice",
  "text": "Requester: Yuki Hayashi\nTopic: the electronics drop-off deadline at Hallam Chess Club\nQueue: support handling\nI'm working through the request and have pasted what was found below.\n\nExcerpts on the electronics drop-off deadline:\n[A] inbox note, tier winter, dated May 25, 2025, independent: \"The electronics drop-off deadline is January 18, 2027.\"\n[B] rate card, tier winter, dated November 5, 2025, independent: \"The electronics drop-off deadline is April 2, 2026.\"\n[C] instruction card, tier autumn, dated August 6, 2025, independent: \"The electronics drop-off deadline is October 17, 2026.\"",
  "question": "How to settle the electronics drop-off deadline from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the electronics drop-off deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value does the fact end up with?",
  "options": [
   "January 18, 2027",
   "April 2, 2026",
   "October 17, 2026"
  ]
 },
 {
  "qid": "q72733cff39",
  "kind": "choice",
  "text": "requested_by: Adaeze Nwosu\nasked_via: member form\norganisation: Fernhill Housing Co-operative\ntopic: the parking charge\nnote: pasted material below\n\nSources on the parking charge:\n- Source S-67: blog entry; tier ganges; dated 26 Feb 2025; independent. It states the parking charge is $12.00.\n- Source S-94: megaphone call; tier ganges; dated 27 Feb 2025; independent. It states the parking charge is $6.00.\n- Source S-57: desk diary; tier ganges; dated 19 Feb 2025; independent. It states the parking charge is $15.00.\n- Source S-54: voice message; tier rhine; dated 25 Feb 2025; copied from Source S-13. It states the parking charge is $12.00.\n- Source S-13: news article; tier tigris; dated 25 Feb 2025; independent. It states the parking charge is $12.00.",
  "question": "How to settle the parking charge from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the parking charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich listed source is the value for the parking charge taken from under the stated rules?",
  "options": [
   "Source S-57",
   "Source S-94",
   "Source S-13",
   "No source: not determinable from reliable sources"
  ]
 },
 {
  "qid": "qab8e4fee09",
  "kind": "yes/no",
  "text": "teammate: Got your message, and the pasted lines below are what to work from.\nJiho Kang: Thanks, on it, the parking charge at Saltmarsh Exchange is the goal here.\n\nSources on the parking charge:\n- Source S-95: forum reply; tier tigris; dated May 23, 2026; independent. It states the parking charge is $12.00.\n- Source S-69: fee schedule; tier tigris; dated May 24, 2026; independent. It states the parking charge is $15.00.\n- Source S-53: door sign; tier rhine; dated May 24, 2026; copied from Source S-95. It states the parking charge is $12.00.\n- Source S-72: on-hold recording; tier rhine; dated May 25, 2026; independent. It states the parking charge is $3.00.\n\nClaim to check: the parking charge is $15.00.",
  "question": "According to the rules given, does the claim to check give the same value for the parking charge as the listed sources settle?",
  "definitions": "How to settle the parking charge from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the parking charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qf8436906cd",
  "kind": "choice",
  "text": "Maja Lindqvist: I need to get a reply out on the shoe hire charge at Halsey Study Centre and I am a bit rushed.\ncolleague: Pass me the extract and I will help you draft it.\ncolleague: Keep going, we are nearly through it.\n\nSources on the shoe hire charge:\n- Source S-39: register extract; tier birch; dated 27 May 2025; independent. It states the shoe hire charge is $4.00.\n- Source S-31: video caption; tier maple; dated 27 May 2026; independent. It states the shoe hire charge is $8.00.\n- Source S-46: shop window card; tier cedar; dated 22 Jul 2025; independent. It states the shoe hire charge is $3.50.\n- Source S-86: conference call; tier maple; dated 30 May 2025; independent. It states the shoe hire charge is $3.50.",
  "question": "How to settle the shoe hire charge from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the shoe hire charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which value for the shoe hire charge is settled from the listed sources?",
  "options": [
   "$3.50",
   "$4.00",
   "$8.00"
  ]
 },
 {
  "qid": "q1d7eb6c83b",
  "kind": "choice",
  "text": "Title: looking into the term start date at Saltmarsh Exchange\nRequester: Tariq Mansour\nTeam: student services\nPasted material is attached.\n\nExcerpts on the term start date:\n[S-78] counter sign, tier lute, dated 25 March 2025, independent: \"The term start date is 11 May 2027.\"\n[S-62] sandwich board, tier lute, dated 25 March 2024, independent: \"The term start date is 21 June 2027.\"\n[S-21] flyer, tier viola, dated 5 July 2025, independent: \"The term start date is 6 October 2026.\"\n[S-70] email message, tier lute, dated 25 March 2025, copied from S-62: \"The term start date is 21 June 2027.\"",
  "question": "How to settle the term start date from the listed sources:\n- Tiers, most reliable first: harp; then lute; then viola.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the term start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, what does the fact come to under the stated rules?",
  "options": [
   "6 October 2026",
   "21 June 2027",
   "11 May 2027"
  ]
 },
 {
  "qid": "q3a7bf4a6f4",
  "kind": "choice",
  "text": "{\"requested_by\": \"Amir Castellano\", \"organisation\": \"Crestline Climbing Gym\", \"topic\": \"the private lesson price\", \"channel\": \"front desk\"}\n\nSources on the private lesson price:\n- Source S-32: news article; tier nickel; dated 21 July 2026; independent. It states the private lesson price is $200.00.\n- Source S-48: telephone menu; tier copper; dated 25 May 2026; independent. It states the private lesson price is $120.00.\n- Source S-35: information sheet; tier copper; dated 1 June 2026; copied from Source S-48. It states the private lesson price is $120.00.\n- Source S-78: lobby poster; tier cobalt; dated 1 June 2026; independent. It states the private lesson price is $120.00.",
  "question": "How to settle the private lesson price from the listed sources:\n- Tiers, most reliable first: cobalt; then nickel; then copper.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the private lesson price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which source do the stated rules take the fact's value from?",
  "options": [
   "Source S-78",
   "Source S-48",
   "Source S-32"
  ]
 },
 {
  "qid": "q8af4500ac5",
  "kind": "yes/no",
  "text": "Dragana Petrovic: Tidying records as we speak, and looking at the plant sale date at Saltmarsh Exchange too.\nteammate: Brilliant, grabbing the notes below.\nsupport: Fine by me, thanks.\n\nExcerpts on the plant sale date:\n[S-60] meeting minutes, tier ganges, dated Friday, January 16, 2026, independent: \"The plant sale date is Friday, February 20, 2026.\"\n[S-44] transaction history, tier tigris, dated Sunday, January 18, 2026, independent: \"The plant sale date is Friday, April 23, 2027.\"\n[S-81] desk diary, tier ganges, dated Saturday, January 17, 2026, independent: \"The plant sale date is Friday, February 20, 2026.\"\n[S-23] on-hold recording, tier ganges, dated Saturday, January 17, 2026, independent: \"The plant sale date is Friday, February 20, 2026.\"\n\nClaim to check: the plant sale date is Friday, April 23, 2027.",
  "question": "According to the rules given, does the claim to check match the value of the plant sale date that the listed sources settle on?",
  "definitions": "How to settle the plant sale date from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the plant sale date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qb6c447bce3",
  "kind": "choice",
  "text": "Sunil Dhawan, acting as a member, looked into the entry price at Hallam Chess Club. The extract pasted in alongside it was read in a careful and orderly way. Readers who need the same check can use this route. Thank you for your attention.\n\nSources on the entry price:\n- Source A: record card; tier maple; dated 14 Aug 2025; independent. It states the entry price is $28.00.\n- Source B: settings screen; tier maple; dated 15 Aug 2025; copied from Source D. It states the entry price is $32.00.\n- Source C: guide booklet; tier birch; dated 14 Aug 2025; copied from Source D. It states the entry price is $32.00.\n- Source D: feed headline; tier maple; dated 14 Aug 2025; independent. It states the entry price is $32.00.",
  "question": "How to settle the entry price from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the entry price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which value for the entry price is settled from the listed sources?",
  "options": [
   "$28.00",
   "$32.00",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q1c746b3c9c",
  "kind": "yes/no",
  "text": "Elena Marchetti: Quick ask at the front desk about the rural route price at Garrow Cab Company, with the gathered material pasted below.\nsupport: Got it, stand by.\ndesk: Happy to help.\n\nSources on the rural route price:\n- Source A: poster; tier wynn; dated April 8, 2026; independent. It states the rural route price is $5.00.\n- Source B: filing cabinet folder; tier wynn; dated April 7, 2026; independent. It states the rural route price is $5.00.\n- Source C: ledger entry; tier wynn; dated April 7, 2026; independent. It states the rural route price is $5.00.\n- Source D: window notice; tier yogh; dated April 14, 2026; independent. It states the rural route price is $2.00.\n\nClaim to check: the rural route price is $5.00.",
  "question": "Does the claim to check agree with the rural route price value that the listed sources yield under the stated rules?",
  "definitions": "How to settle the rural route price from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the rural route price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qfaf940eb61",
  "kind": "yes/no",
  "text": "Internal memo: Farhan Qureshi is a student in a bit of a flap about the registration fee at Corrie Hall Institute. Pasted material is below, ready to read.\n\nSources on the registration fee:\n- Source A: hold message; tier hail; dated 14 January 2026; independent. It states the registration fee is $350.00.\n- Source B: conference call; tier sleet; dated 14 January 2026; independent. It states the registration fee is $250.00.\n- Source C: social post; tier hail; dated 5 April 2026; independent. It states the registration fee is $250.00.\n- Source D: postal notice; tier hail; dated 14 January 2026; independent. It states the registration fee is $350.00.\n- Source E: pamphlet; tier fog; dated 21 January 2026; copied from Source D. It states the registration fee is $350.00.\n\nClaim to check: the registration fee is $350.00.",
  "question": "Going by the listed sources, is the claim to check incorrect about the fact under the stated rules?",
  "definitions": "How to settle the registration fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qd55d7d0550",
  "kind": "yes/no",
  "text": "teammate: Lovely, the young driver fee at Hollin Corner Bazaar is what we are after.\nYuki Hayashi: Great, thanks. The pasted list below is what got dug up.\ndesk: Cheers for pulling it together, that is a big help.\n\nSources on the young driver fee:\n- Source S-80: flyer; tier sleet; dated 1 Oct 2025; independent. It states the young driver fee is $40.00.\n- Source S-12: counter sign; tier fog; dated 3 Oct 2025; copied from Source S-94. It states the young driver fee is $50.00.\n- Source S-23: transaction history; tier sleet; dated 1 Oct 2025; independent. It states the young driver fee is $40.00.\n- Source S-73: poster; tier sleet; dated 30 Sep 2025; independent. It states the young driver fee is $60.00.\n- Source S-94: mobile screen; tier hail; dated 2 Oct 2025; independent. It states the young driver fee is $50.00.\n\nClaim to check: the young driver fee is $50.00.",
  "question": "Does the claim to check for the young driver fee give the same value that the listed sources yield under the stated rules?",
  "definitions": "How to settle the young driver fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the young driver fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qfc3109d23a",
  "kind": "yes/no",
  "text": "Wei Zhang: Writing in as a member regarding the padlock price at Wexcombe Hospice.\nclerk: Thank you for writing in.\nclerk: The pasted material below is set out for your review.\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | telephone menu | hail | May 29, 2025 | independent | $12.00\nB | instant message | sleet | May 27, 2025 | independent | $18.00\nC | video caption | sleet | May 28, 2025 | independent | $10.00\nD | footer text | sleet | May 21, 2025 | independent | $12.00\nE | photo caption | sleet | June 4, 2025 | copied from A | $12.00\n\nClaim to check: the padlock price is $10.00.",
  "question": "Applying the stated rules to these sources, does the claim to check reproduce the value the rules arrive at?",
  "definitions": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qd6218e9e53",
  "kind": "choice",
  "text": "teammate: Got your message, and the pasted lines below are what to work from.\nLucia Carvalho: Thanks, on it, the desk rental fee at Halsey Study Centre is the goal here.\n\nSources on the desk rental fee:\n- Source A: telephone menu; tier garnet; dated 9 May 2026; independent. It states the desk rental fee is $220.00.\n- Source B: letter; tier opal; dated 9 May 2026; independent. It states the desk rental fee is $150.00.\n- Source C: entrance sign; tier topaz; dated 3 Mar 2026; independent. It states the desk rental fee is $150.00.\n- Source D: handbook; tier opal; dated 8 May 2026; independent. It states the desk rental fee is $350.00.\n- Source E: social post; tier opal; dated 9 May 2026; independent. It states the desk rental fee is $150.00.",
  "question": "How to settle the desk rental fee from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the desk rental fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhat value for the desk rental fee do the listed sources yield under the rules given?",
  "options": [
   "$350.00",
   "$220.00",
   "$150.00"
  ]
 },
 {
  "qid": "qdd659c8069",
  "kind": "yes/no",
  "text": "Front desk memo:\nThis memo records that Kofi Mensah is working through a booking and wants the table fee at Linnet Savings Club set out clearly. The pasted material below is there for the desk to read.\n\nSources on the table fee:\n- Source S-72: hold message; tier yogh; dated 2 Aug 2025; independent. It states the table fee is $45.00.\n- Source S-15: car park sign; tier yogh; dated 10 Sep 2025; copied from Source S-25. It states the table fee is $60.00.\n- Source S-23: activity log; tier thorn; dated 3 Aug 2025; copied from Source S-72. It states the table fee is $45.00.\n- Source S-25: postal notice; tier yogh; dated 10 Sep 2025; independent. It states the table fee is $60.00.\n\nClaim to check: the table fee is $45.00.",
  "question": "Does the claim to check state an incorrect value for the table fee under the stated rules and the listed sources?",
  "definitions": "How to settle the table fee from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the table fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q5a0b212d4d",
  "kind": "choice",
  "text": "Subject: Quick check on the shoe hire charge at Harbourside Ferry Lines\nHi there,\nIdris Varga is sorting out a booking and is in a bit of a hurry, so the notes below are pulled together for you. Sorry to hurry you on it.\nThanks,\n\nSources on the shoe hire charge:\n- Source S-29: envelope insert; tier birch; dated 2025-01-30; independent. It states the shoe hire charge is 5.00 USD.\n- Source S-58: desk handout; tier birch; dated 2025-02-06; independent. It states the shoe hire charge is 7.00 USD.\n- Source S-25: on-hold recording; tier birch; dated 2025-02-05; independent. It states the shoe hire charge is 8.00 USD.\n- Source S-77: transaction history; tier birch; dated 2025-02-06; independent. It states the shoe hire charge is 4.00 USD.\n- Source S-39: station announcement; tier birch; dated 2026-02-06; copied from Source S-25. It states the shoe hire charge is 8.00 USD.",
  "question": "How to settle the shoe hire charge from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the shoe hire charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value for the fact do the rules settle on?",
  "options": [
   "4.00 USD",
   "7.00 USD",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q1e2e282403",
  "kind": "yes/no",
  "text": "Subject: planning a visit\nGood day,\nThandiwe Morrow is planning a visit and wants to be clear on the private lesson price at Stonechat Park before arriving. The gathered material is pasted below for reference.\nYours sincerely,\n\nSources on the private lesson price:\n- Source S-83: wall sign; tier copper; dated 6 Sep 2025; independent. It states the private lesson price is 300.00 USD.\n- Source S-29: system log; tier nickel; dated 24 Aug 2025; independent. It states the private lesson price is 250.00 USD.\n- Source S-65: video caption; tier cobalt; dated 26 May 2025; independent. It states the private lesson price is 300.00 USD.\n- Source S-62: queue sign; tier cobalt; dated 27 May 2025; independent. It states the private lesson price is 200.00 USD.\n- Source S-16: window notice; tier cobalt; dated 24 Aug 2025; copied from Source S-29. It states the private lesson price is 250.00 USD.\n\nClaim to check: the private lesson price is 300.00 USD.",
  "question": "Does the claim to check match the value that the stated rules settle on from the listed sources?",
  "definitions": "How to settle the private lesson price from the listed sources:\n- Tiers, most reliable first: cobalt; then nickel; then copper.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the private lesson price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q59766cb328",
  "kind": "yes/no",
  "text": "{\"requested_by\": \"Ananya Iyer\", \"organisation\": \"Larchwood Park\", \"topic\": \"the consultation fee\", \"channel\": \"front desk\", \"note\": \"the pasted list below was gathered for this\"}\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-84 | news article | uranus | 10 Mar 2025 | copied from S-29 | $50.00\nS-52 | meeting minutes | pluto | 28 Apr 2025 | independent | $50.00\nS-29 | tooltip | jupiter | 12 Feb 2025 | independent | $50.00\nS-24 | settings screen | uranus | 10 Mar 2025 | independent | $85.00\n\nClaim to check: the consultation fee is $50.00.",
  "question": "According to the rules given, does the claim to check for the consultation fee state the same value the rules settle on from the listed sources?",
  "definitions": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qbe7b83a6eb",
  "kind": "choice",
  "text": "Yasmin Khoury: Quick word about the desk rental fee at Stonechat Park, since things are busy.\nclerk: Sure, go on then.\nclerk: The material is below, so read it at speed.\n\nSources on the desk rental fee:\n- Source A: case file; tier topaz; dated 26 Mar 2026; copied from Source B. It states the desk rental fee is $300.00.\n- Source B: spoken reminder; tier topaz; dated 16 Dec 2025; independent. It states the desk rental fee is $300.00.\n- Source C: video caption; tier garnet; dated 23 Dec 2025; independent. It states the desk rental fee is $180.00.",
  "question": "How to settle the desk rental fee from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the desk rental fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value of the fact do the rules settle on?",
  "options": [
   "$180.00",
   "$300.00",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q9a055c1b5d",
  "kind": "choice",
  "text": "desk: Thank you for getting in touch about the electronics drop-off deadline at Brookhollow Folk Club.\nFarhan Qureshi: Of course. The notes gathered below are set out in order for you.\nsupport: That helps, thank you.\n\nExcerpts on the electronics drop-off deadline:\n[A] social post, tier winter, dated 16 November 2025, independent: \"The electronics drop-off deadline is 22 May 2027.\"\n[B] footer text, tier winter, dated 22 November 2025, independent: \"The electronics drop-off deadline is 22 May 2027.\"\n[C] information sheet, tier winter, dated 23 November 2025, copied from B: \"The electronics drop-off deadline is 22 May 2027.\"\n[D] catalogue, tier winter, dated 23 November 2025, independent: \"The electronics drop-off deadline is 25 March 2026.\"",
  "question": "How to settle the electronics drop-off deadline from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the electronics drop-off deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value do the listed sources settle on for the fact, according to the stated rules?",
  "options": [
   "25 March 2026",
   "Not determinable from reliable sources",
   "22 May 2027"
  ]
 },
 {
  "qid": "q50bbbb3f08",
  "kind": "choice",
  "text": "organisation: Marrowdown Arts Festival\nrequested_by: Maja Lindqvist\ntopic: the season registration fee\nchannel: parent booking\nnote: material pasted below\n\nSource table for the season registration fee:\nsource | name | tier | dated | origin | stated value\nA | queue sign | rhine | 5 Oct 2025 | independent | $50.00\nB | register extract | ganges | 7 Jul 2025 | independent | $40.00\nC | landing page | ganges | 7 Jul 2025 | copied from E | $50.00\nD | voice message | ganges | 5 Jul 2025 | independent | $60.00\nE | activity log | ganges | 6 Jul 2025 | independent | $50.00",
  "question": "How to settle the season registration fee from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the season registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, which listed source supplies the value for the season registration fee?",
  "options": [
   "Source B",
   "Source A",
   "No source: not determinable from reliable sources"
  ]
 },
 {
  "qid": "qfe4880506b",
  "kind": "yes/no",
  "text": "Fionnuala Doyle: Hi again, sorting the booking and the consultation fee at Linnet Savings Club!\ndesk: Lovely, the lines pasted underneath are a good start.\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-29 | poster | pluto | March 31, 2026 | independent | $95.00\nS-34 | feed item | jupiter | May 16, 2026 | copied from S-29 | $95.00\nS-98 | account page | pluto | June 12, 2026 | copied from S-79 | $45.00\nS-79 | conference call | jupiter | April 1, 2026 | independent | $45.00\nS-20 | forum reply | jupiter | March 30, 2026 | independent | $95.00\n\nClaim to check: the consultation fee is $95.00.",
  "question": "Does the claim to check match the value for the consultation fee the listed sources give under the stated rules?",
  "definitions": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q69cea1925f",
  "kind": "choice",
  "text": "Title | Reply prep for the electronics drop-off deadline at Lowmoor Heath Gardens\nRequester | Adaeze Nwosu\nTeam | customer care\nMaterial for the reply is pasted below.\n\nExcerpts on the electronics drop-off deadline:\n[A] poster, tier winter, dated 18 March 2026, independent: \"The electronics drop-off deadline is 23 February 2027.\"\n[B] board notice, tier autumn, dated 25 March 2026, copied from A: \"The electronics drop-off deadline is 23 February 2027.\"\n[C] activity log, tier autumn, dated 25 March 2026, independent: \"The electronics drop-off deadline is 24 October 2026.\"",
  "question": "How to settle the electronics drop-off deadline from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the electronics drop-off deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, what value for the electronics drop-off deadline is settled by the listed sources?",
  "options": [
   "23 February 2027",
   "Not determinable from reliable sources",
   "24 October 2026"
  ]
 },
 {
  "qid": "q11b5a750f9",
  "kind": "yes/no",
  "text": "Desk memo: Felix Okonjo joined the team a short while back and is getting the hang of things. Looking into the registration fee at Haverley Lending Circle was a good way to learn the ropes, and the notes gathered below are a handy start.\n\nSources on the registration fee:\n- Source A: profile post; tier sleet; dated 26 June 2026; copied from Source D. It states the registration fee is $300.00.\n- Source B: footer text; tier hail; dated 15 July 2025; independent. It states the registration fee is $275.00.\n- Source C: call centre script; tier sleet; dated 26 June 2025; independent. It states the registration fee is $150.00.\n- Source D: forum reply; tier hail; dated 4 July 2025; independent. It states the registration fee is $300.00.\n\nClaim to check: the registration fee is $300.00.",
  "question": "Is the value in the claim to check for the registration fee the same as the listed sources settle on under the stated rules?",
  "definitions": "How to settle the registration fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qf3fcda4798",
  "kind": "yes/no",
  "text": "Nikos Papadakis: Hi, quick word, pinning down the consultation fee at Stanhope Sailing Club before heading off.\ndesk: Sure, that is in the material pasted just below.\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-91 | text message | uranus | Monday, June 30, 2025 | independent | $45.00\nS-98 | wall calendar | uranus | Sunday, June 29, 2025 | independent | $60.00\nS-38 | photo caption | uranus | Monday, June 30, 2025 | copied from S-27 | $50.00\nS-27 | reply letter | jupiter | Monday, June 23, 2025 | independent | $50.00\nS-14 | entrance sign | uranus | Sunday, June 29, 2025 | independent | $60.00\n\nClaim to check: the consultation fee is $45.00.",
  "question": "Applying the stated rules to these sources, does the claim to check match the figure they settle on?",
  "definitions": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qf6ae524554",
  "kind": "choice",
  "text": "{\"requested_by\": \"Yaw Ofori\", \"organisation\": \"Millrace Credit Union\", \"topic\": \"the table fee\", \"note\": \"planning ahead\"}\n\nSources on the table fee:\n- Source S-92: telephone menu; tier thorn; dated May 19, 2025; independent. It states the table fee is 60.00 USD.\n- Source S-93: brochure; tier thorn; dated May 19, 2026; independent. It states the table fee is 25.00 USD.\n- Source S-84: email message; tier thorn; dated July 9, 2026; copied from Source S-93. It states the table fee is 25.00 USD.",
  "question": "How to settle the table fee from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the table fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which value of the table fee do the listed sources land on?",
  "options": [
   "Not determinable from reliable sources",
   "25.00 USD",
   "60.00 USD"
  ]
 },
 {
  "qid": "q2718674b23",
  "kind": "choice",
  "text": "Dear colleague,\nMy name is Abena Boateng and I am writing to look into the padlock price at Quarry Lane Debating Society. I have pasted what was found below for your reference. Thank you for your help on this matter.\nKind regards,\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | window notice | hail | Tuesday, 2 September 2025 | independent | $15.00\nB | record card | hail | Wednesday, 1 October 2025 | independent | $10.00\nC | postal notice | fog | Monday, 24 November 2025 | copied from B | $10.00\nD | fee schedule | fog | Monday, 24 November 2025 | copied from B | $10.00\nE | video caption | fog | Sunday, 23 November 2025 | independent | $25.00",
  "question": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value of the fact do the listed sources settle on under the stated rules?",
  "options": [
   "$25.00",
   "Not determinable from reliable sources",
   "$10.00"
  ]
 },
 {
  "qid": "qda2fd252d0",
  "kind": "choice",
  "text": "Help centre entry: Keiko Lindgren looked into the document request deadline at Hadley Bike Works by reading through the gathered material and setting it out in pasted form. This entry records the approach that was taken.\n\nExcerpts on the document request deadline:\n[S-87] appointment card, tier cumin, dated Saturday, January 17, 2026, copied from S-61: \"The document request deadline is Monday, November 16, 2026.\"\n[S-61] lobby poster, tier clove, dated Wednesday, September 24, 2025, independent: \"The document request deadline is Monday, November 16, 2026.\"\n[S-39] spoken reminder, tier clove, dated Wednesday, September 24, 2025, independent: \"The document request deadline is Friday, June 5, 2026.\"",
  "question": "How to settle the document request deadline from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the document request deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nWhich value do the listed sources settle on for the fact, according to the stated rules?",
  "options": [
   "Monday, November 16, 2026",
   "Friday, June 5, 2026",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "q6f47b82f74",
  "kind": "choice",
  "text": "Title: the rural route price at Fennel Hollow Gardens\nRequester: Abena Boateng\nTeam: volunteers\nHelp is lined up with the pasted material below.\n\nSources on the rural route price:\n- Source A: social post; tier wynn; dated Friday, 17 October 2025; independent. It states the rural route price is 1.50 USD.\n- Source B: profile post; tier wynn; dated Tuesday, 21 October 2025; copied from Source D. It states the rural route price is 4.00 USD.\n- Source C: poster; tier wynn; dated Saturday, 18 October 2025; independent. It states the rural route price is 3.00 USD.\n- Source D: forum reply; tier wynn; dated Saturday, 18 October 2025; independent. It states the rural route price is 4.00 USD.\n- Source E: lobby poster; tier wynn; dated Friday, 17 October 2025; independent. It states the rural route price is 1.50 USD.",
  "question": "How to settle the rural route price from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the rural route price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, what value of the fact is fixed by the stated rules?",
  "options": [
   "4.00 USD",
   "Not determinable from reliable sources",
   "3.00 USD"
  ]
 },
 {
  "qid": "q01a634683d",
  "kind": "yes/no",
  "text": "Subject: Routine look at the express surcharge for Ridgeway Swim Club\nHello,\nKofi Mensah is writing from support on a routine matter. The material gathered below is pasted in as it stands.\nKind regards,\n\nSource table for the express surcharge:\nsource | name | tier | dated | origin | stated value\nA | pricing page | robin | 18 June 2026 | copied from B | $5.00\nB | car park sign | robin | 11 June 2026 | independent | $5.00\nC | flyer | sparrow | 2 September 2026 | independent | $12.00\nD | application form | robin | 18 June 2026 | independent | $12.00\nE | register extract | robin | 11 June 2026 | independent | $5.00\n\nClaim to check: the express surcharge is $5.00.",
  "question": "Under the stated rules, is the claim to check wrong about the express surcharge given the listed sources?",
  "definitions": "How to settle the express surcharge from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the express surcharge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qca26a64830",
  "kind": "yes/no",
  "text": "title: Booking query on the document request deadline at Ormsby Mart\nrequester: Mateo Quiroga\nteam: front desk\nThe notes gathered below tie in with the booking.\n\nExcerpts on the document request deadline:\n[S-30] case file, tier clove, dated Monday, 22 December 2025, copied from S-94: \"The document request deadline is Thursday, 16 July 2026.\"\n[S-78] shop window card, tier clove, dated Thursday, 15 January 2026, independent: \"The document request deadline is Thursday, 1 October 2026.\"\n[S-10] telephone menu, tier clove, dated Thursday, 15 January 2026, independent: \"The document request deadline is Thursday, 1 October 2026.\"\n[S-94] programme, tier clove, dated Tuesday, 9 December 2025, independent: \"The document request deadline is Thursday, 16 July 2026.\"\n\nClaim to check: the document request deadline is Thursday, 16 July 2026.",
  "question": "Applying the stated rules to these sources, does the claim to check reproduce the value the rules arrive at?",
  "definitions": "How to settle the document request deadline from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the document request deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qb91ee503cf",
  "kind": "choice",
  "text": "Sofia Benitez: Greetings to the team. The padlock price at Brightwater Physio Clinic is the matter at hand, and the material gathered is pasted in for your review.\ndesk: Thank you for the note, the material is received.\nsupport: Set the material aside for the review.\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | wall sign | fog | Saturday, 31 May 2025 | independent | $20.00\nB | envelope insert | fog | Saturday, 31 May 2025 | independent | $18.00\nC | fee schedule | sleet | Saturday, 24 May 2025 | independent | $15.00\nD | info pack | fog | Sunday, 31 May 2026 | copied from B | $18.00",
  "question": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which value do the stated rules settle on for this fact?",
  "options": [
   "$18.00",
   "Not determinable from reliable sources",
   "$20.00"
  ]
 },
 {
  "qid": "q30007a4930",
  "kind": "choice",
  "text": "Ilinca Dobre: hiya, just wondering about the rural route price at Meadowbank Dental Practice.\nagent: lovely, let me look at what came in.\nclerk: the gathered material is pasted in just after this, so have a read.\n\nSources on the rural route price:\n- Source A: footer text; tier wynn; dated Friday, 7 November 2025; copied from Source B. It states the rural route price is $4.00.\n- Source B: portal page; tier wynn; dated Thursday, 6 November 2025; independent. It states the rural route price is $4.00.\n- Source C: email message; tier yogh; dated Friday, 7 November 2025; independent. It states the rural route price is $4.00.\n- Source D: queue sign; tier wynn; dated Thursday, 6 November 2025; independent. It states the rural route price is $2.50.",
  "question": "How to settle the rural route price from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the rural route price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which value of the fact is settled under the stated rules?",
  "options": [
   "$2.50",
   "Not determinable from reliable sources",
   "$4.00"
  ]
 },
 {
  "qid": "qaafd778bae",
  "kind": "yes/no",
  "text": "Mei Huang: Hello. Writing in about the season registration fee at Brightwater Physio Clinic, with the material gathered so far.\nclerk: Thank you for getting in touch. Please take a look at the list below.\nclerk: The material below is what turned up on this.\n\nSource table for the season registration fee:\nsource | name | tier | dated | origin | stated value\nA | summary sheet | tigris | 2026-01-08 | independent | $60.00\nB | entrance sign | tigris | 2026-01-07 | independent | $50.00\nC | poster | tigris | 2026-01-07 | independent | $100.00\nD | on-hold recording | tigris | 2027-01-08 | copied from B | $50.00\nE | rate card | rhine | 2026-03-31 | independent | $40.00\n\nClaim to check: the season registration fee is $60.00.",
  "question": "Going by the listed sources, is the claim to check consistent with the value the stated rules settle on?",
  "definitions": "How to settle the season registration fee from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the season registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q0c7518a031",
  "kind": "yes/no",
  "text": "Subject: Quick note about the shoe hire charge at Brookhollow Folk Club\nHi there,\nJiho Kang is helping out at speed and has the notes below ready to pass along. Sorry for the rush.\nThanks again,\n\nSources on the shoe hire charge:\n- Source S-91: comment thread; tier maple; dated Tuesday, October 21, 2025; independent. It states the shoe hire charge is 7.00 USD.\n- Source S-85: shop window card; tier cedar; dated Friday, August 1, 2025; independent. It states the shoe hire charge is 3.00 USD.\n- Source S-20: info pack; tier maple; dated Monday, October 20, 2025; independent. It states the shoe hire charge is 5.00 USD.\n\nClaim to check: the shoe hire charge is 7.00 USD.",
  "question": "Under the stated rules, is the value settled for the shoe hire charge other than the value in the claim to check?",
  "definitions": "How to settle the shoe hire charge from the listed sources:\n- Tiers, most reliable first: birch; then maple; then cedar.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the shoe hire charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q76da882fd5",
  "kind": "choice",
  "text": "Help centre entry: Oksana Bondar dug into the fitness orientation start date at Wexcombe Hospice for a class project, sorting through the pasted material below. It was a bit of a puzzle and great fun to tackle.\n\nExcerpts on the fitness orientation start date:\n[A] price list, tier denim, dated 30 Apr 2025, independent: \"The fitness orientation start date is 26 Jan 2026.\"\n[B] programme, tier linen, dated 30 Apr 2025, independent: \"The fitness orientation start date is 3 Feb 2026.\"\n[C] voice message, tier linen, dated 29 Apr 2025, independent: \"The fitness orientation start date is 25 Jan 2027.\"",
  "question": "How to settle the fitness orientation start date from the listed sources:\n- Tiers, most reliable first: wool; then linen; then denim.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the fitness orientation start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which value of the fact is settled under the stated rules?",
  "options": [
   "3 Feb 2026",
   "25 Jan 2027",
   "26 Jan 2026"
  ]
 },
 {
  "qid": "q687f156d74",
  "kind": "choice",
  "text": "requested_by: Freja Nyberg\nteam: records tidy-up\norganisation: Hallam Chess Club\ntopic: the late return fee\nnote: material pasted below\n\nSources on the late return fee:\n- Source S-75: mobile screen; tier robin; dated November 29, 2025; copied from Source S-98. It states the late return fee is $10.00.\n- Source S-76: programme; tier robin; dated November 28, 2025; copied from Source S-98. It states the late return fee is $10.00.\n- Source S-53: desk handout; tier robin; dated November 28, 2025; independent. It states the late return fee is $15.00.\n- Source S-98: station announcement; tier robin; dated November 27, 2025; independent. It states the late return fee is $10.00.",
  "question": "How to settle the late return fee from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the late return fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, what value of the fact comes out as the settled answer?",
  "options": [
   "$15.00",
   "Not determinable from reliable sources",
   "$10.00"
  ]
 },
 {
  "qid": "qd42a4a49b8",
  "kind": "yes/no",
  "text": "Eleanor Farrant is settling into the role at Quayside Lettings Office and needs to look at the desk rental fee in a hurry. The extract is pasted in here for the team's use. Please pick this up when you get a moment.\n\nSources on the desk rental fee:\n- Source A: letter; tier opal; dated Friday, 7 March 2025; independent. It states the desk rental fee is $150.00.\n- Source B: megaphone call; tier garnet; dated Friday, 28 February 2025; independent. It states the desk rental fee is $150.00.\n- Source C: info pack; tier opal; dated Friday, 14 March 2025; copied from Source A. It states the desk rental fee is $150.00.\n- Source D: pop up message; tier opal; dated Wednesday, 13 November 2024; independent. It states the desk rental fee is $350.00.\n- Source E: lobby poster; tier topaz; dated Monday, 9 December 2024; independent. It states the desk rental fee is $280.00.\n\nClaim to check: the desk rental fee is $150.00.",
  "question": "Is the claim to check inaccurate under the stated rules and the listed sources?",
  "definitions": "How to settle the desk rental fee from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the desk rental fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q46682610c3",
  "kind": "yes/no",
  "text": "Ananya Iyer: Thank you for taking this call about the bicycle carriage charge at Quarry Lane Debating Society.\nagent: Certainly, that is in hand.\nagent: What was found is pasted below.\n\nSources on the bicycle carriage charge:\n- Source A: entrance sign; tier teal; dated Sunday, 27 July 2025; independent. It states the bicycle carriage charge is 18.00 USD.\n- Source B: site banner; tier teal; dated Monday, 28 July 2025; independent. It states the bicycle carriage charge is 15.00 USD.\n- Source C: portal page; tier ochre; dated Monday, 14 July 2025; independent. It states the bicycle carriage charge is 22.00 USD.\n- Source D: summary sheet; tier ochre; dated Tuesday, 29 July 2025; independent. It states the bicycle carriage charge is 22.00 USD.\n- Source E: wall calendar; tier teal; dated Sunday, 27 July 2025; independent. It states the bicycle carriage charge is 22.00 USD.\n\nClaim to check: the bicycle carriage charge is 22.00 USD.",
  "question": "Going by the listed sources, is the claim to check wrong under the stated rules?",
  "definitions": "How to settle the bicycle carriage charge from the listed sources:\n- Tiers, most reliable first: scarlet; then teal; then ochre.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the bicycle carriage charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qc0e69a9df2",
  "kind": "choice",
  "text": "Office memo: Yaw Ofori is planning ahead and wants the electronics drop-off deadline at Thimble Lane Evening Classes written down. The material pasted below is set out for that.\n\nExcerpts on the electronics drop-off deadline:\n[A] filing cabinet folder, tier spring, dated 2025-10-28, independent: \"The electronics drop-off deadline is 2026-08-23.\"\n[B] spoken reminder, tier autumn, dated 2025-11-11, copied from C: \"The electronics drop-off deadline is 2026-09-29.\"\n[C] desk handout, tier autumn, dated 2025-11-04, independent: \"The electronics drop-off deadline is 2026-09-29.\"",
  "question": "How to settle the electronics drop-off deadline from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the electronics drop-off deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which source do the stated rules draw the value from?",
  "options": [
   "Source B",
   "Source A",
   "No source: not determinable from reliable sources"
  ]
 },
 {
  "qid": "q19ac1a00fa",
  "kind": "yes/no",
  "text": "organisation: Haldane Travel Express\nrequested_by: Mateo Quiroga\ntopic: registration fee\nchannel: reply desk\nasked_via: pasted material below\n\nSources on the registration fee:\n- Source A: summary sheet; tier hail; dated Friday, 24 October 2025; independent. It states the registration fee is $250.00.\n- Source B: tooltip; tier sleet; dated Friday, 24 October 2025; independent. It states the registration fee is $180.00.\n- Source C: entrance sign; tier sleet; dated Friday, 31 October 2025; copied from Source A. It states the registration fee is $250.00.\n\nClaim to check: the registration fee is $180.00.",
  "question": "Does the claim to check match the value for the registration fee the listed sources give under the stated rules?",
  "definitions": "How to settle the registration fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q683d33a4ed",
  "kind": "choice",
  "text": "Dragana Petrovic: I am looking into the young driver fee at Hawthorne Walk-In Clinic and have the notes ready.\ndesk: Nice, drop them here.\nsupport: The material below covers it, so start there.\n\nSources on the young driver fee:\n- Source S-68: rate card; tier sleet; dated Wednesday, 15 October 2025; independent. It states the young driver fee is $60.00.\n- Source S-48: account page; tier hail; dated Thursday, 16 October 2025; independent. It states the young driver fee is $25.00.\n- Source S-77: receipt slip; tier hail; dated Saturday, 18 October 2025; copied from Source S-53. It states the young driver fee is $50.00.\n- Source S-80: call centre script; tier sleet; dated Thursday, 16 October 2025; independent. It states the young driver fee is $50.00.\n- Source S-53: shop window card; tier sleet; dated Friday, 17 October 2025; independent. It states the young driver fee is $50.00.",
  "question": "How to settle the young driver fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the young driver fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, what value of the fact is fixed by the stated rules?",
  "options": [
   "$60.00",
   "Not determinable from reliable sources",
   "$50.00"
  ]
 },
 {
  "qid": "qe7cc18a5f4",
  "kind": "yes/no",
  "text": "Support memo: Adaeze Nwosu has a request in about the consultation fee at Saltmarsh Exchange and is working through it steadily. Gathered material is pasted below, so get stuck in.\n\nSource table for the consultation fee:\nsource | name | tier | dated | origin | stated value\nS-48 | flyer | pluto | Tuesday, 15 July 2025 | independent | $95.00\nS-66 | printed notice | pluto | Saturday, 2 August 2025 | copied from S-48 | $95.00\nS-89 | call centre script | jupiter | Saturday, 9 August 2025 | independent | $120.00\nS-30 | handbook | jupiter | Saturday, 9 August 2025 | copied from S-69 | $85.00\nS-69 | queue sign | pluto | Saturday, 2 August 2025 | independent | $85.00\n\nClaim to check: the consultation fee is $95.00.",
  "question": "According to the rules given, does the claim to check for the consultation fee not hold against the listed sources?",
  "definitions": "How to settle the consultation fee from the listed sources:\n- Tiers, most reliable first: uranus; then pluto; then jupiter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the consultation fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q62b5e2ca6a",
  "kind": "choice",
  "text": "Farid Azizi: Tidying records at a steady pace, and the guided tour charge at Starling Cinema is the tricky bit.\nteammate: The gathered material is pasted below, so get it sorted.\ndesk: Give a shout when you want a hand.\n\nSource table for the guided tour charge:\nsource | name | tier | dated | origin | stated value\nA | conference call | cumin | Friday, September 26, 2025 | copied from D | $10.00\nB | pricing page | sumac | Friday, October 3, 2025 | independent | $20.00\nC | letter | sumac | Saturday, September 27, 2025 | independent | $10.00\nD | appointment card | cumin | Thursday, September 25, 2025 | independent | $10.00\nE | info pack | cumin | Friday, September 26, 2025 | independent | $15.00",
  "question": "How to settle the guided tour charge from the listed sources:\n- Tiers, most reliable first: cumin; then sumac; then clove.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the guided tour charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, what value do the stated rules settle on for the fact?",
  "options": [
   "$10.00",
   "$15.00",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "qd4440a8e66",
  "kind": "choice",
  "text": "Subject: Enquiry from a member\nHello there,\nAmir Castellano is writing in about the damage deposit at Oldbridge Language School. The gathered material follows as pasted text, and it helps pick up the thread.\nKind regards,\n\nSources on the damage deposit:\n- Source A: ledger entry; tier sparrow; dated Saturday, 21 March 2026; independent. It states the damage deposit is 400.00 USD.\n- Source B: video caption; tier sparrow; dated Saturday, 14 March 2026; independent. It states the damage deposit is 150.00 USD.\n- Source C: forum reply; tier finch; dated Monday, 8 June 2026; independent. It states the damage deposit is 150.00 USD.",
  "question": "How to settle the damage deposit from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the damage deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which value of the damage deposit do the listed sources land on?",
  "options": [
   "Not determinable from reliable sources",
   "150.00 USD",
   "400.00 USD"
  ]
 },
 {
  "qid": "qff80ee88ef",
  "kind": "yes/no",
  "text": "Logged by: Amir Castellano\nOrganisation: Lowmoor Heath Gardens\nTopic: the padlock price\nI am a member writing in and have pasted the extract here for the desk to look at.\n\nSource table for the padlock price:\nsource | name | tier | dated | origin | stated value\nA | forum reply | fog | 18 Aug 2025 | copied from B | $8.00\nB | receipt slip | hail | 16 Jun 2025 | independent | $8.00\nC | hold message | sleet | 29 Aug 2025 | independent | $20.00\nD | loudspeaker message | sleet | 24 Oct 2025 | copied from B | $8.00\n\nClaim to check: the padlock price is $20.00.",
  "question": "Under the stated rules, does the claim to check give the same value for the padlock price that the listed sources settle on?",
  "definitions": "How to settle the padlock price from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the padlock price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "q6fe8fcd2dd",
  "kind": "yes/no",
  "text": "Help centre entry: Meera Joshi went through the desk rental fee at Hawthorne Walk-In Clinic in a calm, routine way, using the material gathered below. The steps are set out in order, and the pasted details follow straight after.\n\nSources on the desk rental fee:\n- Source A: sandwich board; tier garnet; dated 2026-03-19; independent. It states the desk rental fee is 250.00 USD.\n- Source B: price list; tier garnet; dated 2026-03-19; independent. It states the desk rental fee is 180.00 USD.\n- Source C: pamphlet; tier topaz; dated 2026-03-18; independent. It states the desk rental fee is 180.00 USD.\n- Source D: pricing page; tier garnet; dated 2026-03-11; independent. It states the desk rental fee is 150.00 USD.\n- Source E: programme; tier topaz; dated 2026-03-17; independent. It states the desk rental fee is 250.00 USD.\n\nClaim to check: the desk rental fee is 250.00 USD.",
  "question": "Going by the listed sources, is the claim to check consistent with the value the stated rules settle on?",
  "definitions": "How to settle the desk rental fee from the listed sources:\n- Tiers, most reliable first: opal; then topaz; then garnet.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the desk rental fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 },
 {
  "qid": "qca39a1da75",
  "kind": "yes/no",
  "text": "Help centre entry: Busy desk, so Lucia Carvalho looked into the parking charge at Larchwood Park straight away and pasted the material below. A reply is being put together.\n\nSources on the parking charge:\n- Source S-49: summary sheet; tier rhine; dated 2025-03-03; independent. It states the parking charge is $3.00.\n- Source S-46: wall calendar; tier tigris; dated 2025-03-03; copied from Source S-49. It states the parking charge is $3.00.\n- Source S-65: hold message; tier rhine; dated 2025-03-02; independent. It states the parking charge is $15.00.\n- Source S-69: questions page; tier tigris; dated 2025-03-03; copied from Source S-65. It states the parking charge is $15.00.\n\nClaim to check: the parking charge is $3.00.",
  "question": "Applying the stated rules to these sources, does the claim to check hold the same value they settle on?",
  "definitions": "How to settle the parking charge from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the parking charge not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies."
 }
]
