# T37b blind solver T37b-blind_read-fe18de44-001 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_qc3/s13/answers/T37b-blind_read-fe18de44-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q159ece4779",
  "kind": "yes/no",
  "text": "If you play the 🎸 get in my pants immediately",
  "question": "Is it right to say that this post is not hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "q8bf9179328",
  "kind": "yes/no",
  "text": "Table caption: Mass distribution of available bone tissue samples expressed as total weight (wt) in grams. The percentages of dark and light coloured samples, as well as the rest are shown and expressed as wt%.\n| Level | Hearth | Sample label | Total weight (g) | Dark colour (wt%) | Light colour (wt%) | Rest (<2mm) (wt%) |\n| L4 | a | (5–8)3 | 2.12 | 100 | 0 | 0 |\n| L4 | A | 01 | 34.24 | 56.3 | 23.6 | 20.2 |\n| L4 | B | 04 | 47.05 | 62.3 | 28.5 | 9.1 |\n| L4 | D | 02 | 75.94 | 77.1 | 13.0 | 9.8 |\n| L4 | E | 03 | 5.51 | 59.6 | 0 | 40.4 |\n| L5 | K2 | H301 | 48.71 | 72.2 | 6.2 | 21.6 |\n| L5 | J1 | J301 | 4.08 | 64.3 | 35.7 | 0 |\n| L7 | a | (1–2)1 | 0 | 0 | 0 | 0 |\n| L7 | Y | 01 | 2.26 | 100 | 0 | 0 |\n| L7 | W1 | 02 | 14.01 | 77.4 | 10.4 | 12.2 |\n| L7 | W2b | 2–03 | 3.67 | 63.0 | 37.0 | 0 |\n| L8 | A | 0 | 2.40 | 0 | 100 | 0 |\n| L11 | I | (1–2)1 | 99.57 | 73.05 | 17.1 | 9.9 |\n| L11 | I | (1–2)5 | 120.63 | 69.0 | 20.9 | 10.1 |\n| L11 | L | (5–8)6 | 83.37 | 69.3 | 18.6 | 12.1 |\n| L14 | T | 01 | 67.56 | 74.9 | 17.0 | 8.0 |\n| L14 | V | 03 | 74.78 | 60.5 | 23.1 | 16.4 |\n| L14 | Ω | 01 | 75.24 | 75.5 | 7.9 | 16.6 |\n\nStatement: L11 of sample label (1Ai2)5 has highest total weight of 120.63.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qff5c6e2707",
  "kind": "yes/no",
  "text": "Occupation: Postal Service Clerks\nDuties:\n- Weigh letters and parcels, compute mailing costs based on type, weight, and destination, and affix correct postage.\n- Check mail to ensure correct postage and that packages and letters are in proper condition for mailing.\n- Transport mail from one work station to another.",
  "question": "Does the job of the occupation named above include the listed duties?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qb72d5a821a",
  "kind": "yes/no",
  "text": "Customer: I would like to reserve tickets for a movie.\nAgent: What movie would you like to see?\nCustomer: Well, we are debating a few choices and I wanted to see the showtimes.\nAgent: Ok. What's the first movie you want to see?\nCustomer: Little Women\nAgent: For tonight?\nCustomer: Yes.\nAgent: I see a 6:30 and an 8 pm showing of that at AMC Champaign.\nCustomer: Hm. What are the showtimes for 1917?\nAgent: 1917 is showing at 9 pm and 10:30 pm.\nCustomer: Well, 1917 is probably to late for us. I was hoping for something around 7\nAgent: So, Little Women?\nCustomer: Yes I think so.\nAgent: How many tickets?\nCustomer: Hold on a moment, I need to text my friends.\nAgent: Of course.\nCustomer: It seems that 2 of my friends are not able to attend this evening.\nAgent: Oh, too bad! How many tickets should I purchase, then?\nCustomer: I think that we are actually going to wait until another night, so don't buy anything yet.\nAgent: Ok.",
  "question": "By the conclusion of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q256f76d6e7",
  "kind": "yes/no",
  "text": "Table caption: Exploratory factor analysis for the measures of response inhibition ( N = 179).\n| Measure | Factor loading | Uniqueness |\n| Antisaccade ERR | 0.15 | 0.98 |\n| Stroop ERR | 0.28 | 0.92 |\n| Stroop RT | 0.57 | 0.68 |\n| No-go ERR | 0.36 | 0.87 |\n| SSRT | – | 0.99 |\n\nStatement: There are 5 different types of measures in the given table.",
  "question": "Does the table support the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qcf2d6e4b74",
  "kind": "yes/no",
  "text": "Complaint narrative: I PULLED INTO A PARKING SPOT, PUT THE CAR INTO PARK, AND THEN THE CAR LURCHED FORWARD AT AN EXTREMELY POWERFUL SPEED. THE CAR STRUCK A CYPRESS TREE CAUSING $7,500 DAMAGE ON MY CAR.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "q25893db6be",
  "kind": "yes/no",
  "text": "Instead, the onus should be on the developers to prove the positive. No wind farm developer has ever had to explain the benefits of wind. Evidence tells us that wind power performance shows not only no reduction in CO 2 and other harmful emissions, but the very reverse. But Alex Salmond is driving an aggressive green agenda like an express train across Scotland, bludgeoning anyone who gets in the way as being a Luddite and anti-green.",
  "question": "Does this passage advance the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q63a206be03",
  "kind": "yes/no",
  "text": "Customer: I'd like to go and see a movie tonight with my family.\nAgent: OK. Can you tell me the city and state where the theater is located?\nCustomer: We are in Santa Barbara, California.\nAgent: I see two theaters, AMC Mountain 16 and AMC Mercado 24. Are you interested in a particular movie?\nCustomer: Both of those theaters are really nice.\nAgent: OK. Is there a movie you have in mind?\nCustomer: I'm not sure what's out right now.\nAgent: Sure. Do you have a favorite genre?\nCustomer: What's a genre?\nAgent: Genre the movie category, like comedy, drama, action, etc.\nCustomer: Oh that's what that means. I like action movies a lot.\nAgent: Ok. Let’s see what action films are out.\nAgent: I found one action movie at AMC Mountain 16: No Time To Die.\nCustomer: What time is No Time To Die playing?\nAgent: One moment.\nCustomer: 9:10pm would be great.\nAgent: Got it. And how many tickets?\nCustomer: I need tickets for myself, my husband, and my son.\nAgent: All right. Let me confirm that you’d like three tickets for No Time To Die at AMC Mountain 16 tonight at 9:10pm. Is that all correct?\nCustomer: Yes, you got it.\nAgent: Is it OK to go ahead and purchase these tickets?\nCustomer: Absolutely!\nAgent: OK. Your tickets are purchased and details for how to proceed have been sent to your email address. Can I help with anything else?\nCustomer: Nope, that's all for now.\nAgent: OK. Enjoy your movie!",
  "question": "Has the customer actually bought movie tickets by the time this conversation finishes?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q7c605d126e",
  "kind": "yes/no",
  "text": "In essence, what we have here is a new satellite using new tools to take measurements. The data recovered is analyzed using guesses and inferences. Their analysis is presented with a margin of error as large as the amount of ice they say is melting from Antarctica. The loss is is less than 1% of the normal annual melt.",
  "question": "Is it accurate to say that this paragraph doesn't make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable.\n- no: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy."
 },
 {
  "qid": "qf1bc7f5a7c",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nWeather may marginally affect COVID-19 dynamics, but misconceptions about the way that climate and weather drive exposure and transmission have adversely shaped risk perceptions for both policymakers and citizens.\n\nClaim: Experts demonstrated that seasonal effects would completely prevent the virus from spreading.",
  "question": "Does the evidence contradict it?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q7f3418d35f",
  "kind": "yes/no",
  "text": "Customer: I will just take the first one on the list. Can you make a reservation for 5 at 16:00 this Tuesday?\nAssistant: Unfortunately Bedouin doesn't have anything available. Would you like me to keep going down the list?",
  "question": "Does the assistant's reply confirm, for the booking the customer asked for, that it was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q3cf462cfe2",
  "kind": "yes/no",
  "text": "Complaint narrative: THE JEEP WAS INVOLVED IN A WRECK - HIT A POWER POLE AT AROUND 50 MPH KNOCKED IT DOWN AND THE FLIPPED THE AIR BAGS NEVER DEPLOYED - THE POLICE OFFICER WHO WORKED THE WRECK SAID THE AIRBAGS SHOULD HAVE DEPLOYED AFTER THE TYPE OF HIT THE JEEP TOOK",
  "question": "Would it be correct to say that this vehicle safety complaint doesn't report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "q37370b8001",
  "kind": "yes/no",
  "text": "Statement 1: You are likely to find a muscle in a body..\nStatement 2: You are likely to find a plant in your body.",
  "question": "Is it right to say that, of these two statements, Statement 2 does not go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q39cba72104",
  "kind": "yes/no",
  "text": "Table caption: BET analysis for biochar samples.\n| Sample | BET surface area (m 2 /g) |\n| 300 °C char | 0.0218 |\n| 500 °C char | 0.0899 |\n| 700 °C char | 0.2720 |\n| 900 °C char | 0.2115 |\n\nStatement: BET surface area (m 2 /g) 0.2115 Sample is 900 C char.",
  "question": "Does the table provide support for the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q310abca8bc",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nObjective To investigate the efficacy and safety of recombinant human interferon alpha1b (rhIFN-α) nasal drops in healthy medical staff to prevent 2019 novel coronavirus disease (COVID-19). Conclusion In this investigator-initiated open-label study, we observed that rhIFN-α nasal drops can effectively prevent COVID-19 in treated medical personnel.\n\nClaim: In China, the early results of a study among medical workers were disappointing, concluding that interferon nasal drops “were ineffective at preventing Covid-19 in medical staff.”",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q56640a5e42",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2000 PONTIAC GRAND PRIX. AFTER PARKING THE VEHICLE, THE CONTACT NOTICED SMOKE COMING FROM THE FRONT OF THE VEHICLE. THE CONTACT OPENED THE HOOD AND THE ENGINE COMPARTMENT WAS ON FIRE. THE CONTACT WAS ABLE TO EXTINGUISH THE FIRE. THE VEHICLE WAS INCLUDED IN NHTSA CAMPAIGN NUMBER: 15V701000 (ENGINE AND ENGINE COOLING). THE VEHICLE WAS TAKEN TO AN INDEPENDENT MECHANIC TO BE INSPECTED. THE VEHICLE WAS NOT REPAIRED. THE MANUFACTURER WAS NOT NOTIFIED OF THE FAILURE. THE FAILURE MILEAGE WAS 132,403. VIN TOOL CONFIRMS PARTS NOT AVAILABLE.",
  "question": "Does this vehicle safety complaint say the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qc56a0dba92",
  "kind": "yes/no",
  "text": "Customer: Hey, isn't that world war 1 movie out now?\nAgent: Do you mean 1917?\nCustomer: Yes, that. Buy a ticket for that movie.\nAgent: Ok. When and where do you want to see it?\nCustomer: I want to go the theater downtown. let's say around 10-ish?\nAgent: Ok, let me check. There is showing of that movie downtown at 10.\nCustomer: Ok. When is it showing?\nAgent: Showtimes are 6, 9 and midnight for today.\nCustomer: Ok. Book me a ticket for the 6 pm showing.\nAgent: Ok. It appears the showing has been sold out.\nCustomer: Fine. Try the 9 pm showing then.\nAgent: 9 pm showing is also sold out.\nCustomer: Ok. Try midnight then.\nAgent: It appears the movie is very popular all tickets for tonight have been sold out.\nCustomer: How is that possible? try a different theater nearby.\nAgent: Downtown theater is the only one showing that particular movie.\nCustomer: Unbelievable.\nAgent: What would you like to do now?\nCustomer: Well, nevermind then. I guess I won't watch a movie tonight.\nAgent: Ok. Sorry about that.",
  "question": "By the end of this dialogue, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q38b8e0f595",
  "kind": "yes/no",
  "text": "Bob Saget\nRobert Lane \"Bob\" Saget (born May 17, 1956) is an American stand-up comedian, actor, and television host. His television roles include Danny Tanner on the ABC sitcom \"Full House\" (1987–95) and its Netflix sequel \"Fuller House\", and hosting \"America's Funniest Home Videos\" from 1989 to 1997. Saget is also known for his adult-oriented stand-up routine. He also provided the voice of the future Ted Mosby on the CBS sitcom \"How I Met Your Mother\" from 2005 to 2014.\n\nLyudmil Kirkov\nLyudmil Kirkov (Bulgarian: Людмил Кирков , 14 December 1933 – 12 December 1995) was a Bulgarian film director and actor.",
  "question": "Is it accurate to say that Lyudmil Kirkov and Bob Saget are not both film or TV stars?",
  "definitions": "- yes: The paragraphs do not bear out the positive statement (the question read without its 'not' or 'fail to'): at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer.\n- no: Read together, the paragraphs show that the positive statement (the question read without its 'not' or 'fail to') holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right)."
 },
 {
  "qid": "qf233dffc59",
  "kind": "yes/no",
  "text": "Assistant: Got it, I will put that down as well.\nCustomer: Thanks!\nAssistant: You are welcome! Sorry, the indoor is not available.",
  "question": "Using the assistant's final message, is \"indoor\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q999eba8ba9",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nAmong these, we identify 66 druggable human proteins or host factors targeted by 69 existing FDA-approved drugs, drugs in clinical trials and/or preclinical compounds, that we are currently evaluating for efficacy in live SARS-CoV-2 infection assays.\n\nClaim: A research team found that no drugs target the same proteins in our cells the novel coronavirus does.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q66d1aad504",
  "kind": "yes/no",
  "text": "Action: Sharing a room with someone who doesn't want to.",
  "question": "In most places, is this action against the law?",
  "definitions": "- yes: Doing the action is a crime or legal offence in most places (for example theft, assault, fraud, drunk driving, vandalism, hard-drug use), not merely rude or immoral.\n- no: The action is legal in most places, even if it is rude, unkind, dishonest or morally wrong (for example lying to a friend, cheating on a partner, breaking a promise)."
 },
 {
  "qid": "q8e035fae4f",
  "kind": "yes/no",
  "text": "Customer: I'd like to see a movie this weekend.\nAgent: What movie do you want to see?\nCustomer: Either Knives Out, JoJo Rabbit, or Little Women.\nAgent: Where do you want to see it?\nCustomer: I want to see it at the College 9 Theater.\nAgent: They are all playing at the College 9 Theater.\nCustomer: What times are they showing?\nAgent: Knives Out is at 7 pm, JoJo Rabbit is at 7:30 pm, and Little Women is at 8 pm.\nCustomer: Are they showing at those times on both Saturday and Sunday?\nAgent: Yes.\nCustomer: Are there tickets available for Knives Out at 7 pm on Saturday?\nAgent: No, that show is sold out.\nCustomer: Are there tickets available for Knives Out at 7 pm on Sunday?\nAgent: How many tickets?\nCustomer: 2 or 3 tickets.\nAgent: Yes, there are 2 or 3 tickets available for Knives Out at 7 pm Sunday.\nCustomer: Thank you.\nAgent: Should I purchase the tickets.\nCustomer: No, I will purchase the tickets when I know how many I need.\nAgent: Okay\nCustomer: Thank you for the information.\nAgent: You're welcome.",
  "question": "By the close of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q2ed0f63cbf",
  "kind": "yes/no",
  "text": "Customer: The type of food is not important, but I would like a nice place that has tables available on Saturday evening.\nAssistant: Sure, I would recommend the Midsummer House Resaurant which serves British food.  It is a nice, expensive place located in the Centre.",
  "question": "Going by the text, did the assistant's reply include at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qacd1430848",
  "kind": "yes/no",
  "text": "Statement 1: An infant needs sun, water and soil in order to flourish.\nStatement 2: A basil plant needs sun, water and soil in order to flourish.",
  "question": "Of the statements given: Statement 1, does it go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q78334554b5",
  "kind": "yes/no",
  "text": "Occupation: Nuclear Power Reactor Operators\nDuties:\n- Distribute or process gas for utility companies or industrial plants, using panel boards, control boards, and semi-automatic equipment.\n- Adjust temperature, pressure, vacuum, level, flow rate, or transfer of gas to maintain processes at required levels or to correct problems.\n- Operate construction equipment to install and maintain gas distribution systems.",
  "question": "Are the duties given in the list part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q5136f5b191",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Stewart served as the assistant to Sandy Alderson, the general manager of the Athletics, in 1996.\n- In 1997, he left that position to serve in a similar capacity under Kevin Towers of the San Diego Padres.\n- Stewart left San Diego after the season and interviewed for assistant GM positions with Oakland and the Florida Marlins.\n- His familiarity with the Blue Jays organization was the main reason he accepted the job there under Gord Ash.\n\nSummary sentence:\nGeneral managers he has worked under include Sandy Alderson, Kevin Towers, Gord Ash, and Dean Taylor.",
  "question": "Looking at the summary sentence, is every piece of information in it supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q38cf1b0535",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nReports from China and Italy suggest that risk factors for severe disease include older age and the presence of at least one of several underlying health conditions (3,4).\n\nClaim: COVID-19 severity equally impacts people of all ages with or without chronic diseases.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q867b2531cf",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nRates of ventilation in the HC, HC+AZ, and no HC groups were 13.3%, 6.9%, 14.1%, respectively. The risk of ventilation was similar in the HC group (adjusted hazard ratio, 1.43; 95% CI, 0.53 to 3.79; P=0.48) and in the HC+AZ group (adjusted hazard ratio, 0.43; 95% CI, 0.16 to 1.12; P=0.09), compared to the no HC group. CONCLUSIONS: In this study, we found no evidence that use of hydroxychloroquine, either with or without azithromycin, reduced the risk of mechanical ventilation in patients hospitalized with Covid-19.\n\nClaim: Hydroxychloroquine does not help patients avoid being placed on a ventilator.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q5e3ee79b12",
  "kind": "yes/no",
  "text": "Situation: I'm a stereotypical nerd with WEAK thighs\nAction being judged: Making assumptions about an entire group of people.",
  "question": "Is it correct that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q115aa24e7b",
  "kind": "yes/no",
  "text": "Assistant: Sure, let me check.\nCustomer: Thank you.\nAssistant: Sorry, there is no more olives available at that time.",
  "question": "Is there confirmation of \"olives\" for the customer's pizza order in the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q371ab8a8a0",
  "kind": "yes/no",
  "text": "Customer: I am also looking for a hotel in the same area with zero stars.\nAssistant: I'm sorry, there are no matches.",
  "question": "Did the assistant, in its reply, identify at least a single option that satisfies everything the customer requested?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qce1b29ed83",
  "kind": "yes/no",
  "text": "Whatever it does produce is constantly changing, moment-to-moment; no one can predict what it will produce at any future time. Winds performance history also shows that wind plants generally produce most at the times of least demandand least at the times of peak demand.",
  "question": "Is there an assertion in this paragraph of the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qc6222f3e2f",
  "kind": "yes/no",
  "text": "Customer: Any thriller/suspense movies playing currently?\nAgent: What movie theater do you want to check out?\nCustomer: Check out the AMC River East Theater.\nAgent: Ok, there's Knives Out, The Turning, and Underwater.\nCustomer: What's the runtime for Knives Out?\nAgent: Knives Out has a runtime of 2 hours, 10 minutes.\nCustomer: Does AMC River East 21 offer IMAX screenings?\nAgent: Yes, they do.\nCustomer: Ok, Get me three ticket for me and two of my friends for Knives Out.\nAgent: Ok, and what showtime do you want?\nCustomer: I want the 7:00 PM showtime.\nAgent: What screening type do you want?\nCustomer: Just standard.\nAgent: Ok, that's three tickets for the 7:30 PM standard screening for Knives Out at the AMC River East 21 theater?\nCustomer: Yes, that's right. Oh, by the way, does switching to IMAX screening cost extra\nAgent: Switching to IMAX will incur a 5% surcharge. Do you want to switch from standard screening to IMAX screening.\nCustomer: No, that's fine.\nAgent: Ok, so the total comes to $46.94\nCustomer: Charge my Visa card.\nAgent: Ok, order has been confirmed.\nCustomer: Where's my receipt?\nAgent: It will appear in you email inbox shortly. Anything else?\nCustomer: That's all.\nAgent: Goodbye.",
  "question": "Has the customer actually bought movie tickets by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q7753875dc3",
  "kind": "yes/no",
  "text": "Customer: I'm looking for an expensive polynesian place.\nAssistant: I'm sorry, there is nothing that I can find like that.  Do you have anything else I can look for?",
  "question": "Did the assistant find at least a single option in its reply that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qde83f6ac87",
  "kind": "yes/no",
  "text": "Statement 1: It was so hot that he sweated a ton\nStatement 2: It was hot and he sweated all over the body",
  "question": "Upon examining the statements shown: Statement 2, does it go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q2ebab3f68c",
  "kind": "yes/no",
  "text": "Statement 1: He communicated with his friends by newspapers\nStatement 2: He communicated with his friends by letter",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q603ac87234",
  "kind": "yes/no",
  "text": "That is what I mean by fighting on marshy ground, by fighting on the same ground as the Warmists. No wonder they stand their ground it is as if the Skeptics are fundamentally in agreement with them, only differing in scale.",
  "question": "Does this paragraph put forward the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q7bea315ede",
  "kind": "yes/no",
  "text": "Assistant: $105-120. It will vary depending on some unique factors like traffic delays, tolls, and more. Also trips to and from AUS airport are subject to a $2.00 surcharge.\nCustomer: I understand. That's fine.\nAssistant: I just booked it. They will show up in 15 minutes precisely to the designated ride pickup location at the airport.",
  "question": "Is \"15 minutes\" for the customer's ride booking confirmed in the final message from the assistant?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q326494e495",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nConclusions The population prevalence of SARS-CoV-2 antibodies in Santa Clara County implies that the infection is much more widespread than indicated by the number of confirmed cases.\n\nClaim: \"We found that there are many, many unidentified cases of people having Covid infection that were never identified with it with a virus test,\" said Dr. Jay Bhattacharya, a professor of medicine at Stanford University and one of the paper's authors.",
  "question": "As for the claim, does the evidence contradict it?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q2f885baeaf",
  "kind": "yes/no",
  "text": "Complaint narrative: TAKATA RECALL. THE CONTACT OWNS A 2010 BMW X3 SAV. THE CONTACT STATED THAT THE VEHICLE STALLED WITHOUT WARNING IN THE MIDDLE OF THREE LANES OF TRAFFIC. THE CONTACT EXITED THE VEHICLE WHILE THE PASSENGER REMAINED INSIDE. ANOTHER VEHICLE DRIVING AT A HIGH RATE OF SPEED CRASHED INTO THE REAR OF THE CONTACT'S VEHICLE, PUSHED THE VEHICLE TO THE LEFT, AND CAUSED IT TO CRASH INTO A CURB. THE AIR BAGS DID NOT DEPLOY. THE DRIVER WAS NOT INJURED. THE FRONT PASSENGER SUSTAINED MAJOR INJURIES TO THE BACK, SHOULDER, AND NECK. MEDICAL ATTENTION WAS REQUIRED. A POLICE REPORT WAS FILED. THE VEHICLE WAS TOWED TO A REPAIR SHOP AND THE BODY DAMAGE WAS REPAIRED. THE VEHICLE WAS TOWED TO THE DEALER WHERE THE VANOS HOUSING BOLTS WERE SUPPOSEDLY REPLACED. THE VIN WAS INCLUDED IN NHTSA CAMPAIGN NUMBER: 16V071000 (AIR BAGS). THE CONTACT RECEIVED NOTIFICATION OF A MANUFACTURER RECALL FOR NHTSA CAMPAIGN NUMBER: 14V176000 (ENGINE AND ENGINE COOLING). THE MANUFACTURER WAS NOTIFIED, BUT HAD NOT CALLED THE CONTACT BACK. THE FAILURE MILEAGE WAS NOT AVAILABLE. PARTS DISTRIBUTION DISCONNECT.",
  "question": "Does this safety complaint about a vehicle report that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qad4abf79d5",
  "kind": "yes/no",
  "text": "Statement 1: It rains occasionally which is good for the trees and grass.\nStatement 2: It rains occasionally which is horrible for the trees and grass.",
  "question": "Looking at the statements here: Statement 1, does it go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qcc363d6da1",
  "kind": "yes/no",
  "text": "Customer: Sounds good. Could you book me a reservation for 8, Friday, at 16:15?\nAssistant: I'm sorry, I'm unable to book you a table at 16:15. Would you like to try another time?",
  "question": "Is there confirmation in the assistant's reply that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q2c85eba5be",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS AND RELEVANCE: In this survey of heath care workers in hospitals equipped with fever clinics or wards for patients with COVID-19 in Wuhan and other regions in China, participants reported experiencing psychological burden, especially nurses, women, those in Wuhan, and frontline health care workers directly engaged in the diagnosis, treatment, and care for patients with COVID-19.\n\nClaim: Female front-line workers treating patients with COVID-19 experienced higher rates or more severe symptoms of depression, anxiety, insomnia and distress than health-care workers overall.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qa23be1fa37",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNED A 2000 HONDA CIVIC. WHILE DRIVING 40 MPH, THE DRIVER REAR ENDED THE PRECEDING VEHICLE. THE CONTACT WAS SEATED IN THE FRONT PASSENGER SEAT AND HER AIR BAG DID NOT DEPLOY IN A TIMELY MANNER. AS A RESULT, THE CONTACT'S HEAD STRUCK THE FRONT WINDSHIELD. WHEN IT DEPLOYED, THE PASSENGER AIR BAG CAUSED SKIN ABRASIONS ON THE LEFT FOREARM THAT REQUIRED MEDICAL ATTENTION. A POLICE REPORT WAS FILED. THE VEHICLE WAS DESTROYED AND TOWED. THE MANUFACTURER AND DEALER WERE NOT NOTIFIED. THE CAUSE OF THE FAILURE WAS UNKNOWN. THE FAILURE MILEAGE WAS 137,589.",
  "question": "Was the vehicle actually involved in a crash, according to this vehicle safety complaint?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q25dd8458b4",
  "kind": "yes/no",
  "text": "Complaint narrative: THIS BRAKE PROBLEMS HAS OCCURRED MANY TIMES. DURING APPLICATION OF THE BRAKES AT LOW SPEEDS ON ROUGH ROAD SURFACES THE CAR SUDDENLY LOSES BRAKING POWER FOR A BRIEF TIME THEN STARTS TO WORK AGAIN IF THE BRAKE PEDAL REMAINS DEPRESSED. THIS HAS ALMOST CAUSED ACCIDENTS A NUMBER OF TIMES AND IS QUITE FRIGHTENING. THE CAR WAS BROUGHT IN FOR THE RECALL AND SAFERCAR.GOV STATES THAT THERE ARE NO OPEN RECALLS. WHEN WE BRING THIS TO THE ATTENTION OF THE TOYOTA DEALER WE ARE TOLD THIS PROBLEM IS \"NORMAL\" AND THERE IS NOTHING MORE THEY CAN DO. (HOWEVER, I UNDERSTAND THAT THEY FIXED IT IN THE NEXT MODEL YEAR.) IN MY OPINION THIS IS AN UNSAFE CONDITION AND IT HAS BEEN COMPLAINED ABOUT ONLINE BY OTHER PRIUS OWNERS. I ASK THE NHTSA TO REQUIRE TOYOTA TO FIX THIS IN THE NAME OF SAFETY.",
  "question": "Does this vehicle safety complaint state that the vehicle actually began to burn?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qd404c65b09",
  "kind": "yes/no",
  "text": "Situation: I used to seriously dislike Spongebob.\nAction being judged: Expressing your opinion about a tv show.",
  "question": "Is it correct that the action being judged isn't wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q8d91ad581c",
  "kind": "yes/no",
  "text": "Statement 1: shops are closed every day\nStatement 2: shops are open every day",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q4b59f6b82a",
  "kind": "yes/no",
  "text": "Assistant: Okay I will call them now. Sorry for the inconvenience.\nCustomer: That's okay. Thanks.\nAssistant: So I placed your order for a large pizza with peperoni and bacon at Papa Johns in Sidney Oh.",
  "question": "Pursuant to the assistant's final message, is \"Papa Johns\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qace815a6b8",
  "kind": "yes/no",
  "text": "Occupation: News Analysts, Reporters, and Journalists\nDuties:\n- Confer with clients, editors, publishers, or producers to discuss changes or revisions to written material.\n- Write words to fit musical compositions, including lyrics for operas, musical plays, and choral works.\n- Write humorous material for publication, or for performances such as comedy routines, gags, and comedy shows.",
  "question": "Is it the case that the listed duties aren't part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "q99f1b5419e",
  "kind": "yes/no",
  "text": "Customer: I'm looking for someplace to go in the west.\nAssistant: Might I recommend the Whale of a Time entertainment venue?",
  "question": "Did the assistant, in its reply, identify at least a single option that satisfies everything the customer requested?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 }
]
