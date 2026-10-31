# T37b blind solver T37b-blind_read-9b3e560e-001 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_qc6/s13/answers/T37b-blind_read-9b3e560e-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q755a46e2d2",
  "kind": "yes/no",
  "text": "Table caption: The categories inventoried as industrial process emissions.\n| Sub-sector | Sub-sub-sector ( a NFR code) |\n| Mineral products | Cement production (2.A.1) Lime production (2.A.2) Asphalt roofing (2.D.3.c) Asphalt road paving (2.D.3.b) |\n| Chemical industry | Ammonia (2.B.1) Nitric acid (2B.2) Adipic acid (2.B.3) Carbon black (2.B.10.a) Urea (2.B.10.a) Ammonium nitrate (2.B.10.a) Ammonium phosphate (2.B.10.a) Sulphuric acid (2.B.10.a) Titanium dioxide (2.B.6) |\n| Metal production | Pig iron production (1.A.2.a) Aluminium production (2.C.3) Copper smelting (primary and secondary) (2.C.7) Lead smelting (primary and secondary) (2.C.5) Zinc smelting (primary and secondary) (2.C.6) |\n| Pulp and Paper Industries | Kraft or Alkaline soda pulping (2.H.1) Acid sulphite pulping (2.H.1) Neutral sulphite semi-chemical (2.H.1) |\n| Food and Drink | Alcoholic Beverages (2.H.2) Food Production (2.H.2) |\n| Fugitive emissions of PM from major construction activities |  |\n\nStatement: They have six sub sector.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q6584c7291b",
  "kind": "yes/no",
  "text": "Table caption: Granulometric properties of the soils (mass %).\n| Clay | Silt | Sand | Gravel | Rubble | Name of mine |\n| 37.9 | 51.9 | 9.9 | 0.3 | – | S E |\n| 31.4 | 55.8 | 12.8 | – | – | S M |\n| 34.7 | 60.7 | 4.6 | – | – | S H |\n| 29 | 57.4 | 9.3 | 4.2 | – | S GH |\n| 10 | 79.7 | 10.1 | 0.1 | – | S A |\n| 35.6 | 52.5 | 11.8 | 0.1 | – | S Z |\n\nStatement: SA and SH has same gravel value.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qebea589bfc",
  "kind": "yes/no",
  "text": "Table caption: Peptides from L. fermentum HFD1 with predicted antimicrobial activity\n| № | The protein ID | Peptide sequence | ADAM | CAMPR3 | CAMPR3 | CAMPR3 | AMPA |  | Length in peptidome |\n| № | The protein ID | Peptide sequence | ADAM | SVM | Random Forest | DAC | AMPA | Length | Length in peptidome |\n| 1 | QIX58482.1 | MGLIWSLIVGAIIGAIAGAITNRGAAMGWIANIVAGLIGAWIGQGLLGTWGPSLAGMALIPSIIGAIILVLIVSLVVGRTGKK | 1.52 | 1.0 | 0.566 | 0.527 | 0.24 | 84 | 14 |\n| 2 | QIX58771.1 | MLSLITNTVIILLIIGCAFWQLVKVFKRAKKGKCAACDYDCAVKQQVLKQEKHGAQ | 0.82 | 0.889 | 0.6715 | 0.81 | 0.2226 | 56 | N/A |\n| 3 | QIX58909.1 | MAVKIKTPAGMIDIANDVIATVVGGAATDNYGVVGMASRNPLKDGVNQILGRDSFHQGVVIRQQDNGIAVDVYIIVGYGTKISAVSKSVQEKVKYNLEAMLGVTANSVNIMVQGVRVLGD | 0.09 | 1.00 | 0.9855 | 1.0 | 0.248 | 120 | N/A |\n| 4 | QIX58994.1 | MNNQSNVTPQNGNLQYKFCQNCGAKIDVKAVVCPKCGVPVNGNNAESNSEDRNNGWWNLLGFFFPIVGWILWAVWHKEYPKRAHGICVWSWVSFGISFVIGFVNGFLSTL | 1.32 | 1.00 | 0.7745 | 1.0 | 0.237 | 110 | N/A |\n\nStatement: The protein ID QIX58482.1 has Peptide sequence of MNNQSNVTPQNGNLQYKFCQNCGAKIDVKAVVCPKCGVPVNGNNAESNSEDRNNGWWNLLGFFFPIVGWILWAVWHKEYPKRAHGICVWSWVSFGISFVIGFVNGFLSTL.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qea4850d07c",
  "kind": "yes/no",
  "text": "Customer: Hi! How are you?\nAgent: I am good. What can I help you with?\nCustomer: I am looking to purchase tickets to get see a movie.\nAgent: I understand. Are there any particular movies that you want to see?\nCustomer: None in particular. I just want to see what my options are.\nAgent: Okay. What is your location?\nCustomer: I am on assignment in a Seven Trees, Nebraska.\nAgent: Okay, I have Holiday Cinemark 12 which is 30 miles away from you in the town of Butte Crest.\nCustomer: 30 miles? Is there anything closer than that?\nAgent: Mountain AMC 16 which is 22 miles away in the town of North Fork is the only theater that is closer.\nCustomer: So the closest theater is 22 miles away from me?\nAgent: Yes, that is correct.\nCustomer: That is too far. I am not going to drive that distance to see a movie.\nAgent: There is nothing closer to Seven Trees, Nebraska at this moment. I apologize.\nCustomer: Okay, I am not going to go to the movies then. Thank you anyways.\nAgent: You are welcome.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qedf81dbc83",
  "kind": "yes/no",
  "text": "Situation: When I am hungry, I eat.\nAction being judged: Eating when you are hungry.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q4960fa8ee9",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2008 HYUNDAI VERACRUZ. WHILE DRIVING 5 MPH, THE ABS MODULE MALFUNCTIONED AND CAUSED THE VEHICLE TO CATCH FIRE. THE CONTACT NOTICED SMOKE UNDER THE HOOD OF THE VEHICLE AND FLAMES IGNITED FROM THE BATTERY. A POLICE REPORT WAS NOT FILED. THE FIRE WAS EXTINGUISHED BY ATTENDANTS FROM A NEARBY AUTO BODY SHOP. THERE WERE NO INJURIES. THE VEHICLE WAS NOT DESTROYED. THE DEALER AND MANUFACTURER WERE NOT NOTIFIED. THE FAILURE MILEAGE WAS APPROXIMATELY 144,000.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qaf26958867",
  "kind": "yes/no",
  "text": "Situation: Glanced to my left and made eye contact with a lady\nAction being judged: Looking people in the eyes when you talk to them.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q17f4622811",
  "kind": "yes/no",
  "text": "Situation: Trash Talking Creates a Stink After Warring Couple Reconciles\nAction being judged: Reigniting a conflict that just ended.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qdd531d6cc7",
  "kind": "yes/no",
  "text": "Statement 1: he thought it would rain soon so he carried sunglasses\nStatement 2: he thought it would rain soon so he carried an umbrella",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q4ec52f1c21",
  "kind": "yes/no",
  "text": "Table caption: Correlations between HMB and SJ profiles.\n| Date | Correlation Coefficient | P-Value |\n| July 9, 2018 | 0.93 | 0.0 |\n| July 16, 2018 | 0.83 | 0.0 |\n| July 18, 2018 | 0.88 | 0.0 |\n| July 20, 2018 | 0.84 | 0.0 |\n| July 24, 2018 | 0.91 | 0.0 |\n| July 31, 2018 | 0.72 | 0.0 |\n| August 2, 2018 | 0.92 | 0.0 |\n| August 3, 2018 | 0.87 | 0.0 |\n| August 6, 2018 | 0.68 | 0.0 |\n| August 10, 2018 | 0.85 | 0.0 |\n| August 17, 2018 | 0.92 | 0.0 |\n| All dates | 0.79 | 0.0 |\n\nStatement: There are eleven different Dates of Correlations between HMB and SJ profiles.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qed0a770e9a",
  "kind": "yes/no",
  "text": "Complaint narrative: 2018 DODGE CARAVAN. CONSUMER WRITES IN REGARDS TO DEFECTIVE PASSENGER SEAT WHICH RESULTED IN INJURY TO PASSENGER. *LD THE CONSUMER STATED THE WHILE ATTEMPTING TO ADJUST THE SEAT TO AN UPRIGHT POSITION IT SLAMMED FORWARD AGAINST THE BACK OF THE HEAD. THIS CAUSED AND INJURY TO THE HEAD AND JAW. THE CONSUMER DID NOT SEEK MEDICAL ATTENTION. *JS *TT *BF",
  "question": "Does this vehicle safety complaint report that at least one person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q2f551bd287",
  "kind": "yes/no",
  "text": "Situation: Single Dad Never Pitches In at Neighborhood Potlucks\nAction being judged: Not contributing anything to a potluck you are going to.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qfe624ed6c9",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThese studies confirm that cats are susceptible to productive SARS-CoV-2 infection, but are unlikely to develop clinical disease.\n\nClaim: Cats can be infected by the novel coronavirus but are unlikely to get sick.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q38031fe185",
  "kind": "yes/no",
  "text": "Customer: I need a place to stay in the East. I don't need to have access to the Internet.\nAssistant: I have 7 places available in the east.  What is your price range?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qfb066cc013",
  "kind": "yes/no",
  "text": "Situation: Baby by a married man\nAction being judged: Cheating on your partner and having a baby with someone else.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "qc9c403b7e9",
  "kind": "yes/no",
  "text": "Customer: Hi, Can you help me find White Fang?\nAgent: Sure, do you mean the movie or book?\nCustomer: I mean what theater in Santa Rosa is it showing in now?\nAgent: There are 4, first is Rialto, is that what you'd like?\nCustomer: No, what about Airport Cinema?\nAgent: Sure, it is playing there, what time would you like a ticket for?\nCustomer: Is there something at 5:30 or so?\nAgent: There is a showing at 5:20, would you like tickets?\nCustomer: Sure, I think that will work.\nAgent: How many tickets would you like?\nCustomer: I need 2 please.\nAgent: Sure, 2 for White Fang 5:20, Santa Rosa Airport cinema, is that right?\nCustomer: No, I changed my mind, is there a 5:30 show at the Rialto?\nAgent: There is a 5:40 showing there, would you like to change to there?\nCustomer: Yes, make that change please.\nAgent: change is 2 for White Fang, at the Rialto, 5:40 pm., tonight, in Santa Rosa, regular type screening, is that right?\nCustomer: Yes that's good, thanks.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.\nCustomer: Great, I have them thanks.\nAgent: enjoy your show.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qa6133ea0ca",
  "kind": "yes/no",
  "text": "Customer: Yes. Are any of those restaurants in the centre of town?\nAssistant: Yes, there are three restaurants serving Turkish food in the center of town.",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q8dbd1d97d2",
  "kind": "yes/no",
  "text": "Customer: I want to watch a movie\nAgent: in theater or at home?\nCustomer: in theater\nAgent: do you have a movie in mind?\nCustomer: there are a few\nAgent: such as\nCustomer: ip man, star war, bad boys and a few others\nAgent: do you have a favorite\nCustomer: I don't have a favorite but I do want to watch star war, as well as ipman but I heard ipman may not be playing everywhere\nAgent: the review for ipman 4 is quite good just like the other threes\nCustomer: I always like that series, star war is ok too as I want to see its ending\nAgent: have we decided on a movie yet\nCustomer: if there is a showtime for ipman at landmark 81, book it, otherwise star war\nAgent: there is no ipman playing there, only starwar\nCustomer: then get me two tickets for 3d at 9 pm on saturday in 3d\nAgent: having a date sir?\nCustomer: sort of\nAgent: so 2 tickets for star war at 9 pm this Saturday in 3d\nCustomer: yes, but wait till I double check the schedule with my date\nAgent: all righty\nCustomer: thank you",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qc2abfdf872",
  "kind": "yes/no",
  "text": "Table caption: concentration of R and S amphetamine in seized tablets (mg/g).\n|  | Tablet weight (mg) | Concentration of R -amphetamine (mg/g) | RSD (%) | Concentration of S -amphetamine (mg/g) | RSD (%) | Total amphetamine (mg/g) | ee% |\n| 1 | 150.77 | 35.26 | 3.64 | 38.36 | 3.87 | 73.62 | 4.21 |\n| 2 | 168.67 | 47.82 | 3.81 | 48.40 | 2.48 | 96.22 | 0.60 |\n| 3 | 168.82 | 44.54 | 2.37 | 47.78 | 3.25 | 92.32 | 3.51 |\n| 4 | 165.55 | 30.82 | 3.43 | 31.62 | 1.75 | 62.44 | 1.28 |\n| 5 | 176.65 | 29.00 | 2.07 | 29.78 | 3.57 | 58.78 | 1.33 |\n| 6 | 169.18 | 17.94 | 3.69 | 18.5 | 3.20 | 36.44 | 1.54 |\n| 7 | 147.95 | 36.70 | 3.18 | 40.44 | 2.48 | 77.14 | 4.85 |\n| 8 | 168.70 | 19.02 | 2.63 | 19.86 | 2.44 | 38.88 | 2.16 |\n| 9 | 169.03 | 20.26 | 3.51 | 21.10 | 3.77 | 41.36 | 2.03 |\n| 10 | 166.75 | 37.16 | 2.96 | 45.16 | 2.11 | 82.32 | 9.72 |\n| 11 | 177.45 | 19.12 | 2.18 | 20.26 | 3.35 | 39.38 | 2.89 |\n| 12 | 166.06 | 44.68 | 1.6 | 49.66 | 3.39 | 94.34 | 5.28 |\n\nStatement: The Highest Concentration of R -amphetamine (mg/g) is 47.82.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q35e760a1bc",
  "kind": "yes/no",
  "text": "Customer: I'm looking to go see a movie at the theaters in Davis, California.\nAgent: No problem. Do you have a movie in mind?\nCustomer: I was thinking going to see about No Time To Die.\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: There's no showings in Davis, California then?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: Ah, that's too bad. Do you know what action films are being shown in Davis, California right now?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Is this the original Mad Max film from the 70s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: I think I'll pass, I was looking forward to seeing No Time To Die at the Davis Theaters. Thank you anyways.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qc21e45f542",
  "kind": "yes/no",
  "text": "Customer: You're right. I forgot to select an architectural sight that I wanted to visit. Could you suggest one in the city centre.\nAssistant: Sure thing. I would suggest the old schools.",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q905310dc2d",
  "kind": "yes/no",
  "text": "Customer: I'm looking for attractions that are in the centre, could you help me find some?\nAssistant: There are 44 attractions located in the Centre area.  Are you interested in any particular type of attraction to narrow down your choices?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q7a624a324b",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2014 DODGE CHARGER. WHILE DRIVING AT APPROXIMATELY 60 MPH, THE BRAKE PEDAL WAS DEPRESSED AND THE VEHICLE SLOWED DOWN, WHICH CAUSED THE CONTACT TO LOSE CONTROL AND CRASH INTO A DITCH. A POLICE REPORT WAS FILED. THE CONTACT SUSTAINED INJURIES TO THE NECK, CHEST, AND HEAD. MEDICAL ATTENTION WAS REQUIRED. THE VEHICLE WAS NOT DIAGNOSED OR REPAIRED. THE MANUFACTURER WAS NOT MADE AWARE OF THE FAILURE. THE APPROXIMATE FAILURE MILEAGE WAS 28,000.",
  "question": "Does this vehicle safety complaint report that at least one person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q66bf5f8bdf",
  "kind": "yes/no",
  "text": "Statement 1: She put a cotton pie in the oven to bake.\nStatement 2: She put an apple pie in the over to bake.",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q8b1d9e4222",
  "kind": "yes/no",
  "text": "Assistant: The Cedars offers several hot meals from the grill.\nCustomer: Great, get the tickets at The Cedars.\nAssistant: I've booked you for 2 tickets to The Upside at The Cedars for 6pm",
  "question": "According to the assistant's last message, is \"The Upside\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5ba71a2de0",
  "kind": "yes/no",
  "text": "Occupation: Robotics Engineers\nDuties:\n- Build, configure, or test robots or robotic applications.\n- Conduct research on robotic technology to create new robotic systems or system capabilities.\n- Design software to control robotic systems for applications, such as military defense or manufacturing.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q6281b46fc6",
  "kind": "yes/no",
  "text": "Table caption: Size Comparison of ZnO and TiO 2 nanoparticles synthesized using the plants.\n| Plant species | Plant part used | Synthesized NPs | Size (nm) | References |\n| Azadirachta indica, Emblica Officinalis | leaf | ZnO | 51, 16 |  |\n| Pyrus pyrifolia | leaf | ZnO | 45 |  |\n| Ixora coccinea | leaf | ZnO | 145.1 |  |\n| Passiflora caerulea | Leaf | ZnO | 200 |  |\n| Bauhinia tomentosa | Leaf | ZnO | 22–94 |  |\n| Pandanus odorifer | leaf | ZnO | 90 |  |\n| Allium sativum | Skin | ZnO | 7.77 |  |\n| Psidium guajava | Leaf | TiO 2 | 32.58 |  |\n| Cynodon dactylon | Leaf | TiO 2 | 13–34 |  |\n| Glycosmis cochinchinensis | Leaf | TiO 2 | 45 |  |\n| Cassia fistula | Leaf | TiO 2 | 200 |  |\n\nStatement: Plant part used are same for 10 Plant species that is leaf.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q29f2e4579f",
  "kind": "yes/no",
  "text": "Customer: Yes, please book starting Thursday for 4 people and for 4 nights.\nAssistant: I'm sorry, there were no rooms available. Would you like to find another hotel?",
  "question": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q66aa2621dd",
  "kind": "yes/no",
  "text": "Assistant: actually there is a problem\nCustomer: what kind of problem\nAssistant: there is no uber xl close by",
  "question": "According to the assistant's last message, is \"uber xl\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3dc36aa935",
  "kind": "yes/no",
  "text": "Assistant: That shouldn’t be a problem their easy to work right there.\nCustomer: Thank you.\nAssistant: I’m so sorry they don’t have any pineapples right now.",
  "question": "According to the assistant's last message, is \"pineapples\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe7384c1598",
  "kind": "yes/no",
  "text": "Customer: I need a restaurant that serves catalan food and it should be in the west.\nAssistant: Unfortunately, I'm not finding any Catalan restaurants in the west. Would you like me to look in other areas?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q2666bd0a92",
  "kind": "yes/no",
  "text": "Table caption: 3-D printing settings tested on the Cerberus.\n| Basic Printer Settings | Basic Printer Settings |  |  |  |\n| Material | Nozzle Temperature [ o C] | Bed Temperature [ o C] | Layer Height [mm] | Part Cooling Fan |\n| PEKK | 390 | 180 | 0.3 | OFF |\n| PEI/ULTEM | 380 | 170 | 0.3 | OFF |\n| Polycarbonate | 280 | 130 | 0.3 | ON or OFF |\n\nStatement: Nozzle Temperature will High for PEKK Material.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd7b9e99781",
  "kind": "yes/no",
  "text": "Drank too many 🍹 when I was in Thailand. Fucked me right up",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q3f591cba89",
  "kind": "yes/no",
  "text": "Assistant: It is great. Let me get that order placed in for you.\nCustomer: Thanks so much.\nAssistant: I'm seeing they're actually out of coconut milk for now. But they are offering soy and almond milk if you were trying to avoid dairy.",
  "question": "According to the assistant's last message, is \"coconut milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf7660d7242",
  "kind": "yes/no",
  "text": "Situation: My Mom &amp; Son broke in my place??\nAction being judged: People assuming they're allowed entry into the houses of people, even when they're family.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "qfbce7c04d1",
  "kind": "yes/no",
  "text": "Occupation: Bicycle Repairers\nDuties:\n- Install replacement glass in vehicles.\n- Replace or adjust motorized or manual window-raising mechanisms.\n- Remove all dirt, foreign matter, and loose glass from damaged areas, apply primer along windshield or window edges, and allow primer to dry.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q017ea5a279",
  "kind": "yes/no",
  "text": "Complaint narrative: FRONT LEFT BRAKE LINE RUPTURED, RESULTING IN LOSS OF BRAKE FLUID, DEPRESSES BRAKE PEDAL GOES TO THE FLOORBOARD. NO STOPPING POWER. BACKING OUT OF DRIVEWAY ON THIS OCCASION. NO ACCIDENT. SAME LINE ON RIGHT FRONT RUPTURED LESS THAN A YEAR AGO, EXACT SAME RESULT. LUCKILY NO ACCIDENT BUT WAS AT A STOP LIGHT ON A MAJOR HIGHWAY WHEN PEDAL WHEN STRAIGHT TO FLOOR",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qa5ab7649cb",
  "kind": "yes/no",
  "text": "Complaint narrative: I KEEP HAVING A PROBLEM WITH THE STEERING COLUMN. I HAVE FIXED THIS SAME PROBLEM 3 DIFFERENT TIMES. THE LAST TIME I FIXED THE PART SEEMS TO HAVE CHANGED AND THE PART WAS HIGHER THE LAST TIME. THE PART CHANGED SUPPOSEDLY TO BE BETTER THAN THE PREVIOUS PART BUT IT SEEMS TO GO OUT EVERY YEAR.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q5e437ad6ce",
  "kind": "yes/no",
  "text": "Customer: Please list movies currently showing in San Diego California:\nAgent: The top movies in San Diego today are 'Bad Boys For Life', 'The Rise of Skywalker', '1917', and 'Jumanji, The Next Level' ...\nCustomer: What locations are showing '1917' in San Diego?\nAgent: The movie '1917' is playing at AMC Mission Valley, The Lot at Liberty Station, and UltraStar Cinemas Mission Valley.\nCustomer: Ok, what times does '1917' show at AMC Mission Valley?\nAgent: Standard showings of '1917' are playing at 7:30pm and 9:00pm.\nCustomer: Is '1917' playing on IMAX?\nAgent: 1917' is only playing on standard screens, there is no IMAX option available for this movie.\nCustomer: Ok, how much is the cost for two tickets to the 7:30pm showing of '1917' at AMC Mission Valley?\nAgent: Fandango lists adult tickets for the 7:30pm showing of '1917' at $17.00 each.\nCustomer: Ok, I would like to purchase two adult tickets to the 7:30pm showing of '1917' at AMC Mission Valley.\nAgent: Please confirm your selection of two tickets to the 7:30pm showing of '1917' at AMC Mission Valley 20 for January 20th, 2020. Your total will be $34.00. Say 'OK' to confirm.\nCustomer: Wait, I would like to change my selection... I would like to purchase two tickets to the 9:00pm showing of '1917' instead...\nAgent: No problem. Please confirm your selection of two tickets to the 9:00pm showing of '1917' at AMC Mission Valley 20 for for January 20th, 2020. Your total will be $34.00. Say 'OK' to confirm.\nCustomer: OK. Confirming selection.\nAgent: Please wait while your tickets are purchased...\nCustomer: OK. Thank you.\nAgent: You have purchased two tickets for '1917' at AMC Mission Valley for this evening, January 20th, 2020. Your total charge was $34.00. Your confirmation number is 125673.\nCustomer: Ok. Where will I pick up the tickets?\nAgent: Your tickets will be sent to your email inbox. The email on file for your account is ltestone@gmail.com. Is this correct?\nCustomer: Yes, that is correct.\nAgent: Please check your inbox for your tickets.\nCustomer: Thank you. That's all!\nAgent: Thank you for using virtual movie assistant. Enjoy your show.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q5826edba7e",
  "kind": "yes/no",
  "text": "Recently , about one-third of Americas huge corn crop has been diverted from food and feed into an ultra-costly auto fuel that gives consumers poorer mileage even as it drives up their food costs . The corn ethanol diversion creates an artificial scarcity of farmland, as it attracts more land into corn instead of wheat or other cropsand the price effects are felt globally. In 2008, the ethanol mandate drove food prices up by more than 50 percent worldwide, and triggered food riots in Mexico and several other countries.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q8f4a5ff107",
  "kind": "yes/no",
  "text": "Table caption: Amino acids as butyl esters and their molecular ions. Additional amino acids can be detected and quantified with the matching stable-isotopic labeled standards.\n| Target amino acid | [M+H] + /[M+H] + Internal standard as butylesters |\n| Alanine | 146/150 |\n| Arginine | 231/236 |\n| Aspartic Acid | 246/249 |\n| Citrulline | 232/234 |\n| Glutamic acid | 260/263 |\n| Glycine | 132/134 |\n| Leucine/Isoleucine | 188/191 |\n| Methionine | 206/209 |\n| Ornithine | 189/191 |\n| Phenylalanine | 222/228 |\n| Tyrosine | 238/244 |\n| Valine | 174/182 |\n\nStatement: Leucine/Isoleucine has146/150 as values.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q0849ffce43",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2012 DODGE CHARGER. WHILE DRIVING APPROXIMATELY 60 MPH, THE VEHICLE STARTED TO DECELERATE. THE CONTACT COASTED TO THE SIDE OF THE ROAD. THE VEHICLE WAS TOWED TO THE CONTACT'S RESIDENCE. WHILE THE VEHICLE WAS PARKED, THE ENGINE CAUGHT FIRE. THE VEHICLE WAS TOWED TO THE DEALER WHERE IT WAS DIAGNOSED THAT A FAULTY THERMOSTAT MELTED ONTO THE ENGINE AND BURNED. THE ENGINE NEEDED TO BE REPLACED. THE VEHICLE WAS NOT REPAIRED. THE MANUFACTURER WAS MADE AWARE OF THE FAILURE. THE FAILURE MILEAGE WAS APPROXIMATELY 60,000. THE VIN WAS NOT AVAILABLE.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qc60439f757",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Raj Ghatak\n- Ghatak has worked extensively on stage, and in many original ground-breaking productions.\n\nSummary sentence:\nRaj Ghatak is an actor.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qdeca936fc5",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThis study confirms that serum and saliva IgG antibodies to SARS-CoV-2 are maintained in the majority of COVID-19 patients for at least 3 months PSO. IgG responses in saliva may serve as a surrogate measure of systemic immunity to SARS-CoV-2 based on their correlation with serum IgG responses.\n\nClaim: And a study of Covid-19 patients found that antibody levels in saliva and blood were closely matched.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q67d3e51836",
  "kind": "yes/no",
  "text": "Table caption: Daily (1-day), 3-days, and 5 days average Lot Turnover (LT) for portfolio with two different lot sizes.\n| Estim- | 1-day LT | 1-day LT | 3-days LT | 3-days LT | 5-days LT | 5-days LT |\n| ator | 100 | 500 | 100 | 500 | 100 | 500 |\n| MLE | 128.34 | 18.64 | 152.39 | 21.46 | 143.13 | 20.21 |\n| MCD | 133.94 | 14.23 | 128.85 | 13.59 | 146.38 | 13.96 |\n| S | 121.52 | 16.85 | 124.43 | 15.14 | 126.09 | 15.61 |\n| MM | 129.27 | 21.33 | 135.00 | 17.71 | 128.05 | 19.62 |\n| OGK | 134.24 | 19.12 | 140.74 | 20.55 | 145.14 | 21.66 |\n\nStatement: S Estim will have same value Lot turnover for all the days.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe8b7e8b81d",
  "kind": "yes/no",
  "text": "Customer: I think I'd like to see a movie tonight.\nAgent: Sounds like a plan. Which movie do you want to see?\nCustomer: I think I'll take my daughter to see Sonic the Hedgehog tonight.\nAgent: So, just two tickets?\nCustomer: Yes, just two standard tickets.\nAgent: Which theater were you thinking of seeing it at?\nCustomer: What are the times for Philadelphia Mills AMC?\nAgent: There's a 5:15 PM and a 7:15 PM showing.\nCustomer: That's not much of an option. What about Woodhaven AMC?\nAgent: The showtimes for this evening are 4:45 PM, 6:30 PM, 7:00 PM, 7:30 PM, 9:15 PM, 9:45 PM and 10:15 PM.\nCustomer: 6:30 PM is fine.\nAgent: Okay, so two tickets tonight at Woodhaven AMC for Sonic the Hedgehog at 6:30 PM?\nCustomer: Actually, now that I think about it, 6:30 PM might not work.\nAgent: Would you like the showtimes for a different theater?\nCustomer: No, Woodhaven AMC is fine. I think I'll make it for 7:30 PM instead.\nAgent: So, 7:30 PM instead of 6:30 PM?\nCustomer: Yes.\nAgent: I'll book two tickets tonight for Sonic the Hedgehog at Woodhaven AMC for 7:30 PM?\nCustomer: That's correct.\nAgent: You'r tickets are booked and the confirmation has been emailed to you.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q35768548c9",
  "kind": "yes/no",
  "text": "Karsk\nKarsk (also called Kask) is a Scandinavian cocktail containing coffee together with moonshine or vodka, and sometimes a spoon of sugar (enthusiasts often consider moonshine exclusively to be appropriate as an added component, as it has no inherent taste like other alcoholic beverages). Broader, it can also be found in other parts of Scandinavia.\n\nBLT cocktail\nA BLT cocktail is a cocktail made out of the contents of a BLT sandwich, (bacon, lettuce and tomato), blended together with vodka. Variants on the drink include utilizing bacon vodka instead of traditional vodka, substituting liquor for lettuce, incorporating bacon salt, or including cucumber flavored vodka.",
  "question": "Are Karsk and BLT cocktail both drinks that contain moonshine?",
  "definitions": "- yes: Read together, the paragraphs show the answer is yes: what the question asks holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right).\n- no: The paragraphs do not bear out a yes: at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer."
 },
 {
  "qid": "q34e23a757a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- The album debuted at No. 2 on the country albums charts, Its fourth and fifth singles \"Real Good Man\" and \"Watch the Wind Blow By\" both climbed to number one on the U.S. \"Billboard\" Hot Country Songs chart.\n- \"Shotgun Rider\" became the album's third single and a number 1 Country Airplay hit by the end of 2014.\n\nSummary sentence:\nIn total, McGraw's albums have produced 65 singles, 25 of which have reached number one on the Hot Country Songs or Country Airplay charts.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qc515ec7012",
  "kind": "yes/no",
  "text": "Statement 1: Plato is a man, and all philosophers are men, therefore Plato is a philosopher\nStatement 2: Plato is a philosopher, and all philosophers are men, therefore Plato is a man.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q8ab87c095e",
  "kind": "yes/no",
  "text": "Environment Magazine: \"Back When it Snowed': \"Losing Winter: As Climate Change Takes Hold, Our Coldest Season is the first Casualty'",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 }
]
