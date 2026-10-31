# G5-H blind read T37b-blind_read-1b186e86-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3_qc3/g5h/answers/T37b-blind_read-1b186e86-000.json

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
  "qid": "q841fc87257",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS AND RELEVANCE: In this survey of heath care workers in hospitals equipped with fever clinics or wards for patients with COVID-19 in Wuhan and other regions in China, participants reported experiencing psychological burden, especially nurses, women, those in Wuhan, and frontline health care workers directly engaged in the diagnosis, treatment, and care for patients with COVID-19.\n\nClaim: Female front-line workers treating patients with COVID-19 experienced higher rates or more severe symptoms of depression, anxiety, insomnia and distress than health-care workers overall.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q17e0bb2d1f",
  "kind": "yes/no",
  "text": "Statement 1: He ran a race.\nStatement 2: He spun a race.",
  "question": "Among the statements given: Statement 2, is it going against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q57f095954a",
  "kind": "yes/no",
  "text": "Complaint narrative: WHILE MY WIFE, LINDA, WAS DRIVING LESS THAN 1-2 MPH, TURNING INTO A PARKING SPACE, ALL OF A SUDDEN, THE ENGINE STARTED RACING AND LEAPED FORWARD. HITTING THE BRAKES HAD NO EFFECT ON STOPPING THE VEHICLE. SHE DESPERATELY TURNED THE WHEEL TO MISS PARKED CARS, A STEEL POLE WAS HIT AND TORN OUT OF THE GROUND BY THE RUNAWAY VEHICLE. FINALLY THE CAR CAME TO REST AFTER HITTING A LARGE CONCRETE LIGHT POLE, WHICH MUST HAVE STALLED OUT THE ENGINE. MY WIFE WAS IN A STATE OF SHOCK AND HAD TO GO TO THE HOSPITAL FOR TESTS / XRAYS. EVEN WITH THE SEAT BELT ON, SHE RECEIVED MAJOR IMPACT FROM THE STEERING WHEEL TO HER CHEST.",
  "question": "In this vehicle safety complaint, does it report that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q512fad8e8f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- After leaving parliament, Purnell became the chair of the Institute for Public Policy Research.\n- Purnell became linked with the Blue Labour movement within the Labour Party and in April 2011 he was appointed by the Boston Consulting Group as a Special Advisor to their Public Sector Group.\n\nSummary sentence:\nPurnell chaired the Institute for Public Policy Research until 2010, and was a senior advisor in the Public Sector practice of the Boston Consulting Group.",
  "question": "Is the summary sentence's information, every piece of it, supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q88be34c798",
  "kind": "yes/no",
  "text": "It is interesting, however, that those who seek an arrest and conviction for criminal negligence, or voluntary manslaughter, want the crime to be charged before the victims are dead. The usual cry from the alarmists uses the future tense, as polar ice caps WILL melt, and sea levels WILL rise. Or, more often, the conditional form is used, saying sea levels COULD rise by 20 feet in 100 years.",
  "question": "Within this paragraph, does it make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qbfa36ccdac",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nReports from China and Italy suggest that risk factors for severe disease include older age and the presence of at least one of several underlying health conditions (3,4).\n\nClaim: COVID-19 severity equally impacts people of all ages with or without chronic diseases.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q9bbb5ff402",
  "kind": "yes/no",
  "text": "Customer: Any thriller/suspense movies playing currently?\nAgent: What movie theater do you want to check out?\nCustomer: Check out the AMC River East Theater.\nAgent: Ok, there's Knives Out, The Turning, and Underwater.\nCustomer: What's the runtime for Knives Out?\nAgent: Knives Out has a runtime of 2 hours, 10 minutes.\nCustomer: Does AMC River East 21 offer IMAX screenings?\nAgent: Yes, they do.\nCustomer: Ok, Get me three ticket for me and two of my friends for Knives Out.\nAgent: Ok, and what showtime do you want?\nCustomer: I want the 7:00 PM showtime.\nAgent: What screening type do you want?\nCustomer: Just standard.\nAgent: Ok, that's three tickets for the 7:30 PM standard screening for Knives Out at the AMC River East 21 theater?\nCustomer: Yes, that's right. Oh, by the way, does switching to IMAX screening cost extra\nAgent: Switching to IMAX will incur a 5% surcharge. Do you want to switch from standard screening to IMAX screening.\nCustomer: No, that's fine.\nAgent: Ok, so the total comes to $46.94\nCustomer: Charge my Visa card.\nAgent: Ok, order has been confirmed.\nCustomer: Where's my receipt?\nAgent: It will appear in you email inbox shortly. Anything else?\nCustomer: That's all.\nAgent: Goodbye.",
  "question": "Has the customer actually bought movie tickets by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q72f6e9c370",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nWeather may marginally affect COVID-19 dynamics, but misconceptions about the way that climate and weather drive exposure and transmission have adversely shaped risk perceptions for both policymakers and citizens.\n\nClaim: Experts demonstrated that seasonal effects would completely prevent the virus from spreading.",
  "question": "Does the evidence contradict it?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qf87731b83a",
  "kind": "yes/no",
  "text": "Customer: Hi, I'd like to see a movie tonight.\nAgent: Ok, great which movie do you want to see?\nCustomer: Umm, not sure either No Time to Die or Mulan.\nAgent: Ok, let me check. Where are you located?\nCustomer: Stoneyford Oregon.\nAgent: Ok, let me check Mountain AMC 16.\nCustomer: Great.\nAgent: Oh, no, unfortunately this theater is closed.\nCustomer: Ok, is there any other theater near me?\nAgent: Yes, let me check Holiday Cinemark 12.\nCustomer: Great.\nAgent: Ok, it seems like this theater is closed.\nCustomer: Oh, that's unfortunate.\nAgent: Yes, I can't seem to find any movie theaters open in your area.\nCustomer: Hmmm ok.\nAgent: After some research, I've found that no time to die's release date has been postponed, as well as Mulan's.\nCustomer: Do you know until when?\nAgent: Yes, they are both postponed until the fall.\nCustomer: Ok, thanks for your help.\nAgent: You're welcome.",
  "question": "Has the customer actually bought movie tickets by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qcd9549e372",
  "kind": "yes/no",
  "text": "Statement 1: She took her fish for a walk.\nStatement 2: She took her dog for a walk.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q1d780248c4",
  "kind": "yes/no",
  "text": "Table caption: Mass distribution of available bone tissue samples expressed as total weight (wt) in grams. The percentages of dark and light coloured samples, as well as the rest are shown and expressed as wt%.\n| Level | Hearth | Sample label | Total weight (g) | Dark colour (wt%) | Light colour (wt%) | Rest (<2mm) (wt%) |\n| L4 | a | (5–8)3 | 2.12 | 100 | 0 | 0 |\n| L4 | A | 01 | 34.24 | 56.3 | 23.6 | 20.2 |\n| L4 | B | 04 | 47.05 | 62.3 | 28.5 | 9.1 |\n| L4 | D | 02 | 75.94 | 77.1 | 13.0 | 9.8 |\n| L4 | E | 03 | 5.51 | 59.6 | 0 | 40.4 |\n| L5 | K2 | H301 | 48.71 | 72.2 | 6.2 | 21.6 |\n| L5 | J1 | J301 | 4.08 | 64.3 | 35.7 | 0 |\n| L7 | a | (1–2)1 | 0 | 0 | 0 | 0 |\n| L7 | Y | 01 | 2.26 | 100 | 0 | 0 |\n| L7 | W1 | 02 | 14.01 | 77.4 | 10.4 | 12.2 |\n| L7 | W2b | 2–03 | 3.67 | 63.0 | 37.0 | 0 |\n| L8 | A | 0 | 2.40 | 0 | 100 | 0 |\n| L11 | I | (1–2)1 | 99.57 | 73.05 | 17.1 | 9.9 |\n| L11 | I | (1–2)5 | 120.63 | 69.0 | 20.9 | 10.1 |\n| L11 | L | (5–8)6 | 83.37 | 69.3 | 18.6 | 12.1 |\n| L14 | T | 01 | 67.56 | 74.9 | 17.0 | 8.0 |\n| L14 | V | 03 | 74.78 | 60.5 | 23.1 | 16.4 |\n| L14 | Ω | 01 | 75.24 | 75.5 | 7.9 | 16.6 |\n\nStatement: L11 of sample label (1Ai2)5 has highest total weight of 120.63.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qa864022a6a",
  "kind": "yes/no",
  "text": "Customer: The type of food is not important, but I would like a nice place that has tables available on Saturday evening.\nAssistant: Sure, I would recommend the Midsummer House Resaurant which serves British food.  It is a nice, expensive place located in the Centre.",
  "question": "Going by the text, did the assistant's reply include at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qf055fa0dc9",
  "kind": "yes/no",
  "text": "That is what I mean by fighting on marshy ground, by fighting on the same ground as the Warmists. No wonder they stand their ground it is as if the Skeptics are fundamentally in agreement with them, only differing in scale.",
  "question": "Does this paragraph put forward the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q96435caa8c",
  "kind": "yes/no",
  "text": "Occupation: Postal Service Clerks\nDuties:\n- Weigh letters and parcels, compute mailing costs based on type, weight, and destination, and affix correct postage.\n- Check mail to ensure correct postage and that packages and letters are in proper condition for mailing.\n- Transport mail from one work station to another.",
  "question": "Does the job of the occupation named above include the listed duties?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q19ce1ae8bc",
  "kind": "yes/no",
  "text": "Customer: I want to order two movie tickets for the petoskey cinema.\nAgent: What movie would you like to order tickets to?\nCustomer: Star Wars: Episode IX - The Rise of Skywalker\nAgent: Is there a prefered time?\nCustomer: 7:00 Pm\nAgent: Checking there are no available tickets for this time slot do you have another time?\nCustomer: 4:30 pm\nAgent: Checking again these tickets are sold out for your choice of theatre. Is there another movie?\nCustomer: Jumanji: The Next Level\nAgent: What time would you prefer?\nCustomer: Try the 7 pm show\nAgent: I see there is one ticket available for this time would you like me to book.\nCustomer: No I need two tickets\nAgent: Is there another time\nCustomer: Try the 4:30 pm slot\nAgent: Is this for two tickets as well\nCustomer: Yes\nAgent: Checking and I see there are no tickets for this time slot.\nCustomer: Okay thank you I guess I will try another day.\nAgent: You are welcome Is there anything else I can help you with.\nCustomer: No thank you\nAgent: Goodbye then",
  "question": "Is it correct that, by the end of this conversation, the customer hasn't actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "q2d465c7024",
  "kind": "yes/no",
  "text": "Situation: I used to seriously dislike Spongebob.\nAction being judged: Expressing your opinion about a tv show.",
  "question": "Is it correct that the action being judged isn't wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qa0e2d94f36",
  "kind": "yes/no",
  "text": "Sedjo and Clawson also said \"While the local effects of rapid deforestation may be severe, the evidence does not support the view that either the world or the tropics are experiencing rapid aggregate deforestation. Furthermore, the evidence shows that current rates of deforestation are quite modest in much of the world's virgin tropical forests, for example those of the Amazon; and therefore they are probably in little danger of wholesale destruction in the foreseeable future.\" (Eco-Sanity, p.90)",
  "question": "Within this paragraph, does it make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q2fa8ff434f",
  "kind": "yes/no",
  "text": "Assistant: Ok it looks like the hand toss is unavailable.\nCustomer: Ok do pan crust then.\nAssistant: Ok i'm so sorry but it looks like I can't get meat lovers they are out of ham.",
  "question": "Per the assistant's latest message, is \"meat lovers they are out of ham\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5fe39c929c",
  "kind": "yes/no",
  "text": "Situation: I sat back, and breathed in a sigh of relief as I let out a smile.\nAction being judged: Smiling when you are happy.",
  "question": "Under common social norms, is the action being judged wrong?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "qe6d1ebd624",
  "kind": "yes/no",
  "text": "Situation: Couple Weighs Reconciliation Five Years After Violent Split\nAction being judged: Letting things get violent.",
  "question": "Is it true that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qdcc6404a27",
  "kind": "yes/no",
  "text": "Statement 1: It was so hot that he sweated a ton\nStatement 2: It was hot and he sweated all over the body",
  "question": "Upon examining the statements shown: Statement 2, does it go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q7be93a1b76",
  "kind": "yes/no",
  "text": "Assistant: Okay I will call them now. Sorry for the inconvenience.\nCustomer: That's okay. Thanks.\nAssistant: So I placed your order for a large pizza with peperoni and bacon at Papa Johns in Sidney Oh.",
  "question": "Pursuant to the assistant's final message, is \"Papa Johns\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q021cffe663",
  "kind": "yes/no",
  "text": "Occupation: Pediatric Surgeons\nDuties:\n- Perform transplantation operations, such as organ transplants, on fetuses, infants, children, and adolescents.\n- Examine fetuses, infants, children, and adolescents, and diagnose health issues to determine need for intervention, such as surgery.\n- Operate on fetuses, infants, children, and adolescents to correct deformities, repair injuries, prevent and treat diseases, or improve or restore patients' functions.",
  "question": "Is it the case that the listed duties are not part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "qb7821fc92b",
  "kind": "yes/no",
  "text": "Occupation: Skincare Specialists\nDuties:\n- Determine which products or colors will improve clients' skin quality and appearance.\n- Examine clients' skin, using magnifying lamps or visors when necessary, to evaluate skin condition and appearance.\n- Perform simple extractions to remove blackheads.",
  "question": "Are the listed duties part of the job, for the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qa938eb65a7",
  "kind": "yes/no",
  "text": "Statement 1: The room was dark so I turned on the lamp.\nStatement 2: The room was dark so I turned on the stereo.",
  "question": "Of these two statements, does Statement 1 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q04d9ec50d4",
  "kind": "yes/no",
  "text": "Customer: Hello what movies are playing in the Petoskey area?\nAgent: There are several do you have a preference?\nCustomer: Just list a few and tell me about them.\nAgent: Okay I will list them in release date.\nCustomer: That's good\nAgent: The Gentleman is about a drug lord that tries to sell off his empire\nCustomer: No I'm not into drug lords\nAgent: Okay then there is Gretel and Hansel an offbeat take on the fairy tale.\nCustomer: No interest there either.\nAgent: Bad boys for life is the third instalment of the bad boy starring will smith and Martin lawrence\nCustomer: No I am taking my wife and she would not like that film. Is there any comedy type films.\nAgent: How about Jumanji the next level?\nCustomer: That sounds like a winner we saw the first one and loved it.\nAgent: Okay do you have a time preferences?\nCustomer: Well we will be going to dinner first so the later show would be preferable.\nAgent: There is a 915pm show at the Petoskey Cinema for Jumanji the next level for tonight.\nCustomer: No i am not booking for tonight, this is for Valentines and I am taking my wife to dinner and A movie.\nAgent: So you wish to book the tickets for February 14th.\nCustomer: Make it the thirteenth of February,\nAgent: I can order the tickets if you wish.\nCustomer: No wait until the twelfth, then order in case my plans change.\nAgent: Okay just to confirm on the twelfth of February you wish me to order two tickets for Jumanji the next level for the 915 pm show at The Petoskey Cinema.\nCustomer: Sounds great\nAgent: Consider it done",
  "question": "By the close of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q70a69860e6",
  "kind": "yes/no",
  "text": "Occupation: Chemical Plant and System Operators\nDuties:\n- Control or operate chemical processes or systems of machines, using panelboards, control boards, or semi-automatic equipment.\n- Move control settings to make necessary adjustments on equipment units affecting speeds of chemical reactions, quality, or yields.\n- Interpret chemical reactions visible through sight glasses or on television monitors and review laboratory test reports for process adjustments.",
  "question": "Based on the text, are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q0adc2e1b54",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nWe estimate that the global ability to detect imported cases is 38% (95% HPDI 22% – 64%) of Singapore’s capacity. Equivalently, an estimate of 2.8 (95% HPDI 1.5 – 4.4) times the current number of imported cases, could have been detected, if all countries had had the same detection capacity as Singapore.\n\nClaim: Health experts say that it makes no difference: a study by Harvard’s Center for Communicable Disease Dynamics found that Singapore was just as likely to detect infected people as other nations despite its “very strong epidemiological surveillance and contact-tracing capacity.”",
  "question": "Does the evidence contradict it?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q683ac7d757",
  "kind": "yes/no",
  "text": "Customer: Please book that for 3 people for 3 nights starting on Friday.\nAssistant: Booking was successful.\nReference number is : IKC0PEFS.",
  "question": "Does the assistant's reply verify that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q1fc4f1e4d8",
  "kind": "yes/no",
  "text": "Customer: Yes. I'd like to book a room on Friday for 2 nights for 7 people.\nAssistant: That booking was unsuccessful. Would you like to try a different day, or a different length of stay?",
  "question": "Does the assistant's reply confirm that the reservation the client requested was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q8f441e1931",
  "kind": "yes/no",
  "text": "Situation: I don’t mind vertical filming on phones because I find it hard to hold my phone sideways.\nAction being judged: Not following established social norms.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qbac4c956d2",
  "kind": "yes/no",
  "text": "Bob Saget\nRobert Lane \"Bob\" Saget (born May 17, 1956) is an American stand-up comedian, actor, and television host. His television roles include Danny Tanner on the ABC sitcom \"Full House\" (1987–95) and its Netflix sequel \"Fuller House\", and hosting \"America's Funniest Home Videos\" from 1989 to 1997. Saget is also known for his adult-oriented stand-up routine. He also provided the voice of the future Ted Mosby on the CBS sitcom \"How I Met Your Mother\" from 2005 to 2014.\n\nLyudmil Kirkov\nLyudmil Kirkov (Bulgarian: Людмил Кирков , 14 December 1933 – 12 December 1995) was a Bulgarian film director and actor.",
  "question": "Is it accurate to say that Lyudmil Kirkov and Bob Saget are not both film or TV stars?",
  "definitions": "- yes: The paragraphs do not bear out the positive statement (the question read without its 'not' or 'fail to'): at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer.\n- no: Read together, the paragraphs show that the positive statement (the question read without its 'not' or 'fail to') holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right)."
 },
 {
  "qid": "q77f27bf4a8",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nRates of ventilation in the HC, HC+AZ, and no HC groups were 13.3%, 6.9%, 14.1%, respectively. The risk of ventilation was similar in the HC group (adjusted hazard ratio, 1.43; 95% CI, 0.53 to 3.79; P=0.48) and in the HC+AZ group (adjusted hazard ratio, 0.43; 95% CI, 0.16 to 1.12; P=0.09), compared to the no HC group. CONCLUSIONS: In this study, we found no evidence that use of hydroxychloroquine, either with or without azithromycin, reduced the risk of mechanical ventilation in patients hospitalized with Covid-19.\n\nClaim: Hydroxychloroquine does not help patients avoid being placed on a ventilator.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q217b714379",
  "kind": "yes/no",
  "text": "In essence, what we have here is a new satellite using new tools to take measurements. The data recovered is analyzed using guesses and inferences. Their analysis is presented with a margin of error as large as the amount of ice they say is melting from Antarctica. The loss is is less than 1% of the normal annual melt.",
  "question": "Is it accurate to say that this paragraph doesn't make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable.\n- no: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy."
 },
 {
  "qid": "q60da6e0bb7",
  "kind": "yes/no",
  "text": "Statement 1: Harry stoops down to throw the basketball into the basket\nStatement 2: Harry jumps high to throw the basketball into the basket",
  "question": "Of these two statements, does Statement 2 agree with common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "qf0ff55c872",
  "kind": "yes/no",
  "text": "Customer: Yes can I make a reservation for 1 people at 16:15 on wednesday?\nAssistant: I'm sorry, there are no available tables at that time. Would you like me to look for a different restaurant?",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "q31237c2925",
  "kind": "yes/no",
  "text": "Statement 1: An infant needs sun, water and soil in order to flourish.\nStatement 2: A basil plant needs sun, water and soil in order to flourish.",
  "question": "Of the statements given: Statement 1, does it go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qea64700d59",
  "kind": "yes/no",
  "text": "Assistant: Sorry, but the only 3D showing is at 5:30 pm\nCustomer: That won't work for us. Can you book me the regualar movie at 8pm?\nAssistant: There is no 8pm show. There is a 7pm or 830pm showing",
  "question": "Pursuant to the assistant's final message, is \"8pm\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q17426e48f6",
  "kind": "yes/no",
  "text": "Assistant: What time?\nCustomer: 3pm today.\nAssistant: Okay, there are not two tickets available to see Shazam! at 3:00 at the Cinemark Sugarhouse today. Would you like a different time?",
  "question": "Does the assistant's final message confirm \"3:00\" for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbd9faef1b7",
  "kind": "yes/no",
  "text": "Occupation: Chemical Equipment Operators and Tenders\nDuties:\n- Examine drawings, negatives, or photographic prints to determine coloring, shading, accenting, or other changes required for retouching or restoration.\n- Splice broken or separated film and mount film on reels.\n- Produce timed prints with separate densities or color settings for each scene of a production.",
  "question": "Are the listed duties part of the above-named occupation's job?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q8e6340716b",
  "kind": "yes/no",
  "text": "In terms of greenhouse gases it emits half what coal does, per KWh generated. Unlike oil, or even coal, the worlds gas reserves are expanding dramatically. The coming decades could be a golden age for natural gas, as the International Energy Agency explored in a recent report by this title. However, it is doubtful that Europe will share in this new gas era.",
  "question": "For this paragraph, does it make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qabea10160b",
  "kind": "yes/no",
  "text": "Customer: Are there any swedish places?\nAssistant: I'm sorry. I didn't find any matches.",
  "question": "Did the assistant, in its reply, find for the customer at least a single option meeting everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q53626104b5",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nConclusion and Relevance: Among patients with severe or life-threatening COVID-19, convalescent plasma therapy added to standard treatment, compared with standard treatment alone, did not result in a statistically significant improvement in time to clinical improvement within 28 days.\n\nClaim: COVID-19 patients treated with convalescent plasma recover at faster rates than those without treatment.",
  "question": "Is the claim contradicted by the evidence?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q21846cd9d1",
  "kind": "yes/no",
  "text": "Assistant: So you would like to order a large, thin crust pizza with pepperoni and sausage from Lou Malnatti's?\nCustomer: That's correct.\nAssistant: Your frequent-pizza account at Lou Malnatti's is informing me that the price of this pizza will be discounted 20% because you have ordered 10 pizzas this quarter.",
  "question": "Is \"Lou Malnatti's\" confirmed for the customer's pizza order, as the assistant's final message says?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1cf5eaa9e9",
  "kind": "yes/no",
  "text": "Complaint narrative: PULLING DOWN MY DRIVE WAY MY VEHICLE ACCELERATED WITHOUT ME TRYING. I HIT THE BRAKE AND E BRAKE. IT DID NOT STOP US. IN RESULT OF THE ACCELERATION MY HOUSE STOPPED US.",
  "question": "Has this vehicle safety complaint reported that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qed3bc37486",
  "kind": "yes/no",
  "text": "Occupation: News Analysts, Reporters, and Journalists\nDuties:\n- Confer with clients, editors, publishers, or producers to discuss changes or revisions to written material.\n- Write words to fit musical compositions, including lyrics for operas, musical plays, and choral works.\n- Write humorous material for publication, or for performances such as comedy routines, gags, and comedy shows.",
  "question": "Is it the case that the listed duties aren't part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "qa6211fd1da",
  "kind": "yes/no",
  "text": "Complaint narrative: THIS BRAKE PROBLEMS HAS OCCURRED MANY TIMES. DURING APPLICATION OF THE BRAKES AT LOW SPEEDS ON ROUGH ROAD SURFACES THE CAR SUDDENLY LOSES BRAKING POWER FOR A BRIEF TIME THEN STARTS TO WORK AGAIN IF THE BRAKE PEDAL REMAINS DEPRESSED. THIS HAS ALMOST CAUSED ACCIDENTS A NUMBER OF TIMES AND IS QUITE FRIGHTENING. THE CAR WAS BROUGHT IN FOR THE RECALL AND SAFERCAR.GOV STATES THAT THERE ARE NO OPEN RECALLS. WHEN WE BRING THIS TO THE ATTENTION OF THE TOYOTA DEALER WE ARE TOLD THIS PROBLEM IS \"NORMAL\" AND THERE IS NOTHING MORE THEY CAN DO. (HOWEVER, I UNDERSTAND THAT THEY FIXED IT IN THE NEXT MODEL YEAR.) IN MY OPINION THIS IS AN UNSAFE CONDITION AND IT HAS BEEN COMPLAINED ABOUT ONLINE BY OTHER PRIUS OWNERS. I ASK THE NHTSA TO REQUIRE TOYOTA TO FIX THIS IN THE NAME OF SAFETY.",
  "question": "Does this vehicle safety complaint state that the vehicle actually began to burn?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q68fddb6cd5",
  "kind": "yes/no",
  "text": "Customer: I'm looking for an expensive polynesian place.\nAssistant: I'm sorry, there is nothing that I can find like that.  Do you have anything else I can look for?",
  "question": "Did the assistant find at least a single option in its reply that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q062aa67acd",
  "kind": "yes/no",
  "text": "Assistant: ok and the type of crust?\nCustomer: Gluten free cast.\nAssistant: so your order is: 2 medium chicken bbq pizzas with gluten free crust.",
  "question": "Is \"chicken bbq pizzas\" confirmed for the customer's pizza order according to the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q95386524ed",
  "kind": "yes/no",
  "text": "Assistant: Looks like 8:30 PM works as well! Did you want me to book this?\nCustomer: Yes, please!\nAssistant: Okay! 8:30 PM is booked!",
  "question": "Going by the assistant's latest message, is \"8:30 PM\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
