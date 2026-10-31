# G5-H blind read T37b-blind_read-5eb7574e-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_qc2/g5h/answers/T37b-blind_read-5eb7574e-000.json

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
  "qid": "qf205e0dd92",
  "kind": "yes/no",
  "text": "Action: Murdering others for the benefit of yourself.",
  "question": "Is this act against the law in most places?",
  "definitions": "- yes: Doing the action is a crime or legal offence in most places (for example theft, assault, fraud, drunk driving, vandalism, hard-drug use), not merely rude or immoral.\n- no: The action is legal in most places, even if it is rude, unkind, dishonest or morally wrong (for example lying to a friend, cheating on a partner, breaking a promise)."
 },
 {
  "qid": "qbdec07fd45",
  "kind": "yes/no",
  "text": "Table caption: Operation conditions for Mg and Sr isotope determination with the Plasma II MC-ICP-MS (Nu Instruments).\n| Parameter | Running conditions | Running conditions |\n| Analyte | Mg | Sr |\n| RF power | 1300 | 1300 |\n| Plasma mode | Dry mode, DSN 100 | Wet mode |\n| Auxiliary gas | 0.85–0.9 min −1 | 0.85–0.95 l min −1 |\n| Spray chamber temperature (Peltier) | 5 °C | 5 °C |\n| Nebulizer flow rate | 0.1 ml min −1 | 0.1 ml min −1 |\n| Nebulizer type | MicroMist concentric pyrex nebulizer (GlassExpansion) |  |\n| Cone + skimmer | Ni | Ni |\n\nStatement: RF power has 1800 as Mg value.",
  "question": "Is there support for the statement in the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1e95e1c7ab",
  "kind": "yes/no",
  "text": "The results just presented beg the following question: If the satellite data indicate an insensitive climate system, why do the climate models suggest just the opposite? I believe the answer is due to a misinterpretation of cloud behavior by climate modelers.",
  "question": "Is there confirmation that this paragraph makes the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qedb0e6aee3",
  "kind": "yes/no",
  "text": "Brian Christley, a resident of Abergele, Wales, wrote to the Daily Telegraph : Over the weekend just gone, the coldest of the year so far, all 100-plus off-shore wind turbines along the North Wales coast were idling very slowly, all using grid power for de-icing and to power their hydraulic systems that keep the blades facing in the same direction.",
  "question": "Is this paragraph making the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q9cbc847b33",
  "kind": "yes/no",
  "text": "Occupation: Software Quality Assurance Analysts and Testers\nDuties:\n- Document software defects, using a bug tracking system, and report defects to software developers.\n- Participate in product design reviews to provide input on functional requirements, product designs, schedules, or potential problems.\n- Test system modifications to prepare for implementation.",
  "question": "For the occupation named above, are the listed duties part of its job?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q6884c36d21",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nOur phylogenetic analysis places the majority of these genomes with viruses sequenced from Washington state. By coupling our genomic data with domestic and international travel patterns, we show that early SARS-CoV-2 transmission in Connecticut was likely driven by domestic introductions.\n\nClaim: Widespread cases of COVID-19 in the United States can be traced to international transmission.",
  "question": "According to the evidence, does it support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q583ddef1d2",
  "kind": "yes/no",
  "text": "Customer: Could you try an hour earlier, then?\nAssistant: Certainly. You now have a table for your party of 8 at the Curry Garden, at 16:45. Your reference number is V24OGNJB.",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "q213913f1ef",
  "kind": "yes/no",
  "text": "Table caption: The number of views depending on the rating.\n| responses_rating_grade | views |\n| 1.0 | 1192.8 |\n| 2.0 | 1278.9 |\n| 3.0 | 1391.4 |\n| 4.0 | 1169.8 |\n| 5.0 | 990 |\n\nStatement: Rating grade 5.0 has less number of views.",
  "question": "Is it the case that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qd3258e07f3",
  "kind": "yes/no",
  "text": "Table caption: Correlation between cerebral perfusion pressure and brain tissue oxygenation in 5 patients.\n| Patient No | Pearson coefficient (r) of correlation between CPP and PbtO 2 and probability (p) |\n| 1 | 0.79, p < 0.01 |\n| 2 | 0.38, p < 0.01 |\n| 3 | 0.35, p < 0.01 |\n| 4 | 0.77, p < 0.01 |\n| 5 | 0.7, p < 0.01 |\nTable notes: Abbreviations: r – Pearson's correlation coefficient; CPP – cerebral perfusion pressure; PbtO 2 – partial pressure of oxygen in brain tissue.\n\nStatement: Patient No 4 is having 0.77, p < 0.01 correlation between CPP and PbtO 2 and probability (p).",
  "question": "Does the table provide support for the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q6b921364a6",
  "kind": "yes/no",
  "text": "Complaint narrative: THE SENSOR THAT DETERMINES IF THE PASSENGER AIRBAG TURNS ON DOES NOT WORK PROPERLY. I WEIGH 100 POUNDS (WHICH IS ABOVE THE THRESHOLD FOR WHAT SHOULD TRIGGER THE AIRBAG TO BE ON) AND ABOUT HALF THE TIME THE AIRBAG IS DISABLED WHEN I AM SITTING IN THE SEAT PROPERLY WITH MY FEET ON THE GROUND AND THE CHAIR UPRIGHT. I CONTACTED CHEVROLET TO HAVE THEM REIMBURSE THE COST OF FIXING THIS ISSUE BECAUSE IT IS A SAFETY ISSUE AND HAS CAUSED RECALLS IN OTHER CHEVROLET CARS, BUT THEY HAVE REFUSED TO INVESTIGATE. THE SENSOR MALFUNCTION DOESN'T SEEM TO BE CORRELATED WITH WHETHER THE VEHICLE IS STATIONARY, IN MOTION, ON A STREET OR HIGHWAY, ETC. IT HAPPENS ABOUT HALF OF THE TIME AND CAN SOMETIMES GO ON AND OFF DURING THE SAME CAR TRIP EVEN IF I STAY IN THE SAME POSITION THE WHOLE TIME. THIS ISSUE HAS REPORTED FOR CHEVROLET MALIBUS ON SEVERAL ONLINE FORUMS SO I KNOW IT ISN'T AN ISOLATED ISSUE WITH MY CAR. WE ARE CONCERNED ABOUT WHAT COULD HAPPEN IF WE WERE IN A CRASH AND THE AIRBAG DIDN'T GO OFF OR WENT OFF LATE WHEN THE PASSENGER'S BODY WAS TOO CLOSE TO THE AIRBAG.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "q26faa325a6",
  "kind": "yes/no",
  "text": "Hereward Corley pointed out that the reference to Shaviv (2008) should have been Shaviv (2005). Nir Shaviv another genius of a mathematician had originally sent me the paper saying it was from 2008, but the version he sent was an undated pre-publication copy. Mr. Corley also kindly supplied half a dozen further papers that determine climate sensitivity empirically. Most of the papers find it low, and all find it below the IPCCs estimates. The papers are Chylek & Lohman (2008); Douglass & Knox (2005); Gregory et al. (2002); Hoffert & Covey (1992); Idso (1998); and Loehle & Scafetta (2011).",
  "question": "Does the paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q0f4eb78d82",
  "kind": "yes/no",
  "text": "Customer: I want to watch a movie\nAgent: Ok what movie?\nCustomer: I want to see Mulan\nAgent: Ok when and what time?\nCustomer: Tomorrow maybe round 8pm?\nAgent: Ok let me check\nCustomer: Ok\nAgent: We have two options available\nCustomer: Ok\nAgent: Ciemark 12 which is 30 miles away.\nCustomer: Is there not one closer?\nAgent: you have Mountain AMC 16 which is 22 miles away\nCustomer: I cannot go those are too far\nAgent: We apologize for any inconvenience\nCustomer: It's fine\nAgent: Ok please contact us if we can e of",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qee685f39b0",
  "kind": "yes/no",
  "text": "Assistant: It's about thirty dollars for an entree each.\nCustomer: Hmm, not bad. I think my partner will be happy.\nAssistant: I'm sure they will be. Reservations for Pastabilities, tonight at 7 PM for two people in a private corner are confirmed!",
  "question": "Does the assistant's final message confirm \"private corner\" for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q27ecd80f07",
  "kind": "yes/no",
  "text": "Statement 1: oil can be found in the sky\nStatement 2: oil can be found in the underground",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q22c9725f3b",
  "kind": "yes/no",
  "text": "Complaint narrative: ISSUES JERKING AND HARD SHIFTING WHILE DRIVING. CAR LURCHES FORWARD AND MOVES IN JERKY MOVEMENTS. ALMOST CAUSED AN ACCIDENT BECAUSE VEHICLE STALLED THEN LURCHES FORWARD HARD.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "qb27ab78123",
  "kind": "yes/no",
  "text": "Customer: Yes, please try for 12:00\nAssistant: I'm sorry. I'm not sure what is going on. It will not let me book. Would you like to try a different restaurant?",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "qd408b5be11",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In the 2021 general election, De Mos attempted to return to the House of Representatives as \"lijsttrekker\" of the party Code Orange.\n\nSummary sentence:\nHe was the \"lijsttrekker\" for Code Orange in the 2021 general election.",
  "question": "Is every detail in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q7c92338a47",
  "kind": "yes/no",
  "text": "New York City is 1199's true power center, however. It's hard to overstate the significance of 1199 to the so-called progressive movement that now controls almost every major city office. City council speaker and leader of the Progressive Caucus Melissa Mark-Viverito is a former organizer for 1199, which has played an active role in her career from the beginning. The union suggested that the Puerto Ricanborn and Columbia Universityeducated heiress move from Greenwich Village to East Harlem to establish a political base. To help her launch her campaign for the city council speakership, 1199 threw a lavish party in San Juan. The union's political director, Kevin Finnegan, served on Mark-Viverito's transition team when she became speaker.",
  "question": "Is there an assertion in this paragraph of the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q37b3d1a56a",
  "kind": "yes/no",
  "text": "Assistant: Yes, that will be my pleasure.\nCustomer: Thank you.\nAssistant: Okay, it is booked for you tonight at 7:30 PM for 4 at the Kati Roll Company in NYC.",
  "question": "Did the assistant's final message tell me \"Kati Roll Company\" is confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q94df4b532b",
  "kind": "yes/no",
  "text": "Situation: They saw someone was missing and later found him dead in the maze.\nAction being judged: Reporting a dead body if you stumble across one.",
  "question": "Is the action being judged permissible under common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qe35f9220d3",
  "kind": "yes/no",
  "text": "Customer: Find me a restaurant that serves belgian food in the centre\nAssistant: I'm sorry, there aren't any.",
  "question": "According to its reply, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qf973961be2",
  "kind": "yes/no",
  "text": "Situation: Friends Add to Woman's Grief by Not Being There for Her\nAction being judged: Grieving at times.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q7e858a3df7",
  "kind": "yes/no",
  "text": "Customer: A cheap jamaican restaurant, please. If you cannot find one, then mediterranean.\nAssistant: There are no Jamaican restaurants listed. I will look for Mediterranean.",
  "question": "Did the assistant, in its reply, find for the customer at least a single option meeting everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q14d6a55581",
  "kind": "yes/no",
  "text": "Table caption: Peptide match of ARIP-B.\n| S. No | Plant description | Match Coverage (%) | Total Coverage (%) | RIP activity reported | RIP gene identified | Type of RIP | References |\n| 1 | Populus trichocarpa | 2 + 1 + 1 + 3 + 3 | 10 | Yes | Yes | Type 2 (B domain only) | Peumans and Vandamme (2010) |\n| 2 | Astragalus membranaceus | 10 | 10 | No | No | – | – |\n| 3 | Polygala tenuifolia | 1 | 1 | No | No | – | – |\n| 4 | Vitis vinifera | 0 + 2 | 2 | Yes | No | – | Peumans and Vandamme (2010) |\n| 5 | Triticum aestivum | 2 | 2 | Yes | Yes | Type 1 | Raj and Vennila (2013) |\n| 6 | Glycine max | 2 + 1 | 3 | Yes | No | – | Peumans and Vandamme (2010) |\n| 7 | Brachypodiumdistachyon | 1 | 1 | Yes | Yes | Type 3 | Peumans and Vandamme (2010) |\n| 8 | Hordeum vulgare | 3 | 3 | Yes | Yes | Type 1 | Raj and Vennila (2013) |\n| 9 | Ricinus communis | 2 | 2 | Yes | Yes | Type 2 | – |\n| 10 | Micromonaspusilla | 1 | 1 | Yes | No | – | Peumans and Vandamme (2010) |\n| 11 | Musa acuminata subsp. | 11 | 11 | No | No | – | – |\n| 12 | Arabidopsis lyrata subsp. | 3 | 3 | No | No | – | Peumans and Vandamme (2010) |\n\nStatement: There are four categories of Plant description.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q1367878786",
  "kind": "yes/no",
  "text": "Moreover the WBDGE site writes that Arctic sea ice has grown strongly over last year and that there has been no melting trend there in almost 10 years.",
  "question": "Based on the text, does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q342c518c54",
  "kind": "yes/no",
  "text": "CEI's FOIA request details how the UN informed participants that it was motivated by embarrassing releases of earlier discussions (\"ClimateGate\" key among them) and, to circumvent the problem that national government transparency laws posed, the group itself.",
  "question": "Is this paragraph making the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qe3e6099c36",
  "kind": "yes/no",
  "text": "Assistant: It will be ready in 15 min.\nCustomer: Great.\nAssistant: I have you down for Tall Latte with a lemon bar.",
  "question": "Is \"Latte\" for the customer's coffee order confirmed in the final message from the assistant?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q84ccd30cb2",
  "kind": "yes/no",
  "text": "Customer: I think it would be fun to go to see a movie tonight.\nAgent: Sure. What movie would you like to see?\nCustomer: What's playing at the Boulevard 14 Cinema in Petaluma, California since that would be the closest theater.\nAgent: OK. Boulevard 14 Cinema in Petaluma, California is showing three movies: No Time To Die, Mulan, and Emma.\nCustomer: Do you know anything about the movie?\nAgent: Sure. What specifically would you like to know?\nCustomer: What is the story about?\nAgent: OK. Here’s the synopsis of Mulan: Accompanied by her dragon, Mushu, Mulan uses her smarts to help ward off a Hun invasion, falling in love with a dashing captain along the way.\nCustomer: It sounds like it might be good. Did it get good reviews from both critics and the audiences?\nAgent: Mulan has an 87% Rotten Tomatoes score and a 92% audience rating.\nCustomer: Mulan sounds ok, but I think I'd rather see No Time to Die.\nAgent: OK. No Time To Die is playing 4:00pm, 7:30pm, and 10:55pm. Which time would you like?\nCustomer: We would like to go to the 10:55 pm show and it'll be just my friend and I.\nAgent: All right. Let me confirm that you’d like two tickets for No Time To Die at Boulevard 14 Cinema tonight at 10:55pm. Is that all correct?\nCustomer: Yes, that's correct.\nAgent: Is it OK to go ahead and purchase these tickets?\nCustomer: Yes.\nAgent: OK. Your tickets are purchased and details for how to proceed have been sent to your email address. Can I help with anything else?\nCustomer: I'm not familiar with your email confirmation. How does that work?\nAgent: The email will provide up to three options for your tickets: print at home, electronic tickets, or an option to pick them up at the theater.\nCustomer: Thank you for explaining that to me.\nAgent: OK. Enjoy your movie!",
  "question": "Is it true that, by the end of this conversation, the customer hasn't actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "qb9498133a7",
  "kind": "yes/no",
  "text": "Customer: Hi, can you help me with booking movie tickets in Davis, California?\nAgent: No problem. Do you have a movie in mind?\nCustomer: I'm interested in \"No time to die\".\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: Oh, so noting in Davis then?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: That's too bad! Are there any action movies playing in Davis?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Is it the old one from like the 70's?\nAgent: The release date for this film is October 12, 1979.\nCustomer: Okay, thank you for your help, but I think I'll pass this time. Maybe they will have movies I like later.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By the end of this dialogue, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q7e5d75c5d5",
  "kind": "yes/no",
  "text": "Customer: I am looking for a restaurant that serves Afghan food in the centre.\nAssistant: There are no Afghan restaurants in the centre of town.",
  "question": "According to its reply, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q65798db586",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nWe studied antibody response in 9 healthcare workers in Jeddah, Saudi Arabia, who survived Middle East respiratory syndrome, by using serial ELISA and indirect immunofluorescence assay testing. Among patients who had experienced severe pneumonia, antibody was detected for >18 months after infection.\n\nClaim: Survivors of the 2012 MERS outbreak, who had severe pneumonia, lacked any antibodies against the virus.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q8b91abdfdc",
  "kind": "yes/no",
  "text": "Statement 1: She worried about getting bored at the dark cabinet.\nStatement 2: She worried about getting bored at the dark cabin.",
  "question": "Of these two statements, does Statement 2 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "qf3b7a80bcf",
  "kind": "yes/no",
  "text": "Action: Wishing for someone else to be sad.",
  "question": "Is this deed prohibited by law in most places?",
  "definitions": "- yes: Doing the action is a crime or legal offence in most places (for example theft, assault, fraud, drunk driving, vandalism, hard-drug use), not merely rude or immoral.\n- no: The action is legal in most places, even if it is rude, unkind, dishonest or morally wrong (for example lying to a friend, cheating on a partner, breaking a promise)."
 },
 {
  "qid": "qeddb0c192f",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nVirus was widely distributed on floors, computer mice, trash cans, and sickbed handrails and was detected in air ≈4 m from patients.\n\nClaim: The coronavirus can be detected in the air up to 13 feet away from an infected patient.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q76093bf01e",
  "kind": "yes/no",
  "text": "Occupation: Nannies\nDuties:\n- Observe participants and inform them of corrective measures necessary for skill improvement.\n- Instruct participants in maintaining exertion levels to maximize benefits from exercise routines.\n- Offer alternatives during classes to accommodate different levels of fitness.",
  "question": "Do the listed duties form part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q8a7f051eb2",
  "kind": "yes/no",
  "text": "Customer: Hello.\nAgent: Hi, how may I assist you today?\nCustomer: I'd like to buy some movie tickets, please.\nAgent: Okay, what movie do you want to see?\nCustomer: I live in Stoneyford, Oregon, so can you check Mountain AMC 16?\nAgent: What movie do you want me to check for?\nCustomer: No Time to Die.\nAgent: That movie isn't available there, sorry.\nCustomer: What about 'Mulan'?\nAgent: Sorry, unavailable as well, actually that theater is temporarily closed right now.\nCustomer: Okay then can you check Holiday Cinemark 12?\nAgent: That theater doesn't have either of those movies showing either, it's temporarily closed as well.\nCustomer: Do any other theaters have 'No Time to Die' showings?\nAgent: I've checked and it seems that No Time to Die has had its release date postponed until Fall.\nCustomer: What about 'Mulan'?\nAgent: Release date's postponed until Fall as well, unfortunately, sorry.\nCustomer: That's okay.\nAgent: Is there anything else I could help you with today?\nCustomer: No, thanks for your help.\nAgent: Alright, have a wonderful day.",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q120097827c",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2014 FORD C-MAX ENERGI. THE CONTACT STATED THAT THE VEHICLE WAS PLUGGED IN AND RECHARGING IN THE GARAGE. TWO HOURS LATER, AN EXTENSIVE FIRE ERUPTED FROM THE CHARGE CORD. THE FIRE DEPARTMENT WAS ABLE TO EXTINGUISH THE FLAMES. THE DEALER TESTED THE VEHICLE AND STATED THAT THE CHARGE CORD OVERHEATED. THE MANUFACTURER WAS NOTIFIED OF THE FAILURE AND SENT A TECHNICIAN, BUT WAS NOT ABLE TO DETERMINE THE SPECIFIC CAUSE OF THE FAILURE. THE VEHICLE WAS INSPECTED BY A DEALER AND THE INSURANCE ADJUSTER. THE COSMETIC DAMAGES WERE REPAIRED, BUT THE CONTACT WAS UNABLE TO DETERMINE IF THE FAILURE WOULD RECUR. THE VIN AND FAILURE MILEAGE WERE NOT AVAILABLE.",
  "question": "Does this vehicle safety complaint say the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qf4b169d115",
  "kind": "yes/no",
  "text": "Situation: He pulled her aside after class and asked her.\nAction being judged: Waiting until after class to socialize.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q18e189693b",
  "kind": "yes/no",
  "text": "Occupation: Wind Energy Development Managers\nDuties:\n- Participate in special education-related activities, such as attending meetings and providing support to special educators throughout the district.\n- Establish, coordinate, and oversee particular programs across school districts, such as programs to evaluate student academic achievement.\n- Advocate for new schools to be built, or for existing facilities to be repaired or remodeled.",
  "question": "Are the duties given in the list part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q7de21ab90f",
  "kind": "yes/no",
  "text": "Ossie Davis\nOssie Davis (born Raiford Chatman Davis; December 18, 1917 – February 4, 2005) was an American film, television and Broadway actor, director, poet, playwright, author, and civil rights activist.\n\nAndrew Stevens\nAndrew Stevens (born June 10, 1955) is an American executive, film producer, director and actor.",
  "question": "Would it be correct to say that Andrew Stevens and Ossie Davis are not both Broadway actors?",
  "definitions": "- yes: The paragraphs do not bear out the positive statement (the question read without its 'not' or 'fail to'): at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer.\n- no: Read together, the paragraphs show that the positive statement (the question read without its 'not' or 'fail to') holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right)."
 },
 {
  "qid": "qb0190494d5",
  "kind": "yes/no",
  "text": "Customer: Hi, I would like to buy movie tickets.\nAgent: Hi, I would like to buy movie tickets.\nCustomer: Any place in Chicago.\nAgent: AMC River East 21 works?\nCustomer: Yes it works.\nAgent: When do you want to go to the movies?\nCustomer: This afternoon between 3:00 and 4:00PM.\nAgent: What movie do you want to watch?\nCustomer: Any movie as long as it is not a standard.\nAgent: There is only one movie that is not standard and is in Dolby Cinema.\nCustomer: What movie is this?\nAgent: Birds of Pray. There's a time slot for 4:00PM. Do you want me to continue?\nCustomer: Yes please.\nAgent: How many tickets do you want?\nCustomer: 3\nAgent: There's 3 tickets but they are in the very front. Do you want these seats?\nCustomer: Those are horrible seats to have, why would you suggest it?\nAgent: Those are the only ones available.\nCustomer: Well. I don't want to order anything then.\nAgent: Sorry for the inconvenience.\nCustomer: You should be sorry!\nAgent: Have a good day.",
  "question": "Have movie tickets actually been bought by the customer by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q77f27bf4a8",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nRates of ventilation in the HC, HC+AZ, and no HC groups were 13.3%, 6.9%, 14.1%, respectively. The risk of ventilation was similar in the HC group (adjusted hazard ratio, 1.43; 95% CI, 0.53 to 3.79; P=0.48) and in the HC+AZ group (adjusted hazard ratio, 0.43; 95% CI, 0.16 to 1.12; P=0.09), compared to the no HC group. CONCLUSIONS: In this study, we found no evidence that use of hydroxychloroquine, either with or without azithromycin, reduced the risk of mechanical ventilation in patients hospitalized with Covid-19.\n\nClaim: Hydroxychloroquine does not help patients avoid being placed on a ventilator.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q0c9009dfad",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Dodon was appointed to the post of Associate Minister of Trade and Economics in May 2005, during the second Tarlev Cabinet.\n- He assumed the position of Minister of Trade and Economics in September 2006.\n- He held the position until September 2009, when the government of Zinaida Greceanîi ended.\n- In September 2009, after 8 years of governing, the Communist Party came into opposition.\n- He became an MP in the Parliament, which was reelected in November 2010.\n- After he was elected as the president of Moldova, due to specifics of Moldovan law, Dodon resigned as PSRM chairman and left the party, being replaced by Zinaida Greceanîi as interim leader.\n- Dodon was sworn in on 23 December 2016 in the Palace of the Republic.\n\nSummary sentence:\nHe served as minister of trade and economics in the governments of Vasile Tarlev and Zinaida Greceanîi from September 2006 to September 2009 and was a member of the Parliament of Moldova from 2009 to 2016.",
  "question": "Is every piece of the summary sentence's information supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q53626104b5",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nConclusion and Relevance: Among patients with severe or life-threatening COVID-19, convalescent plasma therapy added to standard treatment, compared with standard treatment alone, did not result in a statistically significant improvement in time to clinical improvement within 28 days.\n\nClaim: COVID-19 patients treated with convalescent plasma recover at faster rates than those without treatment.",
  "question": "Is the claim contradicted by the evidence?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q837a88c6fe",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nHospitalizations were six times higher among patients with a reported underlying condition (45.4%) than those without reported underlying conditions (7.6%).\n\nClaim: Underlying conditions have no correlation with COVID-19 hospitalizations or deaths.",
  "question": "Is there support from the evidence for the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q7e8f9beef7",
  "kind": "yes/no",
  "text": "Customer: I'm also looking for an attraction preferably on a boat in the west.\nAssistant: There are no boats in the west, can I try something else for you?",
  "question": "Did the assistant, in its reply, find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qe03f79dab2",
  "kind": "yes/no",
  "text": "Customer: Hey, how are you?\nAgent: Well, how can I help you?\nCustomer: I would like to see a movie tonight i think\nAgent: sure, is anyone going with you?\nCustomer: just my girlfriend and brother\nAgent: great, what would you like to see?\nCustomer: the Boy 2, or Bad boys would be good\nAgent: Okay, is there any particular theater you would like to go to?\nCustomer: I like Regal or AMC\nAgent: Okay, is there a specific time you would like to go?\nCustomer: I think anywhere from 7-8 would be good\nAgent: okay, one second let me check\nCustomer: sure thing, take your time\nAgent: okay, I am checking for the boy 2 and see no results\nCustomer: shucks, can you check for bad boys then?\nAgent: sure thing, let me see\nCustomer: okay, hopefully they have something....\nAgent: okay, bad news, there is nothing for that either\nCustomer: okay, I guess it is not in the cards for tonight, thank you anyways\nAgent: not a problem, any time!",
  "question": "Is it right to say that, by the end of this conversation, the customer has not actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "qccfdd1d177",
  "kind": "yes/no",
  "text": "Table caption: Probabilities of detection for five A-Train and C-Train sun-synchronous orbiters at about 700 km altitude.\n| Satellite | Hard Body Radius | Threshold | Estimated Detection Rate P(Pc > T) | Data Span | Number of Reports | Number of Days |\n| CloudSat | 3.5 | 1.00E-04 | 75.2% | Apr 2015 - Sep 2019 | 2323 | 1632 |\n| CALIPSO | 14.8 | 1.00E-04 | 92.5% | Jan 2015 - Apr 2019 | 2261 | 1586 |\n| Aqua | 20 | 1.00E-04 | 96.3% | Jun 2016 - Apr 2019 | 1560 | 1047 |\n| Aura | 20 | 1.00E-04 | 96.6% | Jun 2016 - Apr 2019 | 1772 | 1045 |\n| OCO-2 | 6 | 1.00E-04 | 84.7% | Jan 2015 - Sep 2019 | 2402 | 1720 |\n\nStatement: Estimated Detection Rate P(Pc > T) 96.3% for Aqua Satellite.",
  "question": "Does the table back up the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q09639b62dc",
  "kind": "yes/no",
  "text": "Situation: Carl asked him if he could meet him to return his phone.\nAction being judged: Letting your friends borrow your things as long as they return them.",
  "question": "Would it be correct to say that the action being judged isn't wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q1889cab656",
  "kind": "yes/no",
  "text": "Table caption: CEO tenure, chair duality, and compensation. This table presents the relations between the CEO's tenure and CEO-chair duality (columns 1–2) or total current compensation including salary and bonus (columns 3–4). The sample is the same as that in , except for columns 3 and 4, in which the sample is from 1936 to 2011 and conditions on CEO compensation data. Columns 2 and 4 measure CEO tenure effects using the instrumental variable approach of , which, at each point in time, reflects the proportion of a given CEO's ultimate tenure. These columns display within-firm R-squared, while columns 1 and 3 show total R-squared. Firm and year fixed effects are included in all specifications. All standard errors are adjusted for sample clustering at the firm level. *, **, and *** represent results significant at the 10%, 5%, and 1% levels, respectively.\n| Dep. var. | 1 (Chair duality) | 1 (Chair duality) | Log(Compensation) | Log(Compensation) |\n|  | (1) | (2) | (3) | (4) |\n| Model: | OLS | AS-IV | OLS | AS-IV |\n| CEO tenure | 2.180*** | 2.382*** | 0.024*** | 0.025*** |\n|  | (26.38) | (30.04) | (5.73) | (9.11) |\n| log(board size) | –11.369*** | –11.406*** | 0.039 | 0.042 |\n|  | (–7.93) | (–7.96) | (0.47) | (0.52) |\n| log(assets) | 2.998*** | 2.906*** | 0.293*** | 0.293*** |\n|  | (4.55) | (4.40) | (7.56) | (7.86) |\n| q | 0.750* | 0.752* | 0.007 | 0.007 |\n|  | (1.77) | (1.77) | (0.19) | (0.20) |\n| ROA (ind-adj) | 1.168 | 0.681 | 1.463*** | 1.419*** |\n|  | (0.36) | (0.21) | (4.37) | (4.53) |\n| Stock return (ind-adj) | – | – | 0.214*** | 0.214*** |\n|  | – | – | (4.35) | (4.42) |\n| Tangibility | 4.524 | 4.403 | –0.110 | –0.118 |\n|  | (1.24) | (1.20) | (–0.69) | (–0.74) |\n| Firm fixed effects | Y | Y | Y | Y |\n| Year fixed effects | Y | Y | Y | Y |\n| R 2 | 0.534 | 0.197 | 0.880 | 0.832 |\n| N | 67,887 | 67,259 | 3323 | 3314 |\n\nStatement: ROA (ind-adj) 1 (Chair duality) under OLS is (26.38).",
  "question": "Is it right to say that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 }
]
