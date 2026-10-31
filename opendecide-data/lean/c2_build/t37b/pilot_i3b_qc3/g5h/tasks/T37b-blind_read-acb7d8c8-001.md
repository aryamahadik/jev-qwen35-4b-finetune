# G5-H blind read T37b-blind_read-acb7d8c8-001 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_qc3/g5h/answers/T37b-blind_read-acb7d8c8-001.json

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
  "qid": "q188ff07112",
  "kind": "yes/no",
  "text": "Table caption: The mechanical properties of the used steel bars\n| Nominal diameter (mm) | Actual area (mm 2 ) | Yield strength (MPa) | Ultimate strength (MPa) | Elongation (%) |\n| 8 | 49 | 551 | 690 | 17.2 |\n| 12 | 112 | 513 | 671 | 17.5 |\n| 16 | 199 | 482 | 618 | 18.75 |\nTable notes: Note; each value represented an average for three samples.\n\nStatement: 17.2 Elongation Nominal diameter is 8",
  "question": "Is the statement substantiated by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd8a703fbb2",
  "kind": "yes/no",
  "text": "Complaint narrative: MERCEDES BENZ GVA 250. CONSUMER WRITES IN REGARDS TO AIRBAGS BEING DEPLOYED UNEXPECTEDLY. *LD THE CONSUMER STATED THE AIR BAG DEPLOYED WHILE DRIVING CAUSING THE VEHICLE TO FLIP AND DRAGGED ON IT'S ROOF. THE CONSUMER SUFFERED MINOR SCRATCHES AND BRUISES, AS WELL AS A POSSIBLE MICRO CRACK IN A RIB.",
  "question": "Does this vehicle safety complaint state that at least a single individual was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q1dd441c474",
  "kind": "yes/no",
  "text": "Complaint narrative: 3 YR OLD CAR TRANSMISSION WENT OUT COMPLETELY WHILE I WAS DRIVING ON THE FREEWAY. I HAD TO DODGE SPEEDIG CARS TO ROLL OFF THE FREEWAY SINCE I HAD NO USE OF THE GAS PETAL OR SPEED. HAD TO HAVE IT TOWED. ERROR CODES P0732-GEAR 2 INCORRECT GEAR RATIO CAME BACK TO NEEDING A WHOLE NEW TRANSMISSION. HAD THEM FLUSH THE TRANSMISSION FOR $300 TO TRY AND SAVE IT TO NO AVAIL. THE SHIFTER CABLE IS ALREADY ON RECALL NOTICE 18S20/NHTSA RECALL 18V471 AND MY FORD DEALER CANT GET THE PART FOR MONTHS NOW BECAUSE ITS ON BACK ORDER. I BELIEVE THIS LED TO THE TOTAL DEMISE OF THE TRANSMISSION. A USED PART FOR $3000 IS NOT AN OPTION BECAUSE THE DEALERS CANT FIND ONE ANYWHERE. IM ASSUMING ITS DUE TO MANY PEOPLE HAVING THIS SAME ISSUE. MY ONLY OPTIONS ARE SPENDING $5400 ON A NEW TRANSMISSION OR GETTIG RID OF THE CAR THAT I STILL OWE MONEY ON TO SOMEONE WHO MAY SCRAP IT. NO SAFETY RECALL PARTS ARE AVAILABLE STILL AFTER MONTHS AND NO USED PARTS ARE ACAILABLE BECAUSE THERE ARE MANY MORE LIKE ME WITH THIS STYLE VEHICLE. ALSO IN JANUARY THERE WAS A RECALL NOTICE 17S09/NHTSA RECALL 17V-209 THAT HAD TO DO WITH THE CYLINDER HEAD CRACKED THAT MAY CAUSE OIL TO LEAK AND MAY RESULT IN A FIRE IN THE ENGINE COMPARTMENT .",
  "question": "Does this vehicle safety complaint say the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qbcd00cd85b",
  "kind": "yes/no",
  "text": "Statement 1: He shot the lion with a spoon\nStatement 2: He shot the lion with a gun.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q09da7212d4",
  "kind": "yes/no",
  "text": "Like with temperature and sea level data, government climate scientists are tampering with data to make it appear that the past was colder, had lower sea level, and had more sea ice. Perhaps Hansen has been consulting with JAXA.",
  "question": "Is it true that this paragraph does not make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable.\n- no: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy."
 },
 {
  "qid": "qea591bfcf6",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2000 PONTIAC GRAND PRIX. AFTER PARKING THE VEHICLE, THE CONTACT NOTICED SMOKE COMING FROM THE FRONT OF THE VEHICLE. THE CONTACT OPENED THE HOOD AND THE ENGINE COMPARTMENT WAS ON FIRE. THE CONTACT WAS ABLE TO EXTINGUISH THE FIRE. THE VEHICLE WAS INCLUDED IN NHTSA CAMPAIGN NUMBER: 15V701000 (ENGINE AND ENGINE COOLING). THE VEHICLE WAS TAKEN TO AN INDEPENDENT MECHANIC TO BE INSPECTED. THE VEHICLE WAS NOT REPAIRED. THE MANUFACTURER WAS NOT NOTIFIED OF THE FAILURE. THE FAILURE MILEAGE WAS 132,403. VIN TOOL CONFIRMS PARTS NOT AVAILABLE.",
  "question": "Does this vehicle safety complaint say the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qc41d14a03c",
  "kind": "yes/no",
  "text": "Statement 1: He communicated with his friends by newspapers\nStatement 2: He communicated with his friends by letter",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qdadd4810b2",
  "kind": "yes/no",
  "text": "If you play the 🎸 get in my pants immediately",
  "question": "Is it right to say that this post is not hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "qdb634412ab",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Laudrup now works as a pundit and co-commentator for Discovery Networks Denmark, covering the Premier League and Denmark national team.\n\nSummary sentence:\nHe currently works as a football commentator and pundit.",
  "question": "Is every piece of information in the summary sentence substantiated by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q37a71f9e87",
  "kind": "yes/no",
  "text": "Table caption: Resin duct metric name and description.\n| Metric | Type | Description |\n| Duct size (mm 2 ) | Unstandardized | Mean size of all ducts per annual ring |\n| Duct production (no. year −1 ) | Unstandardized | Total number of ducts per annual ring |\n| Total duct area (mm 2 year −1 ) | Unstandardized | Sum of duct area per annual ring |\n| Duct density (no. mm −2 year −1 ) | Standardized | Total number of ducts per annual ring divided by ring area |\n| Relative duct area (% annual ring) | Standardized | Total duct area divided by ring area × 100 |\n\nStatement: There are three table heads Metric , Type and Description.",
  "question": "Is it accurate to say that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qfce44a35f2",
  "kind": "yes/no",
  "text": "Occupation: Roofers\nDuties:\n- Scrape and sand floor edges and areas inaccessible to floor sanders, using scrapers, disk-type sanders, and sandpaper.\n- Buff and vacuum floors to ensure their cleanliness prior to the application of finish.\n- Attach sandpaper to rollers of sanding machines.",
  "question": "Is it true that the listed duties aren't part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "qb753952ff2",
  "kind": "yes/no",
  "text": "Customer: book for  6 people and three  nights starting on thursday.\nAssistant: Booking was successful.\nReference number is : ZCRPOLK8. anything else?",
  "question": "Is there confirmation in the assistant's reply that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q4baa150f1b",
  "kind": "yes/no",
  "text": "Customer: When is the next showing for Star Wars The Rise of Skywalker?\nAgent: What movie theater do you want me to search?\nCustomer: Try the AMC Hilton theater on 121st street.\nAgent: The next showing for Star Wars The Rise of Skywalker at the AMC Hilton is 8:15 PM.\nCustomer: Perfect time for me. What the cost for one adult ticket?\nAgent: One adult ticket costs $13.44, not including tax.\nCustomer: That's not too bad. Okay, book me a ticket, then.\nAgent: Ok, one adult ticket for the 8:15 PM showing of Star Wars The Rise of Skywalker at the AMD Hilton. What screening do you prefer?\nCustomer: Just standard is fine. Oh, is this theater running any deals?\nAgent: This week, all screenings for movies are the same price.\nCustomer: So, if I switch from standard screening to IMAX screening the picket of the ticket doesn't change?\nAgent: That's correct.\nCustomer: I can't miss this. Okay then, switch my screening from standard to IMAX.\nAgent: Ok, switching now.\nCustomer: Ok, play me back they details of the booking now.\nAgent: One adult ticket for the IMAX 8:15 PM showing of Star Wars The Rise of Skywalker at the AMD Hilton. Is that correct?\nCustomer: Yes, it is.\nAgent: How do you want to pay?\nCustomer: Use my Visa card, and include the tax in the final amount when you read the price to me.\nAgent: The total comes to $14.65, tax included. Please look in you email's inbox to get you digital receipt. Is there anything else?\nCustomer: No, that's all.\nAgent: Ok, goodbye.",
  "question": "Would it be correct to say that, by the end of this conversation, the customer hasn't actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "q91b3950e6e",
  "kind": "yes/no",
  "text": "It has been estimated that the U.S. national commitments to the UN to reduce emissions by 28% will prevent threehundredths of a degree centigrade in warming by 2100.",
  "question": "Is this paragraph making the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q9c3d9d95d2",
  "kind": "yes/no",
  "text": "Instead, the onus should be on the developers to prove the positive. No wind farm developer has ever had to explain the benefits of wind. Evidence tells us that wind power performance shows not only no reduction in CO 2 and other harmful emissions, but the very reverse. But Alex Salmond is driving an aggressive green agenda like an express train across Scotland, bludgeoning anyone who gets in the way as being a Luddite and anti-green.",
  "question": "Does this passage advance the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q9437b71609",
  "kind": "yes/no",
  "text": "Situation: Bride's Outrageous Demands Alienate Her Fiance's Sister\nAction being judged: Saying no when a bride is asking too much of you.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qe3f95fab73",
  "kind": "yes/no",
  "text": "Table caption: Characteristics of all ESS 11 cases in relation to gender.\n| Gender | Women ( n = 1087) | Men ( n = 783) | P |\n| Age - years |  |  |  |\n| Median (25 th ,75 th percentile) | 73 (56−84) | 71 (55−81) | 0.025 |\n| Priority at dispatch centre - n (%) a |  |  | 0.001 |\n| Prio 1 | 334 (30.8) | 302 (38.6) |  |\n| Prio 2 | 698 (64.3) | 448 (57.2) |  |\n| Prio 3 | 53 (4.9) | 33 (4.2) |  |\n| Triage colour RETTS - n (%) |  |  | 0.002 |\n| Red | 11 (1.0) | 13 (1.7) |  |\n| Orange | 224 (20.6) | 195 (24.9) |  |\n| Yellow | 587 (54.0) | 423 (54.0) |  |\n| Green | 265 (24.4) | 152 (19.4) |  |\n| Level of care - n (%) |  |  | 0.170 |\n| To hospital | 849 (78.1) | 632 (80.7) |  |\n| Stay at the scene | 238 (21.9) | 151 (19.3) |  |\n| Seek medical advice within 72 h. - n (%) b | 29 (12.2) | 15 (9.9) | 0.517 |\n| Mode of transport - n (%) c |  |  | 0.605 |\n| Ambulance | 764 (90.0) | 584 (92.4) |  |\n| PTS, immobile d | 33 (3.9) | 17 (2.7) |  |\n| PTS, seated | 32 (3.8) | 18 (2.8) |  |\n| Single-responder unit | 8 (0.9) | 9 (1.4) |  |\n| Transport by own means | 12 (1.4) | 4 (0.6) |  |\n| Type of condition - n (%) |  |  |  |\n| Non-time critical | 1040 (95.7) | 734 (93.7) | 0.062 |\n| Time critical | 47 (4.3) | 49 (6.3) |  |\n\nStatement: Transport by own means Men ( n = 783) is 4 (0.6).",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qdcacb8c3da",
  "kind": "yes/no",
  "text": "Statement 1: A steak will give a happy ending to this meal\nStatement 2: A dessert will give a happy ending to this meal",
  "question": "Of the statements shown: Statement 1, does it go against what common sense tells us?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qb2d22d36e2",
  "kind": "yes/no",
  "text": "Situation: I asked my girlfriend to marry me last night.\nAction being judged: Males proposing to the female they are dating when the relationship is serious.",
  "question": "Would it be correct to say that the action being judged is not wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q87a751e256",
  "kind": "yes/no",
  "text": "Customer: Sounds good. Could you book me a reservation for 8, Friday, at 16:15?\nAssistant: I'm sorry, I'm unable to book you a table at 16:15. Would you like to try another time?",
  "question": "Is there confirmation in the assistant's reply that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q300ea23378",
  "kind": "yes/no",
  "text": "Table caption: Results of linear models on the effects of a species’ relative frequency in the seed mixture (hypothesis 3) , fungicide application (hypothesis 4) , and insecticide application (hypothesis 4) as well as their interactions, and the effect of block on aboveground biomass two years after sowing for four exotic focal species. Note that two species ( O. viciifolia, B. orientalis ) had to be omitted because of the many zero values for biomass. See method section for further information on model structure. Abbreviations for factors are given in brackets. (* P < 0.05, *** P < 0.001).\n| Source |  | L. multiflorum | M . x varia | D. giganteus | P . peregrina |\n|  | d.f. | Ξ 2 values | Ξ 2 values | Ξ 2 values | Ξ 2 values |\n| Relative frequency [RF] | 1 | 17.32 *** | 1.99 | 34.56 *** | 31.26 *** |\n| Fungicide application [F] | 1 | 3.48 | 1.71 | 0.46 | 5.12 * |\n| Insecticide application [I] | 1 | 0.12 | 0.45 | 0.01 | 0.01 |\n| RF x F | 1 | 6.26 * | 0.11 | 0.00 | 6.55 * |\n| RF x I | 1 | 0.02 | 0.00 | 0.29 | 3.77 |\n| F x I | 1 | 0.82 | 0.28 | 0.47 | 0.00 |\n| RF x F x I | 1 | 0.30 | 0.08 | 0.00 | 6.40 * |\n| Block | 4 | 5.47 | 6.86 | 9.07 | 4.08 |\n\nStatement: RF x F x I has 9.40 * as P . peregrina value.",
  "question": "Is it right to say that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q2857121703",
  "kind": "yes/no",
  "text": "Assistant: Got it, I will put that down as well.\nCustomer: Thanks!\nAssistant: You are welcome! Sorry, the indoor is not available.",
  "question": "Using the assistant's final message, is \"indoor\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q377c54e8b4",
  "kind": "yes/no",
  "text": "Customer: What are the showtimes for Bad Boys for life at Cinemark?\nAgent: 11am, 12pm, 1pm, 2pm, 3pm, 5pm, 7pm, 9pm, and 11pm\nCustomer: What time is the IMAX showing?\nAgent: 7pm, 9pm, and 11pm\nCustomer: How many seats are available for the 7pm showing?\nAgent: There are only 6 seats left.\nCustomer: How many seats are available for the 11pm showing?\nAgent: The 11 p.m. is sold out.\nCustomer: What is the price of a regular ticket?\nAgent: 8 dollars\nCustomer: How many seats are available for the 11 am showing?\nAgent: There are 24 seats left.\nCustomer: How many seats are available for the 11pm showing tomorrow?\nAgent: The 11 p.m. is sold out.\nCustomer: What day are there seats available for the 11pm showing?\nAgent: Monday\nCustomer: How many seats are available?\nAgent: There are 10 seats left.\nCustomer: Great thanks.\nAgent: You're welcome.",
  "question": "By the end of this dialogue, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q4058f9b823",
  "kind": "yes/no",
  "text": "Situation: I'm a stereotypical nerd with WEAK thighs\nAction being judged: Making assumptions about an entire group of people.",
  "question": "Is it correct that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q22bdf2128b",
  "kind": "yes/no",
  "text": "Complaint narrative: I PULLED INTO A PARKING SPOT, PUT THE CAR INTO PARK, AND THEN THE CAR LURCHED FORWARD AT AN EXTREMELY POWERFUL SPEED. THE CAR STRUCK A CYPRESS TREE CAUSING $7,500 DAMAGE ON MY CAR.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "q2ffd756afd",
  "kind": "yes/no",
  "text": "Assistant: Okay. Placing the order now.\nCustomer: Ok.\nAssistant: 2% milk is no longer available. Would you like to change your order?",
  "question": "Does the assistant's final message confirm \"2% milk\" for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0f96cb453f",
  "kind": "yes/no",
  "text": "Statement 1: The mechanic fixed my car while it was in the shop.\nStatement 2: The mechanic sank my car while it was in the shop.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qa735af8a34",
  "kind": "yes/no",
  "text": "Whatever it does produce is constantly changing, moment-to-moment; no one can predict what it will produce at any future time. Winds performance history also shows that wind plants generally produce most at the times of least demandand least at the times of peak demand.",
  "question": "Is there an assertion in this paragraph of the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qdae55bf3ba",
  "kind": "yes/no",
  "text": "Occupation: Nuclear Power Reactor Operators\nDuties:\n- Distribute or process gas for utility companies or industrial plants, using panel boards, control boards, and semi-automatic equipment.\n- Adjust temperature, pressure, vacuum, level, flow rate, or transfer of gas to maintain processes at required levels or to correct problems.\n- Operate construction equipment to install and maintain gas distribution systems.",
  "question": "Are the duties given in the list part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q30b63a6f74",
  "kind": "yes/no",
  "text": "Table caption: Results of example 1.\n| Bayes factor | p ( H 0 ∣ θ ) | p ( H M ∣ θ ) | Rayleigh statistic | Rayleigh p -value |\n| 38.542 | 0.025 | 0.975 | 0.637 | 0.001 |\n\nStatement: 8.975 is the value for p ( H M .)",
  "question": "Does the table provide support for the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q7968f26e4c",
  "kind": "yes/no",
  "text": "Complaint narrative: DASH IS FALLING APART, FULL OF CRACKS; CHUNKS OF PLASTIC DASH HAVE BROKEN OFF. POTENTIAL SAFETY ISSUE IF INVOLVED IN AN ACCIDENT, ESPECIALLY IF DASH AIRBAG IS DEPLOYED. LARGE SHARP PIECES OF DASH WILL BREAK LOOSE AND BECOME PROJECTILES/ SHRAPNEL. I BELIEVE SUNLIGHT AND HIGH HEAT IN PARKED CAR HAS CAUSED THIS. NOT CAUSED BY AN ACCIDENT. DEFINITELY A DESIGN FLAW. SHOULD BE RECALLED.",
  "question": "So, does this vehicle safety complaint say at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qac0b5c32a8",
  "kind": "yes/no",
  "text": "Assistant: The cost of the repair will be $45.00\nCustomer: Okay that's not bad.\nAssistant: No, and they have you scheduled for 8:30 a.m.",
  "question": "Is it the case that, according to the assistant's last message, \"8:30 a.m\" is not confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order.\n- no: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction."
 },
 {
  "qid": "q03c8661550",
  "kind": "yes/no",
  "text": "Customer: yes, 7 people 4 nights starting Wednesday.\nAssistant: I'm sorry. There is no availability. Would you like to try different dates or another hotel?",
  "question": "Does the assistant's reply confirm that it was actually made, the booking the customer asked for?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q958005c640",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nObjective To investigate the efficacy and safety of recombinant human interferon alpha1b (rhIFN-α) nasal drops in healthy medical staff to prevent 2019 novel coronavirus disease (COVID-19). Conclusion In this investigator-initiated open-label study, we observed that rhIFN-α nasal drops can effectively prevent COVID-19 in treated medical personnel.\n\nClaim: In China, the early results of a study among medical workers were disappointing, concluding that interferon nasal drops “were ineffective at preventing Covid-19 in medical staff.”",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q9288564dc2",
  "kind": "yes/no",
  "text": "Assistant: there are multiple problems, sir\nCustomer: let's hear them\nAssistant: seven is not an available time, they only have space on the roof for nine at nine, and no children are allowed",
  "question": "Is it correct that, according to the assistant's last message, \"seven\" is not confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order.\n- no: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction."
 },
 {
  "qid": "qc9a1543ac6",
  "kind": "yes/no",
  "text": "Customer: I would like to try to find tickets for the movies tonight.\nAgent: Ok. What theater do you prefer?\nCustomer: Oxford theater.\nAgent: What movie do you want to see?\nCustomer: Twist.\nAgent: What time would you like to go?\nCustomer: Either before dinner around 5 or after dinner around 9:00.\nAgent: Please hold, I will check the times.\nCustomer: Thank you.\nAgent: Unfortunately, they only show with tickets left is at 7:00.\nCustomer: That won't work, our dinner reservation is at 7:00.\nAgent: Is there a different theater you can go to?\nCustomer: No, we really like Oxford.\nAgent: Are there any other movies you want to see?\nCustomer: I would like to see Flash.\nAgent: I will check the times.\nCustomer: Thank you.\nAgent: Flash is all sold out for tonight.\nCustomer: Ok, we will have to go to the movies another night.\nAgent: I'm sorry I could not be more helpful.",
  "question": "Has the customer, by the end of this conversation, actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q0f0b51263d",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nConclusions The population prevalence of SARS-CoV-2 antibodies in Santa Clara County implies that the infection is much more widespread than indicated by the number of confirmed cases.\n\nClaim: \"We found that there are many, many unidentified cases of people having Covid infection that were never identified with it with a virus test,\" said Dr. Jay Bhattacharya, a professor of medicine at Stanford University and one of the paper's authors.",
  "question": "As for the claim, does the evidence contradict it?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q3d94df5726",
  "kind": "yes/no",
  "text": "Statement 1: shops are closed every day\nStatement 2: shops are open every day",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q5af15756b9",
  "kind": "yes/no",
  "text": "Table caption: BET analysis for biochar samples.\n| Sample | BET surface area (m 2 /g) |\n| 300 °C char | 0.0218 |\n| 500 °C char | 0.0899 |\n| 700 °C char | 0.2720 |\n| 900 °C char | 0.2115 |\n\nStatement: BET surface area (m 2 /g) 0.2115 Sample is 900 C char.",
  "question": "Does the table provide support for the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q4f0a60bb7e",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2009, Taylor married writer Nick Flynn.\n- They have a daughter Maeve.\n\nSummary sentence:\nShe is married to playwright Nick Flynn, with whom she has a daughter.",
  "question": "Is every bit of info in the summary sentence backed up by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q64c0487cc8",
  "kind": "yes/no",
  "text": "Statement 1: jim cut his finger with the soap\nStatement 2: jim cut his finger with the knife",
  "question": "Would it be correct to say that, of these two statements, Statement 2 does not go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q81988bc9bf",
  "kind": "yes/no",
  "text": "Occupation: Health Education Specialists\nDuties:\n- Collaborate with health specialists and civic groups to determine community health needs and the availability of services and to develop goals for meeting needs.\n- Supervise professional and technical staff in implementing health programs, objectives, and goals.\n- Document activities and record information, such as the numbers of applications completed, presentations conducted, and persons assisted.",
  "question": "So, are the duties on the list part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q0cd8cb08ac",
  "kind": "yes/no",
  "text": "Customer: I'd like to go and see a movie tonight with my family.\nAgent: OK. Can you tell me the city and state where the theater is located?\nCustomer: We are in Santa Barbara, California.\nAgent: I see two theaters, AMC Mountain 16 and AMC Mercado 24. Are you interested in a particular movie?\nCustomer: Both of those theaters are really nice.\nAgent: OK. Is there a movie you have in mind?\nCustomer: I'm not sure what's out right now.\nAgent: Sure. Do you have a favorite genre?\nCustomer: What's a genre?\nAgent: Genre the movie category, like comedy, drama, action, etc.\nCustomer: Oh that's what that means. I like action movies a lot.\nAgent: Ok. Let’s see what action films are out.\nAgent: I found one action movie at AMC Mountain 16: No Time To Die.\nCustomer: What time is No Time To Die playing?\nAgent: One moment.\nCustomer: 9:10pm would be great.\nAgent: Got it. And how many tickets?\nCustomer: I need tickets for myself, my husband, and my son.\nAgent: All right. Let me confirm that you’d like three tickets for No Time To Die at AMC Mountain 16 tonight at 9:10pm. Is that all correct?\nCustomer: Yes, you got it.\nAgent: Is it OK to go ahead and purchase these tickets?\nCustomer: Absolutely!\nAgent: OK. Your tickets are purchased and details for how to proceed have been sent to your email address. Can I help with anything else?\nCustomer: Nope, that's all for now.\nAgent: OK. Enjoy your movie!",
  "question": "Has the customer actually bought movie tickets by the time this conversation finishes?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qca645e01a1",
  "kind": "yes/no",
  "text": "Customer: I'm looking for someplace to go in the west.\nAssistant: Might I recommend the Whale of a Time entertainment venue?",
  "question": "Did the assistant, in its reply, identify at least a single option that satisfies everything the customer requested?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qa38ffa75a5",
  "kind": "yes/no",
  "text": "Assistant: Sure, let me check.\nCustomer: Thank you.\nAssistant: Sorry, there is no more olives available at that time.",
  "question": "Is there confirmation of \"olives\" for the customer's pizza order in the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4701c21a89",
  "kind": "yes/no",
  "text": "Customer: I am also looking for a hotel in the same area with zero stars.\nAssistant: I'm sorry, there are no matches.",
  "question": "Did the assistant, in its reply, identify at least a single option that satisfies everything the customer requested?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q682303e2ee",
  "kind": "yes/no",
  "text": "Table caption: Exploratory factor analysis for the measures of response inhibition ( N = 179).\n| Measure | Factor loading | Uniqueness |\n| Antisaccade ERR | 0.15 | 0.98 |\n| Stroop ERR | 0.28 | 0.92 |\n| Stroop RT | 0.57 | 0.68 |\n| No-go ERR | 0.36 | 0.87 |\n| SSRT | – | 0.99 |\n\nStatement: There are 5 different types of measures in the given table.",
  "question": "Does the table support the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qcf876393fd",
  "kind": "yes/no",
  "text": "Assistant: $105-120. It will vary depending on some unique factors like traffic delays, tolls, and more. Also trips to and from AUS airport are subject to a $2.00 surcharge.\nCustomer: I understand. That's fine.\nAssistant: I just booked it. They will show up in 15 minutes precisely to the designated ride pickup location at the airport.",
  "question": "Is \"15 minutes\" for the customer's ride booking confirmed in the final message from the assistant?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q64ca6fd89e",
  "kind": "yes/no",
  "text": "Customer: I would like to reserve tickets for a movie.\nAgent: What movie would you like to see?\nCustomer: Well, we are debating a few choices and I wanted to see the showtimes.\nAgent: Ok. What's the first movie you want to see?\nCustomer: Little Women\nAgent: For tonight?\nCustomer: Yes.\nAgent: I see a 6:30 and an 8 pm showing of that at AMC Champaign.\nCustomer: Hm. What are the showtimes for 1917?\nAgent: 1917 is showing at 9 pm and 10:30 pm.\nCustomer: Well, 1917 is probably to late for us. I was hoping for something around 7\nAgent: So, Little Women?\nCustomer: Yes I think so.\nAgent: How many tickets?\nCustomer: Hold on a moment, I need to text my friends.\nAgent: Of course.\nCustomer: It seems that 2 of my friends are not able to attend this evening.\nAgent: Oh, too bad! How many tickets should I purchase, then?\nCustomer: I think that we are actually going to wait until another night, so don't buy anything yet.\nAgent: Ok.",
  "question": "By the conclusion of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q40bb42e917",
  "kind": "yes/no",
  "text": "Customer: Hey, isn't that world war 1 movie out now?\nAgent: Do you mean 1917?\nCustomer: Yes, that. Buy a ticket for that movie.\nAgent: Ok. When and where do you want to see it?\nCustomer: I want to go the theater downtown. let's say around 10-ish?\nAgent: Ok, let me check. There is showing of that movie downtown at 10.\nCustomer: Ok. When is it showing?\nAgent: Showtimes are 6, 9 and midnight for today.\nCustomer: Ok. Book me a ticket for the 6 pm showing.\nAgent: Ok. It appears the showing has been sold out.\nCustomer: Fine. Try the 9 pm showing then.\nAgent: 9 pm showing is also sold out.\nCustomer: Ok. Try midnight then.\nAgent: It appears the movie is very popular all tickets for tonight have been sold out.\nCustomer: How is that possible? try a different theater nearby.\nAgent: Downtown theater is the only one showing that particular movie.\nCustomer: Unbelievable.\nAgent: What would you like to do now?\nCustomer: Well, nevermind then. I guess I won't watch a movie tonight.\nAgent: Ok. Sorry about that.",
  "question": "By the end of this dialogue, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 }
]
