# T37b blind solver T37b-blind_read-409c9c79-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3_qc3/s13/answers/T37b-blind_read-409c9c79-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qd6a923be0d",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCOVID-19-related death was associated with: being male (hazard ratio (HR) 1.59, 95% confidence interval (CI) 1.53-1.65); older age and deprivation (both with a strong gradient); diabetes; severe asthma; and various other medical conditions. Compared with people with white ethnicity, Black and South Asian people were at higher risk even after adjustment for other factors (HR 1.48, 1.30-1.69 and 1.44, 1.32-1.58, respectively).\n\nClaim: Older people, men, racial and ethnic minorities, and those with underlying health conditions are among the least at-risk populations when it comes to COVID-19 fatality.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q0bf64467c1",
  "kind": "yes/no",
  "text": "Situation: I sat back, and breathed in a sigh of relief as I let out a smile.\nAction being judged: Smiling when you are happy.",
  "question": "Under common social norms, is the action being judged wrong?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q72bb504aee",
  "kind": "yes/no",
  "text": "Statement 1: A steak will give a happy ending to this meal\nStatement 2: A dessert will give a happy ending to this meal",
  "question": "Of the statements shown: Statement 1, does it go against what common sense tells us?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qa89436132d",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nWe estimate that the global ability to detect imported cases is 38% (95% HPDI 22% – 64%) of Singapore’s capacity. Equivalently, an estimate of 2.8 (95% HPDI 1.5 – 4.4) times the current number of imported cases, could have been detected, if all countries had had the same detection capacity as Singapore.\n\nClaim: Health experts say that it makes no difference: a study by Harvard’s Center for Communicable Disease Dynamics found that Singapore was just as likely to detect infected people as other nations despite its “very strong epidemiological surveillance and contact-tracing capacity.”",
  "question": "Does the evidence contradict it?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qb1fce74aec",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2009, Taylor married writer Nick Flynn.\n- They have a daughter Maeve.\n\nSummary sentence:\nShe is married to playwright Nick Flynn, with whom she has a daughter.",
  "question": "Is every bit of info in the summary sentence backed up by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qaef6a15251",
  "kind": "yes/no",
  "text": "Occupation: Receptionists and Information Clerks\nDuties:\n- Provide information about establishment, such as location of departments or offices, employees within the organization, or services provided.\n- Transmit information or documents to customers, using computer, mail, or facsimile machine.\n- Operate telephone switchboard to answer, screen, or forward calls, providing information, taking messages, or scheduling appointments.",
  "question": "Are the listed duties part of the job, for the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qec503aa2c9",
  "kind": "yes/no",
  "text": "Customer: Hello?\nAgent: Hello there!\nCustomer: I am looking to see a movie.\nAgent: Great! What movie?\nCustomer: I am not sure, any recommendations?\nAgent: Yes, I hear 1917 is great.\nCustomer: Hmm, I am not interested in that. Any other recommendations?\nAgent: Yes, Underwater is excellent.\nCustomer: That sounds perfect.\nAgent: How many people will be in attendance?\nCustomer: Just 2 of us.\nAgent: OK, and what showtime do you prefer?\nCustomer: 7:00 PM.\nAgent: Hmm, no 7:00 PM's are available.\nCustomer: Try 8:00 PM then.\nAgent: I will look now.\nCustomer: Thank you.\nAgent: Unfortunately, I do not see any movies available as of now.\nCustomer: Bummer, thanks anyway.\nAgent: Absolutely! Have a good day.\nCustomer: You as well.",
  "question": "By the end of this conversation, is there actually a purchase of movie tickets by the customer?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q1be6dfccff",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Laudrup now works as a pundit and co-commentator for Discovery Networks Denmark, covering the Premier League and Denmark national team.\n\nSummary sentence:\nHe currently works as a football commentator and pundit.",
  "question": "Is every piece of information in the summary sentence substantiated by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q97fde4e720",
  "kind": "yes/no",
  "text": "Table caption: Characteristics of all ESS 11 cases in relation to gender.\n| Gender | Women ( n = 1087) | Men ( n = 783) | P |\n| Age - years |  |  |  |\n| Median (25 th ,75 th percentile) | 73 (56−84) | 71 (55−81) | 0.025 |\n| Priority at dispatch centre - n (%) a |  |  | 0.001 |\n| Prio 1 | 334 (30.8) | 302 (38.6) |  |\n| Prio 2 | 698 (64.3) | 448 (57.2) |  |\n| Prio 3 | 53 (4.9) | 33 (4.2) |  |\n| Triage colour RETTS - n (%) |  |  | 0.002 |\n| Red | 11 (1.0) | 13 (1.7) |  |\n| Orange | 224 (20.6) | 195 (24.9) |  |\n| Yellow | 587 (54.0) | 423 (54.0) |  |\n| Green | 265 (24.4) | 152 (19.4) |  |\n| Level of care - n (%) |  |  | 0.170 |\n| To hospital | 849 (78.1) | 632 (80.7) |  |\n| Stay at the scene | 238 (21.9) | 151 (19.3) |  |\n| Seek medical advice within 72 h. - n (%) b | 29 (12.2) | 15 (9.9) | 0.517 |\n| Mode of transport - n (%) c |  |  | 0.605 |\n| Ambulance | 764 (90.0) | 584 (92.4) |  |\n| PTS, immobile d | 33 (3.9) | 17 (2.7) |  |\n| PTS, seated | 32 (3.8) | 18 (2.8) |  |\n| Single-responder unit | 8 (0.9) | 9 (1.4) |  |\n| Transport by own means | 12 (1.4) | 4 (0.6) |  |\n| Type of condition - n (%) |  |  |  |\n| Non-time critical | 1040 (95.7) | 734 (93.7) | 0.062 |\n| Time critical | 47 (4.3) | 49 (6.3) |  |\n\nStatement: Transport by own means Men ( n = 783) is 4 (0.6).",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qc0593e71f7",
  "kind": "yes/no",
  "text": "Table caption: Resin duct metric name and description.\n| Metric | Type | Description |\n| Duct size (mm 2 ) | Unstandardized | Mean size of all ducts per annual ring |\n| Duct production (no. year −1 ) | Unstandardized | Total number of ducts per annual ring |\n| Total duct area (mm 2 year −1 ) | Unstandardized | Sum of duct area per annual ring |\n| Duct density (no. mm −2 year −1 ) | Standardized | Total number of ducts per annual ring divided by ring area |\n| Relative duct area (% annual ring) | Standardized | Total duct area divided by ring area × 100 |\n\nStatement: There are three table heads Metric , Type and Description.",
  "question": "Is it accurate to say that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q69f3ca293c",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- After leaving parliament, Purnell became the chair of the Institute for Public Policy Research.\n- Purnell became linked with the Blue Labour movement within the Labour Party and in April 2011 he was appointed by the Boston Consulting Group as a Special Advisor to their Public Sector Group.\n\nSummary sentence:\nPurnell chaired the Institute for Public Policy Research until 2010, and was a senior advisor in the Public Sector practice of the Boston Consulting Group.",
  "question": "Is the summary sentence's information, every piece of it, supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q789eef93d8",
  "kind": "yes/no",
  "text": "Statement 1: He ran a race.\nStatement 2: He spun a race.",
  "question": "Among the statements given: Statement 2, is it going against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qb18aa9c8ff",
  "kind": "yes/no",
  "text": "Statement 1: He shot the lion with a spoon\nStatement 2: He shot the lion with a gun.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q80166d606a",
  "kind": "yes/no",
  "text": "Situation: I asked my girlfriend to marry me last night.\nAction being judged: Males proposing to the female they are dating when the relationship is serious.",
  "question": "Would it be correct to say that the action being judged is not wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q066eedd82d",
  "kind": "yes/no",
  "text": "Table caption: The IC 50 values of essential oils in the A549 cell line.\n| Essential oils | IC 50 (%, v/v) |\n| Dendranthema indicum (L.) Des Moul | 0.03324 |\n| Peucedanum japonicum Thunb | 0.04192 |\n| Dendranthema zawadskii var. latilobum (Maxim.) Kitam | 0.04472 |\n| Agastache rugosa (Fisch.&Mey.) Kuntze | 0.1508 |\n| Vitex rotundifolia L.f | 0.08438 |\n| Pinus rigida Mill | 0.04544 |\n| Orixa japonica Thunb | 0.02833 |\n| Pinus strobus L | 0.03293 |\n| Chamaecyparis pisifera (Siebold et Zucc.) Endl. var. filifera Beissn. et Hochst | 0.06272 |\n| Citrus sunki Hort. ex Tanaka | 0.04242 |\n\nStatement: All Essential oils has unique IC 50 value.",
  "question": "Is the assertion backed by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa82313c225",
  "kind": "yes/no",
  "text": "Statement 1: The room was dark so I turned on the lamp.\nStatement 2: The room was dark so I turned on the stereo.",
  "question": "Of these two statements, does Statement 1 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q5e205470ef",
  "kind": "yes/no",
  "text": "Complaint narrative: WHILE MY WIFE, LINDA, WAS DRIVING LESS THAN 1-2 MPH, TURNING INTO A PARKING SPACE, ALL OF A SUDDEN, THE ENGINE STARTED RACING AND LEAPED FORWARD. HITTING THE BRAKES HAD NO EFFECT ON STOPPING THE VEHICLE. SHE DESPERATELY TURNED THE WHEEL TO MISS PARKED CARS, A STEEL POLE WAS HIT AND TORN OUT OF THE GROUND BY THE RUNAWAY VEHICLE. FINALLY THE CAR CAME TO REST AFTER HITTING A LARGE CONCRETE LIGHT POLE, WHICH MUST HAVE STALLED OUT THE ENGINE. MY WIFE WAS IN A STATE OF SHOCK AND HAD TO GO TO THE HOSPITAL FOR TESTS / XRAYS. EVEN WITH THE SEAT BELT ON, SHE RECEIVED MAJOR IMPACT FROM THE STEERING WHEEL TO HER CHEST.",
  "question": "In this vehicle safety complaint, does it report that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qc6bf30ef62",
  "kind": "yes/no",
  "text": "Occupation: Pediatric Surgeons\nDuties:\n- Perform transplantation operations, such as organ transplants, on fetuses, infants, children, and adolescents.\n- Examine fetuses, infants, children, and adolescents, and diagnose health issues to determine need for intervention, such as surgery.\n- Operate on fetuses, infants, children, and adolescents to correct deformities, repair injuries, prevent and treat diseases, or improve or restore patients' functions.",
  "question": "Is it the case that the listed duties are not part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "qddd7353b84",
  "kind": "yes/no",
  "text": "Occupation: Skincare Specialists\nDuties:\n- Determine which products or colors will improve clients' skin quality and appearance.\n- Examine clients' skin, using magnifying lamps or visors when necessary, to evaluate skin condition and appearance.\n- Perform simple extractions to remove blackheads.",
  "question": "Are the listed duties part of the job, for the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q3578c79b19",
  "kind": "yes/no",
  "text": "Situation: I don’t mind vertical filming on phones because I find it hard to hold my phone sideways.\nAction being judged: Not following established social norms.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q0f35e4f9c4",
  "kind": "yes/no",
  "text": "Complaint narrative: PULLING DOWN MY DRIVE WAY MY VEHICLE ACCELERATED WITHOUT ME TRYING. I HIT THE BRAKE AND E BRAKE. IT DID NOT STOP US. IN RESULT OF THE ACCELERATION MY HOUSE STOPPED US.",
  "question": "Has this vehicle safety complaint reported that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q7e5a698b15",
  "kind": "yes/no",
  "text": "This summer's once-in-a-half-century Midwestern drought caused global prices for staple food products to soar by 10%and corn in particular to jump by 25%, according to the World Bank. The food shortages across Africa, the Middle East and South America are the worst since the 1980s and have produced hunger and political instability, according to the United Nations.",
  "question": "Is it the case that this paragraph does not make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable.\n- no: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy."
 },
 {
  "qid": "qdfa71e418d",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nConclusion and Relevance: Among patients with severe or life-threatening COVID-19, convalescent plasma therapy added to standard treatment, compared with standard treatment alone, did not result in a statistically significant improvement in time to clinical improvement within 28 days.\n\nClaim: COVID-19 patients treated with convalescent plasma recover at faster rates than those without treatment.",
  "question": "Is the claim contradicted by the evidence?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qbfb2911a5c",
  "kind": "yes/no",
  "text": "Assistant: What time?\nCustomer: 3pm today.\nAssistant: Okay, there are not two tickets available to see Shazam! at 3:00 at the Cinemark Sugarhouse today. Would you like a different time?",
  "question": "Does the assistant's final message confirm \"3:00\" for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q703e6e681e",
  "kind": "yes/no",
  "text": "Customer: yes, 7 people 4 nights starting Wednesday.\nAssistant: I'm sorry. There is no availability. Would you like to try different dates or another hotel?",
  "question": "Does the assistant's reply confirm that it was actually made, the booking the customer asked for?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "qfcdc89cfa0",
  "kind": "yes/no",
  "text": "Customer: Yes can I make a reservation for 1 people at 16:15 on wednesday?\nAssistant: I'm sorry, there are no available tables at that time. Would you like me to look for a different restaurant?",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "q480b005773",
  "kind": "yes/no",
  "text": "Statement 1: She took her fish for a walk.\nStatement 2: She took her dog for a walk.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q468242bf88",
  "kind": "yes/no",
  "text": "Occupation: Fabric and Apparel Patternmakers\nDuties:\n- Start pumps to operate distilling systems that drain and reclaim dry cleaning solvents.\n- Operate machines that comb, dry and polish furs, clean, sterilize and fluff feathers and blankets, or roll and package towels.\n- Hang curtains, drapes, blankets, pants, and other garments on stretch frames to dry.",
  "question": "So, are the duties on the list part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q13f16015bd",
  "kind": "yes/no",
  "text": "Assistant: Sorry, but the only 3D showing is at 5:30 pm\nCustomer: That won't work for us. Can you book me the regualar movie at 8pm?\nAssistant: There is no 8pm show. There is a 7pm or 830pm showing",
  "question": "Pursuant to the assistant's final message, is \"8pm\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9f5a69e403",
  "kind": "yes/no",
  "text": "Statement 1: The pilot was not even injured after the air crash since he had watch with him\nStatement 2: The pilot was not even injured after the air crash since he had parachute with him",
  "question": "Is it right to say that, of these two statements, Statement 1 doesn't go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "qb2ac108fe5",
  "kind": "yes/no",
  "text": "Like with temperature and sea level data, government climate scientists are tampering with data to make it appear that the past was colder, had lower sea level, and had more sea ice. Perhaps Hansen has been consulting with JAXA.",
  "question": "Is it true that this paragraph does not make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable.\n- no: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy."
 },
 {
  "qid": "q76d2b938ba",
  "kind": "yes/no",
  "text": "Table caption: Results of linear models on the effects of a species’ relative frequency in the seed mixture (hypothesis 3) , fungicide application (hypothesis 4) , and insecticide application (hypothesis 4) as well as their interactions, and the effect of block on aboveground biomass two years after sowing for four exotic focal species. Note that two species ( O. viciifolia, B. orientalis ) had to be omitted because of the many zero values for biomass. See method section for further information on model structure. Abbreviations for factors are given in brackets. (* P < 0.05, *** P < 0.001).\n| Source |  | L. multiflorum | M . x varia | D. giganteus | P . peregrina |\n|  | d.f. | Ξ 2 values | Ξ 2 values | Ξ 2 values | Ξ 2 values |\n| Relative frequency [RF] | 1 | 17.32 *** | 1.99 | 34.56 *** | 31.26 *** |\n| Fungicide application [F] | 1 | 3.48 | 1.71 | 0.46 | 5.12 * |\n| Insecticide application [I] | 1 | 0.12 | 0.45 | 0.01 | 0.01 |\n| RF x F | 1 | 6.26 * | 0.11 | 0.00 | 6.55 * |\n| RF x I | 1 | 0.02 | 0.00 | 0.29 | 3.77 |\n| F x I | 1 | 0.82 | 0.28 | 0.47 | 0.00 |\n| RF x F x I | 1 | 0.30 | 0.08 | 0.00 | 6.40 * |\n| Block | 4 | 5.47 | 6.86 | 9.07 | 4.08 |\n\nStatement: RF x F x I has 9.40 * as P . peregrina value.",
  "question": "Is it right to say that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q97f94c665d",
  "kind": "yes/no",
  "text": "Complaint narrative: DASH IS FALLING APART, FULL OF CRACKS; CHUNKS OF PLASTIC DASH HAVE BROKEN OFF. POTENTIAL SAFETY ISSUE IF INVOLVED IN AN ACCIDENT, ESPECIALLY IF DASH AIRBAG IS DEPLOYED. LARGE SHARP PIECES OF DASH WILL BREAK LOOSE AND BECOME PROJECTILES/ SHRAPNEL. I BELIEVE SUNLIGHT AND HIGH HEAT IN PARKED CAR HAS CAUSED THIS. NOT CAUSED BY AN ACCIDENT. DEFINITELY A DESIGN FLAW. SHOULD BE RECALLED.",
  "question": "So, does this vehicle safety complaint say at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qb4bc1dbae1",
  "kind": "yes/no",
  "text": "Customer: I would like to try to find tickets for the movies tonight.\nAgent: Ok. What theater do you prefer?\nCustomer: Oxford theater.\nAgent: What movie do you want to see?\nCustomer: Twist.\nAgent: What time would you like to go?\nCustomer: Either before dinner around 5 or after dinner around 9:00.\nAgent: Please hold, I will check the times.\nCustomer: Thank you.\nAgent: Unfortunately, they only show with tickets left is at 7:00.\nCustomer: That won't work, our dinner reservation is at 7:00.\nAgent: Is there a different theater you can go to?\nCustomer: No, we really like Oxford.\nAgent: Are there any other movies you want to see?\nCustomer: I would like to see Flash.\nAgent: I will check the times.\nCustomer: Thank you.\nAgent: Flash is all sold out for tonight.\nCustomer: Ok, we will have to go to the movies another night.\nAgent: I'm sorry I could not be more helpful.",
  "question": "Has the customer, by the end of this conversation, actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qcb171d5fd3",
  "kind": "yes/no",
  "text": "Assistant: The cost of the repair will be $45.00\nCustomer: Okay that's not bad.\nAssistant: No, and they have you scheduled for 8:30 a.m.",
  "question": "Is it the case that, according to the assistant's last message, \"8:30 a.m\" is not confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order.\n- no: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction."
 },
 {
  "qid": "q5c11c58422",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2006, the science journal \"Nature\" listed Pharyngula as the top-ranked blog written by a scientist.\n\nSummary sentence:\nIn 2006 the journal \"Nature\" listed Myers's \"Pharyngula\" as the top-ranked blog by a scientist based on popularity.",
  "question": "Is every item of information in the summary sentence backed by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qc8a1cf4fc0",
  "kind": "yes/no",
  "text": "Customer: I want to see Star Wars tonight at the theater.\nAgent: Okay, I understand you'd like to see Star Wars: the Rise of Skywalker today. Let's buy some movie tickets. First off, how many tickets are you looking to buy?\nCustomer: 4\nAgent: Wonderful. Based on your location, the nearest theaters to you are the Alamo Drafthouse Sloans Lake and the Regal UA Denver. Would you like one of these, or should I look somewhere else?\nCustomer: Regal Denver.\nAgent: Okay, let me look up 4 tickets for Star Wars: the Rise of Skywalker at the Regal UA Denver. What time would you like to go? You can say morning, afternoon, evening, or just name a time, and I'll find something close.\nCustomer: Evening.\nAgent: Okay. Looking up showtimes, I see that Star Wars: the Rise of Skywalker is playing at: 6:30 PM, 9:15 PM. Would you like one of those showtimes?\nCustomer: No. Change order.\nAgent: Okay, I understand you'd like to change something about your order. Say what you'd to change, and we'll look up more tickets.\nCustomer: Movie.\nAgent: I understand you'd like to change movies. What movie would you like to see? Or would you like suggestions?\nCustomer: Jumanji.\nAgent: Okay, let me look up movie tickets for Jumanji: The Next Level. Would you like to keep all previous order details the same?\nCustomer: Yes.\nAgent: Okay. No problem. Looking up tickets, I see that Jumanji: The Next Level is playing at: 7:30 PM, 10:00 PM. Would you like one of these showtimes?\nCustomer: 7:30 PM.\nAgent: Perfect. Let's just make sure everything looks right. You'd like to see Jumanji: The Next Level at the Regal UA Denver, today, 7:30 PM, and you want to buy 4 tickets, which come to a total of $46.32 after fees and taxes. Is this correct?\nCustomer: Correct.\nAgent: To confirm your purchase, please say 'buy movie tickets'.\nCustomer: Buy movie tickets.\nAgent: Thank you! Your tickets have been purchased, and will be e-mailed to you shortly.",
  "question": "Has the customer, by the end of this conversation, actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qcdaf12c0ad",
  "kind": "yes/no",
  "text": "Situation: Couple Weighs Reconciliation Five Years After Violent Split\nAction being judged: Letting things get violent.",
  "question": "Is it true that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q0dc0619568",
  "kind": "yes/no",
  "text": "Statement 1: jim cut his finger with the soap\nStatement 2: jim cut his finger with the knife",
  "question": "Would it be correct to say that, of these two statements, Statement 2 does not go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q356a43072c",
  "kind": "yes/no",
  "text": "Occupation: Chemical Plant and System Operators\nDuties:\n- Control or operate chemical processes or systems of machines, using panelboards, control boards, or semi-automatic equipment.\n- Move control settings to make necessary adjustments on equipment units affecting speeds of chemical reactions, quality, or yields.\n- Interpret chemical reactions visible through sight glasses or on television monitors and review laboratory test reports for process adjustments.",
  "question": "Based on the text, are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qdf5ff1db4d",
  "kind": "yes/no",
  "text": "Assistant: Looks like 8:30 PM works as well! Did you want me to book this?\nCustomer: Yes, please!\nAssistant: Okay! 8:30 PM is booked!",
  "question": "Going by the assistant's latest message, is \"8:30 PM\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q188251d380",
  "kind": "yes/no",
  "text": "Customer: I really love bistro food\nAssistant: Unfortunately, there does not seem to be any bistros in the west side of town, I can look in other areas if you'd like?",
  "question": "Did the assistant, in its reply, find for the customer at least a single option meeting everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q579e9637eb",
  "kind": "yes/no",
  "text": "Occupation: Roofers\nDuties:\n- Scrape and sand floor edges and areas inaccessible to floor sanders, using scrapers, disk-type sanders, and sandpaper.\n- Buff and vacuum floors to ensure their cleanliness prior to the application of finish.\n- Attach sandpaper to rollers of sanding machines.",
  "question": "Is it true that the listed duties aren't part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "q612511406d",
  "kind": "yes/no",
  "text": "Statement 1: The mechanic fixed my car while it was in the shop.\nStatement 2: The mechanic sank my car while it was in the shop.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qa4b1044672",
  "kind": "yes/no",
  "text": "Occupation: Chemical Equipment Operators and Tenders\nDuties:\n- Examine drawings, negatives, or photographic prints to determine coloring, shading, accenting, or other changes required for retouching or restoration.\n- Splice broken or separated film and mount film on reels.\n- Produce timed prints with separate densities or color settings for each scene of a production.",
  "question": "Are the listed duties part of the above-named occupation's job?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q09be7af85e",
  "kind": "yes/no",
  "text": "Table caption: Example for the sum score options for one text in the assessment with a dynamic approach.\n| Scoring and sum score option | Performance on each question type for one text | Performance on each question type for one text | Performance on each question type for one text | Performance on each question type for one text |\n| Scoring and sum score option | Orthographic knowledge | Vocabulary | Sentence-integration | Global text comprehension |\n| Item scoring for first attempts | Item 1 = 0 Item 2 = 0 Item 3 = 2 | Item 1 = 0 Item 2 = 0 | Item 1 = 0 | Item 1 = 1 |\n| Item scoring for first and second attempts | Item 1 = 1 Item 2 = 0 Item 3 = 2 | Item 1 = 1 Item 2 = 1 | Item 1 = 1 | No feedback |\n| Sum score for first attempts | 2 | 0 | 0 | 1 |\n| Sum score for first and second attempts | 3 | 2 | 1 | No feedback |\nTable notes: Note. Item scoring for first attempts (first attempt correct = 2, second attempt correct or incorrect = 0), item scoring for first and second attempts (first attempt correct = 2, second attempt correct = 1, second attempt incorrect = 0).\n\nStatement: Sum score for first attempts three Orthographic knowledge.",
  "question": "Is the assertion backed by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q272c815643",
  "kind": "yes/no",
  "text": "Customer: Hello what movies are playing in the Petoskey area?\nAgent: There are several do you have a preference?\nCustomer: Just list a few and tell me about them.\nAgent: Okay I will list them in release date.\nCustomer: That's good\nAgent: The Gentleman is about a drug lord that tries to sell off his empire\nCustomer: No I'm not into drug lords\nAgent: Okay then there is Gretel and Hansel an offbeat take on the fairy tale.\nCustomer: No interest there either.\nAgent: Bad boys for life is the third instalment of the bad boy starring will smith and Martin lawrence\nCustomer: No I am taking my wife and she would not like that film. Is there any comedy type films.\nAgent: How about Jumanji the next level?\nCustomer: That sounds like a winner we saw the first one and loved it.\nAgent: Okay do you have a time preferences?\nCustomer: Well we will be going to dinner first so the later show would be preferable.\nAgent: There is a 915pm show at the Petoskey Cinema for Jumanji the next level for tonight.\nCustomer: No i am not booking for tonight, this is for Valentines and I am taking my wife to dinner and A movie.\nAgent: So you wish to book the tickets for February 14th.\nCustomer: Make it the thirteenth of February,\nAgent: I can order the tickets if you wish.\nCustomer: No wait until the twelfth, then order in case my plans change.\nAgent: Okay just to confirm on the twelfth of February you wish me to order two tickets for Jumanji the next level for the 915 pm show at The Petoskey Cinema.\nCustomer: Sounds great\nAgent: Consider it done",
  "question": "By the close of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qc8888feb12",
  "kind": "yes/no",
  "text": "Assistant: ok and the type of crust?\nCustomer: Gluten free cast.\nAssistant: so your order is: 2 medium chicken bbq pizzas with gluten free crust.",
  "question": "Is \"chicken bbq pizzas\" confirmed for the customer's pizza order according to the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe3fac12db8",
  "kind": "yes/no",
  "text": "Customer: What are the showtimes for Bad Boys for life at Cinemark?\nAgent: 11am, 12pm, 1pm, 2pm, 3pm, 5pm, 7pm, 9pm, and 11pm\nCustomer: What time is the IMAX showing?\nAgent: 7pm, 9pm, and 11pm\nCustomer: How many seats are available for the 7pm showing?\nAgent: There are only 6 seats left.\nCustomer: How many seats are available for the 11pm showing?\nAgent: The 11 p.m. is sold out.\nCustomer: What is the price of a regular ticket?\nAgent: 8 dollars\nCustomer: How many seats are available for the 11 am showing?\nAgent: There are 24 seats left.\nCustomer: How many seats are available for the 11pm showing tomorrow?\nAgent: The 11 p.m. is sold out.\nCustomer: What day are there seats available for the 11pm showing?\nAgent: Monday\nCustomer: How many seats are available?\nAgent: There are 10 seats left.\nCustomer: Great thanks.\nAgent: You're welcome.",
  "question": "By the end of this dialogue, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q996075280e",
  "kind": "yes/no",
  "text": "Customer: Hi, I'd like to see a movie tonight.\nAgent: Ok, great which movie do you want to see?\nCustomer: Umm, not sure either No Time to Die or Mulan.\nAgent: Ok, let me check. Where are you located?\nCustomer: Stoneyford Oregon.\nAgent: Ok, let me check Mountain AMC 16.\nCustomer: Great.\nAgent: Oh, no, unfortunately this theater is closed.\nCustomer: Ok, is there any other theater near me?\nAgent: Yes, let me check Holiday Cinemark 12.\nCustomer: Great.\nAgent: Ok, it seems like this theater is closed.\nCustomer: Oh, that's unfortunate.\nAgent: Yes, I can't seem to find any movie theaters open in your area.\nCustomer: Hmmm ok.\nAgent: After some research, I've found that no time to die's release date has been postponed, as well as Mulan's.\nCustomer: Do you know until when?\nAgent: Yes, they are both postponed until the fall.\nCustomer: Ok, thanks for your help.\nAgent: You're welcome.",
  "question": "Has the customer actually bought movie tickets by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 }
]
