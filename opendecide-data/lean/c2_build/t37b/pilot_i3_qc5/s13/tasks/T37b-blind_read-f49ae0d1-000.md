# T37b blind solver T37b-blind_read-f49ae0d1-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3_qc5/s13/answers/T37b-blind_read-f49ae0d1-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qd76a70d0ad",
  "kind": "yes/no",
  "text": "Customer: Please make a suggestion and provide the postcode, address, and phone number.\nAssistant: The hotel du vin and bistro is my favorite. Address is 15 - 19 Trumpington Street cb21qa, phone 01223227330",
  "question": "In its reply, did the assistant find at least a single option that satisfies everything the customer requested?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q7277badc84",
  "kind": "yes/no",
  "text": "Assistant: What toppings would you like on it?\nCustomer: I'd like for it to be cheese, hawaiian, and bacon\nAssistant: Unfortunately, the store does not have hawaiian as a topping in stock at the moment",
  "question": "Is it correct that, according to the assistant's last message, \"hawaiian\" isn't confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order.\n- no: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction."
 },
 {
  "qid": "q06db52cc28",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He finished the 2015–16 season leading the Lakers and all rookies in steals per game, and became the youngest player to hit 130 three-pointers in a season.\n- He subsequently earned NBA All-Rookie Second Team honors.\n\nSummary sentence:\nHe was named to the NBA All-Rookie Second Team with the Lakers in 2016.",
  "question": "Is every piece of info in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qb05b65ffd4",
  "kind": "yes/no",
  "text": "Table caption: Consensus scores from clinical evaluation of [ 18 F]FDG PET comparing attenuation correction using CT and DeepDixon (VE11P; n = 104).\n| Consensus score | Number |\n| No difference | 78 (75%) |\n| Minor, not significant | 25 (24%) |\n| Clinically significant | 1 (1%)* |\nTable notes: * Difference caused by warp error in spatial normalization.\n\nStatement: 78 is the number for Consensus score of No difference.",
  "question": "Does the data table back up the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q2a87e3beab",
  "kind": "yes/no",
  "text": "Customer: Look up showtimes for Parasite\nAgent: OK, here's some of the showtimes for Parasite today near you.\nCustomer: Look for showtimes in theaters in Los Angeles.\nAgent: Ok, here are the showtimes for Parasite today near Los Angeles.\nCustomer: Actually look up the showtimes for tomorrow near Los Angeles\nAgent: Here are the showtimes for Parasite for tomorrow.\nCustomer: What theaters have showtimes around or after 9:00 PM?\nAgent: Alamo Drafthouse Cinemas, ArcLight Cinemas - Hollywood, AMC Atlantic Times Square, AMC Burbank, and ArcLight Cinemas - Pasadena all have showtimes around 9:00 PM.\nCustomer: Can you show me the seats available at Alamo Drafthouse at 9:00PM?\nAgent: Here are the seats available for Alamo Drafthouse.\nCustomer: Ok, now show me the seats for ArcLight Cinemas\nAgent: Great, here are the seats for ArcLight Cinemas at 9:00PM\nCustomer: Ok, I'll book 4 tickets for Arclight Cinemas - Hollywood\nAgent: Please pick which seats you want.\nCustomer: Ok done.\nAgent: Great. Just to confirm, here are the four seats for the 9:15 PM showtime at Arclight Cinemas - Pasadena.\nCustomer: No, cancel that. I'd like tickets for ArcLight Cinemas - Hollywood at 9:00 PM\nAgent: Oops, sorry about that. Here are the seats available for ArcLight Cinemas - Hollywood, please pick your seats.\nCustomer: Ok done.\nAgent: Just to confirm, you ordered 4 tickets for the 9:00 PM showtime of Parasite at Arclight Cinemas - Hollywood. Is that correct?\nCustomer: Yes, that's right.\nAgent: Please confirm the payment.\nCustomer: Ok done, thanks.\nAgent: Ok, tickets are booked for Parasite for 9:00 PM at ArcLight Cinemas. Enjoy the movie!",
  "question": "By the conclusion of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qd3d710a041",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNED A 2004 HONDA CR-V. THE CONTACT STATED THAT THE VEHICLE WAS INVOLVED IN A REAR END COLLISION WITH A SEMI-TRUCK. THE AIR BAGS DID NOT DEPLOY. A POLICE REPORT WAS FILED. THE VEHICLE WAS TOWED TO A SALVAGE YARD AND DEEMED DESTROYED. THE CONTACT SUFFERED A CONTUSION AND MODERATE HEADACHES, WHICH REQUIRED MEDICAL ATTENTION. THE MANUFACTURER WAS NOTIFIED OF THE FAILURE. THE FAILURE MILEAGE WAS APPROXIMATELY 250,000.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "q1294d656f0",
  "kind": "yes/no",
  "text": "Statement 1: There are seventy minutes in an hour\nStatement 2: There are sixty minutes in an hour",
  "question": "Of these two statements, does Statement 1 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q2adcd6dc79",
  "kind": "yes/no",
  "text": "Situation: But not to hurt feelings, she said she liked them.\nAction being judged: Protecting the feelings of others.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qa68ae8f329",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS AND RELEVANCE: In this survey of heath care workers in hospitals equipped with fever clinics or wards for patients with COVID-19 in Wuhan and other regions in China, participants reported experiencing psychological burden, especially nurses, women, those in Wuhan, and frontline health care workers directly engaged in the diagnosis, treatment, and care for patients with COVID-19.\n\nClaim: Female front-line workers treating patients with COVID-19 experienced higher rates or more severe symptoms of depression, anxiety, insomnia and distress than health-care workers overall.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qca6430a337",
  "kind": "yes/no",
  "text": "Customer: Can you book it for me? Just for one person starting on Wednesday for 5 nights.\nAssistant: I'm sorry, none of the hotels in the centre are free on those dates.  Would you like to try a different number of days?",
  "question": "Does the assistant's reply confirm the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q349deff59c",
  "kind": "yes/no",
  "text": "Occupation: Medical Equipment Repairers\nDuties:\n- Mix specified amounts of sand, clay, mortar powder, and water to form refractory clay or mortar, using shovels or mixing machines.\n- Climb scaffolding, carrying hoses, and spray surfaces of cupolas with refractory mixtures, using spray equipment.\n- Remove worn or damaged plastic block refractory linings of furnaces, using hand tools.",
  "question": "Is the inclusion of the listed duties in the job of the occupation named above true?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qbc2f464130",
  "kind": "yes/no",
  "text": "Marine life, including that part that fixes CO 2 as the carbonate in limestones such as coral reefs, evolved on an Earth with CO 2 levels many times higher than those of today, as reported by Berner and Kothaval. It may be true to say that todays marine life is getting by in a CO 2 -deprived environment.",
  "question": "Does the paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qbc83ea4e61",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nFINDINGS: COVID-19 transmissibility measured by R(t) has remained at approximately 1 for 8 weeks in Hong Kong. Among respondents to the surveys, 74·5%, 97·5%, and 98·8% reported wearing masks when going out, and 61·3%, 90·2%, and 85·1% reported avoiding crowded places in surveys 1 (n=1008), 2 (n=1000), and 3 (n=1005), respectively. INTERPRETATION: Our study shows that non-pharmaceutical interventions (including border restrictions, quarantine and isolation, distancing, and changes in population behaviour) were associated with reduced transmission of COVID-19 in Hong Kong, and are also likely to have substantially reduced influenza transmission in early February, 2020.\n\nClaim: In Hong Kong, citizens’ near-universal mask-wearing is a factor in the reduced transmission of COVID-19.",
  "question": "Does the evidence back up the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q97f4ba710e",
  "kind": "yes/no",
  "text": "Rudbeckia\nRudbeckia is a plant genus in the sunflower family. The species are commonly called coneflowers and black-eyed-susans; all are native to North America and many species are cultivated in gardens for their showy yellow or gold flower heads.\n\nPhysocarpus\nPhysocarpus, commonly called ninebark, is a genus of flowering plants in the family Rosaceae, native to North America (most species) and northeastern Asia (one species).",
  "question": "Is it right to say that Physocarpus and Rudbeckia aren't both genus of flowering plants?",
  "definitions": "- yes: The paragraphs do not bear out the positive statement (the question read without its 'not' or 'fail to'): at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer.\n- no: Read together, the paragraphs show that the positive statement (the question read without its 'not' or 'fail to') holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right)."
 },
 {
  "qid": "q2c867d7810",
  "kind": "yes/no",
  "text": "Complaint narrative: WHILE DRIVING DOWN THE ROAD AT SLOW SPEED IN THE NEIGHBORHOOD, THE CAR RANDOMLY SHUTS OFF. THE POWER STEERING, THE POWER BRAKES AND THE ENGINE STOP WORKING. IT IS HAPPENING NOW MORE FREQUENTLY - TWICE TODAY AND MY WIFE AND KIDS NEARLY HAD A HEAD ON ACCIDENT. LUCKILY THE OTHER CAR WAS ABLE TO SWERVE TO MISS OUR VAN OTHERWISE THERE WOULD HAVE BEEN A HEAD-ON. I TOOK THE CAR TO MY DEALERSHIP SEVERAL TIMES OVER THE LAST FEW MONTHS BASED ON A RECALL NOTICE THAT WAS ISSUED FOR THE VAN. I WAS TOLD THAT THEY DO NOT HAVE THE PARTS TO FIX IT AND THAT THEY HAVE NO IDEA WHEN THE PARTS WILL BE AVAILABLE. HOW MANY PEOPLE NEED TO BE HURT BY THIS ISSUE BEFORE THEY START DELIVERING THE PARTS TO FIX IT?",
  "question": "Does this complaint about vehicle safety report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q4108c3f7df",
  "kind": "yes/no",
  "text": "Customer: I need to buy tickets for Possession for me and my mom.\nAgent: How many tickets?\nCustomer: Two tickets.\nAgent: What day is this purchase for?\nCustomer: Today.\nAgent: What theater would you like?\nCustomer: Which theater has the latest showtime?\nAgent: Cima Ultraplex 20 has showings at 4:00pm, 6:10pm, and 8:30pm.\nCustomer: What about the other theater?\nAgent: Northgate Cinemas 12 has showings at 6:00pm, 8:10pm, and 10:25pm.\nCustomer: I'll do Northgate Cinemas 12 at 10:25 pm.\nAgent: Okay. To confirm, it is two tickets for Possession at Northgate Cinemas 12 at 10:25 pm tomorrow?\nCustomer: No, the tickets are for today.\nAgent: Sorry about that. Two tickets for Possession at Northgate Cinemas 12 at 10:25 pm today.\nCustomer: Yes, that is correct.\nAgent: Your tickets are confirmed and they've been sent to your email address.\nCustomer: Okay, thank you.\nAgent: You're welcome. Have a good day.\nCustomer: Goodbye.\nAgent: Goodbye.",
  "question": "By the end of this conversation, is there actually a purchase of movie tickets by the customer?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q79dd5e762b",
  "kind": "yes/no",
  "text": "Situation: Baby by a married man\nAction being judged: Cheating on your partner and having a baby with someone else.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q9d7f9422b4",
  "kind": "yes/no",
  "text": "Table caption: Strontium separation, modified after .\n| Step | Amount (ml) | Molarity [mol l −1 ] | Reagent | Elution |\n| Condition | 1 | 3 | HNO 3 |  |\n| Load | 1 | 3 | HNO 3 | Mg, Ca, Zn, Fe, Rb |\n| Wash | 4 | 3 | HNO 3 |  |\n| Collect | 3 | – | H 2 O | Sr, Ca |\n\nStatement: The table contain 4 Step such as Condition, Load, Wash and Collect.",
  "question": "Does the table back up the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q03b271f733",
  "kind": "yes/no",
  "text": "Statement 1: I put the car seat in the car.\nStatement 2: I put the oven in the car.",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qb10d6a1cb7",
  "kind": "yes/no",
  "text": "Customer: ok and get me the reference number please\nAssistant: Reference number is : TFUP32PH. Is there anything else?",
  "question": "Was the booking the customer asked for actually made, as the assistant's reply confirms?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "qa34ae0fc63",
  "kind": "yes/no",
  "text": "Table caption: Correlation between self-ratings and politician ratings (Study 2, Austria).\n| PersonalityDomain | Item | r |\n| O | has fixed ideas, is traditional vs. self-aware person, open to novel things | 0.58 *** |\n| A | relentless, remains tough vs. compliant, compassionate | 0.46 *** |\n| C | casual, easygoing vs. disciplined, orderly | 0.33 *** |\n| S | emotional, shows emotions openly vs. controlled, even-tempered | 0.29 *** |\n| E | reserved, unobtrusive vs. vigorous, dominant | 0.27 *** |\nTable notes: Note: Correlation coefficients ordered by size. Weighting to known population benchmarks was applied; n = 629–631. Significance levels: * p < 0.05, ** p < 0.01 , *** p < 0.001. S = Emotional stability , E = Extraversion , O = Openness to experience , A = Agreeableness , C = Conscientiousness .\n\nStatement: Personality Domain of S item is emotional, shows emotions openly vs. controlled, even-tempered.",
  "question": "Is it the case that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q6a452f2ce0",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nOf these, 94 were working in an 11th-floor call center with 216 employees, translating to an attack rate of 43.5% (95% CI 36.9%–50.4%).\n\nClaim: Superspreading events can happen at call centers.",
  "question": "Does the evidence go against the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q7ecbc9c79e",
  "kind": "yes/no",
  "text": "Situation: Joe wanted to do a romantic dinner for his girlfriend.\nAction being judged: Having romantic dinners with your significant other.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q25c4691702",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Bachchan better established himself in Hindi cinema playing a no-nonsense Mumbai police officer in the hit action thriller \"Dhoom\" (2004), which also starred John Abraham, Uday Chopra, Esha Deol, and Rimi Sen in pivotal roles.\n\nSummary sentence:\nHis first commercial successes came with the 2003 & 2004 action films \"Zameen\" and \"Dhoom\", which changed his career prospects.",
  "question": "Is every piece of the summary sentence's information supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qd3298d221b",
  "kind": "yes/no",
  "text": "Customer: I'm looking for someplace to go in the west.\nAssistant: Might I recommend the Whale of a Time entertainment venue?",
  "question": "Is there confirmation that, in its reply, the assistant found at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q8dd74b9da6",
  "kind": "yes/no",
  "text": "Occupation: Wind Energy Development Managers\nDuties:\n- Participate in special education-related activities, such as attending meetings and providing support to special educators throughout the district.\n- Establish, coordinate, and oversee particular programs across school districts, such as programs to evaluate student academic achievement.\n- Advocate for new schools to be built, or for existing facilities to be repaired or remodeled.",
  "question": "Are the duties given in the list part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q3cc4c65947",
  "kind": "yes/no",
  "text": "Table caption: Peptide match of ARIP-B.\n| S. No | Plant description | Match Coverage (%) | Total Coverage (%) | RIP activity reported | RIP gene identified | Type of RIP | References |\n| 1 | Populus trichocarpa | 2 + 1 + 1 + 3 + 3 | 10 | Yes | Yes | Type 2 (B domain only) | Peumans and Vandamme (2010) |\n| 2 | Astragalus membranaceus | 10 | 10 | No | No | – | – |\n| 3 | Polygala tenuifolia | 1 | 1 | No | No | – | – |\n| 4 | Vitis vinifera | 0 + 2 | 2 | Yes | No | – | Peumans and Vandamme (2010) |\n| 5 | Triticum aestivum | 2 | 2 | Yes | Yes | Type 1 | Raj and Vennila (2013) |\n| 6 | Glycine max | 2 + 1 | 3 | Yes | No | – | Peumans and Vandamme (2010) |\n| 7 | Brachypodiumdistachyon | 1 | 1 | Yes | Yes | Type 3 | Peumans and Vandamme (2010) |\n| 8 | Hordeum vulgare | 3 | 3 | Yes | Yes | Type 1 | Raj and Vennila (2013) |\n| 9 | Ricinus communis | 2 | 2 | Yes | Yes | Type 2 | – |\n| 10 | Micromonaspusilla | 1 | 1 | Yes | No | – | Peumans and Vandamme (2010) |\n| 11 | Musa acuminata subsp. | 11 | 11 | No | No | – | – |\n| 12 | Arabidopsis lyrata subsp. | 3 | 3 | No | No | – | Peumans and Vandamme (2010) |\n\nStatement: There are four categories of Plant description.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q8884f84918",
  "kind": "yes/no",
  "text": "Table caption: Experimental results.\n| Sample ID | P eff [MPa] | v prop [mm/s] | K IIc [MPa*m 0.5 ] | k FOI [−] | e mech [mm] |\n| PGR6-RI-01-07 | 20 | 0.1 | 16.42 | ~520 | – |\n| PGR6-RI-01-08 | 20 | 0.3 | 15.71 | ~230 | 0.07 (0.09–0.1) |\n| PGR6-RI-01-09 | 20 | 0.3 | 15.34 | ~230 | 0.08 (0.07–0.1) |\n\nStatement: The highest standard deviation is 550.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qd4cf4c30d6",
  "kind": "yes/no",
  "text": "Table caption: Band positions and relative intensities in percentage of the samples studied with Raman microscopy. Bands with relative intensities below 5% are not listed.\n| C1-A | C1-A | C2-A | C2-A | C1-P1 | C1-P1 | C1-P2 | C1-P2 | C1-P3 | C1-P3 |\n| [cm −1 ] | [%] | [cm −1 ] | [%] | [cm −1 ] | [%] | [cm −1 ] | [%] | [cm −1 ] | [%] |\n| 1111 | 100 | 1109 | 77 | 1109 | 97 | 1110 | 93 | 1109 | 100 |\n| 1087 | – | 1089 | 29 | 1086 | 22 | 1085 | 47 | 1086 | 31 |\n| 1026 | 20 | 1026 | 15 | 1024 | 23 | 1024 | 23 | 1024 | 22 |\n| 783 | 9 | 779 | 5 | 782 | 8 | 782 | 10 | 781 | 9 |\n| 686 | 11 | 684 | 16 | 686 | 11 | 686 | 11 | 687 | 11 |\n| 603 | 99 | 603 | 100 | 602 | 100 | 601 | 100 | 601 | 98 |\n| 483 | 33 | 483 | 21 | 483 | 34 | 483 | 35 | 482 | 34 |\n| 427 | 20 | 427 | 15 | 427 | 23 | 427 | 23 | 426 | 24 |\n| 384 | 6 | 383 | 13 | 380 | 7 | 383 | 8 | 382 | 8 |\n| 288 | 17 | 283 | 19 | 289 | 16 | 284 | 17 | 290 | 17 |\n\nStatement: The lowest value in C1-P3 is 290.",
  "question": "Does the table provide support for the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf1f046c689",
  "kind": "yes/no",
  "text": "Complaint narrative: THE PASSENGER SEAT WARNING LIGHT.AND SEAT SENSOR MALFUNCTIONED AND NOW THE PASSENGER SEAT BELT WILL NOT ENGAGE.I CANNOT HAVE A PASSENGER IN MY TRUCK BECAUSE OF THI PROBLEM.I DON'T UNDERSTAND HOW THI COULD BE SAFE AT ALL.THE MANUAL SAYS THAT WHEN THIS HAPPENS TO BRING IT IN TO THE DEALER BECAUSE THE SENSOR AND THE SEAT BELT LATCH MUST BE REPLACED. I'VE OWNED.MANY VEHICLES IN MY LIFE AND NEVER EVER HAD A SEAT BELT FAILURE LIKE THIS .THIS IS DANGEROUS WHAT IF THIS OCCURS WHEN I HAVE A PASSENGER IN THE VEHICLE AND THE SEAT BELT.UNMATCHED OR WON'T UNMATCHED. HOW CAN THIS BE SAFE. NO ONE GETS INTO MY VEHICLES WITHOUT PUTTING ON THE SEAT BELTS IN N.Y.IT IS A VIOLATION",
  "question": "Is there a report in this vehicle safety complaint of at least a single person being actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qa75061e453",
  "kind": "yes/no",
  "text": "Further, if India and China don't also sign up to cut their carbon emissions-and they did not embrace Kyoto-these proposed dramatic cuts in American carbon emissions alone would not solve the problems of climate change.",
  "question": "Does this block of text make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q53f72e667a",
  "kind": "yes/no",
  "text": "Complaint narrative: ON NOVEMBER 14, 2017, I BEGAN HEARING SOME KNOCKING NOISE. ABOUT 15 MINUTES LATER, WHILE DRIVING ON THE HIGHWAY, THE SANTA FE SPORT STALLED WITH NO WARNING. I WAS IN HEAVY TRAFFIC AND IT WAS A VERY DANGEROUS SITUATION, WHERE PEOPLE WERE HONKING AND HAVING TO GO AROUND ME. I WAS SO SCARED. I WAS ABLE TO RESTART THE CAR AND DECIDED TO RETURN HOME INSTEAD OF GOING TO MY ORIGINAL DESTINATION. TEN MINUTES LATER, IN HEAVY TRAFFIC, THE SAME THING HAPPENED, THE SANTA FE SPORT STOPPED WITHOUT WARNING. I WAS ABLE TO RESTART THE CAR AND GET HOME. I NEVER RECEIVED ANY RECALL INFORMATION IN THE MAIL. I LATER LEARNED THAT IT IS HYUNDAI RECALL 162. THE SANTA FE HAS ABOUT 54,000 MILES ON IT.",
  "question": "Does this vehicle safety complaint state that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qa482213b4f",
  "kind": "yes/no",
  "text": "Customer: Wonderful. Can you also help me find a cool place to visit in town, maybe a theatre?\nAssistant: We have five excellent theatres in town, located in the centre and the south.",
  "question": "According to its reply, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qbcb2bc4e2c",
  "kind": "yes/no",
  "text": "Tissue and Lewis continue saying that \"glacial plants were severely carbon limited over a very long time period, until atmospheric CO2 began rising during the glacial-interglacial transition.\" In fact, they indicate that \"controlled environment studies with modern plants grown in glacial CO2\" have shown \"significant carbon limitations on plant physiology even when other resources were generally not limiting ,\" citing Dippery et al. (1995) and Tissue et al. (1995). So in spite of anything one could have done to enhance their productivity (other than supply them with more CO2), glacial-age plants simply could not produce the bounty that today's plants do. In fact, they were fortunate to merely survive.",
  "question": "Is it this paragraph that makes the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qb470611ef7",
  "kind": "yes/no",
  "text": "This theory was used to make predictions by at least 73 computer models. Thirty years of observations has proven every prediction wrong. Therefore their theory is wrong. That is how science works.",
  "question": "Within this paragraph, does it make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q8284ddecaf",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- William D. Casey\n- Casey was born in Amherst, Nova Scotia.\n- He was first elected, as a member of the Progressive Conservative Party of Canada, to represent the riding of Cumberland—Colchester in the 1988 election.\n- In common with almost every other PC Member of Parliament (MP) in the 1993 election he lost his seat, in his case being defeated by Liberal candidate Dianne Brushett.\n\nSummary sentence:\nWilliam D. Casey (born February 19, 1945) is a Canadian politician from Nova Scotia who served as a Member of Parliament (MP) in the House of Commons of Canada.",
  "question": "Is every item of information in the summary sentence backed by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q964e4d8c61",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThis cohort study examines the clinical characteristics of men with coronavirus disease 2019 whose semen tested positive for severe acute respiratory syndrome coronavirus 2.\n\nClaim: Scientists have found traces of the coronavirus in men's semen.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q668f017dc1",
  "kind": "yes/no",
  "text": "Table caption: Tree location and perception of traffic, pollution, and temperature.\n| Tree locations (excluding no trees as this was not preferred) | This blocks perception of traffic mean (Std Dev) | This lessens pollution exposure | This make me cooler |\n| Trees between cycle track and street/parked cars | 3.7 (2.3) | 4.1 (2.2) | 4.8 (2.2) |\n| Trees between sidewalk and cycle track | 3.7 (2.3) | 4.4 (2.2) | 5.2 (2.0) |\n| Trees and bushes between cycle track and street/parked cars | 4.7 (2.4) | 5.2 (2.0) | 5.4 (1.9) |\n\nStatement: Trees and bushes between cycle track and street/parked cars will have Same Traffic mean.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qc194b4a370",
  "kind": "yes/no",
  "text": "Complaint narrative: CONSISTENT WITH NHTSA ITEM #10119276, THE MAGNET CLUTCH TO THE AIR CONDITIONER COMPRESSOR DOES NOT ENGAGE CAUSING THE AIR CONDITIONER TO BLOW HOT AIR. UNDER CERTAIN CONDITIONS, THIS COULD POTENTIALLY OVEREXPOSE TTHE OPERATOR TO DANGEROUS LEVELS OF HEAT WHICH COULD ADVERSELY AFFECT THE OPERATOR'S ABILITY TO SAFELY CONTROL OF THE VEHICLE AND THEREFORE LEAD TO CRASHES AS WELL AS INJURY TO THE OPERATOR SUCH AS HEAT EXHAUSTION OR HEAT STROKE. WHEN THE VEHICLE IS MOVING, THE RISK OF THE OPERATOR'S OVEREXPOSURE TO THE HEAT CAN BE REDUCED BY ROLLING DOWN THE WINDOWS. HOWEVER DURING RAINFALL, AT SLOW SPEEDS OR WHILE AT A STANDSTILL, THAT OPTION IS NOT AVAILABLE. AS AN EXAMPLE, WHILE I WAS DRIVING ON THE INTERSTATE, I REACHED A SECTION THAT WAS SHUT DOWN. THE TRAFFIC WAS BACKED UP AND I WAS TRAPPED ON THE INTERSTATE FORCING ME TO OPERATE MY VEHICLE AT A STANDSTILL FOR AN EXTENDED PERIOD OF TIME. WHEN MY OVEREXPOSURE TO THE HEAT CAUSED ME TO BECOME FAINT AND DISORIENTED, I ABANDONED MY VEHICLE ON THE INTERSTATE AND MADE MY WAY TO THE SHOULDER OF THE INTERSTATE. A DOCTOR CAUGHTUP IN THE TRAFFIC BACKUP SAW ME AND WHILE ATTENDING ME STATED THAT I WAS SUFFERING FROM HEAT EXHAUSTION. OTHER MOTORISTS ASSISTED HIM AND WERE ABLE TO FIND SOMEONE WITH A COOLER OF ICE AND SO THE DOCTOR WAS ABLE TO TREAT ME BY ICING ME DOWN. THE DOCTOR TOLD ME THAT I WAS ON THE VERGE OF HEAT STROKE WHICH WAS AN EMERGENCY SITUATION. THIS INCIDENCE MADE ME REALIZE THAT A DEFECTIVE AIR CONDITIONER IS NOT SIMPLY UNCOMFORTABLE AND AN INCONVENIENCE BUT BECAUSE UNDER CERTAIN CONDITIONS IT CAN ADVERSELY AFFECT THE OPERATOR'S ABILITY TO SAFELY CONTROL THE VEHICLE, IT CAN LEAD TO UNSAFE DRIVING CONDITIONS. I NOW BELIEVE THAT ANY PROBLEM THAT HAS THE POTENTIAL TO ADVERSELY AFFECT THE OPERATOR'S ABILITY TO SAFELY CONTROL THE VEHICLE SHOULD BE CONSIDERED A SAFETY ISSUE.",
  "question": "Does this complaint about vehicle safety report that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qe4924391fa",
  "kind": "yes/no",
  "text": "Occupation: Multiple Machine Tool Setters, Operators, and Tenders, Metal and Plastic\nDuties:\n- Set up and operate machines, such as lathes, cutters, shears, borers, millers, grinders, presses, drills, or auxiliary machines, to make metallic and plastic workpieces.\n- Perform minor machine maintenance, such as oiling or cleaning machines, dies, or workpieces, or adding coolant to machine reservoirs.\n- Set machine stops or guides to specified lengths as indicated by scales, rules, or templates.",
  "question": "Based on the text, are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q3bc2144fa6",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nAmong these, we identify 66 druggable human proteins or host factors targeted by 69 existing FDA-approved drugs, drugs in clinical trials and/or preclinical compounds, that we are currently evaluating for efficacy in live SARS-CoV-2 infection assays.\n\nClaim: A research team found that no drugs target the same proteins in our cells the novel coronavirus does.",
  "question": "According to the text, does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q3a489b5d59",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNED A 2010 DODGE AVENGER. WHILE DRIVING 45 MPH, ANOTHER VEHICLE T- BONED THE CONTACT'S VEHICLE. THE FRONT AIR BAGS DEPLOYED, BUT THE SIDE CURTAIN AIR BAGS DID NOT. THE PASSENGER SUSTAINED A CONCUSSION, BROKEN NOSE, AND FRACTURED STERNUM. A POLICE REPORT WAS FILED. MEDICAL ATTENTION WAS RECEIVED. THE VEHICLE WAS DESTROYED AND TOWED. THE CONTACT RECEIVED NOTIFICATION OF NHTSA CAMPAIGN NUMBER: 16V668000 (AIR BAGS). THE MANUFACTURER WAS NOT NOTIFIED OF THE FAILURE. THE FAILURE MILEAGE WAS APPROXIMATELY 78,000.",
  "question": "According to this vehicle safety complaint, was at least a single person actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q25498b8db0",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Truro and Penwith College\n- Truro College was founded in 1993 as a new college in Gloweth near Threemilestone, Truro, Cornwall, to replace the Truro Sixth Form College.\n- It then became a tertiary college named Penwith College.\n- The decision to merge the two colleges was made in 2006, with the merger completed in 2008.\n- It is the top non-selective provider of the International Baccalaureate Diploma in the UK, according to Sunday Times Parent Power league tables.\n- Courses available include Further Education such as A Levels, T levels, Vocational Qualifications (including BTEC Diplomas, National Vocational Qualifications (NVQs) and apprenticeships), Foundation Studies, and the International Baccalaureate Diploma; Higher Education such as Honours Degrees, Foundation Degrees, Higher National Diplomas, higher level Nursing apprenticeships, education qualifications, other professional qualifications; part-time and evening courses.\n\nSummary sentence:\nTruro and Penwith College is a Tertiary College and Further Education College in Cornwall, UK.",
  "question": "Is every piece of information in the summary sentence substantiated by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q9a5307e17e",
  "kind": "yes/no",
  "text": "Homeopathy is based on the principles of like-cures-like and ultra-dilutions. The first says substances that can cause symptoms can be used in diluted form to treat the same symptom in an illness, and the second says the more dilute a substance is, the more potent it is.",
  "question": "Is this paragraph making the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qad22b2ac64",
  "kind": "yes/no",
  "text": "Table caption: Correlation between cerebral perfusion pressure and brain tissue oxygenation in 5 patients.\n| Patient No | Pearson coefficient (r) of correlation between CPP and PbtO 2 and probability (p) |\n| 1 | 0.79, p < 0.01 |\n| 2 | 0.38, p < 0.01 |\n| 3 | 0.35, p < 0.01 |\n| 4 | 0.77, p < 0.01 |\n| 5 | 0.7, p < 0.01 |\nTable notes: Abbreviations: r – Pearson's correlation coefficient; CPP – cerebral perfusion pressure; PbtO 2 – partial pressure of oxygen in brain tissue.\n\nStatement: Patient No 4 is having 0.77, p < 0.01 correlation between CPP and PbtO 2 and probability (p).",
  "question": "According to the table, is the statement supported?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q6d5a3e043d",
  "kind": "yes/no",
  "text": "Table caption: The importance of the first 5 principal components (PC) from the principal component analysis (PCA) for the biotic and abiotic factors.\n|  | PC1 | PC2 | PC3 | PC4 | PC5 |\n| Standard deviation | 1.95 | 1.85 | 1.60 | 1.30 | 1.17 |\n| Proportion of Variance | 0.24 | 0.21 | 0.16 | 0.10 | 0.09 |\n| Cumulative Proportion | 0.24 | 0.45 | 0.61 | 0.71 | 0.80 |\n\nStatement: There are 5 types of Principal components from PC1 to PC5.",
  "question": "Is it right to say that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qcad545f84b",
  "kind": "yes/no",
  "text": "Customer: Will you tell me about a couple of good movies that are currently playing in Spring Hills Kansas?\nAgent: Sure. Do you have a genre in mind?\nCustomer: I am open to anything that's entertaining.\nAgent: Beyond the Storm and Backcountry both receive great reviews from critics.\nCustomer: What are their ratings?\nAgent: Rotten Tomatoes gave Beyond the Storm 81% and Backcountry 91%.\nCustomer: Sounds like the critics like them. What are their storylines?\nAgent: Beyond the Storm is an action film about fishing out at sea and Backcountry is a documentary about Yosemite National Park.\nCustomer: Who directed Beyond the Storm?\nAgent: James Cameron is the director.\nCustomer: What theater and showtimes for Beyond the Storm?\nAgent: Beyond the Storm is currently showing at Cinemark Downtown at 1:30pm, 3:40pm, 6:10pm and 8:30pm.\nCustomer: What theater is showing Backcountry?\nAgent: Backcountry is also showing at Cinemark Downtown.\nCustomer: What are the showtimes for Backcountry?\nAgent: Backcountry is playing at 4:10pm, 7:30pm and 10:15pm.\nCustomer: I like the late showtime. Let me buy three tickets for Backcountry at 10:15pm for tomorrow.\nAgent: Please confirm the purchase of three tickets for Backcountry at 10:15pm for tomorrow at Cinemark Downtown.\nCustomer: That's just perfect.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "Is it correct that, by the end of this conversation, the customer has not actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "qba7217d2ff",
  "kind": "yes/no",
  "text": "Occupation: Molders, Shapers, and Casters, Except Metal and Plastic\nDuties:\n- Pour, pack, spread, or press plaster, concrete, or other materials into or around models or molds.\n- Construct or form molds for use in casting clay or plaster objects, using plaster, fiberglass, rubber, casting machines, patterns, or flasks.\n- Patch broken edges or fractures, using clay or plaster.",
  "question": "Is it accurate to say that the listed duties are not part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "q9c815032ab",
  "kind": "yes/no",
  "text": "Situation: I told them the train goes there but they don't like trains.\nAction being judged: When you don't want to give someone a ride, suggesting alternative means of transportation.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qc49bc2b730",
  "kind": "yes/no",
  "text": "But he, Osama, has also added some improvements. He claims to have found an Al Gore Rhythm to destroy the U.S. economy even more quickly than the conventional cap-and-trade bills were planning to do. A forced demise of the U.S. dollar is a part of his project to decarbonize the world's economy.",
  "question": "Does this paragraph come out with the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 }
]
