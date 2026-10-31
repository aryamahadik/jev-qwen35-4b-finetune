# T37b blind solver T37b-blind_read-31bcf7e7-001 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_qc6/s13/answers/T37b-blind_read-31bcf7e7-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q9b630685cd",
  "kind": "yes/no",
  "text": "Complaint narrative: FRONT LEFT BRAKE LINE RUPTURED, RESULTING IN LOSS OF BRAKE FLUID, DEPRESSES BRAKE PEDAL GOES TO THE FLOORBOARD. NO STOPPING POWER. BACKING OUT OF DRIVEWAY ON THIS OCCASION. NO ACCIDENT. SAME LINE ON RIGHT FRONT RUPTURED LESS THAN A YEAR AGO, EXACT SAME RESULT. LUCKILY NO ACCIDENT BUT WAS AT A STOP LIGHT ON A MAJOR HIGHWAY WHEN PEDAL WHEN STRAIGHT TO FLOOR",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "qc8be1d8a5b",
  "kind": "yes/no",
  "text": "Assistant: Ok, I'll call you back.\nCustomer: Thanks\nAssistant: I confirmed that order of a large Bar-B-Que Pizza that will be ready for you to pickup in about 25 minutes.",
  "question": "Per the assistant's latest message, is \"Bar-B-Que Pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5151127b8d",
  "kind": "yes/no",
  "text": "Occupation: Bicycle Repairers\nDuties:\n- Install replacement glass in vehicles.\n- Replace or adjust motorized or manual window-raising mechanisms.\n- Remove all dirt, foreign matter, and loose glass from damaged areas, apply primer along windshield or window edges, and allow primer to dry.",
  "question": "Is it true that the listed duties are not part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "qff76943e97",
  "kind": "yes/no",
  "text": "BLT cocktail\nA BLT cocktail is a cocktail made out of the contents of a BLT sandwich, (bacon, lettuce and tomato), blended together with vodka. Variants on the drink include utilizing bacon vodka instead of traditional vodka, substituting liquor for lettuce, incorporating bacon salt, or including cucumber flavored vodka.\n\nTamango (Italian cocktail)\nThe Tamango is an Italian cocktail infused with roselle leaves and a variety of mysterious African roots and plants which purportedly give it a hallucinogenic effect; it is 85% alcohol and is the specialty of a pub close to the University of Turin. The name is taken from an 1829 short story (later made into a 1958 film) of a slave ship revolt by French author Prosper Mérimée.",
  "question": "Would it be correct to say that BLT cocktail and Tamango are not both alcoholic drinks?",
  "definitions": "- yes: The paragraphs do not bear out the positive statement (the question read without its 'not' or 'fail to'): at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer.\n- no: Read together, the paragraphs show that the positive statement (the question read without its 'not' or 'fail to') holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right)."
 },
 {
  "qid": "q98ce264956",
  "kind": "yes/no",
  "text": "The worlds climate scientists are almost all employed by western governments. They usually dont pay you to do climate research unless you say you believe manmade global warming is dangerous, and it has been that way for more than 20 years. The result is a near-unanimity that is unusual for a theory in such an immature science.",
  "question": "Based on the text, does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qf31c927f61",
  "kind": "yes/no",
  "text": "Statement 1: he thought it would rain soon so he carried sunglasses\nStatement 2: he thought it would rain soon so he carried an umbrella",
  "question": "Of these two statements, does Statement 2 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q3a29f4dc24",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nUsing global line-list data on COVID-19 cases reported until 29th February 2020 and global gridded temperature data, and after adjusting for surveillance capacity and time since first imported case, higher average temperature was strongly associated with lower COVID-19 incidence for temperatures of 1°C and higher.\n\nClaim: Multiple early studies provide evidence of less correlation between temperature and humidity ranges and the geographic regions where this virus has thrived.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qbd91d2e1b0",
  "kind": "yes/no",
  "text": "Complaint narrative: I KEEP HAVING A PROBLEM WITH THE STEERING COLUMN. I HAVE FIXED THIS SAME PROBLEM 3 DIFFERENT TIMES. THE LAST TIME I FIXED THE PART SEEMS TO HAVE CHANGED AND THE PART WAS HIGHER THE LAST TIME. THE PART CHANGED SUPPOSEDLY TO BE BETTER THAN THE PREVIOUS PART BUT IT SEEMS TO GO OUT EVERY YEAR.",
  "question": "According to this vehicle safety complaint, did the vehicle actually catch fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q3541235f89",
  "kind": "yes/no",
  "text": "Environment Magazine: \"Back When it Snowed': \"Losing Winter: As Climate Change Takes Hold, Our Coldest Season is the first Casualty'",
  "question": "Does this paragraph put forward the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q604020acc5",
  "kind": "yes/no",
  "text": "Situation: He hated muslims for what they did to his family.\nAction being judged: Being bigoted.",
  "question": "Going by common social norms, is the action being judged acceptable?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qf9c49c8002",
  "kind": "yes/no",
  "text": "Assistant: That shouldn’t be a problem their easy to work right there.\nCustomer: Thank you.\nAssistant: I’m so sorry they don’t have any pineapples right now.",
  "question": "Is \"pineapples\" confirmed for the customer's pizza order, according to the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q98993741cd",
  "kind": "yes/no",
  "text": "It is long overdue that the IPCC was called for what it is, an activist eco-political body driven not by the dangerous manmade warming evidence that it pretends exists, but by the beliefs and philosophies of its sponsor, the UNEP, and by key individuals at the time the IPCC was established.",
  "question": "Made by this paragraph, is the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qe5817bf11d",
  "kind": "yes/no",
  "text": "Situation: Trash Talking Creates a Stink After Warring Couple Reconciles\nAction being judged: Reigniting a conflict that just ended.",
  "question": "Is the action being judged permissible under common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qf97a699dc0",
  "kind": "yes/no",
  "text": "Customer: I need a place to stay in the East. I don't need to have access to the Internet.\nAssistant: I have 7 places available in the east.  What is your price range?",
  "question": "According to the assistant's reply, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q1aa4c54213",
  "kind": "yes/no",
  "text": "Assistant: the fare for Uber xl for this ride right now is $8, a bout $2 higher than the other one\nCustomer: that is just fine\nAssistant: the ride is booked and it should be there in 30 minutes as you requested, you can check the status on your phone",
  "question": "Is \"30 minutes\" for the customer's ride booking confirmed in the final message from the assistant?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q95be3b3a1f",
  "kind": "yes/no",
  "text": "Customer: Please list movies currently showing in San Diego California:\nAgent: The top movies in San Diego today are 'Bad Boys For Life', 'The Rise of Skywalker', '1917', and 'Jumanji, The Next Level' ...\nCustomer: What locations are showing '1917' in San Diego?\nAgent: The movie '1917' is playing at AMC Mission Valley, The Lot at Liberty Station, and UltraStar Cinemas Mission Valley.\nCustomer: Ok, what times does '1917' show at AMC Mission Valley?\nAgent: Standard showings of '1917' are playing at 7:30pm and 9:00pm.\nCustomer: Is '1917' playing on IMAX?\nAgent: 1917' is only playing on standard screens, there is no IMAX option available for this movie.\nCustomer: Ok, how much is the cost for two tickets to the 7:30pm showing of '1917' at AMC Mission Valley?\nAgent: Fandango lists adult tickets for the 7:30pm showing of '1917' at $17.00 each.\nCustomer: Ok, I would like to purchase two adult tickets to the 7:30pm showing of '1917' at AMC Mission Valley.\nAgent: Please confirm your selection of two tickets to the 7:30pm showing of '1917' at AMC Mission Valley 20 for January 20th, 2020. Your total will be $34.00. Say 'OK' to confirm.\nCustomer: Wait, I would like to change my selection... I would like to purchase two tickets to the 9:00pm showing of '1917' instead...\nAgent: No problem. Please confirm your selection of two tickets to the 9:00pm showing of '1917' at AMC Mission Valley 20 for for January 20th, 2020. Your total will be $34.00. Say 'OK' to confirm.\nCustomer: OK. Confirming selection.\nAgent: Please wait while your tickets are purchased...\nCustomer: OK. Thank you.\nAgent: You have purchased two tickets for '1917' at AMC Mission Valley for this evening, January 20th, 2020. Your total charge was $34.00. Your confirmation number is 125673.\nCustomer: Ok. Where will I pick up the tickets?\nAgent: Your tickets will be sent to your email inbox. The email on file for your account is ltestone@gmail.com. Is this correct?\nCustomer: Yes, that is correct.\nAgent: Please check your inbox for your tickets.\nCustomer: Thank you. That's all!\nAgent: Thank you for using virtual movie assistant. Enjoy your show.",
  "question": "Have movie tickets actually been bought by the customer by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qee7b06e806",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS AND RELEVANCE: In this survey of heath care workers in hospitals equipped with fever clinics or wards for patients with COVID-19 in Wuhan and other regions in China, participants reported experiencing psychological burden, especially nurses, women, those in Wuhan, and frontline health care workers directly engaged in the diagnosis, treatment, and care for patients with COVID-19.\n\nClaim: Female front-line workers treating patients with COVID-19 experienced higher rates or more severe symptoms of depression, anxiety, insomnia and distress than health-care workers overall.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qbbc2a9d5a6",
  "kind": "yes/no",
  "text": "Customer: I'm looking for attractions that are in the centre, could you help me find some?\nAssistant: There are 44 attractions located in the Centre area.  Are you interested in any particular type of attraction to narrow down your choices?",
  "question": "According to its reply, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q2f7a7341ca",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- The album debuted at No. 2 on the country albums charts, Its fourth and fifth singles \"Real Good Man\" and \"Watch the Wind Blow By\" both climbed to number one on the U.S. \"Billboard\" Hot Country Songs chart.\n- \"Shotgun Rider\" became the album's third single and a number 1 Country Airplay hit by the end of 2014.\n\nSummary sentence:\nIn total, McGraw's albums have produced 65 singles, 25 of which have reached number one on the Hot Country Songs or Country Airplay charts.",
  "question": "Is every piece of information in the summary sentence given support by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qff8c2b3f89",
  "kind": "yes/no",
  "text": "Customer: I would like eritrean, please.\nAssistant: I'm very sorry there are no restaurants that serve eritrean food in the centre area. Is there another type of cuisine we can look for?",
  "question": "Is there confirmation that, in its reply, the assistant found at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q5295e58280",
  "kind": "yes/no",
  "text": "Table caption: concentration of R and S amphetamine in seized tablets (mg/g).\n|  | Tablet weight (mg) | Concentration of R -amphetamine (mg/g) | RSD (%) | Concentration of S -amphetamine (mg/g) | RSD (%) | Total amphetamine (mg/g) | ee% |\n| 1 | 150.77 | 35.26 | 3.64 | 38.36 | 3.87 | 73.62 | 4.21 |\n| 2 | 168.67 | 47.82 | 3.81 | 48.40 | 2.48 | 96.22 | 0.60 |\n| 3 | 168.82 | 44.54 | 2.37 | 47.78 | 3.25 | 92.32 | 3.51 |\n| 4 | 165.55 | 30.82 | 3.43 | 31.62 | 1.75 | 62.44 | 1.28 |\n| 5 | 176.65 | 29.00 | 2.07 | 29.78 | 3.57 | 58.78 | 1.33 |\n| 6 | 169.18 | 17.94 | 3.69 | 18.5 | 3.20 | 36.44 | 1.54 |\n| 7 | 147.95 | 36.70 | 3.18 | 40.44 | 2.48 | 77.14 | 4.85 |\n| 8 | 168.70 | 19.02 | 2.63 | 19.86 | 2.44 | 38.88 | 2.16 |\n| 9 | 169.03 | 20.26 | 3.51 | 21.10 | 3.77 | 41.36 | 2.03 |\n| 10 | 166.75 | 37.16 | 2.96 | 45.16 | 2.11 | 82.32 | 9.72 |\n| 11 | 177.45 | 19.12 | 2.18 | 20.26 | 3.35 | 39.38 | 2.89 |\n| 12 | 166.06 | 44.68 | 1.6 | 49.66 | 3.39 | 94.34 | 5.28 |\n\nStatement: The Highest Concentration of R -amphetamine (mg/g) is 47.82.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q40ee775ec3",
  "kind": "yes/no",
  "text": "Occupation: Robotics Engineers\nDuties:\n- Build, configure, or test robots or robotic applications.\n- Conduct research on robotic technology to create new robotic systems or system capabilities.\n- Design software to control robotic systems for applications, such as military defense or manufacturing.",
  "question": "For the occupation named above, are the listed duties part of its job?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q0d99693c15",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nHowever, encephalopathy was independently associated with worse functional outcome (OR 0.22; 95% CI 0.11–0.42; P < 0.001) and higher mortality within 30 days of hospitalization (35 [21.7%] vs. 11 [3.2%] patients; P < 0.001). Encephalopathy was associated with increased morbidity and mortality, independent of respiratory disease severity.\n\nClaim: Confusion, delirium and other types of altered mental function, called encephalopathy, have occurred during hospitalization for Covid-19 respiratory problems, and a study found that such patients fared better right after hospitalization.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q6d86755010",
  "kind": "yes/no",
  "text": "Table caption: Description of Shear Reinforcements.\n| Specimen designation | No. of specimens | diameter, in(mm | Perimeter length, in(mm). | Perimeter length, in(mm). | Spacing in(mm). | No. of Stirrups |\n| Specimen designation | No. of specimens | diameter, in(mm | Ex. | Int. | Spacing in(mm). | No. of Stirrups |\n| Inverted-U PTB -A | 2 | 0.39(10) | 26.77(680) | 19.68(500) | 2.36(60) | 32 |\n| Closed Stirrups PTB -B | 2 | 0.39(10) | 37(940) | 22.83(580) | 2.36(60) | 32 |\n\nStatement: The No. of specimens are 2 each.",
  "question": "Is it true that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q991214fc0e",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Raj Ghatak\n- Ghatak has worked extensively on stage, and in many original ground-breaking productions.\n\nSummary sentence:\nRaj Ghatak is an actor.",
  "question": "Is every piece of information in the sentence that gives the summary supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qf5738b1935",
  "kind": "yes/no",
  "text": "Complaint narrative: I WAS DIVING DOWN GRATIOT STREET IN SAGINAW MICHIGAN, IT WAS RAINING HEAVILY AND MY WINDSHIELD WIPER DECIDED TO STOP WORKING COMPLETELY. I LOST ALL VISIBILITY AND HAD PULLED OVER IMMEDIATELY TO AVOID CAUSING AN ACCIDENT. WHILE SITTING IN MY CAR WAITING FOR THE RAIN TO STOP I REALIZE THAT MY WINDSHIELD WIPER MOTOR WAS STILL WORKING, BECAUSE I COULD HEAR IT MOVING BACK AND FORTH. BUT MY WIPERS WERE NOT. I HAVE READ THAT THERE IS A PROBLEM WITH SOME OF THE HARD WEAR AND A LOT OF PRIOR YEARS HAVE BEEN RECALLED. I'VE ALREADY HAD TO REPLACE THE ENGINE IN THIS CAR, NOW ONLY TO FIND OUT THAT THIS CAR WITH IT FAULTY EQUIPMENT CAN POTENTIALLY CAUSE ME MY LIFE... I WILL NOT RECOMMEND THIS VEHICLE TO ANYONE.",
  "question": "Is there a report in this vehicle safety complaint that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q92658b90dd",
  "kind": "yes/no",
  "text": "Karsk\nKarsk (also called Kask) is a Scandinavian cocktail containing coffee together with moonshine or vodka, and sometimes a spoon of sugar (enthusiasts often consider moonshine exclusively to be appropriate as an added component, as it has no inherent taste like other alcoholic beverages). Broader, it can also be found in other parts of Scandinavia.\n\nBLT cocktail\nA BLT cocktail is a cocktail made out of the contents of a BLT sandwich, (bacon, lettuce and tomato), blended together with vodka. Variants on the drink include utilizing bacon vodka instead of traditional vodka, substituting liquor for lettuce, incorporating bacon salt, or including cucumber flavored vodka.",
  "question": "Is it true that Karsk and BLT cocktail are not both drinks that contain moonshine?",
  "definitions": "- yes: The paragraphs do not bear out the positive statement (the question read without its 'not' or 'fail to'): at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer.\n- no: Read together, the paragraphs show that the positive statement (the question read without its 'not' or 'fail to') holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right)."
 },
 {
  "qid": "q61f807fe7e",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Manchester United's starting line-up included members of the \"Class of '92\": Neville was joined by his brother Phil, Beckham, Butt, Scholes and Giggs.\n- Neville was a talented cricketer as a schoolboy and played alongside future England captain Michael Vaughan at the Bunbury Cricket Festival and younger brother Phil for Lancashire's Under-14 team, and also for Greenmount Cricket Club in the Bolton Cricket League, for whom on Sunday 19 July 1992 he scored 110 not out in an unbroken partnership of 236 with Australian professional Matthew Hayden in a Hamer Cup tie against Astley Bridge.\n\nSummary sentence:\nNeville is the older brother of twin siblings: his brother, Phil Neville, is currently head coach of Inter Miami CF in MLS and is a former player for Manchester United and Everton, and his sister, Tracey Neville, is a retired netball international.",
  "question": "Do the evidence sentences support every piece of information in the summary sentence?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q03bf3de81d",
  "kind": "yes/no",
  "text": "Customer: Hello Siri!\nAgent: Hello. What can I do for you today?\nCustomer: I need to purchase some movie tickets for tomorrow night.\nAgent: Ok. What movie are you wanting to go see?\nCustomer: We want to see \"Uncut Gems\".\nAgent: Ok. What theater do you want to see the movie at?\nCustomer: We want to go to the AMC NorthPark 15 in Dallas, TX.\nAgent: OK. It looks like they have a showing at 12:05PM tomorrow. That is the only showing.\nCustomer: Ok. We will not be able to go that early. Can you see if the movie is showing tomorrow at the Alamo Drafthouse Cedar in Dallas, TX?\nAgent: Ok. It looks like they do have a 6:05PM showtime for \"Uncut Gems\" tomorrow night.\nCustomer: Ok great. Do they have Reclining seats in that theater?\nAgent: Yes, they do have reclining seats in that theater.\nCustomer: Great. Can you order these tickets for and charge them on my PayPal account?\nAgent: Sure. Just to confirm...you want 2 tickets to see \"Uncut Gems\" tomorrow night at the 6:05 showing at the Alamo Drafthouse Cedar in Dallas, TX?\nCustomer: Yes, that is correct.\nAgent: OK. I have these purchased for you. They will be waiting for you in will call.\nCustomer: Thank you Siri!\nAgent: No problem. Is there anything else I can do for you?\nCustomer: No that is all. Goodbye!\nAgent: Goodbye!",
  "question": "By the end of this conversation, is there actually a purchase of movie tickets by the customer?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qd2c286eb3e",
  "kind": "yes/no",
  "text": "Customer: Yes. Are any of those restaurants in the centre of town?\nAssistant: Yes, there are three restaurants serving Turkish food in the center of town.",
  "question": "In its reply, did the assistant find at least a single option meeting everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q88e4ad221e",
  "kind": "yes/no",
  "text": "women are 🐎",
  "question": "Is it the case that this post isn't hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "q8a15a892ae",
  "kind": "yes/no",
  "text": "Table caption: The categories inventoried as industrial process emissions.\n| Sub-sector | Sub-sub-sector ( a NFR code) |\n| Mineral products | Cement production (2.A.1) Lime production (2.A.2) Asphalt roofing (2.D.3.c) Asphalt road paving (2.D.3.b) |\n| Chemical industry | Ammonia (2.B.1) Nitric acid (2B.2) Adipic acid (2.B.3) Carbon black (2.B.10.a) Urea (2.B.10.a) Ammonium nitrate (2.B.10.a) Ammonium phosphate (2.B.10.a) Sulphuric acid (2.B.10.a) Titanium dioxide (2.B.6) |\n| Metal production | Pig iron production (1.A.2.a) Aluminium production (2.C.3) Copper smelting (primary and secondary) (2.C.7) Lead smelting (primary and secondary) (2.C.5) Zinc smelting (primary and secondary) (2.C.6) |\n| Pulp and Paper Industries | Kraft or Alkaline soda pulping (2.H.1) Acid sulphite pulping (2.H.1) Neutral sulphite semi-chemical (2.H.1) |\n| Food and Drink | Alcoholic Beverages (2.H.2) Food Production (2.H.2) |\n| Fugitive emissions of PM from major construction activities |  |\n\nStatement: They have six sub sector.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q10014c6ea5",
  "kind": "yes/no",
  "text": "Occupation: Fire-Prevention and Protection Engineers\nDuties:\n- Design or direct nuclear research projects to develop, test, modify, or discover new uses for theoretical models.\n- Direct environmental compliance activities associated with nuclear plant operations or maintenance.\n- Direct operating or maintenance activities of nuclear power plants to ensure efficiency and conformity to safety standards.",
  "question": "Does the job of the occupation named above include the listed duties?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q372a0d1f42",
  "kind": "yes/no",
  "text": "Table caption: Level 2 algorithm tests for ABSCO evaluation using OCO-2 soundings.\n| Label | Description |\n| A: B9 Baseline | B9 algorithm, using ABSCO v5.0 (includes EOFs) |\n| B: B9 No EOF | B9 algorithm, using ABSCO v5.0 (no EOFs included in fits to OCO-2 spectra) |\n| C: H 2 O continuum update | As above, with update to H 2 O continuum only |\n| D: O 2 and H 2 O updates | As above, with updates to both H 2 O continuum and O 2 spectroscopy (ABSCO v5.1) |\n| E: B9 with ABSCO v5.1 and EOFs | As above, after re-calculation of EOFs and including these EOFs in the fits to OCO-2 spectra |\n\nStatement: A: B9 Baseline and C: H 2 O Label are having same description B9 algorithm, using ABSCO v5.0 (includes EOFs).",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q3ed43f2072",
  "kind": "yes/no",
  "text": "Assistant: It is great. Let me get that order placed in for you.\nCustomer: Thanks so much.\nAssistant: I'm seeing they're actually out of coconut milk for now. But they are offering soy and almond milk if you were trying to avoid dairy.",
  "question": "According to the final message from the assistant, is \"coconut milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb80a8148f1",
  "kind": "yes/no",
  "text": "Situation: Baby by a married man\nAction being judged: Cheating on your partner and having a baby with someone else.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q86bad9842e",
  "kind": "yes/no",
  "text": "Table caption: Granulometric properties of the soils (mass %).\n| Clay | Silt | Sand | Gravel | Rubble | Name of mine |\n| 37.9 | 51.9 | 9.9 | 0.3 | – | S E |\n| 31.4 | 55.8 | 12.8 | – | – | S M |\n| 34.7 | 60.7 | 4.6 | – | – | S H |\n| 29 | 57.4 | 9.3 | 4.2 | – | S GH |\n| 10 | 79.7 | 10.1 | 0.1 | – | S A |\n| 35.6 | 52.5 | 11.8 | 0.1 | – | S Z |\n\nStatement: SA and SH has same gravel value.",
  "question": "Is the statement supported according to the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1332975219",
  "kind": "yes/no",
  "text": "Situation: Teen Should Go On Strike Until Brother Pays What He Owes\nAction being judged: Borrowing from a family member and not paying it back.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qca0a3778c4",
  "kind": "yes/no",
  "text": "Situation: When I am hungry, I eat.\nAction being judged: Eating when you are hungry.",
  "question": "Is the act being evaluated acceptable in accordance with common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q2d2ea2ff85",
  "kind": "yes/no",
  "text": "Customer: Yes, I was hoping for Austrian food.\nAssistant: There is not an expensive Austrian restaurant in the area. Is there another cuisine you'd like to try?",
  "question": "In its reply, did the assistant find at least a single option that fits everything the customer requested?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qe8b5248f62",
  "kind": "yes/no",
  "text": "Customer: Yes, please book starting Thursday for 4 people and for 4 nights.\nAssistant: I'm sorry, there were no rooms available. Would you like to find another hotel?",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "qba1aad342c",
  "kind": "yes/no",
  "text": "Customer: You're right. I forgot to select an architectural sight that I wanted to visit. Could you suggest one in the city centre.\nAssistant: Sure thing. I would suggest the old schools.",
  "question": "In its reply, did the assistant find at least a single option that fits everything the customer requested?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qc7bef956d0",
  "kind": "yes/no",
  "text": "Situation: I'm 30 years old &amp; I've never had a job or driven anywhere.\nAction being judged: Not being a responsible adult and grow up.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q0985b2b4ae",
  "kind": "yes/no",
  "text": "Statement 1: Plato is a man, and all philosophers are men, therefore Plato is a philosopher\nStatement 2: Plato is a philosopher, and all philosophers are men, therefore Plato is a man.",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q4b5e69c0fd",
  "kind": "yes/no",
  "text": "Occupation: Roof Bolters, Mining\nDuties:\n- Control conveyors that run the entire length of shuttle cars to distribute loads as loading progresses.\n- Monitor loading processes to ensure that materials are loaded according to specifications.\n- Replace hydraulic hoses, headlight bulbs, and gathering-arm teeth.",
  "question": "Do the listed duties form part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qd26fa13394",
  "kind": "yes/no",
  "text": "Statement 1: I CANNOT COUNT STARS.\nStatement 2: I CAN COUNT STARS.",
  "question": "Of these two statements, does Statement 2 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q11fbc87ae0",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nConclusions The population prevalence of SARS-CoV-2 antibodies in Santa Clara County implies that the infection is much more widespread than indicated by the number of confirmed cases.\n\nClaim: \"We found that there are many, many unidentified cases of people having Covid infection that were never identified with it with a virus test,\" said Dr. Jay Bhattacharya, a professor of medicine at Stanford University and one of the paper's authors.",
  "question": "Does the evidence stand at odds with the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qf8842d100a",
  "kind": "yes/no",
  "text": "Homeopathy is based on the principles of like-cures-like and ultra-dilutions. The first says substances that can cause symptoms can be used in diluted form to treat the same symptom in an illness, and the second says the more dilute a substance is, the more potent it is.",
  "question": "Does this paragraph set forth the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q14881b8f68",
  "kind": "yes/no",
  "text": "Assistant: Yes, I have made a note of it.\nCustomer: Thank you.\nAssistant: Your reservations have been confirmed for 7 pm on Sunday for a party of six.",
  "question": "Is \"six\" for the customer's restaurant reservation confirmed in the final message from the assistant?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9d150625d3",
  "kind": "yes/no",
  "text": "Table caption: Size Comparison of ZnO and TiO 2 nanoparticles synthesized using the plants.\n| Plant species | Plant part used | Synthesized NPs | Size (nm) | References |\n| Azadirachta indica, Emblica Officinalis | leaf | ZnO | 51, 16 |  |\n| Pyrus pyrifolia | leaf | ZnO | 45 |  |\n| Ixora coccinea | leaf | ZnO | 145.1 |  |\n| Passiflora caerulea | Leaf | ZnO | 200 |  |\n| Bauhinia tomentosa | Leaf | ZnO | 22–94 |  |\n| Pandanus odorifer | leaf | ZnO | 90 |  |\n| Allium sativum | Skin | ZnO | 7.77 |  |\n| Psidium guajava | Leaf | TiO 2 | 32.58 |  |\n| Cynodon dactylon | Leaf | TiO 2 | 13–34 |  |\n| Glycosmis cochinchinensis | Leaf | TiO 2 | 45 |  |\n| Cassia fistula | Leaf | TiO 2 | 200 |  |\n\nStatement: Plant part used are same for 10 Plant species that is leaf.",
  "question": "Is it true that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 }
]
