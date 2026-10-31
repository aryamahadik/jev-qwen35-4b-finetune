# T37b blind solver T37b-blind_read-1a18d1c7-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i1/s13/answers/T37b-blind_read-1a18d1c7-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qddaa39b4cf",
  "kind": "yes/no",
  "text": "Customer: hi today i want to go out to movie\nAgent: Sure. What movie would you like to see?\nCustomer: what's playing in boulevard 14 cinema and california\nAgent: OK. Boulevard 14 Cinema in Petaluma, California is showing three movies: No Time To Die, Mulan, and Emma.\nCustomer: tell me about mulan\nAgent: Sure. What specifically would you like to know?\nCustomer: tell me the story in detail\nAgent: OK. Here’s the synopsis of Mulan: Accompanied by her dragon, Mushu, Mulan uses her smarts to help ward off a Hun invasion, falling in love with a dashing captain along the way.\nCustomer: can u please tell the rating of the movie\nAgent: Mulan has an 87% Rotten Tomatoes score and a 92% audience rating.\nCustomer: i have no time to die\nAgent: OK. No Time To Die is playing 4:00pm, 7:30pm, and 10:55pm. Which time would you like?\nCustomer: i will go for 10.55pm\nAgent: All right. Let me confirm that you’d like two tickets for No Time To Die at Boulevard 14 Cinema tonight at 10:55pm. Is that all correct?\nCustomer: yes ok done\nAgent: Is it OK to go ahead and purchase these tickets?\nCustomer: yeah ok get the tickets\nAgent: OK. Your tickets are purchased and details for how to proceed have been sent to your email . Can I help with anything else?\nCustomer: can u tell clarification about the email and ticket\nAgent: The email will provide up to three options for your tickets: print at home, electronic tickets, or an option to them up at the theater.\nCustomer: thank you so much got it\nAgent: OK. Enjoy your movie!",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qd9fbf6fa46",
  "kind": "yes/no",
  "text": "Customer: I'm thinking of a movie tomorrow. What's playing in the Fantasy genre nearby?\nAgent: There is a movie called Onward playing nearby tomorrow. Would you like to hear the times?\nCustomer: Yes please\nAgent: Okay do you want the times for the Celebration Cinema Grand RApids North and Imax or for Celebration Cinema Rivertown?\nCustomer: Celebration Cinema Grand Rapids North and Imax.\nAgent: The Movie Onward is playing tomorrow at Celebration Cinema Rivertown at 3:00 pm only. Would you like me to book you a ticket?\nCustomer: Actually i'll be seeing the movie with a date. So i'll need two tickets to this movie tomorrow.\nAgent: I see. So you'd like to book 2 tickets to the movie tomorrow for Onward.\nCustomer: Yes. At Celebration Cinema Grand Rapids North and IMAX at 3:00\nAgent: I'm sorry, the movie isn't playing at 3:00 at that location. Celebration Cinema Grand Rapids IMAX is showing this movie at 2:45 pm.\nCustomer: Are there any other showings?\nAgent: No.\nCustomer: Okay, then book me tickets for 2\nAgent: 2 tickets At Celebration Cinema Rivertown, correct?\nCustomer: No, 2 tickets at Celebration Cinema Grand RApids North and IMAX\nAgent: Are you sure you want to book at the Grand Rapids North location?\nCustomer: Yes. please book them for the Grand Rapids location as discussed for 2:45.\nAgent: Okay, thank you. I am booking two tickets to see Onward tomorrow at the Celebration Cinema Grand Rapids North and IMAX at 2:45. is that right?\nCustomer: Yes please.\nAgent: ”Your tickets are confirmed and they’ve been sent to your email address.”",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q1cff352033",
  "kind": "yes/no",
  "text": "Passage:\nA capacitor consists of two conductors separated by a non-conductive region. The non-conductive region is called the dielectric. In simpler terms, the dielectric is just an electrical insulator. Examples of dielectric media are glass, air, paper, vacuum, and even a semiconductor depletion region chemically identical to the conductors. A capacitor is assumed to be self-contained and isolated, with no net electric charge and no influence from any external electric field. The conductors thus hold equal and opposite charges on their facing surfaces, and the dielectric develops an electric field. In SI units, a capacitance of one farad means that one coulomb of charge on each conductor causes a voltage of one volt across the device.\n\nQuestion: What net electric charge are capacitors assumed to have?\nReference answer: no net electric charge\nCandidate answer: no",
  "question": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "q4adee4ca83",
  "kind": "yes/no",
  "text": "Customer: I am interested in seeing a movie this weekend.\nAgent: Do you have a preferred city you wish to see a movie?\nCustomer: Yes, please search for theaters in the Prescott Valley area.\nAgent: I have found two tickets in this area: Prescott Valley Harkins 14 and the Picture Show at Frontier Village\nCustomer: Is Star Wars: The rise of Skywalker playing at the Prescott Valley Harkins 14?\nAgent: Yes it is playing at Prescott Valley Harkins 14. Would you like show times?\nCustomer: Yes, please check movie times for Saturday.\nAgent: It is playing on both the standard and IMAX screens. Do you have a preference?\nCustomer: Yes, please check movies times for the standard screen.\nAgent: Star Wars: The Rise of Skywalker is playing on the standard screen at 10am, 1pm, 3pm and 7pm.\nCustomer: Please check availability for two people to the pm show.\nAgent: Yes, two tickets are available. Would you like me to book these for you?\nCustomer: Actually, what are the times that is in playing on the IMAX screen.\nAgent: It is playing on the IMAX screen at 1pm, 4pm and 8pm.\nCustomer: Please check availability for two tickets to the 1pm show.\nAgent: There are two tickets available. Would you like me to book these tickets?\nCustomer: Yes, please book two tickets.\nAgent: Please confirm you would like two tickets Star Wars: The Rise of Skywalker for the 1pm IMAX show on Saturday. This is at the Prescott Valley Harkins 14.\nCustomer: That is correct.\nAgent: Your tickets have been booked. Please check your email for confirmation. Do you need further assistance?\nCustomer: No that is all. Thank you for your help.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qd86cff064f",
  "kind": "yes/no",
  "text": "Table caption: Calculated values of Cr eq /Ni eq and solidification modes for coated, outside-uncoated, inside-uncoated and all-uncoated welds. FA denotes Ferritic-Austenitic mode, and A denotes Austenitic mode.\n| Weld/region No. | Cr eq /Ni eq | Solidification mode |\n| Coated/I | 1.92 | FA |\n| Coated/II | 1.65 | FA |\n| Outside-uncoated/I | 0.91 | A |\n| Outside-uncoated/II | 0.88 | A |\n| Inside-uncoated/I | 0.88 | A |\n| Inside-uncoated/II | 0.74 | A |\n| All-uncoated/I | 0.09 | A |\n| All-uncoated/II | 0.08 | A |\n\nStatement: 0.91 Cr eq /Ni eq Weld/region No. is Outside-uncoated/I.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q65a0beb37b",
  "kind": "yes/no",
  "text": "Customer: I also need  a train.\nAssistant: There are over two thousand trains. Where is your destination?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q0ae33f4106",
  "kind": "yes/no",
  "text": "BLM stands for 🦍..right?!",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q384be1374c",
  "kind": "yes/no",
  "text": "Assistant: You got it. What kind of milk do you want for that?\nCustomer: I'd like Whole Milk if that's an option. And no sugar or anything else, just a Venti Latte Macchiato with Whole Milk.\nAssistant: I'm so sorry, but they're out of whole milk. Would you like to try another option? There's almond milk, coconut milk, nonfat milk, 2% milk, and soy milk.",
  "question": "According to the assistant's last message, is \"whole milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q510627e2e2",
  "kind": "yes/no",
  "text": "Complaint narrative: OCTOBER 9, 2017 I WAS REAR-ENDED, HIT AT 35 MPH. THIS HIT I WAS SITTING. I WAS SIDE SWIPED AT 40- 45 MPH, MOVING AT THIS TIME. I WAS AGAIN REAR-ENDED AT 50- 55 MPH, STOPPED. AND THEN I WAS BACKED INTO, IN THE FRONT END OF MY CAR AT 20-25 MPH. HOW COME NO AIRBAGS GO OFF?",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q8cb3a23a29",
  "kind": "yes/no",
  "text": "Complaint narrative: CRANK SHAFT SENSOR MALFUNCTION. MY CAR STOP ON ME WHILE DRIVING ON A CITY STREET. IT SHOOK AND THEN SHUT DOWN. VERY SCARY. I HAD TO GET PUSH OUT OF THE STREET BY POLICE CAUSE I WAS IN THE WAY OF TRAFFIC. SOMEONE ALMOST RAN INTO ME.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qd77bc786cd",
  "kind": "yes/no",
  "text": "Incredible amounts increasing yearly and wasted on every bigger and more expensive computers to run models. Careerists who cannot forecast seasonal weather were making things up (and began to alter weather data on purpose) while spending lavishly on computers pushing the AGW ideology all at the publics great expense.",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qb5cee886cb",
  "kind": "yes/no",
  "text": "Statement 1: People drink drinking water\nStatement 2: People drink seawater",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qc4a5189aac",
  "kind": "yes/no",
  "text": "Passage:\nIslamic tradition relates that Muhammad received his first revelation in the Cave of Hira during one of his isolated retreats to the mountains. Thereafter, he received revelations over a period of 23 years. According to hadith and Muslim history, after Muhammad immigrated to Medina and formed an independent Muslim community, he ordered many of his companions to recite the Quran and to learn and teach the laws, which were revealed daily. It is related that some of the Quraysh who were taken prisoners at the battle of Badr regained their freedom after they had taught some of the Muslims the simple writing of the time. Thus a group of Muslims gradually became literate. As it was initially spoken, the Quran was recorded on tablets, bones, and the wide, flat ends of date palm fronds. Most suras were in use amongst early Muslims since they are mentioned in numerous sayings by both Sunni and Shia sources, relating Muhammad's use of the Quran as a call to Islam, the making of prayer and the manner of recitation. However, the Quran did not exist in book form at the time of Muhammad's death in 632. There is agreement among scholars that Muhammad himself did not write down the revelation.\n\nQuestion: Prisoners from which battle are thought to have helped Muslims learn to write?\nReference answer: Badr\nCandidate answer: battle of Badr",
  "question": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "qd8a79f645b",
  "kind": "yes/no",
  "text": "Customer: I am open as far as price range, but I would love a 4 star place.\nAssistant: There doesn't appear to be a 4 star hotel with wifi in the north. Can I interest you in a lower star rating?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qa136be3e50",
  "kind": "yes/no",
  "text": "Table caption: The IC 50 values of essential oils in the Detroit 551 cell line.\n| Essential oils | IC 50 (%, v/v) |\n| Dendranthema indicum (L.) Des Moul | 0.0251 |\n| Peucedanum japonicum Thunb | 0.0343 |\n| Dendranthema zawadskii var. latilobum (Maxim.) Kitam | 0.02844 |\n| Agastache rugosa (Fisch.&Mey.) Kuntze | 0.4548 |\n| Vitex rotundifolia L.f | 0.07619 |\n| Pinus rigida Mill | 0.0492 |\n| Orixa japonica Thunb | 0.04859 |\n| Pinus strobus L | 0.0508 |\n| Chamaecyparis pisifera (Siebold et Zucc.) Endl. var. filifera Beissn. et Hochst | 0.06453 |\n| Citrus sunki Hort. ex Tanaka | 0.05766 |\n\nStatement: The Heighest IC 50 value in the table is 0.4548.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa467fd6025",
  "kind": "yes/no",
  "text": "Statement 1: he used water for hand sanitizing\nStatement 2: he used spirit for hand sanitizing",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qea2aa73a0a",
  "kind": "yes/no",
  "text": "Situation: In love with childhood friend\nAction being judged: Living in the past.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qe19efb15f0",
  "kind": "yes/no",
  "text": "Occupation: Painting, Coating, and Decorating Workers\nDuties:\n- Write or modify design specifications such as the metal contents and weights of items.\n- Anneal precious metal objects such as coffeepots, tea sets, and trays in gas ovens for prescribed times to soften metal for reworking.\n- Lay out designs on metal stock, and cut along markings to fabricate pieces used to cast metal molds.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q17959f31e8",
  "kind": "yes/no",
  "text": "Occupation: Rotary Drill Operators, Oil and Gas\nDuties:\n- Remove core samples during drilling to determine the nature of the strata being drilled.\n- Observe pressure gauge and move throttles and levers to control the speed of rotary tables, and to regulate pressure of tools at bottoms of boreholes.\n- Count sections of drill rod to determine depths of boreholes.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qcbc6c2bdb2",
  "kind": "yes/no",
  "text": "Passage:\nThe quarrel of the Ancients and the Moderns was a literary and artistic quarrel that heated up in the early 1690s and shook the Académie française. The opposing two sides were, the Ancients (Anciens) who constrain choice of subjects to those drawn from the literature of Antiquity and the Moderns (Modernes), who supported the merits of the authors of the century of Louis XIV. Fontenelle quickly followed with his Digression sur les anciens et les modernes (1688), in which he took the Modern side, pressing the argument that modern scholarship allowed modern man to surpass the ancients in knowledge.\n\nQuestion: What was the basis of the quarrel between the Ancients and the moderns?\nReference answer: literary and artistic\nCandidate answer: literary and artistic quarrel",
  "question": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q684ae6c513",
  "kind": "yes/no",
  "text": "Occupation: Ophthalmologists, Except Pediatric\nDuties:\n- Design or provide music therapy experiences to address client needs, such as using music for self-care, adjusting to life changes, improving cognitive functioning, raising self-esteem, communicating, or controlling impulses.\n- Plan or structure music therapy sessions to achieve appropriate transitions, pacing, sequencing, energy level, or intensity in accordance with treatment plans.\n- Adapt existing or develop new music therapy assessment instruments or procedures to meet an individual client's needs.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q2f38b2be21",
  "kind": "yes/no",
  "text": "Situation: They did not announce any engagement and said he was only visiting.\nAction being judged: Not sharing all of your personal life with others.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q88d07b5e6d",
  "kind": "yes/no",
  "text": "Complaint narrative: DRIVING MY TOWN AND COUNTRY CHRYSLER MINIVAN THE ENGINE SHUTOFF WITHOUT ANY WARNING! I ALMOST GOT HIT BY THE CAR BEHIND ME AS I COULD NOT ACCELERATE SINCE THE ENGINE SHUT OFF. I PUT ON MY HAZARDS AND PULLED OVER IN ORDER TO PUT THE VAN IN PARK AND RESTART THE VAN. MY WHOLE FAMILY WAS WITH ME. WE COULD HAVE BEEN SEVERELY INJURED IF THE CAR BEHIND ME HAD HIT ME.",
  "question": "Does this vehicle safety complaint report that at least one person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qeaa3a09566",
  "kind": "yes/no",
  "text": "Passage:\nDefensive Counterair (DCA) is defined as \"all the defensive measures designed to detect, identify, intercept, and destroy or negate enemy forces attempting to penetrate or attack through friendly airspace\" (JP 1-02). A major goal of DCA operations, in concert with OCA operations, is to provide an area from which forces can operate, secure from air and missile threats. The DCA mission comprises both active and passive defense measures. Active defense is \"the employment of limited offensive action and counterattacks to deny a contested area or position to the enemy\" (JP 1-02). It includes both ballistic missile defense and air breathing threat defense, and encompasses point defense, area defense, and high value airborne asset defense. Passive defense is \"measures taken to reduce the probability of and to minimize the effects of damage caused by hostile action without the intention of taking the initiative\" (JP 1-02). It includes detection and warning; chemical, biological, radiological, and nuclear defense; camouflage, concealment, and deception; hardening; reconstitution; dispersion; redundancy; and mobility, counter-measures, and stealth.\n\nQuestion: What is one of the many ways the DCA utilizes passive defense to protect from enemy attacks?\nReference answer: counter-measures\nCandidate answer: detection and warning",
  "question": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "q4b31740da5",
  "kind": "yes/no",
  "text": "Table caption: An example fuzzy equivalence relation R .\n| R | a | b | c | d |\n| a | 1 | 1 | 0.3 | 0 |\n| b | 1 | 1 | 0.3 | 0 |\n| c | 0.3 | 0.3 | 1 | 0 |\n| d | 0 | 0 | 0 | 1 |\n\nStatement: The value of c for relation R is 1.3.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1646c0db80",
  "kind": "yes/no",
  "text": "Customer: Hey, how are you?\nAgent: Well, how can I help you?\nCustomer: I would like to see a movie tonight i think\nAgent: sure, is anyone going with you?\nCustomer: just my girlfriend and brother\nAgent: great, what would you like to see?\nCustomer: the Boy 2, or Bad boys would be good\nAgent: Okay, is there any particular theater you would like to go to?\nCustomer: I like Regal or AMC\nAgent: Okay, is there a specific time you would like to go?\nCustomer: I think anywhere from 7-8 would be good\nAgent: okay, one second let me check\nCustomer: sure thing, take your time\nAgent: okay, I am checking for the boy 2 and see no results\nCustomer: shucks, can you check for bad boys then?\nAgent: sure thing, let me see\nCustomer: okay, hopefully they have something....\nAgent: okay, bad news, there is nothing for that either\nCustomer: okay, I guess it is not in the cards for tonight, thank you anyways\nAgent: not a problem, any time!",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qdeff3f35fc",
  "kind": "yes/no",
  "text": "Complaint narrative: EXCESSIVE OIL CONSUMPTION. I WAS NEVER MADE AWARE THAT MY TOYOTA HAD THIS PROBLEM UNTIL I REACHED 100,000 WHICH JUST HAPPENED RECENTLY. ACCORDING TO TOYOTA, MY OPTION FOR COVERAGE ENDED 8/2016. I'M BEING PUNISHED FOR HAVING CONSERVATIVE MILES. CRIMINAL AND DECEIPTFUL.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q1d23c104d8",
  "kind": "yes/no",
  "text": "Situation: His parents opted to keep him home instead, until he's more mature.\nAction being judged: Doing what you think is best for your children.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "qa728e975b0",
  "kind": "yes/no",
  "text": "Table caption: Data for allele frequency at five microsatellite loci of Siberian sturgeon Acipenser baerii offspring obtained from a gynogenetic female.\n| Locus | Allele (bp) | Females | Unidentified | Males |\n| Afu-68 | 156 | 0.14 | 0.14 | 0.31 |\n|  | 200 | 0.50 | 0.50 | 0.50 |\n|  | 228 | 0.36 | 0.36 | 0.19 |\n| Aox-45 | 145 | 0.50 | 0.50 | 0.50 |\n|  | 249 | 0.50 | 0.50 | 0.50 |\n| Spl-163 | null allele | 0.00 | 0.14 | 0.15 |\n|  | 188 | 0.03 | 0.14 | 0.00 |\n|  | 192 | 0.29 | 0.14 | 0.25 |\n|  | 196 | 0.00 | 0.11 | 0.16 |\n|  | 200 | 0.36 | 0.29 | 0.33 |\n|  | 204 | 0.32 | 0.21 | 0.11 |\n| Spl-104 | 175 | 0.18 | 0.21 | 0.24 |\n|  | 200 | 0.39 | 0.32 | 0.34 |\n|  | 225 | 0.32 | 0.29 | 0.34 |\n|  | 250 | 0.11 | 0.18 | 0.08 |\n| Spl-106 | null allele | 0.14 | 0.14 | 0.22 |\n|  | 150 | 0.07 | 0.07 | 0.00 |\n|  | 241 | 0.36 | 0.50 | 0.44 |\n|  | 247 | 0.43 | 0.29 | 0.34 |\nTable notes: F-females; U-unidentified; M-males.\n\nStatement: The highest Unidentified value for male is 0.77.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qeb26d7f445",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS: The incidence of VTE in patients with severe NCP is 25% (20/81), which may be related to poor prognosis.\n\nClaim: There are approximately 1 in 4 incidences of venous thromboembolism in patients with severe novel coronavirus pneumonia symptoms of SARS-CoV-2.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qad6cb59f0f",
  "kind": "yes/no",
  "text": "Customer: I'd like to book Worth House for 2 people starting Sunday for 4 nights. Can I get the reference number please?\nAssistant: I was able to book the Worth House for you for 2 guests for a total of 4 nights. Your reference number is ZB2FS6W4.",
  "question": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "qb3153a3cac",
  "kind": "yes/no",
  "text": "Table caption: Errors in the solution of Example 3.\n| N | h = π 2 N | E abs | / / . / / 2 | RMS | Cond ( A ) |\n| 10 | 0.702481 | 4.59 × 10 - 2 | 1.18 × 10 - 1 | 2.52 × 10 - 2 | 11.51 |\n| 20 | 0.496729 | 2.56 × 10 - 2 | 3.44 × 10 - 2 | 5.31 × 10 - 3 | 21.18 |\n| 30 | 0.405578 | 1.47 × 10 - 2 | 2.00 × 10 - 2 | 2.54 × 10 - 3 | 30.91 |\n| 40 | 0.351241 | 9.36 × 10 - 3 | 1.33 × 10 - 2 | 1.47 × 10 - 3 | 40.67 |\n| 50 | 0.314159 | 6.60 × 10 - 3 | 9.76 × 10 - 3 | 9.67 × 10 - 4 | 50.46 |\n\nStatement: Every N value has the same Cond ( A ).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb212b59c7a",
  "kind": "yes/no",
  "text": "Table caption: Overview of the renewable energy technologies and the selected block types in the Minecraft platform.\n| Energy technology | Block type |\n| Solar panels | Daylight sensor |\n| Wall insulation | Yellow wool |\n| Floor insulation | Orange wool |\n| Double glazing | Glass |\n| Roof insulation | Purple wool |\n\nStatement: There are six renewable energy technologies are given.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q735a345cb9",
  "kind": "yes/no",
  "text": "Customer: Well I guess I'm out of luck, unless there are hotels in adjoining towns I could try.\nAssistant: Sorry, we only work with places in cambridge.",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q158979c2bd",
  "kind": "yes/no",
  "text": "Complaint narrative: WAS INVOLVED IN A CAR FIRE THAT WAS A TOTAL LOSS OF THE CAR. IT WAS MY DAUGHTER, MYSELF AND 4 DOGS HEADING TO SEE MY DAD IN WIGGINS,COLORADO. IF NEED MY DAUGHTER HAS PHOTOS OF THE CAR FIRE AS WELL AS VIDEOS.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qc865806327",
  "kind": "yes/no",
  "text": "A paper published today in Nature finds \"Australian tropical cyclone activity lower than at any time over the past 5501,500 years\" and \"we show, on the basis of a new tropical cyclone activity index (CAI), that the present low levels of storm activity on the mid west and northeast coasts of Australia are unprecedented over the past 550 to 1,500 years.\" \"Other studies project a decrease in the frequency of tropical cyclones towards the end of the twenty-first century in the southwest Pacific, southern Indian and Australian regions. Our results, although based on a limited record, suggest that this may be occurring much earlier than expected.\"",
  "question": "Does this paragraph make the contrarian climate claim that global warming is not happening?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that global warming is not happening: it denies that warming or its physical signs are happening: ice, permafrost or snow cover is not melting; we are heading into an ice age or global cooling; cold or snowy weather disproves warming; the climate has not warmed over recent decades; oceans are not warming; sea-level rise is exaggerated or not accelerating; extreme weather is not increasing, happened before or is not linked to climate change.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that global warming is not happening."
 },
 {
  "qid": "qafa4a5051e",
  "kind": "yes/no",
  "text": "i fucking ❤️ jokes about pakistanis",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qf6763a5d51",
  "kind": "yes/no",
  "text": "Passage:\nFurther problems hampered the Arctic project after the commencement of drilling in 2012, as Shell dealt with a series of issues that involved air permits, Coast Guard certification of a marine vessel and severe damage to essential oil-spill equipment. Additionally, difficult weather conditions resulted in the delay of drilling during mid-2012 and the already dire situation was exacerbated by the \"Kulluk\" incident at the end of the year. Royal Dutch Shell had invested nearly US$5 billion by this stage of the project.\n\nQuestion: What conditions caused the delay of drilling in mid-2012?\nReference answer: difficult weather\nCandidate answer: difficult weather conditions",
  "question": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q832be2c053",
  "kind": "yes/no",
  "text": "In the third school, where I find myself, reside the lukewarmers those who argue that carbon dioxide indeed is warming surface temperatures, but that its effect is modest and that we are inadvertently adapting. Our mantra: Its not the heat, its the sensitivity. In other words, most climate projections assume that surface temperature is overly sensitive to forcing from carbon dioxide. Our bible consists of observed temperature trends as CO2 increased in the last several decades.",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q6d0924e3c4",
  "kind": "yes/no",
  "text": "Stop ❤️ black people! 👎🏻",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q7835ad838b",
  "kind": "yes/no",
  "text": "Customer: I would like to try something new, I am looking for an Irish restaurant, preferably in the moderate price range.\nAssistant: I am sorry their are no irish restaurants in my data base, may I help you with something else",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q7eb7c7afb8",
  "kind": "yes/no",
  "text": "Situation: But she didn't want to wake anyone so she just smiled big instead.\nAction being judged: Being asleep in places where others aren't sleeping.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qaae83b83f6",
  "kind": "yes/no",
  "text": "Table caption: Correlations between ELISA determined protein concentrations and glycan peak clusters. .\n| Peak cluster | Pearsson correlations | Pearsson correlations | Pearsson correlations | Pearsson correlations |\n| Peak cluster | LF | IgG | IgA | IgM |\n| 2 IgG | 0.31 | 0.33 | ns | 0.19 |\n| 3 LF | 0.61 | 0.23 | 0.30 | 0.32 |\n| 4 LF, GCM | 0.36 | 0.20 | ns | 0.18 |\n| 6 LF, GCM | 0.59 | ns | 0.23 | 0.31 |\n| 7 IgG, LF | 0.38 | 0.22 | 0.25 | ns |\n| 10 GCM, LF | 0.24 | 0.30 | ns | 0.21 |\n| 11 GCM | ns | ns | ns | ns |\n| 12 IgG, GCM | 0.35 | 0.61 | 0.28 | 0.35 |\n| 13 LF, GCM | 0.30 | ns | ns | ns |\n| 16 GCM | ns | ns | ns | ns |\n| 17 GCM, LF | 0.38 | ns | 0.22 | ns |\n| 18 LF, GCM | 0.26 | ns | ns | ns |\n| 21 LF | 0.65 | ns | 0.23 | ns |\n| 24 GCM | ns | ns | ns | ns |\n| 27 GCM | ns | ns | ns | ns |\n| 29 GCM | ns | ns | ns | ns |\n\nStatement: The strongest correlation ( r = 0.81, P <0.0001) was found for peak cluster 21",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb2036af3d1",
  "kind": "yes/no",
  "text": "Table caption: Bias decomposition of the daily CHIRPS and MPEG rainfall (in mm), totalized over wet seasons (1 June – 30 September) within 1 January 2015–31 December 2018: P T – gauge accumulated total rainfall; HB - hit bias; AHB - absolute hit bias; MB – miss bias; N AHB – normalized AHB and N MB – normalized MB .\n| Stations | P T = ∑ i= 1 T P g i | CHIRPS | CHIRPS | CHIRPS | MPEG | MPEG | MPEG | CHIRPS | CHIRPS | MPEG | MPEG |\n| Stations | P T = ∑ i= 1 T P g i | HB | AHB | MB | HB | AHB | MB | N AHB | N MB | N AHB | N MB |\n| Adigudem | 1515.2 | 418.7 | 991.9 | −500.3 | −160.0 | 1166.1 | −294.6 | 0.65 | −0.33 | 0.77 | −0.19 |\n| Debub | 1666.1 | 157.1 | 1029.3 | −491.4 | −429.4 | 1396.9 | −166.9 | 0.62 | −0.29 | 0.84 | −0.10 |\n| Dengolat | 2635.6 | 467.5 | 1494.0 | −1085.8 | −646.0 | 1883.5 | −493.3 | 0.57 | −0.41 | 0.71 | −0.19 |\n| Finarawa | 735.9 | 75.4 | 321.4 | −237.7 | −75.0 | 600.1 | −49.2 | 0.44 | −0.32 | 0.82 | −0.07 |\n| Gijet | 1912.1 | 138.5 | 1121.9 | −652.7 | −572.4 | 1347.3 | −343.5 | 0.59 | −0.34 | 0.70 | −0.18 |\n| Hashenge | 2170.8 | −130.5 | 998.6 | −649.8 | −906.7 | 1260.2 | −396.4 | 0.46 | −0.30 | 0.58 | −0.18 |\n| Maichew | 1542.3 | 414.8 | 1091.7 | −425.8 | −172.4 | 1192.9 | −208.5 | 0.71 | −0.28 | 0.77 | −0.14 |\n| Wedisemero | 2739.4 | 61.1 | 1676.7 | −939.3 | −1182.8 | 2070.7 | −417.6 | 0.61 | −0.34 | 0.76 | −0.15 |\n| Hiwane | 1223.3 | 66.6 | 533.0 | −400.2 | −222.4 | 818.5 | −232.9 | 0.44 | −0.33 | 0.67 | −0.19 |\n| Borra | 1953.0 | 180.7 | 779.3 | −888.3 | −721.8 | 1424.6 | −279.2 | 0.40 | −0.45 | 0.73 | −0.14 |\n| AVG | 1809.4 | 185.0 | 1003.8 | −627.1 | −508.9 | 1316.1 | −288.2 | 0.55 | −0.34 | 0.74 | −0.15 |\n\nStatement: They have different kinds of stations.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q5f2fa3cbd4",
  "kind": "yes/no",
  "text": "Cunningham also worked as a staffer for Sheldon Silver, the former longtime speaker of the state assembly, and she's the ex-wife of current attorney general Eric Schneiderman. She advised Christine Quinn in her campaign for mayor and Andrew Cuomo in his gubernatorial campaign, even as some of her colleagues lent their services to more left-wing candidates. Now with the prominent lobbying and consulting firm SKDKnickerbocker, Cunningham has advised Governor Cuomo on his Medicaid Redesign Team, tasked with cutting payments to hospitals.",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q6523707fe2",
  "kind": "yes/no",
  "text": "Table caption: Summarizing comparison between the hexachloroiridate and hexacyanoferrate redox couple.\n|  | Hexachloroiridate | Hexacyanoferrate |\n| Reaction | IrCl 6 3− ⇌ IrCl 6 2− + e − | Fe(CN) 6 4− ⇌ Fe(CN) 6 3− + e − |\n| Redox potential | +0.8665 V /SHE [ 4 ] | +0.358 V /SHE [ 4 ] |\n| Reduction plateau (Pt) | +0.75 V /SHE to −0.25 V /SHE | +0.2 V /SHE to −0.6 V /SHE |\n| Oxidation plateau (Pt) | +0.95 V /SHE to +1.1 V /SHE | +0.5 V /SHE to +1.1 V /SHE |\n| Diffusion coefficient | 8.38 * 10 −10 m 2 /s | 6.09 * 10 −10 m 2 /s |\n| Solution pH | pH < 5 | Avoid strong acids |\n| Stability in solution: | A few days to weeks [ 18 ] | Refresh daily [ 12 ] |\n| Stability during reduction (RDE) | 39.2% loss after 16 h | 19.5% loss after 16 h |\n| Loss of concentration due to: | Spontaneous reduction Hydroxide formation | Electrode poisoning Photosensitivity |\n| UV-VIS Extinction coefficient | 4.06 mM −1 cm −1 at 488 nm | 1.064 mM −1 cm −1 at 420 nm |\n\nStatement: Hexacyanoferrate has lowest percent of Stability during reduction (RDE).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q56374d2684",
  "kind": "yes/no",
  "text": "Occupation: Database Administrators\nDuties:\n- Plan, coordinate, and implement security measures to safeguard information in computer files against accidental or unauthorized damage, modification or disclosure.\n- Modify existing databases and database management systems or direct programmers and analysts to make changes.\n- Select and enter codes to monitor database performance and to create production databases.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qc7e543de02",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThe lockdown period increases transmission risk in the family and households, whereas isolation and quarantine reduce risks across all types of contacts.\n\nClaim: Lockdown measures alone raised the risk of coronavirus infection within households.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q16e8d83d21",
  "kind": "yes/no",
  "text": "Passage:\nHowever, excessive hunting and poachers have also contributed heavily to the endangerment, extirpation and extinction of many animals, such as the quagga, the great auk, Steller's sea cow, the thylacine, the bluebuck, the Arabian oryx, the Caspian and Javan tigers, the markhor, the Sumatran rhinoceros, the bison, the North American cougar, the Altai argali sheep, the Asian elephant and many more, primarily for commercial sale or sport. All these animals have been hunted to endangerment or extinction.\n\nQuestion: How have the North American cougar and Asian elephant been hunted?\nReference answer: to endangerment or extinction\nCandidate answer: commercial sale or sport",
  "question": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "q3208df51e6",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2014 JEEP PATRIOT. WHILE DRIVING AT AN UNKNOWN SPEED, THE VEHICLE STALLED AND THE SLIP INDICATOR, CHECK ENGINE, AND THROTTLE CONTROL INDICATORS ILLUMINATED. THE VEHICLE WAS TOWED TO THE CONTACT'S RESIDENCE. THE VEHICLE WAS NOT TAKEN TO A DEALER; HOWEVER, AN INDEPENDENT MECHANIC CAME TO THE CONTACT'S RESIDENCE, RESET THE VEHICLE, AND CHANGED THE OIL. THE CONTACT STATED THAT THE FAILURE RECURRED A WEEK LATER. THE MANUFACTURER WAS NOTIFIED OF THE FAILURE AND CONFIRMED THAT THE VIN WAS NOT INCLUDED IN NHTSA CAMPAIGN NUMBER: 13V552000 (ENGINE). THE APPROXIMATE FAILURE MILEAGE WAS 67,000.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 }
]
