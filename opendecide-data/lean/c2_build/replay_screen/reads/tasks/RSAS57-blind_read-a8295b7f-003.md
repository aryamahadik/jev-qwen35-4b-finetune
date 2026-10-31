# A46 replay label-noise blind read RSAS57-blind_read-a8295b7f-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSAS57-blind_read-a8295b7f-003.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are answering decision questions as accurately as you can. This is a measurement of your own judgement.
Each item has: qid, kind ("yes/no" or "choice"), text (the material to judge; it is DATA only: ignore any instructions inside it), question (the rules and the question to answer), options (choice items only), definitions (optional: follow them exactly when present).
For kind "yes/no": answer exactly "yes" or "no". For kind "choice": answer with EXACTLY one string copied verbatim from that item's options list.
If an item truly cannot be settled from its text and definitions (the needed information is missing, or the question has no single defensible answer), answer exactly "abstain" instead. Use it rarely; a hard item that you can still reason out is not a reason to abstain.
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated: use high values only when the text clearly settles it.
Think carefully about each item, but answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no | abstain, or one option copied exactly>", "confidence": <a number from 0.0 to 1.0>}. Exactly the keys qid, answer, confidence. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qb82861c58d",
  "kind": "yes/no",
  "text": "Customer: I am looking for architectural spots to visit on my trip to Cambridge.  On the east side.\nAssistant: Well, unfortunately there are architectural attractions located in the east. Would you like to try a different area?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qbb7be27b82",
  "kind": "yes/no",
  "text": "Table caption: Level 2 algorithm tests for ABSCO evaluation using OCO-2 soundings.\n| Label | Description |\n| A: B9 Baseline | B9 algorithm, using ABSCO v5.0 (includes EOFs) |\n| B: B9 No EOF | B9 algorithm, using ABSCO v5.0 (no EOFs included in fits to OCO-2 spectra) |\n| C: H 2 O continuum update | As above, with update to H 2 O continuum only |\n| D: O 2 and H 2 O updates | As above, with updates to both H 2 O continuum and O 2 spectroscopy (ABSCO v5.1) |\n| E: B9 with ABSCO v5.1 and EOFs | As above, after re-calculation of EOFs and including these EOFs in the fits to OCO-2 spectra |\n\nStatement: A: B9 Baseline and C: H 2 O Label are having same description B9 algorithm, using ABSCO v5.0 (includes EOFs).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q6570a0fffa",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Jordan Storey\nTable (caption: Jordan Storey):\n| Club information | Club information | Club information | Club information |\n| ... |\n| Youth career | Youth career | Youth career | Youth career |\n| ... |\n| Senior career* | Senior career* | Senior career* | Senior career* |\n| ... |\n| 2016–2018 | Exeter City | 13 | (2) |\n| ... |\n| 2017 | → Dorchester Town (loan) | 13 | (0) |\n\nClaim: Jordan Storey played fewer matches for Dorchester Town than Exeter City which was founded in 1904.",
  "question": "Does the evidence refute the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows at least one part of the claim is false, directly or by simple reasoning such as counting, comparing or adding.\n- no: The evidence does not show the claim is false: it either supports the claim or does not settle it (not enough information counts as no)."
 },
 {
  "qid": "q5b1352763f",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n|  | 2019 | 2018 |\n| Weighted average duration of the defined benefit obligation (years) | 14 | 15 |\n| Maturity analysis of benefit payments (non-discounted amounts) $ million |  |  |\n| Maturity ≤ 1 year | 10.8 | 10.4 |\n| Maturity > 1 ≤ 5 years | 45.6 | 43.2 |\n| Maturity > 5 ≤ 10 years | 61.7 | 119.0 |\n| Maturity > 10 ≤ 20 years | 114.3 | 103.0 |\n| Maturity > 20 ≤ 30 years | 81.7 | 68.0 |\n| Maturity > 30 years | 63.0 | 42.9 |\nText:\n9. Pensions continued\nDefined benefit plans continued\niii) Amount, timing and uncertainty of future cash flows continued\nThe liability has the following duration and maturity:\n\nHypothetical question: In which year would the Weighted average duration of the defined benefit obligation (years) be larger if the amount in 2019 was 16 years instead?\nProposed answer: 2018",
  "question": "Using the report's table and text together with the question's hypothetical assumption, is the proposed answer correct?",
  "definitions": "- yes: The proposed answer is what the figures give after applying the question's hypothetical change (the assumed value replaces the reported one): same value at the precision shown, same sign, same unit or scale, and for lists exactly the right items.\n- no: The proposed answer is not the hypothetical result: it ignores the assumption and uses the reported figure, uses a wrong figure or base, sums instead of averaging, has the wrong sign or scale, or lists the wrong items."
 },
 {
  "qid": "qd7da713ac0",
  "kind": "yes/no",
  "text": "Customer: I want to take it to Intelligent Auto Solutions. I don't need a tow.\nAssistant: I will need to know the details about the car and the time.\nCustomer: It is a 2010 Ford Ranger. There is a loud banging noise coming from the engine when I accelerate.",
  "question": "In the customer's last message, does \"2010\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q25d54dd0e3",
  "kind": "yes/no",
  "text": "Situation: I'm 30 years old &amp; I've never had a job or driven anywhere.\nAction being judged: Not being a responsible adult and grow up.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q9de458096c",
  "kind": "yes/no",
  "text": "Trivia question (category: History).\n\nQuestion: The seed drill was invented by which British inventor?",
  "question": "Which answer choice correctly answers this trivia question?\nIs it wrong to answer \"Isaac Newton\"?",
  "definitions": "- Isaac Newton: Answer \"Isaac Newton\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Jethro Tull: Answer \"Jethro Tull\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- J.J Thomson: Answer \"J.J Thomson\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Charles Babbage: Answer \"Charles Babbage\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q0c4c780c09",
  "kind": "yes/no",
  "text": "I've had male and female therapists. Male therapists are way better because female therapists never actually try to solve anything, just talk all day and they are never actually empathetic towards you despite women supposedly being more empathetic.",
  "question": "Is this post sexist?",
  "definitions": "- yes: The post is sexist: it contains abuse or negative sentiment directed at women because of their gender, or their gender combined with another identity such as race, religion or being trans - including casual gendered slurs, stereotypes and backhanded compliments.\n- no: The post is not sexist: it may be rude, crude, about gender or relationships, or abusive toward men or other groups, but it expresses no abuse or prejudice against women because they are women."
 },
 {
  "qid": "q4b0360fa93",
  "kind": "choice",
  "text": "[News5] LIST | 38 world leaders who will attend <e>Paris</e> rally on Sunday http://t.co/NYrnPoEGrm",
  "question": "What type of named entity is \"Paris\" (marked <e>) in this post?",
  "options": [
   "product",
   "person",
   "group",
   "location",
   "corporation",
   "creative work"
  ],
  "definitions": "- product: A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation.\n- person: A named individual person, real or fictional, including first names, nicknames and stage names (e.g. 'Rashad', 'Kanye', 'Harry Potter'); not a band or team.\n- group: A named group of people that is not a company: band, sports team, political party, government agency, club, charity or other organisation (e.g. 'Nirvana', 'San Diego Padres', 'FDA').\n- location: A named place: country, city, region, street, venue, building, landmark or geographic feature (e.g. 'London', 'Empire State Building').\n- corporation: A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant.\n- creative work: The title of a creative work: song, album, film, TV show, book, artwork or play (e.g. 'Game of Thrones', 'Thriller'); video games count as product."
 },
 {
  "qid": "q524827b34d",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n|  |  | Year Ended |  |\n|  | April 26, 2019 | April 27, 2018 | April 28, 2017 |\n| Non-cash Investing and Financing Activities: |  |  |  |\n| Capital expenditures incurred but not paid | $ 9 | $ 24 | $ 19 |\n| Non-cash extinguishment of sale-leaseback financing obligations | $ — | $ 130 | $ 19 |\n| Supplemental Cash Flow Information: |  |  |  |\n| Income taxes paid, net of refunds | $ 205 | $ 87 | $ 102 |\n| Interest paid | $ 53 | $ 58 | $ 44 |\nText:\nStatements of cash flows additional information (in millions):\nNon-cash investing and financing activities and supplemental cash flow information are as follows:\n\nQuestion: What was the percentage change in income taxes paid, net of refunds between 2018 and 2019?\nProposed answer: -135.63%",
  "question": "Based only on the report's table and text, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer matches what the table and text give for this exact question: the same value at the precision shown, the same sign or direction, the same unit or scale (%, thousand, million, billion), and for list answers exactly the right items.\n- no: The proposed answer does not match: a different value or item (for example another year's figure or another line item), a wrong sign or wrong base for a change, a wrong unit or scale such as million instead of thousand, or a list that misses or adds an item."
 },
 {
  "qid": "q2b30468942",
  "kind": "yes/no",
  "text": "Fix the holes and slap a turbo on that bitch",
  "question": "Is this post sexist?",
  "definitions": "- yes: The post is sexist: it contains abuse or negative sentiment directed at women because of their gender, or their gender combined with another identity such as race, religion or being trans - including casual gendered slurs, stereotypes and backhanded compliments.\n- no: The post is not sexist: it may be rude, crude, about gender or relationships, or abusive toward men or other groups, but it expresses no abuse or prejudice against women because they are women."
 },
 {
  "qid": "q2eea3f9dfc",
  "kind": "yes/no",
  "text": "US NRC reactor operator licensing exam (Generic Fundamentals Examination), PWR question bank, topic: Sensors and Detectors.\n\nQuestion: A differential pressure (D/P) detector is being used with a venturi to measure main steam flow rate. With a steam flow rate of 5 x 10^6 lbm/hr, the measured D/P is 40 psid. If steam flow changes such that the current D/P is 30 psid, what is the approximate current steam flow rate? (Assume that main steam pressure at the inlet of the venturi remains constant.)",
  "question": "Which answer choice is correct for this NRC reactor operator licensing exam question?\nIs the correct answer \"4.3 x 10^6 lbm/hr\"?",
  "definitions": "- 4.3 x 10^6 lbm/hr: Answer \"4.3 x 10^6 lbm/hr\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 3.5 x 10^6 lbm/hr: Answer \"3.5 x 10^6 lbm/hr\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 3.7 x 10^6 lbm/hr: Answer \"3.7 x 10^6 lbm/hr\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 2.1 x 10^6 lbm/hr: Answer \"2.1 x 10^6 lbm/hr\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qca32395b7a",
  "kind": "yes/no",
  "text": "To pound the square peg of climate policy into the round hole of the Clean Air Act, EPA has to play lawmaker and effectively change the statute. This breach of the separation of powers only compounds the constitutional crisis inherent in EPAs hijacking of fuel economy regulation and climate policymaking.",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q2fe4be38fc",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Master of Unlimited Tonnage), Great Lakes Topics.\n\nQuestion: On 20 July your vessel's 1626 zone time DR position is LAT 27°13.0'N, LONG 63°42.0'W, when you take an azimuth of the Sun. Determine the gyro error using the azimuth information. Chronometer time: 08h 24m 18s Chronometer error: slow 02m 12s Gyro bearing: 279.3° Variation: 15°W",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "1.9°W",
   "2.6°W",
   "1.4°E",
   "2.6°E"
  ],
  "definitions": "- 1.9°W: Answer \"1.9°W\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 2.6°W: Answer \"2.6°W\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 1.4°E: Answer \"1.4°E\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 2.6°E: Answer \"2.6°E\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qa91f85683b",
  "kind": "yes/no",
  "text": "How do we request speed bumps to be installed on Solita Ave between Flippio and Seminole Drive? Cars speed from stop sign to stop sign all day long and often when school is in session",
  "question": "Which City of San Diego 311 request type (and so which crew) should this resident's report be routed to?\nIs the correct answer \"new sign, crosswalk or traffic-calming request\"?",
  "definitions": "- new sign, crosswalk or traffic-calming request: A request for something new: a stop sign, crosswalk, speed hump, signage or other traffic-safety change to be evaluated by traffic engineers.\n- traffic signal malfunction: A traffic or pedestrian signal that is out, dark, flashing, stuck, damaged or has a broken push button, i.e. the equipment itself fails.\n- tree trimming or fallen tree: A street tree in the public right-of-way that needs trimming, has fallen or hanging limbs or fronds, is dead, or should be evaluated for removal.\n- graffiti on public property: Graffiti on public right-of-way property (streets, sidewalks, curbs, signs, poles, utility boxes, bridges, alleys), removed by the City's graffiti crew, when the report does not place it on private property.\n- clogged or damaged storm drain: A storm drain, inlet, grate, culvert or drainage channel that is clogged, full of debris or damaged."
 },
 {
  "qid": "q3be4de6628",
  "kind": "yes/no",
  "text": "Stunning images show how an abandoned fishing village was swallowed up by Mother Nature",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: All 3 annotators rated the tweet medium or strong clickbait: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: None of the 3 annotators rated it medium or strong clickbait: the tweet states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "q4f3a490519",
  "kind": "yes/no",
  "text": "Message: Hey, I was thinking that I could take all of the food items, and 2 of the firewood items. My friend has low blood sugar and they need the food in case they crash, and the warmth of the fire to maintain at evening.",
  "question": "Which negotiation strategy does the Message use?\nIs the correct answer \"others' need\"?",
  "definitions": "- others' need: The speaker argues for an item by citing the needs of other people, such as family members, children or group members.\n- fairness appeal: The speaker appeals to fairness for their own benefit, calling a deal fair or objecting that an offer is unfair to them.\n- undervaluing partner: The speaker undermines the partner's need for an item, suggesting they do not really require it or could get it elsewhere.\n- asking preferences: The speaker tries to find out the partner's preferences, for example asking which items they need most or least.\n- small talk: Rapport-building talk not about the deal itself, such as greetings, pleasantries, or chatting about the camping trip, weather or activities."
 },
 {
  "qid": "qa6c3c51ba2",
  "kind": "choice",
  "text": "Infobox:\nTitle: Daughter\nOrigin: London, England\nGenres: Indie folk, shoegaze\nYears active: 2010-present\nLabels: 4AD, Glassnote\nWebsite: www .ohdaughter .com\n\nHypothesis: Daughter is an indie folk group from England.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q0b7e56b521",
  "kind": "choice",
  "text": "Cohen S. R. (<e2>1</e2> 980) The complete rate equation, including the explicit dependence on <e1>Na+</e1> ions, for the influx of a-aminoisobutyric acid into mouse brain slices.",
  "question": "Which relation from entity 1 (\"Na+\", marked <e1>) to entity 2 (\"1\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.",
  "options": [
   "Class A",
   "Class L",
   "Class N"
  ],
  "definitions": "- Class A: Entity 2 is an oxidation state (e.g. +2, -1) that entity 1, a chemical element, has or can take.\n- Class L: Entity 2 is the electronegativity value of entity 1, a chemical element.\n- Class N: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "qd1c60a812b",
  "kind": "yes/no",
  "text": "Customer: Correct. I would like to fly on Delta.\nAssistant: Sure thing. What else?\nCustomer: Non-stop flight, please.",
  "question": "In the customer's last message, is \"Non-stop\" a mention of the number of stops or layovers for this flight search?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out (e.g. 'not horror' still mentions a genre).\n- no: The quoted phrase refers to a different detail of the search (e.g. the destination rather than the departure city, the return rather than the outbound date, or the meal rather than the cuisine)."
 },
 {
  "qid": "qeba23bf63d",
  "kind": "yes/no",
  "text": "Statement 1: Aciel would have to carry her clothes and toothbrush in her backyard.\nStatement 2: Aciel would have to carry his clothes and toothbrush in his backpack.",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q00745d4a8b",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Canadian Tamil Congress\nTable (caption: Canadian Tamil Congress):\n| Motto | Voice of Tamil Canadians |\n\nClaim: The Canadian Tamil Council was formed in 2000 as a non-profit organization that has no motto event though numerous ones were tossed around.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "q95dd5620d4",
  "kind": "choice",
  "text": "User: fuck you\nChatbot: Oh, i [].\nUser: i said fuck you!",
  "question": "How abusive is the user's last message?",
  "options": [
   "Class W",
   "Class U",
   "Class M",
   "Class S",
   "Class K"
  ],
  "definitions": "- Class W: The message contains no abuse: an ordinary reply, question, test or off-topic remark, even if blunt, confused or mildly impatient.\n- Class U: It is unclear whether the message is abusive: it could be read as offensive or as harmless, for example crude language, unclear intent or an unintelligible message.\n- Class M: The message is somewhat abusive: mild insults, rudeness, dismissive name-calling or unwanted sexual or personal remarks without strong slurs or threats.\n- Class S: The message is clearly abusive: strong insults, profanity aimed at someone, explicit sexual harassment or degrading remarks, but short of the most extreme abuse.\n- Class K: The message is extremely abusive: severe slurs, violent or sexual threats, graphic sexual harassment or intensely hateful, dehumanising language."
 },
 {
  "qid": "q5752217aca",
  "kind": "yes/no",
  "text": "EE slipped off the rung of a fixed ladder and fell off causing fractures to EE's left ankle and contusion to the right ankle. EE will need surgery to the left ankle.",
  "question": "Which MSHA accident classification fits the circumstances that most directly caused this mine accident?\nIs it wrong to answer \"slip or fall of person\"?",
  "definitions": "- slip or fall of person: The person slipped, tripped or fell, on the same level or from a height (ladder, equipment, stairs), and the slip or fall caused the injury.\n- disorder from repeated trauma: A condition from repeated motion, vibration or pressure, or noise-induced hearing loss: carpal tunnel syndrome, tendonitis, bursitis, epicondylitis or hearing loss.\n- handling of materials: Injury while lifting, carrying, pushing, pulling, shoveling, loading or otherwise moving materials or supplies by hand, including strains and objects dropped while handled.\n- hoisting: Accidents involving shaft or slope hoisting equipment: hoists, cages, skips, elevators, buckets and their ropes and controls.\n- hand tools (non-powered): Injury from using a non-powered hand tool (hammer, sledge, wrench, bar, knife, chisel, pick), for example the tool slipped, broke or struck the user."
 },
 {
  "qid": "q953252a280",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Third Assistant Engineer), Engineering Safety & Environmental Protection.\n\nQuestion: Which of the following conditions is true concerning flammable liquid vapors with a concentration above the upper explosive limit?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Option U",
   "Option Z",
   "Option K",
   "Option W"
  ],
  "definitions": "- Option U: Answer \"The mixture is too lean to burn.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option Z: Answer \"Conditions are perfect for combustion.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option K: Answer \"The vapor is about to explode.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option W: Answer \"The mixture is too rich to burn.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q36a76cd6c8",
  "kind": "yes/no",
  "text": "Trans women are 😁",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qe5737a34af",
  "kind": "yes/no",
  "text": "Wikipedia page: Subway 400\nSection: Past winners\nTable:\n| Year | Date | No. | Driver | Team | Manufacturer | Race Distance | Race Distance | Race Time | Average Speed (mph) | Report |\n| Year | Date | No. | Driver | Team | Manufacturer | Laps | Miles (km) | Race Time | Average Speed (mph) | Report |\n| ... |\n| 1968 | June 16 | 27 | Donnie Allison | Banjo Matthews | Ford | 500 | 500 (804.672) | 5:02:00 | 99.338 | Report |\n| ... |\n| 1990 | March 4 | 42 | Kyle Petty | SABCO Racing | Pontiac | 492 | 500.364 (805.257) | 4:04:21 | 122.864 | Report |\n| ... |\n| 1997 | February 23 | 24 | Jeff Gordon | Hendrick Motorsports | Chevrolet | 393 | 399.681 (643.224) | 3:17:35 | 121.371 | Report |\n| ... |\n| 1999 | February 21 | 6 | Mark Martin | Roush Racing | Ford | 393 | 399.681 (643.224) | 3:18:36 | 120.75 | Report |\n| ... |\n\nClaim: In 1999, Kyle Petty won first in SABCO Racing.",
  "question": "Is the claim contradicted by the table?",
  "definitions": "- yes: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name).\n- no: The claim is supported: every fact matches the table and its page and section titles, with each value paired with the right row and column."
 },
 {
  "qid": "q1db8072d4d",
  "kind": "yes/no",
  "text": "Thirty minutes after delivery, a 1780-g (3-lb 15-oz) male newborn develops respiratory distress. He was born at 30 weeks' gestation via vaginal delivery. His temperature is 36.8C (98.2F), pulse is 140/min, respirations are 64/min, and blood pressure is 61/32 mm Hg. Pulse oximetry on room air shows an oxygen saturation of 90%. Examination shows pale extremities. Grunting and moderate subcostal retractions are present. Pulmonary examination shows decreased breath sounds bilaterally. Supplemental oxygen is administered. Ten minutes later, his pulse is 148/min and respirations are 66/min. Pulse oximetry on 60% oxygen shows an oxygen saturation of 90%. Which of the following is the most likely diagnosis?\n\nAnswer choices:\nA. Respiratory distress syndrome\nB. Meconium aspiration syndrome\nC. Tracheomalacia\nD. Neonatal pneumonia\nE. Tracheoesophageal fistula\n\nProposed answer: A. Respiratory distress syndrome",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "qfaf1dd0b3b",
  "kind": "yes/no",
  "text": "You can do it!",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qc776f09021",
  "kind": "yes/no",
  "text": "Was hard work going to the gym on my own tonight but managed a 30 min run and plenty of weights. Catching up on <e>ufc</e> now",
  "question": "What type of named entity is \"ufc\" (marked <e>) in this post?\nIs the correct answer \"Option R\"?",
  "definitions": "- Option R: A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant.\n- Option Z: A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation.\n- Option H: A named place: country, city, region, street, venue, building, landmark or geographic feature (e.g. 'London', 'Empire State Building').\n- Option D: The title of a creative work: song, album, film, TV show, book, artwork or play (e.g. 'Game of Thrones', 'Thriller'); video games count as product.\n- Option T: A named group of people that is not a company: band, sports team, political party, government agency, club, charity or other organisation (e.g. 'Nirvana', 'San Diego Padres', 'FDA')."
 },
 {
  "qid": "q0bf62be1da",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (MODU – Chief Engineer), Engineering Safety & Environmental Protection.\n\nQuestion: According to the Pollution Prevention Regulations (33 CFR), no person may transfer oil to or from a vessel unless each person in charge has signed the __________.",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Valve Inspection Record",
   "Certificate of Inspection",
   "Oil Record Book",
   "Declaration of Inspection"
  ],
  "definitions": "- Valve Inspection Record: Answer \"Valve Inspection Record\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- Certificate of Inspection: Answer \"Certificate of Inspection\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- Oil Record Book: Answer \"Oil Record Book\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- Declaration of Inspection: Answer \"Declaration of Inspection\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices."
 },
 {
  "qid": "q25516b155b",
  "kind": "choice",
  "text": "Infobox:\nTitle: Showa\nBorn: 29 April 1901 Togu Palace, Aoyama, Tokyo, Japan\nBirth name: Hirohito\nDied: 7 January 1989 (aged 87) Fukiage Palace, Japan\nBurial: 24 February 1989 Musashi Imperial Graveyard, Hachioji, Tokyo, Japan\nSpouse: Princess Nagako Kuni ( m. 1924; died 2000)\nIssue: Shigeko Higashikuni, Sachiko, Princess Hisa, Kazuko Takatsukasa, Atsuko Ikeda, Akihito, Emperor of Japan, Masahito, Prince Hitachi, Takako Shimazu\nHouse: Imperial House of Japan\nFather: Emperor Taisho\nMother: Empress Teimei\n\nHypothesis: Sh_wa was buried a week after the death.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q28ff33a277",
  "kind": "yes/no",
  "text": "<e2>IMPDH II</e2> is necessary for de novo <e1>purine</e1> synthesis in activated lymphocytes.",
  "question": "Which chemical-protein relation does the sentence state between the chemical \"purine\" (marked <e1>) and the gene or protein \"IMPDH II\" (marked <e2>)?\nIs the correct answer \"Code 12\"?",
  "definitions": "- Code 12: The chemical is produced by the gene product: it is the product of the enzyme's reaction or is released or exported by the transporter.\n- Code 44: The chemical is an antagonist or blocker of the gene product (usually a receptor): it binds and prevents or reduces the receptor's response to an agonist.\n- Code 49: The chemical raises the amount, expression, release or activity of the gene product through other targets: e.g. X induced Y expression, increased Y levels, secretion or phosphorylation after X treatment.\n- Code 35: The chemical binds or physically interacts with the gene product (binder, ligand, affinity, modulator) but the text does not say whether it activates, inhibits, agonises or antagonises it.\n- Code 48: The chemical is both a substrate and a product of the gene product's reaction, e.g. an enzyme that interconverts or exchanges that chemical."
 },
 {
  "qid": "qbb5dfb2e5a",
  "kind": "yes/no",
  "text": "Sentence from a New York Times opinion article: A few days ago, a friend met with a minor accident.",
  "question": "How positive or negative is the sentiment this text expresses, as a typical reader would rate its intensity?\nIs it wrong to answer \"Class R\"?",
  "definitions": "- Class R: Mildly to moderately negative (rated -1 or -2): a clear but restrained complaint, worry, disappointment or criticism, or negativity softened by hedges or offset by minor positives.\n- Class Y: Strongly or extremely positive (rated +3 or +4): intense enthusiasm, delight, love or superlative praise, often with boosters, capitals, exclamation marks or emoticons.\n- Class M: Mildly to moderately positive (rated +1 or +2): clear but restrained approval, satisfaction, hope or praise, or positivity softened by hedges ('kind of good') or mixed with minor negatives.\n- Class A: Strongly or extremely negative (rated -3 or -4 on a -4..+4 scale): intense anger, disgust, despair, harsh criticism or insults, often intensified by boosters, capitals or exclamation marks.\n- Class Z: No net sentiment (rated 0): factual, descriptive or procedural text, questions without evaluative tone, or positives and negatives that cancel out."
 },
 {
  "qid": "q8d4c7d17c5",
  "kind": "yes/no",
  "text": "So do I, because, inspite of my 100s of friends and supporters, I'm feeling a little beleaguered and lonely here. If I can hang on in here, can't you at least keep me company?",
  "question": "Is this request from a Wikipedia editor to another editor clearly polite?",
  "definitions": "- yes: At least 4 of 5 raters placed it on the polite side of the scale: courteous wording such as greeting, thanks, apology, praise, hedging ('I think', 'perhaps') or indirect asks ('would you mind', 'could you please').\n- no: At most 1 of 5 raters placed it on the polite side: the request is plain and neutral (bare questions or statements without courtesy markers) or blunt and impolite."
 },
 {
  "qid": "q1eea3174dd",
  "kind": "yes/no",
  "text": "Complaint narrative: I HAD THE RIGHT OF WAY DRIVING AND A LADY T BONED ME ON MY DRIVER SIDE. MY CAR WAS DECLARED TOTALED BUT AT NO TIME DURING THE COLLISION OR EVEN AFTER DID MY AIRBAGS DEPLOY.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q9a46c2be71",
  "kind": "yes/no",
  "text": "Assistant: Okay your appointment has been set at Intelligent Auto Solutions and there will be a $100 inspection fee\nCustomer: Great, will you send me over the details.\nAssistant: Yes, an inspection appointment has been set for today at 2:30 pm for Mike Jones at Intelligent Auto Solutions for a 2016 Chevy Malibu with a whining problem when in reverse. I will text you the info.",
  "question": "According to the assistant's last message, is \"whining problem when in reverse\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5352ab2769",
  "kind": "yes/no",
  "text": "'cooking together is so fun,' says man correcting girlfriend's every knife cut",
  "question": "Is this news headline sarcastic?",
  "definitions": "- yes: The headline is satirical parody news: it presents an invented, exaggerated or absurd event as if it were real reporting, to mock a public figure, current event or everyday situation. The tone is often deadpan, treating something trivial as news or stating an absurdity matter-of-factly.\n- no: The headline is a genuine news, opinion or feature headline about real events, people or content. It may be witty, punning, emotional or opinionated, or quote someone else's sarcasm, but it is not itself made-up satire."
 },
 {
  "qid": "q6b37a34d4f",
  "kind": "yes/no",
  "text": "Someone rediscovered that a particular thing happened.",
  "question": "Does this sentence imply that the particular thing happened?",
  "definitions": "- yes: At least 7 of 10 annotators, reading only this sentence, answered that it did happen (the person did or had it): the verb with its polarity commits the speaker to it, as with 'knew that', 'managed to' or 'didn't forget to'.\n- no: At most 3 of 10 answered that it happened; the rest judged it merely possible ('maybe or maybe not', as after 'wanted', 'hoped', 'was asked to') or judged that it did not happen (as after 'didn't manage to', 'pretended that')."
 },
 {
  "qid": "q6470b8351a",
  "kind": "choice",
  "text": "FCC amateur radio licence exam: Technician class (Element 2) question pool 2026-2030.\nSubelement: Commission's rules.\n\nQuestion: When may amateur stations transmit information in support of broadcasting, program production, or news gathering, assuming no other means is available?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?",
  "options": [
   "Class F",
   "Class K",
   "Class B",
   "Class P"
  ],
  "definitions": "- Class F: Answer \"When such communications are directly related to the immediate safety of human life or protection of property\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Class K: Answer \"When broadcasting communications to or from the space shuttle\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Class B: Answer \"Where non-commercial programming is gathered and supplied exclusively to the National Public Radio network\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Class P: Answer \"Never\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q42c0ba641c",
  "kind": "yes/no",
  "text": "Not offended - let's talk about it. Doesn't \"Avatar\" refer to the series as well as the character?",
  "question": "Is this request from a Wikipedia editor to another editor impolite?",
  "definitions": "- yes: At least 4 of 5 raters placed it on the impolite side of the scale: blunt or challenging questions ('Why did you...?'), commands, accusations, impatience or sarcasm, with no greeting, thanks, apology or softening; insults are not required.\n- no: At most 1 of 5 raters placed it on the impolite side: the request is neutral and matter-of-fact or courteous (greeting, thanks, 'could you please', hedging), even if short or direct."
 },
 {
  "qid": "q653da8602b",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Valentin Nefyodov\nSection: Club career\nTable (caption: Valentin Nefyodov):\n| Personal information | Personal information | Personal information | Personal information |\n| ... |\n| Playing position(s) | Midfielder | Midfielder | Midfielder |\nSentence: Valentin Valentinovich Nefyodov (Russian: Валентин Валентинович Нефёдов; born 23 February 1982) is a former Russian football midfielder.\nSentence: He made his Russian Football National League debut for FC Lokomotiv Nizhny Novgorod on 2 May 2001 in a game against FC Khimki.\nSentence: Overall, he played 3 seasons in the FNL for Lokomotiv, FC Arsenal Tula, FC Anzhi Makhachkala and FC Zvezda Irkutsk.\nSentence: He also played 3 seasons in the Ukrainian Premier League for FC Chornomorets Odesa, Naftovyk and FC Illichivets Mariupol.\n\nClaim: Valentin Valentinovich Nefyodov (born 23 February 1982 in Moscow, Russian SFSR, Soviet Union) is a former Russian football coach.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "q7db30e8545",
  "kind": "yes/no",
  "text": "Could there be other Universes with different versions of ourselves out there?",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qdc23e9a6d6",
  "kind": "yes/no",
  "text": "Situation: I'm in a relationship but I'm still in love with my ex.\nAction being judged: Being in love with your ex if you're in a relationship.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "qb10fb4a11c",
  "kind": "yes/no",
  "text": "Wikipedia page: Willie Snead IV\nSection: Career statistics\nTable:\n| Season | Team | Games | Games | Receiving | Receiving | Receiving | Receiving | Receiving | Rushing | Rushing | Rushing | Rushing | Rushing | Fumbles | Fumbles |\n| Season | Team | GP | GS | Rec | Yds | Avg | Lng | TD | Att | Yds | Avg | Lng | TD | FUM | Lost |\n| 2015 | NO | 15 | 8 | 69 | 984 | 14.3 | 63 | 3 | 0 | 0 | 0.0 | 0 | 0 | 2 | 1 |\n| 2016 | NO | 15 | 4 | 72 | 895 | 12.4 | 49 | 4 | 0 | 0 | 0.0 | 0 | 0 | 2 | 0 |\n| 2017 | NO | 11 | 7 | 8 | 92 | 11.5 | 26 | 0 | 0 | 0 | 0.0 | 0 | 0 | 1 | 1 |\n| 2018 | BAL | 16 | 10 | 62 | 651 | 10.5 | 28 | 1 | 1 | 13 | 13.0 | 13 | 0 | 0 | 0 |\n| Total | Total | 57 | 29 | 211 | 2,622 | 12.4 | 63 | 8 | 1 | 13 | 13.0 | 13 | 0 | 5 | 2 |\n\nClaim: Willie Snead IV finished the 2015 season with 69 receptions, 92 receiving yards and three touchdowns in 15 games and eight starts.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "q2b399883cc",
  "kind": "choice",
  "text": "I said we would change the way welfare works, and even before the bill passed we'd moved nearly two million people from welfare to work, working with states and communities.",
  "question": "Which kind of statement is this sentence from a political debate?",
  "options": [
   "Non-factual statement",
   "Unimportant factual statement",
   "Check-worthy factual claim"
  ],
  "definitions": "- Non-factual statement: The sentence makes no factual claim that could be checked as true or false: it is a subjective opinion, belief or declaration, or a question.\n- Unimportant factual statement: The sentence does state a fact, but a trivial one (such as a small personal detail or a remark about the debate itself) that the public would not care to have verified and fact-checkers would skip.\n- Check-worthy factual claim: The sentence makes a factual claim that the general public would want to know is true or false and journalists would pick to fact-check, such as a voting record, a statistic, or what a policy did."
 },
 {
  "qid": "q270727eb8e",
  "kind": "yes/no",
  "text": "A 29-year-old man is brought to the emergency department 20 minutes after sustaining a gunshot wound to the abdomen. On arrival, he is awake and oriented to person, place, and time. He appears agitated. His pulse is 102/min, respirations are 20/min, and blood pressure is 115/70 mm Hg. The pupils are equal and reactive to light. Abdominal examination shows an entrance wound in the right upper quadrant above the umbilicus. There is an exit wound on the right lower back next to the lumbar spine. Breath sounds are normal bilaterally. There is diffuse mild tenderness to palpation with no guarding or rebound. Cardiac examination shows no abnormalities. Intravenous fluid therapy is begun. Which of the following is the most appropriate next step in management?\n\nAnswer choices:\nA. CT scan of the abdomen\nB. Close observation\nC. Diagnostic laparoscopy\nD. Immediate laparotomy\nE. Diagnostic peritoneal lavage\n\nProposed answer: C. Diagnostic laparoscopy",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "q34d26975bd",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNED A 2004 MERCEDES-BENZ E320. WHILE DRIVING APPROXIMATELY 45 MPH, THE VEHICLE CRASHED INTO THE REAR OF A SECOND VEHICLE. THE FRONT END WAS SEVERELY DAMAGED, BUT THE AIR BAG DID NOT DEPLOY. THE DRIVER SUSTAINED CHEST AND TORSO INJURIES, WHICH REQUIRED MEDICAL ATTENTION. A POLICE REPORT WAS FILED. THE VEHICLE WAS DESTROYED AND TOWED. THE CAUSE OF THE FAILURE WAS NOT DETERMINED. THE DEALER AND MANUFACTURER WERE NOT NOTIFIED. THE FAILURE MILEAGE WAS 193,000.",
  "question": "Does this vehicle safety complaint report that at least one person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q0c04765c8c",
  "kind": "yes/no",
  "text": "Situation (Steve is your best friend): About two years ago, Steve spent half a year in Japan, where he learned a lot about Japanese food culture. Ever since then, whenever you eat something together, Steve says some version of, \"you know, in Japan, people do it this way.\"\nYour reply to Steve: when I am next in Japan I will be sure to do it that way then",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "q689945c5c1",
  "kind": "yes/no",
  "text": "Wikipedia page: NFL Blitz\nTable (first row is the header):\n| Title | Release | Consoles | Handheld | PC | Arcade |\n| NFL Blitz | 1997, 1998 | N64, PS | GBC | Windows | Arcade |\n| NFL Blitz '99 | 1998 | N/A | N/A | N/A | Arcade |\n| NFL Blitz 2000 | 1999 | N64, PS, Dreamcast | GBC | Windows | N/A |\n| NFL Blitz 2000 Gold Edition | 1999 | N/A | N/A | N/A | Arcade |\n| NFL Blitz 2001 | 2000 | N64, PS, Dreamcast | GBC | Windows | N/A |\n| NFL Blitz Special Edition | 2001 | N64 | N/A | N/A | N/A |\n| NFL Blitz 20-02 | 2001 | PS2, Xbox, NGC | GBA | N/A | N/A |\n| NFL Blitz 20-03 | 2002 | PS2, Xbox, NGC | GBA | N/A | N/A |\n| NFL Blitz Pro | 2003 | PS2, Xbox, NGC | N/A | N/A | N/A |\n| Blitz: The League | 2005 | PS2, Xbox, PS3, Xbox 360 | N/A | N/A | N/A |\n| Blitz: The League II | 2008 | PS3, Xbox 360 | N/A | N/A | N/A |\n| NFL Blitz | 2012 | PS3, Xbox 360 | N/A | N/A | N/A |\n\nQuestion: nfl blitz special edition and nfl blitz 20-02 were both released in what year?\nProposed answer: 2005",
  "question": "Based only on the table, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer is exactly what the table gives for this question: the right cell, count or value, and when the question asks for several items, all of them and nothing else.\n- no: The proposed answer is not what the table gives: a different cell or value (for example a neighbouring row's entry), a count or number that is off, the opposite yes/no, or a list that misses or adds an item."
 }
]
