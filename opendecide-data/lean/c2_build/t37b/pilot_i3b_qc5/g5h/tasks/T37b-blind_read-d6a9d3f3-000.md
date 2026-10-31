# G5-H blind read T37b-blind_read-d6a9d3f3-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_qc5/g5h/answers/T37b-blind_read-d6a9d3f3-000.json

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
  "qid": "q674f6d91bd",
  "kind": "yes/no",
  "text": "Occupation: Molders, Shapers, and Casters, Except Metal and Plastic\nDuties:\n- Pour, pack, spread, or press plaster, concrete, or other materials into or around models or molds.\n- Construct or form molds for use in casting clay or plaster objects, using plaster, fiberglass, rubber, casting machines, patterns, or flasks.\n- Patch broken edges or fractures, using clay or plaster.",
  "question": "Is it accurate to say that the listed duties are not part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "q1945a23b4c",
  "kind": "yes/no",
  "text": "Complaint narrative: I WAS DRIVING AT THE HALLWAY AT 65 MPH AND THE POWER TO THE CAR SHUT OFF. I ALMOST CRASHED INTO OTHER CARS, WHEN THE ENGINE REDUCE POWER LIGHT CAME ON. I PULLED OVER AND WAITED 10 MINUTES TO START THE CAR. I WENT BACK HOME AND IT HAPPENED AGAIN ..... THE WENT TO THE SHOP FOUR TIMES, AND NO ONE WAS ABLE TO DIAGNOSE THE PROBLEM.",
  "question": "Is it correct that this vehicle safety complaint does not report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "q3bccdb8f8a",
  "kind": "yes/no",
  "text": "Customer: Will you tell me about a couple of good movies that are currently playing in Spring Hills Kansas?\nAgent: Sure. Do you have a genre in mind?\nCustomer: I am open to anything that's entertaining.\nAgent: Beyond the Storm and Backcountry both receive great reviews from critics.\nCustomer: What are their ratings?\nAgent: Rotten Tomatoes gave Beyond the Storm 81% and Backcountry 91%.\nCustomer: Sounds like the critics like them. What are their storylines?\nAgent: Beyond the Storm is an action film about fishing out at sea and Backcountry is a documentary about Yosemite National Park.\nCustomer: Who directed Beyond the Storm?\nAgent: James Cameron is the director.\nCustomer: What theater and showtimes for Beyond the Storm?\nAgent: Beyond the Storm is currently showing at Cinemark Downtown at 1:30pm, 3:40pm, 6:10pm and 8:30pm.\nCustomer: What theater is showing Backcountry?\nAgent: Backcountry is also showing at Cinemark Downtown.\nCustomer: What are the showtimes for Backcountry?\nAgent: Backcountry is playing at 4:10pm, 7:30pm and 10:15pm.\nCustomer: I like the late showtime. Let me buy three tickets for Backcountry at 10:15pm for tomorrow.\nAgent: Please confirm the purchase of three tickets for Backcountry at 10:15pm for tomorrow at Cinemark Downtown.\nCustomer: That's just perfect.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "Is it correct that, by the end of this conversation, the customer has not actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "qb25b016b91",
  "kind": "yes/no",
  "text": "Customer: Lets go to the movies.\nAgent: Ok, what theater?\nCustomer: Check AMC Studios 30.\nAgent: Ok, what movie for?\nCustomer: Do they have Street Dancer 3?\nAgent: Yes, they do.\nCustomer: Ok, what times do they have?\nAgent: 3:30 pm, 6:45 pm and 10:00 pm\nCustomer: Does 6:45 pm work?\nAgent: Yes that is perfect.\nCustomer: Ok sounds like a plan.\nAgent: Just to confirm you want two tickets for Street Dancer 3 at 6:45 pm at AMC Studios 30 theater.\nCustomer: No, three tickets, Bruce is coming also.\nAgent: Ok, so its three tickets for Street Dancer 3 at 6:45 pm at AMC Studios 30 theater.\nCustomer: Yes that is perfect.\nAgent: How will you be paying for these.\nCustomer: No need to buy them now, I will deal with that when I get to the theater tonight.\nAgent: Ok that is perfect. I won't book anything.\nCustomer: Thanks for looking this up.\nAgent: No problem, see you then.",
  "question": "By the end of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q665123f68f",
  "kind": "yes/no",
  "text": "Table caption: Summary of real-time LAMP results testing samples comprising Dracunculus -free copepods spiked with D. medinensis or D. insignis larvae. Nt = sample not tested, - = negative result. -ve sample is a no-template control, +ve controls are copepods mixed with Dracunculus DNA. Tp = time to positive, Ta = Annealing temperature.\n| Number spiked into sample | Number spiked into sample | Number spiked into sample | Samples tested with LAMP assays for | Samples tested with LAMP assays for | Samples tested with LAMP assays for | Samples tested with LAMP assays for | Samples tested with LAMP assays for | Samples tested with LAMP assays for |\n| Copepods | D. medinensis | D. insignis | D. medinensis | D. medinensis | D. insignis | D. insignis | Copepod | Copepod |\n| Copepods | D. medinensis | D. insignis | Tp (min:sec) | Ta (°C) | Tp (min:sec) | Ta (°C) | Tp (min:sec) | Ta (°C) |\n| 1 | 1 | 0 | 8:15 | 82.20 | nt | nt | 6:30 | 87.49 |\n| 10 | 1 | 0 | 7:45 | 82.07 | nt | nt | 6:15 | 87.65 |\n| 20 | 1 | 0 | 8:00 | 82.09 | nt | nt | 5:15 | 87.78 |\n| 30 | 1 | 0 | 8:15 | 82.04 | nt | nt | 5:30 | 87.79 |\n| 30 | 1 | 0 | 8:45 | 81.97 | nt | nt | 5:30 | 87.76 |\n| 10 | 0 | 0 | – | – | nt | nt | 6:30 | 87.21 |\n| 20 | 0 | 0 | – | – | nt | nt | 6:00 | 87.75 |\n| ≥50 | 0 | 0 | – | – | nt | nt | 6:15 | 87.16 |\n| ≥100 | 0 | 0 | – | – | nt | nt | 6:15 | 87.21 |\n| 1 | 0 | 1 | nt | nt | 10:15 | 82.50 | 9:00 | 88.26 |\n| 10 | 0 | 1 | nt | nt | 13:00 | 82.49 | 7:30 | 88.31 |\n| 10 | 0 | 0 | nt | nt | – | – | 7:00 | 88.26 |\n| -ve control |  |  | – | – | – | – | – | – |\n|  | +ve control |  | 7:30 | 81.83 | nt | nt | 6:00 | 87.67 |\n|  |  | +ve control | nt | nt | 11:30 | 82.42 | 8:00 | 88.41 |\n\nStatement: Samples tested with LAMP assays for D. medinensis Tp (min:sec) 8:45 Number spiked into sample Number spiked into sample D. medinensis is 1.",
  "question": "Is the statement backed up by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q458dc04050",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He finished the 2015–16 season leading the Lakers and all rookies in steals per game, and became the youngest player to hit 130 three-pointers in a season.\n- He subsequently earned NBA All-Rookie Second Team honors.\n\nSummary sentence:\nHe was named to the NBA All-Rookie Second Team with the Lakers in 2016.",
  "question": "Is every piece of info in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q0f640387f4",
  "kind": "yes/no",
  "text": "Assistant: Ok. What time would you like to see the movie?\nCustomer: Before 8, please.\nAssistant: Sorry, the 7:30 and 7:45 XD showings are currently sold out.",
  "question": "Is \"7:30\" confirmed for the customer's movie ticket order according to the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q915cfbacb1",
  "kind": "yes/no",
  "text": "Table caption: Methods used for the [ 11 C]CO 2 -reduction in published studies on 11 C‑carbonylations.\n| Reduction method | Research articles (total 119) |\n| Zn (400 °C) | 68 |\n| Mo (850 °C) | 38 |\n| Activated charcoal (800–900 °C) | 3 |\n| Organosilanes | 3 |\n| Zn + silica (485 °C) | 3 |\n\nStatement: Activated charcoal (800900 C) Research article is 3.",
  "question": "Would it be correct to say that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q187731bd73",
  "kind": "yes/no",
  "text": "Assistant: No, it doesn't look like they do for the oil change and tire pressure.\nCustomer: Ok, So what time should I be there again?\nAssistant: Your appointment is today, February, 28th at 2 pm.",
  "question": "Is it right to say that, according to the assistant's last message, \"2 pm\" isn't confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order.\n- no: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction."
 },
 {
  "qid": "q748b6284b2",
  "kind": "yes/no",
  "text": "Table caption: Min/max value and MAPE for air velocity of the drying air in the HPD TF1 during drying of separated digestate at different set values\n| v set m·s -1 | v meas minm·s -1 | v meas maxm·s -1 | MAPE (v)% |\n| 0.3 | 0.28 | 0.38 | 8.91 |\n| 0.5 | 0.48 | 0.51 | 0.63 |\n| 0.7 | 0.66 | 0.70 | 0.55 |\n\nStatement: The highest value of MAPE (v)% is 8.91",
  "question": "Is it right to say that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q77eac0802d",
  "kind": "yes/no",
  "text": "Occupation: Medical Equipment Repairers\nDuties:\n- Mix specified amounts of sand, clay, mortar powder, and water to form refractory clay or mortar, using shovels or mixing machines.\n- Climb scaffolding, carrying hoses, and spray surfaces of cupolas with refractory mixtures, using spray equipment.\n- Remove worn or damaged plastic block refractory linings of furnaces, using hand tools.",
  "question": "Is the inclusion of the listed duties in the job of the occupation named above true?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q39f3bd8dc4",
  "kind": "yes/no",
  "text": "Situation: Baby by a married man\nAction being judged: Cheating on your partner and having a baby with someone else.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q3adf761057",
  "kind": "yes/no",
  "text": "I went to this sickening concert with all gay artists 🏳️‍🌈🏳️‍🌈🏳️‍🌈",
  "question": "Would it be correct to say that this post is not hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "qe03aae612d",
  "kind": "yes/no",
  "text": "Table caption: Average values of trash and neps parameters in a dataset of 20 genetic materials, processed with five different ginning approaches.\n| Lint type | Neps per gram (count) | Visible Foreign Matter (%) | Trash per gram (count) | Dust per gram (count) |\n| Reference method | 353 | 3.11 | 156 | 427 |\n| Method I | 196 | 3.71 | 185 | 501 |\n| Method II | 256 , | 0.28 | 16 | 50 |\n| Method III | 257 , | 0.33 | 21 | 49 |\n| Method IV | 258 , | 0.78 | 43 | 128 |\n\nStatement: The lowest count for Trash per gram is 16.",
  "question": "Would it be correct to say that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q4976c0506c",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Bachchan better established himself in Hindi cinema playing a no-nonsense Mumbai police officer in the hit action thriller \"Dhoom\" (2004), which also starred John Abraham, Uday Chopra, Esha Deol, and Rimi Sen in pivotal roles.\n\nSummary sentence:\nHis first commercial successes came with the 2003 & 2004 action films \"Zameen\" and \"Dhoom\", which changed his career prospects.",
  "question": "Is every piece of the summary sentence's information supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q12c8b3425a",
  "kind": "yes/no",
  "text": "Occupation: Soil and Plant Scientists\nDuties:\n- Construct historical, scientific, and nature visitor-center displays.\n- Survey park to determine forest conditions and distribution and abundance of fauna and flora.\n- Conduct field trips to point out scientific, historic, and natural features of parks, forests, historic sites, or other attractions.",
  "question": "Is it right to say that the listed duties are not part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "q9c0574f797",
  "kind": "yes/no",
  "text": "Customer: Yes, are there any options for Italian food in the centre?\nAssistant: There are 9 Italian restaurants in the center. Do you have a preferred price range?",
  "question": "Is there confirmation, in its reply, that the assistant found at least a single option meeting everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q795d2d728a",
  "kind": "yes/no",
  "text": "Customer: Could you help me book a ticket for a movie?\nAgent: Sure thing! What movie?\nCustomer: 1917 please.\nAgent: Can I please know what theater you want to view it at?\nCustomer: AMC Naperville 16\nAgent: What time would you want to see it?\nCustomer: 10 PM\nAgent: They currently don't have that time.\nCustomer: Do you know if AMC South Barrington 24 has it at that time?\nAgent: Yes they do!\nCustomer: Can you book tickets for that theater then?\nAgent: Yes no problem. How many people?\nCustomer: 3 people are going to view it.\nAgent: Do you know if you want IMAX, 3D or standard?\nCustomer: Standard please.\nAgent: That sounds great. Is there any other tickets you need booked?\nCustomer: No that would be all.\nAgent: To confirm you want 3 tickets for 1917 at AMC South Barrington 24 for 10 PM\nCustomer: Yes that is perfect.\nAgent: Okay I have booked your tickets. Enjoy the show.\nCustomer: Thank you!",
  "question": "By the close of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q308ca7e2e7",
  "kind": "yes/no",
  "text": "Structural uncertainty is rarely quantified in context of subsequent model versions. Continual ad hoc adjustment of GCMs(calibration) provides a means for the model to avoid being falsified new model forms with increasing complexity aregenerally regarded better.",
  "question": "Is this paragraph making the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q9a1b315d1a",
  "kind": "yes/no",
  "text": "Customer: Yes, do any serve international food?\nAssistant: I have 2. The varsity restaurant and bloomsberry. Both serve international food and are in the moderate price range. Do you have a preference?",
  "question": "Was at least a single option that meets everything the customer asked for found by the assistant in its reply?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qa84a9c321c",
  "kind": "yes/no",
  "text": "Complaint narrative: THE PASSENGER SEAT WARNING LIGHT.AND SEAT SENSOR MALFUNCTIONED AND NOW THE PASSENGER SEAT BELT WILL NOT ENGAGE.I CANNOT HAVE A PASSENGER IN MY TRUCK BECAUSE OF THI PROBLEM.I DON'T UNDERSTAND HOW THI COULD BE SAFE AT ALL.THE MANUAL SAYS THAT WHEN THIS HAPPENS TO BRING IT IN TO THE DEALER BECAUSE THE SENSOR AND THE SEAT BELT LATCH MUST BE REPLACED. I'VE OWNED.MANY VEHICLES IN MY LIFE AND NEVER EVER HAD A SEAT BELT FAILURE LIKE THIS .THIS IS DANGEROUS WHAT IF THIS OCCURS WHEN I HAVE A PASSENGER IN THE VEHICLE AND THE SEAT BELT.UNMATCHED OR WON'T UNMATCHED. HOW CAN THIS BE SAFE. NO ONE GETS INTO MY VEHICLES WITHOUT PUTTING ON THE SEAT BELTS IN N.Y.IT IS A VIOLATION",
  "question": "Is there a report in this vehicle safety complaint of at least a single person being actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q5573b27d6a",
  "kind": "yes/no",
  "text": "Other fraud is evident through public exposure of e-mail files retrieved from the Climate Research Unit (CRU) at Britain's University of East Anglia. Scandalous exchanges among prominent researchers who have fomented global warming hysteria confirm long-standing and broadly suspected manipulations of climate data. The communications also reveal conspiracies to falsify and withhold information, to suppress contrary findings in scholarly publications, and to exaggerate the existence and threats of man-made global warming. Many of these individuals have had major influence over summary report findings issued by the IPCC. Still other evidence comes from mouths of government officials, international climate summit organizers and leading science spokespeople recorded in candid public admissions.",
  "question": "Does the paragraph here make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q81b6313756",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNED A 2006 TOYOTA SIENNA. WHILE MAKING A LEFT TURN AT APPROXIMATELY 5 MPH, ANOTHER VEHICLE CRASHED INTO THE PASSENGER SIDE OF THE VEHICLE. AS A RESULT, THE CONTACT CRASHED INTO A TRAFFIC SIGNAL POLE. IN ADDITION, THE CONTACT STATED THAT THE DRIVER SIDE SEAT BELT FAILED TO RETRACT PROPERLY AND CAUSED THE CONTACT TO BE THROWN TO THE FRONT PASSENGER SIDE OF THE VEHICLE. THE CONTACT SUSTAINED BACK AND NECK INJURIES THAT REQUIRED MEDICAL ATTENTION. A POLICE REPORT WAS FILED. THE VEHICLE WAS DESTROYED. THE MANUFACTURER WAS NOT NOTIFIED OF THE FAILURE. THE FAILURE MILEAGE WAS 183,000.",
  "question": "According to this vehicle safety complaint, was at least a single person actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q960633694f",
  "kind": "yes/no",
  "text": "Assistant: I will. I'm dialing now.\nCustomer: Have you contacted them yet?\nAssistant: Yes, they are on the way they should arrive within the next 5 min.",
  "question": "Going by the assistant's final message, is \"5 min\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd0f6f9da55",
  "kind": "yes/no",
  "text": "Customer: Is \"Sam's Delight\" playing in town tonight?\nAgent: Did you mean is the movie \"Sam's Delight\" playing tonight at the Legacy Monument Family 12 theater in Land's End?\nCustomer: Yeah.\nAgent: \"Sam's Delight\" is playing tonight at the Legacy Monument Family 12 at 4:00 PM, 6:10 PM, 8:30 PM, and 10:40 PM.\nCustomer: What else is playing?\nAgent: Tonight at the Legacy Monument Family 12 the movie \"Far From You\" is also playing.\nCustomer: What times?\nAgent: \"Far From You\" is playing tonight at the Legacy Monument Family 12 at 8:40 PM and 10:40 PM.\nCustomer: Are tickets available for the eight o'clock shows?\nAgent: Did you mean are there tickets available for the 8:30 PM showing of \"Sam's Delight\" and the 8:40 PM showing of \"Far From You\"?\nCustomer: Yes.\nAgent: How many tickets?\nCustomer: Two adults?\nAgent: Yes, there are tickets available for both shows.\nCustomer: What were the times, again?\nAgent: \"Sam's Delight\" is showing at 8:30 PM and \"Far From You\" is showing at 8:40 PM.\nCustomer: Let's do \"Sam's\".\nAgent: So you would like me to purchase two adult tickets to tonight's 8:30 PM showing of \"Sam's Delight\" at the Legacy Monument Family 12?\nCustomer: Correct.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "Has the customer actually bought movie tickets by the time this conversation finishes?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q26b79c68c4",
  "kind": "yes/no",
  "text": "Customer: Hello from Spring Hills, Kansas! We are looking to see a movie tonight. There are two of us. We need something later in the evening. What do you have available?\nAgent: I show the Cinemark Downtown and the AMC Holiday Theater in Spring Hills, which do you prefer?\nCustomer: Well, doesn't really matter. We can get to either. We are just trying to see what's out there. Maybe if you have something with a pretty high Rotten Tomatoes score.\nAgent: Sure, I'll check that for you.\nCustomer: Thank you.\nAgent: As far as Rotten Tomatoes score the highest ratings right now are for Backcountry at 91% and Beyond the Storm at 81%. They are both playing at the Cinemark Downtown.\nCustomer: Okay, give me some info on those, including times.\nAgent: Sure. Backcountry is a nature documentary about Yosemite National Park. It's a award winning film and it is rated G. Beyond the Storm is a film directed by James Cameron. The film tells the story or a North Sea fishing crew facing nature and the specter of a traitor on board. It's rated PG-13.\nCustomer: What do you have in the evening for Beyond the Storm? Later in the evening.\nAgent: The latest showing of Beyond the Storm is 8:30 pm.\nCustomer: Okay, that will be fine. We will take that for two people. How much will that cost?\nAgent: Total cost for two people for Beyond the Storm tonight is $16 dollars. Did you want to set that up right now?\nCustomer: Yeah, go ahead. So, that will be two people for $16 dollars for Beyond the Storm at the Cinemark tonight at 8:30 pm.\nAgent: That is correct. I can confirm that for you right now.\nCustomer: Yeah, go ahead.\nAgent: Sure, one moment please.\nCustomer: Thanks.\nAgent: Okay, so I will have for you two tickets for a total of $16 dollars for the 8:30 pm showing of Beyond the Storm tonight at the Cinemark Downtown. I will just confirm that right now. Just give me one moment and...your tickets are confirmed and have been sent out to your email address. Is there anything else I can help you with?\nCustomer: No, that will be it. Thank you very much.\nAgent: Thank you and please enjoy your evening.",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q257774b085",
  "kind": "yes/no",
  "text": "Occupation: Range Managers\nDuties:\n- Study rangeland management practices and research range problems to provide sustained production of forage, livestock, and wildlife.\n- Offer advice to rangeland users on water management, forage production methods, and control of brush.\n- Develop methods for protecting range from fire and rodent damage and for controlling poisonous plants.",
  "question": "For the occupation named above, are the listed duties part of its job?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qeef918296e",
  "kind": "yes/no",
  "text": "Table caption: Experimental results.\n| Sample ID | P eff [MPa] | v prop [mm/s] | K IIc [MPa*m 0.5 ] | k FOI [−] | e mech [mm] |\n| PGR6-RI-01-07 | 20 | 0.1 | 16.42 | ~520 | – |\n| PGR6-RI-01-08 | 20 | 0.3 | 15.71 | ~230 | 0.07 (0.09–0.1) |\n| PGR6-RI-01-09 | 20 | 0.3 | 15.34 | ~230 | 0.08 (0.07–0.1) |\n\nStatement: The highest standard deviation is 550.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qb1b76d0da5",
  "kind": "yes/no",
  "text": "Table caption: Path analysis.\n| Factors | Standard Coefficient | SE - value | t-value | 95% biased confidence interval | 95% biased confidence interval | Results |\n| Factors | Standard Coefficient | SE - value | t-value | LL | UL | Results |\n| NSR tourism infrastructure to QOL | 0.15∗∗ | 0.045 | 3.373 | 0.064 | 0.243 | Supported |\n| NSR tourism infrastructure to STD | 0.26∗∗∗ | 0.046 | 5.550 | 0.165 | 0.346 | Supported |\n| Sustainable tourism to QOL | 0.24∗∗∗ | 0.046 | 5.290 | 0.154 | 0.337 | Supported |\nTable notes: Note: ∗∗p<0.005, ∗∗∗p<0.001. NSR = New Silk Road, QOL = Quality of life, STD = Sustainable tourism development .\n\nStatement: NSR tourism infrastructure to STD has the lowest value for t-value of 7.456.",
  "question": "Is the statement backed up by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q168711049a",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2002 CHRYSLER PT CRUISER. WHILE DRIVING APPROXIMATELY 25 MPH, THE CONTACT'S VEHICLE CRASHED INTO THE REAR OF ANOTHER VEHICLE. THE AIR BAGS FAILED TO DEPLOY. THE CONTACT SUSTAINED CHEST INJURIES THAT REQUIRED MEDICAL ATTENTION. A POLICE REPORT WAS FILED. THE VEHICLE WAS TOWED TO AN INDEPENDENT MECHANIC. THE MANUFACTURER WAS MADE AWARE OF THE FAILURE. THE FAILURE MILEAGE WAS 64,000.",
  "question": "Does this vehicle safety grievance report that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q14d6a55581",
  "kind": "yes/no",
  "text": "Table caption: Peptide match of ARIP-B.\n| S. No | Plant description | Match Coverage (%) | Total Coverage (%) | RIP activity reported | RIP gene identified | Type of RIP | References |\n| 1 | Populus trichocarpa | 2 + 1 + 1 + 3 + 3 | 10 | Yes | Yes | Type 2 (B domain only) | Peumans and Vandamme (2010) |\n| 2 | Astragalus membranaceus | 10 | 10 | No | No | – | – |\n| 3 | Polygala tenuifolia | 1 | 1 | No | No | – | – |\n| 4 | Vitis vinifera | 0 + 2 | 2 | Yes | No | – | Peumans and Vandamme (2010) |\n| 5 | Triticum aestivum | 2 | 2 | Yes | Yes | Type 1 | Raj and Vennila (2013) |\n| 6 | Glycine max | 2 + 1 | 3 | Yes | No | – | Peumans and Vandamme (2010) |\n| 7 | Brachypodiumdistachyon | 1 | 1 | Yes | Yes | Type 3 | Peumans and Vandamme (2010) |\n| 8 | Hordeum vulgare | 3 | 3 | Yes | Yes | Type 1 | Raj and Vennila (2013) |\n| 9 | Ricinus communis | 2 | 2 | Yes | Yes | Type 2 | – |\n| 10 | Micromonaspusilla | 1 | 1 | Yes | No | – | Peumans and Vandamme (2010) |\n| 11 | Musa acuminata subsp. | 11 | 11 | No | No | – | – |\n| 12 | Arabidopsis lyrata subsp. | 3 | 3 | No | No | – | Peumans and Vandamme (2010) |\n\nStatement: There are four categories of Plant description.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q6688d5dfe9",
  "kind": "yes/no",
  "text": "Customer: I want a place to dine that is in the centre please.\nAssistant: There are 69 restaurants in the centre. Would you like to narrow it down by type of food or price?",
  "question": "Was at least a single option that meets everything the customer asked for found by the assistant in its reply?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q3f4b360428",
  "kind": "yes/no",
  "text": "Customer: What do you recommend?\nAssistant: Cambridge artworks is wonderful! They are located at 5 greens road cb13ef. There phone number is 01223902168.",
  "question": "In its reply did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qd0526b502e",
  "kind": "yes/no",
  "text": "Tissue and Lewis continue saying that \"glacial plants were severely carbon limited over a very long time period, until atmospheric CO2 began rising during the glacial-interglacial transition.\" In fact, they indicate that \"controlled environment studies with modern plants grown in glacial CO2\" have shown \"significant carbon limitations on plant physiology even when other resources were generally not limiting ,\" citing Dippery et al. (1995) and Tissue et al. (1995). So in spite of anything one could have done to enhance their productivity (other than supply them with more CO2), glacial-age plants simply could not produce the bounty that today's plants do. In fact, they were fortunate to merely survive.",
  "question": "Is it this paragraph that makes the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q60e31db37d",
  "kind": "yes/no",
  "text": "Table caption: Correlation between cerebral perfusion pressure and brain tissue oxygenation in 5 patients.\n| Patient No | Pearson coefficient (r) of correlation between CPP and PbtO 2 and probability (p) |\n| 1 | 0.79, p < 0.01 |\n| 2 | 0.38, p < 0.01 |\n| 3 | 0.35, p < 0.01 |\n| 4 | 0.77, p < 0.01 |\n| 5 | 0.7, p < 0.01 |\nTable notes: Abbreviations: r – Pearson's correlation coefficient; CPP – cerebral perfusion pressure; PbtO 2 – partial pressure of oxygen in brain tissue.\n\nStatement: Patient No 4 is having 0.77, p < 0.01 correlation between CPP and PbtO 2 and probability (p).",
  "question": "According to the table, is the statement supported?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8c7d79bfc2",
  "kind": "yes/no",
  "text": "Customer: Can you book it for me? Just for one person starting on Wednesday for 5 nights.\nAssistant: I'm sorry, none of the hotels in the centre are free on those dates.  Would you like to try a different number of days?",
  "question": "Does the assistant's reply confirm the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "qa2193cc121",
  "kind": "yes/no",
  "text": "Complaint narrative: JUST HAD A NEW FACTORY ENGINE PUT IN MY 2010 BMW 750LI UNDER A CLASS ACTION LAWSUIT, IN AUGUST 2019. DECEMBER 2019 WIFE WAS DRIVING CAR TO GROCERY STORE AND ENGINE SUDDENLY STARTED BUCKING AND SMELL OF GAS WAS OVERWHELMING. SHE WAS IN TRAFFIC AT THE TIME AND COULD NOT MAINTAIN PROPER SPEED ON THE 50MPH HIGHWAY AND LOST TOTAL POWER. SHE NURSED CAR INTO A NEARBY PARKING LOT. IT WAS SNOWING OUT AND HAD TO WAIT FOR A TOW TRUCK FOR AN HOUR IN FREEZING TEMPERATURES. ASIDE FROM THE OVERWHELMING FUEL SMELL, ALMOST CAUSED ACCIDENT BY NOT BEING ABLE TO MAINTAIN PROPER SPEED, SHE WAS WAITING IN FREEZING TEMPERATURES FOR TOW TRUCK. THIS, I FOUND OUT, IS A VERY BIG PROBLEM WITH THESE CARS. ITS WAS A FUEL INJECTOR THAT CAUSED THE ISSUE. THIS IS TRUELY A SAFETY HAZARD FOR THE PUBLIC. AND AN EXTREMELY EXPENSIVE FIX. BMW HAS MANY COMPLAINTS ABOUT THE FUEL INJECTORS, BUT SEEM TO IGNORE THE ISSUE AND PROFIT HEAVILY FROM THE CUSTOMERS LOSS. PLEASE DO SOMETHING ABOUT THIS ISSUE.",
  "question": "Does this complaint about vehicle safety report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qe526a6a0bf",
  "kind": "yes/no",
  "text": "Occupation: Poets, Lyricists and Creative Writers\nDuties:\n- Post and update content on the company's Web site and social media outlets.\n- Develop plans or materials to communicate organizational activities that are beneficial to the environment, public safety, or other important social issues.\n- Coach client representatives in effective communication with the public or with employees.",
  "question": "Are the listed duties part of the above-named occupation's job?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q31176d5130",
  "kind": "yes/no",
  "text": "Further, if India and China don't also sign up to cut their carbon emissions-and they did not embrace Kyoto-these proposed dramatic cuts in American carbon emissions alone would not solve the problems of climate change.",
  "question": "Does this block of text make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q5ea45394ab",
  "kind": "yes/no",
  "text": "Situation: Had a talk with my girlfriend and realized we both need a lot of thereby.\nAction being judged: Realizing when you and your partner need therapy.",
  "question": "Is it correct that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q6fd62816c1",
  "kind": "yes/no",
  "text": "As well as pumping much as 600 million tonnes more greenhouse gases into the atmosphere, the carbon credits scheme has been abused by countries like Russia and the Ukraine which have used them as a money making scam.",
  "question": "Made by this paragraph, is the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qbf7071ebf2",
  "kind": "yes/no",
  "text": "Customer: Yes I need it for 5 nights from Tuesday for 6 people.\nAssistant: I'm sorry but that booking did not go through. Shall I try another hotel for you?",
  "question": "Is there confirmation in the assistant's reply that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "qa777bdc088",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Dubin was described in \"New York Magazine\" in 1998 as one of the city's social leaders who were \"all born after the baby boom and free of its disdain for old conventions\", and was a member of the \"uptown A-listers\" including Prince Alexander von Fürstenberg, Pia Getty, The Crown Princess of Greece, and fashion designer Carolina Herrera Jr.\n\nSummary sentence:\nHe was described by \"New York Magazine\" as being a member of the \"uptown A-listers\".",
  "question": "Based on the text, is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q6afe43bf31",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNED A 2010 DODGE AVENGER. WHILE DRIVING 45 MPH, ANOTHER VEHICLE T- BONED THE CONTACT'S VEHICLE. THE FRONT AIR BAGS DEPLOYED, BUT THE SIDE CURTAIN AIR BAGS DID NOT. THE PASSENGER SUSTAINED A CONCUSSION, BROKEN NOSE, AND FRACTURED STERNUM. A POLICE REPORT WAS FILED. MEDICAL ATTENTION WAS RECEIVED. THE VEHICLE WAS DESTROYED AND TOWED. THE CONTACT RECEIVED NOTIFICATION OF NHTSA CAMPAIGN NUMBER: 16V668000 (AIR BAGS). THE MANUFACTURER WAS NOT NOTIFIED OF THE FAILURE. THE FAILURE MILEAGE WAS APPROXIMATELY 78,000.",
  "question": "According to this vehicle safety complaint, was at least a single person actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q77f27bf4a8",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nRates of ventilation in the HC, HC+AZ, and no HC groups were 13.3%, 6.9%, 14.1%, respectively. The risk of ventilation was similar in the HC group (adjusted hazard ratio, 1.43; 95% CI, 0.53 to 3.79; P=0.48) and in the HC+AZ group (adjusted hazard ratio, 0.43; 95% CI, 0.16 to 1.12; P=0.09), compared to the no HC group. CONCLUSIONS: In this study, we found no evidence that use of hydroxychloroquine, either with or without azithromycin, reduced the risk of mechanical ventilation in patients hospitalized with Covid-19.\n\nClaim: Hydroxychloroquine does not help patients avoid being placed on a ventilator.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q6253894ad9",
  "kind": "yes/no",
  "text": "Table caption: Literature overview of the status of mechanization.\n| Authors | Countries | Estimates on mechanization status | Data source and years |\n| Kirui (2019) | Burkina Faso, Cameroon, Egypt, Ethiopia, Ghana, Kenya, Niger, Senegal, South Africa, Zambia, Zimbabwe | On the average, 12% of the households have access to tractors: ranging from almost 0% in Senegal, Niger, and Cameroon to 12% in Kenya and Ghana and 57% in Egypt 7% own or hire threshers and 3% own or hire choppers, however, these numbers largely reflect the situation in Egypt and South Africa | World Bank/Global Environmental Facility Data (2004) |\n| Sheahan and Barrett (2017) | Ethiopia, Malawi, Niger, Nigeria, Tanzania, and Uganda | 1% of all households across the six countries own or hire tractors | Living Standards Measurement Study – Integrated Survey on Agriculture Data from World Bank (2010–2012) |\n| Mrema et al. (2018) | 26 African countries | Six countries have a tractor population below 1000; six countries of 1000–2000; ten countries of 2000–10,000; and 7 countries of more than 10,000 | FAO Data (1997–2008) |\n| Mrema et al. (2008) | Sub-Saharan Africa | 80% of land area is cultivated by hand, 15% with animals and 5% with tractors Decline in tractors owned from 2 tractors per 1000 ha of arable land in 1980 to 1.3 in 2003 | FAO (2013) |\n| Pingali (2007) | Sub-Saharan Africa | Less than 2 tractors per 1000 ha cropland (while this number has reached six tractors per 1000 ha in South Asia and ten in Latin America) | FAO Data (2002) |\n\nStatement: The Ethiopia, Malawi, Niger, Nigeria, Tanzania, and Uganda has a 1% of all households across the six countries own or hire tractors .",
  "question": "Is it true that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q1d852dcc92",
  "kind": "yes/no",
  "text": "From CEI: Director of Global Warming Policy Myron Ebell and President Fred L. Smith, Jr. sign on to an open letter to the Members of the Senate opposing the global warming amendments.",
  "question": "Is there an assertion in this paragraph of the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qffde82f0da",
  "kind": "yes/no",
  "text": "Situation: Unexpected Guest for Dinner Party Results in Empty Seats\nAction being judged: Making people leave their seats.",
  "question": "Is it true that the action being judged is not acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qe26158703c",
  "kind": "yes/no",
  "text": "Situation: He told his dad he didn't want to hunt quail.\nAction being judged: Saying no to doing something you aren't comfortable with.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 }
]
