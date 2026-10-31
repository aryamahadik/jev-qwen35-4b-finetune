# T37b blind solver T37b-blind_read-133a522a-001 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_qc2/s13/answers/T37b-blind_read-133a522a-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qb23b906f27",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Dodon was appointed to the post of Associate Minister of Trade and Economics in May 2005, during the second Tarlev Cabinet.\n- He assumed the position of Minister of Trade and Economics in September 2006.\n- He held the position until September 2009, when the government of Zinaida Greceanîi ended.\n- In September 2009, after 8 years of governing, the Communist Party came into opposition.\n- He became an MP in the Parliament, which was reelected in November 2010.\n- After he was elected as the president of Moldova, due to specifics of Moldovan law, Dodon resigned as PSRM chairman and left the party, being replaced by Zinaida Greceanîi as interim leader.\n- Dodon was sworn in on 23 December 2016 in the Palace of the Republic.\n\nSummary sentence:\nHe served as minister of trade and economics in the governments of Vasile Tarlev and Zinaida Greceanîi from September 2006 to September 2009 and was a member of the Parliament of Moldova from 2009 to 2016.",
  "question": "Is every piece of the summary sentence's information supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q3b17fdf894",
  "kind": "yes/no",
  "text": "Brian Christley, a resident of Abergele, Wales, wrote to the Daily Telegraph : Over the weekend just gone, the coldest of the year so far, all 100-plus off-shore wind turbines along the North Wales coast were idling very slowly, all using grid power for de-icing and to power their hydraulic systems that keep the blades facing in the same direction.",
  "question": "Is this paragraph making the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qc229b58ac3",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThis cohort study examines the clinical characteristics of men with coronavirus disease 2019 whose semen tested positive for severe acute respiratory syndrome coronavirus 2.\n\nClaim: Scientists have found traces of the coronavirus in men's semen.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q74a8ecc18b",
  "kind": "yes/no",
  "text": "Customer: Hi, can you help me with booking movie tickets in Davis, California?\nAgent: No problem. Do you have a movie in mind?\nCustomer: I'm interested in \"No time to die\".\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: Oh, so noting in Davis then?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: That's too bad! Are there any action movies playing in Davis?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Is it the old one from like the 70's?\nAgent: The release date for this film is October 12, 1979.\nCustomer: Okay, thank you for your help, but I think I'll pass this time. Maybe they will have movies I like later.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By the end of this dialogue, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q09f2f3419c",
  "kind": "yes/no",
  "text": "Goa (India) : \"there is no ongoing sea level rise, sea level has been stable for the last 50 years or so, sea level fell some 20 cm at around 1960.\"",
  "question": "Does this passage advance the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q8b96e16278",
  "kind": "yes/no",
  "text": "Table caption: The number of views depending on the rating.\n| responses_rating_grade | views |\n| 1.0 | 1192.8 |\n| 2.0 | 1278.9 |\n| 3.0 | 1391.4 |\n| 4.0 | 1169.8 |\n| 5.0 | 990 |\n\nStatement: Rating grade 5.0 has less number of views.",
  "question": "Is it the case that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q789154b6cf",
  "kind": "yes/no",
  "text": "Statement 1: She worried about getting bored at the dark cabinet.\nStatement 2: She worried about getting bored at the dark cabin.",
  "question": "Of these two statements, does Statement 2 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q61a44f8c9a",
  "kind": "yes/no",
  "text": "CEI's FOIA request details how the UN informed participants that it was motivated by embarrassing releases of earlier discussions (\"ClimateGate\" key among them) and, to circumvent the problem that national government transparency laws posed, the group itself.",
  "question": "Is this paragraph making the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q86a8309848",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Salam was born in Rampur in 1970.\n- His father, Mufti Abdul Dayem Sahab, an Islamic scholar, had written several scholarly works on Islamic sciences in Urdu and Arabic and also worked as a hadith translator, while his mother is a housewife.\n\nSummary sentence:\nBorn in Rampur, his father was Islamic scholar Mufti Abdul Dayem Sahab while his mother is a housewife.",
  "question": "Is the summary sentence's information, every piece of it, supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qd4709bfdfe",
  "kind": "yes/no",
  "text": "Table caption: Peptide match of ARIP-B.\n| S. No | Plant description | Match Coverage (%) | Total Coverage (%) | RIP activity reported | RIP gene identified | Type of RIP | References |\n| 1 | Populus trichocarpa | 2 + 1 + 1 + 3 + 3 | 10 | Yes | Yes | Type 2 (B domain only) | Peumans and Vandamme (2010) |\n| 2 | Astragalus membranaceus | 10 | 10 | No | No | – | – |\n| 3 | Polygala tenuifolia | 1 | 1 | No | No | – | – |\n| 4 | Vitis vinifera | 0 + 2 | 2 | Yes | No | – | Peumans and Vandamme (2010) |\n| 5 | Triticum aestivum | 2 | 2 | Yes | Yes | Type 1 | Raj and Vennila (2013) |\n| 6 | Glycine max | 2 + 1 | 3 | Yes | No | – | Peumans and Vandamme (2010) |\n| 7 | Brachypodiumdistachyon | 1 | 1 | Yes | Yes | Type 3 | Peumans and Vandamme (2010) |\n| 8 | Hordeum vulgare | 3 | 3 | Yes | Yes | Type 1 | Raj and Vennila (2013) |\n| 9 | Ricinus communis | 2 | 2 | Yes | Yes | Type 2 | – |\n| 10 | Micromonaspusilla | 1 | 1 | Yes | No | – | Peumans and Vandamme (2010) |\n| 11 | Musa acuminata subsp. | 11 | 11 | No | No | – | – |\n| 12 | Arabidopsis lyrata subsp. | 3 | 3 | No | No | – | Peumans and Vandamme (2010) |\n\nStatement: There are four categories of Plant description.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q2fdcdda803",
  "kind": "yes/no",
  "text": "Situation: They saw someone was missing and later found him dead in the maze.\nAction being judged: Reporting a dead body if you stumble across one.",
  "question": "Is the action being judged permissible under common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q17fe1cc9a1",
  "kind": "yes/no",
  "text": "Statement 1: I put the vegetables in hot oil\nStatement 2: I put my hand in the hot oil",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qe2166f1c70",
  "kind": "yes/no",
  "text": "Ossie Davis\nOssie Davis (born Raiford Chatman Davis; December 18, 1917 – February 4, 2005) was an American film, television and Broadway actor, director, poet, playwright, author, and civil rights activist.\n\nAndrew Stevens\nAndrew Stevens (born June 10, 1955) is an American executive, film producer, director and actor.",
  "question": "Would it be correct to say that Andrew Stevens and Ossie Davis are not both Broadway actors?",
  "definitions": "- yes: The paragraphs do not bear out the positive statement (the question read without its 'not' or 'fail to'): at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer.\n- no: Read together, the paragraphs show that the positive statement (the question read without its 'not' or 'fail to') holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right)."
 },
 {
  "qid": "q603955c5b5",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2014 FORD C-MAX ENERGI. THE CONTACT STATED THAT THE VEHICLE WAS PLUGGED IN AND RECHARGING IN THE GARAGE. TWO HOURS LATER, AN EXTENSIVE FIRE ERUPTED FROM THE CHARGE CORD. THE FIRE DEPARTMENT WAS ABLE TO EXTINGUISH THE FLAMES. THE DEALER TESTED THE VEHICLE AND STATED THAT THE CHARGE CORD OVERHEATED. THE MANUFACTURER WAS NOTIFIED OF THE FAILURE AND SENT A TECHNICIAN, BUT WAS NOT ABLE TO DETERMINE THE SPECIFIC CAUSE OF THE FAILURE. THE VEHICLE WAS INSPECTED BY A DEALER AND THE INSURANCE ADJUSTER. THE COSMETIC DAMAGES WERE REPAIRED, BUT THE CONTACT WAS UNABLE TO DETERMINE IF THE FAILURE WOULD RECUR. THE VIN AND FAILURE MILEAGE WERE NOT AVAILABLE.",
  "question": "Does this vehicle safety complaint say the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q6a12937dc3",
  "kind": "yes/no",
  "text": "Hereward Corley pointed out that the reference to Shaviv (2008) should have been Shaviv (2005). Nir Shaviv another genius of a mathematician had originally sent me the paper saying it was from 2008, but the version he sent was an undated pre-publication copy. Mr. Corley also kindly supplied half a dozen further papers that determine climate sensitivity empirically. Most of the papers find it low, and all find it below the IPCCs estimates. The papers are Chylek & Lohman (2008); Douglass & Knox (2005); Gregory et al. (2002); Hoffert & Covey (1992); Idso (1998); and Loehle & Scafetta (2011).",
  "question": "Does the paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qcd35b5dea1",
  "kind": "yes/no",
  "text": "Complaint narrative: MY CAR SMELLS LIKE BURNT OIL AFTER DRIVING IT. I REPORTED IT TO MY DEALER A NUMBER OF TIMES TRYING TO GET AN APPOINTMENT AFTER I GOT MY RECALL BUT THEY STILL SAY THEY DON'T HAVE THE PARTS THIS IS A SERIOUS FIRE HAZARD PLEASE HELP.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q94a9499200",
  "kind": "yes/no",
  "text": "Customer: Hi, can you help me search for films in my area?\nAgent: Sure thing. Can I get your locations to start?\nCustomer: Yes, I am in Spring Hills Kansas.\nAgent: Okay, great. hat movies did you want me to search for you?\nCustomer: I have two films in mind. Once is called Shuttered and the other is called Beyond The Storm.\nAgent: Okay, let me check those titles for you, give me one second.\nCustomer: Sure.\nAgent: Okay, I do see both films playing in separate theaters near you.\nCustomer: Okay, great. I just need to know what the critic scores are for these two films.\nAgent: Sure. Shuttered has a critic score of 61%, and Beyond The Storm has a score of 81%\nCustomer: Great, I just want to confirm, these are both horror movies right?\nAgent: No. Shuttered is the only horror movie out of the two titles. Beyond The Storm is an action film.\nCustomer: Oh, I see. I think I'll go with the horror movies.\nAgent: Great choice. Do you need help getting tickets?\nCustomer: Yes, please.\nAgent: Okay, no problem. Shuttered is playing at the AMC Holiday Theater 3:00pm, 5:45 and 9:00pm. Which show time would you like to book for?\nCustomer: I'll book two tickets for the 9pm show.\nAgent: You have 2 tickets to see Shuttered at the AMC Holiday theater at 9pm tonight.\nCustomer: Yes, that's right.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qc7ecc8e3d4",
  "kind": "yes/no",
  "text": "Complaint narrative: THE RUNNING LIGHTS BURN OUT FREQUENTLY. NOT AT THE SAME TIME. EACH ONE WE'VE REPLACED AT LEAST 4 TIMES, WHICH IS WAY TOO MUCH. WE ARE USING GOOD QUALITY BULBS TOO. NOW THE INSIDE OF THE HEADLIGHT ASSEMBLY IS MELTED WHERE THE BULB SOCKET ITSELF SNAPS IN SO WE CAN'T KEEP THE SOCKET AND BULB IN ITS PLACE. THE REPLACEMENT HEADLIGHT ASSEMBLY IS NOT CHEAP FOR THIS VEHICLE",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q668d949f72",
  "kind": "yes/no",
  "text": "Occupation: Wind Energy Development Managers\nDuties:\n- Participate in special education-related activities, such as attending meetings and providing support to special educators throughout the district.\n- Establish, coordinate, and oversee particular programs across school districts, such as programs to evaluate student academic achievement.\n- Advocate for new schools to be built, or for existing facilities to be repaired or remodeled.",
  "question": "Are the duties given in the list part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q7af7d1333a",
  "kind": "yes/no",
  "text": "Situation: One day he instructed us to write something untrue.\nAction being judged: Improving your writing skills by trying something new.",
  "question": "Is it accurate to say that the action being judged is not acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q3ca4804f1a",
  "kind": "yes/no",
  "text": "Customer: Find me a restaurant that serves belgian food in the centre\nAssistant: I'm sorry, there aren't any.",
  "question": "According to its reply, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qf8b7c289d5",
  "kind": "yes/no",
  "text": "Assistant: It will be ready in 15 min.\nCustomer: Great.\nAssistant: I have you down for Tall Latte with a lemon bar.",
  "question": "Is \"Latte\" for the customer's coffee order confirmed in the final message from the assistant?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0a243ea5df",
  "kind": "yes/no",
  "text": "Customer: Yes, please book starting Thursday for 4 people and for 4 nights.\nAssistant: I'm sorry, there were no rooms available. Would you like to find another hotel?",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "q451d6fff9c",
  "kind": "yes/no",
  "text": "Statement 1: a dog is taken to a pool after getting sick\nStatement 2: a dog is taken to a veterinarian after getting sick",
  "question": "Of these two statements, does Statement 1 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q210070cd41",
  "kind": "yes/no",
  "text": "Customer: I'm looking for a restaurant that serves afghan food in the south\nAssistant: I have not found any, unfortunately. Would you like to try another area of town or cuisine?",
  "question": "In the response the assistant gave, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q91ca4433e4",
  "kind": "yes/no",
  "text": "Customer: I'm also looking for an attraction preferably on a boat in the west.\nAssistant: There are no boats in the west, can I try something else for you?",
  "question": "Did the assistant, in its reply, find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q368772665e",
  "kind": "yes/no",
  "text": "Table caption: Probabilities of detection for five A-Train and C-Train sun-synchronous orbiters at about 700 km altitude.\n| Satellite | Hard Body Radius | Threshold | Estimated Detection Rate P(Pc > T) | Data Span | Number of Reports | Number of Days |\n| CloudSat | 3.5 | 1.00E-04 | 75.2% | Apr 2015 - Sep 2019 | 2323 | 1632 |\n| CALIPSO | 14.8 | 1.00E-04 | 92.5% | Jan 2015 - Apr 2019 | 2261 | 1586 |\n| Aqua | 20 | 1.00E-04 | 96.3% | Jun 2016 - Apr 2019 | 1560 | 1047 |\n| Aura | 20 | 1.00E-04 | 96.6% | Jun 2016 - Apr 2019 | 1772 | 1045 |\n| OCO-2 | 6 | 1.00E-04 | 84.7% | Jan 2015 - Sep 2019 | 2402 | 1720 |\n\nStatement: Estimated Detection Rate P(Pc > T) 96.3% for Aqua Satellite.",
  "question": "Does the table back up the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa64c0fc862",
  "kind": "yes/no",
  "text": "Using data from the Intergovernmental Panel on Climate Change (IPCC), a Science and Public Policy Institute paper published last month found that if the United States eliminated all carbon dioxide emissions, the overall impact on global temperature rise would be only 0.08 degrees Celsius by 2050.",
  "question": "Does this paragraph put forward the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q70420e6b9c",
  "kind": "yes/no",
  "text": "Customer: I want to watch a movie\nAgent: Ok what movie?\nCustomer: I want to see Mulan\nAgent: Ok when and what time?\nCustomer: Tomorrow maybe round 8pm?\nAgent: Ok let me check\nCustomer: Ok\nAgent: We have two options available\nCustomer: Ok\nAgent: Ciemark 12 which is 30 miles away.\nCustomer: Is there not one closer?\nAgent: you have Mountain AMC 16 which is 22 miles away\nCustomer: I cannot go those are too far\nAgent: We apologize for any inconvenience\nCustomer: It's fine\nAgent: Ok please contact us if we can e of",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q5f56f6100b",
  "kind": "yes/no",
  "text": "Situation: I'm fantasizing about a coworker\nAction being judged: Doing things that could make a coworker uncomfortable.",
  "question": "Is the action being judged acceptable as per common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qfe7559d575",
  "kind": "yes/no",
  "text": "Occupation: Podiatrists\nDuties:\n- Teach or train medical staff regarding preventive medicine issues.\n- Direct or manage prevention programs in specialty areas such as aerospace, occupational, infectious disease, and environmental medicine.\n- Coordinate or integrate the resources of health care institutions, social service agencies, public safety workers, or other organizations to improve community health.",
  "question": "Are the enumerated duties included in the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qe7d14791b9",
  "kind": "yes/no",
  "text": "Assistant: So mushrooms and sausage?\nCustomer: Yes, thank you.\nAssistant: your pizza order of mushroom and sausage small personal pan pizza is complete and the pizzas will be ready for pickup in about 25 minutes. your receipt will be sent to your mobile device via text message.",
  "question": "Is \"personal pan pizza\" shown as confirmed for the customer's pizza order in the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb91acc8cf2",
  "kind": "yes/no",
  "text": "Table caption: Formation enthalpy Y (eV/atom), Composition ratio X, Symmetry S, Fitness F (eV/block), Volumes V(Å 3 /atom), Enthalpies E(eV/atom), and Compositions C for the first 10 structures include in the convex hull of the Nb-N system at 0 GPa.\n| ID | C | E | V | F | S | X | Y |\n| 71 | [ ] | −893.5888 | 14.4958 | 0.0000 | 1 | 0.533 | −0.9929 |\n| 75 | [0 14] | −270.1198 | 14.3751 | 0.0000 | 1 | 1.000 | 0.0000 |\n| 89 | [14 ] | −1369.2158 | 18.0875 | 0.0000 | 1 | 0.176 | −0.6086 |\n| 97 | [15 0] | −1603.9973 | 22.8193 | 0.0000 | 1 | 0.000 | 0.000 |\n| 113 | [13 ] | −1183.5582 | 16.1519 | 0.0000 | 1 | 0.316 | −0.7854 |\n| 121 | [ ] | −804.6286 | 14.1712 | 0.0000 | 1 | 0.600 | −0.9578 |\n| 123 | [ ] | −715.6656 | 13.0397 | 0.0000 | 1 | 0.667 | −0.9200 |\n| 125 | [ ] | −626.5662 | 18.2131 | 0.0000 | 1 | 0.733 | −0.7457 |\n| 132 | [ ] | −998.6407 | 14.8818 | 0.0000 | 1 | 0.455 | −0.9513 |\n| 66 | [ 13] | −692.2129 | 10.5534 | 0.0055 | 1 | 0.684 | −0.8686 |\n\nStatement: 0.000 is the value of 97 ID under Y.",
  "question": "Is it the case that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q3ba28f818f",
  "kind": "yes/no",
  "text": "Table caption: Physical properties of coarse aggregate.\n| Sl no. | Name of the test | Details of the relevant code | Test result |\n| 1 | Aggregate Crushing value | IS:2386(Part 4) 1963 (Reaffirmed 2002) | 17.48% |\n| 2 | Aggregate impact value | IS:2386(Part 4) 1963 (Reaffirmed 2002) | 24.12% |\n| 3 | Specific gravity | IS:2386(Part 3) 1963 | 2.47 |\n\nStatement: The test Aggregate Crushing value and Aggregate impact value has different Details of the relevant code of IS:2386(Part 3) 1963.",
  "question": "Is the statement substantiated by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa314a8b267",
  "kind": "yes/no",
  "text": "Situation: He pulled her aside after class and asked her.\nAction being judged: Waiting until after class to socialize.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qf72406a9ec",
  "kind": "yes/no",
  "text": "Customer: I am looking for a restaurant that serves Afghan food in the centre.\nAssistant: There are no Afghan restaurants in the centre of town.",
  "question": "According to its reply, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q0a523e93f2",
  "kind": "yes/no",
  "text": "Table caption: Properties of the source and target structures for the homogenous population case study.\n| Property | Unit | Source | Target |\n| Beam geometry, { l b , w b , t b } | mm | { 5000.0 , 350.0 , 350.0 } | { 4999.0 , 351.2 , 349.7 } |\n| Mass geometry, { l m , w m , t m } | mm | { 12000.0 , 12000.0 , 350.0 } | { 12001.0 , 11998.8 , 351.6 } |\n| Elastic modulus, E | GPa | N 210 . 00 , 1 × 10 - 9 | N 210 . 89 , 1 × 10 - 9 |\n| Density, ρ | kg / m 3 | N 8000 . 0 , 50 | N 8019 . 4 , 10 |\n| Damping coefficient, c | Ns / m | G 8.0000 , 0.8 | G 7.9981 , 0.8 |\n\nStatement: Density, Target is N 8019 . 4 , 10.",
  "question": "Is the statement supported according to the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q521d0bd5ea",
  "kind": "yes/no",
  "text": "Customer: Yes, please 5 people for 5 nights on Saturday.\nAssistant: Have you booked, 9L1SUXC3 is your confirmation. Anything else?",
  "question": "Does the assistant's reply confirm that the reservation the client requested was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q1a548ce139",
  "kind": "yes/no",
  "text": "Customer: I think it would be fun to go to see a movie tonight.\nAgent: Sure. What movie would you like to see?\nCustomer: What's playing at the Boulevard 14 Cinema in Petaluma, California since that would be the closest theater.\nAgent: OK. Boulevard 14 Cinema in Petaluma, California is showing three movies: No Time To Die, Mulan, and Emma.\nCustomer: Do you know anything about the movie?\nAgent: Sure. What specifically would you like to know?\nCustomer: What is the story about?\nAgent: OK. Here’s the synopsis of Mulan: Accompanied by her dragon, Mushu, Mulan uses her smarts to help ward off a Hun invasion, falling in love with a dashing captain along the way.\nCustomer: It sounds like it might be good. Did it get good reviews from both critics and the audiences?\nAgent: Mulan has an 87% Rotten Tomatoes score and a 92% audience rating.\nCustomer: Mulan sounds ok, but I think I'd rather see No Time to Die.\nAgent: OK. No Time To Die is playing 4:00pm, 7:30pm, and 10:55pm. Which time would you like?\nCustomer: We would like to go to the 10:55 pm show and it'll be just my friend and I.\nAgent: All right. Let me confirm that you’d like two tickets for No Time To Die at Boulevard 14 Cinema tonight at 10:55pm. Is that all correct?\nCustomer: Yes, that's correct.\nAgent: Is it OK to go ahead and purchase these tickets?\nCustomer: Yes.\nAgent: OK. Your tickets are purchased and details for how to proceed have been sent to your email address. Can I help with anything else?\nCustomer: I'm not familiar with your email confirmation. How does that work?\nAgent: The email will provide up to three options for your tickets: print at home, electronic tickets, or an option to pick them up at the theater.\nCustomer: Thank you for explaining that to me.\nAgent: OK. Enjoy your movie!",
  "question": "Is it true that, by the end of this conversation, the customer hasn't actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "q68f4e8158d",
  "kind": "yes/no",
  "text": "Complaint narrative: ISSUES JERKING AND HARD SHIFTING WHILE DRIVING. CAR LURCHES FORWARD AND MOVES IN JERKY MOVEMENTS. ALMOST CAUSED AN ACCIDENT BECAUSE VEHICLE STALLED THEN LURCHES FORWARD HARD.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "q618f56b2cb",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nHospitalizations were six times higher among patients with a reported underlying condition (45.4%) than those without reported underlying conditions (7.6%).\n\nClaim: Underlying conditions have no correlation with COVID-19 hospitalizations or deaths.",
  "question": "Is there support from the evidence for the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q4057eefccf",
  "kind": "yes/no",
  "text": "Complaint narrative: THE SENSOR THAT DETERMINES IF THE PASSENGER AIRBAG TURNS ON DOES NOT WORK PROPERLY. I WEIGH 100 POUNDS (WHICH IS ABOVE THE THRESHOLD FOR WHAT SHOULD TRIGGER THE AIRBAG TO BE ON) AND ABOUT HALF THE TIME THE AIRBAG IS DISABLED WHEN I AM SITTING IN THE SEAT PROPERLY WITH MY FEET ON THE GROUND AND THE CHAIR UPRIGHT. I CONTACTED CHEVROLET TO HAVE THEM REIMBURSE THE COST OF FIXING THIS ISSUE BECAUSE IT IS A SAFETY ISSUE AND HAS CAUSED RECALLS IN OTHER CHEVROLET CARS, BUT THEY HAVE REFUSED TO INVESTIGATE. THE SENSOR MALFUNCTION DOESN'T SEEM TO BE CORRELATED WITH WHETHER THE VEHICLE IS STATIONARY, IN MOTION, ON A STREET OR HIGHWAY, ETC. IT HAPPENS ABOUT HALF OF THE TIME AND CAN SOMETIMES GO ON AND OFF DURING THE SAME CAR TRIP EVEN IF I STAY IN THE SAME POSITION THE WHOLE TIME. THIS ISSUE HAS REPORTED FOR CHEVROLET MALIBUS ON SEVERAL ONLINE FORUMS SO I KNOW IT ISN'T AN ISOLATED ISSUE WITH MY CAR. WE ARE CONCERNED ABOUT WHAT COULD HAPPEN IF WE WERE IN A CRASH AND THE AIRBAG DIDN'T GO OFF OR WENT OFF LATE WHEN THE PASSENGER'S BODY WAS TOO CLOSE TO THE AIRBAG.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "qdecd68770b",
  "kind": "yes/no",
  "text": "Assistant: It's about thirty dollars for an entree each.\nCustomer: Hmm, not bad. I think my partner will be happy.\nAssistant: I'm sure they will be. Reservations for Pastabilities, tonight at 7 PM for two people in a private corner are confirmed!",
  "question": "Does the assistant's final message confirm \"private corner\" for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q22905b36ef",
  "kind": "yes/no",
  "text": "Occupation: Nannies\nDuties:\n- Observe participants and inform them of corrective measures necessary for skill improvement.\n- Instruct participants in maintaining exertion levels to maximize benefits from exercise routines.\n- Offer alternatives during classes to accommodate different levels of fitness.",
  "question": "Do the listed duties form part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q91c617fe89",
  "kind": "yes/no",
  "text": "Table caption: Description of columns in ASCII text table.\n| Column Name | Description |\n| System | Multibeam echosounder system |\n| Date | Date of survey, yyyymmdd. |\n| Time | Time of survey (UTC), hhmmss. |\n| Easting | Easting Cartesian coordinate, UTM Zone 27 N projection, WGS84. |\n| Northing | Northing Cartesian coordinate, UTM Zone 27 N projection, WGS84. |\n| Depth | Corrected and processed depth, m. |\n| Latitude | Geographical latitude, DD;MM.mm, WGS1984. |\n| Longitude | Geographical longitude, DD;MM.mm, WGS1984. |\n\nStatement: ASCII text table has two categories- Column Name and Description.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q170b42f557",
  "kind": "yes/no",
  "text": "Occupation: Bicycle Repairers\nDuties:\n- Install replacement glass in vehicles.\n- Replace or adjust motorized or manual window-raising mechanisms.\n- Remove all dirt, foreign matter, and loose glass from damaged areas, apply primer along windshield or window edges, and allow primer to dry.",
  "question": "Is it true that the listed duties are not part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "q7c677461a8",
  "kind": "yes/no",
  "text": "Customer: I am looking for a cheap place to stay in the east part of town.\nAssistant: No problem. We have 3 guesthouses that match that. Do you have a further preference?",
  "question": "Did the assistant find at least a single option in its reply that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q95c23eebeb",
  "kind": "yes/no",
  "text": "Customer: Yes, please try for 12:00\nAssistant: I'm sorry. I'm not sure what is going on. It will not let me book. Would you like to try a different restaurant?",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "qa13db56dcb",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nConclusion and Relevance: Among patients with severe or life-threatening COVID-19, convalescent plasma therapy added to standard treatment, compared with standard treatment alone, did not result in a statistically significant improvement in time to clinical improvement within 28 days.\n\nClaim: COVID-19 patients treated with convalescent plasma recover at faster rates than those without treatment.",
  "question": "Is the claim contradicted by the evidence?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q13d060be66",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- On feast days and at the graveside during burial of members of the community, the monastic community sings the hymn of the American-Cassinese Congregation known as the \"\"Ultima\"\".\n\nSummary sentence:\nThe abbey is a member of the American-Cassinese Congregation of the Benedictine Confederation.",
  "question": "Do the evidence sentences support every piece of information in the summary sentence?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 }
]
