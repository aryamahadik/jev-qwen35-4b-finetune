# T37b blind solver T37b-blind_read-8cc57983-001 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_full/s13/answers/T37b-blind_read-8cc57983-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q71059ed6dc",
  "kind": "yes/no",
  "text": "Customer: Siri, what movies are playing in town?\nAgent: Star Wars and 1917 are playing today.\nCustomer: Are there any showtimes for 1917 tomorrow evening?\nAgent: Yes, 1917 is playing at 7:10pm.\nCustomer: Im unavailable for that time, are there any showings for star wars tomorrow?\nAgent: No, Star Wars is not playing this evening.\nCustomer: Is star wars playing in the town to the west of my location?\nAgent: Yes\nCustomer: What time does it start tomorrow?\nAgent: Star Wars starts playing at 6:35 pm.\nCustomer: What other movies are playing there?\nAgent: 1917 is also playing there.\nCustomer: Are there any showings in the evening?\nAgent: 1917 starts at 9:40pm\nCustomer: How much are tickets for that time?\nAgent: Tickets are $10.\nCustomer: Are there any tickets avalible for Star wars at 6:35?\nAgent: There are no more tickets available.\nCustomer: Are there any tickets for 1917?\nAgent: No, im sorry there are no tickets for 1917.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q453174afa8",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThe transmission rate of undocumented infections per person was 55% the transmission rate of documented infections (95% CI: 46-62%), yet, because of their greater numbers, undocumented infections were the source of 79% of the documented cases.\n\nClaim: Undocumented cases of COVID-19 have never been a significant factor in its transmission.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q0f2d12903f",
  "kind": "yes/no",
  "text": "Complaint narrative: I WAS PULLING OUT OF A PARKING SPACE WHERE MY FRONT WAS UP AGAINST A BUILDING WITH A CAR ON EITHER SIDE OF ME. I REVERSED FOR ABOUT 25' WHERE A TELEPHONE POLE MANDATED THAT I MAKE A K-TURN TO GET OUT. AS I SWITCHED FROM REVERSE TO FORWARD, I SAW A SPARK AS THE CAR JET-PROPELLED FORWARD. I TRIED TO BREAK MULTIPLE TIMES, BUT THE CAR ACCELERATED THE 25' INTO THE WALL. ALL AIRBAGS DEPLOYED, AND FLUID GUSHED OUT OF THE FRONT END. THE CAR WAS DECLARED A TOTAL LOSS. I WAS TOLD BY TOYOTA AND MY INSURANCE COMPANY THAT I MUST HAVE ACCIDENTALLY ACCELERATED INSTEAD OF REPEATEDLY BREAKING. I AM GRATEFUL THAT I HIT A WALL INSTEAD OF PEOPLE. SOMEONE COULD EASILY HAVE DIED HAD I HAD SWITCHED FROM REVERSE GEAR TO FORWARD IN LESS CONFINED LOCATION. THE ENTIRE ACCIDENT LASTED 2 SECONDS, WITH NO OPPORTUNITY TO PULL THE EMERGENCY BREAK OR GO INTO NEUTRAL. PS: I AM A HAPPILY MARRIED DOCTOR WITH BEAUTIFUL CHILDREN AND GRANDCHILDREN, AND NOT AT ALL SUICIDAL. THIS THREE MONTH OLD 2015 PRIUS 3 FAILED BEFORE THE FIRST OIL CHANGE. I AM NOT SATISFIED WITH THE RESULTS.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q7cf9e02475",
  "kind": "yes/no",
  "text": "Complaint narrative: THE RUST CORROSION IS SO BAD THAT THE SPARE TIRE FELL OFF HITTING THE LEAF SPRING SUPPORT BRACKET AND COMPLETELY CAUSED THE BUMPER TO FALL OFF THE TRUCK. THE SPARE TIRE ROLLED INTO ONCOMING TRAFFIC AND ALMOST CAUSED AN ACCIDENT. THE CORROSION IS EVIDENT ALL OVER THE CHASSIS AND OTHER PARTS. THIS HAPPENED WHILE I WAS DRIVING AND PULLING A LANDSCAPE TRAILER ON ROUTE 173 IN NEW JERSEY.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q4ae8a72e50",
  "kind": "yes/no",
  "text": "When asked directly by ABC News in October if taxpayers should worry about the more than $500 million in federal funds on the line, Henrik Fisker was emphatic: \"No, I don't think they need to worry about it.\" When asked if Fisker might be the next Solyndra, he said, \"Absolutely not.\"",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q1ace604e0b",
  "kind": "yes/no",
  "text": "Customer: I am also looking for a place to stay in the east in the expensive price range.\nAssistant: I have one listing for express by holiday inn cambridge, is that okay for you?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q92aa2b640e",
  "kind": "yes/no",
  "text": "Occupation: Roof Bolters, Mining\nDuties:\n- Control conveyors that run the entire length of shuttle cars to distribute loads as loading progresses.\n- Monitor loading processes to ensure that materials are loaded according to specifications.\n- Replace hydraulic hoses, headlight bulbs, and gathering-arm teeth.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q9b3239fa2a",
  "kind": "yes/no",
  "text": "Customer: Hello, I would like to tickets at the movie theaters at Davis, California\nAgent: No problem. Do you have a movie in mind?\nCustomer: Well, my first option is No Time To Die.\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: There is not any showtime for it at Davis, California?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: Oh! I really wanted to watch that movie!. Is there any action movie playing in Davis, California?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: I that the sequel for the original movie from the 1970s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: Well, I'm sorry for wasting your time, but I really wanted to watch No Time To Die and since there is not any showing at Davis, California. I'm going to pass. Thanks for your help.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q9169a6922f",
  "kind": "yes/no",
  "text": "Statement 1: birds' milk is nutrient\nStatement 2: goats' milk is nutrient",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q42e4bbf5e6",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nIn a closed, stagnant air environment, they disappear from the window of view with time constants in the range of 8 to 14 min, which corresponds to droplet nuclei of ca.\n\nClaim: Ordinary speech can emit small respiratory droplets that linger in the air for at least eight minutes and potentially much longer, according to a study published Wednesday.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q68e79bbf24",
  "kind": "yes/no",
  "text": "Customer: I am looking for a cheap place to stay in the east part of town.\nAssistant: No problem. We have 3 guesthouses that match that. Do you have a further preference?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qae276e735e",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nConclusion and Relevance: Among patients with severe or life-threatening COVID-19, convalescent plasma therapy added to standard treatment, compared with standard treatment alone, did not result in a statistically significant improvement in time to clinical improvement within 28 days.\n\nClaim: COVID-19 patients treated with convalescent plasma recover at faster rates than those without treatment.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qdcdbb0afb9",
  "kind": "yes/no",
  "text": "Customer: HELLO\nAgent: Hello, How may I help you Today?\nCustomer: I need to catch a movie\nAgent: Ok,what is you location?\nCustomer: I'm in Sacramento, California\nAgent: Great, any specific genre\nCustomer: yeah, I prefer action or Thriller movies\nAgent: Do you have a specific movie?\nCustomer: Not really, can you recommend\nAgent: sure, you can either watch Angel has Fallen or five feet Apart will be screening at 6:00pm in The Tower Theatre\nCustomer: ok, which one is more thrilling\nAgent: Angel has fallen is quite captivating\nCustomer: Great\nAgent: Do you have any other concern?\nCustomer: yeah, how much are the tickets for two people ?\nAgent: 24\nCustomer: great\nAgent: can I book them for you?\nCustomer: No, will buy them later. Thank you\nAgent: You welcome, have a great time at the show.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q0fb7686031",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- William D. Casey\n- Casey was born in Amherst, Nova Scotia.\n- He was first elected, as a member of the Progressive Conservative Party of Canada, to represent the riding of Cumberland—Colchester in the 1988 election.\n- In common with almost every other PC Member of Parliament (MP) in the 1993 election he lost his seat, in his case being defeated by Liberal candidate Dianne Brushett.\n\nSummary sentence:\nWilliam D. Casey (born February 19, 1945) is a Canadian politician from Nova Scotia who served as a Member of Parliament (MP) in the House of Commons of Canada.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q59c2d6c249",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Amy Lysle Smart\n- Smart was born in Los Angeles, California, and raised in Topanga Canyon.\n- Also in 2005, she starred as Sarah in the British independent film \"The Best Man\" with Seth Green.\n\nSummary sentence:\nAmy Lysle Smart (born March 26, 1976) is an American actress.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q496ef40c3c",
  "kind": "yes/no",
  "text": "Situation: Subject of Uncle Being Gay Never Came Up With Nephew\nAction being judged: Not prying into people's personal lives.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q26c304af81",
  "kind": "yes/no",
  "text": "Assistant: Okay it looks like they are out of pineapple right now?\nCustomer: You better be joking lol.\nAssistant: No i'm actually being serious they dont have any pineapple right now.",
  "question": "According to the assistant's last message, is \"pineapple\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qcab80e0aa0",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nRates of ventilation in the HC, HC+AZ, and no HC groups were 13.3%, 6.9%, 14.1%, respectively. The risk of ventilation was similar in the HC group (adjusted hazard ratio, 1.43; 95% CI, 0.53 to 3.79; P=0.48) and in the HC+AZ group (adjusted hazard ratio, 0.43; 95% CI, 0.16 to 1.12; P=0.09), compared to the no HC group. CONCLUSIONS: In this study, we found no evidence that use of hydroxychloroquine, either with or without azithromycin, reduced the risk of mechanical ventilation in patients hospitalized with Covid-19.\n\nClaim: Hydroxychloroquine does not help patients avoid being placed on a ventilator.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qc0fd543899",
  "kind": "yes/no",
  "text": "Situation: I’ve stolen over $400 from my school.\nAction being judged: Making everyone's life poorer by taking what's not yours.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qa897c74b9d",
  "kind": "yes/no",
  "text": "Earlier today, I was wondering if the motivation was to get more Hollywood glamour in their lives. The old world glamour of royalty, heavy crystal, and gowns must be getting old, but this is the political cynic in me speaking.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q4747996fed",
  "kind": "yes/no",
  "text": "Assistant: Okay, what is the make, model and year of your car?\nCustomer: It is a Hyundai Elantra 2010.\nAssistant: Okay, I have booked you for 6 pm tonight for your Hyundai Elantra 2010..",
  "question": "According to the assistant's last message, is \"Hyundai Elantra\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q25ae266d68",
  "kind": "yes/no",
  "text": "Customer: Thanks! Can you also see if there are any expensive, 4-star guesthouses in the north area of town?\nAssistant: What you are looking for can not be found. Is there any other area you would mind searching in?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qc02df4562e",
  "kind": "yes/no",
  "text": "Occupation: Fashion Designers\nDuties:\n- Adapt other designers' ideas for the mass market.\n- Purchase new or used clothing and accessory items as needed to complete designs.\n- Sketch rough and detailed drawings of apparel or accessories, and write specifications such as color schemes, construction, material types, and accessory requirements.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q6c5bade45c",
  "kind": "yes/no",
  "text": "Complaint narrative: THE HEADLIGHTS ON MY 2018 HYUNDAI SONATA SHOW TWO BLACK NOTCHES AND A BLACK LINE ABOUT 30 FEET IN FRONT OF THE CAR IN LOW LIGHT CONDITIONS. IT IS VERY DISTRACTING AND DANGEROUS AS THESE SHADOWS DART ACROSS YOUR PATH AS YOU MAKE TURNS OR GO UP HILLS. HYUNDAI SERVICE COULD SEE THE NOTCHES, BUT SAID \"THE SYSTEM IS WORKING WITHIN SPECIFICATIONS AT THIS TIME\". SOMETHING NEEDS TO BE DONE BEFORE SOMEONE IS KILLED BECAUSE OF THESE UNSAFE LIGHTS.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qa0b30cfca0",
  "kind": "yes/no",
  "text": "Customer: Hey, I'd like to see a movie\nAgent: Okay, what type of movie do you want to see?\nCustomer: I was thinking of a horror movie?\nAgent: Okay, I found Shuttered - Horror - rated R - Rotten Tomatoes 61% - Sarah Decker moves upstate from her New York City lifestyle to work on her distant cousin’s haunted marijuana farm.\nCustomer: On second thought, I was more in the mood for a romantic comedy.\nAgent: Okay, I found Family Jewels - Romantic Comedy - rated R - Rotten Tomatoes 69% - A famous diamond dealer leaves his European life in Antwerp to pursue a less than genuine romance with an American con artist- Stars Melissa McCarthy and Ryan Reynolds.\nCustomer: Yeah, let's go with Family Jewels\nAgent: Okay, when would you like to see it?\nCustomer: Friday\nAgent: And how many tickets?\nCustomer: 2 please\nAgent: And at what time?\nCustomer: Sometime in evening\nAgent: And where are you located?\nCustomer: Spring Hills Kansas\nAgent: Okay, I found two tickets for Family Jewels on Friday at 8:10 pm at AMC Holiday Theater, does that sound good?\nCustomer: Yes, that's great\nAgent: Anything else I can help with\nCustomer: No, I'm good thanks.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qb3b94d1ae2",
  "kind": "yes/no",
  "text": "Assistant: Great! Give me a few seconds to book your appointment.\nCustomer: Thank you!\nAssistant: Already! You're all set. I have booked an appointment for you at 10:30 in the morning. If the service is not covered, there will be a minimum fee for this service.",
  "question": "According to the assistant's last message, is \"10:30 in the morning\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfe0bd8d73e",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNED A 2004 CHEVROLET MONTE CARLO. WHILE THE VEHICLE WAS PARKED IN THE GARAGE, THE CONTACT NOTICED THAT THE GARAGE WAS ON FIRE. THE FIRE DEPARTMENT EXTINGUISHED THE FIRE. A FIRE REPORT WAS FILED. THE VEHICLE WAS DESTROYED. THE VIN WAS INCLUDED IN NHTSA CAMPAIGN NUMBER: 15V201000 (ENGINE, ENGINE COOLING). THE MANUFACTURER WAS NOT NOTIFIED OF THE FAILURE. THE APPROXIMATE FAILURE MILEAGE WAS 138,000.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q5195e708a2",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNED A 2007 DODGE CHARGER. WHILE THE VEHICLE WAS PARKED, SMOKE EMITTED FROM THE FRONT PASSENGER SIDE WHEEL. THE VEHICLE LATER CAUGHT FIRE. A FIRE REPORT WAS FILED AND THE FIRE DEPARTMENT EXTINGUISHED THE FIRE. THE CONTACT DID NOT SUSTAIN ANY INJURIES. THE VEHICLE WAS DESTROYED. THE MANUFACTURER WAS NOT NOTIFIED OF THE FAILURE. THE FAILURE MILEAGE WAS 240,000. UPDATED 08/31/16*LJ",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qfe35ebd600",
  "kind": "yes/no",
  "text": "Customer: I need to buy movie tickets for theaters in Davis, California, please.\nAgent: No problem. Do you have a movie in mind?\nCustomer: I heard 'No Time To Die' is awesome, so let's try that movie.\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: Can you please check if it's not showing in Davis, California?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: That's unfortunate. What movies are being shown in Davis?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Is that the original movie from the 1970s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: I'm sorry, that's not the movie I was hoping to watch so I would rather not purchase tickets at this time.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q9fc0e8bef7",
  "kind": "yes/no",
  "text": "Table caption: Reasons teens were unwilling or uncertain about allowing researchers to contact their parents for consent purposes ( N = 166).\n| Theme | N (%) | Example responses |\n| Teen privacy | 55 (33) | ● “They don't know about my problem and I want to keep it that way.” ● “I'm not open about my issues with my parents” |\n| Parents lack an understanding of mental health or are unaware of the problem | 38 (23) | ● “I am not sure they would approve, seeing as they don't necessarily believe in mental health problems. Also, mental health is stigmatized in my family.” ● “They don't know about my eating disorder” |\n| Teen is concerned about parents' reaction/response | 34 (20) | ● “I don't want them to worry more about me” ● “They would be concerned/annoyed that I've never talked to them about this before” |\n| Teen autonomy | 26 (16) | ● “I do not like or trust my parents and I don't want them involved in this” ● “I feel old enough to make my own decisions about apps I'd like to try out” |\n| Poor parent-teen relationship | 17 (10) | ● “My family would never let me get help. A lot of parents don't care about whether their kid is hurting or not. This won't work if you make people tell their families. It just won't”. ● “My parents can be judgmental at some points so I don't want them to tell me something about wanting to try something new”. |\n| Parent would not want the teen to participate in research | 13 (8) | ● “They might think it's a scam and say no” ● “My parents might not be open to me participating in such a study or understanding of how I might benefit from such an app” |\n| Fears about online security/privacy | 3 (2) | ● “I am not sure that this survey is really trustworthy or that they would want me taking it” ● “I do not know what kind of information they will be collecting, so I am undecided” |\n\nStatement: Fears about online security/privacy has the least N (%) value of 3 (2).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8323a5ae38",
  "kind": "yes/no",
  "text": "Statement 1: A Canary is a bird\nStatement 2: All birds are Canaries",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q022eedf726",
  "kind": "yes/no",
  "text": "Assistant: No other movie tickets ordered.\nCustomer: Thank you\nAssistant: You're welcome. Tickets for Aquaman 7:00pm showing at Lowes Boston Common are ordered. Cost is $17.99. Receipt is texted to you.",
  "question": "According to the assistant's last message, is \"Lowes Boston Common\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q459702d22b",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Bachchan's first release of 2005 was the crime comedy \"Bunty Aur Babli\", which featured him and Rani Mukerji as the titular con artist duo who perform several successful heists and fall in love along the way.\n- His next two releases \"Dus\" (2005) and \"Bluffmaster!\"\n- (2005) were both moderately successful, but did not earn much critical appreciation.\n- Bachchan earned much critical acclaim for his performance in Mani Ratnam's \"Guru\" (2007), loosely based on the life of business magnate Dhirubhai Ambani.\"\n- His next release was the dance comedy \"Jhoom Barabar Jhoom\" (2007) alongside Preity Zinta, Bobby Deol, and Lara Dutta.\n- Bachchan's first release of 2008 was Ram Gopal Varma's \"Sarkar Raj\", which featured him and his father Amitabh Bachchan reprising their roles from \"Sarkar\" (2005) while his wife Aishwarya Rai Bachchan entered the cast as a new addition.\n- This film proved to be successful at the box office and earned him a nomination for the Filmfare Award for Best Supporting Actor.\n- Bachchan was next seen in \"Dostana\" (2008), a romantic comedy about two men (Bachchan and John Abraham) who pretend to be gay in order to be allowed to live with a girl (Priyanka Chopra), but then find that they have both fallen in love with her.\n- These films were the thriller \"Raavan\" (2010), the social drama \"Khelein Hum Jee Jaan Sey\" (2010), action thrillers \"Game\" (2011), \"Dum Maaro Dum\" (2011) & the heist thriller \"Players\" (2012).\n- Bachchan then played the lead role in Rohit Shetty's comedy \"Bol Bachchan\" (2012), which was a major blockbuster at the box office despite receiving mixed reviews from critics.\n- Bachchan was next seen in Farah Khan's dance comedy \"Happy New Year\", a musical heist film, playing the second lead to Shah Rukh Khan.\n- Bachchan's first release of 2016 was the comedy \"Housefull 3\", the third installment of the Housefull film series.\n\nSummary sentence:\nBachchan has also played leading and supporting roles in commercially successful comedies and dramas, including \"Bunty Aur Babli\" (2005), \"Dus\" (2005), \"Bluffmaster!\" (2005), \"Guru\" (2007), \"Jhoom Barabar Jhoom\" (2007), \"Sarkar Raj\" (2008), \"Dostana\" (2008), \"Dum Maaro Dum\" (2011), \"Bol Bachchan\" (2012), \"Happy New Year\" (2014) and \"Housefull 3\" (2016).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q782cae6a4c",
  "kind": "yes/no",
  "text": "Statement 1: he often plays basketball with me, he hopes me to be \"Yao Ming\"\nStatement 2: he often plays guns with me, he hopes me to be \"Yao Ming\"",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qec7151cb6f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Among other theatre schools and companies, the Dramatic Workshop played a vital role in paving the way for Off-Broadway theatre.\n\nSummary sentence:\nThe Dramatic Workshop considerably contributed to the resurgence of the Off-Broadway theatre.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q3a678a055c",
  "kind": "yes/no",
  "text": "Table caption: The number of views depending on the rating.\n| responses_rating_grade | views |\n| 1.0 | 1192.8 |\n| 2.0 | 1278.9 |\n| 3.0 | 1391.4 |\n| 4.0 | 1169.8 |\n| 5.0 | 990 |\n\nStatement: Rating grade 3.0 having more views.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q98789aae26",
  "kind": "yes/no",
  "text": "Customer: I would love to find an action move to watch tonight with my wife since it's my turn to pick.\nAgent: Sounds like so much fun. There are a number of action movies out there. Would you like me to list those out.\nCustomer: Yes, that would be great.\nAgent: There is Star Wars: Rise of Skywalker, Jumanji: The Next Level, Spies in Disguise, Ford v Ferrari, and 21 Bridges.\nCustomer: That sounds like a lot of choice. Can you narrow it down to those that are R rated and geared towards adults only?\nAgent: No problem. It turns out that is easy as 21 Bridges is the only R rated film in that group.\nCustomer: Can you tell me any more about the movie?\nAgent: Absolutely! It stars Chadwick Boseman and the synopsis states: An NYPD detective searches for two cop killers as authorities close all of Manhattan's 21 bridges.\nCustomer: Wow! It sounds really interesting and fits my desire for action and my wife's love of police related shows. Is it playing in Omaha, Nebraska?\nAgent: It looks like it has a fairly limited release, but is playing at two theaters this evening in or near Omaha.\nCustomer: Could you list those two theaters?\nAgent: AMC COUNCIL BLUFFS 17 and AMC OAKVIEW PLAZA 24.\nCustomer: Those are both about the same distance from my home. Could you tell me the next available time for the showing at AMC OAKVIEW PLAZA 24?\nAgent: Sure thing, but first, do you have any preferred viewing experiences?\nCustomer: I actually am fine with Standard.\nAgent: Thank you. It looks like there is a Standard showing at 5:25.\nCustomer: I think that actually works pretty well, though I know it's not two far away.\nAgent: You mentioned earlier that you would only be needing two tickets?\nCustomer: Yes, just me and my wife.\nAgent: Great. I show you are interested in two tickets for 21 Bridges at AMC OAKVIEW PLAZA 24 for the 5:25 PM.\nCustomer: That is correct.\nAgent: Would you like me to complete your purchase now?\nCustomer: Actually, I think I want to hold off until I talk with my wife. We may purchase at the theater though.\nAgent: Makes sense. Is there anything else I can help with.\nCustomer: No, but thanks for your help and making my movie decision easier!\nAgent: Absolutely and I hope you enjoy your movie!",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q1bfdd2f542",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThis study confirms that serum and saliva IgG antibodies to SARS-CoV-2 are maintained in the majority of COVID-19 patients for at least 3 months PSO. IgG responses in saliva may serve as a surrogate measure of systemic immunity to SARS-CoV-2 based on their correlation with serum IgG responses.\n\nClaim: And a study of Covid-19 patients found that antibody levels in saliva and blood were closely matched.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q602168fcd8",
  "kind": "yes/no",
  "text": "Statement 1: your advice has helped me get along well with my pencils\nStatement 2: your advice has helped me get along well with my classmates",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q53140688cc",
  "kind": "yes/no",
  "text": "Assistant: would you like anything else?\nCustomer: no, that is all I wanted.\nAssistant: ok, I have placed an the order for the venti whole milk caffe mocha at starbucks down the street",
  "question": "According to the assistant's last message, is \"whole milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2d44f87a8d",
  "kind": "yes/no",
  "text": "Situation: I broke up with a girl because of her name\nAction being judged: Breaking up with someone because of their name.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q9e171aba96",
  "kind": "yes/no",
  "text": "Situation: He told his dad he didn't want to hunt quail.\nAction being judged: Saying no to doing something you aren't comfortable with.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q3afe6db676",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nHence, COVID-19 patients can develop psychotic symptoms as a consequence of multiple concurrent factors.\n\nClaim: There are no new-onset psychosis-related symptoms developed as a result of COVID-19.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q403f2ca40c",
  "kind": "yes/no",
  "text": "Assistant: What kind of vehicle would you like.\nCustomer: Sedan.\nAssistant: There is no sedan available around that time.",
  "question": "According to the assistant's last message, is \"sedan\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf47cf062d0",
  "kind": "yes/no",
  "text": "Assistant: How many do you need at your table?\nCustomer: Just two it's a romantic date.\nAssistant: I have you set up for a table for two tonight at Malone's at 8 p.m.",
  "question": "According to the assistant's last message, is \"Malone's\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf7646a8bd8",
  "kind": "yes/no",
  "text": "Complaint narrative: TAKATA RECALL. I HAVE A NOTICE THAT A RECALL IS ACTIVE ON MY VEHICLE. I CALLED THE DEALER TO HAVE IT RESOLVED AND THEY SAY THAT THERE ARE NO PARTS TO MAKE THE REPAIRS AND HAVE NO IDEA WHEN ANY WILL BE AVAILABLE. THE RECALL STATES THAT IF I AM IN A COLLISION AND MY PASSENGER AIR BAG DEPLOYS, THAT MY PASSENGER CAN RECEIVE INJURY OR EVEN DEATH FROM FLYING PIECES OF METAL. HOW IN THE WORLD CAN WE BE ALLOWED TO DRIVE AROUND IN THESE POSSIBLE DEATH MACHINES AND NOBODY SEEMS TO BE DOING ANYHTING ABOUT IT.?????",
  "question": "Does this vehicle safety complaint report that at least one person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q9eb7ee89c4",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In February 2005, Bagwell and Biggio were jointly inducted into the Texas Sports Hall of Fame.\n- Bagwell was eligible for induction into the Baseball Hall of Fame for the first time in 2011.\n- On January 18, 2017, Bagwell was voted into the Hall of Fame with 86.2% of the vote in his seventh year of eligibility.\n\nSummary sentence:\nHe was elected to the Texas Sports Hall of Fame in 2005 and to the Baseball Hall of Fame in 2017.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q7e79015501",
  "kind": "yes/no",
  "text": "Complaint narrative: BOUGHT VEHICLE 2 YEARS AGO, HEADLIGHTS HAVE GOTTEN DIMMER TO THE POINT CAR IS UNSAFE TO DRIVE AT NIGHT. BROUGHT CAR INTO DEALERSHIP AND THEY ARE IN AGREEMENT THE HEADLIGHTS NEED TO BE REPLACED. SAFETY ISSUE. HIGH BEAMS ARE NECESSARY TO DRIVE AFTER DUSK.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q958e5b580f",
  "kind": "yes/no",
  "text": "Just the opposite is demanded in the dead of winter when there is no sun and when the wind dies down. During the week, energy demand soars and their is often not enough supply to meet the demand. And because many power companies are finding it unprofitable to run conventional systems part-time, many are simply mothballing such plants completely, thus making supply even rarer. As a result, the risk of blackouts is becoming a real increasing threat in Germany with each coming winter.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q4f4032bc2d",
  "kind": "yes/no",
  "text": "Complaint narrative: HAVE A SLIGHT MISFIRE AND CALLED ALL MY LOCAL SHOPS AND NO SHOP WILL CHANGE THE PLUGS ON A F-150 WITH A 5.4L TRITON MOTOR. THEY SAID IT'S WELL KNOWN THAT ALL THE SPARK PLUGS WILL SNAP OFF IN THE BLOCK. I CALLED THE DEALER AND THEY WANT $1000 TO CHANGE THEM. WHILE IN ALL OTHER CARS AND TRUCKS IT'S $50-$100 JOB. RESEARCHING THIS ONLINE IT SEEMS THIS HAPPENS TO EVERY FORD THAT HAD THE 5.4L TRITON ENGINE. WHY IS THERE NO RECALL? I CAN'T AFFORD $1000 TO CHANGE MY SPARK PLUGS. I'M A SMALL BUSINESS OWNER AND THIS IS BEYOND MY MEANS CURRENTLY. I EMAILED FORD AND THEY DIDN'T SEEM TO ACKNOWLEDGE IT BEING A KNOWN ISSUE. YET EVERY MECHANIC SHOP WILL AND THERE ARE THOUSANDS OF CASES OF THIS ISSUE ALL OVER THE INTERNET.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 }
]
