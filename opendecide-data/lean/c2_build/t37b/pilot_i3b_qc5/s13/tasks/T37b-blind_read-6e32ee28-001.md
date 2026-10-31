# T37b blind solver T37b-blind_read-6e32ee28-001 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_qc5/s13/answers/T37b-blind_read-6e32ee28-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qd436cce4e8",
  "kind": "yes/no",
  "text": "Complaint narrative: VEHICLE HAS BEEN DRIVING PERFECTLY FINE AND OUT OF NO WHERE IT SHOWS 2 WARNINGS. ONE INDICTING TO SERVICE POWER STEERING, AND THE OTHER INDICTATING TO SERVICE ADVANCE TRAC SYSTEM. THE STEERING FLUID IS FULL AND THERE ARE NO DAMAGED TO THE HOSE OR POWER STEERING SYSTEM. THIS IS SHOWING THE SAME SIGNS OF THE RECALLED EXPLORERS YET THIS ONE HAS NOT BEEN RECALLED.",
  "question": "Does this complaint on vehicle safety say the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qc49bc2b730",
  "kind": "yes/no",
  "text": "But he, Osama, has also added some improvements. He claims to have found an Al Gore Rhythm to destroy the U.S. economy even more quickly than the conventional cap-and-trade bills were planning to do. A forced demise of the U.S. dollar is a part of his project to decarbonize the world's economy.",
  "question": "Does this paragraph come out with the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qcf75bcc01f",
  "kind": "yes/no",
  "text": "Table caption: Results of FT at 8 days.\n| Sample | [OH] mmol l −1 | [CaO] mmol l −1 | TMC [CaO] mmol l −1 | [CaO] reduction (%) |\n| Control | 56.83 | 8.25 | 8.37 | 0.70 |\n| CCA | 39.72 | 4.63 | 14.16 | 50.72 |\n\nStatement: 4.63 [CaO] mmol l 1 Sample is Control.",
  "question": "Supported by the table, is the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1a65c88e48",
  "kind": "yes/no",
  "text": "Customer: Hello from Spring Hills, Kansas! We are looking to see a movie tonight. There are two of us. We need something later in the evening. What do you have available?\nAgent: I show the Cinemark Downtown and the AMC Holiday Theater in Spring Hills, which do you prefer?\nCustomer: Well, doesn't really matter. We can get to either. We are just trying to see what's out there. Maybe if you have something with a pretty high Rotten Tomatoes score.\nAgent: Sure, I'll check that for you.\nCustomer: Thank you.\nAgent: As far as Rotten Tomatoes score the highest ratings right now are for Backcountry at 91% and Beyond the Storm at 81%. They are both playing at the Cinemark Downtown.\nCustomer: Okay, give me some info on those, including times.\nAgent: Sure. Backcountry is a nature documentary about Yosemite National Park. It's a award winning film and it is rated G. Beyond the Storm is a film directed by James Cameron. The film tells the story or a North Sea fishing crew facing nature and the specter of a traitor on board. It's rated PG-13.\nCustomer: What do you have in the evening for Beyond the Storm? Later in the evening.\nAgent: The latest showing of Beyond the Storm is 8:30 pm.\nCustomer: Okay, that will be fine. We will take that for two people. How much will that cost?\nAgent: Total cost for two people for Beyond the Storm tonight is $16 dollars. Did you want to set that up right now?\nCustomer: Yeah, go ahead. So, that will be two people for $16 dollars for Beyond the Storm at the Cinemark tonight at 8:30 pm.\nAgent: That is correct. I can confirm that for you right now.\nCustomer: Yeah, go ahead.\nAgent: Sure, one moment please.\nCustomer: Thanks.\nAgent: Okay, so I will have for you two tickets for a total of $16 dollars for the 8:30 pm showing of Beyond the Storm tonight at the Cinemark Downtown. I will just confirm that right now. Just give me one moment and...your tickets are confirmed and have been sent out to your email address. Is there anything else I can help you with?\nCustomer: No, that will be it. Thank you very much.\nAgent: Thank you and please enjoy your evening.",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q94adfda4c4",
  "kind": "yes/no",
  "text": "Table caption: Herfindahl–Hirschman Index (HHI) of agricultural output (by value).\n|  |  | 2002 | 2004 | 2006 | 2008 | 2010 | 2012 | 2014 | 2016 |\n| Total farms | Mean | 0.426 | 0.417 | 0.475 | 0.501 | 0.498 | 0.466 | 0.461 | 0.468 |\n|  | S.D | 0.262 | 0.254 | 0.275 | 0.292 | 0.307 | 0.324 | 0.322 | 0.322 |\n|  | Median | 0.389 | 0.382 | 0.455 | 0.472 | 0.476 | 0.435 | 0.439 | 0.448 |\n| Smallest 20% | Mean | 0.512 | 0.487 | 0.555 | 0.583 | 0.601 | 0.604 | 0.577 | 0.600 |\n|  | S.D | 0.256 | 0.261 | 0.274 | 0.281 | 0.294 | 0.318 | 0.319 | 0.309 |\n|  | Median | 0.479 | 0.452 | 0.516 | 0.541 | 0.577 | 0.582 | 0.558 | 0.569 |\n| Largest 20% | Mean | 0.391 | 0.382 | 0.391 | 0.405 | 0.386 | 0.333 | 0.363 | 0.336 |\n|  | S.D | 0.329 | 0.312 | 0.337 | 0.356 | 0.356 | 0.354 | 0.358 | 0.348 |\n|  | Median | 0.314 | 0.323 | 0.319 | 0.315 | 0.297 | 0.192 | 0.250 | 0.216 |\nTable notes: Notes: The sample includes households from VHLSS 2002–2016. Smallest (largest) 20% refers to farms with cultivated land (annual crop land, perennial crop land, and water surface) falls in the bottom (top) 20%.\n\nStatement: Mean 0.297 for the year 2010 is Largest 20%.",
  "question": "Would it be correct to say that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qc2b0507c0b",
  "kind": "yes/no",
  "text": "Occupation: Poets, Lyricists and Creative Writers\nDuties:\n- Post and update content on the company's Web site and social media outlets.\n- Develop plans or materials to communicate organizational activities that are beneficial to the environment, public safety, or other important social issues.\n- Coach client representatives in effective communication with the public or with employees.",
  "question": "Are the listed duties part of the above-named occupation's job?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qd46ba38e37",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nImportance: The pandemic of coronavirus disease 2019 (COVID-19) caused by the novel severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) presents an unprecedented challenge to identify effective drugs for prevention and treatment. No therapies have been shown effective to date.\n\nClaim: At the time of writing, there were several effective therapies in combatting COVID-19.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q943e3cc1e2",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Manchester United's starting line-up included members of the \"Class of '92\": Neville was joined by his brother Phil, Beckham, Butt, Scholes and Giggs.\n- Neville was a talented cricketer as a schoolboy and played alongside future England captain Michael Vaughan at the Bunbury Cricket Festival and younger brother Phil for Lancashire's Under-14 team, and also for Greenmount Cricket Club in the Bolton Cricket League, for whom on Sunday 19 July 1992 he scored 110 not out in an unbroken partnership of 236 with Australian professional Matthew Hayden in a Hamer Cup tie against Astley Bridge.\n\nSummary sentence:\nNeville is the older brother of twin siblings: his brother, Phil Neville, is currently head coach of Inter Miami CF in MLS and is a former player for Manchester United and Everton, and his sister, Tracey Neville, is a retired netball international.",
  "question": "Do the evidence sentences support every piece of information in the summary sentence?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q570da183e2",
  "kind": "yes/no",
  "text": "I went to this sickening concert with all gay artists 🏳️‍🌈🏳️‍🌈🏳️‍🌈",
  "question": "Would it be correct to say that this post is not hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "q2d2e7ccbc6",
  "kind": "yes/no",
  "text": "Complaint narrative: MY BRAKES GET HARD WHEN DRIVING IN SLOW TRAFFIC. AND STERRING WHEEL GETS STIFF WHEN PRESSED DURING TURNING CORNERS OR TURNS",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q0624635adf",
  "kind": "yes/no",
  "text": "Complaint narrative: A VERY LOAD BANGING SOUND IS COMING FROM MY RIGHT PASSENGER WHEEL WELL AREA. IT APPEARS THE SHOCK-ABSORBER MOUNTING LOCATION IS RUSTED AWAY AND BREAKING OFF. I CAN SEE INSIDE MY CAR THROUGH THE SPEAKER GRILL NOW. FIRST OCCURED WHEN THE CAR WAS IN MOTION AND DRIVING OVER A ROAD WITH SMALL POTHOLES. THE REST OF THE UNDERSIDE OF THE CAR SEEMS OK.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "q78121db7f3",
  "kind": "yes/no",
  "text": "Situation: Had a talk with my girlfriend and realized we both need a lot of thereby.\nAction being judged: Realizing when you and your partner need therapy.",
  "question": "Is it correct that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qbcc3d8b074",
  "kind": "yes/no",
  "text": "Complaint narrative: JUST HAD A NEW FACTORY ENGINE PUT IN MY 2010 BMW 750LI UNDER A CLASS ACTION LAWSUIT, IN AUGUST 2019. DECEMBER 2019 WIFE WAS DRIVING CAR TO GROCERY STORE AND ENGINE SUDDENLY STARTED BUCKING AND SMELL OF GAS WAS OVERWHELMING. SHE WAS IN TRAFFIC AT THE TIME AND COULD NOT MAINTAIN PROPER SPEED ON THE 50MPH HIGHWAY AND LOST TOTAL POWER. SHE NURSED CAR INTO A NEARBY PARKING LOT. IT WAS SNOWING OUT AND HAD TO WAIT FOR A TOW TRUCK FOR AN HOUR IN FREEZING TEMPERATURES. ASIDE FROM THE OVERWHELMING FUEL SMELL, ALMOST CAUSED ACCIDENT BY NOT BEING ABLE TO MAINTAIN PROPER SPEED, SHE WAS WAITING IN FREEZING TEMPERATURES FOR TOW TRUCK. THIS, I FOUND OUT, IS A VERY BIG PROBLEM WITH THESE CARS. ITS WAS A FUEL INJECTOR THAT CAUSED THE ISSUE. THIS IS TRUELY A SAFETY HAZARD FOR THE PUBLIC. AND AN EXTREMELY EXPENSIVE FIX. BMW HAS MANY COMPLAINTS ABOUT THE FUEL INJECTORS, BUT SEEM TO IGNORE THE ISSUE AND PROFIT HEAVILY FROM THE CUSTOMERS LOSS. PLEASE DO SOMETHING ABOUT THIS ISSUE.",
  "question": "Does this complaint about vehicle safety report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q60b6889bea",
  "kind": "yes/no",
  "text": "Occupation: Plasterers and Stucco Masons\nDuties:\n- Clean and prepare surfaces for applications of plaster, cement, stucco, or similar materials, such as by drywall taping.\n- Apply coats of plaster or stucco to walls, ceilings, or partitions of buildings, using trowels, brushes, or spray guns.\n- Mix mortar and plaster to desired consistency or direct workers who perform mixing.",
  "question": "Is it the case that the listed duties are not part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "q3c00d8d158",
  "kind": "yes/no",
  "text": "Assistant: Ok. What time would you like to see the movie?\nCustomer: Before 8, please.\nAssistant: Sorry, the 7:30 and 7:45 XD showings are currently sold out.",
  "question": "Is \"7:30\" confirmed for the customer's movie ticket order according to the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2a8e3a7f3a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Dubin was described in \"New York Magazine\" in 1998 as one of the city's social leaders who were \"all born after the baby boom and free of its disdain for old conventions\", and was a member of the \"uptown A-listers\" including Prince Alexander von Fürstenberg, Pia Getty, The Crown Princess of Greece, and fashion designer Carolina Herrera Jr.\n\nSummary sentence:\nHe was described by \"New York Magazine\" as being a member of the \"uptown A-listers\".",
  "question": "Based on the text, is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q0f64fcf94c",
  "kind": "yes/no",
  "text": "Table caption: Summary of real-time LAMP results testing samples comprising Dracunculus -free copepods spiked with D. medinensis or D. insignis larvae. Nt = sample not tested, - = negative result. -ve sample is a no-template control, +ve controls are copepods mixed with Dracunculus DNA. Tp = time to positive, Ta = Annealing temperature.\n| Number spiked into sample | Number spiked into sample | Number spiked into sample | Samples tested with LAMP assays for | Samples tested with LAMP assays for | Samples tested with LAMP assays for | Samples tested with LAMP assays for | Samples tested with LAMP assays for | Samples tested with LAMP assays for |\n| Copepods | D. medinensis | D. insignis | D. medinensis | D. medinensis | D. insignis | D. insignis | Copepod | Copepod |\n| Copepods | D. medinensis | D. insignis | Tp (min:sec) | Ta (°C) | Tp (min:sec) | Ta (°C) | Tp (min:sec) | Ta (°C) |\n| 1 | 1 | 0 | 8:15 | 82.20 | nt | nt | 6:30 | 87.49 |\n| 10 | 1 | 0 | 7:45 | 82.07 | nt | nt | 6:15 | 87.65 |\n| 20 | 1 | 0 | 8:00 | 82.09 | nt | nt | 5:15 | 87.78 |\n| 30 | 1 | 0 | 8:15 | 82.04 | nt | nt | 5:30 | 87.79 |\n| 30 | 1 | 0 | 8:45 | 81.97 | nt | nt | 5:30 | 87.76 |\n| 10 | 0 | 0 | – | – | nt | nt | 6:30 | 87.21 |\n| 20 | 0 | 0 | – | – | nt | nt | 6:00 | 87.75 |\n| ≥50 | 0 | 0 | – | – | nt | nt | 6:15 | 87.16 |\n| ≥100 | 0 | 0 | – | – | nt | nt | 6:15 | 87.21 |\n| 1 | 0 | 1 | nt | nt | 10:15 | 82.50 | 9:00 | 88.26 |\n| 10 | 0 | 1 | nt | nt | 13:00 | 82.49 | 7:30 | 88.31 |\n| 10 | 0 | 0 | nt | nt | – | – | 7:00 | 88.26 |\n| -ve control |  |  | – | – | – | – | – | – |\n|  | +ve control |  | 7:30 | 81.83 | nt | nt | 6:00 | 87.67 |\n|  |  | +ve control | nt | nt | 11:30 | 82.42 | 8:00 | 88.41 |\n\nStatement: Samples tested with LAMP assays for D. medinensis Tp (min:sec) 8:45 Number spiked into sample Number spiked into sample D. medinensis is 1.",
  "question": "Is the statement backed up by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q912c0bbe64",
  "kind": "yes/no",
  "text": "Customer: i need to watch good movie in davis california.\nAgent: No problem. Do you have a movie in mind?\nCustomer: need to watch movie no time to die.\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: there no tickets available shows in davis.\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: oh sad, then what action films going in davis.\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Is there any original films from 70s running.\nAgent: The release date for this film is October 12, 1979.\nCustomer: Ok i am not going to buy movie tickets right now. my favourite movies are not available. so need just buy tickets later.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By the end of this dialogue, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q0bd4d6afa8",
  "kind": "yes/no",
  "text": "Assistant: I will. I'm dialing now.\nCustomer: Have you contacted them yet?\nAssistant: Yes, they are on the way they should arrive within the next 5 min.",
  "question": "Going by the assistant's final message, is \"5 min\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd69932387f",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nConclusions The population prevalence of SARS-CoV-2 antibodies in Santa Clara County implies that the infection is much more widespread than indicated by the number of confirmed cases.\n\nClaim: The actual infection rate in Santa Clara County was greater than the rate of confirmed cases.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q5628b424f2",
  "kind": "yes/no",
  "text": "Complaint narrative: WENT OUT FROM WORK TO START MY CAR AND NOTICED THE AIRBAG LIGHT WOULD NOT GO OUT. I SHUT THE CAR OFF AND RESTARTED TO SEE IF IT WOULD GO OUT. IT WOULD NOT. THE VERY NEXT DAY, I WENT TO OPEN THE FRONT DOOR ON THE PASSENGER SIDE TO PUT SOMETHING IN THE CAR. THE HANDLE FELL OFF IN MY HAND. THE PASSENGER SIDE DOOR IS HARDLY USED AS I AM THE ONLY OCCUPANT OF THE CAR. IT HAD NOT BEEN HIT OR DAMAGED, THE COVER JUST BROKE OFF. I TOOK THE VEHICLE IN TO THE KIA DEALER. THE ADVISED ME THAT I WOULD HAVE TO LEAVE THE VEHICLE, PAY $85 FOR A DIAGNOSTIC TEST SO THEY COULD SEE WHY THE LIGHT WOULD NOT GO OUT. THEY SAID IT WAS NOT COVERED UNDER WARRANTY THAT THE WARRANTY FOR IT RAN OUT AT 60K MILES. SAME WITH THE HANDLE. I HAVE TO PAY OVER $40 JUST FOR THEM TO REPLACE THE HANDLE'S COVER. THEY SAID ONCE THEY FOUND OUT WHY THE AIRBAG LIGHT WAS ON, IF I PAID TO HAVE IT REPAIRED THAT THEY WILL WAIVE THE DIAGNOSTIC FEE. SO I HAVE TO RENT A VEHICLE OUT OF POCKET FOR NO TELLING HOW LONG, AND PAY FOR WHAT EVER IS WRONG WITH THE AIRBAG LIGHT. THEY CLAIM THAT IT WILL NOT DEPLOY IF I GO INTO AN ACCIDENT. I'VE READ SEVERAL OTHER COMPLAINTS ABOUT THE 2012 KIA SORRENTO AIRBAG NOT DEPLOYING. ANOTHER LAW SUIT IN THE MAKING JUST LIKE THE GAS MILEAGE ONE THEY JUST WERE SUED FOR.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "qa987495e2a",
  "kind": "yes/no",
  "text": "Customer: Lets go to the movies.\nAgent: Ok, what theater?\nCustomer: Check AMC Studios 30.\nAgent: Ok, what movie for?\nCustomer: Do they have Street Dancer 3?\nAgent: Yes, they do.\nCustomer: Ok, what times do they have?\nAgent: 3:30 pm, 6:45 pm and 10:00 pm\nCustomer: Does 6:45 pm work?\nAgent: Yes that is perfect.\nCustomer: Ok sounds like a plan.\nAgent: Just to confirm you want two tickets for Street Dancer 3 at 6:45 pm at AMC Studios 30 theater.\nCustomer: No, three tickets, Bruce is coming also.\nAgent: Ok, so its three tickets for Street Dancer 3 at 6:45 pm at AMC Studios 30 theater.\nCustomer: Yes that is perfect.\nAgent: How will you be paying for these.\nCustomer: No need to buy them now, I will deal with that when I get to the theater tonight.\nAgent: Ok that is perfect. I won't book anything.\nCustomer: Thanks for looking this up.\nAgent: No problem, see you then.",
  "question": "By the end of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q5c15170c0a",
  "kind": "yes/no",
  "text": "Statement 1: he eats toast every morning\nStatement 2: he eats books every morning",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qb425ba6045",
  "kind": "yes/no",
  "text": "Customer: Hey, what family friendly movies are playing in Las Cruces?\nAgent: Let me check that for you.\nCustomer: Awesome!\nAgent: I see Jumanji, sonic, and Doolittle.\nCustomer: Oh, I think they would like any of those. Where are they playing?\nAgent: I see them at three different theaters, the Allen theater at the mall, the Allen theater in town Square, and the Cinemark.\nCustomer: Can we check times for sonic at the Allen theater in the mall?\nAgent: Yes, what day would you like to see it?\nCustomer: Sometime Saturday morning if possible.\nAgent: OK, I see sonic the hedgehog at the Allen theater in the mall at 11:15 am. Does that work for you?\nCustomer: Yes, that should be good.\nAgent: How many tickets do you need?\nCustomer: I need six tickets, two adults and four children.\nAgent: That sounds good, so you need to adults and four children for the movie sonic the hedgehog at the Allen theater at the mall?\nCustomer: Now that I think about it, my nephew might also be coming with us. I better check and see before I order.\nAgent: Would you like me to save this order for you?\nCustomer: Yes, save it for now and I’ll get back with you soon.\nAgent: OK, I will do it.\nCustomer: Thanks\nAgent: You are welcome.",
  "question": "Has the customer, by the end of this conversation, actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qf028bda4f0",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nRates of ventilation in the HC, HC+AZ, and no HC groups were 13.3%, 6.9%, 14.1%, respectively. The risk of ventilation was similar in the HC group (adjusted hazard ratio, 1.43; 95% CI, 0.53 to 3.79; P=0.48) and in the HC+AZ group (adjusted hazard ratio, 0.43; 95% CI, 0.16 to 1.12; P=0.09), compared to the no HC group. CONCLUSIONS: In this study, we found no evidence that use of hydroxychloroquine, either with or without azithromycin, reduced the risk of mechanical ventilation in patients hospitalized with Covid-19.\n\nClaim: Hydroxychloroquine does not help patients avoid being placed on a ventilator.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q7fd3d4c1e8",
  "kind": "yes/no",
  "text": "Situation: Addicted to the Juul\nAction being judged: Doing things that could cause harm to yourself.",
  "question": "Is the action, as judged by common social norms, acceptable?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qfc5e6afe89",
  "kind": "yes/no",
  "text": "Occupation: Fabric and Apparel Patternmakers\nDuties:\n- Start pumps to operate distilling systems that drain and reclaim dry cleaning solvents.\n- Operate machines that comb, dry and polish furs, clean, sterilize and fluff feathers and blankets, or roll and package towels.\n- Hang curtains, drapes, blankets, pants, and other garments on stretch frames to dry.",
  "question": "So, are the duties on the list part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qb60f279270",
  "kind": "yes/no",
  "text": "\"Google on Monday was among investors pumping $42 million into a climate change inspired technology startup that calculates the chances of crops being ruined by weather.\"",
  "question": "Does this block of text make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q773929c403",
  "kind": "yes/no",
  "text": "boris johnson is a lying bastard😠",
  "question": "Would it be correct to say that this post is not hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "q08365ef040",
  "kind": "yes/no",
  "text": "Customer: I would like to go to a movie.\nAgent: What movie are you interested in.\nCustomer: Either Birds of Prey or Sonic the Hedgehog.\nAgent: What theater?\nCustomer: AMC South Barrington.\nAgent: What showtime?\nCustomer: Something around 4:00 PM.\nAgent: How many tickets?\nCustomer: I need 2 tickets.\nAgent: What type of format?\nCustomer: Standard format is fine.\nAgent: Okay there is a 4:30 PM showing of Birds of Prey.\nCustomer: That times works, is there a showtime for Sonic?\nAgent: There is a 4:45 PM showing for Sonic. Which movie do you prefer?\nCustomer: I like the 4:45 PM showing for Sonic the Hedgehog.\nAgent: So 2 tickets to see Sonic the Hedgehog at 4:45 PM at the AMC South Barrington theater.\nCustomer: Correct, but I think we are going to wait til tomorrow to purchase the tickets.\nAgent: That showtime is available for tomorrow too.\nCustomer: Excellent, I will check with you tomorrow, and get those tickets ordered then.\nAgent: The order has been saved for tomorrow and awaits your approval.",
  "question": "Based on the text, by the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q089ce37118",
  "kind": "yes/no",
  "text": "As well as pumping much as 600 million tonnes more greenhouse gases into the atmosphere, the carbon credits scheme has been abused by countries like Russia and the Ukraine which have used them as a money making scam.",
  "question": "Made by this paragraph, is the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q6e3bd45488",
  "kind": "yes/no",
  "text": "Table caption: Methods used for the [ 11 C]CO 2 -reduction in published studies on 11 C‑carbonylations.\n| Reduction method | Research articles (total 119) |\n| Zn (400 °C) | 68 |\n| Mo (850 °C) | 38 |\n| Activated charcoal (800–900 °C) | 3 |\n| Organosilanes | 3 |\n| Zn + silica (485 °C) | 3 |\n\nStatement: Activated charcoal (800900 C) Research article is 3.",
  "question": "Would it be correct to say that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q0dc98b24c6",
  "kind": "yes/no",
  "text": "Customer: Yes, do any serve international food?\nAssistant: I have 2. The varsity restaurant and bloomsberry. Both serve international food and are in the moderate price range. Do you have a preference?",
  "question": "Was at least a single option that meets everything the customer asked for found by the assistant in its reply?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q6a362149c8",
  "kind": "yes/no",
  "text": "Occupation: Range Managers\nDuties:\n- Study rangeland management practices and research range problems to provide sustained production of forage, livestock, and wildlife.\n- Offer advice to rangeland users on water management, forage production methods, and control of brush.\n- Develop methods for protecting range from fire and rodent damage and for controlling poisonous plants.",
  "question": "For the occupation named above, are the listed duties part of its job?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q2f99440b38",
  "kind": "yes/no",
  "text": "Table caption: Average values of trash and neps parameters in a dataset of 20 genetic materials, processed with five different ginning approaches.\n| Lint type | Neps per gram (count) | Visible Foreign Matter (%) | Trash per gram (count) | Dust per gram (count) |\n| Reference method | 353 | 3.11 | 156 | 427 |\n| Method I | 196 | 3.71 | 185 | 501 |\n| Method II | 256 , | 0.28 | 16 | 50 |\n| Method III | 257 , | 0.33 | 21 | 49 |\n| Method IV | 258 , | 0.78 | 43 | 128 |\n\nStatement: The lowest count for Trash per gram is 16.",
  "question": "Would it be correct to say that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qd2aeabad9d",
  "kind": "yes/no",
  "text": "Occupation: Soil and Plant Scientists\nDuties:\n- Construct historical, scientific, and nature visitor-center displays.\n- Survey park to determine forest conditions and distribution and abundance of fauna and flora.\n- Conduct field trips to point out scientific, historic, and natural features of parks, forests, historic sites, or other attractions.",
  "question": "Is it right to say that the listed duties are not part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "qc0ff52c212",
  "kind": "yes/no",
  "text": "Situation: I can't remember! Why can't I remember what he did to me??\nAction being judged: Doing something to someone without consent.",
  "question": "Is it true that the action being judged is not wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qdfc1d4e742",
  "kind": "yes/no",
  "text": "Customer: What do you recommend?\nAssistant: Cambridge artworks is wonderful! They are located at 5 greens road cb13ef. There phone number is 01223902168.",
  "question": "In its reply did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qe8249c7321",
  "kind": "yes/no",
  "text": "Complaint narrative: I WAS DRIVING AT THE HALLWAY AT 65 MPH AND THE POWER TO THE CAR SHUT OFF. I ALMOST CRASHED INTO OTHER CARS, WHEN THE ENGINE REDUCE POWER LIGHT CAME ON. I PULLED OVER AND WAITED 10 MINUTES TO START THE CAR. I WENT BACK HOME AND IT HAPPENED AGAIN ..... THE WENT TO THE SHOP FOUR TIMES, AND NO ONE WAS ABLE TO DIAGNOSE THE PROBLEM.",
  "question": "Is it correct that this vehicle safety complaint does not report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "q85b637aa73",
  "kind": "yes/no",
  "text": "Customer: Is \"Sam's Delight\" playing in town tonight?\nAgent: Did you mean is the movie \"Sam's Delight\" playing tonight at the Legacy Monument Family 12 theater in Land's End?\nCustomer: Yeah.\nAgent: \"Sam's Delight\" is playing tonight at the Legacy Monument Family 12 at 4:00 PM, 6:10 PM, 8:30 PM, and 10:40 PM.\nCustomer: What else is playing?\nAgent: Tonight at the Legacy Monument Family 12 the movie \"Far From You\" is also playing.\nCustomer: What times?\nAgent: \"Far From You\" is playing tonight at the Legacy Monument Family 12 at 8:40 PM and 10:40 PM.\nCustomer: Are tickets available for the eight o'clock shows?\nAgent: Did you mean are there tickets available for the 8:30 PM showing of \"Sam's Delight\" and the 8:40 PM showing of \"Far From You\"?\nCustomer: Yes.\nAgent: How many tickets?\nCustomer: Two adults?\nAgent: Yes, there are tickets available for both shows.\nCustomer: What were the times, again?\nAgent: \"Sam's Delight\" is showing at 8:30 PM and \"Far From You\" is showing at 8:40 PM.\nCustomer: Let's do \"Sam's\".\nAgent: So you would like me to purchase two adult tickets to tonight's 8:30 PM showing of \"Sam's Delight\" at the Legacy Monument Family 12?\nCustomer: Correct.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "Has the customer actually bought movie tickets by the time this conversation finishes?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qbfd4e7032d",
  "kind": "yes/no",
  "text": "Customer: Could you help me book a ticket for a movie?\nAgent: Sure thing! What movie?\nCustomer: 1917 please.\nAgent: Can I please know what theater you want to view it at?\nCustomer: AMC Naperville 16\nAgent: What time would you want to see it?\nCustomer: 10 PM\nAgent: They currently don't have that time.\nCustomer: Do you know if AMC South Barrington 24 has it at that time?\nAgent: Yes they do!\nCustomer: Can you book tickets for that theater then?\nAgent: Yes no problem. How many people?\nCustomer: 3 people are going to view it.\nAgent: Do you know if you want IMAX, 3D or standard?\nCustomer: Standard please.\nAgent: That sounds great. Is there any other tickets you need booked?\nCustomer: No that would be all.\nAgent: To confirm you want 3 tickets for 1917 at AMC South Barrington 24 for 10 PM\nCustomer: Yes that is perfect.\nAgent: Okay I have booked your tickets. Enjoy the show.\nCustomer: Thank you!",
  "question": "By the close of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qc5981c5f48",
  "kind": "yes/no",
  "text": "Customer: Hey, its time\nAgent: Movie time?\nCustomer: Yeah, any showings on dolittle?\nAgent: Not at the time you want at 11 or 10 pm\nCustomer: wow okay, that hurts\nAgent: yeah sorry\nCustomer: any other showings?\nAgent: Rise of skywalker?\nCustomer: Yes I love star wars!\nAgent: Okay let me see if there is room to book\nCustomer: okay\nAgent: There is not.\nCustomer: Wow\nAgent: sorry\nCustomer: Okay, could you check both again?\nAgent: I can try.\nCustomer: Do it\nAgent: Unavailable.\nCustomer: So no movies?\nAgent: No, sorry, I guess there is no booking to be done.",
  "question": "By the end of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q5d2d3625e9",
  "kind": "yes/no",
  "text": "Situation: He told his dad he didn't want to hunt quail.\nAction being judged: Saying no to doing something you aren't comfortable with.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qc44df1b152",
  "kind": "yes/no",
  "text": "Statement 1: Fish can survive without water\nStatement 2: Fish can't live without water",
  "question": "Among the statements presented: Statement 1, does it go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q64ac7fd0e2",
  "kind": "yes/no",
  "text": "Assistant: No, it doesn't look like they do for the oil change and tire pressure.\nCustomer: Ok, So what time should I be there again?\nAssistant: Your appointment is today, February, 28th at 2 pm.",
  "question": "Is it right to say that, according to the assistant's last message, \"2 pm\" isn't confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order.\n- no: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction."
 },
 {
  "qid": "qb43311e80b",
  "kind": "yes/no",
  "text": "Customer: i am looking for places to go in town. The attraction should be in the type of concerthall and should be in the centre part of town.\nAssistant: I would suggest The Man on the Moon, located at 2 Norfolk Street.",
  "question": "Going by the text, did the assistant's reply include at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qf3a6cf11c3",
  "kind": "yes/no",
  "text": "Complaint narrative: PULLING DOWN MY DRIVE WAY MY VEHICLE ACCELERATED WITHOUT ME TRYING. I HIT THE BRAKE AND E BRAKE. IT DID NOT STOP US. IN RESULT OF THE ACCELERATION MY HOUSE STOPPED US.",
  "question": "Does this vehicle safety complaint say the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qa391f4cc0e",
  "kind": "yes/no",
  "text": "Customer: Yes please make me a reservation at the Bloomsbury for 2 people at 19:30 on Thursday.\nAssistant: I'm sorry I wasn't able to make that booking. Would you like another day or time?",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "qb6d06cfcb4",
  "kind": "yes/no",
  "text": "Complaint narrative: THE HEADLIGHTS ON MY 2018 HYUNDAI SONATA SHOW TWO BLACK NOTCHES AND A BLACK LINE ABOUT 30 FEET IN FRONT OF THE CAR IN LOW LIGHT CONDITIONS. IT IS VERY DISTRACTING AND DANGEROUS AS THESE SHADOWS DART ACROSS YOUR PATH AS YOU MAKE TURNS OR GO UP HILLS. HYUNDAI SERVICE COULD SEE THE NOTCHES, BUT SAID \"THE SYSTEM IS WORKING WITHIN SPECIFICATIONS AT THIS TIME\". SOMETHING NEEDS TO BE DONE BEFORE SOMEONE IS KILLED BECAUSE OF THESE UNSAFE LIGHTS.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "qb0670d527f",
  "kind": "yes/no",
  "text": "Table caption: Min/max value and MAPE for air velocity of the drying air in the HPD TF1 during drying of separated digestate at different set values\n| v set m·s -1 | v meas minm·s -1 | v meas maxm·s -1 | MAPE (v)% |\n| 0.3 | 0.28 | 0.38 | 8.91 |\n| 0.5 | 0.48 | 0.51 | 0.63 |\n| 0.7 | 0.66 | 0.70 | 0.55 |\n\nStatement: The highest value of MAPE (v)% is 8.91",
  "question": "Is it right to say that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 }
]
