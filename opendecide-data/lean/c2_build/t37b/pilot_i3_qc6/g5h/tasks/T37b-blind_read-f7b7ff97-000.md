# G5-H blind read T37b-blind_read-f7b7ff97-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3_qc6/g5h/answers/T37b-blind_read-f7b7ff97-000.json

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
  "qid": "q841fc87257",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS AND RELEVANCE: In this survey of heath care workers in hospitals equipped with fever clinics or wards for patients with COVID-19 in Wuhan and other regions in China, participants reported experiencing psychological burden, especially nurses, women, those in Wuhan, and frontline health care workers directly engaged in the diagnosis, treatment, and care for patients with COVID-19.\n\nClaim: Female front-line workers treating patients with COVID-19 experienced higher rates or more severe symptoms of depression, anxiety, insomnia and distress than health-care workers overall.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qd5ac42a29d",
  "kind": "yes/no",
  "text": "Customer: Hi there. I'd like to buy movie tickets for showings in Davis, CA.\nAgent: No problem. Do you have a movie in mind?\nCustomer: I am considering the movie \"No Time To Die\"\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: Are there no showings in any theaters in Davis, CA?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: Oh that's unfortunate. Are there any action movies playing in Davis?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Okay is that the original movie from the 70s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: You know that's okay. I will wait until the film I wish to see becomes available in Davis.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By the close of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qf62e683741",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nUsing global line-list data on COVID-19 cases reported until 29th February 2020 and global gridded temperature data, and after adjusting for surveillance capacity and time since first imported case, higher average temperature was strongly associated with lower COVID-19 incidence for temperatures of 1°C and higher.\n\nClaim: Multiple early studies provide evidence of less correlation between temperature and humidity ranges and the geographic regions where this virus has thrived.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qfa29cdaa98",
  "kind": "yes/no",
  "text": "Assistant: okay I will have the coffee delivered to you in fifteen minutes\nCustomer: thank you\nAssistant: sorry boss, they ran out of soy milk",
  "question": "Is there confirmation of \"soy milk\" for the customer's coffee order in the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q624b61b4aa",
  "kind": "yes/no",
  "text": "Recently , about one-third of Americas huge corn crop has been diverted from food and feed into an ultra-costly auto fuel that gives consumers poorer mileage even as it drives up their food costs . The corn ethanol diversion creates an artificial scarcity of farmland, as it attracts more land into corn instead of wheat or other cropsand the price effects are felt globally. In 2008, the ethanol mandate drove food prices up by more than 50 percent worldwide, and triggered food riots in Mexico and several other countries.",
  "question": "Does the paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q3e62bb86fb",
  "kind": "yes/no",
  "text": "Customer: I think I would just like you to recommend one.\nAssistant: They just added a second floor at Club Salsa. It's a must see. They are located at 1 Station Road. The entrance fee is 5 pounds.",
  "question": "Did the assistant find at least a single option that meets everything the customer asked for in its reply?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q19c9cf5f6e",
  "kind": "yes/no",
  "text": "Statement 1: I CANNOT COUNT STARS.\nStatement 2: I CAN COUNT STARS.",
  "question": "Of these two statements, does Statement 2 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q02b12ed4f4",
  "kind": "yes/no",
  "text": "Statement 1: he thought it would rain soon so he carried sunglasses\nStatement 2: he thought it would rain soon so he carried an umbrella",
  "question": "Of these two statements, does Statement 2 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q583ddef1d2",
  "kind": "yes/no",
  "text": "Customer: Could you try an hour earlier, then?\nAssistant: Certainly. You now have a table for your party of 8 at the Curry Garden, at 16:45. Your reference number is V24OGNJB.",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "q39f3bd8dc4",
  "kind": "yes/no",
  "text": "Situation: Baby by a married man\nAction being judged: Cheating on your partner and having a baby with someone else.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q3a834dd6d0",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2008 HYUNDAI VERACRUZ. WHILE DRIVING 5 MPH, THE ABS MODULE MALFUNCTIONED AND CAUSED THE VEHICLE TO CATCH FIRE. THE CONTACT NOTICED SMOKE UNDER THE HOOD OF THE VEHICLE AND FLAMES IGNITED FROM THE BATTERY. A POLICE REPORT WAS NOT FILED. THE FIRE WAS EXTINGUISHED BY ATTENDANTS FROM A NEARBY AUTO BODY SHOP. THERE WERE NO INJURIES. THE VEHICLE WAS NOT DESTROYED. THE DEALER AND MANUFACTURER WERE NOT NOTIFIED. THE FAILURE MILEAGE WAS APPROXIMATELY 144,000.",
  "question": "Does this complaint, which is about vehicle safety, report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q084cb36607",
  "kind": "yes/no",
  "text": "Customer: Hi, I'm looking for movie tickets.\nAgent: Okay, for what date?\nCustomer: I don't really care about the date, but something within the week.\nAgent: Sure. And what movie?\nCustomer: Either Mulan or No Time to Die. I'm not picky.\nAgent: No Time to Die or Mulan, okay...what theatre location?\nCustomer: I live in Oregon, Stoneyford to be exact.\nAgent: Alright, there are two movie theatres there. Do you have a preference?\nCustomer: No.\nAgent: Okay, so there is Mountain AMC 16 or Holiday Cinemark 12. One moment please.\nCustomer: Alright, thanks.\nAgent: Hello, so unfortunately I can not secure any tickets at all because both movie theatres are closed.\nCustomer: They are closed? Until how long?\nAgent: There is no end date.\nCustomer: Are any other locations open?\nAgent: No. It seems that all movie theatres are closed until further notice.\nCustomer: Okay...are the movies available on demand or something?\nAgent: Let me check....no, unfortunately their release dates were pushed back.\nCustomer: So when are they being released? Am I just out of luck?\nAgent: Unfortunately, yes, it seems that way. There is no pending release date for either movie, but records indicate sometime in the fall.",
  "question": "By the end of this dialogue, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q76035c52b7",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThese studies confirm that cats are susceptible to productive SARS-CoV-2 infection, but are unlikely to develop clinical disease.\n\nClaim: Cats can be infected by the novel coronavirus but are unlikely to get sick.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "qfec24537a8",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Raj Ghatak\n- Ghatak has worked extensively on stage, and in many original ground-breaking productions.\n\nSummary sentence:\nRaj Ghatak is an actor.",
  "question": "Is every piece of information in the sentence that gives the summary supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qc05de1d59e",
  "kind": "yes/no",
  "text": "Assistant: I'm sorry sir, but we have no booth seating available at that time.\nCustomer: I will take a table for 4 people, please.\nAssistant: You are all set sir. I have booked a table for four for Tuesday evening, March 4th at 6:00PM.",
  "question": "Does the assistant's final message confirm \"table\" for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q13f8e01737",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He finished the 2015–16 season leading the Lakers and all rookies in steals per game, and became the youngest player to hit 130 three-pointers in a season.\n- He subsequently earned NBA All-Rookie Second Team honors.\n\nSummary sentence:\nPlaying point guard, he was named to the NBA All-Rookie Second Team with the Lakers in 2016.",
  "question": "Is every piece of the summary sentence's information supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q8ebfdd1f74",
  "kind": "yes/no",
  "text": "Assistant: The Cedars offers several hot meals from the grill.\nCustomer: Great, get the tickets at The Cedars.\nAssistant: I've booked you for 2 tickets to The Upside at The Cedars for 6pm",
  "question": "Has \"The Upside\" been confirmed for the customer's movie ticket order in the assistant's latest message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q110727aa72",
  "kind": "yes/no",
  "text": "Assistant: Yes, I have made a note of it.\nCustomer: Thank you.\nAssistant: Your reservations have been confirmed for 7 pm on Sunday for a party of six.",
  "question": "Is \"six\" for the customer's restaurant reservation confirmed in the final message from the assistant?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2d94d80c4f",
  "kind": "yes/no",
  "text": "Customer: Starting Sunday for 7 people for 4 nights.\nAssistant: I am unable to book the room at this time.",
  "question": "Does the assistant's reply confirm the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q8e204ef118",
  "kind": "yes/no",
  "text": "Statement 1: They have to say farewell to each other because they are leaving\nStatement 2: They have to say hello to each other because they are leaving",
  "question": "Is it the case that, of these two statements, Statement 2 doesn't go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "qd837804c25",
  "kind": "yes/no",
  "text": "Occupation: Marriage and Family Therapists\nDuties:\n- Diagnose mental and emotional disorders in clients.\n- Encourage individuals and family members to develop and use skills and strategies for confronting their problems in a constructive manner.\n- Collect information about clients, using techniques such as testing, interviewing, discussion, or observation.",
  "question": "Do the listed duties form part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qfeccbbf79d",
  "kind": "yes/no",
  "text": "Customer: No, that doesn't matter, but I'd like something in the moderate price range.\nAssistant: There are 14 options. How about the Avalon? It has 4 stars and free parking and wifi.",
  "question": "According to its reply, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q5831a0ed9f",
  "kind": "yes/no",
  "text": "Table caption: Correlations between HMB and SJ profiles.\n| Date | Correlation Coefficient | P-Value |\n| July 9, 2018 | 0.93 | 0.0 |\n| July 16, 2018 | 0.83 | 0.0 |\n| July 18, 2018 | 0.88 | 0.0 |\n| July 20, 2018 | 0.84 | 0.0 |\n| July 24, 2018 | 0.91 | 0.0 |\n| July 31, 2018 | 0.72 | 0.0 |\n| August 2, 2018 | 0.92 | 0.0 |\n| August 3, 2018 | 0.87 | 0.0 |\n| August 6, 2018 | 0.68 | 0.0 |\n| August 10, 2018 | 0.85 | 0.0 |\n| August 17, 2018 | 0.92 | 0.0 |\n| All dates | 0.79 | 0.0 |\n\nStatement: There are eleven different Dates of Correlations between HMB and SJ profiles.",
  "question": "Is the statement substantiated by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd8a3ad35a8",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThis study confirms that serum and saliva IgG antibodies to SARS-CoV-2 are maintained in the majority of COVID-19 patients for at least 3 months PSO. IgG responses in saliva may serve as a surrogate measure of systemic immunity to SARS-CoV-2 based on their correlation with serum IgG responses.\n\nClaim: And a study of Covid-19 patients found that antibody levels in saliva and blood were closely matched.",
  "question": "Based on the text, does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q2fe083ff62",
  "kind": "yes/no",
  "text": "When the Board voted in December to amend teaching standards to allow students to consider both sides in the climate debate, global warming pressure groups were apoplectic.",
  "question": "Is there confirmation that this paragraph makes the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qda70e8dd10",
  "kind": "yes/no",
  "text": "Table caption: Level 2 algorithm tests for ABSCO evaluation using OCO-2 soundings.\n| Label | Description |\n| A: B9 Baseline | B9 algorithm, using ABSCO v5.0 (includes EOFs) |\n| B: B9 No EOF | B9 algorithm, using ABSCO v5.0 (no EOFs included in fits to OCO-2 spectra) |\n| C: H 2 O continuum update | As above, with update to H 2 O continuum only |\n| D: O 2 and H 2 O updates | As above, with updates to both H 2 O continuum and O 2 spectroscopy (ABSCO v5.1) |\n| E: B9 with ABSCO v5.1 and EOFs | As above, after re-calculation of EOFs and including these EOFs in the fits to OCO-2 spectra |\n\nStatement: A: B9 Baseline and C: H 2 O Label are having same description B9 algorithm, using ABSCO v5.0 (includes EOFs).",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q46ce89666c",
  "kind": "yes/no",
  "text": "Complaint narrative: 2018 DODGE CARAVAN. CONSUMER WRITES IN REGARDS TO DEFECTIVE PASSENGER SEAT WHICH RESULTED IN INJURY TO PASSENGER. *LD THE CONSUMER STATED THE WHILE ATTEMPTING TO ADJUST THE SEAT TO AN UPRIGHT POSITION IT SLAMMED FORWARD AGAINST THE BACK OF THE HEAD. THIS CAUSED AND INJURY TO THE HEAD AND JAW. THE CONSUMER DID NOT SEEK MEDICAL ATTENTION. *JS *TT *BF",
  "question": "Looking at this vehicle safety complaint, does it report that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q5b50f6e1b5",
  "kind": "yes/no",
  "text": "Statement 1: A spider spun a web.\nStatement 2: A horse spun a web",
  "question": "Is it true that, of these two statements, Statement 1 doesn't go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q73b3b53740",
  "kind": "yes/no",
  "text": "Customer: I want to buy movie tickets for tonight\nAgent: OK! What movie would you like to see?\nCustomer: Sonic\nAgent: OK! What theater do you prefer?\nCustomer: The Cinemark in West Valley\nAgent: Great. Would you prefer a Standard or XD screen?\nCustomer: XD\nAgent: OK. And what time would you like to see the show?\nCustomer: 7:00 PM\nAgent: There is a showing at 7pm. How many tickets will you need?\nCustomer: Two\nAgent: OK. Two tickets will be $30\nCustomer: Oh that's too high. Is a standard screen cheaper?\nAgent: Two tickets for a standard showing are $20.\nCustomer: What time is the standard screen?\nAgent: The standard showing is at 6:20pm\nCustomer: OK let's buy that one\nAgent: OK. Just to confirm we have two tickets for Sonic tonight at 6:20pm at the West Valley Cinemark. Your total is $20.\nCustomer: Yes\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "Is it true that, by the end of this conversation, the customer has not actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "qc6bb85e8e8",
  "kind": "yes/no",
  "text": "Table caption: concentration of R and S amphetamine in seized tablets (mg/g).\n|  | Tablet weight (mg) | Concentration of R -amphetamine (mg/g) | RSD (%) | Concentration of S -amphetamine (mg/g) | RSD (%) | Total amphetamine (mg/g) | ee% |\n| 1 | 150.77 | 35.26 | 3.64 | 38.36 | 3.87 | 73.62 | 4.21 |\n| 2 | 168.67 | 47.82 | 3.81 | 48.40 | 2.48 | 96.22 | 0.60 |\n| 3 | 168.82 | 44.54 | 2.37 | 47.78 | 3.25 | 92.32 | 3.51 |\n| 4 | 165.55 | 30.82 | 3.43 | 31.62 | 1.75 | 62.44 | 1.28 |\n| 5 | 176.65 | 29.00 | 2.07 | 29.78 | 3.57 | 58.78 | 1.33 |\n| 6 | 169.18 | 17.94 | 3.69 | 18.5 | 3.20 | 36.44 | 1.54 |\n| 7 | 147.95 | 36.70 | 3.18 | 40.44 | 2.48 | 77.14 | 4.85 |\n| 8 | 168.70 | 19.02 | 2.63 | 19.86 | 2.44 | 38.88 | 2.16 |\n| 9 | 169.03 | 20.26 | 3.51 | 21.10 | 3.77 | 41.36 | 2.03 |\n| 10 | 166.75 | 37.16 | 2.96 | 45.16 | 2.11 | 82.32 | 9.72 |\n| 11 | 177.45 | 19.12 | 2.18 | 20.26 | 3.35 | 39.38 | 2.89 |\n| 12 | 166.06 | 44.68 | 1.6 | 49.66 | 3.39 | 94.34 | 5.28 |\n\nStatement: The Highest Concentration of R -amphetamine (mg/g) is 47.82.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q74b4da3fa1",
  "kind": "yes/no",
  "text": "Statement 1: Sunglasses are worn on the eyeballs.\nStatement 2: Contact lenses are worn on the eyeballs.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q8f53014b9c",
  "kind": "yes/no",
  "text": "It also said the panel had purposely emphasised the negative impacts of climate change and made \"substantive findings\" based on little proof.",
  "question": "Does the paragraph here make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q4786b30349",
  "kind": "yes/no",
  "text": "Situation: Teen Should Go On Strike Until Brother Pays What He Owes\nAction being judged: Borrowing from a family member and not paying it back.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q99d6fb9dfc",
  "kind": "yes/no",
  "text": "Table caption: Description of Shear Reinforcements.\n| Specimen designation | No. of specimens | diameter, in(mm | Perimeter length, in(mm). | Perimeter length, in(mm). | Spacing in(mm). | No. of Stirrups |\n| Specimen designation | No. of specimens | diameter, in(mm | Ex. | Int. | Spacing in(mm). | No. of Stirrups |\n| Inverted-U PTB -A | 2 | 0.39(10) | 26.77(680) | 19.68(500) | 2.36(60) | 32 |\n| Closed Stirrups PTB -B | 2 | 0.39(10) | 37(940) | 22.83(580) | 2.36(60) | 32 |\n\nStatement: The No. of specimens are 2 each.",
  "question": "Is it true that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q07793e9695",
  "kind": "yes/no",
  "text": "Assistant: actually there is a problem\nCustomer: what kind of problem\nAssistant: there is no uber xl close by",
  "question": "Does the assistant's final message say \"uber xl\" is confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdbdd6aabd4",
  "kind": "yes/no",
  "text": "Customer: Hi, Can you help me find White Fang?\nAgent: Sure, do you mean the movie or book?\nCustomer: I mean what theater in Santa Rosa is it showing in now?\nAgent: There are 4, first is Rialto, is that what you'd like?\nCustomer: No, what about Airport Cinema?\nAgent: Sure, it is playing there, what time would you like a ticket for?\nCustomer: Is there something at 5:30 or so?\nAgent: There is a showing at 5:20, would you like tickets?\nCustomer: Sure, I think that will work.\nAgent: How many tickets would you like?\nCustomer: I need 2 please.\nAgent: Sure, 2 for White Fang 5:20, Santa Rosa Airport cinema, is that right?\nCustomer: No, I changed my mind, is there a 5:30 show at the Rialto?\nAgent: There is a 5:40 showing there, would you like to change to there?\nCustomer: Yes, make that change please.\nAgent: change is 2 for White Fang, at the Rialto, 5:40 pm., tonight, in Santa Rosa, regular type screening, is that right?\nCustomer: Yes that's good, thanks.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.\nCustomer: Great, I have them thanks.\nAgent: enjoy your show.",
  "question": "Has the customer, by the end of this conversation, actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qb5948c63a7",
  "kind": "yes/no",
  "text": "Customer: Hi! I would like to watch a movie tonight!\nAgent: What kind of movies interest you?\nCustomer: I prefer horror films.\nAgent: Would The Grudge be good for you for tonight?\nCustomer: Yes! Sign me up for The Grudge!\nAgent: Will you be going alone?\nCustomer: Yes, I am going alone tonight.\nAgent: And when would you like to see it?\nCustomer: I would like to see it at 6 PM tonight?\nAgent: Would you like an upgraded screening experience?\nCustomer: No thanks, I would just like the standard screening.\nAgent: Which theater would you prefer?\nCustomer: I would like the Cinemark in Los Angeles.\nAgent: Okay, and would that be all?\nCustomer: I would actually like to change the screening experience.\nAgent: What would you like to change it to?\nCustomer: I would like the 3D experience.\nAgent: IS this correct? 1 ticket to The Grudge at Cinemark in Los Angeles at 6 PM with a 3D viewing experience?\nCustomer: That is correct!\nAgent: Your order total is $15. Please have your ticket ready!\nCustomer: Thank you so much!\nAgent: I am happy to help.",
  "question": "Based on the text, by the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q1e48b5b404",
  "kind": "yes/no",
  "text": "Table caption: Summary of previously reported cases of COVID-19-associated pulmonary aspergillosis.\n| Study | Country | CAPA* | Aspergillus species | Aspergillus species in culture | Serum or BAL GM positive | BAL Aspergillus PCR positive | Initial Antifungal Therapy | In-hospital mortality |\n| Alanio, 2020 [ ] | France | 9/27 | A. fumigatus (7/9) | 7/9 | 3/9 | 4/9 | VOR (1/9) CAS (1/9) None (7/9) | 4/9 |\n| Koehler, 2020 [ ] | Germany | 5/19 | A. fumigatus (5/5) | 3/5 | 4/5 | 4/5 | VOR (2/5) ISA (1/5) CAS (2/5) | 3/5 |\n| Rutsaert, 2020 [ ] | The Netherlands | 7/34 | A. fumigatus (5/7) A. flavus (1/7) | 6/7 | 6/7 | NR | VOR (4/7) VOR/ISA (2/7) None (1/7) | 4/7 |\n| Nasir, 2020 [ ] | Pakistan | 5/23 | A. flavus (3/5) A. niger (1/5) A. fumigatus and A. flavus (1/5) | 5/5 | 0/5 | NR | VOR (3/5) AmB-d (2/5) | 3/5 |\n| van Arkel, 2020 [ ] | The Netherlands | 6/31 | A. fumigatus (6/6) | 5/6 | 3/6 | NR | VOR plus AND (5/6) L-AmB (1/6) | 4/6 |\n| Blaize, 2020 [ ] | France | 1/1 | A. fumigatus | 1/1 | 0/1 | 1/1 | None | 1/1 |\n| Lahmer, 2020 [ ] | Germany | 2/2 | A. fumigatus (2/2) | 2/2 | 2/2 | NR | L-AmB (2/2) | 2/2 |\n| Wang, 2020 [ ] | China | 8/104 | A. fumigatus | 8/8 | NR | NR | NR | NR |\n| Antinori, 2020 [ ] | Italy | 1/1 | A. fumigatus | 1/1 | 1/1 | 1/1 | L-AmB | 1/1 |\n| Ferreira, 2020 [ ] | France | 1/1 | A. fumigatus | 1/1 | 0/1 | 1/1 | None | 1/1 |\n| Meijer, 2020 [ ] | France | 1/1 | A. fumigatus | 1/1 | 1/1 | NR | VOR plus CAS | 1/1 |\n| Prattes, 2020 [ ] | Austria | 1/1 | A. fumigatus | 1/1 | 0/1 | NR | VOR | 1/1 |\n| Sharma, 2020 [ ] | Australia | 1/1 | A. fumigatus | 1/1 | NR | NR | VOR | 0/1 |\nTable notes: *number with CAPA/total number in the report AmB-d, amphotericin b deoxycholate; AND, anidulafungin; BAL, bronchoalveolar lavage; CAPA, COVID-19-associated pulmonary aspergillosis; CAS, caspofungin; GM, galactomannan; ISA, isavuconazole; L-AmB, liposomal amphotericin; NR, not reported; VOR, voriconazole\n\nStatement: van Arkel, 2020 study had reported France 5/23 for CAPA",
  "question": "Is it correct that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qd562c203c5",
  "kind": "yes/no",
  "text": "Statement 1: She put a cotton pie in the oven to bake.\nStatement 2: She put an apple pie in the over to bake.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q8f462869c3",
  "kind": "yes/no",
  "text": "Complaint narrative: FRONT LEFT BRAKE LINE RUPTURED, RESULTING IN LOSS OF BRAKE FLUID, DEPRESSES BRAKE PEDAL GOES TO THE FLOORBOARD. NO STOPPING POWER. BACKING OUT OF DRIVEWAY ON THIS OCCASION. NO ACCIDENT. SAME LINE ON RIGHT FRONT RUPTURED LESS THAN A YEAR AGO, EXACT SAME RESULT. LUCKILY NO ACCIDENT BUT WAS AT A STOP LIGHT ON A MAJOR HIGHWAY WHEN PEDAL WHEN STRAIGHT TO FLOOR",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "qd1d9d7fa03",
  "kind": "yes/no",
  "text": "Complaint narrative: APRIL 26, 2019 THE ENGINE IN MY 2008 CHEVY EQUINOX SPORT LOCKED UP. THE VEHICLE WAS TOWED TO MIDWEST TIRE & AUTO IN THE CICERO,IL FOR ENGINE REPLACEMENT. A WEEK AFTER RETRIEVING MY SUV ON JUNE 20,2019 FROM THE SHOP IT HAD AN EXCESSIVE ENGINE OIL AND POWER STEERING FLUID LEAK AND IT CAUGHT FIRE. WHILE THE OCCUPANCY OF MY WIFE AND 3 CHILDREN AGES 7,4, AND 2 WERE WITHIN 11 MILES OF TRAVEL FROM OUR RESIDENCE ALONG THE HIGHWAY. THE VEHICLE WAS NOT RECOGNIZABLE FROM THE INTERIOR, FROM FRONT TO CENTER OF THE VEHICLE'S BODY IT WAS A GRAYISH COLOR. SHOWING THE FIRE'S INTENSITY.",
  "question": "Does this complaint, which is about vehicle safety, report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q45b6bd868f",
  "kind": "yes/no",
  "text": "Complaint narrative: IF TRUCK IS NOT DRIVEN IN A FEW WEEKS THE GAS FEED STICKS IN REVERSE, I HAVE NOT HAD IT STICK IN FORWARD. ONLY IN REVERSE, MY WIFE HAD A ACCIDENT WITH THIS TRUCK. I'VE HAD IT STICK ON ME BUT I'M LOOKING FOR IT. FORD AND THE INSURANCE COMPANIES SAY THAT THERE IS NOTHING WRONG. IT HAS OCCURRED SEVERAL TIMES WITH ME AND I DON'T LET MY WIFE DRIVE THE TRUCK.",
  "question": "According to this vehicle safety complaint, was the vehicle actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q7c6f10a8ee",
  "kind": "yes/no",
  "text": "Occupation: Appraisers and Assessors of Real Estate\nDuties:\n- Inspect properties, considering factors such as market value, location, and building or replacement costs to determine appraisal value.\n- Photograph interiors and exteriors of properties to assist in estimating property value, substantiate findings, and complete appraisal reports.\n- Compute final estimation of property values, taking into account such factors as depreciation, replacement costs, value comparisons of similar properties, and income potential.",
  "question": "Is the inclusion of the listed duties in the job of the occupation named above true?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qb3adc91e61",
  "kind": "yes/no",
  "text": "Table caption: The categories and their conditions.\n| Category | More likely to be salient | Less likely to be salient |\n| Loudness | Word intensity of 80 dB | Word intensity of 60 dB |\n| Acoustic Prominence | /t/pronounced as [p] | /t/pronounced as [t] |\n| Grammatical Gender | Violation of grammatical gender | Correct grammatical gender |\n| Frequency | High frequency word | Low frequency word |\n| Conscious Sound Change | /r/pronounced as [ɹ] | /r/pronounced as [r] |\n| Subconscious Sound Change | /v/pronounced as [v] (=voiced) | /v/pronounced as [f] (=voiceless) |\n\nStatement: More likely to be salient for Grammatical Gender is/r/pronounced as [] .",
  "question": "Does the table provide support for the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q5f1445f6b3",
  "kind": "yes/no",
  "text": "Situation: Trash Talking Creates a Stink After Warring Couple Reconciles\nAction being judged: Reigniting a conflict that just ended.",
  "question": "Is the action being judged permissible under common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qd307e9e105",
  "kind": "yes/no",
  "text": "Table caption: Granulometric properties of the soils (mass %).\n| Clay | Silt | Sand | Gravel | Rubble | Name of mine |\n| 37.9 | 51.9 | 9.9 | 0.3 | – | S E |\n| 31.4 | 55.8 | 12.8 | – | – | S M |\n| 34.7 | 60.7 | 4.6 | – | – | S H |\n| 29 | 57.4 | 9.3 | 4.2 | – | S GH |\n| 10 | 79.7 | 10.1 | 0.1 | – | S A |\n| 35.6 | 52.5 | 11.8 | 0.1 | – | S Z |\n\nStatement: SA and SH has same gravel value.",
  "question": "Is the statement supported according to the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8671ad07e1",
  "kind": "yes/no",
  "text": "As weve seen in numerous model-data comparisons, there are few similarities between modeled and observed surface temperatures and precipitation. See here , here , here , here , and here for examples. Weve compared satellite-era sea surface temperature to model outputs in past posts (examples here , here and here ), but we used model outputs from climate models stored in the CMIP3 archive, which was prepared for the 2007 4 th Assessment Report from the IPCC. In this post, were using the outputs of newer CMIP5 models, prepared for the IPCCs upcoming 5 th Assessment Report. Scenario RCP6.0 for the CMIP5 models is presented because it most closely matches the climate forcings of the scenario called SRES A1B, which was widely cited in the past.",
  "question": "Is it accurate to say that this paragraph doesn't make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable.\n- no: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy."
 },
 {
  "qid": "q24f04fe85a",
  "kind": "yes/no",
  "text": "Situation: I regularly give people misinforamtion to teach them to listen clearly\nAction being judged: Giving people misinformation just because they aren't listening.",
  "question": "Is it the case that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qd072b868ec",
  "kind": "yes/no",
  "text": "Situation: Single Dad Never Pitches In at Neighborhood Potlucks\nAction being judged: Not contributing anything to a potluck you are going to.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qe41c2132f7",
  "kind": "yes/no",
  "text": "Table caption: Amino acids as butyl esters and their molecular ions. Additional amino acids can be detected and quantified with the matching stable-isotopic labeled standards.\n| Target amino acid | [M+H] + /[M+H] + Internal standard as butylesters |\n| Alanine | 146/150 |\n| Arginine | 231/236 |\n| Aspartic Acid | 246/249 |\n| Citrulline | 232/234 |\n| Glutamic acid | 260/263 |\n| Glycine | 132/134 |\n| Leucine/Isoleucine | 188/191 |\n| Methionine | 206/209 |\n| Ornithine | 189/191 |\n| Phenylalanine | 222/228 |\n| Tyrosine | 238/244 |\n| Valine | 174/182 |\n\nStatement: Leucine/Isoleucine has146/150 as values.",
  "question": "Would it be correct to say that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 }
]
