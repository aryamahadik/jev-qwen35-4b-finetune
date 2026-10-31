# G5-H blind read T37b-blind_read-0eb807ce-001 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_qc2/g5h/answers/T37b-blind_read-0eb807ce-001.json

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
  "qid": "qb0d47b013f",
  "kind": "yes/no",
  "text": "CEI's FOIA request details how the UN informed participants that it was motivated by embarrassing releases of earlier discussions (\"ClimateGate\" key among them) and, to circumvent the problem that national government transparency laws posed, the group itself.",
  "question": "Is this paragraph making the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qecb6ed068d",
  "kind": "yes/no",
  "text": "Customer: I'm looking for a restaurant that serves afghan food in the south\nAssistant: I have not found any, unfortunately. Would you like to try another area of town or cuisine?",
  "question": "In the response the assistant gave, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q3eb6961d01",
  "kind": "yes/no",
  "text": "Statement 1: She worried about getting bored at the dark cabinet.\nStatement 2: She worried about getting bored at the dark cabin.",
  "question": "Of these two statements, does Statement 2 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "qc6eef2576f",
  "kind": "yes/no",
  "text": "Customer: A cheap jamaican restaurant, please. If you cannot find one, then mediterranean.\nAssistant: There are no Jamaican restaurants listed. I will look for Mediterranean.",
  "question": "Did the assistant, in its reply, find for the customer at least a single option meeting everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qdb867a1c67",
  "kind": "yes/no",
  "text": "Occupation: Private Detectives and Investigators\nDuties:\n- Observe and document activities of individuals to detect unlawful acts or to obtain evidence for cases, using binoculars and still or video cameras.\n- Conduct private investigations on a paid basis.\n- Obtain and analyze information on suspects, crimes, or disturbances to solve cases, to identify criminal activity, or to gather information for court cases.",
  "question": "So, are the duties on the list part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q11d51a82d1",
  "kind": "yes/no",
  "text": "Customer: Hello.\nAgent: Hi, how may I assist you today?\nCustomer: I'd like to buy some movie tickets, please.\nAgent: Okay, what movie do you want to see?\nCustomer: I live in Stoneyford, Oregon, so can you check Mountain AMC 16?\nAgent: What movie do you want me to check for?\nCustomer: No Time to Die.\nAgent: That movie isn't available there, sorry.\nCustomer: What about 'Mulan'?\nAgent: Sorry, unavailable as well, actually that theater is temporarily closed right now.\nCustomer: Okay then can you check Holiday Cinemark 12?\nAgent: That theater doesn't have either of those movies showing either, it's temporarily closed as well.\nCustomer: Do any other theaters have 'No Time to Die' showings?\nAgent: I've checked and it seems that No Time to Die has had its release date postponed until Fall.\nCustomer: What about 'Mulan'?\nAgent: Release date's postponed until Fall as well, unfortunately, sorry.\nCustomer: That's okay.\nAgent: Is there anything else I could help you with today?\nCustomer: No, thanks for your help.\nAgent: Alright, have a wonderful day.",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q5186848cb8",
  "kind": "yes/no",
  "text": "Situation: One day he instructed us to write something untrue.\nAction being judged: Improving your writing skills by trying something new.",
  "question": "Is it accurate to say that the action being judged is not acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q19dfbd97f9",
  "kind": "yes/no",
  "text": "Occupation: Podiatrists\nDuties:\n- Teach or train medical staff regarding preventive medicine issues.\n- Direct or manage prevention programs in specialty areas such as aerospace, occupational, infectious disease, and environmental medicine.\n- Coordinate or integrate the resources of health care institutions, social service agencies, public safety workers, or other organizations to improve community health.",
  "question": "Are the enumerated duties included in the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q39d8b85c97",
  "kind": "yes/no",
  "text": "Customer: I am looking for a restaurant that serves Afghan food in the centre.\nAssistant: There are no Afghan restaurants in the centre of town.",
  "question": "According to its reply, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q54415c805f",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nHospitalizations were six times higher among patients with a reported underlying condition (45.4%) than those without reported underlying conditions (7.6%).\n\nClaim: Underlying conditions have no correlation with COVID-19 hospitalizations or deaths.",
  "question": "Is there support from the evidence for the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qa6dce97849",
  "kind": "yes/no",
  "text": "Occupation: Waiters and Waitresses\nDuties:\n- Take orders from patrons for food or beverages.\n- Clean tables or counters after patrons have finished dining.\n- Write patrons' food orders on order slips, memorize orders, or enter orders into computers for transmittal to kitchen staff.",
  "question": "Is it right to say that the listed duties aren't part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "q07dffbee69",
  "kind": "yes/no",
  "text": "Assistant: Yes, that will be my pleasure.\nCustomer: Thank you.\nAssistant: Okay, it is booked for you tonight at 7:30 PM for 4 at the Kati Roll Company in NYC.",
  "question": "Did the assistant's final message tell me \"Kati Roll Company\" is confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1fa88e63e5",
  "kind": "yes/no",
  "text": "Goa (India) : \"there is no ongoing sea level rise, sea level has been stable for the last 50 years or so, sea level fell some 20 cm at around 1960.\"",
  "question": "Does this passage advance the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q6080f5f098",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2014 FORD C-MAX ENERGI. THE CONTACT STATED THAT THE VEHICLE WAS PLUGGED IN AND RECHARGING IN THE GARAGE. TWO HOURS LATER, AN EXTENSIVE FIRE ERUPTED FROM THE CHARGE CORD. THE FIRE DEPARTMENT WAS ABLE TO EXTINGUISH THE FLAMES. THE DEALER TESTED THE VEHICLE AND STATED THAT THE CHARGE CORD OVERHEATED. THE MANUFACTURER WAS NOTIFIED OF THE FAILURE AND SENT A TECHNICIAN, BUT WAS NOT ABLE TO DETERMINE THE SPECIFIC CAUSE OF THE FAILURE. THE VEHICLE WAS INSPECTED BY A DEALER AND THE INSURANCE ADJUSTER. THE COSMETIC DAMAGES WERE REPAIRED, BUT THE CONTACT WAS UNABLE TO DETERMINE IF THE FAILURE WOULD RECUR. THE VIN AND FAILURE MILEAGE WERE NOT AVAILABLE.",
  "question": "Does this vehicle safety complaint say the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qd2ac37fc42",
  "kind": "yes/no",
  "text": "Customer: I'm also looking for an attraction preferably on a boat in the west.\nAssistant: There are no boats in the west, can I try something else for you?",
  "question": "Did the assistant, in its reply, find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q2ca0011467",
  "kind": "yes/no",
  "text": "Complaint narrative: THE RUNNING LIGHTS BURN OUT FREQUENTLY. NOT AT THE SAME TIME. EACH ONE WE'VE REPLACED AT LEAST 4 TIMES, WHICH IS WAY TOO MUCH. WE ARE USING GOOD QUALITY BULBS TOO. NOW THE INSIDE OF THE HEADLIGHT ASSEMBLY IS MELTED WHERE THE BULB SOCKET ITSELF SNAPS IN SO WE CAN'T KEEP THE SOCKET AND BULB IN ITS PLACE. THE REPLACEMENT HEADLIGHT ASSEMBLY IS NOT CHEAP FOR THIS VEHICLE",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "qd836dd67be",
  "kind": "yes/no",
  "text": "Table caption: The number of views depending on the rating.\n| responses_rating_grade | views |\n| 1.0 | 1192.8 |\n| 2.0 | 1278.9 |\n| 3.0 | 1391.4 |\n| 4.0 | 1169.8 |\n| 5.0 | 990 |\n\nStatement: Rating grade 5.0 has less number of views.",
  "question": "Is it the case that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qb1dc8721e0",
  "kind": "yes/no",
  "text": "Customer: I think it would be fun to go to see a movie tonight.\nAgent: Sure. What movie would you like to see?\nCustomer: What's playing at the Boulevard 14 Cinema in Petaluma, California since that would be the closest theater.\nAgent: OK. Boulevard 14 Cinema in Petaluma, California is showing three movies: No Time To Die, Mulan, and Emma.\nCustomer: Do you know anything about the movie?\nAgent: Sure. What specifically would you like to know?\nCustomer: What is the story about?\nAgent: OK. Here’s the synopsis of Mulan: Accompanied by her dragon, Mushu, Mulan uses her smarts to help ward off a Hun invasion, falling in love with a dashing captain along the way.\nCustomer: It sounds like it might be good. Did it get good reviews from both critics and the audiences?\nAgent: Mulan has an 87% Rotten Tomatoes score and a 92% audience rating.\nCustomer: Mulan sounds ok, but I think I'd rather see No Time to Die.\nAgent: OK. No Time To Die is playing 4:00pm, 7:30pm, and 10:55pm. Which time would you like?\nCustomer: We would like to go to the 10:55 pm show and it'll be just my friend and I.\nAgent: All right. Let me confirm that you’d like two tickets for No Time To Die at Boulevard 14 Cinema tonight at 10:55pm. Is that all correct?\nCustomer: Yes, that's correct.\nAgent: Is it OK to go ahead and purchase these tickets?\nCustomer: Yes.\nAgent: OK. Your tickets are purchased and details for how to proceed have been sent to your email address. Can I help with anything else?\nCustomer: I'm not familiar with your email confirmation. How does that work?\nAgent: The email will provide up to three options for your tickets: print at home, electronic tickets, or an option to pick them up at the theater.\nCustomer: Thank you for explaining that to me.\nAgent: OK. Enjoy your movie!",
  "question": "Is it true that, by the end of this conversation, the customer hasn't actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "qa40dcef3f0",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nVirus was widely distributed on floors, computer mice, trash cans, and sickbed handrails and was detected in air ≈4 m from patients.\n\nClaim: The coronavirus can be detected in the air up to 13 feet away from an infected patient.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qec3a49d8be",
  "kind": "yes/no",
  "text": "Assistant: It's about thirty dollars for an entree each.\nCustomer: Hmm, not bad. I think my partner will be happy.\nAssistant: I'm sure they will be. Reservations for Pastabilities, tonight at 7 PM for two people in a private corner are confirmed!",
  "question": "Does the assistant's final message confirm \"private corner\" for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qcda5f07d46",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2007 CHEVROLET TAHOE. WHILE DRIVING APPROXIMATELY 35 MPH, THE CONTACT NOTICED A BURNING ODOR FROM THE FRONT OF THE VEHICLE. THE WINDSHIELD WIPER FLUID FUNCTION FAILED AND THE RADIO CONTINUED TO FUNCTION AFTER THE CONTACT SHUT THE VEHICLE OFF. THE CONTACT WAS ABLE TO RESTART THE VEHICLE, BUT THE FAILURES RECURRED. THE CONTACT ALSO MENTIONED THAT THE BATTERY WARNING LIGHT WOULD ILLUMINATE INTERMITTENTLY. THE VEHICLE WAS NOT DIAGNOSED OR REPAIRED. THE VEHICLE WAS PREVIOUSLY REPAIRED UNDER NHTSA CAMPAIGN NUMBER: 10V240000 (ELECTRICAL SYSTEM). THE MANUFACTURER WAS NOT MADE AWARE OF THE FAILURE. THE APPROXIMATE FAILURE MILEAGE WAS 110,000.",
  "question": "Is there a report in this vehicle safety complaint of at least a single person being actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q4db55e0d3a",
  "kind": "yes/no",
  "text": "Situation: I'm a hotel cleaner and this what I did to a guest.\nAction being judged: Doing things that others would find gross.",
  "question": "Is the act under review wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q2051d6f08e",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nOur phylogenetic analysis places the majority of these genomes with viruses sequenced from Washington state. By coupling our genomic data with domestic and international travel patterns, we show that early SARS-CoV-2 transmission in Connecticut was likely driven by domestic introductions.\n\nClaim: Widespread cases of COVID-19 in the United States can be traced to international transmission.",
  "question": "According to the evidence, does it support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q3356cdcb4a",
  "kind": "yes/no",
  "text": "Customer: Hi, I would like to buy movie tickets.\nAgent: Hi, I would like to buy movie tickets.\nCustomer: Any place in Chicago.\nAgent: AMC River East 21 works?\nCustomer: Yes it works.\nAgent: When do you want to go to the movies?\nCustomer: This afternoon between 3:00 and 4:00PM.\nAgent: What movie do you want to watch?\nCustomer: Any movie as long as it is not a standard.\nAgent: There is only one movie that is not standard and is in Dolby Cinema.\nCustomer: What movie is this?\nAgent: Birds of Pray. There's a time slot for 4:00PM. Do you want me to continue?\nCustomer: Yes please.\nAgent: How many tickets do you want?\nCustomer: 3\nAgent: There's 3 tickets but they are in the very front. Do you want these seats?\nCustomer: Those are horrible seats to have, why would you suggest it?\nAgent: Those are the only ones available.\nCustomer: Well. I don't want to order anything then.\nAgent: Sorry for the inconvenience.\nCustomer: You should be sorry!\nAgent: Have a good day.",
  "question": "Have movie tickets actually been bought by the customer by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qe93cb23d3f",
  "kind": "yes/no",
  "text": "Customer: Hi, can you help me search for films in my area?\nAgent: Sure thing. Can I get your locations to start?\nCustomer: Yes, I am in Spring Hills Kansas.\nAgent: Okay, great. hat movies did you want me to search for you?\nCustomer: I have two films in mind. Once is called Shuttered and the other is called Beyond The Storm.\nAgent: Okay, let me check those titles for you, give me one second.\nCustomer: Sure.\nAgent: Okay, I do see both films playing in separate theaters near you.\nCustomer: Okay, great. I just need to know what the critic scores are for these two films.\nAgent: Sure. Shuttered has a critic score of 61%, and Beyond The Storm has a score of 81%\nCustomer: Great, I just want to confirm, these are both horror movies right?\nAgent: No. Shuttered is the only horror movie out of the two titles. Beyond The Storm is an action film.\nCustomer: Oh, I see. I think I'll go with the horror movies.\nAgent: Great choice. Do you need help getting tickets?\nCustomer: Yes, please.\nAgent: Okay, no problem. Shuttered is playing at the AMC Holiday Theater 3:00pm, 5:45 and 9:00pm. Which show time would you like to book for?\nCustomer: I'll book two tickets for the 9pm show.\nAgent: You have 2 tickets to see Shuttered at the AMC Holiday theater at 9pm tonight.\nCustomer: Yes, that's right.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qc7773eb460",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nImportance: The pandemic of coronavirus disease 2019 (COVID-19) caused by the novel severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) presents an unprecedented challenge to identify effective drugs for prevention and treatment. No therapies have been shown effective to date.\n\nClaim: At the time of writing, there were several effective therapies in combatting COVID-19.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q68573809db",
  "kind": "yes/no",
  "text": "Situation: They saw someone was missing and later found him dead in the maze.\nAction being judged: Reporting a dead body if you stumble across one.",
  "question": "Is the action being judged permissible under common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qd112e09084",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nVirus was widely distributed on floors, computer mice, trash cans, and sickbed handrails and was detected in air ≈4 m from patients.\n\nClaim: Other studies reported not finding the coronavirus on surfaces such as air vents in hospital rooms and on computer mice, sickbed handrails and doorknobs.",
  "question": "Is the claim contradicted by the evidence?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qfaa8771ae4",
  "kind": "yes/no",
  "text": "Table caption: Probabilities of detection for five A-Train and C-Train sun-synchronous orbiters at about 700 km altitude.\n| Satellite | Hard Body Radius | Threshold | Estimated Detection Rate P(Pc > T) | Data Span | Number of Reports | Number of Days |\n| CloudSat | 3.5 | 1.00E-04 | 75.2% | Apr 2015 - Sep 2019 | 2323 | 1632 |\n| CALIPSO | 14.8 | 1.00E-04 | 92.5% | Jan 2015 - Apr 2019 | 2261 | 1586 |\n| Aqua | 20 | 1.00E-04 | 96.3% | Jun 2016 - Apr 2019 | 1560 | 1047 |\n| Aura | 20 | 1.00E-04 | 96.6% | Jun 2016 - Apr 2019 | 1772 | 1045 |\n| OCO-2 | 6 | 1.00E-04 | 84.7% | Jan 2015 - Sep 2019 | 2402 | 1720 |\n\nStatement: Estimated Detection Rate P(Pc > T) 96.3% for Aqua Satellite.",
  "question": "Does the table back up the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1447acb99f",
  "kind": "yes/no",
  "text": "Assistant: Tom's bistro and italiano pasta house are both open on friday.\nCustomer: make a reservation for 6 at Tom's Bistro friday at 6:30 pm\nAssistant: There is not a table available at 6 pm",
  "question": "Based on the text, is \"6 pm\" confirmed for the customer's restaurant reservation in the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q532b72faa8",
  "kind": "yes/no",
  "text": "Using data from the Intergovernmental Panel on Climate Change (IPCC), a Science and Public Policy Institute paper published last month found that if the United States eliminated all carbon dioxide emissions, the overall impact on global temperature rise would be only 0.08 degrees Celsius by 2050.",
  "question": "Does this paragraph put forward the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q2dbbd04f31",
  "kind": "yes/no",
  "text": "Customer: Yes, please book starting Thursday for 4 people and for 4 nights.\nAssistant: I'm sorry, there were no rooms available. Would you like to find another hotel?",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "qd0722d18cf",
  "kind": "yes/no",
  "text": "Customer: Could you try an hour earlier, then?\nAssistant: Certainly. You now have a table for your party of 8 at the Curry Garden, at 16:45. Your reference number is V24OGNJB.",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "q2a44c09ba5",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nWe studied antibody response in 9 healthcare workers in Jeddah, Saudi Arabia, who survived Middle East respiratory syndrome, by using serial ELISA and indirect immunofluorescence assay testing. Among patients who had experienced severe pneumonia, antibody was detected for >18 months after infection.\n\nClaim: Survivors of the 2012 MERS outbreak, who had severe pneumonia, lacked any antibodies against the virus.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q7fd8145b18",
  "kind": "yes/no",
  "text": "Moreover the WBDGE site writes that Arctic sea ice has grown strongly over last year and that there has been no melting trend there in almost 10 years.",
  "question": "Based on the text, does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qfad558814c",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nRates of ventilation in the HC, HC+AZ, and no HC groups were 13.3%, 6.9%, 14.1%, respectively. The risk of ventilation was similar in the HC group (adjusted hazard ratio, 1.43; 95% CI, 0.53 to 3.79; P=0.48) and in the HC+AZ group (adjusted hazard ratio, 0.43; 95% CI, 0.16 to 1.12; P=0.09), compared to the no HC group. CONCLUSIONS: In this study, we found no evidence that use of hydroxychloroquine, either with or without azithromycin, reduced the risk of mechanical ventilation in patients hospitalized with Covid-19.\n\nClaim: Hydroxychloroquine does not help patients avoid being placed on a ventilator.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qc0c2b68894",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nMethods: Individuals with confirmed or suspected SARS-CoV-2 infection were screened via PCR for presence of viral genome and via enzyme-linked immunosorbent assay for presence of anti SARS-CoV-2 spike antibodies. Results: All but three confirmed SARS-CoV-2 patients seroconverted to the SARS-CoV-2 spike while only 37.4% of suspected SARS-CoV-2 patients seroconverted.\n\nClaim: Most patients who recover from the novel coronavirus will make antibodies.",
  "question": "Does the evidence back up the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qe5d0969e02",
  "kind": "yes/no",
  "text": "Occupation: Nannies\nDuties:\n- Observe participants and inform them of corrective measures necessary for skill improvement.\n- Instruct participants in maintaining exertion levels to maximize benefits from exercise routines.\n- Offer alternatives during classes to accommodate different levels of fitness.",
  "question": "Do the listed duties form part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q0b0008dde2",
  "kind": "yes/no",
  "text": "Table caption: Physical properties of coarse aggregate.\n| Sl no. | Name of the test | Details of the relevant code | Test result |\n| 1 | Aggregate Crushing value | IS:2386(Part 4) 1963 (Reaffirmed 2002) | 17.48% |\n| 2 | Aggregate impact value | IS:2386(Part 4) 1963 (Reaffirmed 2002) | 24.12% |\n| 3 | Specific gravity | IS:2386(Part 3) 1963 | 2.47 |\n\nStatement: The test Aggregate Crushing value and Aggregate impact value has different Details of the relevant code of IS:2386(Part 3) 1963.",
  "question": "Is the statement substantiated by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q976f43a637",
  "kind": "yes/no",
  "text": "Complaint narrative: MY CAR SMELLS LIKE BURNT OIL AFTER DRIVING IT. I REPORTED IT TO MY DEALER A NUMBER OF TIMES TRYING TO GET AN APPOINTMENT AFTER I GOT MY RECALL BUT THEY STILL SAY THEY DON'T HAVE THE PARTS THIS IS A SERIOUS FIRE HAZARD PLEASE HELP.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q881dc4d59c",
  "kind": "yes/no",
  "text": "Action: Wishing for someone else to be sad.",
  "question": "Is this deed prohibited by law in most places?",
  "definitions": "- yes: Doing the action is a crime or legal offence in most places (for example theft, assault, fraud, drunk driving, vandalism, hard-drug use), not merely rude or immoral.\n- no: The action is legal in most places, even if it is rude, unkind, dishonest or morally wrong (for example lying to a friend, cheating on a partner, breaking a promise)."
 },
 {
  "qid": "q2df9f286b4",
  "kind": "yes/no",
  "text": "Situation: I peed in a measuring cup as a kid and now my mom uses it to cook with\nAction being judged: Eating out of something that has been urinated in.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q845a86bd00",
  "kind": "yes/no",
  "text": "Situation: Most people think I'm a sheltered and innocent woman, I actually live in my boyfriends harem with his other girlfriends.\nAction being judged: Keeping the sordid details of your life to yourself when out in public.",
  "question": "Is it the case that the action being judged is not acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q6d985cd516",
  "kind": "yes/no",
  "text": "New York City is 1199's true power center, however. It's hard to overstate the significance of 1199 to the so-called progressive movement that now controls almost every major city office. City council speaker and leader of the Progressive Caucus Melissa Mark-Viverito is a former organizer for 1199, which has played an active role in her career from the beginning. The union suggested that the Puerto Ricanborn and Columbia Universityeducated heiress move from Greenwich Village to East Harlem to establish a political base. To help her launch her campaign for the city council speakership, 1199 threw a lavish party in San Juan. The union's political director, Kevin Finnegan, served on Mark-Viverito's transition team when she became speaker.",
  "question": "Is there an assertion in this paragraph of the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q2cbd59b1ef",
  "kind": "yes/no",
  "text": "Table caption: Formation enthalpy Y (eV/atom), Composition ratio X, Symmetry S, Fitness F (eV/block), Volumes V(Å 3 /atom), Enthalpies E(eV/atom), and Compositions C for the first 10 structures include in the convex hull of the Nb-N system at 0 GPa.\n| ID | C | E | V | F | S | X | Y |\n| 71 | [ ] | −893.5888 | 14.4958 | 0.0000 | 1 | 0.533 | −0.9929 |\n| 75 | [0 14] | −270.1198 | 14.3751 | 0.0000 | 1 | 1.000 | 0.0000 |\n| 89 | [14 ] | −1369.2158 | 18.0875 | 0.0000 | 1 | 0.176 | −0.6086 |\n| 97 | [15 0] | −1603.9973 | 22.8193 | 0.0000 | 1 | 0.000 | 0.000 |\n| 113 | [13 ] | −1183.5582 | 16.1519 | 0.0000 | 1 | 0.316 | −0.7854 |\n| 121 | [ ] | −804.6286 | 14.1712 | 0.0000 | 1 | 0.600 | −0.9578 |\n| 123 | [ ] | −715.6656 | 13.0397 | 0.0000 | 1 | 0.667 | −0.9200 |\n| 125 | [ ] | −626.5662 | 18.2131 | 0.0000 | 1 | 0.733 | −0.7457 |\n| 132 | [ ] | −998.6407 | 14.8818 | 0.0000 | 1 | 0.455 | −0.9513 |\n| 66 | [ 13] | −692.2129 | 10.5534 | 0.0055 | 1 | 0.684 | −0.8686 |\n\nStatement: 0.000 is the value of 97 ID under Y.",
  "question": "Is it the case that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q35330137d1",
  "kind": "yes/no",
  "text": "Customer: I want to watch a movie\nAgent: Ok what movie?\nCustomer: I want to see Mulan\nAgent: Ok when and what time?\nCustomer: Tomorrow maybe round 8pm?\nAgent: Ok let me check\nCustomer: Ok\nAgent: We have two options available\nCustomer: Ok\nAgent: Ciemark 12 which is 30 miles away.\nCustomer: Is there not one closer?\nAgent: you have Mountain AMC 16 which is 22 miles away\nCustomer: I cannot go those are too far\nAgent: We apologize for any inconvenience\nCustomer: It's fine\nAgent: Ok please contact us if we can e of",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qd892d3f840",
  "kind": "yes/no",
  "text": "Situation: Carl asked him if he could meet him to return his phone.\nAction being judged: Letting your friends borrow your things as long as they return them.",
  "question": "Would it be correct to say that the action being judged isn't wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q4e0bc97dfc",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nIndeed, patients with COVID-19 are at accelerated risk for delirium due to at least seven factors including (1) direct central nervous system (CNS) invasion, (2) induction of CNS inflammatory mediators, (3) secondary effect of other organ system failure, (4) effect of sedative strategies, (5) prolonged mechanical ventilation time, (6) immobilization, and (7) other needed but unfortunate environmental factors including social isolation and quarantine without family.\n\nClaim: COVID-19 patients experience no significant risk factors for delirium during their treatment.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qaa245c0275",
  "kind": "yes/no",
  "text": "Customer: Find me a restaurant that serves belgian food in the centre\nAssistant: I'm sorry, there aren't any.",
  "question": "According to its reply, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q57605c8196",
  "kind": "yes/no",
  "text": "Table caption: Properties of the source and target structures for the homogenous population case study.\n| Property | Unit | Source | Target |\n| Beam geometry, { l b , w b , t b } | mm | { 5000.0 , 350.0 , 350.0 } | { 4999.0 , 351.2 , 349.7 } |\n| Mass geometry, { l m , w m , t m } | mm | { 12000.0 , 12000.0 , 350.0 } | { 12001.0 , 11998.8 , 351.6 } |\n| Elastic modulus, E | GPa | N 210 . 00 , 1 × 10 - 9 | N 210 . 89 , 1 × 10 - 9 |\n| Density, ρ | kg / m 3 | N 8000 . 0 , 50 | N 8019 . 4 , 10 |\n| Damping coefficient, c | Ns / m | G 8.0000 , 0.8 | G 7.9981 , 0.8 |\n\nStatement: Density, Target is N 8019 . 4 , 10.",
  "question": "Is the statement supported according to the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 }
]
