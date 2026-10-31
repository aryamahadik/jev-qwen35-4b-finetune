# G5-H blind read T37b-blind_read-f7b7ff97-001 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3_qc6/g5h/answers/T37b-blind_read-f7b7ff97-001.json

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
  "qid": "qd3e91a794d",
  "kind": "yes/no",
  "text": "Assistant: the fare for Uber xl for this ride right now is $8, a bout $2 higher than the other one\nCustomer: that is just fine\nAssistant: the ride is booked and it should be there in 30 minutes as you requested, you can check the status on your phone",
  "question": "Is \"30 minutes\" for the customer's ride booking confirmed in the final message from the assistant?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf3c07b910b",
  "kind": "yes/no",
  "text": "Customer: Hello Siri!\nAgent: Hello. What can I do for you today?\nCustomer: I need to purchase some movie tickets for tomorrow night.\nAgent: Ok. What movie are you wanting to go see?\nCustomer: We want to see \"Uncut Gems\".\nAgent: Ok. What theater do you want to see the movie at?\nCustomer: We want to go to the AMC NorthPark 15 in Dallas, TX.\nAgent: OK. It looks like they have a showing at 12:05PM tomorrow. That is the only showing.\nCustomer: Ok. We will not be able to go that early. Can you see if the movie is showing tomorrow at the Alamo Drafthouse Cedar in Dallas, TX?\nAgent: Ok. It looks like they do have a 6:05PM showtime for \"Uncut Gems\" tomorrow night.\nCustomer: Ok great. Do they have Reclining seats in that theater?\nAgent: Yes, they do have reclining seats in that theater.\nCustomer: Great. Can you order these tickets for and charge them on my PayPal account?\nAgent: Sure. Just to confirm...you want 2 tickets to see \"Uncut Gems\" tomorrow night at the 6:05 showing at the Alamo Drafthouse Cedar in Dallas, TX?\nCustomer: Yes, that is correct.\nAgent: OK. I have these purchased for you. They will be waiting for you in will call.\nCustomer: Thank you Siri!\nAgent: No problem. Is there anything else I can do for you?\nCustomer: No that is all. Goodbye!\nAgent: Goodbye!",
  "question": "By the end of this conversation, is there actually a purchase of movie tickets by the customer?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qd799703466",
  "kind": "yes/no",
  "text": "Situation: My Mom &amp; Son broke in my place??\nAction being judged: People assuming they're allowed entry into the houses of people, even when they're family.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qa314715aa9",
  "kind": "yes/no",
  "text": "Assistant: Great. I'll book it right now.\nCustomer: Perfect.\nAssistant: It appears there are no Select cars currently available.",
  "question": "Is \"Select\" confirmed for the customer's ride booking, according to the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q95386524ed",
  "kind": "yes/no",
  "text": "Assistant: Looks like 8:30 PM works as well! Did you want me to book this?\nCustomer: Yes, please!\nAssistant: Okay! 8:30 PM is booked!",
  "question": "Going by the assistant's latest message, is \"8:30 PM\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q40fc9c0444",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nHowever, encephalopathy was independently associated with worse functional outcome (OR 0.22; 95% CI 0.11–0.42; P < 0.001) and higher mortality within 30 days of hospitalization (35 [21.7%] vs. 11 [3.2%] patients; P < 0.001). Encephalopathy was associated with increased morbidity and mortality, independent of respiratory disease severity.\n\nClaim: Confusion, delirium and other types of altered mental function, called encephalopathy, have occurred during hospitalization for Covid-19 respiratory problems, and a study found that such patients fared better right after hospitalization.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q389a26dad3",
  "kind": "yes/no",
  "text": "The worlds climate scientists are almost all employed by western governments. They usually dont pay you to do climate research unless you say you believe manmade global warming is dangerous, and it has been that way for more than 20 years. The result is a near-unanimity that is unusual for a theory in such an immature science.",
  "question": "Based on the text, does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q09db484afe",
  "kind": "yes/no",
  "text": "Complaint narrative: I PURCHASED A PRE-OWNED 2010 BMW 750LI BACK IN NOVEMBER 2012. AS SOON AS I DROVE IT OFF THE BEVERLY HILLS BMW LOT, I GOT A CHECK ENGINE LIGHT GO OFF. BEVERLY HILLS WROTE IT OFF AS IT WAS THE GAS SENSOR BEING SENSITIVE. FOUND OUT LATER IT WAS THE FUEL INJECTORS THAT WENT BAD ON A CAR WITH 23,000 MILES ON. FAST FORWARD 2 YEARS LATER AND 30,000 MILES, WITH MULTIPLE STOPS AT STERLING BMW AND MY COMPLAINTS OF HAVING TO PUT QUART OF OIL INTO THE ENGINE EVERY 2000 MILES. FOR 2 YEARS, STERLING ADVISED ME IT WAS NORMAL FOR THIS TYPE OF ENGINE TO CONSUME THAT MUCH OIL AND FOR ALL THE OTHER ENGINE PROBLEMS. I HAVE BROUGHT THE CAR IN FOR OVER 6 TIMES (EVER OTHER MONTH ALMOST) TO THE DEALER TO FIX NUMEROUS PROBLEMS WITH THE ENGINE (NOT NORMAL WEAR AND TEAR). THEN COMES THE \"RECALL\" BMW CALLS THE \"COMFORT CARE PACKAGE\" AND WAS PROMISED IT WOULD RESOLVE THE OIL CONSUMPTION WITH BETTER PERFORMANCE IN JANUARY 2015. AFTER THE RECALL, MY ENGINE REQUIRED OIL EVERY 500 MILES AND WHEN I BROUGHT IT BACK TO BMW IN APRIL 2015, THEY ADVISED ME IT WAS A HOSE LEAK AND OIL WAS DRIPPING DOWN TO EXHAUST CAUSING EXCESS SMOKE FROM THE EXHAUST. NOW BMW OF NORTHERN AMERICA TELLS ME THEY DON'T COVER THE REPAIR BECAUSE IT WAS OUR OF WARRANTY DESPITE MY COMPLAINTS (WHICH HAVE BEEN DOCUMENTED BY STERLING FOR 2 YEARS). THE COMFORT CARE PACKAGE MADE MY OIL LEAK WORST AND INTO THE EXHAUST AND BMW REFUSES TO REPAIR THE PROBLEM OR EVEN REMOVE THEIR COMFORT CARE PACKAGE. IT'S BEEN MORE THEN 2 YEARS SINCE I AND MY 2 YEAR OLD DAUGHTER HAVE BEEN BREATHING IN THIS EXCESS SMOKE FROM MY EXHAUST WHICH BMW REFUSES TO REPAIR. THIS ENGINE IS A COMPLETE LEMON.",
  "question": "Does this vehicle safety complaint say the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qc353eb0315",
  "kind": "yes/no",
  "text": "Customer: I am looking for a restaurant that is in the cheap price range and in the east part of town.\nAssistant: The Missing Sock serves cheap food in the east part of town.",
  "question": "Did the assistant find at least a single option in its reply that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q4e1159c4f9",
  "kind": "yes/no",
  "text": "Customer: I would like eritrean, please.\nAssistant: I'm very sorry there are no restaurants that serve eritrean food in the centre area. Is there another type of cuisine we can look for?",
  "question": "Is there confirmation that, in its reply, the assistant found at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q43a1f3675a",
  "kind": "yes/no",
  "text": "Jasper Kirkby of CERN has published a new paper examining the potential link between cosmic rays and climate.",
  "question": "Based on the text, does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qafaca7ae06",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nINTERPRETATION: During the first wave of the COVID-19 pandemic, fewer than 10% of the US adult population formed antibodies against SARS-CoV-2, and fewer than 10% of those with antibodies were diagnosed.\n\nClaim: In blood samples from the first wave of the COVID-19 pandemic in the US, the majority of samples contained antibodies to the virus.",
  "question": "Does that evidence support that claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qa4a877c290",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2012 DODGE CHARGER. WHILE DRIVING APPROXIMATELY 60 MPH, THE VEHICLE STARTED TO DECELERATE. THE CONTACT COASTED TO THE SIDE OF THE ROAD. THE VEHICLE WAS TOWED TO THE CONTACT'S RESIDENCE. WHILE THE VEHICLE WAS PARKED, THE ENGINE CAUGHT FIRE. THE VEHICLE WAS TOWED TO THE DEALER WHERE IT WAS DIAGNOSED THAT A FAULTY THERMOSTAT MELTED ONTO THE ENGINE AND BURNED. THE ENGINE NEEDED TO BE REPLACED. THE VEHICLE WAS NOT REPAIRED. THE MANUFACTURER WAS MADE AWARE OF THE FAILURE. THE FAILURE MILEAGE WAS APPROXIMATELY 60,000. THE VIN WAS NOT AVAILABLE.",
  "question": "Is it right to say that this vehicle safety complaint does not report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "qd75fc3a0d6",
  "kind": "yes/no",
  "text": "Customer: Any price range will be fine.\nAssistant: I have no steakhouse in the east area, but The River Bar Steakhouse and Grill is located in the centre area.",
  "question": "In the response the assistant gave, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qe216e5e001",
  "kind": "yes/no",
  "text": "The results just presented beg the following question: If the satellite data indicate an insensitive climate system, why do the climate models suggest just the opposite? I believe the answer is due to a misinterpretation of cloud behavior by climate modelers.",
  "question": "Does this paragraph set forth the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q7bbe25e0ba",
  "kind": "yes/no",
  "text": "Assistant: OK, how about tomorrow at 8am?\nCustomer: Yes, perfect!\nAssistant: Ok you are all set for tomorrow at 8am to get your tire checked out",
  "question": "Would it be correct to say that, according to the assistant's last message, \"tomorrow\" is not confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order.\n- no: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction."
 },
 {
  "qid": "q70c1ff20df",
  "kind": "yes/no",
  "text": "Table caption: Current status of the line positions of the ν 4 band and the ν 3 +ν 4 -ν 3 hot band of CH 3 I in the C-H stretch region.\n| Technique |  |  | ν 4 | ν 4 | ν 3 +ν 4 -ν 3 | ν 3 +ν 4 -ν 3 |\n|  | Point spacing | Ref. | Assignments | Std. dev./cm -1 | Assignments | Std. dev./cm -1 |\n| FT-IR | 150 MHz | [19] | 500 | 0.005 | – | – |\n| FT-IR | 162 MHz | [20] | 1850 | 0.00083 | 380 | 0.0013 |\n| Comb-FTS | 11 MHz | This work | 2603 | 0.00034 | 831 | 0.00084 |\n\nStatement: The highest Assignments is 2603.",
  "question": "Does the table back up the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3da8129051",
  "kind": "yes/no",
  "text": "Situation: I'm 30 years old &amp; I've never had a job or driven anywhere.\nAction being judged: Not being a responsible adult and grow up.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qd126a47dfb",
  "kind": "yes/no",
  "text": "Laboratory experiments find that more marine creatures thrive than suffer when carbon dioxide lowers the pH level to 7.8. This is because the carbon dioxide dissolves mainly as bicarbonate, which many calcifiers use as raw material for carbonate.",
  "question": "Within this paragraph, does it make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q9f7d2cd924",
  "kind": "yes/no",
  "text": "Customer: Hi! How are you?\nAgent: I am good. What can I help you with?\nCustomer: I am looking to purchase tickets to get see a movie.\nAgent: I understand. Are there any particular movies that you want to see?\nCustomer: None in particular. I just want to see what my options are.\nAgent: Okay. What is your location?\nCustomer: I am on assignment in a Seven Trees, Nebraska.\nAgent: Okay, I have Holiday Cinemark 12 which is 30 miles away from you in the town of Butte Crest.\nCustomer: 30 miles? Is there anything closer than that?\nAgent: Mountain AMC 16 which is 22 miles away in the town of North Fork is the only theater that is closer.\nCustomer: So the closest theater is 22 miles away from me?\nAgent: Yes, that is correct.\nCustomer: That is too far. I am not going to drive that distance to see a movie.\nAgent: There is nothing closer to Seven Trees, Nebraska at this moment. I apologize.\nCustomer: Okay, I am not going to go to the movies then. Thank you anyways.\nAgent: You are welcome.",
  "question": "Has the customer actually bought movie tickets by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q70693710fc",
  "kind": "yes/no",
  "text": "(At the same time, as another paper makes clear, \"some\" U.N. peacekeepers come from countries \"where the armed forces and police are seriously implicated in human rights violations,\" including sexual crimes. While such actions \"cannot be tolerated,\" the paper makes clear the U.N. has no clear answers on how to police its own behavior.)",
  "question": "Is it true that this paragraph doesn't make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable.\n- no: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy."
 },
 {
  "qid": "q26af080dfc",
  "kind": "yes/no",
  "text": "Customer: Yes. Are any of those restaurants in the centre of town?\nAssistant: Yes, there are three restaurants serving Turkish food in the center of town.",
  "question": "In its reply, did the assistant find at least a single option meeting everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q1f0bb63146",
  "kind": "yes/no",
  "text": "Table caption: Distance statistics to investigate the changes in the spatial distribution among ancient buildings, modern buildings and their spatial clustering centers (unit: meter).\n| Index | Ancient building | Modern building |\n| AVERAGE | 106.996 | 190.761 |\n| STDEV.S | 72.664 | 112.324 |\n| MIN | 5.930 | 7.634 |\n| MAX | 308.987 | 505.028 |\n| MEDIAN | 80.988 | 158.405 |\n\nStatement: Ancient building Average meter is 106.996.",
  "question": "Based on the table, is the statement supported?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q6d506c0e4f",
  "kind": "yes/no",
  "text": "Customer: I need a place to stay in the East. I don't need to have access to the Internet.\nAssistant: I have 7 places available in the east.  What is your price range?",
  "question": "According to the assistant's reply, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q7b76f446db",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- On feast days and at the graveside during burial of members of the community, the monastic community sings the hymn of the American-Cassinese Congregation known as the \"\"Ultima\"\".\n\nSummary sentence:\nThe abbey is a member of the American-Cassinese Congregation of the Benedictine Confederation.",
  "question": "Do the evidence sentences support every piece of information in the summary sentence?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q5adeb9e697",
  "kind": "yes/no",
  "text": "Customer: You're right. I forgot to select an architectural sight that I wanted to visit. Could you suggest one in the city centre.\nAssistant: Sure thing. I would suggest the old schools.",
  "question": "In its reply, did the assistant find at least a single option that fits everything the customer requested?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qb0f8cdcd8b",
  "kind": "yes/no",
  "text": "Customer: Yes, I was hoping for Austrian food.\nAssistant: There is not an expensive Austrian restaurant in the area. Is there another cuisine you'd like to try?",
  "question": "In its reply, did the assistant find at least a single option that fits everything the customer requested?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q58d6fec357",
  "kind": "yes/no",
  "text": "Table caption: Daily (1-day), 3-days, and 5 days average Lot Turnover (LT) for portfolio with two different lot sizes.\n| Estim- | 1-day LT | 1-day LT | 3-days LT | 3-days LT | 5-days LT | 5-days LT |\n| ator | 100 | 500 | 100 | 500 | 100 | 500 |\n| MLE | 128.34 | 18.64 | 152.39 | 21.46 | 143.13 | 20.21 |\n| MCD | 133.94 | 14.23 | 128.85 | 13.59 | 146.38 | 13.96 |\n| S | 121.52 | 16.85 | 124.43 | 15.14 | 126.09 | 15.61 |\n| MM | 129.27 | 21.33 | 135.00 | 17.71 | 128.05 | 19.62 |\n| OGK | 134.24 | 19.12 | 140.74 | 20.55 | 145.14 | 21.66 |\n\nStatement: S Estim will have same value Lot turnover for all the days.",
  "question": "Is it correct that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q7ec9d7773e",
  "kind": "yes/no",
  "text": "Customer: Yes, book it for 4 people and 4 nights starting from tuesday.\nAssistant: The booking was unsuccessful. would you like another day or a shorter stay?",
  "question": "Does the assistant's reply verify that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "qbc06c4d5c4",
  "kind": "yes/no",
  "text": "Customer: Are there any 2-star hotels (not guesthouses) in the south that have free parking?\nAssistant: No, I'm sorry there aren't any hotels that meet that criteria. Would you like to try a different area?",
  "question": "In its reply did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q47c749c3ea",
  "kind": "yes/no",
  "text": "Customer: Hey, how are you?\nAgent: Well, how can I help you?\nCustomer: I would like to see a movie tonight i think\nAgent: sure, is anyone going with you?\nCustomer: just my girlfriend and brother\nAgent: great, what would you like to see?\nCustomer: the Boy 2, or Bad boys would be good\nAgent: Okay, is there any particular theater you would like to go to?\nCustomer: I like Regal or AMC\nAgent: Okay, is there a specific time you would like to go?\nCustomer: I think anywhere from 7-8 would be good\nAgent: okay, one second let me check\nCustomer: sure thing, take your time\nAgent: okay, I am checking for the boy 2 and see no results\nCustomer: shucks, can you check for bad boys then?\nAgent: sure thing, let me see\nCustomer: okay, hopefully they have something....\nAgent: okay, bad news, there is nothing for that either\nCustomer: okay, I guess it is not in the cards for tonight, thank you anyways\nAgent: not a problem, any time!",
  "question": "Have movie tickets actually been bought by the customer by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q358092bf6f",
  "kind": "yes/no",
  "text": "Table caption: Peptides from L. fermentum HFD1 with predicted antimicrobial activity\n| № | The protein ID | Peptide sequence | ADAM | CAMPR3 | CAMPR3 | CAMPR3 | AMPA |  | Length in peptidome |\n| № | The protein ID | Peptide sequence | ADAM | SVM | Random Forest | DAC | AMPA | Length | Length in peptidome |\n| 1 | QIX58482.1 | MGLIWSLIVGAIIGAIAGAITNRGAAMGWIANIVAGLIGAWIGQGLLGTWGPSLAGMALIPSIIGAIILVLIVSLVVGRTGKK | 1.52 | 1.0 | 0.566 | 0.527 | 0.24 | 84 | 14 |\n| 2 | QIX58771.1 | MLSLITNTVIILLIIGCAFWQLVKVFKRAKKGKCAACDYDCAVKQQVLKQEKHGAQ | 0.82 | 0.889 | 0.6715 | 0.81 | 0.2226 | 56 | N/A |\n| 3 | QIX58909.1 | MAVKIKTPAGMIDIANDVIATVVGGAATDNYGVVGMASRNPLKDGVNQILGRDSFHQGVVIRQQDNGIAVDVYIIVGYGTKISAVSKSVQEKVKYNLEAMLGVTANSVNIMVQGVRVLGD | 0.09 | 1.00 | 0.9855 | 1.0 | 0.248 | 120 | N/A |\n| 4 | QIX58994.1 | MNNQSNVTPQNGNLQYKFCQNCGAKIDVKAVVCPKCGVPVNGNNAESNSEDRNNGWWNLLGFFFPIVGWILWAVWHKEYPKRAHGICVWSWVSFGISFVIGFVNGFLSTL | 1.32 | 1.00 | 0.7745 | 1.0 | 0.237 | 110 | N/A |\n\nStatement: The protein ID QIX58482.1 has Peptide sequence of MNNQSNVTPQNGNLQYKFCQNCGAKIDVKAVVCPKCGVPVNGNNAESNSEDRNNGWWNLLGFFFPIVGWILWAVWHKEYPKRAHGICVWSWVSFGISFVIGFVNGFLSTL.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q5565284adf",
  "kind": "yes/no",
  "text": "Complaint narrative: THE FUSE BOX IS GETTING MOISTURE CAUSING HEADLIGHTS NOT TO WORK PROPERLY AND NO FUSES OR RELAYS CAN BE CHANGED BECAUSE THEY ARE CORRODED IN THE BOX. CAR LOSES POWER, RADIO CAUGHT FIRE, DOORS LOCK ON THERE OWN OR DON'T LOCK AT ALL, MAJOR MALFUNCTION OF ALL ELECTRICAL COMPONENTS. 2011 AND 2013 WERE RECALLED FOR THIS ISSUE. WHY WASN'T 2012? CAR HAS ISSUES WHILE DRIVING AND IT'S GOING TO CAUSE AN ACCIDENT IF NOT TAKEN CARE OF.",
  "question": "Did the vehicle actually catch fire, according to this vehicle safety complaint?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q0d10cc732a",
  "kind": "yes/no",
  "text": "Labor to introduce register for foreign ownership of land | The Area ...",
  "question": "Does this paragraph put forward the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q10f0c60077",
  "kind": "yes/no",
  "text": "Statement 1: Plato is a man, and all philosophers are men, therefore Plato is a philosopher\nStatement 2: Plato is a philosopher, and all philosophers are men, therefore Plato is a man.",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q4ead1080f6",
  "kind": "yes/no",
  "text": "Customer: I want to watch a movie\nAgent: in theater or at home?\nCustomer: in theater\nAgent: do you have a movie in mind?\nCustomer: there are a few\nAgent: such as\nCustomer: ip man, star war, bad boys and a few others\nAgent: do you have a favorite\nCustomer: I don't have a favorite but I do want to watch star war, as well as ipman but I heard ipman may not be playing everywhere\nAgent: the review for ipman 4 is quite good just like the other threes\nCustomer: I always like that series, star war is ok too as I want to see its ending\nAgent: have we decided on a movie yet\nCustomer: if there is a showtime for ipman at landmark 81, book it, otherwise star war\nAgent: there is no ipman playing there, only starwar\nCustomer: then get me two tickets for 3d at 9 pm on saturday in 3d\nAgent: having a date sir?\nCustomer: sort of\nAgent: so 2 tickets for star war at 9 pm this Saturday in 3d\nCustomer: yes, but wait till I double check the schedule with my date\nAgent: all righty\nCustomer: thank you",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q8576bcff1b",
  "kind": "yes/no",
  "text": "Occupation: Fire-Prevention and Protection Engineers\nDuties:\n- Design or direct nuclear research projects to develop, test, modify, or discover new uses for theoretical models.\n- Direct environmental compliance activities associated with nuclear plant operations or maintenance.\n- Direct operating or maintenance activities of nuclear power plants to ensure efficiency and conformity to safety standards.",
  "question": "Does the job of the occupation named above include the listed duties?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q5367dc9daf",
  "kind": "yes/no",
  "text": "Customer: I think I'd like to see a movie tonight.\nAgent: Sounds like a plan. Which movie do you want to see?\nCustomer: I think I'll take my daughter to see Sonic the Hedgehog tonight.\nAgent: So, just two tickets?\nCustomer: Yes, just two standard tickets.\nAgent: Which theater were you thinking of seeing it at?\nCustomer: What are the times for Philadelphia Mills AMC?\nAgent: There's a 5:15 PM and a 7:15 PM showing.\nCustomer: That's not much of an option. What about Woodhaven AMC?\nAgent: The showtimes for this evening are 4:45 PM, 6:30 PM, 7:00 PM, 7:30 PM, 9:15 PM, 9:45 PM and 10:15 PM.\nCustomer: 6:30 PM is fine.\nAgent: Okay, so two tickets tonight at Woodhaven AMC for Sonic the Hedgehog at 6:30 PM?\nCustomer: Actually, now that I think about it, 6:30 PM might not work.\nAgent: Would you like the showtimes for a different theater?\nCustomer: No, Woodhaven AMC is fine. I think I'll make it for 7:30 PM instead.\nAgent: So, 7:30 PM instead of 6:30 PM?\nCustomer: Yes.\nAgent: I'll book two tickets tonight for Sonic the Hedgehog at Woodhaven AMC for 7:30 PM?\nCustomer: That's correct.\nAgent: You'r tickets are booked and the confirmation has been emailed to you.",
  "question": "By the end of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qd0e52503db",
  "kind": "yes/no",
  "text": "Customer: Yes, please book starting Thursday for 4 people and for 4 nights.\nAssistant: I'm sorry, there were no rooms available. Would you like to find another hotel?",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "qb5b630dc36",
  "kind": "yes/no",
  "text": "Table caption: The categories inventoried as industrial process emissions.\n| Sub-sector | Sub-sub-sector ( a NFR code) |\n| Mineral products | Cement production (2.A.1) Lime production (2.A.2) Asphalt roofing (2.D.3.c) Asphalt road paving (2.D.3.b) |\n| Chemical industry | Ammonia (2.B.1) Nitric acid (2B.2) Adipic acid (2.B.3) Carbon black (2.B.10.a) Urea (2.B.10.a) Ammonium nitrate (2.B.10.a) Ammonium phosphate (2.B.10.a) Sulphuric acid (2.B.10.a) Titanium dioxide (2.B.6) |\n| Metal production | Pig iron production (1.A.2.a) Aluminium production (2.C.3) Copper smelting (primary and secondary) (2.C.7) Lead smelting (primary and secondary) (2.C.5) Zinc smelting (primary and secondary) (2.C.6) |\n| Pulp and Paper Industries | Kraft or Alkaline soda pulping (2.H.1) Acid sulphite pulping (2.H.1) Neutral sulphite semi-chemical (2.H.1) |\n| Food and Drink | Alcoholic Beverages (2.H.2) Food Production (2.H.2) |\n| Fugitive emissions of PM from major construction activities |  |\n\nStatement: They have six sub sector.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q9c32be5950",
  "kind": "yes/no",
  "text": "Customer: Please list movies currently showing in San Diego California:\nAgent: The top movies in San Diego today are 'Bad Boys For Life', 'The Rise of Skywalker', '1917', and 'Jumanji, The Next Level' ...\nCustomer: What locations are showing '1917' in San Diego?\nAgent: The movie '1917' is playing at AMC Mission Valley, The Lot at Liberty Station, and UltraStar Cinemas Mission Valley.\nCustomer: Ok, what times does '1917' show at AMC Mission Valley?\nAgent: Standard showings of '1917' are playing at 7:30pm and 9:00pm.\nCustomer: Is '1917' playing on IMAX?\nAgent: 1917' is only playing on standard screens, there is no IMAX option available for this movie.\nCustomer: Ok, how much is the cost for two tickets to the 7:30pm showing of '1917' at AMC Mission Valley?\nAgent: Fandango lists adult tickets for the 7:30pm showing of '1917' at $17.00 each.\nCustomer: Ok, I would like to purchase two adult tickets to the 7:30pm showing of '1917' at AMC Mission Valley.\nAgent: Please confirm your selection of two tickets to the 7:30pm showing of '1917' at AMC Mission Valley 20 for January 20th, 2020. Your total will be $34.00. Say 'OK' to confirm.\nCustomer: Wait, I would like to change my selection... I would like to purchase two tickets to the 9:00pm showing of '1917' instead...\nAgent: No problem. Please confirm your selection of two tickets to the 9:00pm showing of '1917' at AMC Mission Valley 20 for for January 20th, 2020. Your total will be $34.00. Say 'OK' to confirm.\nCustomer: OK. Confirming selection.\nAgent: Please wait while your tickets are purchased...\nCustomer: OK. Thank you.\nAgent: You have purchased two tickets for '1917' at AMC Mission Valley for this evening, January 20th, 2020. Your total charge was $34.00. Your confirmation number is 125673.\nCustomer: Ok. Where will I pick up the tickets?\nAgent: Your tickets will be sent to your email inbox. The email on file for your account is ltestone@gmail.com. Is this correct?\nCustomer: Yes, that is correct.\nAgent: Please check your inbox for your tickets.\nCustomer: Thank you. That's all!\nAgent: Thank you for using virtual movie assistant. Enjoy your show.",
  "question": "Have movie tickets actually been bought by the customer by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qae21ec8dda",
  "kind": "yes/no",
  "text": "Customer: Thank you . I will also need the booking reference number.\nAssistant: Booking was successful.\nReference number is : XML9YIR2.",
  "question": "Was the booking the customer asked for actually made, as the assistant's reply confirms?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q180710ed2d",
  "kind": "yes/no",
  "text": "Situation: Glanced to my left and made eye contact with a lady\nAction being judged: Looking people in the eyes when you talk to them.",
  "question": "Is the action being judged wrong by common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q078d679e31",
  "kind": "yes/no",
  "text": "Drank too many 🍹 when I was in Thailand. Fucked me right up",
  "question": "Is it right to say that this post isn't hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "q2d8c733dc5",
  "kind": "yes/no",
  "text": "The problem would seem to be the methodologies engendered in treatment for a mix of urban and rural locations; that the adjustment protocol appears to accent to a warming effect rather than eliminate it. This, if correct, leaves serious doubt for whether the rate of increase in temperature found from the adjusted data is due to natural warming trends or warming because of another reason, such as erroneous consideration of the effects of urban warming.",
  "question": "Hey, does this paragraph say the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qbd2f171c57",
  "kind": "yes/no",
  "text": "Occupation: Roof Bolters, Mining\nDuties:\n- Control conveyors that run the entire length of shuttle cars to distribute loads as loading progresses.\n- Monitor loading processes to ensure that materials are loaded according to specifications.\n- Replace hydraulic hoses, headlight bulbs, and gathering-arm teeth.",
  "question": "Do the listed duties form part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q382738dffb",
  "kind": "yes/no",
  "text": "Complaint narrative: I WAS DIVING DOWN GRATIOT STREET IN SAGINAW MICHIGAN, IT WAS RAINING HEAVILY AND MY WINDSHIELD WIPER DECIDED TO STOP WORKING COMPLETELY. I LOST ALL VISIBILITY AND HAD PULLED OVER IMMEDIATELY TO AVOID CAUSING AN ACCIDENT. WHILE SITTING IN MY CAR WAITING FOR THE RAIN TO STOP I REALIZE THAT MY WINDSHIELD WIPER MOTOR WAS STILL WORKING, BECAUSE I COULD HEAR IT MOVING BACK AND FORTH. BUT MY WIPERS WERE NOT. I HAVE READ THAT THERE IS A PROBLEM WITH SOME OF THE HARD WEAR AND A LOT OF PRIOR YEARS HAVE BEEN RECALLED. I'VE ALREADY HAD TO REPLACE THE ENGINE IN THIS CAR, NOW ONLY TO FIND OUT THAT THIS CAR WITH IT FAULTY EQUIPMENT CAN POTENTIALLY CAUSE ME MY LIFE... I WILL NOT RECOMMEND THIS VEHICLE TO ANYONE.",
  "question": "Is there a report in this vehicle safety complaint that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q5a079cd653",
  "kind": "yes/no",
  "text": "It is important to understand why measures to attempt to mitigate CO2 emissions are always going to be unaffordable. First, as the California example demonstrates, regional mitigation measures do not noticeably change the global CO2 concentration. Therefore manmade radiative forcing is scarcely altered.",
  "question": "Is there an assertion in this paragraph of the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q875326865f",
  "kind": "yes/no",
  "text": "Customer: I need a restaurant that serves catalan food and it should be in the west.\nAssistant: Unfortunately, I'm not finding any Catalan restaurants in the west. Would you like me to look in other areas?",
  "question": "Did the assistant, in its reply, identify at least a single option that satisfies everything the customer requested?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q3c2264a38c",
  "kind": "yes/no",
  "text": "They made a little mistake though. Great Lakes ice extent was at an all-time record high for the date at the end of January.",
  "question": "For this paragraph, does it make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 }
]
