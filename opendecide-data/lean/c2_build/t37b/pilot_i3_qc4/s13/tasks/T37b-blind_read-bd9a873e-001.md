# T37b blind solver T37b-blind_read-bd9a873e-001 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3_qc4/s13/answers/T37b-blind_read-bd9a873e-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q8aab379629",
  "kind": "yes/no",
  "text": "Statement 1: getting home after a happy date, he opened the door and invited his girlfriend in\nStatement 2: getting home after a happy date,he closed the door leaving his girlfriend outside",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qb7cf0588cf",
  "kind": "yes/no",
  "text": "Assistant: Ok, so UberX is 26.57 in estimated fare. Is this OK for you?\nCustomer: yes.\nAssistant: Ok, ordering your ride right now. Found your ride, your ride will arrive in 7 minutes from now.",
  "question": "Is \"7 minutes\" for the customer's ride booking confirmed in the final message from the assistant?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe20edb7d95",
  "kind": "yes/no",
  "text": "Sen. Dianne Feinstein (D-Calif.) said she is \"committed\" to keeping a $400 million program that reimburses states for jailing illegal immigrants, a task she called \"a total federal responsibility.\"",
  "question": "Does the paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q9580096048",
  "kind": "yes/no",
  "text": "Situation: He paid all his deposits and his parents helped him move his stuff.\nAction being judged: Paying all your deposits before moving somewhere.",
  "question": "Is it the case that the action being judged isn't wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qa3ba895317",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nWe found that SARS-CoV-2 replicates poorly in dogs, pigs, chickens, and ducks, but efficiently in ferrets and cats. We found that the virus transmits in cats via respiratory droplets.\n\nClaim: The novel coronavirus can be transmitted by respiratory droplets in cats.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qbd2a6e8c67",
  "kind": "yes/no",
  "text": "Situation: Ana was moving out into a home of her own.\nAction being judged: Children moving out of the family home when they become adults.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q151b2abdf9",
  "kind": "yes/no",
  "text": "Occupation: Pediatric Surgeons\nDuties:\n- Perform transplantation operations, such as organ transplants, on fetuses, infants, children, and adolescents.\n- Examine fetuses, infants, children, and adolescents, and diagnose health issues to determine need for intervention, such as surgery.\n- Operate on fetuses, infants, children, and adolescents to correct deformities, repair injuries, prevent and treat diseases, or improve or restore patients' functions.",
  "question": "So, are the duties on the list part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q11920da54c",
  "kind": "yes/no",
  "text": "Assistant: Unfortunately, there is nothing available for 6:30 pm\nCustomer: Ok, how about 8:00 pm?\nAssistant: There is a showing for 8:00 pm, but it's in 35mm, not 3D",
  "question": "Is \"3D\" confirmed for the customer's movie ticket order, as the assistant's final message says?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd40daf4acd",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nObjective To investigate the efficacy and safety of recombinant human interferon alpha1b (rhIFN-α) nasal drops in healthy medical staff to prevent 2019 novel coronavirus disease (COVID-19). Conclusion In this investigator-initiated open-label study, we observed that rhIFN-α nasal drops can effectively prevent COVID-19 in treated medical personnel.\n\nClaim: In China, the early results of a study among medical workers were disappointing, concluding that interferon nasal drops “were ineffective at preventing Covid-19 in medical staff.”",
  "question": "Does the evidence back up the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q8c8a23c0f9",
  "kind": "yes/no",
  "text": "Situation: Only when my wife and family are out of town do I leave the toilet seat up\nAction being judged: Leaving the toilet seat up if nobody else is home.",
  "question": "Is the action judged acceptable by common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qeea2618d5f",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nConclusions The population prevalence of SARS-CoV-2 antibodies in Santa Clara County implies that the infection is much more widespread than indicated by the number of confirmed cases.\n\nClaim: The actual infection rate in Santa Clara County was greater than the rate of confirmed cases.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q35fbfeb59e",
  "kind": "yes/no",
  "text": "Statement 1: You are likely to find a dolphin in sea.\nStatement 2: You are likely to find a dolphin in a pond.",
  "question": "Of these two statements, does Statement 1 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q3d06442357",
  "kind": "yes/no",
  "text": "Situation: I desperately want to leave my husband, but I can’t.\nAction being judged: Staying with someone you don't care about.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qe009d74373",
  "kind": "yes/no",
  "text": "Customer: I would like to make a reservation for this Saturday for 2 people for  4 nights please.\nAssistant: I have booked you and another person for this Saturday for 4 nights.",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "q33032b70d4",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2007 BMW 328I. WHILE DRIVING 65 MPH, THE CHECK ENGINE WARNING INDICATOR ILLUMINATED. IN ADDITION, WHILE THE VEHICLE WAS PARKED IN THE CONTACT'S DRIVEWAY, A LOUD ABNORMAL SOUND WAS HEARD AND THE CONTACT NOTICED FLAMES AROUND THE ENGINE COMPARTMENT. THE FIRE DEPARTMENT EXTINGUISHED THE FIRE AND FILED A REPORT. THERE WERE NO INJURIES. THE FAILURE MILEAGE WAS 130,000.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q66be46dfa5",
  "kind": "yes/no",
  "text": "Ref: Letter to NASA Administrator Charles Bolden, dated 3-26-12, regarding a request for NASA to refrain from making unsubstantiated claims that human produced CO2 is having a catastrophic impact on climate change.",
  "question": "Based on the text, does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q6a06f6360b",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThe odds that a primary case transmitted COVID-19 in a closed environment was 18.7 times greater compared to an open-air environment (95% confidence interval [CI]: 6.0, 57.9).\n\nClaim: The odds of catching the coronavirus are about 20 times higher indoors than outdoors.",
  "question": "According to the evidence, does it support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qeecdf5115f",
  "kind": "yes/no",
  "text": "Table caption: Summary of data formats, sources, contents, and suggested restore utility.\n| Format | Tweets | Users | Import utility |\n| JSON | ✔ | ✔ | mongoimport |\n| BSON | ✔ | ✔ | mongorestore |\n| CSV | ✔ | ✘ | mongoimport |\n\nStatement: There are three different formats.",
  "question": "Based on the table, is the statement supported?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8787167d95",
  "kind": "yes/no",
  "text": "Complaint narrative: I WAS DRIVING HOME FROM WORK. GOT. REARENDED I HIT THE CAR IN FRONT OF ME. I WAS STOPPED AT A LIGHT. THE AIRBAG DID NOT DEPLOY. I SUFFERED A HEAD INJURY. BROKEN SPINE. CAR WAS DESTROYED ONLY THING LEFT WAS WERE I WAS SITTING. AND THE PASSENGER SEAT. NOW NISSAN MURANO 2005 HAS FAULTY AIRBAG TOO. LIGHT ON AND FLASHING. VEHICLE. RENDERED UNSAFE TO OPERATE VEHICLE. NISSAN HAS ONGOING PROBLEMS WITH THEIR AIRBAGS AND WONT HELP CONSUMERS FIX THE PROBLEMS.",
  "question": "Does this vehicle safety complaint say that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q245b77cd41",
  "kind": "yes/no",
  "text": "Situation: Her mom took her there thinking they wouldn't find one.\nAction being judged: Going back on your promises to your children just because you didn't think you'd find what they were looking for.",
  "question": "Is it true that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qe2ec5e1191",
  "kind": "yes/no",
  "text": "Customer: Hi! I'd like to go to the movies tonight.\nAgent: OK. Do you have anything in mind?\nCustomer: No. Not really.\nAgent: Sure. And what city are you looking in?\nCustomer: I'm in Brando, Texas!\nAgent: Brando, Texas. Got it. And is there a particular type of movie you’d like to see?\nCustomer: What's playing?\nAgent: A few titles playing in your area are No Time To Die, Mulan, and Stella’s House.\nCustomer: I've heard Stella's House is good! Who's the director?\nAgent: The director of Stella’s House is Clyde Stewart.\nCustomer: Oh, I love his movies. When are the show times?\nAgent: OK. Stella’s House is playing at the Milford Theater. Showtimes are 4:40pm, 7:10pm, and 9:30pm. Which one would you prefer?\nCustomer: Oh wait! I forgot I have plans tonight. Tomorrow is open though!\nAgent: No problem. Let me check the showtimes for tomorrow.\nAgent: OK. The showtimes for tomorrow are the same. Which one should I book?\nCustomer: What was the latest one again?\nAgent: Sure. The last showing is 9:30pm.\nCustomer: That sounds great!\nAgent: All right. Let me confirm. You’d like 4 tickets for the 9:30pm showing of Stella’s House at Milford Theater tomorrow. Is that all correct?\nCustomer: That's right!\nAgent: Is it OK to go ahead and purchase these tickets?\nCustomer: Yes!\nAgent: OK. Your tickets are purchased and details for how to proceed have been sent to your email address. Can I help with anything else?\nCustomer: No thanks!\nAgent: OK. Enjoy your movie!",
  "question": "Based on the text, by the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q0a989d28e5",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThe COVID-19 epidemic is believed to have started in late January 2020 in France. Here we report a case of a patient hospitalised in December 2019 in an intensive care unit in a hospital in the north of Paris for haemoptysis with no aetiological diagnosis. RT-PCR was performed retrospectively on the stored respiratory sample and confirmed the diagnosis of severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) infection.\n\nClaim: The French government ordered a lockdown on March 16, well in advance of the coronavirus's appearance in France, according to a study of the new case that has been peer-reviewed and accepted for formal publication in the International Journal of Antimicrobial Agents",
  "question": "Is the evidence in contradiction with the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qf3a1569e96",
  "kind": "yes/no",
  "text": "Assistant: That will be $5.00 exactly. I can charge that to your card.\nCustomer: Great!\nAssistant: Your drink is on order and will be ready for pick-up very soon at the Starbucks 14607 Memorial Dr Houston, TX location. Your receipt will be sent to your mobile device via text message.",
  "question": "Based on the text, is \"14607 Memorial Dr Houston, TX\" confirmed for the customer's coffee order in the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5854f04887",
  "kind": "yes/no",
  "text": "It is long past the time to have a real energy policy, one that works for America, not against it.",
  "question": "Does this paragraph put forward the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q46df46becd",
  "kind": "yes/no",
  "text": "Assistant: I will make that request for you.\nCustomer: Great.\nAssistant: Okay, I've made the reservation for 3 at Schmidt and Mccormick on S. Broad St., Philadelphia, PA for tomorrow at 8PM.",
  "question": "Referring to the assistant's final message, is \"S. Broad St., Philadelphia, PA\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7227d0b647",
  "kind": "yes/no",
  "text": "Table caption: Summary of previously reported cases of COVID-19-associated pulmonary aspergillosis.\n| Study | Country | CAPA* | Aspergillus species | Aspergillus species in culture | Serum or BAL GM positive | BAL Aspergillus PCR positive | Initial Antifungal Therapy | In-hospital mortality |\n| Alanio, 2020 [ ] | France | 9/27 | A. fumigatus (7/9) | 7/9 | 3/9 | 4/9 | VOR (1/9) CAS (1/9) None (7/9) | 4/9 |\n| Koehler, 2020 [ ] | Germany | 5/19 | A. fumigatus (5/5) | 3/5 | 4/5 | 4/5 | VOR (2/5) ISA (1/5) CAS (2/5) | 3/5 |\n| Rutsaert, 2020 [ ] | The Netherlands | 7/34 | A. fumigatus (5/7) A. flavus (1/7) | 6/7 | 6/7 | NR | VOR (4/7) VOR/ISA (2/7) None (1/7) | 4/7 |\n| Nasir, 2020 [ ] | Pakistan | 5/23 | A. flavus (3/5) A. niger (1/5) A. fumigatus and A. flavus (1/5) | 5/5 | 0/5 | NR | VOR (3/5) AmB-d (2/5) | 3/5 |\n| van Arkel, 2020 [ ] | The Netherlands | 6/31 | A. fumigatus (6/6) | 5/6 | 3/6 | NR | VOR plus AND (5/6) L-AmB (1/6) | 4/6 |\n| Blaize, 2020 [ ] | France | 1/1 | A. fumigatus | 1/1 | 0/1 | 1/1 | None | 1/1 |\n| Lahmer, 2020 [ ] | Germany | 2/2 | A. fumigatus (2/2) | 2/2 | 2/2 | NR | L-AmB (2/2) | 2/2 |\n| Wang, 2020 [ ] | China | 8/104 | A. fumigatus | 8/8 | NR | NR | NR | NR |\n| Antinori, 2020 [ ] | Italy | 1/1 | A. fumigatus | 1/1 | 1/1 | 1/1 | L-AmB | 1/1 |\n| Ferreira, 2020 [ ] | France | 1/1 | A. fumigatus | 1/1 | 0/1 | 1/1 | None | 1/1 |\n| Meijer, 2020 [ ] | France | 1/1 | A. fumigatus | 1/1 | 1/1 | NR | VOR plus CAS | 1/1 |\n| Prattes, 2020 [ ] | Austria | 1/1 | A. fumigatus | 1/1 | 0/1 | NR | VOR | 1/1 |\n| Sharma, 2020 [ ] | Australia | 1/1 | A. fumigatus | 1/1 | NR | NR | VOR | 0/1 |\nTable notes: *number with CAPA/total number in the report AmB-d, amphotericin b deoxycholate; AND, anidulafungin; BAL, bronchoalveolar lavage; CAPA, COVID-19-associated pulmonary aspergillosis; CAS, caspofungin; GM, galactomannan; ISA, isavuconazole; L-AmB, liposomal amphotericin; NR, not reported; VOR, voriconazole\n\nStatement: van Arkel, 2020 study had reported France 5/23 for CAPA",
  "question": "Is the assertion backed by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb45023e947",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nWe report the available safety, tolerability, and immunogenicity data from an ongoing placebo-controlled, observer-blinded dose escalation study among healthy adults, 18-55 years of age, randomized to receive 2 doses, separated by 21 days, of 10 g, 30 g, or 100 g of BNT162b1, a lipid nanoparticle-formulated, nucleoside-modified, mRNA vaccine that encodes trimerized SARS-CoV-2 spike glycoprotein RBD. Geometric mean neutralizing titers reached 1.8- to 2.8-fold that of a panel of COVID-19 convalescent human sera.\n\nClaim: An mRNA vaccine candidate BNT162b1 against COVID-19 produced little increase in SARS-CoV-2 neutralizing agents in a phase 1 study.",
  "question": "According to the text, does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q2d4637422e",
  "kind": "yes/no",
  "text": "Situation: I support Israel because I dislike Moslems\nAction being judged: Spreading misinformed opinions about matters that you're not involved in.",
  "question": "Is the action being judged permissible under common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q951d1b6394",
  "kind": "yes/no",
  "text": "Assistant: Okay.\nCustomer: That's inside correct?\nAssistant: Yes, oh sorry PF changs are all booked.",
  "question": "Going by the assistant's final message, is \"PF changs\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q38a49f12fb",
  "kind": "yes/no",
  "text": "It also said the panel had purposely emphasised the negative impacts of climate change and made \"substantive findings\" based on little proof.",
  "question": "Does the paragraph here make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q8d034257ba",
  "kind": "yes/no",
  "text": "Situation: She glared at him showing him the rules of the library.\nAction being judged: Making someone aware of rules.",
  "question": "Is it true that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q174b6ee09c",
  "kind": "yes/no",
  "text": "Situation: Wisdom of Age Teaches Man to Hold His Fire After Insult\nAction being judged: Apologizing when you say something hurtful.",
  "question": "Is it true that the action being judged is not acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q5e993aabf5",
  "kind": "yes/no",
  "text": "Statement 1: cows produce juice\nStatement 2: cows produce milk",
  "question": "Of these two statements, does Statement 1 make sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q30c4ce1cf7",
  "kind": "yes/no",
  "text": "Customer: I need to purchase three tickets to see Sonic The Hedgehog on Monday.\nAgent: Of course, which theater would you like to purchase tickets from?\nCustomer: What theater can you recommend for me in the city of Hutchinson?\nAgent: May I recommend B&B Hutchinson Mall 8, it is a nearby theater that will be showing your requested movie on Monday.\nCustomer: Thanks for the recommendation, I think I will go with that theater for my reservation.\nAgent: In that case, what movie time were you hoping to get for your ticket reservation?\nCustomer: I wanted to see a movie with my family at 4:00 pm, it would be best if it was a Enhanced screening by the way.\nAgent: I found one screening matching your description, would you like to select it for your reservation?\nCustomer: Of course, please select it and get two adult tickets and one child ticket.\nAgent: Your reservation is now for three movie tickets, two adults and one child. You may now proceed to select your seats for the reservation.\nCustomer: Select seats C1-C3 if they are available.\nAgent: Confirmed, those seats that you have requested are available and will be reserved for this reservation.\nCustomer: Oh wait, I just remembered, can I switch to a Digital screening instead? You can keep the other details of the reservation intact, just change the screening.\nAgent: Understood, your reservation will be for a digital screening instead. I was able to find a similar screening, and have selected seats C1-C3 for the reservation.\nCustomer: Great, can you tell me how much the total will be for the reservation?\nAgent: Of course, the two adult tickets will be $18.62, while the one child ticket will cost $7.99. All together with the convenience fee, the total will add up to $31.98.\nCustomer: Sounds fair enough, and just to be sure, can you repeat all the details of the reservation one more time?\nAgent: Your reservation will be for three movie tickets to see Sonic The Hedgehog this Monday, February 24 at B&B Theatres Hutchinson Mall 8. The reservation is specifically for two adult tickets and one child ticket, for a digital screening at 4:00 pm. The reservation will reserve seats C1-C3, and will come out to a total of $31.98, was that all correct?\nCustomer: All correct, please make the purchase with my American Express card, the one I have associated with my account.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "Have movie tickets actually been bought by the customer by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q5acc7a77f0",
  "kind": "yes/no",
  "text": "Using data from the Intergovernmental Panel on Climate Change (IPCC), a Science and Public Policy Institute paper published last month found that if the United States eliminated all carbon dioxide emissions, the overall impact on global temperature rise would be only 0.08 degrees Celsius by 2050.",
  "question": "Does this paragraph set forth the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q06b5b73068",
  "kind": "yes/no",
  "text": "Complaint narrative: 3 YR OLD CAR TRANSMISSION WENT OUT COMPLETELY WHILE I WAS DRIVING ON THE FREEWAY. I HAD TO DODGE SPEEDIG CARS TO ROLL OFF THE FREEWAY SINCE I HAD NO USE OF THE GAS PETAL OR SPEED. HAD TO HAVE IT TOWED. ERROR CODES P0732-GEAR 2 INCORRECT GEAR RATIO CAME BACK TO NEEDING A WHOLE NEW TRANSMISSION. HAD THEM FLUSH THE TRANSMISSION FOR $300 TO TRY AND SAVE IT TO NO AVAIL. THE SHIFTER CABLE IS ALREADY ON RECALL NOTICE 18S20/NHTSA RECALL 18V471 AND MY FORD DEALER CANT GET THE PART FOR MONTHS NOW BECAUSE ITS ON BACK ORDER. I BELIEVE THIS LED TO THE TOTAL DEMISE OF THE TRANSMISSION. A USED PART FOR $3000 IS NOT AN OPTION BECAUSE THE DEALERS CANT FIND ONE ANYWHERE. IM ASSUMING ITS DUE TO MANY PEOPLE HAVING THIS SAME ISSUE. MY ONLY OPTIONS ARE SPENDING $5400 ON A NEW TRANSMISSION OR GETTIG RID OF THE CAR THAT I STILL OWE MONEY ON TO SOMEONE WHO MAY SCRAP IT. NO SAFETY RECALL PARTS ARE AVAILABLE STILL AFTER MONTHS AND NO USED PARTS ARE ACAILABLE BECAUSE THERE ARE MANY MORE LIKE ME WITH THIS STYLE VEHICLE. ALSO IN JANUARY THERE WAS A RECALL NOTICE 17S09/NHTSA RECALL 17V-209 THAT HAD TO DO WITH THE CYLINDER HEAD CRACKED THAT MAY CAUSE OIL TO LEAK AND MAY RESULT IN A FIRE IN THE ENGINE COMPARTMENT .",
  "question": "Going by this vehicle safety complaint, did the vehicle actually catch fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q80a78d3c79",
  "kind": "yes/no",
  "text": "Statement 1: The mechanic fixed my car while it was in the shop.\nStatement 2: The mechanic sank my car while it was in the shop.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qd3d3421fda",
  "kind": "yes/no",
  "text": "Table caption: Average number of false positives per scan in the brain datasets. Best performances are indicated in bold.\n|  | GP-Unet (this paper) | GP-Unet no residual | Gated Attention | Grad-CAM | Grad | Guided-backprop | Intensities |\n| Midbrain | 1.03 (0.99 - 1.07) | 1.19 (1.15 - 1.24) | 1.04 (0.99 - 1.09) | 1.10 (1.05 - 1.15) | 1.40 (1.34 - 1.45) | 0.99 (0.94 - 1.03) | 1.11 (1.06 - 1.15) |\n| Hippocampi | 1.12 (1.06 - 1.17) | 1.96 (1.88 - 2.03) | 1.13 (1.06 - 1.19) | 1.16 (1.10 - 1.22) | 2.16 (2.06 - 2.25) | 1.23 (1.16 - 1.29) | 3.34 (3.22 - 3.45) |\n| Basal Ganglia | 1.95 (1.88 - 2.01) | 2.33 (2.27 - 2.39) | 2.16 (2.10 - 2.23) | 2.02 (1.95 - 2.09) | 2.06 (1.98 - 2.13) | 1.98 (1.91 - 2.04) | 2.28 (2.21 - 2.35) |\n| Centrum Semiovale | 5.24 (5.04 - 5.43) | 6.66 (6.46 - 6.86) | 6.23 (6.02 - 6.44) | 5.63 (5.44 - 5.82) | 7.30 (7.03 - 7.57) | 5.92 (5.71 - 6.12) | 9.91 (9.62 - 10.21) |\n| Average | 2.33 +/- 1.71 | 3.04 +/- 2.13 | 2.64 +/- 2.12 | 2.48 +/- 1.86 | 3.23 +/- 2.37 | 2.53 +/- 1.99 | 4.16 +/- 3.41 |\n\nStatement: The highest Gated Attention is 1.04 (0.99 - 1.09) of Midbrain.",
  "question": "According to the table, is the statement supported?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qfa2ac889f2",
  "kind": "yes/no",
  "text": "Customer: Yes, I would like to find a place to eat. Please find me a moderately priced restaurant in the centre.\nAssistant: there are quite a few moderately priced restaurants in the city centre. do you have a preference on cuisine?",
  "question": "According to its reply, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q7e753860a8",
  "kind": "yes/no",
  "text": "Statement 1: We need save his life with two pints of poison.\nStatement 2: We need save his life with two pints of blood.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q1a2c879787",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS: The incidence of VTE in patients with severe NCP is 25% (20/81), which may be related to poor prognosis.\n\nClaim: There are approximately 1 in 4 incidences of venous thromboembolism in patients with severe novel coronavirus pneumonia symptoms of SARS-CoV-2.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q68336a3162",
  "kind": "yes/no",
  "text": "Complaint narrative: WHILE ATTEMPTING TO OPERATE THE ELECTRIC SLIDING SIDE DOOR, A LARGE SPARK AND SMALL DEBRIS FIRE WAS SEEN IN THE BOTTOM DOOR RAIL. UPON INSPECTION, A BREAK IN THE WIRE HARNESS HAD ALOUD WIRES TO BE SEVERED THAT CONTROLS THE DOOR AND LOCKING SYSTEM. THE AUTOMATIC DOOR LOCKS ON BOTH SIDE DOORS NO LONGER WORKED AND THE PASSENGER SIDE DOOR WOULD NO LONGER OPEN ELECTRICALLY. I REMOVED THE WIRING HARNESS AND WIRES AND DISCARDED THEM TO AVOID ANY MORE PROBLEMS (SPARKING AND/OR FIRES). THIS COULD CAUSE A MAJOR FIRE HAZARD IN THE RIGHT ENVIRONMENT.",
  "question": "Is it correct that this vehicle safety complaint doesn't report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q94400fb8c8",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2008 MINI COOPER S. THE CONTACT STATED THAT WHILE PARKED, THERE WAS AN ABNORMAL BURNING OIL ODOR FROM THE VEHICLE. THE FAILURE RECURRED CONSTANTLY. THE CONTACT PARKED THE VEHICLE AND NOTICED OIL LEAKING ONTO THE GROUND. THE VEHICLE WAS NOT DIAGNOSED OR REPAIRED. THE MANUFACTURER WAS MADE OF THE FAILURE. THE APPROXIMATE FAILURE MILEAGE WAS 59,000.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q39a43d7fd3",
  "kind": "yes/no",
  "text": "Customer: Yes, I'd like two tickets, please.\nAssistant: Great. I've booked two tickets for the train, and your reference number is TNF2DMIQ. Can I help you with anything else today?",
  "question": "Based on the text, does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q8c9e097b96",
  "kind": "yes/no",
  "text": "Complaint narrative: TO WHOM IT MAY CONCERN, ON APPROXIMATELY, SUNDAY, AUGUST 10, 2014, I WAS DRIVING MY 2007 KIA RONDO AND A MAN HIT MY BUMPER DUE TO THE FACT HE COULD NOT SEE MY BRAKE LIGHTS (DUE TO THE MANUFACTURER'S RECALLED PARTS; NHTSA CAMPAIGN NUMBERS: 13V114000 AND 09V130000). I WAS UNAWARE OF THE RECALLED PRODUCT UNTIL YESTERDAY, FEBRUARY 1, 2015, WHEN I WAS DOING A GOOGLE SEARCH. THIS WHOLE SITUATION HAS REALLY FRIGHTENED ME BECAUSE I AM ESSENTIALLY DRIVING A TICKING TIME BOMB. THE BRAKE LIGHTS ARE OUT, AND THE RED \"AIR BAG\" LIGHT IS ON (THEREFORE DETERMINING THAT THE AIR BAGS DO NOT WORK; NHTSA CAMPAIGN NUMBER: 12V014000), AND THE YELLOW \"ESC OFF\" LIGHT IS ON, AND DOES NOT GO OFF. I HAVE TO CONTINUOUSLY POP OPEN THE HOOD TO RECONNECT THE BATTERY EVERY OTHER TIME ATTEMPT TO TURN THE CAR ON. I AM A MONDAY-FRIDAY 9-5 WORKING 19 YEAR OLD LIVING ON HIS OWN, AND I AM LIVING TO PAYCHECK TO PAYCHECK. I AM SIMPLY UNABLE TO PAY FOR THE DAMAGES DUE TO THE ENGINEERING BY THE MANUFACTURER, AND I AM PRAYING I WILL RECEIVE SOME TYPE OF COMPENSATION SO I CAN HAVE A RELIABLE CAR FOR MY DAILY LIFE. KIND REGARDS, A 2007 KIA RONDO OWNER",
  "question": "Does this vehicle safety complaint state that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q9a8b221e12",
  "kind": "yes/no",
  "text": "Occupation: Coil Winders, Tapers, and Finishers\nDuties:\n- Bond wood reinforcing strips to decks and cabin structures of watercraft, using resin-saturated fiberglass.\n- Spray chopped fiberglass, resins, and catalysts onto prepared molds or dies using pneumatic spray guns with chopper attachments.\n- Select precut fiberglass mats, cloth, and wood-bracing materials as required by projects being assembled.",
  "question": "Based on the text, are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q5a9db8186a",
  "kind": "yes/no",
  "text": "Table caption: Characteristics of all ESS 11 cases in relation to gender.\n| Gender | Women ( n = 1087) | Men ( n = 783) | P |\n| Age - years |  |  |  |\n| Median (25 th ,75 th percentile) | 73 (56−84) | 71 (55−81) | 0.025 |\n| Priority at dispatch centre - n (%) a |  |  | 0.001 |\n| Prio 1 | 334 (30.8) | 302 (38.6) |  |\n| Prio 2 | 698 (64.3) | 448 (57.2) |  |\n| Prio 3 | 53 (4.9) | 33 (4.2) |  |\n| Triage colour RETTS - n (%) |  |  | 0.002 |\n| Red | 11 (1.0) | 13 (1.7) |  |\n| Orange | 224 (20.6) | 195 (24.9) |  |\n| Yellow | 587 (54.0) | 423 (54.0) |  |\n| Green | 265 (24.4) | 152 (19.4) |  |\n| Level of care - n (%) |  |  | 0.170 |\n| To hospital | 849 (78.1) | 632 (80.7) |  |\n| Stay at the scene | 238 (21.9) | 151 (19.3) |  |\n| Seek medical advice within 72 h. - n (%) b | 29 (12.2) | 15 (9.9) | 0.517 |\n| Mode of transport - n (%) c |  |  | 0.605 |\n| Ambulance | 764 (90.0) | 584 (92.4) |  |\n| PTS, immobile d | 33 (3.9) | 17 (2.7) |  |\n| PTS, seated | 32 (3.8) | 18 (2.8) |  |\n| Single-responder unit | 8 (0.9) | 9 (1.4) |  |\n| Transport by own means | 12 (1.4) | 4 (0.6) |  |\n| Type of condition - n (%) |  |  |  |\n| Non-time critical | 1040 (95.7) | 734 (93.7) | 0.062 |\n| Time critical | 47 (4.3) | 49 (6.3) |  |\n\nStatement: Transport by own means Men ( n = 783) is 4 (0.6).",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qccaa27414f",
  "kind": "yes/no",
  "text": "Customer: Yes, are there any British places to eat at in the same area?\nAssistant: Yes, there are 7 of them. How about restaurant one seven?",
  "question": "In its reply did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q435341358d",
  "kind": "yes/no",
  "text": "Perhaps the good Doc thinks I need to take his matlab class ;)",
  "question": "Is it correct that this paragraph does not make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable.\n- no: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy."
 },
 {
  "qid": "q0fd8f5bbbb",
  "kind": "yes/no",
  "text": "Situation: I'm a stereotypical nerd with WEAK thighs\nAction being judged: Making assumptions about an entire group of people.",
  "question": "Is it correct that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 }
]
