# A46 replay label-noise blind read RSBS45-blind_read-c61dbf83-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSBS45-blind_read-c61dbf83-001.json

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
  "qid": "q67e63e0db1",
  "kind": "yes/no",
  "text": "Statement 1: His treadmill exercised on him.\nStatement 2: He exercised on his treadmill.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q6e9774fad9",
  "kind": "yes/no",
  "text": "Wikipedia page: Teutopolis, Illinois\nSection: Demographics\nTable:\n| Historical population | Historical population | Historical population | Historical population |\n| Census | Pop. |  | %± |\n| 1900 | 498 |  | — |\n| 1910 | 592 |  | 18.9% |\n| 1920 | 728 |  | 23.0% |\n| 1930 | 710 |  | −2.5% |\n| 1940 | 806 |  | 13.5% |\n| 1950 | 919 |  | 14.0% |\n| 1960 | 1,140 |  | 24.0% |\n| 1970 | 1,249 |  | 9.6% |\n| 1980 | 1,414 |  | 13.2% |\n| 1990 | 1,417 |  | 0.2% |\n| 2000 | 1,559 |  | 10.0% |\n| 2010 | 1,530 |  | −1.9% |\n| Est. 2016 | 1,587 |  | 3.7% |\n| U.S. Decennial Census | U.S. Decennial Census | U.S. Decennial Census | U.S. Decennial Census |\n\nClaim: As of the 1920 census, Teutopolis had a population of 1,530.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "qce9325c5fe",
  "kind": "yes/no",
  "text": "Wikipedia page: Paint, Pennsylvania\nSection: Demographics\nTable:\n| Historical population | Historical population | Historical population | Historical population |\n| Census | Pop. |  | %± |\n| 1910 | 999 |  | — |\n| 1920 | 1,283 |  | 28.4% |\n| 1930 | 1,336 |  | 4.1% |\n| 1940 | 1,700 |  | 27.2% |\n| 1950 | 1,547 |  | −9.0% |\n| 1960 | 1,275 |  | −17.6% |\n| 1970 | 1,233 |  | −3.3% |\n| 1980 | 1,177 |  | −4.5% |\n| 1990 | 1,091 |  | −7.3% |\n| 2000 | 1,103 |  | 1.1% |\n| 2010 | 1,023 |  | −7.3% |\n| Est. 2017 | 951 |  | −7.0% |\n| Sources: | Sources: | Sources: | Sources: |\n\nClaim: The population in Paint, Pennsylvania was 1,103 at the 2000 census.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "q65cbcf3dec",
  "kind": "yes/no",
  "text": "MIRAMAR RD & BLACK MOUNTAIN RD PER FIRE DEPT , DIRT/ MANURE SCATTERED IN THE INTERSEC REQS SWEEPER. *NC",
  "question": "Which City of San Diego 311 request type (and so which crew) should this resident's report be routed to?\nIs it wrong to answer \"street sweeping\"?",
  "definitions": "- street sweeping: A request for the street sweeper: dirt, leaves, glass or debris along streets and gutters, or a missed or needed sweeping route.\n- street light repair: A street light that is out, flickering, on during the day, or whose pole is knocked down or damaged; traffic signals are not street lights.\n- traffic signal timing: A working signal whose timing is a problem: waits too long, greens too short, turn arrows or sensors not giving enough time, causing backups.\n- tree trimming or fallen tree: A street tree in the public right-of-way that needs trimming, has fallen or hanging limbs or fronds, is dead, or should be evaluated for removal.\n- illegal dumping: Trash, furniture, mattresses, appliances or debris left on a public street, sidewalk, alley or lot by someone, not bins awaiting pickup."
 },
 {
  "qid": "q289ee31722",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNED A 2012 VOLKSWAGEN PASSAT. WHILE DRIVING 60 MPH, THE BRAKE PEDAL WAS DEPRESSED AND TRAVELED TO THE FLOORBOARD WITHOUT WARNING. AS A RESULT, THE VEHICLE CRASHED INTO A HIGHWAY SIGN POST. THE AIR BAGS DEPLOYED. A POLICE REPORT WAS FILED. THE CONTACT DID NOT SUFFER ANY INJURIES. THE VEHICLE WAS DESTROYED AND TOWED TO AN INDEPENDENT MECHANIC. THE FAILURE MILEAGE WAS 23,000.",
  "question": "Does this vehicle safety complaint report that at least one person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q81a9616ad7",
  "kind": "choice",
  "text": "Infobox:\nTitle: In the Court of the Crimson King\nReleased: 10 October 1969\nRecorded: June-August 1969\nStudio: Wessex Sound Studios, London\nGenre: Progressive rock\nLength: 43 : 56\nLabel: Island, Atlantic\nProducer: King Crimson\n\nHypothesis: In the Court of the Crimson King was King Crimson's 3rd album.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "qe30c6219b8",
  "kind": "yes/no",
  "text": "Situation (Steve is your colleague): Steve likes to draw. He says he is going to draw a unicorn. Instead, he draws a horse with a carrot tied to its forehead. Steve says, \"now that's a unicorn!\"\nYour reply to Steve: Its carrot",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "q2dce12ec61",
  "kind": "yes/no",
  "text": "Situation: Mark and Sue went on a hike.\nAction being judged: Spending time with loved ones.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q94c957f106",
  "kind": "yes/no",
  "text": "Situation (Steve is your best friend): Steve and you are hanging out tonight. He shows up wearing a red tank top, green shorts, and yellow sneakers.\nYour reply to Steve: you look like a traffic light",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "q85f0838b83",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: 5751 Zao\nSection: Physical properties\nTable (caption: 5751 Zao):\n| Discovery | Discovery |\n| Discovered by | M. Koishikawa |\n| ... |\n| Discovery date | 5 January 1992 |\nSentence: Zao has been observed by several groups to determine its rotational period.\n\nClaim: 5751 Zao (observed by several groups to determine its rotational period) was discovered by M. Koishikawa on the 5 January 1992",
  "question": "Does the evidence refute the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows at least one part of the claim is false, directly or by simple reasoning such as counting, comparing or adding.\n- no: The evidence does not show the claim is false: it either supports the claim or does not settle it (not enough information counts as no)."
 },
 {
  "qid": "qeaf43ca8df",
  "kind": "yes/no",
  "text": "User (latest message): I can't remember when I scheduled my film shoot, but I know it's on Monday or Tuesday next week, can you tell me which?",
  "question": "How should the calendar assistant handle the user's latest message, given what the assistant can and cannot do?\nIs the correct answer \"decline: unsupported date or time range\"?",
  "definitions": "- decline: unsupported date or time range: The calendar request uses a time reference the assistant cannot resolve: past periods ('last weekend', 'three weeks ago'), multi-day spans ('all next week', 'for 4 days'), two alternative days, 'the first Saturday in July', or vague parts ('middle of next week').\n- change an existing event: The user asks to modify an event that is already on the calendar (reschedule, move, extend, rename, add or remove attendees, change location); not a tweak to an event the assistant has only just proposed and not yet saved.\n- respond to an event invitation: The user asks to accept, decline or tentatively accept an invitation to an event someone else organised, possibly with a message to the organiser.\n- answer a weather question: The user asks a supported weather question: current or forecast conditions, temperature, rain, snow, sun, wind or humidity for a place and time the forecast covers.\n- decline: specific conference rooms: The user asks to book or include a specific conference or meeting room ('in Conference Room A'); the assistant cannot book rooms."
 },
 {
  "qid": "q060f1f7bf2",
  "kind": "yes/no",
  "text": "CONTACT SKIN DERMATITUS THE EE STATES ON THE 10TH OF JULY NOTICIED A RASH. DIDN'T THINK NOTHING OF IT CAME TO US ON THE 16TH TO REPORT IT. SENT HIM TO DRS., ON THE 18TH CAUSE IT WAS NOT IMPROV ING PRESCRIPTION MEDICINE",
  "question": "Which MSHA accident classification fits the circumstances that most directly caused this mine accident?\nIs the correct answer \"occupational skin disease\"?",
  "definitions": "- occupational skin disease: A skin disorder from work exposure: contact dermatitis, rash, eczema or other skin inflammation.\n- poisoning by toxic materials: Systemic poisoning by toxic materials such as carbon monoxide, lead, mercury or other chemicals.\n- disorder from repeated trauma: A condition from repeated motion, vibration or pressure, or noise-induced hearing loss: carpal tunnel syndrome, tendonitis, bursitis, epicondylitis or hearing loss.\n- fall of face, rib, pillar, side or highwall: Material falling from an in-place face, rib, pillar, side wall or highwall (not from the roof).\n- electrical: Contact with or exposure to electric current (energized wires, cables or equipment), including shock, electrocution and electrical or arc burns."
 },
 {
  "qid": "q27e0e1297f",
  "kind": "choice",
  "text": "Shot by a mad pharmacist or run over by a car while fleeing from police pursuit.",
  "question": "Which emotion does this movie subtitle line express?",
  "options": [
   "anger",
   "anticipation",
   "disgust",
   "fear",
   "joy",
   "sadness",
   "surprise",
   "trust"
  ],
  "definitions": "- anger: The speaker shows annoyance, rage, hostility or irritation toward someone or something, for example through insults, threats, shouting or aggressive demands.\n- anticipation: The speaker looks ahead to something expected: interest, eagerness, planning, curiosity, vigilance or expectation about what will or should happen next, without fear about it.\n- disgust: The speaker shows revulsion, contempt, loathing, disdain or weary boredom toward something seen as gross, offensive, distasteful, worthless or morally repugnant.\n- fear: The speaker shows fright, worry, anxiety, alarm or a sense of threat or danger to themselves or others.\n- joy: The speaker shows happiness, delight, serenity, amusement, pleasure, pride or excitement about something good that is happening or has happened.\n- sadness: The speaker shows sorrow, grief, disappointment, regret, loneliness, hurt or pensiveness about a loss or something bad.\n- surprise: The speaker reacts to something unexpected or just discovered with amazement, astonishment, shock, disbelief or sudden realisation, often as an exclamation or incredulous question.\n- trust: The speaker shows acceptance, agreement, confidence, reliance, reassurance, admiration or faith in someone or something, for example making a deal, a promise or a vouching remark."
 },
 {
  "qid": "q23c26afb12",
  "kind": "yes/no",
  "text": "overwhelmed new grandparents finally feeling what it like to love a child",
  "question": "Is this news headline sarcastic?",
  "definitions": "- yes: The headline is satirical parody news: it presents an invented, exaggerated or absurd event as if it were real reporting, to mock a public figure, current event or everyday situation. The tone is often deadpan, treating something trivial as news or stating an absurdity matter-of-factly.\n- no: The headline is a genuine news, opinion or feature headline about real events, people or content. It may be witty, punning, emotional or opinionated, or quote someone else's sarcasm, but it is not itself made-up satire."
 },
 {
  "qid": "q7d66e2f12e",
  "kind": "choice",
  "text": "Hereditary hemochromatosis (HH) is a common <e>autosomal recessive disorder</e> characterized by tissue iron deposition secondary to excessive dietary iron absorption.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"autosomal recessive disorder\" (marked <e>) in this sentence?",
  "options": [
   "Class E",
   "Class A",
   "Class U",
   "Class L"
  ],
  "definitions": "- Class E: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- Class A: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- Class U: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- Class L: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers')."
 },
 {
  "qid": "q63a0651579",
  "kind": "yes/no",
  "text": "Problem:\nGiven that\n$\\frac 1{2!17!}+\\frac 1{3!16!}+\\frac 1{4!15!}+\\frac 1{5!14!}+\\frac 1{6!13!}+\\frac 1{7!12!}+\\frac 1{8!11!}+\\frac 1{9!10!}=\\frac N{1!18!}$\nfind the greatest integer that is less than $\\frac N{100}$.\n\nSolution steps so far:\nStep 1: I notice that the denominators of the fractions on the left-hand side are all of the form $k!(19-k)!$, where $k$ ranges from $2$ to $9$.\n\nLast step (Step 2):\nI also notice that the denominator of the fraction on the right-hand side is $1!18!$, which is exactly $19!$.",
  "question": "Does the last step of this partial solution contain a mistake or other flaw that makes it a bad step?",
  "definitions": "- yes: The last step is a bad step: it states something mathematically wrong (even if most of it is right), cannot be checked in about 30 seconds, is off-topic or gibberish, leads into an obvious dead end or loop, or gives a final answer that is wrong or not justified by a complete solution.\n- no: The last step has no such flaw: everything it states is correct, quickly verifiable and fits the earlier steps; this includes steps that only restate, stall or try a reasonable approach that may not pan out, and steps that catch an earlier slip."
 },
 {
  "qid": "qfa76925910",
  "kind": "choice",
  "text": "I love seeing the <e>U.S. Capitol building</e> in my rearview mirror when I'm driving home from work. #ILoveDC",
  "question": "What type of named entity is \"U.S. Capitol building\" (marked <e>) in this post?",
  "options": [
   "person",
   "group",
   "location",
   "corporation",
   "creative work",
   "product"
  ],
  "definitions": "- person: A named individual person, real or fictional, including first names, nicknames and stage names (e.g. 'Rashad', 'Kanye', 'Harry Potter'); not a band or team.\n- group: A named group of people that is not a company: band, sports team, political party, government agency, club, charity or other organisation (e.g. 'Nirvana', 'San Diego Padres', 'FDA').\n- location: A named place: country, city, region, street, venue, building, landmark or geographic feature (e.g. 'London', 'Empire State Building').\n- corporation: A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant.\n- creative work: The title of a creative work: song, album, film, TV show, book, artwork or play (e.g. 'Game of Thrones', 'Thriller'); video games count as product.\n- product: A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation."
 },
 {
  "qid": "q6f43fd64d5",
  "kind": "yes/no",
  "text": "Situation: They gave in to my desire and ordered the food.\nAction being judged: Ordering someone their favorite food.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q6921cd3ef3",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Fairport Convention\nAlso known as: Fairport (1976), Fairport Featuring Dave Swarbrick (1976) (US)\nOrigin: London, England\nGenres: Folk, British folk rock, folk rock\nYears active: 1967-79, 1985-present\nLabels: Polydor, Island, A&amp;M, Vertigo, Rough Trade, Transatlantic, Woodworm, Matty Grooves\nAssociated acts: Fotheringay, Trader Horne, Steeleye Span, Giles, Giles and Fripp, The Albion Band, Jethro Tull\nWebsite: fairportconvention.com\n\nHypothesis: Fairport Convention has been a band for more than 45 years total.",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely true?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- no: The hypothesis is not established: either the infobox shows it is false, or it adds details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "qdd6e491a6b",
  "kind": "yes/no",
  "text": "Occupation: Motorboat Operators\nDuties:\n- Clean boats and repair hulls and superstructures, using hand tools, paint, and brushes.\n- Maintain desired courses, using compasses or electronic navigational aids.\n- Oversee operation of vessels used for carrying passengers, motor vehicles, or goods across rivers, harbors, lakes, and coastal waters.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q37d69a0ac2",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Katherine Waterston\nBorn: March 3, 1980 (age 38) Westminster, London, England\nBirth name: Katherine Boyer Waterston\nResidence: New York City, U.S.\nAlma mater: New York University\nOccupation: Actress\nYears active: 2004-present\nHeight: 5 ft 11 in (180 cm)\nParent(s): Lynn Louisa Woodruff, Sam Waterston\nRelatives: James Waterston (paternal half-brother)\n\nHypothesis: Katherine Waterston's acting work has mostly been on television.",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely false?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- no: The hypothesis is not shown to be false: either the infobox confirms it, or it concerns details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "qce74420ba9",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Ignacy Moscicki\nIn office: 4 June 1926 - 30 September 1939\nPrime Minister: Kazimierz Bartel, Jozef Pilsudski, Kazimierz Bartel, Kazimierz Switalski, Kazimierz Bartel, Walery Slawek, Jozef Pilsudski, Walery Slawek, Aleksander Prystor, Janusz Jedrzejewicz, Leon Kozlowski, Walery Slawek, Marian Zyndram-Koscialkowski, Felicjan Slawoj Skladkowski\nPreceded by: Stanis;aw Wojciechowski\nSucceeded by: Wladyslaw Raczkiewicz (President of the Polish Republic in Exile)\n\nHypothesis: Ignacy Mo_cicki was in goverment",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely true?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- no: The hypothesis is not established: either the infobox shows it is false, or it adds details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "qbfef248a60",
  "kind": "yes/no",
  "text": "Situation: So they both got dressed in their nice clothes.\nAction being judged: Putting on nice clothes when attending a fancy party.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q5c046aad76",
  "kind": "yes/no",
  "text": "Situation: Mom Wants To End Daughter's Sleepovers With Her Boyfriend\nAction being judged: Getting involved in another's relationship.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q443a7be0a7",
  "kind": "yes/no",
  "text": "Customer: Are you sure?  A 0 star HOTEL in the west side of time. Please check again.\nAssistant: No hotels or guesthouse in the west, can I try an alternate search?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q41f5239ee5",
  "kind": "choice",
  "text": "Beginning: I enjoyed the movie big time. I ...\n\nPossible endings:\n(A) want to watch it again.\n(B) want the big one.\n(C) want more time to watch.\n(D) need more time.",
  "question": "Which listed ending continues the beginning most sensibly?",
  "options": [
   "A",
   "B",
   "C",
   "D"
  ],
  "definitions": "- A: Ending (A) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- B: Ending (B) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- C: Ending (C) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- D: Ending (D) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning."
 },
 {
  "qid": "q9be70f80a0",
  "kind": "yes/no",
  "text": "The man was going to transfer his plant into a different pot but the _ was too small.\n\nThe blank (_) stands for one of two candidates: \"plant\" or \"pot\".",
  "question": "Does the blank (_) in the sentence stand for \"pot\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q7204a7bcee",
  "kind": "yes/no",
  "text": "Customer: Hi I wanted to check on my shipping status because I never got my package\nCustomer: My name is Joseph Banter\nCustomer: No I never got an email, it was just supposed to arrive 5 days ago and I've been waiting for it ever since",
  "question": "Which specific customer-service request does the customer have?\nIs the correct answer \"billed for returned item\"?",
  "definitions": "- billed for returned item: The customer was billed for an item they already returned and has not received the credit for it; a billing complaint, not a new refund.\n- item never arrived: The customer did not receive an item they ordered and wants to know what happened to it.\n- change shipment details: The customer wants to change something about a shipment in progress, such as the delivery address or the item because they ordered the wrong one.\n- change account payment method: The customer wants to update, add or replace the payment method saved on their account.\n- boots product question: The customer asks a general question about boots, such as stain or gum removal, width, break-in time, waterproofing, laces, sizes in stock or warranty.\n- jacket product question: The customer asks a general question about jackets, such as stain removal, washing or dry cleaning, arm length, detaching the hood, shrinking, stock, material or warmth."
 },
 {
  "qid": "q505cd250cf",
  "kind": "yes/no",
  "text": "A 55-year-old man comes to the physician because of worsening fatigue and recurrent bleeding from his gums for 2 weeks. Physical examination shows marked pallor. There are scattered red, nonblanching pinpoints spots on his trunk and extremities. Laboratory studies show a hemoglobin of 8.0 g/dL, a leukocyte count of 80,000/mm3, and a platelet count of 104,000/mm3. Genetic analysis of a bone marrow aspirate shows leukemic cells with a balanced translocation between the long arms of chromosome 15 and 17. These cells are most likely to stain positive for which of the following?\n\nAnswer choices:\nA. Myeloperoxidase\nB. Tartrate resistant acid phosphatase\nC. Periodic acid-Schiff\nD. Cluster of differentiation 1a\nE. Terminal deoxynucleotidyl transferase\n\nProposed answer: A. Myeloperoxidase",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "qbf7edb6b49",
  "kind": "choice",
  "text": "Heading: Coral, Cucumber and Carnivorous Plants conundrum\nWhy are coral and sea cucumbers considered animals while carnivorous plants such as the Venus fly trap are considered plants? Could you break down the determining criteria and explain how it applies to these examples.",
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
  "qid": "q4a5542dc97",
  "kind": "yes/no",
  "text": "Wikipedia page: Office of National Drug Control Policy\nTable (first row is the header):\n| No. | Name | Term of Office | President(s) served under |\n| 1 | William Bennett | 1989 – 1991 | George H. W. Bush |\n| 2 | Bob Martinez | March 28, 1991 - January 20, 1993 | George H. W. Bush |\n| 3 | Lee P. Brown | January 1993 – December 12, 1995 | Bill Clinton |\n| 4 | Barry McCaffrey | February 29, 1996 – January 4, 2001 | Bill Clinton |\n| 5 | John P. Walters | December 7, 2001 – January 19, 2009 | George W. Bush |\n| 6 | Gil Kerlikowske | May 7, 2009 – March 6, 2014 | Barack Obama |\n| Acting | Michael Botticelli | March 6, 2014 – | Barack Obama |\n\nQuestion: what were the number of directors that stayed in office more than three years?\nProposed answer: 3",
  "question": "Based only on the table, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer is exactly what the table gives for this question: the right cell, count or value, and when the question asks for several items, all of them and nothing else.\n- no: The proposed answer is not what the table gives: a different cell or value (for example a neighbouring row's entry), a count or number that is off, the opposite yes/no, or a list that misses or adds an item."
 },
 {
  "qid": "qdc52a0cf5f",
  "kind": "yes/no",
  "text": "Customer: Yes, are there any British places to eat at in the same area?\nAssistant: Yes, there are 7 of them. How about restaurant one seven?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qf54273d62e",
  "kind": "yes/no",
  "text": "EMPLOYEE ALLEGES THAT WHILE HE WAS DUMPING WHEEL BARROW FILL OF CEMENT DUST, HE STRAINED HIS LOWER BACK. NOTE: EE IS CURRENTLY ON LIMITED DUTY AND HE STARTED PT ON 8/1/01.",
  "question": "Which MSHA accident classification fits the circumstances that most directly caused this mine accident?\nIs the correct answer \"non-powered haulage\"?",
  "definitions": "- non-powered haulage: Injury involving hand-moved haulage such as wheelbarrows, hand carts, dollies or pallet jacks.\n- ignition or explosion of gas or dust: Ignition or explosion of methane or another gas, or of coal or other dust.\n- machinery: Injury from the action of machinery other than haulage or hoisting equipment: roof bolters, continuous miners, drills, crushers, pumps, powered hand tools and welders, including their repair.\n- explosives and breaking agents: Accidents with blasting or breaking agents: detonations, premature or misfired shots, flyrock from a blast, or handling explosives.\n- powered haulage: Accidents involving motorized haulage or conveying: haul, dump and service trucks, shuttle cars, scoops, locomotives, mantrips, mine cars and belt conveyors."
 },
 {
  "qid": "q00ef84909b",
  "kind": "yes/no",
  "text": "The vest suited the dog on the hot summer day unlike the shirt because the _ was closed in.\n\nThe blank (_) stands for one of two candidates: \"vest\" or \"shirt\".",
  "question": "Does the blank (_) in the sentence stand for \"shirt\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q454d240a66",
  "kind": "yes/no",
  "text": ">muh high IQ and creativity   >invests in a shekel grabbing operation by a turk and south indian street shitter    Good job, Alt-right. You're a bunch of weak fags who are easily duped",
  "question": "Which type of group does this post's hateful rhetoric mainly target?\nIs the correct answer \"sexual orientation\"?",
  "definitions": "- sexual orientation: The hateful rhetoric mainly targets people for their sexual orientation, for example gay, lesbian or bisexual people.\n- ideology: The hateful rhetoric mainly targets people for their ideology or worldview, such as liberals, leftists, conservatives or the right wing as a camp of believers, not as members of a party.\n- religion: The hateful rhetoric mainly targets people for their religion or spiritual beliefs, for example anti-Muslim or anti-Christian attacks on believers or the faith.\n- race or ethnicity: The hateful rhetoric mainly targets people for their race or ethnicity, for example anti-Black, anti-Asian, anti-Latino, anti-Arab or antisemitic attacks on Jews as a people (the manual codes antisemitism here).\n- health or disability: The hateful rhetoric mainly targets people for their mental or physical health status, mental illness or a physical disability.\n- political affiliation: The hateful rhetoric mainly targets people for membership of a political organisation or party, such as Democrats or Republicans, or a named party's members or politicians."
 },
 {
  "qid": "qf9e7fa3647",
  "kind": "choice",
  "text": "Premise:\nTitle: Juan Trippe\nBorn: Juan Terry Trippe , (1899-06-27)June 27, 1899 , Sea Bright, New Jersey, U.S.\nDied: April 3, 1981(1981-04-03) (aged 81) , New York City, U.S.\nResting place: Green-Wood Cemetery\nNationality: American\nAlma mater: Yale University\nOccupation: Airline entrepreneur\nSpouse(s): Elizabeth 'Betty' Stettinius ( m. 1928)\nChildren: 4\nRelatives: John Trippe (great-great-grandfather)\nHypothesis: Juan Trippe lived in New Jersey for 34 years.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "qc2c012e7c4",
  "kind": "choice",
  "text": "Personally I would not put 1700 dollars into a car that's worth maybe a grand. That is just crazy. Keep saving your money and drive the Honda until it is no longer safe to do so or the tranny blows, whichever comes first.",
  "question": "How is the potential slur in this comment used?",
  "options": [
   "derogatory",
   "mention without contempt",
   "reclaimed by the targeted group",
   "different meaning"
  ],
  "definitions": "- derogatory: The slur conveys contempt toward a targeted person or group: insults, labels, stand-alone slurs, sexualised use, generalisations about the community, or self-deprecation.\n- mention without contempt: The slur is mentioned rather than aimed at anyone - quoted, discussed as a word, recalled from an incident, used in counter-speech, or in sarcasm that mocks bigotry - by a speaker who is not reclaiming it.\n- reclaimed by the targeted group: A member of the targeted group uses the slur with positive or neutral force about themselves or their community (empowerment, in-group solidarity, humour).\n- different meaning: The word is used in a non-slur sense, such as 'fag' meaning a cigarette or 'tranny' meaning a vehicle transmission."
 },
 {
  "qid": "q2fcaec879f",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Event Horizon\nDirected by: Paul W. S. Anderson\nProduced by: Lawrence Gordon, Lloyd Levin, Jeremy Bolt\nWritten by: Philip Eisner\nStarring: Laurence Fishburne, Sam Neill, Kathleen Quinlan, Joely Richardson\nMusic by: Michael Kamen, Orbital\nCinematography: Adrian Biddle\nEdited by: Martin Hunter\nProduction company: Paramount Pictures, Golar Productions, Impact Pictures\nDistributed by: Paramount Pictures\nRelease date: 15 August 1997 ( 1997-08-15 ) (United States), 22 August 1997 ( 1997-08-22 ) (United Kingdom)\nRunning time: 96 minutes\nCountry: United Kingdom United States\nLanguage: English\nBudget: $60 million\nBox office: $26.7 million (US)\n\nHypothesis: Event Horizon was released in the US earlier than in the UK.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?\nIs the correct answer \"Entailment\"?",
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles)."
 },
 {
  "qid": "q006577f34d",
  "kind": "yes/no",
  "text": "All actual data indicate that if there is an underlying trend beneath the noise of the weather data, it is currently less (and probably much less) than 1 C per century, i.e. certainly much less than 0.5 C in a \"few decades\".",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q5c9eff2b3f",
  "kind": "yes/no",
  "text": "At the harvest party, Randy got through the maze slower than Joseph because _ is better at figuring out puzzles.\n\nThe blank (_) stands for one of two candidates: \"Randy\" or \"Joseph\".",
  "question": "Does the blank (_) in the sentence stand for \"Randy\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q6ce7b0de1a",
  "kind": "yes/no",
  "text": "Customer: December 30th till January 1st.\nAssistant: Okay, do you have a price range?\nCustomer: Less than $250 a night.",
  "question": "In the customer's last message, is \"Less than $250 a night\" a mention of the hotel star rating for this hotel search?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out (e.g. 'not horror' still mentions a genre).\n- no: The quoted phrase refers to a different detail of the search (e.g. the destination rather than the departure city, the return rather than the outbound date, or the meal rather than the cuisine)."
 },
 {
  "qid": "q9a19b3f561",
  "kind": "yes/no",
  "text": "Cut lace on belt splice of conveyor. Box knife slipped and cut left forearm",
  "question": "Which part of the body was injured in this mine accident report?\nIs it wrong to answer \"chest (ribs, breastbone, chest organs)\"?",
  "definitions": "- chest (ribs, breastbone, chest organs): The chest, including the ribs, breastbone and chest organs.\n- forearm (ulna, radius): The arm between the elbow and the wrist, including the ulna and radius.\n- upper extremities, multiple parts: Parts of both arms or hands, or several different arm and hand parts.\n- brain: The brain itself, such as a concussion or other brain injury named as such.\n- wrist: The wrist joint.\n- foot (not ankle or toes): The foot itself (heel, arch, instep, metatarsals), not the ankle or toes."
 },
 {
  "qid": "qb0860cf7a5",
  "kind": "yes/no",
  "text": "Situation: After listening to it in my head for an hour, I gave up and got up.\nAction being judged: Giving up on something you want to do.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q42e6204d99",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n|  | Group |  |\n|  | 2019 | 2018 |\n|  | S$ Mil | S$ Mil |\n| Cost of equipment sold (1) | 3,106.1 | 2,696.7 |\n| Other cost of sales | 2,767.1 | 2,499.2 |\n| Staff costs | 2,597.3 | 2,760.1 |\n| Selling and administrative costs (2) | 2,472.6 | 2,536.6 |\n| Traffic expenses | 1,573.4 | 1,615.8 |\n| Repair and maintenance | 388.0 | 367.9 |\n|  | 12,904.5 | 12,476.3 |\nText:\n5. Operating Expenses\nNotes: (1) Includes equipment costs related to ICT services.\n(2) Includes supplies and services, as well as rentals of properties and mobile base stations.\n\nHypothetical question: In which year did Singtel had higher total operating expenses, if cost of equipment sold was S$3,000.0 in 2018?\nProposed answer: 2018",
  "question": "Using the report's table and text together with the question's hypothetical assumption, is the proposed answer correct?",
  "definitions": "- yes: The proposed answer is what the figures give after applying the question's hypothetical change (the assumed value replaces the reported one): same value at the precision shown, same sign, same unit or scale, and for lists exactly the right items.\n- no: The proposed answer is not the hypothetical result: it ignores the assumption and uses the reported figure, uses a wrong figure or base, sums instead of averaging, has the wrong sign or scale, or lists the wrong items."
 },
 {
  "qid": "q38b6d2fb16",
  "kind": "choice",
  "text": "Beginning: A man is walking across the green toward his golf ball. He ...\n\nPossible endings:\n(A) draws a diagram showing how the system will perform when deployed.\n(B) throws the frisbee to his partner.\n(C) squats down and tries to gauge the break on his putt.\n(D) lays down on the green and tries to get some sleep.",
  "question": "Which listed ending continues the beginning most sensibly?",
  "options": [
   "A",
   "B",
   "C",
   "D"
  ],
  "definitions": "- A: Ending (A) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- B: Ending (B) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- C: Ending (C) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- D: Ending (D) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning."
 },
 {
  "qid": "qc1740c99c6",
  "kind": "yes/no",
  "text": "Statement 1: monkeys hang out on tree tops\nStatement 2: monkeys hang out on the sea",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q044bb9b2fc",
  "kind": "yes/no",
  "text": "The document was given to Nelson to work on and not Kenneth because _ had more experience.\n\nThe blank (_) stands for one of two candidates: \"Nelson\" or \"Kenneth\".",
  "question": "Does the blank (_) in the sentence stand for \"Nelson\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q1e96671b98",
  "kind": "choice",
  "text": "After all, conservation begins with saving those at-risk places -— our forests and deserts, wetlands and oceans, mangroves and coral reefs — that provide a lifeline for precious animals and plants.",
  "question": "Does this text convey a sense of being controlled or of being in control?",
  "options": [
   "controlled",
   "in control"
  ],
  "definitions": "- controlled: The text conveys being controlled, influenced, guided, submissive, awed, overwhelmed or powerless: other people, events or circumstances are in charge rather than the writer or subject.\n- in control: The text conveys being in control, influential, important, dominant, confident or autonomous: the writer or subject acts, decides or masters the situation rather than being subject to it."
 },
 {
  "qid": "q678d94139c",
  "kind": "yes/no",
  "text": "EE alleged carpal tunnel. EE treated with conservative care. Dr recommended surgery on cubital tunnel syndrome with ular nerve. Surgery is scheduled for 2.6.15, EE will return on restrictive duty following surgery.",
  "question": "What is the nature of the injury described in this mine accident report?\nIs it wrong to answer \"Option J\"?",
  "definitions": "- Option J: Inflammation or irritation of joints, tendons or muscles: tendonitis, bursitis, epicondylitis, synovitis, trigger finger or carpal tunnel syndrome.\n- Option N: An electric shock or electrocution without a named electrical burn.\n- Option L: Sunburn.\n- Option F: A sprain or strain of muscles, tendons or ligaments, including a pulled muscle or herniated / ruptured spinal disc.\n- Option X: A contagious or infectious disease contracted at work."
 },
 {
  "qid": "qe7bfe0e27c",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Doshirak\nProduct type: Ramyeon\nProduced by: Paldo\nCountry: South Korea\nIntroduced: 1986\nWebsite: Official website\n\nHypothesis: The country origin is USA",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely false?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- no: The hypothesis is not shown to be false: either the infobox confirms it, or it concerns details the infobox does not cover, so it may or may not be true."
 }
]
