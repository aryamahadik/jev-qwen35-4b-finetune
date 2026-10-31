# T37b blind solver T37b-blind_read-8cc57983-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_full/s13/answers/T37b-blind_read-8cc57983-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q4e0bc74ff5",
  "kind": "yes/no",
  "text": "A quote from an IPCC lead author: There are far too many politically correct appointments, so that developing country scientists are appointed who have insufficient competence to do anything useful.",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q6678b6abe1",
  "kind": "yes/no",
  "text": "Table caption: Rate of Return of different insulation technologies ( Milieucentraal, 2019 ).\n| Insulation technology | Rate of Return (%) |\n| Wall insulation | 11 |\n| Floor insulation | 7 |\n| Double glazing | 6 |\n| Roof insulation | 8 |\n\nStatement: Roof insulation is having 8% second highest of rate of return.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8743e16d6b",
  "kind": "yes/no",
  "text": "Complaint narrative: THIS WAS A LOW MILEAGE (9K) LESS THAN 1 YEAR OLD PRISTINE CONDITION AUDI S6. THE VEHICLE WAS DRIVEN APPROXIMATELY 10 MILES AND THEN PARKED IN A DRIVEWAY WHERE IT WAS TURNED OFF. THE DRIVER SAT IN THE VEHICLE FOR 5 MINUTES WITH THE ENGINE OFF PRIOR TO EXITING THE VEHICLE. BETWEEN 5 TO 10 MINUTES AFTER EXITING THE VEHICLE WE SMELLED SMOKE IN THE HOUSE. WE DISCOVERED THE VEHICLE HAD FLAME AND SMOKE EMANATING FROM UNDER ITS HOOD. THE FIRE DEPARTMENT HAD TO EXTINGUISH THE FLAMES AS WE WERE UNABLE TO DO SO WITH A GARDEN HOSE. THE ENTIRE FRONT OF THE VEHICLE BURNED. IT WAS CLASSIFIED AS TOTALED. THE VEHICLE WAS INSPECTED BY A FIRE CAUSE AND ORIGIN INSPECTOR AND AUDI. I HAVE BEEN TOLD VERBALLY THAT THE FIRE LIKELY BEGAN IN SOME ELECTRICAL COMPONENTS BEHIND THE DRIVER SIDE HEADLIGHT AREA. AUDI HAS CONFIRMED THAT THE FIRE WAS NOT CAUSED BY EXTERNAL FACTORS BUT I HAVE NOT BEEN PROVIDED ANY OTHER FEEDBACK FROM AUDI AS TO WHAT THE ACTUAL DEFECT. WAS. JUST TO RE-CAP: 1. THE IGNITION WAS OFF 2. THE CAR WAS NOT RUNNING 3. THE CAR SPONTANEOUSLY CAUGHT FIRE AND WAS DESTROYED. 4. IT WAS RAINING THAT DAY 5. THE CAR WAS IN LIKE-NEW CONDITION, WELL MAINTAINED AND WITH NO KNOWN DEFECTS. 6. WE WERE LUCKY THE CAR WAS NOT IN THE GARAGE AS THE HOUSE WOULD HAVE CAUGHT FIRE.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qd609f6ae3d",
  "kind": "yes/no",
  "text": "Assistant: O.K. Now for the toppings.\nCustomer: Green olives and tomatoes on one.\nAssistant: Green olives not available.",
  "question": "According to the assistant's last message, is \"Green olives\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q29a05252a9",
  "kind": "yes/no",
  "text": "Statement 1: a dog is taken to a pool after getting sick\nStatement 2: a dog is taken to a veterinarian after getting sick",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q03a2b57320",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nOf these, 94 were working in an 11th-floor call center with 216 employees, translating to an attack rate of 43.5% (95% CI 36.9%–50.4%).\n\nClaim: Superspreading events can happen at call centers.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q14d9838ec3",
  "kind": "yes/no",
  "text": "Customer: Hello assistent\nAgent: Hello\nCustomer: I would like order some movie tickets\nAgent: Ok, what movie would you like to see?\nCustomer: I would like to see the movie, 1917\nAgent: Ok, what theater would you like?\nCustomer: Watertown\nAgent: Ok, and what showtime would you prefer\nCustomer: I would like to get 7:00 PM\nAgent: Alright let me take a look at availability\nCustomer: Perfect, thank you.\nAgent: Alright upon review it seems like the 7:00 PM show for the movie 1917 in Watertown is sold out and there are no tickets available.\nCustomer: Darn.\nAgent: Is there another movie you would have interest in?\nCustomer: Sure, could you tell me what else in playing in Watertown?\nAgent: Yes, the shows currently playing are: Little Women, 1917, Fast Cars, Cats, Bad Boys III, Weekend at Bernies, and Saving Private Ryan.\nCustomer: I would like tickets to Little Women please.\nAgent: Alright, what time?\nCustomer: I would like a 8 PM showing and I would need two tickets for the show.\nAgent: Alright, let me take a look.\nCustomer: Thank you.\nAgent: Alright, upon reviewing the schedule Little Women is not playing at 8 PM. It's show times are only 5:00 PM and 9:00 PM. Will either of those times work for you?\nCustomer: No unfortunately they will not work for me.\nAgent: Sorry, is there anything else i can do for you?",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q19135e0355",
  "kind": "yes/no",
  "text": "And with a low-end temperature rise comes along low-end impacts. Seemingly good news for all!",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q67363bf80a",
  "kind": "yes/no",
  "text": "Assistant: Alright. What type of Uber would you like?\nCustomer: UberBlack is fine.\nAssistant: I'm sorry, it looks like UberBlack is not available at this time. Do you have a second preference?",
  "question": "According to the assistant's last message, is \"UberBlack\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4d4ae43d51",
  "kind": "yes/no",
  "text": "Customer: Hey assistant, when is 1917 playing at Cinemark in Strongsville?\nAgent: 1917 showtimes are 5:00pm, 6:00pm, and 7:15pm. Would you like me to check these times for ticket availability?\nCustomer: Yes, please check 6:00pm\nAgent: How many tickets do you need?\nCustomer: I need 2 tickets\nAgent: There are not enough seats available for this showtime. Would you like to select another?\nCustomer: No, I would like you to check another theater\nAgent: Which theater would you like me to check?\nCustomer: AMC in Ridge Park\nAgent: Are you still interested in seeing 1917?\nCustomer: Yes, what showtimes are available?\nAgent: There are shows at 5:15pm, 6:00pm, 7:15pm and 8:00 pm\nCustomer: Please check availability for 6:00pm\nAgent: Are you still interested in 2 tickets?\nCustomer: Yes\nAgent: Good news, there are 2 tickets available for this showtime. would you like to book this showtime?\nCustomer: Yes\nAgent: Ok, just to confirm, you would like to order 2 tickets to see 1917 at AMC in Ridge Park at 6:00pm\nCustomer: That is correct\nAgent: Great I have placed the order with your default credit card. You will receive a confirmation email shortly.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q4a853087e1",
  "kind": "yes/no",
  "text": "Assistant: Ok. I need what is a best phone number?\nCustomer: They can reach me at 123-456-8989\nAssistant: TOday does not work. Would tomorrow morning at 8 a.m. be Ok?",
  "question": "According to the assistant's last message, is \"TOday\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q95dba05cef",
  "kind": "yes/no",
  "text": "Assistant: 6:30\nCustomer: Ok, I'll get two tickets for the 3d showing\nAssistant: the 3D showing is sold out",
  "question": "According to the assistant's last message, is \"3D\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q90506d30f9",
  "kind": "yes/no",
  "text": "Complaint narrative: WHILE DRIVING ALL OF THE POWER CUTS OFF INCLUDING POWER STEERING. ALTERNATOR, OIL, FUEL, STRUTS, BATTERY X 2 HAVE BEEN CHANGED OUT IN ATTEMPT TO CORRECT ISSUE. ISSUE IS STILL PRESENT. LOCAL CHEVY DEALERSHIP UNABLE TO RECTIFY PROBLEM. THERE HAVE BEEN NUMEROUS INCIDENTS WITH POTENTIAL ACCIDENTS. THERE SEEMS TO BE A POWER DRAW ON THE SYSTEM, UNABLE TO FIND ANY KINKED OR FRAYED WIRES. WHILE DRIVING ALL LIGHTING INCLUDING GAUGES DIMS USUALLY PRIOR TO COMPLETE VEHICLE ELECTRICAL FAILURE. I HAVE A VIDEO OF ELECTRICAL DIMMING, BUT UNABLE TO LOAD ON HERE. VEHICLE IS LABELED AS 2015 BUT MANUFACTURE DATE IS 2014, IVE NOTICED THERE IS A RECALL ON 2014 MODELS FOR ELECTRICAL CHASSIS FAILURE HOWEVER MY VIN IS NOT ENCOMPASSED IN THIS RECALL.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q868cf03659",
  "kind": "yes/no",
  "text": "Customer: Hi,can u please help me to book movie tickets\nAgent: Ya of course,do u any location in your mind\nCustomer: Yes i am looking theater in Spring Hills Kansas\nAgent: Ok,currently there are two movies running in that area\nCustomer: Ok can u please tell me what are the movies and they details\nAgent: Not My Problem, Beyond The Storm this are the movies which are currently running\nCustomer: Can u explain the stories of both the movies\nAgent: Movie1: Not My Problem - Comedy - rated PG-13 - Rotten Tomatoes 72% - A troubled teen tries to convince his depressed elderly neighbor that things are not what they seem. - Stars Matt Damon and Noah Schnapp.\nCustomer: Ratings are good also i would prefer to watch comedy movie,can u tell about the second movie\nAgent: Movie2: Beyond The Storm - Action - rated PG-13 - Rotten Tomatoes 81% - Fishing the North Sea gets ugly as Captain John’s crew faces not only severe weather but a traitor on board - directed by James Cameron.\nCustomer: I love to watch action movies\nAgent: Which movie did u prefer?\nCustomer: I will go with the second movie Beyond The Storm\nAgent: Ok, how many tickets do u need\nCustomer: I need 3 tickets can u tell the timing for both the movies\nAgent: Not My Problem: AMC Holiday Theater - 1pm - 3:55pm - 7pm - 10:05pm Beyond the Storm: Cinemark Downtown - 1:30pm - 3:40 - 6:10pm - 8:30pm\nCustomer: I will go with the 6.10 pm show in cinemark downtown\nAgent: ok, its 3 tickets for BEYOND THE STROM for 6.10 pm show in cinemark downtown is it right can i book for u\nCustomer: Yes, you can boo\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q5b46016ce6",
  "kind": "yes/no",
  "text": "Customer: I would like to purchase movie tickets.\nAgent: What movie would you like to see?\nCustomer: I would like to see Little Women.\nAgent: How many tickets do you need?\nCustomer: I need 2 tickets.\nAgent: Where would you like to see the movie?\nCustomer: At the RiverPark cinemas in Oxnard.\nAgent: Do you have a preference on times?\nCustomer: yes, I would love something in the early afternoon. maybe around 1pm.\nAgent: There is a 1:30pm and a 5:15pm, which works for you?\nCustomer: The 1:30pm, thank you.\nAgent: The 1:30pm showing appears to be sold out. Would you like me to purchase tickets for the 5:15pm?\nCustomer: No, that is too late.\nAgent: Is there anything else I can help you out with?\nCustomer: Yes, is the new Star Wars movie playing at that theater in the early afternoon?\nAgent: There is a 1:45pm showing of the new Star Wars movie.\nCustomer: Is it in 3-D?\nAgent: Yes, would you like me to book the tickets?\nCustomer: Yes please.\nAgent: You are confirmed to see the new Star Wars movie in 3-D at 1:45pm at the RiverPark cinemas in Oxnard.\nCustomer: Thank you!\nAgent: Is there anything else I can assist you with?\nCustomer: No thank you.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q12a8600ef3",
  "kind": "yes/no",
  "text": "In fact, it is almost certain that the wind-generated electricity cost more when the consumer payments, taxpayer subsidies, and the cost of the backup gas generation are added together. There is no doubt that it cost significantly more to generate electricity from wind than from natural gas .",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q733086ee1e",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2006, the science journal \"Nature\" listed Pharyngula as the top-ranked blog written by a scientist.\n\nSummary sentence:\nIn 2006 the journal \"Nature\" listed Myers's \"Pharyngula\" as the top-ranked blog by a scientist based on popularity.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q77174d636d",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nVirus was widely distributed on floors, computer mice, trash cans, and sickbed handrails and was detected in air ≈4 m from patients.\n\nClaim: The coronavirus can be detected in the air up to 13 feet away from an infected patient.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qfccc2c17a9",
  "kind": "yes/no",
  "text": "Customer: I want to watch a movie tonight\nAgent: No problem. Do you have a movie in mind?\nCustomer: I am thinking of No Time To Die\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: is there no showing in Davis, California?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: too bad. what action films are playing in Davis, California?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: is that the original film from the 1970s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: great, I think I will buy the tickets tomorrow\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q413c5cf713",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nIndeed, patients with COVID-19 are at accelerated risk for delirium due to at least seven factors including (1) direct central nervous system (CNS) invasion, (2) induction of CNS inflammatory mediators, (3) secondary effect of other organ system failure, (4) effect of sedative strategies, (5) prolonged mechanical ventilation time, (6) immobilization, and (7) other needed but unfortunate environmental factors including social isolation and quarantine without family.\n\nClaim: COVID-19 patients experience no significant risk factors for delirium during their treatment.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q447c937633",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThese studies confirm that cats are susceptible to productive SARS-CoV-2 infection, but are unlikely to develop clinical disease.\n\nClaim: Cats can be infected by the novel coronavirus but are unlikely to get sick.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q92a69e61c2",
  "kind": "yes/no",
  "text": "Table caption: List of Nature reserves in Kazakhstan.\n| Sr. # | Name | Location | Area of reserves | Year |\n| 1 | Aksu-Jabagly State Nature Reserve | Turkestan and Jambyl regions | 131,934 | 1926 |\n| 2 | Almaty State Nature Reserve | Almaty region | 71,700 | 1931 |\n| 3 | Naurzum State Nature Reserve | Kostanay region | 191,381 | 1931 |\n| 4 | Barsa-Kelme’s State Nature Reserve | Kyzyl Orda region | 160,826 | 1939 |\n| 5 | Korgalzhyn State Nature Reserve | Akmola and Karaganda regions | 543,171 | 1968 |\n| 6 | Markakol State Nature Reserve | East Kazakhstan region | 102,979 | 1976 |\n| 7 | Ustyurt State Nature Reserve | Mangystau region | 223,342 | 1984 |\n| 8 | West Altai State Nature Reserve | East Kazakhstan region | 86,122 | 1992 |\n| 9 | Alakol State Nature Reserve | Almaty and East Kazakhstan | 65,217,9 | 1998 |\n| 10 | Karatau State Nature Reserve | Turkestan region | 34,300 | 2004 |\n\nStatement: Year started from 1926 to 2004 .",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc4711fdf19",
  "kind": "yes/no",
  "text": "Occupation: Textile Cutting Machine Setters, Operators, and Tenders\nDuties:\n- Notify other workers of defects, and direct them to adjust extruding and forming machines.\n- Lower pans inside cabinets to catch molten filaments until flow of polymer through packs has stopped.\n- Start metering pumps and observe operation of machines and equipment to ensure continuous flow of filaments extruded through spinnerettes and to detect processing defects.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q2e159a14e5",
  "kind": "yes/no",
  "text": "Statement 1: oil can be found in the sky\nStatement 2: oil can be found in the underground",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qfbe658b92f",
  "kind": "yes/no",
  "text": "Statement 1: I put the car seat in the car.\nStatement 2: I put the oven in the car.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q8f5fd56bfb",
  "kind": "yes/no",
  "text": "Situation: I'm fantasizing about a coworker\nAction being judged: Doing things that could make a coworker uncomfortable.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q4f4e0e32ab",
  "kind": "yes/no",
  "text": "Situation: I knew when my dad was dying.\nAction being judged: Visiting your parent when they are on their death bed.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qb743daafad",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nUsing global line-list data on COVID-19 cases reported until 29th February 2020 and global gridded temperature data, and after adjusting for surveillance capacity and time since first imported case, higher average temperature was strongly associated with lower COVID-19 incidence for temperatures of 1°C and higher.\n\nClaim: Multiple early studies provide evidence of less correlation between temperature and humidity ranges and the geographic regions where this virus has thrived.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q3e288e229a",
  "kind": "yes/no",
  "text": "Customer: Hi, what's the best movie playing in Spring Hills Kansas right now?\nAgent: Well, that's a good question, regarding Rotten Tomatoes reviews, it would be Back country, playing at the Cinemark Downtown.\nCustomer: What score did they get exactly?\nAgent: 91%, would you like tickets?\nCustomer: Wait, what's it about?\nAgent: It's about Yosemite, it's rated G.\nCustomer: It sounds good but is that James Cameron movie out now?\nAgent: It is, it's playing at the Cinemark Downtown also.\nCustomer: What's the name of it?\nAgent: Beyond the storm.\nCustomer: I think I've heard of it.\nAgent: Would you like tickets?\nCustomer: Yes, I think that's the one.\nAgent: How many tickets would you like?\nCustomer: I need two. Get me the latest showing please.\nAgent: Ok, I have 2 for Beyond the Storm, Cinemark Downtown, tonight's showing, Spring Hills Kansas.\nCustomer: That's perfect yes.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.\nCustomer: Thanks I see them, good night.\nAgent: Enjoy your show.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q8210357ff4",
  "kind": "yes/no",
  "text": "Complaint narrative: WHILE ATTEMPTING TO OPERATE THE ELECTRIC SLIDING SIDE DOOR, A LARGE SPARK AND SMALL DEBRIS FIRE WAS SEEN IN THE BOTTOM DOOR RAIL. UPON INSPECTION, A BREAK IN THE WIRE HARNESS HAD ALOUD WIRES TO BE SEVERED THAT CONTROLS THE DOOR AND LOCKING SYSTEM. THE AUTOMATIC DOOR LOCKS ON BOTH SIDE DOORS NO LONGER WORKED AND THE PASSENGER SIDE DOOR WOULD NO LONGER OPEN ELECTRICALLY. I REMOVED THE WIRING HARNESS AND WIRES AND DISCARDED THEM TO AVOID ANY MORE PROBLEMS (SPARKING AND/OR FIRES). THIS COULD CAUSE A MAJOR FIRE HAZARD IN THE RIGHT ENVIRONMENT.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q7dcf60ad10",
  "kind": "yes/no",
  "text": "Complaint narrative: TAKATA RECALL LETTER THAT WE RECEIVED FROM TOYOTA DIRECTED US TO STOP USING THE PASSENGER SEAT IN THE CAR DUE TO SAFETY CONCERNS, AND ADVISED THAT WE WOULD RECEIVE FURTHER INSTRUCTIONS IN APRIL. IT IS NOW MAY AND WE HAVE NOT HEARD FROM TOYOTA AND THE LOCAL DEALERSHIP ADVISES US THAT NO REMEDY IS AVAILABLE FOR US. WE ARE NOT ABLE TO SAFELY USE THE VEHICLE AS A FAMILY, AND WE HAVE NO IDEA WHEN OR IF WE WILL BE ABLE TO USE THE VEHICLE SAFELY AGAIN. THE VEHICLE IS CURRENTLY BEING USED DAILY BY DRIVER ONLY, AND IT IS UNCLEAR WHETHER THE VEHICLE POSES A THREAT TO DRIVER'S SAFETY.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qa0bf95b19e",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThe odds that a primary case transmitted COVID-19 in a closed environment was 18.7 times greater compared to an open-air environment (95% confidence interval [CI]: 6.0, 57.9).\n\nClaim: The odds of catching the coronavirus are about 20 times higher indoors than outdoors.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qbb74d71880",
  "kind": "yes/no",
  "text": "Customer: Good morning, can I get some movie tickets today?\nAgent: Sure, for what city?\nCustomer: Stoneyford Oregon.\nAgent: What movie would you like to see?\nCustomer: Let’s look for all Mulan.\nAgent: What day and time would you like to see Mulan?\nCustomer: Today, sometime this afternoon it doesn’t matter exactly what time.\nAgent: Do you have a theater preference?\nCustomer: Yes, either the Mountain AMC 16 or Holiday Cinemark 12.\nAgent: There aren’t any showings of Mulan at either theater.\nCustomer: How about No Time To Die?\nAgent: There are no showings for that movie either.\nCustomer: Is anything playing?\nAgent: It appears that the Mountain AMC 16 and Holiday Cinemark 12 are both temporarily closed.\nCustomer: Are those two movies playing anywhere else?\nAgent: No, it appears as though the release dates have been pushed back.\nCustomer: Do you know when they will be coming out?\nAgent: Yes, they have been rescheduled for sometime this fall.\nCustomer: I guess I’ll check back with you sometime this fall. Thanks.\nAgent: No problem.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q168d80dbeb",
  "kind": "yes/no",
  "text": "Customer: I'm looking to buy movie tickets in Davis California\nAgent: No problem. Do you have a movie in mind?\nCustomer: I dunno, I was thinking about that James Bond movie No Time To Die.\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: Are there no showings in Davis, CA?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: Oh, dang, that sucks. What action films are playing in Davis, CA?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Mad Max? You mean the original one from 1970s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: Huh, okay, thanks for all your effort but I'm not gonna buy tickets right now since my film choice isn't available in my area.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q31d3ace76f",
  "kind": "yes/no",
  "text": "Situation: I would, absolutely, sell my soul to a demon for the right price.\nAction being judged: Selling your soul for money.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q028843ed50",
  "kind": "yes/no",
  "text": "Whatever alternative technologies they support comply with their precautionary principle. Whatever they oppose violates it. They trumpet alleged risks of using frackingand hydrocarbon technologies, but ignore even the most obvious benefits of using them and most obvious risks of not using them.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q9b7efc64c0",
  "kind": "yes/no",
  "text": "Customer: Can you help me with booking movie tickets?\nAgent: Yes.\nCustomer: I'm looking for a theater in the Austin area.\nAgent: There is a Alamo and a AMC.\nCustomer: I would like to go to the Alamo Drafthouse.\nAgent: What movie are you going to see?\nCustomer: Bad Boys for Life.\nAgent: How many tickets do you need?\nCustomer: One.\nAgent: Would you like standard, IMAX, or 3d?\nCustomer: 3d.\nAgent: There is a 3d showing at 4:00pm.\nCustomer: That is fine.\nAgent: Where would you like to sit?\nCustomer: The front.\nAgent: Okay. Let me confirm, one ticket for Bad Boys at 4:30?\nCustomer: That's right.\nAgent: Okay. You're confirmation number is 8137768.\nCustomer: Thank you.\nAgent: You are welcome.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qf5dfbbdb53",
  "kind": "yes/no",
  "text": "I frankly find it immensely sad that, not only real events, but also the work and knowledge of serious scientists, accumulated over many years, can apparently be swept aside at the whim of an algorithm. Computer models can have their value, but we surely need to keep an eye on whats happening in the real world.",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qfdf6ce9780",
  "kind": "yes/no",
  "text": "Occupation: Motion Picture Projectionists\nDuties:\n- Set up and adjust picture projectors and screens to achieve proper size, illumination, and focus of images, and proper volume and tone of sound.\n- Coordinate equipment operation with presentation of supplemental material, such as music, oral commentaries, or sound effects.\n- Operate equipment to show films in a number of theaters simultaneously.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qeb26d7f445",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS: The incidence of VTE in patients with severe NCP is 25% (20/81), which may be related to poor prognosis.\n\nClaim: There are approximately 1 in 4 incidences of venous thromboembolism in patients with severe novel coronavirus pneumonia symptoms of SARS-CoV-2.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qa6d10f5f87",
  "kind": "yes/no",
  "text": "Table caption: Results of the 3-way crossed ANOSIM analyses for the taxa fishes, crustaceans and echinoderms. Global tests on the effects of sampling area foundations and controls, year and geographical position.\n|  | Sampling area | Sampling area | Year | Year | Geographical position | Geographical position |\n| Taxa | Global R | P-value | Global R | P-value | Global R | P-value |\n| Fishes | 0.494 | 0.0001 | 0.19 | 0.0001 | 0.078 | 0.012 |\n| Crustaceans | 0.68 | 0.0001 | 0.161 | 0.0001 | 0.034 | 0.122 |\n| Echinoderms | 0.552 | 0.0001 | 0.152 | 0.0001 | 0.055 | 0.056 |\n\nStatement: The P-value for Sampling area and Year is constant 0.0001.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb4570ff125",
  "kind": "yes/no",
  "text": "Situation: I barely taught my dog not to beg but my gf and I let her eat with us constantly.\nAction being judged: Dogs and humans not eating at the same table.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q1aecdc6bb0",
  "kind": "yes/no",
  "text": "U.S. President Barack Obama and first lady Michelle Obama wave during the inaugural parade from the U.S. Capitol to the White House in Washington, January 21, 2013.",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q6cb1d97a37",
  "kind": "yes/no",
  "text": "Customer: Hey!\nAgent: Hi what can I help you with today?\nCustomer: Well I am getting a bit bored and am in the mood for a good movie.\nAgent: SUre I can help. What did you want to see\nCustomer: Well how about Mulan I would need one adult and two child tickets. or perhaps No Time t Die\nAgent: Where did you want to see that at.\nCustomer: Well my first choice would be the Holiday Cinemark in Stoneyford Oregon\nAgent: SUre, let me check\nCustomer: Okay.\nAgent: I am sorry but that Theater is temporarily closed due to the virus. And Mulan is not going to be released now until the fall.\nCustomer: Oh I see, maybe I can get a babysitter so I could go see No time to die.\nAgent: Well did you want to try another theater?\nCustomer: Sure how about the Mountain AMC 16 in Stoneyford.\nAgent: How many tickets\nCustomer: 2 Adults please\nAgent: Ok let me check\nCustomer: Thank you.\nAgent: I am sorry but that theater is also temporarily closed. That movie is also postponed until the fall as well. It seems both theaters are closed and both movies are postponed until the fall.\nCustomer: Ok well I guess I am out of luck.\nAgent: Im sorry! We look forward to serving you again hopefully in the near future!!!!",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q091facebfa",
  "kind": "yes/no",
  "text": "Customer: We are looking for an expensive panasian restaurant and prefer it to be in the same area as the hotel. Any suggestions?\nAssistant: I'm sorry but there does not seem to be any expensive panasian restaurants located on the west side.  Would you like to try to search for something else?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q91a9a8c49f",
  "kind": "yes/no",
  "text": "Situation: I think I sold a suicidal woman sleeping pills\nAction being judged: Selling things that people can use to kill themselves when that person is suicidal.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "qf65782402b",
  "kind": "yes/no",
  "text": "Situation: It took him an hour to eat all the chili in the bowl.\nAction being judged: Taking your time when eating lots of food.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q63075f0773",
  "kind": "yes/no",
  "text": "Situation: I get mad if my parents throw away my bubble wrap.\nAction being judged: Throwing out something when it belongs to someone else.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q5caaaff362",
  "kind": "yes/no",
  "text": "A British High Court judge ruled that \"An Inconvenient Truth\" promotes \"partisan political views,\" was riddled with errors and falsehoods, and could not be shown any more in schools, unless accompanied by a teacher's guide correcting information that Gore had misrepresented. Two of the most egregious distortions are especially likely to scare kids.",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q81c16d867f",
  "kind": "yes/no",
  "text": "Complaint narrative: DROVE TO WORK AT 6 AM WENT TO USE FOR LUNCH VEHICLE HAD NO POWER ASSISTED STEERING MORE LIKE MANUAL STEERING. MAKING VERY DIFFICULT IN PARKING , ON RAMPS TURNING AT INTERSECTIONS. MY MECHANIC TELLS ME STEERING COLUMN PART FAILURE THAT THEY HAVE REPLACED IN SEVERAL ESCAPES & MARINERS. MY BOSS WENT ON LINE AND FOUND INFO ON RECALL OF 915,216 FORD ESCAPES & MERCURY MARINERS. PROBLEM WAS WHEN BACKING OUT OF PARKING SPOT TYING TO TO TURN TO RIGHT WAS VERY DIFFICULT MORE LIKE MANUAL STEERING",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 }
]
