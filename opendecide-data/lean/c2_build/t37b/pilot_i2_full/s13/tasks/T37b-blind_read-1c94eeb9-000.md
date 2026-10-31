# T37b blind solver T37b-blind_read-1c94eeb9-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i2_full/s13/answers/T37b-blind_read-1c94eeb9-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q612fc8252b",
  "kind": "yes/no",
  "text": "Situation: Linda was shocked and quit when the editor didn't like her photos.\nAction being judged: Expressing when you don't like something.",
  "question": "Is it correct that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qe5758223a3",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2014 JEEP PATRIOT. WHILE DRIVING AT AN UNKNOWN SPEED, THE VEHICLE STALLED AND THE SLIP INDICATOR, CHECK ENGINE, AND THROTTLE CONTROL INDICATORS ILLUMINATED. THE VEHICLE WAS TOWED TO THE CONTACT'S RESIDENCE. THE VEHICLE WAS NOT TAKEN TO A DEALER; HOWEVER, AN INDEPENDENT MECHANIC CAME TO THE CONTACT'S RESIDENCE, RESET THE VEHICLE, AND CHANGED THE OIL. THE CONTACT STATED THAT THE FAILURE RECURRED A WEEK LATER. THE MANUFACTURER WAS NOTIFIED OF THE FAILURE AND CONFIRMED THAT THE VIN WAS NOT INCLUDED IN NHTSA CAMPAIGN NUMBER: 13V552000 (ENGINE). THE APPROXIMATE FAILURE MILEAGE WAS 67,000.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q816e87cba6",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Chapman's follow-up album, \"Crossroads\" (1989), was less commercially successful than her debut had been, but it still achieved platinum status in the U.S.\n\nSummary sentence:\nIn 1989, Chapman released her second album, \"Crossroads\".",
  "question": "Is every piece of information in the sentence that gives the summary supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q8f45740b48",
  "kind": "yes/no",
  "text": "Customer: I need to get 5 tickets for a movie tomorrow.\nAgent: Sure, I can help you with that. What city and state, please?\nCustomer: We're in Hillsdale, but we like to go into Spring Hills for movies.\nAgent: Okay. What movie would you like to see?\nCustomer: Could you give me some information on a movie called Shuttered? It sounded strange.\nAgent: Yes, I can. Shuttered is a horror movie rated R. On Rotten Tomatoes it has a 61% rating. Do you want the story line?\nCustomer: No, thanks. How about Beyond the Storm?\nAgent: Beyond the storm is an action movie rated PG-13. It has an 81% rating with Rotten Tomatoes.\nCustomer: What is it about?\nAgent: It is about a fishing trawler in the North Sea. The captain has to deal with the extreme weather and the fact that there is a traitor on board that causes problems.\nCustomer: Are they both playing at Cinemark Downtown?\nAgent: Beyond the Storm is playing at Cinemark Downtown and Shuttered is playing at AMC Holiday.\nCustomer: Okay. Let me go ahead and get 5 tickets to the movie Beyond the Storm. We'd like a showtime around 6 or 7, if possible.\nAgent: The showtimes close to that are 6:10pm and 8:30pm.\nCustomer: Okay. I think we'd better get the 6:10pm.\nAgent: Okay. Please let me know if this is the correct information. You want 5 tickets to see Beyond the Storm tonight at 6:10 PM at Cinemark Downtown?\nCustomer: Yes, that sounds about right. How does that email thing work?\nAgent: You'll get an email and you can either print the tickets at home or take the confirmation to the movie.\nCustomer: That sounds easy, okay.\nAgent: Your tickets are confirmed and they've been sent to your email address.",
  "question": "Based on the text, by the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qffbb1f49d4",
  "kind": "yes/no",
  "text": "Customer: Yes can I make a reservation for 1 people at 16:15 on wednesday?\nAssistant: I'm sorry, there are no available tables at that time. Would you like me to look for a different restaurant?",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "q03a7278194",
  "kind": "yes/no",
  "text": "Table caption: Real-time LAMP results for DNA extraction from Dracunculus medinensis specimens from a range of host species and countries of origin. – indicates no detection and n/a indicates not applicable.\n| Extract ID | Origin | Host | Dracunculus medinensis assay | Dracunculus medinensis assay |\n| Extract ID | Origin | Host | Time to positive (min:sec) | Annealing temperature (°C) |\n| ChDo-339.2 | Chad | Dog | 10:00 | 81.11 |\n| ChHu-69 | Chad | Human | 12:15 | 80.55 |\n| ChDo-1 | Chad | Dog | 7:45 | 81.34 |\n| ChDo-108.5 | Chad | Dog | 8:15 | 81.30 |\n| ChHu-25 | Chad | Human | 8:45 | 80.86 |\n| ChCa-10a | Chad | Cat | 9:00 | 81.15 |\n| ChDo-189 | Chad | Dog | 10:15 | 81.50 |\n| ChDo-13 | Chad | Dog | 8:00 | 81.40 |\n| ChDo-11 | Chad | Dog | 9:00 | 80.86 |\n| ChDo-47.11 | Chad | Dog | 8:30 | 81.60 |\n| ChHu-100 | Chad | Human | 10:15 | 81.35 |\n| ChHu-24 | Chad | Human | 8:30 | 81.45 |\n| ChDo-1 | Chad | Dog | 7:45 | 81.20 |\n| ChHu-283 | Chad | Human | 10:00 | 82.58 |\n| EtDo-172 | Ethiopia | Dog | 12:15 | 82.78 |\n| EtHu-278 | Ethiopia | Human | 10:30 | 82.63 |\n| EtBa-153 | Ethiopia | Baboon | 10:30 | 82.87 |\n| EtHu-152 | Ethiopia | Human | 10:00 | 82.57 |\n| MaHu-165 | Mali | Human | 9:45 | 82.67 |\n| MaHu-240 | Mali | Human | 10:00 | 82.54 |\n| MaHu-242 | Mali | Human | 23:00 | 82.58 |\n| MaHu-253 | Mali | Human | 11:00 | 82.79 |\n| SsHu-201 | South Sudan | Human | 8:45 | 82.50 |\n| SsHu-256 | South Sudan | Human | 10:15 | 82.36 |\n| SsDo-183 | South Sudan | Dog | 10:30 | 82.48 |\n| Uninfected copepod | n/a | n/a | – | – |\n| Dracunculus insignis | n/a | n/a | – | – |\n\nStatement: Time to positive for Dracunculus medinensis assay will be from 7:45 to 23:00.",
  "question": "Based on the table, is the statement supported?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q78554be237",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- However, in 2022 he was instead endorsed by NSW Labor as the party's candidate for the 2022 Strathfield state by-election, following the resignation of former party leader Jodi McKay.\n- Li retained Strathfield for the ALP at the by-election.\n\nSummary sentence:\nHe is a member of the Australian Labor Party (ALP) and was elected to the New South Wales Legislative Assembly at the 2022 Strathfield state by-election.",
  "question": "Is every bit of info in the summary sentence backed up by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q112f2975ea",
  "kind": "yes/no",
  "text": "Statement 1: He runs on the treadmill\nStatement 2: He does yoga on the treadmill",
  "question": "Of these two statements, does Statement 1 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q42e4f6a9ef",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Johanns began campaigning early in Nebraska's 1998 gubernatorial election, holding his first campaign event in October 1995.\n- On November 3, 1998, Johanns and his running mate, David I. Maurstad, defeated Hoppner and his running mate, Pam Bataillon, in the general election, by a margin of 54% to 46%.\n- Johanns succeeded Iowa Governor Tom Vilsack as chair of the Midwestern Governors Association in 2002.\n- Johanns was confirmed in a voice vote by the Senate on January 20, 2005, hours after Bush's second inauguration.\n\nSummary sentence:\nHe served as the governor of Nebraska, elected in 1998 until 2005, and was chair of the Midwestern Governors Association in 2002.",
  "question": "Is every detail in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q503cac8164",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nOn March 13, CDC performed symptom assessments and SARS-CoV-2 testing for 76 (93%) of the 82 facility A residents to evaluate the utility of symptom screening for identification of COVID-19 in SNF residents. Among 23 (30%) residents with positive test results, 10 (43%) had symptoms on the date of testing, and 13 (57%) were asymptomatic.\n\nClaim: In one of the places where there has been extensive testing, the nursing home in Washington state, 56% of those who tested positive had no symptoms when they got tested.",
  "question": "Is there support from the evidence for the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q57f8501822",
  "kind": "yes/no",
  "text": "Table caption: Classification results for the heterogeneous population case study with geometric and material differences trained on the labelled source domain and applied to the unlabelled target domain.\n| Method | Method | k NN | JDA |\n| Mapping Training | Accuracy | 16.7% | 100.0% |\n| Mapping Testing | Accuracy | 16.7% | 100.0% |\n\nStatement: There are 3 Methods of Mapping in the given table.",
  "question": "Is the statement supported according to the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q01d4850eb7",
  "kind": "yes/no",
  "text": "MUSLIM AID is a scam charity IMO 👎🏻",
  "question": "Is it correct that this post is not hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "q1bde814262",
  "kind": "yes/no",
  "text": "The attachment was a polite rejection of our paper. Included were the complete reviews. Although some of the points in the reviews were, in fact, addressed in our paper, we thought it advisable to respond to the reviews in detail, and to revise our paper in order to clarify matters. It was, however, clear, that the revised paper would no longer satisfy the space constraints of PNAS ? especially since the reviewers made clear that important material should not be relegated to ?supplementary material?.",
  "question": "According to this paragraph, does it make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q7b587b096d",
  "kind": "yes/no",
  "text": "Table caption: Characteristics of adolescent participants.\n| Characteristic | n a (%) |\n| Age ( n = 364) |  |\n| 15 years | 107 (29) |\n| 16 years | 119 (33) |\n| 17 years | 138 (38) |\n| Gender ( n = 365) |  |\n| Female | 346 (95) |\n| Male | 2 (1) |\n| Other | 17 (5) |\n| Race/ethnicity |  |\n| Non-Hispanic White | 237 (65) |\n| Non-Hispanic Black | 24 (7) |\n| Non-Hispanic other race | 49 (13) |\n| Hispanic | 56 (15) |\n| Community |  |\n| Urban | 63 (17) |\n| Suburban | 238 (65) |\n| Rural | 49 (13) |\n| Not sure | 16 (4) |\n| ED diagnosis |  |\n| Possible anorexia nervosa | 17 (5) |\n| Bulimia nervosa | 26 (7) |\n| Binge eating disorder | 9 (3) |\n| Subclinical bulimia nervosa | 115 (31) |\n| Subclinical binge eating disorder | 17 (5) |\n| Purging disorder | 4 (1) |\n| Unspecified feeding or eating disorder | 122 (33) |\n| At risk | 23 (6) |\n| Not at risk | 33 (9) |\n| EDQOL ( n = 331) median (inter-quartile range) | 1.36 (0.80, 1.76) |\n| Received treatment in past six months (among n = 245 of those screening positive for a ED clinical/subclinical diagnosis) | 30 (12) |\n| Major depression b ( n = 301) | 194 (64) |\n| Anxiety disorder c ( n = 294) | 172 (58) |\nTable notes: EDQOL = Eating Disorders Quality of Life questionnaire score. Ranges from 0 = never to 4 = always. Higher score indicates worse QOL.\n\nStatement: Age ( n = 364) of 17 years are having highest n (%) 138(38).",
  "question": "Does the table back up the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q2315d2b1fa",
  "kind": "yes/no",
  "text": "Complaint narrative: I RECENTLY PURCHASED THIS BIKE NEW FROM LYNWOOD MOTOPLEX HERE IN THE STATE OF WA. IT NOW HAS ONLY 287 MILES ON IT AND THE SIDESTAND SPRING, PART NO. 7043056 BROKE IN HALF. IF THIS HAPPENED WHILE I WAS RIDING AND TURNING LEFT THIS COULD CAUSE INJURY OR DEATH BY JACKNIFING THE MOTORCYCLE. VEHICLE WAS LUCKILY STATIONARY WHEN THIS OCCURED.",
  "question": "Does this complaint about vehicle safety report that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q7bc148d239",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Zuniga was a founding member of the Earth Communications Office (ECO), and has worked with the Natural Resources Defense Council, the Waterkeeper Alliance, and Environment California.\n\nSummary sentence:\nZuniga has been active in environmental issues since the mid-2000s, and was a founding member of the Earth Communications Office.",
  "question": "Is every piece of information in the sentence that gives the summary supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qde937c7958",
  "kind": "yes/no",
  "text": "Assistant: Do you want extra toppings?\nCustomer: OK, let's add mushrooms.\nAssistant: I'm sorry, but there is no Pacific Veggie Pizza now. Do you want to change your order?",
  "question": "Going by the assistant's final message, is \"Pacific Veggie Pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0767ce77e3",
  "kind": "yes/no",
  "text": "Occupation: Travel Guides\nDuties:\n- Conduct training programs to develop or maintain desired animal behaviors for competition, entertainment, obedience, security, riding, or related purposes.\n- Talk to or interact with animals to familiarize them to human voices or contact.\n- Cue or signal animals during performances.",
  "question": "Are the duties given in the list part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q779c550d46",
  "kind": "yes/no",
  "text": "Customer: Hi. I need some movie tickets.\nAgent: What movie would you like to watch?\nCustomer: Uncut Gems.\nAgent: Where would you like to watch Uncut Gems?\nCustomer: Cleveland, Ohio.\nAgent: Sorry, I was not able to find any Uncut Gems viewings in Cleveland. Would you like to watch another movie?\nCustomer: Okay. I'll watch Parasite instead.\nAgent: Where would you like to watch Parasite.\nCustomer: Still in Cleveland.\nAgent: How many tickets will you need?\nCustomer: 4 adult tickets.\nAgent: What time would you like to watch the movie?\nCustomer: 9:00 PM.\nAgent: Sorry, that showtime is not available for this movie.\nCustomer: How about 7:30 PM then?\nAgent: Sorry, that showtime is not available for this movie. Would you like to pick another movie?\nCustomer: No, that's fine. Just forget about it.\nAgent: Are you sure you don't want any tickets?\nCustomer: Yes, I'm sure. Thank you.\nAgent: Okay. Enjoy your day.",
  "question": "Has the customer actually paid for movie tickets by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qd687accdb8",
  "kind": "yes/no",
  "text": "Situation: Hank took him back to the store for a refund.\nAction being judged: Getting refunds on pets.",
  "question": "Is it accurate to say that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qdf53c05d15",
  "kind": "yes/no",
  "text": "Table caption: Common method bias assessment.\n| Paths | Research model (without marker variable) | Research model (with marker variable) |\n| Incongruent IT-mediated information interruption→ Interruption overload | 0.428*** | 0.410*** |\n| Congruent IT-mediated information interruption→ Interruption overload | 0.442*** | 0.424*** |\n| Interruption overload→ Emotional exhaustion | 0.483*** | 0.483*** |\n| Preemptive processing × incongruent IT-mediated information→ Emotional exhaustion | -0.079* | -0.074* |\n| Sequential processing × congruent IT-mediated information →Emotional exhaustion | -0.123** | -0.116** |\n| Marker variable→ Incongruent IT-mediated information interruption |  | -0.001 |\n| Marker variable→ Congruent IT-mediated information interruption |  | -0.015 |\n| Marker variable→Preemptive processing |  | -0.112 |\n| Marker variable→Sequential processing |  | -0.110 |\n| Marker variable→ Interruption overload |  | -0.001 |\n| Marker variable→ Emotional exhaustion |  | -0.054 |\nTable notes: Note: *p<0.05, **p<0.01, ***p<0.001.\n\nStatement: The paths in the table are observed to be unique.",
  "question": "Based on the table, is the statement supported?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qcdd9a53485",
  "kind": "yes/no",
  "text": "Table caption: Correlations between ELISA determined protein concentrations and glycan peak clusters. .\n| Peak cluster | Pearsson correlations | Pearsson correlations | Pearsson correlations | Pearsson correlations |\n| Peak cluster | LF | IgG | IgA | IgM |\n| 2 IgG | 0.31 | 0.33 | ns | 0.19 |\n| 3 LF | 0.61 | 0.23 | 0.30 | 0.32 |\n| 4 LF, GCM | 0.36 | 0.20 | ns | 0.18 |\n| 6 LF, GCM | 0.59 | ns | 0.23 | 0.31 |\n| 7 IgG, LF | 0.38 | 0.22 | 0.25 | ns |\n| 10 GCM, LF | 0.24 | 0.30 | ns | 0.21 |\n| 11 GCM | ns | ns | ns | ns |\n| 12 IgG, GCM | 0.35 | 0.61 | 0.28 | 0.35 |\n| 13 LF, GCM | 0.30 | ns | ns | ns |\n| 16 GCM | ns | ns | ns | ns |\n| 17 GCM, LF | 0.38 | ns | 0.22 | ns |\n| 18 LF, GCM | 0.26 | ns | ns | ns |\n| 21 LF | 0.65 | ns | 0.23 | ns |\n| 24 GCM | ns | ns | ns | ns |\n| 27 GCM | ns | ns | ns | ns |\n| 29 GCM | ns | ns | ns | ns |\n\nStatement: There are 19 Peak cluster in the table.",
  "question": "Is the assertion backed by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q176862a569",
  "kind": "yes/no",
  "text": "Assistant: I just spoke with them.\nCustomer: Were you able to get it?\nAssistant: Yes, I booked a table in the back for you for 3 at 7pm for this Friday.",
  "question": "Pursuant to the assistant's final message, is \"3\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q090ffba88f",
  "kind": "yes/no",
  "text": "Situation: She had him wash up and then let him hold the baby.\nAction being judged: Having clean hands before touching a baby.",
  "question": "Is it true that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q163a65f612",
  "kind": "yes/no",
  "text": "Statement 1: If you played too much, you could pass the exam.\nStatement 2: If you worked harder, you would have passed the exam.",
  "question": "Of these two statements, does Statement 2 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q4d66784156",
  "kind": "yes/no",
  "text": "Situation: Grandma Weighs Her Decision to Sever Contact With Daughter\nAction being judged: Hurting your family members to the point that they no longer want anything to do with you.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q0cdf3ef751",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS: The incidence of VTE in patients with severe NCP is 25% (20/81), which may be related to poor prognosis.\n\nClaim: There are approximately 1 in 4 incidences of venous thromboembolism in patients with severe novel coronavirus pneumonia symptoms of SARS-CoV-2.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q43641e04da",
  "kind": "yes/no",
  "text": "Complaint narrative: TAKATA RECALL. I HAVE CONTACTED SEVERAL FORD DEALERSHIPS ABOUT COMPLETING THE RECALL REPLACEMENT OF MY AIRBAGS BUT HAVE BEEN TOLD REPEATEDLY THAT THEY DO NOT YET HAVE THE PARTS NECESSARY TO DO IT. IT HAS BEEN WELL OVER A YEAR AND IT IS UNACCEPTABLE THAT THE RECALL CANNOT BE COMPLETED WHEN THERE IS A CLEAR SAFETY HAZARD ASSOCIATED WITH THE TAKATA AIRBAGS.",
  "question": "Does this safety complaint about a vehicle report that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qf94d965e01",
  "kind": "yes/no",
  "text": "Situation: Joe invited his family to a dinner at his new house.\nAction being judged: Doing things with family when you get the chance.",
  "question": "Is it the case that the action being judged is not acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qf1a1c8f14d",
  "kind": "yes/no",
  "text": "Customer: Good afternoon. I need some help getting tickets to a movie or to a game.\nAgent: good afternoon. I would be happy to assist you. Which would you prefer I search first?\nCustomer: Movie tickets will probably be easier.\nAgent: Okay, no problem. Do you have a movie you would like to see?\nCustomer: I'm not sure. What are the most popular movies showing this weekend?\nAgent: Well, they seem to be 1917, Jumanji, Bad Boys, Star Wars, Like a Boss and Doolittle. Do any of those interest you?\nCustomer: Hmm. Well, I would be taking my granddaughter. Doolittle sounds like the best choice.\nAgent: Okay. Which city would you be seeing it in?\nCustomer: Well, maybe Burlington or Franklin.\nAgent: Yes, these movies are showing at theatres in those two cities. What time are you interested in?\nCustomer: Oh, you know what? Actually Sturtevant would be better.\nAgent: Okay, let me check in Sturtevant. Doolittle is showing there. What time would you prefer?\nCustomer: Well, probably a late afternoon or early evening showing. Oh, and it has to be on Friday.\nAgent: Okay, let me search for you. Only 2 tickets, correct?\nCustomer: Yes, one senior citizen and one teenager.\nAgent: Well, I'm afraid it looks like there are only tickets for the 9:00 showing. Would that work?\nCustomer: Oh dear. No, it might not be a problem for my granddaughter, but it's too late for me. Is Jumanji playing there?\nAgent: No, Jumanji is not playing in Sturtevant. It is only playing in Franklin.\nCustomer: What time is available in Franklin. If it's an early showing, that could work.\nAgent: No, there are only tickets available for the 9:00 p.m. showing. Should I try looking at Burlington?\nCustomer: Yes, please.\nAgent: No. I'm afraid that theater is also sold out. Should I look into a basketball game for you, I assume in Milwaukee?\nCustomer: You know what, let me check with my daughter first to make sure I know when my granddaughter is free. Thank you so much for your trouble.\nAgent: No trouble at all. I'm sorry the movie situation didn't work out.",
  "question": "Has the customer actually bought movie tickets by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qec867d4c48",
  "kind": "yes/no",
  "text": "Occupation: Public Safety Telecommunicators\nDuties:\n- Receive incoming telephone or alarm system calls regarding emergency and non-emergency police and fire service, emergency ambulance service, information, and after-hours calls for departments within a city.\n- Scan status charts and computer screens, and contact emergency response field units to determine emergency units available for dispatch.\n- Monitor various radio frequencies, such as those used by public works departments, school security, and civil defense, to stay apprised of developing situations.",
  "question": "Are the enumerated duties included in the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q4f3bb31bc4",
  "kind": "yes/no",
  "text": "Statement 1: he used water for hand sanitizing\nStatement 2: he used spirit for hand sanitizing",
  "question": "Is it right to say that, of these two statements, Statement 2 does not go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q1e0af351dc",
  "kind": "yes/no",
  "text": "Situation: While we were swimming, I wasn't paying much attention.\nAction being judged: Not keeping track of sometime important.",
  "question": "Is it correct that the action being judged isn't wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q8f2c372fd0",
  "kind": "yes/no",
  "text": "Customer: Hi\nAgent: Hi, what can i do for you today?\nCustomer: I would like to purchase movie tickets to see a movie tonight for either no time to die, or mulan.\nAgent: Sounds great, can you give me your location please.\nCustomer: I live in Stoneyford Oregon.\nAgent: Awesome,do you know which movie theater you would like to see either of these two movies in?\nCustomer: Mountain AMC 16 please.\nAgent: Sure, let me check the availability of tickets for you.\nCustomer: No problem.\nAgent: I am sorry. I am afraid this movie theater is temporarily closed until the fall, and the release date of both movies has been pushed back as well.\nCustomer: Oh ok, well would you mind checking another theater for me?\nAgent: Sure, which one?\nCustomer: Holiday Cinemark 12.\nAgent: Ok, one second while i do this for you.\nCustomer: Ok.\nAgent: I am sorry. I am afraid this movie theater is temporarily closed until the fall, and the release date of both movies has been pushed back as well.\nCustomer: Dang, oh well. Is there a way to be notified whe either of these theaters are up and running?\nAgent: Yes, just use our app and add the theater to your favorites. This will give you updates with all of the details necessary when they happen.\nCustomer: Thank you for all your help!\nAgent: No problem. Hope to get to speak with you again soon!",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qa3be9aa79e",
  "kind": "yes/no",
  "text": "Table caption: Reasons teens were unwilling or uncertain about allowing researchers to contact their parents for consent purposes ( N = 166).\n| Theme | N (%) | Example responses |\n| Teen privacy | 55 (33) | ● “They don't know about my problem and I want to keep it that way.” ● “I'm not open about my issues with my parents” |\n| Parents lack an understanding of mental health or are unaware of the problem | 38 (23) | ● “I am not sure they would approve, seeing as they don't necessarily believe in mental health problems. Also, mental health is stigmatized in my family.” ● “They don't know about my eating disorder” |\n| Teen is concerned about parents' reaction/response | 34 (20) | ● “I don't want them to worry more about me” ● “They would be concerned/annoyed that I've never talked to them about this before” |\n| Teen autonomy | 26 (16) | ● “I do not like or trust my parents and I don't want them involved in this” ● “I feel old enough to make my own decisions about apps I'd like to try out” |\n| Poor parent-teen relationship | 17 (10) | ● “My family would never let me get help. A lot of parents don't care about whether their kid is hurting or not. This won't work if you make people tell their families. It just won't”. ● “My parents can be judgmental at some points so I don't want them to tell me something about wanting to try something new”. |\n| Parent would not want the teen to participate in research | 13 (8) | ● “They might think it's a scam and say no” ● “My parents might not be open to me participating in such a study or understanding of how I might benefit from such an app” |\n| Fears about online security/privacy | 3 (2) | ● “I am not sure that this survey is really trustworthy or that they would want me taking it” ● “I do not know what kind of information they will be collecting, so I am undecided” |\n\nStatement: Fears about online security/privacy has the least N (%) value of 3 (2).",
  "question": "Is it accurate to say that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q07d2323739",
  "kind": "yes/no",
  "text": "Customer: I am looking for architectural spots to visit on my trip to Cambridge.  On the east side.\nAssistant: Well, unfortunately there are architectural attractions located in the east. Would you like to try a different area?",
  "question": "Going by the text, did the assistant's reply include at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q0b5396e57a",
  "kind": "yes/no",
  "text": "Assistant: Ok. I need what is a best phone number?\nCustomer: They can reach me at 123-456-8989\nAssistant: TOday does not work. Would tomorrow morning at 8 a.m. be Ok?",
  "question": "Is the assistant's final message saying that \"TOday\" is confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4a002305b0",
  "kind": "yes/no",
  "text": "But of course who can reasonably claim that the American economy or public health is better off since the Obama regulatory machine gun started firing? Moreover, we have far more than enough regulation to ensure the safety of the public health and our economy needs far less regulation in order to return to growth.",
  "question": "Does this paragraph make a claim about climate, namely the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qb69e3118dd",
  "kind": "yes/no",
  "text": "Statement 1: illness can be cured during routine physicals\nStatement 2: illness can be found during routine physicals",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qb19effe4ac",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Andrew Anagnost\n- In these roles, he was credited with Autodesk's transition to software as a service, as well as the adoption of cloud computing.\n- Following a four month search, Anagnost was permanently appointed as President and CEO of the company.\n\nSummary sentence:\nAndrew Anagnost is the President and CEO of Autodesk, having been appointed to the positions.",
  "question": "Looking at the summary sentence, is every piece of information in it supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q708de68dfc",
  "kind": "yes/no",
  "text": "Complaint narrative: DEAR NHTSA, MY 2015 HONDA FIT RATTLE'S ON COLD START INITIALLY WHEN YOU START THE ENGINE. AFTER ABOUT 6-8 HOURS AFTER LETTING THE ENGINE COOL THE NOISE WILL REAPPEAR. THE ISSUE IS THE VTC ACTUATOR. BEING A FAIRLY NEW VEHICLE FOR IT'S AGE IT'S VERY DISAPPOINTING TO HEAR SUCH DISTURBING NOISE EVERY TIME I START UP THE CAR. I HAVE BEEN EXPERIENCING THIS FOR THE PAST YEAR, STARTING IN JUNE 2017. AT FIRST, MY UNDERSTANDING WAS THAT IT WAS THE ENGINE SPLASH GUARD. LAST YEAR I WAS DRIVING ON THE FREEWAY (70MPH ZONE) AND ALL OF A SUDDEN I HEAR A SCRAPPING NOISE. THE ROAD WAS COMPLETELY FREE OF DEBRIS, AND WHEN I PULLED OVER THE ENGINE SPLASH GUARD CAME UP, ALONG WITH BREAKING BOTH TABS ON THE FRONT BUMPER. I HAD ENGINE SPLASH REPLACED 3 MONTHS AGO USING BRAND NEW CLIPS (PLASTIC WHICH ACTUALLY ENDS UP BREAKING) AND SCREWS. EVEN AFTER FIXING THE ENGINE SPLASH GUARD, THE VTC RATTLE NOISE STILL APPEARED. RECENTLY, THE ENGINE SPLASH GUARD STILL MANAGED TO POP OFF ON THE FREEWAY. AT THIS POINT, I'M FED UP WITH THE TERRIBLE DISAPPOINTMENT THIS VEHICLE HAS GIVEN ME ALONG WITH ITS BUILD QUALITY. ANOTHER THING TO NOTE IS THE DOOR PANEL MAKING A RATTLING NOISE. AFTER TAKING OFF THE DOOR PANEL, I NOTICED THE THE PLASTIC LINING IS DETACHING FROM THE BLACK GLUE THAT IS KEEPING IT IN PLACE. POSSIBLY, THE HEAT IS CAUSING THE BLACK GLUE TO MELT.",
  "question": "Is it accurate to say that this vehicle safety complaint does not report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q2f43366986",
  "kind": "yes/no",
  "text": "If there is a more obvious example of crony capitalism to be had in our country than the treatment the wind industry now enjoys, I can't think of it.",
  "question": "Hey, does this paragraph say the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qc91d8fea76",
  "kind": "yes/no",
  "text": "Table caption: Overview of the renewable energy technologies and the selected block types in the Minecraft platform.\n| Energy technology | Block type |\n| Solar panels | Daylight sensor |\n| Wall insulation | Yellow wool |\n| Floor insulation | Orange wool |\n| Double glazing | Glass |\n| Roof insulation | Purple wool |\n\nStatement: There are six renewable energy technologies are given.",
  "question": "Is there support for the statement in the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q4086c606d0",
  "kind": "yes/no",
  "text": "Table caption: Description of columns in ASCII text table.\n| Column Name | Description |\n| System | Multibeam echosounder system |\n| Date | Date of survey, yyyymmdd. |\n| Time | Time of survey (UTC), hhmmss. |\n| Easting | Easting Cartesian coordinate, UTM Zone 27 N projection, WGS84. |\n| Northing | Northing Cartesian coordinate, UTM Zone 27 N projection, WGS84. |\n| Depth | Corrected and processed depth, m. |\n| Latitude | Geographical latitude, DD;MM.mm, WGS1984. |\n| Longitude | Geographical longitude, DD;MM.mm, WGS1984. |\n\nStatement: ASCII text table has three categories- Column Name Ratio and Description.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q5d38c0431f",
  "kind": "yes/no",
  "text": "As a fuel source, coal is a different product from what it was in past decades. Specifically, it is much cleaner. Yet, as always, it is much cheaper and more reliable than renewables such as wind and solar. In the generation of electricity, its real competition is natural gas.",
  "question": "Is it this paragraph that makes the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q9eea3d907f",
  "kind": "yes/no",
  "text": "Table caption: Calculated values of Cr eq /Ni eq and solidification modes for coated, outside-uncoated, inside-uncoated and all-uncoated welds. FA denotes Ferritic-Austenitic mode, and A denotes Austenitic mode.\n| Weld/region No. | Cr eq /Ni eq | Solidification mode |\n| Coated/I | 1.92 | FA |\n| Coated/II | 1.65 | FA |\n| Outside-uncoated/I | 0.91 | A |\n| Outside-uncoated/II | 0.88 | A |\n| Inside-uncoated/I | 0.88 | A |\n| Inside-uncoated/II | 0.74 | A |\n| All-uncoated/I | 0.09 | A |\n| All-uncoated/II | 0.08 | A |\n\nStatement: 0.91 Cr eq /Ni eq Weld/region No. is Outside-uncoated/I.",
  "question": "Based on the table, is the statement supported?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q04a59c2339",
  "kind": "yes/no",
  "text": "Situation: Man Trolling on Dating Sites Is Not Ready to Fall in Love\nAction being judged: Not treating others with respect.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q10f1f476fc",
  "kind": "yes/no",
  "text": "Statement 1: bees like to gather honey\nStatement 2: dragonflies like to collect honey",
  "question": "Is it accurate to say that, of these two statements, Statement 1 doesn't go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "qe1c198d0cb",
  "kind": "yes/no",
  "text": "Complaint narrative: MY VSC OFF LIGHT HAS BEEN BLINKING WHEN I STARTED MY TRUCK WHEN I GOT OFF WORK AT 3:00P.M. CENTRAL TIME. MY CHECK ENGINE LIGHT IS ON AS WELL. I BROUGHT MY TRUCK TO AUTO ZONE FOR A DIAGNOSTICS TEST AND CAME UP WITH CODE P2440. MY VSC OFF LIGHT CAME ON ONE DAY NOT LOO LONG AGO, BUT WENT OFF SO I THOUGHT NOTHING OF IT. LOSS OF POWER.",
  "question": "Does this vehicle safety complaint state that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q2c66e90c1c",
  "kind": "yes/no",
  "text": "The article begins with an account of British Prime Minister Tony Blair's visit to the Bush ranch for a meeting with the \"cowboy president.\" President Bush's plans to take Blair on a tour of the ranch were ruined by severe thunderstorms and golf-ball-sized hail. The article fingers global warming as the culprit. \"But that possibility apparently seemed as remote to Bush as the likelihood that the storm was a sign from God,\" it said.",
  "question": "Is this paragraph making the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 }
]
