# A61 DI-TS label-noise confirmation DTS-confirm-000 (Opus)

ANSWER FILE (write your whole answer here, with the Write tool, and nowhere else):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-TS/confirm/answers/DTS-confirm-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web.

Items: 40. Each item is a training row of a public-source dataset whose gold label was set by the dataset creator (program or crowd). Two blind readers disagreed with the gold (or one disagreed and the other abstained), and a first-pass reviewer called it wrong_gold or ambiguous. You rule on each row.

Verdicts: "wrong_gold" = a careful reader of the text, the options and the definitions would pick a different option than the gold; "ambiguous" = the row has no single defensible answer under the options and definitions, so it should not train the model; "gold_ok" = the gold is the defensible answer and the row stays. Rows are only dropped, never relabelled. Keep the bar: do not drop a row just because it is hard. Template-style rows (temporal, logic) may follow a convention that a careful reader would not infer from the text: if the text alone does not fix the gold, call it ambiguous.

Answer contract: one JSON array, one object per item: {"id": "<the item id>", "verdict": "gold_ok|wrong_gold|ambiguous", "reason": "<= 25 words"}. Exactly those keys, valid JSON only, no text before or after.

## Items
[
 {
  "id": "i7ad1d1981182c1",
  "text": "Statement 1: After Monday, he will leave his job.\nStatement 2: Before Sunday, he will leave his job.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.",
  "gold": "contradiction",
  "reader_A": "neutral",
  "reader_B": "neutral",
  "first_pass": "wrong_gold",
  "first_pass_reason": "after Monday and before Sunday is satisfiable (Tue-Sat), so neutral not contradiction"
 },
 {
  "id": "ia3f38943c04f41",
  "text": "Statement 1: The park was open at 11 AM.\nStatement 2: The park was open after 23:00.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.",
  "gold": "contradiction",
  "reader_A": "neutral",
  "reader_B": "neutral",
  "first_pass": "wrong_gold",
  "first_pass_reason": "open at 11 AM and open after 23:00 can both hold; not a contradiction"
 },
 {
  "id": "i7bb485cebb82b8",
  "text": "Statement 1: A tsunami hit the coast after Wednesday.\nStatement 2: A tsunami hit the coast before Sunday.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.",
  "gold": "contradiction",
  "reader_A": "neutral",
  "reader_B": "neutral",
  "first_pass": "wrong_gold",
  "first_pass_reason": "after Wednesday and before Sunday is satisfiable"
 },
 {
  "id": "ie6d37f43007d43",
  "text": "Statement 1: I will post this picture on Instagram after Tuesday.\nStatement 2: I will post this picture on Instagram before Sunday.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.",
  "gold": "contradiction",
  "reader_A": "neutral",
  "reader_B": "neutral",
  "first_pass": "wrong_gold",
  "first_pass_reason": "after Tuesday and before Sunday is satisfiable"
 },
 {
  "id": "iab552185ab9dea",
  "text": "Statement 1: Kendrick's album is set to drop after Saturday.\nStatement 2: Kendrick's album is set to drop before Thursday.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.",
  "gold": "contradiction",
  "reader_A": "neutral",
  "reader_B": "neutral",
  "first_pass": "ambiguous",
  "first_pass_reason": "weekday order is cyclic here; after Saturday before Thursday is reading dependent"
 },
 {
  "id": "i59245e8a0a7b66",
  "text": "Statement 1: I started my office leave after 02:00.\nStatement 2: I started my office leave before 00:00.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.",
  "gold": "contradiction",
  "reader_A": "neutral",
  "reader_B": "neutral",
  "first_pass": "ambiguous",
  "first_pass_reason": "after 02:00 and before 00:00 depends on whether the day wraps"
 },
 {
  "id": "i41283cea4632a5",
  "text": "Statement 1: The pleasant weather here started after January.\nStatement 2: The pleasant weather here started after Jan.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: The times in statement 1 settle that statement 2 is correct.",
  "gold": "neutral",
  "reader_A": "entailment",
  "reader_B": "entailment",
  "first_pass": "wrong_gold",
  "first_pass_reason": "Jan and January are the same month; the statements are equivalent"
 },
 {
  "id": "ifc6694fe32f0ae",
  "text": "Statement 1: I started working on my MS application before Oct.\nStatement 2: I started working on my MS application before October.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Statement 2 must be true whenever statement 1 is true.",
  "gold": "neutral",
  "reader_A": "entailment",
  "reader_B": "entailment",
  "first_pass": "wrong_gold",
  "first_pass_reason": "Oct and October are the same month; equivalent"
 },
 {
  "id": "i8e575d3f909c20",
  "text": "Statement 1: Before Wednesday, the prison sentence of that convict will end.\nStatement 2: After Tuesday, the prison sentence of that convict will end.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.",
  "gold": "neutral",
  "reader_A": "contradiction",
  "reader_B": "contradiction",
  "first_pass": "ambiguous",
  "first_pass_reason": "day granularity: before Wednesday and after Tuesday leaves no whole day; template convention"
 },
 {
  "id": "ieb7fb44446f3ce",
  "text": "Statement 1: My grandfather was born before March.\nStatement 2: My grandfather was born after February.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.",
  "gold": "neutral",
  "reader_A": "contradiction",
  "reader_B": "contradiction",
  "first_pass": "ambiguous",
  "first_pass_reason": "month granularity: before March vs after February leaves no whole month; template convention"
 },
 {
  "id": "ie6f35778191d2a",
  "text": "Statement 1: Before Friday, the spring quarter began.\nStatement 2: After Thursday, the spring quarter began.",
  "question": "Use ordinary calendar and clock knowledge (days of the week, months, AM and PM, before and after) to relate statement 2 to statement 1.",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.",
  "gold": "neutral",
  "reader_A": "contradiction",
  "reader_B": "contradiction",
  "first_pass": "ambiguous",
  "first_pass_reason": "before Friday vs after Thursday leaves no whole day; template convention"
 },
 {
  "id": "i9c9ff8d6a0fe5e",
  "text": "Statement 1: The tiger was last spotted after Nov.\nStatement 2: The tiger was last spotted before Dec.",
  "question": "Both statements talk about when something happens (a day, a date, a time of day or a month). Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment",
   "neutral"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.",
  "gold": "neutral",
  "reader_A": "contradiction",
  "reader_B": "contradiction",
  "first_pass": "ambiguous",
  "first_pass_reason": "after Nov vs before Dec leaves no whole month; template convention"
 },
 {
  "id": "i585093b2f3b49e",
  "text": "Statement 1: Before May, the Presidential election took place.\nStatement 2: After April, the Presidential election took place.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "entailment",
   "contradiction"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: The times in statement 1 rule out statement 2.",
  "gold": "neutral",
  "reader_A": "contradiction",
  "reader_B": "contradiction",
  "first_pass": "ambiguous",
  "first_pass_reason": "before May vs after April leaves no whole month; template convention"
 },
 {
  "id": "i719ae1d0bee4c1",
  "text": "Statement 1: Our favorite breakfast restaurant opened after September.\nStatement 2: Our favorite breakfast restaurant opened before October.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "entailment",
   "neutral",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 1 and statement 2 cannot both be true.",
  "gold": "neutral",
  "reader_A": "contradiction",
  "reader_B": "contradiction",
  "first_pass": "ambiguous",
  "first_pass_reason": "after September vs before October leaves no whole month; template convention"
 },
 {
  "id": "i6704e4fb478f17",
  "text": "Statement 1: The pandemic began before March.\nStatement 2: The pandemic began after February.",
  "question": "Statement 1 says when an event took place and statement 2 describes that time in another way. Choose the option that fits the pair.",
  "options": [
   "neutral",
   "contradiction",
   "entailment"
  ],
  "definitions": "- neutral: Statement 1 leaves open whether statement 2 is true or false.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.",
  "gold": "neutral",
  "reader_A": "contradiction",
  "reader_B": "contradiction",
  "first_pass": "ambiguous",
  "first_pass_reason": "before March vs after February leaves no whole month; template convention"
 },
 {
  "id": "i322bc69512a3c4",
  "text": "Statement 1: The city had a huge power outage before Saturday.\nStatement 2: The city had a huge power outage after Friday.",
  "question": "Work out from the days, dates or clock times whether statement 2 must hold, cannot hold or is left open by statement 1, and choose that option.",
  "options": [
   "entailment",
   "contradiction",
   "neutral"
  ],
  "definitions": "- entailment: The times in statement 1 settle that statement 2 is correct.\n- contradiction: Statement 2 cannot be true if statement 1 is true.\n- neutral: Both truth values of statement 2 are possible given statement 1.",
  "gold": "neutral",
  "reader_A": "contradiction",
  "reader_B": "contradiction",
  "first_pass": "ambiguous",
  "first_pass_reason": "before Saturday vs after Friday leaves no whole day; template convention"
 },
 {
  "id": "i28f8c11d0f62a4",
  "text": "Statement 1: After Friday, the country declared martial law.\nStatement 2: Before Saturday, the country declared martial law.",
  "question": "Compare the time named in statement 2 with the time given in statement 1. Which option describes their relation?",
  "options": [
   "contradiction",
   "neutral",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- neutral: The times in statement 1 neither confirm nor rule out statement 2.\n- entailment: The times in statement 1 settle that statement 2 is correct.",
  "gold": "neutral",
  "reader_A": "contradiction",
  "reader_B": "contradiction",
  "first_pass": "ambiguous",
  "first_pass_reason": "after Friday vs before Saturday leaves no whole day; template convention"
 },
 {
  "id": "i0b89dbde48a3c4",
  "text": "Statement 1: The coding competition was held from 22nd to 24th.\nStatement 2: The coding competition was held for 3 days.",
  "question": "Count the hours, days or months between the two times in statement 1, then judge the duration in statement 2 against that count.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: The times in statement 1 rule out statement 2.\n- entailment: Statement 2 must be true whenever statement 1 is true.",
  "gold": "contradiction",
  "reader_A": "entailment",
  "reader_B": "entailment",
  "first_pass": "ambiguous",
  "first_pass_reason": "inclusive vs exclusive span counting; gold follows one convention, natural reading differs"
 },
 {
  "id": "idcd5ebba0f2e65",
  "text": "Statement 1: The conference lasted from Thursday to Monday.\nStatement 2: The conference lasted for 5 days.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.",
  "gold": "contradiction",
  "reader_A": "entailment",
  "reader_B": "entailment",
  "first_pass": "ambiguous",
  "first_pass_reason": "inclusive vs exclusive span counting; gold follows one convention, natural reading differs"
 },
 {
  "id": "ic59b35753f7ce1",
  "text": "Statement 1: The park opens in October and closes in December.\nStatement 2: The park is open for 3 months.",
  "question": "Statement 2 states a duration, sometimes with 'less than' or 'more than'. Decide how it relates to the times in statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: If statement 1 is true, statement 2 is guaranteed to be false.",
  "gold": "contradiction",
  "reader_A": "entailment",
  "reader_B": "entailment",
  "first_pass": "ambiguous",
  "first_pass_reason": "inclusive vs exclusive span counting; gold follows one convention, natural reading differs"
 },
 {
  "id": "i3d3c151b56de7e",
  "text": "Statement 1: We visited Disneyland from Saturday to Monday.\nStatement 2: We visited Disneyland for 3 days.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.",
  "gold": "contradiction",
  "reader_A": "entailment",
  "reader_B": "entailment",
  "first_pass": "ambiguous",
  "first_pass_reason": "inclusive vs exclusive span counting; gold follows one convention, natural reading differs"
 },
 {
  "id": "i248fb0d470cf62",
  "text": "Statement 1: I will be on my office leave from 16th to 21st.\nStatement 2: I will be on my office leave for 6 days.",
  "question": "Work out the length of time that statement 1 implies and compare it with the length claimed in statement 2. Which option fits?",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: If statement 1 is true, statement 2 is guaranteed to be true, given what the times say.\n- contradiction: Statement 1 and statement 2 cannot both be true.",
  "gold": "contradiction",
  "reader_A": "entailment",
  "reader_B": "entailment",
  "first_pass": "ambiguous",
  "first_pass_reason": "inclusive vs exclusive span counting; gold follows one convention, natural reading differs"
 },
 {
  "id": "i42673815e3c173",
  "text": "Statement 1: The park opens in May and closes in Jul.\nStatement 2: The park is open for 3 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Statement 2 must be true whenever statement 1 is true.",
  "gold": "contradiction",
  "reader_A": "entailment",
  "reader_B": "entailment",
  "first_pass": "ambiguous",
  "first_pass_reason": "inclusive vs exclusive span counting; gold follows one convention, natural reading differs"
 },
 {
  "id": "iba4123621ba8c3",
  "text": "Statement 1: The park opens on Thursday and closes on Saturday.\nStatement 2: The park is open for 3 days.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Taking statement 1 as true, statement 2 cannot be false.\n- contradiction: Statement 1 and statement 2 cannot both be true.",
  "gold": "contradiction",
  "reader_A": "entailment",
  "reader_B": "entailment",
  "first_pass": "ambiguous",
  "first_pass_reason": "inclusive vs exclusive span counting; gold follows one convention, natural reading differs"
 },
 {
  "id": "i8fd174aed39e21",
  "text": "Statement 1: We attended outdoor concerts from January to December.\nStatement 2: We attended outdoor concerts for 12 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: The times in statement 1 rule out statement 2.",
  "gold": "contradiction",
  "reader_A": "entailment",
  "reader_B": "entailment",
  "first_pass": "ambiguous",
  "first_pass_reason": "inclusive vs exclusive span counting; gold follows one convention, natural reading differs"
 },
 {
  "id": "i859e6643a083c5",
  "text": "Statement 1: The spring quarter begins in Sep and ends in February.\nStatement 2: The spring quarter lasts for 6 months.",
  "question": "The pair is about how long something lasted. Choose the option that says whether statement 2 follows from statement 1 or conflicts with it.",
  "options": [
   "contradiction",
   "entailment"
  ],
  "definitions": "- contradiction: Statement 1 and statement 2 cannot both be true.\n- entailment: Taking statement 1 as true, statement 2 cannot be false.",
  "gold": "contradiction",
  "reader_A": "entailment",
  "reader_B": "entailment",
  "first_pass": "ambiguous",
  "first_pass_reason": "inclusive vs exclusive span counting; gold follows one convention, natural reading differs"
 },
 {
  "id": "i1719d54726e4fd",
  "text": "Statement 1: We attended outdoor concerts from Feb to Mar.\nStatement 2: We attended outdoor concerts for 2 months.",
  "question": "Statement 1 gives a start and an end, and statement 2 says how long the event lasted. Decide how statement 2 relates to statement 1.",
  "options": [
   "entailment",
   "contradiction"
  ],
  "definitions": "- entailment: Statement 2 must be true whenever statement 1 is true.\n- contradiction: Statement 1 and statement 2 cannot both be true.",
  "gold": "contradiction",
  "reader_A": "entailment",
  "reader_B": "entailment",
  "first_pass": "ambiguous",
  "first_pass_reason": "inclusive vs exclusive span counting; gold follows one convention, natural reading differs"
 },
 {
  "id": "ib374dc2f8b6e90",
  "text": "Claim: The Spread of Nuclear Weapons: More may be better\nPerspective: No country has an inherent right to invade or use aggression against another.",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective gives a reason to accept the claim.",
  "gold": "supports",
  "reader_A": "undermines",
  "reader_B": "undermines",
  "first_pass": "ambiguous",
  "first_pass_reason": "link between perspective and claim is indirect"
 },
 {
  "id": "ifac8c2d43f00ab",
  "text": "Claim: The best way to protect Scottish interests in the EU is to vote for independence\nPerspective: Scottish independence might be a faster route out of the EU than a referendum. ",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: Someone who holds this perspective would be more likely to agree with the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim.",
  "gold": "supports",
  "reader_A": "undermines",
  "reader_B": "undermines",
  "first_pass": "ambiguous",
  "first_pass_reason": "independence as a route out of the EU can cut either way"
 },
 {
  "id": "idba625201d284a",
  "text": "Claim: Cut aid to African states that criminalise homosexuality\nPerspective: Western Money, Western Discretion",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim.",
  "gold": "supports",
  "reader_A": "undermines",
  "reader_B": "undermines",
  "first_pass": "ambiguous",
  "first_pass_reason": "perspective too vague to fix a stance"
 },
 {
  "id": "i4d12dc2edb8eb8",
  "text": "Claim: Abolish nuclear weapons\nPerspective: The United States has an obligation to protect international stability due to its unique military strength.",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective argues against the claim.",
  "gold": "supports",
  "reader_A": "undermines",
  "reader_B": "undermines",
  "first_pass": "wrong_gold",
  "first_pass_reason": "argues the US needs its strength, which opposes abolition"
 },
 {
  "id": "i641636be24f6d9",
  "text": "Claim: Historical Artefacts Should Be Repatriated to Their Country of Origin\nPerspective: Artefacts should be accessible to the largest amount of visitors possible ",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective argues against the claim.",
  "gold": "supports",
  "reader_A": "undermines",
  "reader_B": "undermines",
  "first_pass": "wrong_gold",
  "first_pass_reason": "wide visitor access is an argument against repatriation"
 },
 {
  "id": "i0b6b0351f41f8a",
  "text": "Claim: People should lose their jobs for saying the wrong thing\nPerspective: Yes, it is against the law.",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective gives a reason to accept the claim.",
  "gold": "supports",
  "reader_A": "undermines",
  "reader_B": "undermines",
  "first_pass": "ambiguous",
  "first_pass_reason": "perspective lacks context to fix a stance"
 },
 {
  "id": "if9308ccf35a4fb",
  "text": "Claim: Eliminate All Nuclear Weapons\nPerspective: [Iran specific] Iran has threatened to destroy Israel",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective argues against the claim.",
  "gold": "supports",
  "reader_A": "undermines",
  "reader_B": "undermines",
  "first_pass": "ambiguous",
  "first_pass_reason": "threat from Iran can be a reason for or against elimination"
 },
 {
  "id": "i4c79a59521f165",
  "text": "Claim: Unilateral nuclear disarmament is the best way to create a safer world\nPerspective: Nuclear waste disposal is rarely safe/efficient; it is too much to expect a sqeaky clean disposal/disarmament of nuclear weapons  ",
  "question": "Each item gives a claim from a debate and one perspective on it. Decide whether the perspective supports or undermines the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective backs the position the claim takes.\n- undermines: The perspective works against the position the claim takes.",
  "gold": "supports",
  "reader_A": "undermines",
  "reader_B": "undermines",
  "first_pass": "wrong_gold",
  "first_pass_reason": "disposal difficulty is an argument against disarming"
 },
 {
  "id": "i44fd6759a1e2b9",
  "text": "Claim: All nations have a right to nuclear weapons\nPerspective: No country has an inherent right to invade or use aggression against another.",
  "question": "Read the claim and the perspective. Which option describes how the perspective bears on the claim?",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: Someone who holds this perspective would be less likely to agree with the claim.\n- supports: The perspective backs the position the claim takes.",
  "gold": "supports",
  "reader_A": "undermines",
  "reader_B": "undermines",
  "first_pass": "ambiguous",
  "first_pass_reason": "link to a right to nuclear weapons is indirect"
 },
 {
  "id": "i7ab7e496febb94",
  "text": "Claim: The UN should be reformed or replaced\nPerspective: The UN has performed a valuable service in preventing wars and in peacekeeping. ",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective gives a reason to accept the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim.",
  "gold": "supports",
  "reader_A": "undermines",
  "reader_B": "undermines",
  "first_pass": "wrong_gold",
  "first_pass_reason": "praises the UN, which opposes reform or replacement"
 },
 {
  "id": "i7041a52bb87880",
  "text": "Claim: Christmas is a scam\nPerspective: Christmas is more important than presents!",
  "question": "A perspective is a short argument about a debate claim. Pick the option that says which side of the claim the perspective takes.",
  "options": [
   "undermines",
   "supports"
  ],
  "definitions": "- undermines: The perspective works against the position the claim takes.\n- supports: The perspective gives a reason to accept the claim.",
  "gold": "supports",
  "reader_A": "undermines",
  "reader_B": "undermines",
  "first_pass": "ambiguous",
  "first_pass_reason": "stance toward a scam claim is unclear"
 },
 {
  "id": "i0009fc272afeb0",
  "text": "Claim: Wind farms are a good solution to the energy crisis\nPerspective: Cost will make energy prices rise",
  "question": "Judge the stance of the perspective toward the claim.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: The perspective works against the position the claim takes.",
  "gold": "supports",
  "reader_A": "undermines",
  "reader_B": "undermines",
  "first_pass": "wrong_gold",
  "first_pass_reason": "higher prices argue against wind farms"
 },
 {
  "id": "i5e58d0853c0af1",
  "text": "Claim: Junk Food Should Be Banned\nPerspective: A healthy diet starts from home and starts early. ",
  "question": "Say whether the perspective pushes toward accepting the claim or toward rejecting it.",
  "options": [
   "supports",
   "undermines"
  ],
  "definitions": "- supports: The perspective argues in favour of the claim.\n- undermines: Someone who holds this perspective would be less likely to agree with the claim.",
  "gold": "supports",
  "reader_A": "undermines",
  "reader_B": "undermines",
  "first_pass": "ambiguous",
  "first_pass_reason": "healthy diet at home can support or replace a ban"
 }
]
