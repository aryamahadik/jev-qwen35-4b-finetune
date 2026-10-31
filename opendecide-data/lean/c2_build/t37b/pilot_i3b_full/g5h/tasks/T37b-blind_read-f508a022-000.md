# G5-H blind read T37b-blind_read-f508a022-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3b_full/g5h/answers/T37b-blind_read-f508a022-000.json

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
  "qid": "q346eb4df07",
  "kind": "yes/no",
  "text": "Assistant: No other movie tickets ordered.\nCustomer: Thank you\nAssistant: You're welcome. Tickets for Aquaman 7:00pm showing at Lowes Boston Common are ordered. Cost is $17.99. Receipt is texted to you.",
  "question": "Does the assistant's final message say \"Lowes Boston Common\" is confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qaf1c4b66d3",
  "kind": "yes/no",
  "text": "Customer: Can you help me with booking movie tickets?\nAgent: Yes.\nCustomer: I'm looking for a theater in the Austin area.\nAgent: There is a Alamo and a AMC.\nCustomer: I would like to go to the Alamo Drafthouse.\nAgent: What movie are you going to see?\nCustomer: Bad Boys for Life.\nAgent: How many tickets do you need?\nCustomer: One.\nAgent: Would you like standard, IMAX, or 3d?\nCustomer: 3d.\nAgent: There is a 3d showing at 4:00pm.\nCustomer: That is fine.\nAgent: Where would you like to sit?\nCustomer: The front.\nAgent: Okay. Let me confirm, one ticket for Bad Boys at 4:30?\nCustomer: That's right.\nAgent: Okay. You're confirmation number is 8137768.\nCustomer: Thank you.\nAgent: You are welcome.",
  "question": "Is it correct that, by the end of this conversation, the customer hasn't actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "q44a2ac4cea",
  "kind": "yes/no",
  "text": "Customer: Hello assistent\nAgent: Hello\nCustomer: I would like order some movie tickets\nAgent: Ok, what movie would you like to see?\nCustomer: I would like to see the movie, 1917\nAgent: Ok, what theater would you like?\nCustomer: Watertown\nAgent: Ok, and what showtime would you prefer\nCustomer: I would like to get 7:00 PM\nAgent: Alright let me take a look at availability\nCustomer: Perfect, thank you.\nAgent: Alright upon review it seems like the 7:00 PM show for the movie 1917 in Watertown is sold out and there are no tickets available.\nCustomer: Darn.\nAgent: Is there another movie you would have interest in?\nCustomer: Sure, could you tell me what else in playing in Watertown?\nAgent: Yes, the shows currently playing are: Little Women, 1917, Fast Cars, Cats, Bad Boys III, Weekend at Bernies, and Saving Private Ryan.\nCustomer: I would like tickets to Little Women please.\nAgent: Alright, what time?\nCustomer: I would like a 8 PM showing and I would need two tickets for the show.\nAgent: Alright, let me take a look.\nCustomer: Thank you.\nAgent: Alright, upon reviewing the schedule Little Women is not playing at 8 PM. It's show times are only 5:00 PM and 9:00 PM. Will either of those times work for you?\nCustomer: No unfortunately they will not work for me.\nAgent: Sorry, is there anything else i can do for you?",
  "question": "Has the customer, by the end of this conversation, actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qf62e683741",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nUsing global line-list data on COVID-19 cases reported until 29th February 2020 and global gridded temperature data, and after adjusting for surveillance capacity and time since first imported case, higher average temperature was strongly associated with lower COVID-19 incidence for temperatures of 1°C and higher.\n\nClaim: Multiple early studies provide evidence of less correlation between temperature and humidity ranges and the geographic regions where this virus has thrived.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qb1feb75f3a",
  "kind": "yes/no",
  "text": "Assistant: What kind of vehicle would you like.\nCustomer: Sedan.\nAssistant: There is no sedan available around that time.",
  "question": "According to the final message from the assistant, is \"sedan\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa210d68ad6",
  "kind": "yes/no",
  "text": "Assistant: Alright. What type of Uber would you like?\nCustomer: UberBlack is fine.\nAssistant: I'm sorry, it looks like UberBlack is not available at this time. Do you have a second preference?",
  "question": "Is \"UberBlack\" for the customer's ride booking confirmed in the final message from the assistant?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc9e8bb77a9",
  "kind": "yes/no",
  "text": "Complaint narrative: WHILE DRIVING ALL OF THE POWER CUTS OFF INCLUDING POWER STEERING. ALTERNATOR, OIL, FUEL, STRUTS, BATTERY X 2 HAVE BEEN CHANGED OUT IN ATTEMPT TO CORRECT ISSUE. ISSUE IS STILL PRESENT. LOCAL CHEVY DEALERSHIP UNABLE TO RECTIFY PROBLEM. THERE HAVE BEEN NUMEROUS INCIDENTS WITH POTENTIAL ACCIDENTS. THERE SEEMS TO BE A POWER DRAW ON THE SYSTEM, UNABLE TO FIND ANY KINKED OR FRAYED WIRES. WHILE DRIVING ALL LIGHTING INCLUDING GAUGES DIMS USUALLY PRIOR TO COMPLETE VEHICLE ELECTRICAL FAILURE. I HAVE A VIDEO OF ELECTRICAL DIMMING, BUT UNABLE TO LOAD ON HERE. VEHICLE IS LABELED AS 2015 BUT MANUFACTURE DATE IS 2014, IVE NOTICED THERE IS A RECALL ON 2014 MODELS FOR ELECTRICAL CHASSIS FAILURE HOWEVER MY VIN IS NOT ENCOMPASSED IN THIS RECALL.",
  "question": "Is it correct that this vehicle safety complaint does not report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "qb69ef974a6",
  "kind": "yes/no",
  "text": "Statement 1: birds' milk is nutrient\nStatement 2: goats' milk is nutrient",
  "question": "Of these two statements, does Statement 2 make sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q94ba8e9cc8",
  "kind": "yes/no",
  "text": "Complaint narrative: DROVE TO WORK AT 6 AM WENT TO USE FOR LUNCH VEHICLE HAD NO POWER ASSISTED STEERING MORE LIKE MANUAL STEERING. MAKING VERY DIFFICULT IN PARKING , ON RAMPS TURNING AT INTERSECTIONS. MY MECHANIC TELLS ME STEERING COLUMN PART FAILURE THAT THEY HAVE REPLACED IN SEVERAL ESCAPES & MARINERS. MY BOSS WENT ON LINE AND FOUND INFO ON RECALL OF 915,216 FORD ESCAPES & MERCURY MARINERS. PROBLEM WAS WHEN BACKING OUT OF PARKING SPOT TYING TO TO TURN TO RIGHT WAS VERY DIFFICULT MORE LIKE MANUAL STEERING",
  "question": "Does this complaint on vehicle safety say the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qc6c2dcbbfb",
  "kind": "yes/no",
  "text": "Complaint narrative: TAKATA RECALL. I HAVE A NOTICE THAT A RECALL IS ACTIVE ON MY VEHICLE. I CALLED THE DEALER TO HAVE IT RESOLVED AND THEY SAY THAT THERE ARE NO PARTS TO MAKE THE REPAIRS AND HAVE NO IDEA WHEN ANY WILL BE AVAILABLE. THE RECALL STATES THAT IF I AM IN A COLLISION AND MY PASSENGER AIR BAG DEPLOYS, THAT MY PASSENGER CAN RECEIVE INJURY OR EVEN DEATH FROM FLYING PIECES OF METAL. HOW IN THE WORLD CAN WE BE ALLOWED TO DRIVE AROUND IN THESE POSSIBLE DEATH MACHINES AND NOBODY SEEMS TO BE DOING ANYHTING ABOUT IT.?????",
  "question": "Is it in this vehicle safety complaint that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q8312b0c50d",
  "kind": "yes/no",
  "text": "In fact, it is almost certain that the wind-generated electricity cost more when the consumer payments, taxpayer subsidies, and the cost of the backup gas generation are added together. There is no doubt that it cost significantly more to generate electricity from wind than from natural gas .",
  "question": "Is there confirmation that this paragraph makes the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q76035c52b7",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThese studies confirm that cats are susceptible to productive SARS-CoV-2 infection, but are unlikely to develop clinical disease.\n\nClaim: Cats can be infected by the novel coronavirus but are unlikely to get sick.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q7528376ba7",
  "kind": "yes/no",
  "text": "Complaint narrative: I WAS PULLING OUT OF A PARKING SPACE WHERE MY FRONT WAS UP AGAINST A BUILDING WITH A CAR ON EITHER SIDE OF ME. I REVERSED FOR ABOUT 25' WHERE A TELEPHONE POLE MANDATED THAT I MAKE A K-TURN TO GET OUT. AS I SWITCHED FROM REVERSE TO FORWARD, I SAW A SPARK AS THE CAR JET-PROPELLED FORWARD. I TRIED TO BREAK MULTIPLE TIMES, BUT THE CAR ACCELERATED THE 25' INTO THE WALL. ALL AIRBAGS DEPLOYED, AND FLUID GUSHED OUT OF THE FRONT END. THE CAR WAS DECLARED A TOTAL LOSS. I WAS TOLD BY TOYOTA AND MY INSURANCE COMPANY THAT I MUST HAVE ACCIDENTALLY ACCELERATED INSTEAD OF REPEATEDLY BREAKING. I AM GRATEFUL THAT I HIT A WALL INSTEAD OF PEOPLE. SOMEONE COULD EASILY HAVE DIED HAD I HAD SWITCHED FROM REVERSE GEAR TO FORWARD IN LESS CONFINED LOCATION. THE ENTIRE ACCIDENT LASTED 2 SECONDS, WITH NO OPPORTUNITY TO PULL THE EMERGENCY BREAK OR GO INTO NEUTRAL. PS: I AM A HAPPILY MARRIED DOCTOR WITH BEAUTIFUL CHILDREN AND GRANDCHILDREN, AND NOT AT ALL SUICIDAL. THIS THREE MONTH OLD 2015 PRIUS 3 FAILED BEFORE THE FIRST OIL CHANGE. I AM NOT SATISFIED WITH THE RESULTS.",
  "question": "Was the vehicle actually involved in a crash, according to this vehicle safety complaint?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q0901c38cbf",
  "kind": "yes/no",
  "text": "Customer: Hey, I'd like to see a movie\nAgent: Okay, what type of movie do you want to see?\nCustomer: I was thinking of a horror movie?\nAgent: Okay, I found Shuttered - Horror - rated R - Rotten Tomatoes 61% - Sarah Decker moves upstate from her New York City lifestyle to work on her distant cousin’s haunted marijuana farm.\nCustomer: On second thought, I was more in the mood for a romantic comedy.\nAgent: Okay, I found Family Jewels - Romantic Comedy - rated R - Rotten Tomatoes 69% - A famous diamond dealer leaves his European life in Antwerp to pursue a less than genuine romance with an American con artist- Stars Melissa McCarthy and Ryan Reynolds.\nCustomer: Yeah, let's go with Family Jewels\nAgent: Okay, when would you like to see it?\nCustomer: Friday\nAgent: And how many tickets?\nCustomer: 2 please\nAgent: And at what time?\nCustomer: Sometime in evening\nAgent: And where are you located?\nCustomer: Spring Hills Kansas\nAgent: Okay, I found two tickets for Family Jewels on Friday at 8:10 pm at AMC Holiday Theater, does that sound good?\nCustomer: Yes, that's great\nAgent: Anything else I can help with\nCustomer: No, I'm good thanks.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "By this conversation's end, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qea3c9e7d44",
  "kind": "yes/no",
  "text": "Customer: Hey assistant, when is 1917 playing at Cinemark in Strongsville?\nAgent: 1917 showtimes are 5:00pm, 6:00pm, and 7:15pm. Would you like me to check these times for ticket availability?\nCustomer: Yes, please check 6:00pm\nAgent: How many tickets do you need?\nCustomer: I need 2 tickets\nAgent: There are not enough seats available for this showtime. Would you like to select another?\nCustomer: No, I would like you to check another theater\nAgent: Which theater would you like me to check?\nCustomer: AMC in Ridge Park\nAgent: Are you still interested in seeing 1917?\nCustomer: Yes, what showtimes are available?\nAgent: There are shows at 5:15pm, 6:00pm, 7:15pm and 8:00 pm\nCustomer: Please check availability for 6:00pm\nAgent: Are you still interested in 2 tickets?\nCustomer: Yes\nAgent: Good news, there are 2 tickets available for this showtime. would you like to book this showtime?\nCustomer: Yes\nAgent: Ok, just to confirm, you would like to order 2 tickets to see 1917 at AMC in Ridge Park at 6:00pm\nCustomer: That is correct\nAgent: Great I have placed the order with your default credit card. You will receive a confirmation email shortly.",
  "question": "Has the customer actually bought movie tickets by the time this conversation finishes?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q27ecd80f07",
  "kind": "yes/no",
  "text": "Statement 1: oil can be found in the sky\nStatement 2: oil can be found in the underground",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q5fc0acf8de",
  "kind": "yes/no",
  "text": "Assistant: Okay, what is the make, model and year of your car?\nCustomer: It is a Hyundai Elantra 2010.\nAssistant: Okay, I have booked you for 6 pm tonight for your Hyundai Elantra 2010..",
  "question": "Referring to the assistant's final message, is \"Hyundai Elantra\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q989a910dc9",
  "kind": "yes/no",
  "text": "Customer: We are looking for an expensive panasian restaurant and prefer it to be in the same area as the hotel. Any suggestions?\nAssistant: I'm sorry but there does not seem to be any expensive panasian restaurants located on the west side.  Would you like to try to search for something else?",
  "question": "In its reply, did the assistant find at least a single option that fits everything the customer requested?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qfde0b02174",
  "kind": "yes/no",
  "text": "Complaint narrative: THIS WAS A LOW MILEAGE (9K) LESS THAN 1 YEAR OLD PRISTINE CONDITION AUDI S6. THE VEHICLE WAS DRIVEN APPROXIMATELY 10 MILES AND THEN PARKED IN A DRIVEWAY WHERE IT WAS TURNED OFF. THE DRIVER SAT IN THE VEHICLE FOR 5 MINUTES WITH THE ENGINE OFF PRIOR TO EXITING THE VEHICLE. BETWEEN 5 TO 10 MINUTES AFTER EXITING THE VEHICLE WE SMELLED SMOKE IN THE HOUSE. WE DISCOVERED THE VEHICLE HAD FLAME AND SMOKE EMANATING FROM UNDER ITS HOOD. THE FIRE DEPARTMENT HAD TO EXTINGUISH THE FLAMES AS WE WERE UNABLE TO DO SO WITH A GARDEN HOSE. THE ENTIRE FRONT OF THE VEHICLE BURNED. IT WAS CLASSIFIED AS TOTALED. THE VEHICLE WAS INSPECTED BY A FIRE CAUSE AND ORIGIN INSPECTOR AND AUDI. I HAVE BEEN TOLD VERBALLY THAT THE FIRE LIKELY BEGAN IN SOME ELECTRICAL COMPONENTS BEHIND THE DRIVER SIDE HEADLIGHT AREA. AUDI HAS CONFIRMED THAT THE FIRE WAS NOT CAUSED BY EXTERNAL FACTORS BUT I HAVE NOT BEEN PROVIDED ANY OTHER FEEDBACK FROM AUDI AS TO WHAT THE ACTUAL DEFECT. WAS. JUST TO RE-CAP: 1. THE IGNITION WAS OFF 2. THE CAR WAS NOT RUNNING 3. THE CAR SPONTANEOUSLY CAUGHT FIRE AND WAS DESTROYED. 4. IT WAS RAINING THAT DAY 5. THE CAR WAS IN LIKE-NEW CONDITION, WELL MAINTAINED AND WITH NO KNOWN DEFECTS. 6. WE WERE LUCKY THE CAR WAS NOT IN THE GARAGE AS THE HOUSE WOULD HAVE CAUGHT FIRE.",
  "question": "Does this safety complaint about the vehicle report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q04d047699c",
  "kind": "yes/no",
  "text": "Assistant: 6:30\nCustomer: Ok, I'll get two tickets for the 3d showing\nAssistant: the 3D showing is sold out",
  "question": "Is it the case that, according to the assistant's last message, \"3D\" is not confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order.\n- no: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction."
 },
 {
  "qid": "qc9583c9208",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nHence, COVID-19 patients can develop psychotic symptoms as a consequence of multiple concurrent factors.\n\nClaim: There are no new-onset psychosis-related symptoms developed as a result of COVID-19.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q2da9fc6f4c",
  "kind": "yes/no",
  "text": "Situation: I knew when my dad was dying.\nAction being judged: Visiting your parent when they are on their death bed.",
  "question": "Is it true that the action being judged is not acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q30a69935bc",
  "kind": "yes/no",
  "text": "Just the opposite is demanded in the dead of winter when there is no sun and when the wind dies down. During the week, energy demand soars and their is often not enough supply to meet the demand. And because many power companies are finding it unprofitable to run conventional systems part-time, many are simply mothballing such plants completely, thus making supply even rarer. As a result, the risk of blackouts is becoming a real increasing threat in Germany with each coming winter.",
  "question": "Is there confirmation that this paragraph makes the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q06413843f6",
  "kind": "yes/no",
  "text": "Table caption: Rate of Return of different insulation technologies ( Milieucentraal, 2019 ).\n| Insulation technology | Rate of Return (%) |\n| Wall insulation | 11 |\n| Floor insulation | 7 |\n| Double glazing | 6 |\n| Roof insulation | 8 |\n\nStatement: Roof insulation is having 8% second highest of rate of return.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qd361681894",
  "kind": "yes/no",
  "text": "Occupation: Textile Cutting Machine Setters, Operators, and Tenders\nDuties:\n- Notify other workers of defects, and direct them to adjust extruding and forming machines.\n- Lower pans inside cabinets to catch molten filaments until flow of polymer through packs has stopped.\n- Start metering pumps and observe operation of machines and equipment to ensure continuous flow of filaments extruded through spinnerettes and to detect processing defects.",
  "question": "Is it correct that the listed duties are not part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "qcfbc01634e",
  "kind": "yes/no",
  "text": "Situation: I think I sold a suicidal woman sleeping pills\nAction being judged: Selling things that people can use to kill themselves when that person is suicidal.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qd23b04c774",
  "kind": "yes/no",
  "text": "Complaint narrative: WHILE ATTEMPTING TO OPERATE THE ELECTRIC SLIDING SIDE DOOR, A LARGE SPARK AND SMALL DEBRIS FIRE WAS SEEN IN THE BOTTOM DOOR RAIL. UPON INSPECTION, A BREAK IN THE WIRE HARNESS HAD ALOUD WIRES TO BE SEVERED THAT CONTROLS THE DOOR AND LOCKING SYSTEM. THE AUTOMATIC DOOR LOCKS ON BOTH SIDE DOORS NO LONGER WORKED AND THE PASSENGER SIDE DOOR WOULD NO LONGER OPEN ELECTRICALLY. I REMOVED THE WIRING HARNESS AND WIRES AND DISCARDED THEM TO AVOID ANY MORE PROBLEMS (SPARKING AND/OR FIRES). THIS COULD CAUSE A MAJOR FIRE HAZARD IN THE RIGHT ENVIRONMENT.",
  "question": "Does this vehicle safety complaint say that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q74a4312fdd",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThe odds that a primary case transmitted COVID-19 in a closed environment was 18.7 times greater compared to an open-air environment (95% confidence interval [CI]: 6.0, 57.9).\n\nClaim: The odds of catching the coronavirus are about 20 times higher indoors than outdoors.",
  "question": "According to the evidence, does it support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qb1026f23e5",
  "kind": "yes/no",
  "text": "Customer: Hi,can u please help me to book movie tickets\nAgent: Ya of course,do u any location in your mind\nCustomer: Yes i am looking theater in Spring Hills Kansas\nAgent: Ok,currently there are two movies running in that area\nCustomer: Ok can u please tell me what are the movies and they details\nAgent: Not My Problem, Beyond The Storm this are the movies which are currently running\nCustomer: Can u explain the stories of both the movies\nAgent: Movie1: Not My Problem - Comedy - rated PG-13 - Rotten Tomatoes 72% - A troubled teen tries to convince his depressed elderly neighbor that things are not what they seem. - Stars Matt Damon and Noah Schnapp.\nCustomer: Ratings are good also i would prefer to watch comedy movie,can u tell about the second movie\nAgent: Movie2: Beyond The Storm - Action - rated PG-13 - Rotten Tomatoes 81% - Fishing the North Sea gets ugly as Captain John’s crew faces not only severe weather but a traitor on board - directed by James Cameron.\nCustomer: I love to watch action movies\nAgent: Which movie did u prefer?\nCustomer: I will go with the second movie Beyond The Storm\nAgent: Ok, how many tickets do u need\nCustomer: I need 3 tickets can u tell the timing for both the movies\nAgent: Not My Problem: AMC Holiday Theater - 1pm - 3:55pm - 7pm - 10:05pm Beyond the Storm: Cinemark Downtown - 1:30pm - 3:40 - 6:10pm - 8:30pm\nCustomer: I will go with the 6.10 pm show in cinemark downtown\nAgent: ok, its 3 tickets for BEYOND THE STROM for 6.10 pm show in cinemark downtown is it right can i book for u\nCustomer: Yes, you can boo\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "Is it correct that, by the end of this conversation, the customer has not actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "q1a6a3f243e",
  "kind": "yes/no",
  "text": "Customer: I want to watch a movie tonight\nAgent: No problem. Do you have a movie in mind?\nCustomer: I am thinking of No Time To Die\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: is there no showing in Davis, California?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: too bad. what action films are playing in Davis, California?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: is that the original film from the 1970s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: great, I think I will buy the tickets tomorrow\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By this conversation's end, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q88d1650dc7",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Bachchan's first release of 2005 was the crime comedy \"Bunty Aur Babli\", which featured him and Rani Mukerji as the titular con artist duo who perform several successful heists and fall in love along the way.\n- His next two releases \"Dus\" (2005) and \"Bluffmaster!\"\n- (2005) were both moderately successful, but did not earn much critical appreciation.\n- Bachchan earned much critical acclaim for his performance in Mani Ratnam's \"Guru\" (2007), loosely based on the life of business magnate Dhirubhai Ambani.\"\n- His next release was the dance comedy \"Jhoom Barabar Jhoom\" (2007) alongside Preity Zinta, Bobby Deol, and Lara Dutta.\n- Bachchan's first release of 2008 was Ram Gopal Varma's \"Sarkar Raj\", which featured him and his father Amitabh Bachchan reprising their roles from \"Sarkar\" (2005) while his wife Aishwarya Rai Bachchan entered the cast as a new addition.\n- This film proved to be successful at the box office and earned him a nomination for the Filmfare Award for Best Supporting Actor.\n- Bachchan was next seen in \"Dostana\" (2008), a romantic comedy about two men (Bachchan and John Abraham) who pretend to be gay in order to be allowed to live with a girl (Priyanka Chopra), but then find that they have both fallen in love with her.\n- These films were the thriller \"Raavan\" (2010), the social drama \"Khelein Hum Jee Jaan Sey\" (2010), action thrillers \"Game\" (2011), \"Dum Maaro Dum\" (2011) & the heist thriller \"Players\" (2012).\n- Bachchan then played the lead role in Rohit Shetty's comedy \"Bol Bachchan\" (2012), which was a major blockbuster at the box office despite receiving mixed reviews from critics.\n- Bachchan was next seen in Farah Khan's dance comedy \"Happy New Year\", a musical heist film, playing the second lead to Shah Rukh Khan.\n- Bachchan's first release of 2016 was the comedy \"Housefull 3\", the third installment of the Housefull film series.\n\nSummary sentence:\nBachchan has also played leading and supporting roles in commercially successful comedies and dramas, including \"Bunty Aur Babli\" (2005), \"Dus\" (2005), \"Bluffmaster!\" (2005), \"Guru\" (2007), \"Jhoom Barabar Jhoom\" (2007), \"Sarkar Raj\" (2008), \"Dostana\" (2008), \"Dum Maaro Dum\" (2011), \"Bol Bachchan\" (2012), \"Happy New Year\" (2014) and \"Housefull 3\" (2016).",
  "question": "Is every piece of information in the sentence that gives the summary supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q369d9de914",
  "kind": "yes/no",
  "text": "Assistant: Ok. I need what is a best phone number?\nCustomer: They can reach me at 123-456-8989\nAssistant: TOday does not work. Would tomorrow morning at 8 a.m. be Ok?",
  "question": "Is the assistant's final message saying that \"TOday\" is confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qeddb0c192f",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nVirus was widely distributed on floors, computer mice, trash cans, and sickbed handrails and was detected in air ≈4 m from patients.\n\nClaim: The coronavirus can be detected in the air up to 13 feet away from an infected patient.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q94cd1eaeed",
  "kind": "yes/no",
  "text": "Customer: Hey!\nAgent: Hi what can I help you with today?\nCustomer: Well I am getting a bit bored and am in the mood for a good movie.\nAgent: SUre I can help. What did you want to see\nCustomer: Well how about Mulan I would need one adult and two child tickets. or perhaps No Time t Die\nAgent: Where did you want to see that at.\nCustomer: Well my first choice would be the Holiday Cinemark in Stoneyford Oregon\nAgent: SUre, let me check\nCustomer: Okay.\nAgent: I am sorry but that Theater is temporarily closed due to the virus. And Mulan is not going to be released now until the fall.\nCustomer: Oh I see, maybe I can get a babysitter so I could go see No time to die.\nAgent: Well did you want to try another theater?\nCustomer: Sure how about the Mountain AMC 16 in Stoneyford.\nAgent: How many tickets\nCustomer: 2 Adults please\nAgent: Ok let me check\nCustomer: Thank you.\nAgent: I am sorry but that theater is also temporarily closed. That movie is also postponed until the fall as well. It seems both theaters are closed and both movies are postponed until the fall.\nCustomer: Ok well I guess I am out of luck.\nAgent: Im sorry! We look forward to serving you again hopefully in the near future!!!!",
  "question": "Is it correct that, by the end of this conversation, the customer hasn't actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "q2fd7a3ed66",
  "kind": "yes/no",
  "text": "Statement 1: a dog is taken to a pool after getting sick\nStatement 2: a dog is taken to a veterinarian after getting sick",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q0f1dad9c36",
  "kind": "yes/no",
  "text": "Situation: He told his dad he didn't want to hunt quail.\nAction being judged: Saying no to doing something you aren't comfortable with.",
  "question": "According to common social norms, is the action being judged wrong?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q259079e4ca",
  "kind": "yes/no",
  "text": "Customer: I would like to purchase movie tickets.\nAgent: What movie would you like to see?\nCustomer: I would like to see Little Women.\nAgent: How many tickets do you need?\nCustomer: I need 2 tickets.\nAgent: Where would you like to see the movie?\nCustomer: At the RiverPark cinemas in Oxnard.\nAgent: Do you have a preference on times?\nCustomer: yes, I would love something in the early afternoon. maybe around 1pm.\nAgent: There is a 1:30pm and a 5:15pm, which works for you?\nCustomer: The 1:30pm, thank you.\nAgent: The 1:30pm showing appears to be sold out. Would you like me to purchase tickets for the 5:15pm?\nCustomer: No, that is too late.\nAgent: Is there anything else I can help you out with?\nCustomer: Yes, is the new Star Wars movie playing at that theater in the early afternoon?\nAgent: There is a 1:45pm showing of the new Star Wars movie.\nCustomer: Is it in 3-D?\nAgent: Yes, would you like me to book the tickets?\nCustomer: Yes please.\nAgent: You are confirmed to see the new Star Wars movie in 3-D at 1:45pm at the RiverPark cinemas in Oxnard.\nCustomer: Thank you!\nAgent: Is there anything else I can assist you with?\nCustomer: No thank you.",
  "question": "By the end of this dialogue, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qabcae0d7e6",
  "kind": "yes/no",
  "text": "Complaint narrative: TAKATA RECALL LETTER THAT WE RECEIVED FROM TOYOTA DIRECTED US TO STOP USING THE PASSENGER SEAT IN THE CAR DUE TO SAFETY CONCERNS, AND ADVISED THAT WE WOULD RECEIVE FURTHER INSTRUCTIONS IN APRIL. IT IS NOW MAY AND WE HAVE NOT HEARD FROM TOYOTA AND THE LOCAL DEALERSHIP ADVISES US THAT NO REMEDY IS AVAILABLE FOR US. WE ARE NOT ABLE TO SAFELY USE THE VEHICLE AS A FAMILY, AND WE HAVE NO IDEA WHEN OR IF WE WILL BE ABLE TO USE THE VEHICLE SAFELY AGAIN. THE VEHICLE IS CURRENTLY BEING USED DAILY BY DRIVER ONLY, AND IT IS UNCLEAR WHETHER THE VEHICLE POSES A THREAT TO DRIVER'S SAFETY.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q77f27bf4a8",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nRates of ventilation in the HC, HC+AZ, and no HC groups were 13.3%, 6.9%, 14.1%, respectively. The risk of ventilation was similar in the HC group (adjusted hazard ratio, 1.43; 95% CI, 0.53 to 3.79; P=0.48) and in the HC+AZ group (adjusted hazard ratio, 0.43; 95% CI, 0.16 to 1.12; P=0.09), compared to the no HC group. CONCLUSIONS: In this study, we found no evidence that use of hydroxychloroquine, either with or without azithromycin, reduced the risk of mechanical ventilation in patients hospitalized with Covid-19.\n\nClaim: Hydroxychloroquine does not help patients avoid being placed on a ventilator.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qf70e4762a4",
  "kind": "yes/no",
  "text": "Assistant: Great! Give me a few seconds to book your appointment.\nCustomer: Thank you!\nAssistant: Already! You're all set. I have booked an appointment for you at 10:30 in the morning. If the service is not covered, there will be a minimum fee for this service.",
  "question": "Is there confirmation in the assistant's final message of \"10:30 in the morning\" for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q36b1f65880",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nOf these, 94 were working in an 11th-floor call center with 216 employees, translating to an attack rate of 43.5% (95% CI 36.9%–50.4%).\n\nClaim: Superspreading events can happen at call centers.",
  "question": "Is there a contradiction between the evidence and the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q7a3638fc35",
  "kind": "yes/no",
  "text": "Assistant: How many do you need at your table?\nCustomer: Just two it's a romantic date.\nAssistant: I have you set up for a table for two tonight at Malone's at 8 p.m.",
  "question": "Is \"Malone's\" for the customer's restaurant reservation confirmed in the final message from the assistant?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfce92cf217",
  "kind": "yes/no",
  "text": "I frankly find it immensely sad that, not only real events, but also the work and knowledge of serious scientists, accumulated over many years, can apparently be swept aside at the whim of an algorithm. Computer models can have their value, but we surely need to keep an eye on whats happening in the real world.",
  "question": "Within this paragraph, does it make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q15e26d3db2",
  "kind": "yes/no",
  "text": "Customer: I would love to find an action move to watch tonight with my wife since it's my turn to pick.\nAgent: Sounds like so much fun. There are a number of action movies out there. Would you like me to list those out.\nCustomer: Yes, that would be great.\nAgent: There is Star Wars: Rise of Skywalker, Jumanji: The Next Level, Spies in Disguise, Ford v Ferrari, and 21 Bridges.\nCustomer: That sounds like a lot of choice. Can you narrow it down to those that are R rated and geared towards adults only?\nAgent: No problem. It turns out that is easy as 21 Bridges is the only R rated film in that group.\nCustomer: Can you tell me any more about the movie?\nAgent: Absolutely! It stars Chadwick Boseman and the synopsis states: An NYPD detective searches for two cop killers as authorities close all of Manhattan's 21 bridges.\nCustomer: Wow! It sounds really interesting and fits my desire for action and my wife's love of police related shows. Is it playing in Omaha, Nebraska?\nAgent: It looks like it has a fairly limited release, but is playing at two theaters this evening in or near Omaha.\nCustomer: Could you list those two theaters?\nAgent: AMC COUNCIL BLUFFS 17 and AMC OAKVIEW PLAZA 24.\nCustomer: Those are both about the same distance from my home. Could you tell me the next available time for the showing at AMC OAKVIEW PLAZA 24?\nAgent: Sure thing, but first, do you have any preferred viewing experiences?\nCustomer: I actually am fine with Standard.\nAgent: Thank you. It looks like there is a Standard showing at 5:25.\nCustomer: I think that actually works pretty well, though I know it's not two far away.\nAgent: You mentioned earlier that you would only be needing two tickets?\nCustomer: Yes, just me and my wife.\nAgent: Great. I show you are interested in two tickets for 21 Bridges at AMC OAKVIEW PLAZA 24 for the 5:25 PM.\nCustomer: That is correct.\nAgent: Would you like me to complete your purchase now?\nCustomer: Actually, I think I want to hold off until I talk with my wife. We may purchase at the theater though.\nAgent: Makes sense. Is there anything else I can help with.\nCustomer: No, but thanks for your help and making my movie decision easier!\nAgent: Absolutely and I hope you enjoy your movie!",
  "question": "By the end of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q214d263f02",
  "kind": "yes/no",
  "text": "Statement 1: your advice has helped me get along well with my pencils\nStatement 2: your advice has helped me get along well with my classmates",
  "question": "Of these two statements, does Statement 2 make sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q9b2257045d",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS: The incidence of VTE in patients with severe NCP is 25% (20/81), which may be related to poor prognosis.\n\nClaim: There are approximately 1 in 4 incidences of venous thromboembolism in patients with severe novel coronavirus pneumonia symptoms of SARS-CoV-2.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q959caf2438",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Amy Lysle Smart\n- Smart was born in Los Angeles, California, and raised in Topanga Canyon.\n- Also in 2005, she starred as Sarah in the British independent film \"The Best Man\" with Seth Green.\n\nSummary sentence:\nAmy Lysle Smart (born March 26, 1976) is an American actress.",
  "question": "Is every piece of information in the summary sentence given support by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q167b6f9364",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2006, the science journal \"Nature\" listed Pharyngula as the top-ranked blog written by a scientist.\n\nSummary sentence:\nIn 2006 the journal \"Nature\" listed Myers's \"Pharyngula\" as the top-ranked blog by a scientist based on popularity.",
  "question": "Is every bit of info in the summary sentence backed up by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q68c7d2fa9b",
  "kind": "yes/no",
  "text": "Assistant: O.K. Now for the toppings.\nCustomer: Green olives and tomatoes on one.\nAssistant: Green olives not available.",
  "question": "Going by the assistant's latest message, is \"Green olives\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7bb33efcfb",
  "kind": "yes/no",
  "text": "Situation: I get mad if my parents throw away my bubble wrap.\nAction being judged: Throwing out something when it belongs to someone else.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 }
]
