# T37b blind solver T37b-blind_read-f8d1eb98-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_qc3/s13/answers/T37b-blind_read-f8d1eb98-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qabcdac3bb1",
  "kind": "yes/no",
  "text": "Customer: I am also looking for a hotel in the same area with zero stars.\nAssistant: I'm sorry, there are no matches.",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qdafa61ee9f",
  "kind": "yes/no",
  "text": "Situation: I sat back, and breathed in a sigh of relief as I let out a smile.\nAction being judged: Smiling when you are happy.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q4fea591cca",
  "kind": "yes/no",
  "text": "Customer: Hi, I'm interested in some information about movies that are showing. Something adults would enjoy. No kid movies, please, and no horror films.\nAgent: Where are you located?\nCustomer: My wife and I are visiting in Spring Hills, Kansas. I've heard about good things about both Family Jewels and Beyond the Storm. Can you give me information about those?\nAgent: Yes. Family Jewels stars Ryan Reynolds and Melissa McCarthy. It tells the story of a European jewel thief who seemingly falls in love with an American con artist.\nCustomer: Oh, that sounds like something my wife would like. What about Beyond the Storm?\nAgent: Beyond the Storm is an action movie directed by James Cameron. The crew of a fishing boat battles extreme weather and a traitor.\nCustomer: Well that's more my kind of movie. Are both movies playing at the AMC Holiday Theater? That is closest to the restaurant we will be eating at around 6:30 PM.\nAgent: I'm sorry. Beyond the Storm is playing at Cinemark Downtown. I can give you driving directions if you tell me the name or address of the restaurant at which you will be dining.\nCustomer: We have reservations at Bob's Steakhouse. We heard they have good onion rings.\nAgent: Bob's Steakhouse on Pico Canyon Rd is 14.6 miles from Cinemark Downtown theaters. At 7:30 PM on Saturday evening that is a 24 minute drive. Would you like detailed directions?\nCustomer: No, thank you. I don't want to have rush through dinner. AMC Holiday Theater is closer?\nAgent: Bob's Steakhouse on Pico Canyon Rd. is 4 miles from the AMC Holiday Theater.\nCustomer: That sounds much better, but I'd really love to see Beyond the Storm. Are you sure its not playing at any other theater?\nAgent: I'm sorry. Beyond the Storm is only playing at Cinemark Downtown in Spring Hills.\nCustomer: Well, I guess we could book a reservation for dinner closer to Cinemark Downtown.\nAgent: I would be happy to provide you with information about restaurants near Cinemark Downtown.\nCustomer: No, that's all right. Family Jewels it is, then.\nAgent: Just to confirm. Two tickets for this evenings, Saturday, August 8th, 8:10 PM showing of Family Jewels at AMC Holiday Theater.\nCustomer: Yes. That is correct. Thank you.\nAgent: You're tickets are confirmed and they've been sent to your email address. Thank you.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q9887dd979b",
  "kind": "yes/no",
  "text": "Statement 1: An infant needs sun, water and soil in order to flourish.\nStatement 2: A basil plant needs sun, water and soil in order to flourish.",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q0aabb687dd",
  "kind": "yes/no",
  "text": "It has been estimated that the U.S. national commitments to the UN to reduce emissions by 28% will prevent threehundredths of a degree centigrade in warming by 2100.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q67a5550539",
  "kind": "yes/no",
  "text": "Customer: Hey, isn't that world war 1 movie out now?\nAgent: Do you mean 1917?\nCustomer: Yes, that. Buy a ticket for that movie.\nAgent: Ok. When and where do you want to see it?\nCustomer: I want to go the theater downtown. let's say around 10-ish?\nAgent: Ok, let me check. There is showing of that movie downtown at 10.\nCustomer: Ok. When is it showing?\nAgent: Showtimes are 6, 9 and midnight for today.\nCustomer: Ok. Book me a ticket for the 6 pm showing.\nAgent: Ok. It appears the showing has been sold out.\nCustomer: Fine. Try the 9 pm showing then.\nAgent: 9 pm showing is also sold out.\nCustomer: Ok. Try midnight then.\nAgent: It appears the movie is very popular all tickets for tonight have been sold out.\nCustomer: How is that possible? try a different theater nearby.\nAgent: Downtown theater is the only one showing that particular movie.\nCustomer: Unbelievable.\nAgent: What would you like to do now?\nCustomer: Well, nevermind then. I guess I won't watch a movie tonight.\nAgent: Ok. Sorry about that.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q4427b0f123",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nReports from China and Italy suggest that risk factors for severe disease include older age and the presence of at least one of several underlying health conditions (3,4).\n\nClaim: COVID-19 severity equally impacts people of all ages with or without chronic diseases.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q8ad2578e6c",
  "kind": "yes/no",
  "text": "If you play the 🎸 get in my pants immediately",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q9b5e3d9c4c",
  "kind": "yes/no",
  "text": "Situation: I used to seriously dislike Spongebob.\nAction being judged: Expressing your opinion about a tv show.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q7466d6f961",
  "kind": "yes/no",
  "text": "Table caption: Mass distribution of available bone tissue samples expressed as total weight (wt) in grams. The percentages of dark and light coloured samples, as well as the rest are shown and expressed as wt%.\n| Level | Hearth | Sample label | Total weight (g) | Dark colour (wt%) | Light colour (wt%) | Rest (<2mm) (wt%) |\n| L4 | a | (5–8)3 | 2.12 | 100 | 0 | 0 |\n| L4 | A | 01 | 34.24 | 56.3 | 23.6 | 20.2 |\n| L4 | B | 04 | 47.05 | 62.3 | 28.5 | 9.1 |\n| L4 | D | 02 | 75.94 | 77.1 | 13.0 | 9.8 |\n| L4 | E | 03 | 5.51 | 59.6 | 0 | 40.4 |\n| L5 | K2 | H301 | 48.71 | 72.2 | 6.2 | 21.6 |\n| L5 | J1 | J301 | 4.08 | 64.3 | 35.7 | 0 |\n| L7 | a | (1–2)1 | 0 | 0 | 0 | 0 |\n| L7 | Y | 01 | 2.26 | 100 | 0 | 0 |\n| L7 | W1 | 02 | 14.01 | 77.4 | 10.4 | 12.2 |\n| L7 | W2b | 2–03 | 3.67 | 63.0 | 37.0 | 0 |\n| L8 | A | 0 | 2.40 | 0 | 100 | 0 |\n| L11 | I | (1–2)1 | 99.57 | 73.05 | 17.1 | 9.9 |\n| L11 | I | (1–2)5 | 120.63 | 69.0 | 20.9 | 10.1 |\n| L11 | L | (5–8)6 | 83.37 | 69.3 | 18.6 | 12.1 |\n| L14 | T | 01 | 67.56 | 74.9 | 17.0 | 8.0 |\n| L14 | V | 03 | 74.78 | 60.5 | 23.1 | 16.4 |\n| L14 | Ω | 01 | 75.24 | 75.5 | 7.9 | 16.6 |\n\nStatement: L11 of sample label (1Ai2)5 has highest total weight of 120.63.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe683bbcbb6",
  "kind": "yes/no",
  "text": "Customer: That should be fine. Please provide me tickets for the same group of people. I will also need a reference number.\nAssistant: Booking was successful, the total fee is 60.59 GBP payable at the station .\nReference number is : 2L1LA91L",
  "question": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "qac66d0644d",
  "kind": "yes/no",
  "text": "Customer: The type of food is not important, but I would like a nice place that has tables available on Saturday evening.\nAssistant: Sure, I would recommend the Midsummer House Resaurant which serves British food.  It is a nice, expensive place located in the Centre.",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q1dca6f9e11",
  "kind": "yes/no",
  "text": "Occupation: Chemical Equipment Operators and Tenders\nDuties:\n- Examine drawings, negatives, or photographic prints to determine coloring, shading, accenting, or other changes required for retouching or restoration.\n- Splice broken or separated film and mount film on reels.\n- Produce timed prints with separate densities or color settings for each scene of a production.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q8b0b8f3298",
  "kind": "yes/no",
  "text": "Occupation: News Analysts, Reporters, and Journalists\nDuties:\n- Confer with clients, editors, publishers, or producers to discuss changes or revisions to written material.\n- Write words to fit musical compositions, including lyrics for operas, musical plays, and choral works.\n- Write humorous material for publication, or for performances such as comedy routines, gags, and comedy shows.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q19f1b8b295",
  "kind": "yes/no",
  "text": "Assistant: Okay I will call them now. Sorry for the inconvenience.\nCustomer: That's okay. Thanks.\nAssistant: So I placed your order for a large pizza with peperoni and bacon at Papa Johns in Sidney Oh.",
  "question": "According to the assistant's last message, is \"Papa Johns\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q263878f4dc",
  "kind": "yes/no",
  "text": "Situation: I asked my girlfriend to marry me last night.\nAction being judged: Males proposing to the female they are dating when the relationship is serious.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q1a2a813075",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nConclusions The population prevalence of SARS-CoV-2 antibodies in Santa Clara County implies that the infection is much more widespread than indicated by the number of confirmed cases.\n\nClaim: \"We found that there are many, many unidentified cases of people having Covid infection that were never identified with it with a virus test,\" said Dr. Jay Bhattacharya, a professor of medicine at Stanford University and one of the paper's authors.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qbd1a483a55",
  "kind": "yes/no",
  "text": "Customer: What are the showtimes for Bad Boys for life at Cinemark?\nAgent: 11am, 12pm, 1pm, 2pm, 3pm, 5pm, 7pm, 9pm, and 11pm\nCustomer: What time is the IMAX showing?\nAgent: 7pm, 9pm, and 11pm\nCustomer: How many seats are available for the 7pm showing?\nAgent: There are only 6 seats left.\nCustomer: How many seats are available for the 11pm showing?\nAgent: The 11 p.m. is sold out.\nCustomer: What is the price of a regular ticket?\nAgent: 8 dollars\nCustomer: How many seats are available for the 11 am showing?\nAgent: There are 24 seats left.\nCustomer: How many seats are available for the 11pm showing tomorrow?\nAgent: The 11 p.m. is sold out.\nCustomer: What day are there seats available for the 11pm showing?\nAgent: Monday\nCustomer: How many seats are available?\nAgent: There are 10 seats left.\nCustomer: Great thanks.\nAgent: You're welcome.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q43f959c176",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nRates of ventilation in the HC, HC+AZ, and no HC groups were 13.3%, 6.9%, 14.1%, respectively. The risk of ventilation was similar in the HC group (adjusted hazard ratio, 1.43; 95% CI, 0.53 to 3.79; P=0.48) and in the HC+AZ group (adjusted hazard ratio, 0.43; 95% CI, 0.16 to 1.12; P=0.09), compared to the no HC group. CONCLUSIONS: In this study, we found no evidence that use of hydroxychloroquine, either with or without azithromycin, reduced the risk of mechanical ventilation in patients hospitalized with Covid-19.\n\nClaim: Hydroxychloroquine does not help patients avoid being placed on a ventilator.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qc0110e8086",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nAmong these, we identify 66 druggable human proteins or host factors targeted by 69 existing FDA-approved drugs, drugs in clinical trials and/or preclinical compounds, that we are currently evaluating for efficacy in live SARS-CoV-2 infection assays.\n\nClaim: A research team found that no drugs target the same proteins in our cells the novel coronavirus does.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qd34c822aa2",
  "kind": "yes/no",
  "text": "Customer: I'm looking for someplace to go in the west.\nAssistant: Might I recommend the Whale of a Time entertainment venue?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q31ec2b3ea6",
  "kind": "yes/no",
  "text": "Occupation: Pediatric Surgeons\nDuties:\n- Perform transplantation operations, such as organ transplants, on fetuses, infants, children, and adolescents.\n- Examine fetuses, infants, children, and adolescents, and diagnose health issues to determine need for intervention, such as surgery.\n- Operate on fetuses, infants, children, and adolescents to correct deformities, repair injuries, prevent and treat diseases, or improve or restore patients' functions.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qec987f7088",
  "kind": "yes/no",
  "text": "It is long past the time to have a real energy policy, one that works for America, not against it.",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q4743351db3",
  "kind": "yes/no",
  "text": "Table caption: Characteristics of all ESS 11 cases in relation to gender.\n| Gender | Women ( n = 1087) | Men ( n = 783) | P |\n| Age - years |  |  |  |\n| Median (25 th ,75 th percentile) | 73 (56−84) | 71 (55−81) | 0.025 |\n| Priority at dispatch centre - n (%) a |  |  | 0.001 |\n| Prio 1 | 334 (30.8) | 302 (38.6) |  |\n| Prio 2 | 698 (64.3) | 448 (57.2) |  |\n| Prio 3 | 53 (4.9) | 33 (4.2) |  |\n| Triage colour RETTS - n (%) |  |  | 0.002 |\n| Red | 11 (1.0) | 13 (1.7) |  |\n| Orange | 224 (20.6) | 195 (24.9) |  |\n| Yellow | 587 (54.0) | 423 (54.0) |  |\n| Green | 265 (24.4) | 152 (19.4) |  |\n| Level of care - n (%) |  |  | 0.170 |\n| To hospital | 849 (78.1) | 632 (80.7) |  |\n| Stay at the scene | 238 (21.9) | 151 (19.3) |  |\n| Seek medical advice within 72 h. - n (%) b | 29 (12.2) | 15 (9.9) | 0.517 |\n| Mode of transport - n (%) c |  |  | 0.605 |\n| Ambulance | 764 (90.0) | 584 (92.4) |  |\n| PTS, immobile d | 33 (3.9) | 17 (2.7) |  |\n| PTS, seated | 32 (3.8) | 18 (2.8) |  |\n| Single-responder unit | 8 (0.9) | 9 (1.4) |  |\n| Transport by own means | 12 (1.4) | 4 (0.6) |  |\n| Type of condition - n (%) |  |  |  |\n| Non-time critical | 1040 (95.7) | 734 (93.7) | 0.062 |\n| Time critical | 47 (4.3) | 49 (6.3) |  |\n\nStatement: Transport by own means Men ( n = 783) is 4 (0.6).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qcfc4d987c1",
  "kind": "yes/no",
  "text": "Europe has found it needs to keep fossil and nuclear plants equal to 90% of its \"renewable\" power capacityin spinning reserve and burning fuel. Otherwise, factories may have to shut down and stop lights will quit working, not to mention hospital operating rooms. The public thus must build and maintain two power systems, both using up energy but with the \"renewable\" set far more costly.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qbc7d977bc3",
  "kind": "yes/no",
  "text": "Table caption: Exploratory factor analysis for the measures of response inhibition ( N = 179).\n| Measure | Factor loading | Uniqueness |\n| Antisaccade ERR | 0.15 | 0.98 |\n| Stroop ERR | 0.28 | 0.92 |\n| Stroop RT | 0.57 | 0.68 |\n| No-go ERR | 0.36 | 0.87 |\n| SSRT | – | 0.99 |\n\nStatement: There are 5 different types of measures in the given table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe82eee59be",
  "kind": "yes/no",
  "text": "Statement 1: A steak will give a happy ending to this meal\nStatement 2: A dessert will give a happy ending to this meal",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q0df022d587",
  "kind": "yes/no",
  "text": "Table caption: The mechanical properties of the used steel bars\n| Nominal diameter (mm) | Actual area (mm 2 ) | Yield strength (MPa) | Ultimate strength (MPa) | Elongation (%) |\n| 8 | 49 | 551 | 690 | 17.2 |\n| 12 | 112 | 513 | 671 | 17.5 |\n| 16 | 199 | 482 | 618 | 18.75 |\nTable notes: Note; each value represented an average for three samples.\n\nStatement: 17.2 Elongation Nominal diameter is 8",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q04ddda6b87",
  "kind": "yes/no",
  "text": "Customer: yes, 7 people 4 nights starting Wednesday.\nAssistant: I'm sorry. There is no availability. Would you like to try different dates or another hotel?",
  "question": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "qa3bd50dbf0",
  "kind": "yes/no",
  "text": "Table caption: BET analysis for biochar samples.\n| Sample | BET surface area (m 2 /g) |\n| 300 °C char | 0.0218 |\n| 500 °C char | 0.0899 |\n| 700 °C char | 0.2720 |\n| 900 °C char | 0.2115 |\n\nStatement: BET surface area (m 2 /g) 0.2115 Sample is 900 C char.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q216c760b6a",
  "kind": "yes/no",
  "text": "Statement 1: He shot the lion with a spoon\nStatement 2: He shot the lion with a gun.",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q90f3b1c8c2",
  "kind": "yes/no",
  "text": "Assistant: $105-120. It will vary depending on some unique factors like traffic delays, tolls, and more. Also trips to and from AUS airport are subject to a $2.00 surcharge.\nCustomer: I understand. That's fine.\nAssistant: I just booked it. They will show up in 15 minutes precisely to the designated ride pickup location at the airport.",
  "question": "According to the assistant's last message, is \"15 minutes\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfe3bdf7aa7",
  "kind": "yes/no",
  "text": "Statement 1: shops are closed every day\nStatement 2: shops are open every day",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qd6a9788216",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2009, Taylor married writer Nick Flynn.\n- They have a daughter Maeve.\n\nSummary sentence:\nShe is married to playwright Nick Flynn, with whom she has a daughter.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q2aaf69e0e6",
  "kind": "yes/no",
  "text": "Occupation: Skincare Specialists\nDuties:\n- Determine which products or colors will improve clients' skin quality and appearance.\n- Examine clients' skin, using magnifying lamps or visors when necessary, to evaluate skin condition and appearance.\n- Perform simple extractions to remove blackheads.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qdbc5f4bb37",
  "kind": "yes/no",
  "text": "Complaint narrative: PULLING DOWN MY DRIVE WAY MY VEHICLE ACCELERATED WITHOUT ME TRYING. I HIT THE BRAKE AND E BRAKE. IT DID NOT STOP US. IN RESULT OF THE ACCELERATION MY HOUSE STOPPED US.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qcedecce487",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS AND RELEVANCE: In this survey of heath care workers in hospitals equipped with fever clinics or wards for patients with COVID-19 in Wuhan and other regions in China, participants reported experiencing psychological burden, especially nurses, women, those in Wuhan, and frontline health care workers directly engaged in the diagnosis, treatment, and care for patients with COVID-19.\n\nClaim: Female front-line workers treating patients with COVID-19 experienced higher rates or more severe symptoms of depression, anxiety, insomnia and distress than health-care workers overall.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qa04fef268e",
  "kind": "yes/no",
  "text": "Customer: I would like to reserve tickets for a movie.\nAgent: What movie would you like to see?\nCustomer: Well, we are debating a few choices and I wanted to see the showtimes.\nAgent: Ok. What's the first movie you want to see?\nCustomer: Little Women\nAgent: For tonight?\nCustomer: Yes.\nAgent: I see a 6:30 and an 8 pm showing of that at AMC Champaign.\nCustomer: Hm. What are the showtimes for 1917?\nAgent: 1917 is showing at 9 pm and 10:30 pm.\nCustomer: Well, 1917 is probably to late for us. I was hoping for something around 7\nAgent: So, Little Women?\nCustomer: Yes I think so.\nAgent: How many tickets?\nCustomer: Hold on a moment, I need to text my friends.\nAgent: Of course.\nCustomer: It seems that 2 of my friends are not able to attend this evening.\nAgent: Oh, too bad! How many tickets should I purchase, then?\nCustomer: I think that we are actually going to wait until another night, so don't buy anything yet.\nAgent: Ok.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qb5b07ca354",
  "kind": "yes/no",
  "text": "Statement 1: Harry stoops down to throw the basketball into the basket\nStatement 2: Harry jumps high to throw the basketball into the basket",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q196a0970b5",
  "kind": "yes/no",
  "text": "Customer: Yes can I make a reservation for 1 people at 16:15 on wednesday?\nAssistant: I'm sorry, there are no available tables at that time. Would you like me to look for a different restaurant?",
  "question": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "qecae673331",
  "kind": "yes/no",
  "text": "Customer: When is the next showing for Star Wars The Rise of Skywalker?\nAgent: What movie theater do you want me to search?\nCustomer: Try the AMC Hilton theater on 121st street.\nAgent: The next showing for Star Wars The Rise of Skywalker at the AMC Hilton is 8:15 PM.\nCustomer: Perfect time for me. What the cost for one adult ticket?\nAgent: One adult ticket costs $13.44, not including tax.\nCustomer: That's not too bad. Okay, book me a ticket, then.\nAgent: Ok, one adult ticket for the 8:15 PM showing of Star Wars The Rise of Skywalker at the AMD Hilton. What screening do you prefer?\nCustomer: Just standard is fine. Oh, is this theater running any deals?\nAgent: This week, all screenings for movies are the same price.\nCustomer: So, if I switch from standard screening to IMAX screening the picket of the ticket doesn't change?\nAgent: That's correct.\nCustomer: I can't miss this. Okay then, switch my screening from standard to IMAX.\nAgent: Ok, switching now.\nCustomer: Ok, play me back they details of the booking now.\nAgent: One adult ticket for the IMAX 8:15 PM showing of Star Wars The Rise of Skywalker at the AMD Hilton. Is that correct?\nCustomer: Yes, it is.\nAgent: How do you want to pay?\nCustomer: Use my Visa card, and include the tax in the final amount when you read the price to me.\nAgent: The total comes to $14.65, tax included. Please look in you email's inbox to get you digital receipt. Is there anything else?\nCustomer: No, that's all.\nAgent: Ok, goodbye.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q449dc98bd5",
  "kind": "yes/no",
  "text": "Assistant: What kind of vehicle would you like.\nCustomer: Sedan.\nAssistant: There is no sedan available around that time.",
  "question": "According to the assistant's last message, is \"sedan\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3ba8152cd3",
  "kind": "yes/no",
  "text": "Table caption: Results of example 1.\n| Bayes factor | p ( H 0 ∣ θ ) | p ( H M ∣ θ ) | Rayleigh statistic | Rayleigh p -value |\n| 38.542 | 0.025 | 0.975 | 0.637 | 0.001 |\n\nStatement: 8.975 is the value for p ( H M .)",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc2a5a3ddc2",
  "kind": "yes/no",
  "text": "Situation: Bride's Outrageous Demands Alienate Her Fiance's Sister\nAction being judged: Saying no when a bride is asking too much of you.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q71e01c1c10",
  "kind": "yes/no",
  "text": "Statement 1: He communicated with his friends by newspapers\nStatement 2: He communicated with his friends by letter",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q0b96250e26",
  "kind": "yes/no",
  "text": "Customer: I'm looking for an expensive polynesian place.\nAssistant: I'm sorry, there is nothing that I can find like that.  Do you have anything else I can look for?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q4b0e584331",
  "kind": "yes/no",
  "text": "Instead, the onus should be on the developers to prove the positive. No wind farm developer has ever had to explain the benefits of wind. Evidence tells us that wind power performance shows not only no reduction in CO 2 and other harmful emissions, but the very reverse. But Alex Salmond is driving an aggressive green agenda like an express train across Scotland, bludgeoning anyone who gets in the way as being a Luddite and anti-green.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q4e7e788157",
  "kind": "yes/no",
  "text": "Occupation: Health Education Specialists\nDuties:\n- Collaborate with health specialists and civic groups to determine community health needs and the availability of services and to develop goals for meeting needs.\n- Supervise professional and technical staff in implementing health programs, objectives, and goals.\n- Document activities and record information, such as the numbers of applications completed, presentations conducted, and persons assisted.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q66084c6736",
  "kind": "yes/no",
  "text": "Customer: I'd like to see a movie this weekend.\nAgent: What movie do you want to see?\nCustomer: Either Knives Out, JoJo Rabbit, or Little Women.\nAgent: Where do you want to see it?\nCustomer: I want to see it at the College 9 Theater.\nAgent: They are all playing at the College 9 Theater.\nCustomer: What times are they showing?\nAgent: Knives Out is at 7 pm, JoJo Rabbit is at 7:30 pm, and Little Women is at 8 pm.\nCustomer: Are they showing at those times on both Saturday and Sunday?\nAgent: Yes.\nCustomer: Are there tickets available for Knives Out at 7 pm on Saturday?\nAgent: No, that show is sold out.\nCustomer: Are there tickets available for Knives Out at 7 pm on Sunday?\nAgent: How many tickets?\nCustomer: 2 or 3 tickets.\nAgent: Yes, there are 2 or 3 tickets available for Knives Out at 7 pm Sunday.\nCustomer: Thank you.\nAgent: Should I purchase the tickets.\nCustomer: No, I will purchase the tickets when I know how many I need.\nAgent: Okay\nCustomer: Thank you for the information.\nAgent: You're welcome.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qeef245d1e8",
  "kind": "yes/no",
  "text": "Customer: book for  6 people and three  nights starting on thursday.\nAssistant: Booking was successful.\nReference number is : ZCRPOLK8. anything else?",
  "question": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 }
]
