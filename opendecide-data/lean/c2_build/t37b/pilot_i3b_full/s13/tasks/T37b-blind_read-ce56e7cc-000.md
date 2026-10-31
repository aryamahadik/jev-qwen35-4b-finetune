# T37b blind solver T37b-blind_read-ce56e7cc-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_full/s13/answers/T37b-blind_read-ce56e7cc-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q597dd8f4f8",
  "kind": "yes/no",
  "text": "Statement 1: oil can be found in the sky\nStatement 2: oil can be found in the underground",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q9386f9e71e",
  "kind": "yes/no",
  "text": "Table caption: The number of views depending on the rating.\n| responses_rating_grade | views |\n| 1.0 | 1192.8 |\n| 2.0 | 1278.9 |\n| 3.0 | 1391.4 |\n| 4.0 | 1169.8 |\n| 5.0 | 990 |\n\nStatement: Rating grade 3.0 having more views.",
  "question": "Is the statement substantiated by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1f498940a2",
  "kind": "yes/no",
  "text": "Assistant: How many do you need at your table?\nCustomer: Just two it's a romantic date.\nAssistant: I have you set up for a table for two tonight at Malone's at 8 p.m.",
  "question": "Is \"Malone's\" for the customer's restaurant reservation confirmed in the final message from the assistant?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1dd7b315df",
  "kind": "yes/no",
  "text": "Complaint narrative: HAVE A SLIGHT MISFIRE AND CALLED ALL MY LOCAL SHOPS AND NO SHOP WILL CHANGE THE PLUGS ON A F-150 WITH A 5.4L TRITON MOTOR. THEY SAID IT'S WELL KNOWN THAT ALL THE SPARK PLUGS WILL SNAP OFF IN THE BLOCK. I CALLED THE DEALER AND THEY WANT $1000 TO CHANGE THEM. WHILE IN ALL OTHER CARS AND TRUCKS IT'S $50-$100 JOB. RESEARCHING THIS ONLINE IT SEEMS THIS HAPPENS TO EVERY FORD THAT HAD THE 5.4L TRITON ENGINE. WHY IS THERE NO RECALL? I CAN'T AFFORD $1000 TO CHANGE MY SPARK PLUGS. I'M A SMALL BUSINESS OWNER AND THIS IS BEYOND MY MEANS CURRENTLY. I EMAILED FORD AND THEY DIDN'T SEEM TO ACKNOWLEDGE IT BEING A KNOWN ISSUE. YET EVERY MECHANIC SHOP WILL AND THERE ARE THOUSANDS OF CASES OF THIS ISSUE ALL OVER THE INTERNET.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "qf10d855416",
  "kind": "yes/no",
  "text": "Statement 1: birds' milk is nutrient\nStatement 2: goats' milk is nutrient",
  "question": "Of these two statements, does Statement 2 make sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q01fb062488",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nHence, COVID-19 patients can develop psychotic symptoms as a consequence of multiple concurrent factors.\n\nClaim: There are no new-onset psychosis-related symptoms developed as a result of COVID-19.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q6a2c913cac",
  "kind": "yes/no",
  "text": "Earlier today, I was wondering if the motivation was to get more Hollywood glamour in their lives. The old world glamour of royalty, heavy crystal, and gowns must be getting old, but this is the political cynic in me speaking.",
  "question": "Made by this paragraph, is the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qc2d9e2d4b9",
  "kind": "yes/no",
  "text": "Customer: Hey assistant, when is 1917 playing at Cinemark in Strongsville?\nAgent: 1917 showtimes are 5:00pm, 6:00pm, and 7:15pm. Would you like me to check these times for ticket availability?\nCustomer: Yes, please check 6:00pm\nAgent: How many tickets do you need?\nCustomer: I need 2 tickets\nAgent: There are not enough seats available for this showtime. Would you like to select another?\nCustomer: No, I would like you to check another theater\nAgent: Which theater would you like me to check?\nCustomer: AMC in Ridge Park\nAgent: Are you still interested in seeing 1917?\nCustomer: Yes, what showtimes are available?\nAgent: There are shows at 5:15pm, 6:00pm, 7:15pm and 8:00 pm\nCustomer: Please check availability for 6:00pm\nAgent: Are you still interested in 2 tickets?\nCustomer: Yes\nAgent: Good news, there are 2 tickets available for this showtime. would you like to book this showtime?\nCustomer: Yes\nAgent: Ok, just to confirm, you would like to order 2 tickets to see 1917 at AMC in Ridge Park at 6:00pm\nCustomer: That is correct\nAgent: Great I have placed the order with your default credit card. You will receive a confirmation email shortly.",
  "question": "Has the customer actually bought movie tickets by the time this conversation finishes?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q96a129e80d",
  "kind": "yes/no",
  "text": "Situation: It took him an hour to eat all the chili in the bowl.\nAction being judged: Taking your time when eating lots of food.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qe2f828ed3b",
  "kind": "yes/no",
  "text": "Situation: I’ve stolen over $400 from my school.\nAction being judged: Making everyone's life poorer by taking what's not yours.",
  "question": "Is it true that the action being judged is not acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q7c04dc56df",
  "kind": "yes/no",
  "text": "Customer: I want to watch a movie tonight\nAgent: No problem. Do you have a movie in mind?\nCustomer: I am thinking of No Time To Die\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: is there no showing in Davis, California?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: too bad. what action films are playing in Davis, California?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: is that the original film from the 1970s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: great, I think I will buy the tickets tomorrow\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By this conversation's end, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q9dc2a73d89",
  "kind": "yes/no",
  "text": "Customer: I am also looking for a place to stay in the east in the expensive price range.\nAssistant: I have one listing for express by holiday inn cambridge, is that okay for you?",
  "question": "Did the assistant find at least a single option that meets everything the customer asked for in its reply?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q8b32510307",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Bachchan's first release of 2005 was the crime comedy \"Bunty Aur Babli\", which featured him and Rani Mukerji as the titular con artist duo who perform several successful heists and fall in love along the way.\n- His next two releases \"Dus\" (2005) and \"Bluffmaster!\"\n- (2005) were both moderately successful, but did not earn much critical appreciation.\n- Bachchan earned much critical acclaim for his performance in Mani Ratnam's \"Guru\" (2007), loosely based on the life of business magnate Dhirubhai Ambani.\"\n- His next release was the dance comedy \"Jhoom Barabar Jhoom\" (2007) alongside Preity Zinta, Bobby Deol, and Lara Dutta.\n- Bachchan's first release of 2008 was Ram Gopal Varma's \"Sarkar Raj\", which featured him and his father Amitabh Bachchan reprising their roles from \"Sarkar\" (2005) while his wife Aishwarya Rai Bachchan entered the cast as a new addition.\n- This film proved to be successful at the box office and earned him a nomination for the Filmfare Award for Best Supporting Actor.\n- Bachchan was next seen in \"Dostana\" (2008), a romantic comedy about two men (Bachchan and John Abraham) who pretend to be gay in order to be allowed to live with a girl (Priyanka Chopra), but then find that they have both fallen in love with her.\n- These films were the thriller \"Raavan\" (2010), the social drama \"Khelein Hum Jee Jaan Sey\" (2010), action thrillers \"Game\" (2011), \"Dum Maaro Dum\" (2011) & the heist thriller \"Players\" (2012).\n- Bachchan then played the lead role in Rohit Shetty's comedy \"Bol Bachchan\" (2012), which was a major blockbuster at the box office despite receiving mixed reviews from critics.\n- Bachchan was next seen in Farah Khan's dance comedy \"Happy New Year\", a musical heist film, playing the second lead to Shah Rukh Khan.\n- Bachchan's first release of 2016 was the comedy \"Housefull 3\", the third installment of the Housefull film series.\n\nSummary sentence:\nBachchan has also played leading and supporting roles in commercially successful comedies and dramas, including \"Bunty Aur Babli\" (2005), \"Dus\" (2005), \"Bluffmaster!\" (2005), \"Guru\" (2007), \"Jhoom Barabar Jhoom\" (2007), \"Sarkar Raj\" (2008), \"Dostana\" (2008), \"Dum Maaro Dum\" (2011), \"Bol Bachchan\" (2012), \"Happy New Year\" (2014) and \"Housefull 3\" (2016).",
  "question": "Is every piece of information in the sentence that gives the summary supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q712689388d",
  "kind": "yes/no",
  "text": "Customer: Hi, what's the best movie playing in Spring Hills Kansas right now?\nAgent: Well, that's a good question, regarding Rotten Tomatoes reviews, it would be Back country, playing at the Cinemark Downtown.\nCustomer: What score did they get exactly?\nAgent: 91%, would you like tickets?\nCustomer: Wait, what's it about?\nAgent: It's about Yosemite, it's rated G.\nCustomer: It sounds good but is that James Cameron movie out now?\nAgent: It is, it's playing at the Cinemark Downtown also.\nCustomer: What's the name of it?\nAgent: Beyond the storm.\nCustomer: I think I've heard of it.\nAgent: Would you like tickets?\nCustomer: Yes, I think that's the one.\nAgent: How many tickets would you like?\nCustomer: I need two. Get me the latest showing please.\nAgent: Ok, I have 2 for Beyond the Storm, Cinemark Downtown, tonight's showing, Spring Hills Kansas.\nCustomer: That's perfect yes.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.\nCustomer: Thanks I see them, good night.\nAgent: Enjoy your show.",
  "question": "Is it the case that, by the end of this conversation, the customer hasn't actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "qa150aaafe4",
  "kind": "yes/no",
  "text": "Assistant: Okay, what is the make, model and year of your car?\nCustomer: It is a Hyundai Elantra 2010.\nAssistant: Okay, I have booked you for 6 pm tonight for your Hyundai Elantra 2010..",
  "question": "Referring to the assistant's final message, is \"Hyundai Elantra\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbb254cec58",
  "kind": "yes/no",
  "text": "Complaint narrative: BOUGHT VEHICLE 2 YEARS AGO, HEADLIGHTS HAVE GOTTEN DIMMER TO THE POINT CAR IS UNSAFE TO DRIVE AT NIGHT. BROUGHT CAR INTO DEALERSHIP AND THEY ARE IN AGREEMENT THE HEADLIGHTS NEED TO BE REPLACED. SAFETY ISSUE. HIGH BEAMS ARE NECESSARY TO DRIVE AFTER DUSK.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q159f036e76",
  "kind": "yes/no",
  "text": "Complaint narrative: THIS WAS A LOW MILEAGE (9K) LESS THAN 1 YEAR OLD PRISTINE CONDITION AUDI S6. THE VEHICLE WAS DRIVEN APPROXIMATELY 10 MILES AND THEN PARKED IN A DRIVEWAY WHERE IT WAS TURNED OFF. THE DRIVER SAT IN THE VEHICLE FOR 5 MINUTES WITH THE ENGINE OFF PRIOR TO EXITING THE VEHICLE. BETWEEN 5 TO 10 MINUTES AFTER EXITING THE VEHICLE WE SMELLED SMOKE IN THE HOUSE. WE DISCOVERED THE VEHICLE HAD FLAME AND SMOKE EMANATING FROM UNDER ITS HOOD. THE FIRE DEPARTMENT HAD TO EXTINGUISH THE FLAMES AS WE WERE UNABLE TO DO SO WITH A GARDEN HOSE. THE ENTIRE FRONT OF THE VEHICLE BURNED. IT WAS CLASSIFIED AS TOTALED. THE VEHICLE WAS INSPECTED BY A FIRE CAUSE AND ORIGIN INSPECTOR AND AUDI. I HAVE BEEN TOLD VERBALLY THAT THE FIRE LIKELY BEGAN IN SOME ELECTRICAL COMPONENTS BEHIND THE DRIVER SIDE HEADLIGHT AREA. AUDI HAS CONFIRMED THAT THE FIRE WAS NOT CAUSED BY EXTERNAL FACTORS BUT I HAVE NOT BEEN PROVIDED ANY OTHER FEEDBACK FROM AUDI AS TO WHAT THE ACTUAL DEFECT. WAS. JUST TO RE-CAP: 1. THE IGNITION WAS OFF 2. THE CAR WAS NOT RUNNING 3. THE CAR SPONTANEOUSLY CAUGHT FIRE AND WAS DESTROYED. 4. IT WAS RAINING THAT DAY 5. THE CAR WAS IN LIKE-NEW CONDITION, WELL MAINTAINED AND WITH NO KNOWN DEFECTS. 6. WE WERE LUCKY THE CAR WAS NOT IN THE GARAGE AS THE HOUSE WOULD HAVE CAUGHT FIRE.",
  "question": "Does this safety complaint about the vehicle report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qdabb8a3381",
  "kind": "yes/no",
  "text": "Customer: Can you help me with booking movie tickets?\nAgent: Yes.\nCustomer: I'm looking for a theater in the Austin area.\nAgent: There is a Alamo and a AMC.\nCustomer: I would like to go to the Alamo Drafthouse.\nAgent: What movie are you going to see?\nCustomer: Bad Boys for Life.\nAgent: How many tickets do you need?\nCustomer: One.\nAgent: Would you like standard, IMAX, or 3d?\nCustomer: 3d.\nAgent: There is a 3d showing at 4:00pm.\nCustomer: That is fine.\nAgent: Where would you like to sit?\nCustomer: The front.\nAgent: Okay. Let me confirm, one ticket for Bad Boys at 4:30?\nCustomer: That's right.\nAgent: Okay. You're confirmation number is 8137768.\nCustomer: Thank you.\nAgent: You are welcome.",
  "question": "Is it correct that, by the end of this conversation, the customer hasn't actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "q9fa882242e",
  "kind": "yes/no",
  "text": "U.S. President Barack Obama and first lady Michelle Obama wave during the inaugural parade from the U.S. Capitol to the White House in Washington, January 21, 2013.",
  "question": "Does this paragraph come out with the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q38da79848f",
  "kind": "yes/no",
  "text": "Customer: Hello, I would like to tickets at the movie theaters at Davis, California\nAgent: No problem. Do you have a movie in mind?\nCustomer: Well, my first option is No Time To Die.\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: There is not any showtime for it at Davis, California?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: Oh! I really wanted to watch that movie!. Is there any action movie playing in Davis, California?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: I that the sequel for the original movie from the 1970s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: Well, I'm sorry for wasting your time, but I really wanted to watch No Time To Die and since there is not any showing at Davis, California. I'm going to pass. Thanks for your help.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qf9ce336dfc",
  "kind": "yes/no",
  "text": "Customer: I am looking for a cheap place to stay in the east part of town.\nAssistant: No problem. We have 3 guesthouses that match that. Do you have a further preference?",
  "question": "In its reply, did the assistant find at least a single option meeting everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q0cdf3ef751",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS: The incidence of VTE in patients with severe NCP is 25% (20/81), which may be related to poor prognosis.\n\nClaim: There are approximately 1 in 4 incidences of venous thromboembolism in patients with severe novel coronavirus pneumonia symptoms of SARS-CoV-2.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q43d621f39e",
  "kind": "yes/no",
  "text": "Statement 1: I put the car seat in the car.\nStatement 2: I put the oven in the car.",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q53afb44aa9",
  "kind": "yes/no",
  "text": "Complaint narrative: THE HEADLIGHTS ON MY 2018 HYUNDAI SONATA SHOW TWO BLACK NOTCHES AND A BLACK LINE ABOUT 30 FEET IN FRONT OF THE CAR IN LOW LIGHT CONDITIONS. IT IS VERY DISTRACTING AND DANGEROUS AS THESE SHADOWS DART ACROSS YOUR PATH AS YOU MAKE TURNS OR GO UP HILLS. HYUNDAI SERVICE COULD SEE THE NOTCHES, BUT SAID \"THE SYSTEM IS WORKING WITHIN SPECIFICATIONS AT THIS TIME\". SOMETHING NEEDS TO BE DONE BEFORE SOMEONE IS KILLED BECAUSE OF THESE UNSAFE LIGHTS.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "q36aec991e4",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThe odds that a primary case transmitted COVID-19 in a closed environment was 18.7 times greater compared to an open-air environment (95% confidence interval [CI]: 6.0, 57.9).\n\nClaim: The odds of catching the coronavirus are about 20 times higher indoors than outdoors.",
  "question": "According to the evidence, does it support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q63464590f9",
  "kind": "yes/no",
  "text": "And with a low-end temperature rise comes along low-end impacts. Seemingly good news for all!",
  "question": "Is it this paragraph that makes the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q61fcda5ee3",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNED A 2007 DODGE CHARGER. WHILE THE VEHICLE WAS PARKED, SMOKE EMITTED FROM THE FRONT PASSENGER SIDE WHEEL. THE VEHICLE LATER CAUGHT FIRE. A FIRE REPORT WAS FILED AND THE FIRE DEPARTMENT EXTINGUISHED THE FIRE. THE CONTACT DID NOT SUSTAIN ANY INJURIES. THE VEHICLE WAS DESTROYED. THE MANUFACTURER WAS NOT NOTIFIED OF THE FAILURE. THE FAILURE MILEAGE WAS 240,000. UPDATED 08/31/16*LJ",
  "question": "Does the vehicle safety complaint in question state that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qabf2dde96b",
  "kind": "yes/no",
  "text": "Situation: I barely taught my dog not to beg but my gf and I let her eat with us constantly.\nAction being judged: Dogs and humans not eating at the same table.",
  "question": "Is it accurate to say that the action being judged is not acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qf239e1d02f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Among other theatre schools and companies, the Dramatic Workshop played a vital role in paving the way for Off-Broadway theatre.\n\nSummary sentence:\nThe Dramatic Workshop considerably contributed to the resurgence of the Off-Broadway theatre.",
  "question": "In the summary sentence, is every piece of information supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q11b420078e",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nIn a closed, stagnant air environment, they disappear from the window of view with time constants in the range of 8 to 14 min, which corresponds to droplet nuclei of ca.\n\nClaim: Ordinary speech can emit small respiratory droplets that linger in the air for at least eight minutes and potentially much longer, according to a study published Wednesday.",
  "question": "Does that evidence support that claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qb0119e275e",
  "kind": "yes/no",
  "text": "Complaint narrative: THE RUST CORROSION IS SO BAD THAT THE SPARE TIRE FELL OFF HITTING THE LEAF SPRING SUPPORT BRACKET AND COMPLETELY CAUSED THE BUMPER TO FALL OFF THE TRUCK. THE SPARE TIRE ROLLED INTO ONCOMING TRAFFIC AND ALMOST CAUSED AN ACCIDENT. THE CORROSION IS EVIDENT ALL OVER THE CHASSIS AND OTHER PARTS. THIS HAPPENED WHILE I WAS DRIVING AND PULLING A LANDSCAPE TRAILER ON ROUTE 173 IN NEW JERSEY.",
  "question": "Is it true that this vehicle safety complaint doesn't report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "q24dbb44c74",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nOf these, 94 were working in an 11th-floor call center with 216 employees, translating to an attack rate of 43.5% (95% CI 36.9%–50.4%).\n\nClaim: Superspreading events can happen at call centers.",
  "question": "Is there a contradiction between the evidence and the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qa3be9aa79e",
  "kind": "yes/no",
  "text": "Table caption: Reasons teens were unwilling or uncertain about allowing researchers to contact their parents for consent purposes ( N = 166).\n| Theme | N (%) | Example responses |\n| Teen privacy | 55 (33) | ● “They don't know about my problem and I want to keep it that way.” ● “I'm not open about my issues with my parents” |\n| Parents lack an understanding of mental health or are unaware of the problem | 38 (23) | ● “I am not sure they would approve, seeing as they don't necessarily believe in mental health problems. Also, mental health is stigmatized in my family.” ● “They don't know about my eating disorder” |\n| Teen is concerned about parents' reaction/response | 34 (20) | ● “I don't want them to worry more about me” ● “They would be concerned/annoyed that I've never talked to them about this before” |\n| Teen autonomy | 26 (16) | ● “I do not like or trust my parents and I don't want them involved in this” ● “I feel old enough to make my own decisions about apps I'd like to try out” |\n| Poor parent-teen relationship | 17 (10) | ● “My family would never let me get help. A lot of parents don't care about whether their kid is hurting or not. This won't work if you make people tell their families. It just won't”. ● “My parents can be judgmental at some points so I don't want them to tell me something about wanting to try something new”. |\n| Parent would not want the teen to participate in research | 13 (8) | ● “They might think it's a scam and say no” ● “My parents might not be open to me participating in such a study or understanding of how I might benefit from such an app” |\n| Fears about online security/privacy | 3 (2) | ● “I am not sure that this survey is really trustworthy or that they would want me taking it” ● “I do not know what kind of information they will be collecting, so I am undecided” |\n\nStatement: Fears about online security/privacy has the least N (%) value of 3 (2).",
  "question": "Is it accurate to say that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q6892a0f782",
  "kind": "yes/no",
  "text": "Assistant: No other movie tickets ordered.\nCustomer: Thank you\nAssistant: You're welcome. Tickets for Aquaman 7:00pm showing at Lowes Boston Common are ordered. Cost is $17.99. Receipt is texted to you.",
  "question": "Does the assistant's final message say \"Lowes Boston Common\" is confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf117145343",
  "kind": "yes/no",
  "text": "Complaint narrative: TAKATA RECALL LETTER THAT WE RECEIVED FROM TOYOTA DIRECTED US TO STOP USING THE PASSENGER SEAT IN THE CAR DUE TO SAFETY CONCERNS, AND ADVISED THAT WE WOULD RECEIVE FURTHER INSTRUCTIONS IN APRIL. IT IS NOW MAY AND WE HAVE NOT HEARD FROM TOYOTA AND THE LOCAL DEALERSHIP ADVISES US THAT NO REMEDY IS AVAILABLE FOR US. WE ARE NOT ABLE TO SAFELY USE THE VEHICLE AS A FAMILY, AND WE HAVE NO IDEA WHEN OR IF WE WILL BE ABLE TO USE THE VEHICLE SAFELY AGAIN. THE VEHICLE IS CURRENTLY BEING USED DAILY BY DRIVER ONLY, AND IT IS UNCLEAR WHETHER THE VEHICLE POSES A THREAT TO DRIVER'S SAFETY.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q0984ff48dd",
  "kind": "yes/no",
  "text": "Customer: Hi,can u please help me to book movie tickets\nAgent: Ya of course,do u any location in your mind\nCustomer: Yes i am looking theater in Spring Hills Kansas\nAgent: Ok,currently there are two movies running in that area\nCustomer: Ok can u please tell me what are the movies and they details\nAgent: Not My Problem, Beyond The Storm this are the movies which are currently running\nCustomer: Can u explain the stories of both the movies\nAgent: Movie1: Not My Problem - Comedy - rated PG-13 - Rotten Tomatoes 72% - A troubled teen tries to convince his depressed elderly neighbor that things are not what they seem. - Stars Matt Damon and Noah Schnapp.\nCustomer: Ratings are good also i would prefer to watch comedy movie,can u tell about the second movie\nAgent: Movie2: Beyond The Storm - Action - rated PG-13 - Rotten Tomatoes 81% - Fishing the North Sea gets ugly as Captain John’s crew faces not only severe weather but a traitor on board - directed by James Cameron.\nCustomer: I love to watch action movies\nAgent: Which movie did u prefer?\nCustomer: I will go with the second movie Beyond The Storm\nAgent: Ok, how many tickets do u need\nCustomer: I need 3 tickets can u tell the timing for both the movies\nAgent: Not My Problem: AMC Holiday Theater - 1pm - 3:55pm - 7pm - 10:05pm Beyond the Storm: Cinemark Downtown - 1:30pm - 3:40 - 6:10pm - 8:30pm\nCustomer: I will go with the 6.10 pm show in cinemark downtown\nAgent: ok, its 3 tickets for BEYOND THE STROM for 6.10 pm show in cinemark downtown is it right can i book for u\nCustomer: Yes, you can boo\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "Is it correct that, by the end of this conversation, the customer has not actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "q0b5396e57a",
  "kind": "yes/no",
  "text": "Assistant: Ok. I need what is a best phone number?\nCustomer: They can reach me at 123-456-8989\nAssistant: TOday does not work. Would tomorrow morning at 8 a.m. be Ok?",
  "question": "Is the assistant's final message saying that \"TOday\" is confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf537ffaf50",
  "kind": "yes/no",
  "text": "Complaint narrative: I WAS PULLING OUT OF A PARKING SPACE WHERE MY FRONT WAS UP AGAINST A BUILDING WITH A CAR ON EITHER SIDE OF ME. I REVERSED FOR ABOUT 25' WHERE A TELEPHONE POLE MANDATED THAT I MAKE A K-TURN TO GET OUT. AS I SWITCHED FROM REVERSE TO FORWARD, I SAW A SPARK AS THE CAR JET-PROPELLED FORWARD. I TRIED TO BREAK MULTIPLE TIMES, BUT THE CAR ACCELERATED THE 25' INTO THE WALL. ALL AIRBAGS DEPLOYED, AND FLUID GUSHED OUT OF THE FRONT END. THE CAR WAS DECLARED A TOTAL LOSS. I WAS TOLD BY TOYOTA AND MY INSURANCE COMPANY THAT I MUST HAVE ACCIDENTALLY ACCELERATED INSTEAD OF REPEATEDLY BREAKING. I AM GRATEFUL THAT I HIT A WALL INSTEAD OF PEOPLE. SOMEONE COULD EASILY HAVE DIED HAD I HAD SWITCHED FROM REVERSE GEAR TO FORWARD IN LESS CONFINED LOCATION. THE ENTIRE ACCIDENT LASTED 2 SECONDS, WITH NO OPPORTUNITY TO PULL THE EMERGENCY BREAK OR GO INTO NEUTRAL. PS: I AM A HAPPILY MARRIED DOCTOR WITH BEAUTIFUL CHILDREN AND GRANDCHILDREN, AND NOT AT ALL SUICIDAL. THIS THREE MONTH OLD 2015 PRIUS 3 FAILED BEFORE THE FIRST OIL CHANGE. I AM NOT SATISFIED WITH THE RESULTS.",
  "question": "Was the vehicle actually involved in a crash, according to this vehicle safety complaint?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qb19e998b4d",
  "kind": "yes/no",
  "text": "When asked directly by ABC News in October if taxpayers should worry about the more than $500 million in federal funds on the line, Henrik Fisker was emphatic: \"No, I don't think they need to worry about it.\" When asked if Fisker might be the next Solyndra, he said, \"Absolutely not.\"",
  "question": "According to this paragraph, does it make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q858bacdfde",
  "kind": "yes/no",
  "text": "Table caption: List of Nature reserves in Kazakhstan.\n| Sr. # | Name | Location | Area of reserves | Year |\n| 1 | Aksu-Jabagly State Nature Reserve | Turkestan and Jambyl regions | 131,934 | 1926 |\n| 2 | Almaty State Nature Reserve | Almaty region | 71,700 | 1931 |\n| 3 | Naurzum State Nature Reserve | Kostanay region | 191,381 | 1931 |\n| 4 | Barsa-Kelme’s State Nature Reserve | Kyzyl Orda region | 160,826 | 1939 |\n| 5 | Korgalzhyn State Nature Reserve | Akmola and Karaganda regions | 543,171 | 1968 |\n| 6 | Markakol State Nature Reserve | East Kazakhstan region | 102,979 | 1976 |\n| 7 | Ustyurt State Nature Reserve | Mangystau region | 223,342 | 1984 |\n| 8 | West Altai State Nature Reserve | East Kazakhstan region | 86,122 | 1992 |\n| 9 | Alakol State Nature Reserve | Almaty and East Kazakhstan | 65,217,9 | 1998 |\n| 10 | Karatau State Nature Reserve | Turkestan region | 34,300 | 2004 |\n\nStatement: Year started from 1926 to 2004 .",
  "question": "Does the table support the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa39e0c5089",
  "kind": "yes/no",
  "text": "Customer: Thanks! Can you also see if there are any expensive, 4-star guesthouses in the north area of town?\nAssistant: What you are looking for can not be found. Is there any other area you would mind searching in?",
  "question": "Did the assistant, in its reply, find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qec443551e1",
  "kind": "yes/no",
  "text": "I frankly find it immensely sad that, not only real events, but also the work and knowledge of serious scientists, accumulated over many years, can apparently be swept aside at the whim of an algorithm. Computer models can have their value, but we surely need to keep an eye on whats happening in the real world.",
  "question": "Within this paragraph, does it make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q2ad5911138",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nVirus was widely distributed on floors, computer mice, trash cans, and sickbed handrails and was detected in air ≈4 m from patients.\n\nClaim: The coronavirus can be detected in the air up to 13 feet away from an infected patient.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q81296069dc",
  "kind": "yes/no",
  "text": "Statement 1: he often plays basketball with me, he hopes me to be \"Yao Ming\"\nStatement 2: he often plays guns with me, he hopes me to be \"Yao Ming\"",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q8b57c65761",
  "kind": "yes/no",
  "text": "Just the opposite is demanded in the dead of winter when there is no sun and when the wind dies down. During the week, energy demand soars and their is often not enough supply to meet the demand. And because many power companies are finding it unprofitable to run conventional systems part-time, many are simply mothballing such plants completely, thus making supply even rarer. As a result, the risk of blackouts is becoming a real increasing threat in Germany with each coming winter.",
  "question": "Is there confirmation that this paragraph makes the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q1758e654d2",
  "kind": "yes/no",
  "text": "Assistant: O.K. Now for the toppings.\nCustomer: Green olives and tomatoes on one.\nAssistant: Green olives not available.",
  "question": "Going by the assistant's latest message, is \"Green olives\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2247c0ebf3",
  "kind": "yes/no",
  "text": "Situation: I would, absolutely, sell my soul to a demon for the right price.\nAction being judged: Selling your soul for money.",
  "question": "Is it accurate to say that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qd4c165c201",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2006, the science journal \"Nature\" listed Pharyngula as the top-ranked blog written by a scientist.\n\nSummary sentence:\nIn 2006 the journal \"Nature\" listed Myers's \"Pharyngula\" as the top-ranked blog by a scientist based on popularity.",
  "question": "Is every bit of info in the summary sentence backed up by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q863a04b82c",
  "kind": "yes/no",
  "text": "Complaint narrative: DROVE TO WORK AT 6 AM WENT TO USE FOR LUNCH VEHICLE HAD NO POWER ASSISTED STEERING MORE LIKE MANUAL STEERING. MAKING VERY DIFFICULT IN PARKING , ON RAMPS TURNING AT INTERSECTIONS. MY MECHANIC TELLS ME STEERING COLUMN PART FAILURE THAT THEY HAVE REPLACED IN SEVERAL ESCAPES & MARINERS. MY BOSS WENT ON LINE AND FOUND INFO ON RECALL OF 915,216 FORD ESCAPES & MERCURY MARINERS. PROBLEM WAS WHEN BACKING OUT OF PARKING SPOT TYING TO TO TURN TO RIGHT WAS VERY DIFFICULT MORE LIKE MANUAL STEERING",
  "question": "Does this complaint on vehicle safety say the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qf0fda9a7fd",
  "kind": "yes/no",
  "text": "A British High Court judge ruled that \"An Inconvenient Truth\" promotes \"partisan political views,\" was riddled with errors and falsehoods, and could not be shown any more in schools, unless accompanied by a teacher's guide correcting information that Gore had misrepresented. Two of the most egregious distortions are especially likely to scare kids.",
  "question": "Made by this paragraph, is the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 }
]
