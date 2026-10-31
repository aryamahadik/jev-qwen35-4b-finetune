# T37b blind solver T37b-blind_read-31bcf7e7-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_qc6/s13/answers/T37b-blind_read-31bcf7e7-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qb5b8551865",
  "kind": "yes/no",
  "text": "Customer: I want to watch a movie\nAgent: in theater or at home?\nCustomer: in theater\nAgent: do you have a movie in mind?\nCustomer: there are a few\nAgent: such as\nCustomer: ip man, star war, bad boys and a few others\nAgent: do you have a favorite\nCustomer: I don't have a favorite but I do want to watch star war, as well as ipman but I heard ipman may not be playing everywhere\nAgent: the review for ipman 4 is quite good just like the other threes\nCustomer: I always like that series, star war is ok too as I want to see its ending\nAgent: have we decided on a movie yet\nCustomer: if there is a showtime for ipman at landmark 81, book it, otherwise star war\nAgent: there is no ipman playing there, only starwar\nCustomer: then get me two tickets for 3d at 9 pm on saturday in 3d\nAgent: having a date sir?\nCustomer: sort of\nAgent: so 2 tickets for star war at 9 pm this Saturday in 3d\nCustomer: yes, but wait till I double check the schedule with my date\nAgent: all righty\nCustomer: thank you",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q0a9ee702c8",
  "kind": "yes/no",
  "text": "Assistant: Looks like 8:30 PM works as well! Did you want me to book this?\nCustomer: Yes, please!\nAssistant: Okay! 8:30 PM is booked!",
  "question": "Going by the assistant's latest message, is \"8:30 PM\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb3093e576d",
  "kind": "yes/no",
  "text": "Assistant: What toppings would you like on it?\nCustomer: I'd like for it to be cheese, hawaiian, and bacon\nAssistant: Unfortunately, the store does not have hawaiian as a topping in stock at the moment",
  "question": "Is it correct that, according to the assistant's last message, \"hawaiian\" isn't confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order.\n- no: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction."
 },
 {
  "qid": "q4ec4172db8",
  "kind": "yes/no",
  "text": "Customer: I think I'd like to see a movie tonight.\nAgent: Sounds like a plan. Which movie do you want to see?\nCustomer: I think I'll take my daughter to see Sonic the Hedgehog tonight.\nAgent: So, just two tickets?\nCustomer: Yes, just two standard tickets.\nAgent: Which theater were you thinking of seeing it at?\nCustomer: What are the times for Philadelphia Mills AMC?\nAgent: There's a 5:15 PM and a 7:15 PM showing.\nCustomer: That's not much of an option. What about Woodhaven AMC?\nAgent: The showtimes for this evening are 4:45 PM, 6:30 PM, 7:00 PM, 7:30 PM, 9:15 PM, 9:45 PM and 10:15 PM.\nCustomer: 6:30 PM is fine.\nAgent: Okay, so two tickets tonight at Woodhaven AMC for Sonic the Hedgehog at 6:30 PM?\nCustomer: Actually, now that I think about it, 6:30 PM might not work.\nAgent: Would you like the showtimes for a different theater?\nCustomer: No, Woodhaven AMC is fine. I think I'll make it for 7:30 PM instead.\nAgent: So, 7:30 PM instead of 6:30 PM?\nCustomer: Yes.\nAgent: I'll book two tickets tonight for Sonic the Hedgehog at Woodhaven AMC for 7:30 PM?\nCustomer: That's correct.\nAgent: You'r tickets are booked and the confirmation has been emailed to you.",
  "question": "By the end of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q740e191dd1",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2012 DODGE CHARGER. WHILE DRIVING APPROXIMATELY 60 MPH, THE VEHICLE STARTED TO DECELERATE. THE CONTACT COASTED TO THE SIDE OF THE ROAD. THE VEHICLE WAS TOWED TO THE CONTACT'S RESIDENCE. WHILE THE VEHICLE WAS PARKED, THE ENGINE CAUGHT FIRE. THE VEHICLE WAS TOWED TO THE DEALER WHERE IT WAS DIAGNOSED THAT A FAULTY THERMOSTAT MELTED ONTO THE ENGINE AND BURNED. THE ENGINE NEEDED TO BE REPLACED. THE VEHICLE WAS NOT REPAIRED. THE MANUFACTURER WAS MADE AWARE OF THE FAILURE. THE FAILURE MILEAGE WAS APPROXIMATELY 60,000. THE VIN WAS NOT AVAILABLE.",
  "question": "Is it right to say that this vehicle safety complaint does not report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q336d782890",
  "kind": "yes/no",
  "text": "Recently , about one-third of Americas huge corn crop has been diverted from food and feed into an ultra-costly auto fuel that gives consumers poorer mileage even as it drives up their food costs . The corn ethanol diversion creates an artificial scarcity of farmland, as it attracts more land into corn instead of wheat or other cropsand the price effects are felt globally. In 2008, the ethanol mandate drove food prices up by more than 50 percent worldwide, and triggered food riots in Mexico and several other countries.",
  "question": "Does the paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q88e861467d",
  "kind": "yes/no",
  "text": "Statement 1: cows produce juice\nStatement 2: cows produce milk",
  "question": "Is it right to say that, of these two statements, Statement 1 doesn't go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q989172e170",
  "kind": "yes/no",
  "text": "Customer: Hi, I'm looking for movie tickets.\nAgent: Okay, for what date?\nCustomer: I don't really care about the date, but something within the week.\nAgent: Sure. And what movie?\nCustomer: Either Mulan or No Time to Die. I'm not picky.\nAgent: No Time to Die or Mulan, okay...what theatre location?\nCustomer: I live in Oregon, Stoneyford to be exact.\nAgent: Alright, there are two movie theatres there. Do you have a preference?\nCustomer: No.\nAgent: Okay, so there is Mountain AMC 16 or Holiday Cinemark 12. One moment please.\nCustomer: Alright, thanks.\nAgent: Hello, so unfortunately I can not secure any tickets at all because both movie theatres are closed.\nCustomer: They are closed? Until how long?\nAgent: There is no end date.\nCustomer: Are any other locations open?\nAgent: No. It seems that all movie theatres are closed until further notice.\nCustomer: Okay...are the movies available on demand or something?\nAgent: Let me check....no, unfortunately their release dates were pushed back.\nCustomer: So when are they being released? Am I just out of luck?\nAgent: Unfortunately, yes, it seems that way. There is no pending release date for either movie, but records indicate sometime in the fall.",
  "question": "By the end of this dialogue, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q208d9fde16",
  "kind": "yes/no",
  "text": "Table caption: Correlations between HMB and SJ profiles.\n| Date | Correlation Coefficient | P-Value |\n| July 9, 2018 | 0.93 | 0.0 |\n| July 16, 2018 | 0.83 | 0.0 |\n| July 18, 2018 | 0.88 | 0.0 |\n| July 20, 2018 | 0.84 | 0.0 |\n| July 24, 2018 | 0.91 | 0.0 |\n| July 31, 2018 | 0.72 | 0.0 |\n| August 2, 2018 | 0.92 | 0.0 |\n| August 3, 2018 | 0.87 | 0.0 |\n| August 6, 2018 | 0.68 | 0.0 |\n| August 10, 2018 | 0.85 | 0.0 |\n| August 17, 2018 | 0.92 | 0.0 |\n| All dates | 0.79 | 0.0 |\n\nStatement: There are eleven different Dates of Correlations between HMB and SJ profiles.",
  "question": "Is the statement substantiated by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q24cc72e647",
  "kind": "yes/no",
  "text": "Assistant: actually there is a problem\nCustomer: what kind of problem\nAssistant: there is no uber xl close by",
  "question": "Does the assistant's final message say \"uber xl\" is confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qcd00d5b900",
  "kind": "yes/no",
  "text": "Situation: Single Dad Never Pitches In at Neighborhood Potlucks\nAction being judged: Not contributing anything to a potluck you are going to.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q98c610e891",
  "kind": "yes/no",
  "text": "Customer: Hi, Can you help me find White Fang?\nAgent: Sure, do you mean the movie or book?\nCustomer: I mean what theater in Santa Rosa is it showing in now?\nAgent: There are 4, first is Rialto, is that what you'd like?\nCustomer: No, what about Airport Cinema?\nAgent: Sure, it is playing there, what time would you like a ticket for?\nCustomer: Is there something at 5:30 or so?\nAgent: There is a showing at 5:20, would you like tickets?\nCustomer: Sure, I think that will work.\nAgent: How many tickets would you like?\nCustomer: I need 2 please.\nAgent: Sure, 2 for White Fang 5:20, Santa Rosa Airport cinema, is that right?\nCustomer: No, I changed my mind, is there a 5:30 show at the Rialto?\nAgent: There is a 5:40 showing there, would you like to change to there?\nCustomer: Yes, make that change please.\nAgent: change is 2 for White Fang, at the Rialto, 5:40 pm., tonight, in Santa Rosa, regular type screening, is that right?\nCustomer: Yes that's good, thanks.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.\nCustomer: Great, I have them thanks.\nAgent: enjoy your show.",
  "question": "Has the customer, by the end of this conversation, actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q1a0fc2113a",
  "kind": "yes/no",
  "text": "Situation: My Mom &amp; Son broke in my place??\nAction being judged: People assuming they're allowed entry into the houses of people, even when they're family.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q1e99f61040",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2014 DODGE CHARGER. WHILE DRIVING AT APPROXIMATELY 60 MPH, THE BRAKE PEDAL WAS DEPRESSED AND THE VEHICLE SLOWED DOWN, WHICH CAUSED THE CONTACT TO LOSE CONTROL AND CRASH INTO A DITCH. A POLICE REPORT WAS FILED. THE CONTACT SUSTAINED INJURIES TO THE NECK, CHEST, AND HEAD. MEDICAL ATTENTION WAS REQUIRED. THE VEHICLE WAS NOT DIAGNOSED OR REPAIRED. THE MANUFACTURER WAS NOT MADE AWARE OF THE FAILURE. THE APPROXIMATE FAILURE MILEAGE WAS 28,000.",
  "question": "Does this vehicle safety complaint state that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q04866ef789",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nINTERPRETATION: During the first wave of the COVID-19 pandemic, fewer than 10% of the US adult population formed antibodies against SARS-CoV-2, and fewer than 10% of those with antibodies were diagnosed.\n\nClaim: In blood samples from the first wave of the COVID-19 pandemic in the US, the majority of samples contained antibodies to the virus.",
  "question": "Does that evidence support that claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q1a2d865529",
  "kind": "yes/no",
  "text": "Table caption: Summary of previously reported cases of COVID-19-associated pulmonary aspergillosis.\n| Study | Country | CAPA* | Aspergillus species | Aspergillus species in culture | Serum or BAL GM positive | BAL Aspergillus PCR positive | Initial Antifungal Therapy | In-hospital mortality |\n| Alanio, 2020 [ ] | France | 9/27 | A. fumigatus (7/9) | 7/9 | 3/9 | 4/9 | VOR (1/9) CAS (1/9) None (7/9) | 4/9 |\n| Koehler, 2020 [ ] | Germany | 5/19 | A. fumigatus (5/5) | 3/5 | 4/5 | 4/5 | VOR (2/5) ISA (1/5) CAS (2/5) | 3/5 |\n| Rutsaert, 2020 [ ] | The Netherlands | 7/34 | A. fumigatus (5/7) A. flavus (1/7) | 6/7 | 6/7 | NR | VOR (4/7) VOR/ISA (2/7) None (1/7) | 4/7 |\n| Nasir, 2020 [ ] | Pakistan | 5/23 | A. flavus (3/5) A. niger (1/5) A. fumigatus and A. flavus (1/5) | 5/5 | 0/5 | NR | VOR (3/5) AmB-d (2/5) | 3/5 |\n| van Arkel, 2020 [ ] | The Netherlands | 6/31 | A. fumigatus (6/6) | 5/6 | 3/6 | NR | VOR plus AND (5/6) L-AmB (1/6) | 4/6 |\n| Blaize, 2020 [ ] | France | 1/1 | A. fumigatus | 1/1 | 0/1 | 1/1 | None | 1/1 |\n| Lahmer, 2020 [ ] | Germany | 2/2 | A. fumigatus (2/2) | 2/2 | 2/2 | NR | L-AmB (2/2) | 2/2 |\n| Wang, 2020 [ ] | China | 8/104 | A. fumigatus | 8/8 | NR | NR | NR | NR |\n| Antinori, 2020 [ ] | Italy | 1/1 | A. fumigatus | 1/1 | 1/1 | 1/1 | L-AmB | 1/1 |\n| Ferreira, 2020 [ ] | France | 1/1 | A. fumigatus | 1/1 | 0/1 | 1/1 | None | 1/1 |\n| Meijer, 2020 [ ] | France | 1/1 | A. fumigatus | 1/1 | 1/1 | NR | VOR plus CAS | 1/1 |\n| Prattes, 2020 [ ] | Austria | 1/1 | A. fumigatus | 1/1 | 0/1 | NR | VOR | 1/1 |\n| Sharma, 2020 [ ] | Australia | 1/1 | A. fumigatus | 1/1 | NR | NR | VOR | 0/1 |\nTable notes: *number with CAPA/total number in the report AmB-d, amphotericin b deoxycholate; AND, anidulafungin; BAL, bronchoalveolar lavage; CAPA, COVID-19-associated pulmonary aspergillosis; CAS, caspofungin; GM, galactomannan; ISA, isavuconazole; L-AmB, liposomal amphotericin; NR, not reported; VOR, voriconazole\n\nStatement: van Arkel, 2020 study had reported France 5/23 for CAPA",
  "question": "Is it correct that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qf57ac28caf",
  "kind": "yes/no",
  "text": "Customer: I'm looking to go see a movie at the theaters in Davis, California.\nAgent: No problem. Do you have a movie in mind?\nCustomer: I was thinking going to see about No Time To Die.\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: There's no showings in Davis, California then?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: Ah, that's too bad. Do you know what action films are being shown in Davis, California right now?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Is this the original Mad Max film from the 70s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: I think I'll pass, I was looking forward to seeing No Time To Die at the Davis Theaters. Thank you anyways.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "Has the customer, by the end of this conversation, actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qc315ebf164",
  "kind": "yes/no",
  "text": "Customer: Actually I had Japanese in mind.\nAssistant: There are no Japanese restaurants in the cheap price range in the north part of town. Should I check another part of town?",
  "question": "Did the assistant come up with at least a single option in its reply that fits everything the customer wanted?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q21100a1d87",
  "kind": "yes/no",
  "text": "Situation: Glanced to my left and made eye contact with a lady\nAction being judged: Looking people in the eyes when you talk to them.",
  "question": "Is the action being judged wrong by common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q36a8bc6022",
  "kind": "yes/no",
  "text": "Customer: I want to buy movie tickets for tonight\nAgent: OK! What movie would you like to see?\nCustomer: Sonic\nAgent: OK! What theater do you prefer?\nCustomer: The Cinemark in West Valley\nAgent: Great. Would you prefer a Standard or XD screen?\nCustomer: XD\nAgent: OK. And what time would you like to see the show?\nCustomer: 7:00 PM\nAgent: There is a showing at 7pm. How many tickets will you need?\nCustomer: Two\nAgent: OK. Two tickets will be $30\nCustomer: Oh that's too high. Is a standard screen cheaper?\nAgent: Two tickets for a standard showing are $20.\nCustomer: What time is the standard screen?\nAgent: The standard showing is at 6:20pm\nCustomer: OK let's buy that one\nAgent: OK. Just to confirm we have two tickets for Sonic tonight at 6:20pm at the West Valley Cinemark. Your total is $20.\nCustomer: Yes\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "Is it true that, by the end of this conversation, the customer has not actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "qd6f9de7968",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2008 HYUNDAI VERACRUZ. WHILE DRIVING 5 MPH, THE ABS MODULE MALFUNCTIONED AND CAUSED THE VEHICLE TO CATCH FIRE. THE CONTACT NOTICED SMOKE UNDER THE HOOD OF THE VEHICLE AND FLAMES IGNITED FROM THE BATTERY. A POLICE REPORT WAS NOT FILED. THE FIRE WAS EXTINGUISHED BY ATTENDANTS FROM A NEARBY AUTO BODY SHOP. THERE WERE NO INJURIES. THE VEHICLE WAS NOT DESTROYED. THE DEALER AND MANUFACTURER WERE NOT NOTIFIED. THE FAILURE MILEAGE WAS APPROXIMATELY 144,000.",
  "question": "Does this complaint, which is about vehicle safety, report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q3849273431",
  "kind": "yes/no",
  "text": "Table caption: Amino acids as butyl esters and their molecular ions. Additional amino acids can be detected and quantified with the matching stable-isotopic labeled standards.\n| Target amino acid | [M+H] + /[M+H] + Internal standard as butylesters |\n| Alanine | 146/150 |\n| Arginine | 231/236 |\n| Aspartic Acid | 246/249 |\n| Citrulline | 232/234 |\n| Glutamic acid | 260/263 |\n| Glycine | 132/134 |\n| Leucine/Isoleucine | 188/191 |\n| Methionine | 206/209 |\n| Ornithine | 189/191 |\n| Phenylalanine | 222/228 |\n| Tyrosine | 238/244 |\n| Valine | 174/182 |\n\nStatement: Leucine/Isoleucine has146/150 as values.",
  "question": "Would it be correct to say that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q0e4995d308",
  "kind": "yes/no",
  "text": "Complaint narrative: 2018 DODGE CARAVAN. CONSUMER WRITES IN REGARDS TO DEFECTIVE PASSENGER SEAT WHICH RESULTED IN INJURY TO PASSENGER. *LD THE CONSUMER STATED THE WHILE ATTEMPTING TO ADJUST THE SEAT TO AN UPRIGHT POSITION IT SLAMMED FORWARD AGAINST THE BACK OF THE HEAD. THIS CAUSED AND INJURY TO THE HEAD AND JAW. THE CONSUMER DID NOT SEEK MEDICAL ATTENTION. *JS *TT *BF",
  "question": "Looking at this vehicle safety complaint, does it report that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q5b15c24bce",
  "kind": "yes/no",
  "text": "Complaint narrative: I PURCHASED A PRE-OWNED 2010 BMW 750LI BACK IN NOVEMBER 2012. AS SOON AS I DROVE IT OFF THE BEVERLY HILLS BMW LOT, I GOT A CHECK ENGINE LIGHT GO OFF. BEVERLY HILLS WROTE IT OFF AS IT WAS THE GAS SENSOR BEING SENSITIVE. FOUND OUT LATER IT WAS THE FUEL INJECTORS THAT WENT BAD ON A CAR WITH 23,000 MILES ON. FAST FORWARD 2 YEARS LATER AND 30,000 MILES, WITH MULTIPLE STOPS AT STERLING BMW AND MY COMPLAINTS OF HAVING TO PUT QUART OF OIL INTO THE ENGINE EVERY 2000 MILES. FOR 2 YEARS, STERLING ADVISED ME IT WAS NORMAL FOR THIS TYPE OF ENGINE TO CONSUME THAT MUCH OIL AND FOR ALL THE OTHER ENGINE PROBLEMS. I HAVE BROUGHT THE CAR IN FOR OVER 6 TIMES (EVER OTHER MONTH ALMOST) TO THE DEALER TO FIX NUMEROUS PROBLEMS WITH THE ENGINE (NOT NORMAL WEAR AND TEAR). THEN COMES THE \"RECALL\" BMW CALLS THE \"COMFORT CARE PACKAGE\" AND WAS PROMISED IT WOULD RESOLVE THE OIL CONSUMPTION WITH BETTER PERFORMANCE IN JANUARY 2015. AFTER THE RECALL, MY ENGINE REQUIRED OIL EVERY 500 MILES AND WHEN I BROUGHT IT BACK TO BMW IN APRIL 2015, THEY ADVISED ME IT WAS A HOSE LEAK AND OIL WAS DRIPPING DOWN TO EXHAUST CAUSING EXCESS SMOKE FROM THE EXHAUST. NOW BMW OF NORTHERN AMERICA TELLS ME THEY DON'T COVER THE REPAIR BECAUSE IT WAS OUR OF WARRANTY DESPITE MY COMPLAINTS (WHICH HAVE BEEN DOCUMENTED BY STERLING FOR 2 YEARS). THE COMFORT CARE PACKAGE MADE MY OIL LEAK WORST AND INTO THE EXHAUST AND BMW REFUSES TO REPAIR THE PROBLEM OR EVEN REMOVE THEIR COMFORT CARE PACKAGE. IT'S BEEN MORE THEN 2 YEARS SINCE I AND MY 2 YEAR OLD DAUGHTER HAVE BEEN BREATHING IN THIS EXCESS SMOKE FROM MY EXHAUST WHICH BMW REFUSES TO REPAIR. THIS ENGINE IS A COMPLETE LEMON.",
  "question": "Does this vehicle safety complaint say the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q7fe43f60d1",
  "kind": "yes/no",
  "text": "Customer: I need a restaurant that serves catalan food and it should be in the west.\nAssistant: Unfortunately, I'm not finding any Catalan restaurants in the west. Would you like me to look in other areas?",
  "question": "Did the assistant, in its reply, identify at least a single option that satisfies everything the customer requested?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qb78adc2305",
  "kind": "yes/no",
  "text": "Customer: I am looking for a restaurant that is in the cheap price range and in the east part of town.\nAssistant: The Missing Sock serves cheap food in the east part of town.",
  "question": "Did the assistant find at least a single option in its reply that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q121d899b72",
  "kind": "yes/no",
  "text": "Customer: Hi! How are you?\nAgent: I am good. What can I help you with?\nCustomer: I am looking to purchase tickets to get see a movie.\nAgent: I understand. Are there any particular movies that you want to see?\nCustomer: None in particular. I just want to see what my options are.\nAgent: Okay. What is your location?\nCustomer: I am on assignment in a Seven Trees, Nebraska.\nAgent: Okay, I have Holiday Cinemark 12 which is 30 miles away from you in the town of Butte Crest.\nCustomer: 30 miles? Is there anything closer than that?\nAgent: Mountain AMC 16 which is 22 miles away in the town of North Fork is the only theater that is closer.\nCustomer: So the closest theater is 22 miles away from me?\nAgent: Yes, that is correct.\nCustomer: That is too far. I am not going to drive that distance to see a movie.\nAgent: There is nothing closer to Seven Trees, Nebraska at this moment. I apologize.\nCustomer: Okay, I am not going to go to the movies then. Thank you anyways.\nAgent: You are welcome.",
  "question": "Has the customer actually bought movie tickets by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q14d0a48f89",
  "kind": "yes/no",
  "text": "Table caption: The categories and their conditions.\n| Category | More likely to be salient | Less likely to be salient |\n| Loudness | Word intensity of 80 dB | Word intensity of 60 dB |\n| Acoustic Prominence | /t/pronounced as [p] | /t/pronounced as [t] |\n| Grammatical Gender | Violation of grammatical gender | Correct grammatical gender |\n| Frequency | High frequency word | Low frequency word |\n| Conscious Sound Change | /r/pronounced as [ɹ] | /r/pronounced as [r] |\n| Subconscious Sound Change | /v/pronounced as [v] (=voiced) | /v/pronounced as [f] (=voiceless) |\n\nStatement: More likely to be salient for Grammatical Gender is/r/pronounced as [] .",
  "question": "Does the table provide support for the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qaa4444df9b",
  "kind": "yes/no",
  "text": "Table caption: Daily (1-day), 3-days, and 5 days average Lot Turnover (LT) for portfolio with two different lot sizes.\n| Estim- | 1-day LT | 1-day LT | 3-days LT | 3-days LT | 5-days LT | 5-days LT |\n| ator | 100 | 500 | 100 | 500 | 100 | 500 |\n| MLE | 128.34 | 18.64 | 152.39 | 21.46 | 143.13 | 20.21 |\n| MCD | 133.94 | 14.23 | 128.85 | 13.59 | 146.38 | 13.96 |\n| S | 121.52 | 16.85 | 124.43 | 15.14 | 126.09 | 15.61 |\n| MM | 129.27 | 21.33 | 135.00 | 17.71 | 128.05 | 19.62 |\n| OGK | 134.24 | 19.12 | 140.74 | 20.55 | 145.14 | 21.66 |\n\nStatement: S Estim will have same value Lot turnover for all the days.",
  "question": "Is it correct that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qd3e2bf177e",
  "kind": "yes/no",
  "text": "Table caption: 3-D printing settings tested on the Cerberus.\n| Basic Printer Settings | Basic Printer Settings |  |  |  |\n| Material | Nozzle Temperature [ o C] | Bed Temperature [ o C] | Layer Height [mm] | Part Cooling Fan |\n| PEKK | 390 | 180 | 0.3 | OFF |\n| PEI/ULTEM | 380 | 170 | 0.3 | OFF |\n| Polycarbonate | 280 | 130 | 0.3 | ON or OFF |\n\nStatement: Nozzle Temperature will High for PEKK Material.",
  "question": "Is there support for the statement in the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q259b459c61",
  "kind": "yes/no",
  "text": "Occupation: Appraisers and Assessors of Real Estate\nDuties:\n- Inspect properties, considering factors such as market value, location, and building or replacement costs to determine appraisal value.\n- Photograph interiors and exteriors of properties to assist in estimating property value, substantiate findings, and complete appraisal reports.\n- Compute final estimation of property values, taking into account such factors as depreciation, replacement costs, value comparisons of similar properties, and income potential.",
  "question": "Is the inclusion of the listed duties in the job of the occupation named above true?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q94debec818",
  "kind": "yes/no",
  "text": "Situation: I regularly give people misinforamtion to teach them to listen clearly\nAction being judged: Giving people misinformation just because they aren't listening.",
  "question": "Is it the case that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qc96f0f9f32",
  "kind": "yes/no",
  "text": "Statement 1: Sunglasses are worn on the eyeballs.\nStatement 2: Contact lenses are worn on the eyeballs.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qc4ed533153",
  "kind": "yes/no",
  "text": "Assistant: OK, how about tomorrow at 8am?\nCustomer: Yes, perfect!\nAssistant: Ok you are all set for tomorrow at 8am to get your tire checked out",
  "question": "Would it be correct to say that, according to the assistant's last message, \"tomorrow\" is not confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order.\n- no: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction."
 },
 {
  "qid": "qa4710ebf3b",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThese studies confirm that cats are susceptible to productive SARS-CoV-2 infection, but are unlikely to develop clinical disease.\n\nClaim: Cats can be infected by the novel coronavirus but are unlikely to get sick.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q1ad2852870",
  "kind": "yes/no",
  "text": "Table caption: Distance statistics to investigate the changes in the spatial distribution among ancient buildings, modern buildings and their spatial clustering centers (unit: meter).\n| Index | Ancient building | Modern building |\n| AVERAGE | 106.996 | 190.761 |\n| STDEV.S | 72.664 | 112.324 |\n| MIN | 5.930 | 7.634 |\n| MAX | 308.987 | 505.028 |\n| MEDIAN | 80.988 | 158.405 |\n\nStatement: Ancient building Average meter is 106.996.",
  "question": "Based on the table, is the statement supported?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q58b23f33c7",
  "kind": "yes/no",
  "text": "Statement 1: She put a cotton pie in the oven to bake.\nStatement 2: She put an apple pie in the over to bake.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q713364f7d0",
  "kind": "yes/no",
  "text": "Statement 1: They have to say farewell to each other because they are leaving\nStatement 2: They have to say hello to each other because they are leaving",
  "question": "Is it the case that, of these two statements, Statement 2 doesn't go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q37e34df1b3",
  "kind": "yes/no",
  "text": "Table caption: Current status of the line positions of the ν 4 band and the ν 3 +ν 4 -ν 3 hot band of CH 3 I in the C-H stretch region.\n| Technique |  |  | ν 4 | ν 4 | ν 3 +ν 4 -ν 3 | ν 3 +ν 4 -ν 3 |\n|  | Point spacing | Ref. | Assignments | Std. dev./cm -1 | Assignments | Std. dev./cm -1 |\n| FT-IR | 150 MHz | [19] | 500 | 0.005 | – | – |\n| FT-IR | 162 MHz | [20] | 1850 | 0.00083 | 380 | 0.0013 |\n| Comb-FTS | 11 MHz | This work | 2603 | 0.00034 | 831 | 0.00084 |\n\nStatement: The highest Assignments is 2603.",
  "question": "Does the table back up the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd673a30762",
  "kind": "yes/no",
  "text": "Statement 1: A spider spun a web.\nStatement 2: A horse spun a web",
  "question": "Is it true that, of these two statements, Statement 1 doesn't go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "qa2e4fa8360",
  "kind": "yes/no",
  "text": "Occupation: Medical Dosimetrists\nDuties:\n- Develop radiation treatment plans in consultation with members of the radiation oncology team.\n- Calculate the delivery of radiation treatment, such as the amount or extent of radiation per session, based on the prescribed course of radiation therapy.\n- Calculate, or verify calculations of, prescribed radiation doses.",
  "question": "Based on the text, are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q7ab993062e",
  "kind": "yes/no",
  "text": "Assistant: The Cedars offers several hot meals from the grill.\nCustomer: Great, get the tickets at The Cedars.\nAssistant: I've booked you for 2 tickets to The Upside at The Cedars for 6pm",
  "question": "Has \"The Upside\" been confirmed for the customer's movie ticket order in the assistant's latest message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7e97466c37",
  "kind": "yes/no",
  "text": "Complaint narrative: IF TRUCK IS NOT DRIVEN IN A FEW WEEKS THE GAS FEED STICKS IN REVERSE, I HAVE NOT HAD IT STICK IN FORWARD. ONLY IN REVERSE, MY WIFE HAD A ACCIDENT WITH THIS TRUCK. I'VE HAD IT STICK ON ME BUT I'M LOOKING FOR IT. FORD AND THE INSURANCE COMPANIES SAY THAT THERE IS NOTHING WRONG. IT HAS OCCURRED SEVERAL TIMES WITH ME AND I DON'T LET MY WIFE DRIVE THE TRUCK.",
  "question": "According to this vehicle safety complaint, was the vehicle actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q4d37653e91",
  "kind": "yes/no",
  "text": "Drank too many 🍹 when I was in Thailand. Fucked me right up",
  "question": "Is it right to say that this post isn't hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "qdbeee90a23",
  "kind": "yes/no",
  "text": "Customer: Hi there. I'd like to buy movie tickets for showings in Davis, CA.\nAgent: No problem. Do you have a movie in mind?\nCustomer: I am considering the movie \"No Time To Die\"\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: Are there no showings in any theaters in Davis, CA?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: Oh that's unfortunate. Are there any action movies playing in Davis?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Okay is that the original movie from the 70s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: You know that's okay. I will wait until the film I wish to see becomes available in Davis.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By the close of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qcf8dcdf392",
  "kind": "yes/no",
  "text": "Customer: Could you try an hour earlier, then?\nAssistant: Certainly. You now have a table for your party of 8 at the Curry Garden, at 16:45. Your reference number is V24OGNJB.",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "q51a8f79cca",
  "kind": "yes/no",
  "text": "When the Board voted in December to amend teaching standards to allow students to consider both sides in the climate debate, global warming pressure groups were apoplectic.",
  "question": "Is there confirmation that this paragraph makes the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q1d69f48a5b",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThis study confirms that serum and saliva IgG antibodies to SARS-CoV-2 are maintained in the majority of COVID-19 patients for at least 3 months PSO. IgG responses in saliva may serve as a surrogate measure of systemic immunity to SARS-CoV-2 based on their correlation with serum IgG responses.\n\nClaim: And a study of Covid-19 patients found that antibody levels in saliva and blood were closely matched.",
  "question": "Based on the text, does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qdaa69b2858",
  "kind": "yes/no",
  "text": "Customer: Hey, how are you?\nAgent: Well, how can I help you?\nCustomer: I would like to see a movie tonight i think\nAgent: sure, is anyone going with you?\nCustomer: just my girlfriend and brother\nAgent: great, what would you like to see?\nCustomer: the Boy 2, or Bad boys would be good\nAgent: Okay, is there any particular theater you would like to go to?\nCustomer: I like Regal or AMC\nAgent: Okay, is there a specific time you would like to go?\nCustomer: I think anywhere from 7-8 would be good\nAgent: okay, one second let me check\nCustomer: sure thing, take your time\nAgent: okay, I am checking for the boy 2 and see no results\nCustomer: shucks, can you check for bad boys then?\nAgent: sure thing, let me see\nCustomer: okay, hopefully they have something....\nAgent: okay, bad news, there is nothing for that either\nCustomer: okay, I guess it is not in the cards for tonight, thank you anyways\nAgent: not a problem, any time!",
  "question": "Have movie tickets actually been bought by the customer by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q05a8c5677e",
  "kind": "yes/no",
  "text": "Table caption: Peptides from L. fermentum HFD1 with predicted antimicrobial activity\n| № | The protein ID | Peptide sequence | ADAM | CAMPR3 | CAMPR3 | CAMPR3 | AMPA |  | Length in peptidome |\n| № | The protein ID | Peptide sequence | ADAM | SVM | Random Forest | DAC | AMPA | Length | Length in peptidome |\n| 1 | QIX58482.1 | MGLIWSLIVGAIIGAIAGAITNRGAAMGWIANIVAGLIGAWIGQGLLGTWGPSLAGMALIPSIIGAIILVLIVSLVVGRTGKK | 1.52 | 1.0 | 0.566 | 0.527 | 0.24 | 84 | 14 |\n| 2 | QIX58771.1 | MLSLITNTVIILLIIGCAFWQLVKVFKRAKKGKCAACDYDCAVKQQVLKQEKHGAQ | 0.82 | 0.889 | 0.6715 | 0.81 | 0.2226 | 56 | N/A |\n| 3 | QIX58909.1 | MAVKIKTPAGMIDIANDVIATVVGGAATDNYGVVGMASRNPLKDGVNQILGRDSFHQGVVIRQQDNGIAVDVYIIVGYGTKISAVSKSVQEKVKYNLEAMLGVTANSVNIMVQGVRVLGD | 0.09 | 1.00 | 0.9855 | 1.0 | 0.248 | 120 | N/A |\n| 4 | QIX58994.1 | MNNQSNVTPQNGNLQYKFCQNCGAKIDVKAVVCPKCGVPVNGNNAESNSEDRNNGWWNLLGFFFPIVGWILWAVWHKEYPKRAHGICVWSWVSFGISFVIGFVNGFLSTL | 1.32 | 1.00 | 0.7745 | 1.0 | 0.237 | 110 | N/A |\n\nStatement: The protein ID QIX58482.1 has Peptide sequence of MNNQSNVTPQNGNLQYKFCQNCGAKIDVKAVVCPKCGVPVNGNNAESNSEDRNNGWWNLLGFFFPIVGWILWAVWHKEYPKRAHGICVWSWVSFGISFVIGFVNGFLSTL.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 }
]
