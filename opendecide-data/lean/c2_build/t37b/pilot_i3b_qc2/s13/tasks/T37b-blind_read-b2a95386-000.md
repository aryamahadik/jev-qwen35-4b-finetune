# T37b blind solver T37b-blind_read-b2a95386-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_qc2/s13/answers/T37b-blind_read-b2a95386-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qd2b01b3a8c",
  "kind": "yes/no",
  "text": "Action: Murdering others for the benefit of yourself.",
  "question": "Is this action against the law in most places?",
  "definitions": "- yes: Doing the action is a crime or legal offence in most places (for example theft, assault, fraud, drunk driving, vandalism, hard-drug use), not merely rude or immoral.\n- no: The action is legal in most places, even if it is rude, unkind, dishonest or morally wrong (for example lying to a friend, cheating on a partner, breaking a promise)."
 },
 {
  "qid": "q79b4a22fb7",
  "kind": "yes/no",
  "text": "Customer: Hello, I would like to purchase Movie tickets\nAgent: Ok for what film?\nCustomer: No Time To Die or Mulan\nAgent: Where are you located ?\nCustomer: Stoneyford Oregon\nAgent: ok let me see what I have ...\nCustomer: ok...\nAgent: I have Mountain AMC 16.\nCustomer: ok\nAgent: Or Holiday Cinemark 12.\nCustomer: You can check either n let mw know if they have tickets available?\nAgent: I am sorry it is saying at this time both of the theaters are temporarily closed.\nCustomer: oh no ! Does it say when they will be open again ?\nAgent: The release dates of both movies have been postponed until the fall.\nCustomer: ok ..\nAgent: I am very sorry I will not be able to book your tickets at this time.\nCustomer: ok.. I understand\nAgent: Please return in the fall for further updates.\nCustomer: Ok...\nAgent: Have a great day !!",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q60a4285d35",
  "kind": "yes/no",
  "text": "Customer: Find me a restaurant that serves belgian food in the centre\nAssistant: I'm sorry, there aren't any.",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q6e940d5411",
  "kind": "yes/no",
  "text": "Table caption: Correlation between cerebral perfusion pressure and brain tissue oxygenation in 5 patients.\n| Patient No | Pearson coefficient (r) of correlation between CPP and PbtO 2 and probability (p) |\n| 1 | 0.79, p < 0.01 |\n| 2 | 0.38, p < 0.01 |\n| 3 | 0.35, p < 0.01 |\n| 4 | 0.77, p < 0.01 |\n| 5 | 0.7, p < 0.01 |\nTable notes: Abbreviations: r – Pearson's correlation coefficient; CPP – cerebral perfusion pressure; PbtO 2 – partial pressure of oxygen in brain tissue.\n\nStatement: Patient No 4 is having 0.77, p < 0.01 correlation between CPP and PbtO 2 and probability (p).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1b55b5e02c",
  "kind": "yes/no",
  "text": "Assistant: So mushrooms and sausage?\nCustomer: Yes, thank you.\nAssistant: your pizza order of mushroom and sausage small personal pan pizza is complete and the pizzas will be ready for pickup in about 25 minutes. your receipt will be sent to your mobile device via text message.",
  "question": "According to the assistant's last message, is \"personal pan pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6d346ddd59",
  "kind": "yes/no",
  "text": "Situation: I peed in a measuring cup as a kid and now my mom uses it to cook with\nAction being judged: Eating out of something that has been urinated in.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q4231f73681",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nWe studied antibody response in 9 healthcare workers in Jeddah, Saudi Arabia, who survived Middle East respiratory syndrome, by using serial ELISA and indirect immunofluorescence assay testing. Among patients who had experienced severe pneumonia, antibody was detected for >18 months after infection.\n\nClaim: Survivors of the 2012 MERS outbreak, who had severe pneumonia, lacked any antibodies against the virus.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q494488aca6",
  "kind": "yes/no",
  "text": "Table caption: Physical properties of coarse aggregate.\n| Sl no. | Name of the test | Details of the relevant code | Test result |\n| 1 | Aggregate Crushing value | IS:2386(Part 4) 1963 (Reaffirmed 2002) | 17.48% |\n| 2 | Aggregate impact value | IS:2386(Part 4) 1963 (Reaffirmed 2002) | 24.12% |\n| 3 | Specific gravity | IS:2386(Part 3) 1963 | 2.47 |\n\nStatement: The test Aggregate Crushing value and Aggregate impact value has different Details of the relevant code of IS:2386(Part 3) 1963.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd9f35d007f",
  "kind": "yes/no",
  "text": "CEI's FOIA request details how the UN informed participants that it was motivated by embarrassing releases of earlier discussions (\"ClimateGate\" key among them) and, to circumvent the problem that national government transparency laws posed, the group itself.",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q368788f655",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Salam was born in Rampur in 1970.\n- His father, Mufti Abdul Dayem Sahab, an Islamic scholar, had written several scholarly works on Islamic sciences in Urdu and Arabic and also worked as a hadith translator, while his mother is a housewife.\n\nSummary sentence:\nBorn in Rampur, his father was Islamic scholar Mufti Abdul Dayem Sahab while his mother is a housewife.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q1a13decee0",
  "kind": "yes/no",
  "text": "Ossie Davis\nOssie Davis (born Raiford Chatman Davis; December 18, 1917 – February 4, 2005) was an American film, television and Broadway actor, director, poet, playwright, author, and civil rights activist.\n\nAndrew Stevens\nAndrew Stevens (born June 10, 1955) is an American executive, film producer, director and actor.",
  "question": "Are Andrew Stevens and Ossie Davis both Broadway actors?",
  "definitions": "- yes: Read together, the paragraphs show the answer is yes: what the question asks holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right).\n- no: The paragraphs do not bear out a yes: at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer."
 },
 {
  "qid": "q05b7d824c8",
  "kind": "yes/no",
  "text": "Situation: They saw someone was missing and later found him dead in the maze.\nAction being judged: Reporting a dead body if you stumble across one.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qfd45aec4e7",
  "kind": "yes/no",
  "text": "Occupation: Waiters and Waitresses\nDuties:\n- Take orders from patrons for food or beverages.\n- Clean tables or counters after patrons have finished dining.\n- Write patrons' food orders on order slips, memorize orders, or enter orders into computers for transmittal to kitchen staff.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qd00d68b556",
  "kind": "yes/no",
  "text": "Customer: I am looking for a restaurant that serves Afghan food in the centre.\nAssistant: There are no Afghan restaurants in the centre of town.",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q4278d6c2cc",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In the 2021 general election, De Mos attempted to return to the House of Representatives as \"lijsttrekker\" of the party Code Orange.\n\nSummary sentence:\nHe was the \"lijsttrekker\" for Code Orange in the 2021 general election.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q6de269d7e2",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nMethods: Individuals with confirmed or suspected SARS-CoV-2 infection were screened via PCR for presence of viral genome and via enzyme-linked immunosorbent assay for presence of anti SARS-CoV-2 spike antibodies. Results: All but three confirmed SARS-CoV-2 patients seroconverted to the SARS-CoV-2 spike while only 37.4% of suspected SARS-CoV-2 patients seroconverted.\n\nClaim: Most patients who recover from the novel coronavirus will make antibodies.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qe48b8a8a03",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nVirus was widely distributed on floors, computer mice, trash cans, and sickbed handrails and was detected in air ≈4 m from patients.\n\nClaim: Other studies reported not finding the coronavirus on surfaces such as air vents in hospital rooms and on computer mice, sickbed handrails and doorknobs.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q34afb25ac5",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThis cohort study examines the clinical characteristics of men with coronavirus disease 2019 whose semen tested positive for severe acute respiratory syndrome coronavirus 2.\n\nClaim: Scientists have found traces of the coronavirus in men's semen.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q2cb1a80c90",
  "kind": "yes/no",
  "text": "Complaint narrative: THE RUNNING LIGHTS BURN OUT FREQUENTLY. NOT AT THE SAME TIME. EACH ONE WE'VE REPLACED AT LEAST 4 TIMES, WHICH IS WAY TOO MUCH. WE ARE USING GOOD QUALITY BULBS TOO. NOW THE INSIDE OF THE HEADLIGHT ASSEMBLY IS MELTED WHERE THE BULB SOCKET ITSELF SNAPS IN SO WE CAN'T KEEP THE SOCKET AND BULB IN ITS PLACE. THE REPLACEMENT HEADLIGHT ASSEMBLY IS NOT CHEAP FOR THIS VEHICLE",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q95f82a260b",
  "kind": "yes/no",
  "text": "Table caption: Operation conditions for Mg and Sr isotope determination with the Plasma II MC-ICP-MS (Nu Instruments).\n| Parameter | Running conditions | Running conditions |\n| Analyte | Mg | Sr |\n| RF power | 1300 | 1300 |\n| Plasma mode | Dry mode, DSN 100 | Wet mode |\n| Auxiliary gas | 0.85–0.9 min −1 | 0.85–0.95 l min −1 |\n| Spray chamber temperature (Peltier) | 5 °C | 5 °C |\n| Nebulizer flow rate | 0.1 ml min −1 | 0.1 ml min −1 |\n| Nebulizer type | MicroMist concentric pyrex nebulizer (GlassExpansion) |  |\n| Cone + skimmer | Ni | Ni |\n\nStatement: RF power has 1800 as Mg value.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf32c4722f9",
  "kind": "yes/no",
  "text": "Situation: One day he instructed us to write something untrue.\nAction being judged: Improving your writing skills by trying something new.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q7791be29de",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nObjective To investigate the efficacy and safety of recombinant human interferon alpha1b (rhIFN-α) nasal drops in healthy medical staff to prevent 2019 novel coronavirus disease (COVID-19). Conclusion In this investigator-initiated open-label study, we observed that rhIFN-α nasal drops can effectively prevent COVID-19 in treated medical personnel.\n\nClaim: In China, the early results of a study among medical workers were disappointing, concluding that interferon nasal drops “were ineffective at preventing Covid-19 in medical staff.”",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q7cf7be843a",
  "kind": "yes/no",
  "text": "The results just presented beg the following question: If the satellite data indicate an insensitive climate system, why do the climate models suggest just the opposite? I believe the answer is due to a misinterpretation of cloud behavior by climate modelers.",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q648ad71428",
  "kind": "yes/no",
  "text": "Goa (India) : \"there is no ongoing sea level rise, sea level has been stable for the last 50 years or so, sea level fell some 20 cm at around 1960.\"",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q822adf1107",
  "kind": "yes/no",
  "text": "Situation: Most people think I'm a sheltered and innocent woman, I actually live in my boyfriends harem with his other girlfriends.\nAction being judged: Keeping the sordid details of your life to yourself when out in public.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qf312cabd7b",
  "kind": "yes/no",
  "text": "Action: Wishing for someone else to be sad.",
  "question": "Is this action against the law in most places?",
  "definitions": "- yes: Doing the action is a crime or legal offence in most places (for example theft, assault, fraud, drunk driving, vandalism, hard-drug use), not merely rude or immoral.\n- no: The action is legal in most places, even if it is rude, unkind, dishonest or morally wrong (for example lying to a friend, cheating on a partner, breaking a promise)."
 },
 {
  "qid": "qaefdc265c4",
  "kind": "yes/no",
  "text": "Customer: Hi, I would like to buy movie tickets.\nAgent: Hi, I would like to buy movie tickets.\nCustomer: Any place in Chicago.\nAgent: AMC River East 21 works?\nCustomer: Yes it works.\nAgent: When do you want to go to the movies?\nCustomer: This afternoon between 3:00 and 4:00PM.\nAgent: What movie do you want to watch?\nCustomer: Any movie as long as it is not a standard.\nAgent: There is only one movie that is not standard and is in Dolby Cinema.\nCustomer: What movie is this?\nAgent: Birds of Pray. There's a time slot for 4:00PM. Do you want me to continue?\nCustomer: Yes please.\nAgent: How many tickets do you want?\nCustomer: 3\nAgent: There's 3 tickets but they are in the very front. Do you want these seats?\nCustomer: Those are horrible seats to have, why would you suggest it?\nAgent: Those are the only ones available.\nCustomer: Well. I don't want to order anything then.\nAgent: Sorry for the inconvenience.\nCustomer: You should be sorry!\nAgent: Have a good day.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qe2d4c7784e",
  "kind": "yes/no",
  "text": "Table caption: Formation enthalpy Y (eV/atom), Composition ratio X, Symmetry S, Fitness F (eV/block), Volumes V(Å 3 /atom), Enthalpies E(eV/atom), and Compositions C for the first 10 structures include in the convex hull of the Nb-N system at 0 GPa.\n| ID | C | E | V | F | S | X | Y |\n| 71 | [ ] | −893.5888 | 14.4958 | 0.0000 | 1 | 0.533 | −0.9929 |\n| 75 | [0 14] | −270.1198 | 14.3751 | 0.0000 | 1 | 1.000 | 0.0000 |\n| 89 | [14 ] | −1369.2158 | 18.0875 | 0.0000 | 1 | 0.176 | −0.6086 |\n| 97 | [15 0] | −1603.9973 | 22.8193 | 0.0000 | 1 | 0.000 | 0.000 |\n| 113 | [13 ] | −1183.5582 | 16.1519 | 0.0000 | 1 | 0.316 | −0.7854 |\n| 121 | [ ] | −804.6286 | 14.1712 | 0.0000 | 1 | 0.600 | −0.9578 |\n| 123 | [ ] | −715.6656 | 13.0397 | 0.0000 | 1 | 0.667 | −0.9200 |\n| 125 | [ ] | −626.5662 | 18.2131 | 0.0000 | 1 | 0.733 | −0.7457 |\n| 132 | [ ] | −998.6407 | 14.8818 | 0.0000 | 1 | 0.455 | −0.9513 |\n| 66 | [ 13] | −692.2129 | 10.5534 | 0.0055 | 1 | 0.684 | −0.8686 |\n\nStatement: 0.000 is the value of 97 ID under Y.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd53a6da97f",
  "kind": "yes/no",
  "text": "Customer: Yes, please 5 people for 5 nights on Saturday.\nAssistant: Have you booked, 9L1SUXC3 is your confirmation. Anything else?",
  "question": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q1552c5698a",
  "kind": "yes/no",
  "text": "Statement 1: oil can be found in the sky\nStatement 2: oil can be found in the underground",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q7a98363968",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nIndeed, patients with COVID-19 are at accelerated risk for delirium due to at least seven factors including (1) direct central nervous system (CNS) invasion, (2) induction of CNS inflammatory mediators, (3) secondary effect of other organ system failure, (4) effect of sedative strategies, (5) prolonged mechanical ventilation time, (6) immobilization, and (7) other needed but unfortunate environmental factors including social isolation and quarantine without family.\n\nClaim: COVID-19 patients experience no significant risk factors for delirium during their treatment.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qb540dee67c",
  "kind": "yes/no",
  "text": "Situation: I dislike my cat and also scared of him.\nAction being judged: Finding your pet a new home if you don't like them.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "qd4ea20d9f0",
  "kind": "yes/no",
  "text": "Assistant: Perfect, It looks like it's going to be about $25 to get everyone to Megan's house. Since you live right down the road it shouldn't cost too much more. I'll get it set up for you now.\nCustomer: Great! Tell them to hurry, these girls are getting rowdy.\nAssistant: They are on the way, should be to you in four minutes.",
  "question": "According to the assistant's last message, is \"four minutes\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q47cc6ac22f",
  "kind": "yes/no",
  "text": "Table caption: Pearson correlation coefficients (μ) for (Ta,W) and (Ta,W):C thin films in the as-deposited state as well as after annealing at 900 °C.\n|  | (Ta,W) | (Ta,W) | (Ta,W):C | (Ta,W):C |\n|  | as dep. | 900 °C ⁎ | as dep. | 900 °C |\n| μ Ta | 0.06 | N/A | 0.05 | 0.05 |\n| μ W | 0.06 | N/A | 0.03 | 0.06 |\n| μ C | – | – | 0.04 | 0.39 |\n\nStatement: Ta has the lowest value for 900 C of 0.05.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1aa117b4e2",
  "kind": "yes/no",
  "text": "Customer: Could you try an hour earlier, then?\nAssistant: Certainly. You now have a table for your party of 8 at the Curry Garden, at 16:45. Your reference number is V24OGNJB.",
  "question": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q60a12e53e4",
  "kind": "yes/no",
  "text": "Statement 1: a dog is taken to a pool after getting sick\nStatement 2: a dog is taken to a veterinarian after getting sick",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qb123a46e1b",
  "kind": "yes/no",
  "text": "Situation: He pulled her aside after class and asked her.\nAction being judged: Waiting until after class to socialize.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "qe580a2a9b8",
  "kind": "yes/no",
  "text": "Table caption: The number of views depending on the rating.\n| responses_rating_grade | views |\n| 1.0 | 1192.8 |\n| 2.0 | 1278.9 |\n| 3.0 | 1391.4 |\n| 4.0 | 1169.8 |\n| 5.0 | 990 |\n\nStatement: Rating grade 5.0 has less number of views.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb59e9eb97e",
  "kind": "yes/no",
  "text": "Situation: I'm a hotel cleaner and this what I did to a guest.\nAction being judged: Doing things that others would find gross.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q9966f26de3",
  "kind": "yes/no",
  "text": "Customer: I am looking for a cheap place to stay in the east part of town.\nAssistant: No problem. We have 3 guesthouses that match that. Do you have a further preference?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qc6a36e0dc5",
  "kind": "yes/no",
  "text": "Occupation: Nannies\nDuties:\n- Observe participants and inform them of corrective measures necessary for skill improvement.\n- Instruct participants in maintaining exertion levels to maximize benefits from exercise routines.\n- Offer alternatives during classes to accommodate different levels of fitness.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q30d4d08368",
  "kind": "yes/no",
  "text": "Statement 1: Sarah put cats in the fridge.\nStatement 2: Sarah put tuna salad in the fridge.",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q838dc7267f",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2014 FORD C-MAX ENERGI. THE CONTACT STATED THAT THE VEHICLE WAS PLUGGED IN AND RECHARGING IN THE GARAGE. TWO HOURS LATER, AN EXTENSIVE FIRE ERUPTED FROM THE CHARGE CORD. THE FIRE DEPARTMENT WAS ABLE TO EXTINGUISH THE FLAMES. THE DEALER TESTED THE VEHICLE AND STATED THAT THE CHARGE CORD OVERHEATED. THE MANUFACTURER WAS NOTIFIED OF THE FAILURE AND SENT A TECHNICIAN, BUT WAS NOT ABLE TO DETERMINE THE SPECIFIC CAUSE OF THE FAILURE. THE VEHICLE WAS INSPECTED BY A DEALER AND THE INSURANCE ADJUSTER. THE COSMETIC DAMAGES WERE REPAIRED, BUT THE CONTACT WAS UNABLE TO DETERMINE IF THE FAILURE WOULD RECUR. THE VIN AND FAILURE MILEAGE WERE NOT AVAILABLE.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q733ee29e77",
  "kind": "yes/no",
  "text": "Customer: A cheap jamaican restaurant, please. If you cannot find one, then mediterranean.\nAssistant: There are no Jamaican restaurants listed. I will look for Mediterranean.",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qd8f5668d21",
  "kind": "yes/no",
  "text": "Complaint narrative: ISSUES JERKING AND HARD SHIFTING WHILE DRIVING. CAR LURCHES FORWARD AND MOVES IN JERKY MOVEMENTS. ALMOST CAUSED AN ACCIDENT BECAUSE VEHICLE STALLED THEN LURCHES FORWARD HARD.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q1d62642eec",
  "kind": "yes/no",
  "text": "Complaint narrative: FOLLOWING A SPONTANEOUS FIRE THAT CAUSED OUR JEEP TO BE IN FOR REPAIR FROM 11/9/18 TO 1/19/19, ALMOST IMMEDIATELY, THE JEEP BEGAN TO EXPERIENCE BRAKE PROBLEMS. ON JANUARY 24, 2019 (ONLY 5 DAYS AFTER A 10-WEEK REPAIR AT THE JEEP DEALERSHIP), OUR SON ADVISED ME THAT THE 'HILL ASSIST SERVICE' LIGHT WAS COMING ON MULTIPLE TIMES A DAY. I PHONED BRIAN CASWELL AT SHELOR IN CHRISTIANSBURG, VA WHO ADVISED ME TO HAVE OUR SON RETURN THE JEEP TO THE DEALERSHIP WHICH HE DID ON JANUARY 25, 2019. BRIAN CALLED ME ON JANUARY 29, 2019 AND ADVISED THAT THEY WOULD BE DOING A WARRANTY REPAIR ON THE BRAKE LIGHT SWITCH. BRIAN ALSO ADVISED OUR SON THAT THE JEEP HAD TO BE TOWED WHILE PARKED ON THE SHELOR LOT BECAUSE OF THE BRAKE ISSUE, SO IT IS FORTUNATE THAT OUR SON MADE IT FROM BLACKSBURG TO CHRISTIANSBURG, VA WITHOUT AN ACCIDENT. OUR SON PICKED UP THE JEEP ON JANUARY 30, 2019. HOWEVER, WHEN DRIVING THE CAR BACK TO HIS APARTMENT, THE SAME \"HILL START ASSIST\" LIGHT CAME ON AND SO THE CAR WAS NOT DRIVABLE AGAIN. (THIS IS THE 3RD SAFETY INCIDENT WITH THIS VEHICLE IN 3 MONTHS. - ONE RELATED TO A FIRE AND THE SECOND AND THIRD DUE TO BRAKE ISSUES.) BRIAN SENT A TOW TRUCK ON JANUARY 31, 2109 TO BRING THE JEEP BACK TO SHELOR. I ALSO SENT AN EMAIL FROM THE JEEP WEBSITE TO THE FCA USA CUSTOMER CARE CENTER ON JANUARY 31, 2019 ' CLAIM NUMBER 57935124. SINCE THEN, I HAVE ALSO SPOKEN SEVERAL TIMES WITH STEVE STANDER IN THE FCA CORPORATE OFFICE IN WARREN, MI. ON FEBRUARY 4, 2019, BRIAN ADVISED ME THAT THE ANTI-LOCK BRAKE SYSTEM MODULE NEEDS TO BE REPAIRED, AS THIS IS THOUGHT TO BE THE SOURCE OF THE RECURRING BRAKE PROBLEM. THE CAR SUPPOSEDLY IS NOW REPAIRED AS OF 2/7/19 BUT WE WILL FIND OUT IF IT THIS IS THE CASE WHEN MY SON PICKS IT UP IN A DAY OR SO.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qefae866c39",
  "kind": "yes/no",
  "text": "Customer: I think it would be fun to go to see a movie tonight.\nAgent: Sure. What movie would you like to see?\nCustomer: What's playing at the Boulevard 14 Cinema in Petaluma, California since that would be the closest theater.\nAgent: OK. Boulevard 14 Cinema in Petaluma, California is showing three movies: No Time To Die, Mulan, and Emma.\nCustomer: Do you know anything about the movie?\nAgent: Sure. What specifically would you like to know?\nCustomer: What is the story about?\nAgent: OK. Here’s the synopsis of Mulan: Accompanied by her dragon, Mushu, Mulan uses her smarts to help ward off a Hun invasion, falling in love with a dashing captain along the way.\nCustomer: It sounds like it might be good. Did it get good reviews from both critics and the audiences?\nAgent: Mulan has an 87% Rotten Tomatoes score and a 92% audience rating.\nCustomer: Mulan sounds ok, but I think I'd rather see No Time to Die.\nAgent: OK. No Time To Die is playing 4:00pm, 7:30pm, and 10:55pm. Which time would you like?\nCustomer: We would like to go to the 10:55 pm show and it'll be just my friend and I.\nAgent: All right. Let me confirm that you’d like two tickets for No Time To Die at Boulevard 14 Cinema tonight at 10:55pm. Is that all correct?\nCustomer: Yes, that's correct.\nAgent: Is it OK to go ahead and purchase these tickets?\nCustomer: Yes.\nAgent: OK. Your tickets are purchased and details for how to proceed have been sent to your email address. Can I help with anything else?\nCustomer: I'm not familiar with your email confirmation. How does that work?\nAgent: The email will provide up to three options for your tickets: print at home, electronic tickets, or an option to pick them up at the theater.\nCustomer: Thank you for explaining that to me.\nAgent: OK. Enjoy your movie!",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q8a1de92356",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- On feast days and at the graveside during burial of members of the community, the monastic community sings the hymn of the American-Cassinese Congregation known as the \"\"Ultima\"\".\n\nSummary sentence:\nThe abbey is a member of the American-Cassinese Congregation of the Benedictine Confederation.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qff547432a1",
  "kind": "yes/no",
  "text": "Statement 1: I put the vegetables in hot oil\nStatement 2: I put my hand in the hot oil",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qe72b886284",
  "kind": "yes/no",
  "text": "Statement 1: She worried about getting bored at the dark cabinet.\nStatement 2: She worried about getting bored at the dark cabin.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 }
]
