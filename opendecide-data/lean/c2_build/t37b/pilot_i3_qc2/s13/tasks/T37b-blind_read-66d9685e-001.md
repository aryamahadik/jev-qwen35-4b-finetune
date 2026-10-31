# T37b blind solver T37b-blind_read-66d9685e-001 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3_qc2/s13/answers/T37b-blind_read-66d9685e-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
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
 },
 {
  "qid": "qdf42348fea",
  "kind": "yes/no",
  "text": "Complaint narrative: MY CAR SMELLS LIKE BURNT OIL AFTER DRIVING IT. I REPORTED IT TO MY DEALER A NUMBER OF TIMES TRYING TO GET AN APPOINTMENT AFTER I GOT MY RECALL BUT THEY STILL SAY THEY DON'T HAVE THE PARTS THIS IS A SERIOUS FIRE HAZARD PLEASE HELP.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q55fa2e125b",
  "kind": "yes/no",
  "text": "Customer: Hi! How are you?\nAgent: I am good. What can I help you with?\nCustomer: I am looking to purchase tickets to get see a movie.\nAgent: I understand. Are there any particular movies that you want to see?\nCustomer: None in particular. I just want to see what my options are.\nAgent: Okay. What is your location?\nCustomer: I am on assignment in a Seven Trees, Nebraska.\nAgent: Okay, I have Holiday Cinemark 12 which is 30 miles away from you in the town of Butte Crest.\nCustomer: 30 miles? Is there anything closer than that?\nAgent: Mountain AMC 16 which is 22 miles away in the town of North Fork is the only theater that is closer.\nCustomer: So the closest theater is 22 miles away from me?\nAgent: Yes, that is correct.\nCustomer: That is too far. I am not going to drive that distance to see a movie.\nAgent: There is nothing closer to Seven Trees, Nebraska at this moment. I apologize.\nCustomer: Okay, I am not going to go to the movies then. Thank you anyways.\nAgent: You are welcome.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q9e070f5bcb",
  "kind": "yes/no",
  "text": "Occupation: Wind Energy Development Managers\nDuties:\n- Participate in special education-related activities, such as attending meetings and providing support to special educators throughout the district.\n- Establish, coordinate, and oversee particular programs across school districts, such as programs to evaluate student academic achievement.\n- Advocate for new schools to be built, or for existing facilities to be repaired or remodeled.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q5552c37cd0",
  "kind": "yes/no",
  "text": "Assistant: It will be ready in 15 min.\nCustomer: Great.\nAssistant: I have you down for Tall Latte with a lemon bar.",
  "question": "According to the assistant's last message, is \"Latte\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9b81b2167d",
  "kind": "yes/no",
  "text": "Table caption: Description of columns in ASCII text table.\n| Column Name | Description |\n| System | Multibeam echosounder system |\n| Date | Date of survey, yyyymmdd. |\n| Time | Time of survey (UTC), hhmmss. |\n| Easting | Easting Cartesian coordinate, UTM Zone 27 N projection, WGS84. |\n| Northing | Northing Cartesian coordinate, UTM Zone 27 N projection, WGS84. |\n| Depth | Corrected and processed depth, m. |\n| Latitude | Geographical latitude, DD;MM.mm, WGS1984. |\n| Longitude | Geographical longitude, DD;MM.mm, WGS1984. |\n\nStatement: ASCII text table has two categories- Column Name and Description.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q734729ea9c",
  "kind": "yes/no",
  "text": "Assistant: Tom's bistro and italiano pasta house are both open on friday.\nCustomer: make a reservation for 6 at Tom's Bistro friday at 6:30 pm\nAssistant: There is not a table available at 6 pm",
  "question": "According to the assistant's last message, is \"6 pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5323587fee",
  "kind": "yes/no",
  "text": "Table caption: CEO tenure, chair duality, and compensation. This table presents the relations between the CEO's tenure and CEO-chair duality (columns 1–2) or total current compensation including salary and bonus (columns 3–4). The sample is the same as that in , except for columns 3 and 4, in which the sample is from 1936 to 2011 and conditions on CEO compensation data. Columns 2 and 4 measure CEO tenure effects using the instrumental variable approach of , which, at each point in time, reflects the proportion of a given CEO's ultimate tenure. These columns display within-firm R-squared, while columns 1 and 3 show total R-squared. Firm and year fixed effects are included in all specifications. All standard errors are adjusted for sample clustering at the firm level. *, **, and *** represent results significant at the 10%, 5%, and 1% levels, respectively.\n| Dep. var. | 1 (Chair duality) | 1 (Chair duality) | Log(Compensation) | Log(Compensation) |\n|  | (1) | (2) | (3) | (4) |\n| Model: | OLS | AS-IV | OLS | AS-IV |\n| CEO tenure | 2.180*** | 2.382*** | 0.024*** | 0.025*** |\n|  | (26.38) | (30.04) | (5.73) | (9.11) |\n| log(board size) | –11.369*** | –11.406*** | 0.039 | 0.042 |\n|  | (–7.93) | (–7.96) | (0.47) | (0.52) |\n| log(assets) | 2.998*** | 2.906*** | 0.293*** | 0.293*** |\n|  | (4.55) | (4.40) | (7.56) | (7.86) |\n| q | 0.750* | 0.752* | 0.007 | 0.007 |\n|  | (1.77) | (1.77) | (0.19) | (0.20) |\n| ROA (ind-adj) | 1.168 | 0.681 | 1.463*** | 1.419*** |\n|  | (0.36) | (0.21) | (4.37) | (4.53) |\n| Stock return (ind-adj) | – | – | 0.214*** | 0.214*** |\n|  | – | – | (4.35) | (4.42) |\n| Tangibility | 4.524 | 4.403 | –0.110 | –0.118 |\n|  | (1.24) | (1.20) | (–0.69) | (–0.74) |\n| Firm fixed effects | Y | Y | Y | Y |\n| Year fixed effects | Y | Y | Y | Y |\n| R 2 | 0.534 | 0.197 | 0.880 | 0.832 |\n| N | 67,887 | 67,259 | 3323 | 3314 |\n\nStatement: ROA (ind-adj) 1 (Chair duality) under OLS is (26.38).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa72c5e86f5",
  "kind": "yes/no",
  "text": "\"The next generation of entrepreneurs will be focusing on climate change adaptation products, and in a world where billions of people face these challenges, there is a huge marketand enormous payofffor those who succeed.\"",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qe5865c75ff",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nRates of ventilation in the HC, HC+AZ, and no HC groups were 13.3%, 6.9%, 14.1%, respectively. The risk of ventilation was similar in the HC group (adjusted hazard ratio, 1.43; 95% CI, 0.53 to 3.79; P=0.48) and in the HC+AZ group (adjusted hazard ratio, 0.43; 95% CI, 0.16 to 1.12; P=0.09), compared to the no HC group. CONCLUSIONS: In this study, we found no evidence that use of hydroxychloroquine, either with or without azithromycin, reduced the risk of mechanical ventilation in patients hospitalized with Covid-19.\n\nClaim: Hydroxychloroquine does not help patients avoid being placed on a ventilator.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qa13f2ee15b",
  "kind": "yes/no",
  "text": "Brian Christley, a resident of Abergele, Wales, wrote to the Daily Telegraph : Over the weekend just gone, the coldest of the year so far, all 100-plus off-shore wind turbines along the North Wales coast were idling very slowly, all using grid power for de-icing and to power their hydraulic systems that keep the blades facing in the same direction.",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q88bc6f9e7a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Dodon was appointed to the post of Associate Minister of Trade and Economics in May 2005, during the second Tarlev Cabinet.\n- He assumed the position of Minister of Trade and Economics in September 2006.\n- He held the position until September 2009, when the government of Zinaida Greceanîi ended.\n- In September 2009, after 8 years of governing, the Communist Party came into opposition.\n- He became an MP in the Parliament, which was reelected in November 2010.\n- After he was elected as the president of Moldova, due to specifics of Moldovan law, Dodon resigned as PSRM chairman and left the party, being replaced by Zinaida Greceanîi as interim leader.\n- Dodon was sworn in on 23 December 2016 in the Palace of the Republic.\n\nSummary sentence:\nHe served as minister of trade and economics in the governments of Vasile Tarlev and Zinaida Greceanîi from September 2006 to September 2009 and was a member of the Parliament of Moldova from 2009 to 2016.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qcf087b7b55",
  "kind": "yes/no",
  "text": "Statement 1: Helmet is a thing which we wear on head\nStatement 2: Socks is a thing which we wear on neck",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q7df85dd92c",
  "kind": "yes/no",
  "text": "Customer: I need to buy tickets for Possession for me and my mom.\nAgent: How many tickets?\nCustomer: Two tickets.\nAgent: What day is this purchase for?\nCustomer: Today.\nAgent: What theater would you like?\nCustomer: Which theater has the latest showtime?\nAgent: Cima Ultraplex 20 has showings at 4:00pm, 6:10pm, and 8:30pm.\nCustomer: What about the other theater?\nAgent: Northgate Cinemas 12 has showings at 6:00pm, 8:10pm, and 10:25pm.\nCustomer: I'll do Northgate Cinemas 12 at 10:25 pm.\nAgent: Okay. To confirm, it is two tickets for Possession at Northgate Cinemas 12 at 10:25 pm tomorrow?\nCustomer: No, the tickets are for today.\nAgent: Sorry about that. Two tickets for Possession at Northgate Cinemas 12 at 10:25 pm today.\nCustomer: Yes, that is correct.\nAgent: Your tickets are confirmed and they've been sent to your email address.\nCustomer: Okay, thank you.\nAgent: You're welcome. Have a good day.\nCustomer: Goodbye.\nAgent: Goodbye.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qe31291adf7",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nVirus was widely distributed on floors, computer mice, trash cans, and sickbed handrails and was detected in air ≈4 m from patients.\n\nClaim: The coronavirus can be detected in the air up to 13 feet away from an infected patient.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q911f90c729",
  "kind": "yes/no",
  "text": "Customer: Yes, please book starting Thursday for 4 people and for 4 nights.\nAssistant: I'm sorry, there were no rooms available. Would you like to find another hotel?",
  "question": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "qed49450b2f",
  "kind": "yes/no",
  "text": "Statement 1: You are likely to find a dolphin in sea.\nStatement 2: You are likely to find a dolphin in a pond.",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qfc4d6abae9",
  "kind": "yes/no",
  "text": "Let's consider an alternate investment in gas turbine electric generation, and assume it and the wind turbines are displacing coal-fired power. Per Kw-H, gas turbines are going to, even including the fuel, produce power for a fourth or less the cost of wind with these relatively small turbines. And gas is plentiful and most of it comes from the gold old USofA (or at least North America).",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q7858b4f2d8",
  "kind": "yes/no",
  "text": "It should be paid for by those who want it, not by captive taxpayers or electricity consumers.",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q027232e80f",
  "kind": "yes/no",
  "text": "Customer: I'm also looking for an attraction preferably on a boat in the west.\nAssistant: There are no boats in the west, can I try something else for you?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qceabcea1f3",
  "kind": "yes/no",
  "text": "Occupation: Software Quality Assurance Analysts and Testers\nDuties:\n- Document software defects, using a bug tracking system, and report defects to software developers.\n- Participate in product design reviews to provide input on functional requirements, product designs, schedules, or potential problems.\n- Test system modifications to prepare for implementation.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q36c4cda120",
  "kind": "yes/no",
  "text": "Customer: Yes, please try for 12:00\nAssistant: I'm sorry. I'm not sure what is going on. It will not let me book. Would you like to try a different restaurant?",
  "question": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "qb6fce1eb4d",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2007 CHEVROLET TAHOE. WHILE DRIVING APPROXIMATELY 35 MPH, THE CONTACT NOTICED A BURNING ODOR FROM THE FRONT OF THE VEHICLE. THE WINDSHIELD WIPER FLUID FUNCTION FAILED AND THE RADIO CONTINUED TO FUNCTION AFTER THE CONTACT SHUT THE VEHICLE OFF. THE CONTACT WAS ABLE TO RESTART THE VEHICLE, BUT THE FAILURES RECURRED. THE CONTACT ALSO MENTIONED THAT THE BATTERY WARNING LIGHT WOULD ILLUMINATE INTERMITTENTLY. THE VEHICLE WAS NOT DIAGNOSED OR REPAIRED. THE VEHICLE WAS PREVIOUSLY REPAIRED UNDER NHTSA CAMPAIGN NUMBER: 10V240000 (ELECTRICAL SYSTEM). THE MANUFACTURER WAS NOT MADE AWARE OF THE FAILURE. THE APPROXIMATE FAILURE MILEAGE WAS 110,000.",
  "question": "Does this vehicle safety complaint report that at least one person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q4d91032d0a",
  "kind": "yes/no",
  "text": "Occupation: Executive Secretaries and Executive Administrative Assistants\nDuties:\n- Provide clerical support to other departments.\n- Attend meetings to record minutes.\n- Prepare agendas and make arrangements, such as coordinating catering for luncheons, for committee, board, and other meetings.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q32f5ad55a4",
  "kind": "yes/no",
  "text": "Customer: Hi, can you help me search for films in my area?\nAgent: Sure thing. Can I get your locations to start?\nCustomer: Yes, I am in Spring Hills Kansas.\nAgent: Okay, great. hat movies did you want me to search for you?\nCustomer: I have two films in mind. Once is called Shuttered and the other is called Beyond The Storm.\nAgent: Okay, let me check those titles for you, give me one second.\nCustomer: Sure.\nAgent: Okay, I do see both films playing in separate theaters near you.\nCustomer: Okay, great. I just need to know what the critic scores are for these two films.\nAgent: Sure. Shuttered has a critic score of 61%, and Beyond The Storm has a score of 81%\nCustomer: Great, I just want to confirm, these are both horror movies right?\nAgent: No. Shuttered is the only horror movie out of the two titles. Beyond The Storm is an action film.\nCustomer: Oh, I see. I think I'll go with the horror movies.\nAgent: Great choice. Do you need help getting tickets?\nCustomer: Yes, please.\nAgent: Okay, no problem. Shuttered is playing at the AMC Holiday Theater 3:00pm, 5:45 and 9:00pm. Which show time would you like to book for?\nCustomer: I'll book two tickets for the 9pm show.\nAgent: You have 2 tickets to see Shuttered at the AMC Holiday theater at 9pm tonight.\nCustomer: Yes, that's right.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q0a251bfeae",
  "kind": "yes/no",
  "text": "Assistant: Okay, what name and number do you want to put as their contact information?\nCustomer: Jay Turk, 555-555-5555\nAssistant: Okay! I've made an appointment under the name Jay Turk and they will contact you at 555-555-5555 when the vehicle is ready",
  "question": "According to the assistant's last message, is \"Jay Turk\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qab049b03db",
  "kind": "yes/no",
  "text": "Customer: I'm looking for a restaurant that serves afghan food in the south\nAssistant: I have not found any, unfortunately. Would you like to try another area of town or cuisine?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q32d712d69c",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nOur phylogenetic analysis places the majority of these genomes with viruses sequenced from Washington state. By coupling our genomic data with domestic and international travel patterns, we show that early SARS-CoV-2 transmission in Connecticut was likely driven by domestic introductions.\n\nClaim: Widespread cases of COVID-19 in the United States can be traced to international transmission.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qeb826f5493",
  "kind": "yes/no",
  "text": "Statement 1: I planted a puppy in the backyard.\nStatement 2: I planted a tree in the backyard.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qb17bd7c541",
  "kind": "yes/no",
  "text": "Table caption: Papers dealing with the top 4 metallic elements in JIB, and their growths since 1983, and a few specific topics (cancer and anticancer; oxidation and reduction). Data from WoS, July 1, 2020 .\n| Element | 1973–1983 | Last 25 years | Last 10 years | 1973–2020 | Citations | h index |\n| Cu | 90 | 1500 | 638 | 1777 | 46,615 | 90 |\n| Fe | 33 | 1017 | 348 | 1153 | 27,549 | 74 |\n| Pt | 15 | 644 | 283 | 728 | 19,882 | 65 |\n| Zn | 35 | 590 | 267 | 691 | 17,392 | 62 |\n| Cancer and anticancer | 8 | 1177 | 832 | 1201 | 32,343 | 76 |\n| Oxidation or reduction | 38 | 1354 | 570 | 1488 | 37,550 | 84 |\n\nStatement: The highest Citations is 17,392.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa38a07698e",
  "kind": "yes/no",
  "text": "Occupation: Private Detectives and Investigators\nDuties:\n- Observe and document activities of individuals to detect unlawful acts or to obtain evidence for cases, using binoculars and still or video cameras.\n- Conduct private investigations on a paid basis.\n- Obtain and analyze information on suspects, crimes, or disturbances to solve cases, to identify criminal activity, or to gather information for court cases.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qa6f80652e8",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Bachchan's first release of 2005 was the crime comedy \"Bunty Aur Babli\", which featured him and Rani Mukerji as the titular con artist duo who perform several successful heists and fall in love along the way.\n- His next two releases \"Dus\" (2005) and \"Bluffmaster!\"\n- (2005) were both moderately successful, but did not earn much critical appreciation.\n- Bachchan earned much critical acclaim for his performance in Mani Ratnam's \"Guru\" (2007), loosely based on the life of business magnate Dhirubhai Ambani.\"\n- His next release was the dance comedy \"Jhoom Barabar Jhoom\" (2007) alongside Preity Zinta, Bobby Deol, and Lara Dutta.\n- Bachchan's first release of 2008 was Ram Gopal Varma's \"Sarkar Raj\", which featured him and his father Amitabh Bachchan reprising their roles from \"Sarkar\" (2005) while his wife Aishwarya Rai Bachchan entered the cast as a new addition.\n- This film proved to be successful at the box office and earned him a nomination for the Filmfare Award for Best Supporting Actor.\n- Bachchan was next seen in \"Dostana\" (2008), a romantic comedy about two men (Bachchan and John Abraham) who pretend to be gay in order to be allowed to live with a girl (Priyanka Chopra), but then find that they have both fallen in love with her.\n- These films were the thriller \"Raavan\" (2010), the social drama \"Khelein Hum Jee Jaan Sey\" (2010), action thrillers \"Game\" (2011), \"Dum Maaro Dum\" (2011) & the heist thriller \"Players\" (2012).\n- Bachchan then played the lead role in Rohit Shetty's comedy \"Bol Bachchan\" (2012), which was a major blockbuster at the box office despite receiving mixed reviews from critics.\n- Bachchan was next seen in Farah Khan's dance comedy \"Happy New Year\", a musical heist film, playing the second lead to Shah Rukh Khan.\n- Bachchan's first release of 2016 was the comedy \"Housefull 3\", the third installment of the Housefull film series.\n\nSummary sentence:\nBachchan has also played leading and supporting roles in commercially successful comedies and dramas, including \"Bunty Aur Babli\" (2005), \"Dus\" (2005), \"Bluffmaster!\" (2005), \"Guru\" (2007), \"Jhoom Barabar Jhoom\" (2007), \"Sarkar Raj\" (2008), \"Dostana\" (2008), \"Dum Maaro Dum\" (2011), \"Bol Bachchan\" (2012), \"Happy New Year\" (2014) and \"Housefull 3\" (2016).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q8059699d87",
  "kind": "yes/no",
  "text": "So given never let a crisis to to waste it is a very short stroll over to manufacture a crisis as needed. The thing that surprised me was how many folks some of these videos had that watched them, and how many videos there were. Large chunks of the world culture are clearly quite willing to embrace the Conspiracy Conjecture. (Conjecture as it isnt even a hypothesis, never mind a thesis or theory. Hypo meaning below or less than a thesis. Theory being generally accepted as true.)",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q9c4a959092",
  "kind": "yes/no",
  "text": "Situation: A part of me is really okay with most of the baby boomers dying. I've blamed them for a lot of the bad things we're dealing with today and resent their stubbornness\nAction being judged: Judging an entire generation.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q9819d4e527",
  "kind": "yes/no",
  "text": "Situation: I'm fantasizing about a coworker\nAction being judged: Doing things that could make a coworker uncomfortable.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qf8dce091d0",
  "kind": "yes/no",
  "text": "Customer: I think I'd like to see a movie tonight.\nAgent: Sounds like a plan. Which movie do you want to see?\nCustomer: I think I'll take my daughter to see Sonic the Hedgehog tonight.\nAgent: So, just two tickets?\nCustomer: Yes, just two standard tickets.\nAgent: Which theater were you thinking of seeing it at?\nCustomer: What are the times for Philadelphia Mills AMC?\nAgent: There's a 5:15 PM and a 7:15 PM showing.\nCustomer: That's not much of an option. What about Woodhaven AMC?\nAgent: The showtimes for this evening are 4:45 PM, 6:30 PM, 7:00 PM, 7:30 PM, 9:15 PM, 9:45 PM and 10:15 PM.\nCustomer: 6:30 PM is fine.\nAgent: Okay, so two tickets tonight at Woodhaven AMC for Sonic the Hedgehog at 6:30 PM?\nCustomer: Actually, now that I think about it, 6:30 PM might not work.\nAgent: Would you like the showtimes for a different theater?\nCustomer: No, Woodhaven AMC is fine. I think I'll make it for 7:30 PM instead.\nAgent: So, 7:30 PM instead of 6:30 PM?\nCustomer: Yes.\nAgent: I'll book two tickets tonight for Sonic the Hedgehog at Woodhaven AMC for 7:30 PM?\nCustomer: That's correct.\nAgent: You'r tickets are booked and the confirmation has been emailed to you.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q7bcab36518",
  "kind": "yes/no",
  "text": "Table caption: Peptide match of ARIP-B.\n| S. No | Plant description | Match Coverage (%) | Total Coverage (%) | RIP activity reported | RIP gene identified | Type of RIP | References |\n| 1 | Populus trichocarpa | 2 + 1 + 1 + 3 + 3 | 10 | Yes | Yes | Type 2 (B domain only) | Peumans and Vandamme (2010) |\n| 2 | Astragalus membranaceus | 10 | 10 | No | No | – | – |\n| 3 | Polygala tenuifolia | 1 | 1 | No | No | – | – |\n| 4 | Vitis vinifera | 0 + 2 | 2 | Yes | No | – | Peumans and Vandamme (2010) |\n| 5 | Triticum aestivum | 2 | 2 | Yes | Yes | Type 1 | Raj and Vennila (2013) |\n| 6 | Glycine max | 2 + 1 | 3 | Yes | No | – | Peumans and Vandamme (2010) |\n| 7 | Brachypodiumdistachyon | 1 | 1 | Yes | Yes | Type 3 | Peumans and Vandamme (2010) |\n| 8 | Hordeum vulgare | 3 | 3 | Yes | Yes | Type 1 | Raj and Vennila (2013) |\n| 9 | Ricinus communis | 2 | 2 | Yes | Yes | Type 2 | – |\n| 10 | Micromonaspusilla | 1 | 1 | Yes | No | – | Peumans and Vandamme (2010) |\n| 11 | Musa acuminata subsp. | 11 | 11 | No | No | – | – |\n| 12 | Arabidopsis lyrata subsp. | 3 | 3 | No | No | – | Peumans and Vandamme (2010) |\n\nStatement: There are four categories of Plant description.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q52a1711a61",
  "kind": "yes/no",
  "text": "Complaint narrative: I BROUGHT MY VEHICLE INTO KIA FOR SEVERAL RECALLS. ONE WAS THE DOOR LOCKS BEING FAULTY. I SAID I HAD NO PROBLEMS BUT THEY DECIDED TO REPLACE THEM ANYWAY. NOW MY REAR DOOR LOCK IS BROKEN. THE OTHER ISSUE IS WHEN ACCELERATING THE ENGINE REVS. IT ONLY HAPPENED A COUPLE OF TIMES AT FIRST, BUT NOW IT HAPPENS EVERY TIME I DRIVE. IT SEEMS LIKE THE PEDAL IS GETTING STUCK. MY LAST ISSUE IS THE AIR BAG. I WAS REAR ENDED ON THE HIGHWAY AND PUSHED INTO THE CAR IN FRONT OF ME. THE WHOLE FRONT END WAS BANGED UP AND THE AIRBAG NEVER OPENED.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qb457956182",
  "kind": "yes/no",
  "text": "John Cameron Mitchell\nJohn Cameron Mitchell (born April 21, 1963) is an American actor, writer and director, best known for originating the title role in the musical \"Hedwig and the Angry Inch\", and reprising it in the 2001 film adaptation directed by him, as well as for directing the films \"Shortbus\" (2006) and \"Rabbit Hole\" (2010).\n\nWilliam S. Hart\nWilliam Surrey Hart (December 6, 1864 – June 23, 1946) was an American silent film actor, screenwriter, director and producer. He is remembered as a foremost western star of the silent era who \"imbued all of his characters with honor and integrity.\" During the late 1910s and early 1920s, he was one of the most consistently popular movie stars, frequently ranking high among male actors in popularity contests held by movie fan magazines.",
  "question": "Are William S. Hart and John Cameron Mitchell both American actors?",
  "definitions": "- yes: Read together, the paragraphs show the answer is yes: what the question asks holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right).\n- no: The paragraphs do not bear out a yes: at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer."
 },
 {
  "qid": "q0fea3e24bf",
  "kind": "yes/no",
  "text": "New York City is 1199's true power center, however. It's hard to overstate the significance of 1199 to the so-called progressive movement that now controls almost every major city office. City council speaker and leader of the Progressive Caucus Melissa Mark-Viverito is a former organizer for 1199, which has played an active role in her career from the beginning. The union suggested that the Puerto Ricanborn and Columbia Universityeducated heiress move from Greenwich Village to East Harlem to establish a political base. To help her launch her campaign for the city council speakership, 1199 threw a lavish party in San Juan. The union's political director, Kevin Finnegan, served on Mark-Viverito's transition team when she became speaker.",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qb671c47505",
  "kind": "yes/no",
  "text": "Occupation: Carpenters\nDuties:\n- Determine connection interfaces for additional subpanels or for connecting photovoltaic (PV) systems with utility services or other power generation sources.\n- Perform routine photovoltaic (PV) system maintenance on modules, arrays, batteries, power conditioning equipment, safety systems, structural systems, weather sealing, or balance of systems equipment.\n- Identify methods for laying out, orienting, and mounting modules or arrays to ensure efficient installation, electrical configuration, or system maintenance.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q611a4198c7",
  "kind": "yes/no",
  "text": "A British High Court judge ruled that \"An Inconvenient Truth\" promotes \"partisan political views,\" was riddled with errors and falsehoods, and could not be shown any more in schools, unless accompanied by a teacher's guide correcting information that Gore had misrepresented. Two of the most egregious distortions are especially likely to scare kids.",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qab378591a6",
  "kind": "yes/no",
  "text": "Situation: Carl asked him if he could meet him to return his phone.\nAction being judged: Letting your friends borrow your things as long as they return them.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q2792cfeaf9",
  "kind": "yes/no",
  "text": "Hereward Corley pointed out that the reference to Shaviv (2008) should have been Shaviv (2005). Nir Shaviv another genius of a mathematician had originally sent me the paper saying it was from 2008, but the version he sent was an undated pre-publication copy. Mr. Corley also kindly supplied half a dozen further papers that determine climate sensitivity empirically. Most of the papers find it low, and all find it below the IPCCs estimates. The papers are Chylek & Lohman (2008); Douglass & Knox (2005); Gregory et al. (2002); Hoffert & Covey (1992); Idso (1998); and Loehle & Scafetta (2011).",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q6443421181",
  "kind": "yes/no",
  "text": "Complaint narrative: THE SENSOR THAT DETERMINES IF THE PASSENGER AIRBAG TURNS ON DOES NOT WORK PROPERLY. I WEIGH 100 POUNDS (WHICH IS ABOVE THE THRESHOLD FOR WHAT SHOULD TRIGGER THE AIRBAG TO BE ON) AND ABOUT HALF THE TIME THE AIRBAG IS DISABLED WHEN I AM SITTING IN THE SEAT PROPERLY WITH MY FEET ON THE GROUND AND THE CHAIR UPRIGHT. I CONTACTED CHEVROLET TO HAVE THEM REIMBURSE THE COST OF FIXING THIS ISSUE BECAUSE IT IS A SAFETY ISSUE AND HAS CAUSED RECALLS IN OTHER CHEVROLET CARS, BUT THEY HAVE REFUSED TO INVESTIGATE. THE SENSOR MALFUNCTION DOESN'T SEEM TO BE CORRELATED WITH WHETHER THE VEHICLE IS STATIONARY, IN MOTION, ON A STREET OR HIGHWAY, ETC. IT HAPPENS ABOUT HALF OF THE TIME AND CAN SOMETIMES GO ON AND OFF DURING THE SAME CAR TRIP EVEN IF I STAY IN THE SAME POSITION THE WHOLE TIME. THIS ISSUE HAS REPORTED FOR CHEVROLET MALIBUS ON SEVERAL ONLINE FORUMS SO I KNOW IT ISN'T AN ISOLATED ISSUE WITH MY CAR. WE ARE CONCERNED ABOUT WHAT COULD HAPPEN IF WE WERE IN A CRASH AND THE AIRBAG DIDN'T GO OFF OR WENT OFF LATE WHEN THE PASSENGER'S BODY WAS TOO CLOSE TO THE AIRBAG.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q71d9a4d272",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- As of 2019, Shah has denied any wrongdoing.\n\nSummary sentence:\nHe has claimed innocence.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q1b4f67bcba",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nImportance: The pandemic of coronavirus disease 2019 (COVID-19) caused by the novel severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) presents an unprecedented challenge to identify effective drugs for prevention and treatment. No therapies have been shown effective to date.\n\nClaim: At the time of writing, there were several effective therapies in combatting COVID-19.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q59f78f3457",
  "kind": "yes/no",
  "text": "Using data from the Intergovernmental Panel on Climate Change (IPCC), a Science and Public Policy Institute paper published last month found that if the United States eliminated all carbon dioxide emissions, the overall impact on global temperature rise would be only 0.08 degrees Celsius by 2050.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qe9861a3b24",
  "kind": "yes/no",
  "text": "Occupation: Podiatrists\nDuties:\n- Teach or train medical staff regarding preventive medicine issues.\n- Direct or manage prevention programs in specialty areas such as aerospace, occupational, infectious disease, and environmental medicine.\n- Coordinate or integrate the resources of health care institutions, social service agencies, public safety workers, or other organizations to improve community health.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 }
]
