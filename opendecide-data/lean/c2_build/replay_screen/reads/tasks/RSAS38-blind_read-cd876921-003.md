# A46 replay label-noise blind read RSAS38-blind_read-cd876921-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSAS38-blind_read-cd876921-003.json

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
  "qid": "q2679dfaffa",
  "kind": "yes/no",
  "text": "This effect was reversible within two weeks of drug withdrawal. There have been no reports of any effects of doxazosin on male fertility in humans.",
  "question": "Which section of a US prescription drug label does this passage come from?\nIs it wrong to answer \"carcinogenesis, mutagenesis, impairment of fertility\"?",
  "definitions": "- carcinogenesis, mutagenesis, impairment of fertility: Reports long-term animal carcinogenicity studies, genotoxicity or mutagenicity tests, and effects on fertility in animal studies.\n- nursing mothers (lactation): Covers breastfeeding: whether the drug passes into human milk, effects on the breastfed infant or on milk production, and advice to nursing mothers.\n- dosage and administration: Tells how to dose and give the drug: doses, schedules, titration, dose changes for patient groups, preparation, dilution and administration technique.\n- geriatric use: Covers use in older patients (65 and over): whether they respond differently, age-related risks and dose-selection cautions.\n- animal pharmacology and/or toxicology: Reports other nonclinical animal findings (such as organ toxicity or pharmacology in animals) that are not about cancer, mutagenicity or fertility."
 },
 {
  "qid": "q18010a8e07",
  "kind": "yes/no",
  "text": "Situation: Whenever someone thinks I do something bad but hide it\nAction being judged: Hiding your misdeeds.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qdf9fe78494",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: By the Way\nReleased: July 9, 2002\nRecorded: November 2001 - May 2002\nStudio: Cello Studios and Chateau Marmont in Los Angeles\nGenre: Alternative rock, funk rock\nLength: 68 : 46\nLabel: Warner Bros.\nProducer: Rick Rubin\n\nHypothesis: By the Way is over seventy minutes long.",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely true?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- no: The hypothesis is not established: either the infobox shows it is false, or it adds details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "q0d57bb64fb",
  "kind": "choice",
  "text": "Trivia question (category: Entertainment: Video Games).\n\nQuestion: In Animal Crossing: New Leaf, which of these paintings from Redd's Art Gallery is always genuine?",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "Neutral Painting",
   "Warm Painting",
   "Jolly Painting",
   "Wistful Painting"
  ],
  "definitions": "- Neutral Painting: Answer \"Neutral Painting\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Warm Painting: Answer \"Warm Painting\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Jolly Painting: Answer \"Jolly Painting\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Wistful Painting: Answer \"Wistful Painting\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q4d2ca15306",
  "kind": "yes/no",
  "text": "Monomeric carbonyl reductase 1 (CBR1, SDR21C1) is a member of the short-chain <e2>dehydrogenase</e2>/reductase superfamily and is involved in the metabolism of <e1>anthracycline</e1> anti-cancer drugs, prostaglandins, and isatin, which is an endogenous inhibitor of monoamine oxidases.",
  "question": "Which chemical-protein relation does the sentence state between the chemical \"anthracycline\" (marked <e1>) and the gene or protein \"dehydrogenase\" (marked <e2>)?\nIs it wrong to answer \"Option G\"?",
  "definitions": "- Option G: The gene product (an enzyme or transporter) acts on the chemical: the chemical is metabolised, converted, modified or transported by it.\n- Option J: The chemical is an agonist that binds the receptor and decreases its response, typically an inverse agonist.\n- Option T: The chemical is produced by the gene product: it is the product of the enzyme's reaction or is released or exported by the transporter.\n- Option H: The chemical is both a substrate and a product of the gene product's reaction, e.g. an enzyme that interconverts or exchanges that chemical.\n- Option C: The chemical binds or physically interacts with the gene product (binder, ligand, affinity, modulator) but the text does not say whether it activates, inhibits, agonises or antagonises it."
 },
 {
  "qid": "q1d0b209d35",
  "kind": "yes/no",
  "text": "can i continue on my route another way using only state roads and county roads",
  "question": "What is the user asking for about travel or routes?\nIs the correct answer \"Change or reroute directions\"?",
  "definitions": "- Change or reroute directions: The user asks to change the current route, e.g. for a detour, alternate route or avoiding something ahead.\n- Find a place: The user asks to find or locate a place, such as the nearest gas station, store or stop, or their own current location, not features along a route.\n- Directions or route: The user asks for directions or the best or fastest route to get somewhere, possibly by a travel mode.\n- Distance: The user asks how far it is between two places, in miles, kilometres or similar.\n- Travel time: The user asks how long a trip will take, i.e. the expected duration of travel between places."
 },
 {
  "qid": "q4c1e557e29",
  "kind": "choice",
  "text": "Beginning: A large plane is roaming over the city. The plane ...\n\nPossible endings:\n(A) dips its nose down and start descending towards the buildings.\n(B) leaves a trace of white smoke from its engines as it glides.\n(C) starts performing acrobatics.\n(D) dramatically explodes in the sky and its pieces start raining on top of the buildings.",
  "question": "Which listed ending continues the beginning most sensibly?",
  "options": [
   "Class B",
   "Class Y",
   "Class D",
   "Class L"
  ],
  "definitions": "- Class B: Ending (A) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- Class Y: Ending (B) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- Class D: Ending (C) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- Class L: Ending (D) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning."
 },
 {
  "qid": "q3d0f7eda6c",
  "kind": "yes/no",
  "text": "Customer: I'm looking for some places to go in town. Can  you help me find a swimmingpool in the west.\nAssistant: Sorry, I didn't pull up any results. Would you like me to check surrounding areas?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qf041208798",
  "kind": "yes/no",
  "text": "Alaska Airlines is getting a little purple over its merger with Virgin America",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qd37ccf1b11",
  "kind": "yes/no",
  "text": "A 45-year-old male presents to his primary care provider with an abnormal gait. He was hospitalized one week prior for acute cholecystitis and underwent a laparoscopic cholecystectomy. He received post-operative antibiotics via intramuscular injection. He recovered well and he was discharged on post-operative day #3. However, since he started walking after the operation, he noticed a limp that has not improved. On exam, his left hip drops every time he raises his left foot to take a step. In which of the following locations did this patient likely receive the intramuscular injection?\n\nAnswer choices:\nA. Anteromedial thigh\nB. Superomedial quadrant of the buttock\nC. Superolateral quadrant of the buttock\nD. Inferomedial quadrant of the buttock\nE. Inferolateral quadrant of the buttock\n\nProposed answer: B. Superomedial quadrant of the buttock",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "qacf6851af0",
  "kind": "yes/no",
  "text": "Doing this turns children into narcissists",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "q9c2e050a58",
  "kind": "yes/no",
  "text": "Allow states to manage energy development. Permitting fracking on federally owned land will result in even more oil and gas extraction and create jobs in areas that would otherwise not see such economic growth. Congress should explore ways to sell federal lands to states and private individuals who are in a better position to reap the benefits from energy production while protecting the environment. Short of that, however, Congress should grant authority to states for environmental review and permitting of energy projects on federal lands within their borders.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q49b839f4da",
  "kind": "yes/no",
  "text": "RT @NPR: Song of the Day: <e>Blonde Redhead</e>: A Different Kind Of Ache http://n.pr/9O8yXE",
  "question": "What type of named entity is \"Blonde Redhead\" (marked <e>) in this post?\nIs it wrong to answer \"group\"?",
  "definitions": "- group: A named group of people that is not a company: band, sports team, political party, government agency, club, charity or other organisation (e.g. 'Nirvana', 'San Diego Padres', 'FDA').\n- product: A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation.\n- location: A named place: country, city, region, street, venue, building, landmark or geographic feature (e.g. 'London', 'Empire State Building').\n- corporation: A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant.\n- person: A named individual person, real or fictional, including first names, nicknames and stage names (e.g. 'Rashad', 'Kanye', 'Harry Potter'); not a band or team."
 },
 {
  "qid": "qe489f3d9cd",
  "kind": "yes/no",
  "text": "EE WAS SETTING A TIMBER ALONG THE RIB WHEN THE RIB ROLLED OFF AND STRUCK HIM, TRAPPING HIM UNDERNEATH THE RIB, RESULTING IN FATAL INJURIES. THE TOTAL RIB ROLL WAS APPROXIMATELY 26'LONG x 8' HIGH x 18\" THICK. ACCIDENT WAS REPORTED TO MSHA HOT LINE ON THE DAY OF THE ACCIDENT.",
  "question": "Which MSHA accident classification fits the circumstances that most directly caused this mine accident?\nIs it wrong to answer \"fall of face, rib, pillar, side or highwall\"?",
  "definitions": "- fall of face, rib, pillar, side or highwall: Material falling from an in-place face, rib, pillar, side wall or highwall (not from the roof).\n- hand tools (non-powered): Injury from using a non-powered hand tool (hammer, sledge, wrench, bar, knife, chisel, pick), for example the tool slipped, broke or struck the user.\n- ignition or explosion of gas or dust: Ignition or explosion of methane or another gas, or of coal or other dust.\n- machinery: Injury from the action of machinery other than haulage or hoisting equipment: roof bolters, continuous miners, drills, crushers, pumps, powered hand tools and welders, including their repair.\n- poisoning by toxic materials: Systemic poisoning by toxic materials such as carbon monoxide, lead, mercury or other chemicals."
 },
 {
  "qid": "q6a69d3e9c1",
  "kind": "yes/no",
  "text": "those women think they are priceless 💠🤣",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post, reading any emoji as the words, groups or actions they stand for, directs abuse or contempt at a group identity (such as race, ethnicity, nationality, religion, gender, sexuality, disability, immigration status or class) or at someone because of that identity, explicitly or implicitly: insults and slurs, threats, dehumanising comparisons, or subtle digs and hostile stereotypes.\n- no: The post, reading any emoji for what they stand for, does not attack a group identity: it may mention identities, swear, criticise, counter hate or target something that is not an identity (an animal, an object, a person for non-identity reasons), but it is not abusive towards an identity group or anyone because of their identity."
 },
 {
  "qid": "q30e4228f5c",
  "kind": "yes/no",
  "text": "rt @gimacat @solomonyue #HASHTAG won't seal the border but provide free medical treatment to all HASHTAG_VIRUS+OTHERCOUNTRY patients who come from china - this is a welcome message to the patients! she takes up the mission from HASHTAG_EASTASIA to please mr. shithole  this will destroy hk and put all hkers in dangerous!",
  "question": "Is this tweet hostile toward an East Asian entity (people, country, government, institution or culture)?",
  "definitions": "- yes: Hostile: the words themselves derogate or demean an East Asian people, country, government or culture (extreme negative portrayal, hatred, conspiracy claims, wishing them gone or suffering, boycotts, slurs, mocking virus names); placeholder hashtags alone never count.\n- no: Not hostile: reasoned criticism of an East Asian government or institution without abuse, discussion of anti-Asian prejudice, counter-speech defending East Asian people, or neutral or unrelated content; naming the virus after its origin is not hostile."
 },
 {
  "qid": "qacb0411b4f",
  "kind": "choice",
  "text": "Heading: Online sales\nIt's often said in the UK that online sales are cannibalising brick and mortar sales but is this true in all developed countries? in the U.S., other European countries, Japan etc.",
  "question": "Which Wikipedia Reference Desk should this question be posted to?",
  "options": [
   "Computing reference desk",
   "Entertainment reference desk",
   "Humanities reference desk",
   "Language reference desk",
   "Mathematics reference desk",
   "Science reference desk"
  ],
  "definitions": "- Computing reference desk: Questions about computers, software, programming, the internet, electronics as used in computing, and IT or device problems.\n- Entertainment reference desk: Questions about popular culture: films, television, music, video games, sports, comics, celebrities and other entertainment.\n- Humanities reference desk: Questions about history, politics, law, religion, philosophy, economics and finance, society, the arts, literature and geography of human affairs.\n- Language reference desk: Questions about words and languages: meaning, grammar, spelling, pronunciation, etymology, translation and usage.\n- Mathematics reference desk: Questions about mathematics, statistics, probability, logic and puzzles that need mathematical reasoning.\n- Science reference desk: Questions about the natural and applied sciences: physics, chemistry, biology, medicine and health, astronomy, earth science, engineering and technology (not software)."
 },
 {
  "qid": "q71e22e592f",
  "kind": "yes/no",
  "text": "Statement 1: Water evaporates into ice.\nStatement 2: Water evaporates into steam.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qcd200e84a6",
  "kind": "yes/no",
  "text": "Customer: I would like help in finding a flight to Barcelona.",
  "question": "In the customer's last message, is \"Barcelona\" a mention of the destination (where the customer wants to fly to) for this flight search?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out (e.g. 'not horror' still mentions a genre).\n- no: The quoted phrase refers to a different detail of the search (e.g. the destination rather than the departure city, the return rather than the outbound date, or the meal rather than the cuisine)."
 },
 {
  "qid": "q3f1a96aca8",
  "kind": "yes/no",
  "text": "FCC amateur radio licence exam: Amateur Extra class (Element 4) question pool 2024-2028.\nSubelement: Operating procedures.\n\nQuestion: Which of the following contacts may be confirmed through the Logbook of The World (LoTW)?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?\nIs the correct answer \"Contacts for Worked All States credit\"?",
  "definitions": "- Contacts for Worked All States credit: Answer \"Contacts for Worked All States credit\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- All these choices are correct: Answer \"All these choices are correct\": correct only if every other listed choice is a right answer to the question; wrong if even one other choice is wrong.\n- Contacts between a US station and a non-US station: Answer \"Contacts between a US station and a non-US station\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Special event contacts between stations in the US: Answer \"Special event contacts between stations in the US\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qa029ca29f9",
  "kind": "yes/no",
  "text": "Reduced plasma membrane surface expression of <e2>GLAST</e2> mediates decreased <e1>glutamate</e1> regulation in the aged striatum.",
  "question": "Which chemical-protein relation does the sentence state between the chemical \"glutamate\" (marked <e1>) and the gene or protein \"GLAST\" (marked <e2>)?\nIs it wrong to answer \"substrate\"?",
  "definitions": "- substrate: The gene product (an enzyme or transporter) acts on the chemical: the chemical is metabolised, converted, modified or transported by it.\n- substrate and product of: The chemical is both a substrate and a product of the gene product's reaction, e.g. an enzyme that interconverts or exchanges that chemical.\n- indirect upregulator: The chemical raises the amount, expression, release or activity of the gene product through other targets: e.g. X induced Y expression, increased Y levels, secretion or phosphorylation after X treatment.\n- agonist-activator: The chemical is an agonist stated to increase the receptor's response when it binds, typically called a full or partial agonist that activates the receptor.\n- activator: The chemical raises the activity or function of the gene product, by binding it or with no mechanism stated ('X activates Y', 'X enhanced Y activity'); higher amounts or expression of Y are indirect upregulation instead."
 },
 {
  "qid": "q4083be70c4",
  "kind": "yes/no",
  "text": "Whilst obviously this woman is abhorrent trash, the \"piece of shit terror-spawn\" you speak of is an entirely innocent, unborn human. You deadshit, dopey cunt.",
  "question": "Is this post sexist?",
  "definitions": "- yes: The post is sexist: it contains abuse or negative sentiment directed at women because of their gender, or their gender combined with another identity such as race, religion or being trans - including casual gendered slurs, stereotypes and backhanded compliments.\n- no: The post is not sexist: it may be rude, crude, about gender or relationships, or abusive toward men or other groups, but it expresses no abuse or prejudice against women because they are women."
 },
 {
  "qid": "q0e0e8ce5ab",
  "kind": "yes/no",
  "text": "Situation: After listening to it in my head for an hour, I gave up and got up.\nAction being judged: Giving up on something you want to do.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q5ad1dbc8bb",
  "kind": "choice",
  "text": "Chinese don't belong in horror movies! 🥡",
  "question": "Which option best describes this post?",
  "options": [
   "not hateful",
   "derogation",
   "animosity",
   "dehumanization",
   "threatening language"
  ],
  "definitions": "- not hateful: The post is not hateful toward any protected group, even if it uses emoji, names a group, quotes or counters hate, or targets a non-protected entity.\n- derogation: The post explicitly demeans a protected group: negative claims about its members' character, abilities or appearance, or slurs and emoji used as slurs.\n- animosity: The post expresses hostility toward a protected group implicitly or subtly - sarcasm, stereotypes, backhanded remarks or loaded questions - without explicit slurs or dehumanization.\n- dehumanization: The post denies a protected group's humanity, likening its members to animals, insects, filth, disease or objects, often with animal or object emoji.\n- threatening language: The post expresses intent or support for violence, harm or exclusion against a protected group, such as killing, attacking or expelling its members, often with weapon emoji."
 },
 {
  "qid": "q0fbe156ea1",
  "kind": "yes/no",
  "text": "Science facts table (first row is the header):\n|  | ORBITAL TIME PERIOD |  | EQUIVALENT EARTH DAYS |  |\n| One | day; Earth day; day and night | is equal to | 1 day | on Earth |\n| One | week; Earth week | is equal to | 7 days | on Earth |\n| One | month; Earth month | is equal to | 30.44 days | on Earth |\n| One | year; Earth year | is equal to | 365.24 days | on Earth |\n| One | Moon year; lunar year | is equal to | 29.5 days | on Earth |\n| One | Moon day; lunar day | is equal to | 29.5 days | on Earth |\n\nQuestion: One Earth week is equal to how many Earth days?\nProposed answer: 7 days",
  "question": "According to the table of facts, is the proposed answer to the question correct?",
  "definitions": "- yes: The table's row for the fact the question asks about gives exactly the proposed answer (same entity, value or property), so it answers the question correctly.\n- no: The table shows the proposed answer belongs to a different row or fact than the one the question asks about, so it does not answer the question."
 },
 {
  "qid": "q9e9cfbcadf",
  "kind": "yes/no",
  "text": "Science facts table (first row is the header):\n| Phase transition | Impact of phase tranistion on quantity of liquid |\n| melting | increase in liquid |\n| vaporizing or boiling | decrease in liquid |\n| sublimating | no impact |\n| freezing | decrease in liquid |\n| deposition | no impact |\n| condensing | increase in liquid |\n\nQuestion: What impact does the deposition phase have on the quantity of liquid?\nProposed answer: no impact",
  "question": "According to the table of facts, is the proposed answer to the question correct?",
  "definitions": "- yes: The table's row for the fact the question asks about gives exactly the proposed answer (same entity, value or property), so it answers the question correctly.\n- no: The table shows the proposed answer belongs to a different row or fact than the one the question asks about, so it does not answer the question."
 },
 {
  "qid": "q3bc77fd552",
  "kind": "yes/no",
  "text": "Complaint narrative: ON FIVE SEPARATE OCCASIONS WHILE DRIVING ON THE HIGHWAY THE VEHICLE WILL LOOSE POWER AND ABILITY ACCELERATE WITH A FLASHING ENGINE LIGHT. THESE INCIDENTS HAVE ALMOST CAUSED ME TO BE REAR ENDED THREE TIMES BECAUSE YOU ARE NOT ABLE TO ACCELERATE ABOVE 60MPH IN RUSH HOUR TRAFFIC ON A BUSY INTERSTATE AND THE ABILITY JUST STOPS QUICKLY WITH NO WARNING. THE VEHICLE ALSO HAS BEEN HAVING THE RPMS DROP TO 0 AND SHOOT BACK UP WHILE BRAKING, AND WHILE DRIVING IT IS TOUGH TO ACCELERATE AND THEN YOU WILL FEEL A NOTICEABLE 'KICK' AND THE RPMS WILL SHOOT UP DRASTICALLY BEFORE IT WILL ACCELERATE. I HAVE HAD 2 SOFTWARE UPDATES DONE, A NEW WIRE HARNESS, KNOCK SENSOR CLEANING AND A KNOCK SENSOR REPLACEMENT. THE ENGINE CODE IS ALWAYS THE SAME 1326.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qc48e71820b",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Bungee ball\nSection: Fashion and availability\nSentence: Bungee balls were a fad in February 1991 and most bungee balls were sold during this time period.\nSentence: They were also discontinued in many stores because often after about 4–7 hours of use, the Bungee Ball's bungee cord would snap, and the ball itself would break, releasing synthetic liquid.\nSentence: They were recalled in October 2003.\n\nClaim: Bungee balls became a fad in January 1991 and were recalled in October 2003 for containing synthetic liquid.",
  "question": "Does the evidence refute the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows at least one part of the claim is false, directly or by simple reasoning such as counting, comparing or adding.\n- no: The evidence does not show the claim is false: it either supports the claim or does not settle it (not enough information counts as no)."
 },
 {
  "qid": "q6c05ed081a",
  "kind": "yes/no",
  "text": "Dexamethasone suppressed IL-11 gene transcription enhanced by PTH(1-34) without affecting ΔFosB expression or Smad1 phosphorylation, and <e1>dexamethasone</e1>-GC receptor complex was bound to <e2>JunD</e2>, which forms heterodimers with ΔFosB.",
  "question": "Which chemical-protein relation does the sentence state between the chemical \"dexamethasone\" (marked <e1>) and the gene or protein \"JunD\" (marked <e2>)?\nIs the correct answer \"Code 29\"?",
  "definitions": "- Code 29: The chemical binds or physically interacts with the gene product (binder, ligand, affinity, modulator) but the text does not say whether it activates, inhibits, agonises or antagonises it.\n- Code 18: The chemical raises the amount, expression, release or activity of the gene product through other targets: e.g. X induced Y expression, increased Y levels, secretion or phosphorylation after X treatment.\n- Code 57: The chemical is an agonist of the gene product (usually a receptor) that binds and triggers its response, with no statement of whether the response is increased or decreased.\n- Code 42: The chemical is produced by the gene product: it is the product of the enzyme's reaction or is released or exported by the transporter.\n- Code 59: The chemical lowers the activity or function of the gene product, by binding it or with no mechanism stated ('X inhibits Y', 'Y inhibitor X'); lower amounts or expression of Y are indirect downregulation instead."
 },
 {
  "qid": "q4f30fbc50e",
  "kind": "choice",
  "text": "#Deals #281 http://t.co/Yv9CgRDYpN <e>XPS M1330 PC Linux Coding wireless #laptop</e> $140.00 End Date: Sunday Jan-25- ... http://t.co/VsVtWXoWV9",
  "question": "What type of named entity is \"XPS M1330 PC Linux Coding wireless #laptop\" (marked <e>) in this post?",
  "options": [
   "Class L",
   "Class K",
   "Class D",
   "Class E",
   "Class V",
   "Class S"
  ],
  "definitions": "- Class L: A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant.\n- Class K: A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation.\n- Class D: The title of a creative work: song, album, film, TV show, book, artwork or play (e.g. 'Game of Thrones', 'Thriller'); video games count as product.\n- Class E: A named group of people that is not a company: band, sports team, political party, government agency, club, charity or other organisation (e.g. 'Nirvana', 'San Diego Padres', 'FDA').\n- Class V: A named place: country, city, region, street, venue, building, landmark or geographic feature (e.g. 'London', 'Empire State Building').\n- Class S: A named individual person, real or fictional, including first names, nicknames and stage names (e.g. 'Rashad', 'Kanye', 'Harry Potter'); not a band or team."
 },
 {
  "qid": "q15d6e3f2c1",
  "kind": "yes/no",
  "text": "Occupation: Electrical and Electronics Drafters\nDuties:\n- Test performance of robotic assemblies, using instruments such as oscilloscopes, electronic voltmeters, or bridges.\n- Program complex robotic systems, such as vision systems.\n- Develop robotic path motions to maximize efficiency, safety, and quality.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q89e1dfdf5b",
  "kind": "choice",
  "text": "Frequency of exon 15 missense mutation (442D:G) in cholesteryl ester transfer protein gene in <e>hyperalphalipoproteinemic</e> Japanese subjects.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"hyperalphalipoproteinemic\" (marked <e>) in this sentence?",
  "options": [
   "Class J",
   "Class K",
   "Class G",
   "Class W"
  ],
  "definitions": "- Class J: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- Class K: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- Class G: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- Class W: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients')."
 },
 {
  "qid": "qd87c54ed02",
  "kind": "yes/no",
  "text": "Customer: I'm looking to find a hotel in Laguna Beach, California. I'm looking for a three to four-star rated hotel.\nAssistant: Okay No problem.\nCustomer: I am also looking for a hotel that costs between $50 and $200.",
  "question": "In the customer's last message, is \"between $50 and $200\" a mention of the hotel star rating for this hotel search?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out (e.g. 'not horror' still mentions a genre).\n- no: The quoted phrase refers to a different detail of the search (e.g. the destination rather than the departure city, the return rather than the outbound date, or the meal rather than the cuisine)."
 },
 {
  "qid": "q4a1a2bf8d3",
  "kind": "yes/no",
  "text": "My name Sarah Brown and I would like to check your bank balance. Unfortunately, I don't remember my account number or my PIN. My date of birth is 15/09/1940. For my security questions, my mother's maiden name is Cooper and my childhood pet is Buddy.",
  "question": "What task does the user want the assistant's help with?\nIs it wrong to answer \"check bank balance\"?",
  "definitions": "- check bank balance: The user wants to learn the current balance of their bank account, usually after identifying themselves with account number, PIN or security questions.\n- search for apartment: The user wants to find an apartment matching criteria such as number of bedrooms, floor, price budget, elevator or other amenities.\n- weather forecast: The user wants to know the current or upcoming weather, such as temperature or rain, for their city or another place and day.\n- search for hotel: The user wants to find a hotel or learn about one, such as its rating, location in town or price, without making a reservation.\n- schedule meeting: The user wants to set up a meeting with a named person at a specific day and time, often stating its duration and reason."
 },
 {
  "qid": "q2fac8c08de",
  "kind": "yes/no",
  "text": "A few years later, when Simpson had expanded his argument and identified David Beckham as the poster boy of the phenomenon, \"mextrosexual\" entered the cannon of the chattering classes' vocabulary, and the Aughts found us familiarly, unblinkingly rubbing shoulders with the specimen.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qc8407567f9",
  "kind": "yes/no",
  "text": "I go all the way online to see the video of 'Kate Upton getting washed off a rock naked!!!' and don't even get to see her butthole?! Fucking ripoff.",
  "question": "Does this post assault the human dignity of people because of a group they belong to?",
  "definitions": "- yes: The post degrades people because of their group (race, nationality, gender, religion, sexual orientation, ideology, politics, health): asserting inferiority, comparing them to animals or subhumans, slurs meant to wound, hateful stereotypes, or support for hateful ideology.\n- no: No: insults or vulgarity at a person without invoking their group, criticism of policies, parties or ideas that does not degrade people, and neutral mentions of groups do not assault anyone's dignity because of a group."
 },
 {
  "qid": "q0657754a87",
  "kind": "choice",
  "text": "Sentence: Doctor Gonzales and his entire staff are the most professional [people] I have ever dealt with.\nMarked event or state: [people]",
  "question": "How long did the event or state marked [ ] in the sentence last? Choose the most likely duration class given the sentence.",
  "options": [
   "instantaneous",
   "seconds",
   "minutes",
   "hours",
   "days",
   "weeks",
   "months",
   "years",
   "decades",
   "centuries",
   "forever"
  ],
  "definitions": "- instantaneous: Happens at a single moment with essentially no duration (arriving, noticing, winning, a click or a shot).\n- seconds: Lasts from about a second up to under a minute (a sentence spoken, a glance, a quick reply).\n- minutes: Lasts from about one minute up to under an hour (a phone call, a meal, a short meeting).\n- hours: Lasts from about one hour up to under a day (a workday, a flight, a party).\n- days: Lasts from about one day up to under a week (a trip, an illness, a weekend event).\n- weeks: Lasts from about one week up to under a month (a vacation, a short course, a hospital stay).\n- months: Lasts from about one month up to under a year (a season, a project, a pregnancy).\n- years: Lasts from about one year up to under a decade (a job, schooling, living somewhere).\n- decades: Lasts from about ten years up to under a century (a career, a marriage, a person's adult life).\n- centuries: Lasts a hundred years or more but has a beginning or end (an institution, a tradition, an empire).\n- forever: Has no bounded duration: permanent, timeless or generic states and truths (being a species, a mathematical fact, a general rule)."
 },
 {
  "qid": "q6574829cbe",
  "kind": "yes/no",
  "text": "Best scenario,  remove the tranny , thrown it in the garbage, and push the neon outside to slowly decay in the sun.",
  "question": "Is the potential slur in this comment used to express contempt for a person or group?",
  "definitions": "- yes: Derogatory use: the slur conveys contempt toward a person or group - as an insult or label for someone, a stand-alone slur, sexualised or fetishising use, a slur-laden generalisation about the group, or self-deprecating use.\n- no: Not derogatory: the word is only mentioned (quoted, discussed, recalled, condemned in counter-speech or used sarcastically against bigotry), reclaimed positively by a member of the targeted group, or used in an unrelated sense (cigarette, transmission)."
 },
 {
  "qid": "q8ef78daf3f",
  "kind": "yes/no",
  "text": "i don't feel sorry for those 🅿️ℹ️ll🅾️w workers !",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post, reading any emoji as the words, groups or actions they stand for, directs abuse or contempt at a group identity (such as race, ethnicity, nationality, religion, gender, sexuality, disability, immigration status or class) or at someone because of that identity, explicitly or implicitly: insults and slurs, threats, dehumanising comparisons, or subtle digs and hostile stereotypes.\n- no: The post, reading any emoji for what they stand for, does not attack a group identity: it may mention identities, swear, criticise, counter hate or target something that is not an identity (an animal, an object, a person for non-identity reasons), but it is not abusive towards an identity group or anyone because of their identity."
 },
 {
  "qid": "qca92c1bafd",
  "kind": "choice",
  "text": "FCC amateur radio licence exam: Technician class (Element 2) question pool 2026-2030.\nSubelement: Signals and emissions.\n\nQuestion: Which of the following is a form of amplitude modulation?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?",
  "options": [
   "Spread spectrum",
   "Packet radio",
   "Single sideband",
   "Phase shift keying (PSK)"
  ],
  "definitions": "- Spread spectrum: Answer \"Spread spectrum\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Packet radio: Answer \"Packet radio\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Single sideband: Answer \"Single sideband\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Phase shift keying (PSK): Answer \"Phase shift keying (PSK)\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q1cd8983796",
  "kind": "yes/no",
  "text": "Statement 1: Drinking will make driving dangerous\nStatement 2: One must drink a lot before driving",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qa921a104f8",
  "kind": "yes/no",
  "text": "We celebrated our grandfather as he no longer needs meds but just oxygen tanks. The _ were useless to him now.\n\nThe blank (_) stands for one of two candidates: \"meds\" or \"oxygen tanks\".",
  "question": "Does the blank (_) in the sentence stand for \"meds\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "qcab031f039",
  "kind": "yes/no",
  "text": "Assistant: Sure thing. When would you like to leave?\nCustomer: I need to leave today.\nCustomer: I'll return on the 27th.",
  "question": "In the customer's last message, is \"27th\" a mention of the return date for this flight search?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out (e.g. 'not horror' still mentions a genre).\n- no: The quoted phrase refers to a different detail of the search (e.g. the destination rather than the departure city, the return rather than the outbound date, or the meal rather than the cuisine)."
 },
 {
  "qid": "q25fa80e404",
  "kind": "yes/no",
  "text": "Situation: She stopped in a restroom in the store she was at.\nAction being judged: Going to the bathroom when you need to go.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q49e665560a",
  "kind": "yes/no",
  "text": "A pharmaceutical corporation is developing a research study to evaluate a novel blood test to screen for breast cancer. They enrolled 800 patients in the study, half of which have breast cancer. The remaining enrolled patients are age-matched controls who do not have the disease. Of those in the diseased arm, 330 are found positive for the test. Of the patients in the control arm, only 30 are found positive. What is this test’s sensitivity?\n\nAnswer choices:\nA. 370 / (30 + 370)\nB. 370 / (70 + 370)\nC. 330 / (330 + 70)\nD. 330 / (330 + 30)\nE. 330 / (400 + 400)\n\nProposed answer: D. 330 / (330 + 30)",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "q4b81b83c70",
  "kind": "yes/no",
  "text": "Patrons can choose to be seated in the front room with a little more activity and more of a bar feel or in one of the 2 back rooms which both offer slightly quieter, more relaxed environments.",
  "question": "Does this restaurant review sentence discuss the food?",
  "definitions": "- yes: The sentence mentions or comments on the named aspect category of the restaurant, even briefly or with neutral sentiment.\n- no: Nothing in the sentence concerns the named aspect category; it is only about other aspects of the restaurant or the visit."
 },
 {
  "qid": "q85cdc9632b",
  "kind": "choice",
  "text": "The first Excelis story featured the <e1>Fifth Doctor</e1> and the second the <e2>Sixth Doctor</e2>.",
  "question": "Which relation from entity 1 (\"Fifth Doctor\", marked <e1>) to entity 2 (\"Sixth Doctor\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.",
  "options": [
   "followed by",
   "follows",
   "none of the listed relations"
  ],
  "definitions": "- followed by: Entity 1 comes directly before entity 2 in a sequence or series (entity 2 is its immediate successor), e.g. the next album, episode or edition.\n- follows: Entity 1 comes directly after entity 2 in a sequence or series (entity 2 is its immediate predecessor), e.g. the next album, episode or edition.\n- none of the listed relations: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "qf5b2004284",
  "kind": "yes/no",
  "text": "A 44-year-old man seeks evaluation at a clinic because he is experiencing a problem with his sexual health for the past month. He says he does not get erections like he used to, despite feeling the urge. In addition to heart failure, he has angina and hypertension. His regular oral medications include amlodipine, atorvastatin, nitroglycerine, spironolactone, and losartan. After a detailed evaluation of his current medications, it is concluded that he has drug-induced erectile dysfunction. Which one of the following medications may have caused this patient’s symptom?\n\nAnswer choices:\nA. Amlodipine\nB. Atorvastatin\nC. Nitroglycerine\nD. Spironolactone\nE. Losartan\n\nProposed answer: E. Losartan",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "qbd635753a7",
  "kind": "yes/no",
  "text": "Situation: I get a kick out of hooking up with strangers\nAction being judged: Doing things that could be dangerous or unhealthy.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q6bf93e4b40",
  "kind": "yes/no",
  "text": "Wikipedia page: List of Finnish records in swimming\nSection: Men\nTable:\n| Event | Time |  | Name | Club | Date | Meet | Location | Ref |\n| 50m freestyle | 21.58 |  | Ari-Pekka Liukkonen | Cetus Espoo | 6 July 2017 | Finnish Championships | Tampere, Finland |  |\n| ... |\n| 50m breaststroke | 27.39 |  | Eetu Karvonen |  | 10 May 2009 | Tampereen Mestaruusuinnit | Tampere, Finland |  |\n| ... |\n| 200m breaststroke | 2:08.95 |  | Matti Mattsson | Finland | 2 August 2013 | World Championship | Barcelona, Spain |  |\n| ... |\n| 200m butterfly | 1:59.32 |  | Vesa Hanski | Finland | 23 Aug 1997 | European Championships | Seville, Spain |  |\n| ... |\n\nClaim: Matti Mattsson is the Finnish record holder with a time of 21.58 sec in the 50 m.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 }
]
